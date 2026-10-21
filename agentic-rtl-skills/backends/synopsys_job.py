"""Guarded SSH job lifecycle: preflight, immutable run directory, logs and results.

Does not provide tool licenses/PDK or promise signoff. Never invokes shell
instructions from untrusted model output without an operator-reviewed manifest.
"""
import argparse
import hashlib
import json
import re
import shlex
from pathlib import Path
from adapters.ssh_runner import ssh, scp_to, remote_shell_script


class JobError(RuntimeError):
    pass


def safe_name(name):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", name):
        raise JobError("invalid job id")
    return name


def remote_path(value):
    if not value.startswith("/") or any(c in value for c in "
\r\0"):
        raise JobError("absolute remote workspace required")
    if ".." in Path(value).parts:
        raise JobError("parent traversal in remote path")
    return value.rstrip("/")


def launch(server, manifest, results_dir, approved=False):
    if not approved:
        raise JobError("explicit --approve-live required for licensed remote tools")
    if manifest.get("schema_version") != 1:
        raise JobError("unsupported manifest version")
    job = safe_name(manifest["job_id"])
    stage = manifest["stage"]
    if stage not in ("dc", "pt", "power"):
        raise JobError("unsupported EDA stage")
    root = remote_path(server["remote_workspace"])
    base = root + "/" + job
    local = Path(results_dir).resolve() / job
    if local.exists():
        raise JobError("local job ID already exists; choose a new immutable job ID")
    local.mkdir(parents=True, exist_ok=False)
    artifact_paths = manifest["inputs"]
    if not artifact_paths or not all(Path(x).is_file() for x in artifact_paths):
        raise JobError("all manifest inputs must exist")
    if not manifest.get("tool_setup_reviewed", False):
        raise JobError("operator must approve environment and Tcl/SDC/library inputs")
    config = json.dumps({"stage": stage, "inputs": [
        {"name": Path(p).name, "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
        for p in artifact_paths]}, indent=2)
    (local / "manifest.json").write_text(config)
    names = [Path(p).name for p in artifact_paths]
    if len(set(names)) != len(names):
        raise JobError("input basenames must be unique")
    setup = server.get("setup_script", "")
    tool = server["tools"][stage]
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", tool):
        raise JobError("unsafe tool executable")
    if not setup.startswith("/") or not re.fullmatch(r"[A-Za-z0-9_./-]+", setup):
        raise JobError("reviewed absolute setup_script required")
    run_file = manifest.get("run_tcl", "")
    if Path(run_file).name not in names:
        raise JobError("run Tcl must be included in immutable inputs")
    # Mandatory configuration is represented as reviewed inputs and explicit
    # environment entries; never upload PDK or licenses automatically.
    env = manifest.get("environment", {})
    for key, val in env.items():
        if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", key) or not isinstance(val, str) or "
" in val:
            raise JobError("unsafe environment entry")
    create = ssh(server, remote_shell_script([
        "umask 077", "mkdir -p " + shlex.quote(base),
        "test ! -e " + shlex.quote(base + "/.started")]))
    if create.returncode:
        raise JobError("remote preflight failed: " + create.stderr[-400:])
    for path in artifact_paths:
        sent = scp_to(server, path, base + "/" + Path(path).name)
        if sent.returncode:
            raise JobError("remote upload failed: " + sent.stderr[-400:])
    exports = " ".join(k + "=" + shlex.quote(v) for k, v in env.items())
    run = ("cd " + shlex.quote(base) + " && touch .started && "
           + "source " + shlex.quote(setup) + " && "
           + exports + (" " if exports else "")
           + shlex.quote(tool) + " -f " + shlex.quote(Path(run_file).name)
           + " > job.log 2>&1; code=$?; echo $code > exit_code; exit $code")
    result = ssh(server, remote_shell_script([run]), timeout=int(manifest.get("timeout_seconds", 3600)))
    log = ssh(server, remote_shell_script(["cat " + shlex.quote(base + "/job.log")]))
    code = ssh(server, remote_shell_script(["cat " + shlex.quote(base + "/exit_code")]))
    (local / "job.log").write_text(log.stdout)
    (local / "exit_code.txt").write_text(code.stdout)
    success = result.returncode == 0 and log.returncode == 0 and code.stdout.strip() == "0"
    summary = {"job_id": job, "stage": stage, "status": "PASS" if success else "FAIL",
               "remote_exit": result.returncode, "remote_directory": base,
               "local_logs": str(local)}
    (local / "result.json").write_text(json.dumps(summary, indent=2))
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--server", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--approve-live", action="store_true")
    a = p.parse_args()
    try:
        cfg = json.loads(Path(a.config).read_text())
        report = launch(cfg["servers"][a.server], json.loads(Path(a.manifest).read_text()),
                        a.results, a.approve_live)
    except (KeyError, ValueError, OSError, JobError) as e:
        report = {"status": "BLOCKED", "error": str(e)}
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
