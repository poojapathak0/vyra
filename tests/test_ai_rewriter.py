import os

import pytest

from vyra.ai_rewriter import rewrite_source, AiRewriteConfig, AiRewriteError


def test_ai_rewrite_noop_when_disabled():
    src = 'Display "Hello".'
    out, info = rewrite_source(src, config=AiRewriteConfig(enabled=False))
    assert out == src
    assert info is None


def test_ai_rewrite_enabled_requires_config(monkeypatch):
    # Ensure env doesn't accidentally supply config during test.
    monkeypatch.delenv("VYRA_AI_URL", raising=False)
    monkeypatch.delenv("VYRA_AI_MODEL", raising=False)

    with pytest.raises(AiRewriteError) as exc:
        rewrite_source("say hello", config=AiRewriteConfig(enabled=True))

    msg = str(exc.value)
    assert "VYRA_AI_URL" in msg
    assert "VYRA_AI_MODEL" in msg
