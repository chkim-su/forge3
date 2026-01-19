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

### plugin.json Template
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name"
  },
  "license": "MIT",
  "repository": "https://github.com/owner/repo",
  "keywords": ["keyword1", "keyword2"]
}
```

### marketplace.json Template
```json
{
  "$schema": "https://claude.ai/schemas/marketplace.json",
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": ".",
      "description": "Plugin description",
      "version": "1.0.0"
    }
  ]
}
```

**Important:** Do NOT use these invalid patterns:
- `"author": "string"` → Use `"owner": { "name": "string" }`
- `"path": "."` → Use `"source": "."`
- `"config": { ... }` → Not allowed in plugin entries

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
