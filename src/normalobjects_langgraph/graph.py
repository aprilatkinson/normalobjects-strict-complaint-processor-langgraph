from __future__ import annotations

from langgraph.graph import StateGraph, END

from .state import ComplaintState
from .nodes import intake_node, validate_node, investigate_node, resolve_node, close_node


def route_after_validate(state: ComplaintState) -> str:
    """
    Conditional routing after validation:
    - If rejected -> END
    - If escalated -> END (manual review)
    - Else continue to investigate
    """
    status = state.get("status", "validate")
    if status in {"rejected", "escalated"}:
        return "end"
    return "investigate"


def build_app():
    workflow = StateGraph(ComplaintState)

    workflow.add_node("intake", intake_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("investigate", investigate_node)
    workflow.add_node("resolve", resolve_node)
    workflow.add_node("close", close_node)

    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "validate")

    workflow.add_conditional_edges(
        "validate",
        route_after_validate,
        {
            "investigate": "investigate",
            "end": END,
        },
    )

    workflow.add_edge("investigate", "resolve")
    workflow.add_edge("resolve", "close")
    workflow.add_edge("close", END)

    return workflow.compile()