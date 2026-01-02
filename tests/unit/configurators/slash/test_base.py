"""Tests for slash command base configurator protocol."""

import pytest
from pathlib import Path
from typing import Optional
from aurora.configurators.slash.base import SlashCommandConfigurator, SlashCommandTarget


class TestSlashCommandConfigurator:
    """Tests for SlashCommandConfigurator abstract base."""

    @pytest.fixture
    def mock_configurator(self, tmp_path):
        """Create a mock configurator for testing."""
        class MockConfigurator(SlashCommandConfigurator):
            tool_id = "test-tool"
            is_available = True

            def get_relative_path(self, command_id: str) -> str:
                return f".test/commands/aur/{command_id}.md"

            def get_frontmatter(self, command_id: str) -> Optional[str]:
                return f"---\nname: Test {command_id}\ndescription: Test command\n---"

            def get_body(self, command_id: str) -> str:
                return f"# {command_id} command body"

        return MockConfigurator()

    def test_get_targets_returns_all_commands(self, mock_configurator):
        """Test that get_targets returns all configured commands."""
        targets = mock_configurator.get_targets()

        assert isinstance(targets, list)
        assert len(targets) > 0

        # Check structure
        for target in targets:
            assert isinstance(target, SlashCommandTarget)
            assert target.command_id in ["plan", "archive", "implement", "query", "mem", "index", "search"]
            assert target.path.endswith(".md")
            assert target.kind == "slash"

    def test_generate_all_creates_new_files(self, mock_configurator, tmp_path):
        """Test that generate_all creates slash command files."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        created = mock_configurator.generate_all(str(tmp_path), str(aurora_dir))

        assert len(created) > 0

        # Verify files were created
        for path in created:
            file_path = tmp_path / path
            assert file_path.exists()
            content = file_path.read_text()

            # Check for frontmatter
            assert "---" in content
            assert "name:" in content

            # Check for markers
            assert "<!-- AURORA:START -->" in content
            assert "<!-- AURORA:END -->" in content

    def test_generate_all_updates_existing_files(self, mock_configurator, tmp_path):
        """Test that generate_all updates existing files with markers."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        # Create existing file with markers
        test_dir = tmp_path / ".test" / "commands" / "aur"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "plan.md"
        test_file.write_text("""---
name: Old Plan
description: Old description
---

<!-- AURORA:START -->
old body content
<!-- AURORA:END -->
""")

        created = mock_configurator.generate_all(str(tmp_path), str(aurora_dir))

        # Verify file was updated
        content = test_file.read_text()
        assert "# plan command body" in content
        assert "old body content" not in content
        assert "---" in content  # Frontmatter preserved

    def test_update_existing_only_updates_existing_files(self, mock_configurator, tmp_path):
        """Test that update_existing doesn't create new files."""
        aurora_dir = tmp_path / "aurora"
        aurora_dir.mkdir()

        # Create one existing file
        test_dir = tmp_path / ".test" / "commands" / "aur"
        test_dir.mkdir(parents=True)
        test_file = test_dir / "archive.md"
        test_file.write_text("""---
name: Old Archive
---

<!-- AURORA:START -->
old content
<!-- AURORA:END -->
""")

        updated = mock_configurator.update_existing(str(tmp_path), str(aurora_dir))

        # Only one file should be updated (not created)
        assert len(updated) == 1
        assert ".test/commands/aur/archive.md" in updated[0]

        # Verify content was updated
        content = test_file.read_text()
        assert "# archive command body" in content

    def test_resolve_absolute_path(self, mock_configurator, tmp_path):
        """Test that resolve_absolute_path returns correct absolute path."""
        absolute_path = mock_configurator.resolve_absolute_path(str(tmp_path), "plan")

        expected = tmp_path / ".test" / "commands" / "aur" / "plan.md"
        assert Path(absolute_path) == expected

    def test_update_body_raises_error_if_markers_missing(self, mock_configurator, tmp_path):
        """Test that update_body raises error if markers are missing."""
        test_file = tmp_path / "test.md"
        test_file.write_text("File without markers")

        with pytest.raises(ValueError, match="Missing Aurora markers"):
            mock_configurator._update_body(str(test_file), "new body")
