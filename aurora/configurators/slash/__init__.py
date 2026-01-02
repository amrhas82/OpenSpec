"""Slash command configurators for AI coding tools."""

from aurora.configurators.slash.base import (
    SlashCommandConfigurator,
    SlashCommandTarget,
)
from aurora.configurators.slash.registry import SlashCommandRegistry

__all__ = [
    "SlashCommandConfigurator",
    "SlashCommandRegistry",
    "SlashCommandTarget",
]
