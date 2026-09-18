# PK-02 — Fluid & MHD Description — Moments, Continuity & Momentum

Second module of the **PLASMA & KINETIC THEORY** trunk (see `modules/topic_network.txt`).
This carries **KEY BRIDGE B2** into plasmas: the $0^\text{th}$ velocity moment of the
kinetic equation is the *same* continuity law as mass (`~CM-22`), and it ties to the
KrF/LoKI plasma-kinetics code in `Kinetic_Modeling/KrF_and_LoKI`.

- **Prerequisites:** `~PK-01` (the distribution function $f$ and the Vlasov/Boltzmann
  equation the moments are taken of), `~SM-06` (the same moment idea for a neutral gas).
- **Cross-links:** `~CM-22` (mass continuity — identical law, KEY BRIDGE B2), `~CM-23`
  (the neutral Euler/Navier–Stokes fluid limit), `~EM-13` (Maxwell's equations &
  Faraday's law for the induction equation), `~PK-03` (waves & instabilities from
  these fluid equations).

## Scope
A plasma is either followed kinetically (the distribution function $f$ of `~PK-01`) or
described as a **fluid** of smooth fields. The bridge is **taking velocity moments** of
the Vlasov/Boltzmann equation: integrating against $1,\mathbf v,\mathbf{vv},\dots$
collapses phase space onto $n$, $\mathbf u$ and the pressure $\mathsf P$. The
$0^\text{th}$ moment is the **continuity equation** ∂n/∂t + ∇·(n**u**) = 0 — the same
local conservation law as mass, charge and probability (KEY BRIDGE B2); the
$1^\text{st}$ moment is the **momentum equation** m n(∂**u**/∂t + **u**·∇**u**) =
−∇·**P** + qn(**E**+**u**×**B**). The hierarchy is never closed (each moment needs the
next — the **closure problem**), so one truncates with a polytropic equation of state
p = Cρ^γ. Summing the two-fluid equations under quasineutrality gives **ideal MHD**:
ρ D**u**/Dt = −∇p + **J**×**B**, the ideal Ohm's law **E**+**u**×**B** = 0, and the
induction equation ∂**B**/∂t = ∇×(**u**×**B**) with its **frozen-in flux**. Three
characteristic speeds organize the dynamics — sound c_s = √(γp/ρ), Alfvén
v_A = B/√(μ₀ρ), and fast magnetosonic √(c_s²+v_A²) — and the ratio of thermal to
magnetic pressure, the **plasma β** = p/(B²/2μ₀), says whether the field or the gas is
in charge. The code recovers (n, **u**, nk_BT) from a drifting Maxwellian by numerical
moment integration, then evaluates all the speeds and β for a magnetized plasma.

## Operations — `code/fluid_mhd.py`

| call | meaning | reference |
|------|---------|-----------|
| `moments_of_maxwellian(n, u, T, m)` | velocity moments → (n, **u**, p = nk_BT) | Mi §1.2.3–1.2.4.2 |
| `continuity_residual(rho0, rho1, u, dx, dt)` | ∂ρ/∂t + ∂ₓ(ρu) (0th moment; ≈0) | Mi Eq. 1.63; `~CM-22` |
| `sound_speed(gamma, p, rho)` | c_s = √(γp/ρ) | Mi §1.2.4.2, §1.3.2 |
| `alfven_speed(B, rho, mu0=MU0)` | v_A = B/√(μ₀ρ) | Mi Ch.1 (std. MHD) |
| `fast_magnetosonic_speed(c_s, v_A)` | √(c_s²+v_A²), **k**⊥**B** | Mi Ch.1 (std. MHD) |
| `magnetic_pressure(B, mu0=MU0)` | P_B = B²/2μ₀ | Mi Ch.1 (std. MHD) |
| `plasma_beta(n, T, B)` | β = nk_BT/(B²/2μ₀) | Mi Ch.1 (std. MHD) |

Constants (SI, local): `MU0`, `K_B`, `M_P`, `M_E`.

## Use
```python
from fluid_mhd import (moments_of_maxwellian, sound_speed, alfven_speed,
                       plasma_beta, magnetic_pressure, K_B, M_P)

# moments of a drifting Maxwellian recover the fluid fields
n_rec, u_rec, p_rec = moments_of_maxwellian(1e19, (1e5, 0, 0), 1e5, M_P)
p_rec, 1e19 * K_B * 1e5            # 13.8 Pa  ==  n k_B T   (2nd moment)

# a representative magnetized plasma (n=1e19, T~100 eV, B=1 T)
rho = 1e19 * M_P
sound_speed(5/3, 1e19*K_B*1.16e6, rho)   # ~1.26e5 m/s
alfven_speed(1.0, rho)                   # ~6.9e6 m/s  (c_s << v_A)
plasma_beta(1e19, 1.16e6, 1.0)           # ~4e-4  -> magnetically dominated
```

## Run
```bash
cd code
python3 fluid_mhd.py          # demo: moments recover (n,u,nkT); speeds, magnetic pressure, beta; continuity
python3 test_fluid_mhd.py     # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — moments → continuity & momentum, closure, ideal MHD, speeds, plasma β (10 display equations)
- `code/fluid_mhd.py`, `code/test_fluid_mhd.py`
- `problems/problems.md` — worked problems (Michel Ch.1; Rhodes excimer cross-link)
- `refs.md` — citation table (Michel primary, Rhodes cross-cite) + cross-links
