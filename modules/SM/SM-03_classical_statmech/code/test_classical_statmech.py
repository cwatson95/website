"""Tests for SM-03 classical statistical mechanics. Reuses SM-01 (K_B).

Run:  python3 test_classical_statmech.py     ->  "All N tests passed."
"""
import math

# own module first: chains SM-01 (and MA-19) onto sys.path
from classical_statmech import (
    K_B, HBAR, partition_function, boltzmann_probability,
    internal_energy, helmholtz_from_partition, entropy_canonical,
    heat_capacity, two_level_energy, two_level_heat_capacity,
    harmonic_oscillator_energy, einstein_heat_capacity,
    equipartition_energy, grand_partition_function,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_probabilities_normalized_and_ordered():
    levels = [0.0, 1e-21, 2e-21]
    p = boltzmann_probability(levels, 50.0)
    assert _approx(sum(p), 1.0)
    assert p[0] > p[1] > p[2]                              # lower energy -> higher probability


def test_U_equals_minus_dlnZ_dbeta():
    # <E> from probabilities must equal -d ln Z / d beta
    levels = [0.0, 1e-21, 2.5e-21, 4e-21]
    T = 60.0
    U_direct = internal_energy(levels, T)
    beta = 1.0 / (K_B * T)
    db = beta * 1e-6
    lnZ = lambda b: math.log(sum(math.exp(-b * E) for E in levels))
    U_deriv = -(lnZ(beta + db) - lnZ(beta - db)) / (2.0 * db)
    assert _approx(U_direct, U_deriv, tol=1e-4)


def test_heat_capacity_is_energy_variance():
    # C = Var(E)/(k T^2) must equal the numerical dU/dT
    levels = [0.0, 1e-21, 2e-21, 3e-21]
    T = 70.0
    C_fluct = heat_capacity(levels, T)
    dT = T * 1e-5
    C_num = (internal_energy(levels, T + dT) - internal_energy(levels, T - dT)) / (2.0 * dT)
    assert _approx(C_fluct, C_num, tol=1e-3)


def test_two_level_limits():
    eps = 1e-21
    # cold: stuck in ground state, <E> -> 0
    assert two_level_energy(eps, 1.0) < 1e-6 * eps
    # hot: levels equally populated, <E> -> eps/2
    assert _approx(two_level_energy(eps, 1e8), eps / 2.0, tol=1e-3)
    # heat capacity vanishes at both extremes, positive in between (Schottky)
    assert two_level_heat_capacity(eps, 1.0) < two_level_heat_capacity(eps, eps / K_B / 2.4)
    assert two_level_heat_capacity(eps, 1e8) < two_level_heat_capacity(eps, eps / K_B / 2.4)


def test_harmonic_oscillator_limits():
    omega = 1e13
    # T -> 0: zero-point energy hbar w / 2
    assert _approx(harmonic_oscillator_energy(omega, 1.0), 0.5 * HBAR * omega, tol=1e-3)
    # T -> infinity: classical equipartition <E> -> kT
    T = 1e7
    assert _approx(harmonic_oscillator_energy(omega, T), K_B * T, tol=1e-3)


def test_einstein_heat_capacity_dulong_petit():
    omega = 1e13
    # high T -> k (Dulong-Petit per oscillator)
    assert _approx(einstein_heat_capacity(omega, 1e7), K_B, tol=1e-3)
    # low T (kT << hbar w; here hbar w/k ~ 76 K, so T=5 K gives x~15) -> frozen out
    assert einstein_heat_capacity(omega, 5.0) < 0.01 * K_B


def test_equipartition():
    # monatomic ideal gas: 3 translational DoF -> U = (3/2) N k T
    N, T = 1000.0, 300.0
    assert _approx(equipartition_energy(3, N, T), 1.5 * N * K_B * T)
    # diatomic (3 trans + 2 rot) -> (5/2) N k T
    assert _approx(equipartition_energy(5, N, T), 2.5 * N * K_B * T)


def test_free_energy_and_entropy():
    levels = [0.0, 1e-21, 2e-21]
    T = 50.0
    Z = partition_function(levels, T)
    F = helmholtz_from_partition(Z, T)
    U = internal_energy(levels, T)
    S = entropy_canonical(levels, T)
    assert _approx(F, U - T * S)                           # F = U - TS
    assert S > 0                                           # entropy positive


def test_grand_partition_function():
    # Xi = sum z^N Z_N ; for Z_N = 1 all N, Xi = sum z^N = (1-z^{Nmax+1})/(1-z)
    z = 0.5
    Xi = grand_partition_function(lambda N: 1.0, z, 10)
    assert _approx(Xi, (1 - z ** 11) / (1 - z))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
