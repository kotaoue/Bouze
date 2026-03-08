"""Parse buzz cut checklist from PR body and save result as JSON."""

import json
import os
import re
import sys

title = os.environ.get('PR_TITLE', '').strip()
body = os.environ.get('PR_BODY', '')

if not title:
    print("ERROR: PR_TITLE environment variable is required", file=sys.stderr)
    sys.exit(1)

if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', title):
    print(f"SKIP: PR_TITLE '{title}' is not in YYYY-MM-DD format")
    sys.exit(0)


def checked_length() -> int | None:
    """Return the checked length in mm, or None if none checked.

    Logs a warning if multiple lengths are checked; the smallest wins.
    """
    checked = [mm for mm in range(6) if re.search(r'- \[[xX]\] ' + str(mm) + r'mm', body)]
    if len(checked) > 1:
        print(f"WARNING: multiple lengths checked {checked}, using {checked[0]}", file=sys.stderr)
    return checked[0] if checked else None


length = checked_length()
result = {
    "date": title,
    "length_mm": length,
}

with open(f'results/{title}.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"Saved results/{title}.json")
print(f"  length_mm: {length}")
