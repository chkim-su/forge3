---
name: verify
description: Verify and validate plugin components for schema compliance with multi-phase workflow
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
  - Bash
argument-hint: "[component-path]"
---

# /verify

Verify and validate plugin components for schema compliance and correctness.

## Usage

```
/verify [component-path]
```

Without arguments, verifies all components in the plugin.

## Examples

```
/verify                              # Verify all components
/verify skills/my-skill              # Verify specific skill
/verify agents/my-agent.md           # Verify specific agent
/verify hooks/                       # Verify all hooks
```

## Workflow Phases

The `/verify` command executes a multi-phase validation workflow:

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Discover | verify-discovery-agent | Finds all components to validate |
| 2. Validate | verify-validate-agent | Validates each component schema |
| 3. Connectivity | verify-connectivity-agent | Checks cross-references |
| 4. Schema-check | schema-check-agent | Final validation pass |

### Phase Transitions

Phase transitions require explicit `workflow_transition` tool calls with evidence.

```
---
[Phase 1/4: Discover] Starting...
---
```

When a phase completes:
```
---
[Phase 1/4: Discover] Agent complete
---
Allowed next phases: validate

To proceed, use workflow_transition tool.
```

## Validation Checks

### Discovery Phase
- Locates plugin root
- Enumerates all component files
- Catalogs by type (skills, agents, commands, hooks)

### Validate Phase
- YAML frontmatter syntax
- Required fields per component type
- JSON syntax for hooks.json
- Python syntax for hook scripts

### Connectivity Phase
- Skill → Agent references
- Hook → Script references
- Tool name validity
- Marketplace references (if present)

### Schema-check Phase
- Final schema compliance
- Cross-reference validation
- Overall verification status

## Component Requirements

### Skills
- Required fields: name, description, triggers

### Agents
- Required fields: name, description, tools

### Commands
- Required fields: name, description

### plugin.json
- Required: name, version, description, author (as object)

## Output

```
VERIFICATION_REPORT
==================

Phase: schema-check (final)

RESULTS:
[PASS] plugin.json - All required fields present
[PASS] agents/router-agent.md - Valid frontmatter
[FAIL] skills/my-skill/SKILL.md - Missing triggers

SUMMARY:
- Checked: 10 components
- Passed: 9
- Failed: 1

WORKFLOW_STATUS: FAIL
```

## Requirements

- Workflow daemon must be running (`workflowd`)
- Phase transitions require explicit tool calls
- All 4 phases must complete
- Schema-check is mandatory final phase

## Related Commands

- `/assist` - Dispatcher that routes to appropriate command
- `/plan` - Plans component structure
- `/create` - Creates component files
- `/health-check` - Quality analysis (beyond schema compliance)
