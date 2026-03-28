"""CVE warnings for technologies in the stack."""

from __future__ import annotations

from stack_score.database import get_tech, resolve_tech


def check_cves(tech_names: list[str]) -> list[dict]:
    """Check all technologies for known CVEs."""
    results = []
    for name in tech_names:
        canonical = resolve_tech(name)
        if not canonical:
            continue
        data = get_tech(canonical)
        if not data:
            continue
        cves = data.get("cves", [])
        if cves:
            results.append({
                "tech": canonical,
                "cves": cves,
                "min_safe_version": data.get("min_safe_version"),
            })
    return results
