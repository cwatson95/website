# 5.EP — Topic 5 Example Problems (Moran Ch.3 & Ch.6, property evaluation)

Moran 8e worked **Examples 3.2, 3.4, and 6.1** — all WATER — reproduced from their *given*
data with the Topic-5 steam-table tools (concept modules 5.1–5.5) and verified in
`code/examples.py` (`test_examples.py`). Each regenerates the book's published answer. Two
published **in-text illustrations** (p.112, p.296) are added for full table coverage.
Citations in `refs.md`.

| Moran Ex. | concept (module) | given → find | book answer | function |
|-----------|------------------|--------------|-------------|----------|
| **3.2** Heating Water at Constant Volume | quality, saturation tables (`5.1`) | rigid `V=0.5 m³`, `p₁=1 bar`, `x₁=0.5` → `p₂=1.5 bar` | `v₁=0.8475`, `T₁=99.63 °C`, `T₂=111.4 °C`, `m=0.59 kg`, `mg₁=0.295`, `x₂=0.731`, `mg₂=0.431 kg`, `p₃=2.11 bar` | `ex_3_2` |
| **3.4** Analyzing Two Processes in Series | superheated + two-phase, work (`5.1`,`5.2`,`5.4`) | `10 bar, 400 °C` → cool isobaric to sat. vap → cool const-`v` to `150 °C` | `v₁=0.3066`, `u₁=2957.3`, `v₂=0.1944`, `W/m=−112.2`, `x₃=0.494`, `u₃=1584.0`, `Q/m=−1485.5 kJ/kg` | `ex_3_4` |
| **6.1** Reversible Work & Heat for Water | p–v & T–s areas (`5.4`,`5.5`) | sat. liq → sat. vap at `150 °C` (423.15 K), int. reversible, const `p,T` | `W/m=p(v₂−v₁)=186.38`, `Q/m=T(s₂−s₁)=2114.1 kJ/kg` | `ex_6_1` |

### In-text illustrations (published numbers, not numbered Examples)
| where | given → find | book value | function |
|-------|--------------|------------|----------|
| p.112 | water `0.10 MPa`, `u=2537.3 kJ/kg` → `T,v,h`; check `h=u+pv` | `T=120 °C`, `v=1.793`, `h=2716.6 kJ/kg` | `ex_superheat_uh` |
| p.296 (Mollier) | water `240 °C, 0.10 MPa`, isentropic to `0.01 MPa` → `x₂,h₂` | `x₂≈0.98`, `h₂≈2537 kJ/kg` | `ex_mollier` |

**Key lessons.** Inside the dome `p` and `T` are not independent, so a second property
(quality, `v`) is needed (Ex 3.2). A rigid process pins `v`, turning a pressure change into
a quality change (Ex 3.2, 3.4). The work term is the p–v area `∫p dV` and the reversible
heat is the T–s area `∫T dS` (Ex 6.1). Off the grid, interpolate (single, double, or
inverse).

> **Stepwise-rounding note.** Moran rounds the quality of Ex 3.4 to `x₃=0.494` *before*
> forming `u₃ = uf₃ + x₃(ug₃ − uf₃)`; `examples.py` replicates that rounding, so `u₃` and
> `Q/m` reproduce the book exactly (the unrounded quality would give `u₃≈1583.1`). The
> Mollier values (p.296) are **chart reads** the book itself calls approximate
> ("agree closely … x₂=0.98, h₂=2537"); the table computation gives `x₂≈0.979`, `h₂≈2535`,
> checked within chart accuracy.

## Run
```bash
cd code
python3 examples.py          # all examples vs the book answers
python3 test_examples.py     # -> "All 29 tests passed."
```
