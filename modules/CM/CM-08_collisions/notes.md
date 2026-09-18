# CM-08 — Collisions & Scattering (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)* · **MT** = Marion & Thornton 5e *(image scan)*.

## Collisions
Every collision conserves total **momentum** (`~CM-06`). They split by what
happens to **kinetic energy** [F §7.5 p.303; MT §9.6 p.345]:
- **Elastic** — kinetic energy is conserved. In 1-D,
  $$v_1'=\frac{(m_1-m_2)v_1+2m_2 v_2}{m_1+m_2},\quad
    v_2'=\frac{(m_2-m_1)v_2+2m_1 v_1}{m_1+m_2}.$$
  Equal masses **exchange** velocities; a light ball off a massive wall reverses
  (tests).
- **Perfectly inelastic** — the bodies stick; the common velocity is exactly the
  **centre-of-mass velocity** (`~CM-07`), and kinetic energy is lost [MT §9.8 p.358].

Collisions are cleanest in the **C-frame** (`~CM-03`), where the total momentum is
zero [F §7.6 p.306].

## Rutherford scattering
A repulsive 1/r² (Coulomb) force deflects an incoming particle by an angle set by
its **impact parameter** b and energy E [F §6.14 p.264]:
$$\theta=2\arctan\!\frac{k}{2Eb}\quad\Longleftrightarrow\quad b=\frac{k}{2E}\cot\frac\theta2.$$
The **differential cross-section** is the famous result [G §3.10 p.110; MT §9.10 p.369]
$$\frac{d\sigma}{d\Omega}=\Big(\frac{k}{4E}\Big)^2\frac{1}{\sin^4(\theta/2)},$$
which diverges in the forward direction (θ → 0) because the Coulomb force has
infinite range (tests). Code: `rutherford_angle`, `rutherford_cross_section`.
Rutherford's analysis of this curve revealed the atomic nucleus; its quantum
cousin is `~QM-18`.
