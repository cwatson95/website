# NE-06 — Decay kinetics

Sixth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§5.5** (printed pp. 111–117) of Shultis &
Faw, 3rd ed.: the decay constant, exponential decay, half-life, mean life,
activity, and competing decay channels.

- **Prerequisites:** `~NE-05` (which decay mode and how much energy — this module
  supplies the rate), `~MA-09` (first-order linear ODEs), `~ST-11` (the
  exponential distribution, which is the decay-time density).
- **Cross-links:** `~NE-07` (chains of decays, equilibrium, radiodating),
  `~NE-11` (the identical mathematics with distance replacing time: $e^{-\mu x}$),
  `~NE-16` (counting statistics — activity is a rate, so counts are Poisson),
  `~NE-18` (specific activity and half-life set the hazard), `~NE-20` (the same
  kinetics plus a production term becomes reactor point kinetics).

## Scope
One assumption — a constant decay probability per unit time — gives
$dN/dt=-\lambda N$ and therefore $N(t)=N_0e^{-\lambda t}$, and everything else is
a rearrangement: $T_{1/2}=\ln2/\lambda$, mean life $1/\lambda=1.443\,T_{1/2}$,
waiting-time density $\lambda e^{-\lambda t}$, and activity $A=\lambda N$.
Decay is **memoryless**: survival to $t$ does not depend on prior age, so a
nucleus has no meaningful age. What is measured is activity, in becquerels (one
decay per second) or curies ($3.7\times10^{10}$ Bq, historically one gram of
²²⁶Ra — which the code reproduces as 0.989 Ci/g, the 1% gap being a later
revision of radium's half-life). Specific activity goes as $1/T_{1/2}$, spanning
ten orders of magnitude from ³H ($10^{4}$ Ci/g) to ²³⁸U ($10^{-7}$ Ci/g): the
most intensely radioactive nuclides are the ones that vanish fastest, and that
trade-off organises radiological protection and waste management. Competing
channels add **rates**, not half-lives.

## Operations — `code/decay_kinetics.py`

| call | meaning | reference |
|------|---------|-----------|
| `decay_constant(T)`, `half_life(lam)` | $\lambda=\ln2/T_{1/2}$ | Eq. (5.36) |
| `mean_lifetime(T)` | $1/\lambda=1.443\,T_{1/2}$ | Eq. (5.44) |
| `number_remaining(N0, t, T)` | $N_0e^{-\lambda t}$ | Eqs. (5.34), (5.39) |
| `fraction_remaining(t, T)`, `half_lives_elapsed(f)` | $e^{-\lambda t}$; $-\log_2f$ | Eq. (5.38) |
| `survival_probability`, `decay_probability` | $e^{-\lambda t}$; $1-e^{-\lambda t}$ | Eqs. (5.40)–(5.42) |
| `decay_time_pdf(t, T)` | $\lambda e^{-\lambda t}$ | Eq. (5.43) |
| `activity(N, T)`, `activity_at_time(A0, t, T)` | $A=\lambda N$; $A_0e^{-\lambda t}$ | Eq. (5.45) |
| `specific_activity(T_s, A)` | Bq per gram of pure nuclide | §5.5.6 |
| `time_to_fraction(f, T)`, `time_to_activity(A0, A, T)` | invert the exponential | §5.5 |
| `total_decay_constant(lams)` | $\lambda=\sum\lambda_i$ | Eq. (5.48) |
| `branching_fractions(lams)` | $f_i=\lambda_i/\lambda$ | Eq. (5.49) |
| `partial_half_life(T, f)` | $T/f$ — longer than observed, never measured alone | §5.5.8 |
| `curies(bq)`, `becquerels(ci)` | 1 Ci $=3.7\times10^{10}$ Bq | §5.5.6 |
| `parse_half_life(s)`, `load_half_lives()`, `half_life_of(nuc)` | Appendix A.4 half-lives, 918 nuclides | Table A.4 |

## Use
```python
from decay_kinetics import (decay_constant, mean_lifetime, specific_activity,
                            curies, half_life_of, fraction_remaining)

half_life_of("137Cs")                    # 9.52e8 s  (30.17 y)
decay_constant(half_life_of("60Co"))     # 4.167e-9 /s
mean_lifetime(t_half=10.0) / 10.0        # 1.442695 -- NOT 1
curies(specific_activity(half_life_of("226Ra"), 226))   # 0.9886 Ci/g
fraction_remaining(10 * half_life_of("131I"), half_life_of("131I"))   # 9.8e-4
```

## Run
```bash
cd code
python3 decay_kinetics.py        # demo: half-lives, specific activities, branching
python3 test_decay_kinetics.py   # tests  ->  "All 19 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/A4_isotopic_abundances.csv`.

## Files
- `notes.md` — one assumption and everything that follows → activity and the
  curie → specific activity and the inversion it forces → competing channels →
  reading half-lives out of Appendix A.4, with a "Where this goes" map.
- `code/decay_kinetics.py`, `code/test_decay_kinetics.py` (stdlib only). Tests
  verify memorylessness, numerically integrate the decay-time density to confirm
  its normalisation and mean, check ten Appendix A.4 half-lives against standard
  values, and reproduce the historical definition of the curie.
- `problems/problems.md` — 8 worked problems (S&F Ch. 5 problems 8, 10–14 plus
  two added) with numeric `*Check:*` lines.
- `figures/` — the exponential on linear and log axes, specific activity against
  half-life across ten decades, the mean-vs-median gap, and a two-channel
  branching diagram.
- `refs.md` — page-verified citations, plus notes on the curie and on which
  "year" the half-life units use.
