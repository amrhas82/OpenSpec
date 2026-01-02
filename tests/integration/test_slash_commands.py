"""Integration tests for slash command system.

Tests end-to-end slash command configuration and file generation.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from aurora.configurators.slash.registry import SlashCommandRegistry
from aurora.configurators.slash.claude import ClaudeSlashCommandConfigurator
from aurora.configurators.slash.opencode import OpenCodeSlashCommandConfigurator


class TestSlashCommandIntegration:
    """End-to-end tests for slash command system."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        temp_dir = tempfile.mkdtemp(prefix="aurora-slash-e2e-")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture(autouse=True)
    def setup_registry(self):
        """Setup and teardown registry for each test."""
        # Clear and register configurators
        SlashCommandRegistry.clear()
        SlashCommandRegistry.register(ClaudeSlashCommandConfigurator())
        SlashCommandRegistry.register(OpenCodeSlashCommandConfigurator())
        yield
        SlashCommandRegistry.clear()

    def test_registry_has_configurators(self):
        """Test that registry has registered configurators."""
        configurators = SlashCommandRegistry.get_all()
        assert len(configurators) >= 2

    def test_registry_get_by_id(self):
        """Test getting configurator by ID."""
        claude = SlashCommandRegistry.get("claude")
        assert claude is not None
        assert claude.tool_id == "claude"

        opencode = SlashCommandRegistry.get("opencode")
        assert opencode is not None

    def test_claude_configurator_properties(self):
        """Test Claude configurator has required properties."""
        configurator = ClaudeSlashCommandConfigurator()

        assert configurator.tool_id == "claude"
        assert configurator.is_available is True
        assert hasattr(configurator, "get_relative_path")
        assert hasattr(configurator, "get_body")

    def test_opencode_configurator_properties(self):
        """Test OpenCode configurator has required properties."""
        configurator = OpenCodeSlashCommandConfigurator()

        assert configurator.tool_id == "opencode"
        assert hasattr(configurator, "get_relative_path")
        assert hasattr(configurator, "get_body")

    def test_claude_get_path_for_commands(self):
        """Test Claude configurator returns paths for commands."""
        configurator = ClaudeSlashCommandConfigurator()

        # Should have paths for aurora commands
        plan_path = configurator.get_relative_path("plan")
        assert "plan" in plan_path
        assert ".claude" in plan_path or "aur" in plan_path

    def test_registry_get_available(self):
        """Test getting only available configurators."""
        available = SlashCommandRegistry.get_available()

        # Claude should be available
        claude_found = any(c.tool_id == "claude" for c in available)
        assert claude_found


class TestSlashCommandErrors:
    """Tests for error handling in slash commands."""

    @pytest.fixture(autouse=True)
    def setup_registry(self):
        """Setup registry for error tests."""
        SlashCommandRegistry.clear()
        SlashCommandRegistry.register(ClaudeSlashCommandConfigurator())
        yield
        SlashCommandRegistry.clear()

    def test_registry_get_unknown_returns_none(self):
        """Test getting an unknown configurator returns None."""
        result = SlashCommandRegistry.get("unknown-tool-xyz")
        assert result is None

    def test_configurator_handles_unknown_command(self):
        """Test configurator handles unknown command gracefully."""
        configurator = ClaudeSlashCommandConfigurator()

        # Should raise KeyError or similar for unknown command
        try:
            configurator.get_relative_path("nonexistent-command")
            assert False, "Should have raised an error"
        except (KeyError, ValueError):
            pass  # Expected


class TestSlashCommandTemplates:
    """Tests for slash command templates."""

    def test_command_body_content(self):
        """Test that command bodies have content."""
        configurator = ClaudeSlashCommandConfigurator()

        # Get body for plan command
        body = configurator.get_body("plan")

        # Should have meaningful content
        assert len(body) > 0
        assert "plan" in body.lower() or "#" in body

    def test_command_frontmatter(self):
        """Test that commands have frontmatter."""
        configurator = ClaudeSlashCommandConfigurator()

        # Get frontmatter for plan command
        frontmatter = configurator.get_frontmatter("plan")

        if frontmatter:
            # Should have YAML format
            assert "---" in frontmatter
            assert "name" in frontmatter.lower() or "description" in frontmatter.lower()


class TestSlashCommandNormalization:
    """Tests for tool ID normalization."""

    @pytest.fixture(autouse=True)
    def setup_registry(self):
        """Setup registry."""
        SlashCommandRegistry.clear()
        SlashCommandRegistry.register(ClaudeSlashCommandConfigurator())
        yield
        SlashCommandRegistry.clear()

    def test_normalize_lowercase(self):
        """Test that tool IDs are normalized to lowercase."""
        # Should find claude regardless of case
        result1 = SlashCommandRegistry.get("claude")
        result2 = SlashCommandRegistry.get("CLAUDE")
        result3 = SlashCommandRegistry.get("Claude")

        assert result1 is not None
        assert result1 == result2 == result3

    def test_normalize_spaces_to_dashes(self):
        """Test that spaces are converted to dashes."""
        # Register a test configurator
        class TestConfigurator(ClaudeSlashCommandConfigurator):
            @property
            def tool_id(self) -> str:
                return "test tool"

        SlashCommandRegistry.register(TestConfigurator())

        # Should find with dashes
        result = SlashCommandRegistry.get("test-tool")
        assert result is not None
