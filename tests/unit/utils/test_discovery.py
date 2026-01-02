"""Tests for discovery utilities."""

import pytest
from pathlib import Path
from aurora.utils.discovery import get_active_plan_ids, get_capability_ids


class TestGetActivePlanIds:
    """Tests for get_active_plan_ids function."""

    def test_returns_empty_list_when_no_plans_directory(self, tmp_path: Path):
        """Test returns empty list when plans directory doesn't exist."""
        result = get_active_plan_ids(tmp_path / "nonexistent")
        assert result == []

    def test_finds_plans_with_plan_md_files(self, tmp_path: Path):
        """Test finds plans that have plan.md files."""
        plans_dir = tmp_path
        plans_dir.mkdir(exist_ok=True)

        # Create plans with plan.md files
        for name in ["plan-a", "plan-b", "plan-c"]:
            plan_dir = plans_dir / name
            plan_dir.mkdir()
            (plan_dir / "plan.md").write_text("# Plan")

        result = get_active_plan_ids(plans_dir)
        assert result == ["plan-a", "plan-b", "plan-c"]

    def test_ignores_directories_without_plan_md(self, tmp_path: Path):
        """Test ignores directories without plan.md files."""
        plans_dir = tmp_path
        plans_dir.mkdir(exist_ok=True)

        # Create directory without plan.md
        invalid_dir = plans_dir / "invalid"
        invalid_dir.mkdir()

        # Create valid plan
        valid_dir = plans_dir / "valid"
        valid_dir.mkdir()
        (valid_dir / "plan.md").write_text("# Plan")

        result = get_active_plan_ids(plans_dir)
        assert result == ["valid"]

    def test_ignores_archive_directory(self, tmp_path: Path):
        """Test ignores archive directory."""
        plans_dir = tmp_path
        plans_dir.mkdir(exist_ok=True)

        # Create archive directory
        archive_dir = plans_dir / "archive"
        archive_dir.mkdir()
        (archive_dir / "plan.md").write_text("# Plan")

        result = get_active_plan_ids(plans_dir)
        assert result == []

    def test_ignores_hidden_directories(self, tmp_path: Path):
        """Test ignores directories starting with dot."""
        plans_dir = tmp_path
        plans_dir.mkdir(exist_ok=True)

        # Create hidden directory
        hidden_dir = plans_dir / ".hidden"
        hidden_dir.mkdir()
        (hidden_dir / "plan.md").write_text("# Plan")

        result = get_active_plan_ids(plans_dir)
        assert result == []


class TestGetCapabilityIds:
    """Tests for get_capability_ids function."""

    def test_returns_empty_list_when_no_capabilities_directory(self, tmp_path: Path):
        """Test returns empty list when capabilities directory doesn't exist."""
        result = get_capability_ids(tmp_path / "nonexistent")
        assert result == []

    def test_finds_capabilities_with_spec_md_files(self, tmp_path: Path):
        """Test finds capabilities that have spec.md files."""
        caps_dir = tmp_path
        caps_dir.mkdir(exist_ok=True)

        # Create capabilities with spec.md files
        for name in ["cap-a", "cap-b"]:
            cap_dir = caps_dir / name
            cap_dir.mkdir()
            (cap_dir / "spec.md").write_text("# Capability")

        result = get_capability_ids(caps_dir)
        assert result == ["cap-a", "cap-b"]

    def test_ignores_directories_without_spec_md(self, tmp_path: Path):
        """Test ignores directories without spec.md files."""
        caps_dir = tmp_path
        caps_dir.mkdir(exist_ok=True)

        # Create directory without spec.md
        invalid_dir = caps_dir / "invalid"
        invalid_dir.mkdir()

        # Create valid capability
        valid_dir = caps_dir / "valid"
        valid_dir.mkdir()
        (valid_dir / "spec.md").write_text("# Capability")

        result = get_capability_ids(caps_dir)
        assert result == ["valid"]

    def test_ignores_hidden_directories(self, tmp_path: Path):
        """Test ignores directories starting with dot."""
        caps_dir = tmp_path
        caps_dir.mkdir(exist_ok=True)

        # Create hidden directory
        hidden_dir = caps_dir / ".hidden"
        hidden_dir.mkdir()
        (hidden_dir / "spec.md").write_text("# Capability")

        result = get_capability_ids(caps_dir)
        assert result == []
