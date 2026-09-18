# EM-09 — Magnetic Vector Potential (notes)

Magnetostatics (`~EM-08`) closed with two facts about **B**: it is
**divergence-free** (∇·**B** = 0) and its curl is the current (∇×**B** = μ₀**J**).
This module unpacks the first. A divergence-free field is always a curl, so **B**
comes from a **vector potential** **A** — the magnetic counterpart of the scalar
potential V (`~EM-03`), but carrying its own redundancy, the **gauge freedom**,
which is the conceptual payload of the module.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e; page
numbers are the *printed* book pages. The dipole sits at the **origin**, so **r**
is the field point, r = |**r**| its distance, and **r̂** = **r**/r; for the
straight wire, s = √(x²+y²) is the cylindrical distance from the z-axis.

## 1. From ∇·B = 0 to a vector potential
The divergence of any curl vanishes identically, so the magnetostatic law
∇·**B** = 0 is solved *automatically* by writing **B** as a curl (Gr §5.4.1,
Eq. 5.59, p.243):
$$\nabla\cdot\mathbf B=0\;\Longrightarrow\;\mathbf B=\nabla\times\mathbf A.$$
This is the exact mirror of electrostatics: there the curl-free **E** became a
gradient, **E** = −∇V (`~EM-03`); here the divergence-free **B** becomes a curl.
Code: `B_from_A(A)` is just MA-02's `curl` applied to the potential, and the test
suite confirms it returns the right **B** for every example below.

## 2. Gauge freedom and the Coulomb gauge
**A** is underdetermined. Because ∇×(∇λ) = 0, the shift
$$\mathbf A\;\to\;\mathbf A+\nabla\lambda$$
leaves **B** unchanged for *any* scalar λ — the **gauge freedom**. We spend it to
impose the **Coulomb gauge** ∇·**A** = 0 (Gr §5.4.1, p.243). Feeding **B** = ∇×**A**
into Ampère's law ∇×**B** = μ₀**J** and using the identity
∇×(∇×**A**) = ∇(∇·**A**) − ∇²**A**, the gauge term drops and three scalar Poisson
equations remain (Eq. 5.63):
$$\nabla^2\mathbf A=-\mu_0\mathbf J,$$
one per Cartesian component, each the spitting image of ∇²V = −ρ/ε₀ (`~EM-03`).
Code: `coulomb_gauge_residual(A, point)` evaluates ∇·**A** with MA-02's
`divergence`, normalized by |**A**|/r so a gauge-respecting potential reads as a
pure number ≈ 0 rather than in raw T·m.

## 3. The infinite wire as a vector-potential problem
For an infinite straight wire on the z-axis carrying current I, the potential is
parallel to the current (Gr §5.4.1, p.243):
$$\mathbf A=-\frac{\mu_0 I}{2\pi}\ln\!\frac{s}{s_0}\,\hat{\mathbf z},\qquad
  s=\sqrt{x^2+y^2}.$$
Its curl is the familiar encircling field B = μ₀I/2πs (`~EM-08`). The reference
radius s₀ is pure gauge: changing it adds a constant to A_z, i.e. ∇λ with λ
linear in z, and **B** does not notice. Code: `wire_vector_potential(I, s0)`,
whose `B_from_A` reproduces EM-08's `infinite_wire_field` independent of s₀ — a
concrete demonstration that physics lives in **B**, not in **A**.

## 4. The magnetic moment and the dipole vector potential
Far from any localized current loop the potential is dominated by its **dipole**
term. With the **magnetic moment** (Gr §5.4.3, Eq. 5.86, p.252)
$$\mathbf m=I\!\int d\mathbf a=I\,\mathbf a$$
— current times the oriented area it bounds, in A·m² — the leading potential is
(Eq. 5.85)
$$\mathbf A_{\text{dip}}(\mathbf r)=\frac{\mu_0}{4\pi}\,\frac{\mathbf m\times\hat{\mathbf r}}{r^{2}}
  =\frac{\mu_0}{4\pi}\,\frac{\mathbf m\times\mathbf r}{r^{3}}.$$
Code: `magnetic_dipole_moment(I, area_vector)` returns **m** = I**a**;
`dipole_vector_potential(m)` returns A_dip(x,y,z), which falls off as 1/r² and
circulates azimuthally around the **m** axis.

## 5. The dipole field and the electric-dipole correspondence
Taking the curl of A_dip gives the **magnetic dipole field**
$$\mathbf B_{\text{dip}}(\mathbf r)=\frac{\mu_0}{4\pi}\,\frac{1}{r^{3}}
  \Big[\,3(\mathbf m\cdot\hat{\mathbf r})\,\hat{\mathbf r}-\mathbf m\,\Big],$$
identical *in form* to the **electric** dipole field of `~EM-05` (Eq. 3.104,
printed p.158) under the dictionary
$$\frac{1}{4\pi\varepsilon_0}\;\longleftrightarrow\;\frac{\mu_0}{4\pi},\qquad
  \mathbf p\;\longleftrightarrow\;\mathbf m.$$
On the axis the field is 2(μ₀/4π)m/r³; on the equatorial plane it is
−(μ₀/4π)m/r³ — twice as strong and antiparallel, the same 2:1 ratio the electric
dipole shows. Code: `dipole_B_field_closed(m)`; the headline test confirms
`B_from_A(dipole_vector_potential(m))` matches it pointwise, closing the loop
**A** → ∇×**A** → **B**.

## Where this goes
- `~QF-03` (gauge): the freedom **A** → **A** + ∇λ here is the *classical, abelian*
  seed of the gauge principle. Promoted to a local phase symmetry e^{iλ(x)} in QED,
  the same redundancy *forces* the potential to exist and fixes how it couples —
  the endpoint of KEY BRIDGE B8 (MA-18 → CM-18 → QF-03).
- `~EM-05`: the (1/4πε₀, **p**) ↔ (μ₀/4π, **m**) correspondence means every
  electric-dipole result transcribes to a magnetic one; the multipole machinery is
  shared.
- `~EM-10`: the moment **m** = I**a** is the building block of **magnetization M**
  (moment per unit volume), exactly as **p** builds the polarization **P** (`~EM-07`).
- The vector Poisson equation ∇²**A** = −μ₀**J** is solved by the *same* Green's
  function as ∇²V = −ρ/ε₀ (`~MA-14`), giving **A** = (μ₀/4π)∫**J**/η dτ′ and, once
  currents vary in time, the retarded potentials of `~EM-17`.
