---
name: verify-connectivity-skill
description: Connectivity phase for /verify command - validates cross-references
triggers:
  - verify connectivity phase
  - cross-reference validation
  - component connectivity check
---

# Verify Connectivity Phase

The third phase of the `/verify` workflow. Validates cross-references between components.

## Purpose

Ensure all component references are valid and resolvable. Check that the plugin forms a coherent whole.

## Connectivity Checks

### Skill → Agent References

When a skill references an agent (e.g., "use the router-agent"):
- Agent file must exist at `agents/<agent-name>.md`
- Agent must have valid frontmatter

### Hook → Script References

For each hook in `hooks.json`:
- Referenced command script must exist
- Script path must be valid relative to plugin root
- Python syntax must be valid

### Command → Tool References

For `allowed-tools` in commands:
- Tool names should be valid Claude Code tools
- Custom tool references should be resolvable

### Agent → Tool References

For `tools` in agents:
- Tool names should be valid Claude Code tools
- MCP tool references should match available MCP servers

### Manifest References

If `marketplace.json` exists:
- `location` paths must point to valid plugin directories
- Each referenced plugin must have a valid `plugin.json`

## Output Format

```
CONNECTIVITY_REPORT
===================

REFERENCE_CHECKS:

skills/router-skill -> agents/router-agent:
  [PASS] Agent file exists
  [PASS] Agent has valid frontmatter

hooks/hooks.json -> hooks/workflow_hook.py:
  [PASS] Script file exists
  [PASS] Python syntax valid

commands/assist.md -> tools:
  [PASS] Task tool available
  [PASS] Read tool available
  [WARN] Custom tool 'workflow_transition' - verify availability

CIRCULAR_DEPENDENCY_CHECK:
  [PASS] No circular dependencies detected

SUMMARY:
- References checked: 15
- Valid: 14
- Warnings: 1
- Broken: 0
```

## Transition Evidence

To proceed to schema-check phase, provide:
- `references_checked`: Number of references validated
- `valid_count`: Number of valid references
- `broken_count`: Number of broken references (must be 0 for success)
- `warnings`: List of warnings (non-blocking)
