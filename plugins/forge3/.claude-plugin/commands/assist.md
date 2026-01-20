---
name: assist
description: Dispatcher - classifies intent and recommends which command to use for plugin component creation
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
---

# /assist

**Dispatcher command** - Classifies your intent and recommends the appropriate command to run.

## Usage

```
/assist <description of what you want to do>
```

## Examples

```
/assist create a skill for generating commit messages
/assist I need to add an agent for code review
/assist help me create a command to deploy to staging
/assist verify my plugin components
```

## How It Works

`/assist` is a **dispatcher only** - it routes to other commands:

| Your Intent | Recommended Command |
|-------------|---------------------|
| Plan a component | `/plan` |
| Create files | `/create` |
| Validate components | `/verify` |
| Check quality | `/health-check` |

## Workflow

The `/assist` command runs a single phase:

```
---
[Phase 1/1: Router] Starting...
---
```

The router-agent:
1. Analyzes your request
2. Classifies your intent
3. Recommends which command to run next

### After Router Completes

```
---
[Phase 1/1: Router] Agent complete
---
Dispatcher phase complete. Based on the router's classification,
recommend one of these commands to the user:
- /plan - For component structure planning
- /create - For file creation
- /verify - For validation
```

## Important

**`/assist` does NOT create files or execute workflows.**

It only:
- Classifies your intent
- Gathers initial context
- Recommends the next command

## Recommended Workflow

For creating new components:

```bash
# Step 1: Get recommendation
/assist create a skill for code review

# Step 2: Plan the component
/plan a skill for code review

# Step 3: Create the files
/create based on the plan above

# Step 4: Validate the result
/verify skills/code-review-skill
```

## Available Commands

After `/assist` routes your request, use:

| Command | Purpose |
|---------|---------|
| `/plan` | Design component structure |
| `/create` | Generate component files |
| `/verify` | Validate against schemas |
| `/health-check` | Analyze component quality |

## Requirements

- Workflow daemon must be running (`workflowd`)
- Serena MCP server available (for codebase exploration)

## Related Commands

- `/plan` - Component structure planning
- `/create` - File creation
- `/verify` - Schema validation
- `/health-check` - Quality analysis
