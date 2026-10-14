# Auto-generated execution expects environment variables:
# RTL_LIST (newline separated), TOP, SDC, LIB_LIST (space-separated), OUT
# All project paths should be validated on the remote machine before launch.
set search_path [concat $search_path [list .]]
set target_library [split $env(LIB_LIST) " "]
set link_library [concat [list "*"] $target_library]
file mkdir $env(OUT)
set files [split [string trim [read [open $env(RTL_LIST) r]]] "\n"]
foreach f $files {
  if {$f ne ""} { analyze -format sverilog $f }
}
elaborate $env(TOP)
current_design $env(TOP)
link
check_design > $env(OUT)/check_design.rpt
source $env(SDC)
compile_ultra
write -format verilog -hierarchy -output $env(OUT)/mapped.v
write_sdc $env(OUT)/mapped.sdc
report_area -hierarchy > $env(OUT)/area.rpt
report_timing -max_paths 30 > $env(OUT)/timing.rpt
report_reference -hierarchy > $env(OUT)/references.rpt
report_constraint -all_violators > $env(OUT)/violations.rpt
