# PK-01 — Kinetic Description — Distribution Functions, Vlasov & Boltzmann

First module of the **PLASMA & KINETIC THEORY** trunk (see `modules/topic_network.txt`).
It underlies the KrF/LoKI plasma-kinetics code in this repo (`Kinetic_Modeling/KrF_and_LoKI`)
and is the phase-space face of **KEY BRIDGE B2** (continuity) and **B10** (the stat-mech → kinetic → fluid ladder).

- **Prerequisites:** `~SM-06` (the Maxwell–Boltzmann distribution and the Boltzmann transport
  equation), `~MA-19` (probability distributions & moments).
- **Cross-links:** `~CM-22` (continuity of mass / phase space), `~QM-04` (continuity of
  probability — the same residual check), `~PK-02` (velocity moments → fluid/MHD equations),
  `~PK-03` (plasma waves & Landau damping), `~PK-04` (excimer rate kinetics / EEDF — the KrF code).

## Scope
A plasma has far too many particles to follow one by one, yet is too **collisionless** for plain
thermodynamics. The kinetic description tracks one smooth field: the **one-particle distribution
function** f(x,v,t), the number of particles per unit phase-space volume, dN = f d³x d³v. Its
**velocity moments** are the fluid quantities — number density n = ∫f d³v, mean velocity
**u** = (1/n)∫**v**f d³v, and pressure p = (m/3)∫|**v**−**u**|²f d³v — and in equilibrium f is the
**Maxwellian**. Its evolution is the **Boltzmann equation** ∂f/∂t + **v**·∇ₓf + (**F**/m)·∇ᵥf =
(∂f/∂t)_coll; dropping the collision term and letting **F** be the **self-consistent mean field**
(Lorentz force from the smoothed charge/current of f, closed by Maxwell) gives the **Vlasov
equation**. Because the phase-space flow is incompressible, Vlasov is nothing but the **continuity
equation for phase-space density**, df/dt = 0 along orbits — **Liouville's theorem**, the very law
that conserves mass (`~CM-22`) and probability (`~QM-04`). The collective scales decide when this
mean-field picture holds: the **Debye length** λ_D = √(ε₀kT/nq²) (screening), the **plasma
frequency** ω_p = √(nq²/ε₀m) (the fastest collective rate, with λ_D = v_T/ω_p), and the **plasma
parameter** Λ = nλ_D³, the number of particles in a Debye sphere. Λ ≫ 1 means weak coupling and
collective behaviour — collisions are a slow correction (ν_ei/ω_p ∼ lnΛ/Λ ≪ 1), and the Vlasov
equation is the right leading description. The collision term, restored, becomes the excimer rate
chemistry of `~PK-04` and the KrF/LoKI simulator.

## Operations — `code/kinetic_description.py`

| call | meaning | reference |
|------|---------|-----------|
| `maxwellian(v, n, T, m)` | f(v) = n(m/2πk_BT)^{3/2} e^{−mv²/2k_BT}, with ∫f d³v = n | Mi §1.2.3 |
| `thermal_speed(T, m)` | v_T = √(k_BT/m) (per-component rms velocity) | Mi A.1 (A.4) |
| `plasma_frequency(n, q, m)` | ω_p = √(nq²/ε₀m) | Mi §1.2.2; A.1 (A.1) |
| `debye_length(n, T, q)` | λ_D = √(ε₀k_BT/nq²) | Mi §1.2.1; A.1 (A.6) |
| `plasma_parameter(n, T)` | Λ = nλ_D³ (particles in a Debye sphere) | Mi §1.2.1; A.1 (A.8) |
| `free_stream(f0, x, v, dt)` | advect f₁(x,v) = f₀(x − v dt, v) (exact spectral shift) | Mi §1.2.4.1 |
| `vlasov_residual(f0, f1, x, v, dt)` | ∂ₜf + v∂ₓf across one step (≈ 0) | Mi §1.2.4.1 |

Constants (re-exported, SI): `K_B`, `EPS0`, `M_E`, `E_CHARGE`.

## Use
```python
from kinetic_description import (debye_length, plasma_frequency, plasma_parameter,
                                 thermal_speed, M_E, E_CHARGE, K_B)

n = 1e18                       # number density [m^-3]
T = 1.0 * E_CHARGE / K_B       # 1 eV expressed in kelvin (11604.5 K)

plasma_frequency(n)            # 5.64e10 rad/s   (f_p ~ 9 GHz)
debye_length(n, T)             # 7.43e-6 m
debye_length(n, T), thermal_speed(T, M_E) / plasma_frequency(n)   # equal: lambda_D = v_T/omega_p
plasma_parameter(n, T)         # 411  >> 1  -> weakly coupled, collective (mean-field Vlasov holds)
```

## Run
```bash
cd code
python3 kinetic_description.py        # demo: plasma parameters; Maxwellian moments; phase-space continuity
python3 test_kinetic_description.py   # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — distribution function & moments, Boltzmann/Vlasov, Liouville (B2), Debye/ω_p/Λ
- `code/kinetic_description.py`, `code/test_kinetic_description.py`
- `problems/problems.md` — worked problems (Michel §1.2; Rhodes Ch.4/§7.2; Pathria §6.4)
- `refs.md` — citation table (Michel §1.2 & Appendix A.1; Rhodes; cross-shelf Pathria)
