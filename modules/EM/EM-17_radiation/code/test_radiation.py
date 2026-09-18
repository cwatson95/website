"""Tests for EM-17 radiation. Reuses EM-01/EM-08 and MA-01.

Run:  python3 test_radiation.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-08 (and MA-01/MA-02) onto sys.path
from radiation import (
    C, retarded_time, retarded_potential_static,
    lienard_wiechert, larmor_power,
    dipole_radiated_power, dipole_angular_power, total_power_from_pattern,
)
from electrostatics import K_E
from magnetostatics import MU0
from vector_algebra import norm


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_retarded_time_static():
    # static source -> t_r = t - r/c
    src, fp = (0.0, 0.0, 0.0), (3.0, 4.0, 0.0)     # r = 5
    traj = lambda t: src
    tr = retarded_time(fp, traj, t=10.0)
    assert _approx(tr, 10.0 - 5.0 / C)


def test_lienard_wiechert_reduces_to_coulomb_for_static():
    # a charge at rest: LW potential = Coulomb, A = 0
    q = 2e-9
    src = (0.0, 0.0, 0.0)
    traj = lambda t: src
    vel = lambda t: (0.0, 0.0, 0.0)
    fp = (0.0, 0.0, 2.0)
    V, A, tr = lienard_wiechert(q, traj, vel, fp, t=5.0)
    assert _approx(V, K_E * q / 2.0)
    assert norm(A) == 0.0
    assert _approx(tr, 5.0 - 2.0 / C)


def test_lienard_wiechert_beaming_enhances_potential():
    # a charge moving toward the field point has its potential enhanced by
    # the 1/(1 - rhat.v/c) factor relative to the instantaneous Coulomb value
    q, v0 = 1e-9, 0.6 * C
    traj = lambda t: (v0 * t, 0.0, 0.0)
    vel = lambda t: (v0, 0.0, 0.0)
    fp = (10.0, 0.0, 0.0)                            # ahead, on the motion axis
    V, A, tr = lienard_wiechert(q, traj, vel, fp, t=0.0)
    sep = abs(fp[0] - v0 * tr)
    V_inst = K_E * q / sep
    assert V > V_inst                                # beaming enhancement
    assert norm(A) > 0                               # moving charge -> vector potential


def test_larmor_scaling():
    q = 1.602e-19
    P1 = larmor_power(q, 1e20)
    P2 = larmor_power(q, 2e20)
    assert P1 > 0
    assert _approx(P2 / P1, 4.0)                     # P ~ a^2
    assert _approx(larmor_power(q, 1e20), MU0 * q ** 2 * 1e40 / (6.0 * math.pi * C))


def test_dipole_power_scaling():
    P1 = dipole_radiated_power(1e-11, 1e8)
    P2 = dipole_radiated_power(1e-11, 2e8)
    assert _approx(P2 / P1, 16.0)                    # P ~ w^4 (Rayleigh / blue sky)
    P3 = dipole_radiated_power(2e-11, 1e8)
    assert _approx(P3 / P1, 4.0)                     # P ~ p0^2


def test_dipole_pattern_integrates_to_total():
    # integral of dP/dOmega over the sphere = <P>
    p0, w = 1e-11, 2 * math.pi * 1e8
    assert _approx(total_power_from_pattern(p0, w), dipole_radiated_power(p0, w), tol=1e-3)


def test_dipole_pattern_shape():
    p0, w = 1e-11, 1e8
    # null along the axis (theta=0), maximum broadside (theta=pi/2)
    assert _approx(dipole_angular_power(0.0, p0, w), 0.0)
    assert dipole_angular_power(math.pi / 2, p0, w) > dipole_angular_power(math.pi / 4, p0, w) > 0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
