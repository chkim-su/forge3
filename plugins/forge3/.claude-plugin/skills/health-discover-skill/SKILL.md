---
name: health-discover-skill
description: Discovery phase for /health-check command - finds components for health analysis
triggers:
  - health-check discover phase
  - find components for health analysis
  - health discovery
---

# Health-Check Discovery Phase

The first phase of the `/health-check` workflow. Discovers all plugin components for health analysis.

## Purpose

Scan the plugin directory and identify all components that will undergo health analysis.

## Discovery Scope

This phase discovers the same components as verify-discover but with a focus on gathering metadata needed for health scoring:

| Component Type | Discovery Info |
|----------------|----------------|
| Skills | Path, name, trigger count, content length |
| Agents | Path, name, tool count, system prompt length |
| Commands | Path, name, tool count, documentation length |
| Hooks | Path, event types, script count |
| Manifests | Path, field completeness |

## Discovery Process

1. **Locate plugin root**: Find `.claude-plugin` directory
2. **Enumerate components**: List all component files
3. **Collect metadata**: Gather basic stats for scoring
4. **Prepare analysis queue**: Order components for analysis

## Output Format

```
HEALTH_DISCOVERY_REPORT
=======================

Plugin Root: plugins/my-plugin/.claude-plugin

COMPONENTS_FOR_ANALYSIS:

Skills (3):
- router-skill: 5 triggers, 1200 chars
- semantic-skill: 4 triggers, 980 chars
- execute-skill: 3 triggers, 850 chars

Agents (3):
- router-agent: 4 tools, 2000 chars
- semantic-agent: 5 tools, 1800 chars
- execute-agent: 6 tools, 2200 chars

Commands (2):
- assist: 6 tools, full docs
- verify: 4 tools, full docs

Hooks:
- 4 event handlers, 5 scripts

Total: 11 components ready for analysis
```

## Transition Evidence

To proceed to analyze phase, provide:
- `plugin_root`: Path to plugin root
- `components`: List of components with metadata
- `total_count`: Total components to analyze
