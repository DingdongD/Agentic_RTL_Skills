"""SSH runner with fixed-host verification, quoting, and bounded execution.

Never stores passwords. Does not disable StrictHostKeyChecking.
"""
import shlex
import subprocess
from pathlib import Path


def _target(server):
    user = server["user"]
    host = server.get("ssh_config_host") or server["host"]
    if not user or not host or any(x in user + host for x in "\n\r \t;|&$"):
        raise ValueError("invalid SSH identity/host")
    return f"{user}@{host}"


def base_args(server):
    args = ["ssh", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=yes",
            "-o", "ConnectTimeout=15", "-p", str(server.get("port", 22))]
    if server.get("identity_file"):
        args += ["-i", str(Path(server["identity_file"]).expanduser())]
    return args + [_target(server)]


def ssh(server, command, timeout=120):
    return subprocess.run(base_args(server) + [command], capture_output=True,
                          text=True, timeout=timeout, check=False)


def scp_to(server, local, remote, timeout=120):
    # Preserve a pre-created remote job directory; only transfer named files.
    path = Path(local)
    if not path.is_file():
        raise FileNotFoundError(path)
    opts = ["scp", "-B", "-o", "StrictHostKeyChecking=yes", "-P",
            str(server.get("port", 22))]
    if server.get("identity_file"):
        opts += ["-i", str(Path(server["identity_file"]).expanduser())]
    destination = f"{_target(server)}:{remote}"
    return subprocess.run(opts + ["--", str(path), destination],
                          capture_output=True, text=True, timeout=timeout, check=False)


def remote_shell_script(commands):
    """Construct a single quoted bash -lc payload, never untrusted shell fragments."""
    return "bash -lc " + shlex.quote("set -euo pipefail\n" + "\n".join(commands))
