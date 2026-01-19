---
name: execute-skill
triggers:
  - "execute implementation"
  - "create component"
  - "generate files"
---

# Execute Skill

This skill provides exact templates and file locations for creating Claude Code plugin components.

## File Location Rules

| Component | Location | Example |
|-----------|----------|---------|
| plugin.json | `<root>/plugin.json` | `my-plugin/plugin.json` |
| marketplace.json | `<root>/.claude-plugin/marketplace.json` | `my-plugin/.claude-plugin/marketplace.json` |
| Agent | `<root>/agents/<name>.md` | `my-plugin/agents/my-agent.md` |
| Command | `<root>/commands/<name>.md` | `my-plugin/commands/my-command.md` |
| Skill | `<root>/skills/<name>/SKILL.md` | `my-plugin/skills/my-skill/SKILL.md` |
| Hook config | `<root>/hooks/hooks.json` | `my-plugin/hooks/hooks.json` |
| Hook script | `<root>/hooks/<name>.py` | `my-plugin/hooks/my-hook.py` |

---

## Exact Templates

### plugin.json

**Location:** `<plugin-root>/plugin.json` (REQUIRED)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Author Name"
  },
  "license": "MIT",
  "repository": "https://github.com/owner/repo",
  "keywords": ["keyword1", "keyword2"]
}
```

**❌ WRONG - Do NOT create like this:**
```json
{
  "name": "my-plugin",
  "author": "Author Name"  // ❌ Must be object: { "name": "..." }
}
```

---

### marketplace.json

**Location:** `<plugin-root>/.claude-plugin/marketplace.json`

```json
{
  "$schema": "https://claude.ai/schemas/marketplace.json",
  "name": "my-marketplace",
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

**❌ WRONG - Do NOT create like this:**
```json
// WRONG #1: Using "author" instead of "owner"
{
  "name": "my-marketplace",
  "author": "Name",  // ❌ Use "owner": { "name": "Name" }
  "plugins": []
}

// WRONG #2: Using "path" instead of "source"
{
  "plugins": [{
    "path": ".",  // ❌ Use "source": "."
    "config": {}  // ❌ "config" not allowed
  }]
}

// WRONG #3: Adding fields not in schema
{
  "displayName": "...",  // ❌ Not in schema
  "license": "MIT",      // ❌ Not in schema
  "repository": "...",   // ❌ Not in schema
  "keywords": [],        // ❌ Not in schema
  "categories": [],      // ❌ Not in schema
  "requirements": {},    // ❌ Not in schema
  "installation": {}     // ❌ Not in schema
}
```

---

### Agent

**Location:** `<plugin-root>/agents/<agent-name>.md` (NOT in subdirectory!)

```yaml
---
name: my-agent
description: Use this agent when you need to analyze code quality
tools:
  - Read
  - Grep
  - Glob
model: haiku
color: blue
---

# My Agent

You are a specialized agent for...

## Your Responsibilities

1. Task one
2. Task two

## Important Rules

- Rule one
- Rule two
```

**❌ WRONG locations:**
```
agents/my-agent/agent.md     ❌ Wrong: subdirectory
agents/my-agent/AGENT.md     ❌ Wrong: subdirectory
agents/my-agent.md           ✅ Correct
```

**❌ WRONG frontmatter:**
```yaml
---
name: my-agent
allowed_tools:  # ❌ Use "tools" not "allowed_tools"
  - Read
---
```

---

### Command

**Location:** `<plugin-root>/commands/<command-name>.md` (NOT in subdirectory!)

```yaml
---
name: my-command
description: What this command does
allowed-tools:
  - Read
  - Write
  - Bash
argument-hint: "<file-path>"
---

# /my-command

Instructions for implementing this command...
```

**❌ WRONG locations:**
```
commands/my-command/command.md  ❌ Wrong: subdirectory
commands/my-command.md          ✅ Correct
```

**❌ WRONG frontmatter:**
```yaml
---
name: my-command
allowed_tools:  # ❌ Use "allowed-tools" (kebab-case with hyphen)
  - Read
---
```

---

### Skill

**Location:** `<plugin-root>/skills/<skill-name>/SKILL.md` (MUST be in subdirectory, MUST be named SKILL.md)

```yaml
---
name: my-skill
triggers:
  - "use my skill"
  - "my skill please"
  - "activate skill"
---

# My Skill

Skill content goes here...

## Section One

Content...

## Section Two

Content...
```

**❌ WRONG locations:**
```
skills/my-skill.md            ❌ Wrong: not in subdirectory
skills/my-skill/skill.md      ❌ Wrong: lowercase filename
skills/my-skill/index.md      ❌ Wrong: wrong filename
skills/my-skill/SKILL.md      ✅ Correct
```

**❌ WRONG frontmatter:**
```yaml
---
name: my-skill
triggers: "single trigger"  # ❌ Must be array
---
```

---

### hooks.json

**Location:** `<plugin-root>/hooks/hooks.json`

```json
{
  "$schema": "https://claude.ai/schemas/hooks.json",
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "^Bash$",
      "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/validate.py"
    },
    {
      "event": "UserPromptSubmit",
      "matcher": "^/my-command",
      "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/init.py"
    }
  ]
}
```

**Available events:** `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`

**❌ WRONG:**
```json
// WRONG: hooks as object instead of array
{
  "hooks": {
    "PreToolUse": { ... }  // ❌ Must be array
  }
}

// WRONG: Hardcoded path
{
  "hooks": [{
    "event": "PreToolUse",
    "command": "python3 /home/user/hooks/script.py"  // ❌ Use ${CLAUDE_PLUGIN_ROOT}
  }]
}
```

---

### Hook Script (Python)

**Location:** `<plugin-root>/hooks/<hook-name>.py`

```python
#!/usr/bin/env python3
"""Hook script for [purpose]."""
import json
import sys

def main():
    """Main hook handler."""
    try:
        input_data = json.load(sys.stdin)

        # Process input_data...
        # input_data contains event-specific fields

        # Exit codes:
        # 0 = allow (continue)
        # 2 = block (prevent action)
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(0)  # Allow on error (fail-open)

if __name__ == "__main__":
    main()
```

---

## Directory Structure

**✅ CORRECT structure:**
```
my-plugin/
├── plugin.json                      # REQUIRED at root
├── .claude-plugin/
│   └── marketplace.json             # Optional, for marketplace
├── agents/
│   ├── agent-one.md                 # Direct .md file
│   └── agent-two.md
├── commands/
│   ├── command-one.md               # Direct .md file
│   └── command-two.md
├── skills/
│   ├── skill-one/
│   │   └── SKILL.md                 # MUST be SKILL.md
│   └── skill-two/
│       └── SKILL.md
└── hooks/
    ├── hooks.json                   # Hook configuration
    ├── hook-one.py
    └── hook-two.py
```

**❌ WRONG structures:**
```
# Missing plugin.json
my-plugin/
├── .claude-plugin/marketplace.json  # ❌ No plugin.json!
└── agents/

# Agent in subdirectory
agents/my-agent/agent.md             # ❌ Wrong
agents/my-agent.md                   # ✅ Correct

# Command in subdirectory
commands/my-cmd/command.md           # ❌ Wrong
commands/my-cmd.md                   # ✅ Correct

# Skill as direct file
skills/my-skill.md                   # ❌ Wrong
skills/my-skill/SKILL.md             # ✅ Correct

# Skill with wrong filename
skills/my-skill/skill.md             # ❌ Wrong (lowercase)
skills/my-skill/index.md             # ❌ Wrong (wrong name)
skills/my-skill/SKILL.md             # ✅ Correct
```

---

## Quick Reference: Common Mistakes

| Wrong | Correct | Component |
|-------|---------|-----------|
| `"author": "Name"` | `"owner": { "name": "Name" }` | marketplace.json |
| `"path": "."` | `"source": "."` | marketplace.json |
| `"config": { ... }` | Not allowed | marketplace.json |
| `displayName`, `license`, `repository` in marketplace | Remove them | marketplace.json |
| `allowed_tools:` | `allowed-tools:` | commands |
| `agents/x/agent.md` | `agents/x.md` | agents |
| `commands/x/cmd.md` | `commands/x.md` | commands |
| `skills/x.md` | `skills/x/SKILL.md` | skills |
| `skills/x/skill.md` | `skills/x/SKILL.md` | skills |
| `tools: Read, Grep` | `tools: [Read, Grep]` | agents |
| `triggers: "phrase"` | `triggers: ["phrase"]` | skills |
| Hardcoded paths in hooks | `${CLAUDE_PLUGIN_ROOT}/...` | hooks |

---

## Execution Process

1. **Check location rules** - Use correct file paths
2. **Use exact templates** - Copy and modify
3. **Avoid wrong patterns** - Check the ❌ examples
4. **Verify before completing** - Use verify-skill
