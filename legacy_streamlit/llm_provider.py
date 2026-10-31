"""
Modular LLM Provider Architecture
Supports Groq API with structured JSON output, retry/timeout handling,
and graceful fallback generation.
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

import groq
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LLMProvider")

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM providers."""

    @abstractmethod
    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> Dict[str, Any]:
        """
        Generate a structured JSON response from the LLM.
        Must return a parsed Python dictionary.
        """
        pass


class GroqProvider(BaseLLMProvider):
    """
    Groq LLM Provider implementation using high-speed Groq inference
    with json_object response format.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_GROQ_MODEL):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        if not self.api_key:
            logger.warning("GROQ_API_KEY not detected. Groq calls will fall back to FallbackMockProvider unless key is supplied.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key, timeout=30.0)

    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> Dict[str, Any]:
        if not self.client:
            logger.info("No active Groq client. Using Mock Provider for zero-config demonstration.")
            return FallbackMockProvider().generate_json(system_prompt, user_prompt, temperature)

        try:
            logger.info(f"Calling Groq API with model={self.model} ...")
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=4096,
            )

            raw_content = chat_completion.choices[0].message.content
            if not raw_content:
                raise ValueError("Groq returned empty response content.")

            # Parse JSON
            data = json.loads(raw_content)
            return data

        except groq.RateLimitError as rle:
            logger.error(f"Groq Rate Limit Exceeded: {rle}")
            raise RuntimeError(f"Groq API rate limit hit. Please retry in a few moments or adjust your tier: {rle}")
        except groq.APITimeoutError as toe:
            logger.error(f"Groq Request Timed Out: {toe}")
            raise RuntimeError("Groq API request timed out after 30 seconds.")
        except groq.APIConnectionError as ace:
            logger.error(f"Groq Connection Error: {ace}")
            raise RuntimeError(f"Unable to connect to Groq API: {ace}")
        except json.JSONDecodeError as jde:
            logger.error(f"Failed to parse LLM response as JSON: {jde}")
            # Try to clean backticks or parse substring
            try:
                cleaned = raw_content.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                return json.loads(cleaned.strip())
            except Exception:
                raise RuntimeError(f"LLM returned malformed JSON: {raw_content[:200]}...")
        except Exception as e:
            logger.error(f"Unexpected error calling Groq: {e}")
            raise RuntimeError(f"LLM generation failed: {str(e)}")


class FallbackMockProvider(BaseLLMProvider):
    """
    High-craft deterministic fallback provider.
    Used when GROQ_API_KEY is omitted or for unit testing and offline demo mode.
    Guarantees strict math consistency and high-taste creative output.
    """

    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> Dict[str, Any]:
        logger.info("Serving rich high-craft mock generation.")
        # Detect which prompt is being called
        if "experiential event designer" in system_prompt or "theme_title" in system_prompt:
            return {
                "theme_title": "Kinetic Solarium: Warm Brutalism & Botanical Echoes",
                "tagline": "Architectural raw linen, sculpted shadow-play, and unhurried acoustic transitions.",
                "creative_narrative": (
                    "Conceived as an antidote to cookie-cutter celebrations, this design juxtaposes "
                    "honed volcanic stone, brushed raw brass, and deep terracotta with cascading wild olive "
                    "branches and seeded eucalyptus. Guests move through intentional sensory zones: arriving into "
                    "an intimate, low-lit foyer resonant with ambient live Spanish guitar, before the architectural "
                    "doors part into a luminous atrium illuminated by low-slung paper lanterns and 2200K amber pillar candles. "
                    "Rather than scheduled interruptions, the evening unfolds as an uninterrupted rhythmic banquet."
                ),
                "color_palette": [
                    {"name": "Obsidian Slate", "hex_code": "#1A1D24", "usage_role": "Architectural Foundation"},
                    {"name": "Weathered Terracotta", "hex_code": "#C85A32", "usage_role": "Vessel & Ceramic Accent"},
                    {"name": "Raw Belgian Flax", "hex_code": "#D8CAB8", "usage_role": "Textile Ground"},
                    {"name": "Aged Olive Leaf", "hex_code": "#556048", "usage_role": "Botanical Accent"},
                    {"name": "Amber Glow", "hex_code": "#E69C24", "usage_role": "Candlelight Luster"}
                ],
                "sensory_atmosphere": {
                    "lighting_design": "2200K warm-amber pillar clusters, wireless recessed pin-spots on tables, and grazing shadows along textured plaster backdrops.",
                    "acoustic_profile": "Live acoustic fingerstyle transitions into a curated warm vinyl listening lounge (Bossa nova, neo-soul, ambient jazz) capped at 78dB during dining.",
                    "tactile_textures": "Heavyweight stonewashed flax napkins, unglazed ceramic dinnerware, matte powder-coated cutlery, and rough-sawn oak banquet tables.",
                    "scent_and_botanicals": "Potted dwarf citrus trees, crushed rosemary sprigs tucked into menu sleeves, and fresh cut olive foliage; zero synthetic fragrance."
                },
                "signature_moments": [
                    {
                        "moment_name": "The Golden Hour Toast & Apertif Transition",
                        "timing": "19:15 - Dusk Arrival",
                        "description": "Bespoke smoked botanical spritzes served in fluted crystal coupes alongside an acoustic trumpet chime calling guests to dinner.",
                        "wow_factor_detail": "Synchronized transition where ambient daylight dims and table chandeliers illuminate simultaneously."
                    },
                    {
                        "moment_name": "The Communal Midnight Hearth",
                        "timing": "22:45 - Nightcap Gathering",
                        "description": "An open firepit lounge offering hand-poured single origin sipping chocolates and artisan digestifs on slate trays.",
                        "wow_factor_detail": "Custom brass monogram stamps branded onto keepsake linen sachets on departure."
                    },
                    {
                        "moment_name": "Kinetic Audio Unveil",
                        "timing": "21:30 - Party Kickoff",
                        "description": "The acoustic ensemble smoothly hands off the master frequency to a live vinyl selector behind an oak credenza.",
                        "wow_factor_detail": "Zero generic DJ lighting rigs; purely illuminated by warm architectural uplights and warm Edison globes."
                    }
                ],
                "interactive_activities": [
                    {
                        "activity_name": "Artisanal Botanical Fragrance Bar",
                        "audience_fit": "Sophisticated, tactile engagement suitable for all ages without feeling childish.",
                        "description": "An apothecary station where guests blend small vials of pure cold-pressed cypress, bergamot, and cedar oils as custom favors.",
                        "setup_requirement": "6ft wood harvest table, 2 dedicated botanical attendants, amber glass droppers."
                    },
                    {
                        "activity_name": "Analog Typewriter Guestbook Chronicles",
                        "audience_fit": "Intimate storytelling that evokes nostalgia and spontaneous candor.",
                        "description": "Two restored 1960s Olivetti typewriters on vintage desks with heavy handmade cotton rag paper cards for guest letters.",
                        "setup_requirement": "Quiet corner nook with task lamp and leather bound folio."
                    },
                    {
                        "activity_name": "Bespoke Vinyl Listening & Request Library",
                        "audience_fit": "Music lovers, multi-generational conversation starter.",
                        "description": "Guests browse curated vintage crate sleeves to queue favorite deep cuts for the evening DJ set.",
                        "setup_requirement": "Custom oak record bins and wireless headphones for previewing."
                    }
                ]
            }

        elif "financial controller" in system_prompt or "total_budget" in system_prompt:
            # Generate mathematically valid breakdown
            total = 35000.0
            # Try to read budget from user_prompt
            try:
                import re
                match = re.search(r"Total Budget:\s*([\d\.,]+)", user_prompt)
                if match:
                    total = float(match.group(1).replace(",", ""))
            except Exception:
                pass

            contingency = round(total * 0.10, 2)
            allocated = round(total - contingency, 2)

            return {
                "total_budget": total,
                "allocated_subtotal": allocated,
                "contingency_reserve": contingency,
                "cost_per_guest": round(total / 100, 2),
                "currency": "USD",
                "items": [
                    {
                        "category": "Venue & Site Fee",
                        "item_name": "Exclusive Private Estate & Grounds Hire (12 hrs)",
                        "estimated_cost": round(allocated * 0.28, 2),
                        "percentage_of_budget": 25.2,
                        "priority": "Essential",
                        "pro_negotiation_tip": "Negotiate complimentary load-in hours the morning prior to avoid 1.5x weekend overtime delivery fees."
                    },
                    {
                        "category": "Catering & Bar",
                        "item_name": "Farm-to-Table Plated Dining & Artisan Wine Service",
                        "estimated_cost": round(allocated * 0.34, 2),
                        "percentage_of_budget": 30.6,
                        "priority": "Essential",
                        "pro_negotiation_tip": "Supply your own curated vintage wine and negotiate a flat corkage fee cap instead of per-bottle markup."
                    },
                    {
                        "category": "Production & AV",
                        "item_name": "Architectural Ambient Lighting (2200K) & Wireless Audio",
                        "estimated_cost": round(allocated * 0.10, 2),
                        "percentage_of_budget": 9.0,
                        "priority": "High-Impact",
                        "pro_negotiation_tip": "Bundle sound reinforcement with ambient lighting under one production vendor to eliminate duplicate travel and crew fees."
                    },
                    {
                        "category": "Florals & Atmosphere",
                        "item_name": "Seasonal Local Botanicals, Olive Branch Clusters & Pillar Candles",
                        "estimated_cost": round(allocated * 0.11, 2),
                        "percentage_of_budget": 9.9,
                        "priority": "High-Impact",
                        "pro_negotiation_tip": "Repurpose ceremony focal foliage arrangements to flank the head table and lounge seating post-reception."
                    },
                    {
                        "category": "Photography & Film",
                        "item_name": "Documentary Film & Digital Photo Duo (8 Hours)",
                        "estimated_cost": round(allocated * 0.10, 2),
                        "percentage_of_budget": 9.0,
                        "priority": "Essential",
                        "pro_negotiation_tip": "Request delivery of curated raw selects and high-res gallery with full printing rights instead of expensive physical albums."
                    },
                    {
                        "category": "Entertainment",
                        "item_name": "Acoustic Cocktail Trio & Curated Evening Vinyl DJ",
                        "estimated_cost": round(allocated * 0.05, 2),
                        "percentage_of_budget": 4.5,
                        "priority": "High-Impact",
                        "pro_negotiation_tip": "Book an artist who handles both acoustic performance for the opening and DJ sequencing for the finale."
                    },
                    {
                        "category": "Coordination & Permits",
                        "item_name": "Lead Producer & Month-Of Day-Of Coordination Team",
                        "estimated_cost": round(allocated * 0.02, 2),
                        "percentage_of_budget": 1.8,
                        "priority": "Essential",
                        "pro_negotiation_tip": "Lock in early contract booking with fixed flat rate rather than percentage-of-total-spend fee."
                    },
                    {
                        "category": "Contingency Buffer",
                        "item_name": "Unforeseen Weather, Transit & City Sound Permits",
                        "estimated_cost": contingency,
                        "percentage_of_budget": 10.0,
                        "priority": "Essential",
                        "pro_negotiation_tip": "Keep this unallocated in a high-yield account until 14 days before the event."
                    }
                ],
                "financial_health_summary": "A balanced, realistic capital allocation prioritizing high-touch hospitality and ambiance while guarding a vital 10% emergency reserve.",
                "top_cost_saving_levers": [
                    "Limit hard liquor bar to 2 signature botanic cocktails + natural wines to slash bar staffing and spill waste by 22%.",
                    "Choose in-season branch foliage over imported out-of-season blooms to save up to 40% on florals with richer architectural presence.",
                    "Leverage off-peak Sunday or Friday scheduling to negotiate up to 15% venue fee reductions."
                ]
            }

        elif "operational director" in system_prompt or "day_of_run_of_show" in system_prompt:
            return {
                "planning_milestones": [
                    {
                        "phase": "Phase 1: Foundation & High-Leverage Anchors",
                        "timeframe": "6 - 12 Months Out",
                        "action_items": [
                            "Finalize guest capacity ceiling and establish firm budget cap.",
                            "Execute signed venue contract with verified sound ordinance and strike curfew hours.",
                            "Secure high-demand documentary photographer and catering partner."
                        ],
                        "critical_deadline": "Day 45: Venue non-refundable deposit lock",
                        "responsible_party": "Client & Lead Producer"
                    },
                    {
                        "phase": "Phase 2: Aesthetic Architecture & Core Vendors",
                        "timeframe": "3 - 6 Months Out",
                        "action_items": [
                            "Conduct menu tasting and finalize dietary variance protocols.",
                            "Lock architectural lighting design and electrical load schematic.",
                            "Draft invitations and launch private guest portal."
                        ],
                        "critical_deadline": "90 Days Out: Final florist and sound engineer contracts",
                        "responsible_party": "Lead Producer"
                    },
                    {
                        "phase": "Phase 3: Logistics, Seating & Run-of-Show Lock",
                        "timeframe": "4 - 8 Weeks Out",
                        "action_items": [
                            "Collect RSVPs and lock final guest dietary matrix.",
                            "Finalize load-in schedule with all delivery dock time slots.",
                            "Issue vendor Certificates of Insurance (COI) to venue administration."
                        ],
                        "critical_deadline": "3 Weeks Out: Catering guarantee count",
                        "responsible_party": "Lead Producer & Venue Manager"
                    },
                    {
                        "phase": "Phase 4: Execution Week & Dress Run",
                        "timeframe": "72 Hours - Event Day",
                        "action_items": [
                            "Conduct technical audio sound check and wireless mic frequency scan.",
                            "Review emergency contingency protocols and distribute coordinator master contact sheet.",
                            "Distribute vendor tip envelopes and vendor load-out schedule."
                        ],
                        "critical_deadline": "24 Hours Out: Weather go/no-go decision for outdoor zones",
                        "responsible_party": "Lead Coordinator"
                    }
                ],
                "day_of_run_of_show": [
                    {
                        "time_window": "08:00 - 10:30",
                        "segment_title": "Site Handover & Heavy Structural Load-In",
                        "description": "Catering kitchen setup, staging, tables, power distribution runs and AV sound checks.",
                        "coordinator_in_charge": "Production Logistics Lead",
                        "buffer_minutes": 30
                    },
                    {
                        "time_window": "10:30 - 13:00",
                        "segment_title": "Atmosphere, Florals & Tabletop Dressing",
                        "description": "Floral installs, tabletop linens, candle positioning, and printed stationery placement.",
                        "coordinator_in_charge": "Design & Styling Lead",
                        "buffer_minutes": 20
                    },
                    {
                        "time_window": "13:00 - 14:30",
                        "segment_title": "Audio Line Checks & Vendor Walkthrough",
                        "description": "Mic checks, lighting dimmer testing, walk-through with venue manager, final trash sweep.",
                        "coordinator_in_charge": "Lead Producer & Sound Tech",
                        "buffer_minutes": 15
                    },
                    {
                        "time_window": "15:00 - 16:00",
                        "segment_title": "Guest Welcome & Ambient Aperitivo",
                        "description": "Live acoustic guitar begins, welcoming spritzers served, coats checked, ambient glow set to 2400K.",
                        "coordinator_in_charge": "Hospitality & Door Lead",
                        "buffer_minutes": 10
                    },
                    {
                        "time_window": "16:15 - 17:30",
                        "segment_title": "Main Ceremony / Keynote Milestone",
                        "description": "Central event proceedings, scheduled moments, audio recording capture.",
                        "coordinator_in_charge": "Lead Producer",
                        "buffer_minutes": 15
                    },
                    {
                        "time_window": "17:30 - 19:00",
                        "segment_title": "Sunset Cocktail Hour & Transition",
                        "description": "Tray-passed savory bites, acoustic trio expands tempo, dining room reveal preparations.",
                        "coordinator_in_charge": "Catering Captain",
                        "buffer_minutes": 15
                    },
                    {
                        "time_window": "19:00 - 21:15",
                        "segment_title": "Seated Dinner & Curated Toasts",
                        "description": "Multi-course service paced with 2 intentional toast intervals; background volume strictly managed.",
                        "coordinator_in_charge": "Lead Producer & Head Chef",
                        "buffer_minutes": 20
                    },
                    {
                        "time_window": "21:15 - 23:30",
                        "segment_title": "Late Night Music, Vinyl Selector & Dessert",
                        "description": "Dessert station unveil, vinyl DJ tempo shift, dancing, open cocktail service.",
                        "coordinator_in_charge": "Stage Manager",
                        "buffer_minutes": 10
                    },
                    {
                        "time_window": "23:30 - 01:00",
                        "segment_title": "Guest Farewell & Systematic Strike",
                        "description": "Private shuttles, tear-down, rental inventory count, venue inspection and lock-up.",
                        "coordinator_in_charge": "Production Logistics Lead",
                        "buffer_minutes": 30
                    }
                ],
                "buffer_strategy": "15 to 30 minute strategic dampers placed immediately following the ceremony and during dinner toasts to absorb organic speech extensions without derailing catering courses.",
                "critical_path_warning": "Load-in dock access congestion between 09:00-10:00. Stagger florist and AV trucks by minimum 45 minutes to prevent gridlock."
            }

        else:
            # Vendor Guide
            return {
                "vendor_categories": [
                    {
                        "vendor_type": "Venue & Site Administration",
                        "recommended_budget_allocation": "20% - 28% of total budget",
                        "sourcing_checklist": [
                            "Strict curfew hour for outdoor amplified sound (dB limit)",
                            "Total amperage capacity and number of dedicated 20A circuits",
                            "Mandatory vendor exclusivity list vs outside vendor buyout fees"
                        ],
                        "hard_hitting_interview_questions": [
                            "What is your exact hourly rate if our strike crew exceeds the midnight departure by 25 minutes?",
                            "Can you point to your backup generator protocol if a local transformer trips during dinner?",
                            "Are there hidden kitchen prep fees, trash hauling charges, or ice machine access fees not listed on the rate card?"
                        ],
                        "contract_red_flags": [
                            "Unilateral cancellation clauses where venue can cancel for owner private events.",
                            "Mandatory 22% venue administrative fee that does NOT go to service staff.",
                            "Overly restrictive noise clauses that permit the venue to cut master power without warning."
                        ],
                        "key_deliverables_to_lock": [
                            "Guaranteed site access minimum 4 hours prior to guest arrival.",
                            "Designated secure storage room for alcohol and valuables overnight."
                        ]
                    },
                    {
                        "vendor_type": "Catering & Hospitality Services",
                        "recommended_budget_allocation": "30% - 38% of total budget",
                        "sourcing_checklist": [
                            "Staffing ratio: minimum 1 server per 10-12 guests for plated dinner",
                            "Tasting policy and ingredient provenance standards",
                            "Full liability insurance and active liquor license"
                        ],
                        "hard_hitting_interview_questions": [
                            "How do you handle dietary substitutions on the fly when 4 guests didn't notify us beforehand?",
                            "Is your quote inclusive of chef labor, breakdown cleanup, and linen steam press, or is that billed in arrears?",
                            "What percentage of food prep happens on-site versus reheated from a commissary kitchen?"
                        ],
                        "contract_red_flags": [
                            "Vague 'market price' escalation clauses that allow menu price increases after contract signing.",
                            "Non-transparent beverage pour fee where you are billed for open bottles rather than consumed volume."
                        ],
                        "key_deliverables_to_lock": [
                            "Final menu spec sheet with allergy-safe certifications signed 14 days prior.",
                            "Trained banquet captain dedicated solely to timing coordination with producer."
                        ]
                    },
                    {
                        "vendor_type": "Photography & Cinematography",
                        "recommended_budget_allocation": "9% - 12% of total budget",
                        "sourcing_checklist": [
                            "Dual-slot memory card cameras for real-time redundant backup",
                            "Proven documentary / editorial style in low-light environments",
                            "Comprehensive online gallery with full print release rights"
                        ],
                        "hard_hitting_interview_questions": [
                            "What is your exact backup hardware protocol if your primary body or lens fails during the key ceremony moment?",
                            "Who specifically is shooting my event—you or an associate shooter from your agency?",
                            "How do you archive raw files, and for how many years do you guarantee raw file preservation?"
                        ],
                        "contract_red_flags": [
                            "Delivery turnaround times exceeding 16 weeks without liquidated damages.",
                            "Clauses granting the photographer unlimited commercial advertising rights without client preview."
                        ],
                        "key_deliverables_to_lock": [
                            "Sneak-peek highlight gallery of 30-40 color-graded frames within 72 hours.",
                            "Full high-res digital gallery delivered within 6 weeks."
                        ]
                    },
                    {
                        "vendor_type": "Live Audio, DJ & Ambiance Engineering",
                        "recommended_budget_allocation": "5% - 8% of total budget",
                        "sourcing_checklist": [
                            "Clean cable runs and wireless audio transmitters (no messy trip hazards)",
                            "Ability to curate customized vinyl/digital setlists without corny line dances",
                            "Backup mixing console and backup laptop on standby"
                        ],
                        "hard_hitting_interview_questions": [
                            "How do you manage room acoustics and reverberation in high-ceiling or glass-heavy spaces?",
                            "What is your exact protocol if our master timeline runs 35 minutes behind schedule?",
                            "Do you bring dedicated backup wireless microphones on separate RF bands?"
                        ],
                        "contract_red_flags": [
                            "Aggressive overtime billing calculated in full-hour increments for 10-minute overages.",
                            "Vendor-dictated setlists that prohibit client 'do not play' veto lists."
                        ],
                        "key_deliverables_to_lock": [
                            "Comprehensive song curation & veto list confirmation 14 days out.",
                            "Full wireless lapel mic and handheld setup for all speakers."
                        ]
                    }
                ],
                "contract_golden_rules": [
                    "Never pay more than a 25-33% deposit at initial signing; distribute milestones across completion dates.",
                    "Require all vendors to provide an active Certificate of Insurance (COI) listing venue and client as additional insureds.",
                    "Ensure force majeure clauses explicitly include weather emergencies, pandemics, and civil unrest with full credit transfer."
                ],
                "liability_and_permit_advice": "Confirm whether the municipality requires an off-duty police officer for guest counts exceeding 100 with open liquor service. Submit sound permit applications minimum 60 days before the event."
            }


def get_llm_provider(provider_name: str = "groq") -> BaseLLMProvider:
    """
    Factory function to instantiate the selected LLM provider.
    Easily extensible for OpenAI, Anthropic, or Gemini.
    """
    provider_name = provider_name.lower()
    if provider_name == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.info("GROQ_API_KEY is not set in environment. Defaulting to FallbackMockProvider.")
            return FallbackMockProvider()
        return GroqProvider(api_key=api_key)
    elif provider_name == "mock":
        return FallbackMockProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
