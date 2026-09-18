# EM-08 — Magnetostatics (notes)

Magnetostatics = the magnetic fields of **steady currents** — charge in motion at a
steady rate ($\partial\rho/\partial t = 0$, equivalently $\nabla\cdot\mathbf J = 0$). The
central object is the **magnetic field** **B**(**r**), a vector at every point of space;
unlike **E** it is sourced by *currents*, not charges, and it acts only on *moving*
charge. Everything here is built from the Biot–Savart law and the MA-01 cross product.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page numbers
are the *printed* book pages. As in EM-01, **η** ≡ **r** − **r'** is the **separation
vector** from the source point **r'** to the field point **r**, with magnitude η and
direction **η̂** = **η**/η.

## 1. Magnetic fields and the Lorentz force
Griffiths opens (Gr §5.1.1, p.210) with the experimental fact that currents exert forces
on currents. Packaged as a field, the **magnetic force** on a charge $Q$ moving with
velocity **v** is (Gr §5.1.2, Eq. 5.1, p.212):
$$\mathbf F = Q\,(\mathbf v \times \mathbf B),$$
the magnetic part of the full Lorentz force $\mathbf F = Q(\mathbf E + \mathbf v\times\mathbf B)$.
Because the cross product is perpendicular to **v**, the magnetic force **does no work**:
$$dW = \mathbf F\cdot d\boldsymbol\ell = Q(\mathbf v\times\mathbf B)\cdot\mathbf v\,dt = 0.$$
It bends a trajectory without changing its speed — a uniform **B** turns a charge in a
circle of radius $r = mv_\perp/QB$ at the cyclotron frequency $\omega = QB/m$. Code:
`lorentz_force(Q, v, B, E)`; the test confirms $\mathbf F\cdot\mathbf v = 0$ and
$\mathbf F\cdot\mathbf B = 0$.

## 2. Currents and the force on a wire
A current is moving charge, so a field **B** pushes on a current-carrying wire. The force
on a line current $I$ is (Gr §5.1.3, Eq. 5.16, p.216):
$$\mathbf F = \int I\,d\boldsymbol\ell \times \mathbf B ,$$
which for a straight segment **L** in a uniform field is $\mathbf F = I(\mathbf L\times\mathbf B)$.
Code: `force_on_wire(I, dl, B)`. Steady-current magnetostatics requires
$\nabla\cdot\mathbf J = 0$ (charge piles up nowhere) — the static face of the continuity
equation, **KEY BRIDGE B2** (`~CM-22`, `~QM-04`, `~EM-13`).

## 3. The Biot–Savart law
The magnetic analogue of Coulomb's law: a steady line current $I$ sets up (Gr §5.2.2,
Eq. 5.39, p.224)
$$\mathbf B(\mathbf r) = \frac{\mu_0}{4\pi}\,I\!\int \frac{d\boldsymbol\ell' \times \hat{\boldsymbol\eta}}{\eta^{2}},
  \qquad \mu_0 = 4\pi\times10^{-7}\ \mathrm{T\,m/A}.$$
Same $1/\eta^2$ falloff as electrostatics, but the cross product makes **B** *circulate*
around the current rather than point along **η**. Code: `biot_savart` integrates a
parametrized curve `path(t)` numerically (central-difference $d\boldsymbol\ell'$, MA-01
`cross`). Two standard results follow:

- **Infinite straight wire** (Eq. 5.36): $\;B = \dfrac{\mu_0 I}{2\pi s}$, azimuthal
  ($\hat{\boldsymbol\phi}$, right-hand rule about the current) — code `infinite_wire_field`.
- **On the axis of a circular loop** of radius $R$ (Ex. 5.6, Eq. 5.41):
  $$B_z = \frac{\mu_0 I R^2}{2\,(R^2 + z^2)^{3/2}},$$
  which is $\mu_0 I/2R$ at the centre and falls as $\mu_0 I R^2/2z^3$ far away (a magnetic
  dipole, the seed of `~EM-09`) — code `loop_axis_field_closed`, checked against the
  Biot–Savart `circular_loop_field`.

## 4. The divergence and curl of B
Taking the divergence and curl of the Biot–Savart field gives the local magnetostatic
field equations (Gr §5.3.2, p.231):
$$\nabla\cdot\mathbf B = 0\quad(\text{Eq. 5.50}),\qquad
  \nabla\times\mathbf B = \mu_0\mathbf J\quad(\text{Eq. 5.56}).$$
$\nabla\cdot\mathbf B = 0$ everywhere: there are **no magnetic monopoles**, and the field
lines always close on themselves — the sharp contrast with $\nabla\cdot\mathbf E =
\rho/\varepsilon_0$. Code: `div_B_residual` evaluates this with MA-02 `divergence`,
normalized by the gradient scale $|\mathbf B|/r$ so the finite-difference residual reads
as a pure number. The curl law is the magnetic analogue of Gauss's law; integrated, it is
Ampère's law.

## 5. Ampère's law
Integrate $\nabla\times\mathbf B = \mu_0\mathbf J$ over a surface and apply Stokes'
theorem (`~MA-02`) (Gr §5.3.3, Eq. 5.57, p.233):
$$\oint \mathbf B\cdot d\boldsymbol\ell = \mu_0 I_{\text{enc}} .$$
This is the magnetic counterpart of Gauss's law (`~EM-02`): given enough symmetry it
yields **B** at once. For the infinite wire, an amperian circle of radius $s$ gives
$B\,(2\pi s) = \mu_0 I$, hence $B = \mu_0 I/2\pi s$ — recovering Eq. 5.36 without the
Biot–Savart integral. Code: `ampere_circulation` runs MA-02 `line_integral` around the
circle; the test confirms $\oint\mathbf B\cdot d\boldsymbol\ell = \mu_0 I$ independent of $s$.

## Where this goes
- `~EM-09` uses $\nabla\cdot\mathbf B = 0$ to write $\mathbf B = \nabla\times\mathbf A$ —
  the **vector potential**, the magnetic analogue of $\mathbf E = -\nabla V$.
- `~EM-10` puts magnetostatics in matter: bound currents magnetize media and Ampère's law
  is recast for the auxiliary field **H**.
- `~EM-11`/`~EM-13` add time dependence — a changing **B** drives an EMF (Faraday), and
  $\nabla\times\mathbf B = \mu_0\mathbf J$ gains Maxwell's displacement-current term.
- The steady-current condition $\nabla\cdot\mathbf J = 0$ is the magnetostatic face of the
  continuity equation — **KEY BRIDGE B2** (`~CM-22` mass, `~QM-04` probability).
