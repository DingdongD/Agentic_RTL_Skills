"""Real ready/valid FIFO cycle regression; fixed protocol and scoreboard."""
import shutil
import subprocess
import tempfile
from pathlib import Path


RTL = r"""
module sync_fifo #(parameter WIDTH=8, DEPTH=4, ADDR=2) (
  input wire clk, input wire rst_n,
  input wire in_valid, output wire in_ready, input wire [WIDTH-1:0] in_data,
  output wire out_valid, input wire out_ready, output wire [WIDTH-1:0] out_data
);
  reg [WIDTH-1:0] memory [0:DEPTH-1];
  reg [ADDR-1:0] wptr, rptr;
  reg [ADDR:0] used;
  wire take_out = out_valid && out_ready;
  wire take_in = in_valid && in_ready;
  assign out_valid = (used != 0);
  assign in_ready = (used != DEPTH) || take_out;
  assign out_data = memory[rptr];
  always @(posedge clk) begin
    if (!rst_n) begin
      wptr <= 0; rptr <= 0; used <= 0;
    end else begin
      if (take_in) begin
        memory[wptr] <= in_data;
        wptr <= wptr + 1'b1;
      end
      if (take_out) rptr <= rptr + 1'b1;
      case ({take_in,take_out})
        2'b10: used <= used + 1'b1;
        2'b01: used <= used - 1'b1;
        default: used <= used;
      endcase
    end
  end
endmodule
"""

TB = r"""
module tb;
  reg clk=0, rst_n=0, in_valid=0, out_ready=0;
  reg [7:0] in_data=0;
  wire in_ready, out_valid;
  wire [7:0] out_data;
  integer head=0, tail=0, cycle=0, seed=32'h43671;
  reg [7:0] expected[0:2047];
  integer pop, push;
  sync_fifo dut(.clk(clk),.rst_n(rst_n),.in_valid(in_valid),
                .in_ready(in_ready),.in_data(in_data),.out_valid(out_valid),
                .out_ready(out_ready),.out_data(out_data));
  always #5 clk=~clk;
  initial begin
    repeat (3) @(negedge clk);
    rst_n=1;
    for (cycle=0;cycle<600;cycle=cycle+1) begin
      @(negedge clk);
      in_valid=($random(seed) & 3) != 0;
      out_ready=($random(seed) & 3) != 0;
      in_data=cycle[7:0];
      #1;
      pop=out_valid && out_ready;
      push=in_valid && in_ready;
      if (out_valid !== (head!=tail)) $fatal(1,"empty/full mismatch %0d",cycle);
      if (pop && out_data !== expected[head]) $fatal(1,"data mismatch %0d",cycle);
      @(posedge clk);
      if (pop) head=head+1;
      if (push) begin expected[tail]=in_data; tail=tail+1; end
      if (tail-head>4 || tail<head) $fatal(1,"occupancy violation");
    end
    $display("RTL_FIFO_PASS");
    $finish;
  end
  initial begin #100000; $fatal(1,"timeout"); end
endmodule
"""


def run():
    if not shutil.which("iverilog") or not shutil.which("vvp"):
        raise RuntimeError("Icarus unavailable")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "fifo.v").write_text(RTL)
        (root / "tb.v").write_text(TB)
        exe = root / "sim.out"
        a = subprocess.run(["iverilog","-g2012","-s","tb","-o",str(exe),
                            str(root/"fifo.v"),str(root/"tb.v")],
                           capture_output=True,text=True)
        if a.returncode:
            raise RuntimeError(a.stderr)
        b = subprocess.run(["vvp",str(exe)],capture_output=True,text=True,timeout=30)
        if b.returncode or "RTL_FIFO_PASS" not in b.stdout:
            raise RuntimeError(b.stdout + b.stderr)
        print(b.stdout.strip())


if __name__ == "__main__":
    run()
