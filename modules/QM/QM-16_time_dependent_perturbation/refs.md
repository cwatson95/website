# QM-16 — References

Page-level citations **verified by reading the page text** in the PDF (not a
table of contents, not a rendered scan). **Printed** = the number on the page;
**PDF** = the page in the viewer. For this Griffiths QM scan they coincide.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |

> **Offset note.** Verified empirically for this module by extracting page text
> before citing: the Ch. 11 opener "Quantum Dynamics" is on viewer page 510,
> "§11.4 Fermi's Golden Rule" on 538, "§11.2 Emission and Absorption of
> Radiation" on 523 — each matches its printed folio. Same scan as the rest of
> the QM trunk (printed == viewer).

## Topic → location

| Topic (code symbol) | Source | Section | Printed p. |
|---|---|---|---|
| Quantum dynamics: static $H$ ⇒ no transitions; need time-dependent $H'$ | Griffiths 3e | Ch. 11 opener *Quantum Dynamics* | **510** |
| Two-level system; $|\Psi\rangle=c_ae^{-iE_at}\|a\rangle+c_be^{-iE_bt}\|b\rangle$ (`two_level_H`) | Griffiths 3e | §11.1 *Two-Level Systems* (Eqs. 11.5–11.9) | 512 |
| Exact coupled equations for $c_a,c_b$; $\dot c_b=-\tfrac{i}{\hbar}H'_{ba}e^{i\omega_0t}c_a$ | Griffiths 3e | §11.1.1 *The Perturbed System* (Eqs. 11.14–11.18) | 513–514 |
| Constant-coupling two-level problem (Rabi, exactly solvable) | Griffiths 3e | **Problem 11.3** | 514 |
| **First-order amplitude** $c_f^{(1)}=-\tfrac{i}{\hbar}\!\int\!\langle f\|H'\|i\rangle e^{i\omega_{fi}t'}dt'$ (`first_order_amplitude`) | Griffiths 3e | §11.1.2 *Time-Dependent PT* (Eq. 11.21) | **516** |
| First-order picture / higher orders / multi-level series | Griffiths 3e | §11.1.2 (Eqs. 11.22–11.25, Figs. 11.1–11.3) | 516–517 |
| Sinusoidal perturbation; RWA; **transition probability** (Eq. 11.35) (`sinusoidal_probability`) | Griffiths 3e | §11.1.3 *Sinusoidal Perturbations* | **520** |
| Resonance line shape: peak height $(V/\hbar)^2$, width, "higher & narrower" (Fig. 11.5) | Griffiths 3e | §11.1.3 | 521 |
| **Rabi flopping frequency** $\sqrt{\Omega_R^2+\delta^2}$; exact RWA solution never exceeds 1 (`rabi_probability`) | Griffiths 3e | **Problem 11.9** (Eq. 11.37) | 521–522 |
| Emission/absorption of radiation; dipole $H'=-qE_0z\cos\omega t$ | Griffiths 3e | §11.2 / §11.2.1 (Eqs. 11.38, 11.41) | 523–524 |
| Absorption, **stimulated** & spontaneous emission; the laser, population inversion | Griffiths 3e | §11.2.2 | 525 |
| Dipole **selection rules** $\Delta\ell=\pm1,\ \Delta m=0,\pm1$ (→ `~QM-17`) | Griffiths 3e | §11.3.3 *Selection Rules* | 536 |
| **Fermi's golden rule** setup: continuum, density of states $\rho$, $dn=\rho\,dE$ (Eq. 11.79) | Griffiths 3e | §11.4 *Fermi's Golden Rule* | **538** |
| **The rule** $\Gamma=\tfrac{2\pi}{\hbar}\|\langle f\|H'\|i\rangle\|^2\rho(E_f)$ (`golden_rule_rate`); Example 11.2 (Born x-section) | Griffiths 3e | §11.4 (Eq. 11.81) | **539** |

## Problems (verified, Griffiths 3e)
- **Problem 11.3** — solve the two-level equations for a *time-independent*
  perturbation (the exact Rabi/constant-coupling oscillation) — printed **p.514**.
- **Problem 11.4** — a delta-function (in time) perturbation: find $c_a,c_b$ and
  the net transition probability — printed **p.515**.
- **Problem 11.5** — the general case with nonzero diagonal elements $H'_{aa},H'_{bb}$;
  the substitution that restores the simple structure — printed **p.518**.
- **Problem 11.9** — the rotating-wave approximation solved *exactly*: the Rabi
  flopping frequency, $P_{a\to b}$ never exceeds 1, and reduction to Eq. 11.35 —
  printed **pp.521–522**.
- **Problem 11.17** — the photoelectric effect for hydrogen via Fermi's golden
  rule (a continuum final state) — printed **p.540**.

> **Honesty note (per the trunk's citation rule).** Every Griffiths page above
> was confirmed by extracting its text; the page content matches the claim it
> supports. The headline equations are all present and verified: the first-order
> amplitude (Eq. 11.21, p.516), the sinusoidal transition probability (Eq. 11.35,
> p.520), the Rabi formula (Eq. 11.37, Prob. 11.9, p.522), and the golden rule
> (Eq. 11.81, p.539). The **two-level rotating-frame matrix** used in the code is
> the standard Pauli form $H=\tfrac12(\Omega_R\sigma_x+\delta\sigma_z)$ — equivalent
> to Griffiths Eqs. 11.17 in the RWA (Prob. 11.9), here written in spin language
> (`~QM-11`). The **golden-rule band model** (a discrete state coupled to $N$
> evenly spaced finals) is the standard Wigner–Weisskopf demonstration, not a
> verbatim Griffiths construction; **the verification is the code** —
> `test_tdpt.py` checks the linear-in-$t$ rate, its $|V|^2$ and $\rho$ scaling,
> and the exponential decay of the exact $(N{+}1)$-level dynamics, all against
> $\Gamma=2\pi|V|^2\rho$.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: Ch. 5, "Approximation
  Methods" (time-dependent perturbation theory, the interaction picture, the
  Dyson series, and Fermi's golden rule — Sakurai's interaction-picture
  derivation is the natural companion to §2 here).
- **Cohen-Tannoudji, Diu & Laloë, *Quantum Mechanics* Vol. II** —
  `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf` is likewise **image-only**; cite unpinned:
  Ch. XIII, "Approximation methods for time-dependent problems" (sinusoidal
  perturbations, the resonance, and the long-time/continuum limit), and the
  complements on Rabi oscillations.
- **Bethe & Jackiw, *Intermediate QM*** (`QM_Quantum_Mechanics/BetheQM.pdf`, text-extractable)
  — the radiation-theory chapters (emission/absorption, line shapes) parallel §5;
  not page-verified for this module.
