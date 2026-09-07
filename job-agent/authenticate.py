from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

import json

creds = None
existing_scopes = []

if os.path.exists("token.json"):
    try:
        with open("token.json", "r") as f:
            existing_scopes = json.load(f).get("scopes", [])
    except Exception:
        pass
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

scopes_match = creds and set(SCOPES).issubset(set(existing_scopes))

if not creds or not creds.valid or not scopes_match:
    refreshed = False
    if creds and creds.expired and creds.refresh_token and scopes_match:
        try:
            creds.refresh(Request())
            refreshed = True
        except RefreshError:
            print("Stored refresh token was revoked/expired — re-authorizing in browser.")

    if not refreshed:
        print("Starting OAuth server. Opening browser for authorization...", flush=True)
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0, open_browser=True)

    with open("token.json", "w") as token:
        token.write(creds.to_json())

print("Authentication successful!")