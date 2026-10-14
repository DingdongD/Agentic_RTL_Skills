# SRAM macro integration example

Start from `configs/memory.macros.example.json` (illustrative), then verify each actual macro's legal width/depth, port count, read-during-write semantics, read latency, power pins and library corner. Run `adapters/memory_adapter.py` via its Python API `validate_manifest(path)`; this is schema presence validation, **not** a Memory Compiler. Treat missing Liberty/RTL/LEF or unsupported macro settings as unresolved; never substitute zero macro area. Proprietary files should remain on the licensed EDA host.
