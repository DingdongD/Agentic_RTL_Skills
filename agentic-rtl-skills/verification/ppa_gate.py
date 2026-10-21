"""Minimal fail-closed ASIC PPA evidence gate, not physical signoff."""
import argparse
import json
import math
from pathlib import Path


def check(evidence):
    required = ("revision", "tool", "corner", "sdc_sha256", "library_sha256",
                "status", "area_um2", "wns_ns", "power_mw")
    missing = [k for k in required if k not in evidence or evidence[k] is None]
    if missing:
        return {"status": "INCONCLUSIVE", "missing": missing}
    if evidence["status"] != "PASS":
        return {"status": "FAIL", "reason": "EDA stage not PASS"}
    if any(not isinstance(evidence[k], (int, float)) or not math.isfinite(evidence[k])
           for k in ("area_um2", "wns_ns", "power_mw")):
        return {"status": "INCONCLUSIVE", "reason": "invalid metric"}
    if evidence["area_um2"] <= 0 or evidence["power_mw"] < 0:
        return {"status": "INCONCLUSIVE", "reason": "invalid area or power"}
    if evidence["wns_ns"] < 0:
        return {"status": "FAIL", "reason": "negative setup slack"}
    return {"status": "PASS", "notice": "preliminary metric evidence only; not signoff"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", required=True)
    a = parser.parse_args()
    result = check(json.loads(Path(a.evidence).read_text()))
    print(json.dumps(result))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
