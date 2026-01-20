---
name: assist:verify
description: Verify plugin components using multi-agent workflow
allowed-tools:
  - Task
  - mcp__workflow__workflow_transition
argument-hint: "[component-path]"
---

# /assist:verify

Verify and validate plugin components for schema compliance and correctness.

## Critical Rule

**YOU MUST SPAWN AGENTS using the Task tool. DO NOT do agent work directly.**

The main LLM's only job is to:
1. Spawn the right agent for each phase
2. Pass context between phases
3. Call workflow transitions
4. Report final results to the user

## Workflow Phases

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Discovery | discovery-agent | Find all components to validate |
| 2. Validate | analyzer-agent | Validate each component schema |
| 3. Schema-check | schema-check-agent | Final validation pass |

## Phase Execution Instructions

### Phase 1: Discovery

**Start by spawning the discovery-agent:**

```
Task(
  subagent_type: "forge3:discovery-agent"
  prompt: "Mode: verify. Find all components to validate. Target: <PATH_OR_ALL>"
  description: "Discovering components"
  model: "haiku"
)
```

The discovery-agent will return:
- All component paths by type
- Total count
- RECOMMENDED_NEXT_PHASE: validate

### Phase 2: Validate

**After discovery completes, transition and spawn analyzer-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "validate"
  evidence: "discovery-ack"
)

Task(
  subagent_type: "forge3:analyzer-agent"
  prompt: "Mode: validate. Check schema compliance for components: <DISCOVERY_OUTPUT>"
  description: "Validating component schemas"
)
```

The analyzer-agent will return:
- Validation results per component
- Pass/fail status
- Issues found
- RECOMMENDED_NEXT_PHASE: schema-check

### Phase 3: Schema-check

**After validate completes, transition and spawn schema-check-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "schema-check"
  evidence: "validate-ack"
)

Task(
  subagent_type: "forge3:schema-check-agent"
  prompt: "Final validation for: <COMPONENT_LIST>. Previous issues: <VALIDATION_ISSUES>"
  description: "Final schema validation"
  model: "haiku"
)
```

## What NOT to Do

**NEVER do any of these directly:**
- ❌ Run `ls`, `find`, `Glob` to discover components
- ❌ Read and validate files yourself
- ❌ Check YAML syntax yourself

**ALWAYS delegate to agents:**
- ✅ Spawn discovery-agent for component enumeration
- ✅ Spawn analyzer-agent for validation
- ✅ Spawn schema-check-agent for final check

## Usage

```
/assist:verify [component-path]
```

Without arguments, verifies all components in the plugin.

## Examples

```
/assist:verify                              # Verify all components
/assist:verify skills/my-skill              # Verify specific skill
/assist:verify agents/my-agent.md           # Verify specific agent
/assist:verify hooks/                       # Verify all hooks
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
- Cross-references between components

### Schema-check Phase
- Final schema compliance
- Overall verification status

## Component Requirements

| Component | Required Fields |
|-----------|-----------------|
| Skills | name, description, triggers |
| Agents | name, description, tools |
| Commands | name, description |
| plugin.json | name, version, description, author |

## Output

After all phases complete, report to the user:

```
## Verification Report

**Target:** <path or "all components">

**Results:**
| Component | Status | Issues |
|-----------|--------|--------|
| plugin.json | PASS | - |
| agents/router-agent.md | PASS | - |
| skills/my-skill/SKILL.md | FAIL | Missing triggers |

**Summary:**
- Checked: 10 components
- Passed: 9
- Failed: 1

**Status:** FAIL
```

## Requirements

- Workflow daemon must be running
- All 3 phases must complete
- Each phase must spawn its designated agent

## Related Commands

- `/assist:wizard` - Routes to appropriate command
- `/assist:plan` - Plans component structure
- `/assist:create` - Creates component files
- `/assist:health-check` - Quality analysis (beyond schema compliance)
