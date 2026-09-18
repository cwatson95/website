"""
enthalpy.py  —  Module 4.1 (Enthalpy)

The combination U + pV turns up so often -- in control volumes (flow work) and in
constant-pressure heating -- that Moran 8e names it the property **enthalpy** H
(Sec. 3.6.1).  Per unit mass  h = u + p v  (Eq. 3.4).  It is a property because u,
p, v all are.

Two payoffs:
  * constant-pressure closed-system heat is just  Q = m (h2 - h1) = dH  (because
    Q = dU + W = dU + p dV = d(U + pV));
  * inside the vapor dome,  h = hf + x hfg  (Eq. 3.7), the same x-weighted form as
    v and u (module 4.4).

Units: u, h [kJ/kg]; p [kPa]; v [m^3/kg], so p*v is in kJ/kg.  Citations: Moran 8e
(printed pages; PDF = printed + 18); full table in ../refs.md.
"""


def enthalpy(u, p, v):
    """Specific enthalpy  h = u + p v  [kJ/kg]  (p [kPa], v [m^3/kg]).
    [Moran Eq. 3.4, Sec. 3.6.1, p.111]"""
    return u + p * v


def enthalpy_total(U, p, V):
    """Extensive enthalpy  H = U + p V. [Moran Eq. 3.3, Sec. 3.6.1, p.111]"""
    return U + p * V


def enthalpy_molar(u_bar, p, v_bar):
    """Molar enthalpy  h_bar = u_bar + p v_bar. [Moran Eq. 3.5, Sec. 3.6.1, p.111]"""
    return u_bar + p * v_bar


def internal_energy_from_quality(uf, ug, x):
    """Two-phase internal energy  u = uf + x (ug - uf) = uf + x ufg.
    [Moran Eq. 3.6, Sec. 3.6.2, p.112]"""
    return uf + x * (ug - uf)


def enthalpy_from_quality(hf, hg, x):
    """Two-phase enthalpy  h = hf + x (hg - hf) = hf + x hfg.
    [Moran Eq. 3.7, Sec. 3.6.2, p.112]"""
    return hf + x * (hg - hf)


def quality_from_enthalpy(h, hf, hg):
    """Invert Eq. 3.7 for quality:  x = (h - hf)/(hg - hf). [Moran Sec. 3.6.2, p.112]"""
    return (h - hf) / (hg - hf)


def const_pressure_heat(h1, h2, m=1.0):
    """Closed-system heat in a CONSTANT-PRESSURE process:  Q = m (h2 - h1) = dH.
    (From Q = dU + p dV = d(U + pV).)  [Moran Sec. 3.6.1, p.111]"""
    return m * (h2 - h1)


def _demo():
    print("Module 4.1 -- Enthalpy  (h = u + p v)\n")
    h = enthalpy(2537.3, 100.0, 1.793)
    print("  water @0.10 MPa: h = u + p v = 2537.3 + 100*1.793 = %.1f kJ/kg  [Table A-4: 2716.6]" % h)
    x = (144.58 - 58.77) / (230.38 - 58.77)
    h2 = enthalpy_from_quality(59.35, 253.99, x)
    print("  R-22 @12 C: x = %.3f -> h = hf + x hfg = %.2f kJ/kg  [book 156.67]" % (x, h2))
    Q = const_pressure_heat(2939.9, 3531.9, 5.0)
    print("  const-p heat (5 kg, h: 2939.9->3531.9): Q = m dh = %.0f kJ  [book 2960]" % Q)
    print("  (contrast: at constant VOLUME Q = dU, no enthalpy -- e.g. Ex 3.3 rigid tank)")


if __name__ == "__main__":
    _demo()
