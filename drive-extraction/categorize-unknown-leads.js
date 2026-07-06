const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const JSON_PATH = path.join(ROOT, "job-leads-extraction.json");
const OUT_MD = path.join(ROOT, "unknown-categorization-proposal.md");
const OUT_CSV = path.join(ROOT, "proposed-tracker-rows-from-unknown.csv");
const OUT_PHONE_CSV = path.join(ROOT, "proposed-phone-whatsapp-leads.csv");

const WEB_SOURCES = {
  asap: "https://asapmedia.co.in/ ; https://in.linkedin.com/company/asap_media",
  artgripper: "https://artgripper.studio/",
  brandfy: "https://brandfy.net/contact-us/ ; https://www.linkedin.com/company/brandfyagency",
  excellent: "https://www.excellentwebworld.com/contact-us/",
  ikonsult: "https://in.linkedin.com/company/ikonsultrecruitment",
  littlegreen: "https://in.linkedin.com/company/little-green-studio",
  lovedwell: "https://lovedwell.com/pages/contact",
  museocamera: "https://www.museocamera.org/working-at-museo-camera",
  nikah: "https://nikahforever.com/home/contact_us",
  onething: "https://www.onething.design/careers",
  ontime: "https://ontimeuae.com/career/ ; https://ontimeuae.com/on-demand-labour-solutions/",
  ombre: "https://theombre.com/contact",
  orange: "https://www.orangecorporatesolutions.com/join-us",
  paraminfo: "https://paraminfo.com/careers/",
  pfaff: "https://www.pfaffmotorsports.com/team ; https://ca.linkedin.com/company/pfaff-motorsports",
  radlvng: "https://radlvng.com/ ; https://radlvng.com/pages/about-us",
  shell: "https://in.linkedin.com/company/shell-consultancy",
  sitech: "https://www.linkedin.com/company/sitechinc",
  socialwatch: "https://socialwatch.io/careers/",
  soledxb: "https://www.linkedin.com/company/soledxb1 ; https://soledxb.com/",
  studioMurb: "https://www.studiomurb.com/",
  webveda: "https://webveda.com/contactus ; https://in.linkedin.com/company/webveda",
};

function readRecords() {
  return JSON.parse(fs.readFileSync(JSON_PATH, "utf8"));
}

function byTitle(records, title) {
  const record = records.find((item) => item.title === title);
  if (!record) throw new Error(`Missing OCR record: ${title}`);
  return record;
}

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

function csvEscape(value) {
  const text = String(value ?? "");
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function writeCsv(filePath, rows) {
  const headers = [
    "proposed_tab",
    "country_or_region",
    "lead_name",
    "category",
    "email",
    "phone",
    "website_or_domain",
    "source_screenshot",
    "verification_source",
    "confidence",
    "notes",
  ];
  const lines = [headers.join(",")];
  for (const row of rows) {
    lines.push(headers.map((header) => csvEscape(row[header])).join(","));
  }
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`, "utf8");
}

function emailDomain(email) {
  const match = String(email || "").match(/@([^@\s]+)$/);
  return match ? match[1].toLowerCase() : "";
}

function leadNameFromEmail(email) {
  const domain = emailDomain(email);
  const withoutTld = domain.replace(/\.(com|ae|in|org|net|co|me|io|studio|design)$/i, "");
  return withoutTld
    .split(".")
    .filter(Boolean)
    .map((part) => part.replace(/[-_]/g, " "))
    .join(" ")
    .replace(/\b\w/g, (char) => char.toUpperCase()) || email;
}

function agencyListRows(records) {
  const sourceTitles = ["IMG_8334.HEIC", "IMG_8341.HEIC"];
  const seen = new Set();
  const rows = [];
  for (const title of sourceTitles) {
    const record = byTitle(records, title);
    for (const email of record.entities.emails || []) {
      const normalized = normalizeEmail(email);
      if (!normalized || seen.has(normalized)) continue;
      seen.add(normalized);
      rows.push({
        proposed_tab: "Agencies",
        country_or_region: "UAE / Dubai or GCC",
        lead_name: leadNameFromEmail(normalized),
        category: "Recruitment agency / staffing contact",
        email: normalized,
        phone: "",
        website_or_domain: emailDomain(normalized),
        source_screenshot: title,
        verification_source: "OCR agency-list screenshot; many .ae, dxb, middleeast, and UAE staffing domains. Verify before outreach.",
        confidence: normalized.endsWith(".ae") || normalized.includes("middleeast") || normalized.includes("dxb")
          ? "High"
          : "Medium",
        notes: "Move from Unknown into UAE/Dubai agency review queue.",
      });
    }
  }
  return rows;
}

function addRows(rows) {
  return rows.map((row) => ({
    proposed_tab: row.proposed_tab || "",
    country_or_region: row.country_or_region || "",
    lead_name: row.lead_name || "",
    category: row.category || "",
    email: row.email || "",
    phone: row.phone || "",
    website_or_domain: row.website_or_domain || "",
    source_screenshot: row.source_screenshot || "",
    verification_source: row.verification_source || "",
    confidence: row.confidence || "Medium",
    notes: row.notes || "",
  }));
}

function curatedRows() {
  return addRows([
    {
      proposed_tab: "Direct Employers",
      country_or_region: "Egypt",
      lead_name: "Brandfy Agency",
      category: "Creative / digital marketing agency",
      email: "info@brandfy.net",
      website_or_domain: "brandfy.net",
      source_screenshot: "IMG_6882.HEIC",
      verification_source: WEB_SOURCES.brandfy,
      confidence: "High",
      notes: "Website/LinkedIn place Brandfy in Cairo, Egypt. Do not put in Dubai.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Onething Design",
      category: "UI/UX design agency hiring designers",
      email: "people@onething.design",
      website_or_domain: "onething.design",
      source_screenshot: "IMG_7193.HEIC",
      verification_source: WEB_SOURCES.onething,
      confidence: "High",
      notes: "Design roles; route outside Dubai under India.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "Canada",
      lead_name: "Pfaff Motorsports",
      category: "Direct employer / motorsports",
      email: "jobs@pfaffmotorsports.com",
      website_or_domain: "pfaffmotorsports.com",
      source_screenshot: "IMG_7207.HEIC",
      verification_source: WEB_SOURCES.pfaff,
      confidence: "High",
      notes: "Canadian motorsports employer; not UAE.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Little Green Studio",
      category: "Creative / design studio",
      email: "hr@littlegreenstudio.in",
      website_or_domain: "littlegreenstudio.in",
      source_screenshot: "IMG_7871.HEIC",
      verification_source: WEB_SOURCES.littlegreen,
      confidence: "High",
      notes: "Indian domain and LinkedIn hiring post.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Nikah Forever",
      category: "Direct employer",
      email: "career@nikahforever.com",
      phone: "WhatsApp: +91-8448293814",
      website_or_domain: "nikahforever.com",
      source_screenshot: "IMG_7919.HEIC",
      verification_source: WEB_SOURCES.nikah,
      confidence: "High",
      notes: "India lead; keep WhatsApp in row but not phone-only.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Artgripper Studio",
      category: "CGI / brand design studio",
      email: "hello@artgripper.studio",
      website_or_domain: "artgripper.studio",
      source_screenshot: "IMG_7925.HEIC",
      verification_source: WEB_SOURCES.artgripper,
      confidence: "High",
      notes: "Official site shows Indian phone number and India work examples.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "RAD LVNG",
      category: "Consumer brand / creative role",
      email: "talent@radlvng.com",
      website_or_domain: "radlvng.com",
      source_screenshot: "IMG_9323.HEIC",
      verification_source: WEB_SOURCES.radlvng,
      confidence: "High",
      notes: "Official site lists Rad Brands Pvt. Ltd., Noida, India.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "The Ombre",
      category: "Photography / creative studio",
      email: "careers@theombre.com",
      website_or_domain: "theombre.com",
      source_screenshot: "IMG_8936.HEIC",
      verification_source: WEB_SOURCES.ombre,
      confidence: "High",
      notes: "Official contact page says Delhi NCR, India.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "ASAP Media",
      category: "Creative studio hiring designer / photographer / content creator",
      email: "contact@asapmedia.co.in",
      website_or_domain: "asapmedia.co.in",
      source_screenshot: "IMG_8495.HEIC",
      verification_source: WEB_SOURCES.asap,
      confidence: "High",
      notes: "OCR also read spam@asapmedia.co.in; treat that as OCR suspect, use contact@ first.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Museo Camera",
      category: "Museum / design or creative role",
      email: "contact@museocamera.org",
      website_or_domain: "museocamera.org",
      source_screenshot: "IMG_9156.HEIC",
      verification_source: WEB_SOURCES.museocamera,
      confidence: "High",
      notes: "Official page lists Gurugram, Haryana.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "WebVeda",
      category: "Education / content-course company",
      email: "divyam.chutani@webveda.com",
      website_or_domain: "webveda.com",
      source_screenshot: "IMG_9315.HEIC",
      verification_source: WEB_SOURCES.webveda,
      confidence: "High",
      notes: "Official contact page/LinkedIn place WebVeda in Faridabad, India.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Lovedwell",
      category: "Lifestyle/design studio",
      email: "info@lovedwell.com",
      website_or_domain: "lovedwell.com",
      source_screenshot: "IMG_8482.HEIC",
      verification_source: WEB_SOURCES.lovedwell,
      confidence: "High",
      notes: "Official contact page says Simbuno India Pvt. Ltd., Noida.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Social Watch",
      category: "Digital marketing / creative agency",
      email: "hr@socialwatch.io",
      website_or_domain: "socialwatch.io",
      source_screenshot: "IMG_8730.HEIC",
      verification_source: WEB_SOURCES.socialwatch,
      confidence: "High",
      notes: "Official careers page lists Mohali, Punjab, India.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "India",
      lead_name: "Shell Consultancy",
      category: "Recruitment / consultancy",
      email: "careers@shellconsultancy.com",
      website_or_domain: "shellconsultancy.com",
      source_screenshot: "IMG_8710.HEIC",
      verification_source: WEB_SOURCES.shell,
      confidence: "High",
      notes: "LinkedIn hiring posts mention Gurgaon and India roles.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "India",
      lead_name: "Orange Corporate Solutions",
      category: "HR consultancy / recruiter",
      email: "jobs.orange001@gmail.com",
      phone: "WhatsApp: +91 70820 01810",
      website_or_domain: "orangecorporatesolutions.com",
      source_screenshot: "IMG_8950.HEIC",
      verification_source: WEB_SOURCES.orange,
      confidence: "Medium",
      notes: "Gmail differs from official site email; verify before outreach.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "Spain",
      lead_name: "Roberto Castano",
      category: "Photography / creative role",
      email: "thephotographer@robertocastano.com",
      website_or_domain: "robertocastano.com",
      source_screenshot: "IMG_8475.HEIC",
      verification_source: "https://www.behance.net/robertocastano",
      confidence: "Medium",
      notes: "Behance lists Ibiza, Spain; OCR also duplicated uppercase email.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "China / Global",
      lead_name: "Transsion recruiter",
      category: "Recruiter contact",
      email: "kai.mao@transsion.com",
      website_or_domain: "transsion.com",
      source_screenshot: "IMG_8480.HEIC",
      verification_source: "OCR indicates engineering recruitment; web country not verified in this pass.",
      confidence: "Low",
      notes: "Keep outside Dubai unless a UAE role is found.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "Jordan / MENA",
      lead_name: "Sitech",
      category: "IT services / product design company",
      email: "alaa@sitech.me",
      website_or_domain: "sitech.me",
      source_screenshot: "IMG_9321.HEIC",
      verification_source: WEB_SOURCES.sitech,
      confidence: "High",
      notes: "LinkedIn places Sitech in Amman, Jordan.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "UAE / Dubai",
      lead_name: "Sole DXB",
      category: "Creative / culture platform",
      email: "jobs@soledxb.com",
      website_or_domain: "soledxb.com",
      source_screenshot: "IMG_9184.HEIC",
      verification_source: WEB_SOURCES.soledxb,
      confidence: "High",
      notes: "Move to Dubai direct employers.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "UAE / Dubai",
      lead_name: "Ontime Manpower Supply",
      category: "Manpower / staffing agency",
      email: "careers@ontimeuae.ae",
      website_or_domain: "ontimeuae.ae",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: WEB_SOURCES.ontime,
      confidence: "High",
      notes: "Move to Dubai/UAE agency queue.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "UAE / GCC",
      lead_name: "ParamInfo",
      category: "IT staffing / services recruiter",
      email: "rekha.y@paraminfo.com",
      website_or_domain: "paraminfo.com",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: WEB_SOURCES.paraminfo,
      confidence: "High",
      notes: "ParamInfo careers page lists Dubai, Abu Dhabi, Saudi, Bahrain, and India; route as UAE/GCC agency contact.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "UAE / GCC",
      lead_name: "Latinum HR",
      category: "HR / recruitment",
      email: "jobs@latinumhr.com",
      website_or_domain: "latinumhr.com",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: "https://latinumhr.com/en/",
      confidence: "Medium",
      notes: "HR domain; verify exact country before outreach.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "UAE / Global",
      lead_name: "Excellent Webworld",
      category: "Software / app development company",
      email: "murad@excellentwebworld.com",
      website_or_domain: "excellentwebworld.com",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: WEB_SOURCES.excellent,
      confidence: "High",
      notes: "Official site lists UAE office plus global locations.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "UAE / Dubai",
      lead_name: "HTP Global Technologies",
      category: "Technology company",
      email: "hr@myhtptech.com",
      website_or_domain: "myhtptech.com",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: "https://www.crunchbase.com/organization/htp-global-technologies",
      confidence: "Medium",
      notes: "Crunchbase result places HTP Global Technologies in Dubai; verify official careers page before outreach.",
    },
    {
      proposed_tab: "Agencies",
      country_or_region: "India / UAE remote",
      lead_name: "iKonsult Recruitment Solutions",
      category: "Recruitment agency",
      email: "hiring@ikonsult.in",
      website_or_domain: "ikonsult.in",
      source_screenshot: "IMG_8701.HEIC",
      verification_source: WEB_SOURCES.ikonsult,
      confidence: "High",
      notes: "LinkedIn post mentions remote India/UAE roles.",
    },
    {
      proposed_tab: "Direct Employers",
      country_or_region: "India",
      lead_name: "Studio Murb",
      category: "Design / marketing studio",
      email: "hey@studiomurb.com",
      website_or_domain: "studiomurb.com",
      source_screenshot: "IMG_8843.HEIC",
      verification_source: WEB_SOURCES.studioMurb,
      confidence: "Medium",
      notes: "Official site has hiring email; India inferred from web presence and projects.",
    },
  ]);
}

function careerLinkRows() {
  const companies = [
    ["Careem", "careem.com/careers", "IMG_8702.HEIC"],
    ["Swvl", "swvl.com/careers", "IMG_8702.HEIC"],
    ["Fetchr", "fetchr.us/careers", "IMG_8702.HEIC"],
    ["Trukker / Tenderd", "tenderd.com/careers", "IMG_8702.HEIC"],
    ["Talabat", "talabat.com/careers", "IMG_8702.HEIC"],
    ["Kitopi", "kitopi.com/careers", "IMG_8702.HEIC"],
    ["Crafty", "craftydelivers.com/careers", "IMG_8702.HEIC"],
    ["Foodics", "foodics.com/careers", "IMG_8702.HEIC"],
    ["Dubizzle", "dubizzle.com/careers", "IMG_8703.HEIC"],
    ["Property Finder", "propertyfinder.ae/careers", "IMG_8703.HEIC"],
    ["Huspy", "huspy.com/careers", "IMG_8703.HEIC"],
    ["Stake", "getstake.com/careers", "IMG_8703.HEIC"],
    ["Beehive", "beehive.ae/careers", "IMG_8703.HEIC"],
    ["Sarwa", "sarwa.co/careers", "IMG_8703.HEIC"],
    ["Yallacompare", "yallacompare.com/careers", "IMG_8703.HEIC"],
    ["Mamo Pay", "mamopay.com/careers", "IMG_8703.HEIC"],
    ["Ziina", "ziina.com/careers", "IMG_8703.HEIC"],
    ["Lean Technologies", "leantech.me/careers", "IMG_8703.HEIC"],
    ["Pyypl", "pyypl.com/careers", "IMG_8703.HEIC"],
    ["Now Money", "nowmoney.me/careers", "IMG_8703.HEIC"],
    ["NymCard", "nymcard.com/careers", "IMG_8703.HEIC"],
    ["Mangopay MENA", "mangopay.com/careers", "IMG_8703.HEIC"],
    ["Wio Bank", "wio.io/careers", "IMG_8703.HEIC"],
    ["YAP", "yap.com/careers", "IMG_8703.HEIC"],
    ["Tabby", "tabby.ai/careers", "IMG_8704.HEIC"],
    ["Tamara", "tamara.co/careers", "IMG_8704.HEIC"],
    ["Spotii", "spotii.me/careers", "IMG_8704.HEIC"],
    ["Almosafer", "almosafer.com/careers", "IMG_8704.HEIC"],
    ["Flyin", "flyin.com/careers", "IMG_8704.HEIC"],
    ["G42", "g42.ai/careers", "IMG_8705.HEIC"],
    ["Presight AI", "presight.ai/careers", "IMG_8705.HEIC"],
    ["ADNOC Digital", "adnoc.ae/careers", "IMG_8705.HEIC"],
    ["2gether", "2gether.global/careers", "IMG_8705.HEIC"],
  ];

  return addRows(
    companies.map(([name, website, screenshot]) => ({
      proposed_tab: "Direct Employers",
      country_or_region: "UAE / GCC / MENA",
      lead_name: name,
      category: "Company career-link lead",
      email: "",
      phone: "",
      website_or_domain: website,
      source_screenshot: screenshot,
      verification_source: "OCR career-link list from screenshot; web/source verification still needed before applying.",
      confidence: website.includes(".ae") || ["Careem", "Talabat", "Kitopi", "Dubizzle", "Property Finder", "G42", "Presight AI", "ADNOC Digital", "Wio Bank"].includes(name)
        ? "Medium"
        : "Low",
      notes: "Move from Unknown into UAE/GCC direct-employer research queue.",
    })),
  );
}

function phoneRows() {
  return addRows([
    {
      proposed_tab: "Phone / WhatsApp Leads",
      country_or_region: "India",
      lead_name: "Freelance Video Editor lead",
      category: "Phone-only creative job lead",
      phone: "9511116204",
      source_screenshot: "IMG_8494.HEIC",
      verification_source: "OCR screenshot only",
      confidence: "Low",
      notes: "Only a phone number was captured; keep out of email tables.",
    },
    {
      proposed_tab: "Phone / WhatsApp Leads",
      country_or_region: "India / needs verification",
      lead_name: "BSD / Amlanjyoti UX UI lead",
      category: "Phone plus malformed email",
      email: "amlanjyotibharali@bsd.ed",
      phone: "6000236346; 9620045916",
      website_or_domain: "bsd.edu.in",
      source_screenshot: "IMG_9183.HEIC",
      verification_source: "https://in.linkedin.com/in/amlanjyoti-bharali ; https://www.bsd.edu.in/",
      confidence: "Low",
      notes: "OCR email appears malformed; verify image before outreach.",
    },
    {
      proposed_tab: "Phone / WhatsApp Leads",
      country_or_region: "India / needs verification",
      lead_name: "Reslink lead",
      category: "Phone plus domain mismatch",
      email: "team@reslink.org",
      phone: "91-8303982425",
      website_or_domain: "reslink.org",
      source_screenshot: "IMG_8744.HEIC",
      verification_source: "Search found reslink.io, not reslink.org; verify manually.",
      confidence: "Low",
      notes: "Do not merge with reslink.io without visual/web confirmation.",
    },
  ]);
}

function researchRows() {
  return addRows([
    {
      proposed_tab: "Needs Email Research",
      country_or_region: "Unknown / possible India",
      lead_name: "Neeraj / portfolio hiring lead",
      category: "Gmail contact",
      email: "neerajiwtwrs@gmail.com",
      source_screenshot: "IMG_8949.HEIC",
      verification_source: "No reliable domain source found; Gmail only.",
      confidence: "Low",
      notes: "Keep for manual review, not Dubai.",
    },
    {
      proposed_tab: "Needs Email Research",
      country_or_region: "Unknown / possible Indonesia",
      lead_name: "Sukhakala",
      category: "Gmail contact",
      email: "sukhakala.id@gmail.com",
      source_screenshot: "IMG_9185.HEIC",
      verification_source: "No reliable source found; .id in name is not enough for country assignment.",
      confidence: "Low",
      notes: "Manual verification required.",
    },
    {
      proposed_tab: "Needs Email Research",
      country_or_region: "Unknown / likely not a job lead",
      lead_name: "Shivani main account",
      category: "Gmail contact / weak evidence",
      email: "shivanimainacc@gmail.com",
      source_screenshot: "IMG_9218.HEIC",
      verification_source: "OCR suggests meme/non-job context.",
      confidence: "Low",
      notes: "Probably skip unless the screenshot visually confirms a real job lead.",
    },
  ]);
}

function markdown(rows, phoneRowsOnly) {
  const groupMap = new Map();
  for (const row of rows) {
    const key = `${row.proposed_tab} | ${row.country_or_region}`;
    if (!groupMap.has(key)) groupMap.set(key, []);
    groupMap.get(key).push(row);
  }

  const lines = [];
  lines.push("# Unknown Bucket Categorization Proposal");
  lines.push("");
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push("Source files: `job-leads-extraction.json`, OCR screenshots, and targeted web/domain verification.");
  lines.push("");
  lines.push("## Proposed Sheet/Tab Changes");
  lines.push("");
  lines.push("- Rename existing `WhatsApp Other` tab to `Phone / WhatsApp Leads`.");
  lines.push("- Add UAE/GCC recruitment-agency contacts from the two agency-list screenshots into `Agencies`.");
  lines.push("- Add UAE/GCC career-link companies into `Direct Employers` as research rows, not as already-applied rows.");
  lines.push("- Add India, Spain, Canada, Egypt, Jordan/MENA, China/Global, and unknown Gmail contacts under country-specific review sections or `Needs Email Research`.");
  lines.push("- Do not send outreach or update application status from this file without deduping against the live tracker first.");
  lines.push("");
  lines.push("## Output Files");
  lines.push("");
  lines.push("- `proposed-tracker-rows-from-unknown.csv`: all proposed rows.");
  lines.push("- `proposed-phone-whatsapp-leads.csv`: phone/WhatsApp-only or phone-first rows.");
  lines.push("");
  lines.push("## Counts");
  lines.push("");
  lines.push(`- Total proposed rows: ${rows.length}`);
  lines.push(`- Phone/WhatsApp rows: ${phoneRowsOnly.length}`);
  lines.push("");
  lines.push("## Grouped Proposal");
  lines.push("");
  for (const [group, items] of [...groupMap.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    lines.push(`### ${group}`);
    lines.push("");
    lines.push("| Lead | Category | Email | Phone | Website/domain | Screenshot | Confidence | Notes |");
    lines.push("|---|---|---|---|---|---|---|---|");
    for (const row of items) {
      lines.push(
        `| ${row.lead_name} | ${row.category} | ${row.email} | ${row.phone} | ${row.website_or_domain} | ${row.source_screenshot} | ${row.confidence} | ${row.notes} |`,
      );
    }
    lines.push("");
  }
  lines.push("## Verification Sources Used");
  lines.push("");
  for (const source of Object.values(WEB_SOURCES).sort()) lines.push(`- ${source}`);
  lines.push("- https://www.behance.net/robertocastano");
  lines.push("- https://latinumhr.com/en/");
  lines.push("- https://www.crunchbase.com/organization/htp-global-technologies");
  lines.push("- https://in.linkedin.com/in/amlanjyoti-bharali ; https://www.bsd.edu.in/");
  lines.push("");
  return `${lines.join("\n")}\n`;
}

function main() {
  const records = readRecords();
  const agencyRows = agencyListRows(records);
  const rows = [
    ...agencyRows,
    ...curatedRows(),
    ...careerLinkRows(),
    ...phoneRows(),
    ...researchRows(),
  ];

  const seen = new Set();
  const deduped = rows.filter((row) => {
    const key = [row.proposed_tab, row.country_or_region, row.email || row.phone || row.website_or_domain, row.lead_name]
      .join("|")
      .toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  const phoneOnly = deduped.filter((row) => row.proposed_tab === "Phone / WhatsApp Leads");

  writeCsv(OUT_CSV, deduped);
  writeCsv(OUT_PHONE_CSV, phoneOnly);
  fs.writeFileSync(OUT_MD, markdown(deduped, phoneOnly), "utf8");

  const counts = deduped.reduce((acc, row) => {
    const key = row.proposed_tab;
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
  console.log(`Wrote ${OUT_MD}`);
  console.log(`Wrote ${OUT_CSV}`);
  console.log(`Wrote ${OUT_PHONE_CSV}`);
  console.log(JSON.stringify({ total: deduped.length, counts }, null, 2));
}

main();
