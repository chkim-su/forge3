---
name: execute-skill
triggers:
  - "execute implementation"
  - "create component"
  - "generate files"
---

# Execute Skill

This skill provides guidance for executing implementations within the Forge3 workflow system.

## When to Use

Use this skill when you need to:
- Implement a component based on a semantic plan
- Create actual files with content
- Follow project conventions

## Implementation Templates

### Skill Template
```yaml
---
name: skill-name
triggers:
  - "trigger phrase"
---

# Skill Title

Description and usage instructions.
```

### Agent Template
```yaml
---
name: agent-name
description: When to use this agent
tools:
  - Tool1
  - Tool2
---

# Agent Title

System prompt and responsibilities.
```

### Command Template
```yaml
---
name: command-name
description: What this command does
---

# /command-name

Implementation instructions.
```

### Hook Template (Python)
```python
#!/usr/bin/env python3
import json
import sys

def main():
    input_data = json.load(sys.stdin)
    # Process...
    sys.exit(0)  # Allow

if __name__ == "__main__":
    main()
```

## Execution Process

1. **Follow the plan** - Implement exactly as designed
2. **Write content** - Create high-quality files
3. **Verify syntax** - Ensure valid YAML/Python/etc.
4. **Report results** - Document what was created

## Output Format

```
IMPLEMENTATION_COMPLETE:
- files_created: <list>
- files_modified: <list>

RECOMMENDED_NEXT_PHASE: verify
```

## Important Notes

- Execute ONLY follows the plan
- Execute DOES create files
- Execute maintains project conventions
- Always verify syntax before completing
