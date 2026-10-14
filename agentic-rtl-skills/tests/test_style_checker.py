"""Standalone smoke test with dynamic import because Skill folder has hyphens."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rtl_style_check.py"
spec = importlib.util.spec_from_file_location("style_checker", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StyleTests(unittest.TestCase):
    def test_good_and_bad_names(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "rtl/hdl/pe").mkdir(parents=True)
            p = root / "rtl/hdl/pe/compute_pe.sv"
            p.write_text("module compute_pe #(parameter DATA_W = 8) (); endmodule\n")
            good = checker.scan(root, [Path("rtl/hdl/pe/compute_pe.sv")])
            self.assertEqual(good["status"], "pass")
            p.write_text("module MyPE (); endmodule")
            bad = checker.scan(root, [Path("rtl/hdl/pe/compute_pe.sv")])
            self.assertEqual(bad["status"], "fail")


if __name__ == "__main__":
    unittest.main()
