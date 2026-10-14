# Runs pre-layout STA unless annotated parasitics are provided.
# Required env: TOP, LIB_LIST, NETLIST, SDC, OUT; optional SPEF.
set search_path [concat $search_path [list .]]
set_app_var target_library [split $env(LIB_LIST) " "]
set_app_var link_path [concat [list "*"] $target_library]
file mkdir $env(OUT)
read_verilog $env(NETLIST)
current_design $env(TOP)
link_design
read_sdc $env(SDC)
if {[info exists env(SPEF)] && $env(SPEF) ne ""} {
  read_parasitics -format spef $env(SPEF)
}
check_timing -verbose > $env(OUT)/check_timing.rpt
report_analysis_coverage > $env(OUT)/timing_coverage.rpt
report_constraint -all_violators > $env(OUT)/constraints.rpt
report_timing -delay_type max -max_paths 50 > $env(OUT)/setup_paths.rpt
report_timing -delay_type min -max_paths 50 > $env(OUT)/hold_paths.rpt
report_global_timing > $env(OUT)/global_timing.rpt
