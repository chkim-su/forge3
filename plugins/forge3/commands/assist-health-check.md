---
name: assist:health-check
description: Analyze plugin component quality using multi-agent workflow
allowed-tools:
  - Task
  - mcp__workflow__workflow_transition
argument-hint: "[component-path]"
---

# /assist:health-check

Run health and suitability analysis on plugin components to get scored reports with recommendations.

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
| 1. Discovery | discovery-agent | Find components and gather metadata |
| 2. Analyze | analyzer-agent | Score each component's health |
| 3. Report | reporter-agent | Aggregate and produce final report |
| 4. Schema-check | schema-check-agent | Final validation pass |

## Phase Execution Instructions

### Phase 1: Discovery

**Start by spawning the discovery-agent:**

```
Task(
  subagent_type: "forge3:discovery-agent"
  prompt: "Mode: health. Find components with metadata for health analysis. Target: <PATH_OR_ALL>"
  description: "Discovering components for health check"
  model: "haiku"
)
```

The discovery-agent will return:
- Component list with metadata (trigger counts, tool counts, sizes)
- RECOMMENDED_NEXT_PHASE: analyze

### Phase 2: Analyze

**After discovery completes, transition and spawn analyzer-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "analyze"
  evidence: "discovery-ack"
)

Task(
  subagent_type: "forge3:analyzer-agent"
  prompt: "Mode: health. Score components for quality: <DISCOVERY_OUTPUT>"
  description: "Analyzing component health"
)
```

The analyzer-agent will return:
- Scores per component (structure, content, references, suitability)
- Grades (A-F)
- Issues found
- RECOMMENDED_NEXT_PHASE: report

### Phase 3: Report

**After analyze completes, transition and spawn reporter-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "report"
  evidence: "analyze-ack"
)

Task(
  subagent_type: "forge3:reporter-agent"
  prompt: "Aggregate health results: <ANALYSIS_OUTPUT>"
  description: "Generating health report"
  model: "haiku"
)
```

The reporter-agent will return:
- Overall health score
- Pattern analysis
- Prioritized recommendations
- RECOMMENDED_NEXT_PHASE: schema-check

### Phase 4: Schema-check

**After report completes, transition and spawn schema-check-agent:**

```
mcp__workflow__workflow_transition(
  target_phase: "schema-check"
  evidence: "report-ack"
)

Task(
  subagent_type: "forge3:schema-check-agent"
  prompt: "Final validation based on health report: <REPORT_OUTPUT>"
  description: "Final schema validation"
  model: "haiku"
)
```

## What NOT to Do

**NEVER do any of these directly:**
- ❌ Run `ls`, `find`, `Glob` to discover components
- ❌ Read files and analyze quality yourself
- ❌ Calculate scores yourself
- ❌ Generate the report yourself

**ALWAYS delegate to agents:**
- ✅ Spawn discovery-agent for component enumeration with metadata
- ✅ Spawn analyzer-agent for scoring
- ✅ Spawn reporter-agent for aggregation and reporting
- ✅ Spawn schema-check-agent for final validation

## Usage

```
/assist:health-check [component-path]
```

## Examples

```
/assist:health-check                        # Analyze all components
/assist:health-check skills/                # Analyze all skills
/assist:health-check agents/my-agent.md     # Analyze specific agent
/assist:health-check commands/              # Analyze all commands
```

## Analysis Criteria

### Structure Score (25 pts)
- YAML frontmatter validity
- Required fields present
- File organization

### Content Score (25 pts)
- Completeness of documentation
- Examples provided
- Clear instructions

### References Score (25 pts)
- Valid cross-references
- Tool names correct
- No broken links

### Suitability Score (25 pts)
- Appropriate complexity
- Follows best practices
- Production-ready

## Output

After all phases complete, report to the user:

```
## Health Analysis Report

**Target:** <path or "all components">
**Overall Score:** 82/100 (Grade: B)

**Grade Distribution:**
- A (90-100): 3 components
- B (80-89): 3 components
- C (70-79): 2 components

**Patterns Detected:**
- 2 skills missing examples section
- 1 agent has overly broad tool list

**Prioritized Recommendations:**

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

## Difference from /assist:verify

| Feature | /assist:verify | /assist:health-check |
|---------|----------------|----------------------|
| Focus | Schema compliance | Overall quality |
| Checks | Structural validation | Structure + content + suitability |
| Output | Pass/fail per check | Scores and grades |
| Recommendations | Fix structural issues | Improve quality |

## Requirements

- Workflow daemon must be running
- All 4 phases must complete
- Each phase must spawn its designated agent

## Related Commands

- `/assist:verify` - Schema-focused structural validation
- `/assist:wizard` - Routes to appropriate command
- `/assist:plan` - Plans component structure
- `/assist:create` - Creates component files
