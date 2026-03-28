"""Stack-Score CLI — command definitions."""

import re
from typing import Optional

import typer
from rich.console import Console

from stack_score import __version__
from stack_score.database import get_tech, resolve_tech
from stack_score.formatters.json_fmt import format_json
from stack_score.formatters.table import print_comparison, print_popular, print_score
from stack_score.scorer import score_stack
from stack_score.suggestions import get_popular_stacks, suggest_for_use_case

app = typer.Typer(
    name="stack-score",
    help="Rate any tech stack before you build.",
    no_args_is_help=True,
    invoke_without_command=True,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    stack: Optional[str] = typer.Argument(None, help="Tech stack to score (e.g. 'next.js tailwind supabase')"),
    detail: bool = typer.Option(False, "--detail", "-d", help="Show detailed info for single tech"),
    popular: bool = typer.Option(False, "--popular", help="Show top 10 proven stacks"),
    use_case: Optional[str] = typer.Option(None, "--for", help="Best stack for use case"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table or json"),
) -> None:
    """Score a tech stack or compare alternatives."""
    if popular:
        stacks = get_popular_stacks()
        print_popular(stacks)
        return

    if use_case:
        results = suggest_for_use_case(use_case)
        if results:
            print_popular(results)
        else:
            console.print(f"  [yellow]No proven stacks found for '{use_case}'[/]")
            console.print("  Try: ecommerce, saas, blog, api, mobile, cli, landing")
        return

    if not stack:
        return

    # Check for comparison mode: "react vs vue vs svelte"
    if " vs " in stack.lower():
        _handle_comparison(stack, format)
        return

    # Check for single tech detail mode
    if detail:
        _handle_detail(stack)
        return

    # Parse tech names
    tech_names = _parse_stack_string(stack)
    result = score_stack(tech_names)

    if format == "json":
        console.print(format_json(result))
    else:
        print_score(result)


def _handle_comparison(stack_str: str, format: str) -> None:
    """Handle 'tech1 vs tech2 vs tech3' comparison."""
    alternatives = [s.strip() for s in re.split(r"\s+vs\s+", stack_str, flags=re.IGNORECASE)]
    results = [score_stack([alt]) for alt in alternatives]

    if format == "json":
        import json
        output = [{"tech": r.resolved, "overall": r.overall, "rating": r.rating} for r in results]
        console.print(json.dumps(output, indent=2))
    else:
        print_comparison(results)


def _handle_detail(tech_name: str) -> None:
    """Show detailed info for a single technology."""
    canonical = resolve_tech(tech_name.strip())
    if not canonical:
        console.print(f"  [red]Unknown technology: {tech_name}[/]")
        return

    data = get_tech(canonical)
    console.print()
    console.print(f"  [bold cyan]{canonical}[/] — {data.get('description', '')}")
    console.print(f"  Category: {data.get('category', 'unknown')}")
    console.print(f"  Language: {data.get('language', 'unknown')}")
    console.print(f"  GitHub Stars: {data.get('github_stars', 0):,}")
    console.print(f"  Last Release: {data.get('last_release', 'unknown')}")
    console.print(f"  Learning Curve: {data.get('learning_curve', '?')}/10")
    console.print(f"  Performance: {data.get('performance', '?')}/10")
    console.print(f"  Cost: {data.get('cost', 'unknown')}")

    pairs = data.get("pairs_well_with", [])
    if pairs:
        console.print(f"  Pairs well with: {', '.join(pairs)}")

    cves = data.get("cves", [])
    if cves:
        console.print(f"  [yellow]CVEs: {', '.join(cves)}[/]")
        if data.get("min_safe_version"):
            console.print(f"  [yellow]Min safe version: {data['min_safe_version']}[/]")

    console.print()


def _parse_stack_string(stack: str) -> list[str]:
    """Parse a stack string into individual tech names."""
    # Handle: "next.js + tailwind + supabase" or "next.js tailwind supabase"
    stack = stack.replace("+", " ").replace(",", " ")
    return [t.strip() for t in stack.split() if t.strip()]


@app.command()
def version() -> None:
    """Show stack-score version."""
    console.print(f"stack-score v{__version__}")


if __name__ == "__main__":
    app()
