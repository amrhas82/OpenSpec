# Aurora Planning System - API Reference

## Table of Contents

1. [Schemas](#schemas)
2. [Validation](#validation)
3. [Parsers](#parsers)
4. [Commands](#commands)
5. [CLI Classes](#cli-classes)
6. [Utilities](#utilities)
7. [Configurators](#configurators)
8. [Converters](#converters)

---

## Schemas

### `aurora.schemas.base`

```python
class Scenario(BaseModel):
    """A test scenario for a requirement."""
    raw_text: str  # Scenario description (non-empty)

class Requirement(BaseModel):
    """A requirement with SHALL/MUST keyword and scenarios."""
    text: str  # Must contain SHALL or MUST
    scenarios: list[Scenario]  # At least one scenario
```

### `aurora.schemas.plan`

```python
class ModificationOperation(str, Enum):
    """Types of modifications to capabilities."""
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"
    RENAMED = "RENAMED"

class RenameInfo(BaseModel):
    """Information for RENAMED operations."""
    from_name: str  # Original requirement name
    to_name: str    # New requirement name

class Modification(BaseModel):
    """A modification to a capability."""
    capability: str           # Target capability name
    operation: ModificationOperation
    description: str          # At least 10 characters
    requirement: Requirement | None = None   # For single-req ops
    requirements: list[Requirement] | None = None  # For multi-req ops
    rename: RenameInfo | None = None  # For RENAMED ops

class Plan(BaseModel):
    """A plan for changes (was Change in OpenSpec)."""
    name: str              # Plan identifier
    why: str               # Rationale (>10 chars)
    what_changes: str      # Summary of changes
    modifications: list[Modification]  # 1-50 modifications
    metadata: PlanMetadata | None = None
```

### `aurora.schemas.capability`

```python
class Capability(BaseModel):
    """A system capability (was Spec in OpenSpec)."""
    name: str                    # Capability identifier
    overview: str                # Purpose section (>10 chars)
    requirements: list[Any]      # Named requirements
    metadata: CapabilityMetadata | None = None
```

---

## Validation

### `aurora.validation.types`

```python
class ValidationLevel(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

class ValidationIssue(BaseModel):
    level: ValidationLevel
    path: str         # File path or location
    message: str      # Human-readable description
    line: int | None = None
    column: int | None = None

class ValidationReport(BaseModel):
    valid: bool
    issues: list[ValidationIssue]
    summary: ValidationSummary  # Computed: errors, warnings, info counts
```

### `aurora.validation.validator`

```python
class Validator:
    """Main validation class for plans and capabilities."""

    def __init__(self, strict_mode: bool = False):
        """
        Args:
            strict_mode: If True, warnings also cause validation failure
        """

    def validate_capability(self, file_path: str) -> ValidationReport:
        """Validate a capability spec file."""

    def validate_plan(self, file_path: str) -> ValidationReport:
        """Validate a plan file."""

    def validate_plan_modification_specs(
        self, plan_dir: str
    ) -> ValidationReport:
        """Validate delta specs in a plan's specs/ directory."""
```

---

## Parsers

### `aurora.parsers.markdown`

```python
@dataclass
class ParsedScenario:
    text: str

@dataclass
class ParsedRequirement:
    name: str
    text: str
    scenarios: list[ParsedScenario]

@dataclass
class ParsedCapability:
    name: str
    overview: str
    requirements: list[ParsedRequirement]
    raw_content: str = ""
    metadata: ParsedCapabilityMetadata | None = None

@dataclass
class ParsedModification:
    capability: str
    operation: ModificationOperation
    description: str
    requirement: ParsedRequirement | None = None
    requirements: list[ParsedRequirement] | None = None
    rename: dict[str, str] | None = None

@dataclass
class ParsedPlan:
    name: str
    why: str
    what_changes: str
    modifications: list[ParsedModification]
    raw_content: str = ""
    metadata: ParsedPlanMetadata | None = None

class MarkdownParser:
    """Parser for Aurora markdown files."""

    def parse_capability(self, content: str) -> ParsedCapability:
        """Parse a capability spec from markdown content."""

    def parse_plan(self, content: str) -> ParsedPlan:
        """Parse a plan from markdown content."""

    def extract_sections(self, content: str) -> dict[str, str]:
        """Extract top-level sections from markdown."""
```

### `aurora.parsers.plan_parser`

```python
class PlanParser:
    """Specialized parser for plan files."""

    def parse(self, content: str) -> ParsedPlan:
        """Parse a complete plan from markdown content."""
```

### `aurora.parsers.requirements`

```python
@dataclass
class RequirementBlock:
    header_line: str  # e.g., '### Requirement: Something'
    name: str         # e.g., 'Something'
    raw: str          # Full block content

@dataclass
class ModificationPlan:
    added: list[RequirementBlock]
    modified: list[RequirementBlock]
    removed: list[str]  # Requirement names
    renamed: list[dict[str, str]]  # {from: str, to: str}
    section_presence: dict[str, bool]

def parse_modification_spec(content: str) -> ModificationPlan:
    """Parse a delta/modification spec from markdown content."""

def normalize_requirement_name(name: str) -> str:
    """Normalize requirement name for comparison (lowercase, trimmed)."""

def extract_requirements_section(content: str) -> str | None:
    """Extract the ## Requirements section from spec content."""
```

---

## Commands

### `aurora.commands.archive`

```python
class ArchiveCommand:
    """Archive a completed plan and apply changes to capabilities."""

    def execute(
        self,
        project_path: str = ".",
        change_name: str | None = None,
        yes: bool = False,
        skip_validation: bool = False
    ) -> None:
        """
        Execute the archive command.

        Args:
            project_path: Project root directory
            change_name: Plan to archive (prompts if not specified)
            yes: Skip confirmation prompts
            skip_validation: Skip validation (dangerous)
        """
```

### `aurora.commands.init`

```python
class InitCommand:
    """Initialize Aurora planning structure in a project."""

    def execute(
        self,
        project_path: str = ".",
        verbose: bool = False
    ) -> None:
        """
        Execute the init command.

        Creates: aurora/{plans,capabilities}, AGENTS.md
        """
```

### `aurora.commands.list`

```python
class ListCommand:
    """List plans or capabilities."""

    def execute(
        self,
        target_path: str = ".",
        mode: Literal['changes', 'specs'] = 'changes',
        options: dict | None = None
    ) -> None:
        """
        Execute the list command.

        Options:
            sort: 'recent' or 'name' (default: 'recent')
            json: True for JSON output
        """
```

### `aurora.commands.update`

```python
class UpdateCommand:
    """Update AGENTS.md with latest template."""

    def execute(
        self,
        project_path: str = ".",
        verbose: bool = False
    ) -> None:
        """Execute the update command."""
```

### `aurora.commands.view`

```python
class ViewCommand:
    """View project planning dashboard."""

    def execute(
        self,
        project_path: str = ".",
        json_output: bool = False
    ) -> None:
        """Execute the view command."""
```

---

## CLI Classes

### `aurora.cli.plan_cmd`

```python
class PlanCommand:
    """CLI wrapper for plan operations."""

    def show(
        self,
        plan_name: str | None = None,
        json_output: bool = False,
        modifications_only: bool = False
    ) -> str:
        """Show a plan's details."""

    def list(
        self,
        json_output: bool = False,
        long: bool = False
    ) -> str:
        """List all plans."""

    def validate(
        self,
        plan_name: str | None = None,
        strict: bool = False,
        json_output: bool = False
    ) -> str:
        """Validate a plan."""
```

### `aurora.cli.capability_cmd`

```python
class CapabilityCommand:
    """CLI wrapper for capability operations."""

    def show(
        self,
        capability_id: str | None = None,
        json_output: bool = False
    ) -> str:
        """Show a capability's details."""

    def list(
        self,
        json_output: bool = False
    ) -> str:
        """List all capabilities."""

    def validate(
        self,
        capability_id: str,
        strict: bool = False,
        json_output: bool = False
    ) -> str:
        """Validate a capability."""
```

### `aurora.cli.validate_cmd`

```python
class ValidateCommand:
    """CLI wrapper for validation operations."""

    def validate_plan(
        self,
        plan_name: str,
        strict: bool = False,
        json_output: bool = False
    ) -> str:
        """Validate a plan."""

    def validate_capability(
        self,
        capability_id: str,
        strict: bool = False,
        json_output: bool = False
    ) -> str:
        """Validate a capability."""
```

---

## Utilities

### `aurora.utils.discovery`

```python
def get_active_plan_ids(base_path: Path | None = None) -> list[str]:
    """Get list of active plan IDs in the project."""

def get_capability_ids(base_path: Path | None = None) -> list[str]:
    """Get list of capability IDs in the project."""
```

### `aurora.utils.filesystem`

```python
def find_project_root(start_path: Path | None = None) -> Path | None:
    """Find Aurora project root by looking for aurora/ directory."""

def read_markdown_file(file_path: Path) -> str:
    """Read a markdown file with proper encoding."""
```

### `aurora.utils.match`

```python
def nearest_matches(
    query: str,
    candidates: list[str],
    limit: int = 3
) -> list[str]:
    """Find nearest matches using Levenshtein distance."""
```

### `aurora.utils.task_progress`

```python
def count_tasks(content: str) -> dict[str, int]:
    """Count tasks in markdown content.

    Returns:
        {'total': int, 'completed': int}
    """

def get_completion_percent(total: int, completed: int) -> int:
    """Calculate completion percentage."""
```

### `aurora.utils.interactive`

```python
def is_interactive() -> bool:
    """Check if running in interactive terminal."""
```

---

## Configurators

### `aurora.configurators.base`

```python
class ToolConfigurator(Protocol):
    """Protocol for tool configurators."""

    def detect(self, project_path: Path) -> bool:
        """Check if tool is present in project."""

    def configure(self, project_path: Path) -> None:
        """Configure tool for Aurora."""
```

### `aurora.configurators.registry`

```python
class ToolRegistry:
    """Registry of tool configurators."""

    def register(self, name: str, configurator: ToolConfigurator) -> None:
        """Register a configurator."""

    def detect_tools(self, project_path: Path) -> list[str]:
        """Detect which tools are present."""

    def configure_all(self, project_path: Path) -> None:
        """Configure all detected tools."""
```

### `aurora.configurators.slash.registry`

```python
class SlashCommandRegistry:
    """Registry for slash commands."""

    def register(self, name: str, template: str) -> None:
        """Register a slash command template."""

    def get_commands(self) -> dict[str, str]:
        """Get all registered commands."""
```

### `aurora.configurators.slash.claude`

```python
class ClaudeCodeConfigurator:
    """Configurator for Claude Code slash commands."""

    def configure_slash_commands(self, project_path: str) -> None:
        """Create .claude/commands/aur/*.md files."""
```

---

## Converters

### `aurora.converters.json`

```python
def plan_to_json(plan: ParsedPlan) -> dict:
    """Convert parsed plan to JSON-serializable dict."""

def capability_to_json(capability: ParsedCapability) -> dict:
    """Convert parsed capability to JSON-serializable dict."""

def validation_report_to_json(report: ValidationReport) -> dict:
    """Convert validation report to JSON-serializable dict."""
```

---

## Constants

### `aurora.validation.constants`

```python
# Thresholds
MIN_PURPOSE_LENGTH = 10
MIN_MODIFICATION_DESCRIPTION_LENGTH = 10
MAX_REQUIREMENT_TEXT_LENGTH = 2000
MAX_MODIFICATIONS_PER_PLAN = 50

# Messages
class VALIDATION_MESSAGES:
    REQUIREMENT_EMPTY = "Requirement text cannot be empty"
    REQUIREMENT_NO_SHALL = "Requirement must contain SHALL or MUST"
    REQUIREMENT_NO_SCENARIOS = "Requirement must have at least one scenario"
    PLAN_NAME_EMPTY = "Plan name cannot be empty"
    PLAN_NO_MODIFICATIONS = "Plan must have at least one modification"
    # ... many more messages
```

### `aurora.config`

```python
AURORA_MARKERS = {
    "START": "<!-- AURORA:START -->",
    "END": "<!-- AURORA:END -->"
}

AI_TOOLS = {
    "claude": {"file": "CLAUDE.md"},
    "cline": {"file": ".clinerules"},
    "agents": {"file": "AGENTS.md"},
    "codebuddy": {"file": ".codebuddy/config.json"}
}
```

---

## Templates

### `aurora.templates.agents`

```python
AGENTS_TEMPLATE: str  # Complete AGENTS.md template (~457 lines)
```

### `aurora.templates.project`

```python
PROJECT_TEMPLATE: dict[str, str]  # Project structure template
```

### `aurora.templates.slash_commands.templates`

```python
BASE_GUARDRAILS: str      # Common guardrails for all commands
PLAN_TEMPLATE: str        # /aur:plan template
ARCHIVE_TEMPLATE: str     # /aur:archive template
IMPLEMENT_TEMPLATE: str   # /aur:implement template
QUERY_TEMPLATE: str       # /aur:query template
MEM_TEMPLATE: str         # /aur:mem template
INDEX_TEMPLATE: str       # /aur:index template
SEARCH_TEMPLATE: str      # /aur:search template
```
