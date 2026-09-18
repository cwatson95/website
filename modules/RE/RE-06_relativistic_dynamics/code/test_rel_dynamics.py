"""Tests for RE-06 relativistic dynamics.

Run directly:   python3 test_rel_dynamics.py     (-> "All N tests passed.")
Or with pytest: pytest test_rel_dynamics.py

Checks: the mass shell E^2 = p^2 + m^2; the Newtonian limit T -> 1/2 m v^2 and
p -> m v (matched against CM-06); conservation of total 4-momentum; the
frame-independence of system invariant mass; the antiproton threshold 6 m_p; and
the Compton shift.
"""
import math
import random

from rel_dynamics import (
    gamma, energy, momentum, kinetic_energy, four_momentum, photon_four_momentum,
    total_four_momentum, is_conserved, system_invariant_mass, com_velocity,
    inelastic_stick, threshold_kinetic_energy, compton_shift,
)
import minkowski          # RE-05 (on sys.path via rel_dynamics)
import linear_momentum    # CM-06 (on sys.path via rel_dynamics)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _boost(beta_vec):
    """Inline general Lorentz boost (so the test is self-contained)."""
    bx, by, bz = beta_vec
    b2 = bx * bx + by * by + bz * bz
    g = 1.0 / math.sqrt(1.0 - b2)
    b = [bx, by, bz]
    L = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    L[0][0] = g
    for i in range(3):
        L[0][i + 1] = L[i + 1][0] = -g * b[i]
        for j in range(3):
            L[i + 1][j + 1] = (1.0 if i == j else 0.0) + (g - 1.0) * b[i] * b[j] / b2
    return L


def _apply(L, p):
    return [sum(L[i][k] * p[k] for k in range(4)) for i in range(4)]


def _rand_v(rng, hi=0.9):
    while True:
        v = [rng.uniform(-hi, hi) for _ in range(3)]
        if sum(c * c for c in v) < hi * hi:
            return v


def test_mass_shell():
    rng = random.Random(0)
    for _ in range(300):
        m = rng.uniform(0.5, 5.0)
        v = _rand_v(rng)
        E = energy(m, v)
        p = momentum(m, v)
        psq = sum(c * c for c in p)
        assert _approx(E * E - psq, m * m)                  # E^2 - p^2 = m^2
        assert _approx(minkowski.invariant_mass(four_momentum(m, v)), m)


def test_newtonian_limit_matches_CM06():
    """At low speed: T -> 1/2 m v^2 and p -> m v (CM-06)."""
    m = 2.0
    for v1 in (1e-3, 1e-4):
        v = [v1, 0.0, 0.0]
        assert _approx(kinetic_energy(m, v), 0.5 * m * v1 * v1, 1e-4)
        # relativistic momentum collapses onto CM-06's Newtonian momentum
        assert _approx(momentum(m, v)[0], linear_momentum.momentum(m, v)[0], 1e-5)
    # rest energy
    assert _approx(energy(3.0, [0, 0, 0]), 3.0)             # E_0 = m
    # exact identity E = m + T at all speeds
    v = [0.7, 0.1, 0.0]
    assert _approx(energy(1.5, v), 1.5 + kinetic_energy(1.5, v))


def test_photon_is_null():
    p = photon_four_momentum(4.0, [1.0, 2.0, -2.0])
    assert _approx(minkowski.interval2(p), 0.0)             # null: p.p = 0
    assert _approx(p[0], math.sqrt(p[1] ** 2 + p[2] ** 2 + p[3] ** 2))  # E = |p|


def test_four_momentum_conserved_in_collision():
    """A symmetric elastic collision conserves total 4-momentum."""
    before = [four_momentum(1.0, [0.6, 0.0, 0.0]), four_momentum(1.0, [-0.6, 0.0, 0.0])]
    after = [four_momentum(1.0, [0.0, 0.6, 0.0]), four_momentum(1.0, [0.0, -0.6, 0.0])]
    assert is_conserved(before, after)                      # E and p both conserved
    # an energy-violating "after" is rejected
    bad = [four_momentum(1.0, [0.0, 0.3, 0.0]), four_momentum(1.0, [0.0, -0.3, 0.0])]
    assert not is_conserved(before, bad)


def test_system_invariant_mass_is_frame_independent():
    rng = random.Random(1)
    parts = [four_momentum(1.0, _rand_v(rng)), four_momentum(2.0, _rand_v(rng))]
    M = system_invariant_mass(parts)
    for _ in range(50):
        L = _boost(_rand_v(rng))
        boosted = [_apply(L, p) for p in parts]
        assert _approx(system_invariant_mass(boosted), M, 1e-7)   # invariant
    # two back-to-back photons: a massive system from massless parts
    g1 = photon_four_momentum(3.0, [1, 0, 0])
    g2 = photon_four_momentum(3.0, [-1, 0, 0])
    assert _approx(system_invariant_mass([g1, g2]), 6.0)          # = 2E


def test_com_frame_zeroes_momentum():
    parts = [four_momentum(1.0, [0.8, 0.0, 0.0]), four_momentum(1.0, [-0.8, 0.0, 0.0])]
    assert all(_approx(c, 0.0) for c in com_velocity(parts))      # symmetric -> COM at rest
    # asymmetric: transforming to the COM frame (boost with beta = v_com, since
    # RE-03's Lambda(beta) p has spatial part gamma(p - beta E) -> 0) zeroes p
    parts2 = [four_momentum(2.0, [0.5, 0.0, 0.0]), four_momentum(1.0, [-0.3, 0.2, 0.0])]
    vcom = com_velocity(parts2)
    L = _boost(vcom)
    P = total_four_momentum([_apply(L, p) for p in parts2])
    assert all(_approx(P[i], 0.0, 1e-7) for i in (1, 2, 3))       # P_spatial = 0 in COM


def test_inelastic_collision_gains_mass():
    """Kinetic energy converts to rest mass: the product is heavier than the sum."""
    M, v = inelastic_stick(1.0, [0.8, 0, 0], 1.0, [-0.8, 0, 0])
    assert M > 2.0                                          # heavier than 1 + 1
    assert _approx(M, 2.0 * gamma([0.8, 0, 0]))            # = 2 gamma m
    assert all(_approx(c, 0.0) for c in v)                 # symmetric -> at rest
    # energy is conserved: M (at rest) = total energy before
    Ebefore = energy(1.0, [0.8, 0, 0]) + energy(1.0, [-0.8, 0, 0])
    assert _approx(M, Ebefore)


def test_antiproton_threshold():
    """p + p -> p + p + p + pbar: lab kinetic threshold is 6 m_p (m_p = 1)."""
    assert _approx(threshold_kinetic_energy(1.0, 1.0, 4.0), 6.0)
    # pion photoproduction-style sanity: heavier products -> higher threshold
    assert threshold_kinetic_energy(1.0, 1.0, 5.0) > threshold_kinetic_energy(1.0, 1.0, 4.0)


def test_compton_shift():
    m_e = 1.0
    assert _approx(compton_shift(0.0, m_e), 0.0)            # forward: no shift
    assert _approx(compton_shift(math.pi, m_e), 2.0 / m_e)  # backscatter: max 2/m_e
    assert _approx(compton_shift(math.pi / 2, m_e), 1.0 / m_e)
    # heavier scatterer -> smaller shift (1/m_e)
    assert compton_shift(math.pi, 2.0) < compton_shift(math.pi, 1.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
