// One-clock, fall-through-disabled FIFO example.
// Adapt read timing and simultaneous push/pop policy explicitly.
module sfifo_example #(
    parameter DATA_W = 32,
    parameter ADDR_W = 3,
    parameter DEPTH  = (1 << ADDR_W)
) (
    input  wire                 clk,
    input  wire                 rst_n,
    input  wire                 fifo_wr,
    input  wire [DATA_W-1:0]    fifo_wdata,
    output wire                 fifo_ff,
    input  wire                 fifo_rd,
    output reg  [DATA_W-1:0]    fifo_rdata,
    output wire                 fifo_ef
);
    reg [DATA_W-1:0] mem [0:DEPTH-1];
    reg [ADDR_W-1:0] wr_addr;
    reg [ADDR_W-1:0] rd_addr;
    reg [ADDR_W:0]   fifo_cnt;
    wire pop  = fifo_rd && !fifo_ef;
    wire push = fifo_wr && (!fifo_ff || pop);
    assign fifo_ff = (fifo_cnt == DEPTH);
    assign fifo_ef = (fifo_cnt == 0);

    // Template supports DEPTH=2**ADDR_W. For other depths add modulo-wrap.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_addr    <= '0;
            rd_addr    <= '0;
            fifo_cnt   <= '0;
            fifo_rdata <= '0;
        end else begin
            if (push) begin
                mem[wr_addr] <= fifo_wdata;
                wr_addr <= wr_addr + 1'b1;
            end
            if (pop) begin
                fifo_rdata <= mem[rd_addr];
                rd_addr <= rd_addr + 1'b1;
            end
            case ({push, pop})
                2'b10: fifo_cnt <= fifo_cnt + 1'b1;
                2'b01: fifo_cnt <= fifo_cnt - 1'b1;
                default: fifo_cnt <= fifo_cnt;
            endcase
        end
    end
endmodule
