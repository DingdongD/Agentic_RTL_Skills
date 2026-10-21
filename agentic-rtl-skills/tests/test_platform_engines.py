import json
import tempfile
import unittest
from pathlib import Path
from engine.flow_engine import execute, validate, FlowError
from verification.cycle_scoreboard import compare, read_trace
from backends.synopsys_job import safe_name, remote_path, launch, JobError


class EngineTests(unittest.TestCase):
    def test_cycles_and_dependency(self):
        with self.assertRaises(FlowError):
            validate([{"id": "a", "deps": ["b"]}, {"id": "b", "deps": ["a"]}])

    def test_cache_invalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "input.txt").write_text("A")
            state = Path(tmp) / "state.json"
            command = ["python3", "-c", "from pathlib import Path; Path('out.txt').write_text('ok')"]
            plan = {"nodes": [{"id": "build", "command": command,
                               "inputs": ["input.txt"], "outputs": ["out.txt"]}]}
            self.assertEqual(execute(plan, root, state)["build"]["status"], "PASS")
            self.assertTrue(execute(plan, root, state)["build"]["cached"])
            (root / "input.txt").write_text("B")
            self.assertFalse(execute(plan, root, state)["build"]["cached"])

    def test_cycle_scoreboard(self):
        e = {"domain": "clk", "cycle": 3, "kind": "out", "txn_id": 1, "payload": {"v": 7}}
        self.assertEqual(compare([e], [e])["status"], "PASS")
        self.assertEqual(compare([e], [dict(e, cycle=4)])["status"], "FAIL")
        self.assertEqual(compare([e], [dict(e, cycle=4)], "transaction_equivalent")["status"], "PASS")

    def test_domain_order(self):
        a = [{"domain": d, "cycle": i, "kind": "data", "txn_id": i, "payload": 1}
             for d, i in (("a", 1), ("b", 5), ("a", 2))]
        self.assertEqual(compare(a, [a[1], a[0], a[2]], "partial_order")["status"], "PASS")

    def test_malformed_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            p.write_text('{"domain":"x"}\n')
            with self.assertRaises(ValueError):
                read_trace(p)

    def test_remote_fail_closed(self):
        with self.assertRaises(JobError):
            safe_name("../bad")
        with self.assertRaises(JobError):
            remote_path("../bad")
        with self.assertRaises(JobError):
            launch({}, {}, "/tmp", False)


if __name__ == "__main__":
    unittest.main()
