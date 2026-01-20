#!/usr/bin/env python3
"""
Control Client - Typed daemon RPC wrapper for workflow engine.

This module provides a typed interface for all daemon APIs.
The daemon owns ALL workflow policy - this client only sends
the command name and receives policy-resolved state.

Daemon API (AUTHORITATIVE):
- /workflow/init    - Initialize workflow with command name only
- /workflow/status  - Get current state including allowed_next_phases
- /workflow/transition - Validated phase transition
- /workflow/can-stop   - Check if workflow can be stopped
- /event/record     - Record events (agent_completed, etc.)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import httpx

try:
    from _config import ENGINE_URL
except ImportError:
    import importlib.util
    from pathlib import Path

    _config_path = Path(__file__).parent / "_config.py"
    _spec = importlib.util.spec_from_file_location("_config", _config_path)
    _module = importlib.util.module_from_spec(_spec)
    assert _spec and _spec.loader
    _spec.loader.exec_module(_module)
    ENGINE_URL = _module.ENGINE_URL


@dataclass
class WorkflowState:
    """Workflow state returned by daemon."""
    workflow_id: str
    command: str                      # "assist:wizard", "assist:plan", "assist:create", "assist:verify", "assist:health-check"
    workflow_type: str                # "dispatch", "plan", "create", "verify", "health"
    phases: List[str]                 # From daemon policy
    final_phase: Optional[str]        # "schema-check" or None for dispatcher
    current_phase: str
    phase_status: str                 # "agent_required", "agent_running", "agent_complete"
    allowed_next_phases: List[str]    # Valid next phases from current
    is_dispatcher: bool               # True for /assist
    session_id: Optional[str]
    required_agent: Optional[str]     # Agent required for current phase
    prompt: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowState":
        """Create WorkflowState from dict response."""
        return cls(
            workflow_id=data.get("workflow_id", ""),
            command=data.get("command", ""),
            workflow_type=data.get("workflow_type", ""),
            phases=data.get("phases", []),
            final_phase=data.get("final_phase"),
            current_phase=data.get("current_phase", ""),
            phase_status=data.get("phase_status", ""),
            allowed_next_phases=data.get("allowed_next_phases", []),
            is_dispatcher=data.get("is_dispatcher", False),
            session_id=data.get("session_id"),
            required_agent=data.get("required_agent"),
            prompt=data.get("prompt"),
            metadata=data.get("metadata") or {},
        )


@dataclass
class TransitionResult:
    """Result of a phase transition."""
    success: bool
    message: str
    new_phase: Optional[str]
    new_status: Optional[str]
    missing_conditions: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransitionResult":
        return cls(
            success=data.get("success", False),
            message=data.get("message", ""),
            new_phase=data.get("new_phase"),
            new_status=data.get("new_status"),
            missing_conditions=data.get("missing_conditions", []),
        )


@dataclass
class CanStopResult:
    """Result of can-stop check."""
    can_stop: bool
    reason: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CanStopResult":
        return cls(
            can_stop=data.get("can_stop", True),
            reason=data.get("reason", ""),
        )


class WorkflowControlClient:
    """HTTP client wrapper for workflow daemon with typed responses.
    
    The daemon owns ALL workflow policy. This client:
    - Sends only command name to /workflow/init
    - Receives policy-resolved state
    - Never hardcodes workflow definitions
    """

    def __init__(self, base_url: str = ENGINE_URL):
        self.base_url = base_url.rstrip("/")

    def init_workflow(
        self,
        command: str,
        session_id: Optional[str],
        workspace_root: str,
        task: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[WorkflowState]:
        """Initialize workflow with command name.

        The daemon resolves the workflow policy from the command name.

        Args:
            command: Command name ("assist:wizard", "assist:plan", "assist:create", "assist:verify", "assist:health-check")
            session_id: Session identifier
            workspace_root: Workspace root path
            task: Optional task description (for non-dispatcher commands)
            metadata: Optional metadata

        Returns:
            WorkflowState with policy-resolved phases, or None on error
        """
        try:
            resp = httpx.post(
                f"{self.base_url}/workflow/init",
                json={
                    "command": command,
                    "session_id": session_id,
                    "workspace_root": workspace_root,
                    "task": task,
                    "metadata": metadata or {},
                },
                timeout=5.0,
            )
            if resp.status_code == 200:
                return WorkflowState.from_dict(resp.json())
        except Exception:
            pass
        return None

    def get_status(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get workflow status with allowed phases.

        Args:
            workflow_id: Workflow identifier

        Returns:
            WorkflowState with current state and allowed_next_phases, or None
        """
        if not workflow_id:
            return None
        try:
            resp = httpx.get(
                f"{self.base_url}/workflow/status",
                params={"workflow_id": workflow_id},
                timeout=3.0,
            )
            if resp.status_code == 200:
                return WorkflowState.from_dict(resp.json())
        except Exception:
            pass
        return None

    def transition(
        self,
        workflow_id: str,
        from_phase: str,
        to_phase: str,
        evidence: Dict[str, Any],
        conditions_met: List[str],
        session_id: Optional[str] = None,
        commit_sha: Optional[str] = None,
    ) -> TransitionResult:
        """Request a phase transition.
        
        The daemon validates the transition against its policy.
        
        Args:
            workflow_id: Workflow ID
            from_phase: Current phase
            to_phase: Target phase
            evidence: Evidence for transition
            conditions_met: List of satisfied conditions
            session_id: Optional session ID
            commit_sha: Optional commit SHA for validation
            
        Returns:
            TransitionResult with success/failure and new state
        """
        try:
            resp = httpx.post(
                f"{self.base_url}/workflow/transition",
                json={
                    "workflow_id": workflow_id,
                    "session_id": session_id,
                    "from_phase": from_phase,
                    "to_phase": to_phase,
                    "evidence": evidence,
                    "conditions_met": conditions_met,
                    "commit_sha": commit_sha,
                },
                timeout=5.0,
            )
            return TransitionResult.from_dict(resp.json())
        except Exception as e:
            return TransitionResult(
                success=False,
                message=f"Daemon unavailable: {e}",
                new_phase=None,
                new_status=None,
                missing_conditions=[],
            )

    def can_stop(self, workflow_id: str) -> CanStopResult:
        """Check if workflow can be stopped.
        
        Returns:
            CanStopResult with can_stop flag and reason
        """
        if not workflow_id:
            return CanStopResult(can_stop=True, reason="No active workflow")
        try:
            resp = httpx.get(
                f"{self.base_url}/workflow/can-stop",
                params={"workflow_id": workflow_id},
                timeout=3.0,
            )
            if resp.status_code == 200:
                return CanStopResult.from_dict(resp.json())
        except Exception as e:
            return CanStopResult(can_stop=True, reason=f"Daemon check failed: {e}")
        return CanStopResult(can_stop=True, reason="Daemon check failed")

    def record_event(
        self,
        workflow_id: str,
        event_type: str,
        phase: str,
        agent: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Record a workflow event.
        
        Events are logged but do NOT trigger phase transitions.
        
        Args:
            workflow_id: Workflow ID
            event_type: Type of event (e.g., "agent_started", "agent_completed")
            phase: Current phase
            agent: Optional agent name
            data: Optional event data
            
        Returns:
            True if recorded successfully
        """
        try:
            resp = httpx.post(
                f"{self.base_url}/event/record",
                json={
                    "workflow_id": workflow_id,
                    "event_type": event_type,
                    "phase": phase,
                    "agent": agent,
                    "data": data or {},
                },
                timeout=3.0,
            )
            return resp.status_code == 200
        except Exception:
            return False

    def record_agent_invoke(self, workflow_id: str, agent_name: str, phase: str) -> bool:
        """Record agent invocation (legacy compatibility wrapper).
        
        Args:
            workflow_id: Workflow ID
            agent_name: Agent name
            phase: Current phase
            
        Returns:
            True if recorded successfully
        """
        return self.record_event(
            workflow_id=workflow_id,
            event_type="agent_started",
            phase=phase,
            agent=agent_name,
            data={},
        )

    def record_agent_complete(self, workflow_id: str, agent_name: str, phase: str) -> bool:
        """Record agent completion (does NOT advance phase).
        
        This only logs the event - phase transitions require
        explicit workflow_transition tool call.
        
        Args:
            agent_name: Agent name
            phase: Current phase
            
        Returns:
            True if recorded successfully
        """
        return self.record_event(
            workflow_id=workflow_id,
            event_type="agent_completed",
            phase=phase,
            agent=agent_name,
        )


# Legacy compatibility: aliases
DaemonControlClient = WorkflowControlClient
ControlClient = WorkflowControlClient
