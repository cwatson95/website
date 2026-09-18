# 2.3 — Compression Work

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`.

The negative branch of moving-boundary work: when a system is **compressed**
(`V₂<V₁`), `W = ∫p dV < 0` — the surroundings do work on the system (a compressor
or pump). The **work input** is `−W > 0`. Mirror of `2.2`; shared `∫p dV`
machinery in `1.2`/`1.5`.

| call | meaning |
|------|---------|
| `compression_work(p_of_V, V1, V2)` | `∫p dV` (requires `V2<V1`), < 0 |
| `work_input(p_of_V, V1, V2)` | `−W` (the work to supply), > 0 |
| `polytropic_compression(p1, V1, V2, n)` | `pVⁿ=const` work, < 0 |

```bash
cd code && python3 compression_work.py
python3 test_compression_work.py      # "All 6 tests passed."
```

Files: `notes.md`, `code/compression_work.py`, `code/test_compression_work.py`,
`problems/problems.md`, `refs.md`.
