"""Discovery utilities for finding plans and capabilities.

Provides functions to discover plans and capabilities in the project.
"""

from pathlib import Path
from typing import List


def get_active_plan_ids(base_path: Path = None) -> List[str]:
    """Get list of active plan IDs.

    Args:
        base_path: Base path to search (defaults to cwd/aurora/plans)

    Returns:
        List of plan IDs (directory names)
    """
    if base_path is None:
        base_path = Path.cwd() / "aurora" / "plans"

    if not base_path.exists():
        return []

    plans = []
    for entry in base_path.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "archive":
            continue

        # Check if it has a plan.md file
        plan_file = entry / "plan.md"
        if plan_file.exists():
            plans.append(entry.name)

    return sorted(plans)


def get_capability_ids(base_path: Path = None) -> List[str]:
    """Get list of capability IDs.

    Args:
        base_path: Base path to search (defaults to cwd/aurora/capabilities)

    Returns:
        List of capability IDs (directory names)
    """
    if base_path is None:
        base_path = Path.cwd() / "aurora" / "capabilities"

    if not base_path.exists():
        return []

    capabilities = []
    for entry in base_path.iterdir():
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue

        # Check if it has a spec.md file
        spec_file = entry / "spec.md"
        if spec_file.exists():
            capabilities.append(entry.name)

    return sorted(capabilities)
