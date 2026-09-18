# QO-01 — References

| Book (edition) | File | Notes |
|---|---|---|
| Scully & Zubairy, *Quantum Optics* (Cambridge, 1997) — **primary** | `QO_Quantum_Optics/QuantumOptics.ZubairyMuhammadSuhail.pdf` | cited at **section level** (Ch.1 field quantization & Fock states; Ch.2 coherent states) |
| Boyd, *Nonlinear Optics*, **4th ed.** (Academic Press) — cross-cite | `QO_Quantum_Optics/boyd_optics.pdf` (and the equivalent `QO_Quantum_Optics/NonlinearOptics-Boyd-4thEd.pdf`) | the classical-field / mode-amplitude language (Ch.1) and the SBS forward link (Ch.9); cited at **chapter level** |

> **Granularity.** Section/chapter numbers and titles below were read from the
> Scully & Zubairy table of contents and the Boyd contents pages; they are stable
> across printings. Printed↔PDF **page offsets were not verified**, so citations
> are given by **section/chapter title, not page number** (cf. `~SM-06/refs.md`,
> which does pin Pathria page-by-page). Open the PDFs above to tighten to page
> level if needed.

## Topic → location  (Scully & Zubairy, section-level)

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| a field mode = a quantum oscillator; mode expansion, $H=\hbar\omega(a^\dagger a+\tfrac12)$, $[a,a^\dagger]=1$ (`annihilation`, `creation`, `number`, `commutator`, `energy`) | SZ | §1.1 *Quantization of the free electromagnetic field* (1.1.1 mode expansion, 1.1.2 quantization) |
| Fock / number states $|n\rangle$; ladder relations, orthonormality, $E_n$ (`fock_state`, `number`) | SZ | §1.2 *Fock or number states* |
| vacuum fluctuations & the photon concept; zero-point noise (`zero_point_energy`, `quadrature_variance`) | SZ | §1.5 *What is light? — The photon concept* (1.5.1–1.5.2, vacuum fluctuations) |
| the classical amplitude $\alpha$ a coherent state encodes | SZ | §2.1 *Radiation from a classical current* |
| coherent state as eigenstate of $a$, $a|\alpha\rangle=\alpha|\alpha\rangle$; displaced vacuum (`coherent_state`) | SZ | §2.2 *The coherent state as an eigenstate of the annihilation operator and as a displaced harmonic oscillator state* |
| why coherent states are "the most classical"; Poisson statistics, quadrature noise (`photon_distribution`, `mean_n`, `var_n`, `mandel_q`, `quadrature_x/p`) | SZ | §2.3 *What is so coherent about coherent states?* |
| further coherent-state properties (completeness, overlaps) | SZ | §2.4 *Some properties of coherent states* |

## Boyd cross-cite  (chapter-level)

| Topic | Source | Chapter |
|---|---|---|
| classical optical field as a sum of mode amplitudes $\tilde E(t)=\sum_n E(\omega_n)e^{-i\omega_n t}$; the susceptibility framework | Bo | Ch.1 *The Nonlinear Optical Susceptibility* |
| Stimulated Brillouin Scattering — the SBS forward link to `~QO-06` and the user's research | Bo | Ch.9 *Stimulated Brillouin and Stimulated Rayleigh Scattering* |

## See also
- `~QM-09` (the quantum harmonic oscillator — $a,a^\dagger$, the spectrum
  $\hbar\omega(n+\tfrac12)$, the truncation artifact — reused wholesale here;
  **KEY BRIDGE B6**) and `~QM-05` (bra–ket, commutators).
- `~EM-15` (classical electromagnetic waves and the mode expansion that supplies
  the amplitude $\alpha$).
- `~QF-01` (quantizing every mode → second quantization; the $a,a^\dagger$ here
  become particle creation/annihilation operators) and `~QO-02` (atom–field
  coupling), `~QO-05` (squeezing / nonclassical light), `~QO-06` (nonlinear &
  Brillouin SBS).
- Scully & Zubairy Ch.1–2 (primary, rigorous); Boyd Ch.1, Ch.9 (the classical-field
  and SBS context).
