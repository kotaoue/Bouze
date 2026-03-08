# Bouze
Tracking my buzz cut intervals and grooming routine.

![Days since last buzz](results/badge.svg)

## How it works

### 1. Recording a buzz cut
A Pull Request with a checklist (0mm – 5mm) is created automatically each day.  
Check the length you used, then merge the PR.  
The result is saved as a JSON file in `results/`.

### 2. Days-since badge
The badge above is regenerated every day at 03:00 JST and whenever a PR is merged.  
It shows how many days have passed since the last buzz cut.
