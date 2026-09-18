# QF-01 — References

| Book (edition) | File | Notes |
|---|---|---|
| Peskin & Schroeder, *An Introduction to Quantum Field Theory* (1995) | `QF_Quantum_Field_Theory/QFTPeskin.pdf` | **primary**; cited at **section level** (Ch. 2 free scalar field, Ch. 3 Dirac field) |
| Zee, *Quantum Field Theory in a Nutshell*, **2nd ed.** | `QF_Quantum_Field_Theory/Zee_QFT.pdf` | cross-cited at **chapter/section level** (Part I) |
| Weinberg, *The Quantum Theory of Fields, Vol. 1: Foundations* | `QF_Quantum_Field_Theory/Weinberg_The_Quantum_Theory_of_Fields_vol_1.pdf` | cross-cited at **chapter level** |

> **Granularity.** Section/chapter numbers follow the standard editions and are
> stable across printings; printed↔PDF page offsets were **not** individually
> verified for this module, so every citation is given by **section/chapter and
> title**, never by page (cf. `~SM-06/refs.md`, which does verify Pathria
> page-by-page). Peskin's Ch. 2–3 section titles are quoted below; tighten to page
> level if needed by opening the PDFs above.

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| Lagrangian density, canonical momentum $\pi=\partial\mathcal L/\partial(\partial_0\phi)$, Hamiltonian | PS | §2.2 *Elements of Classical Field Theory* |
| Equal-time commutator $[\phi,\pi]=i\delta^3$; Klein–Gordon field as oscillators; $a_{\mathbf p},a_{\mathbf p}^\dagger$, $[a_{\mathbf p},a_{\mathbf q}^\dagger]=(2\pi)^3\delta^3$ (`kg_dispersion`, `annihilation`, `creation`, `commutator`) | PS | §2.3 *The Klein–Gordon Field as Harmonic Oscillators* |
| Hamiltonian $H=\int\!\frac{d^3p}{(2\pi)^3}\omega_{\mathbf p}(a^\dagger a+\tfrac12[\,,])$; spectrum $(n+\tfrac12)\omega$; one-particle states; **vacuum (zero-point) energy** and its divergence (`single_mode_spectrum`, `mode_energy`, `vacuum_energy`, `field_modes`) | PS | §2.3 *...as Harmonic Oscillators* |
| Klein–Gordon field in space-time, propagator, causality (context for `~QF-02`) | PS | §2.4 *The Klein–Gordon Field in Space-Time* |
| **Dirac field**: quantization with **anticommutators** $\{b,b^\dagger\}$, spin–statistics, Pauli exclusion (`anticommutator`, `fermion_annihilation`) | PS | §3.5 *Quantization of the Dirac Field* |
| Field = lattice of coupled oscillators (the B6 picture, in pictures) | Zee | Part I, §I.3 *From Mattress to Field* |
| Canonical vs path-integral quantization of the scalar field | Zee | Part I, §I.2–§I.3 (and §I.8, the **EM field** & gauge) |
| Construction of quantum fields from creation/annihilation operators; **spin–statistics connection**; causality | Wbg | Ch. 5 *Quantum Fields and Antiparticles* |
| Canonical formalism for fields (constraints, the gauge issue of `~QF-03`) | Wbg | Ch. 7 *The Canonical Formalism* |

## See also
- `~QM-09` (the single quantum harmonic oscillator — the mode this module repeats;
  its `annihilation`/`creation`/`number` are mirrored here) and `~CM-16` (classical
  normal modes) — the two lower rungs of **KEY BRIDGE B6**.
- `~QM-22` (Klein–Gordon & Dirac equations — the classical field equations quantized
  here) and `~QM-19` (path integrals — the alternative route, Zee Part I).
- `~QM-14` (identical particles, Pauli exclusion) — the spin–statistics payoff of
  Peskin §3.5; `~EM-09` (vector potential & gauge freedom) — the photon constraint.
- Forward: `~QF-02` (interactions / Feynman diagrams, PS Ch. 4), `~QF-03` (gauge
  theories / QED), `~QF-04` (renormalization — taming the §5 vacuum divergence),
  `~QF-05` (curved-spacetime QFT — Hawking/Unruh; Birrell–Davies & Fulling on this
  shelf; the user's Quantum_Optics work).
- Peskin Ch. 2–3 (primary, computational); Zee Part I (gentle, physical pictures);
  Weinberg Vol. 1 Ch. 5, 7 (axiomatic, spin–statistics from first principles).
