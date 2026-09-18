# CM-14 — Euler's Equations (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## Euler's equations
Because **L** = I**ω** with a *fixed* tensor only in the body frame, the
rotational equation of motion d**L**/dt = **N** (`~CM-09`), rewritten in the
rotating principal-axis frame, becomes **Euler's equations** [F §9.3 p.381;
MT §11.9 p.444]:
$$I_1\dot\omega_1=(I_2-I_3)\omega_2\omega_3+N_1,\quad\text{(and cyclic)}.$$
Code: `euler_rhs`, `integrate_euler`. The coupling term (I₂−I₃)ω₂ω₃ is why an
asymmetric body tumbles.

## Torque-free motion
With **N** = 0 [F §9.4 p.383], two quantities are conserved (tests):
$$|\mathbf L|^2=\sum_i (I_i\omega_i)^2,\qquad T=\tfrac12\sum_i I_i\omega_i^2.$$
- **Steady spin:** rotation about any single principal axis is a fixed point
  (the coupling term vanishes) — stable about the largest and smallest moments,
  unstable about the intermediate one (the tennis-racket theorem).
- **Symmetric top** (I₁ = I₂): ω₃ is constant and (ω₁, ω₂) rotate at the
  **free-precession rate** Ω = (I₃−I₁)/I₁ · ω₃ [F §9.5 p.384] — code
  `precession_rate`; the test confirms ω₃ and ω₁²+ω₂² stay constant.
