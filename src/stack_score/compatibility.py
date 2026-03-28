"""Check pair compatibility between technologies."""

from __future__ import annotations

from stack_score.database import get_tech, resolve_tech


def check_compatibility(tech_a: str, tech_b: str) -> dict:
    """Check if two technologies are compatible."""
    a_canonical = resolve_tech(tech_a)
    b_canonical = resolve_tech(tech_b)

    if not a_canonical or not b_canonical:
        return {
            "compatible": None,
            "reason": f"Unknown technology: {tech_a if not a_canonical else tech_b}",
        }

    a_data = get_tech(a_canonical)
    b_data = get_tech(b_canonical)

    # Check pairs_well_with
    a_pairs = a_data.get("pairs_well_with", [])
    b_pairs = b_data.get("pairs_well_with", [])

    if b_canonical in a_pairs or a_canonical in b_pairs:
        return {"compatible": True, "reason": "These technologies work well together"}

    # Check conflicts
    a_conflicts = a_data.get("conflicts_with", [])
    b_conflicts = b_data.get("conflicts_with", [])

    if b_canonical in a_conflicts or a_canonical in b_conflicts:
        return {"compatible": False, "reason": f"{tech_a} conflicts with {tech_b}"}

    return {"compatible": True, "reason": "No known conflicts"}
