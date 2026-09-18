# NE-05 — Radioactive decay modes (notes)

`~NE-04` computed Q-values for reactions in which neutron and proton numbers are
separately conserved, where the neutral-atom substitution works cleanly. Decay
breaks that condition: $\beta^\pm$ and electron capture convert protons into
neutrons and back. Each mode therefore needs its **own** electron-mass
correction, and getting them confused is the standard error in this subject.

This module derives the four corrections, works out how the released energy is
shared, and checks the answers against two independent appendices — masses
(Appendix B) and measured emission energies (Appendix D).

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§5.1–5.4, cited by **printed** page (PDF = printed + 23).

## 1. The four Q-values

| mode | reaction | $Q$ from **atomic** masses | why |
|---|---|---|---|
| $\alpha$ | $^{A}_{Z}\mathrm{P}\to{}^{A-4}_{Z-2}\mathrm{D}+{}^{4}_{2}\mathrm{He}$ | $M(\mathrm{P})-M(\mathrm{D})-M(^4\mathrm{He})$ | electrons cancel |
| $\beta^-$ | $^{A}_{Z}\mathrm{P}\to{}^{A}_{Z+1}\mathrm{D}+e^-+\bar\nu_e$ | $M(\mathrm{P})-M(\mathrm{D})$ | cancel **exactly** |
| $\beta^+$ | $^{A}_{Z}\mathrm{P}\to{}^{A}_{Z-1}\mathrm{D}+e^++\nu_e$ | $M(\mathrm{P})-M(\mathrm{D})-2m_e$ | **two** electron masses |
| EC | $^{A}_{Z}\mathrm{P}+e^-\to{}^{A}_{Z-1}\mathrm{D}+\nu_e$ | $M(\mathrm{P})-M(\mathrm{D})$ | same form as $\beta^-$ |
| IT | $^{A}_{Z}\mathrm{P}^{*}\to{}^{A}_{Z}\mathrm{P}+\gamma$ | $E^{*}$ | no nuclide change |

Each row deserves its reason.

**Alpha** [S&F Eq. (5.7), p. 103]. The daughter is initially a doubly negative
ion — it keeps $Z$ electrons but needs only $Z-2$ — while the alpha is a bare
${}^{4}_{2}\mathrm{He}^{2+}$ that picks up two electrons as it stops. The two
surplus and the two acquired cancel, so atomic masses work directly. The
neglected electron binding energies are tens of eV against MeV.

**Beta-minus** [S&F Eq. (5.14), p. 105]. The daughter ion $[^{A}_{Z+1}D]^+$ is
short one electron, and the emitted $\beta^-$ is exactly that electron. Atomic
masses cancel with **no correction at all** — the cleanest case.

**Beta-plus** [S&F Eq. (5.18), p. 107]. Here the arithmetic bites twice. The
daughter has $Z$ electrons but needs $Z-1$, so it must shed one; and a positron
has been created from nothing. Both cost $m_ec^{2}$:
$$\boxed{\;Q_{\beta^+}=\big[M(\mathrm{P})-M(\mathrm{D})\big]c^{2}-2m_ec^{2},
\qquad 2m_ec^{2}=1.022\ \text{MeV}\;}$$

**Electron capture** [S&F Eq. (5.22), p. 109]. The captured electron was already
part of the parent atom, so nothing extra is needed and the form is identical to
$\beta^-$.

## 2. The 1.022 MeV window — why light nuclides positron-emit and heavy ones capture

$\beta^+$ and EC connect the *same* parent to the *same* daughter, so they always
compete, and they differ by exactly $2m_ec^{2}$
(`test_beta_plus_and_ec_differ_by_exactly_that_penalty`):
$$Q_{\mathrm{EC}}-Q_{\beta^+}=1.022\ \text{MeV}.$$
Therefore:

- $Q_{\mathrm{EC}}<0$ — neither mode is open.
- $0<Q_{\mathrm{EC}}<1.022$ MeV — **electron capture only**. Positron emission
  is energetically forbidden no matter how favourable it looks.
- $Q_{\mathrm{EC}}>1.022$ MeV — both are open and they branch.

The middle window is not a curiosity; it accounts for whole classes of
radionuclides (`test_electron_capture_only_window`):

| nuclide | $Q_{\mathrm{EC}}$ | $Q_{\beta^+}$ | observed |
|---|---|---|---|
| ⁷Be | $+0.862$ | $-0.160$ | pure EC |
| ⁵¹Cr | $+0.753$ | $-0.269$ | pure EC |
| ⁵⁵Fe | $+0.231$ | $-0.791$ | pure EC |
| ¹²⁵I | $+0.186$ | $-0.836$ | pure EC |

All four are pure electron-capture emitters, as predicted. And because EC leaves
no charged particle behind — only a neutrino, plus x-rays and Auger electrons as
the shell vacancy fills — an EC nuclide is nearly invisible to a charged-particle
detector. That is exactly why ¹²⁵I and ⁵¹Cr are used as medical tracers
(`~NE-27`), and why ⁵⁵Fe is a calibration source.

⁴⁰K is the textbook branching case: $Q_{\beta^-}=+1.311$ MeV to ⁴⁰Ca and
$Q_{\mathrm{EC}}=+1.505$ MeV to ⁴⁰Ar, both open. It does both (89% $\beta^-$,
11% EC), and the argon branch is what makes potassium–argon dating possible
(`~NE-07`).

## 3. Sharp lines versus continuous spectra

**Alpha decay is two-body.** The parent is at rest, so the products leave
back-to-back with equal and opposite momenta [S&F Eqs. (5.8)–(5.9)]:
$$Q_\alpha=\tfrac12M_Dv_D^{2}+\tfrac12M_\alpha v_\alpha^{2},\qquad M_Dv_D=M_\alpha v_\alpha .$$
Two equations, two unknowns, and the energy split is fixed
[S&F Eqs. (5.11)–(5.12)]:
$$\boxed{\;E_\alpha=Q_\alpha\frac{M_D}{M_D+M_\alpha}\simeq Q_\alpha\frac{A_D}{A_D+4},
\qquad E_D=Q_\alpha-E_\alpha\;}$$
`alpha_kinetic_energy` and `daughter_recoil_energy`. The alpha takes about 98% of
the energy and emerges with a **single sharp energy**:

| parent | $Q_\alpha$ | $E_\alpha$ | $E_D$ |
|---|---|---|---|
| ²³⁸U | 4.2703 | 4.1985 | 0.0718 |
| ²²⁶Ra | 4.8706 | 4.7844 | 0.0863 |
| ²²²Rn | 5.5903 | 5.4895 | 0.1008 |
| ²¹⁰Po | 5.4071 | 5.3040 | 0.1031 |

These are the numbers printed in every chart of the nuclides, and
`test_alpha_kinetic_energies_match_measured_line_energies` checks them against
Appendix D. The daughter recoil is small but not negligible — ~100 keV is
thousands of times a chemical bond energy, which is why alpha decay shatters the
host molecule and drives radiation damage in solids (`~NE-18`).

**Beta decay is three-body.** The antineutrino shares the energy, so the electron
emerges with a *continuous* spectrum from zero up to an endpoint
[S&F Eq. (5.16)]:
$$(E_{\beta^-})_{\max}=Q_{\beta^-}.$$
Only the endpoint is sharp, and it is the observable that carries the mass
information. This distinction is why alpha spectroscopy identifies nuclides
cleanly while beta spectroscopy does not (`~NE-15`), and historically the missing
energy in the beta spectrum is what forced Pauli to postulate the neutrino.

## 4. Checking the energetics against measurement

The strongest validation available here spans two independent appendices: Q from
Appendix B **masses** against endpoints from Appendix D **spectroscopy**. For
nuclides that decay essentially entirely to the daughter's ground state
(`test_beta_minus_q_matches_endpoints_for_ground_state_emitters`):

| nuclide | $Q_{\beta^-}$ from masses | Appendix D endpoint |
|---|---|---|
| ³H | 18.59 keV | 18.60 keV |
| ¹⁴C | 156.47 keV | 156.50 keV |
| ³²P | 1710.66 keV | 1710.40 keV |
| ⁹⁰Sr | 546.04 keV | 546.00 keV |

Agreement to a few tenths of a keV out of hundreds — from two data sets that
share no inputs.

When the beta feeds an *excited* level the endpoint alone is **not** $Q$; the
gamma cascade carries the remainder. ⁶⁰Co is the standard case: 99.94% of decays
stop 2505.7 keV short of the ⁶⁰Ni ground state, then two gammas cascade down.
$$E_{\beta,\max}+E_{\gamma1}+E_{\gamma2}=317.9+1173.2+1332.5=2823.6\ \text{keV},$$
against $Q_{\beta^-}=2823.9$ keV from the masses — closure to 0.3 keV
(`test_total_decay_energy_closes_for_a_cascade`). This is why ⁶⁰Co is a *gamma*
source despite being a beta emitter: almost all the decay energy comes out as
the two photons.

> **One place it does not close.** For ¹³⁷Cs, Appendix D's endpoints imply a
> total decay energy of 1173.2 keV while Appendix B's masses give 1176.5 keV — a
> 3.3 keV (0.3%) disagreement between the two evaluations. The modern value,
> 1175.6 keV, lies between them.
> `test_cesium137_shows_a_small_appendix_disagreement` records the gap rather
> than hiding it inside a loose tolerance.

## 5. Predicting the mode

`allowed_decay_modes` returns every mode with $Q>0$; `dominant_decay_mode` picks
the largest. Energetics alone gets the *direction* right across the chart
(`test_dominant_mode_agrees_with_observation`): $\beta^-$ for the neutron-rich
side (³H, ¹⁴C, ⁹⁰Sr, ¹³⁷Cs, ⁶⁰Co), $\alpha$ for the heavy actinides (²³⁸U,
²²⁶Ra, ²¹⁰Po), EC for the proton-rich light nuclides (⁷Be, ⁵⁵Fe).

But a positive $Q$ says only that a mode is **permitted**. Two caveats carry
forward:

- **Barriers.** ²⁰⁸Pb has $Q_\alpha=+0.52$ MeV yet is observationally stable,
  because the alpha must tunnel (`~NE-03` P8). Rate is not energetics.
- **Selection rules.** Angular-momentum and parity changes can suppress an
  energetically favourable beta transition by many orders of magnitude — the
  reason ¹³⁷Cs takes 30 years and ¹³⁷ᵐBa 2.6 minutes.

Which way a nuclide decays is set by the mass parabolas of `~NE-02`: a nuclide on
the neutron-rich side of the valley floor runs $\beta^-$ downhill, one on the
proton-rich side runs $\beta^+$/EC, and the two curves of an even-$A$ isobar are
why odd-odd nuclides like ⁴⁰K can go both ways.

## Where this goes

- `~NE-06` — how *fast* these decays go: the decay constant, half-life and activity.
- `~NE-07` — chains of them, and where they terminate.
- `~NE-09` — fission fragments are born far to the neutron-rich side, so they
  cascade by $\beta^-$; a few emit delayed neutrons.
- `~NE-17` — Appendix D's per-decay energy yields, used here for validation, are
  the input to internal dose calculations.
- `~NE-15` — sharp alpha lines versus continuous beta spectra, and what each
  detector type can do with them.
