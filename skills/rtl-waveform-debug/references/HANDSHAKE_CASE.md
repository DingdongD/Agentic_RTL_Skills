# Waveform-based debug worked procedure

Scenario: buffer read expected at edge N+1 but `lbuf_rdata_vld` is misaligned.

| edge | lbuf_rd_req | lbuf_raddr | expected rdata_vld | observation |
| --- | --- | --- | --- | --- |
| N-1 | 0 | - | 0 | establish idle |
| N | 1 | 5 | 1 after NBA at edge N | registered request |
| N+1 | 0 | - | 0 after NBA at edge N+1 | compare observed data |

The above is an **illustrative trace expectation**, not a trace captured from actual simulation. Sample signals consistently before or after nonblocking-assignment updates. Diagnose whether the testbench expects an extra cycle because it samples just before the active edge. Verify SRAM macro latency separately before adapting this example.

Capture `clk`, `rst_n`, `lbuf_rd_req`, `lbuf_raddr`, `lbuf_rdata`, `lbuf_rdata_vld`. Find the first diverging edge; reproduce with fixed stimulus; distinguish scheduling-region testbench errors from DUT data-path errors.
