"""Fail-closed repository preservation checks for agent-proposed RTL edits.

This module never edits the target repository. It verifies a Git worktree, scope,
publicly protected paths, and patch metadata before downstream EDA work.
"""
import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


class GuardError(RuntimeError):
    pass


def _git(root, *args):
    proc = subprocess.run(["git", "-C", str(root), *args],
                          text=True, capture_output=True, check=False)
    if proc.returncode:
        raise GuardError("git failed: " + " ".join(args) + ": " + proc.stderr.strip())
    return proc.stdout


def _patterns_match(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) or
               (pattern.endswith("/**") and path.startswith(pattern[:-3] + "/"))
               for pattern in patterns)


def evaluate(root, policy, base_ref, mode="read_only"):
    root = Path(root).resolve()
    if mode not in {"read_only", "patch", "cross_layer"}:
        raise GuardError("unknown execution mode")
    git_root = Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve()
    if root != git_root:
        raise GuardError("root must be the Git worktree root")
    worktrees = _git(root, "worktree", "list", "--porcelain")
    blocks = worktrees.strip().split("\n\n")
    roots = [Path(line[9:]).resolve() for block in blocks
             for line in block.splitlines() if line.startswith("worktree ")]
    if policy.get("require_separate_worktree", True) and (len(roots) < 2 or root == roots[0]):
        raise GuardError("candidate must be a separate Git worktree, not primary worktree")
    branch = _git(root, "symbolic-ref", "--quiet", "--short", "HEAD").strip()
    if branch in policy.get("protected_branches", ["main", "master"]):
        raise GuardError("refusing to evaluate mutations on a protected branch")
    if not base_ref or base_ref.startswith("-"):
        raise GuardError("explicit safe base_ref required")
    _git(root, "rev-parse", "--verify", base_ref + "^{commit}")
    # Includes committed changes relative to base, staged, unstaged and untracked files.
    committed = _git(root, "diff", "--name-status", "--find-renames",
                     base_ref + "...HEAD")
    staged = _git(root, "diff", "--cached", "--name-status", "--find-renames")
    unstaged = _git(root, "diff", "--name-status", "--find-renames")
    untracked = _git(root, "ls-files", "--others", "--exclude-standard")
    changes = []
    for data in (committed, staged, unstaged):
        for line in data.splitlines():
            cols = line.split("\t")
            if len(cols) < 2:
                raise GuardError("unparseable git status line")
            status, paths = cols[0], cols[1:]
            if status[0] not in "AMDRCTUXB":
                raise GuardError("unknown Git diff status: " + status)
            for path in paths:
                changes.append({"status": status, "path": path})
    changes += [{"status": "??", "path": p} for p in untracked.splitlines()]
    allowed = policy.get("allowed_paths", [])
    protected = policy.get("protected_paths", [])
    violations = []
    if mode == "cross_layer" and not policy.get("cross_layer_authorized", False):
        violations.append("cross_layer mode requires explicit authorization")
    if mode == "read_only" and changes:
        violations.append("read_only mode requires no changed files")
    for c in changes:
        path, status = c["path"], c["status"]
        if status.startswith(("D", "R")) and not policy.get("allow_deletions", False):
            violations.append("deletion/rename prohibited: " + path)
        if _patterns_match(path, protected):
            violations.append("protected path changed: " + path)
        if not _patterns_match(path, allowed):
            violations.append("out of allowed scope: " + path)
    return {"status": "PASS" if not violations else "FAIL",
            "base_ref": base_ref, "branch": branch, "mode": mode,
            "changes": changes, "violations": sorted(set(violations))}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--base", required=True, help="frozen baseline commit/ref")
    p.add_argument("--mode", choices=["read_only", "patch", "cross_layer"],
                   default="read_only")
    args = p.parse_args()
    try:
        policy = json.loads(Path(args.policy).read_text(encoding="utf-8"))
        report = evaluate(args.root, policy, args.base, args.mode)
    except (GuardError, OSError, ValueError) as exc:
        report = {"status": "BLOCKED", "error": str(exc)}
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
