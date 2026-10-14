// Structural top: example shows explicit parameter/port mapping.
module compute_top_example #(
    parameter DATA_W = 16
) (
    input  wire                 core_clk,
    input  wire                 rst_n,
    input  wire                 din_vld,
    input  wire [DATA_W-1:0]    din0,
    input  wire [DATA_W-1:0]    din1,
    output wire                 dout_vld,
    output wire [DATA_W:0]      dout
);
    compute_pe #(.DATA_W(DATA_W)) u_compute_pe (
        .clk      (core_clk),
        .rst_n    (rst_n),
        .din_vld  (din_vld),
        .din0     (din0),
        .din1     (din1),
        .dout_vld (dout_vld),
        .dout     (dout)
    );
endmodule
