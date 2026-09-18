# CM-07 — Centre of Mass (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)*.

## Centre of mass
The mass-weighted average position of a system [F §7.1 p.275; G §1.2 p.5]:
$$\mathbf R=\frac{\sum_i m_i\mathbf r_i}{\sum_i m_i},\qquad
  \mathbf V=\dot{\mathbf R}=\frac{\sum_i m_i\mathbf v_i}{\sum_i m_i}.$$
The total momentum is **P** = M**V** with M = Σmᵢ, so the CM moves as a single
particle of mass M driven by the external force — internal forces never move it.
Code: `centre_of_mass`, `cm_velocity`.

## Reduced mass
A two-body problem separates into the (free) CM motion plus the **relative motion**
**r** = **r₁** − **r₂**, which obeys a one-body equation with the **reduced mass**
[F §7.3 p.283]:
$$\mu=\frac{m_1 m_2}{m_1+m_2}.$$
Limits: equal masses give μ = m/2; a very heavy partner gives μ → the lighter mass
(a test). Code: `reduced_mass`, `relative_coordinate`, `two_body_decompose`. This
decomposition is what turns the Kepler/central-force problem into a single
effective particle in `~CM-11`.
