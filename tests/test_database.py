"""Tests for the tech database."""

from stack_score.database import get_tech, resolve_tech, PROVEN_STACKS, TECH_DATABASE


def test_resolve_alias():
    assert resolve_tech("nextjs") == "next.js"
    assert resolve_tech("tailwindcss") == "tailwind"
    assert resolve_tech("postgres") == "postgresql"
    assert resolve_tech("rn") == "react-native"


def test_resolve_canonical():
    assert resolve_tech("next.js") == "next.js"
    assert resolve_tech("react") == "react"


def test_resolve_unknown():
    assert resolve_tech("nonexistent") is None


def test_get_tech():
    data = get_tech("next.js")
    assert data is not None
    assert data["category"] == "framework"
    assert data["maintained"] is True


def test_get_tech_via_alias():
    data = get_tech("nextjs")
    assert data is not None
    assert data["category"] == "framework"


def test_database_has_40_plus_entries():
    assert len(TECH_DATABASE) >= 40


def test_proven_stacks_have_valid_techs():
    # Every tech referenced by a proven stack must resolve to a DB entry.
    for name, stack in PROVEN_STACKS.items():
        for tech in stack["techs"]:
            assert resolve_tech(tech) is not None, f"Unresolvable tech in {name}: {tech}"


def test_all_cve_identifiers_are_well_formed():
    import re
    cve_pattern = re.compile(r"^CVE-\d{4}-\d{4,}$")
    ghsa_pattern = re.compile(r"^GHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}$")
    for name, data in TECH_DATABASE.items():
        for cve in data.get("cves", []):
            assert cve_pattern.match(cve) or ghsa_pattern.match(cve), (
                f"{name} has malformed security identifier: {cve}"
            )


def test_nextjs_min_safe_version_matches_advisory():
    # CVE-2025-29927 (GHSA-f82v-jwr5-mffw): first patched 15.x version is 15.2.3
    data = get_tech("next.js")
    assert "CVE-2025-29927" in data["cves"]
    assert data["min_safe_version"] == "15.2.3"


def test_all_techs_have_required_fields():
    required = {"category", "language", "maintained", "learning_curve", "performance"}
    for name, data in TECH_DATABASE.items():
        for field in required:
            assert field in data, f"{name} missing field: {field}"
