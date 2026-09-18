# SM-04 — Quantum Statistics (notes)

When the thermal de Broglie wavelength becomes comparable to the interparticle
spacing, the **indistinguishability** of identical particles (`~QM-14`) can no
longer be ignored, and the classical Boltzmann factor of `~SM-03` is replaced by
two quantum distributions.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria 3e;
**Sch** = Schroeder (image-only). Printed pages. β ≡ 1/kT.

## 1. Indistinguishability and the occupation numbers
Working in the grand canonical ensemble, the **mean occupation** of a single-
particle state of energy ε is [Pa §5.5, p.128; §6.3, p.149]:
$$\langle n_\varepsilon\rangle=\frac{1}{e^{(\varepsilon-\mu)/kT}\mp 1},$$
with the **lower sign (−1) for bosons** (Bose–Einstein) and the **upper (+1) for
fermions** (Fermi–Dirac). The chemical potential µ fixes the particle number. Code:
`bose_einstein`, `fermi_dirac`.

## 2. The classical limit
When $(\varepsilon-\mu)\gg kT$ the $\mp1$ is negligible and both reduce to the
**Maxwell–Boltzmann** occupation
$$\langle n_\varepsilon\rangle\to e^{-(\varepsilon-\mu)/kT},$$
recovering `~SM-03`. Quantum statistics matter only when states are nearly full
(degenerate). Code: `maxwell_boltzmann` (and the demo shows BE > MB > FD).

## 3. Fermions: the Pauli principle and the Fermi sea
The $+1$ keeps $0\le\langle n\rangle\le 1$ — at most one fermion per state, the
**Pauli exclusion principle**. At $\varepsilon=\mu$, $\langle n\rangle=\tfrac12$
exactly. As $T\to0$ the distribution becomes a **step** [Pa §8.1, p.231]: every
state below the **Fermi energy** $\varepsilon_F=\mu(0)$ is filled, every one above
empty. This rigidity underlies the electron gas in metals (Pa §8.3, p.247) and the
pressure that supports white dwarfs. Code: `fermi_dirac_T0`.

## 4. Bosons: condensation
The $-1$ lets $\langle n\rangle$ grow without bound as $\varepsilon\to\mu^{+}$:
a macroscopic number of bosons can occupy the single lowest state — **Bose–Einstein
condensation** [Pa §7.1, p.180].

## 5. The photon gas: Planck, Wien, Stefan–Boltzmann
Photons are bosons with $\mu=0$. Multiplying the BE occupation by the photon density
of states gives the **Planck** spectral energy density [Pa §7.3, p.200]:
$$u(\omega)=\frac{\hbar\omega^3}{\pi^2 c^3}\frac{1}{e^{\hbar\omega/kT}-1}.$$
At low frequency this is the classical **Rayleigh–Jeans** law
$(\omega^2/\pi^2c^3)kT$ (whose unbounded growth is the "ultraviolet catastrophe"
the quantum cuts off). The spectrum peaks where $3(1-e^{-x})=x$, i.e.
$x=\hbar\omega_\text{max}/kT\approx 2.8214$ — **Wien's displacement law**,
$\omega_\text{max}\propto T$. Integrating over all frequencies gives the
**Stefan–Boltzmann** law,
$$\frac{U}{V}=\int_0^\infty u(\omega)\,d\omega=aT^4,\quad a=\frac{\pi^2 k^4}{15\hbar^3c^3},
  \qquad \sigma=\frac{ac}{4}=\frac{\pi^2 k^4}{60\hbar^3 c^2}.$$
Code: `planck_energy_density`, `rayleigh_jeans`, `wien_peak_x` (fixed-point root),
`radiation_energy_density`, `stefan_boltzmann_constant` (matches CODATA 5.670×10⁻⁸).

## Where this goes
- The electron gas, white dwarfs, and semiconductors are Fermi-gas applications (Pa Ch.8, `~CMx`).
- BEC and superfluidity are Bose-gas physics (Pa Ch.7).
- The photon-gas / Planck law connects to `~QO-01` (quantized light) and cosmology (`~RE-15`, the CMB).
- The same occupations seed `~PK-04` (atomic/molecular kinetics) and laser physics (`~QO-03`).
