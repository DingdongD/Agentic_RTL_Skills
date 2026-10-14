"""Machine-readable synthesis/STA/power evidence with explicit unknowns."""
import re


def _number(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return float(match.group(1)) if match else None


def parse_dc(text):
    return {
        "area_um2": _number(text, r"Total cell area:\s*([+-]?[\d.,]+)".replace(",", "")),
        "combinational_area_um2": _number(text, r"Combinational area:\s*([\d.]+)"),
        "sequential_area_um2": _number(text, r"Noncombinational area:\s*([\d.]+)"),
    }


def parse_pt(text):
    return {
        "wns_ns": _number(text, r"^\s*wns\s*\(ns\)\s*[:=]?\s*([-+]?\d+(?:\.\d+)?)"),
        "tns_ns": _number(text, r"^\s*tns\s*\(ns\)\s*[:=]?\s*([-+]?\d+(?:\.\d+)?)"),
        "violating_paths": _number(text, r"^\s*violating_paths\s*[:=]?\s*(\d+)"),
    }


def parse_power(text):
    # Conservative: only accept our adapter's explicit normalized markers.
    return {
        "total_mw": _number(text, r"^POWER_TOTAL_MW=([\d.eE+-]+)"),
        "dynamic_mw": _number(text, r"^POWER_DYNAMIC_MW=([\d.eE+-]+)"),
        "leakage_mw": _number(text, r"^POWER_LEAKAGE_MW=([\d.eE+-]+)"),
    }
