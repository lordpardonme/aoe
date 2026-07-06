import csv
from pathlib import Path

CSV_PATH = Path(r"C:\Users\mohdh\Documents\Job Hunt\resumes\uae-job-opening-scan.csv")
OUT_PATH = Path(r"C:\Users\mohdh\Documents\Job Hunt\resumes\agency-outreach-plan.csv")

SPECIALISATIONS = {
    "ADMS UAE": "UAE hiring and manpower support",
    "AKRS": "UAE recruitment and staffing",
    "ASRS": "UAE recruitment and staffing",
    "Adecco": "IT, digital, permanent recruitment, and staffing across the UAE",
    "Al Mansoor Group": "UAE recruitment and manpower services",
    "Al Nahiya": "UAE recruitment and manpower services",
    "Al Thawiya": "UAE recruitment and staffing",
    "Al Vakil": "GCC recruitment and overseas hiring",
    "Antal": "professional and specialist recruitment",
    "BAC Middle East": "UAE professional recruitment",
    "CIG": "UAE recruitment and staffing",
    "Derby Group": "UAE staffing and outsourcing",
    "Emirates Net": "UAE recruitment and staffing",
    "Executive Solutions ME": "executive and professional hiring in the Middle East",
    "Experts Recruitment": "UAE recruitment and staffing",
    "Hays": "Middle East IT, technology, contract, and permanent recruitment",
    "Horizon Group": "UAE recruitment and manpower services",
    "Innovation UAE": "UAE recruitment, outsourcing, and staffing",
    "Inspire Selection": "Dubai professional recruitment across digital, banking, fintech, sales, marketing, and technology",
    "JVI Global": "global recruitment and jobseeker placement",
    "Kershaw Leonard": "Dubai professional recruitment and executive search",
    "Lobo Management": "GCC technology, startup, digital, and executive recruitment",
    "Mackenzie Jones": "Middle East technology and digital recruitment",
    "Manpower Middle East": "GCC permanent, contingent, outsourcing, and workforce solutions",
    "Michael Page": "Middle East Digital and Technology recruitment including UI/UX, Product, and eCommerce",
    "Nadia Global": "UAE recruitment across IT, technology, digital, consumer, e-commerce, finance, and healthcare",
    "Nathan HR": "UAE recruitment, HR, and staffing support",
    "Pact Employment": "UAE staffing and recruitment",
    "Randstad": "global staffing and professional recruitment",
    "Rawafed": "UAE recruitment and staffing",
    "Reach Group": "UAE recruitment and outsourcing",
    "Receptionist PA": "UAE admin and staffing support",
    "SSA Ltd": "specialist recruitment across GCC built environment and professional roles",
    "Sawaeed": "UAE staffing, outsourcing, and manpower services",
    "Spark": "UAE recruitment and staffing",
    "Sundus Recruitment": "UAE recruitment and outsourcing with technology and project roles",
    "TASC Outsourcing": "UAE recruitment, outsourcing, contract staffing, managed services, and tech talent through AIQU",
    "Talascend": "technical and professional staffing",
    "UHRS": "UAE HR, staffing, and recruitment support",
    "Xperts Jobs": "UAE job placement and recruitment",
}


def normalize_recipients(raw: str) -> str:
    parts = [part.strip() for part in raw.replace(";", ",").split(",")]
    filtered = []
    for part in parts:
        lower = part.lower()
        if "@" not in lower:
            continue
        if lower.startswith("employers@"):
            continue
        filtered.append(part)
    return ", ".join(dict.fromkeys(filtered))


with CSV_PATH.open(encoding="utf-8", newline="") as source:
    rows = list(csv.DictReader(source))

out_rows = []
for row in rows:
    if row.get("Type") != "Agency":
        continue
    company = row["Company / Agency"].strip()
    recipients = normalize_recipients(row["Email"])
    if not recipients:
        continue
    out_rows.append(
        {
            "Company / Agency": company,
            "Recipients": recipients,
            "Specialisation Line": SPECIALISATIONS.get(company, "UAE recruitment and staffing"),
            "Subject": "Product Designer for UAE roles - Mohd Hayaat Ali",
            "Status": "Ready to Send",
            "Gmail Sent ID": "",
        }
    )

with OUT_PATH.open("w", encoding="utf-8", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=list(out_rows[0].keys()))
    writer.writeheader()
    writer.writerows(out_rows)

print(OUT_PATH)
print(len(out_rows))
