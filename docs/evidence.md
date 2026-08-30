# Evidence and compute receipts

[简体中文](evidence.zh-CN.md)

## Evidence classes

- **General argument:** establishes the claimed scope symbolically or deductively.
- **Complete finite certificate:** combines a proof of finite coverage with exact enumeration.
- **Falsification probe:** may find a counterexample but cannot certify an unbounded claim.
- **Regression check:** protects an implementation; it is not independent mathematical evidence.
- **Formal artifact:** certifies only the encoded statement under the reported axioms and toolchain.

## Minimum receipt

Use `templates/attempt/receipt.json`. Record:

- full source commit and dirty-worktree status;
- exact command and working-directory description;
- operating system and tool versions without private host identity;
- UTC start and finish, exit code, and peak resources when material;
- input and output SHA-256 hashes;
- theoretical search total, executed total, and pruning justification;
- deterministic seed or explicit nondeterminism;
- formal toolchain, build command, coverage, and axiom report when applicable.

## Remote execution

Commit code and parameters first. The remote worker pulls the exact SHA into an isolated directory, runs the committed command, and returns only sanitized evidence. Do not commit host, port, username, keys, proxy configuration, cloud credentials, or `known_hosts`.

## Artifact preservation

Preserve decisive source and compact outputs in Git. Store large outputs externally only when the location is durable, access rules are clear, and the repository records content hashes and regeneration instructions. Never hash a modified “clean copy” while discarding the original.
