"""
Unit tests for the in-memory blueprint cache:
- TTL expiry deletes stale entries and returns None
- LRU eviction fires when capacity exceeds 200 entries
- set_cached_blueprint stores and is retrievable
"""

import time
from unittest.mock import patch

import pytest

from backend.main import (
    CACHE_TTL_SECS,
    _blueprint_cache,
    get_cached_blueprint,
    set_cached_blueprint,
)
from backend.schemas import (
    BudgetItem,
    EventBlueprintResponse,
    FinancialBlueprint,
    SensoryBlueprint,
    TimelinePhase,
    VendorContractSpec,
)


def _make_blueprint() -> EventBlueprintResponse:
    """Create a minimal valid EventBlueprintResponse for cache testing."""
    return EventBlueprintResponse(
        event_summary="Cache test blueprint — minimal valid fixture for TTL and LRU tests.",
        sensory_concept=SensoryBlueprint(
            lighting_ambiance="2200K amber pillar clusters across venue perimeter",
            acoustic_vibe="Acoustic guitar into vinyl jazz capped at 78dB",
            decor_color_palette=["#1A1D24 Obsidian", "#FFAD32 Amber"],
            signature_experience="Smoked botanical aperitif at dusk",
        ),
        financial_ledger=FinancialBlueprint(
            total_budget=20000.0,
            allocated_budget=18000.0,
            contingency_reserve=2000.0,
            cost_per_guest=200.0,
            items=[
                BudgetItem(
                    category="Venue",
                    item_name="Historic Estate",
                    estimated_cost=10000.0,
                    percentage_of_total=50.0,
                    notes="Includes 10-hour access window",
                )
            ],
        ),
        timeline=[
            TimelinePhase(
                timeframe="T-Minus 12 Weeks",
                phase_title="Foundation Lock",
                action_items=["Sign venue contract", "Pay caterer deposit"],
                critical_deadline="Week 12",
            )
        ],
        vendor_matrix=[
            VendorContractSpec(
                category="Photography",
                estimated_budget=3000.0,
                deliverables=["8 hours coverage", "Full digital gallery"],
                interview_questions=["Do you shoot dual card slots?"],
                required_permits_coi="Commercial General Liability",
            )
        ],
    )


@pytest.fixture(autouse=True)
def clear_cache():
    """Ensure a clean cache before and after every test in this module."""
    _blueprint_cache.clear()
    yield
    _blueprint_cache.clear()


def test_set_and_get_cached_blueprint():
    """Verify that a blueprint stored in cache is retrievable by the same key."""
    key = "test-key-001"
    bp = _make_blueprint()
    set_cached_blueprint(key, bp)
    result = get_cached_blueprint(key)
    assert result is not None
    assert result.event_summary == bp.event_summary


def test_cache_returns_none_for_missing_key():
    """Verify that a cache miss returns None without raising."""
    result = get_cached_blueprint("nonexistent-key-xyz")
    assert result is None


def test_cache_ttl_expiry_returns_none_and_deletes_entry():
    """
    Verify that get_cached_blueprint returns None and DELETES the stale entry
    when the timestamp exceeds CACHE_TTL_SECS.
    """
    key = "ttl-test-key"
    bp = _make_blueprint()

    # Store entry with a timestamp already in the past (beyond TTL)
    stale_ts = time.time() - CACHE_TTL_SECS - 1
    _blueprint_cache[key] = (bp, stale_ts)

    result = get_cached_blueprint(key)

    assert result is None, "Expired entry must return None"
    assert key not in _blueprint_cache, "Expired entry must be deleted from cache"


def test_cache_ttl_valid_entry_is_returned():
    """Verify that a fresh entry within TTL is returned correctly."""
    key = "fresh-key"
    bp = _make_blueprint()

    # Store with a very recent timestamp
    _blueprint_cache[key] = (bp, time.time())

    result = get_cached_blueprint(key)
    assert result is not None
    assert result.financial_ledger.total_budget == 20000.0


def test_cache_lru_eviction_at_capacity():
    """
    Verify that set_cached_blueprint evicts the oldest entry
    when the cache exceeds 200 items.
    """
    bp = _make_blueprint()

    # Fill cache to exactly 200 entries
    oldest_key = "eviction-oldest"
    _blueprint_cache[oldest_key] = (bp, time.time() - 9999)  # very old

    for i in range(199):
        _blueprint_cache[f"fill-key-{i}"] = (bp, time.time())

    assert len(_blueprint_cache) == 200

    # Adding a 201st entry should trigger eviction of the oldest
    set_cached_blueprint("new-entry-triggers-eviction", bp)

    assert len(_blueprint_cache) == 200, "Cache must stay at or under 200 after eviction"
    assert oldest_key not in _blueprint_cache, "Oldest entry must have been evicted"

