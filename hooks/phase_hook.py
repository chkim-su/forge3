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
  - Validate with workflow daemon
  - BLOCK invalid transitions

Exit codes:
- 0: Allow tool execution
- 2: Block tool execution (with message)
"""

import json
import sys
import os

from client import DaemonControlClient

# Agent name to subagent_type mapping
AGENT_MAPPING = {
    "router-agent": "forge3:router-agent",
    "semantic-agent": "forge3:semantic-agent",
    "execute-agent": "forge3:execute-agent",
    "verify-agent": "forge3:verify-agent",
}


client = DaemonControlClient()

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

    # Get workflow status
    status = client.get_status()

    # If no active workflow, allow tool execution
    if status is None or status.get("message") == "No active workflow found":
        allow()

    workflow_id = status.get("workflow_id")
    current_phase = status.get("current_phase")
    phase_status = status.get("phase_status")
    required_agent = status.get("required_agent")

    # Handle Task tool (agent invocation)
    if tool_name == "Task":
        subagent_type = tool_input.get("subagent_type", "")

        # Check if this is the required agent
        expected_subagent = AGENT_MAPPING.get(required_agent, "")

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

        # Validate with workflow daemon
        result = client.validate_transition(
            workflow_id=workflow_id,
            session_id=status.get("session_id"),
            from_phase=from_phase,
            to_phase=to_phase,
            evidence=evidence,
            conditions=conditions,
            commit_sha=commit_sha,
        )

        if result.get("success"):
            allow()
        else:
            missing = result.get("missing_conditions", [])
            message = result.get("message", "Transition validation failed")
            if missing:
                message += f"\nMissing conditions: {missing}"
            block_with_message(message)

    # For any other tool, allow by default
    allow()


if __name__ == "__main__":
    main()
