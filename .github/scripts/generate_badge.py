"""Generate an SVG badge showing days since the last buzz cut.

Reads JSON files from results/, finds the most recent date with a recorded
length_mm, computes elapsed days, and renders a styled badge with a barber
clipper icon.
"""

import json
import logging
from datetime import date
from pathlib import Path

RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "badge.svg"

# Color palette – warm amber/gold tones to match the barber-pole icon
BG_COLOR = "#1a1a2e"          # deep navy background
ICON_COLOR = "#e8b84b"        # golden amber (matches classic barber pole/clipper)
DAYS_COLOR = "#f5d98b"        # warm light gold for large number
LABEL_COLOR = "#a89060"       # muted amber for sub-label

# ── Clipper icon path data (100×100 viewBox) ──────────────────────────────────
# Inspired by SVG Repo #257790 "hair-salon-barber".
# The clipper is oriented horizontally: handle on the left, blade on the right.
#
#  ╔══════════════════════════════╗ ┐
#  ║  [●]  CLIPPER BODY           ║─┤ blade head
#  ╚══════════════════════════════╝ ┘
#                                  ╫ teeth
#
CLIPPER_PATH = (
    # Outer body (rounded rectangle)
    "M 12,28 C 12,22 17,18 23,18 L 72,18 C 80,18 84,22 84,28 "
    "L 84,72 C 84,78 80,82 72,82 L 23,82 C 17,82 12,78 12,72 Z "
    # Power button (small circle on body)
    "M 28,50 m -6,0 a 6,6 0 1,0 12,0 a 6,6 0 1,0 -12,0 Z "
    # Blade head (wider protrusion on right)
    "M 84,24 L 90,24 L 90,76 L 84,76 Z "
    # Blade teeth (five narrow rectangles protruding right)
    "M 90,28 L 96,28 L 96,35 L 90,35 Z "
    "M 90,39 L 96,39 L 96,46 L 90,46 Z "
    "M 90,50 L 98,50 L 98,57 L 90,57 Z "
    "M 90,61 L 96,61 L 96,68 L 90,68 Z "
)

BADGE_WIDTH = 240
BADGE_HEIGHT = 80
ICON_SIZE = 56     # icon scaled to 56×56 px inside the badge
ICON_X = 12        # left padding for icon
ICON_Y = (BADGE_HEIGHT - ICON_SIZE) // 2


def load_last_buzz_date() -> date | None:
    """Return the most recent date that has a recorded buzz cut (length_mm not None)."""
    latest: date | None = None
    for path in RESULTS_DIR.glob("????-??-??.json"):
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            if obj.get("length_mm") is None:
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

    # Scale the 100×100 icon path down to ICON_SIZE×ICON_SIZE
    scale = ICON_SIZE / 100.0
    icon_transform = f"translate({ICON_X},{ICON_Y}) scale({scale})"

    # Text positions (right of icon)
    text_x = ICON_X + ICON_SIZE + 14
    days_y = BADGE_HEIGHT // 2 - 4
    label_y = days_y + 22

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{BADGE_WIDTH}" height="{BADGE_HEIGHT}"
     viewBox="0 0 {BADGE_WIDTH} {BADGE_HEIGHT}"
     role="img" aria-label="{days_text} days since last buzz">
  <title>{tooltip}</title>
  <!-- Background -->
  <rect width="{BADGE_WIDTH}" height="{BADGE_HEIGHT}" rx="10" fill="{BG_COLOR}"/>
  <!-- Clipper icon -->
  <g transform="{icon_transform}" fill="{ICON_COLOR}">
    <path d="{CLIPPER_PATH}" fill-rule="evenodd"/>
  </g>
  <!-- Days count (large) -->
  <text x="{text_x}" y="{days_y}"
        font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        font-size="36" font-weight="700"
        fill="{DAYS_COLOR}" dominant-baseline="middle">{days_text} days</text>
  <!-- Label (small) -->
  <text x="{text_x}" y="{label_y}"
        font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        font-size="12" font-weight="400"
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
