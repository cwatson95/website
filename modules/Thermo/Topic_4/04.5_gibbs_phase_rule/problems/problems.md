# 4.5 — Problems

Check with `code/gibbs_phase_rule.py`. Citations in `../refs.md`. `N`=components,
`P`=phases, `F`=degrees of freedom.

### P1.  Apply the phase rule  *(Moran 8e Eq. 14.68, p.913)*
Find `F` for: (a) water vapor, (b) a liquid solution of water + ammonia, (c) water
vapor coexisting with ice.
*Answer:* (a) `N=1,P=1 → F=2`; (b) `N=2,P=1 → F=3`; (c) `N=1,P=2 → F=1`. *Check:*
`gibbs_phase_rule(1,1)`=2; `gibbs_phase_rule(2,1)`=3; `gibbs_phase_rule(1,2)`=1.

### P2.  Why a pure substance needs quality in the dome  *(Moran 8e Eq. 14.69, p.913)*
Use the phase rule to explain why specifying the temperature of a wet steam mixture
does not fix its state.
*Answer:* pure substance, two phases ⇒ `F = 3 − P = 3 − 2 = 1`. Only **one** intensive
property is free; along the saturation line `T` fixes `p`, so a *second* property —
the quality `x` — is required (module `4.4`). *Check:* `single_component_dof(2)` = 1.

### P3.  The triple point and the phase limit  *(Moran 8e §14.6.2, p.914)*
How many degrees of freedom has a pure substance at its triple point? What is the most
phases that can coexist?
*Answer:* `F = 3 − 3 = 0` — the triple point is fully fixed (no freedom). The maximum
is `P = N + 2 = 3` phases for a pure substance. *Check:* `single_component_dof(3)` = 0;
`max_phases(1)` = 3.

### P4.  Binary mixtures (Moran review Q23/Q24)  *(Moran 8e §14.6.2, p.916)*
Find `F` for (a) an ammonia–water liquid solution in equilibrium with an ammonia–water
vapor mixture, and (b) a liquid solution of water + lithium bromide.
*Answer:* (a) `N=2,P=2 → F=2`; (b) `N=2,P=1 → F=3`. *Check:* `gibbs_phase_rule(2,2)`=2;
`gibbs_phase_rule(2,1)`=3.
