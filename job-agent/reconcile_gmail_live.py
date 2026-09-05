import sys
import io
import re
import datetime
from pathlib import Path

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
gmail_service = build('gmail', 'v1', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

print("=" * 70)
print("1. SCANNING GMAIL FOR BOUNCES, REJECTIONS, AND REPLIES")
print("=" * 70)

# --- 1A. SCAN FOR BOUNCES (Delivery Status Notifications) ---
print("\n[A] Scanning Mail Delivery Subsystems (Bounces)...")
bounce_query = 'from:mailer-daemon OR from:postmaster OR subject:"Delivery Status Notification (Failure)" OR subject:"Undeliverable"'
bounce_msgs = []
try:
    res_b = gmail_service.users().messages().list(userId='me', q=bounce_query, maxResults=100).execute()
    bounce_msgs = res_b.get('messages', [])
except Exception as e:
    print(f"Error querying bounces: {e}")

print(f"Found {len(bounce_msgs)} bounce notification messages in Gmail.")

bounces_detected = []
for item in bounce_msgs:
    msg_id = item['id']
    m = gmail_service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    snippet = m.get('snippet', '')
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    
    # Try to find failed recipient email from snippet or body
    failed_email = None
    email_matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', snippet)
    for em in email_matches:
        if 'mailer-daemon' not in em and 'googlemail' not in em and 'hayaat' not in em:
            failed_email = em
            break
            
    bounces_detected.append({
        'msg_id': msg_id,
        'subject': subject,
        'date': date,
        'failed_email': failed_email,
        'snippet': snippet[:120]
    })
    print(f"  • BOUNCE: {failed_email or 'Unknown'} | Date: {date} | Subject: {subject}")

# --- 1B. SCAN LABEL 'Job rejections' ---
print("\n[B] Scanning Label 'Job rejections'...")
rejection_msgs = []
try:
    res_r = gmail_service.users().messages().list(userId='me', labelIds=['Label_1022348670332542993'], maxResults=100).execute()
    rejection_msgs = res_r.get('messages', [])
except Exception as e:
    print(f"Error querying Job rejections label: {e}")

print(f"Found {len(rejection_msgs)} messages tagged with 'Job rejections'.")

rejections_detected = []
for item in rejection_msgs:
    msg_id = item['id']
    m = gmail_service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_header = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    snippet = m.get('snippet', '')
    
    rejections_detected.append({
        'msg_id': msg_id,
        'from': from_header,
        'subject': subject,
        'date': date,
        'snippet': snippet[:120]
    })
    print(f"  • REJECTION: {from_header} | Subject: {subject} | Date: {date}")

# --- 1C. SCAN INBOX FOR INBOUND REPLIES ---
print("\n[C] Scanning INBOX for Incoming Human/Recruiter Responses...")
inbox_msgs = []
try:
    res_i = gmail_service.users().messages().list(userId='me', q='label:INBOX -from:me', maxResults=100).execute()
    inbox_msgs = res_i.get('messages', [])
except Exception as e:
    print(f"Error querying INBOX: {e}")

print(f"Found {len(inbox_msgs)} incoming inbox messages.")

inbox_replies = []
for item in inbox_msgs:
    msg_id = item['id']
    m = gmail_service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    headers = {h['name'].lower(): h['value'] for h in m['payload'].get('headers', [])}
    from_header = headers.get('from', '')
    subject = headers.get('subject', '')
    date = headers.get('date', '')
    snippet = m.get('snippet', '')
    
    # Filter out automated marketing / security newsletters if needed
    inbox_replies.append({
        'msg_id': msg_id,
        'from': from_header,
        'subject': subject,
        'date': date,
        'snippet': snippet[:140]
    })

print(f"Processed {len(inbox_replies)} non-self inbox emails.")
for r in inbox_replies[:15]:
    print(f"  • INBOX: From: {r['from'][:40]:<40} | Subject: {r['subject'][:45]}")

print("\nScan completed successfully. Ready to cross-reference with Google Sheet.")
