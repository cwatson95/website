"""Tests for MA-06 complex analysis. Pure stdlib.

Run:  python3 test_complex_analysis.py     ->  "All N tests passed."
"""
import cmath
import math

from complex_analysis import (
    cauchy_riemann, complex_derivative, contour_integral, circle,
    winding_number, residue_at, cauchy_integral_formula,
)

PI = math.pi


def _capprox(z, w, tol=1e-6):
    return abs(z - w) <= tol * (1.0 + abs(w))


def test_cauchy_riemann():
    assert cauchy_riemann(lambda z: z * z, 1 + 1j)
    assert cauchy_riemann(cmath.exp, 0.3 + 0.7j)
    assert cauchy_riemann(lambda z: z ** 3, -0.5 + 0.4j)
    assert not cauchy_riemann(lambda z: z.conjugate(), 1 + 1j)      # anti-analytic
    assert not cauchy_riemann(lambda z: z.real + 0j, 0.7 + 0.2j)    # Re z


def test_complex_derivative():
    assert _capprox(complex_derivative(lambda z: z * z, 2 + 1j), 2 * (2 + 1j), tol=1e-4)
    assert _capprox(complex_derivative(lambda z: z ** 3, 1 + 1j), 3 * (1 + 1j) ** 2, tol=1e-4)
    assert _capprox(complex_derivative(cmath.exp, 0.5 + 0.5j), cmath.exp(0.5 + 0.5j), tol=1e-4)


def test_cauchy_integral_theorem():
    # analytic integrand around a closed loop -> 0
    unit = circle(0, 1)
    assert _capprox(contour_integral(lambda z: z * z, unit, 0, 2 * PI), 0, tol=1e-6)
    assert _capprox(contour_integral(cmath.exp, unit, 0, 2 * PI), 0, tol=1e-6)
    # the canonical nonzero one: oint dz/z = 2 pi i
    assert _capprox(contour_integral(lambda z: 1 / z, unit, 0, 2 * PI), 2j * PI, tol=1e-5)


def test_winding_number():
    unit = circle(0, 1)
    assert _capprox(winding_number(unit, 0.0), 1.0, tol=1e-5)        # encloses 0 once
    assert _capprox(winding_number(unit, 0.5), 1.0, tol=1e-5)        # 0.5 inside
    assert _capprox(winding_number(unit, 2.0), 0.0, tol=1e-5)        # 2 outside
    assert _capprox(winding_number(circle(0, 1), 0.0, n=4000), 1.0, tol=1e-5)


def test_residues():
    assert _capprox(residue_at(lambda z: 1 / (z - 1), 1 + 0j), 1 + 0j, tol=1e-5)
    assert _capprox(residue_at(lambda z: 1 / (z * z + 1), 1j), 1 / (2j), tol=1e-4)   # = -0.5i
    assert _capprox(residue_at(lambda z: 1 / (z * z), 0 + 0j), 0 + 0j, tol=1e-5)     # double pole, res 0


def test_residue_theorem():
    # oint f = 2 pi i * sum of enclosed residues
    f = lambda z: z / ((z - 0.3) * (z - 0.6))
    loop = contour_integral(f, circle(0, 1), 0, 2 * PI)
    r1, r2 = residue_at(f, 0.3 + 0j), residue_at(f, 0.6 + 0j)
    assert _capprox(r1, -1 + 0j, tol=1e-4) and _capprox(r2, 2 + 0j, tol=1e-4)
    assert _capprox(loop, 2j * PI * (r1 + r2), tol=1e-4)


def test_cauchy_integral_formula():
    assert _capprox(cauchy_integral_formula(cmath.exp, 0 + 0j), 1 + 0j, tol=1e-5)
    f = lambda z: z * z + 3
    assert _capprox(cauchy_integral_formula(f, 0.5 + 0j, r=0.4), f(0.5 + 0j), tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
