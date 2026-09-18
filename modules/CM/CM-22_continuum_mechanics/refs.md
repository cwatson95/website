# CM-22 — References

**Verification:** Boas and Griffiths both have real **text layers** (citations
text-extracted and confirmed). *(The ClassicalMechanics shelf — Fowles/M&T/
Goldstein — is particle & rigid-body mechanics with no continuum chapter, so the
continuity equation is cited from the vector-calculus and EM texts where it is
actually derived and named.)*

| Book (edition) | File | Printed → PDF | source |
|---|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** | text-verified |
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** | text-verified |

| Topic (code) | Source | Section / title | Printed p. | PDF p. |
|---|---|---|---|---|
| continuity equation for **mass**; ∇·(ρv)+∂ρ/∂t=0 (`continuity_residual`) | Boas | Ch.6 §10 *The Divergence and the Divergence Theorem* (Eq. 10.9, "Equation of continuity") | 317 | 336 |
| velocity field / divergence as net outflow per volume (`material_derivative`, `divergence_of_velocity`) | Boas | Ch.6 §10 (fluid-flow setup, p.314; "net rate of outflow per unit volume", p.316) | 314–316 | 333–335 |
| continuity equation for **charge** (first named) | Griffiths | §5.1.3 *Currents* (∇·J = −∂ρ/∂t, Eq. 5.29; "it is called the continuity equation") | 222 | 240 |
| **The Continuity Equation** (the cross-domain bridge) | Griffiths | §8.1.1 *The Continuity Equation* ("the paradigm for all conservation laws", Eq. 8.4) | 356 | 374 |

- Built on `~MA-02`'s `divergence`/`gradient`; the divergence-theorem derivation is Boas Ch.6 §10 (= `~MA-02` refs).
