# EM-03 — Electric Potential (notes)

The **potential** $V(\mathbf r)$ is a single scalar at every point of space whose
gradient is (minus) the electric field. It exists at all *only* because electrostatic
**E** is curl-free (`~EM-02`); once it exists it is the easiest route to the field,
since a scalar superposes by plain addition. Everything here is the EM-01 field run
through the MA-02 operators `line_integral`, `gradient`, and `laplacian`.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page
numbers are the *printed* book pages. As in EM-01, **η** ≡ **r** − **r'** is the
**separation vector** from the source point **r'** to the field point **r**, with
magnitude η.

## 1. The potential: V = −∫E·dl
Because $\nabla\times\mathbf E=\mathbf 0$ for any electrostatic field (`~EM-02`), the
line integral of **E** between two points is **path-independent** and $\oint\mathbf
E\cdot d\mathbf l=0$. That is exactly the condition for **E** to be a gradient, so we
may define a scalar (Gr §2.3.1, Eq. 2.21, p.78):
$$V(\mathbf r) = -\int_{\mathcal O}^{\mathbf r}\mathbf E\cdot d\mathbf l ,$$
with $\mathcal O$ a reference point (usually infinity) where $V=0$. Only the
**difference** is physical, $V(\mathbf b)-V(\mathbf a)=-\int_{\mathbf a}^{\mathbf b}
\mathbf E\cdot d\mathbf l$. Code: `potential_from_field(E, reference)` integrates along
the straight segment from `reference` to the field point with MA-02's `line_integral`;
path-independence is what licenses that straight-line choice, and `test_path_independence`
confirms two different references give the same difference.

## 2. The field from the potential: E = −∇V
The fundamental theorem for gradients inverts Eq. 2.21 (Gr §2.3.1, Eq. 2.23, p.78):
$$\mathbf E = -\nabla V .$$
Three field components collapse to one scalar, then unfold again by a derivative — no
information is lost because the curl-free condition removed the three numbers' worth of
freedom in the first place. Code: `field_from_potential(V)` is MA-02's `gradient`,
negated, returned as a field function; `test_field_is_minus_grad_V` checks it reproduces
the *exact* EM-01 Coulomb field of a point charge. Since only the gradient of $V$ enters,
$V$ is fixed **only up to an additive constant** — moving the reference point adds a
constant and changes no field, a freedom Griffiths catalogues alongside the units (volts)
and the scalar superposition rule (Gr §2.3.2, p.80).

## 3. Superposition of the potential (a scalar)
For a single point charge $q$ at the origin, Eq. 2.21 with $E=kq/\eta^{2}$ gives
$V=(1/4\pi\varepsilon_0)\,q/\eta$. Because the integral defining $V$ is linear in **E** and
**E** superposes, **V superposes too — but as a scalar** (Gr §2.3.4, Eq. 2.29, p.84):
$$V(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\sum_i\frac{q_i}{\eta_i}
            =\frac{1}{4\pi\varepsilon_0}\int\frac{\rho(\mathbf r')}{\eta}\,d\tau' .$$
No vectors, no angles — a plain sum of $q/\eta$ terms — which is precisely why the
potential is the easier road to **E**. Code: `potential_of_charge(q, source)` for one
charge, `potential_point_charges(charges)` for the sum. A $+q,-q$ pair gives a potential
that is **odd** under reflection through its midplane, so that whole plane sits at $V=0$
(`test_superposition_and_dipole_antisymmetry`); its far field is the dipole term that
opens `~EM-05`.

## 4. Poisson's and Laplace's equations
Combine $\mathbf E=-\nabla V$ (Eq. 2.23) with Gauss's law $\nabla\cdot\mathbf
E=\rho/\varepsilon_0$ (`~EM-02`): $\nabla\cdot(-\nabla V)=\rho/\varepsilon_0$, i.e.
(Gr §2.3.3, Eq. 2.24, p.83)
$$\nabla^2 V = -\frac{\rho}{\varepsilon_0}\qquad\text{(Poisson)},$$
and wherever there is no charge (Gr §2.3.3, Eq. 2.25, p.83)
$$\nabla^2 V = 0\qquad\text{(Laplace)}.$$
This is the central PDE of electrostatics and the gateway to `~MA-08` (separation of
variables) and `~MA-14` (Green's functions): recovering $V$ from $\rho$ and boundary
data is the boundary-value problem of `~EM-04`. Code: `poisson_residual(V, rho, point)`
returns $\nabla^2V+\rho/\varepsilon_0$ via MA-02's `laplacian`, normalized by the natural
curvature scale $|V|/L^2$ so truncation error reads as a pure number; for the
point-charge potential in vacuum it is $\approx 0$, as `test_laplace_in_vacuum` checks.

## 5. Boundary conditions
Across a surface carrying charge density $\sigma$ the field jumps but the potential does
not (Gr §2.3.5, Eq. 2.31–2.33, p.88):
$$\mathbf E_{\text{above}}-\mathbf E_{\text{below}}=\frac{\sigma}{\varepsilon_0}\,
  \hat{\mathbf n},\qquad
  V_{\text{above}}=V_{\text{below}},\qquad
  \frac{\partial V_{\text{above}}}{\partial n}-\frac{\partial V_{\text{below}}}{\partial n}
  =-\frac{\sigma}{\varepsilon_0}.$$
The **normal** component of **E** is discontinuous by $\sigma/\varepsilon_0$ (the
tangential part is continuous because $\nabla\times\mathbf E=\mathbf 0$); $V$ itself is
continuous because $\int\mathbf E\cdot d\mathbf l$ over a vanishing path is zero, while
its normal derivative inherits the field's jump. These matching conditions are what make
the boundary-value problems of `~EM-04` well posed.

## Where this goes
- `~EM-04` solves $\nabla^2 V=-\rho/\varepsilon_0$ (or $=0$) with boundary data —
  separation of variables, method of images, uniqueness theorems.
- `~EM-05` expands $V$ of a localized cloud in powers of $1/r$ (the multipole series),
  whose dipole term is the $+q,-q$ potential of §3.
- `~EM-06` integrates $W=\tfrac12\int\rho V\,d\tau$ (equivalently $\tfrac{\varepsilon_0}{2}\int|\mathbf E|^2$)
  for the energy stored in the configuration.
- `~MA-08` (PDEs) and `~MA-14` (Green's functions) are the math engines for
  Poisson/Laplace.
- The same $1/r$ potential is Kepler's and the hydrogen atom's, reappearing in `~CM-11`
  and `~QM-12` — `KEY BRIDGE B4`.
