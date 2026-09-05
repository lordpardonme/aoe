import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

today_str = "2026-08-25"
follow_up_str = "2026-09-01"

# 1. Update Master Job Tracker Row 189
# Columns: Country(A), Company(B), Email(C), Type(D), Status(E), Date Applied(F), Follow-up(G), Notes(H), Scan Status(I), Matched Role(J), URL(K), Confidence(L), Recommended Action(M), Scan Date(N)

update_range = "'Master Job Tracker'!E189:K189"
status_val = "Applied"
note_val = "Applied via careers portal for Social Video Producer with tailored cover letter and creative showreel. (Also sent cold email to jobs@getyourguide.com ID: 1a038b654987a6cd)"
role_val = "Social Video Producer"
url_val = "https://www.getyourguide.careers/jobs/8020488#apply"

body = {'values': [[status_val, today_str, follow_up_str, note_val, 'Portal Applied', role_val, url_val]]}
service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=update_range, valueInputOption='RAW', body=body).execute()
print("Updated Master Job Tracker Row 189 for GetYourGuide Social Video Producer.")

# 2. Append/Update in local staging log
log_path = Path("Job Hunt/resumes/batch-staging-log.md")
current_log = log_path.read_text(encoding='utf-8')
staging_entry = f"| 2026-08-25 17:54 IST | GetYourGuide (Berlin) | Social Video Producer | portal (https://www.getyourguide.careers/jobs/8020488#apply) | APPLIED | `Portal Form` | `Mohd_Hayaat_Ali_GetYourGuide_Cover_Letter.pdf` | Portal Application | Tailored Cover Letter + Creative Showreel |"
new_log = current_log.rstrip() + "\n" + staging_entry + "\n"
log_path.write_text(new_log, encoding='utf-8')
print("Updated local batch-staging-log.md.")

print("GETYOURGUIDE SOCIAL VIDEO PRODUCER MARKED AS APPLIED CLEANLY!")
