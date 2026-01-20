---
name: plan
description: Plan component structure (semantic phase) - designs the implementation structure for plugin components
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
argument-hint: "<component description>"
---

# /plan

Plan the structure of a plugin component before creating it.

## Usage

```
/plan <description of component to plan>
```

## Examples

```
/plan a skill for generating commit messages
/plan an agent that reviews pull requests
/plan a command to deploy to staging
/plan a hook that blocks dangerous git commands
```

## Workflow Phases

The `/plan` command executes a focused planning workflow:

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Semantic | semantic-agent | Plans the implementation structure |
| 2. Schema-check | schema-check-agent | Validates the plan against schemas |

### Phase Transitions

Phase transitions require explicit `workflow_transition` tool calls with evidence.

```
---
[Phase 1/2: Semantic] Starting...
---
```

When semantic phase completes:
```
---
[Phase 1/2: Semantic] Agent complete
---
Allowed next phases: schema-check

To proceed, use workflow_transition tool.
```

## What Happens

When you run `/plan`:

1. **Semantic Phase**: The semantic-agent analyzes your request and:
   - Determines the component type (skill, agent, command, hook)
   - Plans the file structure and location
   - Designs the YAML frontmatter fields
   - Outlines the content structure

2. **Schema-check Phase**: Validates the plan against Claude Code plugin schemas

## Output

The plan includes:
- Component type determination
- File path(s) to create
- YAML frontmatter structure
- Content outline
- Dependencies and references

## After Planning

After `/plan` completes, you can:
- Run `/create` to generate the actual files
- Modify the plan and run `/plan` again
- Run `/verify` to check existing components

## Requirements

- Workflow daemon must be running (`workflowd`)
- Phase transitions require explicit tool calls
- Schema-check is mandatory final phase

## Related Commands

- `/assist` - Dispatcher that routes to appropriate command
- `/create` - Creates files based on plan
- `/verify` - Validates existing components
