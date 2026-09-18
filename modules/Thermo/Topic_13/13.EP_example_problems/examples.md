# 13.EP — Topic 13 Example Problems (Moran Ch.9, compressible flow)

Moran 8e's Chapter-9 worked **Examples 9.14 and 9.15** — converging nozzle and
converging–diverging nozzle — reproduced from their *given* data with the Topic-13
compressible-flow relations and verified in `code/examples.py` (`test_examples.py`). Each
regenerates the book's published answer. Citations in `refs.md`.

| Moran Ex. | concept (module) | given → find | book answer | function |
|-----------|------------------|--------------|-------------|----------|
| **9.14** Converging nozzle, back-pressure effect | choking, isentropic functions (`13.1`,`13.2`) | po=1.0 MPa, To=360 K, A₂=10⁻³ m², k=1.4; pB=(a) 500, (b) 784 kPa | p*=528 kPa; **(a)** choked: M₂=1, p₂=528 kPa, T₂=300 K, V₂=347.2 m/s, ṁ=2.13 kg/s; **(b)** subsonic: M₂=0.6, T₂=336 K, V₂=220.5 m/s, ṁ=1.79 kg/s | `ex_9_14` |
| **9.15** C–D nozzle, five cases | area–Mach, critical ratios, normal shock (`13.2`,`13.3`) | po=100 lbf/in², To=500 °R, At=1.0 in², A₂=2.4 in², k=1.4 | see below | `ex_9_15` |

### Example 9.15 — the five cases (book answers)
| case | description | exit M₂ | exit p₂ (lbf/in²) | ṁ (lb/s) |
|------|-------------|---------|-------------------|----------|
| (a) | isentropic, Mt=0.7 (A₂/A*=2.6265) | 0.24 | 95.9 | 2.29 |
| (b) | Mt=1, diverging = diffuser (subsonic root of A₂/A*=2.4) | 0.26 | 95.3 | 2.46 (choked) |
| (c) | Mt=1, diverging = nozzle (supersonic root) | 2.4 | 6.84 | 2.46 |
| (d) | normal shock at exit (Mx=2.4, px=6.84 → My=0.52, py/px=6.5533) | 0.52 | 44.82 | 2.46 |
| (e) | shock in diverging section at Ax=2.0 in² (Mx=2.2, poy/pox=0.62812, A₂/A*y=1.51) | 0.43 | 55.3 | 2.46 |

**Key lesson (§9.13–9.14).** First test for **choking**: a converging nozzle chokes when
pB ≤ p* = (2/(k+1))^{k/(k−1)}·po; once choked the mass flow is fixed at its maximum. A
C–D nozzle’s exit can be subsonic *or* supersonic for the same A₂/A* (two roots); off the
supersonic design pressure, a **normal shock** appears in the diverging section, dropping
poy/pox and raising the exit pressure.

> **Stepwise-rounding note.** Where Moran reads coarse **Table 9.2 / 9.3** values
> (e.g. M₂=0.24 with T₂/To=0.988, p₂/po=0.959 in 9.15a), `examples.py` uses the same
> table-read values the book quotes, so the published answers reproduce exactly; the
> A/A*, p*/po and shock ratios that Moran computes are computed here as well.

## Run
```bash
cd code
python3 examples.py          # both examples vs the book answers
python3 test_examples.py     # -> "All 39 tests passed."
```
