#!/usr/bin/env python3
"""
Stop Hook - Prevent stopping with incomplete workflow.

Event: Stop
Trigger: Always (no matcher)

CRITICAL BEHAVIOR:
- Check if workflow can be stopped via workflow daemon
- BLOCK if workflow is incomplete
- ALLOW if workflow is complete, cancelled, or no active workflow

Exit codes:
- 0: Allow stop
- 2: Block stop (with message)
"""

import json
import sys
import os

from control_client import WorkflowControlClient
from _config import get_current_workflow_id


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
    """Allow the stop."""
    sys.exit(0)


def main():
    """Handle Stop event."""
    session_id = os.environ.get("CSC_SESSION_ID", "")
    workflow_id = get_current_workflow_id(session_id)
    if not workflow_id:
        allow()

    # Check with workflow daemon
    result = client.can_stop(workflow_id)

    if result.can_stop:
        allow()
    else:
        block_with_message(
            f"Cannot stop: {result.reason}\n\n"
            "The workflow is incomplete. Please either:\n"
            "1. Complete the current phase by invoking the required agent and calling mcp__workflow__workflow_transition\n"
            "2. Cancel the workflow explicitly\n"
        )


if __name__ == "__main__":
    main()
