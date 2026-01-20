---
name: health-aggregate-skill
description: Aggregation phase for /health-check command - produces final report
triggers:
  - health-check aggregate phase
  - health report generation
  - aggregate health scores
---

# Health-Check Aggregation Phase

The third phase of the `/health-check` workflow. Aggregates individual scores into a comprehensive health report.

## Purpose

Combine individual component scores into an overall plugin health assessment with actionable recommendations.

## Aggregation Process

1. **Collect scores**: Gather all component scores from analyze phase
2. **Calculate averages**: Weighted average based on component importance
3. **Identify patterns**: Find common issues across components
4. **Generate recommendations**: Prioritize improvements by impact

## Weighting

| Component Type | Weight |
|----------------|--------|
| plugin.json | 1.5x |
| Skills | 1.0x |
| Agents | 1.2x |
| Commands | 1.0x |
| Hooks | 1.0x |
| marketplace.json | 0.8x |

## Report Sections

### Summary

- Overall health score and grade
- Total components analyzed
- Grade distribution
- Critical issues count

### Component Details

- Individual scores and grades
- Per-component issues
- Per-component recommendations

### Pattern Analysis

- Common issues found across multiple components
- Systemic problems
- Best practices violations

### Recommendations

Prioritized list of improvements:
1. **Critical** (blocks deployment)
2. **High** (significantly impacts quality)
3. **Medium** (improves quality)
4. **Low** (nice to have)

## Output Format

```
HEALTH_ANALYSIS_REPORT
======================

SUMMARY:
- Total Components: 11
- Overall Health Score: 85/100
- Overall Grade: B

GRADE_DISTRIBUTION:
- A (90-100): 4 components
- B (80-89): 5 components  
- C (70-79): 2 components
- D (60-69): 0 components
- F (< 60): 0 components

COMPONENT_REPORTS:
[Individual component scores...]

PATTERNS_DETECTED:
- 3 skills missing examples section
- 2 agents have overly broad tool lists

PRIORITIZED_RECOMMENDATIONS:

[HIGH] Add examples to skills
- Affects: router-skill, semantic-skill, execute-skill
- Impact: Improves Claude's understanding

[MEDIUM] Refine agent tool lists
- Affects: execute-agent, verify-agent
- Impact: Reduces potential for tool misuse

[LOW] Add more trigger phrases
- Affects: All skills
- Impact: Improves skill discovery
```

## Transition Evidence

To proceed to schema-check phase, provide:
- `overall_score`: Weighted average health score
- `overall_grade`: Letter grade
- `critical_count`: Number of critical issues (must be 0)
- `recommendations`: Prioritized recommendation list
