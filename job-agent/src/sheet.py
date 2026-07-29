"""Google Sheets application tracker (with a local CSV mirror)."""

from __future__ import annotations

import csv
from datetime import date as _date
from pathlib import Path
from typing import List, Optional

from .config import GOOGLE_SCOPES, TRACKER_DIR, get_settings, load_google_credentials
from .logger import get_logger
from .utils import retry

log = get_logger("sheet")

HEADER: List[str] = ["Date", "Company", "Role", "Status", "URL", "Resume", "Notes"]
LOCAL_TRACKER = TRACKER_DIR / "applications.csv"


class SheetClient:
    """Append application rows to a Google Sheet, mirroring to a local CSV."""

    def __init__(self) -> None:
        self._service = None
        self._settings = get_settings()
        self._spreadsheet_id = self._settings.tracker_spreadsheet_id or ""

    # --- service ---------------------------------------------------------
    @property
    def service(self):
        if self._service is None:
            from googleapiclient.discovery import build

            creds = load_google_credentials(GOOGLE_SCOPES)
            self._service = build("sheets", "v4", credentials=creds)
            log.info("Sheets service initialised")
        return self._service

    @property
    def sheet_name(self) -> str:
        return self._settings.tracker_sheet_name

    # --- spreadsheet lifecycle ------------------------------------------
    @retry(attempts=3, backoff_seconds=2.0)
    def _create_spreadsheet(self) -> str:
        body = {
            "properties": {"title": "Job Agent — Application Tracker"},
            "sheets": [{"properties": {"title": self.sheet_name}}],
        }
        result = self.service.spreadsheets().create(
            body=body, fields="spreadsheetId"
        ).execute()
        sid = result["spreadsheetId"]
        log.info("Created new tracker spreadsheet id=%s", sid)
        self._write_header(sid)
        return sid

    def _ensure_spreadsheet(self) -> Optional[str]:
        """Return a usable spreadsheet id, creating one if needed.

        In dry-run mode we never create/modify remote sheets.
        """
        if self._spreadsheet_id:
            return self._spreadsheet_id
        if self._settings.dry_run:
            log.warning(
                "DRY_RUN + no TRACKER_SPREADSHEET_ID — skipping remote sheet "
                "(local CSV still updated)."
            )
            return None
        self._spreadsheet_id = self._create_spreadsheet()
        log.warning(
            "Created a tracker spreadsheet. Add this to your .env to reuse it: "
            "TRACKER_SPREADSHEET_ID=%s",
            self._spreadsheet_id,
        )
        return self._spreadsheet_id

    @retry(attempts=3, backoff_seconds=2.0)
    def _write_header(self, sid: str) -> None:
        self.service.spreadsheets().values().update(
            spreadsheetId=sid,
            range=f"{self.sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": [HEADER]},
        ).execute()

    def _ensure_header(self, sid: str) -> None:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=sid, range=f"{self.sheet_name}!A1:G1"
        ).execute()
        if not result.get("values"):
            self._write_header(sid)

    # --- public API ------------------------------------------------------
    def update_tracker(
        self,
        company: str,
        role: str,
        url: str,
        date: Optional[str] = None,
        resume: str = "",
        status: str = "Applied",
        notes: str = "",
    ) -> dict:
        """Append one application row to the tracker (and local CSV).

        Returns a small status dict describing what happened.
        """
        date = date or _date.today().isoformat()
        row = [date, company, role, status, url or "", resume or "", notes or ""]

        # Always record locally first — this never fails on network issues.
        self._append_local(row)

        sid = self._ensure_spreadsheet()
        if sid is None:
            return {"remote": False, "local": True, "reason": "dry_run_or_no_id"}

        self._ensure_header(sid)
        self._append_remote(sid, row)
        return {"remote": True, "local": True, "spreadsheet_id": sid}

    @retry(attempts=3, backoff_seconds=2.0)
    def _append_remote(self, sid: str, row: List[str]) -> None:
        self.service.spreadsheets().values().append(
            spreadsheetId=sid,
            range=f"{self.sheet_name}!A1",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": [row]},
        ).execute()
        log.info("Appended application row to spreadsheet %s", sid)

    def _append_local(self, row: List[str]) -> Path:
        LOCAL_TRACKER.parent.mkdir(parents=True, exist_ok=True)
        new_file = not LOCAL_TRACKER.exists()
        with LOCAL_TRACKER.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            if new_file:
                writer.writerow(HEADER)
            writer.writerow(row)
        log.info("Recorded application locally -> %s", LOCAL_TRACKER)
        return LOCAL_TRACKER
