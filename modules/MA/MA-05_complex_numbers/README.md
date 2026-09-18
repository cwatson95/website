# MA-05 — Complex Numbers

Math trunk (see `modules/topic_network.txt`). **Prereq:** none (root).
**Feeds:** `~MA-06` (complex analysis), `~EM-12`/`~CM-15` (AC circuits &
oscillations via e^{iωt}), `~QM-02` (complex wavefunctions), and complex
eigenvalues from `~MA-04`.

## Scope
Polar form (modulus & argument), Euler's formula e^{iθ}=cosθ+i sinθ, De Moivre's
theorem, the n distinct nth roots of a complex number, and the **principal
branch** of √ and log (with the negative-real-axis cut). Python already has
`complex`/`cmath`; this module exposes the mechanics explicitly. Pure stdlib.

## Operations — `code/complex_numbers.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `modulus`, `argument`, `to_polar`, `from_polar` | r, arg, polar form r e^{iθ} | Boas §3 p.47, §4 p.49 |
| `euler(theta)` | e^{iθ} = cosθ + i sinθ | Boas §9 p.61 |
| `de_moivre(theta, n)` | (cosθ+i sinθ)ⁿ = cos nθ + i sin nθ | Boas §10 p.64 |
| `power(z, n)` | zⁿ via rⁿ e^{inθ} | Boas §10 p.64 |
| `nth_roots(z, n)`, `roots_of_unity(n)` | the n nth roots | Boas §10 p.64 |
| `principal_sqrt`, `principal_log` | principal branch of √, log | Boas §11 p.67, §13 p.72 |
| `conjugate` | x − iy | Boas §4–5 |

## Use
```python
import math
from complex_numbers import euler, de_moivre, nth_roots, roots_of_unity, principal_log

euler(math.pi)               # ~ -1+0j     (e^{i*pi} = -1)
de_moivre(0.3, 5)            # = euler(0.3)**5
roots_of_unity(3)            # three cube roots of 1; they sum to 0
principal_log(complex(-1,0)) # i*pi        (Log(-1), principal value)
```

## Run
```bash
cd code
python3 complex_numbers.py          # demo (Euler, De Moivre, roots, principal branch)
python3 test_complex_numbers.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/complex_numbers.py` · `code/test_complex_numbers.py` · `problems/problems.md`
