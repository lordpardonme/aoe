import sys
import io
import re
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'job-agent')

from src.config import GOOGLE_SCOPES, load_google_credentials
from googleapiclient.discovery import build

creds = load_google_credentials(GOOGLE_SCOPES)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI'

enrichments_3 = {
    115: {'email': 'info@nl.randstad.com', 'action': 'Agency Representation Pitch', 'notes': 'Randstad Netherlands intake'},
    127: {'email': 'careers@2gether.ae', 'action': 'Direct Digital Agency Pitch', 'notes': '2gether Dubai'},
    129: {'email': 'accenture.middleeast@accenture.com', 'action': 'Middle East Design & Consulting', 'notes': 'Accenture UAE Middle East'},
    130: {'email': 'careers@adidas.com', 'action': 'Design & Product Innovation', 'notes': 'Adidas Germany / Global'},
    131: {'email': 'jobs@adjust.com', 'action': 'Product Analytics & UI/UX Pitch', 'notes': 'Adjust Berlin'},
    132: {'email': 'careers@adnoc.ae', 'action': 'ADNOC Digital / Energy UX Pitch', 'notes': 'ADNOC Digital Abu Dhabi'},
    133: {'email': 'recruitment.middleeast@aecom.com', 'action': 'Infrastructure & Digital Design', 'notes': 'AECOM UAE'},
    134: {'email': 'recruitment@alfuttaim.com', 'action': 'Automotive & Retail Digital UX', 'notes': 'Al Futtaim Group Dubai'},
    136: {'email': 'alshayajobs@alshaya.com', 'action': 'E-Commerce & Retail Digital UX', 'notes': 'Alshaya Group Dubai'},
    138: {'email': 'recruitment@arkonline.org', 'action': 'EdTech & Educational Platforms UX', 'notes': 'ARK Schools UK'},
    142: {'email': 'recrutement@atrya.fr', 'action': 'European Digital Products UX', 'notes': 'Atrya Germany / France'},
    143: {'email': 'careers@bayer.com', 'action': 'HealthTech & Life Sciences UX', 'notes': 'Bayer Germany'},
    145: {'email': 'jobs@blinkist.com', 'action': 'Consumer Microlearning App UX', 'notes': 'Blinkist Berlin'},
    146: {'email': 'careers@bmwgroup.com', 'action': 'Automotive In-Car & Mobile UX', 'notes': 'BMW Group Germany'},
    149: {'email': 'recruitment.uk@capgemini.com', 'action': 'Enterprise Digital Transformation', 'notes': 'Capgemini UK'},
    150: {'email': 'recruitment@carrefouruae.com', 'action': 'Omnichannel Grocery & E-commerce UX', 'notes': 'Carrefour UAE / Majid Al Futtaim'},
    151: {'email': 'careers@celonis.com', 'action': 'Process Mining & Enterprise SaaS UX', 'notes': 'Celonis India / Munich'},
    152: {'email': 'careers@chalhoub.com', 'action': 'Luxury E-Commerce & Retail Digital UX', 'notes': 'Chalhoub Group Dubai'},
    153: {'email': 'jobs@choco.com', 'action': 'F&B Marketplace & Supply Chain UX', 'notes': 'Choco Berlin'},
    154: {'email': 'careers@contentful.com', 'action': 'Composable Content Platform UI/UX', 'notes': 'Contentful Berlin'},
    155: {'email': 'hello@crafty.ae', 'action': 'Creative Design & Brand UI/UX', 'notes': 'Crafty Dubai'},
    156: {'email': 'hr@daralshifa.com', 'action': 'Hospital & Patient Care Digital UX', 'notes': 'Dar Al Shifa Hospitals Dubai'},
    158: {'email': 'jobs@deepl.com', 'action': 'AI & Machine Translation UI/UX', 'notes': 'DeepL Germany'},
    163: {'email': 'recruitment@du.ae', 'action': 'Telco & Self-Service Mobile App UX', 'notes': 'du Telecom UAE'},
    166: {'email': 'Customer.Service@ddf.ae', 'action': 'Travel Retail & Airport Shopping UX', 'notes': 'Dubai Duty Free'},
    167: {'email': 'HRRecruitment@dha.gov.ae', 'action': 'Public Healthcare & Government UX', 'notes': 'Dubai Health Authority'},
    169: {'email': 'mail@dubaipolice.gov.ae', 'action': 'Smart Police & Public Safety Services UX', 'notes': 'Dubai Police'},
    174: {'email': 'careers@etihad.ae', 'action': 'Aviation & Passenger Journey UX', 'notes': 'Etihad Airways Abu Dhabi'},
    177: {'email': 'info@evoqdxb.ae', 'action': 'PropTech & Luxury Real Estate UX', 'notes': 'EVOQ Dubai'},
    179: {'email': 'jobs@exmox.com', 'action': 'Mobile Gaming & Advertising Tech UX', 'notes': 'exmox Hamburg'},
    182: {'email': 'jobs@finn.com', 'action': 'Car Subscription & Consumer Mobility UX', 'notes': 'FINN Munich'},
    183: {'email': 'jobs@flixbus.com', 'action': 'Intercity Travel & Booking Engine UX', 'notes': 'Flix / FlixBus Munich'},
    185: {'email': 'customercare@flyin.com', 'action': 'Online Travel Agency & Booking UX', 'notes': 'Flyin Dubai / Saudi'},
    187: {'email': 'careers@forto.com', 'action': 'Digital Freight Forwarding & Logistics UX', 'notes': 'Forto Berlin'},
    188: {'email': 'careers@g42.ai', 'action': 'AI & Sovereign Cloud Digital Platforms UX', 'notes': 'G42 Abu Dhabi'},
    189: {'email': 'jobs@getyourguide.com', 'action': 'Travel Experiences & Marketplace UX', 'notes': 'GetYourGuide Berlin'},
    191: {'email': 'talent@helsing.ai', 'action': 'AI & Defense Technology UI/UX', 'notes': 'Helsing Munich'},
    197: {'email': 'careers.me@ibm.com', 'action': 'Enterprise AI & Cloud Consulting UX', 'notes': 'IBM Middle East Dubai'},
    198: {'email': 'careers@infineon.com', 'action': 'Semiconductors & IoT Platforms UX', 'notes': 'Infineon Munich'},
    201: {'email': 'jobs@kaufland-ecommerce.com', 'action': 'E-Commerce Marketplace & Checkout UX', 'notes': 'Kaufland e-commerce Germany'},
    203: {'email': 'jobs@kombo.co', 'action': 'Travel Booking & Multi-modal Transit UX', 'notes': 'Kombo Germany'},
    205: {'email': 'contact@leantech.me', 'action': 'Open Banking & API Developer Portal UX', 'notes': 'Lean Technologies Dubai'},
    207: {'email': 'info@lilium.com', 'action': 'eVTOL Jet & Urban Air Mobility UX', 'notes': 'Lilium Munich'},
    208: {'email': 'info@lillydoo.com', 'action': 'D2C Subscription & Baby Care App UX', 'notes': 'LILLYDOO Frankfurt'},
    210: {'email': 'recruitment@lloydsbanking.com', 'action': 'Corporate & Retail Banking UX', 'notes': 'Lloyds Banking Group UK'},
    212: {'email': 'careers@lhsystems.com', 'action': 'Aviation IT & Airline Operations UX', 'notes': 'Lufthansa Systems Germany'},
    213: {'email': 'careers@maf.ae', 'action': 'Retail, Leisure & SuperApp Digital UX', 'notes': 'Majid Al Futtaim Dubai'},
    214: {'email': 'jobs@mambo.co', 'action': 'Digital Products & Scaleup UX', 'notes': 'Mambo Germany'},
    216: {'email': 'careers@mangopay.com', 'action': 'Payment Infrastructure & Marketplace UX', 'notes': 'Mangopay MENA / Dubai'},
    220: {'email': 'careers@medivet.co.uk', 'action': 'Veterinary Practice & Booking UX', 'notes': 'Medivet UK'},
    221: {'email': 'careers.india@merckgroup.com', 'action': 'Healthcare & Life Sciences Platforms UX', 'notes': 'Merck India'},
    224: {'email': 'careers@msquire.co.uk', 'action': 'IT Consulting & Digital Transformation UX', 'notes': 'MSQUIRE IT Services UK'},
    227: {'email': 'careers.me@nestle.com', 'action': 'FMCG Digital Platforms & Consumer UX', 'notes': 'Nestle Middle East Dubai'},
    232: {'email': 'jobs@omio.com', 'action': 'Multi-modal Travel & Ticketing App UX', 'notes': 'Omio Berlin'},
    236: {'email': 'careers@personio.de', 'action': 'HR Management SaaS & Employee Experience UX', 'notes': 'Personio Munich'},
    238: {'email': 'careers@presight.ai', 'action': 'Big Data Analytics & AI Dashboards UX', 'notes': 'Presight AI Abu Dhabi'},
    239: {'email': 'careers.im@pg.com', 'action': 'Consumer Goods Brand & Retail UX', 'notes': 'Procter & Gamble UAE'},
    241: {'email': 'support@pyypl.com', 'action': 'Prepaid Card & Remittance FinTech UX', 'notes': 'Pyypl Dubai'},
    244: {'email': 'design.talent@remotehub.io', 'action': 'Remote Product Design Mandates', 'notes': 'Remote Design Collective'},
    245: {'email': 'jobs@remotework.io', 'action': 'Global Remote Product Design', 'notes': 'Remote Job Platform'},
    247: {'email': 'careers@rotana.com', 'action': 'Hospitality & Luxury Booking Engine UX', 'notes': 'Rotana Hotels Dubai'},
    249: {'email': 'careers@sap.com', 'action': 'Enterprise Software & Fiori Design Systems UX', 'notes': 'SAP Germany'},
    254: {'email': 'careers@siemens.com', 'action': 'Industrial IoT & Digital Enterprise UX', 'notes': 'Siemens Germany'},
    257: {'email': 'jobs@solarisgroup.com', 'action': 'Embedded Finance & BaaS Platform UX', 'notes': 'Solaris Berlin'},
    259: {'email': 'jobs@sonarsource.com', 'action': 'Developer Tools & Code Quality UI/UX', 'notes': 'SonarSource Germany'},
    260: {'email': 'shoppersupport@spotii.me', 'action': 'BNPL Checkout & Merchant Portal UX', 'notes': 'Spotii Dubai'},
    265: {'email': 'jobs@sumup.com', 'action': 'POS Hardware & Merchant Payments Mobile UX', 'notes': 'SumUp Berlin'},
    267: {'email': 'help@tabby.ai', 'action': 'Buy Now Pay Later Consumer & Merchant UX', 'notes': 'Tabby Dubai'},
    276: {'email': 'unilever.recruitment@unilever.com', 'action': 'FMCG Digital Brand & E-Commerce UX', 'notes': 'Unilever Gulf Dubai'},
    277: {'email': 'careers@volkswagen.de', 'action': 'Automotive Connected Car & Digital Cockpit UX', 'notes': 'Volkswagen Group Germany'},
    278: {'email': 'info@volocopter.com', 'action': 'Urban Air Mobility & Passenger Booking UX', 'notes': 'Volocopter Germany'},
    281: {'email': 'care@wio.io', 'action': 'Next-Gen Digital Banking App UX', 'notes': 'Wio Bank Abu Dhabi'},
    282: {'email': 'jobs@wolt.com', 'action': 'Food Delivery & Local Commerce Mobile UX', 'notes': 'Wolt Germany'},
    284: {'email': 'help@yap.com', 'action': 'Digital Banking & Mobile Wallet UX', 'notes': 'YAP Dubai'},
    288: {'email': 'hello@caliberly.com', 'action': 'Dubai Recruitment Agency Representation', 'notes': 'Caliberly Dubai'},
    289: {'email': 'info@cander.me', 'action': 'Executive Search & Tech Talent Pitch', 'notes': 'Cander Dubai'},
    291: {'email': 'info@cooperfitch.ae', 'action': 'Dubai Recruitment Agency Representation', 'notes': 'Cooper Fitch Dubai'},
    292: {'email': 'info@greengage.co', 'action': 'Sustainability & Digital Advisory UX', 'notes': 'Greengage Dubai'},
    295: {'email': 'info@masdar.ae', 'action': 'Clean Energy & Smart City Platforms UX', 'notes': 'Masdar Abu Dhabi'},
    296: {'email': 'hello@million.co', 'action': 'Creative & Digital Experience Pitch', 'notes': 'Million Dubai'},
    298: {'email': 'hello@petty.ae', 'action': 'PetCare E-Commerce & Service Mobile UX', 'notes': 'Petty Dubai'},
    300: {'email': 'info@sheisarab.com', 'action': 'Social Enterprise & Platform UI/UX', 'notes': 'She is Arab Dubai'},
    306: {'email': 'work@mushroomstudios.in', 'action': 'Video Editing & Creative Lead Pitch', 'notes': 'Creative Video Lead Verified'}
}

# 1. Read entire Master Job Tracker in 1 single call
res = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Master Job Tracker'!A1:N").execute()
rows = res.get('values', [])
headers = rows[0]
data = rows[1:]

print(f"Read {len(data)} rows from Master Job Tracker.")

# 2. Update rows in memory
updated_count = 0
for idx, r in enumerate(data):
    row_num = idx + 2 # sheet row number
    if row_num in enrichments_3:
        info = enrichments_3[row_num]
        # Pad row to 14
        r = r + [''] * (14 - len(r))
        r[2] = info['email'] # Column C (Email)
        r[12] = info['action'] # Column M (Recommended Action)
        data[idx] = r
        updated_count += 1

print(f"Updated {updated_count} rows in memory.")

# 3. Write ALL rows back to Master Job Tracker in ONE SINGLE CALL
all_data = [headers] + data
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=f"'Master Job Tracker'!A1:N{len(all_data)}",
    valueInputOption='RAW',
    body={'values': all_data}
).execute()

print("Master Job Tracker 100% updated in 1 single write call.")

# 4. Rebuild Priority Outreach Backlog in ONE call
backlog_rows = []
priority_counter = 1

for r in data:
    r = r + [''] * (14 - len(r))
    country, comp, email, l_type, status, dt_app, dt_foll, notes, scan_st, role, url, conf, rec_act, dt_scan = r
    if status.strip().lower() == 'to contact':
        backlog_rows.append([
            priority_counter,
            'Master Tracker Backlog',
            country or 'India',
            comp,
            email.strip(),
            l_type or 'Direct Employer',
            role or 'Product / UI-UX Designer',
            'To Contact',
            rec_act or 'Direct Tailored Pitch',
            notes
        ])
        priority_counter += 1

# Append August batches
res_ag = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'Agencies Aug 2026'!A2:J").execute()
for r in res_ag.get('values', []):
    r = r + [''] * (10 - len(r))
    backlog_rows.append([priority_counter, 'Agencies Aug 2026', 'India / Global', r[0], r[2], r[1], r[3], 'To Contact', 'Agency Talent Representation', r[9]])
    priority_counter += 1

res_yc = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'YC Startups Aug 2026'!A2:J").execute()
for r in res_yc.get('values', []):
    r = r + [''] * (10 - len(r))
    backlog_rows.append([priority_counter, 'YC Startups Aug 2026', 'US / Global (Remote)', r[0], r[2], 'YC Tech Startup', r[3], 'To Contact', '0-to-1 Product Design Velocity Pitch', r[9]])
    priority_counter += 1

res_it = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range="'IT Services Aug 2026'!A2:J").execute()
for r in res_it.get('values', []):
    r = r + [''] * (10 - len(r))
    backlog_rows.append([priority_counter, 'IT Services Aug 2026', 'India', r[0], r[2], 'IT Services & Software', r[3], 'To Contact', 'Enterprise UI/UX Pitch', r[9]])
    priority_counter += 1

# Write Priority Outreach Backlog in ONE call
backlog_all = [['# Priority', 'Source Queue', 'Country / Region', 'Company / Target', 'Email Address', 'Type / Category', 'Contact Person / Role', 'Status', 'Recommended Pitch', 'Notes']] + backlog_rows

service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range="'Priority Outreach Backlog'!A1:Z2000").execute()
service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range="'Priority Outreach Backlog'!A1",
    valueInputOption='RAW',
    body={'values': backlog_all}
).execute()

print(f"Priority Outreach Backlog 100% updated with {len(backlog_rows)} rows in 1 single call.")
