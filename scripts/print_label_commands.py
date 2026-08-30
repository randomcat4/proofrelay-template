"""Print GitHub CLI commands for the labels in config/labels.json."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def main() -> None:
    data = json.loads((ROOT / "config" / "labels.json").read_text(encoding="utf-8"))
    for label in data["labels"]:
        print(
            "gh label create "
            f"{quote(label['name'])} --color {quote(label['color'])} "
            f"--description {quote(label['description'])} --force"
        )


if __name__ == "__main__":
    main()
