"""
Pydantic Schemas for Event Planning Assistant
Defines strict data contracts for input profiles and structured GenAI outputs.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class EventProfileRequest(BaseModel):
    event_type: str = Field(
        ...,
        description="Type of event: Wedding, Milestone Birthday, Community Gala, Corporate Retreat, etc.",
        examples=["Wedding"]
    )
    guest_count: int = Field(
        ...,
        ge=1,
        le=50000,
        description="Estimated number of guests attending",
        examples=[120]
    )
    total_budget: float = Field(
        ...,
        gt=0,
        description="Maximum budget allocated for the event",
        examples=[45000.0]
    )
    currency: str = Field(
        default="USD",
        description="Currency code: USD ($), EUR (€), GBP (£), INR (₹), CAD ($), AUD ($), etc.",
        examples=["USD"]
    )
    location: str = Field(
        ...,
        description="City, venue type, indoor/outdoor specifics",
        examples=["Napa Valley, CA - Outdoor Vineyard & Historic Cellar"]
    )
    aesthetic_vibe: str = Field(
        ...,
        description="Desired mood, aesthetic concept, styling preferences",
        examples=["Warm Organic Modernism, muted eucalyptus, raw linen, and golden hour ambient lighting"]
    )
    custom_notes: Optional[str] = Field(
        default="",
        description="Dietary requirements, accessibility needs, must-have moments"
    )
    timeline_urgency_weeks: Optional[int] = Field(
        default=26,
        ge=1,
        le=156,
        description="Weeks until event date"
    )


# -------------------------------------------------------------
# 1. Creative Concepts & Atmosphere
# -------------------------------------------------------------

class ColorSwatch(BaseModel):
    name: str = Field(..., description="Descriptive name of the color")
    hex_code: str = Field(..., description="Hex code, e.g. #2C3E50")
    usage_role: str = Field(..., description="Primary, Accent, Foundation, or Ambient")


class SensoryAtmosphere(BaseModel):
    lighting_design: str = Field(..., description="Lighting layout, candle warmth, luminary accents")
    acoustic_profile: str = Field(..., description="Musical cues, sound levels across zones")
    tactile_textures: str = Field(..., description="Materials like raw stoneware, matte linen, velvet, polished wood")
    scent_and_botanicals: str = Field(..., description="Signature botanicals, seasonal florals, scent atmosphere")


class SignatureMoment(BaseModel):
    moment_name: str
    timing: str
    description: str
    wow_factor_detail: str


class InteractiveActivity(BaseModel):
    activity_name: str
    audience_fit: str
    description: str
    setup_requirement: str


class IdeasResponse(BaseModel):
    theme_title: str
    tagline: str
    creative_narrative: str
    color_palette: List[ColorSwatch]
    sensory_atmosphere: SensoryAtmosphere
    signature_moments: List[SignatureMoment]
    interactive_activities: List[InteractiveActivity]


# -------------------------------------------------------------
# 2. Financial Breakdown & Itemized Budget
# -------------------------------------------------------------

class BudgetItem(BaseModel):
    category: str = Field(..., description="Venue, Catering, Decor, AV & Music, Photo/Video, Logistics, etc.")
    item_name: str = Field(..., description="Item or service title")
    estimated_cost: float = Field(..., ge=0, description="Estimated cost in designated currency")
    percentage_of_budget: float = Field(..., description="Percentage of total budget")
    priority: str = Field(..., description="Essential, High-Impact, or Optional Upgrade")
    pro_negotiation_tip: str = Field(..., description="Actionable insider tip to reduce cost or extract value")


class BudgetResponse(BaseModel):
    total_budget: float
    allocated_subtotal: float
    contingency_reserve: float
    cost_per_guest: float
    currency: str
    items: List[BudgetItem]
    financial_health_summary: str
    top_cost_saving_levers: List[str]


# -------------------------------------------------------------
# 3. Timeline Roadmap & Day-Of Run-of-Show
# -------------------------------------------------------------

class PlanningMilestone(BaseModel):
    phase: str = Field(..., description="e.g. Phase 1 (Initial Blueprint), Phase 2 (Vendor Locking), etc.")
    timeframe: str = Field(..., description="e.g. 6-9 Months Out, 2-4 Weeks Out")
    action_items: List[str]
    critical_deadline: str
    responsible_party: str


class DayOfScheduleItem(BaseModel):
    time_window: str = Field(..., description="e.g. 09:00 AM - 10:30 AM")
    segment_title: str
    description: str
    coordinator_in_charge: str
    buffer_minutes: int


class TimelineResponse(BaseModel):
    planning_milestones: List[PlanningMilestone]
    day_of_run_of_show: List[DayOfScheduleItem]
    buffer_strategy: str
    critical_path_warning: str


# -------------------------------------------------------------
# 4. Vendor Management & Interview Guides
# -------------------------------------------------------------

class VendorCategoryGuide(BaseModel):
    vendor_type: str = Field(..., description="Venue, Catering, Photo/Video, Florist, DJ/Band, Lighting/AV")
    recommended_budget_allocation: str
    sourcing_checklist: List[str]
    hard_hitting_interview_questions: List[str]
    contract_red_flags: List[str]
    key_deliverables_to_lock: List[str]


class VendorsResponse(BaseModel):
    vendor_categories: List[VendorCategoryGuide]
    contract_golden_rules: List[str]
    liability_and_permit_advice: str


# -------------------------------------------------------------
# 5. Master Cohesive Plan
# -------------------------------------------------------------

class FullEventPlanResponse(BaseModel):
    profile: EventProfileRequest
    ideas: IdeasResponse
    budget: BudgetResponse
    timeline: TimelineResponse
    vendors: VendorsResponse
    generated_at: str
    model_used: str
    status: str = "success"
