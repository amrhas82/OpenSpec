"""OpenCode slash command configurator.

Configures slash commands for OpenCode in .opencode/command/ directory.
OpenCode uses a different file structure with $ARGUMENTS placeholders.
"""

from typing import Dict, Optional

from aurora.configurators.slash.base import SlashCommandConfigurator
from aurora.templates.slash_commands import get_command_body


# File paths for each command
FILE_PATHS: Dict[str, str] = {
    "plan": ".opencode/command/aurora-plan.md",
    "archive": ".opencode/command/aurora-archive.md",
    "implement": ".opencode/command/aurora-implement.md",
    "query": ".opencode/command/aurora-query.md",
    "mem": ".opencode/command/aurora-mem.md",
    "index": ".opencode/command/aurora-index.md",
    "search": ".opencode/command/aurora-search.md",
}

# Frontmatter for each command (OpenCode format with $ARGUMENTS)
FRONTMATTER: Dict[str, str] = {
    "plan": """---
description: Generate structured plans with agent delegation.
---
The user has requested a new plan. Use the aurora instructions below to create their plan.
<UserRequest>
  $ARGUMENTS
</UserRequest>
""",
    "archive": """---
description: Archive completed plans with timestamp.
---
<PlanId>
  $ARGUMENTS
</PlanId>
""",
    "implement": """---
description: Execute plans by delegating to agents.
---
The user has requested to implement a plan. Find the plan and follow the instructions below.
<UserRequest>
  $ARGUMENTS
</UserRequest>
""",
    "query": """---
description: Search codebase using memory system.
---
<Query>
  $ARGUMENTS
</Query>
""",
    "mem": """---
description: Memory operations (index, search, status).
---
<Command>
  $ARGUMENTS
</Command>
""",
    "index": """---
description: Index codebase for semantic search.
---
<Path>
  $ARGUMENTS
</Path>
""",
    "search": """---
description: Search indexed code.
---
<Query>
  $ARGUMENTS
</Query>
""",
}


class OpenCodeSlashCommandConfigurator(SlashCommandConfigurator):
    """Slash command configurator for OpenCode.

    Creates slash commands in .opencode/command/ directory for
    all Aurora commands. Uses OpenCode's $ARGUMENTS placeholder format.
    """

    @property
    def tool_id(self) -> str:
        """Tool identifier."""
        return "opencode"

    @property
    def is_available(self) -> bool:
        """OpenCode is always available (doesn't require detection)."""
        return True

    def get_relative_path(self, command_id: str) -> str:
        """Get relative path for a slash command file.

        Args:
            command_id: Command identifier

        Returns:
            Relative path from project root
        """
        return FILE_PATHS[command_id]

    def get_frontmatter(self, command_id: str) -> Optional[str]:
        """Get frontmatter for a slash command file.

        OpenCode uses $ARGUMENTS placeholder for command arguments.

        Args:
            command_id: Command identifier

        Returns:
            Frontmatter string with $ARGUMENTS placeholder
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
