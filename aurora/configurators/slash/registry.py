"""Registry for slash command configurators.

Manages registration and retrieval of tool-specific configurators.
"""


from aurora.configurators.slash.base import SlashCommandConfigurator


class SlashCommandRegistry:
    """Central registry for slash command configurators.

    Provides a singleton-like interface for managing tool configurators.
    """

    _configurators: dict[str, SlashCommandConfigurator] = {}

    @classmethod
    def register(cls, configurator: SlashCommandConfigurator) -> None:
        """Register a slash command configurator.

        Args:
            configurator: Configurator instance to register

        Note:
            Tool IDs are normalized (lowercase, spaces to dashes).
        """
        tool_id = cls._normalize_tool_id(configurator.tool_id)
        cls._configurators[tool_id] = configurator

    @classmethod
    def get(cls, tool_id: str) -> SlashCommandConfigurator | None:
        """Get a configurator by tool ID.

        Args:
            tool_id: Tool identifier

        Returns:
            Configurator instance or None if not found
        """
        normalized_id = cls._normalize_tool_id(tool_id)
        return cls._configurators.get(normalized_id)

    @classmethod
    def get_all(cls) -> list[SlashCommandConfigurator]:
        """Get all registered configurators.

        Returns:
            List of all configurator instances
        """
        return list(cls._configurators.values())

    @classmethod
    def get_available(cls) -> list[SlashCommandConfigurator]:
        """Get only available configurators.

        Returns:
            List of configurators where is_available is True
        """
        return [c for c in cls._configurators.values() if c.is_available]

    @classmethod
    def clear(cls) -> None:
        """Clear all registered configurators.

        Used primarily for testing.
        """
        cls._configurators.clear()

    @staticmethod
    def _normalize_tool_id(tool_id: str) -> str:
        """Normalize a tool ID.

        Args:
            tool_id: Tool identifier to normalize

        Returns:
            Normalized tool ID (lowercase, spaces to dashes)
        """
        return tool_id.lower().replace(" ", "-")
