const fs = require("fs");
const path = require("path");
const Module = require("module");

const NODE_MODULES =
  "C:\\Users\\hayaa\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules";
process.env.NODE_PATH = [
  NODE_MODULES,
  path.join(NODE_MODULES, ".pnpm", "node_modules"),
].join(path.delimiter);
Module._initPaths();

const sharp = require("sharp");
const Tesseract = require("tesseract.js");

const ROOT = __dirname;
const FOLDER_ID = "1TFLtC3N5WjVCb4kD7Ecqb-fR03j8KxHL";
const FOLDER_URL = `https://drive.google.com/drive/folders/${FOLDER_ID}?usp=sharing`;
const IMAGES_DIR = path.join(ROOT, "images");
const OCR_DIR = path.join(ROOT, "ocr");
const TESSDATA_DIR = path.join(ROOT, "tessdata");
const REPORT_PATH = path.join(ROOT, "job-leads-extraction.md");
const JSON_PATH = path.join(ROOT, "job-leads-extraction.json");
const MANIFEST_PATH = path.join(ROOT, "manifest.json");
const FULL_MANIFEST_PATH = path.join(ROOT, "full-manifest.json");
const FOLDER_HTML_PATH = path.join(ROOT, "folder.html");

const TESSERACT_WORKER = path.join(NODE_MODULES, "tesseract.js", "dist", "worker.min.js");
const TESSERACT_CORE = path.join(
  NODE_MODULES,
  ".pnpm",
  "node_modules",
  "tesseract.js-core",
  "tesseract-core.wasm.js",
);

function ensureDirs() {
  for (const dir of [ROOT, IMAGES_DIR, OCR_DIR, TESSDATA_DIR]) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function decodeHtml(value) {
  return value
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

async function fetchText(url) {
  const res = await fetch(url, {
    headers: {
      "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
    },
  });
  if (!res.ok) throw new Error(`GET ${url} failed: ${res.status} ${res.statusText}`);
  return res.text();
}

async function fetchBuffer(url) {
  const res = await fetch(url, {
    headers: {
      "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
    },
  });
  if (!res.ok) throw new Error(`GET ${url} failed: ${res.status} ${res.statusText}`);
  return Buffer.from(await res.arrayBuffer());
}

async function loadFolderHtml() {
  const html = await fetchText(FOLDER_URL);
  fs.writeFileSync(FOLDER_HTML_PATH, html, "utf8");
  return html;
}

function parseManifest(html) {
  const files = new Map();
  const patterns = [
    /<tr[\s\S]*?data-id="([^"]+)"[\s\S]*?data-tooltip="(IMG_[^"]+\.(?:HEIC|PNG)) Image"[\s\S]*?<\/tr>/g,
    /data-id="([^"]+)"[^>]*data-tooltip="(IMG_[^"]+\.(?:HEIC|PNG)) Image"/g,
    /\[\[null,"([^"]+)"\][\s\S]{0,700}?\[\[\["(IMG_[^"]+\.(?:HEIC|PNG))"/g,
  ];

  for (const re of patterns) {
    let match;
    while ((match = re.exec(html))) {
      const id = decodeHtml(match[1]);
      const title = decodeHtml(match[2]);
      if (!files.has(id)) files.set(id, { id, title });
    }
  }

  return [...files.values()].sort((a, b) => {
    const an = Number((a.title.match(/IMG_(\d+)/) || [])[1] || 0);
    const bn = Number((b.title.match(/IMG_(\d+)/) || [])[1] || 0);
    return an - bn || a.title.localeCompare(b.title);
  });
}

function safeBase(title) {
  return title.replace(/[^a-zA-Z0-9._-]/g, "_").replace(/\.(HEIC|PNG)$/i, "");
}

async function downloadImage(file) {
  const out = path.join(IMAGES_DIR, `${safeBase(file.title)}.jpg`);
  if (fs.existsSync(out) && fs.statSync(out).size > 10000) return out;

  const url = `https://drive.google.com/thumbnail?id=${encodeURIComponent(file.id)}&sz=w3000`;
  const buf = await fetchBuffer(url);
  if (buf.slice(0, 20).toString("utf8").includes("<!DOCTYPE")) {
    throw new Error(`Thumbnail download returned HTML for ${file.title}`);
  }
  fs.writeFileSync(out, buf);
  return out;
}

async function preprocessForOcr(imagePath) {
  return sharp(imagePath)
    .rotate()
    .grayscale()
    .normalize()
    .sharpen()
    .resize({ width: 2200, withoutEnlargement: false })
    .png()
    .toBuffer();
}

function cleanText(text) {
  return text
    .replace(/\r/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function extractEntities(text) {
  const stitchedText = text.replace(/(https?:\/\/\S+)\s*\n\s*([A-Za-z0-9?&=/_#.-]+)/g, "$1$2");
  const emails = [...new Set(text.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi) || [])];
  const urls = [
    ...new Set(
      stitchedText.match(
        /(?:https?:\/\/|www\.|forms\.gle\/|docs\.google\.com\/forms|bit\.ly\/|linkedin\.com\/|wa\.me\/)[^\s<>"']+/gi,
      ) || [],
    ),
  ].map((u) => u.replace(/[),.;]+$/, ""));
  const phoneCandidates =
    text.match(
      /(?:(?:WhatsApp|Whatsapp|WA|Call|Phone|Mobile|Tel|Contact)[:\s-]*)?(?:\+?\d[\d\s().-]{7,}\d)/gi,
    ) || [];
  const phones = [
    ...new Set(
      phoneCandidates
        .map((phone) => phone.replace(/\s+/g, " ").trim())
        .filter((phone) => {
          const digits = phone.replace(/\D/g, "");
          return digits.length >= 10 && (digits.length <= 15 || /whatsapp|call|phone|mobile|tel|contact/i.test(phone));
        }),
    ),
  ];
  return { emails, urls, phones };
}

function inferLocations(text) {
  const locationWords = [
    "Dubai",
    "Abu Dhabi",
    "Sharjah",
    "Ajman",
    "UAE",
    "Saudi",
    "KSA",
    "Riyadh",
    "Jeddah",
    "Qatar",
    "Doha",
    "Kuwait",
    "Bahrain",
    "Oman",
    "India",
    "Mumbai",
    "Bangalore",
    "Bengaluru",
    "Hyderabad",
    "Delhi",
    "Pune",
    "Chennai",
    "Germany",
    "Berlin",
    "Munich",
    "Netherlands",
    "Amsterdam",
    "UK",
    "London",
    "USA",
    "Remote",
    "Hybrid",
  ];
  return locationWords.filter((word) => new RegExp(`\\b${word.replace(/\s+/g, "\\s+")}\\b`, "i").test(text));
}

function trackerBucket(record) {
  const text = `${record.locations.join(" ")} ${record.text}`.toLowerCase();
  if (/\b(dubai|abu dhabi|sharjah|ajman|uae|united arab emirates)\b/.test(text)) return "UAE / Dubai";
  if (/\b(saudi|ksa|riyadh|jeddah)\b/.test(text)) return "Saudi Arabia";
  if (/\b(india|mumbai|bangalore|bengaluru|hyderabad|delhi|pune|chennai|ncr)\b/.test(text)) return "India";
  if (/\b(germany|berlin|munich|walldorf|herzogenaurach)\b/.test(text)) return "Germany";
  if (/\b(netherlands|amsterdam)\b/.test(text)) return "Netherlands";
  if (/\b(uk|london|united kingdom)\b/.test(text)) return "United Kingdom";
  if (/\b(qatar|doha)\b/.test(text)) return "Qatar";
  if (/\b(kuwait)\b/.test(text)) return "Kuwait";
  if (/\b(bahrain)\b/.test(text)) return "Bahrain";
  if (/\b(oman)\b/.test(text)) return "Oman";
  if (/\b(remote|work-from-home|work from home|wfh)\b/.test(text)) return "Remote / unclear country";
  return "Unknown / needs review";
}

function extractCompanyRows(text) {
  const seen = new Set();
  const rows = [];
  for (const line of text.split("\n")) {
    const cleaned = line.replace(/^[\sâ€¢*.-]+/, "").trim();
    const match = cleaned.match(/^(.{2,80}?)\s*\|\s*([A-Za-z][A-Za-z\s.-]{2,50})$/);
    if (!match) continue;
    const company = match[1].replace(/\s+/g, " ").trim();
    const location = match[2].replace(/\s+/g, " ").trim();
    const key = `${company}|${location}`.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    rows.push({ company, location });
  }
  return rows.slice(0, 100);
}

function inferKind(text) {
  if (/\b(recruitment|recruiter|agency|manpower|consultancy|staffing|talent acquisition)\b/i.test(text)) {
    return "Agency / recruiter";
  }
  if (/\b(hiring|vacancy|opening|job|role|apply|career|position)\b/i.test(text)) {
    return "Job lead / direct employer";
  }
  if (/\b(companies|company list|hiring companies)\b/i.test(text)) {
    return "Company list";
  }
  return "Unclassified lead";
}

function extractCandidateLines(text) {
  return text
    .split("\n")
    .map((line) => line.replace(/^[\s•*.-]+/, "").trim())
    .filter(Boolean)
    .filter((line) => {
      if (line.length < 4) return false;
      if (/^(message|camera|image|sort|download|shared|modified|size|storage used)$/i.test(line)) return false;
      return /(@|https?:\/\/|forms\.gle|www\.|\|\s*[A-Z]|Dubai|UAE|Saudi|India|Hiring|Companies|Recruit|Apply|Job|Vacancy|Opening|Role)/i.test(
        line,
      );
    })
    .slice(0, 80);
}

function buildMarkdown(records) {
  const generated = new Date().toISOString();
  const allEmails = [...new Set(records.flatMap((r) => r.entities.emails))].sort();
  const allUrls = [...new Set(records.flatMap((r) => r.entities.urls))].sort();
  const allPhones = [...new Set(records.flatMap((r) => r.entities.phones))].sort();
  const byLocation = new Map();
  const byBucket = new Map();

  for (const r of records) {
    const key = r.locations.length ? r.locations.join(", ") : "Unknown / not visible";
    if (!byLocation.has(key)) byLocation.set(key, []);
    byLocation.get(key).push(r);

    const bucket = trackerBucket(r);
    if (!byBucket.has(bucket)) byBucket.set(bucket, []);
    byBucket.get(bucket).push(r);
  }

  const lines = [];
  lines.push("# Job Leads Extraction");
  lines.push("");
  lines.push(`Source folder: ${FOLDER_URL}`);
  lines.push(`Generated: ${generated}`);
  lines.push(`Images processed: ${records.length}`);
  lines.push("");
  lines.push("## Quick Counts");
  lines.push("");
  lines.push(`- Unique emails: ${allEmails.length}`);
  lines.push(`- Unique links/forms: ${allUrls.length}`);
  lines.push(`- Unique phone-like values: ${allPhones.length}`);
  lines.push("");

  lines.push("## Review Checklist");
  lines.push("");
  lines.push("- Use the grouped sections below to review by location.");
  lines.push("- Use the suggested tracker bucket first, then confirm the original screenshot before adding it to the sheet.");
  lines.push("- Use the per-image raw OCR files when a line looks unclear.");
  lines.push("- Treat low-confidence OCR rows as review-needed before adding them to the tracker.");
  lines.push("");

  lines.push("## Suggested Tracker Buckets");
  lines.push("");
  lines.push("| Bucket | Images | Suggested use |");
  lines.push("|---|---:|---|");
  [...byBucket.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([bucket, items]) => {
      const suggestedUse =
        bucket === "UAE / Dubai"
          ? "Review for agencies vs direct employers in the Dubai/UAE tracker."
          : bucket === "Unknown / needs review"
            ? "Open image/raw OCR before deciding country or tracker table."
            : "Create or append to the outside-Dubai country table.";
      lines.push(`| ${bucket} | ${items.length} | ${suggestedUse} |`);
    });
  lines.push("");

  if (allEmails.length) {
    lines.push("## Emails Found");
    lines.push("");
    allEmails.forEach((email) => lines.push(`- ${email}`));
    lines.push("");
  }

  if (allUrls.length) {
    lines.push("## Links And Forms Found");
    lines.push("");
    allUrls.forEach((url) => lines.push(`- ${url}`));
    lines.push("");
  }

  if (allPhones.length) {
    lines.push("## Phone / WhatsApp Values Found");
    lines.push("");
    allPhones.forEach((phone) => lines.push(`- ${phone}`));
    lines.push("");
  }

  lines.push("## Grouped By Tracker Bucket");
  lines.push("");
  [...byBucket.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([bucket, items]) => {
      lines.push(`### ${bucket}`);
      lines.push("");
      for (const r of items) {
        lines.push(`#### ${r.title}`);
        lines.push("");
        lines.push(`- Type: ${r.kind}`);
        lines.push(`- Detected locations: ${r.locations.join(", ") || "Unknown / not visible"}`);
        lines.push(`- OCR confidence: ${Math.round(r.confidence || 0)}`);
        lines.push(`- Drive file: https://drive.google.com/file/d/${r.id}/view`);
        lines.push(`- Local image: images/${path.basename(r.imagePath)}`);
        lines.push(`- Raw OCR: ocr/${path.basename(r.ocrPath)}`);
        if (r.entities.emails.length) lines.push(`- Emails: ${r.entities.emails.join("; ")}`);
        if (r.entities.urls.length) lines.push(`- Links/forms: ${r.entities.urls.join("; ")}`);
        if (r.entities.phones.length) lines.push(`- Phones: ${r.entities.phones.join("; ")}`);
        if (r.companyRows.length) {
          lines.push("");
          lines.push("Company/location rows:");
          for (const row of r.companyRows.slice(0, 30)) lines.push(`- ${row.company} | ${row.location}`);
        }
        if (r.candidateLines.length) {
          lines.push("");
          lines.push("Key lines:");
          for (const line of r.candidateLines.slice(0, 30)) lines.push(`- ${line}`);
        }
        lines.push("");
      }
    });

  lines.push("## Image Index");
  lines.push("");
  lines.push("| # | Image | Type | Locations | Emails | Links | Confidence |");
  lines.push("|---:|---|---|---|---:|---:|---:|");
  records.forEach((r, i) => {
    lines.push(
      `| ${i + 1} | ${r.title} | ${r.kind} | ${trackerBucket(r)}; ${r.locations.join(", ") || "Unknown"} | ${r.entities.emails.length} | ${r.entities.urls.length} | ${Math.round(r.confidence || 0)} |`,
    );
  });
  lines.push("");

  return `${lines.join("\n")}\n`;
}

async function createOcrWorker() {
  const worker = await Tesseract.createWorker("eng", 1, {
    corePath: TESSERACT_CORE,
    langPath: TESSDATA_DIR,
    cachePath: TESSDATA_DIR,
    gzip: true,
    logger: () => {},
  });
  await worker.setParameters({
    tessedit_pageseg_mode: "6",
    preserve_interword_spaces: "1",
  });
  return worker;
}

async function main() {
  ensureDirs();

  if (!fs.existsSync(path.join(TESSDATA_DIR, "eng.traineddata.gz"))) {
    throw new Error(
      `Missing OCR language data: ${path.join(TESSDATA_DIR, "eng.traineddata.gz")}. Download it before running.`,
    );
  }

  const limit = Number(process.env.LIMIT || 0);
  let manifest;
  if (fs.existsSync(FULL_MANIFEST_PATH)) {
    manifest = JSON.parse(fs.readFileSync(FULL_MANIFEST_PATH, "utf8"));
  } else {
    const html = await loadFolderHtml();
    manifest = parseManifest(html);
  }
  manifest = manifest
    .filter((file) => file.id && /\.(HEIC|PNG)$/i.test(file.title))
    .sort((a, b) => {
      const an = Number((a.title.match(/IMG_(\d+)/) || [])[1] || 0);
      const bn = Number((b.title.match(/IMG_(\d+)/) || [])[1] || 0);
      return an - bn || a.title.localeCompare(b.title);
    })
    .slice(0, limit || undefined);
  if (!manifest.length) throw new Error("No Drive image files were found in the folder HTML.");
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), "utf8");
  console.log(`Found ${manifest.length} images.`);

  const reuseOcr = process.env.REUSE_OCR === "1";
  const previousRecords = fs.existsSync(JSON_PATH)
    ? new Map(JSON.parse(fs.readFileSync(JSON_PATH, "utf8")).map((record) => [record.id, record]))
    : new Map();
  const worker = reuseOcr ? null : await createOcrWorker();
  const records = [];

  for (let i = 0; i < manifest.length; i++) {
    const file = manifest[i];
    console.log(`[${i + 1}/${manifest.length}] ${file.title}`);
    const imagePath = await downloadImage(file);
    const ocrPath = path.join(OCR_DIR, `${safeBase(file.title)}.txt`);
    let text;
    let confidence = previousRecords.get(file.id)?.confidence || 0;

    if (reuseOcr && fs.existsSync(ocrPath) && fs.statSync(ocrPath).size > 0) {
      text = fs.readFileSync(ocrPath, "utf8");
    } else {
      const input = await preprocessForOcr(imagePath);
      const result = await worker.recognize(input);
      text = cleanText(result.data.text || "");
      confidence = result.data.confidence || 0;
      fs.writeFileSync(ocrPath, text, "utf8");
    }

    const entities = extractEntities(text);
    const locations = inferLocations(text);
    const candidateLines = extractCandidateLines(text);
    const companyRows = extractCompanyRows(text);
    const kind = inferKind(text);

    records.push({
      ...file,
      kind,
      locations,
      entities,
      candidateLines,
      companyRows,
      confidence,
      imagePath,
      ocrPath,
      text,
    });
  }

  if (worker) await worker.terminate();
  fs.writeFileSync(JSON_PATH, JSON.stringify(records, null, 2), "utf8");
  fs.writeFileSync(REPORT_PATH, buildMarkdown(records), "utf8");
  console.log(`Wrote ${REPORT_PATH}`);
  console.log(`Wrote ${JSON_PATH}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
