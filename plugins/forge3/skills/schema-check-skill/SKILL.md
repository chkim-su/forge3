---
name: schema-check-skill
description: Common schema validation rules for all plugin components
triggers:
  - schema-check phase
  - final validation
  - component schema validation
---

# Schema Check Phase

This is the **mandatory final phase** for all non-dispatcher workflows. Every workflow (except `/assist`) ends with schema-check validation.

## Purpose

Validate all generated/modified plugin components against Claude Code plugin schemas and conventions.

## Validation Rules

### plugin.json Schema

Required fields:
- `name`: String, lowercase with hyphens, no spaces
- `version`: Semantic version (e.g., "1.0.0")
- `description`: Non-empty string
- `author`: Object with `name` field (NOT a string)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name"
  }
}
```

### marketplace.json Schema

Required structure:
```json
{
  "plugins": [
    {
      "location": "plugins/<name>/.claude-plugin",
      "owner": "owner-name",
      "source": {
        "type": "git",
        "url": "https://github.com/owner/repo"
      }
    }
  ]
}
```

### File Location Rules

| Component | Location Pattern |
|-----------|------------------|
| Skills | `skills/<skill-name>/SKILL.md` |
| Agents | `agents/<agent-name>.md` |
| Commands | `commands/<command-name>.md` |
| Hooks | `hooks/hooks.json` + `hooks/*.py` |

### YAML Frontmatter Rules

**Skills:**
```yaml
---
name: skill-name
description: What this skill does
triggers:
  - trigger phrase 1
  - trigger phrase 2
---
```

**Agents:**
```yaml
---
name: agent-name
description: Agent description
tools:
  - Tool1
  - Tool2
---
```

**Commands:**
```yaml
---
name: command-name
description: Command description
allowed-tools:
  - Tool1
  - Tool2
---
```

### Cross-Reference Validation

1. **Skill → Agent pairs**: Skills that reference agents must have matching agents
2. **Hook → Script**: Hooks in hooks.json must point to existing scripts
3. **Command → Tools**: Commands must only list valid tool names

## Output Format

```
SCHEMA_CHECK_REPORT
===================

Checked: <number> components
Passed: <number>
Failed: <number>

RESULTS:

[PASS] plugin.json - All required fields present
[PASS] agents/my-agent.md - Valid frontmatter and content
[FAIL] skills/my-skill/SKILL.md - Missing 'triggers' field

ISSUES:
- skills/my-skill/SKILL.md: Missing required 'triggers' field in frontmatter

RECOMMENDATIONS:
- Add triggers field to skills/my-skill/SKILL.md
```

## Transition Conditions

To complete this phase:
1. All checked components must pass validation
2. No critical schema errors
3. Cross-references must be valid

Evidence required for workflow completion:
- `checked_count`: Number of components validated
- `passed_count`: Number passing validation
- `failed_count`: Number failing validation (must be 0)
