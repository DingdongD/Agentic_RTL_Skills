#!/usr/bin/env python3
"""Read-only SSH preflight for a configured licensed EDA host.

No tool invocation or RTL upload. Validates host key with ordinary SSH policy.
"""
import argparse
import json
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from adapters.ssh_runner import remote_shell_script, ssh

SAFE_TOOL = re.compile(r"^[A-Za-z_][A-Za-z0-9_./-]*$")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--server", required=True)
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    server = config["servers"][args.server]
    tools = server.get("tools", {})
    if not tools:
        raise SystemExit("No tools configured")
    if not all(isinstance(x, str) and SAFE_TOOL.fullmatch(x) for x in tools.values()):
        raise SystemExit("Unsafe tool executable entry: use a simple path, not shell commands")
    setup = server.get("setup_script")
    # Source only operator-controlled setup path, never expand a raw command string.
    commands = []
    if setup:
        if not isinstance(setup, str) or not setup.startswith("/") or "\n" in setup:
            raise SystemExit("setup_script must be a single absolute file path")
        commands.append("source " + shlex.quote(setup))
    for role, executable in tools.items():
        commands.append("command -v " + shlex.quote(executable) +
                        " >/dev/null && printf '%s\\n' " + shlex.quote("OK " + role) +
                        " || printf '%s\\n' " + shlex.quote("MISSING " + role))
    try:
        result = ssh(server, remote_shell_script(commands), timeout=60)
    except Exception as exc:
        raise SystemExit(f"SSH preflight could not run: {exc}") from exc
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode:
        raise SystemExit(result.returncode)
    if "MISSING " in result.stdout:
        raise SystemExit(2)
    print("Executables found. Licenses and actual tool operation NOT verified.")


if __name__ == "__main__":
    main()
