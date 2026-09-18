# QO-03 — References

| Book (edition) | File | Notes |
|---|---|---|
| Scully & Zubairy, *Quantum Optics* (Cambridge Univ. Press, 1997) | `QO_Quantum_Optics/QuantumOptics.ZubairyMuhammadSuhail.pdf` | cited at **chapter / section level** — section titles below were read off the book's own Contents in the PDF; **page numbers are not given** (the scan's printed↔viewer offset was not verified per-page) |

> **Granularity.** Citations are to numbered **sections / chapters**, by title,
> confirmed against the Contents pages of this PDF. No printed page numbers are
> asserted (cf. `~SM-06/refs.md`, which *does* verify Pathria page-by-page; this
> module deliberately does not). Einstein's $A$/$B$ detailed-balance argument is the
> classic 1917 result; in Scully & Zubairy it sits in the introductory radiation
> chapter and is underpinned by the Weisskopf–Wigner spontaneous-emission rate of
> §6.3 — cited here at that chapter/section level, not to a single equation.

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| Black-body / Planck spectrum; photon concept; Einstein's radiation argument (`planck_spectral_energy_density`, `einstein_A_over_B`) | S&Z | **Ch. 1** *Quantum theory of radiation* (black-body & Planck introduction) |
| Stimulated emission vs. absorption, physical picture; semiclassical inversion (`stimulated_to_spontaneous`, `boltzmann_population_ratio`) | S&Z | **§5.6** *A physical picture of stimulated emission and absorption* |
| Spontaneous-emission rate (the $A$ coefficient), quantized field | S&Z | **§6.3** *Weisskopf–Wigner theory of spontaneous emission* |
| Semiclassical laser theory; rate equations, gain (`laser_rate_rhs`, `laser_steady_state`) | S&Z | **§5.5** *Semiclassical laser theory* (Lamb) |
| Laser photon statistics & the threshold condition (`laser_threshold`) | S&Z | **§11.2** *Laser photon statistics* (Ch. 11 *Quantum theory of the laser — density operator approach*) |
| Threshold as a second-order phase transition (order-parameter turn-on) | S&Z | **§11.6** *Analogy between the laser threshold and a second-order phase transition* |
| Photon detection & quantum coherence functions; first-order coherence, visibility (`g2_from_distribution` context) | S&Z | **§4.2** *Photon detection and quantum coherence functions*; **§4.3** *First-order coherence and Young-type double-source experiments* |
| Second-order coherence; HBT; bunching, antibunching, sub-Poissonian (`g2_thermal`, `g2_coherent`, `g2_fock`) | S&Z | **§4.4** *Second-order coherence* (incl. §4.4.1 HBT, §4.4.4 *Photon antibunching, Poissonian, and sub-Poissonian*) |
| Photon counting & photon statistics ($\langle n(n-1)\rangle$, $g^{(2)}(0)$) | S&Z | **§4.5** *Photon counting and photon statistics* |

## See also
- `~QM-16` (time-dependent perturbation theory — the emission/absorption *rate*
  $\propto|\langle f|H'|i\rangle|^2$ that becomes Einstein's $B$ coefficient; its
  §5 already flags the laser/inversion bridge to here).
- `~PK-04` (atomic & molecular kinetics — the KrF\* excimer laser kinetics in this
  repo: 248 nm gain, bound–free inversion, and the rate equations of §5–6 here).
- `~QO-01` (modes & photon number / coherent states), `~QO-02` (atom–field Rabi /
  Jaynes–Cummings — the dynamics behind $A$, $B$, and emitted-light coherence),
  `~QO-05` (squeezing & the nonclassical $g^{(2)}<1$ frontier).
- Scully & Zubairy Ch. 1 (radiation & Planck), Ch. 4 (coherence), Ch. 5–6
  (atom–field, emission), Ch. 11 (laser theory) — the spine of this module.
