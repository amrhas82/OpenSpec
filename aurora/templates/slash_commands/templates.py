"""Template bodies for Aurora slash commands.

Each template provides instructions for AI coding tools on how to execute
the corresponding Aurora command.
"""

from typing import Dict

# Base guardrails for all commands
BASE_GUARDRAILS = """**Guardrails**
- Favor straightforward, minimal implementations first and add complexity only when requested or clearly required.
- Keep changes tightly scoped to the requested outcome.
- Refer to `aurora/AGENTS.md` if you need additional Aurora conventions or clarifications."""

# /aur:plan - Plan generation command
PLAN_TEMPLATE = f"""{BASE_GUARDRAILS}
- Identify any vague or ambiguous details and ask the necessary follow-up questions before creating the plan.
- Do not write any code during planning. Only create design documents (plan.md, prd.md, tasks.md, agents.json).

**Steps**
1. Review existing plans with `aur plan list` and codebase context to ground the plan in current behavior.
2. Choose a unique descriptive plan ID (e.g., "0001-oauth-auth") and create plan.md with high-level overview.
3. If user confirms, expand to prd.md with detailed requirements and acceptance criteria.
4. Generate tasks.md with ordered, verifiable work items that deliver incremental progress.
5. Create agents.json with subgoals and agent recommendations using `aur agents search`.
6. Validate with `aur plan show <id>` before sharing the plan.

**Reference**
- Use `aur plan list` to see existing plans
- Use `aur agents list` to see available agents
- Search codebase with memory system: `aur query <question>`"""

# /aur:archive - Archive completed plans
ARCHIVE_TEMPLATE = f"""{BASE_GUARDRAILS}

**Steps**
1. Determine the plan ID to archive:
   - If already specified in conversation, use that value after trimming whitespace.
   - If referenced loosely, run `aur plan list` to find candidates and confirm with user.
   - Otherwise, ask user which plan to archive and wait for confirmation.
2. Validate plan exists by running `aur plan list` or `aur plan show <id>`.
3. Run `aur plan archive <id>` to move plan to archive with timestamp.
4. Verify output confirms successful archival.

**Reference**
- Use `aur plan list` to confirm plan IDs before archiving
- Use `aur plan list --archived` to view archived plans"""

# /aur:implement - Execute plan with agents
IMPLEMENT_TEMPLATE = f"""{BASE_GUARDRAILS}

**Steps**
Track these steps as TODOs and complete them one by one.
1. Read plan.md, prd.md, and tasks.md to confirm scope and acceptance criteria.
2. Work through tasks sequentially from tasks.md, keeping edits minimal and focused.
3. For each subgoal in agents.json, consider delegating to the recommended agent.
4. Confirm completion before updating statuses—ensure every item is finished.
5. Update task checkboxes as work progresses so status reflects reality.

**Reference**
- Use `aur plan show <id>` for plan details
- Use `aur agents show <agent-id>` for agent capabilities"""

# /aur:query - Codebase query with memory
QUERY_TEMPLATE = f"""{BASE_GUARDRAILS}

**Usage**
Run `aur query "<your question>"` to search the codebase using Aurora's memory system.

**Features**
- Semantic search across indexed code
- Hybrid BM25 + embedding search
- Context-aware results with file paths and line numbers
- Automatic quality scoring (groundedness)

**Reference**
- Use `aur mem index` to index the codebase first
- Use `aur query --context file.py` to add specific files as context"""

# /aur:mem - Memory operations
MEM_TEMPLATE = f"""{BASE_GUARDRAILS}

**Commands**
- `aur mem index <path>` - Index codebase for semantic search
- `aur mem search "<query>"` - Search indexed code
- `aur mem status` - Show memory system status

**Reference**
- Index before querying: `aur mem index .`
- Search is fast: uses hybrid BM25 + embeddings"""

# /aur:index - Index codebase (alias for mem index)
INDEX_TEMPLATE = f"""{BASE_GUARDRAILS}

**Usage**
Run `aur index <path>` to index codebase for semantic search.

This is an alias for `aur mem index <path>`.

**Reference**
- Indexes Python files by default
- Creates chunks for semantic search
- Enables `aur query` functionality"""

# /aur:search - Search indexed code (alias for mem search)
SEARCH_TEMPLATE = f"""{BASE_GUARDRAILS}

**Usage**
Run `aur search "<query>"` to search indexed code.

This is an alias for `aur mem search "<query>"`.

**Reference**
- Returns file paths and line numbers
- Uses hybrid BM25 + embedding search
- Shows match scores"""

# Command templates dictionary
COMMAND_TEMPLATES: Dict[str, str] = {
    "plan": PLAN_TEMPLATE,
    "archive": ARCHIVE_TEMPLATE,
    "implement": IMPLEMENT_TEMPLATE,
    "query": QUERY_TEMPLATE,
    "mem": MEM_TEMPLATE,
    "index": INDEX_TEMPLATE,
    "search": SEARCH_TEMPLATE,
}


def get_command_body(command_id: str) -> str:
    """Get the template body for a command.

    Args:
        command_id: Command identifier (e.g., "plan", "archive")

    Returns:
        Template body string

    Raises:
        KeyError: If command_id is not found
    """
    if command_id not in COMMAND_TEMPLATES:
        raise KeyError(f"Unknown command: {command_id}")

    return COMMAND_TEMPLATES[command_id]
