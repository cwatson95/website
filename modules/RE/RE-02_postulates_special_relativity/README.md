# RE-02 — Postulates of Special Relativity

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The
conceptual root of special relativity: the two postulates, what "the speed of
light is constant" *operationally means*, and the consequences forced the instant
you accept it — the relativity of simultaneity and time dilation.

- **Prerequisites:** `RE-01` (Galilean relativity & its failure — Michelson–Morley,
  the ether). Soft: `~CM-03` (inertial frames — the `c→∞` limit recovered here).
- **Feeds into:** `RE-03` (the Lorentz boost is the unique linear map honouring
  these postulates), `~RE-04` (time dilation & length contraction made
  quantitative), `~RE-07` (the Bondi `k` **is** the relativistic Doppler factor).

## Scope
Einstein's **two postulates** (principle of relativity + universal `c`); why
Galilean kinematics is **incompatible with Maxwell**; **Einstein clock
synchronization** (the midpoint / two-way-light convention) and the operational
meaning of constant `c`; the **relativity of simultaneity** as the immediate
consequence; the **Bondi k-calculus / radar method** with Doppler factor
`k = √((1+β)/(1−β))`; and the **transverse light clock** that *derives* the
time-dilation factor `γ` straight from the constancy of `c`.

## Conventions (whole RE trunk)
- Natural units **c = 1**; an event is `x = (ct, x, y, z)` (time component `x⁰=ct`).
- `β = v/c`, `γ = 1/√(1−β²)`.
- Metric **η = diag(−1,+1,+1,+1)** (mostly-plus). A boost to a frame moving at
  `+β` acts as `ct' = γ(ct − βx)`, `x' = γ(x − βct)` — same as `RE-03`.

## The one idea
Demote **time**, not the speed of light. Holding the principle of relativity
*and* a frame-independent `c` is impossible while keeping a universal "now": the
casualty is **absolute simultaneity**. Time dilation, length contraction and the
whole Lorentz transformation then *follow* — they are consequences of the
postulates, not extra assumptions. This module shows the two cleanest
derivations: the **light clock** turns constant `c` into `γ` (one Pythagorean
triangle), and the **radar / Bondi method** coordinatizes spacetime with only a
clock and light echoes (`k = √((1+β)/(1−β))`).

## Operations — `code/postulates.py`
| call | meaning |
|------|---------|
| `gamma(beta)` | Lorentz factor `1/√(1−β²)` (derived, not assumed, by the light clock) |
| `bondi_k(beta)` | Bondi / Doppler factor `k = √((1+β)/(1−β))` |
| `beta_from_k(k)` | velocity from a measured factor: `β = (k²−1)/(k²+1)` |
| `radar_coordinates(t_send, t_echo)` | radar/Einstein coords `((t_s+t_e)/2, (t_e−t_s)/2)` |
| `light_clock_gamma(beta, gap=1.0)` | **derive** `γ` from the transverse light-clock triangle |
| `leading_clocks_lag(beta, L)` | rest-synced clocks offset by `βL` — "leading clocks lag" |
| `simultaneity_breakdown(beta, dt, dx)` | `Δt′ = γ(Δt − βΔx)` — when "now" splits |

## Use
```python
from postulates import bondi_k, beta_from_k, radar_coordinates, light_clock_gamma, simultaneity_breakdown

bondi_k(0.6)                              # 2.0     (Doppler factor; redshift)
beta_from_k(bondi_k(0.6))                 # 0.6     (clean inverse)
radar_coordinates(5 - 3, 5 + 3)           # (5.0, 3.0)   recovers an event at (t=5, x=3)
light_clock_gamma(0.6) == 1/(1-0.6**2)**0.5   # True   (γ DERIVED from constant c)
simultaneity_breakdown(0.6, 0.0, 2.0)     # -1.5    simultaneous in S, not in S'
```

## Run
```bash
cd code
python3 postulates.py            # demo: Doppler/k table, radar method, light-clock γ, simultaneity
python3 test_postulates.py       # 9 property-based tests -> "All 9 tests passed."
```

## Files
- `notes.md` — postulates, Galileo-vs-Maxwell, synchronization, simultaneity, k-calculus, light clock
- `code/postulates.py` — the library (pure stdlib; coordinates are plain tuples)
- `code/test_postulates.py` — Bondi reciprocity/inversion, radar↔k² consistency, geometric `γ`, simultaneity
- `problems/problems.md` — worked problems (Griffiths Ch.12, Zee III)
- `refs.md` — verified textbook citations
