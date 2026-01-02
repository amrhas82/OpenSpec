# Aurora Planning System Integration Guide

This guide explains how to integrate the ported OpenSpec planning system into the main Aurora repository.

## Overview

The OpenSpec → Aurora port provides a structured planning system for managing change proposals, capabilities, and validation. The port consists of ~7,454 lines of Python code with 284 passing tests.

## Package Structure

```
aurora/
├── __init__.py
├── schemas/           # Pydantic models (Plan, Capability, Modification)
├── validation/        # Validator class and validation types
├── parsers/           # Markdown and plan parsers
├── commands/          # Core commands (archive, init, list, update, view)
├── cli/               # CLI wrapper classes
├── configurators/     # Tool detection and slash commands
│   └── slash/         # Slash command configurators
├── templates/         # AGENTS.md, project templates
│   └── slash_commands/  # Slash command templates
├── converters/        # JSON conversion utilities
└── utils/             # Discovery, filesystem, matching utilities
```

## Integration Steps

### Step 1: Copy Package

```bash
# From Aurora main repo root
cp -r /tmp/openspec-source/aurora packages/cli/src/aurora_cli/planning
```

### Step 2: Update Package Imports

Update `packages/cli/src/aurora_cli/__init__.py` to export planning modules:

```python
from aurora_cli.planning import (
    Validator,
    Plan,
    Capability,
    PlanParser,
    MarkdownParser,
    # ... other exports
)
```

### Step 3: Add CLI Commands

Add planning commands to the main Aurora CLI in `packages/cli/src/aurora_cli/main.py`:

```python
from aurora_cli.planning.commands.init import InitCommand
from aurora_cli.planning.commands.list import ListCommand
from aurora_cli.planning.commands.archive import ArchiveCommand
from aurora_cli.planning.commands.update import UpdateCommand
from aurora_cli.planning.commands.view import ViewCommand

@cli.group()
def plan():
    """Planning system commands."""
    pass

@plan.command()
@click.argument('project_path', default='.')
def init(project_path):
    """Initialize planning structure."""
    cmd = InitCommand()
    cmd.execute(project_path)

@plan.command()
@click.option('--mode', default='changes', type=click.Choice(['changes', 'specs']))
def list(mode):
    """List plans or capabilities."""
    cmd = ListCommand()
    cmd.execute('.', mode=mode)

# ... similar for archive, update, view
```

### Step 4: Update Dependencies

Add required dependencies to `pyproject.toml` if not already present:

```toml
[project.dependencies]
pydantic = ">=2.0.0"
# rich (already in Aurora)
```

### Step 5: Run Tests

```bash
# Run ported tests
pytest packages/cli/src/aurora_cli/planning/tests/ -v

# Run full Aurora test suite
make test
```

## Key APIs

### Validation

```python
from aurora_cli.planning.validation.validator import Validator

validator = Validator(strict_mode=True)

# Validate a capability
report = validator.validate_capability('/path/to/spec.md')
if report.valid:
    print("Valid!")
else:
    for issue in report.issues:
        print(f"{issue.level}: {issue.message}")

# Validate a plan
report = validator.validate_plan('/path/to/plan.md')
```

### Parsing

```python
from aurora_cli.planning.parsers.markdown import MarkdownParser
from aurora_cli.planning.parsers.plan_parser import PlanParser

# Parse a capability spec
parser = MarkdownParser()
cap = parser.parse_capability(content)

# Parse a plan
plan_parser = PlanParser()
plan = plan_parser.parse(content)
```

### Commands

```python
from aurora_cli.planning.commands.archive import ArchiveCommand

cmd = ArchiveCommand()
cmd.execute(
    project_path='/path/to/project',
    change_name='my-change',
    yes=True,
    skip_validation=False
)
```

## Slash Commands

The port includes 7 slash commands for AI assistants:

- `/aur:plan` - Plan generation
- `/aur:archive` - Archive plans
- `/aur:implement` - Execute plans
- `/aur:query` - Codebase query
- `/aur:mem` - Memory operations
- `/aur:index` - Index codebase
- `/aur:search` - Semantic search

These are configured via:

```python
from aurora_cli.planning.configurators.slash.claude import ClaudeCodeConfigurator

configurator = ClaudeCodeConfigurator()
configurator.configure_slash_commands(project_path)
```

## Terminology Mapping

When reading code, remember the OpenSpec → Aurora terminology:

| OpenSpec | Aurora |
|----------|--------|
| change | plan |
| spec | capability |
| delta | modification |
| openspec/ | aurora/ |
| changes/ | plans/ |
| specs/ | capabilities/ |

## Testing

The ported code includes 284 tests covering:

- Schema validation
- Parsing edge cases
- Command execution
- CLI workflows
- Integration scenarios

Run tests with:

```bash
cd /tmp/openspec-source
pytest tests/ -v
```

## Quality Status

- **Tests**: 284 passing
- **Type checking**: 0 mypy errors
- **Lint**: 58 style issues (E501 line length - non-blocking)

## Further Reading

- `PORT_REPORT.md` - Detailed port status
- `API_REFERENCE.md` - Complete API documentation
- Original OpenSpec: https://github.com/Fission-AI/OpenSpec
