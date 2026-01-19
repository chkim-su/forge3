#!/usr/bin/env python3
"""
Announce Hook - Phase transition announcer for SubagentStop events.

Event: SubagentStop
Trigger: subagent_type matches ^forge3:

Announces phase completion and next phase when forge3 agents complete.
"""

import json
import sys
import os

from client import DaemonControlClient

# Phase display names and order
PHASE_INFO = {
    "router": {"display": "Router", "number": 1},
    "semantic": {"display": "Semantic", "number": 2},
    "execute": {"display": "Execute", "number": 3},
    "verify": {"display": "Verify", "number": 4},
}

PHASE_ORDER = ["router", "semantic", "execute", "verify"]


def get_next_phase(current: str) -> str | None:
    """Get the next phase in the workflow, or None if complete."""
    try:
        idx = PHASE_ORDER.index(current)
        if idx + 1 < len(PHASE_ORDER):
            return PHASE_ORDER[idx + 1]
    except ValueError:
        pass
    return None


def format_phase_banner(phase: str, status: str) -> str:
    """Format a phase banner line."""
    info = PHASE_INFO.get(phase, {"display": phase.capitalize(), "number": "?"})
    return f"[Phase {info['number']}: {info['display']}] {status}"


def main():
    """Handle SubagentStop event for forge3 agents."""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    # Get the agent type that just completed
    subagent_type = input_data.get("subagent_type", "")

    # Only handle forge3 agents
    if not subagent_type.startswith("forge3:"):
        sys.exit(0)

    # Extract agent name (e.g., "forge3:router-agent" -> "router")
    agent_name = subagent_type.replace("forge3:", "").replace("-agent", "")

    # Query workflow daemon for current phase
    client = DaemonControlClient()
    status = client.get_status()

    if not status:
        # Daemon not available, skip announcement
        sys.exit(0)

    current_phase = status.get("current_phase", agent_name)
    next_phase = get_next_phase(current_phase)

    # Build announcement message
    complete_banner = format_phase_banner(current_phase, "Complete")

    if next_phase:
        next_banner = format_phase_banner(next_phase, "Starting...")
        announcement = f"\n---\n{complete_banner}\n{next_banner}\n---\n"
    else:
        announcement = f"\n---\n{complete_banner}\nWorkflow finished.\n---\n"

    # Output the announcement as appendToPrompt
    result = {
        "decision": "modify",
        "modifications": {
            "appendToPrompt": announcement
        }
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
