# NE-03 — Binding energy and separation energies (notes)

`~NE-02` built a *model* of nuclear binding. This module measures it. Everything
here comes from one fact — **a nucleus weighs less than its parts** — and one
table, the 2931 measured atomic masses of Appendix B. From those alone we get
the binding-energy curve that explains why fission and fusion both release
energy, and the separation energies that expose the pairing and shell structure
the liquid drop model could only hint at.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§4.1–4.3, cited by **printed** page (PDF = printed + 23). Masses from
`../data_tables/B1_atomic_masses.csv`.

## 1. Atomic masses, nuclear masses, and why we use the former

Appendix B tabulates **atomic** masses $M({}^{A}_{Z}\mathrm{X})$ — nucleus plus
$Z$ electrons — not nuclear masses $m({}^{A}_{Z}\mathrm{X})$. The two are related
by [S&F Eq. (4.8), p. 81]
$$M({}^{A}_{Z}\mathrm{X})=m({}^{A}_{Z}\mathrm{X})+Zm_e-\frac{BE_{Ze}}{c^{2}},$$
where $BE_{Ze}$ is the total electron binding energy. `atomic_to_nuclear_mass`
implements this, dropping the last term. That is safe by a wide margin: ionizing
hydrogen costs 13.6 eV, a mass change of
$$\frac{13.6\ \text{eV}}{9.315\times10^{8}\ \text{eV/u}}=1.46\times10^{-8}\ \text{u},$$
negligible even against the electron mass ($5.5\times10^{-4}$ u), let alone the
atom ($\approx1$ u). `electron_binding_fraction` quantifies it.

Nuclear masses are not measured directly — mass spectrometry weighs ions, so
atomic masses are what is known to high accuracy. The whole of nuclear energetics
is therefore written in atomic masses, and the electrons are made to cancel.

## 2. Binding energy from measured masses

Assembling a nucleus from $Z$ protons and $N=A-Z$ neutrons releases energy
[S&F Eq. (4.9)]:
$$Z\,\text{protons}+(A-Z)\,\text{neutrons}\longrightarrow{}^{A}_{Z}\mathrm{X}+BE .$$
The energy comes out of the mass, so [S&F Eq. (4.10)]
$$\frac{BE}{c^{2}}=Zm_p+(A-Z)m_n-m({}^{A}_{Z}\mathrm{X}),$$
the **mass defect**. Substituting Eq. (4.8) on both sides replaces each proton by
a hydrogen *atom*, and the $Z$ electron masses cancel; what is left over is
$[Z\,BE_{1e}-BE_{Ze}]/c^{2}$, which is dropped for the two reasons above — the
electron binding energies largely cancel, and both are $10^{6}$ times smaller than
nuclear binding. The working formula is [S&F Eq. (4.12), p. 81]
$$\boxed{\;BE({}^{A}_{Z}\mathrm{X})=\big[ZM({}^{1}_{1}\mathrm{H})+(A-Z)m_n
-M({}^{A}_{Z}\mathrm{X})\big]c^{2}\;}$$
— `binding_energy(A, Z)`, with $c^{2}=931.494043$ MeV/u. Worked through Appendix B:

| nuclide | $M$ (u) | defect (u) | $BE$ (MeV) | $BE/A$ (MeV) |
|---|---|---|---|---|
| ²H | 2.014102 | 0.002388 | 2.22 | 1.112 |
| ⁴He | 4.002603 | 0.030377 | 28.30 | 7.074 |
| ¹²C | 12.000000 | 0.098940 | 92.16 | 7.680 |
| ⁵⁶Fe | 55.934942 | 0.528456 | 492.25 | 8.790 |
| ²⁰⁸Pb | 207.976636 | 1.756796 | 1636.45 | 7.868 |
| ²³⁸U | 238.050783 | 1.934198 | 1801.69 | 7.570 |

Note the scale. Uranium's mass defect is **1.93 u** — nearly two nucleons'
worth, about 0.8% of the atom. Compare the $1.4\times10^{-8}$ u of atomic
binding from §1: six orders of magnitude, the same ratio `~NE-01` found between
eV and MeV. Mass is conserved to excellent approximation in chemistry and
manifestly not in nuclear physics.

> **A book-internal inconsistency.** Table A.1 (p. 555) gives
> $m_n=1.008\,664\,915\,6$ u; Appendix B gives $1.008\,664\,923\,3$ u. The gap is
> $7.7\times10^{-9}$ u $=7.2$ eV — irrelevant against MeV binding energies, but
> it means `binding_energy(1, 0)` is not *identically* zero. Which table a
> calculation leans on is worth knowing;
> `test_free_nucleons_have_zero_binding_energy` pins the size of the effect.

## 3. The curve, and the peak that is not iron

`binding_energy_per_nucleon` over the whole table gives the most important curve
in nuclear engineering: $BE/A$ rises steeply to about 8.8 MeV near $A\approx60$,
then declines slowly to 7.6 MeV at uranium. `~NE-02` explained the shape
(surface penalty dying away, Coulomb penalty growing). Two consequences:

- **Fusing** light nuclei moves up the curve → energy out (`~NE-10`).
- **Fissioning** heavy nuclei also moves up → energy out (`~NE-09`). Splitting
  ²³⁸U ($7.57$ MeV/nucleon) into two $A\approx119$ fragments ($\approx8.5$
  MeV/nucleon) gains about $0.9\times238\approx210$ MeV.

`most_bound_nuclide()` returns **⁶²Ni at 8.7945 MeV/nucleon**, not ⁵⁶Fe
(8.7903). The popular claim that iron is the most bound nuclide is off by one
entry; the top of the curve is so flat that ⁵⁶Fe, ⁵⁸Fe and ⁶²Ni lie within 0.005
MeV/nucleon of each other (`test_most_bound_nuclide_is_nickel_62`). Iron's
cosmic abundance is set by stellar *kinetics* — the ⁵⁶Ni decay chain in
supernovae — not by a binding-energy record (`~NE-10`).

## 4. Separation energies: the interesting quantity

$BE/A$ is an average, and averages hide structure. The energy to remove **one**
neutron is far more revealing [S&F Eq. (4.13), p. 87]:
$$S_n({}^{A}_{Z}\mathrm{X})=\big[M({}^{A-1}_{\ \ Z}\mathrm{X})+m_n
-M({}^{A}_{Z}\mathrm{X})\big]c^{2},$$
which in terms of binding energies is simply [S&F Eq. (4.14)]
$$\boxed{\;S_n({}^{A}_{Z}\mathrm{X})=BE({}^{A}_{Z}\mathrm{X})
-BE({}^{A-1}_{\ \ Z}\mathrm{X})\;}$$
— `neutron_separation_energy(A, Z)`, with the two formulations agreeing to
machine precision (`test_separation_energy_two_formulations_agree`). $S_n$ is the
nuclear analogue of an ionization energy (`~NE-01`): the cost of removing the
*last* particle, not the average cost per particle.

**Example 4.3** [S&F p. 87]: for ¹⁶O,
$$S_n=[15.0030654+1.00866492-15.9949146]\ \text{u}\times931.5\ \text{MeV/u}
=15.66\ \text{MeV},$$
which `neutron_separation_energy(16, 8)` reproduces exactly. The book calls this
"exceptionally high", and it is — nearly twice the 7.98 MeV/nucleon average,
because ¹⁶O is doubly magic and removing a neutron breaks the $N=8$ closure. The
very next neutron, in ¹⁷O, costs only 4.14 MeV.

`proton_separation_energy`, `two_neutron_separation_energy` and
`alpha_separation_energy` are the same construction for other emitted fragments.

## 5. What separation energies expose

**Pairing.** Along the oxygen isotopes ($Z=8$):

| $A$ | $N$ | $S_n$ (MeV) | $N$ parity |
|---|---|---|---|
| 15 | 7 | 13.22 | odd |
| 16 | 8 | 15.66 | even |
| 17 | 9 | 4.14 | odd |
| 18 | 10 | 8.04 | even |
| 19 | 11 | 3.96 | odd |
| 20 | 12 | 7.61 | even |

$S_n$ **alternates**, high for even $N$ and low for odd $N$, by 3–4 MeV. Adding a
neutron to an odd-$N$ nucleus completes a pair and releases the pairing energy;
adding one to an even-$N$ nucleus starts a new pair and does not.
`pairing_stagger` measures the alternation, which is $\approx2a_p/\sqrt A$ — the
direct experimental signature of `~NE-02`'s pairing term, visible without any
model at all. Because the stagger obscures everything else, $S_{2n}$
(`two_neutron_separation_energy`) is the smooth quantity in which trends are read.

**Shell closures.** $S_n$ falls off a cliff just past a magic neutron number:

| nuclide | $N$ | $S_n$ (MeV) |
|---|---|---|
| ¹⁴⁰Ce | 82 | 9.20 |
| ¹⁴¹Ce | 83 | 5.43 |
| ²⁰⁸Pb | 126 | 7.37 |
| ²⁰⁹Pb | 127 | 3.94 |

The last neutron *inside* a closed shell is tightly held; the first one *outside*
is barely held at all — exactly as the first electron outside a noble-gas shell
is loosely bound (`test_shell_closure_drops_the_separation_energy`). This is why
magic nuclides have small neutron-capture cross sections (visible in
`../data_tables/C1_thermal_neutron_cross_sections.csv`) and why they act as
bottlenecks in stellar neutron capture, producing the abundance peaks of the
s-process (`~NE-10`).

**Alpha instability.** `alpha_separation_energy` is
$$S_\alpha=BE(A,Z)-BE(A-4,Z-2)-BE(4,2),$$
the cost of removing an alpha *as a unit*. Because ⁴He is itself very tightly
bound (28.3 MeV for four nucleons), $S_\alpha$ goes **negative** for heavy
nuclides — the nucleus is energetically unstable to alpha emission, with
$Q_\alpha=-S_\alpha$:

| nuclide | $S_\alpha$ (MeV) |
|---|---|
| ⁵⁶Fe | $+7.61$ |
| ¹²⁰Sn | $+4.81$ |
| ¹⁵⁰Sm | $-1.45$ |
| ²⁰⁸Pb | $-0.52$ |
| ²²⁶Ra | $-4.87$ |
| ²³⁸U | $-4.27$ |

Even ²⁰⁸Pb is *energetically* alpha-unstable, by 0.5 MeV; it survives because the
Coulomb barrier makes the tunnelling lifetime astronomically long (`~NE-05`).
Energetic instability and observed instability are different statements, and the
gap between them is the entire content of alpha-decay theory.

## Where this goes

- `~NE-04` — Q-values, which are exactly these mass differences applied to
  general reactions rather than to nucleon removal.
- `~NE-05` — $Q_\alpha=-S_\alpha$ sets alpha decay energies; the same machinery
  in atomic masses gives beta and electron-capture energetics.
- `~NE-09` — the $BE/A$ step from uranium to the fission peak is the 200 MeV
  per fission.
- `~NE-10` — the same curve, climbed from below; the iron/nickel peak is where
  stellar fusion stops paying.
- `~NE-13` — $S_n$ is the energy released on neutron capture and therefore the
  energy available to the compound nucleus.
