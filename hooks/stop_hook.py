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

from client import DaemonControlClient


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
    """Allow the stop."""
    sys.exit(0)


def main():
    """Handle Stop event."""
    # Check with workflow daemon
    result = client.can_stop()

    can_stop = result.get("can_stop", True)
    reason = result.get("reason", "Unknown")

    if can_stop:
        allow()
    else:
        block_with_message(
            f"Cannot stop: {reason}\n\n"
            "The workflow is incomplete. Please either:\n"
            "1. Complete the current phase by invoking the required agent and calling workflow_transition\n"
            "2. Cancel the workflow explicitly\n"
        )


if __name__ == "__main__":
    main()
