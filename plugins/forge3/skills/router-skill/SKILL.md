---
name: router-skill
triggers:
  - "route request"
  - "classify intent"
  - "workflow routing"
---

# Router Skill

This skill provides guidance for routing user requests within the Forge3 workflow system.

## When to Use

Use this skill when you need to:
- Classify a user's intent for component creation
- Route a request to the appropriate workflow phase
- Understand the routing decision-making process

## Intent Classification

The router classifies requests into these categories:

| Category | Description | Key Indicators |
|----------|-------------|----------------|
| `create_skill` | Create a new skill | "skill", "SKILL.md", "triggers" |
| `create_agent` | Create a new agent | "agent", "subagent", "autonomous" |
| `create_command` | Create a slash command | "command", "/xyz", "slash" |
| `create_hook` | Create a hook | "hook", "PreToolUse", "event" |
| `modify_existing` | Modify existing component | "update", "fix", "change" |
| `verify` | Verify components | "verify", "validate", "check" |

## Routing Process

1. **Parse the request** - Extract key terms and context
2. **Match to category** - Use indicators to classify
3. **Set confidence** - High/Medium/Low based on clarity
4. **Output decision** - Structured routing result

## Output Format

```
INTENT_CLASSIFICATION:
- category: <category>
- confidence: <high|medium|low>
- reasoning: <brief explanation>

RECOMMENDED_NEXT_PHASE: semantic
```

## Important Notes

- Routing does NOT create files
- Routing does NOT make implementation decisions
- Routing ONLY classifies and directs
- When uncertain, set confidence to "low"
