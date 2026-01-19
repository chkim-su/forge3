---
name: assist
description: Start a guided workflow to create Claude Code plugin components (skills, agents, commands, hooks)
allowed-tools:
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

The assist command guides you through a structured workflow with visible phase indicators:

```
---
[Phase 1: Router] Starting...
---
```

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Router | router-agent | Classifies your intent |
| 2. Semantic | semantic-agent | Plans the implementation structure |
| 3. Execute | execute-agent | Creates the actual files |
| 4. Verify | verify-agent | Validates the implementation |

### Phase Transitions

When each phase completes, you'll see:

```
---
[Phase N: Name] Complete
[Phase N+1: Name] Starting...
---
```

When the workflow finishes:

```
---
[Phase 4: Verify] Complete
Workflow finished.
---
```

## What Happens

When you run `/assist`:

1. The router-agent analyzes your request
2. The semantic-agent designs the component structure
3. The execute-agent creates the files
4. The verify-agent validates the result

Each agent produces concise output - exploration and file reading happens internally.

## Requirements

- Workflow daemon must be running (`workflowd`)
- Serena MCP server must be available (for efficient codebase exploration)
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
1. Check workflow daemon is running
2. Check Serena MCP server is available
3. Verify current phase status
4. Invoke the required agent manually

Use `/verify` to check component validity after creation.
