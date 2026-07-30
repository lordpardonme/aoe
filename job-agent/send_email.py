import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)

service = build("gmail", "v1", credentials=creds)

message = MIMEText("This is a test email sent using the Gmail API.")
message["to"] = "hayaat0806@gmail.com"
message["from"] = "hayaat0806@gmail.com"
message["subject"] = "Gmail API Test"

raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

service.users().messages().send(
    userId="me",
    body={"raw": raw}
).execute()

print("Email sent successfully!")