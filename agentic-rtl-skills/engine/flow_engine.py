"""Deterministic, resumable DAG runner with content-addressed invalidation."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


class FlowError(Exception):
    pass


def digest(paths, root):
    h = hashlib.sha256()
    for value in sorted(set(paths)):
        p = (root / value).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file():
            raise FlowError("missing/unsafe input: " + value)
        h.update(value.encode())
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def validate(nodes):
    ids = [n["id"] for n in nodes]
    if len(set(ids)) != len(ids):
        raise FlowError("duplicate node ID")
    lookup = {n["id"]: n for n in nodes}
    order, active, finished = [], set(), set()

    def visit(name):
        if name not in lookup:
            raise FlowError("unknown dependency: " + name)
        if name in active:
            raise FlowError("dependency cycle")
        if name in finished:
            return
        active.add(name)
        for dep in lookup[name].get("deps", []):
            visit(dep)
        active.remove(name)
        finished.add(name)
        order.append(name)
    for name in ids:
        visit(name)
    return order, lookup


def execute(plan, root, state_path, dry_run=False):
    root = Path(root).resolve()
    state_path = Path(state_path).resolve()
    if state_path.is_relative_to(root):
        raise FlowError("state must reside outside source tree")
    order, lookup = validate(plan["nodes"])
    old = json.loads(state_path.read_text()) if state_path.exists() else {}
    states = {}
    for name in order:
        node = lookup[name]
        deps = node.get("deps", [])
        if any(states[d]["status"] != "PASS" for d in deps):
            states[name] = {"status": "BLOCKED", "reason": "dependency not PASS"}
            continue
        argv = node["command"]
        if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
            raise FlowError("command must be a nonempty argv list")
        inp_hash = digest(node.get("inputs", []), root)
        dep_hashes = [states[d]["fingerprint"] for d in deps]
        fingerprint = hashlib.sha256(json.dumps([name, argv, inp_hash, dep_hashes],
                              sort_keys=True).encode()).hexdigest()
        outputs = node.get("outputs", [])
        def outputs_exist():
            return all((root / o).is_file() and (root / o).resolve().is_relative_to(root) for o in outputs)
        prev = old.get(name, {})
        if prev.get("status") == "PASS" and prev.get("fingerprint") == fingerprint and outputs_exist():
            states[name] = dict(prev)
            states[name]["cached"] = True
            continue
        if dry_run:
            states[name] = {"status": "NOT_RUN", "fingerprint": fingerprint}
            continue
        # Commands are specified in trusted operator-reviewed plans; no shell expansion.
        try:
            proc = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                                  timeout=int(node.get("timeout_seconds", 600)), check=False)
            ok = proc.returncode == 0 and outputs_exist()
            states[name] = {"status": "PASS" if ok else "FAIL", "fingerprint": fingerprint,
                            "exit_code": proc.returncode, "stdout_tail": proc.stdout[-4096:],
                            "stderr_tail": proc.stderr[-4096:], "cached": False}
        except (OSError, subprocess.TimeoutExpired) as exc:
            states[name] = {"status": "BLOCKED", "fingerprint": fingerprint,
                            "reason": str(exc)}
        state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(states, indent=2, sort_keys=True))
        tmp.replace(state_path)
    if not dry_run:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(states, indent=2, sort_keys=True))
        tmp.replace(state_path)
    return states


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--root", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = execute(json.loads(Path(args.plan).read_text()), args.root, args.state, args.dry_run)
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if all(x["status"] == "PASS" for x in result.values()) else 1)
    except (FlowError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
