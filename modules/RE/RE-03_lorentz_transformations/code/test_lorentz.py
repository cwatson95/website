"""Tests for RE-03 Lorentz transformations.

Run directly:   python3 test_lorentz.py        (-> "All N tests passed.")
Or with pytest: pytest test_lorentz.py

The checks are property-based: random boosts must (i) preserve the Minkowski
metric eta, (ii) leave every interval invariant, (iii) keep the light cone, and
(iv) realise velocity addition as rapidity addition.
"""
import math
import random

from lorentz import (
    gamma, rapidity, beta_from_rapidity,
    boost, general_boost, identity4, apply, compose, inverse,
    dot4, interval2, classify,
    velocity_add, four_velocity, three_velocity, velocity_add_3d,
    preserves_eta, is_proper, is_orthochronous, ETA,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _mapprox(A, B, tol=1e-8):
    return all(_approx(A[i][j], B[i][j], tol) for i in range(4) for j in range(4))


def _rand_beta(rng, hi=0.95):
    return rng.uniform(-hi, hi)


def _rand_beta_vec(rng, hi=0.9):
    """A random velocity 3-vector with |beta| < hi."""
    while True:
        b = [rng.uniform(-hi, hi) for _ in range(3)]
        if b[0] ** 2 + b[1] ** 2 + b[2] ** 2 < hi * hi:
            return b


def _rand_event(rng):
    return [rng.uniform(-3.0, 3.0) for _ in range(4)]


def test_gamma_rapidity_consistency():
    assert _approx(gamma(0.0), 1.0)
    rng = random.Random(0)
    for _ in range(300):
        b = _rand_beta(rng)
        phi = rapidity(b)
        assert _approx(gamma(b), math.cosh(phi))            # gamma = cosh phi
        assert _approx(gamma(b) * b, math.sinh(phi))        # gamma beta = sinh phi
        assert _approx(beta_from_rapidity(phi), b)          # tanh inverts artanh


def test_boost_preserves_metric():
    rng = random.Random(1)
    for _ in range(300):
        for axis in (1, 2, 3):
            assert preserves_eta(boost(_rand_beta(rng), axis))
        assert preserves_eta(general_boost(_rand_beta_vec(rng)))


def test_general_boost_reduces_to_axis():
    rng = random.Random(2)
    for _ in range(200):
        b = _rand_beta(rng)
        assert _mapprox(general_boost((b, 0.0, 0.0)), boost(b, 1))
        assert _mapprox(general_boost((0.0, b, 0.0)), boost(b, 2))
        assert _mapprox(general_boost((0.0, 0.0, b)), boost(b, 3))
    assert _mapprox(general_boost((0.0, 0.0, 0.0)), identity4())


def test_interval_invariance():
    rng = random.Random(3)
    for _ in range(400):
        L = general_boost(_rand_beta_vec(rng))
        x = _rand_event(rng)
        assert _approx(interval2(apply(L, x)), interval2(x))
        # the full Minkowski product of two vectors is invariant too
        y = _rand_event(rng)
        assert _approx(dot4(apply(L, x), apply(L, y)), dot4(x, y))


def test_rapidity_additivity():
    """Collinear boosts compose by adding rapidities == adding velocities."""
    rng = random.Random(4)
    for _ in range(300):
        b1, b2 = _rand_beta(rng, 0.9), _rand_beta(rng, 0.9)
        w = velocity_add(b1, b2)
        assert _approx(rapidity(b1) + rapidity(b2), rapidity(w))      # phi adds
        assert _mapprox(compose(boost(b1), boost(b2)), boost(w))      # boosts compose


def test_velocity_addition_bounds_and_light():
    rng = random.Random(5)
    for _ in range(500):
        u, v = _rand_beta(rng, 0.999), _rand_beta(rng, 0.999)
        assert abs(velocity_add(u, v)) < 1.0                 # never reach c
        assert _approx(velocity_add(v, 1.0), 1.0)            # c (+) v = c
        assert _approx(velocity_add(v, -1.0), -1.0)


def test_velocity_add_3d_matches_collinear_and_caps():
    rng = random.Random(6)
    for _ in range(300):
        u, v = _rand_beta(rng, 0.9), _rand_beta(rng, 0.9)
        w3 = velocity_add_3d((u, 0.0, 0.0), (v, 0.0, 0.0))
        assert _approx(w3[0], velocity_add(u, v))            # collinear agreement
        assert _approx(w3[1], 0.0) and _approx(w3[2], 0.0)
        # a general boost of a general velocity stays sub-luminal
        uv, vv = _rand_beta_vec(rng), _rand_beta_vec(rng)
        w = velocity_add_3d(uv, vv)
        assert math.sqrt(sum(c * c for c in w)) < 1.0


def test_light_speed_is_invariant():
    """A photon's 3-speed is 1 in every frame (the whole point of SR)."""
    rng = random.Random(7)
    for _ in range(300):
        # null event along a random direction: (t, t n_hat)
        n = _rand_beta_vec(rng, 1.0)
        nn = math.sqrt(sum(c * c for c in n)) or 1.0
        n = [c / nn for c in n]
        photon = [1.0, n[0], n[1], n[2]]
        assert _approx(interval2(photon), 0.0)
        out = apply(general_boost(_rand_beta_vec(rng)), photon)
        speed = math.sqrt(out[1] ** 2 + out[2] ** 2 + out[3] ** 2) / out[0]
        assert _approx(speed, 1.0)
        assert classify(out) == "null"


def test_inverse_is_opposite_boost():
    rng = random.Random(8)
    for _ in range(300):
        b = _rand_beta_vec(rng)
        L = general_boost(b)
        assert _mapprox(compose(inverse(L), L), identity4())
        assert _mapprox(inverse(L), general_boost((-b[0], -b[1], -b[2])))


def test_proper_orthochronous():
    rng = random.Random(9)
    for _ in range(200):
        L = general_boost(_rand_beta_vec(rng))
        assert is_proper(L)               # det = +1
        assert is_orthochronous(L)        # L^0_0 >= 1
    # a spatial parity flip is a Lorentz transformation but NOT proper
    P = identity4(); P[1][1] = -1.0
    assert preserves_eta(P) and not is_proper(P)
    # time reversal preserves eta but is not orthochronous
    T = identity4(); T[0][0] = -1.0
    assert preserves_eta(T) and not is_orthochronous(T)


def test_four_velocity_normalisation():
    rng = random.Random(10)
    for _ in range(300):
        v = _rand_beta_vec(rng)
        U = four_velocity(v)
        assert _approx(dot4(U, U), -1.0)                     # U.U = -1 (timelike)
        assert _approx(three_velocity(U)[0], v[0])
        # boosting a 4-velocity is still a unit timelike vector
        Up = apply(general_boost(_rand_beta_vec(rng)), U)
        assert _approx(dot4(Up, Up), -1.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
