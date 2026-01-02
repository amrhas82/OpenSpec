"""CLI wrapper for standalone validation commands.

This module provides the ValidateCommand class for validating plans and capabilities.
It's a simpler wrapper than the full TypeScript version - focused on single-item validation.
"""

import json
from pathlib import Path

from aurora.validation.validator import Validator


class ValidateCommand:
    """CLI wrapper for validation operations."""

    def __init__(self) -> None:
        """Initialize ValidateCommand."""
        pass

    def validate_plan(
        self, plan_name: str, strict: bool = False, json_output: bool = False
    ) -> str:
        """Validate a plan.

        Args:
            plan_name: Name of plan to validate
            strict: Whether to use strict validation
            json_output: Whether to output JSON

        Returns:
            String output (text or JSON)

        Raises:
            Exception: If plan not found
        """
        plans_path = Path.cwd() / "aurora" / "plans"
        plan_dir = plans_path / plan_name

        if not plan_dir.exists():
            raise Exception(f'Plan "{plan_name}" not found at {plan_dir}')

        validator = Validator(strict_mode=strict)
        report = validator.validate_plan_modification_specs(str(plan_dir))

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
                return f'Plan "{plan_name}" is valid'
            else:
                lines = [f'Plan "{plan_name}" has validation issues:']
                for issue in report.issues:
                    label = "ERROR" if issue.level == "ERROR" else "WARNING"
                    prefix = "✗" if issue.level == "ERROR" else "⚠"
                    lines.append(f"{prefix} [{label}] {issue.path}: {issue.message}")
                return "\n".join(lines)

    def validate_capability(
        self, capability_file: str, strict: bool = False, json_output: bool = False
    ) -> str:
        """Validate a capability file.

        Args:
            capability_file: Path to capability file
            strict: Whether to use strict validation
            json_output: Whether to output JSON

        Returns:
            String output (text or JSON)

        Raises:
            Exception: If capability file not found
        """
        cap_path = Path(capability_file)

        if not cap_path.exists():
            raise Exception(f'Capability file not found: {capability_file}')

        validator = Validator(strict_mode=strict)
        report = validator.validate_capability(str(cap_path))

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
                return f'Capability "{capability_file}" is valid'
            else:
                lines = [f'Capability "{capability_file}" has validation issues:']
                for issue in report.issues:
                    label = "ERROR" if issue.level == "ERROR" else "WARNING"
                    prefix = "✗" if issue.level == "ERROR" else "⚠"
                    lines.append(f"{prefix} [{label}] {issue.path}: {issue.message}")
                return "\n".join(lines)
