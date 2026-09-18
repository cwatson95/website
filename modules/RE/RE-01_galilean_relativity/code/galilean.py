"""
RE-01  Galilean relativity & its failure  --  the Galilean transformation, its
invariance for Newton but not for Maxwell, and the Michelson-Morley experiment.

Part of the physics topic network (see modules/topic_network.txt, module RE-01).
Prerequisites: ~CM-03 (reference frames / Galilean boosts).  Feeds into: RE-02
(the postulates that replace it), RE-03 (the Lorentz transformation it is the
c -> infinity limit of).

THE ONE IDEA.  Galilean relativity -- velocities just add, time is absolute --
is exactly right for mechanics and exactly wrong for light.  Newton's laws are
invariant under a Galilean boost (acceleration, hence F = m a, is unchanged), but
Maxwell's equations carry a fixed speed c = 1/sqrt(eps0 mu0) with no reference to
any frame, so Galilean velocity addition would make light travel at c - v in a
boosted frame.  The Michelson-Morley experiment looked for that v and found
nothing.  The fix is not a patch but new kinematics: the Galilean transformation
is the  c -> infinity  limit of the Lorentz transformation (RE-03), and
Einstein's velocity-addition rule reduces to  u + v  in the same limit.

This module sits at the seam between the two worlds: it *imports* CM-03's
Galilean boost and RE-03's Lorentz machinery and shows precisely how the first is
the low-speed shadow of the second.  Units: c is explicit here (the whole point
is the size of v/c).
"""

import os
import sys
import math

# --- import CM-03 (Galilean frames) and RE-03 (Lorentz) by relative path ------
_CM03 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "CM", "CM-03_reference_frames", "code")
_RE03 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-03_lorentz_transformations", "code")
for _p in (_CM03, _RE03):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import reference_frames as galframe   # CM-03: galilean_position, galilean_velocity
import lorentz                        # RE-03: velocity_add (c = 1), boost

__all__ = [
    "C_LIGHT",
    "galilean_position", "galilean_velocity", "galilean_velocity_add",
    "relativistic_velocity_add", "galilean_limit_error",
    "galilean_invariant_acceleration", "light_speed_galilean",
    "michelson_morley_shift", "ether_wind_dt",
]

C_LIGHT = 299_792_458.0  # m/s


# --- the Galilean transformation (from CM-03) --------------------------------

def galilean_position(r, V, t):
    """Position in a frame moving at constant velocity V (CM-03): r' = r - V t.
    Time is absolute (t' = t); this is the transformation SR overturns."""
    return galframe.galilean_position(r, V, t)


def galilean_velocity(v, V):
    """Velocity in the boosted frame (CM-03): v' = v - V."""
    return galframe.galilean_velocity(v, V)


def galilean_velocity_add(u, v):
    """Galilean composition of collinear velocities: w = u + v. Unbounded -- it
    lets a signal exceed c, which is exactly where it fails for light."""
    return u + v


# --- the relativistic rule it is the limit of (from RE-03) -------------------

def relativistic_velocity_add(u, v, c=C_LIGHT):
    """Einstein velocity addition with explicit c, built from RE-03's
    dimensionless rule:  w = c * velocity_add(u/c, v/c) = (u+v)/(1 + u v/c^2).
    Reduces to galilean_velocity_add as c -> infinity."""
    return c * lorentz.velocity_add(u / c, v / c)


def galilean_limit_error(u, v, c=C_LIGHT):
    """|relativistic - Galilean| for collinear u, v. Scales like u v (u+v)/c^2,
    so it -> 0 as c -> infinity (or v << c): Galilean is the low-speed limit."""
    return abs(relativistic_velocity_add(u, v, c) - galilean_velocity_add(u, v))


# --- why Newton is happy but light is not ------------------------------------

def galilean_invariant_acceleration(a, V_boost=0.0):
    """Acceleration is unchanged by a constant-velocity (Galilean) boost: a' = a,
    because v' = v - V with V constant means dv'/dt = dv/dt. Hence F = m a takes
    the same form in every inertial frame -- Newton IS Galilean-invariant. The
    boost velocity is irrelevant; this returns a unchanged to make that explicit."""
    return a


def light_speed_galilean(v, c=C_LIGHT):
    """What Galilean addition WRONGLY predicts for a light beam met head-on while
    moving at v into the 'ether': c + v (and c - v chasing it). Experiment says
    the answer is c either way -- the contradiction that breaks Galilean relativity."""
    return c + v


# --- the Michelson-Morley experiment -----------------------------------------

def ether_wind_dt(v, L, c=C_LIGHT):
    """Exact round-trip time DIFFERENCE between an interferometer arm parallel to
    the 'ether wind' v and one perpendicular, each of length L:
        t_par  = (2L/c) / (1 - v^2/c^2),
        t_perp = (2L/c) / sqrt(1 - v^2/c^2),
        dt = t_par - t_perp  ~  (L/c)(v/c)^2   for v << c.
    The predicted, non-zero signal that the experiment did not see."""
    b2 = (v / c) ** 2
    t_par = (2.0 * L / c) / (1.0 - b2)
    t_perp = (2.0 * L / c) / math.sqrt(1.0 - b2)
    return t_par - t_perp


def michelson_morley_shift(v, L, wavelength, c=C_LIGHT):
    """Expected fringe shift when the interferometer is rotated by 90 degrees
    (swapping the two arms), to leading order:
        Delta N = (2 L / wavelength) (v/c)^2.
    For the 1887 apparatus (L ~ 11 m, lambda ~ 500 nm, v ~ 30 km/s Earth orbital)
    this is ~ 0.4 fringe -- large and clearly visible. The observed shift was
    essentially zero, refuting the ether."""
    return (2.0 * L / wavelength) * (v / c) ** 2


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-01  Galilean relativity & its failure -- demo")
    print("=" * 48)
    print("imports CM-03 (Galilean boost) and RE-03 (Lorentz)\n")

    print("velocities: Galilean u+v vs Einstein (u (+) v), as v/c grows:")
    c = C_LIGHT
    for u_frac, v_frac in ((1e-4, 1e-4), (0.1, 0.1), (0.7, 0.7), (0.9, 0.9)):
        u, v = u_frac * c, v_frac * c
        g = galilean_velocity_add(u, v)
        r = relativistic_velocity_add(u, v, c)
        print("  u=v=%4.1f%%c:  Galilean=%.4fc   Einstein=%.4fc   (Galilean %s)"
              % (u_frac * 100, g / c, r / c,
                 "ok" if abs(g - r) / c < 1e-6 else "OVERSHOOTS c" if g > c else "off"))

    print("\nGalilean = the c->infinity limit of Einstein addition:")
    for c_try in (3e8, 3e10, 3e12, 3e20):
        err = galilean_limit_error(1e7, 2e7, c_try)
        print("  c=%.0e m/s:  |relativistic - Galilean| = %.3e m/s" % (c_try, err))

    print("\nNewton is Galilean-invariant, light is not:")
    print("  acceleration in a boosted frame: a' = a  (F=ma unchanged) -> invariant")
    print("  Galilean light speed met head-on: c+v = %.0f m/s  (postulate says c) -> CONTRADICTION"
          % light_speed_galilean(30_000.0))

    print("\nMichelson-Morley (1887): L=11 m, lambda=500 nm, v=30 km/s (Earth orbit):")
    shift = michelson_morley_shift(30_000.0, 11.0, 500e-9)
    print("  predicted fringe shift on 90deg rotation: %.2f fringes" % shift)
    print("  observed: ~0  ->  no ether wind  ->  Galilean kinematics must go (RE-02, RE-03)")


if __name__ == "__main__":
    _demo()
