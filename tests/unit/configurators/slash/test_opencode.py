"""Tests for OpenCode slash command configurator."""

import pytest
from pathlib import Path
from aurora.configurators.slash.opencode import OpenCodeSlashCommandConfigurator


class TestOpenCodeSlashCommandConfigurator:
    """Tests for OpenCode configurator."""

    @pytest.fixture
    def configurator(self):
        """Create OpenCode configurator instance."""
        return OpenCodeSlashCommandConfigurator()

    def test_tool_id_is_opencode(self, configurator):
        """Test tool ID is 'opencode'."""
        assert configurator.tool_id == "opencode"

    def test_is_available_is_true(self, configurator):
        """Test configurator is marked as available."""
        assert configurator.is_available is True

    def test_get_relative_path_returns_opencode_commands_path(self, configurator):
        """Test relative paths are in .opencode/command/ directory."""
        path = configurator.get_relative_path("plan")
        assert path == ".opencode/command/aurora-plan.md"

        path = configurator.get_relative_path("archive")
        assert path == ".opencode/command/aurora-archive.md"

    def test_get_frontmatter_includes_arguments_placeholder(self, configurator):
        """Test frontmatter includes $ARGUMENTS placeholder for OpenCode."""
        frontmatter = configurator.get_frontmatter("plan")

        assert "---" in frontmatter
        assert "description:" in frontmatter
        assert "$ARGUMENTS" in frontmatter
        assert "<UserRequest>" in frontmatter

    def test_get_body_returns_template_content(self, configurator):
        """Test get_body returns template from templates module."""
        body = configurator.get_body("plan")

        assert "**Guardrails**" in body
        assert "**Steps**" in body
        assert "aur plan" in body

    def test_generate_all_creates_opencode_command_files(self, configurator, tmp_path):
        """Test generate_all creates files in .opencode/command/ directory."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        created = configurator.generate_all(str(tmp_path), str(aurora_dir))

        # Should create 7 command files
        assert len(created) == 7

        # Verify plan command file
        plan_file = tmp_path / ".opencode" / "command" / "aurora-plan.md"
        assert plan_file.exists()

        content = plan_file.read_text()
        assert "description:" in content
        assert "$ARGUMENTS" in content
        assert "<!-- AURORA:START -->" in content
        assert "<!-- AURORA:END -->" in content
        assert "**Guardrails**" in content

    def test_all_command_ids_have_paths_and_frontmatter(self, configurator):
        """Test all 7 command IDs have paths and frontmatter."""
        command_ids = ["plan", "archive", "implement", "query", "mem", "index", "search"]

        for cmd_id in command_ids:
            # Should not raise
            path = configurator.get_relative_path(cmd_id)
            assert path.startswith(".opencode/command/")
            assert path.endswith(".md")

            frontmatter = configurator.get_frontmatter(cmd_id)
            assert "---" in frontmatter
            assert "description:" in frontmatter

            body = configurator.get_body(cmd_id)
            assert len(body) > 0
