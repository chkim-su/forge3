"""
Shared configuration for forge3 hooks.

Single source of truth: workflow_mcp.config
Hooks read from env vars (if set) or import defaults from workflow_mcp.
"""

import os


def get_engine_url() -> str:
    """Resolve engine URL with legacy fallbacks."""
    url = os.environ.get("WORKFLOW_ENGINE_URL")
    if url:
        return url

    host = os.environ.get("WORKFLOW_ENGINE_HOST")
    port = os.environ.get("WORKFLOW_ENGINE_PORT")
    if host and port:
        return f"http://{host}:{port}"

    host = os.environ.get("WORKFLOW_MCP_HOST")
    port = os.environ.get("WORKFLOW_MCP_PORT")
    if host and port:
        return f"http://{host}:{port}"

    legacy_url = os.environ.get("FORGE3_MCP_URL")
    if legacy_url:
        return legacy_url

    try:
        from workflow_mcp.config import DEFAULT_HOST, DEFAULT_PORT
        return f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
    except ImportError:
        raise RuntimeError(
            "workflow engine not installed. Run: pip install -e /path/to/mcp/workflow"
        )


ENGINE_URL = get_engine_url()
