# RE-04 — Time Dilation, Length Contraction & Simultaneity

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The three
geometrical consequences of the Lorentz boost — and the "paradoxes" that dissolve
once you take them together.

- **Prerequisites:** `RE-03` (Lorentz transformations — every effect here is read
  off one boost). Soft: `~CM-03` (the Newtonian c→∞ limit each result reduces to).
- **Feeds into:** `~RE-05` (Minkowski 4-vectors & the invariant interval, where
  proper time becomes timelike arc length), `~RE-06` (relativistic dynamics),
  `~RE-07` (Doppler & aberration).

## Scope
Proper time and **time dilation** Δt = γΔτ (moving clocks run slow); **length
contraction** L = L₀/γ (longitudinal only) and how it is *operationally* measured;
the **relativity of simultaneity** (leading clocks lag βL₀); the realisation that
these three are **one boost read three ways**; **muon decay** as the canonical
experimental confirmation; and the **pole-in-barn** and **twin** paradoxes
resolved. Closes with the **Minkowski diagram** picture: worldlines and the
scissoring of boosted axes.

## Conventions (whole RE trunk)
- Natural units **c = 1**; an event is `x = (ct, x, y, z)`. Times and lengths share
  a unit, so e.g. `distance/(βτ)` is dimensionless.
- `β = v/c`, `γ = 1/√(1−β²) ≥ 1`.
- Metric **η = diag(−1,+1,+1,+1)** (mostly-plus). Frame **S′** moves at **+β x̂**
  relative to S; the boost is `ct' = γ(ct − βx)`, `x' = γ(x − βct)`.
- **Proper** = measured in the object's own rest frame: proper time τ (clock at one
  place), rest/proper length L₀ (rod at rest).

## The one idea
Time dilation, length contraction, and the relativity of simultaneity are **not
three effects but one Lorentz boost read three ways**. Feed pairs of events into
`ct' = γ(ct − βx)`, `x' = γ(x − βct)`:

```
two ticks of one clock      (same x')  →  Δt  = γ Δτ      time dilation
two ends of a rod at one t  (same ct)  →  L   = L₀ / γ    length contraction
two synced clocks at one t  (same ct)  →  lag = β L₀      simultaneity
```

The γ that **stretches** time is the same γ that **shrinks** length; the "βx"
cross-term that **desynchronises** clocks is what makes the paradoxes evaporate.

## Operations — `code/sr_effects.py`
| call | meaning |
|------|---------|
| `gamma(beta)` | Lorentz factor γ = 1/√(1−β²) |
| `time_dilation(dtau, beta)` / `proper_time(dt, beta)` | Δt = γΔτ ↔ Δτ = Δt/γ (inverses) |
| `length_contraction(L0, beta)` / `rest_length(L, beta)` | L = L₀/γ ↔ L₀ = γL (inverses) |
| `leading_clocks_lag(L0, beta)` | βL₀ — the leading clock's deficit |
| `muon_fraction(tau0, beta, distance)` | (relativistic, naive) survival fractions |
| `twin_ages(beta, T_home)` | (T_home, T_home/γ) — traveller returns younger |
| `pole_in_barn(L0_pole, L_barn, beta)` | contracted pole, "fits?", door-shut gap in each frame |
| `boosted_axes(beta)` | ct′-axis `[1,β]`, x′-axis `[β,1]` in the (ct,x) diagram |

## Use
```python
from sr_effects import time_dilation, length_contraction, muon_fraction, pole_in_barn

time_dilation(1.0, 0.6)            # 1.25   (a 1 s tick read as 1.25 s)
length_contraction(1.0, 0.6)       # 0.80   (a 1 m rod measured at 0.80 m)
muon_fraction(2.2, 0.98, 33.0)     # (0.0476, 2.25e-07): relativity vs Newton
pole_in_barn(10, 10, 0.6)          # door-shuts simultaneous in barn frame, not pole frame
```

## Run
```bash
cd code
python3 sr_effects.py          # demo: γ table, the three readings, muon, twins, barn, axes
python3 test_sr_effects.py     # 8 property-based tests -> "All 8 tests passed."
```

## Files
- `notes.md` — proper time → dilation, contraction & its measurement, simultaneity, one-boost-three-ways, muon, paradoxes, Minkowski diagrams
- `code/sr_effects.py` — the library (pure stdlib; events / diagram directions are short lists)
- `code/test_sr_effects.py` — inverses, boost cross-checks, leading-clock lag, muon, twins, barn, scissored axes
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee III.4)
- `refs.md` — verified textbook citations
