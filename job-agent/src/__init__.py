"""Job Agent — an autonomous AI job-application assistant.

Package modules:
    config       Runtime configuration + Google credential loading.
    logger       Central logging (app.log / error.log + rich console).
    utils        Shared helpers (slugify, retry, file IO).
    jobs         Job-description fetching, parsing and modelling.
    resume       ATS-optimised resume tailoring (never touches the master).
    coverletter  Tailored cover-letter generation.
    emailer      Application email (markdown + HTML) generation.
    pdf          Reportlab-based DOCX/text -> PDF rendering.
    gmail        Gmail API client (send with attachments, HTML + plain text).
    sheet        Google Sheets application-tracker client.
    agent        Orchestrates the full apply pipeline.
    cli          Typer command-line interface.
"""

__version__ = "1.0.0"
