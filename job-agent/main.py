"""Job Agent entrypoint.

Usage:
    python main.py apply --url <URL>
    python main.py apply --file jd.txt
    python main.py resume --file jd.txt
    python main.py email  --file jd.txt
    python main.py tracker --company Acme --role "Product Designer"
    python main.py send   --file jd.txt --to hiring@acme.com
    python main.py test
"""

from __future__ import annotations

from src.cli import app

if __name__ == "__main__":
    app()
