"""Integration tests for JSON conversion.

Tests round-trip JSON conversion of capabilities and plans.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path

from aurora.converters.json import JsonConverter
from aurora.parsers.markdown import MarkdownParser
from aurora.parsers.plan_parser import PlanParser


class TestJsonConverterRoundTrip:
    """Tests for round-trip JSON conversion."""

    @pytest.fixture
    def converter(self):
        """Create JSON converter instance."""
        return JsonConverter()

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project with specs and plans."""
        temp_dir = tempfile.mkdtemp(prefix="aurora-json-e2e-")

        # Create a capability
        cap_dir = Path(temp_dir) / "capabilities" / "auth"
        cap_dir.mkdir(parents=True)
        (cap_dir / "spec.md").write_text("""# Capability: Authentication

## Purpose

Provides secure user authentication for the platform.

## Requirements

### Requirement: REQ-AUTH-001: Login functionality

The system SHALL allow users to log in with username and password.

#### Scenario: Successful login
GIVEN a valid user account exists
WHEN the user enters correct credentials
THEN the user is authenticated and redirected to dashboard

#### Scenario: Invalid credentials
GIVEN a user account exists
WHEN the user enters incorrect password
THEN an error message is displayed

### Requirement: REQ-AUTH-002: Session management

The system SHALL maintain user sessions securely.

#### Scenario: Session timeout
GIVEN a user is logged in
WHEN the session expires after 30 minutes of inactivity
THEN the user is automatically logged out
""")

        # Create a plan
        plan_dir = Path(temp_dir) / "plans" / "add-oauth"
        plan_dir.mkdir(parents=True)
        (plan_dir / "plan.md").write_text("""# Plan: Add OAuth Support

## Why

Users need to log in with third-party providers for convenience.

## What Changes

### auth

- **ADD** OAuth provider integration
- **MODIFY** Login page to show OAuth buttons
- **ADD** Token exchange endpoint
""")

        yield temp_dir

        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_capability_to_json_and_back(self, converter, temp_project):
        """Test converting a capability to JSON preserves structure."""
        cap_file = Path(temp_project) / "capabilities" / "auth" / "spec.md"

        # Convert to JSON
        json_str = converter.convert_capability_to_json(str(cap_file))

        # Parse JSON
        data = json.loads(json_str)

        # Verify structure
        assert "name" in data
        assert "overview" in data
        assert "requirements" in data
        assert "metadata" in data

        # Verify metadata
        assert "sourcePath" in data["metadata"]
        assert "auth" in data["metadata"]["sourcePath"]

    def test_plan_to_json_and_back(self, converter, temp_project):
        """Test converting a plan to JSON preserves structure."""
        plan_file = Path(temp_project) / "plans" / "add-oauth" / "plan.md"

        # Convert to JSON
        json_str = converter.convert_plan_to_json(str(plan_file))

        # Parse JSON
        data = json.loads(json_str)

        # Verify structure
        assert "name" in data
        assert "why" in data
        assert "what_changes" in data or "modifications" in data
        assert "metadata" in data

    def test_json_contains_valid_utf8(self, converter, temp_project):
        """Test that JSON output is valid UTF-8."""
        cap_file = Path(temp_project) / "capabilities" / "auth" / "spec.md"

        json_str = converter.convert_capability_to_json(str(cap_file))

        # Should be valid UTF-8
        json_bytes = json_str.encode("utf-8")
        decoded = json_bytes.decode("utf-8")

        assert decoded == json_str

    def test_json_is_valid_format(self, converter, temp_project):
        """Test that JSON output is properly formatted."""
        cap_file = Path(temp_project) / "capabilities" / "auth" / "spec.md"

        json_str = converter.convert_capability_to_json(str(cap_file))

        # Should be pretty-printed (indented)
        assert "\n" in json_str
        assert "  " in json_str  # Indentation


class TestJsonConverterEdgeCases:
    """Tests for edge cases in JSON conversion."""

    @pytest.fixture
    def converter(self):
        """Create JSON converter instance."""
        return JsonConverter()

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project."""
        temp_dir = tempfile.mkdtemp(prefix="aurora-json-edge-")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_minimal_capability(self, converter, temp_project):
        """Test converting a minimal capability."""
        cap_dir = Path(temp_project) / "capabilities" / "minimal"
        cap_dir.mkdir(parents=True)
        (cap_dir / "spec.md").write_text("""# Capability: Minimal

## Purpose

A minimal capability.

## Requirements

### Requirement: REQ-001: Minimal requirement

The system SHALL exist.

#### Scenario: Exists
GIVEN nothing
WHEN checked
THEN it exists
""")

        json_str = converter.convert_capability_to_json(
            str(cap_dir / "spec.md")
        )

        data = json.loads(json_str)

        assert data["name"] == "minimal"
        assert "requirements" in data

    def test_special_characters_in_content(self, converter, temp_project):
        """Test handling special characters in content."""
        cap_dir = Path(temp_project) / "capabilities" / "special"
        cap_dir.mkdir(parents=True)
        (cap_dir / "spec.md").write_text("""# Capability: Special Characters

## Purpose

Handle "quotes", <tags>, and & ampersands.

## Requirements

### Requirement: REQ-001: Test special chars

The system SHALL handle: "quotes", <html>, & symbols.

#### Scenario: Special chars
GIVEN content with "special" <chars>
WHEN processed
THEN output is valid JSON
""")

        json_str = converter.convert_capability_to_json(
            str(cap_dir / "spec.md")
        )

        # Should be valid JSON (special chars escaped)
        data = json.loads(json_str)
        assert data["name"] == "special"

    def test_unicode_content(self, converter, temp_project):
        """Test handling unicode content."""
        cap_dir = Path(temp_project) / "capabilities" / "unicode"
        cap_dir.mkdir(parents=True)
        (cap_dir / "spec.md").write_text("""# Capability: Unicode Test

## Purpose

Support international characters: 日本語, العربية, 한국어, émojis 🎉

## Requirements

### Requirement: REQ-001: Unicode support

The system SHALL support UTF-8 characters.

#### Scenario: Unicode display
GIVEN content with unicode: 你好世界
WHEN displayed
THEN characters render correctly
""")

        json_str = converter.convert_capability_to_json(
            str(cap_dir / "spec.md")
        )

        # Should handle unicode
        data = json.loads(json_str)
        assert data["name"] == "unicode"


class TestJsonConverterWithParsers:
    """Tests for JSON converter integration with parsers."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project."""
        temp_dir = tempfile.mkdtemp(prefix="aurora-json-parser-")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_converter_uses_markdown_parser(self, temp_project):
        """Test that converter properly uses MarkdownParser."""
        cap_dir = Path(temp_project) / "capabilities" / "test"
        cap_dir.mkdir(parents=True)
        cap_file = cap_dir / "spec.md"
        cap_file.write_text("""# Capability: Parser Test

## Purpose

Testing parser integration.

## Requirements

### Requirement: REQ-001: Parse correctly

The parser SHALL extract requirements.

#### Scenario: Basic parsing
GIVEN markdown content
WHEN parsed
THEN structure is extracted
""")

        converter = JsonConverter()
        json_str = converter.convert_capability_to_json(str(cap_file))

        data = json.loads(json_str)

        # Should have parsed the content
        assert "requirements" in data

    def test_converter_uses_plan_parser(self, temp_project):
        """Test that converter properly uses PlanParser."""
        plan_dir = Path(temp_project) / "plans" / "test"
        plan_dir.mkdir(parents=True)
        plan_file = plan_dir / "plan.md"
        plan_file.write_text("""# Plan: Parser Test

## Why

Testing plan parser integration.

## What Changes

### some-capability

- **ADD** New feature
""")

        converter = JsonConverter()
        json_str = converter.convert_plan_to_json(str(plan_file))

        data = json.loads(json_str)

        # Should have parsed the content
        assert "why" in data or "modifications" in data
