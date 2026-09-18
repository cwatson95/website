# NE-07 — Decay chains, equilibria and radiodating

Seventh module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§5.6–5.9** (printed pp. 117–131) of Shultis
& Faw, 3rd ed.: decay with production, the Bateman chain equations, secular and
transient equilibrium, the four natural decay series, and radiodating.

- **Prerequisites:** `~NE-06` (single-nuclide kinetics — this module adds the
  source term), `~NE-05` (decay modes and branching, needed for the K/Ar
  correction), `~MA-11` (coupled linear ODE systems).
- **Cross-links:** `~NE-09` (fission products cascade down isobaric chains like
  these), `~NE-18` (radon, the largest natural dose contributor, is a
  secular-equilibrium consequence), `~NE-20` (the same production-and-decay
  equation with a neutron flux becomes xenon poisoning), `~NE-23` (spent-fuel
  activity vs cooling time is a Bateman problem), `~NE-26`/`~NE-27` (activation
  analysis and the ⁹⁹Mo/⁹⁹ᵐTc generator).

## Scope
Adding production to the decay equation, $dN/dt=-\lambda N+Q$, gives
$N(t)=N_0e^{-\lambda t}+(Q_0/\lambda)(1-e^{-\lambda t})$: activity **saturates**
at the production rate, 97% of the way there after five half-lives. For a chain,
the Bateman solution is a sum of exponentials with coefficients fixed entirely by
the decay constants. Two limits dominate practice. When the parent barely
outlives the daughter, **transient** equilibrium sets a fixed ratio
$A_2/A_1=\lambda_2/(\lambda_2-\lambda_1)>1$; when it vastly outlives it,
**secular** equilibrium makes every member of the chain carry the *same
activity* — which is why an undisturbed uranium ore holds equal activities of
²³⁸U, ²²⁶Ra and ²²²Rn despite half-lives spanning 4.5 Gy to 3.8 d, and why radon
accumulates in basements. Since $A\bmod4$ is conserved along a chain there are
exactly four series, and only three survive: the neptunium series' 2.14 My parent
has run through 2100 half-lives since the Earth formed. Dating works either by
the surviving parent (radiocarbon, good to ~57 ky) or by the accumulated stable
daughter (U/Pb, K/Ar, good to billions of years) — the latter needing no
initial-amount assumption, but needing the **branching fraction** for K/Ar.

## Operations — `code/decay_chains.py`

| call | meaning | reference |
|------|---------|-----------|
| `decay_with_production(N0, Q0, t, T)` | $N_0e^{-\lambda t}+(Q_0/\lambda)(1-e^{-\lambda t})$ | Eq. (5.53) |
| `equilibrium_number(Q0, T)`, `approach_fraction(t, T)` | $Q_0/\lambda$; $1-e^{-\lambda t}$ | §5.6.1 |
| `bateman_coefficients(lams, j)` | $C_m$ of the chain solution | Eq. (5.70) |
| `bateman_activity(lams, N1_0, t, j)`, `bateman_number(...)` | $A_j(t)$, $N_j(t)$ | Eq. (5.69) |
| `two_component_chain(l1, l2, N1_0, t)` | the closed-form parent/daughter pair | §5.6.2 |
| `daughter_maximum_time(l1, l2)` | $\ln(\lambda_2/\lambda_1)/(\lambda_2-\lambda_1)$ | §5.6.2 |
| `secular_equilibrium_activities(A, n)` | $A_0=A_1=\cdots$ | Eq. (5.72) |
| `is_secular(T1, T2)`, `is_transient(T1, T2)` | which regime applies | §5.7.4 |
| `activity_ratio(l1, l2)` | $\lambda_2/(\lambda_2-\lambda_1)$ | §5.7.4 |
| `series_of(A)`, `NATURAL_SERIES` | the four $A\bmod4$ series | §5.7.3 |
| `age_from_parent_fraction(f, T)` | $(1/\lambda)\ln(N_0/N)$ | §5.8.1 |
| `age_from_daughter_ratio(r, T, branch_fraction)` | $(1/\lambda)\ln(1+r/f)$ | §5.8.2 |
| `carbon14_age(dpm_per_g)` | radiocarbon age against 13.56 dpm/g | §5.8.1 |
| `K40_TO_AR40_BRANCH` | 0.1072 — the correction K/Ar dating needs | `~NE-05` |

## Use
```python
from decay_chains import (approach_fraction, two_component_chain, daughter_maximum_time,
                          is_secular, carbon14_age, age_from_daughter_ratio,
                          half_life_of, decay_constant, K40_TO_AR40_BRANCH)

approach_fraction(5 * T, T)                    # 0.969 -- five half-lives is enough
daughter_maximum_time(decay_constant(66.), decay_constant(6.01))   # 22.9 h
is_secular(half_life_of("238U"), half_life_of("222Rn"))            # True
carbon14_age(1.8)                              # 16606 years
age_from_daughter_ratio(0.1, half_life_of("238U")) / 3.156e7       # 6.14e8 years
age_from_daughter_ratio(1.0, half_life_of("40K"),
                        branch_fraction=K40_TO_AR40_BRANCH)        # 3.4x the naive answer
```

## Run
```bash
cd code
python3 decay_chains.py        # demo: saturation, generators, the four series, dating
python3 test_decay_chains.py   # tests  ->  "All 20 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/A4_isotopic_abundances.csv`.

## Files
- `notes.md` — decay with production and saturation → the Bateman chain →
  transient vs secular equilibrium and the equal-activity result → four series,
  three survivors → the two dating strategies and the K/Ar branching trap, with a
  "Where this goes" map.
- `code/decay_chains.py`, `code/test_decay_chains.py` (stdlib only). Tests verify
  the Bateman solution numerically against the chain ODEs, confirm the daughter
  maximum is where production equals loss, check the ⁹⁹Mo/⁹⁹ᵐTc milking interval,
  and pin the K/Ar branching factor.
- `problems/problems.md` — 8 worked problems (S&F Ch. 5 problems 18, 19, 23, 25,
  26, 28 plus two added) with numeric `*Check:*` lines.
- `figures/` — activation saturation, the ⁹⁹Mo/⁹⁹ᵐTc pair with its maximum, the
  three equilibrium regimes side by side, and the radiocarbon dating curve.
- `refs.md` — page-verified citations, plus the branching caution for
  daughter-ratio dating.
