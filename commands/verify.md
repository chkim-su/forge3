---
name: verify
description: Verify and validate plugin components for schema compliance
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
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

## Validation Checks

### Skills
- YAML frontmatter syntax
- Required fields: name, triggers
- Content structure

### Agents
- YAML frontmatter syntax
- Required fields: name, description, tools
- System prompt presence

### Commands
- YAML frontmatter syntax
- Required fields: name, description
- Implementation content

### Hooks
- JSON syntax in hooks.json
- Python syntax in hook scripts
- Valid event types
- Correct exit codes

## Output

```
VERIFICATION REPORT
==================

Component: skills/my-skill
Status: PASS

Checks:
[PASS] File exists
[PASS] YAML valid
[PASS] name field present
[PASS] triggers field present
[PASS] Content structure valid

Issues: None
Recommendations: None
```

## Exit Codes

- 0: All checks passed
- 1: Some checks failed
- 2: Critical errors found

## Integration

This command can be used:
- Manually to check components
- As part of the /assist workflow (verify phase)
- In CI/CD pipelines for validation

## Related

- `/assist` - Create components with guided workflow
