# MA-06 — Complex Analysis

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-05`.
**Feeds:** `~QM-19` (propagators, Green's functions), `~EM-15` (dispersion,
Kramers–Kronig), `~MA-12` (special functions via contour integrals).

## Scope
Analytic functions and the **Cauchy–Riemann** conditions; **contour integration**;
**Cauchy's integral theorem & formula**; **residues** and the **residue theorem**;
the **winding number**. Complex functions are `f(z)`; contours are `gamma(t)->complex`,
and `contour_integral` is the spectrally-accurate trapezoid on a closed loop.

## Operations — `code/complex_analysis.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `cauchy_riemann(f, z)` | analytic at z? (u_x=v_y, u_y=−v_x) | Boas §14.2 p.667 |
| `complex_derivative(f, z)` | f′(z) | Boas §14.2 p.667 |
| `contour_integral(f, gamma, a, b)` | ∫_γ f dz (Cauchy thm: =0 if analytic) | Boas §14.3 p.674 |
| `circle(z0, r)` | the contour \|z−z0\|=r | — |
| `winding_number(gamma, z0)` | (1/2πi)∮ dz/(z−z0) | Boas §14.5 p.682 |
| `residue_at(f, z0)` | residue at an isolated singularity | Boas §14.5 p.682 |
| `cauchy_integral_formula(f, z0)` | f(z0) = (1/2πi)∮ f/(z−z0) dz | Boas §14.3 (Thm VI) p.675 |

## Use
```python
import cmath, math
from complex_analysis import cauchy_riemann, contour_integral, circle, residue_at

cauchy_riemann(lambda z: z*z, 1+1j)            # True  (z^2 is analytic)
cauchy_riemann(lambda z: z.conjugate(), 1+1j)  # False (not analytic)
contour_integral(lambda z: 1/z, circle(0,1), 0, 2*math.pi)   # ~ 2*pi*i
residue_at(lambda z: 1/(z*z+1), 1j)            # ~ -0.5j  (= 1/2i)
```

## Run
```bash
cd code
python3 complex_analysis.py          # demo (CR, Cauchy theorem, residues, formula)
python3 test_complex_analysis.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/complex_analysis.py` · `code/test_complex_analysis.py` · `problems/problems.md`
