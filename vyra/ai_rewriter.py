"""Optional AI rewrite hook for Vyra.

This module is intentionally OFF by default.

Goal: allow users to run "free-form English" through an external LLM that rewrites
it into canonical Vyra statements before parsing.

No network calls are made unless explicitly enabled (CLI `--ai` or env `VYRA_AI=1`).
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from dataclasses import dataclass
from typing import Optional, Tuple


class AiRewriteError(RuntimeError):
    pass


@dataclass(frozen=True)
class AiRewriteConfig:
    enabled: bool = False
    provider: str = "openai_compatible"
    url: Optional[str] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    timeout_seconds: int = 30


_SYSTEM_PROMPT = (
    "You rewrite free-form English into canonical Vyra code. "
    "Return ONLY Vyra source code, no explanations. "
    "Rules: one statement per line; end simple statements with '.'; "
    "end block headers with ':'; indent block bodies by exactly two spaces. "
    "Use existing Vyra verbs like Set/Store/Display/If/Otherwise/While/Repeat/For each/" 
    "Create function/Call/Return/Break/Continue."
)


def _strip_code_fences(text: str) -> str:
    # Remove common Markdown fences if the model returns them.
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", text)
        text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


def config_from_env() -> AiRewriteConfig:
    enabled = os.getenv("VYRA_AI", "0").strip() in {"1", "true", "yes", "on"}
    provider = os.getenv("VYRA_AI_PROVIDER", "openai_compatible").strip() or "openai_compatible"
    url = os.getenv("VYRA_AI_URL")
    model = os.getenv("VYRA_AI_MODEL")
    api_key = os.getenv("VYRA_AI_API_KEY")

    timeout_seconds = 30
    raw_timeout = os.getenv("VYRA_AI_TIMEOUT")
    if raw_timeout:
        try:
            timeout_seconds = max(1, int(raw_timeout))
        except ValueError:
            timeout_seconds = 30

    return AiRewriteConfig(
        enabled=enabled,
        provider=provider,
        url=url,
        model=model,
        api_key=api_key,
        timeout_seconds=timeout_seconds,
    )


def rewrite_source(source: str, *, config: Optional[AiRewriteConfig] = None) -> Tuple[str, Optional[str]]:
    """Rewrite source code using an external AI provider.

    Returns: (rewritten_source, info_message)

    If disabled, returns (source, None).
    """

    cfg = config or config_from_env()
    if not cfg.enabled:
        return source, None

    provider = (cfg.provider or "").strip().lower()
    if provider != "openai_compatible":
        raise AiRewriteError(
            f"Unsupported VYRA_AI_PROVIDER '{cfg.provider}'. Supported: openai_compatible"
        )

    missing = []
    if not cfg.url:
        missing.append("VYRA_AI_URL")
    if not cfg.model:
        missing.append("VYRA_AI_MODEL")
    if missing:
        raise AiRewriteError(
            "AI rewrite is enabled but missing configuration: " + ", ".join(missing)
        )

    # API key is optional for local/self-hosted endpoints.
    headers = {
        "Content-Type": "application/json",
    }
    if cfg.api_key:
        headers["Authorization"] = f"Bearer {cfg.api_key}"

    payload = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": source},
        ],
        "temperature": 0,
    }

    req = urllib.request.Request(
        cfg.url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout_seconds) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        raise AiRewriteError(f"AI rewrite request failed: {e}") from e

    try:
        data = json.loads(body)
        content = data["choices"][0]["message"]["content"]
        rewritten = _strip_code_fences(str(content))
        if not rewritten.strip():
            raise AiRewriteError("AI rewrite returned empty output")
        return rewritten, "AI rewrite applied"
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise AiRewriteError("AI rewrite response was not in expected format") from e
