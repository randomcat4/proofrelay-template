#!/usr/bin/env python3
"""Check that a math-theorem run has an auditable artifact structure.

This validates files, ledgers, and verdict markers only. It does not validate
mathematics, literature status, semantic fidelity, or novelty.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read_lower(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").lower()


def require_files(root: Path, names: tuple[str, ...], errors: list[str]) -> None:
    for name in names:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")


def validate_discovery(
    root: Path, errors: list[str], warnings: list[str]
) -> dict[str, object]:
    require_files(
        root,
        (
            "search_scope.md",
            "candidate_ledger.md",
            "prior_art.md",
            "shortlist.md",
            "search_metrics.md",
            "provenance.md",
            "rounds.md",
        ),
        errors,
    )

    candidate_count = 0
    pipeline_statuses = {
        "verified_open": 0,
        "status_uncertain": 0,
        "solved_or_occupied": 0,
        "malformed": 0,
        "rejected": 0,
        "hold": 0,
        "scout": 0,
        "deep": 0,
    }
    ledger = root / "candidate_ledger.md"
    if ledger.is_file():
        text = ledger.read_text(encoding="utf-8", errors="replace")
        candidate_count = len(re.findall(r"^##\s+CAND-", text, flags=re.MULTILINE))
        if candidate_count == 0:
            warnings.append("candidate_ledger.md has no '## CAND-' entries")
        upper = text.upper()
        for key in pipeline_statuses:
            pipeline_statuses[key] = upper.count(key.upper())
        for marker in (
            "意图契约",
            "事前价值",
            "语义忠实性",
            "收集候选总数",
            "工作单元",
        ):
            if marker not in text:
                warnings.append(f"candidate ledger lacks marker: {marker}")

    shortlist = root / "shortlist.md"
    if shortlist.is_file():
        text = shortlist.read_text(encoding="utf-8", errors="replace")
        for marker in ("搜索分母", "意图契约", "最终验证器", "主要风险"):
            if marker not in text:
                warnings.append(f"shortlist lacks marker: {marker}")

    metrics = root / "search_metrics.md"
    if metrics.is_file():
        text = metrics.read_text(encoding="utf-8", errors="replace")
        for marker in (
            "候选总数",
            "人工审计时间",
            "工作单元",
            "诚实弃权",
            "误放行",
            "pass@budget",
        ):
            if marker not in text:
                warnings.append(f"search metrics lacks marker: {marker}")

    return {
        "candidate_count": candidate_count,
        "candidate_status_mentions": pipeline_statuses,
    }


def validate_theorem_run(
    root: Path,
    mode: str,
    min_proofs: int,
    min_verifiers: int,
    errors: list[str],
    warnings: list[str],
) -> dict[str, object]:
    require_files(root, ("problem.md", "assumptions.md", "rounds.md", "verdict.md"), errors)
    if mode == "research":
        require_files(
            root,
            (
                "prior_art.md",
                "local_toolbox.md",
                "route_registry.md",
                "hazards.md",
                "lemma_ledger.md",
                "provenance.md",
            ),
            errors,
        )

    frozen = sorted(root.glob("frozen_theorem_v*.md"))
    if not frozen:
        errors.append("missing frozen_theorem_v*.md")
    else:
        for path in frozen:
            text = read_lower(path)
            if "不得修改" not in text and "must not" not in text:
                warnings.append(f"no explicit premise-freeze marker: {path.name}")

    proof_dir = root / "proofs"
    proofs = sorted(proof_dir.glob("*.md")) if proof_dir.is_dir() else []
    if len(proofs) < min_proofs:
        errors.append(f"found {len(proofs)} proofs; need {min_proofs}")

    verify_dir = root / "verifications"
    verifiers = sorted(verify_dir.glob("*.md")) if verify_dir.is_dir() else []
    if len(verifiers) < min_verifiers:
        errors.append(f"found {len(verifiers)} verification reports; need {min_verifiers}")

    statuses = {"correct": 0, "critical_gaps": 0, "other": 0}
    for path in verifiers:
        text = path.read_text(encoding="utf-8", errors="replace").upper()
        if "CRITICAL_GAPS" in text or "CRITICAL GAPS" in text:
            statuses["critical_gaps"] += 1
        elif "STATUS: CORRECT" in text or "STATUS:CORRECT" in text:
            statuses["correct"] += 1
        else:
            statuses["other"] += 1
            warnings.append(f"unrecognized verifier status: {path.name}")

    if mode == "research":
        route_registry = root / "route_registry.md"
        if route_registry.is_file():
            text = route_registry.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"^##\s+ROUTE-", text, flags=re.MULTILINE):
                warnings.append("route_registry.md has no '## ROUTE-' entries")
            for marker in ("目标范畴", "共同瓶颈", "最快证伪测试", "工作单元"):
                if marker not in text:
                    warnings.append(f"route registry lacks marker: {marker}")

        local_toolbox = root / "local_toolbox.md"
        if local_toolbox.is_file():
            text = local_toolbox.read_text(encoding="utf-8", errors="replace")
            for marker in ("已用尽的本地工具", "给 0D 的紧凑排除表"):
                if marker not in text:
                    warnings.append(f"local_toolbox.md lacks marker: {marker}")

        lemma_ledger = root / "lemma_ledger.md"
        if lemma_ledger.is_file():
            text = lemma_ledger.read_text(encoding="utf-8", errors="replace")
            for marker in ("EQUIVALENT_BLOCKER", "相对原命题", "外部定理条件核验"):
                if marker not in text:
                    warnings.append(f"lemma ledger lacks marker: {marker}")

    return {
        "frozen_versions": [p.name for p in frozen],
        "proof_count": len(proofs),
        "verification_count": len(verifiers),
        "verification_statuses": statuses,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--mode", choices=("standard", "research", "discovery"), default="standard"
    )
    parser.add_argument("--min-proofs", type=int)
    parser.add_argument("--min-verifiers", type=int)
    args = parser.parse_args()

    root = args.run_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if args.mode == "discovery":
        details = validate_discovery(root, errors, warnings)
    else:
        min_proofs = 1 if args.min_proofs is None else args.min_proofs
        min_verifiers = 1 if args.min_verifiers is None else args.min_verifiers
        details = validate_theorem_run(
            root,
            args.mode,
            min_proofs,
            min_verifiers,
            errors,
            warnings,
        )

    report = {
        "run_dir": str(root),
        "mode": args.mode,
        "ok": not errors,
        **details,
        "errors": errors,
        "warnings": warnings,
        "note": (
            "Structure only; mathematical correctness, semantic fidelity, "
            "literature status, and novelty are not checked."
        ),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
