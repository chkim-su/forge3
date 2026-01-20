#!/usr/bin/env python3
"""
Announce Hook - EVENT LOGGING ONLY for SubagentStop events.

Event: SubagentStop
Trigger: subagent_type matches ^forge3:

CRITICAL BEHAVIOR:
- Records agent_completed event with daemon
- Updates phase_status -> agent_complete
- NEVER advances phases
- NO phase transitions here

DESIGN PRINCIPLE:
- This hook logs events ONLY
- Phase transitions require explicit workflow_transition tool call
- Daemon owns workflow policy
"""

import json
import sys
import os

from control_client import WorkflowControlClient
from skill_loader import get_phase_skill_injection_v2


client = WorkflowControlClient()


def main():
    """Handle SubagentStop event for forge3 agents.

    EVENT LOGGING ONLY - does NOT advance phases.
    """
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    # Get the agent type that just completed
    subagent_type = input_data.get("subagent_type", "")

    # Only handle forge3 agents
    if not subagent_type.startswith("forge3:"):
        sys.exit(0)

    # Extract agent name (e.g., "forge3:router-agent" -> "router-agent")
    agent_name = subagent_type.replace("forge3:", "")

    # Query workflow daemon for current state
    state = client.get_status()

    if not state:
        # Daemon not available, skip
        sys.exit(0)

    current_phase = state.current_phase
    command = state.command
    phases = state.phases
    final_phase = state.final_phase
    allowed_next_phases = state.allowed_next_phases
    is_dispatcher = state.is_dispatcher

    # Record agent completion event (EVENT LOGGING ONLY)
    # This does NOT advance the phase
    client.record_agent_complete(agent_name, current_phase)

    # Calculate phase number for display
    phase_num = phases.index(current_phase) + 1 if current_phase in phases else "?"
    total_phases = len(phases)
    if final_phase and final_phase not in phases:
        total_phases += 1

    # Build announcement message
    complete_banner = f"[Phase {phase_num}/{total_phases}: {current_phase.capitalize()}] Agent complete"

    # Build next steps message
    if is_dispatcher:
        # Dispatcher (/assist) - recommend which command to run
        next_steps = (
            "\nDispatcher phase complete. Based on the router's classification, "
            "recommend one of these commands to the user:\n"
            "- /plan - For component structure planning\n"
            "- /create - For file creation\n"
            "- /verify - For validation\n"
        )
    elif allowed_next_phases:
        # Non-dispatcher - show allowed transitions
        next_phases_str = ", ".join(allowed_next_phases)
        next_steps = (
            f"\nAllowed next phases: {next_phases_str}\n\n"
            "To proceed to the next phase, use the workflow_transition tool:\n"
            "```\n"
            "workflow_transition(\n"
            f"  from_phase=\"{current_phase}\",\n"
            f"  to_phase=\"{allowed_next_phases[0] if allowed_next_phases else 'next_phase'}\",\n"
            "  evidence={...},\n"
            "  conditions_met=[...]\n"
            ")\n"
            "```\n"
        )
    else:
        # No more phases - workflow complete
        next_steps = "\nWorkflow complete. All phases finished.\n"

    announcement = f"\n---\n{complete_banner}\n---\n{next_steps}"

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
