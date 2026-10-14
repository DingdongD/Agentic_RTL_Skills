# PrimeTime report triage

Given a hypothetical mapped design, first check clocks and unconstrained endpoints, then maximum and minimum timing reports. WNS >= 0 with no constrained paths is **not** a pass. Record the analysis coverage report and classify unchecked paths; report top failing startpoint/endpoint, cells, net/logic delay, corner, SDC hash and parasitics. A pre-layout run with no SPEF must be labeled pre-layout. Timing coverage is not VCS functional coverage.
