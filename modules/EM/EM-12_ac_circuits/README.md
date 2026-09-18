# EM-12 — AC Circuits & Driven RLC

Twelfth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-11` (electromagnetic induction — the EMF and inductance of
  the very elements driven here), `~MA-05` / `~MA-06` (complex numbers and the
  e^{iωt} method).
- **Cross-link:** `~CM-15` (the driven, damped oscillator — resonance and Q). The series
  RLC is its term-for-term **electrical twin**; this is the EM end of **KEY BRIDGE B6**
  (the oscillator).
- **Feeds into:** `~EM-16` (transmission lines reuse impedance; microwave cavities reuse
  resonance and Q), `~EM-15` (the same phasor ansatz e^{i(kz−ωt)}, and a wave's E/H ratio
  is an impedance), and `~EM-13` (the displacement current is what lets a capacitor
  "carry" the AC current).

## Scope
Take the induction physics of `~EM-11` — a resistor, an inductor (EMF = −L dI/dt) and a
capacitor — and **drive the loop sinusoidally** at angular frequency ω. Writing the drive
as the real part of a phasor V₀e^{iωt} and seeking a current ∝ e^{iωt} turns every element
into a complex **impedance** obeying a phasor Ohm's law **V = IZ**:
Z_R = R, Z_L = iωL, Z_C = 1/(iωC). For a **series RLC** the impedances add,
Z = R + i(ωL − 1/ωC); the reactance cancels at the **resonant frequency** ω₀ = 1/√(LC),
where Z = R is purely resistive, the current peaks at V₀/R and runs **in phase** with the
drive. How sharp that peak is — the **quality factor** — is Q = ω₀L/R = (1/R)√(L/C).

Everything here is the **electrical twin of the `~CM-15` driven oscillator**: the loop
equation L q'' + R q' + q/C = V₀ cos ωt is, term for term, the driven damped oscillator
m x'' + b x' + k x = F₀ cos ωt (**KEY BRIDGE B6**). The steady-state solver is the
`~MA-05`/`~MA-06` complex exponential. AC circuit theory is **not** a numbered Griffiths
section — he develops it in the Ch. 7 *problems* on top of §7.1–7.2 (EMF and inductance) —
so `refs.md` gives the honest citation picture.

## Operations — `code/ac_circuits.py`

| call | meaning | reference |
|------|---------|-----------|
| `impedance_resistor(R)` | Z_R = R (real; current in phase) | Gr §7.1.2 p303 |
| `impedance_inductor(L, omega)` | Z_L = iωL (voltage leads current 90°) | Gr §7.2.3 p321 |
| `impedance_capacitor(C, omega)` | Z_C = 1/(iωC) = −i/ωC (current leads) | complex method, `~MA-05` |
| `impedance_series(*Zs)` | series combination: impedances add | `~MA-05` / Boas Ch. 2 |
| `impedance_parallel(*Zs)` | parallel combination: reciprocals add | `~MA-05` / Boas Ch. 2 |
| `series_rlc_impedance(R, L, C, omega)` | Z = R + i(ωL − 1/ωC) | complex method; `~CM-15` |
| `resonant_frequency(L, C)` | ω₀ = 1/√(LC) | `~CM-15` resonance |
| `quality_factor(R, L, C)` | Q = ω₀L/R = (1/R)√(L/C) | `~CM-15` Q-factor |
| `bandwidth(R, L)` | Δω = R/L = ω₀/Q (half-power width) | `~CM-15` |
| `current_amplitude(V0, Z)` | \|I\| = V₀/\|Z\| (phasor Ohm's law) | `~MA-05` |
| `current_phase(Z)` | φ = −arg Z (+ leads / − lags) | `~MA-05` |
| `average_power(V0, Z)` | ⟨P⟩ = ½\|I\|²R = ½V₀² ReZ/\|Z\|² | `~CM-15` |

Impedances are returned as Python `complex` (the phasor Ohm's law V = IZ). The module is
**self-contained on the standard-library `cmath`/`math`** — no `~MA` imports. Because AC
steady-state theory is not a numbered Griffiths section, the resistor/inductor rows cite
the underlying EMF/inductance physics (§7.1.2 p303, §7.2.3 p321) and impedance/resonance
follow the complex-exponential method (`~MA-05`/`~MA-06`, Boas Ch. 2) plus the `~CM-15`
analogy; see `refs.md`.

## Use
```python
import math
from ac_circuits import (series_rlc_impedance, resonant_frequency, quality_factor,
                         current_amplitude, current_phase, average_power)

R, L, C, V0 = 10.0, 1e-3, 1e-6, 5.0
w0 = resonant_frequency(L, C)                 # 1/sqrt(LC) ~ 3.162e4 rad/s
quality_factor(R, L, C)                       # Q = (1/R)sqrt(L/C) ~ 3.162

Z = series_rlc_impedance(R, L, C, w0)         # (10+0j): purely resistive at resonance
current_amplitude(V0, Z)                      # |I| = V0/R = 0.5 A   (peak current)
current_phase(Z)                              # 0.0 rad: current in phase with drive
average_power(V0, Z)                          # <P> = V0^2/2R = 1.25 W  (peak power)

Zlo = series_rlc_impedance(R, L, C, 0.5 * w0) # below resonance: net capacitive
math.degrees(current_phase(Zlo))              # ~ +78 deg: the current leads the voltage
```

## Run
```bash
cd code
python3 ac_circuits.py          # demo: RLC resonance, sweep w/w0 in {0.5, 0.9, 1.0, 1.1, 2.0}
python3 test_ac_circuits.py     # tests  ->  "All 7 tests passed."
```
(`ac_circuits.py` is self-contained on the standard-library `cmath`/`math` — no
cross-module imports — so it runs anywhere.)

## Files
- `notes.md` — derivations with inline citations (and the `~CM-15` dictionary)
- `code/ac_circuits.py`, `code/test_ac_circuits.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 7 / `~CM-15` analogy)
- `refs.md` — citation table (edition, section, **printed + PDF page**) and the honest
  "not a numbered section" caveat
