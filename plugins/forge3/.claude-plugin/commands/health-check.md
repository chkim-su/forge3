---
name: health-check
description: Run health and suitability analysis on plugin components
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

## What Happens

1. **Discovery** - Finds all components matching the path (or all if no path given)
2. **Analysis** - Invokes the health-analyzer agent to examine each component
3. **Scoring** - Calculates health scores based on structure, content, references, and suitability
4. **Reporting** - Produces a detailed report with grades and recommendations

## Output

```
HEALTH_ANALYSIS_REPORT
======================

SUMMARY:
- total_components: 8
- overall_health_score: 82
- overall_grade: B

COMPONENT_REPORTS:

Component: router-skill
Type: skill
Health Score: 90 (A)
[PASS] All structure checks
[PASS] All content checks
[PASS] All reference checks
Suitability: appropriate
Issues: None
Recommendations: None

Component: my-agent
Type: agent
Health Score: 75 (C)
[PASS] Location correct
[FAIL] Missing important notes section
[WARN] Description could be clearer
Suitability: appropriate
Issues:
- Missing important notes section
Recommendations:
- Add an "Important Notes" section
- Expand description to be more specific

OVERALL_RECOMMENDATIONS:
1. Add missing sections to my-agent
2. Consider adding more trigger phrases to skills
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

## Integration

This command can be used:
- After `/assist` to validate new components
- Before publishing plugins
- In CI/CD pipelines for quality gates
- During code review

## Related

- `/verify` - Schema-focused structural validation
- `/assist` - Guided component creation workflow
- `health-analyzer` agent - The underlying analysis agent
