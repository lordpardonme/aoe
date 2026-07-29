"""Central logging configuration.

Every action is written to ``logs/app.log`` (INFO+) and every error to
``logs/error.log`` (ERROR+).  A :class:`rich.logging.RichHandler` mirrors output
to the console for interactive use.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from .config import LOGS_DIR

_CONSOLE = Console(stderr=True)
_CONFIGURED = False

APP_LOG = LOGS_DIR / "app.log"
ERROR_LOG = LOGS_DIR / "error.log"

_FILE_FORMAT = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _configure_root() -> None:
    """Attach file + console handlers to the ``job_agent`` root logger once."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger("job_agent")
    root.setLevel(logging.DEBUG)
    root.propagate = False

    # All actions -> app.log
    app_handler = RotatingFileHandler(
        APP_LOG, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(_FILE_FORMAT)

    # Errors only -> error.log
    error_handler = RotatingFileHandler(
        ERROR_LOG, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(_FILE_FORMAT)

    # Human-friendly console output
    console_handler = RichHandler(
        console=_CONSOLE,
        show_time=True,
        show_path=False,
        rich_tracebacks=True,
        markup=False,
    )
    console_handler.setLevel(logging.INFO)

    root.addHandler(app_handler)
    root.addHandler(error_handler)
    root.addHandler(console_handler)
    _CONFIGURED = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a namespaced child of the configured ``job_agent`` logger."""
    _configure_root()
    return logging.getLogger("job_agent" if not name else f"job_agent.{name}")


def get_console() -> Console:
    """Return the shared :class:`rich.console.Console` for pretty CLI output."""
    return _CONSOLE
