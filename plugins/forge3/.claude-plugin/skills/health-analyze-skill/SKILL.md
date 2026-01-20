---
name: health-analyze-skill
description: Analysis phase for /health-check command - scores each component
triggers:
  - health-check analyze phase
  - component health scoring
  - quality analysis
---

# Health-Check Analysis Phase

The second phase of the `/health-check` workflow. Performs detailed health analysis and scoring of each component.

## Purpose

Analyze each component's quality, completeness, and suitability, producing a health score.

## Scoring Dimensions

### Structure Score (25%)

| Factor | Points |
|--------|--------|
| File exists in correct location | 5 |
| Valid YAML frontmatter | 5 |
| All required fields present | 10 |
| Optional fields present | 5 |

### Content Score (25%)

| Factor | Points |
|--------|--------|
| Non-trivial content length | 10 |
| Clear formatting | 5 |
| Proper sections | 5 |
| No placeholder text | 5 |

### Reference Score (25%)

| Factor | Points |
|--------|--------|
| All references valid | 10 |
| Appropriate tool selection | 10 |
| No orphaned components | 5 |

### Suitability Score (25%)

| Factor | Points |
|--------|--------|
| Component type matches purpose | 10 |
| Appropriate for Claude Code plugin | 10 |
| Follows best practices | 5 |

## Component-Specific Criteria

### Skills

- Clear trigger phrases (not generic)
- Focused on single purpose
- Adequate context provided
- Examples where helpful

### Agents

- Appropriate tool selection
- Clear system prompt
- Defined scope
- Error handling guidance

### Commands

- Clear usage instructions
- Helpful examples
- Appropriate tool restrictions
- Good documentation

## Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent - Production ready |
| 80-89 | B | Good - Minor improvements possible |
| 70-79 | C | Acceptable - Should address issues |
| 60-69 | D | Needs work - Multiple issues |
| < 60 | F | Critical - Requires significant fixes |

## Output Format (Per Component)

```
COMPONENT: skills/router-skill
TYPE: skill
SCORES:
  Structure: 22/25
  Content: 23/25
  References: 25/25
  Suitability: 20/25
  TOTAL: 90/100 (A)

ISSUES:
- None

RECOMMENDATIONS:
- Consider adding more trigger phrase variations
```

## Transition Evidence

To proceed to aggregate phase, provide:
- `analyzed_count`: Number of components analyzed
- `scores`: Map of component path to score
- `grade_distribution`: Count of A/B/C/D/F grades
