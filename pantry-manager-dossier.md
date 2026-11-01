---
repo_url: https://github.com/awbjcj/pantry-manager
repo_name: food-manager
role: sole author
generated_at: 2026-10-31
source_revision: 4b66acf207eb29b5b92ebae7bb42ade7959b1736
---

# Project: Pantry Manager

## Summary

Pantry Manager is a household food tracker that accepts receipt photos and text, records expiry dates, and suggests recipes and meal plans. People can use it through Telegram, Slack, or WhatsApp; a Telegram Mini App provides a browser workspace (`app/messaging/`, `app/miniapp_workspace.py`). Household members share pantry data while choosing their own language and model provider (`app/models.py`, `app/providers.py`). The project is active and has one human author alongside automation-account commits.

Role: sole author (463 of 483 commits across the owner's Git identities; the remaining 20 are automation-account commits; `git shortlog -sne 4b66acf`; `git rev-list --count 4b66acf`)
Repository: https://github.com/awbjcj/pantry-manager
Timeline: 2026-05 – present (`git log --reverse --format=%as 4b66acf`; `git log -1 --format=%as 4b66acf`)

## Tech stack (evidence-backed)

- Python — application services and handlers in `app/`.
- TypeScript — Mini App interface and API contracts in `web/src/`.
- aiogram — Telegram dispatcher and handlers in `app/bot.py` and `app/handlers/`.
- aiohttp — Mini App and connection administration routes in `app/webapp.py` and `app/connection_admin.py`.
- HTTPX — asynchronous messaging and recipe-source requests in `app/messaging/adapters/http.py` and `app/cook/recipe_source.py`.
- SQLModel — household, pantry, messaging, and subscription models in `app/models.py`.
- SQLAlchemy — engine and session construction in `app/db.py`.
- SQLite — file-backed persistence in `app/db.py`.
- Alembic — schema migrations in `migrations/versions/`.
- Pydantic — validated messaging contracts and settings in `app/messaging/contracts.py` and `app/settings.py`.
- APScheduler — per-user reminder scheduling in `app/scheduler.py`.
- Agno — model construction in `app/agno_models.py`.
- Anthropic API — model clients in `app/llm.py`.
- OpenAI API — model clients in `app/llm.py` and `app/cook/llm.py`.
- Google Gemini — model clients in `app/gemini_llm.py`.
- DeepSeek — model clients in `app/deepseek_llm.py`.
- Spoonacular API — recipe source in `app/cook/recipe_source.py`.
- TheMealDB API — recipe source in `app/cook/recipe_source.py`.
- Telegram — messaging adapter in `app/messaging/adapters/telegram.py`.
- Slack — messaging adapter and webhook parsing in `app/messaging/adapters/slack.py` and `app/messaging/ingress.py`.
- WhatsApp — messaging adapter and webhook parsing in `app/messaging/adapters/whatsapp.py` and `app/messaging/ingress.py`.
- React — Mini App interface in `web/src/`.
- Vite — Mini App build configuration in `web/vite.config.ts`.
- pytest — application and fixture tests in `tests/`.
- Playwright — Mini App browser tests in `web/tests/browser/mini-app.spec.ts`.
- Docker — application image in `Dockerfile`.
- GitHub Actions — build and test workflows in `.github/workflows/ci.yml`.

## Architecture highlights

- Built messaging adapters for Telegram, Slack, and WhatsApp around shared event and delivery contracts (`app/messaging/contracts.py`, `app/messaging/adapters/`, `app/messaging/runtime.py`).
- Hardened webhook intake with signature and provider-account checks, then deduplicated admitted events in a persistent inbox (`app/messaging/ingress.py`, `app/messaging/queue_service.py`, `app/connection_admin.py`).
- Routed model requests by capability, preserving the selected text provider while allowing a photo-capable fallback for receipt parsing (`app/providers.py`, `app/llm.py`, `bin/run.py`).
- Built versioned pantry batch actions that reject stale requests and commit item changes together (`app/batch_service.py`, `tests/test_store_batch.py`).
- Ranked sourced recipes using expiry, nutrition, and household preferences while filtering excluded ingredients (`app/cook/service.py`, `app/cook/logic.py`, `app/preference_service.py`).
- Implemented household usage admission and committed payment ledger entries and entitlement updates in one transaction (`app/billing/meter.py`, `app/handlers/billing.py`).
- Reused domain authorization and confirmation flows in the Mini App by dispatching commands and server-owned card actions to existing handlers (`app/miniapp_workspace.py`, `tests/test_miniapp_workspace.py`).
- Localized pantry interactions with static catalogs and cached translations for dynamic names (`app/i18n.py`, `app/translation_service.py`, `web/src/i18n.ts`).

## Quantified outcomes

- Reduced a local pytest-reported full-suite run from 176.25 s to 164.59 s (6.6%) by reusing schema-only SQLite templates; the later run included two additional tests (`docs/testing-performance.md`, commit `75706b3`).
- Counted 968 Python test function or method declarations across 104 files at the source revision by summing per-file counts; this is a static count, not a test-pass or coverage result (`git grep -c -E '^[[:space:]]*(async[[:space:]]+)?def[[:space:]]+test_' 4b66acf -- tests`).

## Skills demonstrated

Languages: Python, TypeScript
Frameworks: aiogram, aiohttp, SQLModel, SQLAlchemy, Pydantic, APScheduler, Agno, React
Databases: SQLite
APIs: Anthropic API, OpenAI API, Google Gemini, DeepSeek, Spoonacular API, TheMealDB API, Telegram, Slack, WhatsApp
Testing: pytest, Playwright
Tooling: HTTPX, Alembic, Vite, Docker, GitHub Actions
