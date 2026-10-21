"""Real HDL smoke regression for generated RTL, using iverilog/vvp."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from generation.rtl_scaffold import generate


def run():
    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        raise RuntimeError("iverilog/vvp unavailable: real RTL regression is BLOCKED")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        spec = root / "spec.json"
        spec.write_text(json.dumps({"kind":"counter","reset":"synchronous_active_low",
                                    "module":"generated_counter","width":8}))
        rtl = generate(spec, root / "generated_counter.v")
        bench = root / "tb.v"
        bench.write_text("""
module tb;
  reg clk=0, rst_n=0, en=0;
  wire [7:0] count;
  generated_counter dut(.clk(clk),.rst_n(rst_n),.en(en),.count(count));
  always #5 clk=~clk;
  initial begin
    @(negedge clk);
    @(posedge clk); #1;
    if (count !== 8'd0) $fatal(1, "reset failure");
    @(negedge clk); rst_n=1; en=1;
    @(posedge clk); #1;
    if (count !== 8'd1) $fatal(1, "enable failure");
    @(negedge clk); en=0;
    @(posedge clk); #1;
    if (count !== 8'd1) $fatal(1, "hold failure");
    @(negedge clk); en=1;
    repeat (255) @(posedge clk);
    #1;
    if (count !== 8'd0) $fatal(1, "overflow wrap failure");
    $display("RTL_COUNTER_PASS");
    $finish;
  end
  initial begin #10000; $fatal(1, "timeout"); end
endmodule
""")
        output = root / "sim.out"
        build = subprocess.run(["iverilog","-g2005","-s","tb","-o",str(output),
                                str(rtl),str(bench)],capture_output=True,text=True)
        if build.returncode != 0:
            raise RuntimeError(build.stderr)
        result = subprocess.run(["vvp",str(output)],capture_output=True,text=True)
        if result.returncode != 0 or "RTL_COUNTER_PASS" not in result.stdout:
            raise RuntimeError("real RTL simulation failed: " + result.stdout + result.stderr)
        print(result.stdout.strip())


if __name__ == "__main__":
    run()
