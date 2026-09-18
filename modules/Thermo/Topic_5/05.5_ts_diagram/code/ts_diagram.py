"""
ts_diagram.py  —  Module 5.5 (The T-S diagram: area under a path is heat)

Entropy is defined so that for an internally reversible process dS = (dQ/T)_int,rev,
hence dQ_int,rev = T dS.  Integrating (Moran 8e Sec. 6.6.1, p.302):
      Q_int,rev = integral_1^2 T dS                (Moran Eq. 6.23)
so heat transfer in an internally reversible process is the AREA UNDER THE PATH on a
temperature-entropy (T-S) diagram, with T in KELVIN (or degrees Rankine).  As with
work on the p-V diagram, this area is path-dependent and is NOT valid for irreversible
processes.

Common reversible paths:
      isothermal (T const):     Q = T (S2 - S1)            (a rectangle)
      linear T in S:            Q = 1/2 (T1 + T2)(S2 - S1) (a trapezoid)
      isentropic (S const):     Q = 0                      (adiabatic reversible)

Carnot cycle on T-S (Moran Sec. 6.6.2, p.303): two isotherms + two isentropes form a
rectangle whose enclosed area is the net heat = net work,
      W_net = (T_H - T_C)(Delta S),   eta = W_net/Q_in = 1 - T_C/T_H.

This module computes those areas (trapezoid rule + closed forms).  Units: T [K],
S [kJ/K] (or s [kJ/kg.K]) give Q in kJ (or kJ/kg).
Citations: Moran 8e (PDF page = printed + 18).
"""


def heat_TdS(T, S):
    """Heat as the AREA under a T-S path, trapezoid rule over samples (T[i], S[i]):
    Q = integral T dS = sum 1/2 (T_i+T_{i+1})(S_{i+1}-S_i).  T must be absolute (K).
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    if len(T) != len(S) or len(T) < 2:
        raise ValueError("need >= 2 matching (T, S) samples")
    return sum(0.5 * (T[i] + T[i + 1]) * (S[i + 1] - S[i]) for i in range(len(T) - 1))


def heat_isothermal(T, S1, S2):
    """Internally reversible isothermal process:  Q = T (S2 - S1)  (rectangle on T-S).
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return T * (S2 - S1)


def heat_linear_TS(T1, T2, S1, S2):
    """Reversible path with T linear in S:  Q = 1/2 (T1 + T2)(S2 - S1)  (trapezoid).
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return 0.5 * (T1 + T2) * (S2 - S1)


def carnot_net_work(T_H, T_C, dS):
    """Carnot cycle: enclosed T-S area = net heat = net work = (T_H - T_C) dS.
    [Moran Sec. 6.6.2, p.303]"""
    return (T_H - T_C) * dS


def carnot_efficiency(T_H, T_C):
    """Carnot thermal efficiency from the T-S area ratio:  eta = 1 - T_C/T_H.
    [Moran Sec. 6.6.2, p.303; Eq. 5.9]"""
    return 1.0 - T_C / T_H


def _demo():
    print("Module 5.5 -- T-S diagram: area under the path = heat (integral T dS)\n")
    # Moran Example 6.1: water sat.liq -> sat.vap @150 C (423.15 K), isothermal reversible
    T = 423.15; s1, s2 = 1.8418, 6.8379
    print("  Ex 6.1 isothermal Q/m = T(s2-s1) = %.1f kJ/kg     [book 2114.1]"
          % heat_isothermal(T, s1, s2))
    print("     same as trapezoid integral T ds = %.1f kJ/kg" % heat_TdS([T, T], [s1, s2]))
    # Carnot cycle: T_H=600 K, T_C=300 K, dS=1 kJ/K
    TH, TC, dS = 600.0, 300.0, 1.0
    print("\n  Carnot cycle  T_H=%g K, T_C=%g K, dS=%g kJ/K:" % (TH, TC, dS))
    print("     Q_in = T_H dS = %.0f kJ ; Q_out = T_C dS = %.0f kJ" % (TH * dS, TC * dS))
    print("     W_net = (T_H-T_C)dS = %.0f kJ ; eta = 1-T_C/T_H = %.3f"
          % (carnot_net_work(TH, TC, dS), carnot_efficiency(TH, TC)))
    # closed-loop integral around the rectangle equals the net work
    loop = heat_TdS([TH, TH, TC, TC, TH], [0.0, dS, dS, 0.0, 0.0])
    print("     closed-loop integral T dS = %.0f kJ  (= W_net)" % loop)
    # isentropic leg carries no heat
    print("  isentropic (S const): Q = %.1f kJ" % heat_TdS([600.0, 300.0], [2.0, 2.0]))


if __name__ == "__main__":
    _demo()
