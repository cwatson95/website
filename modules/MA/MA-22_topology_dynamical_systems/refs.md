# MA-22 — References

Page-level citations **verified by reading the page text** in the PDFs.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Chicone, *Ordinary Differential Equations with Applications*, **2nd ed.** | `MA_Mathematics/ode_with_applications_chicone.pdf` | PDF = printed **+ 20** |
| Hatcher, *Algebraic Topology* | `MA_Mathematics/algebraic_topology_hatcher.pdf` | PDF = printed **+ 9** |

(PDF = 1-based viewer page. For PyMuPDF use `load_page(PDF − 1)`.)

### Dynamical systems — Chicone
| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| existence/uniqueness of solutions | §1.1 *Existence and Uniqueness* | 3 | 23 |
| rest point (equilibrium) definition | §1.6 (Definition 1.38) | 10 | 30 |
| stability & linearization; eigenvalue classification (`classify_equilibrium`) | §1.6 *Stability and Linearization* (sink/source/saddle/center/spiral) | 20–23 | 40–43 |
| Lyapunov function/exponent (`lyapunov_logistic`) | *strict Lyapunov function* | 28 | 48 |
| limit cycle | (figure & discussion) | 95 | 115 |
| Poincaré–Bendixson theorem | *Limit Sets and Poincaré–Bendixson Theory* | 91 | 111 |
| bifurcation / period-doubling (`period_of_orbit`) | §8 *Local Bifurcation*; first example | 545; 13 | 565; 33 |
| chaos / the Lorenz system (`logistic` as the discrete analogue) | Ch.6 *…Chaos*; Lorenz system | 449; 33 | 469; 53 |

### Topology — Hatcher
| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Euler characteristic (`euler_characteristic`, `PLATONIC`) | intro; §*Euler Characteristic* | 6; 146 | 15; 155 |
| CW / cell complex (how V,E,F are defined) | Ch.0 | 5 | 14 |
| the idea of homology (χ = alternating sum of Betti numbers) | *The Idea of Homology* | 98 | 107 |
| fundamental group π₁ (the deeper invariant) | §1.1 (Prop. 1.3: π₁ is a group) | 26 | 35 |

## Notes (verified)
- **Honest caveat (Chicone):** the book classifies planar equilibria by the **real
  parts of the eigenvalues** of the Jacobian (sink/source/saddle/center/spiral,
  pp.20–23). It has **no named "trace–determinant plane"** figure — the `tr`/`det`
  shortcut gives the same eigenvalues, but the citation is the eigenvalue
  classification, not a trace–determinant diagram.
- Chicone's offset (+19) is pinned by the index entry "Lorenz system, 33, 454" and
  the §1.1 running head; Hatcher's (+8) by "The Idea of Homology / 99" and the
  §2.1 running heads.
- The logistic map itself is the standard discrete-time chaos exemplar; Chicone's
  continuous-time bifurcation/chaos chapters (Ch.8, Ch.6) are the cited anchors,
  with the map as their one-dimensional analogue.
