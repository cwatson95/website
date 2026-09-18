"""Tests for RE-02 postulates of special relativity.

Run directly:   python3 test_postulates.py      (-> "All N tests passed.")
Or with pytest: pytest test_postulates.py

The checks are property-based and encode the physics, not arithmetic: the Bondi
factor is reciprocal under beta -> -beta and inverts cleanly; the radar method
recovers any placed event and is consistent with k^2 echo stretching; the
transverse light clock reproduces gamma = 1/sqrt(1-beta^2) independently of the
mirror gap; leading clocks lag by beta*L; and simultaneity fails exactly when
beta != 0 and the spatial separation is nonzero.  The Galilean (beta -> 0) limit
returns absolute time.
"""
import math
import random

from postulates import (
    gamma,
    bondi_k, beta_from_k,
    radar_coordinates,
    light_clock_gamma,
    leading_clocks_lag,
    simultaneity_breakdown,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _rand_beta(rng, hi=0.95):
    return rng.uniform(-hi, hi)


def test_bondi_k_basic_and_reciprocity():
    """k(0)=1; k matches its closed form; k(b)*k(-b)=1; k>1 receding, <1 approaching."""
    assert _approx(bondi_k(0.0), 1.0)
    rng = random.Random(0)
    for _ in range(400):
        b = _rand_beta(rng)
        k = bondi_k(b)
        assert _approx(k, math.sqrt((1.0 + b) / (1.0 - b)))   # definition
        assert _approx(k * bondi_k(-b), 1.0)                  # reciprocal in beta
        assert k > 0.0
        if b > 0.0:
            assert k > 1.0                                    # recession -> redshift
        if b < 0.0:
            assert k < 1.0                                    # approach  -> blueshift


def test_beta_from_k_inverts_bondi_k():
    """beta_from_k inverts bondi_k both ways, over beta in (-1,1) and k in (0, inf)."""
    rng = random.Random(1)
    for _ in range(400):
        b = _rand_beta(rng, 0.999)
        assert _approx(beta_from_k(bondi_k(b)), b)            # k then beta
        k = math.exp(rng.uniform(-3.0, 3.0))                 # any positive k
        assert _approx(bondi_k(beta_from_k(k)), k)            # beta then k
        assert abs(beta_from_k(k)) < 1.0                      # always sub-luminal


def test_radar_recovers_placed_event():
    """Emit at t-x, get the echo at t+x: the radar coordinates recover (t, x)."""
    rng = random.Random(2)
    for _ in range(500):
        t = rng.uniform(0.5, 10.0)
        x = rng.uniform(0.0, t)                              # x <= t: echo after emission
        t_ev, x_ev = radar_coordinates(t - x, t + x)
        assert _approx(t_ev, t) and _approx(x_ev, x)
        # midpoint / half-round-trip identities
        assert _approx(t_ev, 0.5 * ((t - x) + (t + x)))
        assert _approx(x_ev, 0.5 * ((t + x) - (t - x)))


def test_radar_consistent_with_bondi_k_squared():
    """A pulse reflected off a worldline at beta returns stretched by k^2, and the
    radar coordinates of the reflection lie on that worldline (x/t = beta)."""
    rng = random.Random(3)
    for _ in range(400):
        b = _rand_beta(rng, 0.95)
        t_send = rng.uniform(0.2, 5.0)
        t_echo = bondi_k(b) ** 2 * t_send                   # one factor of k each way
        t_ev, x_ev = radar_coordinates(t_send, t_echo)
        assert _approx(x_ev / t_ev, b)                       # event sits on the worldline
        assert _approx(beta_from_k(math.sqrt(t_echo / t_send)), b)


def test_light_clock_derives_gamma():
    """The transverse light clock reproduces gamma = 1/sqrt(1-beta^2) (several beta),
    independent of the mirror gap, and the photon triangle actually closes."""
    assert _approx(light_clock_gamma(0.0), 1.0)
    rng = random.Random(4)
    for _ in range(400):
        b = _rand_beta(rng)
        g_geom = light_clock_gamma(b)
        g_closed = 1.0 / math.sqrt(1.0 - b * b)              # independent closed form
        assert _approx(g_geom, g_closed)
        assert _approx(g_geom, gamma(b))
        assert g_geom >= 1.0                                 # time always dilates
        # gap-independence: the dilation ratio cannot depend on D
        assert _approx(light_clock_gamma(b, 3.7), g_geom)
        # the light path of length tau is the hypotenuse of legs (beta*tau, D)
        for D in (1.0, 2.5):
            tau = light_clock_gamma(b, D) * D
            assert _approx(math.hypot(b * tau, D), tau)


def test_light_clock_monotonic_and_diverges():
    """gamma grows with |beta| and blows up as beta -> 1 (c is unreachable)."""
    assert light_clock_gamma(0.9) > light_clock_gamma(0.5) > light_clock_gamma(0.1) > 1.0
    assert light_clock_gamma(0.999) > 20.0
    # even in |beta| (direction of motion does not matter for dilation)
    rng = random.Random(5)
    for _ in range(200):
        b = _rand_beta(rng)
        assert _approx(light_clock_gamma(b), light_clock_gamma(-b))


def test_leading_clocks_lag_sign_and_magnitude():
    """Offset = beta*L: linear in L, antisymmetric in beta, zero iff beta=0 or L=0."""
    rng = random.Random(6)
    for _ in range(400):
        b = _rand_beta(rng)
        L = rng.uniform(-5.0, 5.0)
        off = leading_clocks_lag(b, L)
        assert _approx(off, b * L)                           # the formula
        assert _approx(leading_clocks_lag(-b, L), -off)      # reverse motion -> swap
        assert _approx(leading_clocks_lag(b, 2.0 * L), 2.0 * off)  # linear in L
        if abs(b) > 1e-12 and abs(L) > 1e-12:
            assert abs(off) > 0.0
        # for beta, L > 0 the rear clock leads (offset positive)
        assert leading_clocks_lag(abs(b) + 0.01, abs(L) + 0.01) > 0.0
    assert _approx(leading_clocks_lag(0.0, 3.0), 0.0)        # no motion
    assert _approx(leading_clocks_lag(0.7, 0.0), 0.0)        # coincident clocks


def test_simultaneity_breakdown_formula_and_zeros():
    """dt' = gamma(dt - beta*dx); for events simultaneous in S (dt=0) it is
    -gamma*beta*dx, zero iff beta=0 or dx=0."""
    rng = random.Random(7)
    for _ in range(500):
        b = _rand_beta(rng)
        dt = rng.uniform(-4.0, 4.0)
        dx = rng.uniform(-4.0, 4.0)
        g = 1.0 / math.sqrt(1.0 - b * b)                     # independent gamma
        assert _approx(simultaneity_breakdown(b, dt, dx), g * (dt - b * dx))
        # events simultaneous in S
        sim = simultaneity_breakdown(b, 0.0, dx)
        assert _approx(sim, -g * b * dx)
        if abs(b) > 1e-9 and abs(dx) > 1e-9:
            assert abs(sim) > 0.0                            # NOT simultaneous in S'
    # the two listed escape hatches give exact simultaneity in S' too
    assert _approx(simultaneity_breakdown(0.0, 0.0, 9.0), 0.0)   # beta = 0
    assert _approx(simultaneity_breakdown(0.8, 0.0, 0.0), 0.0)   # dx = 0


def test_galilean_limit():
    """As beta -> 0 the postulates' machinery collapses to Newton: k -> 1, gamma -> 1,
    dt' -> dt (absolute time), and the simultaneity offset vanishes (~CM-03 / RE-01)."""
    small = 1e-7
    assert _approx(bondi_k(small), 1.0, tol=1e-6)
    assert _approx(light_clock_gamma(small), 1.0, tol=1e-6)
    assert _approx(simultaneity_breakdown(small, 2.0, 3.0), 2.0, tol=1e-6)  # dt' -> dt
    assert _approx(leading_clocks_lag(small, 3.0), 0.0, tol=1e-6)
    # exact Galilean point
    assert _approx(bondi_k(0.0), 1.0)
    assert _approx(light_clock_gamma(0.0), 1.0)
    assert _approx(simultaneity_breakdown(0.0, 2.0, 3.0), 2.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
