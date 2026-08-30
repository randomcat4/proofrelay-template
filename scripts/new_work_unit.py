"""Scaffold a candidate attempt or independent verification directory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


def safe(value: str, label: str) -> str:
    if not SAFE.fullmatch(value):
        raise SystemExit(f"{label} must match {SAFE.pattern}")
    return value


def next_sequence(parent: Path, handle: str) -> int:
    values = []
    for path in parent.glob(f"{handle}-*"):
        tail = path.name.rsplit("-", 1)[-1]
        if tail.isdigit():
            values.append(int(tail))
    return max(values, default=0) + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("attempt", "verification"))
    parser.add_argument("work_unit")
    parser.add_argument("handle")
    args = parser.parse_args()

    work_unit = safe(args.work_unit.lower(), "work_unit")
    handle = safe(args.handle.lower(), "handle")

    if args.kind == "attempt":
        parent = ROOT / "attempts" / work_unit
        source = ROOT / "templates" / "attempt"
    else:
        parent = ROOT / "verifications" / "reports" / work_unit
        source = ROOT / "templates" / "verification"

    sequence = next_sequence(parent, handle)
    destination = parent / f"{handle}-{sequence:02d}"
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination.relative_to(ROOT)}")
    destination.mkdir(parents=True)

    replacements = {
        '- Work unit: `REPLACE_ME`': f'- Work unit: `{work_unit}`',
        '- Verifier: `REPLACE_ME`': f'- Verifier: `{handle}`',
        '"work_unit": "REPLACE_ME"': f'"work_unit": "{work_unit}"',
        '"actor": "REPLACE_ME"': f'"actor": "{handle}"',
    }
    for path in source.iterdir():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for old, new in replacements.items():
                text = text.replace(old, new)
            (destination / path.name).write_text(text, encoding="utf-8")
    if args.kind == "attempt":
        (destination / "src").mkdir()
        (destination / "out").mkdir()
        (destination / "src" / ".gitkeep").touch()
        (destination / "out" / ".gitkeep").touch()

    print(destination.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
