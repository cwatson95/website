"""Tests for CM-11 central-force motion. Reuses CM-07/MA-07 (imported transitively).

Run:  python3 test_central_force.py     ->  "All N tests passed."
"""
import math

from central_force import (
    effective_potential, kepler_potential, kepler_force,
    circular_orbit_radius, kepler_period, orbit,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_effective_potential_minimum():
    mu, k, L = 1.0, 2.0, 1.5
    r0 = circular_orbit_radius(L, mu, k)
    Ueff = effective_potential(kepler_potential(k), L, mu)
    deriv = (Ueff(r0 + 1e-6) - Ueff(r0 - 1e-6)) / 2e-6
    assert abs(deriv) < 1e-4                                  # circular orbit = min of U_eff
    second = (Ueff(r0 + 1e-4) - 2 * Ueff(r0) + Ueff(r0 - 1e-4)) / 1e-8
    assert second > 0                                         # it's a minimum (stable)


def test_circular_orbit_stays_circular():
    mu, k, L = 1.0, 1.0, 1.0
    r0 = circular_orbit_radius(L, mu, k)
    vc = L / (mu * r0)
    ts, ys = orbit(kepler_force(k), mu, (r0, 0.0), (0.0, vc), 0.0, kepler_period(r0, mu, k), 4000)
    radii = [math.hypot(s[0], s[1]) for s in ys]
    assert max(radii) - min(radii) < 1e-3                     # radius constant


def test_energy_and_angular_momentum_conserved():
    mu, k = 1.0, 1.0
    # an elliptical bound orbit (perihelion start, v less than circular)
    r0 = 1.0
    vc = math.sqrt(k / (mu * r0))                             # circular speed here
    v = 0.8 * vc                                              # bound ellipse
    ts, ys = orbit(kepler_force(k), mu, (r0, 0.0), (0.0, v), 0.0, 6.0, 6000)
    U = kepler_potential(k)

    def E(s):
        r = math.hypot(s[0], s[1])
        return 0.5 * mu * (s[2] ** 2 + s[3] ** 2) + U(r)

    def Lz(s):
        return mu * (s[0] * s[3] - s[1] * s[2])
    E0, L0 = E(ys[0]), Lz(ys[0])
    for s in ys[::200]:
        assert _approx(E(s), E0, tol=1e-4)                   # energy conserved
        assert _approx(Lz(s), L0, tol=1e-4)                  # angular momentum conserved
    assert E0 < 0                                             # bound orbit


def test_kepler_third_law():
    mu, k = 1.0, 1.0
    ratios = [kepler_period(a, mu, k) ** 2 / a ** 3 for a in (0.5, 1.0, 2.0, 4.0)]
    for rr in ratios:
        assert _approx(rr, ratios[0])                        # T^2/a^3 is the same for all orbits
    assert _approx(ratios[0], 4 * math.pi ** 2 * mu / k)     # = 4 pi^2 mu / k


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
