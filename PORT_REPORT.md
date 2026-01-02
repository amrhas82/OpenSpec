# OpenSpec → Aurora Port Report

**Source**: OpenSpec v0.17.2 (https://github.com/Fission-AI/OpenSpec)
**Fork**: https://github.com/amrhas82/OpenSpec
**Branch**: `refactored`
**Target**: Aurora Planning System (Python)
**Started**: 2026-01-02

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total OpenSpec Lines | 11,396 (source) + 12,053 (tests) = 23,449 |
| Lines to Port | ~4,600 (source) + ~5,000 (tests) = ~9,600 |
| Lines Skipped | ~6,800 (source) + ~7,000 (tests) = ~13,800 |
| Port Percentage | ~41% |

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

---

## Stack Translation

| TypeScript/Node | Python | Notes |
|-----------------|--------|-------|
| Zod | Pydantic | Schema validation |
| Commander.js | Click | CLI framework |
| Inquirer.js | Rich.prompt | Interactive prompts |
| Chalk | Rich.console | Terminal colors |
| fs/path | pathlib | File system |
| vitest | pytest | Testing |
| async/await | async/await | Same pattern |

---

## Ported Modules

### ✅ Core Validation (CRITICAL)

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/validation/validator.ts` | 449 | `aurora/validation/validator.py` | 🔲 TODO |
| `src/core/validation/constants.ts` | 48 | `aurora/validation/constants.py` | 🔲 TODO |
| `src/core/validation/types.ts` | 18 | `aurora/validation/types.py` | 🔲 TODO |

**Key Functions to Port:**
- `validateSpec()` → `validate_capability()`
- `validateChange()` → `validate_plan()`
- `validateChangeDeltaSpecs()` → `validate_plan_delta_specs()`
- `applySpecRules()` → `_apply_capability_rules()`
- `applyChangeRules()` → `_apply_plan_rules()`
- `extractRequirementText()` → `_extract_requirement_text()`
- `containsShallOrMust()` → `_contains_shall_or_must()`
- `countScenarios()` → `_count_scenarios()`

### ✅ Parsers (CRITICAL)

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/parsers/markdown-parser.ts` | 236 | `aurora/parsers/markdown.py` | 🔲 TODO |
| `src/core/parsers/change-parser.ts` | 233 | `aurora/parsers/plan.py` | 🔲 TODO |
| `src/core/parsers/requirement-blocks.ts` | 234 | `aurora/parsers/requirements.py` | 🔲 TODO |

**Key Functions to Port:**
- `MarkdownParser` class → `MarkdownParser` class
- `parseDeltaSpec()` → `parse_delta_spec()`
- `extractRequirementsSection()` → `extract_requirements_section()`
- `normalizeRequirementName()` → `normalize_requirement_name()`

### ✅ Schemas

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/schemas/base.schema.ts` | 19 | `aurora/schemas/base.py` | 🔲 TODO |
| `src/core/schemas/change.schema.ts` | 41 | `aurora/schemas/plan.py` | 🔲 TODO |
| `src/core/schemas/spec.schema.ts` | 16 | `aurora/schemas/capability.py` | 🔲 TODO |

**Zod → Pydantic Mapping:**
```typescript
// TypeScript (Zod)
const ScenarioSchema = z.object({
  rawText: z.string().min(1, VALIDATION_MESSAGES.SCENARIO_EMPTY),
});
```
```python
# Python (Pydantic)
class Scenario(BaseModel):
    raw_text: str = Field(min_length=1)
```

### ✅ Commands

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/archive.ts` | 625 | `aurora/archive.py` | 🔲 TODO |
| `src/core/init.ts` | 986 | `aurora/init.py` | 🔲 TODO |
| `src/core/list.ts` | 193 | `aurora/list.py` | 🔲 TODO |
| `src/core/view.ts` | 218 | `aurora/view.py` | 🔲 TODO |
| `src/core/update.ts` | 129 | `aurora/update.py` | 🔲 TODO |

### ✅ Configurators (Tool Discovery)

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/configurators/registry.ts` | 49 | `aurora/configurators/registry.py` | 🔲 TODO |
| `src/core/configurators/base.ts` | 5 | `aurora/configurators/base.py` | 🔲 TODO |
| `src/core/configurators/claude.ts` | 22 | `aurora/configurators/claude.py` | 🔲 TODO |
| `src/core/configurators/cline.ts` | 23 | `aurora/configurators/cline.py` | 🔲 TODO |
| `src/core/configurators/agents.ts` | 23 | `aurora/configurators/agents.py` | 🔲 TODO |
| Other configurators... | ~200 | `aurora/configurators/*.py` | 🔲 TODO |

**Supported AI Tools (20+):**
- Amazon Q Developer
- Antigravity
- Auggie (Augment CLI)
- Claude Code
- Cline
- Codex
- CodeBuddy
- CoStrict
- Crush
- Cursor
- Factory Droid
- Gemini CLI
- GitHub Copilot
- iFlow
- Kilo Code
- OpenCode
- Qoder
- Qwen Code
- RooCode
- Windsurf
- AGENTS.md standard

### ✅ Templates

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/core/templates/agents-template.ts` | 457 | `aurora/templates/agents.py` | 🔲 TODO |
| `src/core/templates/project-template.ts` | 37 | `aurora/templates/project.py` | 🔲 TODO |
| `src/core/templates/claude-template.ts` | 1 | `aurora/templates/claude.py` | 🔲 TODO |
| `src/core/templates/cline-template.ts` | 1 | `aurora/templates/cline.py` | 🔲 TODO |

### ✅ Utilities

| Source File | Lines | Target File | Status |
|-------------|-------|-------------|--------|
| `src/utils/file-system.ts` | 209 | `aurora/utils/filesystem.py` | 🔲 TODO |
| `src/utils/task-progress.ts` | 43 | `aurora/utils/progress.py` | 🔲 TODO |
| `src/utils/item-discovery.ts` | 66 | `aurora/utils/discovery.py` | 🔲 TODO |
| `src/utils/change-utils.ts` | 102 | `aurora/utils/plan_utils.py` | 🔲 TODO |
| `src/core/converters/json-converter.ts` | 62 | `aurora/converters/json.py` | 🔲 TODO |
| `src/core/config.ts` | 41 | `aurora/config.py` | 🔲 TODO |

---

## Skipped Modules

### ❌ Completions (Use Click Instead)

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/completions/command-registry.ts` | 364 | Click has built-in completions |
| `src/core/completions/completion-provider.ts` | 128 | Click handles this |
| `src/core/completions/factory.ts` | 74 | Not needed |
| `src/core/completions/types.ts` | 90 | Not needed |
| `src/core/completions/generators/zsh-generator.ts` | 374 | Click provides this |
| `src/core/completions/installers/zsh-installer.ts` | 507 | Click provides this |
| **Total** | **~1,537** | |

**Rationale:** Click provides shell completion for bash, zsh, and fish out of the box. OpenSpec's custom completion system is over-engineered for our needs.

### ❌ Artifact Graph (Experimental)

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/artifact-graph/graph.ts` | 167 | Experimental feature |
| `src/core/artifact-graph/index.ts` | 42 | Not in core scope |
| `src/core/artifact-graph/instruction-loader.ts` | 285 | Complex, revisit later |
| `src/core/artifact-graph/resolver.ts` | 158 | Not needed now |
| `src/core/artifact-graph/schema.ts` | 124 | Not needed now |
| `src/core/artifact-graph/state.ts` | 64 | Not needed now |
| `src/core/artifact-graph/types.ts` | 34 | Not needed now |
| `src/commands/artifact-workflow.ts` | 595 | Experimental command |
| **Total** | **~1,469** | |

**Rationale:** Artifact-graph is a workflow orchestration system that's still experimental. Aurora has its own SOAR-based decomposition. May revisit later if useful.

### ❌ CLI Entry Point (Integrate into Aurora)

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/cli/index.ts` | 326 | Aurora has own main.py |

**Rationale:** Aurora already has a CLI structure. We'll integrate commands into `aurora_cli/commands/`, not create a separate CLI.

### ❌ Slash Command Configurators (Tool-Specific)

| Source File | Lines | Reason |
|-------------|-------|--------|
| `src/core/configurators/slash/*.ts` | ~1,500 | Very tool-specific |

**Rationale:** These configure slash commands for specific tools (Claude, Cline, etc.). May port later if needed for Aurora's tool integration.

---

## Tests Ported

### ✅ Tests to Port

| Test File | Lines | Status |
|-----------|-------|--------|
| `test/core/validation.test.ts` | ~500 | 🔲 TODO |
| `test/core/parsers/markdown-parser.test.ts` | ~300 | 🔲 TODO |
| `test/core/archive.test.ts` | ~400 | 🔲 TODO |
| `test/core/init.test.ts` | ~300 | 🔲 TODO |
| `test/core/list.test.ts` | ~200 | 🔲 TODO |
| `test/core/view.test.ts` | ~200 | 🔲 TODO |
| `test/core/config-schema.test.ts` | ~200 | 🔲 TODO |
| `test/core/global-config.test.ts` | ~200 | 🔲 TODO |
| `test/core/update.test.ts` | ~200 | 🔲 TODO |
| `test/core/converters/*.test.ts` | ~150 | 🔲 TODO |
| `test/utils/*.test.ts` | ~300 | 🔲 TODO |
| `test/commands/*.test.ts` | ~500 | 🔲 TODO |
| `test/cli-e2e/basic.test.ts` | ~300 | 🔲 TODO |

### ❌ Tests Skipped

| Test File | Lines | Reason |
|-----------|-------|--------|
| `test/core/completions/*.test.ts` | ~1,000 | Completions skipped |
| `test/core/artifact-graph/*.test.ts` | ~1,500 | Artifact-graph skipped |

---

## Fixtures Used

### ✅ Fixtures to Use

| Fixture | Purpose |
|---------|---------|
| `test/fixtures/` | Test data directory |
| `openspec/specs/` | 20 real spec examples (dogfooding) |
| `openspec/changes/` | Real change examples |

---

## Port Progress

### Phase 0.5.1: Setup (Current)
- [x] Fork OpenSpec repo
- [x] Create `refactored` branch
- [x] Create PORT_REPORT.md
- [ ] Create Python package structure

### Phase 0.5.2: Schemas (TDD)
- [ ] Port tests for schemas
- [ ] Implement Pydantic models

### Phase 0.5.3: Validation (TDD)
- [ ] Port tests for validation
- [ ] Implement Validator class

### Phase 0.5.4: Parsers (TDD)
- [ ] Port tests for parsers
- [ ] Implement MarkdownParser, PlanParser, RequirementsParser

### Phase 0.5.5: Commands (TDD)
- [ ] Port tests for commands
- [ ] Implement archive, init, list, view, update

### Phase 0.5.6: Configurators
- [ ] Port tool registry
- [ ] Port individual configurators

### Phase 0.5.7: Templates
- [ ] Port template generation

### Phase 0.5.8: Integration
- [ ] Integrate into Aurora's planning module
- [ ] Replace old Phase 1 code

---

## Validation Checklist

Before declaring port complete:

- [ ] All ported tests pass (`pytest`)
- [ ] Type checking passes (`mypy`)
- [ ] Linting passes (`ruff`)
- [ ] Behavior matches OpenSpec for key operations:
  - [ ] `aurora plan init` ≈ `openspec init`
  - [ ] `aurora plan list` ≈ `openspec list`
  - [ ] `aurora plan validate` ≈ `openspec validate`
  - [ ] `aurora plan archive` ≈ `openspec archive`
- [ ] Documentation updated

---

## Notes

- **TDD Approach**: Write Python tests first (based on TypeScript tests), then implement
- **Reference**: Keep `main` branch as untouched OpenSpec reference
- **This Branch**: `refactored` contains all Aurora port work
- **Next Phase**: After port complete, integrate into `aurora_cli/planning/`

---

*Last Updated: 2026-01-02*
