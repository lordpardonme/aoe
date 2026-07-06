const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const JSON_PATH = path.join(ROOT, "job-leads-extraction.json");
const OUT_PATH = path.join(ROOT, "unknown-needs-review-summary.md");

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

function clean(line) {
  return String(line || "")
    .replace(/^[\s>*•.-]+/, "")
    .replace(/\s+/g, " ")
    .trim();
}

function uniq(values) {
  return [...new Set(values.filter(Boolean))];
}

function clip(value, max = 130) {
  const text = clean(value);
  return text.length > max ? `${text.slice(0, max - 3)}...` : text;
}

function inferHints(record) {
  const text = record.text || "";
  const lower = text.toLowerCase();
  const hints = [];

  if (/\bwhatsapp|wa\b/i.test(text) || /\+91|\.in\b|gmail\.com/i.test(text)) hints.push("possible India/personal-contact lead");
  if (/\bdesigner|ui\/ux|ui ux|product designer|graphic designer|creative|figma|visual designer|brand/i.test(text)) {
    hints.push("design-related");
  }
  if (/\bhiring|job|role|vacancy|opening|apply|career|send your cv|join/i.test(text)) hints.push("job/application lead");
  if (/\bagency|recruitment|recruiter|consultancy|talent/i.test(text)) hints.push("agency/recruiter");
  if (/\bdubai|uae|arabia|dxb|middle east|mideast/i.test(text)) hints.push("possible UAE/GCC despite bucket");
  if (/\bcanada|toronto|ontario|usa|united states|new york|california/i.test(text)) hints.push("possible North America");
  if (lower.includes("linkedin")) hints.push("LinkedIn screenshot");

  return uniq(hints);
}

function score(record) {
  const emails = record.entities?.emails?.length || 0;
  const urls = record.entities?.urls?.length || 0;
  const phones = record.entities?.phones?.length || 0;
  const hints = inferHints(record).length;
  const confidence = record.confidence || 0;
  return emails * 4 + urls * 3 + phones * 3 + hints * 2 + Math.min(5, Math.floor(confidence / 20));
}

function keyLines(record) {
  const entityLines = [];
  const emails = record.entities?.emails || [];
  const urls = record.entities?.urls || [];
  const phones = record.entities?.phones || [];
  if (emails.length) entityLines.push(`Emails: ${emails.join("; ")}`);
  if (urls.length) entityLines.push(`Links: ${urls.join("; ")}`);
  if (phones.length) entityLines.push(`Phones: ${phones.join("; ")}`);

  const textLines = (record.text || "")
    .split("\n")
    .map(clean)
    .filter(Boolean)
    .filter((line) => {
      if (line.length < 4) return false;
      if (/^\d{1,2}:\d{2}$/.test(line)) return false;
      if (/^(message|camera|download|shared|modified|storage used|image)$/i.test(line)) return false;
      return /@|https?:\/\/|www\.|whatsapp|hiring|job|role|designer|recruit|career|apply|cv|send|studio|agency|company|contact/i.test(
        line,
      );
    })
    .map((line) => clip(line))
    .slice(0, 8);

  return uniq([...entityLines, ...textLines]).slice(0, 10);
}

function tableEscape(value) {
  return String(value || "").replace(/\|/g, "\\|").replace(/\r?\n/g, "<br>");
}

function main() {
  const records = JSON.parse(fs.readFileSync(JSON_PATH, "utf8"));
  const unknown = records.filter((record) => trackerBucket(record) === "Unknown / needs review");
  const useful = unknown.filter((record) => score(record) >= 7).sort((a, b) => score(b) - score(a));
  const reviewOnly = unknown.filter((record) => score(record) < 7).sort((a, b) => score(b) - score(a));

  const allEmails = uniq(unknown.flatMap((r) => r.entities?.emails || []));
  const allUrls = uniq(unknown.flatMap((r) => r.entities?.urls || []));
  const allPhones = uniq(unknown.flatMap((r) => r.entities?.phones || []));

  const lines = [];
  lines.push("# Unknown / Needs Review Summary");
  lines.push("");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push("Source: `job-leads-extraction.json`");
  lines.push("");
  lines.push("## What This Bucket Means");
  lines.push("");
  lines.push("These screenshots did not contain a clear country/location in OCR, so they were not safe to put directly into UAE, India, Germany, or another country bucket.");
  lines.push("Many are still useful because they contain emails, WhatsApp numbers, company names, job posts, or recruiter clues.");
  lines.push("");
  lines.push("## Counts");
  lines.push("");
  lines.push(`- Screenshots in this bucket: ${unknown.length}`);
  lines.push(`- Contact-rich / likely useful: ${useful.length}`);
  lines.push(`- Needs visual/manual review first: ${reviewOnly.length}`);
  lines.push(`- Unique email-like values: ${allEmails.length}`);
  lines.push(`- Unique links/forms: ${allUrls.length}`);
  lines.push(`- Unique phone-like values: ${allPhones.length}`);
  lines.push("");
  lines.push("## Best Leads To Review First");
  lines.push("");
  lines.push("| Priority | Image | Type | Score | Hints | Contacts |");
  lines.push("|---:|---|---|---:|---|---|");
  useful.slice(0, 30).forEach((record, index) => {
    const contacts = [
      ...(record.entities?.emails || []).slice(0, 3),
      ...(record.entities?.urls || []).slice(0, 2),
      ...(record.entities?.phones || []).slice(0, 2),
    ];
    const more =
      (record.entities?.emails?.length || 0) +
      (record.entities?.urls?.length || 0) +
      (record.entities?.phones?.length || 0) -
      contacts.length;
    lines.push(
      `| ${index + 1} | ${record.title} | ${tableEscape(record.kind)} | ${score(record)} | ${tableEscape(
        inferHints(record).join("; "),
      )} | ${tableEscape(contacts.join("<br>") + (more > 0 ? `<br>+${more} more` : ""))} |`,
    );
  });
  lines.push("");
  lines.push("## Per-Screenshot Notes");
  lines.push("");
  for (const record of [...useful, ...reviewOnly]) {
    lines.push(`### ${record.title}`);
    lines.push("");
    lines.push(`- Type from OCR: ${record.kind}`);
    lines.push(`- OCR confidence: ${Math.round(record.confidence || 0)}`);
    lines.push(`- Usefulness score: ${score(record)}`);
    lines.push(`- Hints: ${inferHints(record).join("; ") || "No reliable hint"}`);
    lines.push(`- Drive file: https://drive.google.com/file/d/${record.id}/view`);
    lines.push(`- Local image: images/${path.basename(record.imagePath)}`);
    lines.push(`- Raw OCR: ocr/${path.basename(record.ocrPath)}`);
    const linesForRecord = keyLines(record);
    if (linesForRecord.length) {
      lines.push("");
      lines.push("Useful OCR lines:");
      linesForRecord.forEach((line) => lines.push(`- ${line}`));
    } else {
      lines.push("");
      lines.push("Useful OCR lines: none extracted reliably; inspect the image.");
    }
    lines.push("");
  }

  fs.writeFileSync(OUT_PATH, `${lines.join("\n")}\n`, "utf8");
  console.log(`Wrote ${OUT_PATH}`);
  console.log(
    JSON.stringify(
      {
        unknown: unknown.length,
        useful: useful.length,
        reviewOnly: reviewOnly.length,
        emails: allEmails.length,
        urls: allUrls.length,
        phones: allPhones.length,
      },
      null,
      2,
    ),
  );
}

main();
