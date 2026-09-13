"""LLM module exports and factory."""

import os
from typing import Optional

from .provider import BaseLLMClient, LLMConfig
from .adapters import (
    GeminiClient,
    OpenAIClient,
    GroqClient,
    AnthropicClient,
    OllamaClient,
)


def get_llm_client(config: Optional[LLMConfig] = None) -> BaseLLMClient:
    """Factory to instantiate the appropriate LLM client."""
    if config is None:
        # Sourced from environment
        provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        api_key = (
            os.getenv(f"{provider.upper()}_API_KEY")
            or os.getenv("LLM_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or ""
        )
        model = os.getenv("LLM_MODEL", "")
        base_url = os.getenv("LLM_BASE_URL")
        config = LLMConfig(provider=provider, api_key=api_key, model=model, base_url=base_url)

    prov = (config.provider or "gemini").lower()

    if prov == "gemini":
        return GeminiClient(config)
    elif prov == "openai":
        return OpenAIClient(config)
    elif prov == "groq":
        return GroqClient(config)
    elif prov == "anthropic":
        return AnthropicClient(config)
    elif prov == "ollama":
        return OllamaClient(config)
    else:
        # Default to OpenAI compatible format
        return OpenAIClient(config)
