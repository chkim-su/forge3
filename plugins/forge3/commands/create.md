---
name: create
description: Create component files (execute phase) - generates actual plugin component files
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "<component description or plan reference>"
---

# /create

Create plugin component files based on a plan or description.

## Usage

```
/create <description of component to create>
/create based on the previous plan
```

## Examples

```
/create a skill for generating commit messages
/create an agent that reviews pull requests  
/create the component from the semantic plan above
/create a hook that blocks force push to main
```

## Workflow Phases

The `/create` command executes a file creation workflow:

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Execute | execute-agent | Creates the actual files |
| 2. Schema-check | schema-check-agent | Validates created files |

### Phase Transitions

Phase transitions require explicit `workflow_transition` tool calls with evidence.

```
---
[Phase 1/2: Execute] Starting...
---
```

When execute phase completes:
```
---
[Phase 1/2: Execute] Agent complete
---
Allowed next phases: schema-check

To proceed, use workflow_transition tool.
```

## What Happens

When you run `/create`:

1. **Execute Phase**: The execute-agent:
   - Creates files in the correct locations
   - Generates YAML frontmatter with required fields
   - Writes the component content
   - Ensures proper file structure

2. **Schema-check Phase**: Validates created files against schemas

## File Locations

Components are created in standard locations:

| Component | Location |
|-----------|----------|
| Skill | `skills/<skill-name>/SKILL.md` |
| Agent | `agents/<agent-name>.md` |
| Command | `commands/<command-name>.md` |
| Hook | `hooks/hooks.json` + `hooks/<script>.py` |

## Output

After successful creation:
- Files created in correct locations
- Proper YAML frontmatter
- Schema-validated content
- Summary of created files

## Best Practice: Plan First

For complex components, run `/plan` first:

```
/plan a skill for code review
# Review the plan
/create based on the plan above
```

## Requirements

- Workflow daemon must be running (`workflowd`)
- Phase transitions require explicit tool calls
- Schema-check is mandatory final phase

## Related Commands

- `/assist` - Dispatcher that routes to appropriate command
- `/plan` - Plans component structure first
- `/verify` - Validates created components
- `/health-check` - Analyzes component quality
