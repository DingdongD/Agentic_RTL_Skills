# PTPX/PrimePower is license/version dependent; verify commands on site.
# Required env TOP LIB_LIST NETLIST SDC OUT; optional SAIF STRIP_PATH.
set_app_var target_library [split $env(LIB_LIST) " "]
set_app_var link_path [concat [list "*"] $target_library]
file mkdir $env(OUT)
read_verilog $env(NETLIST)
current_design $env(TOP)
link_design
read_sdc $env(SDC)
if {[info exists env(SAIF)] && $env(SAIF) ne ""} {
  if {[info exists env(STRIP_PATH)] && $env(STRIP_PATH) ne ""} {
    read_saif -input $env(SAIF) -strip_path $env(STRIP_PATH)
  } else {
    read_saif -input $env(SAIF)
  }
}
update_power
report_power -hierarchy > $env(OUT)/power.rpt
report_switching_activity > $env(OUT)/activity.rpt
