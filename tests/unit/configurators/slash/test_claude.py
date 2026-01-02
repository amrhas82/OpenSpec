"""Tests for Claude Code slash command configurator."""

import pytest
from pathlib import Path
from aurora.configurators.slash.claude import ClaudeSlashCommandConfigurator


class TestClaudeSlashCommandConfigurator:
    """Tests for Claude Code configurator."""

    @pytest.fixture
    def configurator(self):
        """Create Claude configurator instance."""
        return ClaudeSlashCommandConfigurator()

    def test_tool_id_is_claude(self, configurator):
        """Test tool ID is 'claude'."""
        assert configurator.tool_id == "claude"

    def test_is_available_is_true(self, configurator):
        """Test configurator is marked as available."""
        assert configurator.is_available is True

    def test_get_relative_path_returns_claude_commands_path(self, configurator):
        """Test relative paths are in .claude/commands/aur/ directory."""
        path = configurator.get_relative_path("plan")
        assert path == ".claude/commands/aur/plan.md"

        path = configurator.get_relative_path("archive")
        assert path == ".claude/commands/aur/archive.md"

    def test_get_frontmatter_includes_command_metadata(self, configurator):
        """Test frontmatter includes name, description, category, tags."""
        frontmatter = configurator.get_frontmatter("plan")

        assert "---" in frontmatter
        assert "name: Aurora: Plan" in frontmatter
        assert "description:" in frontmatter
        assert "category: Aurora" in frontmatter
        assert "tags: [aurora, planning]" in frontmatter

    def test_get_body_returns_template_content(self, configurator):
        """Test get_body returns template from templates module."""
        body = configurator.get_body("plan")

        assert "**Guardrails**" in body
        assert "**Steps**" in body
        assert "aur plan" in body

    def test_generate_all_creates_claude_command_files(self, configurator, tmp_path):
        """Test generate_all creates files in .claude/commands/aur/ directory."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        created = configurator.generate_all(str(tmp_path), str(aurora_dir))

        # Should create 7 command files
        assert len(created) == 7

        # Verify plan command file
        plan_file = tmp_path / ".claude" / "commands" / "aur" / "plan.md"
        assert plan_file.exists()

        content = plan_file.read_text()
        assert "name: Aurora: Plan" in content
        assert "<!-- AURORA:START -->" in content
        assert "<!-- AURORA:END -->" in content
        assert "**Guardrails**" in content

    def test_update_existing_updates_only_existing_files(self, configurator, tmp_path):
        """Test update_existing only updates existing command files."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        # Create one existing file
        commands_dir = tmp_path / ".claude" / "commands" / "aur"
        commands_dir.mkdir(parents=True)
        archive_file = commands_dir / "archive.md"
        archive_file.write_text("""---
name: Aurora: Archive
---

<!-- AURORA:START -->
old content
<!-- AURORA:END -->
""")

        updated = configurator.update_existing(str(tmp_path), str(aurora_dir))

        # Only archive should be updated
        assert len(updated) == 1
        assert ".claude/commands/aur/archive.md" in updated[0]

        # Verify content was updated
        content = archive_file.read_text()
        assert "**Guardrails**" in content
        assert "old content" not in content

    def test_all_command_ids_have_paths_and_frontmatter(self, configurator):
        """Test all 7 command IDs have paths and frontmatter."""
        command_ids = ["plan", "archive", "implement", "query", "mem", "index", "search"]

        for cmd_id in command_ids:
            # Should not raise
            path = configurator.get_relative_path(cmd_id)
            assert path.startswith(".claude/commands/aur/")
            assert path.endswith(f"{cmd_id}.md")

            frontmatter = configurator.get_frontmatter(cmd_id)
            assert "---" in frontmatter
            assert "name: Aurora:" in frontmatter

            body = configurator.get_body(cmd_id)
            assert len(body) > 0
