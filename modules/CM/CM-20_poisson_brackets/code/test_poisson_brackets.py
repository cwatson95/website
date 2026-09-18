"""Tests for CM-20 Poisson brackets. Pure stdlib.

Run:  python3 test_poisson_brackets.py     ->  "All N tests passed."
"""
import random

from poisson_brackets import poisson_bracket, time_derivative, is_canonical

Q = lambda q, p: q
P = lambda q, p: p


def _approx(x, y, tol=1e-5):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_fundamental_brackets():
    rng = random.Random(0)
    for _ in range(50):
        q, p = rng.uniform(-2, 2), rng.uniform(-2, 2)
        assert _approx(poisson_bracket(Q, P, q, p), 1.0)        # {q,p}=1
        assert _approx(poisson_bracket(Q, Q, q, p), 0.0)        # {q,q}=0
        assert _approx(poisson_bracket(P, P, q, p), 0.0)        # {p,p}=0


def test_antisymmetry():
    rng = random.Random(1)
    f = lambda q, p: q * q + p
    g = lambda q, p: q * p - p * p
    for _ in range(50):
        q, p = rng.uniform(-2, 2), rng.uniform(-2, 2)
        assert _approx(poisson_bracket(f, g, q, p), -poisson_bracket(g, f, q, p))


def test_equation_of_motion():
    # for H = p^2/2 + 1/2 w^2 q^2:  {q,H}=p,  {p,H}=-w^2 q
    w = 2.0
    H = lambda q, p: 0.5 * p * p + 0.5 * w * w * q * q
    for q, p in ((1.0, 0.5), (-0.3, 2.0), (1.5, -1.0)):
        assert _approx(time_derivative(Q, H, q, p), p, tol=1e-4)            # qdot = p
        assert _approx(time_derivative(P, H, q, p), -w * w * q, tol=1e-4)   # pdot = -w^2 q


def test_conserved_quantity_has_zero_bracket():
    # a free particle H=p^2/2: {p,H}=0, so p is conserved
    H = lambda q, p: 0.5 * p * p
    assert _approx(time_derivative(P, H, 1.0, 0.7), 0.0, tol=1e-5)
    assert _approx(poisson_bracket(H, H, 1.0, 0.7), 0.0)                    # {H,H}=0


def test_canonical_transformations():
    assert is_canonical(lambda q, p: 2 * q, lambda q, p: p / 2, 1.0, 1.0)   # scaling
    assert is_canonical(lambda q, p: p, lambda q, p: -q, 1.0, 1.0)          # swap (q,p)->(p,-q)
    assert not is_canonical(lambda q, p: q, lambda q, p: 2 * p, 1.0, 1.0)   # {Q,P}=2, not canonical


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
