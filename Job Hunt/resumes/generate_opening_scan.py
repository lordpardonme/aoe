import csv

SRC = r"C:\Users\mohdh\Documents\Job Hunt\sheet-export.csv"
OUT = r"C:\Users\mohdh\Documents\Job Hunt\resumes\uae-job-opening-scan.csv"
SCAN_DATE = "2026-06-02"

FINDINGS = {
    "Careem": (
        "Openings Found",
        "Senior Product Designer; Senior Product Designer - Design System",
        "https://tenurecareers.io/jobs/senior-product-designer-careem-dubai | https://designproject.io/jobs/jobs/senior-product-designer-at-careem-ub5m1e",
        "High",
        "Tailor resume and apply on company site",
    ),
    "Talabat": (
        "Openings Found",
        "Staff Product Designer; Product Designer",
        "https://designproject.io/jobs/staff-product-designer-global-hub-q-commerce-at-delivery-hero-devjh1 | https://ae.indeed.com/viewjob?jk=4027932f0f2914b3",
        "High",
        "Tailor resume and apply",
    ),
    "Property Finder": (
        "Opening Found",
        "Product Designer",
        "https://www.remotedxb.com/job/product-designer-property-finder",
        "High",
        "Tailor resume and apply",
    ),
    "Emirates NBD": (
        "Opening Found via Agency",
        "Senior Product Designer (Design Systems); older Product Designer listing",
        "https://www.glassdoor.com/job-listing/senior-product-designer-design-systems-gsstech-group-JV_IC2204498_KO0%2C38_KE39%2C52.htm?jl=1010083370981 | https://www.hubmub.com/jobs/596850/product-designer",
        "Medium",
        "Apply via GSSTech or verify direct careers",
    ),
    "Noon": (
        "Needs Verification",
        "Product Designer result found, likely Gurgaon not Dubai",
        "https://jobs.weekday.works/noon-product-designer",
        "Low",
        "Verify location before applying",
    ),
    "Amazon UAE": (
        "No Relevant UAE Opening Found",
        "Sr Product Designer found outside UAE",
        "https://www.amazon.jobs/jobs/3173021",
        "Low",
        "Skip unless open to non-UAE",
    ),
    "Microsoft Gulf": (
        "No Relevant UAE Opening Found",
        "UX Designer result found outside UAE",
        "https://designproject.io/jobs/jobs/ux-designer-ii-at-microsoft-x2ydsb",
        "Low",
        "Monitor careers",
    ),
    "Google UAE": ("No Relevant UAE Opening Found", "", "", "Low", "Monitor careers"),
    "SAP Middle East": ("No Relevant UAE Opening Found", "", "", "Low", "Monitor careers"),
    "Mashreq Bank": ("No Clear Opening Found", "", "", "Low", "Monitor and outreach"),
    "ADCB": ("No Clear Opening Found", "", "", "Low", "Monitor and outreach"),
}


with open(SRC, encoding="utf-8-sig", newline="") as source:
    rows = list(csv.DictReader(source))

extra_fields = [
    "Opening Scan Status",
    "Matched Role(s)",
    "Opening Source URL(s)",
    "Confidence",
    "Recommended Action",
    "Scan Date",
]
fieldnames = list(rows[0].keys()) + extra_fields

with open(OUT, "w", encoding="utf-8", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        company = row["Company / Agency"]
        match = None
        for key, value in FINDINGS.items():
            if key.lower() in company.lower():
                match = value
                break
        if match is None:
            match = ("Needs Manual Check", "", "", "Unknown", "Run company careers/LinkedIn check")
        row.update(
            {
                "Opening Scan Status": match[0],
                "Matched Role(s)": match[1],
                "Opening Source URL(s)": match[2],
                "Confidence": match[3],
                "Recommended Action": match[4],
                "Scan Date": SCAN_DATE,
            }
        )
        writer.writerow(row)

print(OUT)
