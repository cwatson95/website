# NE-02 — Nuclear models (notes)

`~NE-01` ended with a nucleus that is tiny, massive and structureless. This
module gives it structure — or rather two competing structures, because no single
picture works. The **liquid drop model** treats the nucleus as a drop of
incompressible fluid and predicts masses across the whole chart to about 0.1
MeV/nucleon; the **shell model** treats nucleons as independent particles in
orbitals and explains the magic numbers the drop model cannot see. Both are
wrong, both are indispensable, and between them they explain why some nuclides
are stable, which way the others decay (`~NE-05`), and why both fission
(`~NE-09`) and fusion (`~NE-10`) release energy.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §3.2,
cited by **printed** page (PDF page = printed + 23). Measured masses come from
`../data_tables/B1_atomic_masses.csv`, the extraction of the book's Appendix B.

## 1. Nuclear matter is incompressible

Electron scattering and muonic x-rays measure the proton distribution inside a
nucleus, which is well fitted by a Fermi (Woods–Saxon) profile [S&F Eq. (3.11)]
$$\rho(r)=\frac{\rho_o}{1+\exp[(r-R)/a]},$$
with $R$ the radius at half central density and $a\approx0.5$ fm the surface
thickness. The empirical finding is that $R$ scales as $A^{1/3}$
[S&F Eq. (3.13), p. 64]:
$$\boxed{\;R = 1.1\,A^{1/3}\ \text{fm}\;}$$
— `nuclear_radius(A)`. Since $V\propto R^{3}\propto A$, the nucleon number
density $A/V$ is **the same for every nucleus**:
$$n=\frac{A}{\frac43\pi R^{3}}=0.179\ \text{nucleons/fm}^{3},$$
`nucleon_number_density(A)`, constant to machine precision across $A=4$ to $238$
(`test_radius_law_and_constant_density`). Two consequences follow immediately.
Nuclear matter is **incompressible** — squeezing it costs enormously, which is
why the drop analogy works. And the nuclear force must **saturate**: if every
nucleon attracted every other, binding energy would grow as $A^{2}$ and the
nucleus would collapse to a point. Instead each nucleon binds only to its
immediate neighbours, exactly as molecules do in a liquid.

## 2. The semi-empirical mass formula

Start from the crude estimate that a nucleus weighs what its parts weigh
[S&F Eq. (3.15), p. 71]:
$$m({}^{A}_{Z}\mathrm{X})=Zm_p+(A-Z)m_n .$$
The real mass is always *less*, because energy is released when the nucleons
bind; the deficit is the binding energy $BE$, and $BE/c^{2}$ must be subtracted.
The liquid drop model builds $BE$ from five terms [S&F Eq. (3.16), p. 73] —
`semf_terms(A, Z)` returns them individually:

| term | form | why |
|---|---|---|
| volume | $+a_vA$ | each nucleon binds to its neighbours; saturation makes this $\propto A$ |
| surface | $-a_sA^{2/3}$ | surface nucleons have fewer neighbours — surface tension |
| Coulomb | $-a_cZ^{2}/A^{1/3}$ | protons repel; energy $\propto Z(Z-1)/R\simeq Z^{2}/A^{1/3}$ |
| asymmetry | $-a_a(A-2Z)^{2}/A$ | departing from $N=Z$ costs binding |
| pairing | $-a_p/\sqrt{A}$ | paired nucleons bind better |

$$\boxed{\;BE=a_vA-a_sA^{2/3}-a_c\frac{Z^{2}}{A^{1/3}}
-a_a\frac{(A-2Z)^{2}}{A}-\frac{a_p}{\sqrt A}\;}$$
with [Wapstra 1958, S&F p. 73]
$$a_v=15.835,\quad a_s=18.33,\quad a_c=0.714,\quad a_a=23.20\ \text{MeV},$$
$$a_p=\begin{cases}
+11.2\ \text{MeV} & \text{odd }N,\ \text{odd }Z\\
0 & \text{odd-even or even-odd}\\
-11.2\ \text{MeV} & \text{even }N,\ \text{even }Z .
\end{cases}$$

> **Watch the pairing sign.** $a_p$ is *positive* for odd-odd and *negative* for
> even-even, and it enters $BE$ as $-a_p/\sqrt A$. So even-even nuclei **gain**
> $11.2/\sqrt A$ MeV and odd-odd nuclei **lose** it. Flipping this inverts the
> mass parabolas of §5 and predicts exactly the wrong decay directions.
> `pairing_sign`/`pairing_term` encode it, and
> `test_pairing_helps_even_even_and_hurts_odd_odd` pins it down.

The mass then follows as `semf_nuclear_mass_u(A, Z)`. Adding $Z$ electrons to
both sides converts $Z$ protons into $Z$ hydrogen atoms and gives the **atomic**
mass [S&F pp. 73–74]
$$M({}^{A}_{Z}\mathrm{X})=ZM({}^{1}_{1}\mathrm{H})+(A-Z)m_n-\frac{BE}{c^{2}},$$
`semf_atomic_mass_u(A, Z)`. The electron binding energies dropped in this step
are eV-scale against MeV-scale nuclear binding — the $10^{6}$ ratio established
in `~NE-01` — and they largely cancel between the two sides.

## 3. How well does it work?

Against the measured masses of Appendix B (`measured_binding_energy`), which
invert the same relation on real data:

| nuclide | SEMF $B/A$ | measured $B/A$ | error |
|---|---|---|---|
| ⁴He | 5.238 | 7.074 | −1.836 |
| ¹⁶O | 7.602 | 7.976 | −0.374 |
| ⁴⁰Ca | 8.432 | 8.551 | −0.119 |
| ⁵⁶Fe | 8.699 | 8.790 | −0.091 |
| ²⁰⁸Pb | 7.811 | 7.868 | −0.056 |
| ²³⁸U | 7.589 | 7.570 | +0.018 |

For $A\ge40$ the model is good to better than 0.25 MeV/nucleon across the entire
chart — `test_semf_tracks_measured_masses_for_medium_and_heavy_nuclei` checks
this over 150+ nuclides. It fails badly for ⁴He, and it should: "a drop of
liquid" is a meaningless description of four nucleons, all of which are surface.

The competition between the volume term (grows as $A$) and the surface term
(grows as $A^{2/3}$, i.e. falls per nucleon) makes $B/A$ **rise** at small $A$;
the Coulomb term (grows as $Z^{2}/A^{1/3}$) makes it **fall** at large $A$. The
result is a maximum near $A\approx56$ — `test_binding_energy_per_nucleon_peaks_in_the_iron_region`
locates it at $A=50$–$70$ with $B/A\approx8.7$ MeV. **This single curve is why
nuclear energy exists:** climbing toward the peak from either end releases energy,
by fusion from below (`~NE-10`) and fission from above (`~NE-09`).

## 4. The line of stability

For fixed $A$, the most stable nuclide is the lightest. Differentiating
Eq. (3.16) with respect to $Z$ [S&F Eq. (3.17)] and setting it to zero gives
[S&F Eq. (3.18), p. 73]
$$\boxed{\;Z(A)=\frac{A}{2}\,
\frac{1+(m_n-m_p)c^{2}/(4a_a)}{1+a_cA^{2/3}/(4a_a)}\;}$$
— `most_stable_Z(A)`. Read the structure rather than the algebra. Without the
Coulomb term the answer would be $Z\approx A/2$: the asymmetry term alone wants
$N=Z$. The $a_cA^{2/3}$ in the denominator is proton–proton repulsion, and it
grows with $A$, pushing the optimum steadily **below** $A/2$. So light stable
nuclides sit on $N=Z$ and heavy ones are neutron rich:

| $A$ | $Z(A)$ | $N/Z$ |
|---|---|---|
| 20 | 9.60 | 1.00 |
| 56 | 25.52 | 1.15 |
| 120 | 51.24 | 1.34 |
| 208 | 83.02 | 1.51 |
| 238 | 93.14 | 1.56 |

`test_most_stable_Z_matches_known_stable_nuclides` checks the rounded prediction
lands within one unit of the actual stable $Z$ for ²⁷Al, ⁴⁰Ca, ⁵⁶Fe, ¹²⁰Sn and
²⁰⁸Pb. The one place it is off by a full unit is instructive: at $A=120$ it
predicts $Z=51$, while nature picks $Z=50$ — because 50 is a magic number, and a
smooth formula cannot know that (§6). The neutron excess of heavy nuclei is not a detail — it is why fission
fragments are born neutron rich and must shed neutrons (`~NE-09`), and it is the
origin of delayed neutrons and hence of controllable reactors (`~NE-20`).

## 5. Mass parabolas

Fix $A$ and plot mass against $Z$ [S&F §3.2.6, p. 74]. Since $BE$ is quadratic in
$Z$, the masses lie on a parabola — except that the pairing term splits it in
two: **even-even nuclides on a lower curve, odd-odd on an upper one**, separated
by $2a_p/\sqrt A$. `isobar_masses(A)` generates the data.

For $A=110$ (the book's Fig. 3.13) the predicted minimum is at $Z(110)=47.39$,
and the two curves give:

| $Z$ | parity | $M-109.9$ (mu) |
|---|---|---|
| 45 | odd-odd | 12.82 |
| 46 | even-even | 7.04 |
| 47 | odd-odd | 7.97 |
| 48 | even-even | 6.45 |
| 49 | odd-odd | 11.65 |

The two stable nuclides of this isobar are ¹¹⁰Pd ($Z=46$) and ¹¹⁰Cd ($Z=48$) —
both even-even, and they **straddle** the predicted 47.39, exactly as S&F
observe (`test_isobar_110_reproduces_the_book_figure`). ¹¹⁰Ag ($Z=47$, odd-odd)
sits between them in $Z$ but *above* both in mass, so it can beta-decay either
way. The two-parabola structure is the reason: (i) most odd-$A$ isobars have
exactly one stable nuclide, (ii) many even-$A$ isobars have two or three, and
(iii) odd-odd nuclides are almost all unstable — only four are stable in nature.
All of this is the input to `~NE-05`.

## 6. What the drop model cannot do — magic numbers

Nuclides with $Z$ or $N$ equal to [S&F §3.2.7, p. 75]
$$2,\ 8,\ 20,\ 28,\ 50,\ 82,\ 126$$
are anomalously abundant, anomalously tightly bound, and anomalously reluctant to
absorb another neutron. The liquid drop model is **smooth** in $A$ and $Z$, so it
cannot produce a bump at special values — and the residuals prove it
(`test_shell_closures_show_up_as_extra_binding`):

| nuclide | $Z$, $N$ | measured − SEMF |
|---|---|---|
| ⁴He | 2, 2 | +7.34 MeV |
| ¹⁶O | 8, 8 | +5.98 MeV |
| ⁴⁰Ca | 20, 20 | +4.78 MeV |
| ⁴⁸Ca | 20, 28 | +5.91 MeV |
| ²⁰⁸Pb | 82, 126 | +11.70 MeV |

Every doubly magic nucleus is *more* bound than the smooth formula allows, by up
to 12 MeV. These are the nuclear analogue of the noble gases: closed shells. The
**shell model** [S&F §3.2.7] obtains them by solving Schrödinger's equation for a
nucleon in the average potential of all the others — the same independent-particle
idea as `~QM-14`, and it needs a strong spin–orbit term to reproduce 28, 50, 82
and 126. `is_magic`, `is_doubly_magic` and `magic_gap` expose the numbers; the
low neutron-absorption cross sections of magic nuclides are visible directly in
`../data_tables/C1_thermal_neutron_cross_sections.csv` and matter for reactor
materials selection in `~NE-19`.

## Where this goes

- `~NE-03` — binding energy and separation energies made quantitative from real
  masses; the $B/A$ curve of §3 is that module's central object.
- `~NE-04` — Q-values, which are mass differences of exactly the kind computed here.
- `~NE-05`, `~NE-07` — the mass parabolas of §5 decide which decay mode a nuclide
  takes and where a decay chain terminates.
- `~NE-09` — the drop model's surface-vs-Coulomb competition is the basis of the
  fission barrier and of the fissionability parameter $Z^{2}/A$.
- `~QM-14` — the independent-particle picture behind the shell model.
