# NE-05 — Problems

Work each by hand, then check with `code/decay_modes.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P7 are
the seven parts of the book's Chapter 5 Problem 1 (printed 132); P8 is its
Problem 2. Masses from `../data_tables/B1_atomic_masses.csv`,
$c^{2}=931.494043$ MeV/u, $2m_ec^{2}=1.02200$ MeV.

### P1.  $^{210}_{84}\mathrm{Po}\to(?)+{}^{4}_{2}\mathrm{He}$  *(S&F Ch. 5, Prob. 1.1)*
Identify the decay and give the total kinetic energy of the products.
*Check:* `q_alpha(210, 84)`$=5.4071$ MeV; `alpha_kinetic_energy(210, 84)`$=5.3040$ MeV.

**Solution.** Alpha decay. Balancing, $A: 210-4=206$ and $Z: 84-2=82$, so the
daughter is $^{206}_{82}\mathrm{Pb}$ — stable lead, the end of the uranium series.
$$Q_\alpha=\big[M(^{210}\mathrm{Po})-M(^{206}\mathrm{Pb})-M(^{4}\mathrm{He})\big]c^{2}
=5.4071\ \text{MeV},$$
which **is** the total kinetic energy of the products. It divides as
$E_\alpha=Q\,M_D/(M_D+M_\alpha)=5.3040$ MeV to the alpha and $0.1031$ MeV to the
recoiling lead. Polonium-210 is the classic pure alpha emitter: one sharp
5.30 MeV line and essentially no gammas, which is what makes it both a
convenient calibration source and notoriously hazardous if ingested (`~NE-18`).

### P2.  $^{38}_{16}\mathrm{S}\to(?)+{}^{0}_{-1}e+\bar\nu_e$  *(S&F Ch. 5, Prob. 1.2)*
*Check:* `q_beta_minus(38, 16)`$=2.9365$ MeV.

**Solution.** Beta-minus. $A$ is unchanged and $Z$ rises by one, so the daughter
is $^{38}_{17}\mathrm{Cl}$. Atomic masses cancel with no correction [Eq. (5.14)]:
$$Q_{\beta^-}=\big[M(^{38}\mathrm{S})-M(^{38}\mathrm{Cl})\big]c^{2}=2.9365\ \text{MeV}.$$
That 2.94 MeV is shared between the electron and the antineutrino, so the
electron's energy is **continuous** from 0 to 2.9365 MeV, with the endpoint the
only sharp feature. The total kinetic energy of the products is $Q$ in every
decay, but no single product has a fixed share — the contrast with P1.

### P3.  $(?)\to{}^{27}_{13}\mathrm{Al}+{}^{0}_{+1}e+\nu_e$  *(S&F Ch. 5, Prob. 1.3)*
*Check:* `q_beta_plus(27, 14)`$=3.7904$ MeV; `q_electron_capture(27, 14)`$=4.8124$ MeV.

**Solution.** Positron emission, so the parent has the same $A$ and one more
proton: $^{27}_{14}\mathrm{Si}$. With the two-electron-mass penalty [Eq. (5.18)]:
$$Q_{\beta^+}=\big[M(^{27}\mathrm{Si})-M(^{27}\mathrm{Al})\big]c^{2}-2m_ec^{2}
=4.8124-1.0220=3.7904\ \text{MeV}.$$
Since $Q_{\mathrm{EC}}=4.81$ MeV comfortably exceeds 1.022 MeV, **both** positron
emission and electron capture are open here and the nuclide branches (it is
predominantly $\beta^+$). Note the total kinetic energy released to the *charged*
products is 3.79 MeV, not 4.81 — the missing 1.02 MeV went into creating the
positron and shedding an electron, and it reappears as two 511 keV annihilation
photons when the positron stops (`~NE-27`, the basis of PET).

### P4.  $^{145}_{62}\mathrm{Sm}\to{}^{145}_{61}\mathrm{Pm}+(?)$  *(S&F Ch. 5, Prob. 1.4)*
*Check:* `q_electron_capture(145, 62)`$=+0.6166$ MeV but
`q_beta_plus(145, 62)`$=-0.4053$ MeV.

**Solution.** $Z$ falls by one at constant $A$, so this is either $\beta^+$ or EC.
Test both:
$$Q_{\mathrm{EC}}=+0.617\ \text{MeV},\qquad
Q_{\beta^+}=Q_{\mathrm{EC}}-1.022=-0.405\ \text{MeV}.$$
$Q_{\beta^+}<0$, so **positron emission is energetically forbidden** and the
missing product is a neutrino: the decay is electron capture,
$$^{145}_{62}\mathrm{Sm}+e^-\to{}^{145}_{61}\mathrm{Pm}+\nu_e .$$
This is the 1.022 MeV window of §2 of the notes in action. Because $Q_{\mathrm{EC}}$
lands between 0 and 1.022 MeV, capture is the only channel, and the only
detectable radiations are the daughter's x-rays and Auger electrons as the K-shell
vacancy fills.

### P5.  $^{137}_{54}\mathrm{Xe}^{*}\to(?)+{}^{1}_{0}n$, $E^{*}=6.71$ MeV  *(S&F Ch. 5, Prob. 1.5)*
*Check:* `q_neutron_emission(137, 54)`$=-4.0258$ MeV, so with the excitation
$Q=-4.0258+6.71=+2.684$ MeV.

**Solution.** Neutron emission: $A$ falls by one, $Z$ is unchanged, so the
daughter is $^{136}_{54}\mathrm{Xe}$. From the ground state the decay is
**forbidden**,
$$Q_n=\big[M(^{137}\mathrm{Xe})-M(^{136}\mathrm{Xe})-m_n\big]c^{2}=-4.026\ \text{MeV},$$
which is simply minus the neutron separation energy of $^{137}$Xe (`~NE-03`). But
the nucleus starts 6.71 MeV **above** its ground state, and that excitation is
available:
$$Q=E^{*}-S_n=6.71-4.03=+2.68\ \text{MeV}.$$

This is the mechanism of **delayed neutrons**. $^{137}$Xe is produced by the beta
decay of the fission product $^{137}$I, and it is born excited above its neutron
separation energy, so it promptly sheds a neutron. Those neutrons appear on the
timescale of the *precursor's* beta decay — seconds, not microseconds — and they
are what makes a reactor controllable (`~NE-20`). Without them, reactor period
would be set by the ~$10^{-4}$ s prompt neutron lifetime and no mechanical control
system could keep up.

### P6.  $^{108}_{52}\mathrm{Te}\to{}^{107}_{51}\mathrm{Sb}+(?)$, $E^{*}=3.4$ MeV  *(S&F Ch. 5, Prob. 1.6)*
*Check:* `q_proton_emission(108, 52)`$=-2.3148$ MeV, so with the excitation
$Q=+1.085$ MeV.

**Solution.** Both $A$ and $Z$ fall by one, so the emitted particle is a
**proton**. Using the neutral-atom substitution (the proton is charged to a $^1$H
atom, `~NE-04`):
$$Q_p=\big[M(^{108}\mathrm{Te})-M(^{107}\mathrm{Sb})-M(^{1}\mathrm{H})\big]c^{2}
=-2.315\ \text{MeV},$$
forbidden from the ground state, but with $E^{*}=3.4$ MeV supplied,
$$Q=3.4-2.315=+1.085\ \text{MeV}.$$
This is *delayed proton* emission, the proton-rich mirror of P5, and it occurs
for the same reason: beta decay populates a state above the particle separation
energy. It is a signature of nuclides far to the proton-rich side of the valley
of stability (`~NE-02`).

### P7.  $^{60}_{28}\mathrm{Ni}^{*}\to(?)+{}^{0}_{-1}e$, $E^{*}=0.125$ MeV, $BE_e^{K}=8.33$ keV  *(S&F Ch. 5, Prob. 1.7)*
*Check:* the ejected electron carries $0.125-0.00833=0.1167$ MeV.

**Solution.** Neither $A$ nor $Z$ changes, and an electron is emitted: this is
**internal conversion**, not beta decay. The excited nucleus transfers its energy
directly to a K-shell electron rather than emitting a photon, and the electron
leaves with the excitation energy minus its own binding:
$$E_{\mathrm{IC}}=E^{*}-BE_e^{K}=125.0-8.33=116.7\ \text{keV}.$$
The daughter is $^{60}_{28}\mathrm{Ni}$ in its ground state, plus a K-shell
vacancy that promptly fills, emitting nickel x-rays or Auger electrons.

The diagnostic difference from beta decay is decisive: conversion electrons are
**monoenergetic** (one energy per shell — K, L, M lines), while beta electrons
are continuous. Seeing sharp lines on top of a beta continuum is how internal
conversion is identified, and Appendix D lists the two groups separately for
exactly this reason (`conversion_auger_electron` versus `beta`).

### P8.  Gamma recoil  *(S&F Ch. 5, Prob. 2)*
A stationary nucleus of mass $m_n$ de-excites from $E^{*}$ by emitting a photon.
Show $E_\gamma<E^{*}$, derive the relation, and check that the difference is
negligible.
*Check:* for $E^{*}=1.3325$ MeV on a mass-60 nucleus,
$E^{*}-E_\gamma=15.9$ eV.

**Solution.** The photon carries momentum $p_\gamma=E_\gamma/c$, so the nucleus
must recoil with equal and opposite momentum, taking kinetic energy
$E_R=p^{2}/2m_n=E_\gamma^{2}/2m_nc^{2}$. Energy conservation gives
$$E^{*}=E_\gamma+\frac{E_\gamma^{2}}{2m_nc^{2}},$$
so $E_\gamma<E^{*}$ necessarily — some of the excitation always goes into recoil.
Solving the quadratic for $E_\gamma$,
$$E_\gamma=m_nc^{2}\left[\sqrt{1+\frac{2E^{*}}{m_nc^{2}}}-1\right]
\simeq E^{*}\left(1-\frac{E^{*}}{2m_nc^{2}}\right),$$
the expansion holding because $E^{*}\ll m_nc^{2}$.

For the 1.3325 MeV gamma of $^{60}$Ni, $m_nc^{2}=59.93\times931.49=55{,}825$ MeV, so
$$E^{*}-E_\gamma\simeq\frac{(E^{*})^{2}}{2m_nc^{2}}
=\frac{1.3325^{2}}{2(55825)}=1.59\times10^{-5}\ \text{MeV}=15.9\ \text{eV}.$$
That is 12 parts per million — utterly negligible for any energy accounting, which
is why `q_isomeric_transition` simply returns $E^{*}$. It is *not* negligible for
resonant absorption, though: 15.9 eV vastly exceeds the natural linewidth of the
state, so a free nucleus cannot reabsorb its own gamma. Locking the nucleus into
a crystal lattice removes the recoil (the whole lattice takes it) and restores
resonance — the Mössbauer effect.
