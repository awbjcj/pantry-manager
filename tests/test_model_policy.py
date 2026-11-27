"""Model retirement applies to deployed environment overrides and Agno seams."""

import pytest

from app.agno_models import build_agno_model
from app.providers import ProviderCredentials
from app.settings import Settings


@pytest.mark.parametrize("variable,attribute,old,replacement", [
    ("OPENAI_MODEL", "openai_model", "gpt-6-sol", "gpt-6.2-sol"),
    ("OPENAI_MODEL", "openai_model", "gpt-5.6-sol", "gpt-6.2-sol"),
    ("OPENAI_TEXT_MODEL", "openai_text_model", "gpt-5.6-luna", "gpt-6-luna"),
    ("OPENAI_TEXT_MODEL", "openai_text_model", "gpt-6-luna", "gpt-6-luna"),
    ("OPENAI_TEXT_MODEL", "openai_text_model", " GPT-5.6-Luna ", "gpt-6-luna"),
    ("ANTHROPIC_MODEL", "anthropic_model", "claude-opus-4-6", "claude-opus-5-5"),
    ("ANTHROPIC_MODEL", "anthropic_model", "claude-opus-5-5", "claude-opus-5-5"),
    ("ANTHROPIC_SEARCH_MODEL", "anthropic_search_model", "claude-opus-5-5", "claude-opus-5-5"),
    ("ANTHROPIC_MODEL", "anthropic_model", "claude-sonnet-4-6", "claude-sonnet-5-5"),
    ("ANTHROPIC_SEARCH_MODEL", "anthropic_search_model", "claude-sonnet-5", "claude-sonnet-5-5"),
    ("ANTHROPIC_TEXT_MODEL", "anthropic_text_model", "claude-haiku-4-5-20251001", "claude-haiku-5-5"),
    ("OPENAI_MODEL", "openai_model", "gpt-6.1-sol", "gpt-6.2-sol"),
    ("OPENAI_MODEL", "openai_model", "gpt-6-astra", "gpt-6.2-astra"),
    ("ANTHROPIC_MODEL", "anthropic_model", "claude-fable-5-1", "claude-fable-5-2"),
    ("GEMINI_MODEL", "gemini_model", "gemini-3.7-flash", "gemini-3.8-flash"),
    ("GEMINI_MODEL", "gemini_model", "gemini-3.8-flash", "gemini-3.8-flash"),
    ("GEMINI_MODEL", "gemini_model", "gemini-3.1-pro-preview", "gemini-4-argon"),
    ("GEMINI_TEXT_MODEL", "gemini_text_model", "gemini-2.5-flash", "gemini-3.5-flash-lite"),
    ("OPENAI_MODEL", "openai_model", "my-gateway-deployment", "my-gateway-deployment"),
])
def test_settings_upgrade_explicit_environment_models(
    monkeypatch, variable, attribute, old, replacement,
):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-only")
    monkeypatch.setenv("ALLOWED_TELEGRAM_USER_ID", "1")
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-only")
    monkeypatch.setenv(variable, old)
    settings = Settings(_env_file=None)  # type: ignore[call-arg]
    assert getattr(settings, attribute) == replacement


@pytest.mark.parametrize("provider,old,replacement", [
    ("openai", "gpt-5.6-luna", "gpt-6-luna"),
    ("anthropic", "claude-sonnet-4-5-20250929", "claude-sonnet-5-5"),
    ("gemini", "gemini-3-flash-preview", "gemini-3.6-flash"),
])
def test_agno_construction_also_resolves_legacy_configuration(provider, old, replacement):
    credentials = ProviderCredentials(provider=provider, mode="api", api_key="test-only")
    assert build_agno_model(model_id=old, credentials=credentials).id == replacement
