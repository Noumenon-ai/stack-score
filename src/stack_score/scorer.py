"""Calculate 7-dimension score for a tech stack."""

from __future__ import annotations

from dataclasses import dataclass, field

from stack_score.database import get_tech, resolve_tech


@dataclass
class DimensionScore:
    name: str
    score: int
    notes: str


@dataclass
class StackScore:
    techs: list[str]
    resolved: list[str]
    unknown: list[str]
    dimensions: list[DimensionScore]
    overall: int
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    proven_combos: list[str] = field(default_factory=list)

    @property
    def rating(self) -> str:
        if self.overall >= 85:
            return "EXCELLENT"
        elif self.overall >= 70:
            return "STRONG"
        elif self.overall >= 50:
            return "DECENT"
        elif self.overall >= 30:
            return "WEAK"
        return "AVOID"


def score_stack(tech_names: list[str]) -> StackScore:
    """Score a tech stack across 7 dimensions."""
    resolved = []
    unknown = []
    tech_data = []

    for name in tech_names:
        canonical = resolve_tech(name)
        if canonical:
            resolved.append(canonical)
            tech_data.append(get_tech(canonical))
        else:
            unknown.append(name)

    if not tech_data:
        return StackScore(
            techs=tech_names,
            resolved=[],
            unknown=unknown,
            dimensions=[],
            overall=0,
            warnings=["No recognized technologies found."],
        )

    dimensions = [
        _score_compatibility(resolved, tech_data),
        _score_security(tech_data),
        _score_community(tech_data),
        _score_performance(tech_data),
        _score_cost(tech_data),
        _score_learning_curve(tech_data),
        _score_maintenance(tech_data),
    ]

    overall = round(sum(d.score for d in dimensions) / len(dimensions))

    warnings = _collect_warnings(tech_data)
    suggestions = _generate_suggestions(resolved)
    proven = _find_proven_combos(resolved)

    return StackScore(
        techs=tech_names,
        resolved=resolved,
        unknown=unknown,
        dimensions=dimensions,
        overall=overall,
        warnings=warnings,
        suggestions=suggestions,
        proven_combos=proven,
    )


def _score_compatibility(resolved: list[str], data: list[dict]) -> DimensionScore:
    """Score how well the technologies work together."""
    if len(resolved) <= 1:
        return DimensionScore("Compatibility", 100, "Single technology — no conflicts")

    pair_scores = []
    conflicts = []

    for i, tech in enumerate(resolved):
        td = data[i]
        pairs = td.get("pairs_well_with", [])
        conf = td.get("conflicts_with", [])

        for j, other in enumerate(resolved):
            if i == j:
                continue
            if other in pairs:
                pair_scores.append(1.0)
            elif other in conf:
                pair_scores.append(0.0)
                conflicts.append(f"{tech} conflicts with {other}")
            else:
                pair_scores.append(0.5)

    score = round((sum(pair_scores) / max(len(pair_scores), 1)) * 100)
    notes = f"{len(conflicts)} conflicts" if conflicts else "All tools work well together"
    if conflicts:
        notes = ", ".join(conflicts[:2])
    return DimensionScore("Compatibility", min(score, 100), notes)


def _score_security(data: list[dict]) -> DimensionScore:
    """Score based on known CVEs."""
    total_cves = sum(len(d.get("cves", [])) for d in data)
    if total_cves == 0:
        return DimensionScore("Security", 100, "No known CVEs")
    elif total_cves <= 2:
        cve_names = []
        for d in data:
            cve_names.extend(d.get("cves", []))
        return DimensionScore("Security", 72, f"{total_cves} CVEs: {', '.join(cve_names[:2])}")
    else:
        return DimensionScore("Security", max(40, 100 - total_cves * 10), f"{total_cves} CVEs found")


def _score_community(data: list[dict]) -> DimensionScore:
    """Score based on GitHub stars and maintenance."""
    stars = [d.get("github_stars", 0) for d in data]
    avg_stars = sum(stars) / max(len(stars), 1)
    if avg_stars >= 50000:
        return DimensionScore("Community", 98, "All have massive communities")
    elif avg_stars >= 20000:
        return DimensionScore("Community", 85, "Strong community support")
    elif avg_stars >= 5000:
        return DimensionScore("Community", 70, "Growing community")
    return DimensionScore("Community", 50, "Smaller communities — less help available")


def _score_performance(data: list[dict]) -> DimensionScore:
    """Score based on performance ratings."""
    perfs = [d.get("performance", 7) for d in data]
    avg = sum(perfs) / max(len(perfs), 1)
    score = round(avg * 10)
    if score >= 90:
        notes = "Excellent performance characteristics"
    elif score >= 70:
        notes = "Good performance for most use cases"
    else:
        notes = "May have performance bottlenecks"
    return DimensionScore("Performance", min(score, 100), notes)


def _score_cost(data: list[dict]) -> DimensionScore:
    """Score based on cost at scale."""
    costs = [d.get("cost_at_scale", 7) for d in data]
    avg = sum(costs) / max(len(costs), 1)
    score = round(avg * 10)
    if score >= 90:
        notes = "Cheap at any scale"
    elif score >= 70:
        notes = "Manageable costs at scale"
    else:
        notes = "Watch costs carefully at scale"
    return DimensionScore("Cost at Scale", min(score, 100), notes)


def _score_learning_curve(data: list[dict]) -> DimensionScore:
    """Score based on learning curve (lower is easier, but invert for score)."""
    curves = [d.get("learning_curve", 5) for d in data]
    avg = sum(curves) / max(len(curves), 1)
    # Invert: 1 (easy) = 100, 10 (hard) = 10
    score = round(100 - (avg - 1) * 10)
    if score >= 80:
        notes = "Easy to learn and use"
    elif score >= 60:
        notes = "Moderate learning curve"
    else:
        notes = "Steep learning curve — invest in training"
    return DimensionScore("Learning Curve", max(score, 10), notes)


def _score_maintenance(data: list[dict]) -> DimensionScore:
    """Score based on maintenance status."""
    maintained = sum(1 for d in data if d.get("maintained", False))
    ratio = maintained / max(len(data), 1)
    score = round(ratio * 100)
    if score == 100:
        notes = "All actively maintained in 2026"
    else:
        notes = f"{len(data) - maintained} unmaintained technologies"
    return DimensionScore("Maintenance", score, notes)


def _collect_warnings(data: list[dict]) -> list[str]:
    """Collect all warnings from tech data."""
    warnings = []
    for d in data:
        for w in d.get("warnings", []):
            warnings.append(w)
        if d.get("min_safe_version"):
            name = d.get("description", "").split(" ")[0] if d.get("description") else "Tech"
            warnings.append(f"Patch to >= {d['min_safe_version']} ({', '.join(d.get('cves', [])[:2])})")
    return warnings


def _generate_suggestions(resolved: list[str]) -> list[str]:
    """Suggest complementary technologies."""
    suggestions = []
    categories_present = set()

    for name in resolved:
        td = get_tech(name)
        if td:
            categories_present.add(td.get("category", ""))

    if "monitoring" not in categories_present:
        suggestions.append("Consider adding: Sentry (error monitoring)")
    if "email" not in categories_present and "auth" not in categories_present:
        suggestions.append("Consider adding: Resend (email)")
    if "devops" not in categories_present and "hosting" not in categories_present:
        suggestions.append("Consider adding: Docker (containerization)")

    return suggestions[:3]


def _find_proven_combos(resolved: list[str]) -> list[str]:
    """Find any proven stack combinations in the tech list."""
    from stack_score.database import PROVEN_STACKS

    combos = []
    resolved_set = set(resolved)

    for name, stack in PROVEN_STACKS.items():
        stack_set = set(stack["techs"])
        overlap = resolved_set & stack_set
        if len(overlap) >= 2:
            combos.append(f"{' + '.join(sorted(overlap))}: {stack['description']}")

    return combos[:3]
