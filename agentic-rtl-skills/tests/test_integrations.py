import tempfile
import unittest
from pathlib import Path
from integrations.compiler_codes import run
from verification.physical_gate import assess


class IntegrationTests(unittest.TestCase):
    def test_missing_project_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(d)["status"], "BLOCKED")

    def test_physical_comparability(self):
        a = dict(source_sha="a", netlist_sha="x", sdc_sha="same",
                 library_sha="lib", corner="tt", tool="OpenROAD", stage="placement",
                 area_um2=100, wns_ns=0.2, power_mw=4, status="PASS")
        b = dict(a, source_sha="b", netlist_sha="y", area_um2=90, power_mw=3)
        self.assertEqual(assess(a, b)["status"], "PASS")
        self.assertEqual(assess(a, dict(b, corner="ss"))["status"], "INCONCLUSIVE")
        self.assertEqual(assess(a, dict(b, wns_ns=-0.3))["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
