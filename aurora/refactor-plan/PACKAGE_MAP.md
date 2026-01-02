# Aurora Planning Package Map

Complete mapping of what each package does for Phase 1 integration into `aurora_cli.planning`.

---

## Package Overview

```
aurora/                          # Root planning package
├── schemas/                     # Data models (Pydantic)
├── validation/                  # Validation engine
├── parsers/                     # Markdown parsing
├── commands/                    # Core command logic
├── cli/                         # CLI wrapper classes
├── configurators/               # Tool detection
│   └── slash/                   # Slash command system
├── templates/                   # File templates
│   └── slash_commands/          # Slash command templates
├── converters/                  # Format conversion
└── utils/                       # Utilities
```

---

## 1. `aurora/schemas/` - Data Models

**Purpose**: Pydantic models representing core data structures.

| File | Classes | Description |
|------|---------|-------------|
| `base.py` | `Scenario`, `Requirement` | Base requirement with scenarios |
| `plan.py` | `Plan`, `Modification`, `ModificationOperation`, `RenameInfo` | Plan (change proposal) with modifications |
| `capability.py` | `Capability`, `CapabilityMetadata` | System capability (spec) |

**Key Concepts**:
- `Requirement` must contain `SHALL` or `MUST` keyword
- `Scenario` describes test cases for requirements
- `Modification` represents ADDED/MODIFIED/REMOVED/RENAMED operations
- `Plan` bundles modifications to capabilities

**Integration Point**: Used by parsers, validators, and commands.

```python
from aurora.schemas.plan import Plan, Modification, ModificationOperation
from aurora.schemas.capability import Capability
from aurora.schemas.base import Requirement, Scenario
```

---

## 2. `aurora/validation/` - Validation Engine

**Purpose**: Validate plans and capabilities against rules.

| File | Classes/Functions | Description |
|------|-------------------|-------------|
| `constants.py` | `VALIDATION_MESSAGES`, thresholds | Error messages, limits |
| `types.py` | `ValidationLevel`, `ValidationIssue`, `ValidationReport` | Validation result types |
| `validator.py` | `Validator` | Main validation class |

**Key Features**:
- Strict mode (warnings = errors)
- Delta spec validation (ADDED/MODIFIED/REMOVED/RENAMED sections)
- Requirement format validation (SHALL/MUST, scenarios)
- Cross-reference validation (renamed requirements)

**Integration Point**: Called by commands before archiving/processing.

```python
from aurora.validation.validator import Validator
from aurora.validation.types import ValidationReport, ValidationLevel

validator = Validator(strict_mode=True)
report = validator.validate_plan('/path/to/plan.md')
report = validator.validate_capability('/path/to/spec.md')
report = validator.validate_plan_modification_specs('/path/to/plan/')
```

---

## 3. `aurora/parsers/` - Markdown Parsing

**Purpose**: Parse markdown files into structured data.

| File | Classes/Functions | Description |
|------|-------------------|-------------|
| `markdown.py` | `MarkdownParser`, `ParsedCapability`, `ParsedPlan`, etc. | General markdown parser |
| `plan_parser.py` | `PlanParser` | Specialized plan parser |
| `requirements.py` | `parse_modification_spec()`, `RequirementBlock`, `ModificationPlan` | Delta spec parsing |

**Key Features**:
- Extract sections from markdown
- Parse requirements with scenarios
- Parse modification specs (ADDED/MODIFIED/REMOVED/RENAMED)
- Handle renamed requirement pairs (FROM/TO)

**Integration Point**: Used by validators and commands.

```python
from aurora.parsers.markdown import MarkdownParser
from aurora.parsers.plan_parser import PlanParser
from aurora.parsers.requirements import parse_modification_spec

parser = MarkdownParser()
cap = parser.parse_capability(content)
plan = parser.parse_plan(content)

mod_plan = parse_modification_spec(delta_content)
```

---

## 4. `aurora/commands/` - Core Command Logic

**Purpose**: Business logic for planning operations.

| File | Class | Description |
|------|-------|-------------|
| `archive.py` | `ArchiveCommand` | Archive completed plans, apply delta specs |
| `init.py` | `InitCommand` | Initialize planning structure |
| `list.py` | `ListCommand` | List plans or capabilities |
| `view.py` | `ViewCommand` | View planning dashboard |
| `update.py` | `UpdateCommand` | Update AGENTS.md template |

**Key Features**:
- `ArchiveCommand`: Most complex - validates, applies deltas, moves to archive
- `InitCommand`: Creates `aurora/{plans,capabilities}`, AGENTS.md
- `ListCommand`: JSON output, sorting, task progress tracking
- `ViewCommand`: Dashboard with categorized plans (draft, active, complete)

**Integration Point**: Called by CLI wrappers.

```python
from aurora.commands.archive import ArchiveCommand
from aurora.commands.init import InitCommand
from aurora.commands.list import ListCommand

cmd = ArchiveCommand()
cmd.execute(project_path='.', change_name='my-plan', yes=True)
```

---

## 5. `aurora/cli/` - CLI Wrapper Classes

**Purpose**: High-level CLI operations with formatting.

| File | Class | Description |
|------|-------|-------------|
| `plan_cmd.py` | `PlanCommand` | Show, list, validate plans |
| `capability_cmd.py` | `CapabilityCommand` | Show, list, validate capabilities |
| `validate_cmd.py` | `ValidateCommand` | Standalone validation |

**Key Features**:
- JSON output mode
- Long format with task progress
- Formatted text output

**Integration Point**: Called by Click commands in main.py.

```python
from aurora.cli.plan_cmd import PlanCommand

cmd = PlanCommand()
output = cmd.list(json_output=True, long=True)
output = cmd.show(plan_name='my-plan', modifications_only=True)
output = cmd.validate(plan_name='my-plan', strict=True)
```

---

## 6. `aurora/configurators/` - Tool Detection

**Purpose**: Detect and configure AI coding tools.

| File | Classes | Description |
|------|---------|-------------|
| `base.py` | `ToolConfigurator` (Protocol) | Base interface |
| `registry.py` | `ToolRegistry` | Registry of configurators |

**Key Features**:
- Detect Claude Code, Cline, AGENTS.md, CodeBuddy
- Configure tool-specific files

**Integration Point**: Used by init command.

```python
from aurora.configurators.registry import ToolRegistry

registry = ToolRegistry()
detected = registry.detect_tools(project_path)
registry.configure_all(project_path)
```

---

## 7. `aurora/configurators/slash/` - Slash Command System

**Purpose**: Generate slash commands for AI assistants.

| File | Classes | Description |
|------|---------|-------------|
| `base.py` | `SlashCommandConfigurator` (Protocol) | Base interface |
| `registry.py` | `SlashCommandRegistry` | Registry of slash configurators |
| `claude.py` | `ClaudeCodeConfigurator` | Claude Code slash commands |
| `opencode.py` | `OpenCodeConfigurator` | OpenCode slash commands |

**Key Features**:
- Generate `.claude/commands/aur/*.md` files
- Generate `.opencode/commands/*.md` files
- 7 commands: plan, archive, implement, query, mem, index, search

**Integration Point**: Called during init or update.

```python
from aurora.configurators.slash.claude import ClaudeCodeConfigurator

configurator = ClaudeCodeConfigurator()
configurator.generate_all(project_path)
```

---

## 8. `aurora/templates/` - File Templates

**Purpose**: Templates for generated files.

| File | Constants | Description |
|------|-----------|-------------|
| `agents.py` | `AGENTS_TEMPLATE` | AGENTS.md template (457 lines) |
| `project.py` | `PROJECT_TEMPLATE` | Project structure template |
| `claude.py` | `CLAUDE_TEMPLATE` | CLAUDE.md template |

**Integration Point**: Used by init and update commands.

```python
from aurora.templates.agents import AGENTS_TEMPLATE
from aurora.templates.project import PROJECT_TEMPLATE
```

---

## 9. `aurora/templates/slash_commands/` - Slash Command Templates

**Purpose**: Content templates for slash commands.

| File | Constants | Description |
|------|-----------|-------------|
| `templates.py` | `BASE_GUARDRAILS`, `PLAN_TEMPLATE`, `ARCHIVE_TEMPLATE`, etc. | 7 command templates |

**Commands**:
- `/aur:plan` - Plan generation
- `/aur:archive` - Archive plans
- `/aur:implement` - Execute plans
- `/aur:query` - Codebase query
- `/aur:mem` - Memory operations
- `/aur:index` - Index codebase
- `/aur:search` - Semantic search

```python
from aurora.templates.slash_commands.templates import PLAN_TEMPLATE, ARCHIVE_TEMPLATE
```

---

## 10. `aurora/converters/` - Format Conversion

**Purpose**: Convert between formats.

| File | Functions | Description |
|------|-----------|-------------|
| `json.py` | `plan_to_json()`, `capability_to_json()`, `validation_report_to_json()` | JSON conversion |

**Integration Point**: Used by CLI for --json output.

```python
from aurora.converters.json import plan_to_json, capability_to_json

json_data = plan_to_json(parsed_plan)
```

---

## 11. `aurora/utils/` - Utilities

**Purpose**: Common utility functions.

| File | Functions | Description |
|------|-----------|-------------|
| `filesystem.py` | `find_project_root()`, `read_markdown_file()` | File operations |
| `discovery.py` | `get_active_plan_ids()`, `get_capability_ids()` | Find plans/capabilities |
| `interactive.py` | `is_interactive()` | Terminal detection |
| `task_progress.py` | `count_tasks()`, `format_task_status()` | Task counting |
| `match.py` | `levenshtein()`, `nearest_matches()` | Fuzzy matching |

**Integration Point**: Used throughout the package.

```python
from aurora.utils.discovery import get_active_plan_ids, get_capability_ids
from aurora.utils.filesystem import find_project_root
from aurora.utils.match import nearest_matches
from aurora.utils.task_progress import count_tasks
```

---

## 12. `aurora/config.py` & `aurora/global_config.py` - Configuration

**Purpose**: Configuration constants and global config management.

| File | Content | Description |
|------|---------|-------------|
| `config.py` | `AURORA_MARKERS`, `AI_TOOLS` | Tool markers and paths |
| `global_config.py` | `get_global_config()`, `save_global_config()` | XDG config management |

**Integration Point**: Used by configurators.

```python
from aurora.config import AURORA_MARKERS, AI_TOOLS
from aurora.global_config import get_global_config, save_global_config
```

---

## Dependency Graph

```
                    ┌─────────────┐
                    │   schemas   │
                    └─────┬───────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌─────────┐ ┌──────────┐ ┌─────────┐
        │ parsers │ │validation│ │converters│
        └────┬────┘ └────┬─────┘ └─────────┘
             │           │
             └─────┬─────┘
                   ▼
            ┌──────────┐
            │ commands │
            └────┬─────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌───────────┐
│   cli   │ │templates│ │configurators│
└─────────┘ └─────────┘ └───────────┘
                              │
                              ▼
                        ┌───────────┐
                        │   slash   │
                        └───────────┘
```

---

## Quick Reference: What to Import

### For Validation
```python
from aurora.validation.validator import Validator
from aurora.validation.types import ValidationReport, ValidationIssue, ValidationLevel
```

### For Parsing
```python
from aurora.parsers.markdown import MarkdownParser, ParsedCapability, ParsedPlan
from aurora.parsers.plan_parser import PlanParser
from aurora.parsers.requirements import parse_modification_spec
```

### For Commands
```python
from aurora.commands.archive import ArchiveCommand
from aurora.commands.init import InitCommand
from aurora.commands.list import ListCommand
from aurora.commands.update import UpdateCommand
from aurora.commands.view import ViewCommand
```

### For CLI Wrappers
```python
from aurora.cli.plan_cmd import PlanCommand
from aurora.cli.capability_cmd import CapabilityCommand
from aurora.cli.validate_cmd import ValidateCommand
```

### For Slash Commands
```python
from aurora.configurators.slash.registry import SlashCommandRegistry
from aurora.configurators.slash.claude import ClaudeCodeConfigurator
from aurora.configurators.slash.opencode import OpenCodeConfigurator
```

### For Utilities
```python
from aurora.utils.discovery import get_active_plan_ids, get_capability_ids
from aurora.utils.filesystem import find_project_root, read_markdown_file
from aurora.utils.match import nearest_matches
from aurora.utils.task_progress import count_tasks, format_task_status
```
