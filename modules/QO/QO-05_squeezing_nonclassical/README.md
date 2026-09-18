# QO-05 — Squeezing & Nonclassical Light — Squeezed & Entangled Photons

A node of the **QUANTUM & NONLINEAR OPTICS** trunk (see `modules/topic_network.txt`).
Ties directly to the user's squeezed-light / SBS / `Quantum_Optics` research.

- **Prerequisites:** `~QO-01` (classical & quantized light: modes, coherent and
  Fock states — the standard-quantum-limit baseline), `~QM-09` (the oscillator
  ladder operators $a,a^\dagger$ and quadratures). Helpful: `~QM-07` (the
  uncertainty relation that squeezing saturates).
- **Cross-links:** `~QM-21` (entanglement, EPR, Bell — §6 is the continuous-
  variable instance), `~QO-06` (the $\chi^{(2)}$ parametric / four-wave-mixing
  processes that physically generate squeezed & entangled light; SBS),
  `~QO-04` (open systems — how squeezing decoheres).

## Scope
The vacuum of a single field mode (`~QM-09`) carries irreducible zero-point noise:
each **quadrature** $X_1=(a+a^\dagger)/2$, $X_2=(a-a^\dagger)/2i$ fluctuates with
variance $\tfrac14$, the **standard quantum limit** (SQL), and coherent states sit
at the same bound. **Squeezing** redistributes that noise. The **squeeze operator**
$S(\xi)=\exp[\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})]$, $\xi=re^{i\phi}$, drives the
**squeezed vacuum** $|\xi\rangle=S(\xi)|0\rangle$, whose quadrature variances are
$\tfrac14 e^{-2r}$ and $\tfrac14 e^{+2r}$ — one pushed **below** the vacuum noise at
the cost of the other, with product pinned at the minimum $\tfrac1{16}$. Built from
$a^2,a^{\dagger2}$, $S$ makes photons in **pairs**, so the squeezed vacuum contains
**only even** photon numbers with $\langle n\rangle=\sinh^2 r$. Such states are
**nonclassical** — no classical stochastic field reproduces them — but nonclassicality
has independent faces: quadrature squeezing (variance $<\tfrac14$), and
sub-Poissonian / antibunched counting ($g^{(2)}(0)<1$, Mandel $Q<0$; a Fock state).
Tellingly, the squeezed vacuum is quadrature-squeezed yet **super**-Poissonian.
Promoting $a^2\to ab$ gives **two-mode squeezing**: the photon-number-correlated,
EPR-entangled state $\propto\sum_n\tanh^n r\,|n,n\rangle$ with joint quadratures
below the SQL (`~QM-21`), the resource produced by parametric down-conversion
(`~QO-06`). The code builds all of this in a truncated Fock basis and checks every
closed form.

## Operations — `code/squeezing.py`  (natural units $\hbar=1$)

| call | meaning | reference |
|------|---------|-----------|
| `annihilation(N)` / `creation(N)` | $a$, $a^\dagger$ in the $N$-level Fock basis | SZ §1.1.2 |
| `quadrature_operators(N)` | $X_1=(a{+}a^\dagger)/2$, $X_2=(a{-}a^\dagger)/2i$; $[X_1,X_2]=i/2$ | SZ §2.7.1 |
| `vacuum_state` / `fock_state(n,N)` / `coherent_state(α,N)` | reference states (the SQL baseline) | SZ §2.2–2.4 |
| `squeeze_operator(r, N, phi)` | $S(\xi)=\exp[\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})]$ via `expm` | SZ §2.7 |
| `squeezed_vacuum(r, N, phi)` | $\lvert\xi\rangle=S(\xi)\lvert0\rangle$ (even photons; $r{=}0\to$ vacuum) | SZ §2.7 |
| `quadrature_variances(state)` | $(\mathrm{Var}\,X_1,\mathrm{Var}\,X_2)=(\tfrac14 e^{-2r},\tfrac14 e^{+2r})$ | SZ §2.7.1 |
| `photon_distribution(state)` | $P(n)=\lvert\langle n\lvert\psi\rangle\rvert^2$ (odd $\to0$) | SZ §2.7 |
| `mean_photon(r)` / `mean_photon_number(state)` | $\langle n\rangle=\sinh^2 r$ (closed / summed) | SZ §2.7 |
| `g2_zero(state)` / `mandel_q(state)` | $g^{(2)}(0)$, $Q$ — sub-/super-Poissonian test | SZ §4.4.4 |
| `two_mode_squeeze_operator(r, N, phi)` | $S_2=\exp(\xi^{*}ab-\xi a^\dagger b^\dagger)$ | SZ §16.1 |
| `two_mode_squeezed_vacuum(r, N, phi)` | $\mathrm{sech}\,r\sum_n\tanh^n r\,\lvert n,n\rangle$ (EPR) | SZ Ch.16, 18 |
| `two_mode_photon_distribution(state, N)` | joint $P(n_a,n_b)$ (diagonal) | SZ Ch.16 |
| `epr_variances(r, N, phi)` | $\mathrm{Var}(X_a{+}X_b)=\mathrm{Var}(Y_a{-}Y_b)=\tfrac12 e^{-2r}$ | SZ Ch.18 |

Constants: `DEFAULT_N` = 80 (single-mode), `TWO_MODE_N` = 16 (per mode).

## Use
```python
import numpy as np
from squeezing import (squeezed_vacuum, quadrature_variances,
                       photon_distribution, mean_photon, epr_variances)

sv = squeezed_vacuum(r=0.8)                  # S(r)|0> in the N=80 Fock basis
quadrature_variances(sv)                     # (0.0505, 1.238) = (1/4 e^-2r, 1/4 e^+2r)
float(np.prod(quadrature_variances(sv)))     # 0.0625 = 1/16  (minimum uncertainty)
photon_distribution(sv)[1::2].max()          # ~1e-17  ->  only even photon numbers
mean_photon(0.8)                             # 0.789 = sinh^2(0.8)
epr_variances(0.6)                           # (0.151, 0.151) < 0.5  ->  two-mode EPR
```

## Run
```bash
cd code
python3 squeezing.py        # demo: SQL vs squeezed variances, even-only photons, g2/Q, two-mode EPR
python3 test_squeezing.py   # tests  ->  "All 17 tests passed."
```

## Files
- `notes.md` — quadratures & the SQL; the squeeze operator & Bogoliubov transform;
  squeezed-vacuum variances; even-photon statistics & $\langle n\rangle=\sinh^2 r$;
  $g^{(2)}(0)$/Mandel $Q$; two-mode squeezing & EPR
- `code/squeezing.py`, `code/test_squeezing.py` (numpy + scipy only; self-contained)
- `problems/problems.md` — worked problems (Scully & Zubairy Ch. 2–3, 16, 18)
- `refs.md` — citation table (Scully & Zubairy, section/chapter granularity) + cross-links
