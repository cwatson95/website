# QM-21 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module: printed folio == viewer
> page. Spot-checks below — §12.1 "The EPR Paradox" reads on viewer page 567,
> §12.2 "Bell's Theorem" on 569, Eq. 12.4 / the Bell derivation on 570, "the
> famous Bell inequality" + the 45° violation on 571 — each confirmed by
> extracting the page text before citing. Same scan as the rest of the QM trunk.

## Topic → location

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| Ch. 12 "Afterword": realist vs orthodox; what QM *means* | Griffiths 3e | §12 opening | 566 |
| **EPR paradox**; $\pi^0\to e^-e^+$ → singlet (Eq. 12.1); locality; "spooky action" (`singlet`) | Griffiths 3e | **§12.1 The EPR Paradox** | **567** |
| **Entangled states**: the no-factorization theorem $\alpha|01\rangle+\beta|10\rangle$ can't be a product (`is_product_state`, `concurrence`) | Griffiths 3e | §12.1, **Problem 12.1** | 568 |
| **Bell's theorem**; independently-oriented detectors; record $\pm1$; $E(a,b)$ defined; aligned/anti-aligned $E=\mp1$ (Eqs. 12.2–12.3) (`correlation`) | Griffiths 3e | **§12.2 Bell's Theorem** | **569** |
| Singlet correlation $E(a,b)=-\mathbf a\!\cdot\!\mathbf b$ (Eq. 12.4); LHV functions $A,B=\pm1$ (Eqs. 12.5–12.6); $P=\int\rho AB$ (Eq. 12.7); Bell inequality derivation (Eqs. 12.8–12.12) (`E_singlet`, `bell_3setting`) | Griffiths 3e | §12.2 | **570** |
| "The famous **Bell inequality**" $|P(a,b)-P(a,c)|\le1+P(b,c)$ (Eq. 12.12); the **45° QM violation** (Fig. 12.3); Aspect–Grangier–Roger experiments (`bell_3setting`) | Griffiths 3e | §12.2 | **571** |
| **No-signaling**: lists at each end are "completely random"; "causal" vs "ethereal" influences; the bug's-shadow argument (Fig. 12.4) (`no_signaling_unitary`, `no_signaling_measurement`) | Griffiths 3e | §12.2 (end) | 571–572 |
| Mixed states & the density matrix (reduced state $\rho_A$; the `~QM-20` companion) | Griffiths 3e | §12.3 | 575 |

> **CHSH vs Griffiths.** Griffiths states the *original 3-setting* Bell
> inequality $|P(a,b)-P(a,c)|\le1+P(b,c)$ (Eq. 12.12, **p.571**) — built here as
> `bell_3setting` and verified to be violated by his own 45° example. The
> module's **primary** object is the modern *4-setting* **CHSH** inequality
> $|S|\le2$ with the **Tsirelson** quantum bound $2\sqrt2$ (Clauser–Horne–
> Shimony–Holt 1969; Cirel'son 1980) — the form used in real Bell tests and the
> one with the clean $2\sqrt2$ maximum. Griffiths does **not** give CHSH or name
> Tsirelson, so those are **not** page-cited to him; **the verification is the
> code** (`test_chsh_*` checks $|S|\le2$ exhaustively over the 16 local
> strategies, $|S|=2\sqrt2$ at the optimal angles, and $|S|\le2\sqrt2$ — the
> Tsirelson bound — over thousands of random settings and at the operator level).

## Problems (verified, Griffiths 3e Ch. 12)
- **Problem 12.1** — *Entangled states*: prove that
  $\alpha|s_1\rangle|s_2\rangle+\beta|s_2\rangle|s_1\rangle$ cannot be written as
  a single product $|r\rangle|q\rangle$ unless $\alpha=0$ or $\beta=0$ — the
  no-factorization theorem — printed **p.568**. (Checked numerically by
  `concurrence`/`is_product_state`: `test_no_factorization_theorem`.)
- **Problem 12.3** — a *(local) deterministic hidden-variable* theory =
  classical mechanics (the "baseballs" model): record the sign of the spin
  component along $\mathbf a$, $\mathbf b$; with isotropic launch the correlation
  is $P(a,b)=-1+2\eta/\pi$, which **satisfies** Bell's inequality (Eq. 12.12) —
  printed **p.573**. (This is exactly the physical LHV model in
  `test_chsh_physical_lhv_model_below_2`, which lands at/under the classical
  bound 2, far below $2\sqrt2$.)

> **Honesty note (per the trunk's citation rule).** Every Griffiths page above
> was confirmed by extracting its text. The headings §12.1 (p.567), §12.2
> (p.569), the singlet (Eq. 12.1, p.567), $E=-\mathbf a\!\cdot\!\mathbf b$
> (Eq. 12.4, p.570), the Bell inequality (Eq. 12.12) and 45° violation (p.571),
> and the no-signaling discussion (p.571–572) all match the claims they support.
> Two intentional extensions beyond Griffiths' text: (i) the **CHSH** 4-setting
> inequality and the **Tsirelson** $2\sqrt2$ bound (standard results, not in
> Griffiths — verified in code, not cited to him), and (ii) the **concurrence /
> Schmidt-rank** machinery (a modern quantum-information packaging of his
> separability discussion; also verified in code). The spin-½ optimal CHSH
> angles are $0°,90°,45°,135°$ because $E=-\cos\theta$; the *photon*-polarization
> angles $0°,22.5°,45°,67.5°$ (the famous Aspect values) are halved because
> polarization correlation goes as $\cos2\theta$ — that optical version is `~QO-05`.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer**; confirmed `get_text()` returns 0
  characters across sampled pages). Cite unpinned: the chapter on quantum
  entanglement / EPR & Bell's inequality (Sakurai gives the CHSH treatment and
  the spin-correlation analysis in detail — the natural companion to §3–§5 here).
- **Cohen-Tannoudji, Diu & Laloë, *Quantum Mechanics*** —
  `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is likewise **image-only** (confirmed, 0 text
  chars). Cite unpinned: the complements on the EPR argument, Bell's inequality,
  and entangled states.
- **Bethe & Jackiw, *Intermediate QM*** (`QM_Quantum_Mechanics/BetheQM.pdf`, text-extractable)
  is an *applications* text (scattering, perturbation theory) and does **not**
  cover entanglement or Bell's theorem; **not cited here**.
- Primary literature (not on this shelf): J. S. Bell, *Physics* **1**, 195
  (1964); Clauser, Horne, Shimony & Holt, *Phys. Rev. Lett.* **23**, 880 (1969)
  (CHSH); B. S. Cirel'son [Tsirelson], *Lett. Math. Phys.* **4**, 93 (1980)
  (the $2\sqrt2$ bound); Aspect, Grangier & Roger, *Phys. Rev. Lett.* **49**,
  91 & 1804 (1982).
