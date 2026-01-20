---
name: verify-discover-skill
description: Discovery phase for /assist:verify command - finds all components to validate
triggers:
  - verify discover phase
  - find components to verify
  - component discovery for validation
---

# Verify Discovery Phase

The first phase of the `/assist:verify` workflow. Discovers all plugin components that need validation.

## Purpose

Scan the plugin directory structure and identify all components that require schema validation.

## Discovery Targets

| Component Type | Search Pattern | Expected Structure |
|----------------|----------------|-------------------|
| Skills | `skills/*/SKILL.md` | Directory with SKILL.md |
| Agents | `agents/*.md` | Markdown files |
| Commands | `commands/*.md` | Markdown files |
| Hooks | `hooks/hooks.json` | JSON config + Python scripts |
| Plugin Manifest | `plugin.json` | Root manifest |
| Marketplace | `marketplace.json` | Optional marketplace config |

## Discovery Process

1. **Locate plugin root**: Find `.claude-plugin` directory
2. **Scan directories**: Check each component directory
3. **Catalog files**: Record path, type, and basic info for each component
4. **Verify existence**: Confirm files actually exist and are readable

## Output Format

```
DISCOVERY_REPORT
================

Plugin Root: plugins/my-plugin/.claude-plugin

COMPONENTS_FOUND:

Skills:
- skills/router-skill/SKILL.md
- skills/semantic-skill/SKILL.md

Agents:
- agents/router-agent.md
- agents/semantic-agent.md

Commands:
- commands/assist-wizard.md
- commands/assist-verify.md

Hooks:
- hooks/hooks.json
- hooks/workflow_hook.py
- hooks/phase_hook.py

Manifests:
- plugin.json
- marketplace.json (optional)

Total: <count> components
```

## Transition Evidence

To proceed to the validate phase, provide:
- `plugin_root`: Path to plugin root
- `components_found`: List of discovered components with types
- `total_count`: Total number of components to validate
