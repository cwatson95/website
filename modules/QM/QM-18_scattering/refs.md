# QM-18 — References

Page-level citations **verified by reading the page text** in the PDF (extracted
with `fitz`, not eyeballed off a scan). **Printed** = the number printed on the
page; **PDF** = the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |
| Bethe & Jackiw, *Intermediate Quantum Mechanics*, 3rd ed. | `QM_Quantum_Mechanics/BetheQM.pdf` | fitz index = printed **+ 18** |

> **Offset notes.**
> *Griffiths:* the printed folio equals the viewer page throughout the body (read
> printed page `P` with `fitz.open(path)[P-1]`). Confirmed on every page cited
> below (e.g. fitz idx 492 carries folio 493 = §10.4 heading).
> *Bethe:* fitz index 264 carries printed folio 246, so `fitz_index = printed + 18`
> (read printed page `P` with `fitz.open(path)[P+18]`). Confirmed at the Born page.

## Topic → location (Griffiths 3e — the primary source, Chapter 10)

| Topic (code symbol) | Section / Eq. | Printed p. |
|---|---|---|
| §10.1 *Introduction* (heading) | §10.1 | 476 |
| Classical scattering: impact parameter $b$, angle $\theta$; hard-sphere Example 10.1 | §10.1.1 *Classical Scattering Theory* | 477 |
| Classical differential cross-section $d\sigma/d\Omega=(b/\sin\theta)\lvert db/d\theta\rvert$ (Eq. 10.4) | §10.1.1 | 478 |
| Classical hard-sphere total cross-section $\sigma=\pi R^2$ (Eq. 10.8) — the geometric shadow (cf. `~CM-08`) | §10.1.1, Example 10.2 | 479 |
| Rutherford classical cross-section (Eq. 10.11); total $\sigma_{\rm Coul}=\infty$ | §10.1.1, Problem 10.1 | 480 |
| Asymptotic wave $\psi\simeq A[e^{ikz}+f(\theta)e^{ikr}/r]$ (Eq. 10.12); **$d\sigma/d\Omega=\lvert f\rvert^2$ (Eq. 10.14)** (`differential_cross_section`) | §10.1.2 *Quantum Scattering Theory* | 481 |
| §10.2 *Partial Wave Analysis* (heading) | §10.2 | **483** |
| $f=\frac1k\sum(2\ell+1)a_\ell P_\ell$ (Eq. 10.25); $d\sigma/d\Omega$ (10.26); $\sigma=4\pi\sum(2\ell+1)\lvert a_\ell\rvert^2$ (Eq. 10.27) (`partial_wave_amplitude`,`total_cross_section`) | §10.2.1 *Formalism* | 486 |
| Rayleigh's formula $e^{ikz}=\sum i^\ell(2\ell+1)j_\ell(kr)P_\ell$ (Eq. 10.29); quantum hard sphere (Example 10.3) | §10.2.2 *Strategy* | 487 |
| Low-energy hard sphere $\sigma\to4\pi a^2$ — **four times** geometric (Eq. 10.36) (`hard_sphere_phase_shift`) | §10.2.2, Example 10.3 | 488 |
| §10.3 *Phase Shifts* (heading); 1-D phase shift $\delta$ (Eq. 10.40) | §10.3 | 490 |
| $a_\ell=\frac1k e^{i\delta_\ell}\sin\delta_\ell$ (Eq. 10.46); **$f=\frac1k\sum(2\ell+1)e^{i\delta_\ell}\sin\delta_\ell P_\ell$ (Eq. 10.47)**; **$\sigma=\frac{4\pi}{k^2}\sum(2\ell+1)\sin^2\delta_\ell$ (Eq. 10.48)** | §10.3 | 491 |
| Hard-sphere partial-wave phase shifts (Problem 10.6) | §10.3 | 492 |
| §10.4 *The Born Approximation* (heading) | §10.4 | 493 |
| Integral form of the Schrödinger eq.; Helmholtz Green's function (Eqs. 10.49–10.65) | §10.4.1 | 494–496 |
| §10.4.2 *The First Born Approximation*; **$f=-\frac{m}{2\pi\hbar^2}\!\int e^{i\mathbf q\cdot\mathbf r}V\,d^3r$ (Eq. 10.79)** (`born_amplitude_radial`) | §10.4.2 | 498–499 |
| Spherical Born $f=-\frac{2m}{\hbar^2\kappa}\!\int rV\sin(\kappa r)dr$ (Eq. 10.88); **$\kappa=q=2k\sin(\theta/2)$ (Eq. 10.89)** | §10.4.2 | 500 |
| **Yukawa** $V=\beta e^{-\mu r}/r\Rightarrow f=-\frac{2m\beta}{\hbar^2(\mu^2+q^2)}$ (Example 10.5, Eq. 10.91) (`born_amplitude_yukawa`) | §10.4.2 | 500 |
| **Rutherford** as the Coulomb $\mu\to0$ limit (Example 10.6, Eqs. 10.92–10.93) (`rutherford_cross_section`) | §10.4.2 | 500–501 |
| **Optical theorem** $\sigma_{\rm tot}=\frac{4\pi}{k}\operatorname{Im}f(0)$ (Problem 10.19; hint uses Eqs. 10.47–10.48) (`optical_theorem_sigma`) | Further Problems | **504** |

> **Anchor correction (encouraged by the build rule).** The task anchor listed
> "§10.2 Partial Wave Analysis — p.482"; the §10.2 *heading* is in fact on printed
> **p.483** (p.482 is the tail of §10.1.2, ending with the sentence that names the
> two techniques and Problem 10.2). The partial-wave *formulae* (`f`, `σ`) are on
> p.486 (amplitudes) and p.491 (phase-shift form). All other task anchors (p.477,
> p.490, p.493) are confirmed exactly.

## Topic → location (Bethe & Jackiw — verified second source)

| Topic | Section / Eq. | Printed p. |
|---|---|---|
| Born elastic scattering amplitude $f(\theta)\propto\int e^{i\mathbf q\cdot\mathbf r}V(r)\,d\mathbf r$, with $\mathbf q=\mathbf k_0-\mathbf k$ and **$q=2k\sin(\theta/2)$** (Eqs. 13-8a,b) | §13 *Elastic Scattering at High Energies* | 246 |
| Atomic form factor $F(q)=\int\rho(r)e^{i\mathbf q\cdot\mathbf r}d\mathbf r$ (Eq. 13-4a); validity criterion for the Born formula (Eqs. 13-6/13-7, Table 13-1) | §13 | 244–245 |

## Problems (verified, Griffiths 3e)
- **Problem 10.1** — classical Rutherford: derive $b(\theta)$, the differential
  cross-section, and that the total Coulomb cross-section is infinite — printed **p.480**.
- **Problem 10.3** — prove the hard-sphere coefficient relation (Eq. 10.33) from
  orthogonality of the $P_\ell$ — printed **p.488**.
- **Problem 10.4** — low-energy scattering from a delta-shell; $f$, $d\sigma/d\Omega$,
  $\sigma$ — printed **p.488**.
- **Problem 10.6** — hard-sphere partial-wave phase shifts — printed **p.492**.
- **Problem 10.11** — evaluate the Yukawa Born integral (Eq. 10.91) — printed **p.501**.
- **Problem 10.12** — total cross-section for the Yukawa potential in the Born
  approximation, as a function of $E$ — printed **p.501**.
- **Problem 10.19** — prove the **optical theorem** $\sigma=\frac{4\pi}{k}\operatorname{Im}f(0)$
  (hint: Eqs. 10.47–10.48) — printed **p.504**.

> **Honesty note (per the trunk's citation rule).** Scattering is *core* Griffiths
> (Chapter 10) and every formula in `notes.md` is on a page verified above —
> derived there from first principles. Two caveats: (i) the **square-well**
> log-derivative phase shift coded here is the standard central-potential matching
> (Griffiths §10.2.2 strategy, p.487); Griffiths works the hard sphere and the
> delta-shell explicitly and leaves the square well to the same method, so its
> s-wave is verified in the code against the closed form
> $\delta_0=-ka+\arctan[(k/k_{\rm in})\tan(k_{\rm in}a)]$. (ii) Griffiths writes
> the momentum transfer $\kappa$; this module calls it $q$ (Bethe's notation),
> identical object $q=2k\sin(\theta/2)$. The numerical **verification is the
> code**: `test_scattering.py` checks $\delta_0=-ka$, $\sigma\to4\pi a^2$, the
> optical-theorem identity, the Born integral vs the Yukawa closed form, and the
> Rutherford limit.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: Ch. 6/7 *Scattering Theory*
  (Lippmann–Schwinger equation, the $T$-matrix, partial waves and the optical
  theorem from unitarity of $S$).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. II** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned: Ch. VIII *Collision theory* (stationary
  scattering states, partial waves, the Born series).
- `~MA-12` (this repo) — Legendre $P_\ell$ (imported by the code) and the spherical
  Bessel functions of the radial problem.
- `~CM-08` (this repo) — the classical collision/cross-section theory whose
  Rutherford $d\sigma/d\Omega$ the Born/Coulomb limit reproduces exactly.
