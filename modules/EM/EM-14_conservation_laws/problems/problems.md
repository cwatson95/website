# EM-14 — Problems

Work by hand, then check with `code/conservation_laws.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages). Build the fields as `E(x,y,z)`/`B(x,y,z)` functions
(the `~EM-01`/`~EM-08` convention) and feed them straight to the operators.

### P1.  Poynting flux and energy of a plane wave  *(Gr §8.1.2, p.357–358)*
A wave travels in $+z$ with $\mathbf E=E_0\cos(kz)\,\hat x$ and
$\mathbf B=(E_0/c)\cos(kz)\,\hat y$. Show
$$\mathbf S=\frac{E_0^2}{\mu_0 c}\cos^2(kz)\,\hat z,\qquad u=\varepsilon_0E_0^2\cos^2(kz),$$
and hence that $S=c\,u$ at every point (use $1/\mu_0 c=\varepsilon_0 c$). *Check:*
`plane_wave_snapshot(E0, k)` builds the pair; confirm `norm(poynting_vector(E,B)(x,y,z))`
equals `C * energy_density(E,B)(x,y,z)`, and that **S** points along $+\hat z$.

**Solution.** With $\mathbf E=E_0\cos(kz)\,\hat x$ and $\mathbf B=(E_0/c)\cos(kz)\,\hat y$,
the cross product uses $\hat x\times\hat y=\hat z$:
$$\mathbf S=\frac1{\mu_0}\mathbf E\times\mathbf B=\frac{1}{\mu_0}\frac{E_0^2}{c}\cos^2(kz)\,\hat z=\frac{E_0^2}{\mu_0 c}\cos^2(kz)\,\hat z.$$
For the energy density, $1/c^2=\mu_0\varepsilon_0$ makes the magnetic store equal the electric,
$\frac1{2\mu_0}(E_0/c)^2=\tfrac{\varepsilon_0}{2}E_0^2$, so
$$u=\tfrac{\varepsilon_0}{2}E_0^2\cos^2(kz)+\tfrac1{2\mu_0}\tfrac{E_0^2}{c^2}\cos^2(kz)=\varepsilon_0E_0^2\cos^2(kz).$$
Dividing, $S/u=(1/\mu_0 c)/\varepsilon_0=1/(\mu_0\varepsilon_0 c)=c$, i.e. $S=c\,u$. For $E_0=1000$ V/m
at a crest the code returns $|\mathbf S|=2654$ W/m² and $C\cdot u=2654$ W/m² — equal, with $\mathbf S\parallel+\hat z$.

### P2.  Equipartition of energy in a wave  *(Gr §8.1.2, p.357)*
For any field obeying the plane-wave relation $B=E/c$, show the electric and magnetic
contributions to $u$ are equal,
$$\tfrac12\varepsilon_0E^2=\frac{1}{2\mu_0}B^2 ,$$
so that $u=\varepsilon_0E^2$. (This equipartition is why the §8 collapses are so tidy.)
*Check:* take $\mathbf E,\mathbf B$ from `plane_wave_snapshot`, then compare
$\tfrac12\varepsilon_0|\mathbf E|^2$ with $|\mathbf B|^2/2\mu_0$; their sum is
`energy_density(E,B)`.

**Solution.** The plane-wave relation $B=E/c$ with $c^2=1/\mu_0\varepsilon_0$ turns the magnetic
density into the electric one:
$$\frac1{2\mu_0}B^2=\frac1{2\mu_0}\frac{E^2}{c^2}=\frac1{2\mu_0}E^2\mu_0\varepsilon_0=\tfrac12\varepsilon_0E^2 .$$
The two halves of $u$ are therefore equal, and
$$u=\tfrac12\varepsilon_0E^2+\frac1{2\mu_0}B^2=\tfrac12\varepsilon_0E^2+\tfrac12\varepsilon_0E^2=\varepsilon_0E^2 .$$
Numerically (with $E_0=1000$ V/m) the code reports electric $u_E=4.427\times10^{-6}$ J/m³
equal to magnetic $u_B=4.427\times10^{-6}$ J/m³, summing to $u=8.854\times10^{-6}$ J/m³ = `energy_density(E,B)`.

### P3.  Field momentum and the pressure of sunlight  *(Gr §8.2.3, p.366)*
The solar constant is $S\approx1361\ \mathrm{W/m^2}$. Find the momentum density
$g=S/c^2$ carried by the sunlight just above the atmosphere, and the pressure on (a) a
perfectly black panel and (b) a perfect mirror. Why does the mirror feel twice the push?
*Check:* `momentum_density` gives $|\mathbf g|=u/c=S/c^2$; `radiation_pressure(1361)`
returns $S/c$ and `radiation_pressure(1361, reflected=True)` returns $2S/c$ (a few μPa).

**Solution.** The momentum density is $g=S/c^2=1361/(2.998\times10^8)^2=1.51\times10^{-14}\ \mathrm{kg/(m^2\,s)}$.
A black panel absorbs the beam, gaining its momentum at rate $S/c$ per unit area, so
$$P_{\text{abs}}=\frac Sc=\frac{1361}{2.998\times10^8}=4.54\ \mu\text{Pa}.$$
A mirror sends the beam back, reversing the momentum, so it must supply twice the impulse,
$P_{\text{refl}}=2S/c=9.08\ \mu\text{Pa}$ — the factor 2 is exactly $\Delta p=2p$ for reflection
versus $\Delta p=p$ for absorption. These reproduce `radiation_pressure(1361)` $=4.54\times10^{-6}$ Pa
and `radiation_pressure(1361, reflected=True)` $=9.08\times10^{-6}$ Pa.

### P4.  The stress tensor of a plane wave  *(Gr §8.2.2, p.362)*
For the $+z$ wave of P1 evaluate $T_{ij}$ and show every off-diagonal entry vanishes while
$$T_{xx}=T_{yy}=0,\qquad T_{zz}=-u ,$$
so $-T_{zz}=u$ is exactly the momentum carried per unit area per unit time — the radiation
pressure of §8.2.3. (Use the equipartition of P2 to kill the $xx$ and $yy$ diagonals.)
*Check:* `maxwell_stress_tensor(E,B)(0,0,0)` is symmetric, with `T[2][2]` equal to
`-energy_density(E,B)(0,0,0)`.

**Solution.** Only $E_x$ and $B_y$ are nonzero, so $E^2=E_x^2$, $B^2=B_y^2$, and every product
$E_iE_j$ (and $B_iB_j$) vanishes unless $i=j=x$ (resp. $i=j=y$) — so all off-diagonal $T_{ij}=0$.
Using equipartition $\tfrac12\varepsilon_0E_x^2=\tfrac1{2\mu_0}B_y^2$ (P2),
$$T_{xx}=\varepsilon_0\!\big(E_x^2-\tfrac12E^2\big)-\tfrac1{2\mu_0}B^2=\tfrac12\varepsilon_0E_x^2-\tfrac1{2\mu_0}B_y^2=0,$$
and likewise $T_{yy}=-\tfrac12\varepsilon_0E_x^2+\tfrac1{2\mu_0}B_y^2=0$, while
$$T_{zz}=-\tfrac12\varepsilon_0E_x^2-\tfrac1{2\mu_0}B_y^2=-\big(\tfrac12\varepsilon_0E^2+\tfrac1{2\mu_0}B^2\big)=-u .$$
So $\mathbf T=\mathrm{diag}(0,0,-u)$; the code gives the symmetric matrix with `T[2][2]`
$=-8.854\times10^{-6}=-$`energy_density(E,B)(0,0,0)`.

### P5.  Energy flow into a resistive wire  *(Gr §8.1.2, p.358)*
A long straight wire of radius $a$ carries current $I$ with a longitudinal surface field
$E_z$ (from the potential drop along it) and an azimuthal $B=\mu_0 I/2\pi a$. Show that at
the surface
$$\mathbf S=\frac{1}{\mu_0}\,\mathbf E\times\mathbf B$$
points **radially inward**, with magnitude $|\mathbf S|=E_zB/\mu_0$, and that
$\oint\mathbf S\cdot d\mathbf a=I^2R$ — the Joule heat flows *into* the wire through its
sides, carried by the field, not along the wire. *Check:* at the surface point $(a,0,0)$
take `E = lambda x,y,z:(0,0,Ez)` and `B = lambda x,y,z:(0,Bphi,0)`; then
`poynting_vector(E,B)(a,0,0)` points along $-\hat x$ (inward). Contrast a static field
($\mathbf B=\mathbf 0$), for which `poynting_vector` returns **0** — stored energy, no flow.

**Solution.** At $(a,0,0)$ the azimuthal direction is $\hat\phi=\hat y$, so $\mathbf E=E_z\hat z$
and $\mathbf B=B\,\hat y$. With $\hat z\times\hat y=-\hat x$,
$$\mathbf S=\frac1{\mu_0}\mathbf E\times\mathbf B=\frac{E_zB}{\mu_0}(\hat z\times\hat y)=-\frac{E_zB}{\mu_0}\hat x,$$
radially **inward**, magnitude $|\mathbf S|=E_zB/\mu_0$. Integrating the inward flux over the
side area $2\pi a L$ and inserting $B=\mu_0I/2\pi a$,
$$\oint|\mathbf S|\,da=\frac{E_zB}{\mu_0}\,2\pi aL=\frac{E_z}{\mu_0}\frac{\mu_0 I}{2\pi a}\,2\pi aL=E_zL\,I=V I=I^2R,$$
since $V=E_zL$ is the potential drop ($V=IR$). The Joule heat enters through the sides,
carried by the field. The code returns $\mathbf S(a,0,0)$ along $-\hat x$ (e.g. $(-79.6,0,0)$ for
the sample $E_z,B$) and exactly $\mathbf 0$ when $\mathbf B=\mathbf 0$.
