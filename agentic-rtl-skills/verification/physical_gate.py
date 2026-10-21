"""Fail-closed physical-evidence comparison; no synthetic timing estimates."""
import argparse
import json
import math
from pathlib import Path

FIELDS = ("source_sha", "netlist_sha", "sdc_sha", "library_sha",
          "corner", "tool", "stage", "area_um2", "wns_ns", "power_mw")


def assess(base, candidate):
    for tag, ev in (("baseline", base), ("candidate", candidate)):
        absent = [k for k in FIELDS if ev.get(k) in (None, "")]
        if absent:
            return {"status": "INCONCLUSIVE", "reason": tag + " missing " + ",".join(absent)}
        if ev.get("status") != "PASS":
            return {"status": "BLOCKED", "reason": tag + " physical run not PASS"}
        for k in ("area_um2", "wns_ns", "power_mw"):
            v = ev[k]
            if type(v) not in (int, float) or not math.isfinite(v):
                return {"status": "INCONCLUSIVE", "reason": tag + " invalid " + k}
    for key in ("sdc_sha", "library_sha", "corner", "tool", "stage"):
        if base[key] != candidate[key]:
            return {"status": "INCONCLUSIVE", "reason": "incomparable " + key}
    if candidate["wns_ns"] < 0:
        return {"status": "FAIL", "reason": "candidate negative setup slack"}
    return {"status": "PASS",
            "area_change_pct": 100 * (candidate["area_um2"] / base["area_um2"] - 1)
            if base["area_um2"] > 0 else None,
            "power_change_pct": 100 * (candidate["power_mw"] / base["power_mw"] - 1)
            if base["power_mw"] > 0 else None,
            "wns_change_ns": candidate["wns_ns"] - base["wns_ns"],
            "scope": "comparable reported measurements only, not signoff"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    a = p.parse_args()
    out = assess(json.loads(Path(a.baseline).read_text()),
                 json.loads(Path(a.candidate).read_text()))
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
