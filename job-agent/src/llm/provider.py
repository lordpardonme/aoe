"""Base LLM interface and provider definitions for Job Hunt Agent.

Supports Bring-Your-Own-Key (BYOK) across multiple LLM providers:
- Google Gemini
- OpenAI (GPT-4o, GPT-4o-mini, o3-mini)
- Anthropic (Claude 3.5 Sonnet, Claude 3.7 Sonnet)
- Groq (Llama 3.3 70B, etc.)
- Ollama / Local LLM
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional

log = logging.getLogger("llm")


@dataclass
class LLMConfig:
    """Configuration for LLM generation."""
    provider: str = "gemini"  # gemini, openai, anthropic, groq, ollama
    api_key: str = ""
    model: str = ""
    base_url: Optional[str] = None
    temperature: float = 0.4
    max_tokens: int = 4096


class BaseLLMClient(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate plain text from prompt."""
        pass

    def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """Generate structured JSON response.
        
        Attempts to parse markdown code blocks or raw JSON from model response.
        """
        system = (
            (system_prompt + "\n\n" if system_prompt else "")
            + "IMPORTANT: You MUST respond ONLY with a valid JSON object. "
            + "Do not include any introductory or concluding markdown text outside the JSON."
        )
        raw = self.generate(prompt, system_prompt=system).strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            lines = raw.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw = "\n".join(lines).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            log.warning("JSON decode failed on LLM output (%s). Raw: %s", exc, raw[:200])
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(raw[start : end + 1])
                except Exception:
                    pass
            raise ValueError(f"Model failed to return valid JSON: {raw[:300]}") from exc
