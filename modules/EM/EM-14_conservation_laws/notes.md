# EM-14 — EM Conservation Laws (notes)

When charges and fields are both in play, energy and momentum flow back and forth
between matter and field. The content of this module is that the **field** is a genuine
repository of energy, momentum and angular momentum, and that each is **locally
conserved**: what leaves a region must cross its boundary. Everything is built from the
`~EM-01`/`~EM-08` fields with the `~MA-01` cross product.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page numbers
are the *printed* book pages. Throughout, $c = 1/\sqrt{\mu_0\varepsilon_0}$ is the speed of
light (`C` in the code), and indices $i,j$ run over $x,y,z$ with $\delta_{ij}$ the
Kronecker delta.

## 1. The continuity equation (the template)
Local conservation of charge (Gr §8.1.1, Eq. 8.4, p.356):
$$\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0 .$$
Charge does not teleport: the only way the charge in a volume can change is for current to
cross its surface. This is the **prototype** every conservation law in the module copies —
*(rate of change of density)* $+\ \nabla\cdot$ *(flux)* $=$ *(source)*. The identical
equation governs mass in a fluid (`~CM-22`), probability in quantum mechanics (`~QM-04`)
and phase-space density in kinetics (`~PK-02`): one law, many densities — **KEY BRIDGE B2**.

## 2. Poynting's theorem — field energy and its flux
The work done by the EM force on the charges in a volume comes out of the field. Writing
that balance in terms of the fields alone defines an **energy density** (Gr §8.1.2,
Eq. 8.13, p.357)
$$u=\frac{\varepsilon_0}{2}\,E^2+\frac{1}{2\mu_0}\,B^2$$
and an energy **flux**, the **Poynting vector** (Eq. 8.10, p.358)
$$\mathbf S\equiv\frac{1}{\mu_0}\,(\mathbf E\times\mathbf B).$$
**Poynting's theorem** is then a continuity equation with a source:
$$\frac{\partial u}{\partial t}+\nabla\cdot\mathbf S=-\,\mathbf J\cdot\mathbf E ,$$
the right-hand side being the work per unit volume done on the charges. In a source-free
region ($\mathbf J\cdot\mathbf E=0$) it is pure continuity, $\partial_t u+\nabla\cdot\mathbf S=0$:
field energy is conserved and **S** tells you where it goes. Code: `energy_density` and
`poynting_vector` (the latter is literally `cross(E, B)/μ₀`). A purely electrostatic or
magnetostatic field has one of **E**, **B** equal to zero, so $\mathbf S=\mathbf 0$ — energy
is stored but nothing flows (checked in `test_static_field_has_no_poynting_flux`).

## 3. The Maxwell stress tensor — how fields push
The force the field exerts on the matter in a volume can be written entirely as a
**surface** integral, the flux of a rank-2 tensor (Gr §8.2.2, Eq. 8.19, p.362):
$$T_{ij}=\varepsilon_0\!\left(E_iE_j-\tfrac12\delta_{ij}E^2\right)+\frac{1}{\mu_0}\!\left(B_iB_j-\tfrac12\delta_{ij}B^2\right).$$
$T_{ij}$ is symmetric, and it is the force per unit area in the $i$-direction acting on a
surface element whose normal points in the $j$-direction; the total electromagnetic force
on the charges in a volume $\mathcal V$ is $F_i=\oint_{\mathcal S}T_{ij}\,da_j$ (plus, when
the fields are time-dependent, the momentum-storage term of §4). Diagonal entries are
**pressures** or tensions along the field, off-diagonal entries are **shears**. Code:
`maxwell_stress_tensor` returns the full $3\times3$; for a $+z$ plane wave it is
$\mathrm{diag}(0,0,-u)$, so $T_{zz}=-u$ is the push along the propagation direction
(checked, together with symmetry, in `test_stress_tensor_symmetric_and_Tzz`).

## 4. Field momentum and radiation pressure
If the fields hold energy and can push, they must also store **momentum**. Momentum
conservation for field + matter introduces a **momentum density** (Gr §8.2.3,
Eqs. 8.29–8.30, p.366)
$$\mathbf g=\varepsilon_0\mu_0\,\mathbf S=\varepsilon_0\,(\mathbf E\times\mathbf B)=\frac{\mathbf S}{c^{2}},$$
with $-T_{ij}$ playing the role of the momentum *flux*. For a monochromatic **plane wave**
(`~EM-15`, with $B_0=E_0/c$) the three densities lock together:
$$S=c\,u,\qquad g=\frac{u}{c},\qquad T_{zz}=-u .$$
Code: `momentum_density` gives $|\mathbf g|=|\mathbf S|/c^2=u/c$ (checked in
`test_momentum_density_is_S_over_c2`). A beam of intensity $S$ striking a surface deposits
its momentum, so it presses with a **radiation pressure**
$$P=\frac{S}{c}\ \text{(perfect absorber)},\qquad P=\frac{2S}{c}\ \text{(perfect reflector)},$$
which is `radiation_pressure(S_mag, reflected)`. Sunlight at Earth
($S\approx1361\ \mathrm{W/m^2}$, the solar constant) gives only $P\approx4.5\ \mu\mathrm{Pa}$
on a black surface — tiny, but the principle behind solar sails.

One fact makes the collapses above so clean: in a wave the electric and magnetic energy
densities are **equal**, $\tfrac12\varepsilon_0E^2=\tfrac{1}{2\mu_0}B^2$ (because $B=E/c$),
so $u=\varepsilon_0E^2$ (checked in `test_plane_wave_equipartition`).

## Where this goes
- `~EM-15` makes these densities concrete for waves: $\langle S\rangle=\tfrac12 c\varepsilon_0E_0^2$,
  and the same radiation pressure $S/c$.
- `~EM-17` — an accelerating charge radiates a Poynting flux that survives to infinity
  ($\propto 1/r^2$), giving the Larmor power.
- `~CM-22` / **KEY BRIDGE B2** — the §1 continuity equation is the mass-conservation law of
  continuum mechanics and the probability current of `~QM-04`: one structure across trunks.
- `~RE-13` — $T_{ij}$ is the space–space block of the relativistic **stress–energy tensor**
  $T^{\mu\nu}$, with $(u,\,\mathbf S/c)$ its energy row; that object is what sources gravity
  in the Einstein field equations.
