"""Tests for CM-06 linear momentum. Pure stdlib.

Run:  python3 test_linear_momentum.py     ->  "All N tests passed."
"""
from linear_momentum import momentum, total_momentum, impulse


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_momentum():
    assert _vapprox(momentum(2.0, (3.0, 0.0, -1.0)), [6.0, 0.0, -2.0])


def test_total_momentum():
    assert _vapprox(total_momentum([2.0, 1.0], [[1, 0, 0], [-2, 0, 0]]), [0.0, 0.0, 0.0])
    assert _vapprox(total_momentum([1.0, 3.0], [[0, 2, 0], [0, 0, 1]]), [0.0, 2.0, 3.0])


def test_impulse_constant_force():
    assert _vapprox(impulse(lambda t: (3.0, 0.0, 0.0), 0.0, 2.0), [6.0, 0.0, 0.0])   # F * dt


def test_impulse_time_varying():
    # J = integral (t,0,0) dt over [0,2] = (2,0,0)
    assert _vapprox(impulse(lambda t: (t, 0.0, 0.0), 0.0, 2.0), [2.0, 0.0, 0.0], tol=1e-6)


def test_impulse_equals_delta_p():
    # particle m under constant force: J = F*dt should equal p_final - p_initial
    m, F, T = 2.0, (4.0, 0.0, 0.0), 3.0
    v0 = (1.0, 0.0, 0.0)
    a = (F[0] / m, F[1] / m, F[2] / m)
    vT = (v0[0] + a[0] * T, v0[1] + a[1] * T, v0[2] + a[2] * T)
    J = impulse(lambda t: F, 0.0, T)
    dp = [momentum(m, vT)[i] - momentum(m, v0)[i] for i in range(3)]
    assert _vapprox(J, dp, tol=1e-6)


def test_third_law_conserves_momentum():
    f = lambda t: (5.0 * t, -2.0, 1.0)
    J1 = impulse(f, 0.0, 1.0)
    J2 = impulse(lambda t: [-c for c in f(t)], 0.0, 1.0)
    assert _vapprox([J1[i] + J2[i] for i in range(3)], [0.0, 0.0, 0.0], tol=1e-9)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
