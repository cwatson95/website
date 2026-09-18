# EM-07 — Problems

Work by hand, then check with `code/dielectrics.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  The uniformly polarized slab  *(Gr §4.2.1, p.173)*
A slab fills the region $0\le z\le d$ with uniform polarization $\mathbf P=P\,\hat{\mathbf z}$.
Show the bound charge is purely a pair of surface sheets, $\sigma_b=+P$ on the top face
($\hat{\mathbf n}=+\hat{\mathbf z}$) and $\sigma_b=-P$ on the bottom ($\hat{\mathbf n}=-\hat{\mathbf z}$),
with $\rho_b=-\nabla\cdot\mathbf P=0$ throughout the interior and zero charge on the sides
($\sigma_b=\mathbf P\cdot\hat{\mathbf n}=0$). Confirm the slab is overall neutral.
*Check:* `bound_surface_charge(P, n̂)` gives $\pm P$ on the faces and $0$ on a side normal;
`bound_volume_charge` on the uniform field is $0$.

**Solution.** With $\mathbf P=P\,\hat{\mathbf z}$ constant, the bound *volume* density vanishes everywhere,
$$\rho_b=-\nabla\cdot\mathbf P=-\partial_z P=0,$$
so all bound charge sits on the surfaces through $\sigma_b=\mathbf P\cdot\hat{\mathbf n}$. On the top face $\hat{\mathbf n}=+\hat{\mathbf z}$ gives $\sigma_b=P(\hat{\mathbf z}\cdot\hat{\mathbf z})=+P$; on the bottom $\hat{\mathbf n}=-\hat{\mathbf z}$ gives $-P$; on any side $\hat{\mathbf n}\perp\hat{\mathbf z}$ gives $0$. The two sheets carry $\pm P A$ over equal-area faces, so the slab is neutral. With $P=2\times10^{-6}\ \mathrm{C/m^2}$ the code returns $\sigma_b=+2\times10^{-6}$ (top), $-2\times10^{-6}$ (bottom), $0$ (side), and `bound_volume_charge` $=0$ — the pair-of-sheets picture exactly.

### P2.  Frozen-in radial polarization  *(Gr §4.2.1, p.173)*
A sphere of radius $R$ carries the "frozen-in" radial polarization $\mathbf P=k\,\mathbf r$
(magnitude growing linearly with radius). Compute the bound volume charge
$\rho_b=-\nabla\cdot\mathbf P=-3k$ and the bound surface charge $\sigma_b=\mathbf P\cdot\hat{\mathbf r}=kR$,
and verify the two cancel: $\rho_b\cdot\tfrac{4}{3}\pi R^3+\sigma_b\cdot4\pi R^2=0$.
*Check:* `bound_volume_charge` on `P_field = lambda x,y,z: (k*x, k*y, k*z)` returns $-3k$ at
any interior point; at the north pole `bound_surface_charge((0, 0, k*R), (0, 0, 1))` returns $kR$.

**Solution.** Write $\mathbf P=k\,\mathbf r=k(x,y,z)$. Its divergence is
$$\nabla\cdot\mathbf P=k\big(\partial_x x+\partial_y y+\partial_z z\big)=3k
\quad\Longrightarrow\quad \rho_b=-\nabla\cdot\mathbf P=-3k.$$
At the surface $\hat{\mathbf n}=\hat{\mathbf r}$, and $\mathbf P\cdot\hat{\mathbf r}=k\,\mathbf r\cdot\hat{\mathbf r}=kr=kR$, so $\sigma_b=kR$. The totals cancel:
$$\rho_b\cdot\tfrac43\pi R^3+\sigma_b\cdot4\pi R^2=-3k\cdot\tfrac43\pi R^3+kR\cdot4\pi R^2=-4\pi kR^3+4\pi kR^3=0,$$
as required for a dielectric with no free charge. The code (e.g. $k=3,\ R=2$) returns `bound_volume_charge` $=-9=-3k$ and `bound_surface_charge` $=6=kR$, with the weighted sum zero to rounding.

### P3.  Free charge embedded in a dielectric — Gauss for D  *(Gr §4.3.1, Eq. 4.23, p.181)*
A free point charge $q_f$ sits at the centre of a large block of linear dielectric. Using
$\oint\mathbf D\cdot d\mathbf a=Q_{f,\mathrm{enc}}$ on a concentric sphere, show
$\mathbf D=\dfrac{q_f}{4\pi r^2}\,\hat{\mathbf r}$ — *independent of the medium* — and hence
$\mathbf E=\mathbf D/\varepsilon=\dfrac{q_f}{4\pi\varepsilon r^2}\hat{\mathbf r}$, reduced from the
vacuum value by $\varepsilon_r$. *Check:* `free_charge_enclosed(displacement_point_free_charge(q_f), R=R)`
returns $q_f$ for several radii $R$ (the flux is the same through every sphere).

**Solution.** Spherical symmetry forces $\mathbf D=D(r)\,\hat{\mathbf r}$, so Gauss's law for $\mathbf D$ on a concentric sphere gives
$$\oint\mathbf D\cdot d\mathbf a=D(r)\,4\pi r^2=Q_{f,\mathrm{enc}}=q_f
\quad\Longrightarrow\quad\mathbf D=\frac{q_f}{4\pi r^2}\,\hat{\mathbf r}.$$
No permittivity enters — $\mathbf D$ is sourced by free charge alone and is the *same in every medium*. Dividing by $\varepsilon=\varepsilon_r\varepsilon_0$ recovers the field,
$$\mathbf E=\frac{\mathbf D}{\varepsilon}=\frac{q_f}{4\pi\varepsilon r^2}\,\hat{\mathbf r}
=\frac{1}{\varepsilon_r}\,\mathbf E_{\mathrm{vac}},$$
the vacuum Coulomb field screened by $\varepsilon_r$. Because the enclosed free charge is the same at every radius, `free_charge_enclosed` returns $q_f$ ($\approx5.0003\times10^{-9}$ C for $q_f=5$ nC) at $R=0.1,0.2,0.5,1.0$ alike — the tiny excess is the 80-point flux quadrature, not physics.

### P4.  The two faces of D in a linear dielectric  *(Gr §4.4.1, Eq. 4.30–4.34, p.185)*
A linear dielectric of dielectric constant $\varepsilon_r$ sits in a field $\mathbf E$. Show the
two definitions of the displacement coincide,
$$\mathbf D=\varepsilon\mathbf E=\varepsilon_0(1+\chi_e)\mathbf E
   =\varepsilon_0\mathbf E+\underbrace{\varepsilon_0\chi_e\mathbf E}_{\mathbf P},
   \qquad \chi_e=\varepsilon_r-1,$$
so that $\varepsilon\mathbf E$ and $\varepsilon_0\mathbf E+\mathbf P$ are the *same vector*.
*Check:* with `eps_r = 4`, `displacement_linear(eps_r, E)(p)` equals
`displacement_field(E, polarization_linear(eps_r, E))(p)` at any point `p`.

**Solution.** Start from the definition $\mathbf D=\varepsilon_0\mathbf E+\mathbf P$ and substitute the linear law $\mathbf P=\varepsilon_0\chi_e\mathbf E$:
$$\mathbf D=\varepsilon_0\mathbf E+\varepsilon_0\chi_e\mathbf E=\varepsilon_0(1+\chi_e)\mathbf E\equiv\varepsilon\mathbf E,$$
with $\varepsilon=\varepsilon_0(1+\chi_e)=\varepsilon_0\varepsilon_r$ and $\chi_e=\varepsilon_r-1$. The two expressions are not two fields but one vector regrouped: $\varepsilon\mathbf E$ bundles the vacuum term $\varepsilon_0\mathbf E$ together with the material response $\mathbf P=\varepsilon_0\chi_e\mathbf E$ into a single constant times $\mathbf E$. For $\varepsilon_r=4$ ($\chi_e=3$) both `displacement_linear(eps_r, E)` and `displacement_field(E, polarization_linear(eps_r, E))` return the identical $D_x=1.5915\times10^{-7}$ at the test point — the equality the tests check.

### P5.  The uniformly polarized sphere and the magnetic analogue  *(Gr §4.2.1, Ex. 4.2)*
Take a sphere with uniform $\mathbf P=P\,\hat{\mathbf z}$. Show the surface charge is
$\sigma_b=P\cos\theta$ (so the net bound charge vanishes), and that the field *inside* is the
uniform **depolarizing field**
$$\mathbf E_{\mathrm{in}}=-\frac{\mathbf P}{3\varepsilon_0}.$$
Note that this is the electric mirror of the uniformly **magnetized** sphere of `~EM-10`,
whose interior holds a uniform $\mathbf B$ built the same way from bound currents.
*Check:* `polarized_sphere_surface_charge(P)(θ)` returns $P\cos\theta$ and integrates to $0$
over the sphere; `polarized_sphere_inner_field((0,0,P))` returns $(0,0,-P/3\varepsilon_0)$.

**Solution.** With $\mathbf P=P\,\hat{\mathbf z}$ and $\hat{\mathbf n}=\hat{\mathbf r}$,
$$\sigma_b=\mathbf P\cdot\hat{\mathbf r}=P(\hat{\mathbf z}\cdot\hat{\mathbf r})=P\cos\theta.$$
The net bound charge vanishes, $\oint\sigma_b\,da=PR^2\!\int_0^{2\pi}\!d\phi\int_0^\pi\cos\theta\sin\theta\,d\theta=0$, since $\int_0^\pi\cos\theta\sin\theta\,d\theta=0$. For the interior, model the sphere as overlapping balls of charge $\pm\rho$ displaced by $\mathbf s$ with $\mathbf P=\rho\mathbf s$. Inside a uniform ball Gauss gives $\mathbf E=\rho\mathbf r/3\varepsilon_0$; superposing the positive ball (centre $\mathbf s$) and the negative ball (centre $0$),
$$\mathbf E_{\mathrm{in}}=\frac{\rho}{3\varepsilon_0}\big[(\mathbf r-\mathbf s)-\mathbf r\big]=-\frac{\rho\mathbf s}{3\varepsilon_0}=-\frac{\mathbf P}{3\varepsilon_0},$$
a uniform depolarizing field. The code confirms `polarized_sphere_surface_charge(P)(θ)` $=P\cos\theta$ (integrating to $0$) and `polarized_sphere_inner_field((0,0,P))` $=(0,0,-P/3\varepsilon_0)$, e.g. $-3.7647\times10^{4}$ V/m for $P=10^{-6}$.
