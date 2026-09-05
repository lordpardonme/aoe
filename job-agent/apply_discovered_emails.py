import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Discovered contact emails & portals for Master Job Tracker rows
enrichments = {
    101: {'email': 'amsterdam@adamsrecruitment.com', 'action': 'Agency Representation Pitch', 'notes': 'Adams Multilingual Netherlands official intake'},
    102: {'email': 'talentacquisition@airswift.com', 'action': 'Direct Recruiter Outreach', 'notes': 'Airswift Global Talent Acquisition'},
    103: {'email': 'amsterdam@bluelynx.com', 'action': 'Agency Representation Pitch', 'notes': 'Blue Lynx Netherlands official intake'},
    108: {'email': 'apply@irwinanddow.com', 'action': 'Dubai Agency Talent Pitch', 'notes': 'Irwin & Dow Dubai recruitment team'},
    112: {'email': 'info@octagon.nl', 'action': 'Agency Representation Pitch', 'notes': 'Octagon Professionals Netherlands'},
    116: {'email': 'info@ravecruitment.com', 'action': 'Agency Representation Pitch', 'notes': 'Ravecruitment Netherlands'},
    119: {'email': 'info@rtc-1.com', 'action': 'Dubai Agency Talent Pitch', 'notes': 'RTC-1 Employment Services Dubai'},
    126: {'email': 'hq@undutchables.nl', 'action': 'Agency Representation Pitch', 'notes': 'Undutchables Netherlands official intake'},
    135: {'email': 'careers@almosafer.com', 'action': 'Direct Product Designer Pitch', 'notes': 'Almosafer Dubai / Saudi travel tech'},
    285: {'email': 'marcomm@acx.net', 'action': 'Direct Outreach', 'notes': 'ACX Abu Dhabi'},
    286: {'email': 'contact@addenda.ai', 'action': 'Direct 0-to-1 InsurTech Pitch', 'notes': 'Addenda Dubai AI / InsurTech'},
    290: {'email': 'info@charterhouse.ae', 'action': 'Dubai Agency Representation', 'notes': 'Charterhouse Middle East Dubai'},
    293: {'email': 'info@halian.com', 'action': 'Dubai Agency Representation', 'notes': 'Halian Middle East Dubai'},
    294: {'email': 'info@kinfitz.com', 'action': 'Dubai Agency Representation', 'notes': 'KinFitz & Co Dubai'},
    287: {'email': 'info@amwalcp.com', 'action': 'FinTech / Asset Management Pitch', 'notes': 'Amwal Capital Partners Dubai'},
    299: {'email': 'mena@welovesalt.com', 'action': 'Dubai Agency Representation', 'notes': 'Salt Recruitment Dubai / MENA'},
}

print(f"Updating {len(enrichments)} discovered email rows in Master Job Tracker...")

for row_idx, data in enrichments.items():
    # Update Email (Col C / Col 3) and Recommended Action (Col M / Col 13) and Notes (Col H / Col 8)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'Master Job Tracker'!C{row_idx}",
        valueInputOption='RAW',
        body={'values': [[data['email']]]}
    ).execute()
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'Master Job Tracker'!M{row_idx}",
        valueInputOption='RAW',
        body={'values': [[data['action']]]}
    ).execute()

print("Master Job Tracker successfully updated with discovered emails.")

# Now rebuild Priority Outreach Backlog to incorporate all enriched emails
from update_full_backlog import *
print("Refreshed Priority Outreach Backlog with newly enriched contact emails.")
