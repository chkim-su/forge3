#!/usr/bin/env python3
"""
Phase Hook - Enforce agent invocation and validate transitions.

Event: PreToolUse
Trigger: Tool name matches ^(Task|workflow_transition)$

CRITICAL BEHAVIOR:
- If phase_status == "agent_required":
  - ALLOW Task tool with required agent
  - BLOCK everything else
- If tool is workflow_transition:
  - Validate with workflow daemon (ONLY source of truth)
  - BLOCK invalid transitions

DESIGN PRINCIPLE:
- Daemon owns ALL workflow policy
- This hook queries daemon for allowed phases (NO hardcoding)
- Validates transitions via daemon only

Exit codes:
- 0: Allow tool execution
- 2: Block tool execution (with message)
"""

import json
import sys
import os

from control_client import WorkflowControlClient
from injection_metadata import get_agent_for_phase


# Build agent mapping dynamically for all known agents
def get_agent_subagent_type(agent_name: str, command: str = None) -> str:
    """Get the subagent_type for an agent name.

    Args:
        agent_name: The agent name (e.g., "router-agent")
        command: Optional command for command-specific agents

    Returns:
        The subagent_type string (e.g., "forge3:router-agent")
    """
    # All forge3 agents use forge3: prefix
    return f"forge3:{agent_name}"


client = WorkflowControlClient()


def block_with_message(message: str):
    """Output block response and exit."""
    result = {
        "decision": "block",
        "reason": message,
    }
    print(json.dumps(result))
    sys.exit(2)


def allow():
    """Allow the tool execution."""
    sys.exit(0)


def main():
    """Handle PreToolUse event."""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # No input - allow by default
        allow()

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Get workflow status from daemon
    state = client.get_status()

    # If no active workflow, allow tool execution
    if state is None:
        allow()

    workflow_id = state.workflow_id
    command = state.command
    current_phase = state.current_phase
    phase_status = state.phase_status
    required_agent = state.required_agent
    allowed_next_phases = state.allowed_next_phases

    # Handle Task tool (agent invocation)
    if tool_name == "Task":
        subagent_type = tool_input.get("subagent_type", "")

        # Get expected subagent type for required agent
        expected_subagent = get_agent_subagent_type(required_agent, command) if required_agent else ""

        if phase_status == "agent_required":
            # Only allow the required agent
            if subagent_type == expected_subagent or subagent_type == required_agent:
                # Record agent invocation
                client.record_agent_invoke(workflow_id, required_agent, current_phase)
                allow()
            else:
                block_with_message(
                    f"Phase {current_phase} requires {required_agent} agent. "
                    f"Got: {subagent_type}. "
                    f"You MUST invoke {expected_subagent or required_agent} first."
                )

        # If agent is running or complete, allow other Task calls
        if phase_status in ["agent_running", "agent_complete"]:
            allow()

        # Default: allow
        allow()

    # Handle workflow_transition tool
    if tool_name == "workflow_transition":
        from_phase = tool_input.get("from_phase", current_phase)
        to_phase = tool_input.get("to_phase")
        commit_sha = tool_input.get("commit_sha")
        evidence = tool_input.get("evidence", {})
        conditions = tool_input.get("conditions_met", [])

        # Validate to_phase is in allowed_next_phases (daemon-provided)
        if to_phase not in allowed_next_phases:
            block_with_message(
                f"Invalid transition from {from_phase} to {to_phase}. "
                f"Allowed next phases: {allowed_next_phases}"
            )

        # Validate with workflow daemon (AUTHORITATIVE)
        result = client.transition(
            from_phase=from_phase,
            to_phase=to_phase,
            evidence=evidence,
            conditions_met=conditions,
            commit_sha=commit_sha,
        )

        if result.success:
            allow()
        else:
            message = result.message
            if result.missing_conditions:
                message += f"\nMissing conditions: {result.missing_conditions}"
            block_with_message(message)

    # For any other tool, allow by default
    allow()


if __name__ == "__main__":
    main()
