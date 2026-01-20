---
name: assist:plan
description: Plan component structure using multi-agent workflow
allowed-tools:
  - Task
  - mcp__workflow__workflow_transition
argument-hint: "<component description>"
---

# /assist:plan

Plan the structure of a plugin component before creating it.

## Critical Rule

**YOU MUST SPAWN AGENTS using the Task tool. DO NOT do agent work directly.**

The main LLM's only job is to:
1. Spawn the right agent for each phase
2. Pass context between phases
3. Call workflow transitions
4. Present the plan to the user

## Workflow Phases

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Discovery | discovery-agent | Find plugin location, existing patterns |
| 2. Semantic | semantic-agent | Plan the implementation structure |
| 3. Schema-check | schema-check-agent | Validate the plan structure |

## Phase Execution Instructions

### Phase 1: Discovery

**Start by spawning the discovery-agent:**

```
Task(
  subagent_type: "forge3:discovery-agent"
  prompt: "Mode: create. Find plugin location and existing patterns for planning: <USER_REQUEST>"
  description: "Discovering plugin structure"
  model: "haiku"
)
```

The discovery-agent will return:
- Plugin path
- Existing component patterns
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
  prompt: "Plan structure for: <USER_REQUEST>. Discovery context: <DISCOVERY_OUTPUT>"
  description: "Planning component structure"
)
```

The semantic-agent will return:
- Component type and name
- File paths to create
- YAML frontmatter structure
- Content outline
- RECOMMENDED_NEXT_PHASE: schema-check

### Phase 3: Schema-check

**After semantic completes, transition and spawn schema-check-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "schema-check"
  evidence: "semantic-ack"
)

Task(
  subagent_type: "forge3:schema-check-agent"
  prompt: "Validate plan structure: <SEMANTIC_OUTPUT>"
  description: "Validating plan against schema"
  model: "haiku"
)
```

## What NOT to Do

**NEVER do any of these directly:**
- ❌ Run `ls`, `find`, `Glob` to discover patterns
- ❌ Read existing skills/agents to learn structure
- ❌ Design the component structure yourself

**ALWAYS delegate to agents:**
- ✅ Spawn discovery-agent for location/pattern discovery
- ✅ Spawn semantic-agent for structure planning
- ✅ Spawn schema-check-agent for validation

## Usage

```
/assist:plan <description of component to plan>
```

## Examples

```
/assist:plan a skill for generating commit messages
/assist:plan an agent that reviews pull requests
/assist:plan a command to deploy to staging
/assist:plan a hook that blocks dangerous git commands
```

## Plan Output

After all phases complete, present the plan to the user:

```
## Component Plan

**Type:** <skill|agent|command|hook>
**Name:** <component-name>

**Files to create:**
- <path1>
- <path2>

**YAML Frontmatter:**
```yaml
name: <name>
description: <description>
triggers:
  - <trigger1>
  - <trigger2>
```

**Content Outline:**
1. <section1>
2. <section2>
3. <section3>

**Validation:** <pass|issues found>

**Next step:** Run `/assist:create based on this plan`
```

## Difference from /assist:create

| Command | What it does |
|---------|--------------|
| `/assist:plan` | Produces a plan only (no file creation) |
| `/assist:create` | Creates actual files (includes planning internally) |

Use `/assist:plan` when you want to review the plan before committing to file creation.

## Requirements

- Workflow daemon must be running
- All 3 phases must complete
- Each phase must spawn its designated agent

## Related Commands

- `/assist:wizard` - Routes to appropriate command
- `/assist:create` - Creates files (includes planning)
- `/assist:verify` - Validates existing components
