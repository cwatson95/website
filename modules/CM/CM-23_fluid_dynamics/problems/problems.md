# CM-23 — Problems

Work by hand, then check with `code/fluid_dynamics.py`. Citations in `../refs.md`.

### P1.  Vorticity of rigid rotation  *(Boas 3e §6.11, p.324)*
For **v** = **Ω**×**r** (here (−Ωy, Ωx, 0)) show ω = ∇×v = 2**Ω**. *Check:*
`vorticity` = (0, 0, 2Ω).

*Answer:* $\boldsymbol\omega=2\boldsymbol\Omega=(0,0,2\Omega)$ — the vorticity is twice the (uniform) angular velocity of the fluid elements.

**Solution.** The vorticity is the curl of the velocity field,
$$\boldsymbol\omega=\nabla\times\mathbf v=\big(\partial_y v_z-\partial_z v_y,\ \partial_z v_x-\partial_x v_z,\ \partial_x v_y-\partial_y v_x\big).$$
For $\mathbf v=(-\Omega y,\ \Omega x,\ 0)$ the first two components vanish ($v_z=0$ and nothing depends on $z$), while the third is $\partial_x(\Omega x)-\partial_y(-\Omega y)=\Omega+\Omega=2\Omega$. Hence $\boldsymbol\omega=(0,0,2\Omega)$ — uniform across the flow, because every element turns rigidly at the same rate $\Omega$ and the vorticity counts that spin twice. With $\Omega=1.5$ this is $(0,0,3)$, matching `vorticity` $=(0,0,2\Omega)$.

### P2.  Shear has vorticity  *(Boas 3e §6.11, p.324)*
For the shear flow **v** = (y, 0, 0) show ω = (0, 0, −1) even though no element
"orbits". *Check:* `vorticity((y,0,0))` = (0,0,−1).

*Answer:* $\boldsymbol\omega=(0,0,-1)$; straight streamlines still carry vorticity because of the transverse velocity gradient (shear).

**Solution.** The only nonvanishing derivative of $\mathbf v=(y,0,0)$ is $\partial_y v_x=1$, so
$$\boldsymbol\omega=\nabla\times\mathbf v=\big(0,\ 0,\ \partial_x v_y-\partial_y v_x\big)=(0,0,-1).$$
Even though the streamlines are straight (the fluid moves only along $\hat x$), a tiny paddle wheel dropped in the flow spins clockwise: the faster fluid above drags its top forward while the slower fluid below holds its bottom back. Vorticity registers this shear-induced local rotation, not orbital motion — exactly the $(0,0,-1)$ returned by `vorticity((y,0,0))`.

### P3.  Potential flow is irrotational  *(Boas 3e §6.10, p.314)*
Show **v** = ∇φ has zero vorticity (curl of a gradient = 0), e.g. φ = x²−y².
*Check:* `is_irrotational` True; for this φ also `is_incompressible` (∇²φ = 0).

*Answer:* $\nabla\times\nabla\varphi\equiv0$ (every potential flow is irrotational); for $\varphi=x^2-y^2$ also $\nabla\cdot\mathbf v=\nabla^2\varphi=0$, so incompressible.

**Solution.** For any twice-differentiable potential the curl of a gradient vanishes identically, because mixed partials commute:
$$(\nabla\times\nabla\varphi)_z=\partial_x(\partial_y\varphi)-\partial_y(\partial_x\varphi)=0,$$
and likewise for the other two components — so $\mathbf v=\nabla\varphi$ is always irrotational. Taking $\varphi=x^2-y^2$ gives $\mathbf v=(2x,-2y,0)$, whose divergence is $\nabla\cdot\mathbf v=\nabla^2\varphi=2-2=0$: this potential is harmonic, so the flow is incompressible as well. Both `is_irrotational` and `is_incompressible` return True.

### P4.  Source flow is compressible  *(Boas 3e §6.10, p.316)*
For **v** = **r** show ∇·v = 3 (a source), so the flow is not incompressible, yet
it is still irrotational. *Check:* `is_incompressible` False, `is_irrotational` True.

*Answer:* $\nabla\cdot\mathbf v=3$ (a uniform source — not incompressible), yet $\nabla\times\mathbf v=0$ (still irrotational).

**Solution.** For the radial field $\mathbf v=\mathbf r=(x,y,z)$,
$$\nabla\cdot\mathbf v=\partial_x x+\partial_y y+\partial_z z=1+1+1=3\neq0,$$
so fluid is produced at a rate $3$ per unit volume — a source, not volume-preserving. Its curl, however, vanishes: $(\nabla\times\mathbf r)_z=\partial_x y-\partial_y x=0$, and the same for the other components, because each velocity component depends only on its own coordinate. Compressibility and rotation are independent properties, so `is_incompressible` is False while `is_irrotational` is True.

### P5.  Bernoulli and lift
Use ½v² + p/ρ + gz = const to explain why pressure drops where a fluid speeds up
(the Venturi effect / aerofoil lift). *Check:* compare `bernoulli_constant` at two
speeds with the same constant.

*Answer:* at fixed height $\tfrac12 v^2+p/\rho=\text{const}$, so faster flow forces lower pressure — the Venturi effect and the origin of aerodynamic lift.

**Solution.** Along a streamline at constant height Bernoulli's relation reduces to
$$\tfrac12 v^2+\frac{p}{\rho}=\text{const}\quad\Rightarrow\quad p_2-p_1=\tfrac12\rho\big(v_1^2-v_2^2\big),$$
so wherever the flow speeds up ($v_2>v_1$) the pressure must drop. Concretely, with $\rho=1000$ a point at $v=2\ \mathrm{m/s},\ p=100\ \mathrm{kPa}$ has constant $\tfrac12(2^2)+100=102$; at a constriction where $v=4\ \mathrm{m/s}$ the same constant forces $p/\rho=102-\tfrac12(4^2)=94$, i.e. $p=94\ \mathrm{kPa}$ — a $6\ \mathrm{kPa}$ drop. Over an aerofoil the air runs faster across the longer upper surface, lowering the pressure there and producing net upward lift. Both states share the same `bernoulli_constant`: `bernoulli_constant(2,1e5,1000,0)` $=$ `bernoulli_constant(4,9.4e4,1000,0)` $=102$.
