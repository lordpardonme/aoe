"""
First-Reader Simulation & Attention Auditor for CareerHero Studio.
Simulates a busy hiring manager or founder reading cold outreach emails,
evaluating hook strength, conciseness, jargon density, and cognitive drop-off points.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

CLICHE_JARGON = [
    "synergy", "rockstar", "ninja", "passionate about", "hard-working",
    "results-oriented", "detail-oriented", "go-getter", "dynamic professional",
    "self-starter", "proven track record", "think outside the box", "value-add"
]

HIGH_VALUE_HOOKS = [
    "shipped", "built", "reduced", "increased", "converted", "metric",
    "design system", "0 to 1", "0-1", "dau", "revenue", "b2b", "retention"
]

def audit_outreach_pitch(subject: str, body: str) -> Dict[str, Any]:
    """
    Audits a cold email subject and body, scoring attention retention (0-100).
    """
    words = body.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', body)
    sentence_count = max(len([s for s in sentences if s.strip()]), 1)
    
    score = 100
    deductions = []
    strengths = []

    # 1. Length penalty: > 140 words is too long for busy founders
    if word_count > 160:
        penalty = min(30, (word_count - 160) // 5)
        score -= penalty
        deductions.append(f"Too long ({word_count} words). Ideal length is 60-120 words for quick mobile scanning.")
    elif word_count < 35:
        score -= 20
        deductions.append(f"Too short ({word_count} words). Lacks concrete proof of competence or metric.")
    else:
        strengths.append(f"Optimal length ({word_count} words) — readable in under 20 seconds.")

    # 2. Subject Line Check
    sub_words = subject.split()
    if len(sub_words) > 9:
        score -= 10
        deductions.append("Subject line is too long (> 9 words); gets truncated on mobile inboxes.")
    elif len(sub_words) < 2:
        score -= 15
        deductions.append("Subject line too vague.")
    else:
        strengths.append("Punchy subject line optimized for mobile preview.")

    # 3. Jargon Density
    body_lower = body.lower()
    found_jargon = [j for j in CLICHE_JARGON if j in body_lower]
    if found_jargon:
        score -= min(25, len(found_jargon) * 8)
        deductions.append(f"Contains generic cliches: {', '.join(found_jargon)}. Replace with verifiable outcomes.")
    else:
        strengths.append("Zero generic buzzwords detected.")

    # 4. Metric & Proof Check
    numbers_present = bool(re.search(r'\d+%|\$\d+|₹\d+|£\d+|\b\d+k\b|\b\d+x\b', body, re.IGNORECASE))
    if numbers_present:
        score = min(100, score + 10)
        strengths.append("Contains quantified metrics/impact data (+10 bonus).")
    else:
        score -= 15
        deductions.append("Missing quantifiable outcomes or metrics (e.g. '+18% QoQ', '100k users').")

    # 5. Call to Action (CTA)
    has_cta = any(phrase in body_lower for phrase in [
        "worth a quick", "open to", "chat this week", "quick call", "send over", "thoughts?"
    ])
    if not has_cta:
        score -= 10
        deductions.append("Lacks a low-friction closing question or call-to-action.")
    else:
        strengths.append("Clear, low-friction closing call-to-action.")

    final_score = max(10, min(100, score))
    
    # Grade
    if final_score >= 85:
        grade = "A (High Conversion)"
    elif final_score >= 70:
        grade = "B (Good)"
    elif final_score >= 50:
        grade = "C (Needs Polish)"
    else:
        grade = "D (High Drop-off Risk)"

    return {
        "score": final_score,
        "attention_score": final_score,
        "grade": grade,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "strengths": strengths,
        "deductions": deductions,
        "recommendations": deductions if deductions else ["Concise pitch with strong opening retention."],
        "breakdown": {
            "hook_rating": grade,
            "word_count": word_count,
            "sentence_count": sentence_count
        },
        "metrics": {
            "est_scan_seconds": max(5, int(word_count / 3.5))
        },
        "verdict": "Ready to send" if final_score >= 75 else "Recommended to refine before dispatch"
    }
