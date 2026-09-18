"""
third_law.py  —  Module 3.4 (Third Law)

The third law fixes the ZERO of the entropy scale.  Moran 8e Sec. 13.5.1 (p.837):

   "the entropy of a PURE CRYSTALLINE substance is zero at the absolute zero of
    temperature, 0 K or 0 degR."

Substances without a perfect-crystal structure at 0 K keep a nonzero *residual*
entropy.  With S(0)=0 as the datum, the **absolute entropy** at any T follows from
calorimetry:  S(T) = \\int_0^T c_p(T')/T' dT'  (entropy definition, Sec. 6.2 / module
4.2).  Near T=0 the Debye result c_p ~ a T^3 makes the integrand a T^2 -> 0, so the
integral converges to a finite value -- consistent with, and required by, the law.

A practical corollary is **unattainability**: a reversible refrigerator's COP
T_C/(T_H - T_C) -> 0 as T_C -> 0, so removing the last bit of heat to reach 0 K
would take unbounded work (cf. Sec. 5.9.2).

Citations: Moran 8e (printed pages; PDF = printed + 18); see ../refs.md.
T must be ABSOLUTE (K or degR).
"""


def standard_entropy_at_zero(pure_crystalline=True):
    """Third law: S(0 K) = 0 for a PURE CRYSTALLINE substance; non-crystalline
    substances keep residual entropy (return None -> not fixed by the law).
    [Moran Sec. 13.5.1, p.837]"""
    return 0.0 if pure_crystalline else None


def debye_cp(T, a):
    """Low-temperature Debye heat capacity  c_p ~ a T^3  (standard T->0 limit).
    Used to show the absolute-entropy integral converges."""
    return a * T ** 3


def absolute_entropy(T, cp_func, n_steps=20000, T0=1e-9):
    """Absolute (third-law) entropy  S(T) = \\int_0^T c_p(T')/T' dT', with S(0)=0.
    Integrates from a tiny T0>0 (trapezoid); for c_p ~ T^3 the integrand -> 0 at 0,
    so the result is finite. [Moran Sec. 13.5.1, p.837; entropy def. Sec. 6.2]"""
    h = (T - T0) / n_steps
    f = lambda Tp: cp_func(Tp) / Tp
    tot = 0.5 * (f(T0) + f(T))
    for k in range(1, n_steps):
        tot += f(T0 + k * h)
    return tot * h


def absolute_entropy_debye(T, a):
    """Closed form for c_p = a T^3:  S(T) = \\int_0^T a T'^2 dT' = a T^3 / 3.
    Analytic check of absolute_entropy()."""
    return a * T ** 3 / 3.0


def carnot_cop_refrigerator(T_C, T_H):
    """Reversible refrigerator COP  beta = T_C/(T_H - T_C)  (module 3.3, Eq. 5.10).
    beta -> 0 as T_C -> 0: the third-law UNATTAINABILITY corollary. [Moran Sec. 5.9.2, p.267]"""
    return T_C / (T_H - T_C)


def _demo():
    print("Module 3.4 -- Third Law  (S=0 for a pure crystal at 0 K)\n")
    print("  S(0 K), pure crystal      :", standard_entropy_at_zero(True))
    print("  S(0 K), non-crystalline   :", standard_entropy_at_zero(False), "(residual entropy)")
    a = 1.0e-3
    print("\n  Absolute entropy with Debye c_p = a T^3 (a=1e-3):")
    for T in (10.0, 20.0):
        num = absolute_entropy(T, lambda Tp: debye_cp(Tp, a))
        ana = absolute_entropy_debye(T, a)
        print("    T=%4.0f K:  numeric S = %.5f   analytic aT^3/3 = %.5f" % (T, num, ana))
    print("\n  Unattainability (T_H = 300 K), COP_ref = T_C/(T_H - T_C):")
    for T_C in (250.0, 50.0, 1.0):
        print("    T_C=%6.1f K -> COP = %.4f" % (T_C, carnot_cop_refrigerator(T_C, 300.0)))
    print("    COP -> 0 as T_C -> 0: reaching absolute zero needs unbounded work.")


if __name__ == "__main__":
    _demo()
