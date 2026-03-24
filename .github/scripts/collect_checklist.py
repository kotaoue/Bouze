"""Parse GFM checkboxes from a PR body and write results to a JSON file.

Reads PR data from /tmp/pr_data.json and uses the following environment variables:
  CHECKLIST_DATE  – date string to embed in the output (e.g. "2026-03-24")
  OUTPUT_FILE     – path to write the result JSON (e.g. "results/2026-03-24.json")
"""

import json
import os
import sys
from pathlib import Path


def parse_checks(body: str) -> dict[str, bool]:
    """Return an ordered dict of checkbox label → checked state."""
    checks: dict[str, bool] = {}
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("- [x] ") or line.startswith("- [X] "):
            checks[line[6:]] = True
        elif line.startswith("- [ ] "):
            checks[line[6:]] = False
    return checks


def main() -> None:
    with open("/tmp/pr_data.json") as f:
        pr = json.load(f)

    body = pr.get("body") or ""
    checks = parse_checks(body)

    if not checks:
        print("error: no checklist items found in pull request body", file=sys.stderr)
        sys.exit(1)

    checklist_date = os.environ["CHECKLIST_DATE"]
    output_file = Path(os.environ["OUTPUT_FILE"])

    content = json.dumps({"date": checklist_date, "checks": checks}, indent=2)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content)
    print(f"Written {output_file}")


if __name__ == "__main__":
    main()
