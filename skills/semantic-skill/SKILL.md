---
name: semantic-skill
triggers:
  - "semantic analysis"
  - "component structure"
  - "plan implementation"
---

# Semantic Skill

This skill provides guidance for semantic analysis and implementation planning within the Forge3 workflow system.

## When to Use

Use this skill when you need to:
- Analyze a classified intent for detailed requirements
- Plan the structure of a component
- Design file organization and content outline

## Component Structures

### Skills
```
skills/<skill-name>/SKILL.md
```
Required: name, triggers, description, usage

### Agents
```
agents/<agent-name>.md
```
Required: name, description, tools, system prompt

### Commands
```
commands/<command-name>.md
```
Required: name, description, implementation

### Hooks
```
hooks/hooks.json (entry)
hooks/<hook-name>.py
```
Required: event, matcher, handler script

## Planning Process

1. **Analyze intent** - Understand specific requirements
2. **Research patterns** - Look at existing components
3. **Design structure** - Plan files and content
4. **Output plan** - Structured implementation plan

## Output Format

```
COMPONENT_ANALYSIS:
- type: <skill|agent|command|hook>
- name: <component-name>

STRUCTURE_PLAN:
- files_to_create: <list>
- files_to_modify: <list>

RECOMMENDED_NEXT_PHASE: execute
```

## Important Notes

- Planning does NOT create files
- Planning does NOT write content
- Planning ONLY designs structure
- Reference existing components for consistency
