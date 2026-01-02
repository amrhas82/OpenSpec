"""Tests for CapabilityCommand CLI wrapper."""

import pytest
from pathlib import Path
from aurora.cli.capability_cmd import CapabilityCommand


@pytest.fixture
def capability_command() -> CapabilityCommand:
    """Create a CapabilityCommand instance."""
    return CapabilityCommand()


@pytest.fixture
def temp_project(tmp_path: Path) -> Path:
    """Create a temporary project structure."""
    aurora_dir = tmp_path / "aurora"
    caps_dir = aurora_dir / "capabilities"
    caps_dir.mkdir(parents=True)
    return tmp_path


class TestCapabilityCommandShow:
    """Tests for showing capabilities."""

    def test_show_capability_text_mode(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test showing a capability in text mode."""
        cap_dir = temp_project / "aurora" / "capabilities" / "test-cap"
        cap_dir.mkdir(parents=True)
        cap_file = cap_dir / "spec.md"
        cap_file.write_text("# Capability: Test\n\n## Purpose\n\nThis capability provides test functionality.\n\n## Requirements\n\n### Requirement: REQ-001: Test\n\nThe system SHALL support tests.\n\n#### Scenario: Test\nGIVEN state\nWHEN action\nTHEN result")

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            result = capability_command.show("test-cap", json_output=False)
            assert "Test" in result
        finally:
            os.chdir(original_cwd)

    def test_show_capability_json_mode(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test showing a capability in JSON mode."""
        cap_dir = temp_project / "aurora" / "capabilities" / "test-cap"
        cap_dir.mkdir(parents=True)
        cap_file = cap_dir / "spec.md"
        cap_file.write_text("# Capability: Test\n\n## Purpose\n\nThis capability provides test functionality.\n\n## Requirements\n\n### Requirement: REQ-001: Test\n\nThe system SHALL support tests.\n\n#### Scenario: Test\nGIVEN state\nWHEN action\nTHEN result")

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            result = capability_command.show("test-cap", json_output=True)
            import json
            data = json.loads(result)
            assert "id" in data
            assert "title" in data
        finally:
            os.chdir(original_cwd)


class TestCapabilityCommandList:
    """Tests for listing capabilities."""

    def test_list_capabilities_text_mode(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test listing capabilities in text mode."""
        caps_dir = temp_project / "aurora" / "capabilities"
        for name in ["cap-a", "cap-b"]:
            cap_dir = caps_dir / name
            cap_dir.mkdir(parents=True)
            cap_file = cap_dir / "spec.md"
            cap_file.write_text(f"# Capability: {name}\n\n## Purpose\n\nTest purpose.\n\n## Requirements\n\n### Requirement: REQ-001: Test\n\nThe system SHALL support testing.")

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            result = capability_command.list(json_output=False)
            assert "cap-a" in result
            assert "cap-b" in result
        finally:
            os.chdir(original_cwd)

    def test_list_empty_capabilities(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test listing when no capabilities exist."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            result = capability_command.list(json_output=False)
            assert "no capabilities found" in result.lower()
        finally:
            os.chdir(original_cwd)


class TestCapabilityCommandValidate:
    """Tests for validating capabilities."""

    def test_validate_valid_capability(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test validating a valid capability."""
        cap_dir = temp_project / "aurora" / "capabilities" / "test-cap"
        cap_dir.mkdir(parents=True)
        cap_file = cap_dir / "spec.md"
        cap_file.write_text("""# Capability: Test

## Purpose

This capability provides test functionality.

## Requirements

### Requirement: REQ-001: Test requirement

The system SHALL support test functionality.

#### Scenario: Basic scenario
GIVEN initial state
WHEN action occurs
THEN result happens
""")

        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            result = capability_command.validate("test-cap", strict=False, json_output=False)
            assert "valid" in result.lower()
        finally:
            os.chdir(original_cwd)

    def test_validate_capability_not_found(self, temp_project: Path, capability_command: CapabilityCommand):
        """Test validation of non-existent capability."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_project)
            with pytest.raises(Exception) as exc_info:
                capability_command.validate("nonexistent", strict=False, json_output=False)
            assert "not found" in str(exc_info.value).lower()
        finally:
            os.chdir(original_cwd)
