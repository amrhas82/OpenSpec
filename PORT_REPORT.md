# OpenSpec → Aurora Port Report

**Source**: OpenSpec v0.17.2 (https://github.com/Fission-AI/OpenSpec)
**Fork**: https://github.com/amrhas82/OpenSpec
**Branch**: `refactored`
**Target**: Aurora Planning System (Python)
**Started**: 2026-01-02
**Last Updated**: 2026-01-02

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total OpenSpec Lines | ~8,659 (source to consider) |
| Lines to Port | ~5,800 (source) |
| Lines Skipped | ~2,800 (completions, artifact-graph, slash configurators) |
| Port Percentage | ~67% of considered source |

---

## Terminology Mapping

| OpenSpec | Aurora | Notes |
|----------|--------|-------|
| `openspec` | `aurora` | Package/directory name |
| `change` | `plan` | A proposal for changes |
| `spec` | `capability` | A system capability |
| `delta` | `modification` | A change to a requirement |
| `proposal.md` | `plan.md` | Main plan file |
| `Change` | `Plan` | Class/type name |
| `Spec` | `Capability` | Class/type name |
| `Delta` | `Modification` | Class/type name |
| `openspec/` dir | `aurora/` dir | Project directory |
| `changes/` | `plans/` | Plans directory |
| `specs/` | `capabilities/` | Capabilities directory |

---

## Stack Translation

| TypeScript/Node | Python | Notes |
|-----------------|--------|-------|
| Zod | Pydantic | Schema validation |
| Commander.js | Click | CLI framework |
| Inquirer.js | Rich.prompt / questionary | Interactive prompts |
| Chalk | Rich.console | Terminal colors |
| ora | Rich.progress | Spinners/progress |
| fs/path | pathlib | File system |
| vitest | pytest | Testing |
| async/await | async/await | Same pattern |

---

## COMPLETE File Mapping: TO PORT

### Phase 1: Schemas (76 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/schemas/base.schema.ts` | 19 | `aurora/schemas/base.py` | 🔲 TODO | `Scenario`, `Requirement` |
| `src/core/schemas/change.schema.ts` | 41 | `aurora/schemas/plan.py` | 🔲 TODO | `ModificationOperation`, `Modification`, `Plan` |
| `src/core/schemas/spec.schema.ts` | 16 | `aurora/schemas/capability.py` | 🔲 TODO | `Capability` |

### Phase 2: Validation (515 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/validation/constants.ts` | 48 | `aurora/validation/constants.py` | 🔲 TODO | `VALIDATION_MESSAGES`, thresholds |
| `src/core/validation/types.ts` | 18 | `aurora/validation/types.py` | 🔲 TODO | `ValidationIssue`, `ValidationReport` |
| `src/core/validation/validator.ts` | 449 | `aurora/validation/validator.py` | 🔲 TODO | `Validator` class |

**Validator Key Functions:**
- `validateSpec()` → `validate_capability()`
- `validateChange()` → `validate_plan()`
- `validateChangeDeltaSpecs()` → `validate_plan_modification_specs()`
- `applySpecRules()` → `_apply_capability_rules()`
- `applyChangeRules()` → `_apply_plan_rules()`
- `extractRequirementText()` → `_extract_requirement_text()`
- `containsShallOrMust()` → `_contains_shall_or_must()`
- `countScenarios()` → `_count_scenarios()`

### Phase 3: Parsers (703 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/parsers/markdown-parser.ts` | 236 | `aurora/parsers/markdown.py` | 🔲 TODO | `MarkdownParser` class |
| `src/core/parsers/change-parser.ts` | 233 | `aurora/parsers/plan.py` | 🔲 TODO | `PlanParser` class |
| `src/core/parsers/requirement-blocks.ts` | 234 | `aurora/parsers/requirements.py` | 🔲 TODO | `parse_modification_spec()` |

**Parser Key Functions:**
- `MarkdownParser.parse()` → `MarkdownParser.parse()`
- `MarkdownParser.extractSections()` → `MarkdownParser.extract_sections()`
- `parseDeltaSpec()` → `parse_modification_spec()`
- `extractRequirementsSection()` → `extract_requirements_section()`
- `normalizeRequirementName()` → `normalize_requirement_name()`

### Phase 4: Core Commands (2,151 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/archive.ts` | 625 | `aurora/commands/archive.py` | 🔲 TODO | `archive_plan()` |
| `src/core/init.ts` | 986 | `aurora/commands/init.py` | 🔲 TODO | `init_project()` |
| `src/core/list.ts` | 193 | `aurora/commands/list.py` | 🔲 TODO | `list_items()` |
| `src/core/view.ts` | 218 | `aurora/commands/view.py` | 🔲 TODO | `view_dashboard()` |
| `src/core/update.ts` | 129 | `aurora/commands/update.py` | 🔲 TODO | `update_instructions()` |

### Phase 5: CLI Command Classes (1,240 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/commands/change.ts` | 292 | `aurora/cli/plan_cmd.py` | 🔲 TODO | `PlanCommand` class |
| `src/commands/validate.ts` | 326 | `aurora/cli/validate_cmd.py` | 🔲 TODO | `ValidateCommand` class |
| `src/commands/spec.ts` | 251 | `aurora/cli/capability_cmd.py` | 🔲 TODO | `CapabilityCommand` class |
| `src/commands/config.ts` | 233 | `aurora/cli/config_cmd.py` | 🔲 TODO | `ConfigCommand` class |
| `src/commands/show.ts` | 138 | `aurora/cli/show_cmd.py` | 🔲 TODO | `ShowCommand` class |

### Phase 6: Config (368 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/config.ts` | 41 | `aurora/config.py` | 🔲 TODO | `AURORA_MARKERS`, `AI_TOOLS` |
| `src/core/config-schema.ts` | 231 | `aurora/config_schema.py` | 🔲 TODO | `GlobalConfigSchema`, nested utils |
| `src/core/global-config.ts` | 137 | `aurora/global_config.py` | 🔲 TODO | XDG paths, load/save config |

**Config Key Functions:**
- `getGlobalConfigDir()` → `get_global_config_dir()`
- `getGlobalDataDir()` → `get_global_data_dir()`
- `getGlobalConfig()` → `get_global_config()`
- `saveGlobalConfig()` → `save_global_config()`
- `validateConfigKeyPath()` → `validate_config_key_path()`
- `getNestedValue()` → `get_nested_value()`
- `setNestedValue()` → `set_nested_value()`

### Phase 7: Configurators - Tool Detection (145 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/configurators/base.ts` | 5 | `aurora/configurators/base.py` | 🔲 TODO | `ToolConfigurator` protocol |
| `src/core/configurators/registry.ts` | 49 | `aurora/configurators/registry.py` | 🔲 TODO | `ToolRegistry` class |
| `src/core/configurators/claude.ts` | 22 | `aurora/configurators/claude.py` | 🔲 TODO | Claude Code detection |
| `src/core/configurators/cline.ts` | 23 | `aurora/configurators/cline.py` | 🔲 TODO | Cline detection |
| `src/core/configurators/agents.ts` | 23 | `aurora/configurators/agents.py` | 🔲 TODO | AGENTS.md detection |
| `src/core/configurators/codebuddy.ts` | 23 | `aurora/configurators/codebuddy.py` | 🔲 TODO | CodeBuddy detection |

### Phase 8: Templates (496 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/templates/index.ts` | 1 | `aurora/templates/__init__.py` | 🔲 TODO | Template exports |
| `src/core/templates/agents-template.ts` | 457 | `aurora/templates/agents.py` | 🔲 TODO | AGENTS.md template |
| `src/core/templates/project-template.ts` | 37 | `aurora/templates/project.py` | 🔲 TODO | Project template |
| `src/core/templates/claude-template.ts` | 1 | `aurora/templates/claude.py` | 🔲 TODO | CLAUDE.md template |

### Phase 9: Utilities (537 lines)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/utils/file-system.ts` | 209 | `aurora/utils/filesystem.py` | 🔲 TODO | File operations |
| `src/utils/task-progress.ts` | 43 | `aurora/utils/progress.py` | 🔲 TODO | Progress tracking |
| `src/utils/item-discovery.ts` | 66 | `aurora/utils/discovery.py` | 🔲 TODO | Find plans/capabilities |
| `src/utils/change-utils.ts` | 102 | `aurora/utils/plan_utils.py` | 🔲 TODO | Plan helpers |
| `src/utils/match.ts` | 26 | `aurora/utils/match.py` | 🔲 TODO | Fuzzy matching |
| `src/utils/interactive.ts` | 29 | `aurora/utils/interactive.py` | 🔲 TODO | `is_interactive()` |
| `src/utils/shell-detection.ts` | 62 | `aurora/utils/shell.py` | 🔲 TODO | Shell detection |
| `src/core/converters/json-converter.ts` | 62 | `aurora/converters/json.py` | 🔲 TODO | JSON conversion |

**Utils Key Functions:**
- `findProjectRoot()` → `find_project_root()`
- `readMarkdownFile()` → `read_markdown_file()`
- `getActiveChangeIds()` → `get_active_plan_ids()`
- `getSpecIds()` → `get_capability_ids()`
- `nearestMatches()` → `nearest_matches()`
- `isInteractive()` → `is_interactive()`

---

## COMPLETE File Mapping: TO SKIP

### ❌ Completions (Use Click Instead) - ~1,537 lines

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/completions/command-registry.ts` | 364 | Click has built-in completions |
| `src/core/completions/completion-provider.ts` | 128 | Click handles this |
| `src/core/completions/factory.ts` | 74 | Not needed |
| `src/core/completions/types.ts` | 90 | Not needed |
| `src/core/completions/generators/*.ts` | ~374 | Click provides this |
| `src/core/completions/installers/*.ts` | ~507 | Click provides this |

**Rationale:** Click provides shell completion for bash, zsh, and fish out of the box.

### ❌ Artifact Graph (Experimental) - ~1,469 lines

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/artifact-graph/*.ts` | ~874 | Experimental workflow orchestration |
| `src/commands/artifact-workflow.ts` | 595 | Experimental command |

**Rationale:** Aurora has SOAR-based decomposition. May revisit later.

### ❌ Slash Command Configurators - ~1,500 lines

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/configurators/slash/*.ts` | ~1,500 | Very tool-specific slash commands |

**Rationale:** These configure slash commands for specific tools. May port later if needed.

### ❌ CLI Entry Point - 326 lines

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/cli/index.ts` | 326 | Aurora has own main.py |

**Rationale:** Integrate into existing Aurora CLI.

### ❌ Index Re-exports - ~23 lines

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/index.ts` | 1 | Just re-exports |
| `src/core/index.ts` | 1 | Just re-exports |
| `src/core/schemas/index.ts` | 19 | Just re-exports |
| `src/utils/index.ts` | 2 | Just re-exports |

---

## Tests to Port

| Test File | Target | Status |
|-----------|--------|--------|
| `test/core/validation.test.ts` | `tests/unit/validation/test_validator.py` | 🔲 TODO |
| `test/core/parsers/markdown-parser.test.ts` | `tests/unit/parsers/test_markdown.py` | 🔲 TODO |
| `test/core/archive.test.ts` | `tests/unit/commands/test_archive.py` | 🔲 TODO |
| `test/core/init.test.ts` | `tests/unit/commands/test_init.py` | 🔲 TODO |
| `test/core/list.test.ts` | `tests/unit/commands/test_list.py` | 🔲 TODO |
| `test/core/view.test.ts` | `tests/unit/commands/test_view.py` | 🔲 TODO |
| `test/core/update.test.ts` | `tests/unit/commands/test_update.py` | 🔲 TODO |
| `test/core/config-schema.test.ts` | `tests/unit/test_config_schema.py` | 🔲 TODO |
| `test/core/global-config.test.ts` | `tests/unit/test_global_config.py` | 🔲 TODO |
| `test/core/converters/*.test.ts` | `tests/unit/converters/test_json.py` | 🔲 TODO |
| `test/utils/*.test.ts` | `tests/unit/utils/test_*.py` | 🔲 TODO |
| `test/commands/*.test.ts` | `tests/unit/cli/test_*_cmd.py` | 🔲 TODO |
| `test/cli-e2e/basic.test.ts` | `tests/integration/test_cli_e2e.py` | 🔲 TODO |

---

## Port Progress Tracking

### Phase 0: Setup ✅ COMPLETE
- [x] Fork OpenSpec repo
- [x] Create `refactored` branch
- [x] Create PORT_REPORT.md
- [x] Create Python package structure
- [x] Create tests/ structure
- [x] Commit and push (8d83043, 532a40b)

### Phase 1: Schemas (TDD) 🔲 IN PROGRESS
- [ ] 1.1 Port `base.schema.ts` → `aurora/schemas/base.py`
- [ ] 1.2 Port `change.schema.ts` → `aurora/schemas/plan.py`
- [ ] 1.3 Port `spec.schema.ts` → `aurora/schemas/capability.py`

### Phase 2: Validation (TDD) 🔲 TODO
- [ ] 2.1 Port `constants.ts` → `aurora/validation/constants.py`
- [ ] 2.2 Port `types.ts` → `aurora/validation/types.py`
- [ ] 2.3 Port `validator.ts` → `aurora/validation/validator.py`

### Phase 3: Parsers (TDD) 🔲 TODO
- [ ] 3.1 Port `markdown-parser.ts` → `aurora/parsers/markdown.py`
- [ ] 3.2 Port `change-parser.ts` → `aurora/parsers/plan.py`
- [ ] 3.3 Port `requirement-blocks.ts` → `aurora/parsers/requirements.py`

### Phase 4: Core Commands (TDD) 🔲 TODO
- [ ] 4.1 Port `archive.ts` → `aurora/commands/archive.py`
- [ ] 4.2 Port `init.ts` → `aurora/commands/init.py`
- [ ] 4.3 Port `list.ts` → `aurora/commands/list.py`
- [ ] 4.4 Port `view.ts` → `aurora/commands/view.py`
- [ ] 4.5 Port `update.ts` → `aurora/commands/update.py`

### Phase 5: CLI Commands (TDD) 🔲 TODO
- [ ] 5.1 Port `change.ts` → `aurora/cli/plan_cmd.py`
- [ ] 5.2 Port `validate.ts` → `aurora/cli/validate_cmd.py`
- [ ] 5.3 Port `spec.ts` → `aurora/cli/capability_cmd.py`
- [ ] 5.4 Port `config.ts` → `aurora/cli/config_cmd.py`
- [ ] 5.5 Port `show.ts` → `aurora/cli/show_cmd.py`

### Phase 6: Config 🔲 TODO
- [ ] 6.1 Port `config.ts` → `aurora/config.py`
- [ ] 6.2 Port `config-schema.ts` → `aurora/config_schema.py`
- [ ] 6.3 Port `global-config.ts` → `aurora/global_config.py`

### Phase 7: Configurators 🔲 TODO
- [ ] 7.1 Port `base.ts` → `aurora/configurators/base.py`
- [ ] 7.2 Port `registry.ts` → `aurora/configurators/registry.py`
- [ ] 7.3 Port individual tool configurators

### Phase 8: Templates 🔲 TODO
- [ ] 8.1 Port `agents-template.ts` → `aurora/templates/agents.py`
- [ ] 8.2 Port `project-template.ts` → `aurora/templates/project.py`
- [ ] 8.3 Port other templates

### Phase 9: Utilities 🔲 TODO
- [ ] 9.1 Port `file-system.ts` → `aurora/utils/filesystem.py`
- [ ] 9.2 Port `task-progress.ts` → `aurora/utils/progress.py`
- [ ] 9.3 Port `item-discovery.ts` → `aurora/utils/discovery.py`
- [ ] 9.4 Port `change-utils.ts` → `aurora/utils/plan_utils.py`
- [ ] 9.5 Port `match.ts` → `aurora/utils/match.py`
- [ ] 9.6 Port `interactive.ts` → `aurora/utils/interactive.py`
- [ ] 9.7 Port `shell-detection.ts` → `aurora/utils/shell.py`
- [ ] 9.8 Port `json-converter.ts` → `aurora/converters/json.py`

### Phase 10: Integration Tests 🔲 TODO
- [ ] 10.1 Port E2E tests

### Phase 11: Quality Assurance 🔲 TODO
- [ ] 11.1 Run full test suite
- [ ] 11.2 Type check (mypy)
- [ ] 11.3 Lint (ruff)
- [ ] 11.4 Coverage check

---

## Validation Checklist

Before declaring port complete:

- [ ] All ported tests pass (`pytest tests/ -v`)
- [ ] Type checking passes (`mypy aurora/`)
- [ ] Linting passes (`ruff check aurora/`)
- [ ] Behavior matches OpenSpec for key operations:
  - [ ] `aurora plan init` ≈ `openspec init`
  - [ ] `aurora plan list` ≈ `openspec list`
  - [ ] `aurora plan validate` ≈ `openspec validate`
  - [ ] `aurora plan archive` ≈ `openspec archive`
- [ ] PORT_REPORT.md fully updated with ✅ status
- [ ] Ready for integration into Aurora CLI

---

## Notes

- **TDD Approach**: Write Python tests first (based on TypeScript tests), then implement
- **Reference**: Keep `main` branch as untouched OpenSpec reference
- **This Branch**: `refactored` contains all Aurora port work
- **Next Phase**: After port complete, integrate into `aurora_cli/planning/`

---

*Working Directory: `/tmp/openspec-source/`*
*Branch: `refactored`*
