"""
Pydantic Schemas for Event Architecture & Production Studio.
Strict Pydantic v2 data models for request validation and structured LLM outputs.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    event_type: str = Field(..., min_length=2, max_length=120, examples=["Wedding"])
    location: str = Field(
        ..., min_length=2, max_length=300,
        examples=["Napa Valley, CA - Private Vineyard Lawn & Stone Cellar"],
    )
    guest_count: int = Field(..., gt=0, le=50_000, examples=[120])
    currency: str = Field(default="USD", min_length=3, max_length=10, examples=["USD"])
    total_budget: float = Field(..., gt=0, examples=[48000.0])
    weeks_to_event: int = Field(..., gt=0, le=520, examples=[36])
    sensory_theme: str = Field(
        ..., min_length=5, max_length=500,
        examples=["Warm Organic Modernism, muted eucalyptus, raw linen, 2200K amber pillar candles"],
    )
    operational_constraints: Optional[str] = Field(
        None, max_length=1000,
        examples=["Bride is celiac. Groom's family wants an espresso bar after 10 PM."],
    )


class BudgetItem(BaseModel):
    category: str = Field(..., min_length=1, max_length=120)
    item_name: str = Field(..., min_length=1, max_length=255)
    estimated_cost: float = Field(..., ge=0)
    percentage_of_total: float = Field(..., ge=0, le=100)
    notes: str = Field(..., max_length=500)


class FinancialBlueprint(BaseModel):
    total_budget: float = Field(..., gt=0)
    allocated_budget: float = Field(..., ge=0)
    contingency_reserve: float = Field(..., ge=0)
    cost_per_guest: float = Field(..., gt=0)
    items: List[BudgetItem] = Field(..., min_length=1)


class TimelinePhase(BaseModel):
    timeframe: str = Field(..., min_length=1, max_length=120)  # e.g. "T-Minus 36 to 24 Weeks"
    phase_title: str = Field(..., min_length=1, max_length=200)
    action_items: List[str] = Field(..., min_length=1)
    critical_deadline: str = Field(..., min_length=1, max_length=200)


class VendorContractSpec(BaseModel):
    category: str = Field(..., min_length=1, max_length=120)
    estimated_budget: float = Field(..., ge=0)
    deliverables: List[str] = Field(..., min_length=1)
    interview_questions: List[str] = Field(..., min_length=1)
    required_permits_coi: str = Field(..., max_length=500)


class SensoryBlueprint(BaseModel):
    lighting_ambiance: str = Field(..., min_length=5, max_length=500)
    acoustic_vibe: str = Field(..., min_length=5, max_length=500)
    decor_color_palette: List[str] = Field(..., min_length=1)
    signature_experience: str = Field(..., min_length=5, max_length=500)


class EventBlueprintResponse(BaseModel):
    event_summary: str = Field(..., min_length=20, max_length=1000)
    sensory_concept: SensoryBlueprint
    financial_ledger: FinancialBlueprint
    timeline: List[TimelinePhase] = Field(..., min_length=1)
    vendor_matrix: List[VendorContractSpec] = Field(..., min_length=1)
