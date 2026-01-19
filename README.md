# Forge3 Workflow System

Workflow engine-based system for creating Claude Code plugin components with structured phases and state management.

## Overview

Forge3 provides a structured workflow for creating plugin components (skills, agents, commands, hooks) with:

- **Workflow daemon as SSOT** - Single source of truth for workflow state
- **Event-driven architecture** - SSE-based notifications instead of polling
- **Phase enforcement** - Hooks enforce agent invocation and transition rules
- **Core invariants** - Strict separation of concerns

## Core Invariants

1. **LLM never owns state** - workflow daemon is the authority
2. **Agent never makes final file decisions** - Main LLM does
3. **Hook never makes semantic judgments** - Only structural enforcement
4. **Router Agent is always invoked** - Pattern matching is optimization only
5. **Phase start = Agent execution first** - Mandatory
6. **Completion signal = workflow_transition Tool Call** - Single source

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start workflow daemon
workflowd
```

## Usage

```bash
# Create a new component
/assist create a skill for generating commit messages

# Verify a component
/verify skills/my-skill
```

## Architecture

```
forge3/
├── mcp/                    # Workflow daemon (FastAPI server)
│   ├── workflow_schema.py  # Pydantic models
│   ├── state_store.py      # In-memory + JSON persistence
│   ├── workflow_engine.py  # State machine logic
│   ├── sse_broadcaster.py  # SSE event broadcasting
│   └── workflow_server.py  # FastAPI endpoints
├── hooks/                  # Event hooks
│   ├── hooks.json          # Hook configuration
│   ├── router_hook.py      # UserPromptSubmit handler
│   ├── phase_hook.py       # PreToolUse enforcement
│   └── stop_hook.py        # Stop prevention
├── agents/                 # Subagents
│   ├── router-agent.md     # Intent classification
│   ├── semantic-agent.md   # Structure planning
│   ├── execute-agent.md    # Implementation
│   └── verify-agent.md     # Validation
├── skills/                 # Skill definitions
├── commands/               # Slash commands
└── scripts/                # Utilities
```

## Workflow Phases

| Phase | Agent | Purpose |
|-------|-------|---------|
| Router | router-agent | Classify intent |
| Semantic | semantic-agent | Plan structure |
| Execute | execute-agent | Create files |
| Verify | verify-agent | Validate result |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/workflow/init` | POST | Initialize workflow |
| `/workflow/status` | GET | Query current state |
| `/workflow/transition` | POST | Validate & transition |
| `/workflow/current` | GET | Get context |
| `/agent/invoke` | POST | Record agent invocation |
| `/agent/complete` | POST | Mark agent done |
| `/sse/events` | GET | SSE subscription |

## Monitoring

```bash
# Monitor workflow events
python scripts/workflow_monitor.py

# Check current status
python scripts/workflow_monitor.py --status

# Filter by workflow ID
python scripts/workflow_monitor.py --workflow-id <id>
```

## Development

```bash
# Start server in development mode
cd forge3
workflowd

# Test endpoints
curl http://127.0.0.1:8766/health
curl http://127.0.0.1:8766/workflow/status
```

## Testing

1. **Unit Test** - workflow daemon endpoints
   ```bash
   curl http://127.0.0.1:8766/workflow/status
   ```

2. **Hook Test** - Hook communication
   ```bash
   echo '{"prompt":"/assist create skill"}' | python3 hooks/router_hook.py
   ```

3. **E2E Test** - Full workflow
   - Run `/assist create a hello skill`
   - Verify phase transitions
   - Verify component created

## License

MIT
