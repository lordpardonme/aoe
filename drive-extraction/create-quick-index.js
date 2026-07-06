const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const JSON_PATH = path.join(ROOT, "job-leads-extraction.json");
const QUICK_INDEX_PATH = path.join(ROOT, "job-leads-quick-index.md");

function trackerBucket(record) {
  const text = `${(record.locations || []).join(" ")} ${record.text || ""}`.toLowerCase();
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

function uniq(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function shortList(values, limit = 3) {
  const items = uniq(values);
  if (!items.length) return "";
  const shown = items.slice(0, limit).join("<br>");
  return items.length > limit ? `${shown}<br>+${items.length - limit} more` : shown;
}

function tableEscape(value) {
  return String(value || "")
    .replace(/\|/g, "\\|")
    .replace(/\r?\n/g, "<br>");
}

function main() {
  const records = JSON.parse(fs.readFileSync(JSON_PATH, "utf8"));
  const buckets = new Map();
  for (const record of records) {
    const bucket = trackerBucket(record);
    if (!buckets.has(bucket)) buckets.set(bucket, []);
    buckets.get(bucket).push(record);
  }

  const allEmails = uniq(records.flatMap((r) => r.entities?.emails || []));
  const allUrls = uniq(records.flatMap((r) => r.entities?.urls || []));
  const allPhones = uniq(records.flatMap((r) => r.entities?.phones || []));
  const lines = [];

  lines.push("# Job Leads Quick Index");
  lines.push("");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Screenshots processed: ${records.length}`);
  lines.push("");
  lines.push("## Open These Files");
  lines.push("");
  lines.push("- Full extraction report: `job-leads-extraction.md`");
  lines.push("- Structured data: `job-leads-extraction.json`");
  lines.push("- Raw OCR text: `ocr/`");
  lines.push("- Downloaded preview images: `images/`");
  lines.push("");
  lines.push("## Counts");
  lines.push("");
  lines.push(`- Unique email-like values: ${allEmails.length}`);
  lines.push(`- Unique links/forms: ${allUrls.length}`);
  lines.push(`- Unique phone-like values: ${allPhones.length}`);
  lines.push("");
  lines.push("## Review Order");
  lines.push("");
  lines.push("1. Start with `UAE / Dubai` because those are the likely tracker rows for agencies/direct employers.");
  lines.push("2. Then review named countries outside Dubai: India, Germany, Netherlands, United Kingdom, and any GCC country that appears.");
  lines.push("3. Finish `Unknown / needs review`; these need screenshot inspection because OCR did not capture a reliable location.");
  lines.push("");
  lines.push("## Bucket Counts");
  lines.push("");
  lines.push("| Bucket | Screenshots | Agencies/recruiters | Direct/job leads | Unknown type |");
  lines.push("|---|---:|---:|---:|---:|");
  for (const [bucket, items] of [...buckets.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const agency = items.filter((r) => r.kind === "Agency / recruiter").length;
    const direct = items.filter((r) => r.kind === "Job lead / direct employer").length;
    const unknown = items.length - agency - direct;
    lines.push(`| ${bucket} | ${items.length} | ${agency} | ${direct} | ${unknown} |`);
  }
  lines.push("");
  lines.push("## Contact-Rich Screenshots");
  lines.push("");
  lines.push("| Bucket | Image | Type | Emails | Links | Phones |");
  lines.push("|---|---|---|---|---|---|");
  for (const record of records) {
    const emails = record.entities?.emails || [];
    const urls = record.entities?.urls || [];
    const phones = record.entities?.phones || [];
    if (!emails.length && !urls.length && !phones.length) continue;
    lines.push(
      `| ${trackerBucket(record)} | ${record.title} | ${tableEscape(record.kind)} | ${tableEscape(
        shortList(emails),
      )} | ${tableEscape(shortList(urls, 2))} | ${tableEscape(shortList(phones, 2))} |`,
    );
  }
  lines.push("");
  lines.push("## All Screenshots");
  lines.push("");
  lines.push("| # | Bucket | Image | Type | Locations | Emails | Links | Phones | OCR confidence |");
  lines.push("|---:|---|---|---|---|---:|---:|---:|---:|");
  records.forEach((record, index) => {
    lines.push(
      `| ${index + 1} | ${trackerBucket(record)} | ${record.title} | ${tableEscape(record.kind)} | ${tableEscape(
        (record.locations || []).join(", ") || "Unknown",
      )} | ${(record.entities?.emails || []).length} | ${(record.entities?.urls || []).length} | ${
        (record.entities?.phones || []).length
      } | ${Math.round(record.confidence || 0)} |`,
    );
  });
  lines.push("");
  lines.push("## Notes");
  lines.push("");
  lines.push("- This is OCR from screenshots, so verify low-confidence or garbled text against the original image before updating the tracker.");
  lines.push("- The full report contains key OCR lines per screenshot; use this quick index only for navigation.");
  lines.push("");

  fs.writeFileSync(QUICK_INDEX_PATH, `${lines.join("\n")}\n`, "utf8");
  console.log(`Wrote ${QUICK_INDEX_PATH}`);
}

main();
