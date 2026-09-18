# NE-01 — Atomic models (notes)

Nuclear engineering begins with a picture of the atom, and the picture that
matters is the one that failed and the one that replaced it. By 1910 the atom was
known to contain electrons and to be electrically neutral, but nothing was known
about how the positive charge was arranged. Two experiments settled it: **alpha
scattering**, which put the positive charge in a nucleus $10^{4}$ times smaller
than the atom, and the **hydrogen emission spectrum**, whose sharp lines no
classical orbit could produce. Bohr's model reconciled them well enough to
predict hydrogen's spectrum to eight significant figures — and its failures are
what make `~QM-08` necessary.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw, *Fundamentals
of Nuclear Science and Engineering*, 3rd ed., §3.1, cited by **printed** page
(PDF page = printed + 23).

## 1. Why the plum-pudding atom had to go

In Thomson's model the positive charge is smeared through the whole atomic
volume, so an alpha particle crossing a foil feels only many small deflections.
For a gold foil $4\times10^{-5}$ cm thick, the probability of scattering by at
least an angle $\phi$ works out to [S&F p. 58]
$$P(\ge\phi)=e^{-\phi/\phi_m},\qquad \phi_m\simeq1^{\circ},$$
which is `thomson_scattering_probability(phi_deg)`. At $\phi=90^{\circ}$ this is
$$P\simeq e^{-90}\approx 8\times10^{-40},$$
an impossibility. Geiger and Marsden measured **one alpha in 8000** scattered
past $90^{\circ}$ — larger by 36 orders of magnitude
(`test_thomson_model_fails_by_36_orders_of_magnitude`). A backscatter needs the
whole positive charge concentrated in one small, massive lump, and Rutherford
concluded in 1911 that it sits within a radius of about $10^{-12}$ cm while the
electrons orbit at about $10^{-8}$ cm [S&F p. 58]. That factor of $10^{4}$ in
radius — $10^{12}$ in volume — is why the nucleus can be treated as a point in
`~NE-11` and why nuclear energies are a million times chemical ones.

## 2. Bohr's three postulates

Rutherford's atom is unstable classically: an orbiting electron accelerates, and
an accelerating charge radiates, so it should spiral in within $\sim10^{-9}$ s
while emitting a *continuous* spectrum. Neither happens. Bohr's response
(1913–15) was to keep the orbits and quantize them [S&F p. 59]:

1. the electron moves in a circular orbit obeying classical mechanics;
2. only orbits with angular momentum $L=n h/2\pi$ are allowed;
3. radiation is emitted only on a transition between allowed orbits, with
   $E=h\nu$ equal to the energy difference.

Postulate 1 balances the Coulomb attraction against the centripetal requirement
[S&F Eq. (3.2)],
$$\frac{m_e v^{2}}{r}=\frac{Ze^{2}}{4\pi\epsilon_0 r^{2}},$$
checked in `test_coulomb_balances_centripetal_force`; postulate 2 is
[S&F Eq. (3.3)]
$$L\equiv m_e v r = n\frac{h}{2\pi},\qquad n=1,2,3,\dots$$
(`bohr_angular_momentum`, `test_angular_momentum_is_quantized`). Solving the two
together for $r$ and $v$ gives [S&F Eq. (3.4)]
$$\boxed{\;v_n=\frac{Ze^{2}}{2\epsilon_0 n h},\qquad
r_n=\frac{n^{2}h^{2}\epsilon_0}{\pi m_e Z e^{2}}\;}$$
— `bohr_velocity(n, Z)` and `bohr_radius(n, Z)`. The scalings $r_n\propto n^2/Z$
and $v_n\propto Z/n$ are the whole content of the model's geometry
(`test_radius_and_velocity_scaling`). For $n=1,Z=1$,
$$r_1=5.2918\times10^{-11}\ \text{m},\qquad v_1=2.1877\times10^{6}\ \text{m/s},$$
matching the book's $5.293\times10^{-11}$ m and $2.187\times10^6$ m/s [S&F p. 60].
$r_1$ is the **Bohr radius**, and it sets the size of every atom.

## 3. The energy levels

The electron carries potential energy $V_n=-Ze^{2}/(4\pi\epsilon_0 r_n)$ and
kinetic energy $T_n=\tfrac12 m_e v_n^{2}$, which the force balance turns into
$T_n=\tfrac12 Ze^{2}/(4\pi\epsilon_0 r_n)=-\tfrac12 V_n$. Their sum is
[S&F Eq. (3.5)]
$$\boxed{\;E_n=T_n+V_n=-\frac{1}{2}\frac{Ze^{2}}{4\pi\epsilon_0 r_n}
=-\frac{m_e (Ze^{2})^{2}}{8\epsilon_0^{2}n^{2}h^{2}}
=-13.606\,\frac{Z^{2}}{n^{2}}\ \text{eV}\;}$$
which is `bohr_energy(n, Z)`. Three things are worth pausing on.

**The relation $T=-E$, $V=2E$** is the virial theorem for a $1/r$ potential, and
it holds orbit by orbit (`test_virial_theorem`). It is why the binding energy of
a level equals its kinetic energy — a fact reused for nucleons in `~NE-03`.

**The sign.** $E_n<0$ because the electron is bound; the zero of energy is the
freed electron at rest at infinite separation. The work to remove it is
$-E_n$, so `ionization_energy(Z, n)` $=-E_n$. For hydrogen this is
$13.606$ eV, the measured ionization energy [S&F p. 60]. The book's Example 3.1
asks for singly ionized helium, $Z=2$, $n=1$: the $Z^{2}$ scaling gives
$4\times13.606=54.42$ eV (`test_helium_ion_ionization_energy`).

**The $Z^{2}/n^{2}$ scaling** means inner-shell binding energies grow rapidly
with $Z$ — the reason heavy elements have keV-scale K-shell edges, which is what
produces the photoelectric edges tabulated in `data_tables/C3_*.csv` and used in
`~NE-12`.

## 4. The spectrum, and the model's one triumph

By postulate 3 a transition $n\to n_o$ with $n>n_o$ emits [S&F Eq. (3.6)]
$$h\nu_{n\to n_o}=E_n-E_{n_o}
=\frac{m_e Z^{2}e^{4}}{8\epsilon_0^{2}h^{2}}
\left(\frac{1}{n_o^{2}}-\frac{1}{n^{2}}\right),$$
`transition_energy(n_lo, n_hi, Z)`, and since $1/\lambda=\nu/c$ [S&F Eq. (3.7)]
$$\frac{1}{\lambda_{n\to n_o}}
=\frac{m_e Z^{2}e^{4}}{8\epsilon_0^{2}ch^{3}}
\left(\frac{1}{n_o^{2}}-\frac{1}{n^{2}}\right)
=R_\infty Z^{2}\left(\frac{1}{n_o^{2}}-\frac{1}{n^{2}}\right).$$
This has *exactly* the form of the empirical formula [S&F Eq. (3.1)]
$$\frac{1}{\lambda}=R_H\left(\frac{1}{n_o^{2}}-\frac{1}{n^{2}}\right)$$
that spectroscopists had fitted to hydrogen decades earlier, with
$R_H=10\,967\,758$ m$^{-1}$ measured. Deriving a fitted constant from
$m_e$, $e$, $h$ and $\epsilon_0$ is the model's claim to fame, and
`test_transitions_reproduce_the_rydberg_formula` checks that
`transition_wavelength` and `rydberg_wavelength` agree to machine precision.
Each $n_o$ labels a series [S&F Table 3.1, p. 59] — `series_name(n_lo)`:

| $n_o$ | series | where it lies |
|---|---|---|
| 1 | Lyman | ultraviolet |
| 2 | Balmer | visible and near ultraviolet |
| 3 | Paschen | infrared |
| 4 | Brackett | infrared |
| 5 | Pfund | infrared |

Letting $n\to\infty$ gives the **series limit** $\lambda=n_o^{2}/(R Z^{2})$
(`series_limit_wavelength`), the shortest wavelength in a series and the
ionization threshold from level $n_o$: 91.2 nm for Lyman, 364.7 nm for Balmer.

## 5. The reduced-mass correction — and a misprint

The derivation above assumes an infinitely heavy nucleus, so the electron circles
a fixed point. In fact both orbit their common centre of mass, and the correct
one-body reduction replaces $m_e$ by the **reduced mass** [S&F p. 60]
$$\mu_e=\frac{m_e m_p}{m_e+m_p},$$
`reduced_mass(m1, m2)`. This turns $R_\infty$ into $R_H$:
$$R_H=\frac{\mu_e e^{4}}{8\epsilon_0^{2}ch^{3}}=\frac{\mu_e}{m_e}R_\infty .$$
Numerically $R_\infty=1.0973732\times10^{7}$ m$^{-1}$ and, with
$\mu_e/m_e=0.999455679$, $R_H=1.0967758\times10^{7}$ m$^{-1}$ — the measured
value to eight figures, exactly as the book claims. A 0.05% correction sounds
negligible until you notice it moves Balmer-$\alpha$ from 656.11 nm to
656.47 nm, and the observed line is at 656.3 nm (air) / 656.47 nm (vacuum)
[S&F Fig. 3.4]: the correction is the difference between agreeing with experiment
and not (`test_balmer_alpha_is_the_red_line`).

> **Misprint.** S&F p. 60 prints $\mu_e = 0.999445568\,m_e$. That ratio gives
> $R_H = 10\,967\,647$ m$^{-1}$, missing the value printed two lines later by
> $111$ m$^{-1}$ — about $10^{5}$ times the quoted precision. The correct ratio
> is $0.999455679$, and it reproduces $10\,967\,758$ m$^{-1}$ exactly.
> `test_reduced_mass_ratio_reproduces_book_R_H` asserts both halves of this.

Because $\mu$ depends on the nucleus, the same transition sits at slightly
different wavelengths in hydrogen and deuterium — the **isotope shift**, which is
how deuterium was discovered.

## 6. Where the model breaks, and what survives

The Bohr atom gets hydrogen's energies right and essentially everything else
wrong. It cannot explain line *intensities*, the splitting of lines in a magnetic
field, or any multi-electron atom. Sommerfeld's elliptic orbits [S&F §3.1.5,
p. 61] add a second quantum number and buy a little more agreement, but the
patch-up ends there: the electron does not follow a trajectory at all, and the
quantum-mechanical atom [S&F §3.1.6, p. 62] replaces orbits with orbitals — the
subject of `~QM-08`.

Two results do survive intact, and both are used downstream:

- **The energy scale.** $E_n\propto Z^{2}/n^{2}$ with a 13.6 eV prefactor fixes
  atomic binding energies in the eV–keV range. Nuclear binding energies are
  MeV-scale (`~NE-03`) — a factor of $10^{6}$, and the entire reason nuclear
  power is worth the trouble.
- **The length scale.** $r_1=0.529$ Å sets atomic size; the nucleus is $10^{4}$
  times smaller. That separation is what lets `~NE-11` treat a nucleus as a
  structureless scattering centre with a cross section, and what makes the
  "atom is mostly empty space" statement quantitative.

Finally, the consistency check the book performs [S&F p. 60]: $v_1/c$ is
$$\frac{v_1}{c}=\frac{e^{2}}{2\epsilon_0 hc}=\alpha=\frac{1}{137.04},$$
the fine-structure constant (`fine_structure_constant`). Small enough that
non-relativistic mechanics was justified — but for a hydrogen-like ion with
$Z=92$, $v_1/c=0.67$ and it is not (`test_fine_structure_constant_is_v1_over_c`).
Inner-shell electrons in heavy atoms are genuinely relativistic, which is why
`~RE-06` is a prerequisite for the rest of this trunk.

## Where this goes

- `~NE-02` — the same "model it, then test it against data" move applied to the
  nucleus: the liquid drop model and the chart of the nuclides.
- `~NE-03` — nuclear binding energies, $10^{6}$ times the atomic ones computed here.
- `~NE-05` — internal conversion and electron capture, which involve exactly these
  atomic levels; `~NE-12` — photoelectric absorption edges are ionization energies
  of inner shells.
- `~QM-08` — the quantum atom that replaces Bohr's orbits with orbitals.
