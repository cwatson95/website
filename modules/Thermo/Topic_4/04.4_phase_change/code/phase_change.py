"""
phase_change.py  —  Module 4.4 (Phase change & quality)

Inside the vapor dome a liquid-vapor mixture's intensive state is NOT fixed by T and
p alone (they are dependent along the saturation line) -- you need a second property,
the **quality**  x = m_vapor / m_total  (Moran 8e Eq. 3.1, Sec. 3.3): x = 0 at
saturated liquid, x = 1 at saturated vapor.

Every specific property of the mixture is the saturated-liquid value plus x times the
"evaporation" increment (subscript fg) -- the SAME form for v, u, h, s:
    v = vf + x vfg      (Eq. 3.2)
    u = uf + x ufg      (Eq. 3.6)
    h = hf + x hfg      (Eq. 3.7)
    s = sf + x sfg      (Eq. 6.4)         (Moran: "identical in form", p.112/312)

So `mixture_property(yf, yg, x)` covers all four; invert it to FIND quality from any
measured property.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


def quality(m_vapor, m_total):
    """Quality  x = m_vapor / m_total  (dimensionless, 0..1).
    [Moran Eq. 3.1, Sec. 3.3, p.102]"""
    return m_vapor / m_total


def mixture_property(yf, yg, x):
    """Any specific property of a two-phase mixture:  y = yf + x (yg - yf) = yf + x yfg.
    Same form for v, u, h, s. [Moran Eqs. 3.2/3.6/3.7/6.4]"""
    return yf + x * (yg - yf)


def quality_from_property(y, yf, yg):
    """Invert the mixture relation for quality:  x = (y - yf)/(yg - yf).
    Works for v, u, h, or s. [Moran Sec. 3.5.2, p.108]"""
    return (y - yf) / (yg - yf)


def latent_heat(hf, hg):
    """Latent heat of vaporization  hfg = hg - hf  [kJ/kg]. [Moran Sec. 3.5.2]"""
    return hg - hf


def mass_from_volume(V, v):
    """Total mass from volume and specific volume:  m = V / v."""
    return V / v


def liquid_volume_fraction(x, vf, vg):
    """Fraction of TOTAL volume occupied by the liquid phase:
    V_liq/V = (1 - x) vf / [vf + x(vg - vf)].
    Tiny even at large x, because vg >> vf (HW 3.16). [Moran Sec. 3.3-3.5]"""
    v = mixture_property(vf, vg, x)
    return (1.0 - x) * vf / v


def _demo():
    print("Module 4.4 -- Phase change & quality  (y = yf + x*yfg)\n")
    # water at 100 C, x = 0.9
    v = mixture_property(1.0435e-3, 1.673, 0.9)
    print("  water @100 C, x=0.9: v = vf + x*vfg = %.3f m^3/kg   [book 1.506]" % v)
    # latent heat of water at 100 C
    print("  latent heat hfg(100 C) = hg - hf = %.1f kJ/kg          [book ~2257]"
          % latent_heat(419.04, 2676.1))
    # HW 3.16: CO2 tank, x=0.7
    vf, vg, x = 0.9827e-3, 1.756e-2, 0.7
    v = mixture_property(vf, vg, x); m = mass_from_volume(1.0, v)
    print("\n  CO2 tank (1 m^3, x=0.7): v=%.6f, m=%.1f kg" % (v, m))
    print("    m_vap=%.1f kg, m_liq=%.1f kg; liquid fills %.2f%% of the volume  [book 2.34%%]"
          % (x * m, (1 - x) * m, 100 * liquid_volume_fraction(x, vf, vg)))


if __name__ == "__main__":
    _demo()
