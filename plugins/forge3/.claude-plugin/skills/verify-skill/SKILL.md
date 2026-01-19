---
name: verify-skill
triggers:
  - "verify component"
  - "validate implementation"
  - "check schema"
---

# Verify Skill

This skill provides exact schemas and validation rules for Claude Code plugin components.

## Exact Schemas

### plugin.json Schema

**Location:** `<plugin-root>/plugin.json`

```json
{
  "name": "string (required, kebab-case)",
  "version": "string (required, semver)",
  "description": "string (required)",
  "author": {
    "name": "string (required if author present)"
  },
  "license": "string (optional)",
  "repository": "string (optional, URL)",
  "keywords": ["array of strings (optional)"]
}
```

**✅ CORRECT plugin.json:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A plugin description",
  "author": {
    "name": "Developer Name"
  }
}
```

**❌ WRONG plugin.json examples:**
```json
// WRONG: author as string instead of object
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A plugin",
  "author": "Developer Name"  // ❌ Must be object: { "name": "..." }
}

// WRONG: missing required fields
{
  "name": "my-plugin"  // ❌ Missing version and description
}

// WRONG: invalid name format
{
  "name": "My Plugin",  // ❌ Must be kebab-case: "my-plugin"
  "version": "1.0.0",
  "description": "A plugin"
}
```

---

### marketplace.json Schema

**Location:** `<plugin-root>/.claude-plugin/marketplace.json`

```json
{
  "$schema": "string (optional, https://claude.ai/schemas/marketplace.json)",
  "name": "string (required, kebab-case)",
  "owner": {
    "name": "string (required)"
  },
  "metadata": {
    "description": "string (optional)",
    "version": "string (optional, semver)"
  },
  "plugins": [
    {
      "name": "string (required)",
      "source": "string (required, path or URL)",
      "description": "string (optional)",
      "version": "string (optional)"
    }
  ]
}
```

**✅ CORRECT marketplace.json:**
```json
{
  "$schema": "https://claude.ai/schemas/marketplace.json",
  "name": "my-marketplace",
  "owner": {
    "name": "Team Name"
  },
  "metadata": {
    "description": "Marketplace description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./",
      "description": "Plugin description",
      "version": "1.0.0"
    }
  ]
}
```

**❌ WRONG marketplace.json examples:**
```json
// WRONG #1: "author" instead of "owner"
{
  "name": "my-marketplace",
  "author": "Team Name",  // ❌ WRONG: Use "owner": { "name": "..." }
  "plugins": []
}

// WRONG #2: "owner" as string instead of object
{
  "name": "my-marketplace",
  "owner": "Team Name",  // ❌ WRONG: Must be object with "name" field
  "plugins": []
}

// WRONG #3: "path" instead of "source" in plugins
{
  "name": "my-marketplace",
  "owner": { "name": "Team" },
  "plugins": [
    {
      "name": "plugin",
      "path": "."  // ❌ WRONG: Use "source": "./"
    }
  ]
}

// WRONG #4: "config" object in plugins (not allowed)
{
  "name": "my-marketplace",
  "owner": { "name": "Team" },
  "plugins": [
    {
      "path": ".",
      "config": {  // ❌ WRONG: "config" is not allowed
        "name": "plugin",
        "version": "1.0.0"
      }
    }
  ]
}

// WRONG #5: Extra fields not in schema
{
  "name": "my-marketplace",
  "owner": { "name": "Team" },
  "displayName": "My Marketplace",  // ❌ WRONG: Not in schema
  "license": "MIT",                  // ❌ WRONG: Not in schema
  "repository": "https://...",       // ❌ WRONG: Not in schema
  "keywords": [],                    // ❌ WRONG: Not in schema
  "categories": [],                  // ❌ WRONG: Not in schema
  "requirements": {},                // ❌ WRONG: Not in schema
  "installation": {},                // ❌ WRONG: Not in schema
  "plugins": []
}
```

---

### Agent Schema

**Location:** `<plugin-root>/agents/<agent-name>.md`

```yaml
---
name: string (required, kebab-case)
description: string (required, when to use this agent)
tools:
  - ToolName (required, array)
model: string (optional: haiku, sonnet, opus)
color: string (optional: blue, cyan, green, yellow, magenta, red)
---

# System Prompt Content
```

**✅ CORRECT agent:**
```yaml
---
name: my-agent
description: Use this agent when analyzing code quality
tools:
  - Read
  - Grep
  - Glob
model: haiku
color: blue
---

# My Agent

You are a code analysis agent...
```

**❌ WRONG agent examples:**
```yaml
# WRONG: File at wrong location
# Location: agents/my-agent/agent.md  ❌
# Correct:  agents/my-agent.md  ✅

# WRONG: Missing required fields
---
name: my-agent
# ❌ Missing description and tools
---

# WRONG: tools as string instead of array
---
name: my-agent
description: An agent
tools: Read, Grep  # ❌ Must be array: ["Read", "Grep"]
---

# WRONG: allowed_tools instead of tools
---
name: my-agent
description: An agent
allowed_tools:  # ❌ WRONG: Use "tools" not "allowed_tools"
  - Read
---
```

---

### Command Schema

**Location:** `<plugin-root>/commands/<command-name>.md`

```yaml
---
name: string (required, kebab-case)
description: string (required)
allowed-tools:
  - ToolName (optional, array, kebab-case field name!)
argument-hint: string (optional)
---

# Command Content
```

**✅ CORRECT command:**
```yaml
---
name: my-command
description: Runs my command
allowed-tools:
  - Read
  - Write
argument-hint: "<file-path>"
---

# /my-command

Instructions for the command...
```

**❌ WRONG command examples:**
```yaml
# WRONG: allowed_tools (underscore) instead of allowed-tools (hyphen)
---
name: my-command
description: A command
allowed_tools:  # ❌ WRONG: Use "allowed-tools" (kebab-case)
  - Read
---

# WRONG: File at wrong location
# Location: commands/my-command/command.md  ❌
# Correct:  commands/my-command.md  ✅
```

---

### Skill Schema

**Location:** `<plugin-root>/skills/<skill-name>/SKILL.md`

```yaml
---
name: string (required, kebab-case)
triggers:
  - string (required, array of trigger phrases)
---

# Skill Content
```

**✅ CORRECT skill:**
```yaml
---
name: my-skill
triggers:
  - "use my skill"
  - "activate skill"
---

# My Skill

Skill content...
```

**❌ WRONG skill examples:**
```yaml
# WRONG: File at wrong location
# Location: skills/my-skill.md  ❌
# Correct:  skills/my-skill/SKILL.md  ✅

# WRONG: triggers as string
---
name: my-skill
triggers: "use my skill"  # ❌ Must be array
---

# WRONG: Missing SKILL.md filename
# Location: skills/my-skill/index.md  ❌
# Correct:  skills/my-skill/SKILL.md  ✅
```

---

### hooks.json Schema

**Location:** `<plugin-root>/hooks/hooks.json`

```json
{
  "$schema": "https://claude.ai/schemas/hooks.json",
  "description": "string (optional)",
  "hooks": {
    "EventName": [
      {
        "matcher": "string (optional, regex pattern)",
        "hooks": [
          {
            "type": "command",
            "command": "string (required, with ${CLAUDE_PLUGIN_ROOT})",
            "timeout": "number (optional, seconds)"
          }
        ]
      }
    ]
  }
}
```

**Event names:** `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `PreCompact`, `Notification`

**✅ CORRECT hooks.json:**
```json
{
  "$schema": "https://claude.ai/schemas/hooks.json",
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

**❌ WRONG hooks.json examples:**
```json
// WRONG #1: hooks as array instead of object
{
  "hooks": [  // ❌ Must be object keyed by event name
    {
      "event": "PreToolUse",
      "matcher": "^Bash$",
      "command": "..."
    }
  ]
}

// WRONG #2: Using "event" field instead of object key
{
  "hooks": {
    "PreToolUse": [
      {
        "event": "PreToolUse",  // ❌ Don't use event field, it's the object key
        "hooks": [...]
      }
    ]
  }
}

// WRONG #3: Missing nested "hooks" array
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "command": "..."  // ❌ Must be inside hooks array with type
      }
    ]
  }
}

// WRONG #4: Missing "type": "command"
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "command": "python3 script.py"  // ❌ Missing "type": "command"
          }
        ]
      }
    ]
  }
}

// WRONG #5: Hardcoded path
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

## Directory Structure

**✅ CORRECT plugin structure:**
```
my-plugin/
├── plugin.json                      # Required at root
├── .claude-plugin/
│   └── marketplace.json             # If publishing to marketplace
├── agents/
│   └── my-agent.md                  # Direct file, not subdirectory
├── commands/
│   └── my-command.md                # Direct file, not subdirectory
├── skills/
│   └── my-skill/
│       └── SKILL.md                 # Must be SKILL.md in subdirectory
└── hooks/
    ├── hooks.json                   # Hook configuration
    └── my-hook.py                   # Hook scripts
```

**❌ WRONG directory structures:**
```
# WRONG: Agent in subdirectory
agents/my-agent/agent.md  ❌
agents/my-agent.md        ✅

# WRONG: Command in subdirectory
commands/my-command/command.md  ❌
commands/my-command.md          ✅

# WRONG: Skill as direct file
skills/my-skill.md              ❌
skills/my-skill/SKILL.md        ✅

# WRONG: Skill with wrong filename
skills/my-skill/index.md        ❌
skills/my-skill/skill.md        ❌
skills/my-skill/SKILL.md        ✅

# WRONG: Missing plugin.json at root
my-plugin/
├── .claude-plugin/
│   └── marketplace.json   # ❌ plugin.json missing at root!
└── agents/
```

---

## Verification Commands

```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('file.json'))"

# Validate YAML frontmatter
python3 -c "import yaml; yaml.safe_load(open('file.md').read().split('---')[1])"

# Validate Python syntax
python3 -m py_compile file.py

# Check file exists
test -f path/to/file && echo "EXISTS" || echo "MISSING"
```

---

## Quick Reference: Common Mistakes

| Wrong | Correct |
|-------|---------|
| `"author": "Name"` | `"owner": { "name": "Name" }` |
| `"path": "."` | `"source": "./"` |
| `"config": { ... }` | Not allowed in plugins array |
| `allowed_tools:` | `allowed-tools:` |
| `agents/x/agent.md` | `agents/x.md` |
| `skills/x.md` | `skills/x/SKILL.md` |
| `tools: Read, Grep` | `tools: [Read, Grep]` |
| `"hooks": [...]` (array) | `"hooks": { "EventName": [...] }` (object) |
| Missing `"type": "command"` | Always include in hook command |

---

## Marketplace Cross-Validation

When validating a marketplace.json, perform these additional cross-checks:

### 1. Plugin Source Path Validation
For each plugin in the `plugins` array:
- The `source` path must point to a directory containing a valid `plugin.json`
- Resolve relative paths from the marketplace.json location

### 2. Name Consistency Check
- Plugin `name` in marketplace.json must match the `name` field in the corresponding plugin.json
- Report mismatches as validation errors

### 3. Invalid Fields Detection
The following fields are NOT allowed in marketplace.json:
- `author` at root level (use `owner` instead)
- `path` in plugins (use `source` instead)
- `config` object in plugins

Validation should fail if any of these invalid fields are present.

### Cross-Validation Commands

```bash
# Check plugin.json exists at source path
SOURCE_PATH="./path/to/plugin"
test -f "${SOURCE_PATH}/plugin.json" && echo "EXISTS" || echo "MISSING"

# Extract and compare names
MARKETPLACE_NAME=$(python3 -c "import json; print(json.load(open('marketplace.json'))['plugins'][0]['name'])")
PLUGIN_NAME=$(python3 -c "import json; print(json.load(open('${SOURCE_PATH}/plugin.json'))['name'])")
[ "$MARKETPLACE_NAME" = "$PLUGIN_NAME" ] && echo "MATCH" || echo "MISMATCH: $MARKETPLACE_NAME vs $PLUGIN_NAME"
```
