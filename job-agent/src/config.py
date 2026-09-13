"""Runtime configuration and Google credential loading.

All settings come from environment variables (loaded from ``.env``) with sane
defaults.  Paths are resolved relative to the project root so the app can be run
from anywhere.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Well-known locations -------------------------------------------------
# ``config.py`` lives at <root>/src/config.py, so the project root is two up.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

TEMPLATES_DIR: Path = PROJECT_ROOT / "templates"
GENERATED_DIR: Path = PROJECT_ROOT / "generated"
RESUMES_DIR: Path = GENERATED_DIR / "resumes"
COVERLETTERS_DIR: Path = GENERATED_DIR / "coverletters"
EMAILS_DIR: Path = GENERATED_DIR / "emails"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
TRACKER_DIR: Path = PROJECT_ROOT / "tracker"
MASTER_RESUME: Path = PROJECT_ROOT / "master_resume.docx"

# OAuth scopes required across Gmail + Sheets + Drive.
GOOGLE_SCOPES: List[str] = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]


class Settings(BaseSettings):
    """Strongly-typed application settings sourced from ``.env``."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Google auth
    google_credentials_file: str = "credentials.json"
    google_token_file: str = "token.json"

    # Sheets tracker
    tracker_spreadsheet_id: str = ""
    tracker_sheet_name: str = "Applications"

    # Candidate identity
    candidate_name: str = ""
    candidate_email: str = ""
    candidate_phone: str = ""
    candidate_location: str = ""
    candidate_portfolio: str = ""
    candidate_linkedin: str = ""

    # Email
    sender_email: str = ""
    default_recipient: str = ""

    # Environment & Deployment
    app_env: str = "production"  # "uat", "staging", "production"
    port: int = 8000
    db_name: str = ""

    # Behaviour
    dry_run: bool = True
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0

    # --- Derived, absolute paths -----------------------------------------
    @property
    def credentials_path(self) -> Path:
        return _resolve(self.google_credentials_file)

    @property
    def token_path(self) -> Path:
        return _resolve(self.google_token_file)

    def ensure_dirs(self) -> None:
        """Create every runtime output directory if missing."""
        for directory in (
            TEMPLATES_DIR,
            RESUMES_DIR,
            COVERLETTERS_DIR,
            EMAILS_DIR,
            LOGS_DIR,
            TRACKER_DIR,
        ):
            directory.mkdir(parents=True, exist_ok=True)


def _resolve(value: str) -> Path:
    """Resolve *value* against the project root if it is not already absolute."""
    path = Path(value)
    return path if path.is_absolute() else (PROJECT_ROOT / path)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    settings = Settings()
    settings.ensure_dirs()
    return settings


def load_google_credentials(scopes: Optional[List[str]] = None):
    """Load, refresh and return Google OAuth credentials.

    Reads ``token.json`` (produced by ``authenticate.py``), transparently
    refreshing it when expired.  Import of Google libraries is deferred so the
    rest of the app (and the offline test suite) works without them installed.

    Raises:
        FileNotFoundError: if the token file does not exist yet.
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    settings = get_settings()
    scopes = scopes or GOOGLE_SCOPES
    token_path = settings.token_path

    if not token_path.exists():
        raise FileNotFoundError(
            f"Google token not found at {token_path}. "
            "Run `python authenticate.py` first to authorise the app."
        )

    creds = Credentials.from_authorized_user_file(str(token_path), scopes)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            token_path.write_text(creds.to_json(), encoding="utf-8")
        else:  # pragma: no cover - requires interactive re-auth
            raise RuntimeError(
                "Google credentials are invalid and cannot be refreshed. "
                "Re-run `python authenticate.py`."
            )
    return creds
