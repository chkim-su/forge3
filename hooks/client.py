"""
Control client for workflow engine daemon.

Hooks must call into this client instead of touching state directly. This keeps
the hook surface stable if the underlying transport changes.
"""

from typing import Any, Dict, Optional

import httpx

from _config import ENGINE_URL


class DaemonControlClient:
    """HTTP client wrapper for workflow engine."""

    def __init__(self, base_url: str = ENGINE_URL):
        self.base_url = base_url.rstrip("/")

    def init_workflow(
        self,
        prompt: str,
        session_id: Optional[str],
        workspace_root: str,
        metadata: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        try:
            resp = httpx.post(
                f"{self.base_url}/workflow/init",
                json={
                    "prompt": prompt,
                    "intent_hint": None,
                    "metadata": metadata,
                    "session_id": session_id,
                    "workspace_root": workspace_root,
                },
                timeout=3.0,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            return None
        return None

    def get_status(self) -> Optional[Dict[str, Any]]:
        try:
            resp = httpx.get(f"{self.base_url}/workflow/status", timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            return None
        return None

    def record_agent_invoke(self, workflow_id: str, agent_name: str, phase: str) -> bool:
        try:
            resp = httpx.post(
                f"{self.base_url}/agent/invoke",
                json={
                    "workflow_id": workflow_id,
                    "agent_name": agent_name,
                    "phase": phase,
                },
                timeout=3.0,
            )
            return resp.status_code == 200
        except Exception:
            return False

    def validate_transition(
        self,
        workflow_id: str,
        session_id: Optional[str],
        from_phase: str,
        to_phase: str,
        evidence: Dict[str, Any],
        conditions: list[str],
        commit_sha: Optional[str],
    ) -> Dict[str, Any]:
        try:
            resp = httpx.post(
                f"{self.base_url}/workflow/transition",
                json={
                    "workflow_id": workflow_id,
                    "session_id": session_id,
                    "from_phase": from_phase,
                    "to_phase": to_phase,
                    "evidence": evidence,
                    "conditions_met": conditions,
                    "commit_sha": commit_sha,
                },
                timeout=5.0,
            )
            return resp.json()
        except Exception as e:
            return {"success": False, "message": f"Workflow daemon unavailable: {e}"}

    def can_stop(self) -> Dict[str, Any]:
        try:
            resp = httpx.get(f"{self.base_url}/workflow/can-stop", timeout=3.0)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            return {"can_stop": True, "reason": f"Workflow daemon check failed: {e}"}
        return {"can_stop": True, "reason": "Workflow daemon check failed"}
