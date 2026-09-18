"""SM-05  Phase transitions & critical phenomena -- Ising, mean field, Landau.

Physics topic network, module SM-05 (modules/topic_network.txt).
Source: Pathria 3e, Ch. 12 (criticality / mean field), Ch. 13 (exact Ising),
Ch. 14 (renormalization group).  Builds on ~SM-01 (K_B); ~QF-04 is the field-
theoretic RG.

The **mean-field (Weiss) Ising model** replaces each spin's neighbors by their
average, giving the self-consistency (Pa Sect. 12.5)
    m = tanh[(T_c/T) m + b],     T_c = q J / k  (q = coordination number),
which has a nonzero **spontaneous magnetization** below T_c and m = 0 above it --
a continuous (second-order) transition with critical exponent beta = 1/2.  The
**exact 1-D Ising** model (Pa Sect. 13.2) has NO transition at T > 0.  **Landau
theory** expands the free energy F = a(T-T_c)m^2 + b m^4, whose double well below
T_c reproduces the same m ~ (T_c - T)^{1/2}.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "SM-01_probability_ensembles", "code"))
if _SM01 not in sys.path:
    sys.path.insert(0, _SM01)

from probability_ensembles import K_B                       # noqa: E402

__all__ = [
    "K_B", "critical_temperature", "mean_field_magnetization",
    "mean_field_residual", "spontaneous_magnetization",
    "ising_1d_magnetization", "landau_free_energy",
    "landau_equilibrium_magnetization", "critical_exponent_beta",
]


# --- mean-field (Weiss) Ising model (Pa Sect. 12.5) --------------------------

def critical_temperature(q, J):
    """Mean-field critical temperature  T_c = q J / k  (q = number of neighbors)."""
    return q * J / K_B


def mean_field_magnetization(T, Tc, reduced_field=0.0, iters=200):
    """Self-consistent magnetization from  m = tanh[(Tc/T) m + b]  (b = reduced
    field mu B / kT), solved by bisection on f(m) = m - tanh[(Tc/T) m + b].

    Bisection (not fixed-point iteration) is essential near Tc: there the map's
    slope -> 1 and naive iteration suffers critical slowing down, mis-estimating
    the order parameter and its exponent."""
    a = Tc / T
    f = lambda m: m - math.tanh(a * m + reduced_field)
    if reduced_field == 0.0:
        if a <= 1.0:
            return 0.0                                 # no spontaneous magnetization at T >= Tc
        lo, hi = 1e-12, 1.0                            # bracket the nontrivial root (skip m=0)
    elif reduced_field > 0.0:
        lo, hi = 0.0, 1.0                              # field > 0 -> m > 0
    else:
        lo, hi = -1.0, 0.0
    # f < 0 below the root, f > 0 above it; compare f(mid) to 0 directly so the
    # bracket survives tanh saturating to 1.0 at large Tc/T (else f(hi) rounds to 0).
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm < 0.0:
            lo = mid
        elif fm > 0.0:
            hi = mid
        else:
            return mid
    return 0.5 * (lo + hi)


def mean_field_residual(m, T, Tc, reduced_field=0.0):
    """Residual of the self-consistency equation  m - tanh[(Tc/T) m + b]  (~0 at a solution)."""
    return m - math.tanh((Tc / T) * m + reduced_field)


def spontaneous_magnetization(T, Tc):
    """Zero-field spontaneous magnetization: nonzero for T < Tc, exactly 0 for
    T >= Tc (the order parameter of the ferromagnetic transition)."""
    if T >= Tc:
        return 0.0
    return mean_field_magnetization(T, Tc, 0.0)


# --- exact 1-D Ising model (Pa Sect. 13.2) -----------------------------------

def ising_1d_magnetization(T, J, h):
    """Exact magnetization per spin of the 1-D Ising chain (transfer matrix):
        m = sinh(bh) / sqrt(sinh^2(bh) + e^{-4 bJ}),   b = 1/kT.
    At h = 0 this is 0 for every T > 0: NO spontaneous magnetization in 1-D."""
    b = 1.0 / (K_B * T)
    sh = math.sinh(b * h)
    return sh / math.sqrt(sh * sh + math.exp(-4.0 * b * J))


# --- Landau theory (Pa Sect. 12.10) ------------------------------------------

def landau_free_energy(m, T, Tc, a=1.0, b=1.0):
    """Landau free energy density  F(m) = a(T - Tc) m^2 + b m^4  (a, b > 0).
    Single well (min at m=0) for T > Tc, double well (min at +/- m0) for T < Tc."""
    return a * (T - Tc) * m ** 2 + b * m ** 4


def landau_equilibrium_magnetization(T, Tc, a=1.0, b=1.0):
    """Order parameter minimizing F:  m0 = sqrt(a(Tc - T)/(2b)) for T < Tc, else 0.
    Near Tc this gives m0 ~ (Tc - T)^{1/2}: the mean-field exponent beta = 1/2."""
    if T >= Tc:
        return 0.0
    return math.sqrt(a * (Tc - T) / (2.0 * b))


def critical_exponent_beta(Tc, model="landau", a=1.0, b=1.0):
    """Estimate the order-parameter exponent beta in m ~ (Tc - T)^beta near Tc,
    by the log-log slope of m vs (Tc - T).  Mean field / Landau give beta = 1/2."""
    t1, t2 = 1e-4, 1e-5                               # reduced distances (Tc - T)/Tc
    if model == "landau":
        m1 = landau_equilibrium_magnetization(Tc * (1 - t1), Tc, a, b)
        m2 = landau_equilibrium_magnetization(Tc * (1 - t2), Tc, a, b)
    else:
        m1 = mean_field_magnetization(Tc * (1 - t1), Tc, 0.0)
        m2 = mean_field_magnetization(Tc * (1 - t2), Tc, 0.0)
    return math.log(m1 / m2) / math.log(t1 / t2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-05 phase transitions & critical phenomena -- demo")
    print("=" * 52)

    Tc = 300.0
    print(f"mean-field Ising (Tc = {Tc} K), zero-field spontaneous magnetization:")
    for T in (150.0, 270.0, 300.0, 330.0):
        m = spontaneous_magnetization(T, Tc)
        print(f"  T={T:>6} K (T/Tc={T/Tc:.2f}): m = {m:.4f}  "
              f"(residual {mean_field_residual(m, T, Tc):.1e})")
    print("  -> order parameter m switches on continuously below Tc (2nd-order transition).")

    print(f"\ncritical exponent beta (m ~ (Tc-T)^beta):")
    print(f"  mean field: {critical_exponent_beta(Tc, 'meanfield'):.4f}   "
          f"Landau: {critical_exponent_beta(Tc, 'landau'):.4f}   (exact mean-field value = 0.5)")

    print(f"\nexact 1-D Ising (J/k = 100 K): NO spontaneous magnetization")
    J = 100.0 * K_B
    for T in (50.0, 200.0):
        print(f"  T={T:>5} K: m(h=0) = {ising_1d_magnetization(T, J, 0.0):.2e}  "
              f"m(h: muB/k=20K) = {ising_1d_magnetization(T, J, 20.0*K_B):.4f}")

    print(f"\nLandau free energy F(m) = a(T-Tc)m^2 + b m^4:")
    for T in (270.0, 330.0):
        m0 = landau_equilibrium_magnetization(T, Tc)
        well = "double well" if T < Tc else "single well"
        print(f"  T={T} K ({well}): equilibrium m0 = {m0:.4f}, F(m0) = {landau_free_energy(m0, T, Tc):.3f}")


if __name__ == "__main__":
    _demo()
