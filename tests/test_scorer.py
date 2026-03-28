"""Tests for the stack scorer."""

from stack_score.scorer import score_stack


def test_strong_stack():
    result = score_stack(["next.js", "tailwind", "supabase"])
    assert result.overall > 70
    assert result.rating in ("STRONG", "EXCELLENT")
    assert len(result.dimensions) == 7


def test_weak_stack():
    result = score_stack(["react", "vue"])  # Conflicting frameworks
    # Should detect the conflict
    compat = next(d for d in result.dimensions if d.name == "Compatibility")
    assert compat.score < 100


def test_unknown_tech():
    result = score_stack(["next.js", "nonexistent-tech"])
    assert "nonexistent-tech" in result.unknown
    assert "next.js" in result.resolved


def test_single_tech():
    result = score_stack(["next.js"])
    assert result.overall > 0
    assert len(result.dimensions) == 7


def test_empty_stack():
    result = score_stack(["totally-fake-tech"])
    assert result.overall == 0
    assert len(result.warnings) > 0


def test_proven_combos_detected():
    result = score_stack(["next.js", "tailwind", "supabase", "stripe", "vercel"])
    assert len(result.proven_combos) > 0


def test_suggestions_generated():
    result = score_stack(["next.js", "tailwind"])
    assert len(result.suggestions) > 0


def test_cve_warnings():
    result = score_stack(["next.js", "react"])
    assert len(result.warnings) > 0  # Both have CVEs
