"""Rich terminal table output formatter."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from stack_score import __version__
from stack_score.scorer import StackScore

console = Console()

RATING_COLORS = {
    "EXCELLENT": "bold green",
    "STRONG": "green",
    "DECENT": "yellow",
    "WEAK": "red",
    "AVOID": "bold red",
}


def print_score(result: StackScore) -> None:
    """Print stack score as a rich terminal table."""
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]STACK-SCORE[/] v{__version__}",
        border_style="cyan",
    ))
    console.print()
    console.print(f"  Stack: [bold]{', '.join(result.resolved)}[/]")
    if result.unknown:
        console.print(f"  [yellow]Unknown: {', '.join(result.unknown)}[/]")
    console.print()

    # Dimensions table
    table = Table(border_style="dim", show_lines=False)
    table.add_column("Dimension", style="bold")
    table.add_column("Score", justify="right")
    table.add_column("Notes")

    for d in result.dimensions:
        color = "green" if d.score >= 80 else "yellow" if d.score >= 60 else "red"
        table.add_row(d.name, f"[{color}]{d.score}/100[/{color}]", d.notes)

    console.print(table)
    console.print()

    # Overall score with bar
    bar_len = 20
    filled = int(bar_len * result.overall / 100)
    rating_color = RATING_COLORS.get(result.rating, "white")
    bar = "[green]" + "█" * filled + "[/]" + "[dim]" + "░" * (bar_len - filled) + "[/]"
    console.print(f"  Overall: {bar} [{rating_color}]{result.overall}/100 {result.rating}[/{rating_color}]")
    console.print()

    # Warnings
    if result.warnings:
        console.print("  [yellow]Warnings:[/]")
        for w in result.warnings:
            console.print(f"    [yellow]•[/] {w}")
        console.print()

    # Proven combos
    if result.proven_combos:
        console.print("  [green]Proven Combos:[/]")
        for c in result.proven_combos:
            console.print(f"    [green]•[/] {c}")
        console.print()

    # Suggestions
    if result.suggestions:
        console.print("  [cyan]Suggestions:[/]")
        for s in result.suggestions:
            console.print(f"    [cyan]•[/] {s}")
        console.print()


def print_comparison(stacks: list[StackScore]) -> None:
    """Print a comparison table of multiple stacks."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]STACK-SCORE[/] — Comparison",
        border_style="cyan",
    ))
    console.print()

    table = Table(border_style="dim")
    table.add_column("Dimension", style="bold")

    for s in stacks:
        table.add_column(", ".join(s.resolved[:2]), justify="center")

    dim_names = [d.name for d in stacks[0].dimensions] if stacks else []
    for dim_name in dim_names:
        row = [dim_name]
        for s in stacks:
            for d in s.dimensions:
                if d.name == dim_name:
                    color = "green" if d.score >= 80 else "yellow" if d.score >= 60 else "red"
                    row.append(f"[{color}]{d.score}[/{color}]")
                    break
        table.add_row(*row)

    # Overall row
    row = ["[bold]Overall[/]"]
    for s in stacks:
        color = RATING_COLORS.get(s.rating, "white")
        row.append(f"[{color}]{s.overall} {s.rating}[/{color}]")
    table.add_row(*row)

    console.print(table)
    console.print()


def print_popular(stacks: list[dict]) -> None:
    """Print popular stacks."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]STACK-SCORE[/] — Popular Stacks",
        border_style="cyan",
    ))
    console.print()

    table = Table(border_style="dim")
    table.add_column("Stack", style="bold")
    table.add_column("Technologies")
    table.add_column("Use Case")

    for s in stacks:
        table.add_row(
            s["name"].replace("_", " ").title(),
            ", ".join(s["techs"]),
            s["use_case"],
        )

    console.print(table)
    console.print()
