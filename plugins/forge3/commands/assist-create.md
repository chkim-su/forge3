---
name: assist:create
description: Create plugin component files using multi-agent workflow
allowed-tools:
  - Task
  - mcp__workflow__workflow_transition
argument-hint: "<component description or plan reference>"
---

# /assist:create

Create plugin component files based on a plan or description.

## Critical Rule

**YOU MUST SPAWN AGENTS using the Task tool. DO NOT do agent work directly.**

The main LLM's only job is to:
1. Spawn the right agent for each phase
2. Pass context between phases
3. Call workflow transitions
4. Report final results to the user

## Workflow Phases

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Discovery | discovery-agent | Find plugin location, existing patterns |
| 2. Semantic | semantic-agent | Plan the implementation structure |
| 3. Execute | execute-agent | Create the actual files |
| 4. Schema-check | schema-check-agent | Validate created files |

## Phase Execution Instructions

### Phase 1: Discovery

**Start by spawning the discovery-agent:**

```
Task(
  subagent_type: "forge3:discovery-agent"
  prompt: "Find the plugin location and existing component patterns for creating: <USER_REQUEST>"
  description: "Discovering plugin structure"
  model: "haiku"
)
```

The discovery-agent will return:
- Plugin installation path
- Existing component patterns found
- RECOMMENDED_NEXT_PHASE: semantic

### Phase 2: Semantic

**After discovery completes, transition and spawn semantic-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "semantic"
  evidence: "discovery-ack"
)

Task(
  subagent_type: "forge3:semantic-agent"
  prompt: "Plan implementation for: <USER_REQUEST>. Discovery context: <DISCOVERY_OUTPUT>"
  description: "Planning component structure"
)
```

The semantic-agent will return:
- Component type and name
- File paths to create
- Content outline
- RECOMMENDED_NEXT_PHASE: execute

### Phase 3: Execute

**After semantic completes, transition and spawn execute-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "execute"
  evidence: "semantic-ack"
)

Task(
  subagent_type: "forge3:execute-agent"
  prompt: "Create files based on plan: <SEMANTIC_OUTPUT>. User request: <USER_REQUEST>"
  description: "Creating component files"
)
```

The execute-agent will return:
- Files created (paths and summaries)
- RECOMMENDED_NEXT_PHASE: schema-check

### Phase 4: Schema-check

**After execute completes, transition and spawn schema-check-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "schema-check"
  evidence: "execute-ack"
)

Task(
  subagent_type: "forge3:schema-check-agent"
  prompt: "Validate files created: <LIST_OF_FILES_FROM_EXECUTE>"
  description: "Validating schema compliance"
  model: "haiku"
)
```

## Context Passing

Each agent's output becomes input for the next phase:

```
User Request
    ↓
[discovery-agent] → plugin_path, existing_patterns
    ↓
[semantic-agent] → component_type, file_paths, content_outline
    ↓
[execute-agent] → files_created, content_summaries
    ↓
[schema-check-agent] → validation_results
    ↓
Final Report to User
```

## What NOT to Do

**NEVER do any of these directly:**
- ❌ Run `ls`, `find`, `Glob` to discover plugin location
- ❌ Read existing skills/agents to learn patterns
- ❌ Write files using Write/Edit tools
- ❌ Validate schemas yourself

**ALWAYS delegate to agents:**
- ✅ Spawn discovery-agent for location/pattern discovery
- ✅ Spawn semantic-agent for planning
- ✅ Spawn execute-agent for file creation
- ✅ Spawn schema-check-agent for validation

## Usage

```
/assist:create <description of component to create>
/assist:create based on the previous plan
```

## Examples

```
/assist:create a skill for generating commit messages
/assist:create an agent that reviews pull requests
/assist:create the component from the semantic plan above
/assist:create a hook that blocks force push to main
```

## File Locations

Components are created in standard locations:

| Component | Location |
|-----------|----------|
| Skill | `skills/<skill-name>/SKILL.md` |
| Agent | `agents/<agent-name>.md` |
| Command | `commands/<command-name>.md` |
| Hook | `hooks/hooks.json` + `hooks/<script>.py` |

## Final Report

After all phases complete, report to the user:

```
## Creation Complete

**Component:** <name>
**Type:** <skill|agent|command|hook>
**Files created:**
- <path1>
- <path2>

**Validation:** <pass|fail with issues>

**Next steps:**
- Test the component
- Run /assist:verify for detailed validation
```

## Requirements

- Workflow daemon must be running
- All 4 phases must complete
- Each phase must spawn its designated agent
- Schema-check is mandatory final phase

## Related Commands

- `/assist:wizard` - Routes to appropriate command
- `/assist:plan` - Plans structure only (skip execute)
- `/assist:verify` - Validates existing components
- `/assist:health-check` - Analyzes component quality
