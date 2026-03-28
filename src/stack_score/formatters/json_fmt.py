"""JSON output formatter."""

import json
from datetime import datetime, timezone

from stack_score.scorer import StackScore


def format_json(result: StackScore) -> str:
    """Format stack score as JSON string."""
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stack": result.resolved,
        "unknown": result.unknown,
        "overall": result.overall,
        "rating": result.rating,
        "dimensions": [
            {"name": d.name, "score": d.score, "notes": d.notes}
            for d in result.dimensions
        ],
        "warnings": result.warnings,
        "suggestions": result.suggestions,
        "proven_combos": result.proven_combos,
    }
    return json.dumps(output, indent=2)
