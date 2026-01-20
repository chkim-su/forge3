#!/usr/bin/env python3
"""
Workflow Hook - Initialize workflow on command invocation.

Event: UserPromptSubmit
Trigger: Prompt matches ^/(assist|plan|create|verify|health-check)\b

CRITICAL BEHAVIOR:
- Sends ONLY command name to daemon
- Daemon resolves workflow policy internally
- Exit 0 immediately (NO waiting!)
- Returns instruction for Claude to invoke required agent

DESIGN PRINCIPLE:
- Daemon owns ALL workflow policy (SSOT)
- Plugin sends only command name
- Daemon returns policy-resolved state
"""

import json
import sys
import os
import re
import subprocess
from typing import Optional

from control_client import WorkflowControlClient
from skill_loader import get_phase_skill_injection_v2


# Commands that trigger workflow initialization
WORKFLOW_COMMANDS = ["assist", "plan", "create", "verify", "health-check"]


def block_with_message(message: str):
    """Output block response and exit."""
    result = {
        "decision": "block",
        "reason": message,
    }
    print(json.dumps(result))
    sys.exit(2)


def _git_toplevel(path: str) -> Optional[str]:
    """Get git repository root."""
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
    """Resolve workspace root from environment or git."""
    env_root = os.environ.get("WORKFLOW_WORKSPACE_ROOT")
    if env_root:
        return os.path.abspath(os.path.expanduser(env_root))

    cwd = os.path.abspath(os.getcwd())
    git_root = _git_toplevel(cwd)
    return git_root if git_root else cwd


def parse_command(prompt: str) -> tuple[Optional[str], str]:
    """Parse command and task from prompt.
    
    Args:
        prompt: The user prompt
        
    Returns:
        Tuple of (command_name, task_description)
    """
    for cmd in WORKFLOW_COMMANDS:
        pattern = rf"^/{cmd}\b\s*(.*)"
        match = re.match(pattern, prompt, re.IGNORECASE)
        if match:
            task = match.group(1).strip() or prompt
            return cmd, task
    return None, prompt


def format_phase_header(state) -> str:
    """Format phase header for display.
    
    Args:
        state: WorkflowState from daemon
        
    Returns:
        Formatted phase header
    """
    phase = state.current_phase
    phase_num = state.phases.index(phase) + 1 if phase in state.phases else 1
    total_phases = len(state.phases)
    if state.final_phase and state.final_phase not in state.phases:
        total_phases += 1
    
    return f"[Phase {phase_num}/{total_phases}: {phase.capitalize()}] Starting..."


def main():
    """Handle UserPromptSubmit event."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # No input or invalid JSON - pass through
        sys.exit(0)

    prompt = input_data.get("prompt", "")

    # Parse command from prompt
    command, task = parse_command(prompt)
    
    if command is None:
        # Not a workflow command - pass through
        sys.exit(0)

    session_id = os.environ.get("CSC_SESSION_ID")
    workspace_root = resolve_workspace_root()
    
    if not os.path.isdir(workspace_root):
        block_with_message(f"Workflow init failed: invalid workspace_root {workspace_root}")

    # Initialize workflow via daemon
    # CRITICAL: Send ONLY command name - daemon resolves policy
    client = WorkflowControlClient()
    state = client.init_workflow(
        command=command,
        session_id=session_id,
        workspace_root=workspace_root,
        task=task if command != "assist" else None,  # Assist is dispatcher, no task
        metadata={
            "source": "workflow_hook",
            "original_prompt": prompt,
        },
    )

    if state:
        # Get skill content for current phase
        skill_injection = get_phase_skill_injection_v2(
            phase=state.current_phase,
            command=state.command,
        ) or ""

        # Build response based on workflow type
        if state.is_dispatcher:
            # /assist is a dispatcher - just routes to other commands
            action_message = (
                f"Required action: Invoke {state.required_agent} agent using Task tool.\n\n"
                f"IMPORTANT: You MUST invoke the {state.required_agent} agent first.\n"
                f"After router completes, recommend which command to run (/plan, /create, or /verify)."
            )
        else:
            # Non-dispatcher commands execute their workflows
            action_message = (
                f"Required action: Invoke {state.required_agent} agent using Task tool.\n\n"
                f"IMPORTANT: You MUST invoke the {state.required_agent} agent before any other tools.\n"
                f"Phases: {' → '.join(state.phases)}"
                + (f" → {state.final_phase}" if state.final_phase else "")
            )

        phase_header = format_phase_header(state)

        result = {
            "decision": "modify",
            "modifications": {
                "appendToPrompt": f"""

---
{phase_header}
---

<workflow-context>
Workflow initialized: {state.workflow_id}
Command: /{state.command}
Workflow type: {state.workflow_type}
Session: {state.session_id or "default"}
Current phase: {state.current_phase}

{action_message}
</workflow-context>

{skill_injection}"""
            }
        }
        print(json.dumps(result))
    else:
        sys.stderr.write("Workflow init failed; proceeding without workflow\n")

    # CRITICAL: Exit 0 immediately, no waiting!
    sys.exit(0)


if __name__ == "__main__":
    main()
