# EM-06 — Conductors & Capacitance (notes)

The **energy** locked up in a static charge configuration, and the electrostatics
of **conductors** and **capacitors**. The one idea threaded through §2.4 is that
this energy can be attributed equally to the *charges* or to the *field* — two
expressions, one number — and §2.5 then applies it to conductors (equipotentials
whose surface charge is squeezed outward) and to capacitors.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages. Densities and fields are reused from
`~EM-01` and `~EM-02`; $k\equiv1/4\pi\varepsilon_0$.

## 1. The work it takes to move a charge
Carrying a charge $Q$ in from infinity to a point where the pre-existing potential
is $V$ costs work (Gr §2.4.1, Eq. 2.39, p.91)
$$W=QV ,$$
because $V$ is potential *energy per unit charge* and the electrostatic force is
conservative — the work is path-independent, set only by the endpoints. This is the
atom from which every energy below is built: bring the charges in one at a time and
add up the $QV$ costs.

## 2. Energy of a point-charge distribution
Assembling point charges, the $k$-th charge costs $q_k$ times the potential of those
already present. Summing every pair once (Gr §2.4.2, Eq. 2.41, p.92),
$$W=\frac{1}{4\pi\varepsilon_0}\sum_{i<j}\frac{q_iq_j}{r_{ij}}
   =\frac12\sum_i q_iV_i ,$$
the right form (Gr Eq. 2.42) being the symmetric rewrite, with $V_i$ the potential
at charge $i$ due to **all the others**; the $\tfrac12$ undoes the double counting
of each pair. Code: `work_to_assemble` evaluates the pairwise $i<j$ sum directly, so
it carries **no self-energy** — the (infinite) cost of assembling each point charge
out of itself is simply omitted. Sanity checks live in the tests: two charges give
$kq^2/r$; an equilateral triangle of side $s$ gives $3kq^2/s$.

## 3. Energy of a continuous distribution — energy in the field
Smear the charge out and the sum becomes $W=\tfrac12\int\rho V\,d\tau$ (Gr Eq. 2.43).
Using Gauss's law $\rho=\varepsilon_0\nabla\!\cdot\!\mathbf E$ and integrating by
parts, the boundary term pushed to infinity, this turns into an integral over the
**field** alone, throughout *all* space (Gr §2.4.3, Eq. 2.45, p.94):
$$W=\frac{\varepsilon_0}{2}\int_{\text{all space}}|\mathbf E|^2\,d\tau,
   \qquad u=\frac{\varepsilon_0}{2}|\mathbf E|^2 .$$
The energy now sits in the field at density $u$, wherever **E** is nonzero. Code:
`field_energy_density` returns $u$ as a scalar field (reusing the `~EM-01`
`field_magnitude`); `field_energy` integrates it over a box by midpoint quadrature
(exact when **E** is uniform, e.g. a capacitor gap); `field_energy_spherical` does
the radial integral $\int\tfrac{\varepsilon_0}{2}E^2\,4\pi r^2\,dr$, which lets the
$1/r^4$ tail run cheaply out to large $r$.

**Worked case — the uniformly charged sphere** (Gr §2.4.3, Ex. 2.9). With the
`~EM-02` field ($E=kQr/R^3$ inside, $kQ/r^2$ outside), splitting the integral gives
$W_\text{out}=\tfrac12 kQ^2/R$ and $W_\text{in}=\tfrac1{10}kQ^2/R$, so
$$W=\frac35\,\frac{1}{4\pi\varepsilon_0}\frac{Q^2}{R},$$
returned in closed form by `self_energy_uniform_sphere` and reproduced numerically
by `field_energy_spherical`. **Caveat:** the two pictures agree for spread-out charge
but *disagree* on ideal point charges — the pairwise sum of §2 drops the self-energy
(finite), while $\tfrac{\varepsilon_0}{2}\int E^2$ keeps it (divergent). The gap is
exactly the infinite self-energy of a point charge (Gr §2.4.3 discussion); for real,
finite distributions Eq. 2.45 is the trustworthy one.

## 4. Conductors: equipotentials and surface pressure
In a **conductor** free charges move until the interior field vanishes (Gr §2.5.1,
p.97): **E** = 0 inside, hence $\rho=0$ inside (all net charge migrates to the
surface), the whole conductor is an **equipotential** ($V$ constant), and just
outside **E** is perpendicular to the surface with magnitude $\sigma/\varepsilon_0$.

The surface charge sits in the field discontinuity it creates ($\sigma/\varepsilon_0$
outside, $0$ inside), so the field acting *on the sheet* is the **average**,
$\tfrac12\,\sigma/\varepsilon_0$. The force per unit area is therefore outward (Gr
§2.5.3, Eq. 2.51, p.103),
$$P=\frac{\sigma^2}{2\varepsilon_0}=\frac{\varepsilon_0}{2}E^2 ,
  \qquad E=\frac{\sigma}{\varepsilon_0}\ \text{just outside},$$
always pulling the surface *into* the field region regardless of the sign of
$\sigma$ — the same $\varepsilon_0E^2/2$ that is the energy density of §3, now read
as a pressure. Code: `surface_pressure(sigma)`.

## 5. Capacitors
Two conductors carrying $\pm Q$ set up a potential difference $V$ strictly
proportional to $Q$, so the ratio (Gr §2.5.4, Eq. 2.53, p.105)
$$C=\frac{Q}{V}$$
depends on **geometry only**. For parallel plates of area $A$ and gap $d$ the field
is uniform, $E=\sigma/\varepsilon_0=Q/\varepsilon_0A$, so $V=Ed$ and (Gr Eq. 2.54)
$$C=\frac{\varepsilon_0 A}{d}.$$
The same $C=Q/V$ route with the `~EM-02` fields gives the other standard geometries
(Gr §2.5.4, Ex. 2.11): an isolated sphere $C=4\pi\varepsilon_0R$; concentric spheres
$C=4\pi\varepsilon_0\,ab/(b-a)$, which $\to4\pi\varepsilon_0a$ as $b\to\infty$
(the isolated sphere recovered); coaxial cylinders $C=2\pi\varepsilon_0L/\ln(b/a)$.
Code: `capacitance_parallel_plate`, `capacitance_isolated_sphere`,
`capacitance_spherical`, `capacitance_cylindrical`.

Charging the capacitor by ferrying charge across the growing potential difference
stores (Gr Eq. 2.55)
$$W=\frac12CV^2=\frac12\frac{Q^2}{C}=\frac12QV ,$$
returned by `energy_stored(C, V)`. Written instead as $\tfrac{\varepsilon_0}{2}\int
E^2\,d\tau$ over the gap, $\tfrac12CV^2$ reproduces Eq. 2.45 identically — the demo
checks the field-energy integral against $\tfrac12CV^2$ for the parallel plate, the
two-ways-must-agree theme one more time.

## Where this goes
- `~EM-07` fills the gap with a dielectric: $C\to\kappa C$, the stored energy density
  becomes $\tfrac12\mathbf D\cdot\mathbf E$, and bound charge lowers **E** at fixed $Q$.
- The surface pressure $\varepsilon_0E^2/2$ is the electrostatic piece of the Maxwell
  stress tensor, and $u=\tfrac{\varepsilon_0}{2}E^2$ the electric half of the field
  energy density carried by the Poynting flux — both unpacked in `~EM-14`.
- The energy `~EM-01`/`~EM-02` fields feed in here is the same energy that, once the
  fields are allowed to move, radiates (`~EM-17`).
