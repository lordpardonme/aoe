"""Shared helper utilities: slugify, retry decorator, safe file writes."""

from __future__ import annotations

import functools
import re
import time
import unicodedata
from pathlib import Path
from typing import Callable, Iterable, Tuple, Type, TypeVar

from .logger import get_logger

log = get_logger("utils")

T = TypeVar("T")


def slugify(value: str, *, max_length: int = 60) -> str:
    """Turn an arbitrary string into a filesystem-safe snake_case slug.

    ``"Trinity Consulting, Inc."`` -> ``"trinity_consulting_inc"``.
    Falls back to ``"unknown"`` for empty input.
    """
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    value = re.sub(r"_+", "_", value)
    if len(value) > max_length:
        value = value[:max_length].rstrip("_")
    return value or "unknown"


def retry(
    *,
    attempts: int = 3,
    backoff_seconds: float = 2.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that retries a function with linear back-off.

    Args:
        attempts: total number of tries (>= 1).
        backoff_seconds: base delay, multiplied by the attempt index.
        exceptions: exception types that should trigger a retry.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exc: BaseException | None = None
            for attempt in range(1, max(1, attempts) + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # noqa: PERF203 - retry is the point
                    last_exc = exc
                    if attempt >= attempts:
                        log.error(
                            "%s failed after %d attempt(s): %s",
                            func.__name__,
                            attempt,
                            exc,
                        )
                        raise
                    delay = backoff_seconds * attempt
                    log.warning(
                        "%s failed (attempt %d/%d): %s — retrying in %.1fs",
                        func.__name__,
                        attempt,
                        attempts,
                        exc,
                        delay,
                    )
                    time.sleep(delay)
            # Unreachable, but keeps type checkers happy.
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


def write_text(path: Path, content: str) -> Path:
    """Write UTF-8 text, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    log.info("Wrote %s (%d chars)", path, len(content))
    return path


def unique_terms(terms: Iterable[str]) -> list[str]:
    """De-duplicate while preserving first-seen order (case-insensitive)."""
    seen: set[str] = set()
    out: list[str] = []
    for term in terms:
        key = term.lower().strip()
        if key and key not in seen:
            seen.add(key)
            out.append(term.strip())
    return out
