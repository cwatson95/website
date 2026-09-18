"""Tests for MA-10 Laplace transforms. Pure stdlib.

Run:  python3 test_laplace.py     ->  "All N tests passed."
"""
import math

from laplace import (
    laplace_numeric, convolve, F_const, F_exp, F_pow, F_cos, F_sin,
    invert_quadratic, solve_ivp_laplace, rk4,
)


def _approx(x, y, tol=1e-5):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_table_pairs():
    for s in (2.0, 3.5):
        assert _approx(laplace_numeric(lambda t: 1.0, s).real, F_const(s))
        assert _approx(laplace_numeric(lambda t: t * t, s).real, F_pow(2, s))
        for a in (-1.0, -0.3):
            assert _approx(laplace_numeric(lambda t, a=a: math.exp(a * t), s).real, F_exp(a, s))
        for w in (1.0, 3.0):
            assert _approx(laplace_numeric(lambda t, w=w: math.cos(w * t), s).real, F_cos(w, s))
            assert _approx(laplace_numeric(lambda t, w=w: math.sin(w * t), s).real, F_sin(w, s))


def test_derivative_rule():
    # L[f'](s) = s F(s) - f(0).  f = sin wt, f(0)=0, f' = w cos wt.
    w, s = 2.0, 3.0
    lhs = laplace_numeric(lambda t: w * math.cos(w * t), s).real
    rhs = s * F_sin(w, s) - 0.0
    assert _approx(lhs, rhs)
    # f = cos wt, f(0)=1, f' = -w sin wt
    lhs = laplace_numeric(lambda t: -w * math.sin(w * t), s).real
    rhs = s * F_cos(w, s) - 1.0
    assert _approx(lhs, rhs)


def test_first_shift_rule():
    # L[e^{at} f(t)](s) = F(s-a).   take f = cos wt
    a, w, s = -0.5, 2.0, 3.0
    lhs = laplace_numeric(lambda t: math.exp(a * t) * math.cos(w * t), s).real
    rhs = F_cos(w, s - a)
    assert _approx(lhs, rhs)


def test_convolution_theorem():
    # f=e^{-t}, g=e^{-2t} -> (f*g)(t)=e^{-t}-e^{-2t}; transform = F(s)G(s)
    f = lambda t: math.exp(-t)
    g = lambda t: math.exp(-2 * t)
    for t in (0.5, 1.3, 2.7):
        closed = math.exp(-t) - math.exp(-2 * t)
        assert _approx(convolve(f, g, t), closed, tol=1e-4)
    s = 2.5
    prod = F_exp(-1.0, s) * F_exp(-2.0, s)
    trans = laplace_numeric(lambda t: math.exp(-t) - math.exp(-2 * t), s).real
    assert _approx(trans, prod)


def test_invert_quadratic_cases():
    # underdamped: s^2 + 0 s + 4 with N(s)=s -> cos 2t
    y = invert_quadratic(1.0, 0.0, 0.0, 4.0)
    for t in (0.3, 1.1, 2.0):
        assert _approx(y(t), math.cos(2 * t), tol=1e-9)
    # overdamped distinct roots: (s+3)/((s+1)(s+2)) -> 2 e^{-t} - e^{-2t}
    #   s^2+3s+2, N(s)=s+3
    y = invert_quadratic(1.0, 3.0, 3.0, 2.0)
    for t in (0.3, 1.1, 2.0):
        assert _approx(y(t), 2 * math.exp(-t) - math.exp(-2 * t), tol=1e-9)
    # repeated root: 1/(s+1)^2 -> t e^{-t}   (b1=0,b0=1,p=2,q=1)
    y = invert_quadratic(0.0, 1.0, 2.0, 1.0)
    for t in (0.3, 1.1, 2.0):
        assert _approx(y(t), t * math.exp(-t), tol=1e-9)


def test_ivp_vs_rk4():
    cases = [
        (0.0, 4.0, 1.0, 0.0, 0.0),    # undamped
        (0.5, 4.0, 1.0, 0.0, 0.0),    # underdamped
        (5.0, 4.0, 2.0, -1.0, 0.0),   # overdamped
        (4.0, 4.0, 1.0, 0.0, 0.0),    # critically damped
        (0.5, 4.0, 0.0, 0.0, 3.0),    # step forced -> steady state 0.75
    ]
    for p, q, y0, v0, F0 in cases:
        y = solve_ivp_laplace(p, q, y0, v0, F0)
        for t in (0.5, 1.5, 3.0, 5.0):
            assert _approx(y(t), rk4(p, q, y0, v0, F0, t), tol=1e-4)


def test_step_response_steady_state():
    y = solve_ivp_laplace(0.5, 4.0, 0.0, 0.0, F0=3.0)
    assert _approx(y(20.0), 0.75, tol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
