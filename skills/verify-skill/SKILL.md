---
name: verify-skill
triggers:
  - "verify component"
  - "validate implementation"
  - "check schema"
---

# Verify Skill

This skill provides guidance for verifying implementations within the Forge3 workflow system.

## When to Use

Use this skill when you need to:
- Validate a created component
- Check schema compliance
- Test basic functionality

## Validation Checklists

### Skill Validation
- [ ] File exists at `skills/<name>/SKILL.md`
- [ ] YAML frontmatter is valid
- [ ] `name` field present
- [ ] `triggers` field has entries
- [ ] Content sections present

### Agent Validation
- [ ] File exists at `agents/<name>.md`
- [ ] YAML frontmatter is valid
- [ ] `name` field present
- [ ] `description` field present
- [ ] `tools` field lists tools
- [ ] System prompt meaningful

### Command Validation
- [ ] File exists at `commands/<name>.md`
- [ ] YAML frontmatter is valid
- [ ] `name` field present
- [ ] `description` field present
- [ ] Implementation present

### Hook Validation
- [ ] Entry in `hooks/hooks.json`
- [ ] JSON is valid
- [ ] Script exists and is valid Python
- [ ] Exit codes used correctly

## Verification Commands

```bash
# YAML validation
python3 -c "import yaml; yaml.safe_load(open('file.md'))"

# Python validation
python3 -m py_compile file.py

# JSON validation
python3 -c "import json; json.load(open('file.json'))"
```

## Verification Process

1. **Check structure** - Files in correct locations
2. **Validate schema** - Required fields present
3. **Test syntax** - Valid YAML/Python/JSON
4. **Report results** - Pass/Fail with details

## Output Format

```
VERIFICATION_RESULTS:
- component: <name>
- status: <pass|fail>

CHECKS_PERFORMED:
- <check>: <pass|fail>

WORKFLOW_STATUS: <complete|needs_fixes>
```

## Important Notes

- Verify does NOT modify files
- Verify ONLY reads and validates
- Report actual issues, not preferences
- Mark complete only when all checks pass
