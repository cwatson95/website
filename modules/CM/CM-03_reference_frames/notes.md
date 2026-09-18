# CM-03 — Reference Frames (notes)

Citation key (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e.

## Inertial frames and the Galilean transformation
An **inertial frame** is one in which a free particle moves at constant velocity
(Newton's 1st law). Two inertial frames differ by a constant relative velocity
**V**; with coincident origins at t = 0 [F §5.1 p.184]:
$$\mathbf r'=\mathbf r-\mathbf V t,\qquad \mathbf v'=\mathbf v-\mathbf V,\qquad
  \mathbf a'=\mathbf a,\qquad t'=t.$$
Acceleration — and therefore **F** = m**a** — is the same in every inertial frame
(Galilean invariance). Relative velocities are likewise frame-independent
(a test). Fowles names this "Galilean relativity" [F §2.1 p.54]; it is exactly
what special relativity `~RE-01` replaces at high speed.

## The centre-of-mass (C) frame
A specially useful inertial frame moves with the centre of mass [F §7.1 p.275]:
$$\mathbf V_{\rm cm}=\frac{\sum_i m_i\mathbf v_i}{\sum_i m_i}.$$
Boosting to it (`to_cm_frame`) makes the **total momentum vanish** — the defining
property, and why collisions are simplest there [F §7.6 p.306] (`~CM-08`). Code:
`cm_velocity`, `to_cm_frame`; the test confirms ΣP = 0 in the C-frame.

*(Non-inertial / rotating frames, where fictitious forces appear, are `~CM-12`;
Fowles §5.2 p.189.)*
