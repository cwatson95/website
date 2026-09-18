# CM-04 — Problems

Work by hand, then check with `code/work_energy.py`. Citations in `../refs.md`.

### P1.  Work of a constant force  *(Fowles 7e §4.1, p.145)*
Show that for a constant force the work is W = **F**·**d** (displacement), path
detail irrelevant. *Check:* `work(lambda x,y,z:F, straight_path, 0, 1)`.

**Solution.** For a constant force $\mathbf F$ the work integral factors out the force, leaving only the net displacement:
$$W=\int_C\mathbf F\cdot d\mathbf l=\mathbf F\cdot\int_C d\mathbf l=\mathbf F\cdot(\mathbf b-\mathbf a)=\mathbf F\cdot\mathbf d.$$
Because only the endpoints $\mathbf a,\mathbf b$ enter, the path taken between them is irrelevant. With $\mathbf F=(2,0,0)$ pushed straight from the origin to $(5,0,0)$, $W=2\times5=10$ J, exactly what `work(lambda x,y,z:F, straight_path, 0, 1)` returns.

### P2.  The work–energy theorem  *(Fowles 7e §4.1, p.145)*
For a particle from rest under a constant force, integrate the work along its
actual path and show it equals ΔT = ½mv². *Check:* compare `work(...)` to
`kinetic_energy(m, vT)`.

**Solution.** Newton's law $\mathbf F=m\,d\mathbf v/dt$ dotted with $d\mathbf l=\mathbf v\,dt$ turns the integrand into a perfect differential:
$$\mathbf F\cdot d\mathbf l=m\,\mathbf v\cdot d\mathbf v=d\big(\tfrac12 m|\mathbf v|^2\big)\ \Longrightarrow\ W=\int_{\mathbf a}^{\mathbf b}\mathbf F\cdot d\mathbf l=\tfrac12 m v_b^2-\tfrac12 m v_a^2=\Delta T.$$
Starting from rest ($v_a=0$), $W=\tfrac12 m v^2$. With $F_0=3,\ m=2$ the acceleration is $a=F_0/m=1.5$, so after $T=2$ the speed is $v=aT=3$; integrating the work gives $W=9.000$, equal to $\tfrac12 m v^2=\tfrac12(2)(3^2)=9$ from `kinetic_energy(m, vT)`.

### P3.  Work of gravity  *(Marion & Thornton 5e §2.6, p.82)*
Show that lowering a mass m by height h releases W = mgh, independent of the path.
*Check:* `work(lambda x,y,z:(0,0,-m*g), drop_path, 0, 1)` ≈ mgh.

**Solution.** Take constant gravity $\mathbf F=(0,0,-mg)$ and lower the mass from $z=0$ to $z=-h$, a displacement $\mathbf d=(0,0,-h)$ (plus any horizontal wandering). Since $\mathbf F$ is constant the work is path-independent (P1):
$$W=\mathbf F\cdot\mathbf d=(0,0,-mg)\cdot(0,0,-h)=mgh,$$
and horizontal motion contributes nothing because $\mathbf F$ has no $x,y$ component. For $m=3,\ g=9.81,\ h=4$ this gives $W=mgh=117.72$ J, matching `work(lambda x,y,z:(0,0,-m*g), drop_path, 0, 1)`.

### P4.  Power on a circle  *(Fowles 7e §4.1, p.145)*
For uniform circular motion the centripetal force is perpendicular to **v**, so
P = **F**·**v** = 0 — it does no work and the speed is constant. Confirm with a
centripetal force and a tangential velocity. *Check:* `power(F_radial, v_tangential)`.

**Solution.** In uniform circular motion the centripetal force points radially inward, along $-\hat{\mathbf r}$, while the velocity is tangential, along $\hat{\boldsymbol\theta}$; the two are orthogonal, $\hat{\mathbf r}\cdot\hat{\boldsymbol\theta}=0$. Hence the instantaneous power is
$$P=\mathbf F\cdot\mathbf v=0.$$
No power means no work is done, so by the work–energy theorem $\Delta T=0$ and the speed stays constant — the force only turns $\mathbf v$, it never lengthens it. With a radial $\mathbf F$ and perpendicular $\mathbf v$, `power(F_radial, v_tangential)` returns $0$.

### P5.  Kinetic energy is frame-dependent  *(→ `~CM-03`)*
Compute T for a particle in the lab frame and in the centre-of-mass frame and note
they differ — kinetic energy is not a Galilean invariant (work is, between the
same two states). *Check:* `kinetic_energy` with velocities from `to_cm_frame`.

**Solution.** Kinetic energy depends on velocity, which shifts by the boost $\mathbf V$ between frames, $\mathbf v'=\mathbf v-\mathbf V$. For a system, König's theorem splits the lab kinetic energy into a bulk part plus an internal part:
$$T_\text{lab}=\sum_i\tfrac12 m_i|\mathbf v_i|^2=\tfrac12 M|\mathbf V_\text{cm}|^2+\underbrace{\sum_i\tfrac12 m_i|\mathbf v_i-\mathbf V_\text{cm}|^2}_{T_\text{cm}}.$$
Thus $T_\text{lab}=T_\text{cm}+\tfrac12 M|\mathbf V_\text{cm}|^2>T_\text{cm}$ whenever the centre of mass moves — kinetic energy is **not** Galilean-invariant. Feeding lab velocities, then their `to_cm_frame` images, into `kinetic_energy` returns these two different numbers, differing by exactly $\tfrac12 M|\mathbf V_\text{cm}|^2$.
