# RTL source management compatible with Compiler_Codes

## Observed ACTransformer-DS pattern
```text
rtl/ACTransformer_DS/rtl/
  hdl/
    common/{fifo,ram,sync,clk,...}/
    buf_mgr/
    ctc/ct_cluster_ds/{common,ct_ctrl,mixed_precision,pp,tdp,top}/
    ...
  filelist/
    common.f
    ctc.f
    buf_mgr.f
    npu_top.f
    ...
  tb/
  macro/
```

## Recommended layout for a new accelerator
```text
rtl/
  hdl/
    common/{fifo,ram,sync,arithmetic}/
    compute/{pe,array,postprocess}/
    memory/{bank,buffer,controller}/
    control/
    top/
  macro/
  filelist/{common,compute,memory,top,sim}.f
  tb/{unit,integration}/
  assertions/
  constraints/{sdc}/
  scripts/{sim,synth,sta,power}/
  docs/
build/               # ignored
reports/             # ignored
```
The recommended layout is an extension, not a claim that Compiler_Codes uses all these directories. For an existing project, preserve its original hierarchy.

## Source management rules
1. Exactly one authoritative top-level source manifest for each build target; lower-level manifests may be included using a documented resolution base.
2. Maintain explicit RTL source listings in a deterministic order; do not rely on shell recursive globbing as the synthesis filelist.
3. Verify the filelist parser's syntax. Some tools interpret nested `-f` relative to CWD, others relative to the including file; normalize before invoking tools.
4. Never compile `.vh` or `.svh` headers as standalone modules unless the project deliberately defines them as compilation units.
5. Preserve defines, include paths and compilation order in both local lint and remote DC/VCS staging.
6. Prefer a single canonical owner of reusable primitives such as FIFO and float_adder to avoid duplicate-module collisions.
7. When moving RTL: update parent instantiations only if necessary, all affected filelists, tests, include paths, synthesis constraints and generated build metadata.
8. Testbench and DUT must not share accidental duplicate module names; simulation-only code must not enter synthesis.
9. Generated content goes under ignored build/output directories; no proprietary SRAM views or foundry data in public Git.
10. Validate elaboration of top-level build and any independently built submodules after reorganizing.
