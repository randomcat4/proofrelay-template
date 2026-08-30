"""Validate ProofRelay structure and evidence gates using the Python standard library."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    "README.md",
    "README.zh-CN.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.zh-CN.md",
    "SECURITY.md",
    "SECURITY.zh-CN.md",
    "LICENSE",
    "contracts/frozen-target.md",
    "contracts/frozen-target.zh-CN.md",
    "state/PROJECT_STATE.json",
    "state/STATUS.md",
    "state/STATUS.zh-CN.md",
    "docs/discipline.md",
    "docs/discipline.zh-CN.md",
    "docs/workflow.md",
    "docs/workflow.zh-CN.md",
    "docs/status-model.md",
    "docs/status-model.zh-CN.md",
    "docs/verification.md",
    "docs/verification.zh-CN.md",
    "docs/evidence.md",
    "docs/evidence.zh-CN.md",
    "docs/governance.md",
    "docs/governance.zh-CN.md",
    "manifests/artifacts.json",
    "config/policy.json",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate.yml",
)

TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".yml", ".yaml", ".toml"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "dist", "build"}

SECRET_PATTERNS = (
    ("private key block", re.compile(r"BEGIN\s+[A-Z ]*PRIVATE\s+KEY")),
    ("GitHub classic token", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("OpenAI-style secret", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("root SSH target", re.compile(r"ssh\s+root@", re.IGNORECASE)),
    (
        "public IPv4 infrastructure endpoint",
        re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
    ),
)

MARKERS = {
    "project_id": ("project", "id"),
    "project_status": ("project", "status"),
    "target_version": ("frozen_target", "version"),
    "target_status": ("frozen_target", "status"),
    "truth_status": ("top_level_claim", "truth_status"),
    "novelty_status": ("top_level_claim", "novelty_status"),
}


class ValidationError(Exception):
    """Raised when a repository invariant fails."""


def fail(message: str) -> None:
    raise ValidationError(message)


def load_json(relative: str) -> dict:
    try:
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid JSON from {relative}: {exc}")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def nested(state: dict, path: tuple[str, ...]) -> object:
    value: object = state
    for key in path:
        if not isinstance(value, dict) or key not in value:
            fail(f"state is missing {'.'.join(path)}")
        value = value[key]
    return value


def parse_markers(path: Path) -> dict[str, str]:
    pattern = re.compile(r"<!--\s*([a-z_]+):\s*(.*?)\s*-->")
    return dict(pattern.findall(path.read_text(encoding="utf-8")))


def validate_required() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def validate_state() -> None:
    state = load_json("state/PROJECT_STATE.json")
    if state.get("schema_version") != 1:
        fail("state.schema_version must be 1")
    if not isinstance(state.get("routes"), list):
        fail("state.routes must be a list")
    if not isinstance(state.get("accepted_results"), list):
        fail("state.accepted_results must be a list")

    policy = state.get("verification_policy", {})
    if policy.get("author_may_verify_own_candidate") is not False:
        fail("authors may not verify their own candidates")
    for field in ("route_level_required", "project_level_required"):
        value = policy.get(field)
        if not isinstance(value, int) or value < 1:
            fail(f"verification_policy.{field} must be a positive integer")
    if policy["project_level_required"] < policy["route_level_required"]:
        fail("project-level verification cannot be weaker than route-level verification")

    accepted_ids: set[str] = set()
    for result in state["accepted_results"]:
        if not isinstance(result, dict) or not result.get("id"):
            fail("every accepted result needs an id")
        if result["id"] in accepted_ids:
            fail(f"duplicate accepted result id: {result['id']}")
        accepted_ids.add(result["id"])
        evidence = result.get("evidence")
        if not isinstance(evidence, dict):
            fail(f"accepted result {result['id']} needs an evidence object")
        required_evidence = {"candidate_commit", "candidate_pr", "main_audit", "verification_prs"}
        missing = sorted(required_evidence - evidence.keys())
        if missing:
            fail(f"accepted result {result['id']} lacks evidence: {', '.join(missing)}")
        if len(evidence.get("verification_prs", [])) < policy["route_level_required"]:
            fail(f"accepted result {result['id']} lacks enough verification PRs")

    for status_file in ("state/STATUS.md", "state/STATUS.zh-CN.md"):
        markers = parse_markers(ROOT / status_file)
        for marker, state_path in MARKERS.items():
            expected = str(nested(state, state_path))
            if markers.get(marker) != expected:
                fail(f"{status_file} marker {marker!r} must equal {expected!r}")

    if nested(state, ("project", "status")) != "SETUP":
        authoritative = (
            ROOT / "state/PROJECT_STATE.json",
            ROOT / "state/STATUS.md",
            ROOT / "contracts/frozen-target.md",
            ROOT / ".github/ISSUE_TEMPLATE/config.yml",
        )
        for path in authoritative:
            if "REPLACE_ME" in path.read_text(encoding="utf-8"):
                fail(f"project left SETUP while placeholders remain in {path.relative_to(ROOT)}")


def validate_local_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            target = target.replace("%20", " ")
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"Markdown link escapes repository in {path.relative_to(ROOT)}: {raw_target}")
            if not resolved.exists():
                fail(f"broken local link in {path.relative_to(ROOT)}: {raw_target}")


def validate_manifest() -> None:
    manifest = load_json("manifests/artifacts.json")
    if manifest.get("hash_algorithm") != "sha256":
        fail("manifest hash_algorithm must be sha256")
    seen: set[str] = set()
    for item in manifest.get("artifacts", []):
        relative = item.get("path")
        if not isinstance(relative, str) or not relative:
            fail("every manifest item needs a path")
        path = (ROOT / relative).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"manifest path escapes repository: {relative}")
        if relative in seen:
            fail(f"duplicate manifest path: {relative}")
        seen.add(relative)
        if not path.is_file():
            fail(f"manifest artifact is missing: {relative}")
        if item.get("bytes") != path.stat().st_size:
            fail(f"manifest byte count mismatch: {relative}")
        if str(item.get("sha256", "")).lower() != digest(path):
            fail(f"manifest hash mismatch: {relative}")


def validate_secret_boundary() -> None:
    policy = load_json("config/policy.json")
    forbidden_suffixes = {value.lower() for value in policy.get("forbidden_suffixes", [])}
    forbidden_names = set(policy.get("forbidden_filenames", []))

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            fail(f"symlink not allowed in audited content: {relative}")
        if path.suffix.lower() in forbidden_suffixes or path.name in forbidden_names:
            fail(f"forbidden secret-bearing filename: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"{label} found in {relative}")


def validate_attempts() -> None:
    policy = load_json("config/policy.json")
    allowed = set(policy["allowed_result_statuses"])
    attempts = ROOT / "attempts"
    for receipt in attempts.rglob("receipt.json"):
        directory = receipt.parent
        answer = directory / "answer.md"
        if not answer.is_file():
            fail(f"attempt receipt lacks answer.md: {directory.relative_to(ROOT)}")
        first = answer.read_text(encoding="utf-8").splitlines()[0].strip()
        if not first.startswith("STATUS: ") or first[8:] not in allowed:
            fail(f"invalid attempt status in {answer.relative_to(ROOT)}")
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if data.get("role") != "AUTHOR":
            fail(f"attempt receipt role must be AUTHOR: {receipt.relative_to(ROOT)}")


def validate_verifications() -> None:
    allowed = set(load_json("config/policy.json")["allowed_verdicts"])
    reports = ROOT / "verifications" / "reports"
    if not reports.exists():
        return
    for receipt in reports.rglob("receipt.json"):
        directory = receipt.parent
        report = directory / "report.md"
        if not report.is_file():
            fail(f"verification receipt lacks report.md: {directory.relative_to(ROOT)}")
        first = report.read_text(encoding="utf-8").splitlines()[0].strip()
        if not first.startswith("VERDICT: ") or first[9:] not in allowed:
            fail(f"invalid verification verdict in {report.relative_to(ROOT)}")
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if data.get("role") != "VERIFIER" or data.get("verdict") not in allowed:
            fail(f"invalid verification receipt: {receipt.relative_to(ROOT)}")


def main() -> int:
    checks = (
        validate_required,
        validate_state,
        validate_manifest,
        validate_secret_boundary,
        validate_local_markdown_links,
        validate_attempts,
        validate_verifications,
    )
    try:
        for check in checks:
            check()
    except (ValidationError, OSError, json.JSONDecodeError, IndexError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: structure, dual ledgers, evidence gates, manifest, and secret boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
