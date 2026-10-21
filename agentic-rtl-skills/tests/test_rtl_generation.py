import tempfile
import unittest
from pathlib import Path
from generation.rtl_scaffold import counter, generate
from verification.ppa_gate import check


class CodegenTests(unittest.TestCase):
    def test_counter_template(self):
        result = counter({"kind": "counter", "reset": "synchronous_active_low",
                          "module": "test_counter", "width": 8})
        self.assertIn("module test_counter", result)
        self.assertIn("always @(posedge clk)", result)

    def test_fail_closed_template(self):
        with self.assertRaises(ValueError):
            counter({"kind": "arbitrary_soc", "module": "m", "width": 8})
        with self.assertRaises(ValueError):
            counter({"kind": "counter", "reset": "synchronous_active_low",
                     "module": "not-valid", "width": 8})

    def test_ppa_missing_evidence(self):
        self.assertEqual(check({"status": "PASS"})["status"], "INCONCLUSIVE")

    def test_ppa_negative_slack(self):
        data = {"revision": "abcdef1", "tool": "dc", "corner": "tt",
                "sdc_sha256": "a", "library_sha256": "b", "status": "PASS",
                "area_um2": 100.0, "wns_ns": -0.1, "power_mw": 2.5}
        self.assertEqual(check(data)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
