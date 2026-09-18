# QM-15 — References

Page-level citations **verified by extracting the page text** in the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified for this module by reading the page text: printed
> p.356 carries "7.1 Nondegenerate Perturbation Theory", p.417 the chapter title
> "8 The Variational Principle", p.449 "9 The WKB Approximation" — each at viewer
> page = printed page. Consistent with the QM-trunk offset (folio = fitz index + 1).

## Topic → location (Griffiths 3e, all page-text-confirmed)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| **§7.1 Nondegenerate Perturbation Theory** (heading) | §7.1 | **356** |
| General formulation; $H=H^0+\lambda H'$; power series Eq. 7.5–7.6 | §7.1.1 | **357** |
| Order-by-order equations (1st order Eq. 7.7, 2nd Eq. 7.8) | §7.1.1 | **358** |
| **§7.1.2 First-Order Theory**; $E_n^{(1)}=\langle\psi_n^0|H'|\psi_n^0\rangle$ (Eq. 7.9) (`first_order_energy`) | §7.1.2 | **359** |
| First-order state $|\psi_n^{(1)}\rangle$ (Eq. 7.13); nondegeneracy needed for safe denominator (`first_order_correction`) | §7.1.2 | **361** |
| **§7.1.3 Second-Order Energies**; $E_n^{(2)}=\sum_{m\neq n}|H'_{mn}|^2/(E_n^0-E_m^0)$ (Eq. 7.15) (`second_order_energy`) | §7.1.3 | **363** |
| **§7.2 Degenerate Perturbation Theory** (heading); ordinary PT blows up | §7.2 | **366** |
| **§7.2.1 Two-Fold Degeneracy**; the "good" states problem | §7.2.1 | **367** |
| $W_{ij}=\langle\psi_i^0|H'|\psi_j^0\rangle$; eigenvalues of $W$ = first-order splittings (Eq. 7.30/7.33) (`degenerate_first_order_split`) | §7.2.1 | **370** |
| **Ch.8 The Variational Principle** (chapter title) | Ch.8 | **417** |
| **§8.1 Theory**; $\langle H\rangle\ge E_{gs}$ (Eq. 8.1) + proof (`variational_energy`) | §8.1 | **418** |
| Example 8.1: Gaussian trial on the oscillator → exact $E_0=\tfrac12\hbar\omega$ (Eq. 8.2–8.7) (`gaussian_trial`, `gaussian_ho_energy`) | §8.1 | **418–419** |
| Example 8.2: Gaussian on the delta well (upper bound, not exact) | §8.1 | **420** |
| **Ch.9 The WKB Approximation** (chapter title) | Ch.9 | **449** |
| **§9.1 The "Classical" Region**; $p=\sqrt{2m(E-V)}$ (Eq. 9.2); WKB $\psi\propto p^{-1/2}e^{\pm i\int p\,dx/\hbar}$ (Eq. 9.10), $|\psi|^2\propto1/p$ (Eq. 9.11) (`classical_momentum`, `action_integral`) | §9.1 | **450–451** |
| Example 9.1: two vertical walls, $\int p\,dx=n\pi\hbar$ (Eq. 9.17) | §9.1 | **452** |
| **§9.2 Tunneling**; $T\approx e^{-2\gamma}$ (Eq. 9.22), $\gamma=\tfrac1\hbar\int|p|\,dx$ (Eq. 9.23) (`tunneling_probability`, `barrier_action`) | §9.2 | **455** |
| Example 9.2: Gamow's theory of alpha decay (the tunnelling exponent in nature) | §9.2 | **456** |
| **§9.3 The Connection Formulas** (Airy patching at a turning point, Eq. 9.47) | §9.3 | **460, 463** |
| Example 9.3: one vertical wall, $\int p\,dx=(n-\tfrac14)\pi\hbar$ (Eq. 9.48); half-harmonic = exact odd HO levels | §9.3 | **464** |
| Two smooth turning points: $\int_{x_1}^{x_2}p\,dx=(n-\tfrac12)\pi\hbar$ (Eq. 9.50) (`bohr_sommerfeld_energy`, default $\gamma=\tfrac12$) | §9.3 | **465** |

> **Anchor correction (encouraged by the dispatch).** The task prompt listed
> §7.2 Degenerate Perturbation Theory at printed **p.361**; reading the pages,
> p.361 is actually still **§7.1.2** (the first-order *wave-function* correction,
> Eq. 7.13, plus Problems 7.1–7.2). The numbered heading "**7.2 Degenerate
> Perturbation Theory**" begins on **p.366**, and "7.2.1 Two-Fold Degeneracy" on
> **p.367**, with the central result (eigenvalues of $W$) on **p.370**. The true
> pages are cited above (a verified p.366 beats an approximate p.361). The other
> three anchors (p.356, p.417, p.449) were correct as given.

> **Index convention.** Griffiths writes the smooth-turning-point condition as
> $\int_{x_1}^{x_2}p\,dx=(n-\tfrac12)\pi\hbar$ with $n=1,2,3,\dots$ (Eq. 9.50);
> the code uses the ground-state-is-$n{=}0$ convention $(n+\tfrac12)\pi\hbar$,
> $n=0,1,2,\dots$ — identical physics. The connection-formula constant subtracted
> from $n$ is 0 / $\tfrac14$ / $\tfrac12$ for two walls / one wall / two smooth
> turns (Griffiths p.465); the code exposes it as `gamma` = 1 / $\tfrac34$ / $\tfrac12$.

## Problems (verified, Griffiths 3e)
- **Problem 7.2** — harmonic oscillator with a slightly stiffer spring; first-order
  energy via Eq. 7.9 vs the exact expansion — printed **p.361**.
- **Problem 7.4** — the most general two-level system; expand the exact energies
  and match 1st/2nd-order PT; convergence condition on $H'$ — printed **p.363**.
- **Problem 7.6** — charged oscillator in a uniform field ($H'\propto x$): no
  first-order shift, exact second-order via completing the square — printed **p.364**.
- **Problem 8.1** — Gaussian trial for the (a) linear and (b) **quartic**
  potential ground states (exactly the quartic test in this module) — printed **p.422**.
- **Problem 8.2** — best variational bound on the oscillator with a non-Gaussian
  trial — printed **p.422**.
- **Problem 8.4** — variational corollary for the *first excited* state (orthogonal
  trial) — printed **p.422**.
- **Problem 9.7** — the "bouncing ball" (linear well) via WKB, compared to the
  exact Airy-function answer — printed **p.466**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned. Time-independent
  perturbation theory and the variational method are in **Ch. 5** (Approximation
  Methods); WKB appears there too.
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. II** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned (**Ch. XI** stationary perturbation
  theory; the variational method and WKB in the complements).
- **~MA-21** (`modules/MA/MA-21_dimensional_analysis_asymptotics/`) — asymptotic
  series: a perturbation expansion is generically asymptotic (often divergent but
  superbly accurate at low order), which is the rigorous backdrop for the
  $O(\lambda^2)/O(\lambda^3)$ error scaling measured in the tests.
- **~QM-08** (`modules/QM/QM-08_1d_problems/`) — its exact `transmission_barrier`
  is **imported by this module's test** to validate the WKB tunnelling exponent;
  the two share $e^{-2\kappa a}$ and differ only by an $O(1)$ prefactor.

> **Honesty note.** Griffiths 3e covers all three pillars first-hand and in depth
> (Ch.7–9 above), so the citations here are to genuine derivations, not mentions.
> Where the code goes beyond the book — the explicit $O(\lambda^2)/O(\lambda^3)$
> error-scaling measurement, the Airy-zero comparison, and the QM-08 tunnelling
> cross-check — **the verification is the code** (`test_approximations.py`).
