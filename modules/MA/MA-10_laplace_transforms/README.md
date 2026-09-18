# MA-10 — Laplace & Integral Transforms

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-07` (ODEs),
`~MA-05` (complex numbers); pairs with `~MA-09` (Fourier transforms).
**Feeds:** `~CM-15` (driven oscillator & transient response), `~EM-12` (AC
transients), and the causal Green's function of `~MA-14`.

## Scope
The Laplace transform F(s) = ∫₀^∞ f(t)e^{−st}dt as an operational calculus: the
**linearity**, **first-shift** and **derivative** rules; the **convolution
theorem** L{f∗g}=F·G; and the headline application — turning a linear
constant-coefficient ODE **initial-value problem** into algebra in s, then
inverting through the standard table (Boas Ch.8 §8–10). The forward transform is
done by quadrature; ODEs are inverted by partial fractions over the quadratic
s²+ps+q, whose root cases *are* the over/critically/under-damped responses.

## Operations — `code/laplace.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `laplace_numeric(f, s)` | F(s)=∫₀^∞ f e^{−st}dt by Simpson | Boas §8 p.437 |
| `F_const, F_exp, F_pow, F_cos, F_sin` | table pairs 1, e^{at}, tⁿ, cos, sin | Boas Table p.469 |
| `convolve(f, g, t)` | (f∗g)(t)=∫₀ᵗ f(τ)g(t−τ)dτ | Boas §10 p.445 |
| `invert_quadratic(b1, b0, p, q)` | L⁻¹ of (b₁s+b₀)/(s²+ps+q) | Boas §9 p.440; Table p.469 |
| `solve_ivp_laplace(p, q, y0, v0, F0)` | solve y″+py′+qy=F₀ via Laplace | Boas §9 p.440 |
| `rk4(...)` | independent RK4 check of the closed form | — |

## Use
```python
import math
from laplace import laplace_numeric, F_cos, convolve, solve_ivp_laplace, rk4

laplace_numeric(lambda t: math.cos(3*t), 2.0).real   # ~ F_cos(3, 2) = 2/13
# damped driven oscillator, solved by transform-algebra-invert:
y = solve_ivp_laplace(0.5, 4.0, 1.0, 0.0)            # y'' + 0.5 y' + 4 y = 0
y(2.0), rk4(0.5, 4.0, 1.0, 0.0, 0.0, 2.0)            # agree to ~1e-4
```

## Run
```bash
cd code
python3 laplace.py            # demo (table pairs, convolution, IVP vs RK4, step response)
python3 test_laplace.py       # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/laplace.py` · `code/test_laplace.py` · `problems/problems.md`
