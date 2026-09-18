# MA-15 — The Dirac Delta & Distributions

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-09` (Fourier),
basic integration. **Feeds:** `~MA-14` (the point source L G = δ), `~QM-02`/`~QM-05`
(position eigenstates, ⟨x|x′⟩=δ(x−x′)), `~EM-01` (point-charge density).

## Scope
The Dirac delta as the limit of **nascent sequences** (Gaussian, Lorentzian, box,
sinc) and as a **linear functional** — the sifting map φ ↦ φ(0). The defining
**sifting property**, the **composition rule** δ(g(x))=Σ δ(x−x_i)/|g′(x_i)|, the
**derivative** δ′ (⟨δ′,φ⟩=−φ′(0)), the **Heaviside relation** H′=δ, and the
**Fourier representation** δ(x)=(1/2π)∫e^{ikx}dk. Every identity is realized as the
small-width limit of an explicit sequence and checked by quadrature.

## Operations — `code/dirac_delta.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `gaussian_delta, lorentzian_delta, box_delta, sinc_delta` | nascent δ sequences | Boas §11 p.449 |
| `sift(phi, x0, kind, a)` | ∫δ_a(x−x0)φ dx → φ(x0) | Boas §11 p.449 |
| `delta_compose_rhs / _integral` | δ(g(x))=Σ δ(x−x_i)/|g′(x_i)| | Boas §11 eq.11.19e p.456 |
| `gaussian_delta_prime`, `delta_prime_sift` | ⟨δ′,φ⟩=−φ′(0) | Boas §11 p.449 |
| `heaviside` | step with H′=δ | Boas §11 p.449 |
| `fourier_delta_kernel(x, K)` | sin(Kx)/(πx)→δ; ∫e^{ikx}dk/2π | Boas §11 p.454; Ch.7 §12 p.378 |

## Use
```python
import math
from dirac_delta import sift, delta_compose_rhs, delta_prime_sift

sift(lambda x: math.cos(x) + 0.3*math.sin(2*x), 1.2, "gaussian", 0.01)  # -> phi(1.2)
delta_compose_rhs(lambda x: x*x, [1.5, -1.5], lambda x: 2*x)            # delta(x^2-c^2)
delta_prime_sift(lambda x: math.exp(-x), 0.03)                          # -> -psi'(0) = +1
```

## Run
```bash
cd code
python3 dirac_delta.py        # demo (sifting, composition, delta', Heaviside, Fourier kernel)
python3 test_dirac_delta.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/dirac_delta.py` · `code/test_dirac_delta.py` · `problems/problems.md`
