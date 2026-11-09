"""Pending actions are claimed and applied in the same database transaction."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, date, datetime, timedelta
from threading import Barrier
from unittest.mock import AsyncMock

import pytest
from sqlmodel import Session, select

import app.callbacks.pending as pending_callbacks
from app.application.context import ActionContext
from app.correction_service import AddPayload, add_payload_to_json
from app.db import make_engine
from app.i18n import t
from app.models import Household, PantryItem, PendingCorrection
from app.pending_service import create_pending


@pytest.fixture
def pending_db(sqlite_db_path):
    engine = make_engine(str(sqlite_db_path))
    today = date.today()
    payload = AddPayload(
        name="Milk",
        shelf_life_days=7,
        expires_on=today + timedelta(days=7),
        purchased_on=today,
        shelf_life_source="manual_fallback",
        ingest_shelf_life_source="manual_fallback",
        explicit_user_expiry=False,
        confidence=1,
    )
    with Session(engine) as session:
        session.add(Household(id=1, created_at=datetime.now(UTC)))
        session.commit()
        pending = create_pending(
            session, household_id=1, action_type="add", item_id=None,
            proposed_json=add_payload_to_json(payload), snapshot_json=None,
            cost_micros_usd=None, chat_id=1, now=datetime.now(UTC),
        )
        pending_id = pending.id
        assert pending_id is not None
    yield engine, pending_id, today
    engine.dispose()


@pytest.mark.parametrize("verbs", [("apply", "apply"), ("apply", "cancel")])
def test_concurrent_callbacks_claim_a_pending_action_only_once(pending_db, monkeypatch, verbs):
    engine, pending_id, today = pending_db
    barrier = Barrier(2)
    load_pending = pending_callbacks.load_pending

    def synchronized_load(session, **kwargs):
        pending = load_pending(session, **kwargs)
        assert pending is not None and pending.status == "pending"
        barrier.wait(timeout=10)
        return pending

    monkeypatch.setattr(pending_callbacks, "load_pending", synchronized_load)

    def callback(verb):
        acknowledge = AsyncMock()
        cb = ActionContext(actor_id=1, data=None, source=None, acknowledge=acknowledge)
        with Session(engine) as session:
            asyncio.run(pending_callbacks._handle_pending_callback(
                cb, session=session, today=today, household_id=1,
                pending_id=pending_id, verb=verb,
            ))
        assert acknowledge.await_args is not None
        return acknowledge.await_args.args[0]

    with ThreadPoolExecutor(max_workers=2) as pool:
        acknowledgements = list(pool.map(callback, verbs))

    with Session(engine) as session:
        pending = session.get(PendingCorrection, pending_id)
        assert pending is not None
        items = session.exec(select(PantryItem)).all()
        assert pending.status in ("applied", "cancelled")
        assert len(items) == (1 if pending.status == "applied" else 0)
        assert t("toast.already_status", "en", status=pending.status) in acknowledgements
        assert (
            t("toast.added", "en") if pending.status == "applied"
            else t("toast.cancelled", "en")
        ) in acknowledgements


async def test_failed_add_rolls_back_the_claim_and_can_be_retried(pending_db, monkeypatch):
    engine, pending_id, today = pending_db
    real_apply = pending_callbacks.apply_add

    def fail_after_insert(*args, **kwargs):
        real_apply(*args, **kwargs)
        raise RuntimeError("simulated write failure")

    def context():
        return ActionContext(actor_id=1, data=None, source=None, acknowledge=AsyncMock())

    with monkeypatch.context() as patch:
        patch.setattr(pending_callbacks, "apply_add", fail_after_insert)
        with Session(engine) as session, pytest.raises(RuntimeError, match="simulated"):
            await pending_callbacks._handle_pending_callback(
                context(), session=session, today=today, household_id=1,
                pending_id=pending_id, verb="apply",
            )

    with Session(engine) as session:
        pending = session.get(PendingCorrection, pending_id)
        assert pending is not None and pending.status == "pending"
        assert not session.exec(select(PantryItem)).all()
        await pending_callbacks._handle_pending_callback(
            context(), session=session, today=today, household_id=1,
            pending_id=pending_id, verb="apply",
        )

    with Session(engine) as session:
        pending = session.get(PendingCorrection, pending_id)
        assert pending is not None and pending.status == "applied"
        assert len(session.exec(select(PantryItem)).all()) == 1
