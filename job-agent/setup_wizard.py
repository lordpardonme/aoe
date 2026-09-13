import os
import sys
import subprocess
from pathlib import Path
import importlib.util

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
    from rich.table import Table
except ImportError:
    print("The 'rich' library is required for the setup wizard.")
    print("Please run: pip install rich")
    sys.exit(1)

console = Console()

def welcome_banner():
    banner = Panel.fit(
        "[bold cyan]Welcome to Job Agent Setup Wizard[/bold cyan]\n\n"
        "This wizard will walk you through everything needed to configure the job hunt automation tool.\n"
        "Press [bold red]Ctrl+C[/bold red] at any time to exit.",
        title="[bold green]Job Agent[/bold green]"
    )
    console.print(banner)
    print()

def check_python_version():
    console.print("[cyan]Checking Python version...[/cyan]")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        console.print(f"[bold red]Error:[/bold red] Python 3.9+ is required. Found {version.major}.{version.minor}")
        sys.exit(1)
    console.print(f"[green]✓ Python {version.major}.{version.minor} detected.[/green]\n")

def check_dependencies():
    console.print("[cyan]Checking required dependencies...[/cyan]")
    required_packages = {
        'google.auth': 'google-auth',
        'googleapiclient': 'google-api-python-client',
        'pydantic': 'pydantic',
        'pydantic_settings': 'pydantic-settings',
        'typer': 'typer',
        'rich': 'rich',
        'docx': 'python-docx',
        'reportlab': 'reportlab',
        'requests': 'requests',
        'bs4': 'beautifulsoup4'
    }
    
    missing = []
    for module_name, pip_name in required_packages.items():
        if importlib.util.find_spec(module_name) is None:
            missing.append(pip_name)
            
    if missing:
        console.print("[bold red]Missing required packages:[/bold red]")
        for pkg in missing:
            console.print(f"  - {pkg}")
        console.print("\n[yellow]Please run:[/yellow] pip install " + " ".join(missing))
        sys.exit(1)
    console.print("[green]✓ All dependencies installed.[/green]\n")

def gcp_setup_instructions():
    console.print(Panel(
        "[bold]Google Cloud Platform Setup Instructions:[/bold]\n\n"
        "1. Go to [cyan]https://console.cloud.google.com/[/cyan]\n"
        "2. Create a new project (e.g., 'Job Hunt Agent')\n"
        "3. Go to APIs & Services > Library and enable:\n"
        "   - Gmail API\n"
        "   - Google Sheets API\n"
        "4. Go to APIs & Services > OAuth consent screen\n"
        "   - Choose 'External' type\n"
        "   - Fill in required app name and email fields\n"
        "   - Add yourself as a Test User\n"
        "5. Go to APIs & Services > Credentials\n"
        "   - Click 'Create Credentials' -> 'OAuth client ID'\n"
        "   - Application type: 'Desktop app'\n"
        "   - Name it and create\n"
        "6. Download the JSON file and save it as [bold green]credentials.json[/bold green] in this directory.",
        title="GCP OAuth Configuration",
        border_style="blue"
    ))
    
    while True:
        input("\nPress Enter when you have saved credentials.json in the current directory...")
        if os.path.exists("credentials.json"):
            console.print("[green]✓ credentials.json found![/green]\n")
            break
        else:
            console.print("[red]credentials.json not found in the current directory. Please make sure the name is exactly 'credentials.json' and it is in the same folder as this script.[/red]")

def oauth_flow():
    console.print("[cyan]Starting OAuth authorization flow...[/cyan]")
    try:
        # Run authenticate.py as a subprocess so it doesn't mess with our imports
        result = subprocess.run([sys.executable, "authenticate.py"], check=True)
        if os.path.exists("token.json"):
            console.print("[green]✓ token.json created. Authorization successful![/green]\n")
        else:
            console.print("[red]token.json was not created. Authorization may have failed.[/red]")
            sys.exit(1)
    except subprocess.CalledProcessError:
        console.print("[red]Authentication script failed.[/red]")
        sys.exit(1)

def collect_candidate_profile():
    console.print(Panel("[bold]Candidate Profile[/bold]\nLet's configure your personal information for the resumes and emails.", style="magenta"))
    
    profile = {}
    profile['NAME'] = Prompt.ask("Full Name")
    profile['EMAIL'] = Prompt.ask("Contact Email (for resume header)")
    profile['PHONE'] = Prompt.ask("Phone Number")
    profile['LOCATION'] = Prompt.ask("Location (e.g., New York, NY)")
    profile['PORTFOLIO_URL'] = Prompt.ask("Portfolio URL (optional)", default="")
    profile['LINKEDIN_URL'] = Prompt.ask("LinkedIn URL (optional)", default="")
    profile['GMAIL_SENDER'] = Prompt.ask("Gmail sending address (the account you just authorized)")
    
    return profile

def select_profession():
    console.print("\n[cyan]Checking for professions...[/cyan]")
    professions_dir = Path("professions")
    if not professions_dir.exists():
        professions_dir.mkdir()
    
    yaml_files = list(professions_dir.glob("*.yaml")) + list(professions_dir.glob("*.yml"))
    
    if not yaml_files:
        console.print("[yellow]No profession YAML files found in 'professions/'. Skipping profession selection.[/yellow]")
        return ""
    
    table = Table(title="Available Professions")
    table.add_column("Index", style="cyan")
    table.add_column("Profession File", style="green")
    
    for i, file in enumerate(yaml_files, 1):
        table.add_row(str(i), file.name)
        
    console.print(table)
    
    while True:
        choice = Prompt.ask("Select a profession by index (or press Enter to skip)", default="")
        if not choice:
            return ""
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(yaml_files):
                return yaml_files[idx].stem
            else:
                console.print("[red]Invalid index.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

def tracker_setup():
    console.print(Panel("[bold]Google Sheets Tracker[/bold]\nWe use a Google Sheet to track applied jobs.", style="blue"))
    sheet_id = Prompt.ask("Enter existing Google Sheet ID (leave blank to auto-create on first run)", default="")
    return sheet_id

def write_env(profile, profession, sheet_id):
    console.print("\n[cyan]Generating .env file...[/cyan]")
    env_lines = []
    
    for k, v in profile.items():
        env_lines.append(f"{k}={v}")
        
    if profession:
        env_lines.append(f"PROFESSION={profession}")
        
    if sheet_id:
        env_lines.append(f"SPREADSHEET_ID={sheet_id}")
        
    with open(".env", "w") as f:
        f.write("\n".join(env_lines) + "\n")
        
    console.print("[green]✓ .env file created successfully![/green]\n")

def check_master_resume():
    console.print(Panel("[bold]Master Resume[/bold]\nThe agent needs your master resume as a .docx file.", style="yellow"))
    
    while True:
        exists = os.path.exists("master_resume.docx")
        if exists:
            console.print("[green]✓ master_resume.docx found in project root![/green]\n")
            break
        
        console.print("[yellow]Please place your 'master_resume.docx' in the project root directory.[/yellow]")
        choice = Confirm.ask("Ready to check again?")
        if not choice:
            console.print("[yellow]You can add 'master_resume.docx' later.[/yellow]\n")
            break

def self_test():
    console.print("[cyan]Running self-test...[/cyan]")
    
    # 1. Config test
    env_exists = os.path.exists(".env")
    console.print(f"{'[green]✓[/green]' if env_exists else '[red]✗[/red]'} .env file exists")
    
    # 2. Credentials test
    creds_exists = os.path.exists("credentials.json")
    token_exists = os.path.exists("token.json")
    console.print(f"{'[green]✓[/green]' if creds_exists and token_exists else '[red]✗[/red]'} OAuth credentials exist")
    
    # 3. Master Resume test
    resume_exists = os.path.exists("master_resume.docx")
    console.print(f"{'[green]✓[/green]' if resume_exists else '[yellow]⚠[/yellow]'} Master resume exists")
    
    if env_exists and creds_exists and token_exists:
        console.print("\n[green]All core components are configured properly![/green]")
    else:
        console.print("\n[yellow]Some components are missing. Please review the output above.[/yellow]")

def success_message():
    console.print(Panel.fit(
        "[bold green]Setup Complete![/bold green]\n\n"
        "You are now ready to start automating your job hunt.\n\n"
        "[bold]Available Commands:[/bold]\n"
        "  [cyan]python -m job_agent apply --url <JOB_URL>[/cyan]  - Apply to a job\n"
        "  [cyan]python -m job_agent batch path/to/urls.txt[/cyan] - Batch apply\n\n"
        "Good luck!",
        border_style="green"
    ))

def main():
    try:
        welcome_banner()
        check_python_version()
        check_dependencies()
        gcp_setup_instructions()
        oauth_flow()
        profile = collect_candidate_profile()
        profession = select_profession()
        sheet_id = tracker_setup()
        write_env(profile, profession, sheet_id)
        check_master_resume()
        self_test()
        success_message()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup wizard interrupted by user. Exiting...[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n\n[bold red]An unexpected error occurred:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
