"""CLI wrapper for capability (spec) commands.

This module provides the CapabilityCommand class for working with capabilities.
Simplified version focused on core functionality.
"""

import builtins
import json
from pathlib import Path

from aurora.parsers.markdown import MarkdownParser
from aurora.validation.validator import Validator


class CapabilityCommand:
    """CLI wrapper for capability operations."""

    CAPABILITIES_DIR = "aurora/capabilities"

    def __init__(self) -> None:
        """Initialize CapabilityCommand."""
        pass

    def show(
        self, capability_id: str | None = None, json_output: bool = False
    ) -> str:
        """Show a capability.

        Args:
            capability_id: ID of capability to show
            json_output: Whether to output JSON

        Returns:
            String output (text or JSON)

        Raises:
            Exception: If capability not found
        """
        if not capability_id:
            raise ValueError("Capability ID is required")

        cap_dir = Path.cwd() / self.CAPABILITIES_DIR / capability_id
        cap_file = cap_dir / "spec.md"

        if not cap_file.exists():
            raise Exception(
                f'Capability "{capability_id}" not found at {cap_file}'
            )

        if json_output:
            # Parse and return JSON
            content = cap_file.read_text()
            parser = MarkdownParser(content)
            capability = parser.parse_capability(capability_id)

            output = {
                "id": capability_id,
                "title": capability.name,
                "overview": capability.overview or "",
                "requirementCount": len(capability.requirements or []),
                "requirements": [
                    {
                        "text": req.text,
                        "scenarioCount": len(req.scenarios or []),
                        "scenarios": [
                            scenario.raw_text
                            for scenario in (req.scenarios or [])
                        ],
                    }
                    for req in (capability.requirements or [])
                ],
            }
            return json.dumps(output, indent=2)
        else:
            # Return raw markdown
            return cap_file.read_text()

    def list(self, json_output: bool = False) -> str:
        """List capabilities.

        Args:
            json_output: Whether to output JSON

        Returns:
            String output (text or JSON)
        """
        cap_base = Path.cwd() / self.CAPABILITIES_DIR

        capabilities = self._get_capabilities(cap_base)

        if json_output:
            # Build JSON output
            cap_details = []
            for cap_id in capabilities:
                cap_file = cap_base / cap_id / "spec.md"
                try:
                    content = cap_file.read_text()
                    parser = MarkdownParser(content)
                    capability = parser.parse_capability(cap_id)

                    cap_details.append(
                        {
                            "id": cap_id,
                            "title": capability.name,
                            "requirementCount": len(capability.requirements or []),
                        }
                    )
                except Exception:
                    cap_details.append(
                        {
                            "id": cap_id,
                            "title": "Unknown",
                            "requirementCount": 0,
                        }
                    )

            sorted_details = sorted(cap_details, key=lambda x: str(x["id"]))
            return json.dumps(sorted_details, indent=2)
        else:
            if len(capabilities) == 0:
                return "No capabilities found"

            sorted_caps = sorted(capabilities)
            return "\n".join(sorted_caps)

    def validate(
        self, capability_id: str, strict: bool = False, json_output: bool = False
    ) -> str:
        """Validate a capability.

        Args:
            capability_id: ID of capability to validate
            strict: Whether to use strict validation
            json_output: Whether to output JSON

        Returns:
            String output (text or JSON)

        Raises:
            Exception: If capability not found
        """
        cap_dir = Path.cwd() / self.CAPABILITIES_DIR / capability_id
        cap_file = cap_dir / "spec.md"

        if not cap_file.exists():
            raise Exception(
                f'Capability "{capability_id}" not found at {cap_file}'
            )

        validator = Validator(strict_mode=strict)
        report = validator.validate_capability(str(cap_file))

        if json_output:
            return json.dumps(
                {
                    "valid": report.valid,
                    "issues": [
                        {
                            "level": issue.level,
                            "path": issue.path,
                            "message": issue.message,
                        }
                        for issue in report.issues
                    ],
                },
                indent=2,
            )
        else:
            if report.valid:
                return f'Capability "{capability_id}" is valid'
            else:
                lines = [f'Capability "{capability_id}" has issues:']
                for issue in report.issues:
                    label = "ERROR" if issue.level == "ERROR" else "WARNING"
                    prefix = "✗" if issue.level == "ERROR" else "⚠"
                    lines.append(f"{prefix} [{label}] {issue.path}: {issue.message}")
                return "\n".join(lines)

    def _get_capabilities(self, cap_base: Path) -> builtins.list[str]:
        """Get list of capability IDs.

        Args:
            cap_base: Path to capabilities directory

        Returns:
            List of capability IDs
        """
        if not cap_base.exists():
            return []

        result = []
        for entry in cap_base.iterdir():
            if not entry.is_dir():
                continue
            if entry.name.startswith("."):
                continue

            cap_file = entry / "spec.md"
            if cap_file.exists():
                result.append(entry.name)

        return sorted(result)
