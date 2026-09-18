# QF-04 — References

| Book (edition) | File | Notes |
|---|---|---|
| Peskin & Schroeder, *An Introduction to Quantum Field Theory* | `QF_Quantum_Field_Theory/QFTPeskin.pdf` | **primary**; cited at **chapter/section level** (Ch. 7 running charge, Ch. 10 systematics of renormalization, Ch. 12 the RG, Ch. 13 critical exponents, Ch. 16–17 asymptotic freedom) |
| Zee, *Quantum Field Theory in a Nutshell* | `QF_Quantum_Field_Theory/Zee_QFT.pdf` | gentle/physical; Part III (renormalization & counterterms), Part VI.8 (RG flow) |
| Rivasseau, *From Perturbative to Constructive Renormalization* | `QF_Quantum_Field_Theory/Rivasseau_Perturbative_to_Constructive_Renormalization.pdf` | **rigorous/advanced**; power counting, BPHZ, the RG (Part I) and the constructive program (Part II) |

> Section numbers follow the standard editions and are stable across printings;
> printed↔PDF page offsets were **not** verified here, so citations are given by
> chapter/section/title rather than page (cf. `~SM-06/refs.md`, which does verify
> Pathria page-by-page). Tighten to page level by opening the PDFs above.

## Topic → location

| Topic (code symbol) | Source | Chapter / section |
|---|---|---|
| UV divergences, power counting, counterterms (`beta_phi4`) | PS | Ch. 10 *Systematics of Renormalization* (§10.1 counting divergences, §10.2 renormalized perturbation theory) |
| renormalization of QED, the $Z$-factors | PS | Ch. 10, §10.3 *Renormalization of Quantum Electrodynamics* |
| running electric charge, $\alpha(q^2)$ (`qed_running_alpha`, `qed_alpha_sm`, `beta_qed`) | PS | Ch. 7, §7.5 *Renormalization of the Electric Charge* (vacuum polarization) |
| the renormalization group, Callan–Symanzik, β functions, running, Landau pole (`qed_landau_pole`, `phi4_running`) | PS | Ch. 12 *The Renormalization Group* (§12.1 Wilson, §12.2 Callan–Symanzik, §12.3 evolution of couplings) |
| fixed points & critical exponents, Wilson–Fisher (`fixed_point`, `beta_toy`) | PS | Ch. 12–13 (Ch. 13 *Critical Exponents and Scalar Field Theory*, §13.1) |
| asymptotic freedom, non-abelian β < 0 (`beta_qcd`, `qcd_running_alpha`) | PS | Ch. 16 *Quantization of Non-Abelian Gauge Theories* (§16.5–16.7 one-loop divergences & asymptotic freedom); Ch. 17 *QCD* |
| cutting off ignorance, counterterms, RG flow | Zee | Part III (§III.1–III.3); Part VI.8 *Renormalization Group Flow* |
| rigorous perturbative renormalization & the RG | Riv | Part I (power counting, BPHZ, renormalization group); Part II (constructive) |

## See also
- `~SM-05` (phase transitions & critical phenomena) — the **same** renormalization
  group: $\beta(g_*)=0$ fixed points and the linearized eigenvalues $\beta'(g_*)$ are
  the critical exponents; the Wilson–Fisher fixed point of $\phi^4$ in $d=4-\epsilon$
  is the Ising universality class. SM-05 cross-links back here.
- `~QF-02` (interactions & Feynman diagrams) — the loop integrals (vacuum
  polarization, the $\phi^4$ bubble) that diverge and are renormalized here.
- `~QF-03` (gauge theories / QED) — the electric charge that runs; gauge invariance
  (Ward identities) constrains the counterterms.
- Peskin Ch. 10 & 12 (the systematic treatment); Zee Part III & VI.8 (physical
  intuition); Rivasseau (mathematical rigor).
