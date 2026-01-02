# OpenSpec → Aurora Port Report

**Source**: OpenSpec v0.17.2 (https://github.com/Fission-AI/OpenSpec)
**Fork**: https://github.com/amrhas82/OpenSpec
**Branch**: `refactored`
**Target**: Aurora Planning System (Python)
**Started**: 2026-01-02
**Completed**: 2026-01-02
**Status**: ✅ COMPLETE

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total OpenSpec Lines | ~8,659 (source to consider) |
| Lines Ported | ~7,454 (Python implementation) |
| Lines Skipped | ~2,800 (completions, artifact-graph) |
| Port Percentage | ~67% of considered source |
| **Total Tests** | **284 passing** |
| **Type Checking** | **0 mypy errors** |
| **Lint Status** | 58 style issues (non-blocking) |

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

## Phase Completion Status

### Phase 1: Schemas ✅ COMPLETE (23 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/schemas/base.schema.ts` | 19 | `aurora/schemas/base.py` | ✅ DONE | `Scenario`, `Requirement` |
| `src/core/schemas/change.schema.ts` | 41 | `aurora/schemas/plan.py` | ✅ DONE | `ModificationOperation`, `Modification`, `Plan` |
| `src/core/schemas/spec.schema.ts` | 16 | `aurora/schemas/capability.py` | ✅ DONE | `Capability` |

### Phase 2: Validation ✅ COMPLETE (23 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/validation/constants.ts` | 48 | `aurora/validation/constants.py` | ✅ DONE | `VALIDATION_MESSAGES`, thresholds |
| `src/core/validation/types.ts` | 18 | `aurora/validation/types.py` | ✅ DONE | `ValidationIssue`, `ValidationReport` |
| `src/core/validation/validator.ts` | 449 | `aurora/validation/validator.py` | ✅ DONE | `Validator` class (786 lines) |

### Phase 3: Parsers ✅ COMPLETE (36 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/parsers/markdown-parser.ts` | 236 | `aurora/parsers/markdown.py` | ✅ DONE | `MarkdownParser` class |
| `src/core/parsers/change-parser.ts` | 233 | `aurora/parsers/plan_parser.py` | ✅ DONE | `PlanParser` class |
| `src/core/parsers/requirement-blocks.ts` | 234 | `aurora/parsers/requirements.py` | ✅ DONE | `parse_modification_spec()` |

### Phase 4: Core Commands ✅ COMPLETE (49 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/archive.ts` | 625 | `aurora/commands/archive.py` | ✅ DONE (20 tests) | `ArchiveCommand.execute()` |
| `src/core/update.ts` | 129 | `aurora/commands/update.py` | ✅ DONE (6 tests) | `UpdateCommand.execute()` |
| `src/core/init.ts` | 986 | `aurora/commands/init.py` | ✅ DONE (8 tests) | `init_project()` |
| `src/core/list.ts` | 193 | `aurora/commands/list.py` | ✅ DONE (13 tests) | `list_items()` |
| `src/core/view.ts` | 218 | `aurora/commands/view.py` | ✅ DONE (2 tests) | `view_dashboard()` |

### Phase 5: CLI Commands ✅ COMPLETE (20 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/commands/change.ts` | 292 | `aurora/cli/plan_cmd.py` | ✅ DONE (9 tests) | `PlanCommand` class |
| `src/commands/validate.ts` | 326 | `aurora/cli/validate_cmd.py` | ✅ DONE (5 tests) | `ValidateCommand` |
| `src/commands/spec.ts` | 251 | `aurora/cli/capability_cmd.py` | ✅ DONE (6 tests) | `CapabilityCommand` class |

### Phase 6: Config ✅ COMPLETE (22 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/config.ts` | 41 | `aurora/config.py` | ✅ DONE (10 tests) | `AURORA_MARKERS`, `AI_TOOLS` |
| `src/core/global-config.ts` | 137 | `aurora/global_config.py` | ✅ DONE (12 tests) | XDG paths, load/save config |

### Phase 7: Configurators ✅ COMPLETE (8 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/configurators/base.ts` | 5 | `aurora/configurators/base.py` | ✅ DONE | `ToolConfigurator` protocol |
| `src/core/configurators/registry.ts` | 49 | `aurora/configurators/registry.py` | ✅ DONE (8 tests) | `ToolRegistry` class |

### Phase 8: Templates ✅ COMPLETE

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/templates/agents-template.ts` | 457 | `aurora/templates/agents.py` | ✅ DONE | AGENTS.md template (full) |
| `src/core/templates/project-template.ts` | 37 | `aurora/templates/project.py` | ✅ DONE | Project template |
| `src/core/templates/claude-template.ts` | 1 | `aurora/templates/claude.py` | ✅ DONE | CLAUDE.md template |

### Phase 9: Utilities ✅ COMPLETE (21 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/utils/file-system.ts` | 209 | `aurora/utils/filesystem.py` | ✅ DONE (6 tests) | File operations |
| `src/utils/item-discovery.ts` | 66 | `aurora/utils/discovery.py` | ✅ DONE (9 tests) | Find plans/capabilities |
| `src/utils/interactive.ts` | 29 | `aurora/utils/interactive.py` | ✅ DONE (6 tests) | `is_interactive()` |

### Phase 10: Slash Commands ✅ COMPLETE (29 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| Slash base/registry | ~500 | `aurora/configurators/slash/` | ✅ DONE | SlashCommandConfigurator, Registry |
| Claude configurator | ~200 | `aurora/configurators/slash/claude.py` | ✅ DONE | Claude Code integration |
| OpenCode configurator | ~200 | `aurora/configurators/slash/opencode.py` | ✅ DONE | OpenCode integration |
| Command templates | ~185 | `aurora/templates/slash_commands/` | ✅ DONE | 7 slash commands |

### Phase 11: Converters & Utils ✅ COMPLETE (25 tests)

| Source File | Lines | Target File | Status | Key Items |
|-------------|-------|-------------|--------|-----------|
| `src/core/converters/json-converter.ts` | 62 | `aurora/converters/json.py` | ✅ DONE (7 tests) | JSON conversion |
| `src/utils/task-progress.ts` | 43 | `aurora/utils/task_progress.py` | ✅ DONE (10 tests) | Task counting |
| `src/utils/match.ts` | 26 | `aurora/utils/match.py` | ✅ DONE (8 tests) | Fuzzy matching |

### Phase 12: Integration Tests ✅ COMPLETE (28 tests)

- CLI E2E tests: 7 tests
- Slash command integration: 11 tests
- JSON conversion integration: 10 tests

### Phase 13: Quality Assurance ✅ COMPLETE

- **Tests**: 284 passing
- **Type Checking**: 0 mypy errors (all fixed)
- **Lint**: 58 style issues (E501 line length, SIM suggestions - non-blocking)
- **Coverage**: Available via pytest-cov

### Phase 14: Finalization ✅ COMPLETE

- PORT_REPORT.md updated with final status
- INTEGRATION_GUIDE.md created
- API_REFERENCE.md created
- All documentation current

---

## Skipped Files (Documented)

| Category | Lines | Reason | Status |
|----------|-------|--------|--------|
| Completions (`src/core/completions/`) | ~1,537 | Use Click's built-in | SKIP ✅ |
| Artifact Graph (`src/core/artifact-graph/`) | ~1,469 | Aurora has SOAR for dependencies | SKIP ✅ |
| CLI Entry (`src/cli/index.ts`) | 326 | Integrate into Aurora's main.py | SKIP ✅ |
| Index re-exports | ~23 | Just re-exports | SKIP ✅ |
| Styles (`src/core/styles/`) | ~50 | Use Python's rich library | SKIP ✅ |

---

## Next Steps: Aurora Integration

1. **Copy `aurora/` package** to `packages/cli/src/aurora_cli/planning/`
2. **Update Aurora imports** to use new planning modules
3. **Run Aurora's full test suite** to ensure no regressions
4. **Update CLAUDE.md** to document new planning commands

---

## Validation Checklist

- [x] All ported tests pass (`pytest tests/ -v`) - **284 tests**
- [x] Type checking passes (`mypy aurora/`) - **0 errors**
- [x] Linting checked (`ruff check aurora/`) - **58 style issues (acceptable)**
- [x] PORT_REPORT.md fully updated with ✅ status
- [x] Ready for integration into Aurora CLI

---

*Working Directory: `/tmp/openspec-source/`*
*Branch: `refactored`*
*Completed: 2026-01-02*
