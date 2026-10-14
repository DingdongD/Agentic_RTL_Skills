"""Validate SRAM manifests; compiler execution is vendor/PDK-specific."""
import json
from pathlib import Path


def validate_manifest(path):
    data = json.loads(Path(path).read_text())
    result = []
    for macro in data.get("macros", []):
        for field in ("instance", "module", "depth", "width", "liberty", "lef", "verilog_model"):
            if field not in macro:
                raise ValueError(f"macro missing {field}")
        if int(macro["depth"]) <= 0 or int(macro["width"]) <= 0:
            raise ValueError("SRAM depth/width must be positive")
        result.append(macro)
    return result
