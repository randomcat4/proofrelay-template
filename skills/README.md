# Agent Skills

[简体中文](README.zh-CN.md)

This directory ships installable [Agent Skills](https://github.com/anthropics/skills) that pair with the ProofRelay protocol. Each skill is a self-contained directory with a `SKILL.md` entry point; no runtime dependencies are added to the repository itself.

## Bundled skills

| Skill | Purpose |
|---|---|
| [`math-theorem/`](math-theorem/SKILL.md) | Research-grade theorem discovery, proving, refutation, minimal-assumption repair, and novelty certification. Enforces frozen statements, isolated proof instances, fresh-context verification, prior-art auditing, and separate verdicts for truth, proof completeness, and novelty. |

`math-theorem` is deliberately aligned with ProofRelay: its run artifacts (frozen theorem, route registry, lemma ledger, provenance, verdict) map onto this repository's `contracts/`, `routes/`, `attempts/`, `verifications/`, and `state/` lifecycle. The skill governs the mathematical discipline inside a work unit; ProofRelay governs how that work is claimed, audited, and preserved on GitHub.

## Installation

Copy the skill directory into your agent's skill search path. The directory name must stay `math-theorem` and `SKILL.md` must sit at its root.

### Codex CLI

```bash
# Linux / macOS
mkdir -p ~/.codex/skills
cp -r skills/math-theorem ~/.codex/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Force skills\math-theorem "$HOME\.codex\skills\math-theorem"
```

### QwenWork (千问办公)

```bash
# Linux / macOS
mkdir -p ~/.qwenworkcn/skills
cp -r skills/math-theorem ~/.qwenworkcn/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Force skills\math-theorem "$HOME\.qwenworkcn\skills\math-theorem"
```

### Other agents

Any agent that reads the Agent Skills format works. Point it at a copy of `math-theorem/`:

- Claude Code: `~/.claude/skills/math-theorem/` (user level) or `.claude/skills/math-theorem/` inside the project.
- Project-local: place the directory wherever your agent scans for skills, e.g. `.agents/skills/` in a repository created from this template.

### Verify the installation

Start a new session and issue a trigger request, for example:

> Prove or disprove: for every martingale (M_n) and every almost-surely finite stopping time τ, E[M_τ] = E[M_0].

The agent should load `SKILL.md`, freeze the statement, and produce the run-directory artifacts instead of answering informally. If it answers casually, the skill was not picked up; recheck the directory name and location.

## Requirements

- An agent that can read `SKILL.md` and run shell commands.
- Python 3 (standard library only) for `math-theorem/scripts/validate_run.py`, which checks that a run directory is structurally complete. Structural checks do not certify mathematical correctness.
- Optional: a Lean 4 toolchain (elan). The skill probes the project-pinned `lean-toolchain` and never silently substitutes another version.
- Optional: sub-agent capability. With it, proof and verification run in isolated instances; without it, the skill falls back to independent, non-inheriting rounds.

## Compatibility

`SKILL.md` uses the common Agent Skills convention: YAML front matter with `name` and `description`, followed by the instruction body, with `references/` loaded on demand. Verified with Codex CLI and QwenWork (千问办公). The skill contains no service credentials and no machine-specific secrets; one example Lean probe path in `SKILL.md` is illustrative and can be edited for your environment.

## Updating a skill

Replace the installed copy with the new version directory, then re-run the verification prompt above. Skills are shipped as plain directories without their own version tags; if you need reproducibility, record the template commit you copied from.
