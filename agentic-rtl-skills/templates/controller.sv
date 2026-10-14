// Start/done controller, serialized operations, parameterized latency.
// Pulse done for one cycle; start while busy is ignored.
module ct_ctrl_example #(
    parameter LATENCY = 4,
    parameter CNT_W   = $clog2(LATENCY+1)
) (
    input  wire clk,
    input  wire rst_n,
    input  wire din_st,
    output reg  busy,
    output reg  dout_vld
);
    reg [CNT_W-1:0] cycle_cnt;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            busy      <= 1'b0;
            dout_vld  <= 1'b0;
            cycle_cnt <= '0;
        end else begin
            dout_vld <= 1'b0;
            if (!busy && din_st) begin
                busy      <= 1'b1;
                cycle_cnt <= LATENCY-1;
            end else if (busy && cycle_cnt == 0) begin
                busy      <= 1'b0;
                dout_vld  <= 1'b1;
            end else if (busy) begin
                cycle_cnt <= cycle_cnt - 1'b1;
            end
        end
    end
endmodule
