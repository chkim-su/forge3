#!/usr/bin/env python3
"""
Router Hook - Initialize workflow on /assist command.

Event: UserPromptSubmit
Trigger: Prompt matches ^/assist\\b

CRITICAL BEHAVIOR:
- POST to workflow daemon to initialize workflow
- Exit 0 immediately (NO waiting!)
- Returns instruction for Claude to invoke router-agent
"""

import json
import sys
import os
import re
import subprocess
from typing import Optional

from client import DaemonControlClient


def block_with_message(message: str):
    result = {
        "decision": "block",
        "reason": message,
    }
    print(json.dumps(result))
    sys.exit(2)


def _git_toplevel(path: str) -> Optional[str]:
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


def main():
    """Handle UserPromptSubmit event."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # No input or invalid JSON - pass through
        sys.exit(0)

    prompt = input_data.get("prompt", "")

    # Check if this is an /assist command
    if not re.match(r"^/assist\b", prompt):
        sys.exit(0)

    # Extract the actual task from the prompt
    task = re.sub(r"^/assist\s*", "", prompt).strip()
    if not task:
        task = prompt  # Use full prompt if no task after /assist

    session_id = os.environ.get("CSC_SESSION_ID")
    workspace_root = resolve_workspace_root()
    if not os.path.isdir(workspace_root):
        block_with_message(f"workflow init failed: invalid workspace_root {workspace_root}")
    client = DaemonControlClient()

    data = client.init_workflow(
        prompt=task,
        session_id=session_id,
        workspace_root=workspace_root,
        metadata={
            "source": "router_hook",
            "original_prompt": prompt,
        },
    )

    if data:
        workflow_id = data.get("workflow_id", "unknown")
        required_agent = data.get("required_agent", "router-agent")

        result = {
            "decision": "modify",
            "modifications": {
                "appendToPrompt": f"""

---
[Phase 1: Router] Starting...
---

<workflow-context>
Workflow initialized: {workflow_id}
Session: {data.get("session_id", session_id or "default")}
Current phase: router
Required action: Invoke {required_agent} agent using Task tool.

IMPORTANT: You MUST invoke the {required_agent} agent before any other tools.
</workflow-context>"""
            }
        }
        print(json.dumps(result))
    else:
        sys.stderr.write("Workflow init failed; proceeding without workflow\n")

    # CRITICAL: Exit 0 immediately, no waiting!
    sys.exit(0)


if __name__ == "__main__":
    main()
