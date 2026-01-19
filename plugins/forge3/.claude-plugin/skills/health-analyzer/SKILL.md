---
name: health-analyzer
triggers:
  - "health check"
  - "component health"
  - "analyze plugin health"
  - "suitability analysis"
  - "component quality"
  - "plugin health"
---

# Health Analyzer Skill

This skill provides criteria and metrics for analyzing the health and suitability of Claude Code plugin components.

## When to Use

Use this skill when you need to:
- Assess the overall health of plugin components
- Determine if components are suitable for their purpose
- Get a quality score for skills, agents, commands, or hooks
- Identify issues beyond basic schema validation

## Health Criteria by Component Type

### Skills

| Check | Pass Criteria | Weight |
|-------|--------------|--------|
| Location | `skills/<name>/SKILL.md` | 10% |
| YAML valid | Frontmatter parses without error | 10% |
| `name` field | Present, kebab-case | 10% |
| `triggers` field | Array with 2+ trigger phrases | 10% |
| Content length | 200+ characters | 15% |
| Sections | Has usage/examples | 15% |
| Documentation | Clear purpose statement | 15% |
| References | Files referenced exist | 15% |

### Agents

| Check | Pass Criteria | Weight |
|-------|--------------|--------|
| Location | `agents/<name>.md` (not subdirectory) | 10% |
| YAML valid | Frontmatter parses without error | 10% |
| `name` field | Present, kebab-case | 10% |
| `description` field | 20+ characters, starts with "Use this agent when" | 15% |
| `tools` field | Array of valid tool names | 10% |
| System prompt | 100+ characters, actionable instructions | 20% |
| Output format | Defined output structure | 15% |
| Important notes | Safety/behavior guidelines | 10% |

### Commands

| Check | Pass Criteria | Weight |
|-------|--------------|--------|
| Location | `commands/<name>.md` (not subdirectory) | 10% |
| YAML valid | Frontmatter parses without error | 10% |
| `name` field | Present, kebab-case | 10% |
| `description` field | Present, meaningful | 10% |
| `allowed-tools` | Uses kebab-case (not `allowed_tools`) | 10% |
| Usage section | Code block with examples | 15% |
| Examples | 2+ usage examples | 15% |
| What Happens | Clear explanation of behavior | 10% |
| Related section | Links to related commands | 10% |

### Hooks

| Check | Pass Criteria | Weight |
|-------|--------------|--------|
| hooks.json valid | Valid JSON syntax | 15% |
| Structure | Object with event keys (not array) | 15% |
| Event names | Valid: PreToolUse, PostToolUse, Stop, etc. | 10% |
| Nested hooks | Each entry has `hooks` array | 15% |
| Type field | `"type": "command"` present | 10% |
| Script path | Uses `${CLAUDE_PLUGIN_ROOT}` | 10% |
| Script exists | Referenced Python files exist | 15% |
| Python valid | Scripts have valid syntax | 10% |

## Suitability Criteria

### Component Type Appropriateness

| If the component... | It should be a... |
|--------------------|-------------------|
| Provides reference knowledge or guidance | Skill |
| Performs autonomous multi-step tasks | Agent |
| Is user-invoked with specific arguments | Command |
| Reacts to system events automatically | Hook |

### Suitability Indicators

**High suitability:**
- Clear, focused purpose
- Name reflects functionality
- Appropriate component type for the task
- Integrates well with existing components
- Documentation matches behavior

**Low suitability:**
- Vague or overly broad purpose
- Misleading name
- Wrong component type for the task
- Duplicates existing functionality
- Missing or inaccurate documentation

## Scoring Framework

### Score Calculation

```
Health Score = (Structure * 0.30) + (Content * 0.30) + (References * 0.20) + (Suitability * 0.20)
```

### Grade Thresholds

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | A | Excellent - Production ready |
| 80-89 | B | Good - Minor improvements possible |
| 70-79 | C | Acceptable - Should address issues |
| 60-69 | D | Needs work - Multiple issues |
| < 60 | F | Critical - Requires significant fixes |

## Common Issues Reference

| Issue | Component | Fix |
|-------|-----------|-----|
| `allowed_tools` (underscore) | Command | Use `allowed-tools` (kebab-case) |
| Agent in subdirectory | Agent | Move to `agents/name.md` |
| Skill as direct file | Skill | Move to `skills/name/SKILL.md` |
| hooks as array | Hook | Use object: `"hooks": { "Event": [...] }` |
| Missing `type: command` | Hook | Add `"type": "command"` in hook entry |
| Hardcoded paths | Hook | Use `${CLAUDE_PLUGIN_ROOT}` |
| Tools as string | Agent | Use array: `tools: [Read, Grep]` |
| Missing description | Agent/Command | Add meaningful description field |

## Output Format

When performing health analysis, report results as:

```
HEALTH_ANALYSIS_REPORT
======================

SUMMARY:
- total_components: <count>
- overall_health_score: <0-100>
- overall_grade: <A-F>

COMPONENT_DETAILS:

Component: <name>
Type: <skill|agent|command|hook>
Health Score: <0-100> (<grade>)

Structure: [PASS|FAIL] <details>
Content: [PASS|FAIL|WARN] <details>
References: [PASS|FAIL] <details>
Suitability: <appropriate|questionable|inappropriate>

Issues:
- <issue 1>
- <issue 2>

Recommendations:
- <recommendation 1>
- <recommendation 2>
```

## Related

- `/verify` - Schema-focused validation (structural checks only)
- `/health-check` - On-demand health analysis command
- `health-analyzer` agent - Autonomous health analysis
