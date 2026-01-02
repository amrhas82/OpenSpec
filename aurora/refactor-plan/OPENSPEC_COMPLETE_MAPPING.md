# OpenSpec Complete Mapping - Every Package Explained

**Purpose**: Comprehensive understanding of ALL OpenSpec functionality to ensure nothing is missed during Aurora integration.

**Date**: 2026-01-02
**Source**: OpenSpec TypeScript codebase (92 .ts files)
**Target**: Aurora Python planning system

---

## CRITICAL USER REQUIREMENTS (6 Points)

### 1. Phase 1-3 Adaptations from OpenSpec
- **agents.json**: NEW file format for agent delegation (not in OpenSpec)
- **File structure changes**: Rename openspec/ → aurora/, changes/ → plans/, specs/ → capabilities/
- **Template format changes**: Append agent recommendations to markdown templates

### 2. Slash Commands - CRITICAL & MISSING
- **Current status**: ❌ NOT ported
- **Required for**: ALL aur commands (query, mem, index, search, plan, archive)
- **MCP consolidation**: Replace failed MCP with slash commands
- **Tools**: Claude Code, OpenCode, AmpCode configurators needed

### 3. Multi-Tool Configuration
- **Scope**: Configure slash commands for ALL CLI AI agents
- **Tools**: Claude Code, OpenCode, AmpCode (primary focus)
- **Commands to configure**: aur query, mem, index, search, plan, archive, implement

### 4. Planning System Differences
- **Aurora approach**: Plan decomposition + agent discovery + memory retrieval
- **OpenSpec approach**: Single-step plan generation
- **Aurora changes**: 2-step with pause (generate → review → expand)
- **Directory structure**: Streamlined, simpler names, consolidated docs

### 5. Execution System
- **Phase 1**: Generic execution from tasks.md (from OpenSpec)
- **Phase 2**: SOAR orchestrator spawning agents for subgoals
- **Integration point**: tasks.md → SOAR orchestrator → agent invocation

### 6. Complete Refactoring Awareness
- **Need**: MD document mapping EVERY package
- **Purpose**: Don't miss any calls when building aurora-planning package
- **This document**: Serves that purpose

---

## DIRECTORY STRUCTURE ANALYSIS

```
src/
├── cli/                          [CLI Entry Points]
├── commands/                     [Core Commands Implementation]
├── core/                         [Core Functionality]
│   ├── artifact-graph/          [Dependency Tracking]
│   ├── completions/             [Shell Completions]
│   │   ├── generators/          [Generate completion scripts]
│   │   └── installers/          [Install completions]
│   ├── configurators/           [Tool Detection & Config]
│   │   └── slash/               [Slash Command Configurators]
│   ├── converters/              [Format Converters]
│   ├── parsers/                 [Markdown Parsers]
│   ├── schemas/                 [Data Schemas]
│   ├── styles/                  [Output Styling]
│   ├── templates/               [File Templates]
│   └── validation/              [Validation Rules]
└── utils/                        [Utilities]
```

---

## PACKAGE-BY-PACKAGE ANALYSIS

