"""Pareto filtering over observed PPA metrics; no fabricated predictions."""
import argparse
import json
import math
from pathlib import Path


def frontier(candidates):
    required = ("id", "area_um2", "energy_uj", "latency_cycles", "evidence")
    valid = []
    for c in candidates:
        if any(k not in c for k in required) or c.get("verification") != "PASS":
            continue
        metrics = [c[k] for k in required[1:4]]
        if any(type(v) not in (float, int) or not math.isfinite(v) or v < 0
               for v in metrics) or not c["evidence"]:
            continue
        valid.append(c)
    keys = ("area_um2", "energy_uj", "latency_cycles")
    result = [candidate for candidate in valid
              if not any(other["id"] != candidate["id"]
                         and all(other[k] <= candidate[k] for k in keys)
                         and any(other[k] < candidate[k] for k in keys)
                         for other in valid)]
    return {"eligible": len(valid), "frontier": sorted(result, key=lambda c: c["id"]),
            "rejected": len(candidates) - len(valid)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    result = frontier(json.loads(Path(a.input).read_text())["candidates"])
    Path(a.output).write_text(json.dumps(result, indent=2))
    print(json.dumps({"eligible": result["eligible"], "pareto": len(result["frontier"])}))


if __name__ == "__main__":
    main()
