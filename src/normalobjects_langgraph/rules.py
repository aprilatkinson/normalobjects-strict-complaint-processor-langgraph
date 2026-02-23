from __future__ import annotations

from typing import Dict, Optional, List, Tuple, Any
from .state import Category


import re
from typing import Dict, Optional

def extract_essentials(complaint: str) -> Dict[str, Optional[str]]:
    """
    Minimal, deterministic extractor for lab flow.
    Goal: reliably populate at least 'what' so valid complaints can proceed.
    """
    text = complaint.strip()
    lower = text.lower()

    # WHAT: use the complaint itself as the "what" (good enough for lab + traceability)
    what = text if text else None

    # WHO: detect a likely named entity at the start (e.g., "El ..."), otherwise None
    # Simple heuristic: first word capitalized and not "The"/"This"/"Why"/"How"/"Demogorgons"
    first_word = re.split(r"\s+", text)[0] if text else ""
    stop = {"The", "This", "Why", "How", "Demogorgons", "El"}  # keep El special-case below
    who = None
    if first_word == "El":
        who = "El"
    elif first_word and first_word[0].isupper() and first_word not in stop:
        who = first_word

    # WHEN: if mentions time-ish terms
    when = None
    if any(k in lower for k in ["today", "yesterday", "tomorrow", "each day", "every day", "daily", "at", "when", "time", "timing"]):
        when = "mentioned"

    # WHERE: if mentions location-ish terms
    where = None
    if any(k in lower for k in ["location", "where", "here", "there", "in ", "at "]):
        # We keep it simple: just mark that location is referenced
        where = "mentioned"

    return {"who": who, "what": what, "when": when, "where": where}


def has_minimum_essentials(essentials: Dict[str, Optional[str]]) -> bool:
    """
    Lab-friendly threshold: require at least 'what'.
    (The protocol says missing details should be flagged; we can still flag later
     without blocking every complaint.)
    """
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