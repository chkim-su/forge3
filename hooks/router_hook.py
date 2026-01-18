#!/usr/bin/env python3
"""
Router Hook - Initialize workflow on /assist command.

Event: UserPromptSubmit
Trigger: Prompt matches ^/assist\\b

CRITICAL BEHAVIOR:
- POST to MCP daemon to initialize workflow
- Exit 0 immediately (NO waiting!)
- Returns instruction for Claude to invoke router-agent
"""

import json
import sys
import os
import re

# MCP server URL
MCP_URL = os.environ.get("FORGE3_MCP_URL", "http://127.0.0.1:8765")


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

    try:
        import httpx

        # Initialize workflow via MCP daemon
        response = httpx.post(
            f"{MCP_URL}/workflow/init",
            json={
                "prompt": task,
                "intent_hint": None,
                "metadata": {
                    "source": "router_hook",
                    "original_prompt": prompt,
                }
            },
            timeout=3.0,
        )

        if response.status_code == 200:
            data = response.json()
            workflow_id = data.get("workflow_id", "unknown")
            required_agent = data.get("required_agent", "router-agent")

            # Output instruction for Claude
            result = {
                "decision": "modify",
                "modifications": {
                    "appendToPrompt": f"""

<workflow-context>
Workflow initialized: {workflow_id}
Current phase: router
Required action: Invoke {required_agent} agent using Task tool.

IMPORTANT: You MUST invoke the {required_agent} agent before any other tools.
</workflow-context>"""
                }
            }
            print(json.dumps(result))
        else:
            # MCP server error - log but don't block
            sys.stderr.write(f"MCP init failed: {response.status_code}\n")

    except ImportError:
        # httpx not available - output fallback instruction
        result = {
            "decision": "modify",
            "modifications": {
                "appendToPrompt": """

<workflow-context>
MCP daemon not available. Proceeding with manual workflow.
Required action: Invoke router-agent using Task tool.
</workflow-context>"""
            }
        }
        print(json.dumps(result))

    except Exception as e:
        # Network error or timeout - log but don't block
        sys.stderr.write(f"Router hook error: {e}\n")

    # CRITICAL: Exit 0 immediately, no waiting!
    sys.exit(0)


if __name__ == "__main__":
    main()
