---
name: execute-skill
triggers:
  - "execute implementation"
  - "create component"
  - "generate files"
---

# Execute Skill

This skill provides exact templates and file locations for creating Claude Code plugin components.

## Two Distribution Models

### Model A: Standalone Plugin (Local Development)
For plugins installed via local path or symlink.

```
my-plugin/
├── plugin.json           # At root
├── agents/
├── commands/
├── skills/
└── hooks/
```

### Model B: Marketplace (GitHub Distribution)
For plugins distributed via `/plugin add github:owner/repo`.

```
my-marketplace/
├── marketplace.json      # At ROOT of repo
├── README.md
├── LICENSE
└── plugins/
    └── my-plugin/
        └── .claude-plugin/
            ├── plugin.json
            ├── agents/
            ├── commands/
            ├── skills/
            └── hooks/
```

**CRITICAL:** In a marketplace, all plugin content goes inside `plugins/<name>/.claude-plugin/`, NOT at repo root!

---

## File Location Rules

### For Standalone Plugin (Model A)

| Component | Location | Example |
|-----------|----------|---------|
| plugin.json | `<root>/plugin.json` | `my-plugin/plugin.json` |
| Agent | `<root>/agents/<name>.md` | `my-plugin/agents/my-agent.md` |
| Command | `<root>/commands/<name>.md` | `my-plugin/commands/my-command.md` |
| Skill | `<root>/skills/<name>/SKILL.md` | `my-plugin/skills/my-skill/SKILL.md` |
| Hook config | `<root>/hooks/hooks.json` | `my-plugin/hooks/hooks.json` |
| Hook script | `<root>/hooks/<name>.py` | `my-plugin/hooks/my-hook.py` |

### For Marketplace (Model B)

| Component | Location | Example |
|-----------|----------|---------|
| marketplace.json | `<repo-root>/marketplace.json` | `my-marketplace/marketplace.json` |
| plugin.json | `<repo>/plugins/<name>/.claude-plugin/plugin.json` | `my-marketplace/plugins/my-plugin/.claude-plugin/plugin.json` |
| Agent | `<repo>/plugins/<name>/.claude-plugin/agents/<agent>.md` | `.../agents/my-agent.md` |
| Command | `<repo>/plugins/<name>/.claude-plugin/commands/<cmd>.md` | `.../commands/my-cmd.md` |
| Skill | `<repo>/plugins/<name>/.claude-plugin/skills/<skill>/SKILL.md` | `.../skills/my-skill/SKILL.md` |
| Hooks | `<repo>/plugins/<name>/.claude-plugin/hooks/` | `.../hooks/hooks.json` |

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

**Location:** `<repo-root>/marketplace.json` (at repository ROOT, NOT inside .claude-plugin!)

**IMPORTANT:** Use this ONLY for Model B (Marketplace distribution).

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
      "name": "my-plugin",
      "source": "plugins/my-plugin/.claude-plugin",
      "description": "Plugin description",
      "version": "1.0.0"
    }
  ]
}
```

**❌ WRONG - Do NOT create like this:**
```json
// WRONG #1: marketplace.json in wrong location
// ❌ my-plugin/.claude-plugin/marketplace.json  (WRONG!)
// ✅ my-marketplace/marketplace.json            (CORRECT - at repo root)

// WRONG #2: source pointing to root instead of plugin directory
{
  "plugins": [{
    "name": "my-plugin",
    "source": "./"  // ❌ WRONG for marketplace - use "plugins/my-plugin/.claude-plugin"
  }]
}

// WRONG #3: Using "author" instead of "owner"
{
  "name": "my-marketplace",
  "author": "Name",  // ❌ Use "owner": { "name": "Name" }
  "plugins": []
}

// WRONG #4: Using "path" instead of "source"
{
  "plugins": [{
    "path": ".",  // ❌ Use "source": "plugins/name/.claude-plugin"
    "config": {}  // ❌ "config" not allowed
  }]
}

// WRONG #5: Adding fields not in schema
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

**IMPORTANT:** `hooks` must be an **object keyed by event name**, NOT an array!

```json
{
  "$schema": "https://claude.ai/schemas/hooks.json",
  "description": "My plugin hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/validate.py",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "^/my-command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/init.py",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/stop.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**Available events:** `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`

**❌ WRONG - These patterns are INVALID:**
```json
// WRONG #1: hooks as array (VERY COMMON MISTAKE!)
{
  "hooks": [  // ❌ WRONG: Must be object, not array
    {
      "event": "PreToolUse",
      "command": "..."
    }
  ]
}

// WRONG #2: Missing nested "hooks" array and "type"
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "command": "..."  // ❌ Must be inside hooks array with type: command
      }
    ]
  }
}

// WRONG #3: Hardcoded path
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 /home/user/hooks/script.py"  // ❌ Use ${CLAUDE_PLUGIN_ROOT}
          }
        ]
      }
    ]
  }
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

### Model A: Standalone Plugin

**✅ CORRECT structure:**
```
my-plugin/
├── plugin.json                      # REQUIRED at root
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

### Model B: Marketplace (GitHub Distribution)

**✅ CORRECT structure:**
```
my-marketplace/                      # Repository root
├── marketplace.json                 # At ROOT (defines plugins)
├── README.md
├── LICENSE
└── plugins/
    └── my-plugin/
        └── .claude-plugin/          # Plugin content HERE
            ├── plugin.json          # Required
            ├── agents/
            │   └── my-agent.md
            ├── commands/
            │   └── my-cmd.md
            ├── skills/
            │   └── my-skill/
            │       └── SKILL.md
            └── hooks/
                ├── hooks.json
                └── my-hook.py
```

**❌ WRONG marketplace structures:**
```
# WRONG: Plugin content at repo root (not in plugins/ directory)
my-marketplace/
├── marketplace.json
├── plugin.json                      # ❌ Should be in plugins/<name>/.claude-plugin/
├── agents/                          # ❌ Should be in plugins/<name>/.claude-plugin/
└── skills/                          # ❌ Should be in plugins/<name>/.claude-plugin/

# WRONG: marketplace.json inside .claude-plugin
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json             # ❌ Should be at repo root
└── plugins/

# WRONG: Missing .claude-plugin directory
my-marketplace/
├── marketplace.json
└── plugins/
    └── my-plugin/
        ├── plugin.json              # ❌ Missing .claude-plugin/ wrapper
        └── agents/
```

**❌ General WRONG structures:**
```
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
| `.claude-plugin/marketplace.json` | `marketplace.json` at repo root | marketplace location |
| `"source": "./"` (for marketplace) | `"source": "plugins/name/.claude-plugin"` | marketplace.json |
| Plugin content at repo root | Inside `plugins/<name>/.claude-plugin/` | marketplace structure |
| `"author": "Name"` | `"owner": { "name": "Name" }` | marketplace.json |
| `"path": "."` | `"source": "plugins/name/.claude-plugin"` | marketplace.json |
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
| `"hooks": [...]` (array) | `"hooks": { "EventName": [...] }` | hooks.json |
| Missing `"type": "command"` | Required in hook command object | hooks.json |

---

## Execution Process

1. **Check location rules** - Use correct file paths
2. **Use exact templates** - Copy and modify
3. **Avoid wrong patterns** - Check the ❌ examples
4. **Verify before completing** - Use verify-skill
