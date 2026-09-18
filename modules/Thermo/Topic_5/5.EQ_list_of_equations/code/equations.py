"""
equations.py  —  Module 5.EQ (Topic 5: canonical equation registry, Property Data)

The key equations of Topic 5 (Moran 8e Ch.3 "Evaluating Properties", plus the Ch.6 T-s
material) in canonical form, one per function:
  * quality and the two-phase mixture rule (Eqs. 3.1, 3.2, 3.6, 3.7, 6.4)
  * enthalpy definition (Eqs. 3.3, 3.4)
  * linear interpolation in the property tables (Sec. 3.5.1)
  * saturated-liquid approximations for compressed liquid (Eqs. 3.11-3.14, 6.5)
  * area interpretations: boundary work W=integral p dV (Eq. 2.17) on the p-v diagram,
    and reversible heat Q=integral T dS (Eq. 6.23) on the T-s diagram; Carnot eta (Eq. 5.9)

test_equations.py checks each value AND imports the concept modules 5.1-5.5, asserting
they reproduce these forms (so any formula drift fails the test).

Citations: Moran 8e (printed pages; PDF = printed + 18).  Full table in ../equations.md
and ../refs.md.
"""
import math


# --- quality & two-phase mixture rule (Moran Sec. 3.3, 3.5.2, 3.6.2, 6.2.2) ---
def quality(m_vap, m_liq):
    """x = m_vap/(m_liq + m_vap), the vapor mass fraction. [Moran Eq. 3.1, Sec. 3.3, p.102]"""
    return m_vap / (m_liq + m_vap)


def mixture(yf, yg, x):
    """Two-phase property  y = yf + x (yg - yf)  for y = v, u, h, s.
    [Moran Eq. 3.2 (v), 3.6 (u), 3.7 (h), p.108/112; Eq. 6.4 (s), p.293]"""
    return yf + x * (yg - yf)


def quality_from_v(v, vf, vg):
    """Invert the mixture rule:  x = (v - vf)/(vg - vf). [Moran Eq. 3.2, Sec. 3.5.2, p.108]"""
    return (v - vf) / (vg - vf)


# --- enthalpy definition (Moran Sec. 3.6.1) ---------------------------------
def enthalpy_extensive(U, p, V):
    """H = U + pV. [Moran Eq. 3.3, Sec. 3.6.1, p.111]"""
    return U + p * V


def enthalpy(u, p, v):
    """h = u + p v  (per unit mass). [Moran Eq. 3.4, Sec. 3.6.1, p.111]"""
    return u + p * v


# --- interpolation (Moran Sec. 3.5.1) ---------------------------------------
def linear_interp(x, x1, x2, y1, y2):
    """Linear interpolation y(x) between (x1,y1) and (x2,y2). [Moran Sec. 3.5.1, p.105]"""
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


# --- saturated-liquid approximations (Moran Sec. 3.10.1, 6.2.3) -------------
def v_approx(vf_T):
    """v(T, p) ~= vf(T). [Moran Eq. 3.11, Sec. 3.10.1, p.123]"""
    return vf_T


def u_approx(uf_T):
    """u(T, p) ~= uf(T). [Moran Eq. 3.12, Sec. 3.10.1, p.123]"""
    return uf_T


def h_approx(hf_T, vf_T, p, psat_T):
    """h(T, p) ~= hf(T) + vf(T)[p - psat(T)]  (consistent units, e.g. p,psat in kPa,
    vf in m^3/kg -> kJ/kg). [Moran Eq. 3.13, Sec. 3.10.1, p.123]"""
    return hf_T + vf_T * (p - psat_T)


def h_approx_simple(hf_T):
    """h(T, p) ~= hf(T)  (pressure term negligible). [Moran Eq. 3.14, Sec. 3.10.1, p.123]"""
    return hf_T


def s_approx(sf_T):
    """s(T, p) ~= sf(T). [Moran Eq. 6.5, Sec. 6.2.3, p.293]"""
    return sf_T


# --- area interpretations: work on p-v, heat on T-s (Moran Sec. 2.2.5, 6.6.1)
def work_isobaric(p, V1, V2):
    """Internally reversible isobaric boundary work  W = p (V2 - V1).
    [Moran Eq. 2.17, Sec. 2.2.5, p.49]"""
    return p * (V2 - V1)


def work_pdV(p, V):
    """Boundary work as the area under a p-V path (trapezoid rule):
    W = integral p dV = sum 1/2 (p_i+p_{i+1})(V_{i+1}-V_i). [Moran Eq. 2.17, p.49]"""
    return sum(0.5 * (p[i] + p[i + 1]) * (V[i + 1] - V[i]) for i in range(len(p) - 1))


def heat_isothermal(T, S1, S2):
    """Internally reversible isothermal heat  Q = T (S2 - S1), T absolute (K).
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return T * (S2 - S1)


def heat_TdS(T, S):
    """Reversible heat as the area under a T-S path (trapezoid rule), T absolute (K).
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return sum(0.5 * (T[i] + T[i + 1]) * (S[i + 1] - S[i]) for i in range(len(T) - 1))


def carnot_efficiency(T_H, T_C):
    """Carnot efficiency from the T-S area ratio:  eta = 1 - T_C/T_H.
    [Moran Sec. 6.6.2, p.303; Eq. 5.9]"""
    return 1.0 - T_C / T_H


REGISTRY = [
    ("3.1",  "quality",            "x = m_vap/(m_liq+m_vap)",        "5.1", "Sec. 3.3, p.102"),
    ("3.2",  "mixture",            "y = yf + x(yg-yf)  [v]",         "5.1", "Sec. 3.5.2, p.108"),
    ("3.2'", "quality_from_v",     "x = (v-vf)/(vg-vf)",             "5.1", "Sec. 3.5.2, p.108"),
    ("3.6",  "mixture",            "u = uf + x(ug-uf)",              "5.1", "Sec. 3.6.2, p.112"),
    ("3.7",  "mixture",            "h = hf + x(hg-hf)",              "5.1", "Sec. 3.6.2, p.112"),
    ("6.4",  "mixture",            "s = sf + x(sg-sf)",              "5.1", "Sec. 6.2.2, p.293"),
    ("3.3",  "enthalpy_extensive", "H = U + pV",                     "5.2", "Sec. 3.6.1, p.111"),
    ("3.4",  "enthalpy",           "h = u + pv",                     "5.2", "Sec. 3.6.1, p.111"),
    ("--",   "linear_interp",      "y = y1 + (x-x1)/(x2-x1)(y2-y1)", "5.2", "Sec. 3.5.1, p.105"),
    ("3.11", "v_approx",           "v(T,p) ~= vf(T)",                "5.3", "Sec. 3.10.1, p.123"),
    ("3.12", "u_approx",           "u(T,p) ~= uf(T)",                "5.3", "Sec. 3.10.1, p.123"),
    ("3.13", "h_approx",           "h ~= hf + vf[p-psat]",           "5.3", "Sec. 3.10.1, p.123"),
    ("3.14", "h_approx_simple",    "h(T,p) ~= hf(T)",                "5.3", "Sec. 3.10.1, p.123"),
    ("6.5",  "s_approx",           "s(T,p) ~= sf(T)",                "5.3", "Sec. 6.2.3, p.293"),
    ("2.17", "work_isobaric",      "W = p(V2-V1)  (area on p-V)",    "5.4", "Sec. 2.2.5, p.49"),
    ("2.17", "work_pdV",           "W = integral p dV",              "5.4", "Sec. 2.2.5, p.49"),
    ("6.23", "heat_isothermal",    "Q = T(S2-S1)  (area on T-S)",    "5.5", "Sec. 6.6.1, p.302"),
    ("6.23", "heat_TdS",           "Q = integral T dS",              "5.5", "Sec. 6.6.1, p.302"),
    ("5.9",  "carnot_efficiency",  "eta = 1 - T_C/T_H",              "5.5", "Sec. 6.6.2, p.303"),
]


def _demo():
    print("Module 5.EQ -- Topic 5 (Property Data: Tables & Diagrams) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print(f"  [{mod}] Eq {eq:<5} {fn:<19} {form:<33} [Moran {src}]")


if __name__ == "__main__":
    _demo()
