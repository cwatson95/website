# QM-17 — Fine Structure, Zeeman & Hyperfine (notes)

The hydrogen spectrum of `~QM-12`, $E_n=-13.6\,\mathrm{eV}/n^2$, is the answer to
the Bohr Hamiltonian $H_0=p^2/2m-e^2/4\pi\varepsilon_0 r$. But that is "not quite
the whole story" (Griffiths 3e §7.3, p.378): there is a hierarchy of ever-smaller
corrections, each a textbook application of the time-independent perturbation
theory of `~QM-15`, where the first-order shift of a level is
$$E^1=\langle\psi^0|\,H'\,|\psi^0\rangle.$$
The hierarchy (Griffiths Table 7.1, p.378), in units of $E_n$:
fine structure $\sim\alpha^2$, Lamb shift $\sim\alpha^3$, hyperfine
$\sim\alpha^2(m_e/m_p)$.

## 0. The scale — the fine-structure constant

Everything is measured against one dimensionless number (Griffiths Eq. 7.44, p.378),
$$\boxed{\;\alpha=\frac{e^2}{4\pi\varepsilon_0\hbar c}\approx\frac1{137.036}\;}$$
It is the ratio of the electron's speed in the Bohr ground state to $c$. The Bohr
energy is itself $\alpha^2$ below the rest energy,
$$\mathrm{Ry}=\tfrac12\alpha^2 m_ec^2=13.606\ \mathrm{eV},$$
so a *further* factor $\alpha^2$ takes $13.6\,\mathrm{eV}$ down to the
$\sim10^{-4}\,\mathrm{eV}$ fine structure. (`fine_structure_constant`,
`rydberg_energy_eV` — both rederived from $e,\hbar,c,m_e,\varepsilon_0$ and checked
to CODATA, the `~QM-01` house rule.)

## 1. Fine structure — relativistic correction

The kinetic term $p^2/2m$ is only the leading piece of the relativistic
$T=\sqrt{p^2c^2+m^2c^4}-mc^2$. Expanding (Griffiths §7.3.1, p.380),
$$H'_{\rm rel}=-\frac{p^4}{8m^3c^2}.$$
Its expectation value in $|n\,\ell\,m\rangle$, using
$\langle 1/r\rangle$ and $\langle 1/r^2\rangle$ for hydrogen, is (Griffiths Eq. 7.58,
p.381)
$$E^1_{\rm rel}=-\frac{(E_n)^2}{2mc^2}\!\left[\frac{4n}{\ell+\tfrac12}-3\right].$$
It is negative (mass increases with speed, binding deepens) and depends on $n$ and
$\ell$ — **not** on $j$. (`relativistic_correction_eV`.)

## 2. Fine structure — spin-orbit coupling

In the electron's frame the proton orbits, making a magnetic field $\mathbf B\propto
\mathbf L$; the electron's spin moment $\boldsymbol\mu_s\propto\mathbf S$ sits in it,
giving $H'_{\rm so}\propto\mathbf L\!\cdot\!\mathbf S$ (Griffiths §7.3.2, p.384; the
Thomas-precession $\tfrac12$ is included, p.385). Because $\mathbf L$ and $\mathbf S$
are no longer separately conserved, the good states diagonalize the total
$\mathbf J=\mathbf L+\mathbf S$ (`~QM-13`); then $J^2=L^2+S^2+2\,\mathbf L\!\cdot\!\mathbf S$
gives (Griffiths Eq. 7.65, p.386)
$$\boxed{\;\langle\mathbf L\!\cdot\!\mathbf S\rangle=\frac{\hbar^2}{2}\big[\,j(j+1)-\ell(\ell+1)-s(s+1)\,\big]\;}$$
For a $p$ electron ($\ell=1,\,s=\tfrac12$): $p_{1/2}$ gives $-\hbar^2$ and $p_{3/2}$
gives $+\tfrac12\hbar^2$, and the $(2j+1)$-weighted average vanishes (the
center-of-gravity rule). (`LS_coupling`.) The energy shift is (Griffiths Eq. 7.67,
p.386)
$$E^1_{\rm so}=\frac{(E_n)^2}{mc^2}\,
\frac{n\big[j(j+1)-\ell(\ell+1)-\tfrac34\big]}{\ell(\ell+\tfrac12)(\ell+1)},$$
which vanishes for $\ell=0$ (no orbital motion). (`spin_orbit_correction_eV`.)

## 3. Fine structure — the grand result

Relativistic and spin-orbit corrections are "remarkably" the same order $\alpha^2$
(Griffiths p.386). For $\ell=0$ there is a third piece, the **Darwin term** (the
electron's *Zitterbewegung* smears the contact Coulomb interaction; it is a relic of
the Dirac equation, `~QM-22`, beyond Griffiths §7.3):
$$E^1_{\rm Darwin}=\frac{2n\,(E_n)^2}{mc^2}\quad(\ell=0),\qquad 0\quad(\ell\neq0).$$
Adding all three, the $\ell$-dependence cancels and only $j$ survives — the
celebrated **fine-structure formula** (Griffiths Eq. 7.68, p.386):
$$\boxed{\;E^1_{\rm fs}=-\frac{13.6\,\mathrm{eV}}{n^2}\,\frac{\alpha^2}{n^2}
\left[\frac{n}{\,j+\tfrac12\,}-\frac34\right]\;}$$
and the energy levels including fine structure (Griffiths Eq. 7.69, p.386):
$$E_{nj}=-\frac{13.6\,\mathrm{eV}}{n^2}\left[1+\frac{\alpha^2}{n^2}
\left(\frac{n}{\,j+\tfrac12\,}-\frac34\right)\right].$$
The code verifies $E^1_{\rm rel}+E^1_{\rm so}+E^1_{\rm Darwin}=E^1_{\rm fs}$ to
machine precision for every state. The structure (Griffiths Fig. 7.8, p.387): fine
structure **breaks the $\ell$-degeneracy** (the $2S_{1/2}$ and $2P_{3/2}$ states of
$n=2$ split apart) but **preserves the $j$-degeneracy** ($2S_{1/2}$ and $2P_{1/2}$
remain exactly coincident). The $n=2$ interval $2P_{3/2}-2P_{1/2}\approx
4.5\times10^{-5}\,\mathrm{eV}\approx10.9\,\mathrm{GHz}$ (Griffiths Problem 7.21).
(`fine_structure_correction_eV`, `hydrogen_energy_eV`.)

## 4. The Zeeman effect — an external field

Put the atom in a uniform field $\mathbf B_{\rm ext}$ (Griffiths §7.4, p.389). The
perturbation is the magnetic energy of the orbital + spin moments,
$$H'_Z=-(\boldsymbol\mu_\ell+\boldsymbol\mu_s)\!\cdot\!\mathbf B_{\rm ext}
=\frac{\mu_B}{\hbar}(\mathbf L+2\mathbf S)\!\cdot\!\mathbf B_{\rm ext},\qquad
\mu_B=\frac{e\hbar}{2m_e}=5.79\times10^{-5}\,\mathrm{eV/T},$$
the $2$ being the electron's spin $g$-factor. The outcome depends on $B_{\rm ext}$
versus the *internal* spin-orbit field ($\sim$ a few tesla in hydrogen).

**Weak field** ($B_{\rm ext}\ll B_{\rm int}$, Griffiths §7.4.1, p.390): fine
structure dominates, the good states are $|n\,\ell\,j\,m_j\rangle$. Since
$\mathbf L,\mathbf S$ precess about the conserved $\mathbf J$, only their projection
on $\mathbf J$ survives, replacing $(\mathbf L+2\mathbf S)$ by $g_J\mathbf J$ with the
**Landé $g$-factor** (Griffiths Eq. 7.78, p.390):
$$\boxed{\;g_J=1+\frac{j(j+1)+s(s+1)-\ell(\ell+1)}{2\,j(j+1)}\;},\qquad
E^1_Z=\mu_B\,g_J\,B_{\rm ext}\,m_j.$$
$g_J$ interpolates between the orbital value $1$ ($s=0$) and the spin value $2$
($\ell=0$): $^2S_{1/2}\to2$, $^2P_{1/2}\to\tfrac23$, $^2P_{3/2}\to\tfrac43$. Each
level fans into $2j+1$ equally spaced sublevels — the *anomalous* Zeeman effect.
(`lande_g_factor`, `zeeman_weak_field_eV`.)

**Strong field / Paschen–Back** ($B_{\rm ext}\gg B_{\rm int}$, Griffiths §7.4.2,
p.393): the field decouples $\mathbf L$ and $\mathbf S$, so $m_\ell$ and $m_s$ are
separately good and
$$E^1_Z=\mu_B B_{\rm ext}\,(m_\ell+2m_s),$$
with fine structure now the small perturbation on top. (`zeeman_strong_field_eV`.)

## 5. Hyperfine splitting — the 21 cm line

The proton is itself a tiny magnet, $\boldsymbol\mu_p=\dfrac{g_p e}{2m_p}\mathbf S_p$
with $g_p\approx5.59$ (it is a composite of three quarks, so $g_p\neq2$; Griffiths
§7.5, p.398). The electron sits in the proton's dipole field, giving **spin-spin
coupling** $H'_{\rm hf}\propto\mathbf S_p\!\cdot\!\mathbf S_e$. The good states
diagonalize the grand total $\mathbf F=\mathbf S_p+\mathbf S_e$ (`~QM-13` again):
$$\langle\mathbf S_p\!\cdot\!\mathbf S_e\rangle=\frac{\hbar^2}{2}\big[F(F+1)-\tfrac34-\tfrac34\big],$$
so the **triplet** $F=1$ is raised ($+\tfrac14\hbar^2$) and the **singlet** $F=0$ is
depressed ($-\tfrac34\hbar^2$). The ground state of hydrogen splits by (Griffiths
Eq. 7.97, p.399)
$$\boxed{\;\Delta E_{\rm hf}=\frac{4\,g_p\,\hbar^4}{3\,m_p m_e^2 c^2 a_0^4}\approx 5.9\ \mu\mathrm{eV}\;}$$
— another factor $\sim m_e/m_p$ below fine structure, the last rung of Table 7.1.
The emitted photon (Griffiths Eqs. 7.98–7.99, p.399) has
$$f=\frac{\Delta E_{\rm hf}}{h}\approx1420\ \mathrm{MHz},\qquad
\lambda=\frac cf\approx21\ \mathrm{cm}.$$
This **21-centimetre line** is "among the most pervasive forms of radiation in the
universe" — it maps neutral hydrogen across galaxies. The closed form lands within
$\sim0.1\%$ of the measured $1420.405751\,\mathrm{MHz}$; the residue is QED + proton
structure. (`spin_spin_coupling`, `hyperfine_splitting_eV`, `hyperfine_frequency`,
`hyperfine_wavelength`.)

---
### Why this module sits where it does
It is the **payoff of perturbation theory** (`~QM-15`): three genuinely different
physical mechanisms — special relativity, magnetism, and the proton's spin — all
reduce to first-order energy shifts of the hydrogen levels, each landing on a
number you can look up (the $10.9\,\mathrm{GHz}$ $n=2$ interval, the Landé factors,
the $21\,\mathrm{cm}$ line). The same machinery of *adding angular momenta*
(`~QM-13`) appears twice, as $\mathbf J=\mathbf L+\mathbf S$ (fine structure,
Zeeman) and $\mathbf F=\mathbf I+\mathbf S$ (hyperfine). The exact fine-structure
formula and the *origin* of the Darwin term and $g_e=2$ are deferred to the Dirac
equation (`~QM-22`).
