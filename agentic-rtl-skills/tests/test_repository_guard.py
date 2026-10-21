"""Unit checks for the scope enforcement function."""
import sys
import tempfile
import subprocess
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.repository_guard import evaluate, GuardError


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


class RepositoryGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, "init")
        git(self.root, "config", "user.email", "test@example.org")
        git(self.root, "config", "user.name", "Guard Test")
        (self.root / "rtl").mkdir()
        (self.root / "rtl" / "pe.sv").write_text("module pe; endmodule\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "base")
        self.base = git(self.root, "rev-parse", "HEAD")
        git(self.root, "checkout", "-b", "agent/candidate")
        self.policy = {"allowed_paths": ["rtl/**"], "protected_paths": ["compiler/**"],
                       "allow_deletions": False, "require_separate_worktree": False}

    def test_valid_patch(self):
        (self.root / "rtl" / "pe.sv").write_text("module pe(input clk); endmodule\n")
        self.assertEqual(evaluate(self.root, self.policy, self.base, "patch")["status"], "PASS")

    def test_read_only_fails_on_change(self):
        (self.root / "rtl" / "pe.sv").write_text("changed\n")
        self.assertEqual(evaluate(self.root, self.policy, self.base)["status"], "FAIL")

    def test_untracked_outside_scope(self):
        (self.root / "unexpected.txt").write_text("bad")
        self.assertEqual(evaluate(self.root, self.policy, self.base, "patch")["status"], "FAIL")

    def test_delete_denied(self):
        (self.root / "rtl" / "pe.sv").unlink()
        self.assertEqual(evaluate(self.root, self.policy, self.base, "patch")["status"], "FAIL")

    def test_protected_branch_denied(self):
        git(self.root, "checkout", "-b", "main")
        with self.assertRaises(GuardError):
            evaluate(self.root, self.policy, self.base, "patch")


if __name__ == "__main__":
    unittest.main()
