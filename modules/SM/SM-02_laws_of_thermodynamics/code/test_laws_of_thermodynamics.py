"""Tests for SM-02 laws of thermodynamics. Reuses SM-01 (K_B).

Run:  python3 test_laws_of_thermodynamics.py     ->  "All N tests passed."
"""
import math

# own module first: chains SM-01 (and MA-19) onto sys.path
from laws_of_thermodynamics import (
    K_B, enthalpy, helmholtz_free_energy, gibbs_free_energy,
    temperature_from_entropy, pressure_from_helmholtz,
    maxwell_relation_residual, carnot_efficiency,
    carnot_cop_refrigerator, carnot_cop_heat_pump,
    entropy_change_heat, total_entropy_change_heat_flow,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_potentials_and_legendre():
    U, T, S, P, V = 100.0, 300.0, 0.2, 1e5, 1e-3
    H = enthalpy(U, P, V)
    F = helmholtz_free_energy(U, T, S)
    G = gibbs_free_energy(U, T, S, P, V)
    assert _approx(H, U + P * V)
    assert _approx(F, U - T * S)
    assert _approx(G, H - T * S)                          # G = H - TS
    assert _approx(G, F + P * V)                          # G = F + PV


def test_temperature_from_ideal_gas_entropy():
    # S = (3/2) N k ln U  =>  1/T = dS/dU = (3/2)Nk/U  =>  U = (3/2) N k T
    N = 2.0
    S_of_U = lambda U: 1.5 * N * K_B * math.log(U)
    U = 5.0e-21
    T = temperature_from_entropy(S_of_U, U)
    assert _approx(1.5 * N * K_B * T, U, tol=1e-4)


def test_pressure_from_free_energy():
    # ideal gas F = -N k T ln V (+ const) => P = -dF/dV = N k T / V
    NkT = 4.0
    F_of_V = lambda V: -NkT * math.log(V)
    V = 2.0
    assert _approx(pressure_from_helmholtz(F_of_V, V, T=None), NkT / V, tol=1e-5)


def test_maxwell_relation_ideal_gas():
    Nk = 3.0
    S_TV = lambda T, V: Nk * (math.log(V) + 1.5 * math.log(T))
    P_TV = lambda T, V: Nk * T / V
    assert abs(maxwell_relation_residual(S_TV, P_TV, 350.0, 2e-3)) < 1e-4


def test_carnot_efficiency():
    assert _approx(carnot_efficiency(300.0, 600.0), 0.5)
    assert _approx(carnot_efficiency(300.0, 300.0), 0.0)  # no temperature drop -> no work
    assert 0.0 < carnot_efficiency(300.0, 400.0) < 1.0    # always < 1
    # efficiency rises as the hot reservoir gets hotter
    assert carnot_efficiency(300.0, 900.0) > carnot_efficiency(300.0, 400.0)


def test_carnot_cop_identity():
    Tc, Th = 270.0, 300.0
    assert _approx(carnot_cop_heat_pump(Tc, Th), 1.0 + carnot_cop_refrigerator(Tc, Th))


def test_second_law_heat_flow():
    # heat flows hot -> cold spontaneously: total entropy increases
    dS = total_entropy_change_heat_flow(10.0, T_hot=500.0, T_cold=300.0)
    assert dS > 0
    assert _approx(dS, entropy_change_heat(10.0, 300.0) - entropy_change_heat(10.0, 500.0))
    # reversible limit (Th -> Tc): dS -> 0
    assert total_entropy_change_heat_flow(10.0, 300.001, 300.0) < dS


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
