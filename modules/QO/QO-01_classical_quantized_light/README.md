# QO-01 — Classical & Quantized Light — Modes, Fock & Coherent States

First module of the **QUANTUM & NONLINEAR OPTICS** trunk (see
`modules/topic_network.txt`). This is the optics face of **KEY BRIDGE B6**: a
single mode of the electromagnetic field *is* a quantum harmonic oscillator.

- **Prerequisites:** `~QM-09` (the quantum SHO — its ladder operators $a,a^\dagger$
  are reused wholesale here), `~QM-05` (Hilbert space, bra–ket, commutators).
  Helpful: `~EM-15` (classical EM waves and the mode expansion that supplies the
  amplitude $\alpha$).
- **Cross-links:** `~EM-15` (classical modes), `~QM-09` (the oscillator, bridge
  B6), `~QF-01` (quantize *every* mode → field quantization / second
  quantization), `~QO-02` (atom–field coupling), `~QO-05` (squeezing — breaks the
  equal-quadrature noise here), `~QO-06` (nonlinear / Brillouin SBS — the user's
  research, pumped by coherent states).

## Scope
A beam of light is a set of field **modes**; classically each is an oscillation
with a complex amplitude $\alpha$ (`~EM-15`). Quantum optics promotes that
amplitude to ladder operators, so **one mode is a quantum harmonic oscillator**
(`~QM-09`, **bridge B6**): $H=\hbar\omega(a^\dagger a+\tfrac12)$,
$[a,a^\dagger]=1$, number operator $n=a^\dagger a$, energies $(n+\tfrac12)\hbar\omega$
with a **vacuum zero-point** $\tfrac12\hbar\omega$. Its eigenstates are the **Fock
(number) states** $|n\rangle$ ($n$ photons): orthonormal, $a|n\rangle=\sqrt n\,
|n-1\rangle$, $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$, with a sharp photon
number but undefined phase. The **quadratures** $X=(a+a^\dagger)/2$,
$P=(a-a^\dagger)/2i$ obey $[X,P]=i/2$, so the field has irreducible **vacuum
fluctuations** $\Delta X\,\Delta P=\tfrac14$. The **coherent states**
$|\alpha\rangle=e^{-|\alpha|^2/2}\sum_n \alpha^n/\sqrt{n!}\,|n\rangle$ are the
eigenstates of $a$ ($a|\alpha\rangle=\alpha|\alpha\rangle$); they have **Poissonian**
photon statistics ($\langle n\rangle=|\alpha|^2$, $\Delta n=\sqrt{\langle n\rangle}
=|\alpha|$, Mandel $Q=0$) and the same minimum-uncertainty, vacuum-level noise as
$|0\rangle$ — the **"most classical" states**, and the model for an ideal laser
field and for the pump/Stokes fields of the SBS work this trunk feeds. The code
builds $a,a^\dagger,n$ as matrices in a truncated Fock basis and verifies every one
of these claims numerically.

## Operations — `code/quantized_light.py`  (natural units ℏ = ω = 1)

| call | meaning | reference |
|------|---------|-----------|
| `annihilation(N)` | photon lowering operator $a$, $a\lvert n\rangle=\sqrt n\,\lvert n{-}1\rangle$ | SZ §1.1–1.2 |
| `creation(N)` | photon raising operator $a^\dagger$, $a^\dagger\lvert n\rangle=\sqrt{n{+}1}\,\lvert n{+}1\rangle$ | SZ §1.1–1.2 |
| `number(N)` | number operator $n=a^\dagger a=\mathrm{diag}(0,1,\dots)$ | SZ §1.2 |
| `commutator(A,B)` | $[A,B]=AB-BA$ (gives $[a,a^\dagger]=1$ on the interior) | SZ §1.1 |
| `energy(n)` / `zero_point_energy()` | $E_n=\hbar\omega(n{+}\tfrac12)$ / $\tfrac12\hbar\omega$ | SZ §1.1–1.2 |
| `fock_state(n, N)` | number state $\lvert n\rangle$ (orthonormal) | SZ §1.2 |
| `coherent_state(alpha, N)` | $\lvert\alpha\rangle=e^{-\lvert\alpha\rvert^2/2}\sum_n \alpha^n/\sqrt{n!}\,\lvert n\rangle$ | SZ §2.2 |
| `photon_distribution(state)` | $P(n)=\lvert\langle n\rvert\psi\rangle\rvert^2$ (Poisson for $\lvert\alpha\rangle$) | SZ §2.3 |
| `mean_n(state)` / `var_n(state)` | $\langle n\rangle$ / $(\Delta n)^2$ | SZ §2.3 |
| `mandel_q(state)` | $Q=((\Delta n)^2-\langle n\rangle)/\langle n\rangle$ (0 = Poissonian) | SZ §2.3–2.4 |
| `quadrature_x(N)` / `quadrature_p(N)` | $X=(a{+}a^\dagger)/2$ / $P=(a{-}a^\dagger)/2i$ | SZ §2.3 |
| `quadrature_variance(state)` | $(\mathrm{Var}\,X,\ \mathrm{Var}\,P)$; vacuum $=(\tfrac14,\tfrac14)$ | SZ §2.3–2.4 |
| `expectation(op, state)` | $\langle\psi\rvert op\lvert\psi\rangle/\langle\psi\vert\psi\rangle$ | — (helper) |

Constants `HBAR`, `OMEGA` ($=1$). **SZ** = Scully & Zubairy, *Quantum Optics*
(section-level; see `refs.md`).

## Use
```python
import numpy as np
from quantized_light import (annihilation, coherent_state, mean_n, var_n,
                             mandel_q, fock_state, quadrature_variance)

alpha, N = 2.0, 60
coh = coherent_state(alpha, N)                  # |alpha>, a coherent state
np.linalg.norm(annihilation(N) @ coh - alpha*coh)   # ~1e-16  -> a|alpha> = alpha|alpha>
mean_n(coh), var_n(coh)                         # (4.0, 4.0): <n>=|alpha|^2, (Dn)^2=<n>
mandel_q(coh)                                   # ~0  -> Poissonian ("most classical")
quadrature_variance(fock_state(0, N))           # (0.25, 0.25): vacuum DX DP = 1/4
```

## Run
```bash
cd code
python3 quantized_light.py        # demo: ladder, coherent <n>/Dn/Mandel-Q, vacuum DX DP = 1/4
python3 test_quantized_light.py   # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — the mode→oscillator bridge (B6), Fock states & the ladder,
  quadratures & vacuum fluctuations, coherent states & Poisson statistics
- `code/quantized_light.py`, `code/test_quantized_light.py`
- `problems/problems.md` — worked problems (Scully & Zubairy Ch.1–2)
- `refs.md` — citation table (Scully & Zubairy primary; Boyd cross-cite) + cross-links
