"""
Shared configuration for forge3 hooks.

Single source of truth: workflowd.config
Hooks read from env vars (if set) or import defaults from workflowd.
"""

import json
import os
from pathlib import Path
from typing import Optional


def get_engine_url() -> str:
    """Resolve engine URL with legacy fallbacks."""
    url = os.environ.get("WORKFLOW_ENGINE_URL")
    if url:
        return url

    host = os.environ.get("WORKFLOW_ENGINE_HOST")
    port = os.environ.get("WORKFLOW_ENGINE_PORT")
    if host and port:
        return f"http://{host}:{port}"

    try:
        from workflowd.config import DEFAULT_HOST, DEFAULT_PORT
        return f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
    except ImportError:
        raise RuntimeError(
            "workflow engine not installed. Run: pip install -e /path/to/csc/workflow-daemon"
        )


ENGINE_URL = get_engine_url()


def get_workflows_root() -> Path:
    """Resolve workflows root for artifact discovery."""
    env_root = os.environ.get("WORKFLOW_ENGINE_WORKFLOWS_DIR")
    if env_root:
        return Path(env_root).expanduser()

    try:
        from workflowd.config import WORKFLOWS_DIR
        return WORKFLOWS_DIR
    except ImportError:
        return Path.home() / ".claude" / "local" / "workflows"


def get_current_workflow_id(session_id: str) -> Optional[str]:
    """Read current workflow_id from session pointer."""
    if not session_id:
        return None
    current_path = get_workflows_root() / session_id / "current.json"
    if not current_path.exists():
        return None
    try:
        data = json.loads(current_path.read_text())
    except json.JSONDecodeError:
        return None
    return data.get("workflow_id")
