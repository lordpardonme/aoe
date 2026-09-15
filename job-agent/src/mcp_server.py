"""Model Context Protocol (MCP) Server for AOE (Autonomous Outreach Engine).

Enables Munder Difflin, Claude Code, Antigravity (`agy`), and Cursor to orchestrate
AOE natively via the standard Model Context Protocol over stdio JSON-RPC.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from .config import RESUMES_DIR, TRACKER_DIR
from .gmail import GmailClient
from .hive import HiveCoordinator
from .logger import get_logger
from .web.db import list_applications, list_leads

log = get_logger("mcp")

TOOLS = [
    {
        "name": "aoe_run_hive_pipeline",
        "description": "Run AOE's multi-agent Hive pipeline (Scout, Resume Architect, Copywriter, Quality Reviewer) on a job description to tailor a 1-page PDF resume and draft cold outreach.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Raw text of the job description"},
                "company": {"type": "string", "description": "Target company name"},
                "role": {"type": "string", "description": "Target job title/role"},
                "url": {"type": "string", "description": "Job posting URL (optional)"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "aoe_list_leads",
        "description": "List leads from AOE's local SQLite tracker database filtered by status or country.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status, e.g. 'Not Contacted', 'Applied', 'Follow-up Needed'"},
                "country": {"type": "string", "description": "Filter by country (e.g. Germany, UK, Netherlands)"},
                "limit": {"type": "integer", "description": "Maximum number of leads to return (default 20)"}
            }
        }
    },
    {
        "name": "aoe_get_stats",
        "description": "Retrieve live job hunt analytics, application volume, interview rates, and response activity summary.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "aoe_scan_recruiter_replies",
        "description": "Scan connected Gmail account for inbound recruiter interview invitations, assessments, and rejections.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "max_results": {"type": "integer", "description": "Maximum email threads to scan (default 15)"}
            }
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool and return MCP content block."""
    if name == "aoe_run_hive_pipeline":
        coordinator = HiveCoordinator()
        result = coordinator.run_pipeline(
            text=arguments.get("text", ""),
            company=arguments.get("company"),
            role=arguments.get("role"),
            url=arguments.get("url")
        )
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result["artifacts"], indent=2)
                }
            ]
        }

    elif name == "aoe_list_leads":
        limit = arguments.get("limit", 20)
        leads = list_leads(limit=limit)
        status_filter = arguments.get("status")
        country_filter = arguments.get("country")

        filtered = []
        for lead in leads:
            if status_filter and lead.get("status", "").lower() != status_filter.lower():
                continue
            if country_filter and lead.get("country", "").lower() != country_filter.lower():
                continue
            filtered.append({
                "id": lead.get("id"),
                "company": lead.get("company"),
                "role": lead.get("role"),
                "country": lead.get("country"),
                "status": lead.get("status"),
                "email": lead.get("email"),
                "url": lead.get("url")
            })

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(filtered, indent=2)
                }
            ]
        }

    elif name == "aoe_get_stats":
        apps = list_applications()
        total = len(apps)
        interviews = sum(1 for a in apps if "interview" in str(a.get("status", "")).lower())
        applied = sum(1 for a in apps if "applied" in str(a.get("status", "")).lower())
        leads = list_leads(limit=1000)

        stats = {
            "total_applications": total,
            "applied_count": applied,
            "interview_count": interviews,
            "interview_rate": f"{(interviews / total * 100):.1f}%" if total > 0 else "0.0%",
            "total_leads_in_db": len(leads),
            "resumes_generated": len(list(RESUMES_DIR.glob("*.pdf")))
        }
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(stats, indent=2)
                }
            ]
        }

    elif name == "aoe_scan_recruiter_replies":
        client = GmailClient()
        max_results = arguments.get("max_results", 15)
        replies = client.check_replies(max_results=max_results)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(replies, indent=2)
                }
            ]
        }

    else:
        raise ValueError(f"Unknown MCP tool: {name}")


def run_stdio_server():
    """Run JSON-RPC 2.0 stdio server loop for MCP."""
    log.info("Starting AOE MCP Server over stdio...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        response: Dict[str, Any] = {"jsonrpc": "2.0", "id": req_id}

        if method == "initialize":
            response["result"] = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "aoe-mcp-server",
                    "version": "1.0.0"
                }
            }
        elif method == "notifications/initialized":
            continue
        elif method == "ping":
            response["result"] = {}
        elif method == "tools/list":
            response["result"] = {"tools": TOOLS}
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                result = handle_tool_call(tool_name, tool_args)
                response["result"] = result
            except Exception as err:
                response["error"] = {
                    "code": -32000,
                    "message": str(err)
                }
        else:
            if req_id is not None:
                response["error"] = {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }

        if req_id is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
