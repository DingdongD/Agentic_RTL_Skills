// Compute PE template: generic original example, not proprietary RTL.
// Contract: one accepted input per cycle; one registered output after one clock edge.
module compute_pe #(
    parameter DATA_W = 16
) (
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  din_vld,
    input  wire [DATA_W-1:0]     din0,
    input  wire [DATA_W-1:0]     din1,
    output reg                   dout_vld,
    output reg  [DATA_W:0]       dout
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            dout     <= {(DATA_W+1){1'b0}};
            dout_vld <= 1'b0;
        end else begin
            dout_vld <= din_vld;
            if (din_vld)
                dout <= {1'b0, din0} + {1'b0, din1};
        end
    end

endmodule
