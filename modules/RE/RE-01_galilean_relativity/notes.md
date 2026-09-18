# RE-01 — Galilean Relativity & Its Failure (notes)

## 1. The Galilean transformation (from CM-03)
Two inertial frames S, S′ with S′ moving at constant velocity **V**, origins
coincident at `t=0`. The pre-relativistic relation between coordinates is the
**Galilean transformation**
$$\mathbf r' = \mathbf r - \mathbf V t,\qquad t' = t,$$
with **absolute time** built in (`t'=t`). Differentiating: velocities **add**,
`v' = v − V` (`galilean_velocity`, CM-03), and accelerations are **unchanged**,
`a' = a`. The principle of **Galilean relativity**: the laws of mechanics take the
same form in every inertial frame — Newton's `F = ma` is invariant because both
`m` and `a` are.

## 2. Newton is happy, Maxwell is not
Galilean invariance is exact for mechanics. But **Maxwell's equations** predict
electromagnetic waves at a definite speed
$$c = \frac{1}{\sqrt{\varepsilon_0\mu_0}},$$
a constant built from lab measurements with **no reference to any frame**. Under a
Galilean boost, a wave at `c` in S would move at `c − V` in S′
(`light_speed_galilean`). So either:
- Maxwell's equations hold in only **one** special frame — the **luminiferous
  ether**, the medium light waves ride — and Galilean relativity fails for
  electromagnetism; or
- the speed of light really is the same in every frame, and **Galilean kinematics
  is wrong**.

The 19th century bet on the ether. The job became: detect Earth's motion through
it.

## 3. The Michelson–Morley experiment (1887)
Earth orbits the Sun at `v ≈ 30 km/s`, so it should feel an **ether wind**.
Michelson's interferometer splits light down two perpendicular arms of length `L`
and recombines them. Riding the wind, the round-trip times differ:
$$t_\parallel = \frac{2L/c}{1-v^2/c^2},\qquad
  t_\perp = \frac{2L/c}{\sqrt{1-v^2/c^2}},\qquad
  \Delta t = t_\parallel - t_\perp \approx \frac{L}{c}\frac{v^2}{c^2}$$
(`ether_wind_dt`). Rotating the apparatus 90° swaps the arms, doubling the path
difference, so the **fringe pattern should shift** by
$$\boxed{\;\Delta N = \frac{2L}{\lambda}\left(\frac{v}{c}\right)^2\;}$$
(`michelson_morley_shift`). For the real apparatus (`L≈11 m` via multiple
reflections, `λ≈500 nm`, `v≈30 km/s`) this is `ΔN ≈ 0.4` fringe — well within the
resolution. **The observed shift was essentially zero.** No ether wind. Light
travels at `c` regardless of Earth's motion.

Note the effect is **second order** in `v/c` (`∼10⁻⁸`); that smallness is why it
took an interferometer to test, and why everyday mechanics never noticed.

## 4. The patches — and the real fix
- **FitzGerald–Lorentz contraction.** If bodies moving through the ether shrank
  by `√(1−v²/c²)` along the motion, `t_∥` would match `t_⊥` and the null result is
  "explained." But this was an *ad hoc* rescue with no independent justification —
  a fudge to save the ether.
- **Einstein (1905).** Take the constancy of `c` as a **postulate** (RE-02) and
  rebuild kinematics. Time is no longer absolute; the Galilean transformation is
  replaced by the **Lorentz transformation** (RE-03). The "contraction" then falls
  out as real geometry (RE-04), not a patch.

## 5. Galilean relativity as the `c → ∞` limit
SR does not discard Galilean physics — it contains it. The Lorentz boost reduces
to the Galilean one as `c → ∞` (equivalently `v/c → 0`), and Einstein's
velocity-addition rule
$$w = \frac{u+v}{1+uv/c^2}\ \xrightarrow{\,c\to\infty\,}\ u+v$$
(`relativistic_velocity_add → galilean_velocity_add`; the gap
`galilean_limit_error ∝ 1/c²` — `test_relativistic_reduces_to_galilean…`). So
Galilean relativity is the **low-speed shadow** of special relativity: correct
whenever `v ≪ c`, which is why Newton works and why the failure only shows up for
light. This module imports both — CM-03's Galilean boost and RE-03's Lorentz
machinery — and measures exactly how the first emerges from the second.
