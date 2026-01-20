#!/usr/bin/env python3
"""
Injection Metadata - Read-only skill injection hints for workflow phases.

IMPORTANT: This is NOT authoritative workflow policy.
Policy comes from the workflow daemon (workflow-daemon).
This module provides read-only hints for skill/agent injection only.
"""

from typing import Optional, Dict

# Read-only metadata for skill injection
# Policy comes from daemon, this is just injection hints

# Map generic phase names to their skill directory names
PHASE_SKILL_MAP: Dict[str, Optional[str]] = {
    # Common phases
    "router": "router-skill",
    "semantic": "semantic-skill",
    "execute": "execute-skill",
    "schema-check": "schema-check-skill",
    # Phases that vary by command (resolved via COMMAND_PHASE_SKILLS)
    "discover": None,
    "validate": None,
    "connectivity": None,
    "analyze": None,
    "aggregate": None,
}

# Command-specific phase-to-skill mappings
# Used when PHASE_SKILL_MAP returns None for a phase
COMMAND_PHASE_SKILLS: Dict[str, Dict[str, str]] = {
    "assist:verify": {
        "discover": "verify-discover-skill",
        "validate": "verify-validate-skill",
        "connectivity": "verify-connectivity-skill",
    },
    "assist:health-check": {
        "discover": "health-discover-skill",
        "analyze": "health-analyze-skill",
        "aggregate": "health-aggregate-skill",
    },
}

# Map phase names to their required agent
PHASE_AGENT_MAP: Dict[str, Optional[str]] = {
    # Common phases
    "router": "router-agent",
    "semantic": "semantic-agent",
    "execute": "execute-agent",
    "schema-check": "schema-check-agent",
    # Phases that vary by command (resolved via COMMAND_PHASE_AGENTS)
    "discover": None,
    "validate": None,
    "connectivity": None,
    "analyze": None,
    "aggregate": None,
}

# Command-specific phase-to-agent mappings
COMMAND_PHASE_AGENTS: Dict[str, Dict[str, str]] = {
    "assist:verify": {
        "discover": "verify-discovery-agent",
        "validate": "verify-validate-agent",
        "connectivity": "verify-connectivity-agent",
    },
    "assist:health-check": {
        "discover": "health-discovery-agent",
        "analyze": "health-analyze-agent",
        "aggregate": "health-aggregate-agent",
    },
}


def get_skill_for_phase(phase: str, command: Optional[str] = None) -> Optional[str]:
    """Get the skill name for a given phase.
    
    Args:
        phase: The phase name
        command: Optional command name for command-specific phases
        
    Returns:
        Skill directory name, or None if not found
    """
    # First check generic mapping
    skill = PHASE_SKILL_MAP.get(phase)
    if skill:
        return skill
    
    # Then check command-specific mapping
    if command and command in COMMAND_PHASE_SKILLS:
        return COMMAND_PHASE_SKILLS[command].get(phase)
    
    return None


def get_agent_for_phase(phase: str, command: Optional[str] = None) -> Optional[str]:
    """Get the agent name for a given phase.
    
    Args:
        phase: The phase name
        command: Optional command name for command-specific phases
        
    Returns:
        Agent name, or None if not found
    """
    # First check generic mapping
    agent = PHASE_AGENT_MAP.get(phase)
    if agent:
        return agent
    
    # Then check command-specific mapping
    if command and command in COMMAND_PHASE_AGENTS:
        return COMMAND_PHASE_AGENTS[command].get(phase)
    
    return None
