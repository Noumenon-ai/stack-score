"""Recommend technologies based on use case."""

from __future__ import annotations

from stack_score.database import PROVEN_STACKS


def suggest_for_use_case(use_case: str) -> list[dict]:
    """Suggest proven stacks for a use case."""
    use_case_lower = use_case.lower()
    results = []

    for name, stack in PROVEN_STACKS.items():
        desc_lower = stack["description"].lower()
        uc_lower = stack["use_case"].lower()
        name_lower = name.replace("_", " ")

        if (use_case_lower in desc_lower or
            use_case_lower in uc_lower or
            use_case_lower in name_lower):
            results.append({
                "name": name,
                "techs": stack["techs"],
                "description": stack["description"],
                "use_case": stack["use_case"],
            })

    return results


def get_popular_stacks(limit: int = 10) -> list[dict]:
    """Return the top proven stacks."""
    return [
        {
            "name": name,
            "techs": stack["techs"],
            "description": stack["description"],
            "use_case": stack["use_case"],
        }
        for name, stack in list(PROVEN_STACKS.items())[:limit]
    ]
