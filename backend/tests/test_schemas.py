"""
Unit & Contract Tests for Pydantic v2 Schemas and Domain Logic.
"""

import pytest
from pydantic import ValidationError

from backend.schemas import (
    BudgetItem,
    EventBlueprintResponse,
    EventRequest,
    FinancialBlueprint,
    SensoryBlueprint,
    TimelinePhase,
    VendorContractSpec,
)


def test_event_request_valid():
    """Test valid event request creation with all required fields."""
    req = EventRequest(
        event_type="Wedding",
        location="Napa Valley, CA",
        guest_count=120,
        currency="USD",
        total_budget=48000.0,
        weeks_to_event=36,
        sensory_theme="Warm Organic Modernism, 2200K amber candles",
        operational_constraints="Bride is celiac.",
    )
    assert req.guest_count == 120
    assert req.total_budget == 48000.0
    assert req.currency == "USD"


def test_event_request_invalid_budget():
    """Test that zero or negative budgets raise ValidationError."""
    for bad_budget in (0.0, -5000.0):
        with pytest.raises(ValidationError):
            EventRequest(
                event_type="Wedding",
                location="Napa Valley, CA",
                guest_count=100,
                total_budget=bad_budget,
                weeks_to_event=24,
                sensory_theme="Classic Elegance",
            )


def test_event_request_invalid_guest_count():
    """Test that zero or negative guest counts raise ValidationError."""
    with pytest.raises(ValidationError):
        EventRequest(
            event_type="Birthday",
            location="Brooklyn Loft",
            guest_count=0,  # invalid
            total_budget=15000.0,
            weeks_to_event=12,
            sensory_theme="Neon Cyberpunk",
        )


def test_event_request_exceeds_max_guests():
    """Test that a guest_count exceeding 50,000 raises ValidationError."""
    with pytest.raises(ValidationError):
        EventRequest(
            event_type="Festival",
            location="Stadium",
            guest_count=100_001,
            total_budget=5_000_000.0,
            weeks_to_event=52,
            sensory_theme="Massive outdoor stage production",
        )


def test_budget_item_non_negative_cost():
    """Test that a negative estimated_cost raises ValidationError."""
    with pytest.raises(ValidationError):
        BudgetItem(
            category="Venue",
            item_name="Estate",
            estimated_cost=-1.0,  # invalid
            percentage_of_total=30.0,
            notes="Some note",
        )


def test_financial_blueprint_math():
    """Test financial ledger math integrity and contingency reserve."""
    total = 50000.0
    contingency = round(total * 0.10, 2)
    allocated = round(total - contingency, 2)
    guests = 100
    cost_per_guest = round(total / guests, 2)

    ledger = FinancialBlueprint(
        total_budget=total,
        allocated_budget=allocated,
        contingency_reserve=contingency,
        cost_per_guest=cost_per_guest,
        items=[
            BudgetItem(
                category="Venue",
                item_name="Historic Estate",
                estimated_cost=15000.0,
                percentage_of_total=30.0,
                notes="Off-peak discount",
            )
        ],
    )
    assert ledger.contingency_reserve == 5000.0
    assert ledger.allocated_budget == 45000.0
    assert ledger.cost_per_guest == 500.0
    assert len(ledger.items) == 1


def test_full_blueprint_response_structure():
    """Test complete EventBlueprintResponse validation."""
    response = EventBlueprintResponse(
        event_summary="High-craft wedding in Napa Valley with curated sensory design.",
        sensory_concept=SensoryBlueprint(
            lighting_ambiance="2200K amber glow across pillar clusters",
            acoustic_vibe="Vinyl jazz under 78dB for dining",
            decor_color_palette=["#1A1D24 Slate", "#FFAD32 Amber"],
            signature_experience="Smoked botanical aperitif on arrival",
        ),
        financial_ledger=FinancialBlueprint(
            total_budget=40000.0,
            allocated_budget=36000.0,
            contingency_reserve=4000.0,
            cost_per_guest=400.0,
            items=[
                BudgetItem(
                    category="Catering",
                    item_name="Farm to table feast",
                    estimated_cost=18000.0,
                    percentage_of_total=45.0,
                    notes="Locally sourced seasonal menu",
                )
            ],
        ),
        timeline=[
            TimelinePhase(
                timeframe="T-Minus 24 Weeks",
                phase_title="Venue & Concept Lock",
                action_items=["Sign contract", "Secure deposit"],
                critical_deadline="Week 24",
            )
        ],
        vendor_matrix=[
            VendorContractSpec(
                category="Photography",
                estimated_budget=4500.0,
                deliverables=["10 hours coverage", "Full digital master"],
                interview_questions=["Do you shoot dual card slots?"],
                required_permits_coi="Commercial General Liability",
            )
        ],
    )
    assert response.sensory_concept.lighting_ambiance == "2200K amber glow across pillar clusters"
    assert len(response.vendor_matrix) == 1
    assert response.financial_ledger.contingency_reserve == 4000.0
