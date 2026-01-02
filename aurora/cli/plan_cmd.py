"""CLI wrapper for plan commands.

This module provides the PlanCommand class which wraps core plan functionality
for CLI invocation. It handles:
- Showing plans (text and JSON modes)
- Listing plans (with optional long format)
- Validating plans (with strict mode)
"""

import builtins
import json
from pathlib import Path

from aurora.parsers.plan_parser import PlanParser
from aurora.validation.validator import Validator


class PlanCommand:
    """CLI wrapper for plan operations."""

    # Constants
    ARCHIVE_DIR = "archive"
    TASK_PATTERN = r"^[-*]\s+\[[\sx]\]"
    COMPLETED_TASK_PATTERN = r"^[-*]\s+\[x\]"

    def __init__(self) -> None:
        """Initialize PlanCommand."""
        pass

    def show(
        self,
        plan_name: str | None = None,
        json_output: bool = False,
        modifications_only: bool = False,
    ) -> str:
        """Show a plan.

        Args:
            plan_name: Name of the plan to show
            json_output: Whether to output JSON
            modifications_only: Whether to show only modifications

        Returns:
            String output (text or JSON)

        Raises:
            Exception: If plan not found
        """
        plans_path = Path.cwd() / "aurora" / "plans"

        if not plan_name:
            raise ValueError("Plan name is required")

        plan_dir = plans_path / plan_name
        plan_file = plan_dir / "plan.md"

        if not plan_file.exists():
            raise Exception(f'Plan "{plan_name}" not found at {plan_file}')

        if json_output:
            # Parse the plan and return JSON
            content = plan_file.read_text()
            parser = PlanParser(content, str(plan_dir))
            plan = parser.parse_plan_with_modifications(plan_name)

            title = self._extract_title(content, plan_name)
            modifications = plan.modifications or []

            output = {
                "id": plan_name,
                "title": title,
                "modificationCount": len(modifications),
                "modifications": [
                    {
                        "operation": mod.operation,
                        "capability": mod.capability,
                        "description": mod.description,
                    }
                    for mod in modifications
                ],
            }

            if modifications_only:
                output = {
                    "id": plan_name,
                    "title": title,
                    "modificationCount": len(modifications),
                    "modifications": output["modifications"],
                }

            return json.dumps(output, indent=2)
        else:
            # Return raw markdown
            content = plan_file.read_text()
            return content

    def list(self, json_output: bool = False, long: bool = False) -> str:
        """List active plans.

        Args:
            json_output: Whether to output JSON
            long: Whether to show detailed information

        Returns:
            String output (text or JSON)
        """
        plans_path = Path.cwd() / "aurora" / "plans"

        plans = self._get_active_plans(plans_path)

        if json_output:
            # Build JSON output with details
            plan_details = []
            for plan_name in plans:
                plan_file = plans_path / plan_name / "plan.md"
                tasks_file = plans_path / plan_name / "tasks.md"

                try:
                    content = plan_file.read_text()
                    plan_dir = plans_path / plan_name
                    parser = PlanParser(content, str(plan_dir))
                    plan = parser.parse_plan_with_modifications(plan_name)

                    task_status = {"total": 0, "completed": 0}
                    if tasks_file.exists():
                        tasks_content = tasks_file.read_text()
                        task_status = self._count_tasks(tasks_content)

                    plan_details.append(
                        {
                            "id": plan_name,
                            "title": self._extract_title(content, plan_name),
                            "modificationCount": len(plan.modifications or []),
                            "taskStatus": task_status,
                        }
                    )
                except Exception:
                    plan_details.append(
                        {
                            "id": plan_name,
                            "title": "Unknown",
                            "modificationCount": 0,
                            "taskStatus": {"total": 0, "completed": 0},
                        }
                    )

            sorted_details = sorted(plan_details, key=lambda x: str(x["id"]))
            return json.dumps(sorted_details, indent=2)
        else:
            if len(plans) == 0:
                return "No items found"

            sorted_plans = sorted(plans)
            if not long:
                # Just IDs
                return "\n".join(sorted_plans)

            # Long format with details
            lines = []
            for plan_name in sorted_plans:
                plan_file = plans_path / plan_name / "plan.md"
                tasks_file = plans_path / plan_name / "tasks.md"

                try:
                    content = plan_file.read_text()
                    title = self._extract_title(content, plan_name)

                    task_status_text = ""
                    if tasks_file.exists():
                        tasks_content = tasks_file.read_text()
                        task_status = self._count_tasks(tasks_content)
                        task_status_text = (
                            f" [tasks {task_status['completed']}/{task_status['total']}]"
                        )

                    plan_dir = plans_path / plan_name
                    parser = PlanParser(content, str(plan_dir))
                    plan = parser.parse_plan_with_modifications(plan_name)
                    mod_count = len(plan.modifications or [])
                    mod_count_text = f" [modifications {mod_count}]"

                    lines.append(f"{plan_name}: {title}{mod_count_text}{task_status_text}")
                except Exception:
                    lines.append(f"{plan_name}: (unable to read)")

            return "\n".join(lines)

    def validate(
        self, plan_name: str | None = None, strict: bool = False, json_output: bool = False
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

        if not plan_name:
            raise ValueError("Plan name is required")

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
                lines = [f'Plan "{plan_name}" has issues']
                for issue in report.issues:
                    label = "ERROR" if issue.level == "ERROR" else "WARNING"
                    prefix = "✗" if issue.level == "ERROR" else "⚠"
                    lines.append(f"{prefix} [{label}] {issue.path}: {issue.message}")

                # Add next steps
                lines.append("\nNext steps:")
                lines.append(
                    "  - Ensure plan has modifications in capabilities/: use headers ## ADDED/MODIFIED/REMOVED/RENAMED Requirements"
                )
                lines.append(
                    "  - Each requirement MUST include at least one #### Scenario: block"
                )
                lines.append(
                    f"  - Debug parsed modifications: aurora plan show {plan_name} --json --modifications-only"
                )

                return "\n".join(lines)

    def _get_active_plans(self, plans_path: Path) -> builtins.list[str]:
        """Get list of active plan IDs.

        Args:
            plans_path: Path to plans directory

        Returns:
            List of plan IDs
        """
        if not plans_path.exists():
            return []

        result = []
        for entry in plans_path.iterdir():
            if not entry.is_dir():
                continue
            if entry.name.startswith(".") or entry.name == self.ARCHIVE_DIR:
                continue

            plan_file = entry / "plan.md"
            if plan_file.exists():
                result.append(entry.name)

        return sorted(result)

    def _extract_title(self, content: str, plan_name: str) -> str:
        """Extract title from plan content.

        Args:
            content: Plan markdown content
            plan_name: Fallback plan name

        Returns:
            Extracted title or plan name
        """
        import re

        match = re.search(r"^#\s+(?:Plan:\s+)?(.+)$", content, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else plan_name

    def _count_tasks(self, content: str) -> dict[str, int]:
        """Count tasks in content.

        Args:
            content: Task markdown content

        Returns:
            Dict with 'total' and 'completed' counts
        """
        import re

        lines = content.split("\n")
        total = 0
        completed = 0

        task_pattern = re.compile(self.TASK_PATTERN)
        completed_pattern = re.compile(self.COMPLETED_TASK_PATTERN)

        for line in lines:
            if task_pattern.match(line):
                total += 1
                if completed_pattern.match(line):
                    completed += 1

        return {"total": total, "completed": completed}
