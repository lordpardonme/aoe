#!/usr/bin/env python3
"""CareerHero Studio — Full-Stack Environment & Release Manager.

Provides professional lifecycle controls for switching environments (UAT, Staging, Production),
enforcing test verification gates, and promoting releases safely.

Usage:
    python manage_env.py status
    python manage_env.py switch [uat|staging|production]
    python manage_env.py test
    python manage_env.py promote [uat->staging|staging->production]
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
AGENT_DIR = ROOT_DIR / "job-agent"
VENV_PYTHON = AGENT_DIR / ".venv" / "Scripts" / "python.exe"

VALID_ENVS = ["uat", "staging", "production"]


def get_current_git_branch() -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=ROOT_DIR)
        return res.stdout.strip() if res.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def get_active_env_info():
    env_name = os.getenv("APP_ENV")
    dot_env = AGENT_DIR / ".env"
    if not env_name and dot_env.exists():
        for line in dot_env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("APP_ENV="):
                env_name = line.strip().split("=", 1)[1].strip()
                break
    env_name = (env_name or "production").lower()
    
    ports = {"uat": 8001, "staging": 8002, "production": 8000}
    dbs = {
        "uat": "job-agent/tracker/jobhunt_uat.db",
        "staging": "job-agent/tracker/jobhunt_staging.db",
        "production": "job-agent/tracker/jobhunt.db"
    }
    
    return {
        "env": env_name,
        "port": ports.get(env_name, 8000),
        "db": dbs.get(env_name, "job-agent/tracker/jobhunt.db"),
        "branch": get_current_git_branch()
    }


def cmd_status():
    info = get_active_env_info()
    env = info["env"]
    
    colors = {
        "uat": "\033[93m",      # Yellow
        "staging": "\033[94m",  # Blue
        "production": "\033[92m"# Green
    }
    col = colors.get(env, "\033[0m")
    reset = "\033[0m"

    print("\n" + "=" * 65)
    print("  CAREERHERO STUDIO -- ENVIRONMENT STATUS & CONTROLS")
    print("=" * 65)
    print(f"  Active Environment : {col}{env.upper()}{reset}")
    print(f"  Allocated Port     : {info['port']}")
    print(f"  Isolated Database  : {info['db']}")
    print(f"  Current Git Branch : {info['branch']}")
    
    expected_branch = "main" if env == "production" else env
    if info["branch"] != expected_branch and info["branch"] != "unknown":
        print(f"  [!] Note: Git branch '{info['branch']}' does not match environment '{expected_branch}'.")
    else:
        print(f"  [OK] Git branch aligned with environment target.")

    print("=" * 65)
    print("  Available Commands:")
    print("    python manage_env.py switch <uat|staging|production>")
    print("    python manage_env.py test")
    print("    python manage_env.py promote <uat->staging|staging->production>")
    print("=" * 65 + "\n")


def cmd_switch(target_env: str):
    target_env = target_env.lower()
    if target_env not in VALID_ENVS:
        print(f"Error: Invalid environment '{target_env}'. Must be one of: {VALID_ENVS}")
        sys.exit(1)

    src_env = ROOT_DIR / f".env.{target_env}"
    if not src_env.exists():
        src_env = AGENT_DIR / f".env.{target_env}"

    if not src_env.exists():
        print(f"Error: Config template .env.{target_env} not found!")
        sys.exit(1)

    # Copy to active .env files
    shutil.copy(src_env, ROOT_DIR / ".env")
    shutil.copy(src_env, AGENT_DIR / ".env")

    print(f"\n[OK] Successfully switched active environment to: {target_env.upper()}")
    cmd_status()


def cmd_test():
    print("\n================================================================")
    print("  RUNNING MANDATORY PRE-FLIGHT VERIFICATION GATE")
    print("================================================================\n")
    
    test_script = Path(r"C:\Users\hayaa\.gemini\antigravity\brain\d94b57f9-eb51-41d5-a38c-ce6eee667288\scratch\verify_complete_system.py")

    py = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    cmd = [py, str(test_script)]
    
    res = subprocess.run(cmd, cwd=ROOT_DIR)
    if res.returncode == 0:
        print("\n================================================================")
        print("  [OK] ALL QUALITY GATES PASSED! READY FOR PROMOTION.")
        print("================================================================\n")
        return True
    else:
        print("\n================================================================")
        print("  [FAIL] VERIFICATION GATE FAILED! PROMOTION BLOCKED.")
        print("================================================================\n")
        return False


def cmd_promote(pipeline: str):
    pipeline = pipeline.lower().replace(" ", "")
    valid_pipelines = {
        "uat->staging": ("uat", "staging"),
        "staging->production": ("staging", "main")
    }
    
    if pipeline not in valid_pipelines:
        print(f"Error: Invalid promotion path '{pipeline}'. Choose 'uat->staging' or 'staging->production'.")
        sys.exit(1)

    source_branch, target_branch = valid_pipelines[pipeline]
    print(f"\nInitiating promotion pipeline: {source_branch} -> {target_branch}...")

    # 1. Mandatory test execution
    print("\n[Stage 1/3] Executing quality gate test suite...")
    if not cmd_test():
        print("Promotion aborted: tests must pass 100% before code can be promoted.")
        sys.exit(1)

    # 2. Git operations
    print(f"[Stage 2/3] Checking out target branch '{target_branch}' and merging '{source_branch}'...")
    try:
        subprocess.run(["git", "checkout", target_branch], check=True, cwd=ROOT_DIR)
        subprocess.run(["git", "merge", source_branch, "--no-ff", "-m", f"chore(release): promote {source_branch} to {target_branch}"], check=True, cwd=ROOT_DIR)
        print(f"[OK] Successfully merged {source_branch} into {target_branch}.")
    except subprocess.CalledProcessError as e:
        print(f"Git merge failed: {e}")
        sys.exit(1)

    # 3. Remote Push
    print(f"[Stage 3/3] Pushing promoted release to remote...")
    try:
        remotes = subprocess.run(["git", "remote"], capture_output=True, text=True, cwd=ROOT_DIR).stdout
        target_remote = "github" if "github" in remotes else "origin"
        subprocess.run(["git", "push", target_remote, target_branch], check=True, cwd=ROOT_DIR)
        print(f"[OK] Successfully pushed {target_branch} to remote '{target_remote}'.")
    except subprocess.CalledProcessError as e:
        print(f"Notice: Could not auto-push to remote: {e}")

    print(f"\n================================================================")
    print(f"  PROMOTION COMPLETE: {source_branch} -> {target_branch}")
    print(f"================================================================\n")


def main():
    if len(sys.argv) < 2:
        cmd_status()
        return

    action = sys.argv[1].lower()
    if action == "status":
        cmd_status()
    elif action == "switch":
        if len(sys.argv) < 3:
            print("Usage: python manage_env.py switch [uat|staging|production]")
            sys.exit(1)
        cmd_switch(sys.argv[2])
    elif action == "test":
        success = cmd_test()
        sys.exit(0 if success else 1)
    elif action == "promote":
        if len(sys.argv) < 3:
            print("Usage: python manage_env.py promote [uat->staging|staging->production]")
            sys.exit(1)
        cmd_promote(sys.argv[2])
    else:
        print(f"Unknown command '{action}'. Use status, switch, test, or promote.")


if __name__ == "__main__":
    main()
