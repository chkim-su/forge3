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
- Phase transitions require explicit workflow_transition tool call (MCP: mcp__workflow__workflow_transition)
- Daemon owns workflow policy
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path

from control_client import WorkflowControlClient
from skill_loader import get_phase_skill_injection_v2
from _config import get_current_workflow_id


client = WorkflowControlClient()
COMMANDS = ["assist:plan", "assist:create", "assist:verify", "assist:health-check"]


def _git_toplevel(path: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def resolve_workspace_root() -> str:
    env_root = os.environ.get("WORKFLOW_WORKSPACE_ROOT")
    if env_root:
        return os.path.abspath(os.path.expanduser(env_root))

    cwd = os.path.abspath(os.getcwd())
    git_root = _git_toplevel(cwd)
    return git_root if git_root else cwd


def extract_tool_text(input_data: dict) -> str:
    tool_output = input_data.get("tool_output")
    if isinstance(tool_output, dict):
        for key in ("stdout", "output", "content", "text", "message"):
            value = tool_output.get(key)
            if isinstance(value, str) and value.strip():
                return value
        if isinstance(tool_output.get("content"), list):
            for item in tool_output.get("content", []):
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    return item["text"]
    if isinstance(tool_output, str) and tool_output.strip():
        return tool_output

    for key in ("output", "result", "content"):
        value = input_data.get(key)
        if isinstance(value, str) and value.strip():
            return value

    env_output = os.environ.get("TOOL_OUTPUT", "")
    if env_output.strip():
        return env_output
    return ""


def find_recommended_command(text: str) -> str | None:
    if not text:
        return None
    lowered = text.lower()
    pattern = re.compile(r"/assist:(plan|create|verify|health-check)", re.IGNORECASE)

    for marker in ("recommendation", "recommended command", "recommended"):
        idx = lowered.find(marker)
        if idx != -1:
            match = pattern.search(text[idx:])
            if match:
                return f"/assist:{match.group(1).lower()}"

    return None


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

    session_id = os.environ.get("CSC_SESSION_ID", "")
    workflow_id = get_current_workflow_id(session_id)
    if not workflow_id:
        sys.exit(0)

    # Query workflow daemon for current state
    state = client.get_status(workflow_id)

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
    recorded = client.record_agent_complete(workflow_id, agent_name, current_phase)

    auto_chain_message = ""
    if state.is_dispatcher and state.command == "assist:wizard":
        router_output = extract_tool_text(input_data)
        recommended = find_recommended_command(router_output)
        if recommended:
            workspace_root = resolve_workspace_root()
            next_command = recommended.lstrip("/")
            next_state = client.init_workflow(
                command=next_command,
                session_id=session_id,
                workspace_root=workspace_root,
                task=state.prompt,
                metadata={
                    "source": "auto_chain",
                    "routed_from": state.workflow_id,
                    "recommended_command": recommended,
                },
            )
            if next_state:
                skill_injection = get_phase_skill_injection_v2(
                    phase=next_state.current_phase,
                    command=next_state.command,
                ) or ""

                phase_sequence = list(next_state.phases)
                if next_state.final_phase and next_state.final_phase not in phase_sequence:
                    phase_sequence.append(next_state.final_phase)
                phase_num = phase_sequence.index(next_state.current_phase) + 1 if next_state.current_phase in phase_sequence else 1
                total_phases = len(phase_sequence)

                auto_chain_message = f"""

---
[Phase {phase_num}/{total_phases}: {next_state.current_phase.capitalize()}] Starting...
---

<workflow-context>
Auto-started: /{next_state.command}
Workflow: {next_state.workflow_id}
Session: {next_state.session_id or "default"}
Current phase: {next_state.current_phase}

Required action: Invoke {next_state.required_agent} agent using Task tool.
</workflow-context>

{skill_injection}"""

    # Calculate phase number for display
    phase_num = phases.index(current_phase) + 1 if current_phase in phases else "?"
    total_phases = len(phases)
    if final_phase and final_phase not in phases:
        total_phases += 1

    # Build announcement message
    complete_banner = f"[Phase {phase_num}/{total_phases}: {current_phase.capitalize()}] Agent complete"

    # Build next steps message
    if is_dispatcher:
        # Dispatcher (/assist:wizard) - recommend which command to run
        next_steps = (
            "\nDispatcher phase complete. Based on the router's classification, "
            "recommend one of these commands to the user:\n"
            "- /assist:plan - For component structure planning\n"
            "- /assist:create - For file creation\n"
            "- /assist:verify - For validation\n"
            "- /assist:health-check - For quality analysis\n"
        )
    elif allowed_next_phases:
        # Non-dispatcher - show allowed transitions
        next_phases_str = ", ".join(allowed_next_phases)
        next_steps = (
            f"\nAllowed next phases: {next_phases_str}\n\n"
            "To proceed to the next phase, use the workflow_transition tool (MCP: mcp__workflow__workflow_transition):\n"
            "```\n"
            "mcp__workflow__workflow_transition(\n"
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

    warning = ""
    if not recorded:
        warning = (
            "\n[WARN] Failed to record agent completion with workflow daemon.\n"
            "Workflow status and progress may be stale.\n"
            "Ensure workflow-daemon is running and reachable at WORKFLOW_ENGINE_URL.\n"
        )

    announcement = (
        f"\n---\n{complete_banner}\n---\n"
        f"{next_steps}{warning}{auto_chain_message}"
    )

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
