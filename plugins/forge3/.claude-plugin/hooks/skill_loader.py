#!/usr/bin/env python3
"""
Skill Loader - Utility for loading skill content for phase injection.

Maps workflow phases to their corresponding skills and provides
functions to read skill content with frontmatter stripped.

Uses injection_metadata.py for phase-to-skill mapping (read-only hints).
"""

import os
import re
from typing import Optional

from injection_metadata import get_skill_for_phase


# Legacy mapping for backward compatibility
PHASE_TO_SKILL = {
    "router": "router-skill",
    "semantic": "semantic-skill",
    "execute": "execute-skill",
    "verify": "verify-skill",
}


def get_plugin_root() -> str:
    """Get the plugin root directory from environment or derive from this file's location."""
    env_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env_root:
        return env_root
    # Derive from this file's location (hooks/ directory is under plugin root)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown content.

    Frontmatter is delimited by --- at the start of the file.
    Returns content after the closing ---.
    """
    # Pattern matches content between --- delimiters at start of file
    pattern = r"^---\s*\n.*?\n---\s*\n"
    stripped = re.sub(pattern, "", content, count=1, flags=re.DOTALL)
    return stripped.strip()


def read_skill_content(skill_name: str) -> Optional[str]:
    """Read skill content by skill directory name, stripping frontmatter.

    Args:
        skill_name: The skill directory name (e.g., "router-skill")

    Returns:
        Skill content without frontmatter, or None if not found
    """
    if not skill_name:
        return None

    plugin_root = get_plugin_root()
    skill_path = os.path.join(plugin_root, "skills", skill_name, "SKILL.md")

    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
        return strip_frontmatter(content)
    except (IOError, OSError):
        return None


def read_phase_skill(phase: str) -> Optional[str]:
    """Read skill content for a phase, stripping frontmatter.

    Legacy function - uses hardcoded PHASE_TO_SKILL mapping.

    Args:
        phase: The phase name (router, semantic, execute, verify)

    Returns:
        Skill content without frontmatter, or None if not found
    """
    skill_name = PHASE_TO_SKILL.get(phase)
    return read_skill_content(skill_name)


def read_phase_skill_v2(phase: str, command: Optional[str] = None) -> Optional[str]:
    """Read skill content for a phase using injection_metadata.

    Uses the centralized injection_metadata for phase-to-skill mapping.
    Supports command-specific phases (e.g., verify/discover vs health-check/discover).

    Args:
        phase: The phase name
        command: Optional command name for command-specific phases

    Returns:
        Skill content without frontmatter, or None if not found
    """
    skill_name = get_skill_for_phase(phase, command)
    return read_skill_content(skill_name)


def format_skill_tag(phase: str, content: str, command: Optional[str] = None) -> str:
    """Format skill content in a phase-skill-reference tag.

    Args:
        phase: The phase name
        content: The skill content
        command: Optional command name for context

    Returns:
        Content wrapped in <phase-skill-reference> tag
    """
    if command:
        return f'<phase-skill-reference phase="{phase}" command="{command}">\n{content}\n</phase-skill-reference>'
    return f'<phase-skill-reference phase="{phase}">\n{content}\n</phase-skill-reference>'


def get_phase_skill_injection(phase: str) -> Optional[str]:
    """Get formatted skill injection for a phase.

    Legacy function - uses hardcoded PHASE_TO_SKILL mapping.

    Args:
        phase: The phase name

    Returns:
        Formatted skill content in tag, or None if not found
    """
    content = read_phase_skill(phase)
    if content:
        return format_skill_tag(phase, content)
    return None


def get_phase_skill_injection_v2(phase: str, command: Optional[str] = None) -> Optional[str]:
    """Get formatted skill injection for a phase using injection_metadata.

    Uses the centralized injection_metadata for phase-to-skill mapping.
    Supports command-specific phases.

    Args:
        phase: The phase name
        command: Optional command name for command-specific phases

    Returns:
        Formatted skill content in tag, or None if not found
    """
    content = read_phase_skill_v2(phase, command)
    if content:
        return format_skill_tag(phase, content, command)
    return None
