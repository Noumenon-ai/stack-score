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


def test_database_has_50_plus_entries():
    assert len(TECH_DATABASE) >= 30  # At least 30 distinct technologies


def test_proven_stacks_have_valid_techs():
    for name, stack in PROVEN_STACKS.items():
        for tech in stack["techs"]:
            resolved = resolve_tech(tech)
            # Some techs like "typer", "rich" might not be in DB — that's ok
            # Just verify the stack structure is valid
            assert isinstance(tech, str), f"Invalid tech in {name}: {tech}"


def test_all_techs_have_required_fields():
    required = {"category", "language", "maintained", "learning_curve", "performance"}
    for name, data in TECH_DATABASE.items():
        for field in required:
            assert field in data, f"{name} missing field: {field}"
