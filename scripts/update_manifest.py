"""Add or refresh explicitly named files in manifests/artifacts.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "artifacts.json"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="repository-relative files to preserve")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = {item["path"]: item for item in manifest.get("artifacts", [])}
    for raw in args.paths:
        path = (ROOT / raw).resolve()
        relative = path.relative_to(ROOT.resolve()).as_posix()
        if not path.is_file():
            raise SystemExit(f"not a file: {raw}")
        entries[relative] = {
            "path": relative,
            "sha256": digest(path),
            "bytes": path.stat().st_size,
        }

    manifest["generated_at"] = date.today().isoformat()
    manifest["artifacts"] = [entries[key] for key in sorted(entries)]
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {MANIFEST.relative_to(ROOT)} with {len(args.paths)} requested artifact(s)")


if __name__ == "__main__":
    main()
