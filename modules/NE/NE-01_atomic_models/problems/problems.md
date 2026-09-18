# NE-01 — Problems

Work each by hand, then check with `code/atomic_models.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page.
Problems P1–P6 follow the book's own Chapter 3 problems 1–5 and 8 (printed 77);
P7–P8 are added to close the loop on the model's self-consistency.

Throughout, $E_n=-13.606\,Z^{2}/n^{2}$ eV, $r_n=n^{2}a_0/Z$ with
$a_0=5.2918\times10^{-11}$ m, and $R_H=1.0967758\times10^{7}$ m$^{-1}$.

### P1.  The Lyman series  *(S&F Ch. 3, Prob. 1)*
Estimate the wavelengths of the first three lines of the Lyman series
($n=2,3,4\to n_o=1$) and the photon energy of each. Use the reduced-mass
constant $R_H$, not $R_\infty$.
*Check:* `transition_wavelength(1, n, nuclear_mass=M_P)*1e9` gives
$121.57,\,102.57,\,97.25$ nm and `transition_energy(1, n, nuclear_mass=M_P)`
gives $10.199,\,12.087,\,12.748$ eV.

**Solution.** From $1/\lambda=R_H(1/1^{2}-1/n^{2})$ with $R_H=1.0967758\times10^{7}$ m$^{-1}$:
$$n=2:\ \frac1\lambda=R_H\Big(1-\tfrac14\Big)=\tfrac34R_H \Rightarrow \lambda=\frac{4}{3R_H}=121.57\ \text{nm},$$
$$n=3:\ \lambda=\frac{9}{8R_H}=102.57\ \text{nm},\qquad
n=4:\ \lambda=\frac{16}{15R_H}=97.25\ \text{nm}.$$
The energies follow from $E=hc/\lambda$, or directly from the level differences
$E=13.606(1-1/n^{2})$ eV: $10.199$, $12.087$, $12.748$ eV. All three are
ultraviolet — the Lyman series lies entirely below 122 nm, which is why hydrogen
is transparent to visible light but opaque in the far UV. These match the Check.

### P2.  The first Bohr orbit  *(S&F Ch. 3, Prob. 2)*
For the $n=1$ orbit of hydrogen find (a) the radius in metres, (b) the total
energy in eV, and (c) the energy needed to ionize the atom from this state.
*Check:* `bohr_radius(1)`$=5.2918\times10^{-11}$ m, `bohr_energy(1)`$=-13.6057$ eV,
`ionization_energy(1)`$=13.6057$ eV.

**Solution.** (a) With $n=1$, $Z=1$ in $r_n=n^{2}h^{2}\epsilon_0/(\pi m_eZe^{2})$,
$$r_1=\frac{(6.6261\times10^{-34})^{2}(8.8542\times10^{-12})}
{\pi(9.1094\times10^{-31})(1.6022\times10^{-19})^{2}}=5.2918\times10^{-11}\ \text{m},$$
the Bohr radius, $0.529$ Å. (b) From Eq. (3.5),
$E_1=-m_ee^{4}/(8\epsilon_0^{2}h^{2})=-13.606$ eV. (c) Ionization means moving
the electron to $n=\infty$, where $E_\infty=0$; the work required is
$$E_\infty-E_1=0-(-13.606)=13.606\ \text{eV},$$
which is the measured ionization energy of hydrogen [S&F p. 60]. The agreement of
(b) with (c) is not a coincidence — it is the definition of the binding energy.

### P3.  First excitation  *(S&F Ch. 3, Prob. 3)*
What photon energy raises the hydrogen electron from $n=1$ to $n=2$?
*Check:* `transition_energy(1, 2)`$=10.2043$ eV.

**Solution.** $$\Delta E=E_2-E_1=-\frac{13.606}{4}-(-13.606)
=13.606\Big(1-\tfrac14\Big)=13.606\times\tfrac34=10.204\ \text{eV}.$$
Note this is **75%** of the ionization energy: the first excited state already
sits three-quarters of the way to the continuum, because the levels crowd as
$1/n^{2}$. A 10.2 eV photon is the Lyman-$\alpha$ line of P1 read backwards —
absorption and emission are the same transition.

### P4.  De Broglie waves and postulate 2  *(S&F Ch. 3, Prob. 4)*
Compute the de Broglie wavelength $\lambda=h/(m_ev_1)$ of the electron in the
first Bohr orbit and compare it with the circumference $2\pi r_1$. What does the
comparison say about Bohr's quantization postulate?
*Check:* both equal $3.3249\times10^{-10}$ m; their ratio is $1.000000000000$.

**Solution.** With $v_1=2.1877\times10^{6}$ m/s,
$$\lambda_{\text{dB}}=\frac{h}{m_ev_1}
=\frac{6.6261\times10^{-34}}{(9.1094\times10^{-31})(2.1877\times10^{6})}
=3.3249\times10^{-10}\ \text{m},$$
while $2\pi r_1=2\pi(5.2918\times10^{-11})=3.3249\times10^{-10}$ m. They are
**exactly equal**, and the identity is algebraic, not numerical: postulate 2 says
$m_evr=nh/2\pi$, so
$$2\pi r=\frac{nh}{m_ev}=n\lambda_{\text{dB}} .$$
An allowed orbit is one whose circumference holds a whole number of electron
wavelengths — a standing wave that closes on itself. Bohr's *ad hoc* postulate is
de Broglie's condition in disguise, which is why the model works at all and the
hint that the real theory is a wave theory (`~QM-08`).

### P5.  Series limits  *(S&F Ch. 3, Prob. 5)*
Find the limiting (smallest) wavelength of the Lyman, Balmer and Paschen series.
*Check:* `series_limit_wavelength(n)*1e9` gives $91.18,\,364.71,\,820.59$ nm for
$n=1,2,3$.

**Solution.** The limit is the $n\to\infty$ transition, where $1/n^{2}\to0$:
$$\frac{1}{\lambda_{\min}}=\frac{R_H}{n_o^{2}}
\quad\Longrightarrow\quad \lambda_{\min}=\frac{n_o^{2}}{R_H}.$$
So $\lambda_{\min}=1/R_H=91.18$ nm (Lyman), $4/R_H=364.71$ nm (Balmer) and
$9/R_H=820.59$ nm (Paschen). Physically the limit is the **ionization edge** from
level $n_o$: a photon of exactly this wavelength strips the electron to rest at
infinity, and anything shorter ionizes it with kinetic energy left over. The
Balmer limit at 364.7 nm is where the visible hydrogen lines pile up and the
continuum begins.

### P6.  The hydrogen mass defect  *(S&F Ch. 3, Prob. 8)*
The mass of a ${}^{1}$H atom is $1.007825032$ u (Appendix B); a free proton is
$1.0072764669$ u and an electron $5.485799\times10^{-4}$ u (Table A.1). Estimate
the electron's binding energy from the mass difference, compare it with the Bohr
value, and give the fraction of the atom's mass lost on binding.
*Check:* the Bohr binding energy $13.6057$ eV corresponds to
$1.4606\times10^{-8}$ u, i.e. $1.449\times10^{-8}$ of the atomic mass.

**Solution.** Adding the constituents,
$$m_p+m_e=1.0072764669+0.0005485799=1.0078250468\ \text{u},$$
against the tabulated atom $1.007825032$ u. The difference is
$$\Delta m = 1.5\times10^{-8}\ \text{u},$$
which is right at the last digit of the tabulated masses — the mass table simply
does not carry enough figures to resolve it. Converting the Bohr energy instead,
$$\Delta m=\frac{13.6057\ \text{eV}}{931.494043\times10^{6}\ \text{eV/u}}
=1.4606\times10^{-8}\ \text{u},$$
a fraction $1.4606\times10^{-8}/1.007825=1.449\times10^{-8}$ of the atom. **This
is the point of the problem:** chemical/atomic binding changes mass by one part
in $10^{8}$, which is why chemists may treat mass as conserved. Nuclear binding
changes it by nearly one part in $10^{2}$ (`~NE-03`) — six orders of magnitude
larger, and the reason mass–energy bookkeeping is unavoidable in this trunk.

### P7.  Is the classical treatment legitimate?  *(S&F p. 60)*
Show that $v_1/c$ for hydrogen equals the fine-structure constant $\alpha$, and
decide whether a non-relativistic treatment is defensible for hydrogen and for
hydrogen-like uranium ($Z=92$).
*Check:* `fine_structure_constant()`$=0.00729735=$`bohr_velocity(1)/C`,
$1/\alpha=137.036$; `is_nonrelativistic(1)` is `True` but
`is_nonrelativistic(1, Z=92)` is `False`.

**Solution.** From $v_n=Ze^{2}/(2\epsilon_0nh)$ with $n=Z=1$,
$$\frac{v_1}{c}=\frac{e^{2}}{2\epsilon_0hc}\equiv\alpha=7.297\times10^{-3}
=\frac{1}{137.04}.$$
The relativistic correction enters at order $(v/c)^{2}\approx5\times10^{-5}$, so
for hydrogen the classical orbit is good to about one part in $10^{4}$ — S&F's
justification on p. 60. But $v_1\propto Z$, so for $Z=92$
$$\frac{v_1}{c}=92\alpha=0.67,$$
giving $\gamma\approx1.35$. Inner-shell electrons in heavy atoms move at
appreciable fractions of $c$, which is why K-shell binding energies in lead and
uranium (tens of keV) cannot be obtained from the non-relativistic $Z^{2}$ scaling
and why `~RE-06` is a prerequisite here.

### P8.  How badly the plum pudding fails  *(S&F p. 58)*
Thomson's model gives $P(\ge\phi)=e^{-\phi/\phi_m}$ with $\phi_m\simeq1^{\circ}$.
Compare its prediction for $\phi\ge90^{\circ}$ with the measured 1 alpha in 8000,
and separately show that a classical Rutherford atom would collapse in far fewer
than $10^{-9}$ s worth of orbits.
*Check:* `thomson_scattering_probability(90.0)`$=8.194\times10^{-40}$ versus
$1.25\times10^{-4}$ measured — a ratio of $1.5\times10^{35}$;
`bohr_orbital_period(1)`$=1.5198\times10^{-16}$ s.

**Solution.** The Thomson estimate is
$$P(\ge90^{\circ})=e^{-90/1}=e^{-90}=8.19\times10^{-40},$$
against the observed $1/8000=1.25\times10^{-4}$: wrong by a factor of
$1.5\times10^{35}$. No amount of experimental error covers 35 orders of
magnitude, so the *model* is wrong — the positive charge must be concentrated
hard enough to turn an alpha around, which requires it packed inside
$\sim10^{-12}$ cm rather than spread over $10^{-8}$ cm.

For the collapse, the $n=1$ orbital period is
$$T=\frac{2\pi r_1}{v_1}=\frac{2\pi(5.2918\times10^{-11})}{2.1877\times10^{6}}
=1.52\times10^{-16}\ \text{s},$$
so in the $\sim10^{-9}$ s a classical radiating electron would survive it
completes $10^{-9}/1.52\times10^{-16}\approx6.6\times10^{6}$ revolutions — and
then the atom is gone. Since atoms manifestly persist, and since the emitted
spectrum is discrete rather than the continuum a spiralling charge would radiate,
classical electrodynamics must fail inside the atom. That is the pressure Bohr's
postulates were invented to relieve.
