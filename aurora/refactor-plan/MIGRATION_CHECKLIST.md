# Aurora Planning Migration Checklist

Step-by-step checklist for migrating the ported OpenSpec code to `aurora_cli.planning`.

---

## Pre-Migration Verification

### Source Verification (in `/tmp/openspec-source/`)

- [ ] **1.1** All 284 tests pass
  ```bash
  cd /tmp/openspec-source
  pytest tests/ -v
  # Expected: 284 passed
  ```

- [ ] **1.2** No mypy errors
  ```bash
  mypy aurora/ --ignore-missing-imports
  # Expected: Success: no issues found in 47 source files
  ```

- [ ] **1.3** Ruff check (style issues documented)
  ```bash
  ruff check aurora/
  # Expected: 58 errors (E501 line length - acceptable)
  ```

---

## Phase 1: Copy Package

### Directory Setup

- [ ] **2.1** Create target directory
  ```bash
  cd /home/hamr/PycharmProjects/aurora
  mkdir -p packages/cli/src/aurora_cli/planning
  ```

- [ ] **2.2** Copy aurora package
  ```bash
  cp -r /tmp/openspec-source/aurora/* packages/cli/src/aurora_cli/planning/
  ```

- [ ] **2.3** Copy tests
  ```bash
  mkdir -p packages/cli/tests/planning
  cp -r /tmp/openspec-source/tests/* packages/cli/tests/planning/
  ```

- [ ] **2.4** Verify file counts
  ```bash
  find packages/cli/src/aurora_cli/planning -name "*.py" | wc -l
  # Expected: 47 Python files

  find packages/cli/tests/planning -name "test_*.py" | wc -l
  # Expected: ~30 test files
  ```

---

## Phase 2: Fix Imports

### Update Package Imports

- [ ] **3.1** Update all internal imports from `aurora.` to `aurora_cli.planning.`
  ```bash
  # In packages/cli/src/aurora_cli/planning/
  find . -name "*.py" -exec sed -i 's/from aurora\./from aurora_cli.planning./g' {} \;
  find . -name "*.py" -exec sed -i 's/import aurora\./import aurora_cli.planning./g' {} \;
  ```

- [ ] **3.2** Update test imports
  ```bash
  # In packages/cli/tests/planning/
  find . -name "*.py" -exec sed -i 's/from aurora\./from aurora_cli.planning./g' {} \;
  find . -name "*.py" -exec sed -i 's/import aurora\./import aurora_cli.planning./g' {} \;
  ```

- [ ] **3.3** Verify no remaining `from aurora.` imports
  ```bash
  grep -r "from aurora\." packages/cli/src/aurora_cli/planning/
  grep -r "import aurora\." packages/cli/src/aurora_cli/planning/
  # Expected: No matches (or only in docstrings/comments)
  ```

### Create Package __init__.py

- [ ] **3.4** Create/update `packages/cli/src/aurora_cli/planning/__init__.py`
  ```python
  """Aurora Planning System - ported from OpenSpec."""

  from aurora_cli.planning.schemas.plan import Plan, Modification, ModificationOperation
  from aurora_cli.planning.schemas.capability import Capability
  from aurora_cli.planning.schemas.base import Requirement, Scenario
  from aurora_cli.planning.validation.validator import Validator
  from aurora_cli.planning.validation.types import ValidationReport, ValidationIssue
  from aurora_cli.planning.parsers.markdown import MarkdownParser
  from aurora_cli.planning.parsers.plan_parser import PlanParser

  __all__ = [
      "Plan", "Modification", "ModificationOperation",
      "Capability", "Requirement", "Scenario",
      "Validator", "ValidationReport", "ValidationIssue",
      "MarkdownParser", "PlanParser",
  ]
  ```

---

## Phase 3: Test Migration Verification

### Run Tests in New Location

- [ ] **4.1** Set PYTHONPATH and run tests
  ```bash
  cd /home/hamr/PycharmProjects/aurora
  PYTHONPATH=packages/cli/src pytest packages/cli/tests/planning/ -v
  # Expected: 284 passed
  ```

- [ ] **4.2** Run mypy on migrated code
  ```bash
  MYPYPATH=packages/cli/src mypy packages/cli/src/aurora_cli/planning/ --ignore-missing-imports
  # Expected: Success: no issues found
  ```

- [ ] **4.3** Run specific test categories
  ```bash
  # Unit tests
  PYTHONPATH=packages/cli/src pytest packages/cli/tests/planning/unit/ -v
  # Expected: 256 passed

  # Integration tests
  PYTHONPATH=packages/cli/src pytest packages/cli/tests/planning/integration/ -v
  # Expected: 28 passed
  ```

### Verify Import Resolution

- [ ] **4.4** Test imports from Python REPL
  ```bash
  cd /home/hamr/PycharmProjects/aurora
  PYTHONPATH=packages/cli/src python3 -c "
  from aurora_cli.planning import Validator, Plan, Capability
  from aurora_cli.planning.commands.archive import ArchiveCommand
  from aurora_cli.planning.configurators.slash.claude import ClaudeCodeConfigurator
  print('All imports successful!')
  "
  ```

---

## Phase 4: CLI Integration

### Add Planning Commands to Main CLI

- [ ] **5.1** Update `packages/cli/src/aurora_cli/main.py`
  ```python
  # Add imports
  from aurora_cli.planning.commands.init import InitCommand
  from aurora_cli.planning.commands.list import ListCommand
  from aurora_cli.planning.commands.archive import ArchiveCommand
  from aurora_cli.planning.commands.update import UpdateCommand
  from aurora_cli.planning.commands.view import ViewCommand

  # Add command group
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
  @click.option('--mode', '-m', default='changes', type=click.Choice(['changes', 'specs']))
  @click.option('--json', 'json_output', is_flag=True)
  @click.option('--sort', default='recent', type=click.Choice(['recent', 'name']))
  def list(mode, json_output, sort):
      """List plans or capabilities."""
      cmd = ListCommand()
      cmd.execute('.', mode=mode, options={'json': json_output, 'sort': sort})

  @plan.command()
  @click.argument('change_name', required=False)
  @click.option('--yes', '-y', is_flag=True)
  @click.option('--skip-validation', is_flag=True)
  def archive(change_name, yes, skip_validation):
      """Archive a completed plan."""
      cmd = ArchiveCommand()
      cmd.execute('.', change_name=change_name, yes=yes, skip_validation=skip_validation)

  @plan.command()
  def update():
      """Update AGENTS.md template."""
      cmd = UpdateCommand()
      cmd.execute('.')

  @plan.command()
  @click.option('--json', 'json_output', is_flag=True)
  def view(json_output):
      """View planning dashboard."""
      cmd = ViewCommand()
      cmd.execute('.', json_output=json_output)
  ```

- [ ] **5.2** Test CLI commands
  ```bash
  cd /home/hamr/PycharmProjects/aurora
  aur plan --help
  aur plan init --help
  aur plan list --help
  ```

---

## Phase 5: Full Test Suite

### Run Aurora's Full Test Suite

- [ ] **6.1** Run all Aurora tests
  ```bash
  cd /home/hamr/PycharmProjects/aurora
  make test
  ```

- [ ] **6.2** Run quality checks
  ```bash
  make quality-check
  ```

- [ ] **6.3** Verify no regressions
  ```bash
  # Compare test counts before and after
  pytest tests/ --collect-only 2>/dev/null | tail -1
  ```

---

## Phase 6: Documentation

### Update Aurora Documentation

- [ ] **7.1** Update CLAUDE.md with planning commands
  ```markdown
  ## Planning Commands

  aur plan init .        # Initialize planning structure
  aur plan list          # List active plans
  aur plan list --specs  # List capabilities
  aur plan archive <name> # Archive completed plan
  aur plan update        # Update AGENTS.md template
  aur plan view          # View planning dashboard
  ```

- [ ] **7.2** Copy reference docs
  ```bash
  mkdir -p docs/planning
  cp /tmp/openspec-source/aurora/refactor-plan/PACKAGE_MAP.md docs/planning/
  cp /tmp/openspec-source/aurora/refactor-plan/API_REFERENCE.md docs/planning/
  cp /tmp/openspec-source/aurora/refactor-plan/FILE_TO_FILE_MAPPING.md docs/planning/
  ```

---

## Phase 7: Cleanup

### Remove Temporary Files

- [ ] **8.1** Remove refactor-plan directory from planning package
  ```bash
  rm -rf packages/cli/src/aurora_cli/planning/refactor-plan
  ```

- [ ] **8.2** Remove __pycache__ directories
  ```bash
  find packages/cli/src/aurora_cli/planning -name "__pycache__" -type d -exec rm -rf {} +
  find packages/cli/tests/planning -name "__pycache__" -type d -exec rm -rf {} +
  ```

---

## Post-Migration Verification

### Final Checks

- [ ] **9.1** All 284 planning tests pass in new location
- [ ] **9.2** All existing Aurora tests still pass
- [ ] **9.3** CLI commands work (`aur plan init`, `aur plan list`, etc.)
- [ ] **9.4** No import errors when using the package
- [ ] **9.5** Type checking passes
- [ ] **9.6** Documentation updated

---

## Rollback Plan

If migration fails:

1. Remove migrated files:
   ```bash
   rm -rf packages/cli/src/aurora_cli/planning
   rm -rf packages/cli/tests/planning
   ```

2. Revert main.py changes:
   ```bash
   git checkout packages/cli/src/aurora_cli/main.py
   ```

3. Original code remains in `/tmp/openspec-source/aurora/`

---

## Test Count Summary

| Category | Tests | Location |
|----------|-------|----------|
| Unit: Schemas | 23 | `tests/unit/schemas/` |
| Unit: Validation | 23 | `tests/unit/validation/` |
| Unit: Parsers | 36 | `tests/unit/parsers/` |
| Unit: Commands | 49 | `tests/unit/commands/` |
| Unit: CLI | 20 | `tests/unit/cli/` |
| Unit: Config | 22 | `tests/unit/` |
| Unit: Configurators | 8 | `tests/unit/configurators/` |
| Unit: Slash | 29 | `tests/unit/configurators/slash/` |
| Unit: Converters | 7 | `tests/unit/converters/` |
| Unit: Utils | 39 | `tests/unit/utils/` |
| Integration | 28 | `tests/integration/` |
| **TOTAL** | **284** | |

---

## Quick Commands Reference

```bash
# Run all planning tests
PYTHONPATH=packages/cli/src pytest packages/cli/tests/planning/ -v

# Run specific test file
PYTHONPATH=packages/cli/src pytest packages/cli/tests/planning/unit/validation/test_validator.py -v

# Check imports work
PYTHONPATH=packages/cli/src python3 -c "from aurora_cli.planning import Validator; print('OK')"

# Type check
MYPYPATH=packages/cli/src mypy packages/cli/src/aurora_cli/planning/ --ignore-missing-imports
```
