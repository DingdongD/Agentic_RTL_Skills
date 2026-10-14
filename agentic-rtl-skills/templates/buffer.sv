// Buffer wrapper with synchronous 1-cycle registered read-data behavior.
// One outstanding read per cycle; read-during-write same-address is not defined.
module lbuf_wrap_example #(
    parameter DATA_W = 32,
    parameter ADDR_W = 8
) (
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 lbuf_wr_req,
    input  wire [ADDR_W-1:0]    lbuf_waddr,
    input  wire [DATA_W-1:0]    lbuf_wdata,
    input  wire                 lbuf_rd_req,
    input  wire [ADDR_W-1:0]    lbuf_raddr,
    output reg  [DATA_W-1:0]    lbuf_rdata,
    output reg                  lbuf_rdata_vld
);
    reg [DATA_W-1:0] mem [0:(1<<ADDR_W)-1];

    always @(posedge clk) begin
        if (lbuf_wr_req)
            mem[lbuf_waddr] <= lbuf_wdata;
        if (lbuf_rd_req)
            lbuf_rdata <= mem[lbuf_raddr];
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            lbuf_rdata_vld <= 1'b0;
        else
            lbuf_rdata_vld <= lbuf_rd_req;
    end
endmodule
