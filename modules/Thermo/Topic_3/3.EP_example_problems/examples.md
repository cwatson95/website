# 3.EP — Topic 3 Example Problems (Moran Ch.5, the second law)

Moran 8e's Chapter-5 worked **Examples 5.1–5.3** — power cycle, refrigerator, heat
pump — reproduced from their *given* data with the Topic-3 relations and verified in
`code/examples.py` (`test_examples.py`). Each regenerates the book's published
answer. Citations in `refs.md`. (Topic-1 already covers the Ch.1–2 examples; Topic-3
adds the second-law set.)

| Moran Ex. | concept (module) | given → find | book answer | function |
|-----------|------------------|--------------|-------------|----------|
| **5.1** Power-cycle performance | Carnot ceiling, corollary 1 (`3.3`) | T_H=2000 K, T_C=400 K; (a) η=60%, (b) Q_H=1000/W=850 kJ, (c) Q_H=1000/Q_C=200 kJ | η_max=80%; (a) irreversible, (b) **impossible**, (c) W=800 kJ, reversible | `ex_5_1` |
| **5.2** Evaluating a refrigerator | max COP β (`3.3`, Eq. 5.10) | T_C=268 K, T_H=295 K; Q̇_C=8000, Ẇ=3200 kJ/h | β=2.5, β_max=9.9 → irreversible; inventor's β=10 claim **invalid** | `ex_5_2` |
| **5.3** Evaluating a heat pump | max COP γ (`3.3`, Eq. 5.11) | T_H=530 °R, T_C=492 °R; Q_H=5×10⁵ Btu/day; $0.13/kWh | γ_max=13.95; W_min=3.58×10⁴ Btu/day; cost $1.36/day | `ex_5_3` |

**Key lesson (corollaries of §5.5/§5.9):** an actual cycle's η is *below* the Carnot
ceiling and its COP is *below* β_max/γ_max; a claim that exceeds them is impossible.
Temperatures in Carnot formulas must be **absolute** (K or °R).

## Run
```bash
cd code
python3 examples.py          # all three examples vs the book answers
python3 test_examples.py     # -> "All 14 tests passed."
```
