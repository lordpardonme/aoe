import sys
import io
import re
import urllib.parse
import urllib.request
import json
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

# Target batch 1 of 20 companies
batch_1_targets = [
    {'row': 101, 'company': 'Adams Multilingual', 'country': 'Netherlands'},
    {'row': 102, 'company': 'Airswift', 'country': 'Netherlands'},
    {'row': 103, 'company': 'Blue Lynx', 'country': 'Netherlands'},
    {'row': 108, 'company': 'Irwin & Dow', 'country': 'UAE / Dubai'},
    {'row': 112, 'company': 'Octagon Professionals', 'country': 'Netherlands'},
    {'row': 115, 'company': 'Randstad', 'country': 'Netherlands'},
    {'row': 116, 'company': 'Ravecruitment', 'country': 'Netherlands'},
    {'row': 119, 'company': 'RTC-1 Employment Services', 'country': 'UAE / Dubai'},
    {'row': 126, 'company': 'Undutchables', 'country': 'Netherlands'},
    {'row': 127, 'company': '2gether', 'country': 'UAE / Dubai'},
    {'row': 129, 'company': 'Accenture UAE', 'country': 'UAE / Dubai'},
    {'row': 130, 'company': 'Adidas', 'country': 'Germany'},
    {'row': 131, 'company': 'Adjust', 'country': 'Germany'},
    {'row': 132, 'company': 'ADNOC Digital', 'country': 'UAE / Dubai'},
    {'row': 133, 'company': 'AECOM UAE', 'country': 'UAE / Dubai'},
    {'row': 134, 'company': 'Al Futtaim Group', 'country': 'UAE / Dubai'},
    {'row': 135, 'company': 'Almosafer', 'country': 'UAE / Dubai'},
    {'row': 136, 'company': 'Alshaya Group', 'country': 'UAE / Dubai'},
    {'row': 138, 'company': 'ARK Schools', 'country': 'United Kingdom'},
    {'row': 142, 'company': 'Atrya', 'country': 'Germany'}
]

print(f"Starting discovery for {len(batch_1_targets)} targets...")

# We can query DuckDuckGo HTML or use direct known recruiter patterns
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

discovered_emails = {}

for target in batch_1_targets:
    comp = target['company']
    row = target['row']
    country = target['country']
    query = f'"{comp}" recruitment OR HR OR careers email {country}'
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    found_email = None
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for mailto: or email regex
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', html)
            valid = []
            for em in emails:
                em_l = em.lower()
                if not any(k in em_l for k in ['duckduckgo', 'yandex', 'google', 'example', 'domain', 'w3.org', 'sentry', 'schema.org']):
                    valid.append(em_l)
            if valid:
                found_email = valid[0]
    except Exception as e:
        print(f"Search error for {comp}: {e}")
        
    print(f"Row {row:3d} | {comp:<30} -> {found_email or '[Manual search needed]'}")
    discovered_emails[row] = found_email
    time.sleep(1)

print("\nDone initial scan.")
