"""Parse buzz cut checklist from PR body and save result as JSON."""

import json
import os
import re
import sys

raw_title = os.environ.get('PR_TITLE', '').strip()
body = os.environ.get('PR_BODY', '')

# PR title format from pr-checklist-collector: "Add checklist (YYYY-MM-DD)"
m = re.search(r'\((\d{4}-\d{2}-\d{2})\)', raw_title)
if not m:
    print(f"SKIP: PR_TITLE '{raw_title}' does not contain a YYYY-MM-DD date")
    sys.exit(0)

title = m.group(1)


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
