#!/usr/bin/env python3
"""Conservative, stdlib-only RTL naming and file-manifest policy checker.

A lexical checker is not a parser; compile and run a real lint tool separately.
"""
import argparse
import json
import re
import sys
from pathlib import Path

MODULE = re.compile(r"(?m)^\s*module\s+(?:automatic\s+)?([A-Za-z_]\w*)\b")
INSTANCE = re.compile(r"(?m)^\s*([A-Za-z_]\w*)\s*(?:#\s*\([^;]*?\)\s*)?([A-Za-z_]\w*)\s*\(", re.S)
LOW = re.compile(r"^[a-z][a-z0-9_]*$")
UP = re.compile(r"^[A-Z][A-Z0-9_]*$")


def scan(root, paths, strict=False):
    errors, warnings, modules = [], [], {}
    for rel in paths:
        path = root / rel
        if not path.is_file() or path.suffix not in (".sv", ".v"):
            errors.append(f"{rel}: missing RTL source or invalid extension")
            continue
        text = path.read_text(errors="replace")
        # Remove comments to avoid interpreting old module names as declarations.
        clean = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
        found = MODULE.findall(clean)
        if not found:
            errors.append(f"{rel}: no module declaration")
        for module in found:
            if not LOW.fullmatch(module):
                errors.append(f"{rel}: module {module} should use lowercase snake_case")
            if module in modules:
                errors.append(f"{rel}: duplicate module {module} (also in {modules[module]})")
            modules[module] = str(rel)
        if len(found) == 1 and path.stem != found[0]:
            warnings.append(f"{rel}: filename differs from module {found[0]}")
        if "/hdl/" not in "/" + rel.as_posix() and not rel.as_posix().startswith("hdl/"):
            warnings.append(f"{rel}: source is outside an hdl/ directory")
        for param in re.findall(r"\b(?:localparam|parameter)\s+(?:(?:signed|integer|int|logic|reg|bit)\s+)?(?:\[[^]]+\]\s*)?([A-Za-z_]\w*)\b", clean):
            if not UP.fullmatch(param):
                warnings.append(f"{rel}: parameter {param} should be UPPER_SNAKE_CASE")
        if re.search(r"\bcasex\s*\(", clean):
            errors.append(f"{rel}: casex forbidden")
        if re.search(r"\balways\s*@\s*\(\s*\*\s*\)", clean):
            warnings.append(f"{rel}: legacy always @(*) is allowed but always_comb may help new SV")
    if strict:
        errors.extend(warnings)
        warnings = []
    return {"status": "fail" if errors else "pass", "errors": errors, "warnings": warnings,
            "sources_checked": len(paths), "modules": modules}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--filelist", type=Path, required=True)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve()
    manifest = (root / args.filelist).resolve()
    if not manifest.is_relative_to(root):
        ap.error("filelist must be inside root")
    if not manifest.is_file():
        ap.error("filelist does not exist")
    paths, unsupported = [], []
    for line in manifest.read_text().splitlines():
        entry = line.split("//", 1)[0].split("#", 1)[0].strip()
        if not entry:
            continue
        if entry.startswith(("+incdir+", "+define+", "-I", "-D")) or entry.endswith((".svh", ".vh")):
            continue
        if entry.startswith("-f ") or entry.startswith("-F "):
            unsupported.append("nested filelists: " + entry)
            continue
        if entry.startswith("-"):
            unsupported.append("unsupported filelist directive: " + entry)
            continue
        candidate = (manifest.parent / entry).resolve()
        if not candidate.is_file():
            candidate = (root / entry).resolve()
        if not candidate.is_relative_to(root):
            unsupported.append("outside root: " + entry)
            continue
        paths.append(candidate.relative_to(root))
    result = scan(root, paths, args.strict)
    result["errors"].extend(unsupported)
    if unsupported:
        result["status"] = "fail"
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
