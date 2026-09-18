# EM-01 — Electrostatics (notes)

Electrostatics = the fields of charges **at rest**. The central object is the
**electric field** **E**(**r**), a vector at every point of space; everything in
this module is built from Coulomb's law by superposition and the MA-01 vector
operations.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages. Following Griffiths, **η** ≡ **r** − **r'**
is the **separation vector** from the source point **r'** to the field point **r**,
with magnitude η and direction **η̂** = **η**/η.

## 1. Coulomb's law
The force between two point charges (Gr §2.1.2, Eq. 2.1, p.60):
$$\mathbf F=\frac{1}{4\pi\varepsilon_0}\frac{qQ}{\eta^{2}}\,\hat{\boldsymbol\eta},
\qquad \frac{1}{4\pi\varepsilon_0}\approx 8.99\times10^{9}\ \mathrm{N\,m^2/C^2}.$$
Like charges repel, unlike attract; the force is along the line joining them and
falls off as 1/η². The constant is `K_E`, with ε₀ = `EPS0` the permittivity of
free space.

## 2. The electric field
Factor the test charge out of the force: the **field** is what the *source* sets
up, ready to push on whatever test charge $Q$ you place there (Gr §2.1.3, Eqs. 2.3–2.4, p.61):
$$\mathbf F=Q\,\mathbf E,\qquad
  \mathbf E(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\sum_{i}\frac{q_i}{\eta_i^{2}}\,\hat{\boldsymbol\eta}_i .$$
Code: `point_charge_field(q, source)` for one charge, `coulomb_field(charges)` for
the sum, `force_on_charge(Q, E)` for **F** = Q**E**. The field of a positive charge
points radially outward; `field_magnitude` and `field_line_direction` (MA-01 `norm`
and `unit`) split **E** into its strength and its field-line direction.

## 3. Superposition
The sum in Eq. 2.4 is the whole content of the **superposition principle**: the
field of a collection of charges is the vector sum of the individual fields, with
no cross-terms. Two equal charges therefore produce **E** = 0 at their midpoint;
a +q,−q pair (a *dipole*) leaves a nonzero field that, on the perpendicular
bisector, points antiparallel to the dipole axis — the seed of `~EM-05`.

## 4. Continuous charge distributions
For charge smeared out with volume density ρ(**r'**), the sum becomes an integral
(Gr §2.1.4, Eq. 2.8, p.63):
$$\mathbf E(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\int\frac{\hat{\boldsymbol\eta}}{\eta^{2}}\,\rho(\mathbf r')\,d\tau'.$$
Code: `field_of_distribution` lumps each cell of a box into a point charge
ρ dτ' and reuses `coulomb_field`. Seen from far away any localized blob looks like
a single point charge $kQ/r^2$ (the monopole / shell-theorem limit, tested) — the
leading term of the multipole expansion `~EM-05`.

## 5. The structure of E (bridge to EM-02)
The two facts that organize all of electrostatics are *local* statements about **E**:
$$\nabla\times\mathbf E=\mathbf 0\quad\text{(everywhere)},\qquad
  \nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}\quad\text{(Gauss)} .$$
Because the field functions here are ordinary vector fields, MA-02's `curl` and
`divergence` evaluate both directly: `curl(E)` returns **0**, and `divergence(E)`
returns 0 in charge-free space (the finite-difference residual is checked
*relative to the gradient scale* \|**E**\|/r, not in absolute V/m). The curl law
makes **E** the gradient of a potential `~EM-03`; the divergence law, integrated,
is Gauss's law `~EM-02`.

## Where this goes
- `~EM-02` turns ∇·**E** = ρ/ε₀ into the flux integral ∮**E**·d**a** = Q_enc/ε₀.
- `~EM-03` uses ∇×**E** = 0 to write **E** = −∇V.
- `~EM-05` expands the field of a localized cloud in powers of 1/r.
- `~EM-06` integrates ½ε₀\|**E**\|² to get the energy stored in the field.
- The same 1/r² inverse-square law reappears as Newtonian gravity (`~CM-11`) — `KEY BRIDGE B4`.
