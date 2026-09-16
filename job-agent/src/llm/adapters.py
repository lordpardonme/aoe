"""HTTP-based adapters for all supported LLM providers."""

from __future__ import annotations

import logging
from typing import Optional

import requests

from .provider import BaseLLMClient, LLMConfig

log = logging.getLogger("llm.adapters")


class GeminiClient(BaseLLMClient):
    """Google Gemini REST API client."""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(config)
        self.model = config.model or "gemini-2.0-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        api_key = (self.config.api_key or "").strip()
        if not api_key:
            raise ValueError("Google Gemini API Key is missing. Please set it in Settings.")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.config.temperature,
                "maxOutputTokens": self.config.max_tokens,
            },
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.HTTPError as err:
            detail = ""
            try:
                err_data = resp.json()
                if "error" in err_data:
                    err_val = err_data["error"]
                    detail = err_val.get("message", str(err_val)) if isinstance(err_val, dict) else str(err_val)
            except Exception:
                detail = resp.text[:200] if resp and resp.text else ""
            msg = f"{resp.status_code} Error: {detail}" if detail else str(err)
            raise RuntimeError(msg) from err
        except (KeyError, IndexError) as e:
            log.error("Unexpected Gemini response structure: %s", data)
            raise RuntimeError(f"Gemini API returned unexpected format: {data}") from e


class OpenAIClient(BaseLLMClient):
    """OpenAI compatible REST API client (supports OpenAI, Groq, OpenRouter)."""

    def __init__(self, config: LLMConfig, default_model: str = "gpt-4o-mini", default_base_url: str = "https://api.openai.com/v1") -> None:
        super().__init__(config)
        self.model = (config.model or default_model).strip()
        raw_url = (config.base_url or default_base_url).strip().rstrip("/")
        # Auto-upgrade http to https for remote API endpoints to prevent 301 POST-to-GET redirect drops
        if raw_url.startswith("http://") and "localhost" not in raw_url and "127.0.0.1" not in raw_url:
            raw_url = "https://" + raw_url[7:]
        self.base_url = raw_url

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        api_key = (self.config.api_key or "").strip()
        if api_key.startswith("Bearer "):
            api_key = api_key[7:].strip()

        if not api_key and "localhost" not in self.base_url:
            raise ValueError("OpenAI / Groq API Key is missing. Please set it in Settings.")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as err:
            detail = ""
            try:
                err_data = resp.json()
                if "error" in err_data:
                    err_val = err_data["error"]
                    detail = err_val.get("message", str(err_val)) if isinstance(err_val, dict) else str(err_val)
            except Exception:
                detail = resp.text[:200] if resp and resp.text else ""
            msg = f"{resp.status_code} Error: {detail}" if detail else str(err)
            raise RuntimeError(msg) from err
        except (KeyError, IndexError) as e:
            log.error("Unexpected OpenAI response: %s", data)
            raise RuntimeError(f"OpenAI API returned unexpected format: {data}") from e


class GroqClient(OpenAIClient):
    """Groq ultra-fast inference client."""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(
            config,
            default_model="llama-3.3-70b-versatile",
            default_base_url="https://api.groq.com/openai/v1",
        )


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude REST API client."""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(config)
        self.model = (config.model or "claude-3-5-sonnet-20241022").strip()

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        api_key = (self.config.api_key or "").strip()
        if not api_key:
            raise ValueError("Anthropic API Key is missing. Please set it in Settings.")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]
        except requests.exceptions.HTTPError as err:
            detail = ""
            try:
                err_data = resp.json()
                if "error" in err_data:
                    err_val = err_data["error"]
                    detail = err_val.get("message", str(err_val)) if isinstance(err_val, dict) else str(err_val)
            except Exception:
                detail = resp.text[:200] if resp and resp.text else ""
            msg = f"{resp.status_code} Error: {detail}" if detail else str(err)
            raise RuntimeError(msg) from err
        except (KeyError, IndexError) as e:
            log.error("Unexpected Anthropic response: %s", data)
            raise RuntimeError(f"Anthropic API returned unexpected format: {data}") from e


class OllamaClient(BaseLLMClient):
    """Local Ollama instance REST client."""

    def __init__(self, config: LLMConfig) -> None:
        super().__init__(config)
        self.model = config.model or "llama3.2"
        self.base_url = (config.base_url or "http://localhost:11434").rstrip("/")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = f"{self.base_url}/api/chat"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": self.config.temperature},
        }

        try:
            resp = requests.post(url, json=payload, timeout=90)
            resp.raise_for_status()
            data = resp.json()
            return data["message"]["content"]
        except requests.RequestException as e:
            raise RuntimeError(
                f"Failed to connect to local Ollama at {self.base_url}. Make sure Ollama is running (`ollama serve`)."
            ) from e
