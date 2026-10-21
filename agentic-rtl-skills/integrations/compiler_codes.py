"""Read-only Compiler_Codes portable ACTSim regression runner."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run(root, timeout=240):
    root = Path(root).resolve()
    sub = root / "cyclesim" / "ACTransformerCycleSim"
    if not (sub / "actsim" / "__init__.py").is_file():
        return {"status": "BLOCKED", "reason": "ACTSim package absent"}
    tests = ["tests.unit.test_rtl_modules", "tests.unit.test_bits",
             "tests.unit.test_trace"]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(sub)
    command = [sys.executable, "-m", "unittest", "-v", *tests]
    try:
        result = subprocess.run(command, cwd=sub, env=env, capture_output=True,
                                text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "BLOCKED", "reason": str(exc), "command": command}
    combined = result.stdout + result.stderr
    return {"status": "PASS" if result.returncode == 0 else "FAIL",
            "command": command, "exit_code": result.returncode,
            "log_tail": combined[-8000:],
            "scope": "portable Python RTL-like resource/cycle tests, not RTL equivalence"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    report = run(args.root)
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(json.dumps({"status": report["status"], "scope": report.get("scope")}))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
