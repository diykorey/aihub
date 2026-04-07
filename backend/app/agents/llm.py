"""Provider-agnostic LLM client for agent pipeline.

Supported providers:
- openai  (OpenAI SDK)
- anthropic (Anthropic SDK)
- gemini  (Google GenAI SDK)
- grok    (xAI — OpenAI-compatible, uses OpenAI SDK with custom base_url)

Configuration is environment-driven:
- LLM_PROVIDER=openai|anthropic|gemini|grok
- LLM_MODEL=<provider model name>
- provider-specific API key vars (see `.env.example`)

If the selected provider is not configured, `chat_complete()` returns a
clear stub string so local development can continue without secrets.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

_TIMEOUT_SECONDS = 60


def _provider() -> str:
    return os.getenv("LLM_PROVIDER", "openai").strip().lower()


def _model_for(provider: str) -> str:
    default_by_provider = {
        "openai": "gpt-5-nano",
        "anthropic": "claude-3-5-sonnet-latest",
        "gemini": "gemini-2.0-flash",
        "grok": "grok-2-latest",
    }
    return os.getenv("LLM_MODEL", default_by_provider.get(provider, "gpt-4o-mini"))


def _openai_key() -> str:
    return os.getenv("OPENAI_API_KEY", "")


def _anthropic_key() -> str:
    return os.getenv("ANTHROPIC_API_KEY", "")


def _gemini_key() -> str:
    return os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")


def _grok_key() -> str:
    return os.getenv("XAI_API_KEY", "") or os.getenv("GROK_API_KEY", "")


def is_configured() -> bool:
    """Return True when the selected provider has required credentials."""
    provider = _provider()
    if provider == "openai":
        return bool(_openai_key())
    if provider == "anthropic":
        return bool(_anthropic_key())
    if provider == "gemini":
        return bool(_gemini_key())
    if provider == "grok":
        return bool(_grok_key())
    return False


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------


def _chat_openai(user_prompt: str, system_prompt: str) -> str:
    from openai import OpenAI

    base_url = (
        os.getenv("LLM_BASE_URL")
        or os.getenv("OPENAI_BASE_URL")
        or "https://api.openai.com/v1"
    )
    client = OpenAI(api_key=_openai_key(), base_url=base_url, timeout=_TIMEOUT_SECONDS)
    response = client.chat.completions.create(
        model=_model_for("openai"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""


def _chat_grok(user_prompt: str, system_prompt: str) -> str:
    from openai import OpenAI

    base_url = (
        os.getenv("LLM_BASE_URL")
        or os.getenv("GROK_BASE_URL")
        or "https://api.x.ai/v1"
    )
    client = OpenAI(api_key=_grok_key(), base_url=base_url, timeout=_TIMEOUT_SECONDS)
    response = client.chat.completions.create(
        model=_model_for("grok"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""


def _chat_anthropic(user_prompt: str, system_prompt: str) -> str:
    from anthropic import Anthropic

    base_url = os.getenv("ANTHROPIC_BASE_URL") or None
    client = Anthropic(
        api_key=_anthropic_key(),
        base_url=base_url,
        timeout=_TIMEOUT_SECONDS,
    )
    response = client.messages.create(
        model=_model_for("anthropic"),
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text if response.content else ""


def _chat_gemini(user_prompt: str, system_prompt: str) -> str:
    from google import genai

    client = genai.Client(api_key=_gemini_key())
    response = client.models.generate_content(
        model=_model_for("gemini"),
        contents=user_prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )
    return response.text or ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def chat_complete(
    user_prompt: str,
    system_prompt: str = "You are a helpful AI assistant.",
) -> str:
    """Call selected provider and return plain text response.

    If provider credentials are missing, returns a stub marker string.
    """
    provider = _provider()
    if not is_configured():
        return (
            "[STUB - configure provider credentials to enable real LLM calls. "
            f"provider={provider}, prompt={user_prompt[:80]}...]"
        )

    if provider == "openai":
        return _chat_openai(user_prompt, system_prompt)
    if provider == "anthropic":
        return _chat_anthropic(user_prompt, system_prompt)
    if provider == "gemini":
        return _chat_gemini(user_prompt, system_prompt)
    if provider == "grok":
        return _chat_grok(user_prompt, system_prompt)

    return (
        "[STUB - unsupported LLM_PROVIDER. "
        f"got={provider}, expected one of: openai|anthropic|gemini|grok]"
    )
