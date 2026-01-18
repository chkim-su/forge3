---
name: assist
description: Start a guided workflow to create Claude Code plugin components (skills, agents, commands, hooks)
allowed_tools:
  - Task
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# /assist

Start a guided workflow to create Claude Code plugin components.

## Usage

```
/assist <description of what you want to create>
```

## Examples

```
/assist create a skill for generating commit messages
/assist add an agent for code review
/assist create a command to deploy to staging
/assist add a hook to prevent commits without tests
```

## Workflow Phases

The assist command guides you through a structured workflow:

1. **Router Phase** - Classifies your intent
2. **Semantic Phase** - Plans the implementation structure
3. **Execute Phase** - Creates the actual files
4. **Verify Phase** - Validates the implementation

## What Happens

When you run `/assist`:

1. The router-agent analyzes your request
2. The semantic-agent designs the component structure
3. The execute-agent creates the files
4. The verify-agent validates the result

## Requirements

- MCP daemon must be running (`python -m mcp.workflow_server`)
- Each phase must complete before the next begins
- You cannot skip phases

## Component Types

| Type | Creates | Location |
|------|---------|----------|
| Skill | SKILL.md | skills/<name>/ |
| Agent | <name>.md | agents/ |
| Command | <name>.md | commands/ |
| Hook | hooks.json + .py | hooks/ |

## Troubleshooting

If the workflow gets stuck:
1. Check MCP daemon is running
2. Verify current phase status
3. Invoke the required agent manually

Use `/verify` to check component validity after creation.
