---
name: verify-validate-skill
description: Validation phase for /assist:verify command - validates each component
triggers:
  - verify validate phase
  - component validation
  - schema validation
---

# Verify Validation Phase

The second phase of the `/assist:verify` workflow. Validates each discovered component against schemas.

## Purpose

Perform detailed validation of each component found in the discovery phase.

## Validation Checks Per Component Type

### Skills

| Check | Rule |
|-------|------|
| File exists | SKILL.md must exist in skill directory |
| YAML frontmatter | Must have valid YAML between `---` delimiters |
| Required fields | `name`, `description`, `triggers` |
| Triggers format | Must be a list with at least one item |
| Content present | Must have content after frontmatter |

### Agents

| Check | Rule |
|-------|------|
| File exists | `<name>.md` must exist in agents/ |
| YAML frontmatter | Must have valid YAML between `---` delimiters |
| Required fields | `name`, `description`, `tools` |
| Tools format | Must be a list of valid tool names |
| System prompt | Must have content (system prompt) after frontmatter |

### Commands

| Check | Rule |
|-------|------|
| File exists | `<name>.md` must exist in commands/ |
| YAML frontmatter | Must have valid YAML between `---` delimiters |
| Required fields | `name`, `description` |
| Optional fields | `allowed-tools`, `argument-hint` |

### Hooks

| Check | Rule |
|-------|------|
| hooks.json syntax | Must be valid JSON |
| Event types | Must use valid event types (PreToolUse, PostToolUse, etc.) |
| Script references | Referenced Python scripts must exist |
| Python syntax | Hook scripts must have valid Python syntax |

### plugin.json

| Check | Rule |
|-------|------|
| Valid JSON | Must be parseable |
| Required fields | `name`, `version`, `description`, `author` |
| Author format | Must be object with `name` field |
| Version format | Semantic version recommended |

## Output Format

```
VALIDATION_REPORT
=================

RESULTS:

skills/router-skill/SKILL.md:
  [PASS] File exists
  [PASS] YAML frontmatter valid
  [PASS] Required fields present
  [PASS] Triggers format valid

agents/my-agent.md:
  [PASS] File exists
  [FAIL] Missing 'tools' field
  
SUMMARY:
- Checked: 10 components
- Passed: 9
- Failed: 1

ISSUES:
- agents/my-agent.md: Missing required 'tools' field
```

## Transition Evidence

To proceed to the connectivity phase, provide:
- `validated_count`: Number of components validated
- `passed_count`: Number passing all checks
- `failed_count`: Number with failures
- `issues`: List of issues found
