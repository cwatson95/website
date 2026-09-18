# QO-02 — References

| Book (edition) | File | Notes |
|---|---|---|
| Scully & Zubairy, *Quantum Optics* (Cambridge, 1997) | `QO_Quantum_Optics/QuantumOptics.ZubairyMuhammadSuhail.pdf` | the primary source; cited at **chapter/section level** |
| Boyd, *Nonlinear Optics* (4th ed.) | `QO_Quantum_Optics/NonlinearOptics-Boyd-4thEd.pdf` | §6.3 two-level-atom / density-matrix Rabi treatment (further reading; matrix-element conventions differ) |

> **Granularity.** Section numbers and titles below were read directly from the
> book's own table of contents in the PDF (its §5 *Atom–field interaction —
> semiclassical theory* and §6 *Atom–field interaction — quantum theory*). The
> printed↔PDF page offset was **not** verified per page, so citations are given by
> **section/title**, not page (cf. `~SM-06/refs.md`, which does pin Pathria
> page-by-page). Tighten to page level by opening the PDF at the sections below.

## Topic → location (Scully & Zubairy — the primary source)

| Topic (code symbol) | Section / title |
|---|---|
| Two-level atom, dipole $-\mathbf d\!\cdot\!\mathbf E$ / $\mathbf r\!\cdot\!\mathbf E$ Hamiltonian (`sigma_z`, `sigma_plus`, `sigma_minus`) | §5.1 *Atom-field interaction Hamiltonian* (5.1.2 *Dipole approximation and r·E Hamiltonian*) |
| Semiclassical Rabi flopping; $P_e=(\Omega^2/\Omega_R^2)\sin^2(\Omega_R t/2)$, $\Omega_R=\sqrt{\Omega^2+\delta^2}$ (`rabi_excited_population`, `generalized_rabi`, `two_level_hamiltonian`) | §5.2 *Interaction of a single two-level atom with a single-mode field* (5.2.1 *Probability amplitude method*, 5.2.2 *Interaction picture*) |
| Rotating-wave approximation & its validity / Bloch–Siegert correction | §5.2.3 *Beyond the rotating-wave approximation* |
| Quantized single mode: $a,a^\dagger$, number states, coherent state $|\alpha\rangle$ (`annihilation`, `number_operator`, `coherent_state`) | §6.1 *Atom-field interaction Hamiltonian*; Ch. 2 *Coherent and squeezed states* (coherent state, Poisson statistics) |
| Jaynes–Cummings Hamiltonian $H=\hbar\omega_c a^\dagger a+\tfrac12\hbar\omega_a\sigma_z+\hbar g(a\sigma^++a^\dagger\sigma^-)$ (`jcm_hamiltonian`) | §6.1–6.2 |
| Dressed states $E_{n,\pm}$, vacuum Rabi splitting $2g$ (`dressed_energies`, `vacuum_rabi_splitting`) | §6.2 (the $\{|e,n\rangle,|g,n+1\rangle\}$ doublets) |
| Collapse & revival of the inversion $\langle\sigma_z\rangle=\sum_n P_n\cos(2g\sqrt{n+1}\,t)$ (`jcm_inversion`, `resonant_inversion_series`, `collapse_time`, `revival_time`) | §6.2 / §6.2.1 *Probability amplitude method* |

> **Honesty note.** The atomic Hamiltonian is taken as $\tfrac12\hbar\omega_a\sigma_z$
> exactly as written in `jcm_hamiltonian`, so `dressed_energies` returns the
> eigenvalues of that operator's block, $\hbar\omega_c(n+\tfrac12)\pm\tfrac12\hbar
> \sqrt{\delta^2+4g^2(n+1)}$ — **verified against `eigh`** in
> `test_dressed_energies_match_block_and_vacuum_rabi`. The commonly quoted form
> $\hbar\omega_c(n+1)-\tfrac12\hbar\delta'\pm\tfrac12\hbar\sqrt{\delta'^2+4g^2(n+1)}$
> (with $\delta'=\omega_c-\omega_a$) measures the atom from its ground state and so
> differs only by the unobservable global constant $\tfrac12\hbar\omega_a$; the
> **splitting** $2g\sqrt{n+1}$ — and hence the vacuum Rabi splitting $2g$ and all
> dynamics — is identical. Both forms appear in `notes.md` §5.

## See also
- `~QO-01` — quantization of the field, number states $|n\rangle$, coherent states
  $|\alpha\rangle$ (the field this module drives the atom with).
- `~QO-03` — spontaneous & stimulated emission and laser physics (the JCM with a
  *lossy* mode; the gain medium of the KrF/excimer code in this repo, `~PK-04`).
- `~QO-04` — open quantum systems / master equations: damped Rabi oscillations and
  the strong-coupling condition $g\gg\Gamma,\kappa$ behind the vacuum Rabi splitting.
- `~QM-11` — the two-level/spin algebra ($\sigma_z,\sigma^\pm$) and the driven-spin
  Rabi flop reused here; `~QM-16` — time-dependent perturbation theory (the dipole
  drive and the weak-field limit of the Rabi formula).
- Scully & Zubairy Ch. 5–6 (primary, rigorous); Boyd *Nonlinear Optics* §6.3
  (density-matrix two-level treatment, further reading).
