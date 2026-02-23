from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Any, List

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from .state import ComplaintState, Category
from . import rules


def _log(state: ComplaintState, message: str) -> None:
    logs = state.get("logs", [])
    logs.append(message)
    state["logs"] = logs


def get_llm() -> ChatOpenAI:
    # Keep it simple: reads OPENAI_API_KEY from environment if set
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def intake_node(state: ComplaintState) -> ComplaintState:
    """Step 1: Intake - parse and categorize + essentials + dedupe stub."""
    complaint = state["complaint"]
    llm = get_llm()

    prompt = f"""Categorize this Downside Up complaint into exactly one category:
- portal
- monster
- psychic
- environmental
- other

Complaint: {complaint}

Respond with ONLY the category name."""
    category_text = llm.invoke([HumanMessage(content=prompt)]).content.strip().lower()

    # Hard-guard: coerce to allowed categories
    allowed = {"portal", "monster", "psychic", "environmental", "other"}
    category: Category = category_text if category_text in allowed else "other"  # type: ignore

    essentials = rules.extract_essentials(complaint)

    new_state: ComplaintState = {
        **state,
        "category": category,
        "essentials": essentials,
        "workflow_path": state.get("workflow_path", []) + ["intake"],
        "status": "intake",
    }

    _log(new_state, f"[INTAKE] Categorized as '{category}'.")
    return new_state


def validate_node(state: ComplaintState) -> ComplaintState:
    """Step 2: Validate - enforce category-specific validity + essentials threshold."""
    complaint = state["complaint"]
    category = state.get("category", "other")  # type: ignore
    essentials = state.get("essentials", {})

    valid_by_category, errors = rules.validate_by_category(category, complaint)

    # Essentials gate (placeholder threshold)
    essentials_ok = rules.has_minimum_essentials(essentials)
    if not essentials_ok:
        errors.append("Missing essential details; request clarification (who/what/when/where).")

    is_valid = valid_by_category and essentials_ok
    status = "validate" if is_valid else ("escalated" if category == "other" else "rejected")

    new_state: ComplaintState = {
        **state,
        "is_valid": is_valid,
        "validation_errors": errors,
        "workflow_path": state.get("workflow_path", []) + ["validate"],
        "status": status,  # validate/rejected/escalated
    }

    _log(new_state, f"[VALIDATE] is_valid={is_valid}. Errors={errors}")
    return new_state


def investigate_node(state: ComplaintState) -> ComplaintState:
    """Step 3: Investigate - must produce documented evidence."""
    category = state.get("category", "other")  # type: ignore

    evidence: Dict[str, Any] = {
        "category": category,
        "notes": "Placeholder investigation evidence. Replace with category-specific evidence gathering.",
    }

    new_state: ComplaintState = {
        **state,
        "evidence": evidence,
        "workflow_path": state.get("workflow_path", []) + ["investigate"],
        "status": "investigate",
    }
    _log(new_state, "[INVESTIGATE] Evidence documented.")
    return new_state


def resolve_node(state: ComplaintState) -> ComplaintState:
    """Step 4: Resolve - requires evidence; include protocol reference + effectiveness rating."""
    category = state.get("category", "other")  # type: ignore
    evidence = state.get("evidence")

    # Hard gate: if no evidence, resolution should not proceed (we still keep placeholder safe)
    if not evidence:
        resolution = "Cannot resolve: missing investigation evidence."
        effectiveness = "low"
        requires_escalation = True
    else:
        resolution = f"Apply Downside Up Protocol for '{category}' based on documented evidence."
        effectiveness = "medium"
        requires_escalation = category in {"monster", "environmental"}

    new_state: ComplaintState = {
        **state,
        "resolution": resolution,
        "effectiveness": effectiveness,  # type: ignore
        "requires_escalation": requires_escalation,
        "workflow_path": state.get("workflow_path", []) + ["resolve"],
        "status": "resolve",
    }
    _log(new_state, f"[RESOLVE] {resolution} (effectiveness={effectiveness})")
    return new_state


def close_node(state: ComplaintState) -> ComplaintState:
    """Step 5: Close - confirm applied + satisfaction attempted + log timestamp + follow-up if low."""
    effectiveness = state.get("effectiveness", "medium")
    follow_up_required = effectiveness == "low"

    new_state: ComplaintState = {
        **state,
        "applied": True,  # placeholder
        "customer_satisfaction_attempted": True,  # placeholder
        "outcome": "closed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "follow_up_required": follow_up_required,
        "workflow_path": state.get("workflow_path", []) + ["close"],
        "status": "close",
    }
    _log(new_state, f"[CLOSE] Closed. follow_up_required={follow_up_required}")
    return new_state