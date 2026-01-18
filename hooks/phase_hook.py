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
  - Validate with MCP daemon
  - BLOCK invalid transitions

Exit codes:
- 0: Allow tool execution
- 2: Block tool execution (with message)
"""

import json
import sys
import os

# MCP server URL
MCP_URL = os.environ.get("FORGE3_MCP_URL", "http://127.0.0.1:8765")

# Agent name to subagent_type mapping
AGENT_MAPPING = {
    "router-agent": "forge3:router-agent",
    "semantic-agent": "forge3:semantic-agent",
    "execute-agent": "forge3:execute-agent",
    "verify-agent": "forge3:verify-agent",
}


def get_workflow_status():
    """Get current workflow status from MCP daemon."""
    try:
        import httpx
        response = httpx.get(f"{MCP_URL}/workflow/status", timeout=3.0)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        sys.stderr.write(f"Phase hook: Could not get workflow status: {e}\n")
    return None


def record_agent_invoke(workflow_id: str, agent_name: str, phase: str):
    """Record agent invocation with MCP daemon."""
    try:
        import httpx
        response = httpx.post(
            f"{MCP_URL}/agent/invoke",
            json={
                "workflow_id": workflow_id,
                "agent_name": agent_name,
                "phase": phase,
            },
            timeout=3.0,
        )
        return response.status_code == 200
    except Exception as e:
        sys.stderr.write(f"Phase hook: Could not record agent invoke: {e}\n")
    return False


def validate_transition(workflow_id: str, from_phase: str, to_phase: str, evidence: dict, conditions: list):
    """Validate phase transition with MCP daemon."""
    try:
        import httpx
        response = httpx.post(
            f"{MCP_URL}/workflow/transition",
            json={
                "workflow_id": workflow_id,
                "from_phase": from_phase,
                "to_phase": to_phase,
                "evidence": evidence,
                "conditions_met": conditions,
            },
            timeout=5.0,
        )
        return response.json()
    except Exception as e:
        sys.stderr.write(f"Phase hook: Could not validate transition: {e}\n")
    return {"success": False, "message": "MCP daemon unavailable"}


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
    status = get_workflow_status()

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
                record_agent_invoke(workflow_id, required_agent, current_phase)
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
        evidence = tool_input.get("evidence", {})
        conditions = tool_input.get("conditions_met", [])

        # Validate with MCP daemon
        result = validate_transition(
            workflow_id,
            from_phase,
            to_phase,
            evidence,
            conditions,
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
