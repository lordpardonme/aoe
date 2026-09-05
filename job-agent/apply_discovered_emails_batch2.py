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

# Newly discovered high-value verified emails
enrichments_2 = {
    144: {'email': 'careers@mamopay.com', 'action': 'Direct FinTech Pitch', 'notes': 'Mamo Pay Dubai'},
    157: {'email': 'info@dastn.com', 'action': 'Direct Talent Pitch', 'notes': 'DastN Berlin'},
    160: {'email': 'talent@distribusion.com', 'action': 'Direct Travel Tech Pitch', 'notes': 'Distribusion Berlin'},
    170: {'email': 'bayutdubizzle@jobs.workablemail.com', 'action': 'Direct Tech Recruitment', 'notes': 'Dubizzle / Bayut Group Dubai'},
    181: {'email': 'fetchr@jobs.workablemail.com', 'action': 'Direct Logistics Tech Pitch', 'notes': 'Fetchr Dubai'},
    186: {'email': 'foodics@jobs.workablemail.com', 'action': 'Direct F&B Tech Pitch', 'notes': 'Foodics Dubai'},
    202: {'email': 'kitopi@jobs.workablemail.com', 'action': 'Direct Cloud Kitchens Pitch', 'notes': 'Kitopi Dubai'},
    215: {'email': 'careers@mamopay.com', 'action': 'Direct FinTech Pitch', 'notes': 'Mamo Pay Dubai'},
    230: {'email': 'recruitment@nowmoney.me', 'action': 'Direct FinTech Pitch', 'notes': 'NOW Money Dubai'},
    231: {'email': 'careers@nymcard.com', 'action': 'Direct Banking-as-a-Service Pitch', 'notes': 'NymCard Dubai'},
    243: {'email': 'jobs@raisin.com', 'action': 'Direct FinTech Pitch', 'notes': 'Raisin Berlin'},
    251: {'email': 'careers@sarwa.co', 'action': 'Direct WealthTech Pitch', 'notes': 'Sarwa Dubai'},
    261: {'email': 'contact@getstake.com', 'action': 'Direct PropTech Pitch', 'notes': 'Stake Dubai'},
    266: {'email': 'swvl@jobs.workablemail.com', 'action': 'Direct Mobility Tech Pitch', 'notes': 'Swvl Dubai'},
    270: {'email': 'talentacquistion@taxfix.de', 'action': 'Direct FinTech Pitch', 'notes': 'Taxfix Berlin'},
    272: {'email': 'recruitment@transguardgroup.com', 'action': 'Dubai Recruitment Team', 'notes': 'Transguard Group Dubai'},
    273: {'email': 'info@truechart.com', 'action': 'Direct Enterprise BI Pitch', 'notes': 'TRUECHART Germany'},
    274: {'email': 'career@trukker.com', 'action': 'Direct Logistics Tech Pitch', 'notes': 'Trukker Dubai'},
    283: {'email': 'careers@yallacompare.com', 'action': 'Direct FinTech Pitch', 'notes': 'Yallacompare Dubai'},
    302: {'email': 'hi@sparklo.com', 'action': 'Direct CleanTech Pitch', 'notes': 'Sparklo Dubai'},
    304: {'email': 'hello@umatr.io', 'action': 'Direct Tech Recruitment', 'notes': 'UMATR Dubai'}
}

print(f"Updating {len(enrichments_2)} newly discovered scaleup/fintech emails in Master Job Tracker...")

for row_idx, data in enrichments_2.items():
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

print("Master Job Tracker successfully updated with Batch 2 discovered emails.")

# Rebuild Priority Outreach Backlog
from update_full_backlog import *
print("Refreshed Priority Outreach Backlog with newly enriched emails.")
