from __future__ import annotations

from typing import Any
from .state import ComplaintState


def summarize_run(state: ComplaintState) -> str:
    path = " → ".join(state.get("workflow_path", []))
    category = state.get("category", "unknown")
    status = state.get("status", "unknown")
    is_valid = state.get("is_valid", None)
    effectiveness = state.get("effectiveness", None)

    return (
        f"Path: {path}\n"
        f"Category: {category}\n"
        f"Status: {status}\n"
        f"Valid: {is_valid}\n"
        f"Effectiveness: {effectiveness}\n"
    )