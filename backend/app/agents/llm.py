"""Provider-agnostic LLM client for agent pipeline.

Supported providers:
- openai
- anthropic
- gemini
- grok (xAI)

Configuration is environment-driven:
- LLM_PROVIDER=openai|anthropic|gemini|grok
- LLM_MODEL=<provider model name>
- provider-specific API key vars (see `.env.example`)

If the selected provider is not configured, `chat_complete()` returns a
clear stub string so local development can continue without secrets.
"""

from __future__ import annotations

import json
import os
from urllib import error, parse, request

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
    # Support either variable name.
    return os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")


def _grok_key() -> str:
    # Support either variable name.
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


def _post_json(url: str, payload: dict, headers: dict[str, str]) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8") if exc.fp else ""
        raise RuntimeError(f"LLM HTTP {exc.code}: {body[:500]}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"LLM network error: {exc}") from exc


def _chat_openai(user_prompt: str, system_prompt: str) -> str:
    base_url = os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": _model_for("openai"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {_openai_key()}",
        "Content-Type": "application/json",
    }
    data = _post_json(url, payload, headers)
    return data.get("choices", [{}])[0].get("message", {}).get("content", "") or ""


def _chat_grok(user_prompt: str, system_prompt: str) -> str:
    # xAI is OpenAI-compatible.
    base_url = os.getenv("LLM_BASE_URL") or os.getenv("GROK_BASE_URL") or "https://api.x.ai/v1"
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": _model_for("grok"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {_grok_key()}",
        "Content-Type": "application/json",
    }
    data = _post_json(url, payload, headers)
    return data.get("choices", [{}])[0].get("message", {}).get("content", "") or ""


def _chat_anthropic(user_prompt: str, system_prompt: str) -> str:
    url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1/messages")
    payload = {
        "model": _model_for("anthropic"),
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    headers = {
        "x-api-key": _anthropic_key(),
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    data = _post_json(url, payload, headers)
    content = data.get("content", [])
    if content and isinstance(content[0], dict):
        return content[0].get("text", "") or ""
    return ""


def _chat_gemini(user_prompt: str, system_prompt: str) -> str:
    model = _model_for("gemini")
    key = _gemini_key()
    url = (
        os.getenv("GEMINI_BASE_URL")
        or f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    )
    query_sep = "&" if "?" in url else "?"
    url = f"{url}{query_sep}key={parse.quote(key)}"

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
    }
    headers = {"Content-Type": "application/json"}
    data = _post_json(url, payload, headers)

    candidates = data.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        return ""
    return parts[0].get("text", "") or ""


# noinspection PyPackageRequirements
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
