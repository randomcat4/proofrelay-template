# Candidate attempts

Each attempt owns `attempts/<work-unit>/<handle>-<sequence>/`. It contains `answer.md`, `receipt.json`, `src/`, and `out/`. Attempts are immutable historical units: revise with a new commit or sequence, never erase a failed result.

Use `python scripts/new_work_unit.py attempt <work-unit> <handle>` to create one.
