"""Generate an SVG badge showing days since the last buzz cut.

Reads JSON files from results/, finds the most recent date with a recorded
length_mm, computes elapsed days, and renders a styled text badge.
"""

import json
import logging
from datetime import date
from pathlib import Path

RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "badge.svg"

# Color palette – warm amber/gold tones
BG_COLOR = "#1a1a2e"          # deep navy background
DAYS_COLOR = "#f5d98b"        # warm light gold for large number
LABEL_COLOR = "#a89060"       # muted amber for sub-label

BADGE_WIDTH = 200
BADGE_HEIGHT = 80


def load_last_buzz_date() -> date | None:
    """Return the most recent date that has a recorded buzz cut (any checkbox checked)."""
    latest: date | None = None
    for path in RESULTS_DIR.glob("????-??-??.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            checks = obj.get("checks", {})
            if not any(checks.values()):
                continue
            d = date.fromisoformat(obj["date"])
            if latest is None or d > latest:
                latest = d
        except Exception as exc:
            logging.warning("Skipping %s: %s", path.name, exc)
    return latest


def generate_svg(days: int | None, last_date: date | None) -> str:
    """Render the badge as an SVG string.

    Args:
        days: Number of days since last buzz cut, or None if no record exists.
        last_date: The date of the last buzz cut, used in the tooltip.

    Returns:
        The complete SVG document as a string.
    """
    if days is None:
        days_text = "—"
    else:
        days_text = str(days)

    tooltip = f"Last buzz: {last_date.isoformat()}" if last_date else "No records yet"

    # Center text horizontally
    cx = BADGE_WIDTH // 2
    days_y = BADGE_HEIGHT // 2 - 8
    label_y = days_y + 24

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{BADGE_WIDTH}" height="{BADGE_HEIGHT}"
     viewBox="0 0 {BADGE_WIDTH} {BADGE_HEIGHT}"
     role="img" aria-label="{days_text} days since last buzz">
  <title>{tooltip}</title>
  <!-- Background -->
  <rect width="{BADGE_WIDTH}" height="{BADGE_HEIGHT}" rx="10" fill="{BG_COLOR}"/>
  <!-- Days count (large) -->
  <text x="{cx}" y="{days_y}"
        font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        font-size="36" font-weight="700" text-anchor="middle"
        fill="{DAYS_COLOR}" dominant-baseline="middle">{days_text} days</text>
  <!-- Label (small) -->
  <text x="{cx}" y="{label_y}"
        font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="400" text-anchor="middle"
        fill="{LABEL_COLOR}" dominant-baseline="middle">since last buzz</text>
</svg>"""
    return svg


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
    today = date.today()
    last = load_last_buzz_date()
    days = (today - last).days if last is not None else None
    svg = generate_svg(days, last)
    OUTPUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}  (days since last buzz: {days}, last: {last})")
