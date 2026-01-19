#!/usr/bin/env python3
"""
Skill Loader - Utility for loading skill content for phase injection.

Maps workflow phases to their corresponding skills and provides
functions to read skill content with frontmatter stripped.
"""

import os
import re
from typing import Optional

# Map phases to their skill directory names
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


def read_phase_skill(phase: str) -> Optional[str]:
    """Read skill content for a phase, stripping frontmatter.

    Args:
        phase: The phase name (router, semantic, execute, verify)

    Returns:
        Skill content without frontmatter, or None if not found
    """
    skill_name = PHASE_TO_SKILL.get(phase)
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


def format_skill_tag(phase: str, content: str) -> str:
    """Format skill content in a phase-skill-reference tag.

    Args:
        phase: The phase name
        content: The skill content

    Returns:
        Content wrapped in <phase-skill-reference> tag
    """
    return f"<phase-skill-reference phase=\"{phase}\">\n{content}\n</phase-skill-reference>"


def get_phase_skill_injection(phase: str) -> Optional[str]:
    """Get formatted skill injection for a phase.

    Args:
        phase: The phase name

    Returns:
        Formatted skill content in tag, or None if not found
    """
    content = read_phase_skill(phase)
    if content:
        return format_skill_tag(phase, content)
    return None
