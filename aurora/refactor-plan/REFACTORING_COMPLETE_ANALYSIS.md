# OpenSpec → Aurora: Complete Refactoring Analysis

**Date**: 2026-01-02
**Purpose**: Comprehensive mapping of ALL OpenSpec functionality for Aurora integration
**Status**: CRITICAL GAPS IDENTIFIED - Additional work required

---

## EXECUTIVE SUMMARY

### What We've Ported (Phases 1-9): ✅ 202 tests passing
- ✅ Schemas (base, plan, capability)
- ✅ Validation (rules, types, validator)
- ✅ Parsers (markdown, requirements, plan_parser)
- ✅ Core Commands (archive, init, list, update, view)
- ✅ CLI Commands (plan_cmd, validate_cmd, capability_cmd)
- ✅ Config (constants, global_config)
- ✅ Configurators (base protocol, registry)
- ✅ Templates (agents, project, claude)
- ✅ Utilities (filesystem, discovery, interactive)

### What We're MISSING (CRITICAL): ❌
1. **Slash Commands System** (~1,800 lines) - BLOCKING for Phase 1
2. **Shell Completions** (~400 lines) - Nice to have
3. **Artifact Workflow Commands** (~550 lines) - Experimental, review needed
4. **Config Management Commands** (~220 lines) - CLI config commands
5. **Show/Spec Commands** (~400 lines) - View commands
6. **Converters (JSON)** (~62 lines) - Format conversion
7. **Styles (Palette)** (~50 lines) - Terminal colors

---

## USER REQUIREMENTS ANALYSIS (6 Critical Points)

### ✅ 1. Phase 1-3 Adaptations from OpenSpec
**Requirement**: Rename structures, add agents.json, adjust templates

**Current Status**:
- ✅ File structure: Can adapt (openspec/ → aurora/, changes/ → plans/, specs/ → capabilities/)
- ❌ agents.json: NOT in OpenSpec, need to design from scratch based on PRD
- ✅ Template adjustments: agents.py template exists, can append agent recommendations

**Action Needed**: Design agents.json schema (not in OpenSpec source)

---

### ❌ 2. Slash Commands - CRITICAL & MISSING
**Requirement**: Replace MCP, slash commands for ALL aur commands

**Current Status**:
- ✅ Base configurator protocol ported
- ✅ Registry ported
- ❌ Slash command template system NOT ported
- ❌ Slash command generators NOT ported
- ❌ Tool-specific configurators NOT ported

**What's in OpenSpec**:
```
src/core/configurators/slash/
├── base.ts (3,257 lines) - SlashCommandConfigurator base class
├── registry.ts (4,065 lines) - SlashCommandRegistry
├── claude.ts (1,176 lines) - Claude Code slash commands
├── opencode.ts (2,800 lines) - OpenCode slash commands
├── qoder.ts (2,618 lines) - Qoder slash commands
└── 21 other tool configurators
```

**Key Functions**:
- `SlashCommandConfigurator.configure()` - Writes `.claude/commands/openspec/*.md` files
- `getFrontmatter()` - YAML frontmatter for slash commands
- `getCommandContent()` - Command template content
- `getRelativePath()` - Tool-specific paths

**What We Need to Port**: (~5,000 lines for 3 tools)
1. ✅ Base protocol (already have)
2. ❌ Slash command template generation system
3. ❌ Claude Code configurator
4. ❌ OpenCode configurator (if needed)
5. ❌ AmpCode configurator (if exists - not in OpenSpec, may need custom)

**Files to Create**:
```python
aurora/configurators/slash/
├── __init__.py
├── base.py                    # SlashCommandConfigurator protocol
├── registry.py                # Command registry
├── claude.py                  # Claude Code: .claude/commands/aur/*.md
├── opencode.py                # OpenCode config
└── ampcode.py                 # AmpCode config (custom)

aurora/templates/slash_commands/
├── __init__.py
├── plan.py                    # /aur:plan template
├── archive.py                 # /aur:archive template
├── implement.py               # /aur:implement template
├── query.py                   # /aur:query template
├── mem.py                     # /aur:mem template
└── index.py                   # /aur:index template
```

---

### ❌ 3. Multi-Tool Configuration
**Requirement**: Configure ALL aur commands for Claude Code, OpenCode, AmpCode

**Commands to Configure**:
- `/aur:plan` - Plan generation (Phase 1)
- `/aur:archive` - Archive plans (Phase 1)
- `/aur:implement` - Execute plans (Phase 3)
- `/aur:query` - Codebase query
- `/aur:mem` - Memory operations
- `/aur:index` - Index codebase
- `/aur:search` - Semantic search

**Current Status**: ❌ None configured yet

---

### ✅ 4. Planning System Differences
**Requirement**: 2-step with pause, streamlined structure, simpler names

**OpenSpec Approach**:
```
openspec/
├── changes/
│   └── my-change/
│       ├── change.md              # Single file with why/what/specs
│       └── specs/                 # Delta specs (added/modified/removed)
└── specs/
    └── my-spec/
        └── spec.md                # Current capability definition
```

**Aurora Approach** (from PRD):
```
~/.aurora/
└── plans/
    ├── active/
    │   └── 0001-oauth-auth/
    │       ├── plan.md            # High-level plan
    │       ├── prd.md             # Expanded PRD (step 2)
    │       ├── tasks.md           # Generated tasks (step 2)
    │       └── agents.json        # Agent delegation info
    └── archive/
        └── 2026-01-15-0001-oauth-auth/
            └── [same 4 files]
```

**Key Differences**:
1. **4 files** vs OpenSpec's 1-2 files
2. **2-step process**: generate plan.md → pause → expand to prd.md + tasks.md
3. **agents.json**: NEW - not in OpenSpec
4. **Simpler names**: plans/ instead of changes/, no delta specs/
5. **Global location**: ~/.aurora/ instead of project ./openspec/

**Action Needed**:
- ✅ Parsers can be adapted (we have markdown parser)
- ❌ Need 2-step workflow implementation
- ❌ Need agents.json generation logic

---

### ⚠️ 5. Execution System
**Requirement**: Start with OpenSpec tasks.md, migrate to SOAR orchestrator

**Phase 1 (Generic)**:
- Parse tasks.md
- Execute tasks sequentially
- Track completion

**Phase 2 (SOAR Integration)**:
- tasks.md → SOAR orchestrator
- Spawn agents for subgoals
- Agent invocation system

**OpenSpec Execution** (from artifact-workflow.ts):
```typescript
// Reads task lists from change.md
// Tracks completion status
// Generates next-step instructions
```

**Current Status**: ❌ Not ported (artifact-workflow is experimental)

**What We Need**:
1. Task parser (parse tasks.md checkboxes)
2. Task executor (run commands/track status)
3. SOAR integration bridge (later)

---

### ❌ 6. Complete Awareness for Integration
**Requirement**: Map EVERY package to avoid missing calls

**This Document Addresses This**: See "Complete Package Mapping" below

---

## COMPLETE PACKAGE MAPPING

### Category 1: CLI Entry Points

#### `src/cli/index.ts` (326 lines)
**Purpose**: Commander.js CLI setup, register all commands

**Key Functions**:
- `program.name('openspec')` - CLI name
- `registerChangeCommands()` - change, show, archive
- `registerSpecCommands()` - spec commands
- `registerValidateCommand()` - validate
- `registerConfigCommand()` - config get/set/list
- `registerCompletionCommand()` - shell completions
- `registerArtifactWorkflowCommands()` - experimental

**Aurora Equivalent**: `aurora_cli/main.py` with Click

**Port Status**: ❌ Not ported (will integrate into Aurora's main.py)

---

### Category 2: Core Commands (src/commands/)

#### `change.ts` (269 lines) → ✅ `commands/archive.py`
**Purpose**: Show, list, archive change proposals

**Key Methods**:
- `show()` - Display change.md
- `list()` - List all changes
- `archive()` - Move to archive/

**Port Status**: ✅ Ported as archive.py (changed API)

---

#### `spec.ts` (231 lines) → ✅ `commands/view.py`, `commands/list.py`
**Purpose**: Show, list capability specs

**Key Methods**:
- `show()` - Display spec.md
- `list()` - List all specs
- `validate()` - Validate spec

**Port Status**: ✅ Ported across view.py and list.py

---

#### `validate.ts` (337 lines) → ✅ `validation/validator.py`
**Purpose**: Validation command orchestration

**Port Status**: ✅ Ported to validator.py + cli/validate_cmd.py

---

#### `config.ts` (220 lines) → ⚠️ PARTIAL `config.py`, `global_config.py`
**Purpose**: Global config management (get/set/list/edit)

**Key Features**:
- `get <key>` - Get config value
- `set <key> <value>` - Set config value
- `list` - List all config
- `edit` - Open editor
- `path` - Show config file path

**Port Status**:
- ✅ Config data structures ported (config.py, global_config.py)
- ❌ Config CLI commands NOT ported (get/set/list/edit)

**Action Needed**: Port config command if needed (or use Click alternatives)

---

#### `completion.ts` (207 lines) → ❌ NOT PORTED
**Purpose**: Install/uninstall shell completions

**Key Features**:
- `install` - Install completions for current shell
- `uninstall` - Remove completions
- Supports: zsh (others planned)

**Depends On**:
- `core/completions/generators/zsh-generator.ts` (283 lines)
- `core/completions/installers/zsh-installer.ts` (383 lines)

**Total Lines**: ~400 lines

**Port Status**: ❌ Not ported (nice-to-have, not critical)

**Action Needed**: Skip for now, add later if needed

---

#### `artifact-workflow.ts` (456 lines) → ❌ NOT PORTED (EXPERIMENTAL)
**Purpose**: Artifact dependency graph workflow commands

**Key Features**:
- `openspec artifact view <change>` - View artifacts in change
- `openspec artifact ready <change>` - Show ready artifacts
- `openspec artifact instruct <change> <artifact>` - Generate instructions
- `openspec artifact schema list` - List schemas
- `openspec artifact schema show <name>` - Show schema

**Comment in File**:
```typescript
/**
 * Artifact Workflow CLI Commands (Experimental)
 *
 * To remove this feature:
 * 1. Delete this file
 * 2. Remove the registerArtifactWorkflowCommands() call
 */
```

**Depends On**:
- `core/artifact-graph/` (entire directory, ~1,469 lines)

**Port Status**: ❌ Not ported

**Action Needed**:
- ⚠️ Evaluate if Aurora needs artifact dependency tracking
- Aurora has SOAR for task/agent dependencies
- Artifact-graph is for file/build artifact dependencies
- **Recommendation**: Skip unless specific use case identified

---

#### `show.ts` (129 lines) → ⚠️ PARTIAL (logic in cli/plan_cmd.py)
**Purpose**: Interactive change/spec selection for show command

**Key Features**:
- No args → interactive picker
- Auto-detect if arg is change or spec
- Fuzzy matching

**Port Status**:
- ✅ Show logic ported to cli/plan_cmd.py
- ❌ Interactive picker NOT ported

**Action Needed**: Add interactive picker if needed (use prompt_toolkit or similar)

---

### Category 3: Core Functionality (src/core/)

#### 3.1 Schemas ✅ COMPLETE
```
schemas/
├── base.schema.ts → schemas/base.py ✅
├── change.schema.ts → schemas/plan.py ✅
└── spec.schema.ts → schemas/capability.py ✅
```

---

#### 3.2 Validation ✅ COMPLETE
```
validation/
├── constants.ts → validation/constants.py ✅
├── types.ts → validation/types.py ✅
└── validator.ts → validation/validator.py ✅
```

---

#### 3.3 Parsers ✅ COMPLETE
```
parsers/
├── markdown.ts → parsers/markdown.py ✅
├── requirements.ts → parsers/requirements.py ✅
└── change-parser.ts → parsers/plan_parser.py ✅
```

---

#### 3.4 Templates ✅ COMPLETE
```
templates/
├── agents-template.ts → templates/agents.py ✅
├── project-template.ts → templates/project.py ✅
├── claude-template.ts → templates/claude.py ✅
└── slash-command-templates.ts → ❌ NOT PORTED
```

**Missing**: `slash-command-templates.ts` (185 lines)

**Purpose**: Templates for slash commands
- proposal template
- apply template
- archive template

**Action Needed**: Port this for slash command system

---

#### 3.5 Configurators ⚠️ PARTIAL
```
configurators/
├── base.ts → configurators/base.py ✅
├── registry.ts → configurators/registry.py ✅
├── claude.ts → ❌ NOT PORTED
├── cline.ts → ❌ NOT PORTED
├── agents.ts → ❌ NOT PORTED
└── slash/ → ❌ ENTIRE DIRECTORY NOT PORTED
    ├── base.ts (3,257 lines)
    ├── registry.ts (4,065 lines)
    ├── claude.ts (1,176 lines)
    ├── opencode.ts (2,800 lines)
    └── 21 other tools
```

**Port Status**:
- ✅ Base protocol and registry ported
- ❌ Individual tool configurators NOT ported
- ❌ Slash command system NOT ported (~12,000 lines total)

**Action Needed**: Port slash command system (CRITICAL)

---

#### 3.6 Converters ❌ NOT PORTED
```
converters/
└── json-converter.ts (62 lines)
```

**Purpose**: Convert between markdown and JSON formats

**Key Methods**:
- `changeToJson()` - Change → JSON
- `specToJson()` - Spec → JSON

**Port Status**: ❌ Not ported

**Action Needed**: Port if JSON output needed (PRD shows `--json` flags)

---

#### 3.7 Styles ❌ NOT PORTED
```
styles/
└── palette.ts (50 lines)
```

**Purpose**: Terminal color definitions

**Port Status**: ❌ Not ported (Python has rich/click.style)

**Action Needed**: Use Python's rich library instead

---

#### 3.8 Completions ❌ NOT PORTED
```
completions/
├── generators/
│   └── zsh-generator.ts (283 lines)
└── installers/
    └── zsh-installer.ts (383 lines)
```

**Purpose**: Generate and install shell completions

**Port Status**: ❌ Not ported

**Action Needed**: Skip for now (Click has built-in completion support)

---

#### 3.9 Artifact Graph ❌ NOT PORTED
```
artifact-graph/
├── graph.ts (287 lines)
├── schema.ts (174 lines)
├── types.ts (94 lines)
├── context.ts (249 lines)
├── instruction-loader.ts (309 lines)
└── index.ts (356 lines)
```

**Total**: ~1,469 lines

**Purpose**: Dependency graph for artifacts, build order tracking

**Port Status**: ❌ Not ported (marked experimental)

**Action Needed**: Evaluate need, likely skip (SOAR handles dependencies)

---

### Category 4: Utilities ✅ MOSTLY COMPLETE

```
utils/
├── file-system.ts → utils/filesystem.py ✅
├── item-discovery.ts → utils/discovery.py ✅
├── interactive.ts → utils/interactive.py ✅
├── change-utils.ts → ⚠️ PARTIAL (some in parsers)
├── match.ts → ❌ NOT PORTED
├── task-progress.ts → ❌ NOT PORTED
└── shell-detection.ts → ❌ NOT PORTED
```

**Missing Utils**:
- `change-utils.ts` (102 lines) - createChange, validateChangeName
- `match.ts` (26 lines) - fuzzy matching for names
- `task-progress.ts` (43 lines) - task list progress tracking
- `shell-detection.ts` (62 lines) - detect user's shell

**Action Needed**: Port if needed (task-progress may be useful)

---

## CRITICAL GAPS SUMMARY

### Must Port Now (Phase 0.5 Extension):

#### 1. Slash Command System (~2,000 lines) - BLOCKING
**Files**:
- `core/configurators/slash/base.ts` → `configurators/slash/base.py`
- `core/configurators/slash/registry.ts` → `configurators/slash/registry.py`
- `core/configurators/slash/claude.ts` → `configurators/slash/claude.py`
- `core/templates/slash-command-templates.ts` → `templates/slash_commands/*.py`

**Why Critical**: User requirement #2 - replace MCP with slash commands

---

#### 2. JSON Converter (~62 lines)
**Files**:
- `core/converters/json-converter.ts` → `converters/json.py`

**Why Needed**: PRD shows `--json` output flags

---

#### 3. Task Progress Tracker (~43 lines)
**Files**:
- `utils/task-progress.ts` → `utils/task_progress.py`

**Why Needed**: Track task completion in tasks.md

---

### Nice to Have (Can Defer):

#### 4. Shell Completions (~400 lines)
- Not critical (Click has built-in support)

#### 5. Config CLI Commands (~220 lines)
- Have config storage, commands can be added later

#### 6. Fuzzy Matching (~26 lines)
- Nice UX improvement, not blocking

---

### Skip (Not Needed):

#### 7. Artifact Graph (~1,469 lines)
- SOAR handles dependencies
- Different use case (file artifacts vs task dependencies)

#### 8. Styles/Palette (~50 lines)
- Use Python's rich library

---

## UPDATED PHASE 0.5 SCOPE

### Current Phases 1-9: ✅ COMPLETE (202 tests)

### NEW: Phase 10 - Slash Commands (CRITICAL)
**Est. Lines**: ~2,000
**Est. Tests**: ~30

**Tasks**:
- [ ] 10.1 Port `src/core/configurators/slash/base.ts` → `aurora/configurators/slash/base.py`
- [ ] 10.2 Port `src/core/configurators/slash/registry.ts` → `aurora/configurators/slash/registry.py`
- [ ] 10.3 Port `src/core/configurators/slash/claude.ts` → `aurora/configurators/slash/claude.py`
- [ ] 10.4 Create Aurora slash command templates (plan, archive, implement, query, mem, index)
- [ ] 10.5 Write tests for slash command generation
- [ ] 10.6 Test `.claude/commands/aur/*.md` file generation

---

### NEW: Phase 11 - Converters & Utils
**Est. Lines**: ~130
**Est. Tests**: ~15

**Tasks**:
- [ ] 11.1 Port `src/core/converters/json-converter.ts` → `aurora/converters/json.py`
- [ ] 11.2 Port `src/utils/task-progress.ts` → `aurora/utils/task_progress.py`
- [ ] 11.3 Port `src/utils/match.ts` → `aurora/utils/match.py` (fuzzy matching)
- [ ] 11.4 Write tests for converters
- [ ] 11.5 Write tests for task progress

---

### Revised Phase 12 - Integration Tests
- [ ] 12.1 Test slash command generation end-to-end
- [ ] 12.2 Test JSON conversion (plan → JSON → plan)
- [ ] 12.3 Test task progress tracking

---

### Revised Phase 13 - Quality Assurance
- [ ] 13.1 Run full test suite: `pytest tests/ -v`
- [ ] 13.2 Check coverage: `pytest --cov=aurora tests/`
- [ ] 13.3 Type check: `mypy aurora/`
- [ ] 13.4 Lint: `ruff check aurora/`

---

### Revised Phase 14 - Finalize
- [ ] 14.1 Update PORT_REPORT.md with all modules
- [ ] 14.2 Create INTEGRATION_GUIDE.md for Aurora package integration
- [ ] 14.3 Commit and push to refactored branch
- [ ] 14.4 Create integration plan for Aurora main repo

---

## INTEGRATION STRATEGY (For Aurora Main Repo)

### Step 1: Copy Refactored Package
```bash
cp -r /tmp/openspec-source/aurora/ \
      /home/hamr/PycharmProjects/aurora/packages/cli/src/aurora_cli/planning/
```

### Step 2: Update Import Paths
```python
# Old (if any exist):
from openspec.schemas import Plan

# New:
from aurora_cli.planning.schemas import Plan
```

### Step 3: Integrate with Existing Commands
```python
# In aurora_cli/main.py
from aurora_cli.planning.commands import PlanCommand
from aurora_cli.planning.configurators.slash.claude import ClaudeSlashCommandConfigurator

@cli.group()
def plan():
    """Planning system commands."""
    pass

@plan.command()
def create():
    """Create a new plan."""
    # Use PlanCommand from refactored code
```

### Step 4: Configure Slash Commands
```python
# During aur init or aur config init
configurator = ClaudeSlashCommandConfigurator()
configurator.configure(
    project_path=os.getcwd(),
    aurora_dir=get_aurora_dir(),
    commands=['plan', 'archive', 'implement', 'query', 'mem', 'index']
)
```

### Step 5: Test Integration
```bash
# Test planning system
aur plan create "Add OAuth authentication"
aur plan list
aur plan show 0001

# Test slash commands
# In Claude Code:
/aur:plan Add OAuth authentication
/aur:archive 0001
```

---

## CRITICAL CALLS TO NOT MISS

### From Parsers:
```python
# markdown.py
parse_capability(content: str) -> ParsedCapability
parse_plan(content: str) -> ParsedPlan

# requirements.py
parse_modification_spec(content: str) -> List[ParsedModification]
extract_requirements_section(content: str) -> str

# plan_parser.py
parse_plan_with_modifications(plan_dir: Path) -> Tuple[ParsedPlan, List[ParsedModification]]
```

### From Validation:
```python
# validator.py
validate_capability(capability_path: Path, strict_mode: bool = False) -> ValidationReport
validate_plan(plan_path: Path, strict_mode: bool = False) -> ValidationReport
validate_plan_modification_specs(plan_dir: Path, strict_mode: bool = False) -> ValidationReport
```

### From Commands:
```python
# archive.py
archive_plan(plan_name: str, skip_validation: bool = False, skip_specs: bool = False) -> str

# list.py
list_plans(json_output: bool = False, specs_mode: bool = False) -> str

# init.py
init_aurora_directory(target_path: str, ai_tools: List[str], extend: bool = False) -> None
```

### From Configurators:
```python
# registry.py
ToolRegistry.register(tool: ToolConfigurator) -> None
ToolRegistry.get(tool_id: str) -> Optional[ToolConfigurator]
ToolRegistry.get_available() -> List[ToolConfigurator]

# slash/claude.py (TO BE PORTED)
ClaudeSlashCommandConfigurator.configure(project_path: str, aurora_dir: str, commands: List[str]) -> None
```

---

## DELIVERABLES FOR PHASE 0.5 COMPLETION

1. ✅ **Phases 1-9**: Core functionality (202 tests passing)
2. ❌ **Phase 10**: Slash command system (~30 tests)
3. ❌ **Phase 11**: Converters & utils (~15 tests)
4. ❌ **Phase 12-14**: Integration tests, QA, finalization

**Total Tests Target**: ~247 tests (currently at 202)

---

## FILES TO CREATE (Phase 10-11)

```
aurora/
├── configurators/
│   └── slash/
│       ├── __init__.py
│       ├── base.py                    # SlashCommandConfigurator protocol
│       ├── registry.py                # Slash command registry
│       ├── claude.py                  # Claude Code configurator
│       ├── opencode.py                # OpenCode configurator
│       └── ampcode.py                 # AmpCode configurator (custom)
├── templates/
│   └── slash_commands/
│       ├── __init__.py
│       ├── plan.py                    # /aur:plan template
│       ├── archive.py                 # /aur:archive template
│       ├── implement.py               # /aur:implement template
│       ├── query.py                   # /aur:query template
│       ├── mem.py                     # /aur:mem template
│       └── index.py                   # /aur:index template
├── converters/
│   ├── __init__.py
│   └── json.py                        # JSON converter
└── utils/
    ├── task_progress.py               # Task completion tracking
    └── match.py                       # Fuzzy matching

tests/unit/
├── configurators/
│   └── slash/
│       ├── test_base.py
│       ├── test_registry.py
│       └── test_claude.py
├── templates/
│   └── slash_commands/
│       └── test_templates.py
├── converters/
│   └── test_json.py
└── utils/
    ├── test_task_progress.py
    └── test_match.py
```

---

## CONCLUSION

**Current Status**: Phase 0.5 is 75% complete (9/13 phases)

**Critical Gaps Identified**:
1. Slash command system (BLOCKING for Phase 1)
2. JSON converter (needed for --json flags)
3. Task progress tracker (needed for execution)

**Recommendation**:
1. Complete Phases 10-11 now (slash commands + converters)
2. Then proceed to integration planning
3. Update PRD Phase 0.5 task list with new phases

**Est. Additional Work**: ~2,130 lines, ~45 tests, ~2-3 days
