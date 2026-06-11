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


def test_rating_bands():
    from stack_score.scorer import StackScore
    def with_overall(n):
        return StackScore(techs=[], resolved=[], unknown=[], dimensions=[], overall=n)
    assert with_overall(87).rating == "EXCELLENT"
    assert with_overall(84).rating == "STRONG"
    assert with_overall(55).rating == "DECENT"
    assert with_overall(35).rating == "WEAK"
    assert with_overall(10).rating == "AVOID"


def test_version_word_not_scored_as_tech():
    from typer.testing import CliRunner
    from stack_score.cli import app
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "stack-score v" in result.output
    assert "AVOID" not in result.output


def test_version_flag():
    from typer.testing import CliRunner
    from stack_score.cli import app
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "stack-score v" in result.output
