from __future__ import annotations

from typing import Literal, Optional, TypedDict, List, Dict, Any


Category = Literal["portal", "monster", "psychic", "environmental", "other"]
Status = Literal["new", "intake", "validate", "investigate", "resolve", "close", "rejected", "escalated"]


class ComplaintState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.
    total=False means keys are optional until set by a node.
    """

    # Input
    complaint: str
    complainant_id: str  # used for dedupe/linking; can be a placeholder in lab

    # Intake outputs
    category: Category
    essentials: Dict[str, Optional[str]]  # who/what/when/where extracted (can be partial)
    is_duplicate: bool
    duplicate_of: Optional[str]  # complaint/case id if linked

    # Validation outputs
    is_valid: bool
    validation_errors: List[str]

    # Investigation outputs
    evidence: Dict[str, Any]  # documented evidence (structure depends on category)

    # Resolution outputs
    resolution: str
    effectiveness: Literal["high", "medium", "low"]
    requires_escalation: bool

    # Closure outputs
    applied: bool
    customer_satisfaction_attempted: bool
    outcome: str
    timestamp: str
    follow_up_required: bool

    # Audit / tracing
    workflow_path: List[str]
    status: Status
    logs: List[str]