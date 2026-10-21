"""Fail-closed simple Verilog-2005 counter generator; not a general RTL synthesis agent."""
import argparse
import json
import re
from pathlib import Path


def ident(s):
    if not isinstance(s, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", s):
        raise ValueError("invalid Verilog identifier")
    return s


def counter(spec):
    if spec.get("kind") != "counter" or spec.get("reset") != "synchronous_active_low":
        raise ValueError("unsupported verified template")
    name = ident(spec["module"])
    width = spec["width"]
    if type(width) is not int or not 1 <= width <= 64:
        raise ValueError("width out of range")
    clk = ident(spec.get("clock", "clk"))
    rst = ident(spec.get("reset_port", "rst_n"))
    en = ident(spec.get("enable", "en"))
    if len(set((clk, rst, en))) != 3:
        raise ValueError("duplicate inputs")
    text = f"""// Generated from a validated counter template. Review before integration.
module {name} (
    input wire {clk},
    input wire {rst},
    input wire {en},
    output reg [{width-1}:0] count
);
  always @(posedge {clk}) begin
    if (!{rst})
      count <= {width}'d0;
    else if ({en})
      count <= count + {width}'d1;
  end
endmodule
"""
    return text


def generate(spec_path, output):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    result = counter(spec)
    out = Path(output)
    if out.exists():
        raise FileExistsError("refusing to overwrite existing RTL")
    if out.suffix != ".v" or out.stem != spec["module"]:
        raise ValueError("output filename must match module")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out", required=True)
    a = parser.parse_args()
    generate(a.spec, a.out)


if __name__ == "__main__":
    main()
