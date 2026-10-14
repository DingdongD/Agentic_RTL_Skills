"""Standard-library smoke tests: no EDA license or remote host required."""
import json
import tempfile
import unittest
from pathlib import Path

from adapters.memory_adapter import validate_manifest
from adapters.report_parser import parse_dc, parse_pt, parse_power
from adapters.ssh_runner import remote_shell_script


class AdapterTests(unittest.TestCase):
    def test_dc(self):
        self.assertEqual(parse_dc("Total cell area: 1234.50")["area_um2"], 1234.5)
        self.assertIsNone(parse_dc("no valid area")["area_um2"])

    def test_pt(self):
        self.assertEqual(parse_pt("wns (ns) -0.123\ntns (ns) -2.500")["wns_ns"], -0.123)

    def test_power(self):
        self.assertEqual(parse_power("POWER_TOTAL_MW=1.2")["total_mw"], 1.2)
        self.assertIsNone(parse_power("Total Power = 1.2")["total_mw"])

    def test_memory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "macros.json"
            path.write_text(json.dumps({"macros": [{"instance": "s", "module": "S",
                "depth": 32, "width": 8, "liberty": "a", "lef": "b", "verilog_model": "c"}]}))
            self.assertEqual(validate_manifest(path)[0]["width"], 8)

    def test_shell_quoting(self):
        command = remote_shell_script(["printf '%s' 'pass'"])
        self.assertIn("bash -lc", command)


if __name__ == "__main__":
    unittest.main()
