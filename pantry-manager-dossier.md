---
repo_url: https://github.com/awbjcj/pantry-manager
repo_name: food-manager
role: maintainer
generated_at: 2026-11-04
---

# Project: Pantry Manager

## Summary

Pantry Manager is a household food tracker that accepts receipt photos and text, tracks expiry dates, and suggests recipes and meal plans. It supports Telegram, Slack, and WhatsApp, with a Telegram Mini App for browser access (`app/messaging/`, `app/miniapp_workspace.py`). Household members share pantry data while choosing their own language and model provider (`app/models.py`, `app/providers.py`). The maintainer implemented the messaging runtime and pantry batch workflow (commits `a26af884`, `171e6e5c`). The repository is active.

Role: maintainer (465 of 485 reachable commits across the owner's Git identities; the remaining 20 are automation-account commits, including an application-code change in `b697244`; `git shortlog -sne 3b44ed7`; `git rev-list --count 3b44ed7`)
Repository: https://github.com/awbjcj/pantry-manager
Timeline: 2026-05 – present (`git log --reverse --format=%as 3b44ed7`; `git log -1 --format=%as 3b44ed7`)
Project context: unknown

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
- cryptography — encrypted managed messaging credentials in `app/messaging/connection_service.py`.
- OAuth 2.0 — Slack connection authorization in `app/connection_admin.py`.
- APScheduler — per-user reminder scheduling in `app/scheduler.py`.
- Agno — model construction in `app/agno_models.py`.
- Anthropic API — model clients in `app/llm.py`.
- OpenAI API — model clients in `app/llm.py` and `app/cook/llm.py`.
- Google Gemini — model clients in `app/gemini_llm.py`.
- DeepSeek — model clients in `app/deepseek_llm.py`.
- Spoonacular API — recipe source in `app/cook/recipe_source.py`.
- TheMealDB API — recipe source in `app/cook/recipe_source.py`, wired at bootstrap in `bin/run.py`.
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
- Prevented automatic repetition of uncertain in-flight sends and paid operations after a restart by marking them unknown (`app/messaging/queue_service.py:recover_interrupted`, `app/messaging/runtime.py:MessagingRuntime.start`; commit `a26af884`).
- Restricted queued deliveries after membership revocation by checking the saved household and membership generation before sending (`app/messaging/runtime.py:MessagingRuntime.send_one`, `tests/test_messaging.py:test_revocation_suppresses_pending_delivery_and_restart_never_repeats_unknown`; commit `a26af884`).
- Protected managed provider credentials with encryption and bound Slack OAuth 2.0 state to an admin session, expiry, and connection revision (`app/messaging/connection_service.py:SecretStore`, `app/connection_admin.py:ConnectionAdmin.oauth_callback`; commit `a26af884`).
- Routed model requests by capability, preserving the selected text provider while allowing a photo-capable fallback for receipt parsing (`app/providers.py`, `app/llm.py`, `bin/run.py`).
- Modeled forward-only food storage transitions and recalculated expiry from a shared purchase-or-storage date (`app/storage_state.py`, `tests/test_fridge_storage.py:test_origin_and_expiry_use_stored_on_when_present`; commit `c3fda98e`).
- Resolved fridge and frozen shelf life through household cache, a local FoodKeeper table, optional search, and a default (`app/frozen_shelf_life.py:resolve_storage_days`; commit `c3fda98e`).
- Built versioned pantry batch actions that reject stale requests and commit item changes together (`app/batch_service.py`, `tests/test_store_batch.py`).
- Ranked sourced recipes using expiry, nutrition, and household preferences while filtering excluded ingredients (`app/cook/service.py`, `app/cook/logic.py`, `app/preference_service.py`).
- Implemented household usage admission and committed payment ledger entries and entitlement updates in one transaction (`app/billing/meter.py`, `app/handlers/billing.py`).
- Prevented a replayed payment from granting a top-up twice by checking its charge ID before committing the ledger and entitlement (`app/handlers/billing.py:handle_successful_payment`, `tests/test_v60_payments.py:test_replayed_topup_is_not_double_granted`; commit `c8455e37`).
- Reused domain authorization and confirmation flows in the Mini App by dispatching commands and server-owned card actions to existing handlers (`app/miniapp_workspace.py`, `tests/test_miniapp_workspace.py`).
- Acknowledged callbacks before deferred work and retried failed message edits as fresh messages (`app/callback_dispatch.py:apply`, `app/callback_dispatch.py:edit_or_resend`; commits `a075fe44`, `26e1fff0`).
- Localized pantry interactions with static catalogs and cached translations for dynamic names (`app/i18n.py`, `app/translation_service.py`, `web/src/i18n.ts`).

## Quantified outcomes

- Reduced one local pytest-reported full-suite run from 176.25 s to 164.59 s (6.6%) after reusing schema-only SQLite templates; the later serial run included two additional fixture tests (`docs/testing-performance.md`, commit `75706b3`).
- Reduced the summed test-phase time for seven affected modules from 43.97 s to 14.17 s (67.8%) in the same local comparison (`docs/testing-performance.md`, commit `75706b3`).
- Counted 968 Python test function or method declarations across 104 files at revision `3b44ed7` by summing per-file counts; this is a static count, not a test-pass or coverage result (`git grep -c -E '^[[:space:]]*(async[[:space:]]+)?def[[:space:]]+test_' 3b44ed7 -- tests`).

## Skills demonstrated

### Languages

- Name: Python
  - Context: Built asynchronous receipt ingestion and shelf-life resolution for household pantry records.
  - Evidence:
    - Parsed receipt photos and created pantry records — `app/ingest_service.py:ingest_photo` (commit `5b745c76`).
    - Resolved item shelf lives using cached and model-provided estimates — `app/ingest_service.py:compute_shelf_life` (commit `5b745c76`).
- Name: TypeScript
  - Context: Implemented typed browser requests and locale-aware Mini App text.
  - Evidence:
    - Sent workspace actions and returned typed workspace state — `web/src/api.ts:workspaceAction` (commit `28b4a9ea`).
    - Resolved localized message keys and interpolation values — `web/src/i18n.ts:t` (commit `45aacef0`).

### Frameworks

- Name: aiogram
  - Context: Connected Telegram updates and message delivery to the application handlers.
  - Evidence:
    - Built the dispatcher and registered command and callback handlers — `app/bot.py:build_dispatcher` (commit `85cc0a16`).
    - Sent and updated messages through the bot adapter — `app/messaging/adapters/telegram.py:TelegramAdapter.deliver` (commit `a26af884`).
- Name: aiohttp
  - Context: Exposed authenticated Mini App operations through an asynchronous web server.
  - Evidence:
    - Registered account and workspace routes — `app/webapp.py:build_web_app` (commit `3463a8d7`).
    - Accepted workspace actions and delegated them to the workspace runtime — `app/webapp.py:MiniAppApi.workspace_action` (commit `28b4a9ea`).
- Name: SQLModel
  - Context: Modeled pantry records and durable messaging events as database tables.
  - Evidence:
    - Defined household-scoped pantry items and their expiry data — `app/models.py:PantryItem` (commit `0512d6b3`).
    - Defined persisted inbound messages for event admission — `app/models.py:MessagingInbox` (commit `a26af884`).
- Name: SQLAlchemy
  - Context: Configured database connections and used conditional updates to protect batch changes.
  - Evidence:
    - Installed connection event hooks for database pragmas — `app/db.py:make_engine` (commit `e51332fa`).
    - Used a version-checked update before changing selected items — `app/batch_service.py:change_selection` (commit `171e6e5c`).
- Name: Pydantic
  - Context: Validated model output and cross-object messaging boundaries.
  - Evidence:
    - Defined typed fields for parsed receipt items — `app/llm.py:ParsedItem` (commit `5b745c76`).
    - Rejected incoming events whose actor, conversation, or content refer to another connection — `app/messaging/contracts.py:IncomingEvent.same_connection` (commit `a26af884`).
- Name: cryptography
  - Aliases: Python cryptography
  - Context: Encrypted managed messaging credentials before storing them and rejected missing keys or invalid ciphertext.
  - Evidence:
    - Serialized and encrypted connection credentials with Fernet — `app/messaging/connection_service.py:SecretStore.encrypt` (commit `a26af884`).
    - Decrypted credentials for the runtime and rejected invalid ciphertext — `app/messaging/connection_service.py:SecretStore.decrypt` (commit `a26af884`).
- Name: APScheduler
  - Context: Scheduled per-user digests and cleanup jobs.
  - Evidence:
    - Registered a digest job using the user's configured hour and time zone — `app/scheduler.py:schedule_user_digest` (commit `85cc0a16`).
    - Registered a recurring sweep for expired pending corrections — `app/scheduler.py:register_sweep_expired_pendings` (commit `9b283950`).
- Name: Agno
  - Context: Constructed provider-backed agents with structured intent output.
  - Evidence:
    - Selected model adapters and gateway configuration from provider credentials — `app/agno_models.py:build_agno_model` (commit `28b3e997`).
    - Built an intent agent with an output schema — `app/nl_intent.py:build_intent_agent` (commit `6b4d5246`).
- Name: React
  - Context: Built the Mini App's account views and interactive pantry workspace.
  - Evidence:
    - Managed workspace actions, loading state, and form drafts — `web/src/Workspace.tsx:WorkspaceView` (commits `28b4a9ea`, `b6329586`).
    - Composed navigation and account screens — `web/src/App.tsx:App` (commit `3463a8d7`).

### Databases

- Name: SQLite
  - Context: Used file-backed databases for the application and isolated copies for tests.
  - Evidence:
    - Enabled write-ahead logging and foreign-key checks on connections — `app/db.py:make_engine` (commit `0512d6b3`; connection pragmas added in `e51332f`).
    - Copied a schema-only database into each test's temporary directory — `tests/conftest.py:sqlite_db_path` (commit `75706b37`).

### Cloud & Infra

- Name: OAuth 2.0
  - Aliases: OAuth2
  - Context: Implemented Slack installation with session-bound, expiring authorization state.
  - Evidence:
    - Generated a state token tied to the admin session and connection revision — `app/connection_admin.py:ConnectionAdmin.oauth_start` (commit `a26af884`).
    - Consumed the state once and rejected expired, mismatched, or stale connection requests — `app/connection_admin.py:ConnectionAdmin.oauth_callback` (commit `a26af884`).
    - Tested that the state belongs to its original session and cannot be reused — `tests/test_messaging_runtime.py:test_slack_oauth_state_is_session_bound_and_single_use` (commit `a26af884`).
- Name: Anthropic API
  - Context: Integrated receipt-image parsing and natural-language pantry commands.
  - Evidence:
    - Submitted receipt images with a parsing tool and validated the result — `app/llm.py:AnthropicLLMClient.extract_items_from_image` (commit `23aefd91`).
    - Parsed natural-language additions and corrections against a schema — `app/llm.py:AnthropicTextLLMClient` (commit `c839726d`).
- Name: OpenAI API
  - Context: Integrated structured receipt and text parsing through the provider's model clients.
  - Evidence:
    - Sent receipt images and parsed structured results — `app/llm.py:OpenAILLMClient.extract_items_from_image` (commit `5a0571fb`).
    - Implemented text parsing for pantry additions and corrections — `app/llm.py:OpenAITextLLMClient` (commit `5a0571fb`).
- Name: Google Gemini
  - Context: Added image parsing and search-backed shelf-life lookup.
  - Evidence:
    - Extracted receipt items from images — `app/gemini_llm.py:GeminiLLMClient.extract_items_from_image` (commit `c7ea58b0`).
    - Queried shelf-life information with search grounding — `app/gemini_llm.py:GeminiSearchClient.lookup_shelf_life` (commit `c7ea58b0`).
- Name: DeepSeek
  - Context: Added text parsing and a separate shelf-life search client.
  - Evidence:
    - Parsed pantry additions and corrections — `app/deepseek_llm.py:DeepSeekTextLLMClient` (commit `c7ea58b0`).
    - Implemented a web-search shelf-life lookup — `app/deepseek_llm.py:DeepSeekSearchClient` (commit `5a48532e`).
- Name: Spoonacular API
  - Context: Queried recipes using pantry ingredients and household constraints.
  - Evidence:
    - Mapped diet, exclusions, and ingredient criteria into request parameters — `app/cook/recipe_source.py:spoonacular_params` (commit `5faf297e`).
    - Fetched and mapped recipe results into application candidates — `app/cook/recipe_source.py:SpoonacularSource.search` (commit `43a4b5f5`).
- Name: TheMealDB API
  - Context: Implemented a recipe source with ingredient search and detail lookup and added it to the configured source chain.
  - Evidence:
    - Fetched recipe details and mapped their ingredients — `app/cook/recipe_source.py:TheMealDbSource` (commit `87276a20`).
    - Tested mapping when nutrition data is unavailable — `tests/test_recipe_source.py:test_themealdb_source_maps_recipe_without_nutrition` (commit `87276a20`).
    - Added the source to the application bootstrap — `bin/run.py:485-487` (commit `d9870fc4`).
- Name: Telegram
  - Context: Delivered pantry messages and handled receipt media through a messaging adapter.
  - Evidence:
    - Sent or updated chat messages with action buttons — `app/messaging/adapters/telegram.py:TelegramAdapter.deliver` (commit `a26af884`).
    - Downloaded receipt images through the bot connection — `app/messaging/adapters/telegram.py:TelegramAdapter.download_image` (commit `a26af884`).
- Name: Slack
  - Context: Added workspace message delivery and authenticated event intake.
  - Evidence:
    - Sent messages and action blocks to a workspace — `app/messaging/adapters/slack.py:SlackAdapter.deliver` (commit `a26af884`).
    - Checked webhook signatures and request age — `app/messaging/ingress.py:verify_slack` (commit `a26af884`).
- Name: WhatsApp
  - Context: Added message delivery and authenticated webhook intake.
  - Evidence:
    - Sent messages and interactive choices through the provider — `app/messaging/adapters/whatsapp.py:WhatsAppAdapter.deliver` (commit `a26af884`).
    - Verified webhook signatures before processing — `app/messaging/ingress.py:verify_whatsapp` (commit `a26af884`).

### Testing

- Name: pytest
  - Context: Wrote regression cases for database isolation, pantry changes, storage rules, and delivery recovery.
  - Evidence:
    - Checked that copied schemas start empty and retain real commits — `tests/test_database_fixtures.py:test_schema_copy_starts_empty_and_preserves_real_commits` (commit `75706b37`).
    - Tested rollback when a selected batch row is missing — `tests/test_store_batch.py:test_batch_atomic_rollback_and_missing_selected_row` (commit `87db2f65`).
    - Tested forward-only storage changes and expiry calculation — `tests/test_fridge_storage.py:test_forward_only_transitions`, `tests/test_fridge_storage.py:test_origin_and_expiry_use_stored_on_when_present` (commit `c3fda98e`).
    - Checked that a rate-limited send is retried while an unknown delivery is not repeated — `tests/test_messaging_runtime.py:test_sender_rate_limit_retries_but_unknown_is_terminal` (commit `a26af884`).
- Name: Playwright
  - Context: Exercised Mini App forms and confirmation behavior in browser tests.
  - Evidence:
    - Checked that editing a pending change requires renewed confirmation — `web/tests/browser/mini-app.spec.ts:113-129` (commit `b6329586`).
    - Checked that invalid receipt files are rejected before upload — `web/tests/browser/mini-app.spec.ts:188-198` (commit `b6329586`).

### Architecture

- Name: API design
  - Context: Separated provider-specific messaging from shared application events and actions.
  - Evidence:
    - Defined a delivery and media-download adapter contract — `app/messaging/contracts.py:MessagingAdapter` (commit `a26af884`).
    - Dispatched browser workspace actions to existing command and callback handlers — `app/miniapp_workspace.py:WorkspaceRuntime._run` (commit `28b4a9ea`).
- Name: Security
  - Context: Validated webhook requests, protected managed credentials, and checked identity before linking accounts or sending messages.
  - Evidence:
    - Checked signed requests and rejected stale Slack events — `app/messaging/ingress.py:verify_slack` (commit `a26af884`).
    - Required the original account to confirm a pending account link — `app/messaging/identity_service.py:confirm_link` (commit `a26af884`).
    - Checked Mini App users against household authorization before serving account data — `app/webapp.py:MiniAppApi.authorized_user` (commit `5c39dea1`).
    - Suppressed queued messages when the saved membership no longer matched the current user — `app/messaging/runtime.py:MessagingRuntime.send_one` (commit `a26af884`).
    - Returned credential presence rather than the stored credential in connection details — `app/messaging/connection_service.py:public_connection` (commit `a26af884`).
- Name: Data privacy
  - Context: Limited exposure of managed credentials and old inbound message content.
  - Evidence:
    - Kept managed provider credentials encrypted and omitted their values from the connection response — `app/messaging/connection_service.py:SecretStore.encrypt`, `app/messaging/connection_service.py:public_connection` (commit `a26af884`).
    - Cleared content from completed, failed, and unknown inbox records older than 30 days during startup recovery while retaining their deduplication keys — `app/messaging/queue_service.py:recover_interrupted`, `app/messaging/runtime.py:MessagingRuntime.start` (commit `a26af884`).
- Name: Concurrency
  - Context: Protected state changes from stale requests and isolated shared-agent sessions.
  - Evidence:
    - Claimed a batch version before changing pantry items — `app/batch_service.py:change_selection` (commit `171e6e5c`).
    - Assigned a fresh session identifier to each intent request — `app/nl_intent.py:AgnoIntentAgent.parse` (commit `6001ef0d`).
- Name: Domain modeling
  - Context: Modeled food storage as forward-only states and based expiry on the applicable purchase or storage date.
  - Evidence:
    - Defined valid storage transitions and the shared expiry formula — `app/storage_state.py:next_storage_options`, `app/storage_state.py:compute_expiry` (commit `c3fda98e`).
    - Resolved storage-specific durations through the cache, local reference data, search, and fallback — `app/frozen_shelf_life.py:resolve_storage_days` (commit `c3fda98e`).
    - Tested that chilling and then freezing resets the shelf-life origin — `tests/test_fridge_storage.py:test_chill_then_freeze_resets_origin_and_shelf_life` (commit `c3fda98e`).
- Name: Reliability engineering
  - Context: Distinguished retryable failures from uncertain external outcomes and kept interactive callbacks responsive.
  - Evidence:
    - Marked interrupted inbox processing and outbox sends unknown rather than repeating potentially completed work — `app/messaging/queue_service.py:recover_interrupted` (commit `a26af884`).
    - Tested that a rate-limited delivery can retry while an unknown send is terminal — `tests/test_messaging_runtime.py:test_sender_rate_limit_retries_but_unknown_is_terminal` (commit `a26af884`).
    - Acknowledged callbacks before deferred work and attempted a fresh message after an unsuccessful edit — `app/callback_dispatch.py:apply`, `app/callback_dispatch.py:edit_or_resend` (commits `a075fe44`, `26e1fff0`).
- Name: Database transactions
  - Context: Kept batch mutations and payment entitlement changes consistent.
  - Evidence:
    - Committed a batch result and its item updates together, with rollback on error — `app/batch_service.py:change_selection` (commit `171e6e5c`).
    - Staged a payment ledger entry and entitlement update before committing — `app/handlers/billing.py:handle_successful_payment` (commit `c8455e37`).
- Name: Internationalization
  - Context: Rendered interface text in the user's language and cached dynamic-name translations.
  - Evidence:
    - Rendered per-language messages with English fallback — `app/i18n.py:t` (commit `6863d81d`).
    - Reused cached name translations and fell back when translation failed — `app/translation_service.py:translate_texts` (commit `cf38b0f3`).
- Name: Ranking algorithms
  - Context: Scored recipe candidates against nutrition, expiry, and household preferences.
  - Evidence:
    - Combined candidate attributes and household preferences, then sorted by final score — `app/cook/service.py:_score_sourced` (commits `f9835f7f`, `87db2f65`).
    - Calculated the weighted score from nutrition and pantry-use signals — `app/cook/logic.py:blended_score` (commit `deec12b0`).
- Name: Payment processing
  - Context: Validated purchases and applied household entitlements.
  - Evidence:
    - Checked the payer and purchase payload before checkout — `app/handlers/billing.py:_validate_checkout` (commit `c8455e37`).
    - Recorded successful payments and applied a subscription or top-up — `app/handlers/billing.py:handle_successful_payment` (commit `c8455e37`).
- Name: Usage metering
  - Context: Applied household quota limits and recorded usage and model costs.
  - Evidence:
    - Evaluated receipt, action, and cost limits before admitting work — `app/billing/meter.py:admit` (commit `74957dfb`).
    - Recorded operation counts and cost against household usage — `app/billing/meter.py:commit` (commit `74957dfb`).
- Name: Performance optimization
  - Context: Reduced repeated test database setup and moved pantry statistics into aggregate queries.
  - Evidence:
    - Reused an empty schema template across isolated test files — `tests/conftest.py:_empty_sqlite_schema` (commit `75706b37`).
    - Aggregated pantry statistics in database queries instead of loading full records — `app/pantry_service.py:compute_stats` (commit `f62d384`).
- Name: LLM integration
  - Context: Routed model work by capability and validated receipt responses.
  - Evidence:
    - Selected a configured provider with optional capability fallback — `app/providers.py:ProviderSelector.for_provider` (commit `92ff624d`).
    - Validated receipt output and retried a malformed result with the original image — `app/llm.py:AnthropicLLMClient.extract_items_from_image` (commit `23aefd91`).

### Tooling

- Name: HTTPX
  - Context: Used asynchronous HTTP requests for messaging-provider integrations.
  - Evidence:
    - Streamed receipt media only from allowed provider hosts — `app/messaging/adapters/http.py:download` (commit `a26af884`).
    - Classified rate limits, authentication failures, and ambiguous sends — `app/messaging/adapters/http.py:json_request` (commit `a26af884`).
- Name: Alembic
  - Context: Versioned schema changes and configured online migrations.
  - Evidence:
    - Added receipt store names and the persisted pantry batch table — `migrations/versions/0022_receipt_store_batch.py:upgrade` (commit `171e6e5c`).
    - Configured migration execution against the application database — `migrations/env.py:run_migrations_online` (commit `0512d6b3`).
- Name: Vite
  - Context: Configured development proxying and production builds for the Mini App.
  - Evidence:
    - Enabled the React plugin, local API proxy, and build output directory — `web/vite.config.ts:4-11` (commit `3463a8d7`).
    - Defined the type-check and production build command — `web/package.json:10` (commit `3463a8d7`).
- Name: Docker
  - Context: Packaged the browser build and Python application in a multi-stage image.
  - Evidence:
    - Copied built browser assets into the application image — `Dockerfile:26` (commit `3463a8d7`).
    - Configured the container to start the application entry point — `Dockerfile:38` (commit `c342a5b4`).
- Name: GitHub Actions
  - Context: Automated application checks, container builds, and releases.
  - Evidence:
    - Added an empty-database migration check and test run to the quality workflow — `.github/workflows/ci.yml:54-60` (commit `efdea780`; test timing update `75706b37`).
    - Configured version tagging and weekly release publication — `.github/workflows/release.yml:40-55` (commit `2fcc369f`).
