"""Typer command-line interface for Job Agent.

Commands:
    apply    Full pipeline: tailor -> cover letter -> email -> PDFs -> send -> track.
    resume   Generate only the tailored resume (DOCX + PDF).
    email    Generate only the application email (Markdown + HTML).
    tracker  Append a row to the application tracker.
    send     Build the application and send the email (no tracker update).
    test     Run offline self-checks and probe Google connectivity.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.panel import Panel
from rich.table import Table

from .agent import ApplicationResult, JobAgent
from .config import get_settings
from .jobs import JobDescription
from .logger import get_console, get_logger

app = typer.Typer(
    add_completion=False,
    help="Autonomous AI job-application agent.",
    no_args_is_help=True,
)
console = get_console()
log = get_logger("cli")


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------
def _resolve_job(
    agent: JobAgent,
    url: Optional[str],
    file: Optional[str],
    text: Optional[str],
    company: Optional[str],
    role: Optional[str],
) -> JobDescription:
    """Build a :class:`JobDescription` from whichever source was provided."""
    if url:
        return agent.job_from_url(url, company=company, role=role)
    if file:
        return agent.job_from_file(file, company=company, role=role)
    if text:
        return agent.job_from_text(text, company=company, role=role)
    raise typer.BadParameter("Provide one of --url, --file or --text.")


def _print_result(result: ApplicationResult) -> None:
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_row("Company", result.company)
    table.add_row("Role", result.role)
    table.add_row("Keywords", ", ".join(result.keywords) or "—")
    table.add_row("Email", f"{result.email_status} -> {result.email_to or '—'}")
    table.add_row("Tracker", result.tracker_status)
    table.add_row("Dry run", "yes" if result.dry_run else "NO (live)")
    console.print(Panel(table, title="Application summary", border_style="green"))
    files = Table(title="Generated files", show_lines=False)
    files.add_column("Artifact", style="cyan")
    files.add_column("Path")
    for key, path in result.files.items():
        files.add_row(key, path)
    console.print(files)


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------
@app.command()
def apply(
    url: Optional[str] = typer.Option(None, "--url", help="Job posting URL."),
    file: Optional[str] = typer.Option(None, "--file", help="Path to a job description text file."),
    text: Optional[str] = typer.Option(None, "--text", help="Raw job description text."),
    company: Optional[str] = typer.Option(None, "--company", help="Override the detected company."),
    role: Optional[str] = typer.Option(None, "--role", help="Override the detected role."),
    recipient: Optional[str] = typer.Option(None, "--to", help="Override the recipient email."),
    no_send: bool = typer.Option(False, "--no-send", help="Skip sending the email."),
    no_sheet: bool = typer.Option(False, "--no-sheet", help="Skip updating the tracker."),
) -> None:
    """Run the full application pipeline for a single job."""
    agent = JobAgent()
    job = _resolve_job(agent, url, file, text, company, role)
    result = agent.apply(
        job,
        send=not no_send,
        update_sheet=not no_sheet,
        recipient=recipient,
    )
    _print_result(result)


@app.command()
def resume(
    url: Optional[str] = typer.Option(None, "--url"),
    file: Optional[str] = typer.Option(None, "--file"),
    text: Optional[str] = typer.Option(None, "--text"),
    company: Optional[str] = typer.Option(None, "--company"),
    role: Optional[str] = typer.Option(None, "--role"),
) -> None:
    """Generate only the tailored resume (DOCX + PDF)."""
    from .pdf import render_resume_pdf
    from .config import RESUMES_DIR
    from .utils import slugify

    agent = JobAgent()
    job = _resolve_job(agent, url, file, text, company, role)
    data, docx_path = agent.resume_builder.build(job)
    pdf_path = render_resume_pdf(data, RESUMES_DIR / f"{slugify(job.company)}_resume.pdf")
    console.print(f"[green]Resume written:[/green] {docx_path}")
    console.print(f"[green]Resume PDF:[/green]    {pdf_path}")


@app.command()
def email(
    url: Optional[str] = typer.Option(None, "--url"),
    file: Optional[str] = typer.Option(None, "--file"),
    text: Optional[str] = typer.Option(None, "--text"),
    company: Optional[str] = typer.Option(None, "--company"),
    role: Optional[str] = typer.Option(None, "--role"),
) -> None:
    """Generate only the application email (Markdown + HTML)."""
    agent = JobAgent()
    job = _resolve_job(agent, url, file, text, company, role)
    resume_data = agent.resume_builder.tailor(job)
    result = agent.email_builder.build(job, resume_data)
    console.print(f"[green]Subject:[/green] {result['subject']}")
    console.print(f"[green]Email MD:[/green]   {result['md']}")
    console.print(f"[green]Email HTML:[/green] {result['html']}")


@app.command()
def tracker(
    company: str = typer.Option(..., "--company"),
    role: str = typer.Option(..., "--role"),
    url: str = typer.Option("", "--url"),
    status: str = typer.Option("Applied", "--status"),
    resume: str = typer.Option("", "--resume", help="Path/name of the resume used."),
    notes: str = typer.Option("", "--notes"),
) -> None:
    """Append a single row to the application tracker (Sheet + local CSV)."""
    from .sheet import SheetClient

    outcome = SheetClient().update_tracker(
        company=company, role=role, url=url, resume=resume, status=status, notes=notes
    )
    console.print(f"[green]Tracker updated:[/green] {outcome}")


@app.command()
def send(
    url: Optional[str] = typer.Option(None, "--url"),
    file: Optional[str] = typer.Option(None, "--file"),
    text: Optional[str] = typer.Option(None, "--text"),
    company: Optional[str] = typer.Option(None, "--company"),
    role: Optional[str] = typer.Option(None, "--role"),
    recipient: Optional[str] = typer.Option(None, "--to", help="Recipient email address."),
) -> None:
    """Build the application documents and send the email (no tracker update)."""
    agent = JobAgent()
    job = _resolve_job(agent, url, file, text, company, role)
    files = agent.generate_documents(job)
    outcome = agent.send_application_email(job, files, recipient)
    if outcome["status"] == "dry_run":
        console.print(
            "[yellow]DRY_RUN is on — email was NOT sent.[/yellow] "
            "Set DRY_RUN=false in .env to send for real."
        )
    console.print(f"[green]Send result:[/green] {outcome}")


@app.command()
def test() -> None:
    """Run offline self-checks, then probe Google connectivity (best effort)."""
    from .resume import ResumeBuilder
    from .pdf import render_resume_pdf, render_text_pdf
    from .config import RESUMES_DIR, COVERLETTERS_DIR

    settings = get_settings()
    results: list[tuple[str, bool, str]] = []

    def check(name: str, fn) -> None:
        try:
            detail = fn() or "ok"
            results.append((name, True, str(detail)))
        except Exception as exc:  # noqa: BLE001 - report every failure
            log.error("Self-check %s failed: %s", name, exc)
            results.append((name, False, str(exc)))

    sample_jd = (
        "We are hiring a Senior Product Designer at Acme Labs. You will own user "
        "flows, wireframing, prototyping in Figma, design systems, usability "
        "testing and developer handoff for our B2B SaaS dashboard. Contact "
        "careers@acme.example."
    )

    agent = JobAgent()
    job_holder: dict = {}

    check("Settings load", lambda: f"dry_run={settings.dry_run}")
    check("Master resume parse", lambda: f"{len(ResumeBuilder().load_master().sections)} sections")

    def parse_job():
        job = agent.job_from_text(sample_jd, company="Acme Labs", role="Senior Product Designer")
        job_holder["job"] = job
        return f"{len(job.keywords)} keywords, contact={job.contact_email}"

    check("Job parse + keywords", parse_job)

    def gen_docs():
        job = job_holder["job"]
        files = agent.generate_documents(job)
        return f"{len(files)} files generated"

    check("Generate docs + PDFs", gen_docs)

    def gmail_probe():
        from .gmail import GmailClient
        profile = GmailClient().get_profile()
        return f"Gmail OK: {profile.get('emailAddress')}"

    check("Gmail connectivity", gmail_probe)

    # --- report ----------------------------------------------------------
    table = Table(title="Self-check results")
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Detail")
    all_offline_ok = True
    for name, ok, detail in results:
        status = "[green]PASS[/green]" if ok else "[red]FAIL[/red]"
        table.add_row(name, status, detail)
        if not ok and name != "Gmail connectivity":
            all_offline_ok = False
    console.print(table)

    if all_offline_ok:
        console.print("[green]All offline checks passed.[/green]")
    else:
        console.print("[red]Some offline checks failed — see logs/error.log.[/red]")
        raise typer.Exit(code=1)
