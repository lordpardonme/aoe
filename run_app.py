#!/usr/bin/env python3
"""Job Hunt Studio — Localhost Launcher.

Runs the local FastAPI backend server and automatically opens the browser UI.
Auto-detects and uses the project virtual environment (job-agent/.venv) even if
called from system Python.

Usage:
    python run_app.py
    python run_app.py --port 8080 --no-browser
"""

import os
import sys
import subprocess
from pathlib import Path

# --- 1. Smart Virtual Environment Auto-Detection ---
ROOT_DIR = Path(__file__).resolve().parent
AGENT_VENV_PY = ROOT_DIR / "job-agent" / ".venv" / "Scripts" / "python.exe"
ROOT_VENV_PY = ROOT_DIR / ".venv" / "Scripts" / "python.exe"

# If current python is not the venv python and a venv exists, auto-relaunch with venv python!
current_py = Path(sys.executable).resolve()
target_py = None

if AGENT_VENV_PY.exists() and current_py != AGENT_VENV_PY.resolve():
    target_py = AGENT_VENV_PY
elif ROOT_VENV_PY.exists() and current_py != ROOT_VENV_PY.resolve():
    target_py = ROOT_VENV_PY

if target_py and not os.environ.get("__REEXEC_VENV__"):
    os.environ["__REEXEC_VENV__"] = "1"
    try:
        sys.exit(subprocess.call([str(target_py), *sys.argv]))
    except Exception as err:
        print(f"Failed to auto-switch to virtualenv ({err}); continuing with current Python...")

# --- 2. Setup paths and imports ---
import argparse
import threading
import time
import webbrowser

JOB_AGENT_DIR = ROOT_DIR / "job-agent"
if str(JOB_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(JOB_AGENT_DIR))

try:
    import uvicorn
    from src.web.app import app
except ImportError as e:
    print(f"\033[91mError: Missing dependencies ({e})\033[0m")
    print("Please install requirements using the project virtualenv:")
    print("    cd job-agent && .venv\\Scripts\\pip.exe install -r requirements.txt fastapi uvicorn pyyaml reportlab")
    sys.exit(1)


def open_browser(url: str, delay: float = 1.2):
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Job Hunt Studio — Localhost Web App")
    parser.add_argument("--env", choices=["uat", "staging", "production"], default=os.getenv("APP_ENV", "production"), help="Target runtime environment (uat, staging, production)")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=None, help="Port number (defaults: uat=8001, staging=8002, production=8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open web browser automatically")
    args = parser.parse_args()

    # Load environment file
    env = args.env.lower()
    os.environ["APP_ENV"] = env
    env_file = ROOT_DIR / f".env.{env}"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    default_ports = {"uat": 8001, "staging": 8002, "production": 8000}
    port = args.port or int(os.getenv("PORT", default_ports.get(env, 8000)))

    url = f"http://{args.host}:{port}"
    env_badges = {
        "uat": "[UAT ORBIT - ISOLATED DB]",
        "staging": "[STAGING ORBIT - PRE-PROD]",
        "production": "[PRODUCTION ORBIT - LIVE]"
    }
    badge = env_badges.get(env, "[CUSTOM ORBIT]")

    print("=" * 65)
    print(f"  [+] CAREERHERO STUDIO -- {badge}")
    print(f"  Starting local server at: {url}")
    print(f"  Environment: {env.upper()} | DB Target: {os.getenv('DB_NAME', f'jobhunt_{env}.db')}")
    print("  Press Ctrl+C at any time to stop the server.")
    print("=" * 65 + "\n")

    if not args.no_browser:
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()

    uvicorn.run(app, host=args.host, port=port, log_level="info")


if __name__ == "__main__":
    main()
