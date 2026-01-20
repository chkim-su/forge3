---
name: health-check
description: Run health and suitability analysis on plugin components with multi-phase workflow
allowed-tools:
  - Task
  - Read
  - Grep
  - Glob
argument-hint: "[component-path]"
---

# /health-check

Run health and suitability analysis on plugin components to get scored reports with recommendations.

## Usage

```
/health-check                        # Analyze all components
/health-check skills/                # Analyze all skills
/health-check agents/my-agent.md     # Analyze specific agent
/health-check commands/              # Analyze all commands
/health-check hooks/                 # Analyze hooks configuration
```

## Examples

```
/health-check
```
Analyzes all plugin components and produces a comprehensive health report.

```
/health-check skills/router-skill
```
Analyzes only the router-skill component.

```
/health-check agents/
```
Analyzes all agents in the plugin.

## Workflow Phases

The `/health-check` command executes a multi-phase analysis workflow:

| Phase | Agent | Purpose |
|-------|-------|---------|
| 1. Discover | health-discovery-agent | Finds components and gathers metadata |
| 2. Analyze | health-analyze-agent | Scores each component's health |
| 3. Aggregate | health-aggregate-agent | Produces final report |
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
Allowed next phases: analyze

To proceed, use workflow_transition tool.
```

## Analysis Phases

### Discovery Phase
- Locates plugin root
- Enumerates all component files
- Gathers metadata (trigger counts, tool counts, content length)

### Analyze Phase
- Scores structure (25 pts)
- Scores content (25 pts)
- Scores references (25 pts)
- Scores suitability (25 pts)
- Calculates grades (A-F)

### Aggregate Phase
- Calculates weighted overall score
- Identifies patterns across components
- Prioritizes recommendations
- Generates final report

### Schema-check Phase
- Ensures critical issues are addressed
- Final validation of changes

## Output

```
HEALTH_ANALYSIS_REPORT
======================

SUMMARY:
- Total Components: 8
- Overall Health Score: 82/100
- Overall Grade: B

GRADE_DISTRIBUTION:
- A (90-100): 3 components
- B (80-89): 3 components
- C (70-79): 2 components

PATTERNS_DETECTED:
- 2 skills missing examples section
- 1 agent has overly broad tool list

PRIORITIZED_RECOMMENDATIONS:

[HIGH] Add examples to skills
  Affects: router-skill, semantic-skill

[MEDIUM] Refine agent tool lists
  Affects: execute-agent
```

## Score Interpretation

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent - Production ready |
| 80-89 | B | Good - Minor improvements possible |
| 70-79 | C | Acceptable - Should address issues |
| 60-69 | D | Needs work - Multiple issues |
| < 60 | F | Critical - Requires significant fixes |

## Difference from /verify

| Feature | /verify | /health-check |
|---------|---------|---------------|
| Focus | Schema compliance | Overall quality |
| Checks | Structural validation | Structure + content + suitability |
| Output | Pass/fail per check | Scores and grades |
| Recommendations | Fix structural issues | Improve quality |

Use `/verify` first to ensure components are structurally valid, then `/health-check` for deeper quality analysis.

## Requirements

- Workflow daemon must be running (`workflowd`)
- Phase transitions require explicit tool calls
- All 4 phases must complete
- Schema-check is mandatory final phase

## Related Commands

- `/verify` - Schema-focused structural validation
- `/assist` - Dispatcher that routes to appropriate command
- `/plan` - Plans component structure
- `/create` - Creates component files
