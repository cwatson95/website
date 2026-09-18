# EM-17 — Radiation

Penultimate module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the Coulomb field and `EPS0`, `K_E` = 1/4πε₀),
  `~EM-08` (magnetostatics — supplies `MU0`, hence `c` = 1/√(μ₀ε₀), and the vector
  potential **A**), `~MA-01` (vector algebra — `norm`, `unit`, `dot`).
- **Feeds-into:** `~EM-18` (relativistic electrodynamics — the covariant fields of a
  moving charge generalize the Liénard-Wiechert result), and cross-trunk `~QO-03`
  (spontaneous/stimulated emission & laser physics rest on this dipole-radiation
  picture). Related: `~MA-14` (the retarded potential is a Green's-function /
  retarded-propagator solution of the wave equation) and `~EM-05` (the oscillating
  electric **dipole** is what radiates in §11.1).

## Scope
The first **time-dependent** fields of the trunk. News of a source travels at the
finite speed `c`, so the potentials at **r** depend on the state of the source at the
**retarded time** $t_r = t - \eta/c$ — one light-travel-time `η/c` in the past. Feed a
*moving* point charge through that delay and the potentials become the **Liénard-Wiechert
potentials** (Eq. 10.46–10.47), with a $1/(1-\hat{\boldsymbol\eta}\cdot\mathbf v/c)$
"beaming" enhancement. Differentiate them and you find that **accelerating charges
radiate**: the **Larmor formula** $P=\mu_0 q^2 a^2/(6\pi c)$ (Eq. 11.70) for a slow
charge, and **electric-dipole radiation** with the $\sin^2\theta$ doughnut pattern and
total time-averaged power $\langle P\rangle=\mu_0 p_0^2\omega^4/(12\pi c)$ (Eq. 11.22).
The retarded potential is itself a **Green's-function** solution of the wave equation
(`~MA-14`); the radiating dipole is the `~EM-05` dipole set oscillating. SI units throughout;
a trajectory is supplied as a function `w(t) -> (x,y,z)`, a velocity as `v(t) -> (vx,vy,vz)`.

## Operations — `code/radiation.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `retarded_time(field_point, trajectory, t)` | solve $t_r = t - \eta(t_r)/c$ for a source on trajectory **w**(·) | Gr §10.2.1 Eq.10.19 p.444 |
| `retarded_potential_static(q, source, field_point, t)` | static charge: $V=q/4\pi\varepsilon_0\eta$, tagged with $t_r=t-\eta/c$ | Gr §10.2.1 Eq.10.26 p.444 |
| `lienard_wiechert(q, trajectory, velocity, field_point, t)` | $(V,\mathbf A,t_r)$ of a moving point charge | Gr §10.3.1 Eq.10.46–10.47 p.451 |
| `larmor_power(q, a)` | $P=\mu_0 q^2 a^2/6\pi c$, a slow accelerating charge | Gr §11.2.1 Eq.11.70 p.484 |
| `dipole_radiated_power(p0, omega)` | $\langle P\rangle=\mu_0 p_0^2\omega^4/12\pi c$ | Gr §11.1.2 Eq.11.22 p.467 |
| `dipole_angular_power(theta, p0, omega)` | $dP/d\Omega=(\mu_0 p_0^2\omega^4/32\pi^2 c)\sin^2\theta$ | Gr §11.1.2 Eq.11.21 p.467 |
| `total_power_from_pattern(p0, omega)` | $\oint (dP/d\Omega)\,d\Omega$ → recovers $\langle P\rangle$ | Gr §11.1.2 Eq.11.22 p.467 |

Constants: `C` = 1/√(μ₀ε₀) ≈ 2.998×10⁸ m/s, the speed of light, built from `EPS0`
(`~EM-01`) and `MU0` (`~EM-08`); `K_E` = 1/4πε₀. Here **η** = (field point) − (source
position **at** $t_r$) is Griffiths' "script-r" separation, **η̂** = **η**/η its direction.

## Use
```python
from radiation import (retarded_potential_static, lienard_wiechert, larmor_power,
                       dipole_radiated_power, dipole_angular_power,
                       total_power_from_pattern, C)
import math

# static charge: the retarded potential is just Coulomb's, tagged with t_r = t - r/c
retarded_potential_static(1e-9, (0,0,0), (3,0,0), t=10.0)    # ~ (3.0 V, 9.99999999 s)

# a point charge gliding at 0.6c straight at the field point -> potential is "beamed" up
traj = lambda tt: (0.6*C*tt, 0, 0)
vel  = lambda tt: (0.6*C, 0, 0)
V, A, t_r = lienard_wiechert(1e-9, traj, vel, (10,0,0), t=0.0)   # V > Coulomb, |A| != 0

larmor_power(1.602e-19, 1e22)             # accelerating electron radiates ~5.7e-10 W (P ~ a^2)

# oscillating dipole: closed form vs. the integral of the sin^2 angular pattern
w = 2*math.pi*1e8                          # 100 MHz
dipole_radiated_power(1e-11, w)            # <P> = mu0 p0^2 w^4 / (12 pi c)
total_power_from_pattern(1e-11, w)         # same number to <0.1% (integral of dP/dOmega)
dipole_angular_power(math.pi/2, 1e-11, w)  # broadside maximum; exactly 0 on the axis
```

## Run
```bash
cd code
python3 radiation.py          # demo: retarded potential, LW beaming, Larmor, dipole pattern
python3 test_radiation.py     # tests  ->  "All 7 tests passed."
```
(`radiation.py` puts the EM-01 and EM-08 `code/` dirs on `sys.path`; MA-01's
`vector_algebra` rides along via EM-01. This becomes `from physkit… import …` once
the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/radiation.py`, `code/test_radiation.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 10–11)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
