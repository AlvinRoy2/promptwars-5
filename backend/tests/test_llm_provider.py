"""
Unit tests for LLM Provider abstractions:
- FallbackMockProvider returns correct structured data for each prompt type
- GroqProvider error handling for RateLimitError, TimeoutError, malformed JSON
"""

import json
from unittest.mock import MagicMock, patch

import pytest

# Ensure backend is importable (conftest.py handles sys.path)
from backend.llm_provider import FallbackMockProvider, GroqProvider


# ──────────────────────────────────────────────────────────────────────────────
# FallbackMockProvider Tests
# ──────────────────────────────────────────────────────────────────────────────

class TestFallbackMockProvider:
    """Test the deterministic FallbackMockProvider used in offline/demo mode."""

    def setup_method(self):
        self.provider = FallbackMockProvider()

    def test_ideas_response_has_required_keys(self):
        """Verify ideas response contains all required schema keys."""
        result = self.provider.generate_json(
            system_prompt="You are an experiential event designer with theme_title focus.",
            user_prompt="Event: Wedding\nTotal Budget: 48000\nGuests: 120",
        )
        assert "theme_title" in result
        assert "tagline" in result
        assert "creative_narrative" in result
        assert "color_palette" in result
        assert "sensory_atmosphere" in result
        assert "signature_moments" in result
        assert "interactive_activities" in result

    def test_ideas_color_palette_has_hex_codes(self):
        """Verify color palette entries have hex_code and name fields."""
        result = self.provider.generate_json(
            system_prompt="theme_title structured output",
            user_prompt="Any prompt",
        )
        palette = result.get("color_palette", [])
        assert len(palette) >= 3
        for swatch in palette:
            assert "hex_code" in swatch
            assert swatch["hex_code"].startswith("#"), f"Invalid hex: {swatch['hex_code']}"
            assert "name" in swatch

    def test_ideas_signature_moments_minimum_count(self):
        """Verify at least 3 signature moments are returned."""
        result = self.provider.generate_json(
            system_prompt="theme_title and signature_moments",
            user_prompt="Event: Gala",
        )
        moments = result.get("signature_moments", [])
        assert len(moments) >= 3, f"Expected >=3 signature moments, got {len(moments)}"

    def test_budget_response_math_integrity(self):
        """Verify fallback budget response enforces allocated + contingency == total."""
        result = self.provider.generate_json(
            system_prompt="financial controller total_budget",
            user_prompt="Event: Milestone Birthday\nTotal Budget: 40000\nGuests: 80",
        )
        assert "total_budget" in result
        assert "allocated_subtotal" in result
        assert "contingency_reserve" in result

        total = result["total_budget"]
        allocated = result["allocated_subtotal"]
        contingency = result["contingency_reserve"]

        # Within floating point tolerance
        assert abs((allocated + contingency) - total) < 0.05, (
            f"Budget math broken: {allocated} + {contingency} != {total}"
        )

    def test_budget_response_parses_budget_from_prompt(self):
        """Verify the fallback provider extracts total budget from the user prompt."""
        result = self.provider.generate_json(
            system_prompt="financial controller total_budget",
            user_prompt="Total Budget: 60,000",
        )
        assert result["total_budget"] == 60000.0

    def test_fallback_returns_dict_not_string(self):
        """Verify the provider always returns a parsed dict, never a raw string."""
        for prompt_type in [
            "theme_title and experiential event designer",
            "financial controller total_budget",
            "planning_milestones day_of_run_of_show",
            "vendor_categories contract_golden_rules",
        ]:
            result = self.provider.generate_json(
                system_prompt=prompt_type,
                user_prompt="Generic event",
            )
            assert isinstance(result, dict), f"Expected dict for prompt: {prompt_type}"


# ──────────────────────────────────────────────────────────────────────────────
# GroqProvider Error Handling Tests (no real API calls)
# ──────────────────────────────────────────────────────────────────────────────

class TestGroqProviderErrorHandling:
    """Test GroqProvider graceful error handling with mocked Groq client."""

    def test_no_api_key_delegates_to_fallback(self):
        """Verify GroqProvider with no key falls back to FallbackMockProvider."""
        provider = GroqProvider(api_key=None)
        result = provider.generate_json(
            system_prompt="theme_title experiential event designer",
            user_prompt="Event: Test",
        )
        # FallbackMockProvider response should contain theme_title
        assert "theme_title" in result

    @patch("backend.llm_provider.Groq")
    def test_rate_limit_error_raises_runtime_error(self, mock_groq_cls):
        """Verify RateLimitError is converted to RuntimeError with informative message."""
        import groq as groq_module

        mock_client = MagicMock()
        mock_groq_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = groq_module.RateLimitError(
            message="rate limit", response=MagicMock(status_code=429), body={}
        )

        provider = GroqProvider(api_key="dummy-key-for-test")
        with pytest.raises(RuntimeError, match="rate limit"):
            provider.generate_json(
                system_prompt="theme_title",
                user_prompt="Event: Test",
            )

    @patch("backend.llm_provider.Groq")
    def test_malformed_json_is_cleaned_and_parsed(self, mock_groq_cls):
        """Verify that markdown-fenced JSON responses are cleaned and parsed correctly."""
        mock_client = MagicMock()
        mock_groq_cls.return_value = mock_client

        # Simulate LLM returning markdown-fenced JSON
        fenced_response = '```json\n{"theme_title": "Test Title", "tagline": "Test tagline"}\n```'
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=fenced_response))
        ]

        provider = GroqProvider(api_key="dummy-key-for-test")
        result = provider.generate_json(
            system_prompt="theme_title",
            user_prompt="Event: Test",
        )
        assert result["theme_title"] == "Test Title"

    @patch("backend.llm_provider.Groq")
    def test_empty_response_raises_runtime_error(self, mock_groq_cls):
        """Verify that an empty LLM response content raises a RuntimeError."""
        mock_client = MagicMock()
        mock_groq_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content=None))
        ]

        provider = GroqProvider(api_key="dummy-key-for-test")
        with pytest.raises(RuntimeError):
            provider.generate_json(
                system_prompt="theme_title",
                user_prompt="Event: Test",
            )

