"""
Pydantic Schemas for Event Architecture & Production Studio.
Strict Pydantic v2 data models for request validation and structured LLM outputs.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    event_type: str = Field(..., examples=["Wedding"])
    location: str = Field(..., examples=["Napa Valley, CA - Private Vineyard Lawn & Stone Cellar"])
    guest_count: int = Field(..., gt=0, examples=[120])
    currency: str = Field(default="USD", examples=["USD"])
    total_budget: float = Field(..., gt=0, examples=[48000.0])
    weeks_to_event: int = Field(..., gt=0, examples=[36])
    sensory_theme: str = Field(..., examples=["Warm Organic Modernism, muted eucalyptus, raw linen, 2200K amber pillar candles"])
    operational_constraints: Optional[str] = Field(None, examples=["Bride is celiac. Groom's family wants an espresso bar after 10 PM."])


class BudgetItem(BaseModel):
    category: str
    item_name: str
    estimated_cost: float
    percentage_of_total: float
    notes: str


class FinancialBlueprint(BaseModel):
    total_budget: float
    allocated_budget: float
    contingency_reserve: float
    cost_per_guest: float
    items: List[BudgetItem]


class TimelinePhase(BaseModel):
    timeframe: str  # e.g., "T-Minus 36 to 24 Weeks"
    phase_title: str
    action_items: List[str]
    critical_deadline: str


class VendorContractSpec(BaseModel):
    category: str
    estimated_budget: float
    deliverables: List[str]
    interview_questions: List[str]
    required_permits_coi: str


class SensoryBlueprint(BaseModel):
    lighting_ambiance: str
    acoustic_vibe: str
    decor_color_palette: List[str]
    signature_experience: str


class EventBlueprintResponse(BaseModel):
    event_summary: str
    sensory_concept: SensoryBlueprint
    financial_ledger: FinancialBlueprint
    timeline: List[TimelinePhase]
    vendor_matrix: List[VendorContractSpec]
