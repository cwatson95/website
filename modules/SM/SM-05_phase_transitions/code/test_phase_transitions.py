"""Tests for SM-05 phase transitions. Reuses SM-01 (K_B).

Run:  python3 test_phase_transitions.py     ->  "All N tests passed."
"""
import math

# own module first: chains SM-01 (and MA-19) onto sys.path
from phase_transitions import (
    K_B, critical_temperature, mean_field_magnetization, mean_field_residual,
    spontaneous_magnetization, ising_1d_magnetization,
    landau_free_energy, landau_equilibrium_magnetization, critical_exponent_beta,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_critical_temperature():
    J = 1e-21
    assert _approx(critical_temperature(4, J), 4 * J / K_B)


def test_spontaneous_magnetization_switches_at_Tc():
    Tc = 300.0
    assert spontaneous_magnetization(330.0, Tc) == 0.0      # paramagnet above Tc
    assert spontaneous_magnetization(301.0, Tc) == 0.0
    m = spontaneous_magnetization(150.0, Tc)               # ferromagnet below Tc
    assert 0.0 < m < 1.0
    assert spontaneous_magnetization(50.0, Tc) > m         # grows as T falls
    # deep cold -> nearly saturated
    assert spontaneous_magnetization(5.0, Tc) > 0.99


def test_mean_field_self_consistency():
    Tc = 300.0
    for T in (100.0, 200.0, 280.0):
        m = spontaneous_magnetization(T, Tc)
        assert abs(mean_field_residual(m, T, Tc)) < 1e-6   # m = tanh(Tc m/T)


def test_mean_field_with_field_above_Tc():
    # an applied field induces magnetization even in the paramagnetic phase
    Tc = 300.0
    m = mean_field_magnetization(400.0, Tc, reduced_field=0.1)
    assert m > 0.0
    assert abs(mean_field_residual(m, 400.0, Tc, 0.1)) < 1e-6


def test_critical_exponent_is_one_half():
    Tc = 300.0
    assert _approx(critical_exponent_beta(Tc, "landau"), 0.5, tol=1e-3)
    assert _approx(critical_exponent_beta(Tc, "meanfield"), 0.5, tol=1e-2)


def test_ising_1d_no_spontaneous_magnetization():
    # the exact 1-D chain has m = 0 at h = 0 for every T > 0 (no transition)
    J = 100.0 * K_B
    for T in (10.0, 100.0, 500.0):
        assert _approx(ising_1d_magnetization(T, J, 0.0), 0.0, tol=1e-12)
    # but a field magnetizes it, and m -> 1 as T -> 0 with the field on
    assert ising_1d_magnetization(100.0, J, 50.0 * K_B) > 0.0
    assert ising_1d_magnetization(1.0, J, 50.0 * K_B) > 0.99


def test_landau_double_well():
    Tc, a, b = 300.0, 1.0, 1.0
    # below Tc: equilibrium m0 > 0 and it is a genuine minimum (F(m0) < F(0))
    T = 250.0
    m0 = landau_equilibrium_magnetization(T, Tc, a, b)
    assert m0 > 0.0
    assert landau_free_energy(m0, T, Tc, a, b) < landau_free_energy(0.0, T, Tc, a, b)
    # symmetric well: F(+m0) = F(-m0)
    assert _approx(landau_free_energy(m0, T, Tc, a, b), landau_free_energy(-m0, T, Tc, a, b))
    # above Tc: only the m = 0 minimum
    assert landau_equilibrium_magnetization(350.0, Tc, a, b) == 0.0
    assert landau_free_energy(0.1, 350.0, Tc, a, b) > landau_free_energy(0.0, 350.0, Tc, a, b)


def test_landau_order_parameter_scaling():
    # m0 = sqrt(a(Tc-T)/2b): doubling (Tc-T) scales m0 by sqrt(2)
    Tc, a, b = 300.0, 2.0, 0.5
    m1 = landau_equilibrium_magnetization(Tc - 10.0, Tc, a, b)
    m2 = landau_equilibrium_magnetization(Tc - 20.0, Tc, a, b)
    assert _approx(m2 / m1, math.sqrt(2.0))
    assert _approx(m1, math.sqrt(a * 10.0 / (2 * b)))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
