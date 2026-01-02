"""Base protocol for tool configurators.

Defines the interface that all tool configurators must implement.
"""

from typing import Protocol


class ToolConfigurator(Protocol):
    """Protocol for tool configurators.

    Tool configurators detect and configure integration with various AI coding tools.
    """

    name: str
    """Human-readable name of the tool."""

    config_file_name: str
    """Configuration file name for this tool."""

    is_available: bool
    """Whether this tool is available in the current environment."""

    def configure(self, project_path: str, aurora_dir: str) -> None:
        """Configure the tool for the given project.

        Args:
            project_path: Root path of the project
            aurora_dir: Path to the aurora directory (e.g., aurora/)

        Raises:
            Exception: If configuration fails
        """
        ...
