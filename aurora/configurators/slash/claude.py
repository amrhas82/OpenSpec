"""Claude Code slash command configurator.

Configures slash commands for Claude Code in .claude/commands/aur/ directory.
"""


from aurora.configurators.slash.base import SlashCommandConfigurator
from aurora.templates.slash_commands import get_command_body

# File paths for each command
FILE_PATHS: dict[str, str] = {
    "plan": ".claude/commands/aur/plan.md",
    "archive": ".claude/commands/aur/archive.md",
    "implement": ".claude/commands/aur/implement.md",
    "query": ".claude/commands/aur/query.md",
    "mem": ".claude/commands/aur/mem.md",
    "index": ".claude/commands/aur/index.md",
    "search": ".claude/commands/aur/search.md",
}

# Frontmatter for each command
FRONTMATTER: dict[str, str] = {
    "plan": """---
name: Aurora: Plan
description: Generate structured plans with agent delegation
category: Aurora
tags: [aurora, planning]
---""",
    "archive": """---
name: Aurora: Archive
description: Archive completed plans with timestamp
category: Aurora
tags: [aurora, planning]
---""",
    "implement": """---
name: Aurora: Implement
description: Execute plans by delegating to agents
category: Aurora
tags: [aurora, execution]
---""",
    "query": """---
name: Aurora: Query
description: Search codebase using memory system
category: Aurora
tags: [aurora, search, memory]
---""",
    "mem": """---
name: Aurora: Memory
description: Memory operations (index, search, status)
category: Aurora
tags: [aurora, memory]
---""",
    "index": """---
name: Aurora: Index
description: Index codebase for semantic search
category: Aurora
tags: [aurora, memory]
---""",
    "search": """---
name: Aurora: Search
description: Search indexed code
category: Aurora
tags: [aurora, search, memory]
---""",
}


class ClaudeSlashCommandConfigurator(SlashCommandConfigurator):
    """Slash command configurator for Claude Code.

    Creates slash commands in .claude/commands/aur/ directory for
    all Aurora commands.
    """

    @property
    def tool_id(self) -> str:
        """Tool identifier."""
        return "claude"

    @property
    def is_available(self) -> bool:
        """Claude Code is always available (doesn't require detection)."""
        return True

    def get_relative_path(self, command_id: str) -> str:
        """Get relative path for a slash command file.

        Args:
            command_id: Command identifier

        Returns:
            Relative path from project root
        """
        return FILE_PATHS[command_id]

    def get_frontmatter(self, command_id: str) -> str | None:
        """Get frontmatter for a slash command file.

        Args:
            command_id: Command identifier

        Returns:
            YAML frontmatter string
        """
        return FRONTMATTER[command_id]

    def get_body(self, command_id: str) -> str:
        """Get body content for a slash command.

        Args:
            command_id: Command identifier

        Returns:
            Command body content from templates
        """
        return get_command_body(command_id)
