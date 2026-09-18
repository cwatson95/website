# QM-17 — References

Page-level citations **verified by reading the page text** in the PDF (extracted
with `fitz`, not eyeballed off a scan). **Printed** = the number printed on the
page; **PDF** = the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified for this scan: the printed folio equals the viewer
> page throughout the body (read printed page `P` with `fitz.open(path)[P-1]`).
> Confirmed on pp.378, 380, 384, 386, 389, 390, 393, 398, 399. The whole QM trunk
> uses this scan.

## Topic → location (Griffiths 3e — the primary source, all page-verified)

| Topic (code symbol) | Section / Eq. | Printed p. |
|---|---|---|
| Fine structure intro; fine-structure constant $\alpha=e^2/4\pi\varepsilon_0\hbar c$ (Eq. 7.44); Table 7.1 hierarchy (`fine_structure_constant`) | §7.3 *The Fine Structure of Hydrogen* | 378 |
| Relativistic kinetic correction $H'_{\rm rel}=-p^4/8m^3c^2$ (Eqs. 7.45–7.51) | §7.3.1 *The Relativistic Correction* | 380 |
| $E^1_{\rm rel}=-(E_n^2/2mc^2)[4n/(\ell+\tfrac12)-3]$ (Eq. 7.58) (`relativistic_correction_eV`) | §7.3.1 | 381 |
| Spin-orbit Hamiltonian $\propto\mathbf L\!\cdot\!\mathbf S$; proton's field; gyromagnetic ratio (Eqs. 7.59–7.63) | §7.3.2 *Spin-Orbit Coupling* | 384 |
| Thomas-precession factor $\tfrac12$; electron moment "twice the classical value" | §7.3.2 | 385 |
| $\langle\mathbf L\!\cdot\!\mathbf S\rangle=\tfrac{\hbar^2}{2}[j(j{+}1){-}\ell(\ell{+}1){-}s(s{+}1)]$ (Eq. 7.65); $E^1_{\rm so}$ (Eq. 7.67); fine-structure formula (Eq. 7.68); $E_{nj}$ grand result (Eq. 7.69) (`LS_coupling`, `spin_orbit_correction_eV`, `fine_structure_correction_eV`, `hydrogen_energy_eV`) | §7.3.2 | 386 |
| Fine structure breaks $\ell$-degeneracy, preserves $j$-degeneracy; energy-level diagram Fig. 7.8 | §7.3.2 (end) | 387 |
| Zeeman perturbation $H'_Z=-(\boldsymbol\mu_\ell+\boldsymbol\mu_s)\!\cdot\!\mathbf B$ (Eqs. 7.70–7.73); weak/strong regimes vs internal field | §7.4 *The Zeeman Effect* | 389 |
| Landé $g_J=1+[j(j{+}1){+}s(s{+}1){-}\ell(\ell{+}1)]/2j(j{+}1)$ (Eq. 7.78) (`lande_g_factor`) | §7.4.1 *Weak-Field Zeeman* | 390 |
| $E^1_Z=\mu_B g_J B m_j$ (Eq. 7.79); Bohr magneton $\mu_B=e\hbar/2m_e$ (Eq. 7.80) (`zeeman_weak_field_eV`, `bohr_magneton`) | §7.4.1 | 391 |
| Paschen–Back $E^1_Z=\mu_B B(m_\ell+2m_s)$ (Eq. 7.83) (`zeeman_strong_field_eV`) | §7.4.2 *Strong-Field Zeeman* | 393 |
| Proton moment & $g_p\!=\!5.59$ (Eq. 7.89); spin-spin $\propto\mathbf S_p\!\cdot\!\mathbf S_e$; $\langle\mathbf S_p\!\cdot\!\mathbf S_e\rangle$ (Eq. 7.96) (`spin_spin_coupling`) | §7.5 *Hyperfine Splitting* | 398 |
| Triplet/singlet; gap $\Delta E=4g_p\hbar^4/3m_p m_e^2c^2a^4$ (Eq. 7.97); $f$ (Eq. 7.98); $\lambda\approx21$ cm (Eq. 7.99) (`hyperfine_splitting_eV`, `hyperfine_frequency`, `hyperfine_wavelength`) | §7.5 | 399 |

> **Honesty note (per the trunk's citation rule).** Fine structure, the Zeeman
> effect, and hyperfine splitting are **core Griffiths Chapter 7** and are derived
> there from first principles by perturbation theory — every formula in `notes.md`
> and every code function above is on a page verified here. **Two items go a step
> beyond Griffiths §7.3** and are flagged as such in the code:
> 1. The **Darwin term** (`darwin_correction_eV`). Griffiths obtains the $\ell=0$
>    fine-structure result by an accident — the $\ell\to0$ limit of the spin-orbit
>    formula (Eq. 7.67) happens to equal the Darwin contribution — and never names
>    it. The Darwin term is standard physics from the Dirac equation (`~QM-22`);
>    here **the verification is the code**, which checks
>    $E_{\rm rel}+E_{\rm so}+E_{\rm Darwin}=E^1_{\rm fs}$ (Eq. 7.68) to machine
>    precision for every state, including $\ell=0$.
> 2. The electron's **anomalous** $g_e=2.0023$ is a QED correction (`~QM-22`);
>    Griffiths Eqs. 7.78/7.83 use the Dirac value $g_e=2$, and so does the code's
>    Zeeman physics. $g_e=2.0023$ is exported only as a documented reference
>    constant.

## Problems (verified, Griffiths 3e)
- **Problem 7.14** — express the Bohr energies via $\alpha$ and $mc^2$; compute
  $\alpha$ from first principles — printed **p.378**.
- **Problem 7.17** — lowest-order relativistic correction to the 1-D harmonic
  oscillator — printed **p.382**.
- **Problem 7.20** — derive the fine-structure formula (Eq. 7.68) from the
  relativistic (Eq. 7.58) and spin-orbit (Eq. 7.67) terms — printed **p.387**.
- **Problem 7.21** — the red Balmer line ($n{=}3\to2$): how fine structure splits
  it, and the line spacing in Hz — printed **p.387–388**.
- **Problem 7.22** — the exact (Dirac) fine-structure formula; expand to order
  $\alpha^4$ and recover Eq. 7.69 — printed **p.388**.
- **Problem 7.23** — estimate the internal field; characterize "weak" vs "strong"
  Zeeman fields — printed **p.389**.
- **Problem 7.24** — the eight $n{=}2$ states under weak-field Zeeman; energies and
  slopes — printed **p.391**.
- **Problem 7.27** — the eight $n{=}2$ states under strong-field (Paschen–Back)
  Zeeman — printed **p.393**.
- **Problem 7.31** — the angular integral that kills the dipole-dipole term and
  leaves the contact (spin-spin) interaction for $\ell{=}0$ — printed **p.399**.
- **Problem 7.32** — hyperfine splitting of muonic hydrogen, positronium, and
  muonium (modify the H formula with reduced mass / masses) — printed **p.399–400**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: the fine-structure /
  hydrogen-with-spin sections and the discussion of the Lamb shift.
- **Cohen-Tannoudji, *Quantum Mechanics*** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is
  likewise **image-only**; cite unpinned: the chapter/complements on the hydrogen
  fine and hyperfine structure and the 21 cm line.
- **The Dirac equation** (`~QM-22`) gives the *exact* fine-structure formula and
  explains both the Darwin term and $g_e=2$ — the natural sequel to this module.
- `~QM-15` (this repo) — the perturbation theory whose machinery every result here
  uses; `~QM-13` — the addition of angular momenta ($\mathbf J=\mathbf L+\mathbf S$,
  $\mathbf F=\mathbf I+\mathbf S$) behind the "good" quantum numbers.
