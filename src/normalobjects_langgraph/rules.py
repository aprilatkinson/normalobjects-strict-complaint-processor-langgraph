from __future__ import annotations

from typing import Dict, Optional, List, Tuple, Any
from .state import Category


def extract_essentials(complaint: str) -> Dict[str, Optional[str]]:
    """
    Placeholder extractor.
    Later we can use an LLM or simple heuristics to extract who/what/when/where.
    """
    return {"who": None, "what": None, "when": None, "where": None}


def has_minimum_essentials(essentials: Dict[str, Optional[str]]) -> bool:
    """
    Minimum required detail for processing.
    Lab requirement: missing who/what/when/where should be flagged for clarification.
    You can decide the threshold later (e.g., require what + (when or where)).
    """
    # Conservative placeholder: require 'what' at minimum
    return bool(essentials.get("what"))


def validate_by_category(category: Category, complaint: str) -> Tuple[bool, List[str]]:
    """
    Encodes Bloyce's Protocol validation rules.
    Returns (is_valid, errors).
    """
    errors: List[str] = []

    if category == "portal":
        # Must reference specific location or timing anomalies
        if not any(k in complaint.lower() for k in ["time", "timing", "when", "location", "where", "opens", "close"]):
            errors.append("Portal complaints must reference timing or location anomalies.")
    elif category == "monster":
        # Must describe creature behavior or interactions
        if not any(k in complaint.lower() for k in ["attack", "behavior", "fight", "hunting", "interaction", "demogorgon", "creature"]):
            errors.append("Monster complaints must describe creature behavior or interactions.")
    elif category == "psychic":
        # Must reference ability limitations or malfunctions
        if not any(k in complaint.lower() for k in ["can’t", "cant", "cannot", "ability", "limit", "malfunction", "telekinesis", "mind"]):
            errors.append("Psychic complaints must reference ability limitations or malfunctions.")
    elif category == "environmental":
        # Must connect to electricity/weather/observable phenomena
        if not any(k in complaint.lower() for k in ["power", "electric", "line", "storm", "weather", "atmosphere", "lights"]):
            errors.append("Environmental complaints must connect to electricity, weather, or observable phenomena.")
    elif category == "other":
        # Automatically escalated, not "invalid" per se — but not routable
        errors.append("Other category complaints require manual review (auto-escalation).")
    else:
        errors.append("Unknown category.")

    return (len(errors) == 0, errors)


def requires_manual_review(category: Category) -> bool:
    return category == "other"