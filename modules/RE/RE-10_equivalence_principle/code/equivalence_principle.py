"""
RE-10  The equivalence principle  --  gravity as geometry, from "the happiest
thought" to gravitational redshift, light bending, Rindler horizons and tides.

Part of the physics topic network (see modules/topic_network.txt, module RE-10).
Prerequisites: RE-03 (boosts), RE-09 (metric & geodesics).  Feeds into: RE-11
(curvature & geodesic deviation -- the tidal field made precise), RE-14
(Schwarzschild horizons, of which the Rindler horizon here is the local seed),
QF-05 (the Unruh effect, built on the accelerated observer).

UNITS -- a DELIBERATE departure from the RE trunk's natural units.  Everywhere
else in the trunk we set c = 1; here we keep  c, g, G  EXPLICIT in SI, because
this module is about *realistic gravitational numbers* (a 22.5 m tower, a 1-g
rocket, Earth's tides) whose magnitudes are the whole point.  Stating a redshift
of 2.45e-15 or a horizon at 0.97 light-years is far clearer with the constants in
place than with everything measured in light-seconds.  So:
    c = 2.99792458e8  m/s,   g = 9.80665 m/s^2 (standard gravity),
    G = 6.674e-11 m^3 kg^-1 s^-2.
Potentials Phi are Newtonian gravitational potentials in J/kg (m^2/s^2), with the
usual sign Phi -> 0 at infinity and Phi < 0 (more negative) deeper in a well.

THE ONE IDEA (Einstein's "happiest thought", 1907).  *A freely falling observer
feels no gravity.*  Equivalently: a uniformly accelerated frame is LOCALLY
indistinguishable from a uniform gravitational field.  From this single premise --
with no field equations -- follow gravitational redshift (Delta f/f = -Delta Phi
/c^2), the slowing of clocks deep in a potential, and the bending of light.  What
free fall can NOT remove is the *tidal* field: two nearby free-fallers still drift
relative to one another (acceleration ~ d^2 Phi), and that irreducible remainder
IS spacetime curvature (developed in RE-11).  Gravity = geometry.

No third-party dependencies: pure stdlib (import math).  Every quantity is a plain
float in SI units.
"""

import math

__all__ = [
    "C", "G_NEWTON", "STD_GRAVITY",
    "grav_redshift", "redshift_uniform_field", "pound_rebka",
    "accelerated_frame_redshift", "grav_time_dilation",
    "rindler_horizon", "light_deflection_elevator",
    "tidal_acceleration", "eotvos_parameter",
]

C = 2.99792458e8       # speed of light in vacuum, m/s (exact, SI definition)
G_NEWTON = 6.674e-11   # Newtonian constant of gravitation, m^3 kg^-1 s^-2
STD_GRAVITY = 9.80665  # standard gravity g_0, m/s^2 (defined constant)


# --- gravitational redshift from the equivalence principle alone --------------

def grav_redshift(delta_phi, c=C):
    """Fractional frequency shift  Delta f / f = -Delta Phi / c^2  of a photon.

    delta_phi = Phi_receiver - Phi_emitter  (J/kg).  A photon climbing OUT of a
    potential well reaches a higher (less negative) potential, so delta_phi > 0
    and the shift is NEGATIVE -- a redshift; energy is "spent" climbing.  Falling
    in (delta_phi < 0) gives a blueshift.  This follows from the equivalence
    principle with no field equations (Zee V.2).
    """
    return -delta_phi / (c * c)


def redshift_uniform_field(g, h, c=C):
    """Redshift  Delta f / f = -g h / c^2  for a photon rising height h in a
    uniform field g.  The potential gain is Delta Phi = g h, so this is just
    grav_redshift(g*h).  Negative: rising light loses frequency."""
    return -g * h / (c * c)


def pound_rebka(h=22.5, g=STD_GRAVITY, c=C):
    """Magnitude  |Delta f / f| = g h / c^2  of the Pound-Rebka shift.

    Pound & Rebka (1959) sent 14.4 keV gamma rays up the 22.5 m Jefferson tower at
    Harvard and measured the blue/redshift via the Mossbauer effect.  The default
    h = 22.5 m, g = 9.80665 m/s^2 give |Delta f/f| ~ 2.45e-15 -- the first
    terrestrial confirmation of gravitational redshift.  Returns the magnitude.
    """
    return abs(g) * h / (c * c)


def accelerated_frame_redshift(a, h, c=C):
    """Redshift  Delta f / f = -a h / c^2  between floor and ceiling of a rocket
    accelerating at a, the ceiling a height h above the emitter.

    During the light's flight time h/c the ceiling has gained speed a h / c away
    from the emission event, Doppler-shifting the received light by -a h / c^2.
    THIS IS THE EQUIVALENCE PRINCIPLE made quantitative: it is numerically
    identical to redshift_uniform_field(a, h) -- no experiment in the sealed
    cabin can tell the acceleration a from a gravitational field g = a.
    """
    return -a * h / (c * c)


def grav_time_dilation(phi_lower, phi_upper, c=C):
    """Clock-rate ratio  dtau_lower / dtau_upper ~= 1 + (Phi_lower - Phi_upper)/c^2.

    The proper rate of an ideal clock at potential Phi is dtau/dt ~= 1 + Phi/c^2
    (weak field).  Since Phi_lower < Phi_upper deeper in a well, the ratio is < 1:
    the LOWER (deeper) clock runs SLOW relative to the higher one.  This is the
    same physics as grav_redshift -- a descending photon's crests arrive faster
    only because the receiving clock is itself ticking slow.
    """
    return 1.0 + (phi_lower - phi_upper) / (c * c)


# --- the accelerated observer: Rindler horizon --------------------------------

def rindler_horizon(a, c=C):
    """Distance  d = c^2 / a  from a uniformly accelerated observer to the horizon
    that forms BEHIND them.

    An observer with constant proper acceleration a follows a hyperbola in
    spacetime; light emitted from farther than c^2/a behind can never catch up.
    As a -> 0 the horizon recedes to infinity (an inertial observer has none);
    for a = g (Earth gravity) the horizon sits ~9.2e15 m ~ 0.97 light-years away.
    This is the LOCAL seed of the black-hole event horizon (RE-14) and of the
    Unruh temperature (QF-05).
    """
    if a == 0.0:
        return math.inf
    return c * c / a


# --- the accelerating elevator: light bends in gravity ------------------------

def light_deflection_elevator(g, L, c=C):
    """Deflection of light crossing a box of width L that accelerates at g.

    A light ray entering horizontally takes time L/c to cross; in that time the
    accelerating floor rises, so the ray appears to fall.  Returns (drop, angle):
        drop  = (1/2) g (L/c)^2   -- transverse displacement on exit (m),
        angle = g L / c^2         -- small-angle deflection (rad).
    By the equivalence principle the same must happen in a real field g: light
    bends in gravity.  CAVEAT -- this uniform-field argument captures only HALF
    the true GR deflection of starlight by the Sun (Einstein's 1911 value); the
    missing half comes from spatial curvature, which the EP alone cannot see and
    which RE-11 supplies.
    """
    drop = 0.5 * g * (L / c) ** 2
    angle = g * L / (c * c)
    return drop, angle


# --- what free fall can NOT remove: the tidal (curvature) field ---------------

def tidal_acceleration(M, r, dr, G=G_NEWTON):
    """Relative (tidal) acceleration  a_tidal = (2 G M / r^3) dr  of two test
    masses separated radially by dr at distance r from a mass M.

    The near mass is pulled harder than the far one, so they STRETCH apart along
    the radial direction; this is the gradient d/dr (G M / r^2) times dr.  Unlike
    the local field G M / r^2 -- which a freely falling frame removes entirely --
    this difference cannot be transformed away: as dr -> 0 it vanishes, but for
    any finite separation it is real.  It falls off as 1/r^3 and IS the curvature
    that free fall leaves behind (geodesic deviation, RE-11).
    """
    return (2.0 * G * M / r ** 3) * dr


# --- the weak equivalence principle: universality of free fall ----------------

def eotvos_parameter(a1, a2):
    """Eotvos ratio  eta = 2 |a1 - a2| / (a1 + a2)  for two bodies falling with
    accelerations a1, a2 in the same field.

    The weak equivalence principle (universality of free fall, m_inertial =
    m_grav) demands a1 = a2, i.e. eta = 0, for ALL compositions.  Torsion-balance
    (Eotvos; Eot-Wash) and lunar-laser-ranging experiments bound eta below about
    1e-13, and the MICROSCOPE satellite pushed it to ~1e-15.  Any eta > 0 is a
    measure of WEP violation.
    """
    return 2.0 * abs(a1 - a2) / (a1 + a2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-10  The equivalence principle -- demo")
    print("=" * 41)
    print("SI units kept explicit:  c=%.6e m/s  g=%.5f m/s^2  G=%.3e\n"
          % (C, STD_GRAVITY, G_NEWTON))

    GM_E, R_E = 3.986004418e14, 6.371e6   # Earth: GM (m^3/s^2), radius (m)

    print("1. Weak EP (universality of free fall):")
    print("   feather and hammer both fall at g -> eotvos eta = %.1f"
          % eotvos_parameter(STD_GRAVITY, STD_GRAVITY))
    a2 = STD_GRAVITY * (1.0 + 1e-13)
    print("   a hypothetical 1e-13 difference -> eta = %.2e (modern bound)"
          % eotvos_parameter(STD_GRAVITY, a2))

    print("\n2. The happiest thought: a freely falling observer feels no gravity")
    print("   (their proper acceleration is 0; weight g is locally transformed away).")

    print("\n3. Gravitational redshift WITHOUT field equations:")
    pr = pound_rebka()
    print("   Pound-Rebka (h=22.5 m): |Delta f/f| = g h/c^2 = %.3e" % pr)
    print("   equals |redshift_uniform_field(g, 22.5)| = %.3e"
          % abs(redshift_uniform_field(STD_GRAVITY, 22.5)))

    print("\n4. The equivalence, numerically:  rocket(a) == field(g=a)")
    a, h = 9.80665, 22.5
    print("   accelerated_frame_redshift(a,h) = %.3e" % accelerated_frame_redshift(a, h))
    print("   redshift_uniform_field(a,h)     = %.3e   (identical)"
          % redshift_uniform_field(a, h))

    print("\n5. Clocks run slow deep in a well (GPS must correct for this):")
    phi_surf = -GM_E / R_E
    phi_orbit = -GM_E / (R_E + 2.02e7)        # ~GPS altitude
    ratio = grav_time_dilation(phi_surf, phi_orbit)
    print("   dtau_surface/dtau_GPS = %.12f  (< 1: ground clock ticks slower)" % ratio)

    print("\n6. Light bends in gravity (accelerating elevator, L = 10 m):")
    drop, ang = light_deflection_elevator(STD_GRAVITY, 10.0)
    print("   transverse drop = %.3e m,  deflection = %.3e rad" % (drop, ang))
    print("   (uniform-field EP gives HALF the true Sun deflection; curvature -> RE-11)")

    print("\n7. The accelerated observer has a horizon (a = g):")
    d = rindler_horizon(STD_GRAVITY)
    print("   Rindler horizon c^2/g = %.3e m = %.2f light-years behind"
          % (d, d / 9.4607e15))

    print("\n8. What free fall canNOT remove -- the tidal field is real curvature:")
    dr = 1.0
    t = tidal_acceleration(GM_E / G_NEWTON, R_E, dr)
    print("   two masses 1 m apart, falling near Earth: a_tidal = %.3e m/s^2" % t)
    print("   -> 0 as dr -> 0, but != 0 for finite dr: free fall kills g, not tides.")


if __name__ == "__main__":
    _demo()
