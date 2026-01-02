"""Tests for slash command registry."""

import pytest
from typing import Optional
from aurora.configurators.slash.registry import SlashCommandRegistry
from aurora.configurators.slash.base import SlashCommandConfigurator


class TestSlashCommandRegistry:
    """Tests for SlashCommandRegistry."""

    @pytest.fixture
    def mock_configurator_available(self):
        """Create a mock available configurator."""
        class AvailableConfigurator(SlashCommandConfigurator):
            tool_id = "test-available"
            is_available = True

            def get_relative_path(self, command_id: str) -> str:
                return f".test/commands/{command_id}.md"

            def get_frontmatter(self, command_id: str) -> Optional[str]:
                return "---\nname: Test\n---"

            def get_body(self, command_id: str) -> str:
                return "body"

        return AvailableConfigurator()

    @pytest.fixture
    def mock_configurator_unavailable(self):
        """Create a mock unavailable configurator."""
        class UnavailableConfigurator(SlashCommandConfigurator):
            tool_id = "test-unavailable"
            is_available = False

            def get_relative_path(self, command_id: str) -> str:
                return f".test/commands/{command_id}.md"

            def get_frontmatter(self, command_id: str) -> Optional[str]:
                return None

            def get_body(self, command_id: str) -> str:
                return "body"

        return UnavailableConfigurator()

    @pytest.fixture(autouse=True)
    def clear_registry(self):
        """Clear registry before each test."""
        SlashCommandRegistry.clear()
        yield
        SlashCommandRegistry.clear()

    def test_register_configurator(self, mock_configurator_available):
        """Test registering a configurator."""
        SlashCommandRegistry.register(mock_configurator_available)

        result = SlashCommandRegistry.get("test-available")
        assert result is not None
        assert result.tool_id == "test-available"

    def test_register_multiple_configurators(
        self, mock_configurator_available, mock_configurator_unavailable
    ):
        """Test registering multiple configurators."""
        SlashCommandRegistry.register(mock_configurator_available)
        SlashCommandRegistry.register(mock_configurator_unavailable)

        assert SlashCommandRegistry.get("test-available") is not None
        assert SlashCommandRegistry.get("test-unavailable") is not None

    def test_get_nonexistent_configurator_returns_none(self):
        """Test getting a configurator that doesn't exist."""
        result = SlashCommandRegistry.get("nonexistent")
        assert result is None

    def test_get_all_returns_all_configurators(
        self, mock_configurator_available, mock_configurator_unavailable
    ):
        """Test get_all returns all registered configurators."""
        SlashCommandRegistry.register(mock_configurator_available)
        SlashCommandRegistry.register(mock_configurator_unavailable)

        all_configurators = SlashCommandRegistry.get_all()
        assert len(all_configurators) == 2
        assert mock_configurator_available in all_configurators
        assert mock_configurator_unavailable in all_configurators

    def test_get_available_filters_unavailable_configurators(
        self, mock_configurator_available, mock_configurator_unavailable
    ):
        """Test get_available only returns available configurators."""
        SlashCommandRegistry.register(mock_configurator_available)
        SlashCommandRegistry.register(mock_configurator_unavailable)

        available = SlashCommandRegistry.get_available()
        assert len(available) == 1
        assert available[0].tool_id == "test-available"

    def test_clear_removes_all_configurators(self, mock_configurator_available):
        """Test clear removes all configurators."""
        SlashCommandRegistry.register(mock_configurator_available)
        assert SlashCommandRegistry.get("test-available") is not None

        SlashCommandRegistry.clear()
        assert SlashCommandRegistry.get("test-available") is None

    def test_tool_id_normalization_with_spaces(self, mock_configurator_available):
        """Test tool IDs with spaces are normalized."""
        # Override tool_id with spaces
        mock_configurator_available.tool_id = "Test Available Tool"
        SlashCommandRegistry.register(mock_configurator_available)

        # Should be accessible with normalized ID
        result = SlashCommandRegistry.get("test-available-tool")
        assert result is not None

    def test_get_all_returns_empty_list_when_no_configurators(self):
        """Test get_all returns empty list when registry is empty."""
        all_configurators = SlashCommandRegistry.get_all()
        assert isinstance(all_configurators, list)
        assert len(all_configurators) == 0
