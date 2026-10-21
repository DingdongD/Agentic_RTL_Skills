"""Compare normalized RTL and CModel event traces without hiding missing events."""
import argparse
import json
from collections import Counter
from pathlib import Path


class TraceError(ValueError):
    pass


def read_trace(path):
    events = []
    for index, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TraceError(f"invalid JSON line {index}: {exc}") from exc
        required = ("domain", "cycle", "kind", "txn_id", "payload")
        if not isinstance(event, dict) or any(k not in event for k in required):
            raise TraceError(f"missing required event fields line {index}")
        if not isinstance(event["cycle"], int) or event["cycle"] < 0:
            raise TraceError(f"invalid cycle line {index}")
        if not isinstance(event["domain"], str) or not event["domain"]:
            raise TraceError(f"invalid domain line {index}")
        events.append(event)
    return events


def compare(reference, observed, mode="cycle_exact"):
    if mode not in ("cycle_exact", "transaction_equivalent", "partial_order"):
        raise TraceError("unknown comparison mode")
    def key(event):
        return (event["domain"], event["cycle"] if mode == "cycle_exact" else None,
                event["kind"], str(event["txn_id"]),
                json.dumps(event["payload"], sort_keys=True))
    if mode == "partial_order":
        # Cross-domain order is intentionally not inferred; preserve each domain-local
        # event sequence and exact transaction identity, allow arbitrary interleaving.
        def grouped(events):
            out = {}
            for e in events:
                out.setdefault(e["domain"], []).append(key(e))
            return out
        expected, actual = grouped(reference), grouped(observed)
    elif mode == "transaction_equivalent":
        expected, actual = Counter(map(key, reference)), Counter(map(key, observed))
    else:
        expected, actual = list(map(key, reference)), list(map(key, observed))
    passed = expected == actual
    return {"status": "PASS" if passed else "FAIL", "mode": mode,
            "reference_events": len(reference), "rtl_events": len(observed),
            "first_difference": None if passed else str(next(
                ((i, a, b) for i, (a, b) in enumerate(zip(reference, observed)) if key(a) != key(b)),
                (min(len(reference), len(observed)), None, None)))}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reference", required=True)
    p.add_argument("--rtl", required=True)
    p.add_argument("--mode", default="cycle_exact",
                   choices=("cycle_exact", "transaction_equivalent", "partial_order"))
    p.add_argument("--out", required=True)
    args = p.parse_args()
    try:
        result = compare(read_trace(args.reference), read_trace(args.rtl), args.mode)
    except (OSError, TraceError) as exc:
        result = {"status": "BLOCKED", "error": str(exc)}
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
