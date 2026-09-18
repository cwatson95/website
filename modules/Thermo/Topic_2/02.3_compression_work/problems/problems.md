# 2.3 — Problems

Check with `code/compression_work.py`. Citations in `../refs.md`.

### P1.  Polytropic compression work  *(Moran 8e Example 2.1a, p.50)*
Air is compressed along `pV^1.3 = const` from 100 kPa, 1 m³ to 0.5 m³. Find the
work and the work input.
*Answer:* `W = −77.05 kJ`; work input `= −W = 77.05 kJ`.
*Check:* `polytropic_compression(100,1,0.5,1.3)` ≈ −77.05.

### P2.  Constant-pressure compression input  *(Moran 8e Eq. 2.17, p.48)*
A gas is compressed at constant 150 kPa from 1 m³ to 0.6 m³. Find the work input.
*Answer:* `W = 150(0.6−1) = −60 kJ`; work input `= 60 kJ`.
*Check:* `work_input(lambda V: 150, 1, 0.6)` = 60.
