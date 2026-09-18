# EM-02 — Gauss's Law (notes)

Gauss's law is **Coulomb's law repackaged as a statement about flux**. Take the field
**E** from `~EM-01`, push it through a closed surface with MA-02's `surface_flux`, and
the inverse-square law conspires so that only the *enclosed* charge survives:
∮**E**·d**a** = Q_enc/ε₀. The same content written locally is ∇·**E** = ρ/ε₀. With
enough symmetry this gives the field directly, and it is half of what fixes
electrostatics — the other half being ∇×**E** = 0.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page
numbers are the *printed* book pages. For a charge at the origin, $r$ is the distance
from it; for cylindrical (line) symmetry $s$ is the distance from the axis.

## 1. Flux and the integral law
The **flux** of **E** through a surface $\mathcal S$ counts the field lines crossing it
(Gr §2.2.1, p.66):
$$\Phi_E=\int_{\mathcal S}\mathbf E\cdot d\mathbf a .$$
Put a point charge at the centre of a sphere of radius $r$:
$\mathbf E=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\hat{\mathbf r}$ and
$d\mathbf a=r^2\sin\theta\,d\theta\,d\varphi\,\hat{\mathbf r}$, so the two factors of
$r^2$ cancel:
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\frac{1}{4\pi\varepsilon_0}\frac{q}{r^2}\,(4\pi r^2)=\frac{q}{\varepsilon_0}.$$
The radius dropped out — and since field lines are unbroken in charge-free space, **any**
closed surface enclosing $q$ gives the same flux, while a charge *outside* contributes
zero (every line that enters also leaves). Superposing charges gives **Gauss's law**
(Gr §2.2.1, Eq. 2.13, p.66):
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\frac{Q_{\text{enc}}}{\varepsilon_0}.$$
Code: `flux_through_sphere` evaluates the left side by handing EM-01's field and
`sphere_surface` to MA-02's `surface_flux`; `enclosed_charge` reads
$Q_{\text{enc}}=\varepsilon_0\Phi_E$ back off it. The surface-independence, and the
zero-for-outside-charges, are exactly the tested headline.

## 2. Applications — the three symmetries
When the distribution is symmetric enough that $\mathbf E$ is constant in magnitude and
normal (or parallel) to a well-chosen Gaussian surface, Gauss's law returns the field in
one step (Gr §2.2.3, p.71):

**Spherical** — a uniformly charged solid sphere, total $Q$, radius $R$. A concentric
Gaussian sphere of radius $r$ encloses all of $Q$ outside but only $Q(r/R)^3$ inside:
$$\mathbf E=\begin{cases}\dfrac{1}{4\pi\varepsilon_0}\dfrac{Q}{r^2}\,\hat{\mathbf r}, & r\ge R\\[1.4ex]\dfrac{1}{4\pi\varepsilon_0}\dfrac{Q\,r}{R^3}\,\hat{\mathbf r}, & r<R\end{cases}$$
continuous at $r=R$: point-charge-like outside, growing linearly inside. Code:
`uniform_sphere_field`.

**Cylindrical** — an infinite line charge $\lambda$, with a coaxial Gaussian cylinder of
radius $s$:
$$\mathbf E=\frac{\lambda}{2\pi\varepsilon_0 s}\,\hat{\mathbf s},$$
radial and falling off as $1/s$ (the result `~EM-01` could only reach as the $L\to\infty$
limit of a finite segment). Code: `line_charge_field`.

**Planar** — an infinite sheet of surface charge $\sigma$, with a Gaussian pillbox
straddling it:
$$\mathbf E=\frac{\sigma}{2\varepsilon_0}\,\hat{\mathbf n},$$
*uniform* — independent of distance — and reversing across the sheet, so $\mathbf E$
jumps by $\sigma/\varepsilon_0$ there. Code: `plane_sheet_field`.

## 3. The divergence of E — the local form
Apply the divergence theorem to the left of Gauss's law and write
$Q_{\text{enc}}=\int_{\mathcal V}\rho\,d\tau$ on the right (Gr §2.2.2, p.71):
$$\oint_{\mathcal S}\mathbf E\cdot d\mathbf a=\int_{\mathcal V}(\nabla\cdot\mathbf E)\,d\tau=\int_{\mathcal V}\frac{\rho}{\varepsilon_0}\,d\tau .$$
This holds for **every** volume $\mathcal V$, so the integrands must match —
**differential Gauss's law** (Gr §2.2.2, Eq. 2.16, p.71):
$$\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}.$$
Integral and differential forms are equivalent through MA-02's Gauss theorem; this is the
first of Maxwell's equations. Code: `gauss_residual(E, rho, point)` evaluates
`divergence(E)` (MA-02) at a point and subtracts $\rho/\varepsilon_0$, reporting the
result *relative to the scale $\rho/\varepsilon_0$* so the finite-difference truncation
error reads as a pure number; inside the uniform sphere it returns ~0.

## 4. The curl of E
The companion to the divergence is the curl. Whether from $\mathbf E=-\nabla V$ or
directly from the inverse-square field by superposition, the electrostatic field is
irrotational (Gr §2.2.4, Eq. 2.19, p.77):
$$\nabla\times\mathbf E=\mathbf 0 .$$
Together, $\nabla\cdot\mathbf E=\rho/\varepsilon_0$ and $\nabla\times\mathbf E=\mathbf 0$
*completely* determine electrostatics (Helmholtz). The curl law is checked in `~EM-01`
with MA-02's `curl`; here it closes the §2.2 picture and licenses the potential of
`~EM-03`.

## Where this goes
- `~EM-03` uses ∇×**E** = 0 to set **E** = −∇V; Gauss then becomes Poisson's equation
  ∇²V = −ρ/ε₀.
- `~EM-06` reads the field just outside a conductor (**E** = σ/ε₀ **n̂**) and the energy
  ½ε₀∫\|**E**\|² straight off Gauss's law.
- `~EM-07` re-runs the flux argument for the displacement **D**: ∮**D**·d**a** = Q_f,enc
  in dielectrics.
- `~EM-08` is the magnetic mirror image: ∇·**B** = 0 (no magnetic charge), the same
  divergence-theorem move.
- `~EM-13` collects ∇·**E** = ρ/ε₀ as the first of **Maxwell's equations**.
