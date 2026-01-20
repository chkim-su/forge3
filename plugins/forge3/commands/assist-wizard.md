---
name: assist:wizard
description: Dispatcher - classifies intent and routes to appropriate workflow
allowed-tools:
  - Task
  - mcp__workflow__workflow_transition
---

# /assist:wizard

**Dispatcher command** - Classifies your intent and routes to the appropriate workflow.

## Critical Rule

**YOU MUST SPAWN AGENTS using the Task tool. DO NOT classify intent directly.**

The main LLM's only job is to:
1. Spawn the router-agent to classify intent
2. Based on classification, recommend or auto-start the appropriate command
3. Report the routing decision to the user

## Workflow

The `/assist:wizard` command runs a single phase:

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Router | router-agent | Classify user intent |

## Phase Execution Instructions

### Phase 1: Router

**Spawn the router-agent to classify the request:**

```
Task(
  subagent_type: "forge3:router-agent"
  prompt: "Classify intent for: <USER_REQUEST>"
  description: "Classifying user intent"
  model: "haiku"
)
```

The router-agent will return:
- Intent category (create_skill, create_agent, create_command, create_hook, verify, health_check, unknown)
- Confidence (high, medium, low)
- Recommended command

## What NOT to Do

**NEVER do any of these directly:**
- ❌ Analyze the user's request yourself
- ❌ Decide what type of component to create
- ❌ Start exploring the codebase

**ALWAYS delegate to agents:**
- ✅ Spawn router-agent for intent classification

## Intent Routing

Based on the router-agent's classification:

| Intent | Recommended Command |
|--------|---------------------|
| `create_skill` | `/assist:create` or `/assist:plan` |
| `create_agent` | `/assist:create` or `/assist:plan` |
| `create_command` | `/assist:create` or `/assist:plan` |
| `create_hook` | `/assist:create` or `/assist:plan` |
| `modify_existing` | `/assist:create` with modification context |
| `verify` | `/assist:verify` |
| `health_check` | `/assist:health-check` |
| `unknown` | Ask user for clarification |

## Auto-Chain Behavior

After router-agent returns with HIGH confidence:
1. Report the classification to the user
2. Auto-start the recommended command

After router-agent returns with LOW confidence:
1. Report the classification and uncertainty
2. Ask user to confirm or clarify

## Usage

```
/assist:wizard <description of what you want to do>
```

## Examples

```
/assist:wizard create a skill for generating commit messages
/assist:wizard I need to add an agent for code review
/assist:wizard help me create a command to deploy to staging
/assist:wizard verify my plugin components
/assist:wizard check the health of my agents
```

## Output

After routing completes, report to the user:

```
## Intent Classification

**Request:** <user request summary>
**Classification:** create_skill
**Confidence:** high
**Recommended command:** /assist:create

Starting /assist:create workflow...
```

Or for low confidence:

```
## Intent Classification

**Request:** <user request summary>
**Classification:** unknown
**Confidence:** low
**Possible interpretations:**
- Create a new skill
- Modify an existing skill

Please clarify: Are you creating something new or modifying existing?
```

## Important Notes

- `/assist:wizard` is a **dispatcher** - it does NOT create files
- It classifies intent and routes to the appropriate command
- For complex requests, prefer `/assist:plan` before `/assist:create`

## Recommended Workflow

For new users:
```
/assist:wizard <description>  →  routes to appropriate command
```

For experienced users (skip routing):
```
/assist:plan <description>    →  get structure plan
/assist:create based on plan  →  create files
/assist:verify                →  validate result
```

## Available Commands

After `/assist:wizard` routes your request:

| Command | Purpose |
|---------|---------|
| `/assist:plan` | Design component structure only |
| `/assist:create` | Create component files |
| `/assist:verify` | Validate against schemas |
| `/assist:health-check` | Analyze component quality |

## Requirements

- Workflow daemon must be running
- Router-agent must be spawned via Task tool

## Related Commands

- `/assist:plan` - Component structure planning
- `/assist:create` - File creation
- `/assist:verify` - Schema validation
- `/assist:health-check` - Quality analysis
