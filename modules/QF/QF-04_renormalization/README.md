# QF-04 — Renormalization & the Renormalization Group

Fourth module of the **QUANTUM FIELD THEORY** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QF-02` (loop diagrams & the S-matrix — the integrals that
  diverge), `~QF-03` (QED & gauge invariance — the coupling that runs).
- **Cross-links:** `~SM-05` (the *same* renormalization group: fixed points,
  critical exponents, universality), `~QF-02` (vacuum polarization / the $\phi^4$
  bubble), `~QF-03` (the QED electric charge).

## Scope
Loop corrections in quantum field theory are ultraviolet-**divergent**. One first
**regularizes** them — a momentum cutoff $\Lambda$, or symmetry-preserving
**dimensional regularization** in $d=4-\epsilon$ — and then **renormalizes**: the
divergences are absorbed into unmeasurable *bare* parameters via $Z$-factors and
**counterterms**, leaving every physical quantity finite. The residue of this
procedure is that the renormalized coupling depends on the sliding scale $\mu$ at
which it is defined; how it slides is the **beta function** $\beta(g)=\mu\,dg/d\mu$,
and its integral is the **running coupling** — the heart of the **renormalization
group**. In **QED** vacuum polarization screens charge, $\beta(\alpha)=+2\alpha^2/3\pi>0$,
so $\alpha$ grows with energy ($\alpha(0)\approx1/137\to\alpha(M_Z)\approx1/128$) up
to an astronomically high **Landau pole**. Scalar **$\phi^4$** shares the sign
($\beta=3\lambda^2/16\pi^2>0$, "triviality"); non-abelian **QCD** reverses it
($\beta<0$, **asymptotic freedom**). A zero $\beta(g_*)=0$ is a **fixed point** whose
linearized slope $\beta'(g_*)$ sets its stability — and those eigenvalues are exactly
the **critical exponents** of statistical mechanics, the bridge to `~SM-05`.

## Operations — `code/renormalization.py`  (scales in GeV)

| call | meaning | reference |
|------|---------|-----------|
| `beta_qed(alpha, sum_q2=1)` | β(α) = (2/3π) S α² > 0 | PS Ch. 7, 12 |
| `qed_running_alpha(Q, alpha0, Q0, sum_q2=1)` | α(Q) = α₀/[1 − (α₀/3π)S ln(Q²/Q0²)] | PS Ch. 7 |
| `qed_alpha_sm(Q)` | α(Q) summed over all charged SM fermions → 1/128 at M_Z | PS Ch. 7 |
| `qed_landau_pole(alpha0, Q0, sum_q2=1)` | Q = Q0 exp(3π/2α₀S), denominator → 0 | PS Ch. 12 |
| `beta_phi4(lam)` | β(λ) = 3λ²/16π² > 0 | PS Ch. 10, 12 |
| `phi4_running(lam0, mu0, mu)` | integrate dλ/d ln μ = β(λ) (scipy) | PS Ch. 12 |
| `phi4_landau_pole(lam0, mu0)` | triviality scale μ₀ exp(16π²/3λ₀) | PS Ch. 12 |
| `beta_qcd(alpha_s, nf=5)` | β = −(b₀/2π)α_s², b₀ = 11 − (2/3)n_f < 0 | PS Ch. 16, 17 |
| `qcd_running_alpha(Q, alpha_s0, Q0, nf=5)` | α_s(Q) decreases with Q (asymptotic freedom) | PS Ch. 16, 17 |
| `beta_toy(g, a, b)` | toy β(g) = a g² − b g³ | PS Ch. 12 |
| `fixed_point(a, b)` | g* = a/b, β'(g*) = −a²/b, stability | PS Ch. 12–13 |

Constants: `ALPHA0` (≈1/137), `M_E`, `M_MU`, `M_TAU`, `M_Z`, `SM_FERMIONS`.

## Use
```python
from renormalization import qed_running_alpha, qed_alpha_sm, qed_landau_pole, fixed_point, M_Z

1.0 / qed_running_alpha(M_Z)        # 134.5: electron loop alone (1/137 -> 1/134.5)
1.0 / qed_alpha_sm(M_Z)             # 128.4: all charged SM fermions -> measured ~1/128
qed_landau_pole()                   # ~1.45e277 GeV  (>> Planck scale 1e19 GeV)
fixed_point(2.0, 4.0)               # g*=0.5, beta'=-1.0 -> 'UV-attractive'
```

## Run
```bash
cd code
python3 renormalization.py          # demo: alpha(Q), alpha(M_Z)~1/128, Landau pole, phi4, QCD, fixed point
python3 test_renormalization.py     # tests  ->  "All 9 tests passed."
```

## Files
- `notes.md` — divergences → regularization → renormalization → RG, with derivations
- `code/renormalization.py`, `code/test_renormalization.py`
- `problems/problems.md` — worked problems (Peskin Ch.7, 10, 12, 16)
- `refs.md` — citation table (Peskin primary; Zee, Rivasseau cross-cites; `~SM-05`)
