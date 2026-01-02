# OpenSpec → Aurora: Complete File-to-File Mapping

## Package-to-Package Mapping

| OpenSpec Package | Aurora Package | Purpose |
|------------------|----------------|---------|
| `src/core/schemas/` | `aurora/schemas/` | Data models (Pydantic) |
| `src/core/validation/` | `aurora/validation/` | Validation rules |
| `src/core/parsers/` | `aurora/parsers/` | Markdown parsing |
| `src/core/` (commands) | `aurora/commands/` | Core command logic |
| `src/commands/` | `aurora/cli/` | CLI wrappers |
| `src/core/config*.ts` | `aurora/config.py`, `aurora/global_config.py` | Configuration |
| `src/core/configurators/` | `aurora/configurators/` | Tool detection |
| `src/core/configurators/slash/` | `aurora/configurators/slash/` | Slash commands |
| `src/core/templates/` | `aurora/templates/` | Templates |
| `src/core/converters/` | `aurora/converters/` | Format conversion |
| `src/utils/` | `aurora/utils/` | Utilities |

---

## Complete File-to-File Mapping

### Schemas (Phase 1) - 3 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/schemas/base.schema.ts` | `aurora/schemas/base.py` | `Scenario`, `Requirement` |
| `src/core/schemas/change.schema.ts` | `aurora/schemas/plan.py` | `ModificationOperation`, `Modification`, `Plan`, `RenameInfo` |
| `src/core/schemas/spec.schema.ts` | `aurora/schemas/capability.py` | `Capability`, `CapabilityMetadata` |

### Validation (Phase 2) - 3 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/validation/constants.ts` | `aurora/validation/constants.py` | `VALIDATION_MESSAGES`, thresholds |
| `src/core/validation/types.ts` | `aurora/validation/types.py` | `ValidationLevel`, `ValidationIssue`, `ValidationReport` |
| `src/core/validation/validator.ts` | `aurora/validation/validator.py` | `Validator` class |

### Parsers (Phase 3) - 3 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/parsers/markdown-parser.ts` | `aurora/parsers/markdown.py` | `MarkdownParser`, `ParsedCapability`, `ParsedPlan`, etc. |
| `src/core/parsers/change-parser.ts` | `aurora/parsers/plan_parser.py` | `PlanParser` |
| `src/core/parsers/requirement-blocks.ts` | `aurora/parsers/requirements.py` | `parse_modification_spec()`, `RequirementBlock`, `ModificationPlan` |

### Core Commands (Phase 4) - 5 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/archive.ts` | `aurora/commands/archive.py` | `ArchiveCommand` |
| `src/core/init.ts` | `aurora/commands/init.py` | `InitCommand` |
| `src/core/list.ts` | `aurora/commands/list.py` | `ListCommand` |
| `src/core/view.ts` | `aurora/commands/view.py` | `ViewCommand` |
| `src/core/update.ts` | `aurora/commands/update.py` | `UpdateCommand` |

### CLI Commands (Phase 5) - 3 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/commands/change.ts` | `aurora/cli/plan_cmd.py` | `PlanCommand` |
| `src/commands/validate.ts` | `aurora/cli/validate_cmd.py` | `ValidateCommand` |
| `src/commands/spec.ts` | `aurora/cli/capability_cmd.py` | `CapabilityCommand` |

### Config (Phase 6) - 2 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/config.ts` | `aurora/config.py` | `AURORA_MARKERS`, `AI_TOOLS` |
| `src/core/global-config.ts` | `aurora/global_config.py` | `get_global_config()`, `save_global_config()` |

### Configurators (Phase 7) - 2 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/configurators/base.ts` | `aurora/configurators/base.py` | `ToolConfigurator` (Protocol) |
| `src/core/configurators/registry.ts` | `aurora/configurators/registry.py` | `ToolRegistry` |

### Templates (Phase 8) - 3 files

| TypeScript Source | Python Target | Content |
|-------------------|---------------|---------|
| `src/core/templates/agents-template.ts` | `aurora/templates/agents.py` | `AGENTS_TEMPLATE` (457 lines) |
| `src/core/templates/project-template.ts` | `aurora/templates/project.py` | `PROJECT_TEMPLATE` |
| `src/core/templates/claude-template.ts` | `aurora/templates/claude.py` | `CLAUDE_TEMPLATE` |

### Utilities (Phase 9) - 3 files

| TypeScript Source | Python Target | Functions |
|-------------------|---------------|-----------|
| `src/utils/file-system.ts` | `aurora/utils/filesystem.py` | `find_project_root()`, `read_markdown_file()` |
| `src/utils/item-discovery.ts` | `aurora/utils/discovery.py` | `get_active_plan_ids()`, `get_capability_ids()` |
| `src/utils/interactive.ts` | `aurora/utils/interactive.py` | `is_interactive()` |

### Slash Commands (Phase 10) - 4 files

| TypeScript Source | Python Target | Classes/Functions |
|-------------------|---------------|-------------------|
| `src/core/configurators/slash/base.ts` | `aurora/configurators/slash/base.py` | `SlashCommandConfigurator` (Protocol) |
| `src/core/configurators/slash/registry.ts` | `aurora/configurators/slash/registry.py` | `SlashCommandRegistry` |
| `src/core/configurators/slash/claude.ts` | `aurora/configurators/slash/claude.py` | `ClaudeCodeConfigurator` |
| `src/core/configurators/slash/opencode.ts` | `aurora/configurators/slash/opencode.py` | `OpenCodeConfigurator` |
| `src/core/templates/slash-command-templates.ts` | `aurora/templates/slash_commands/templates.py` | 7 command templates |

### Converters & Utils (Phase 11) - 3 files

| TypeScript Source | Python Target | Functions |
|-------------------|---------------|-----------|
| `src/core/converters/json-converter.ts` | `aurora/converters/json.py` | `plan_to_json()`, `capability_to_json()` |
| `src/utils/task-progress.ts` | `aurora/utils/task_progress.py` | `count_tasks()`, `format_task_status()` |
| `src/utils/match.ts` | `aurora/utils/match.py` | `levenshtein()`, `nearest_matches()` |

---

## Skipped Files (with reason)

| TypeScript Source | Reason |
|-------------------|--------|
| `src/core/completions/**` (~1,537 lines) | Use Click's built-in shell completions |
| `src/core/artifact-graph/**` (~1,469 lines) | Aurora has SOAR for dependency tracking |
| `src/cli/index.ts` (326 lines) | Integrate into Aurora's existing main.py |
| `src/core/styles/**` (~50 lines) | Use Python's rich library |
| `src/commands/config.ts` (~220 lines) | Lower priority, Click alternatives exist |
| `src/commands/show.ts` (~138 lines) | Functionality in other commands |

---

## Function Name Mappings

### Validation
| TypeScript | Python |
|------------|--------|
| `validateSpec()` | `validate_capability()` |
| `validateChange()` | `validate_plan()` |
| `validateChangeDeltaSpecs()` | `validate_plan_modification_specs()` |
| `applySpecRules()` | `_apply_capability_rules()` |
| `applyChangeRules()` | `_apply_plan_rules()` |

### Parsers
| TypeScript | Python |
|------------|--------|
| `parseDeltaSpec()` | `parse_modification_spec()` |
| `extractRequirementsSection()` | `extract_requirements_section()` |
| `normalizeRequirementName()` | `normalize_requirement_name()` |

### Config
| TypeScript | Python |
|------------|--------|
| `getGlobalConfigDir()` | `get_global_config_dir()` |
| `getGlobalDataDir()` | `get_global_data_dir()` |
| `getGlobalConfig()` | `get_global_config()` |
| `saveGlobalConfig()` | `save_global_config()` |

### Utils
| TypeScript | Python |
|------------|--------|
| `findProjectRoot()` | `find_project_root()` |
| `readMarkdownFile()` | `read_markdown_file()` |
| `getActiveChangeIds()` | `get_active_plan_ids()` |
| `getSpecIds()` | `get_capability_ids()` |
| `nearestMatches()` | `nearest_matches()` |
| `isInteractive()` | `is_interactive()` |

---

## Directory Structure Comparison

### TypeScript (OpenSpec)
```
src/
├── cli/index.ts                    # Entry point
├── commands/                       # CLI wrappers
│   ├── change.ts
│   ├── spec.ts
│   └── validate.ts
├── core/
│   ├── archive.ts                  # Core commands
│   ├── init.ts
│   ├── list.ts
│   ├── view.ts
│   ├── update.ts
│   ├── config.ts
│   ├── global-config.ts
│   ├── schemas/
│   ├── validation/
│   ├── parsers/
│   ├── configurators/
│   │   └── slash/
│   ├── templates/
│   └── converters/
└── utils/
```

### Python (Aurora)
```
aurora/
├── __init__.py
├── config.py                       # Config constants
├── global_config.py                # Global config management
├── schemas/
│   ├── base.py
│   ├── plan.py
│   └── capability.py
├── validation/
│   ├── constants.py
│   ├── types.py
│   └── validator.py
├── parsers/
│   ├── markdown.py
│   ├── plan_parser.py
│   └── requirements.py
├── commands/
│   ├── archive.py
│   ├── init.py
│   ├── list.py
│   ├── view.py
│   └── update.py
├── cli/
│   ├── plan_cmd.py
│   ├── capability_cmd.py
│   └── validate_cmd.py
├── configurators/
│   ├── base.py
│   ├── registry.py
│   └── slash/
│       ├── base.py
│       ├── registry.py
│       ├── claude.py
│       └── opencode.py
├── templates/
│   ├── agents.py
│   ├── project.py
│   ├── claude.py
│   └── slash_commands/
│       └── templates.py
├── converters/
│   └── json.py
└── utils/
    ├── filesystem.py
    ├── discovery.py
    ├── interactive.py
    ├── task_progress.py
    └── match.py
```

---

## Test Mapping

| TypeScript Test | Python Test | Tests |
|-----------------|-------------|-------|
| `test/core/validation.test.ts` | `tests/unit/validation/test_validator.py` | 15 |
| `test/core/parsers/*.test.ts` | `tests/unit/parsers/test_*.py` | 36 |
| `test/core/archive.test.ts` | `tests/unit/commands/test_archive.py` | 20 |
| `test/core/init.test.ts` | `tests/unit/commands/test_init.py` | 8 |
| `test/core/list.test.ts` | `tests/unit/commands/test_list.py` | 13 |
| `test/core/view.test.ts` | `tests/unit/commands/test_view.py` | 2 |
| `test/core/update.test.ts` | `tests/unit/commands/test_update.py` | 6 |
| `test/commands/*.test.ts` | `tests/unit/cli/test_*_cmd.py` | 20 |
| `test/cli-e2e/*.test.ts` | `tests/integration/test_cli_e2e.py` | 7 |
| N/A (new) | `tests/unit/configurators/slash/test_*.py` | 29 |
| N/A (new) | `tests/integration/test_slash_commands.py` | 11 |
| N/A (new) | `tests/integration/test_json_conversion.py` | 10 |

**Total: 284 tests**
