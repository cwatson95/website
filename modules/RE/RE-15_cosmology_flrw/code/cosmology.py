"""
RE-15  Cosmology: the FLRW universe  --  the cosmological principle, the scale
factor a(t), cosmological redshift, and the Friedmann equations that govern the
whole expanding universe.

Part of the physics topic network (see modules/topic_network.txt, module RE-15).
Prerequisites: RE-11 (curvature -- the Einstein tensor, which this module IMPORTS)
and RE-13 (the Einstein field equations).  Feeds into observational cosmology
(distances, the CMB, structure growth).

THE ONE IDEA.  Assume the universe is the same everywhere (homogeneous) and the
same in every direction (isotropic) -- the **cosmological principle**.  That single
symmetry demand collapses the ten functions of four variables in a general metric
down to ONE function of ONE variable, the scale factor a(t):
        ds^2 = -dt^2 + a(t)^2 [ dr^2/(1 - k r^2) + r^2 dOmega^2 ],
with k = +1, 0, -1 the curvature of the homogeneous 3-space (the constant-curvature
slices of RE-11 sec.6: 3-sphere / flat / hyperbolic).  Feed this metric into the
Einstein equations G_{mu nu} = 8 pi T_{mu nu} (RE-11/RE-13) and the entire content
reduces to two ordinary differential equations for a(t), the **Friedmann equations**
        (a'/a)^2 = (8 pi/3) rho - k/a^2 + Lambda/3        (energy / G_{00})
         a''/a   = -(4 pi/3)(rho + 3 p) + Lambda/3        (acceleration / G_{ij}).
The universe is described by one equation -- Einstein's audacious idea, made literal.

This module *uses RE-11* (`curvature.einstein_tensor`) to DEMONSTRATE the first
Friedmann equation directly: `G00_from_flrw` builds the FLRW metric, hands it to the
finite-difference curvature machine, and recovers G_{00} = 3[(a'/a)^2 + k/a^2] -- so
the Friedmann equation is not asserted but *computed* from the metric.  Everything
else (the two residuals, the fluid equation, critical density / Omega, redshift) is
closed-form.  Geometrized units G = c = 1; mostly-plus signature (-,+,+,+).
"""

import os
import sys
import math

# --- consume RE-11 (curvature) by relative path (cf. RE-11 -> MA-17) ----------
_RE11 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-11_curvature", "code")
if _RE11 not in sys.path:
    sys.path.insert(0, _RE11)
import curvature  # RE-11: einstein_tensor (-> MA-17 finite-difference curvature)

__all__ = [
    "flrw_metric", "hubble", "redshift",
    "friedmann_1_residual", "friedmann_2_residual", "fluid_equation_residual",
    "critical_density", "omega",
    "G00_from_flrw",
    "de_sitter_scale_factor", "power_law_scale_factor",
    "era_density",
]

_FOUR_PI = 4.0 * math.pi
_EIGHT_PI = 8.0 * math.pi


# --- the FLRW metric ----------------------------------------------------------

def flrw_metric(a_func, k):
    """The Friedmann-Lemaitre-Robertson-Walker metric as a callable x -> g(x),
    in comoving coordinates x = (t, r, theta, phi) and mostly-plus signature:

        ds^2 = -dt^2 + a(t)^2 [ dr^2/(1 - k r^2) + r^2 (dtheta^2 + sin^2 theta dphi^2) ].

    `a_func` is the scale factor t -> a(t); `k` is the spatial curvature constant
    (+1 closed / 0 flat / -1 open).  The spatial part is exactly the round S^3 /
    flat / H^3 constant-curvature 3-metric of RE-11 sec.6.  Feed the returned metric
    to `curvature.einstein_tensor` (see `G00_from_flrw`) to get the Friedmann eqs."""
    def g(x):
        t, r, th, ph = x
        a = a_func(t)
        a2 = a * a
        grr = a2 / (1.0 - k * r * r)
        gthth = a2 * r * r
        gphph = a2 * r * r * math.sin(th) ** 2
        return [[-1.0, 0.0, 0.0, 0.0],
                [0.0, grr, 0.0, 0.0],
                [0.0, 0.0, gthth, 0.0],
                [0.0, 0.0, 0.0, gphph]]
    return g


# --- kinematics: Hubble rate and redshift ------------------------------------

def hubble(a, adot):
    """The Hubble rate H = a'/a -- the fractional expansion rate of the universe.
    H_0 (its value today) sets the size and age scales of the cosmos."""
    return adot / a


def redshift(a_emit, a_obs=1.0):
    """Cosmological redshift  1 + z = a_obs / a_emit, hence z = a_obs/a_emit - 1.
    Light emitted when the universe was smaller (a_emit < a_obs) arrives stretched
    to longer wavelength: the expansion of space itself, not a Doppler shift.
    With the convention a_0 = 1 today, a_emit = 1/(1+z)."""
    return a_obs / a_emit - 1.0


# --- the Friedmann equations (residual form) ---------------------------------

def friedmann_1_residual(a, adot, rho, k, Lambda=0.0):
    """Residual of the FIRST Friedmann equation (the G_{00} / energy constraint):
        (a'/a)^2 = (8 pi/3) rho - k/a^2 + Lambda/3,
    returned as LHS - RHS = (a'/a)^2 - (8 pi/3) rho + k/a^2 - Lambda/3.
    Zero exactly when a(t), rho satisfy the energy equation.  This is `G00_from_flrw`
    divided by 3 minus (8 pi/3) rho - Lambda/3: curvature really does give it."""
    H = adot / a
    return H * H - (_EIGHT_PI / 3.0) * rho + k / (a * a) - Lambda / 3.0


def friedmann_2_residual(a, addot, rho, p, Lambda=0.0):
    """Residual of the SECOND Friedmann (acceleration) equation:
        a''/a = -(4 pi/3)(rho + 3 p) + Lambda/3,
    returned as a''/a + (4 pi/3)(rho + 3 p) - Lambda/3.  Gravity decelerates the
    expansion unless rho + 3 p < 0: pressure gravitates, and only a sufficiently
    negative pressure (dark energy, Lambda) can drive acceleration (a'' > 0)."""
    return addot / a + (_FOUR_PI / 3.0) * (rho + 3.0 * p) - Lambda / 3.0


def fluid_equation_residual(rho, rhodot, a, adot, p):
    """Residual of the fluid (continuity) equation  rho' = -3 (a'/a)(rho + p),
    returned as rho' + 3 (a'/a)(rho + p).  This is exactly nabla_mu T^{mu nu} = 0
    (local energy conservation) in an FLRW background, and it is NOT independent:
    it follows from the two Friedmann equations via the contracted Bianchi identity
    (RE-11 sec.3).  Solving it gives rho ~ a^{-3(1+w)} for a fluid with p = w rho:
    matter (w=0) ~ a^{-3}, radiation (w=1/3) ~ a^{-4}, Lambda (w=-1) ~ const."""
    return rhodot + 3.0 * (adot / a) * (rho + p)


# --- critical density and the density parameter ------------------------------

def critical_density(H):
    """Critical density  rho_c = 3 H^2 / (8 pi): the energy density of a spatially
    FLAT (k = 0, Lambda = 0) universe expanding at Hubble rate H.  It is the
    knife-edge that separates eternal expansion from eventual recollapse."""
    return 3.0 * H * H / _EIGHT_PI


def omega(rho, H):
    """Density parameter  Omega = rho / rho_c = 8 pi rho / (3 H^2).  The flat/open/
    closed trichotomy of the homogeneous 3-space is read off Omega_total directly:
    Omega = 1 <=> rho = rho_c <=> k = 0 (flat); Omega > 1 <=> k = +1 (closed);
    Omega < 1 <=> k = -1 (open).  (With Lambda included, use the total Omega.)"""
    return rho / critical_density(H)


# --- reference scale factors and exact era densities --------------------------

def de_sitter_scale_factor(H):
    """Exponential (de Sitter) expansion  a(t) = e^{H t}: the late-time, dark-
    energy / cosmological-constant dominated universe (constant H, a'' > 0)."""
    return lambda t: math.exp(H * t)


def power_law_scale_factor(power):
    """Power-law expansion  a(t) = t^p.  The decelerating single-fluid eras of a
    flat universe: matter p = 2/3 (a ~ t^{2/3}), radiation p = 1/2 (a ~ t^{1/2})."""
    return lambda t: t ** power


def era_density(a, w):
    """Energy density at scale factor `a` for a fluid with equation of state
    p = w rho, normalised to rho = 1 at a = 1:  rho(a) = a^{-3(1+w)}.
    Matter w = 0 -> a^{-3}; radiation w = 1/3 -> a^{-4}; Lambda w = -1 -> const."""
    return a ** (-3.0 * (1.0 + w))


# --- FLRW  =>  Friedmann, computed from the Einstein tensor (uses RE-11) -------

def G00_from_flrw(a_func, k, t, eps=1e-3):
    """Build the FLRW metric for `a_func`, `k` and hand it to RE-11's
    `curvature.einstein_tensor` (finite-difference curvature) at the representative
    event x = (t, 0.1, 1.0, 1.0); return the time-time component G_{00}.

    For FLRW this is the LEFT side of the first Friedmann equation:
        G_{00} = 3 [ (a'/a)^2 + k/a^2 ] = 3 (a'^2 + k) / a^2,
    so G_{00} = 8 pi T_{00} = 8 pi rho reproduces (a'/a)^2 = 8 pi rho/3 - k/a^2.
    `eps` is the outer finite-difference step (loose-tolerance numerical curvature).
    This is the headline: the Friedmann equation is COMPUTED from the metric, not
    assumed."""
    g = flrw_metric(a_func, k)
    G = curvature.einstein_tensor(g, [t, 0.1, 1.0, 1.0], eps_out=eps)
    return G[0][0]


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-15  Cosmology: the FLRW universe -- demo")
    print("=" * 56)

    print("\nFLRW => Friedmann:  G_00 from the metric (RE-11 curvature)")
    print("  vs the exact 3[(a'/a)^2 + k/a^2]:")
    # de Sitter, flat: G_00 should be the constant 3 H^2
    for H in (0.5, 1.0):
        a = de_sitter_scale_factor(H)
        g00 = G00_from_flrw(a, 0, 0.7)
        print("  de Sitter H=%.1f, k=0:  G_00=%.5f   3H^2=%.5f" % (H, g00, 3 * H * H))
    # matter, flat: G_00 = 3 (a'/a)^2 = 3 (2/3t)^2
    am = power_law_scale_factor(2.0 / 3.0)
    for t in (1.0, 2.0):
        adot = (2.0 / 3.0) * t ** (-1.0 / 3.0)
        aval = t ** (2.0 / 3.0)
        print("  matter a=t^2/3, k=0, t=%.1f:  G_00=%.5f   3(a'/a)^2=%.5f"
              % (t, G00_from_flrw(am, 0, t), 3.0 * (adot / aval) ** 2))
    # curved matter: the k/a^2 term shows up with the right sign
    for k in (1, -1):
        t = 2.0
        adot = (2.0 / 3.0) * t ** (-1.0 / 3.0); aval = t ** (2.0 / 3.0)
        exact = 3.0 * ((adot / aval) ** 2 + k / (aval * aval))
        print("  matter, k=%+d, t=2.0:  G_00=%.5f   3((a'/a)^2+k/a^2)=%.5f"
              % (k, G00_from_flrw(am, k, t), exact))

    print("\nThe three eras satisfy BOTH Friedmann residuals (~0):")
    # matter: a=t^2/3, p=0, rho = 3H^2/8pi ~ a^-3
    for name, power, w in (("matter   ", 2.0 / 3.0, 0.0),
                           ("radiation", 1.0 / 2.0, 1.0 / 3.0)):
        t = 1.3
        aval = t ** power
        adot = power * t ** (power - 1.0)
        addot = power * (power - 1.0) * t ** (power - 2.0)
        H = adot / aval
        rho = critical_density(H)               # on-shell flat density
        p = w * rho
        r1 = friedmann_1_residual(aval, adot, rho, 0)
        r2 = friedmann_2_residual(aval, addot, rho, p)
        rd = -3.0 * H * (rho + p)               # rho' from the fluid law
        rf = fluid_equation_residual(rho, rd, aval, adot, p)
        print("  %s w=%+.3f:  F1=%+.2e  F2=%+.2e  fluid=%+.2e"
              % (name, w, r1, r2, rf))
    # de Sitter: rho = Lambda/8pi = const, p = -rho
    H = 0.8
    Lam = 3.0 * H * H
    rho = Lam / _EIGHT_PI                        # = 3H^2/8pi
    aval, adot, addot = math.exp(H), H * math.exp(H), H * H * math.exp(H)
    r1 = friedmann_1_residual(aval, adot, rho, 0)
    r2 = friedmann_2_residual(aval, addot, rho, -rho)
    print("  de Sitter w=-1.000:  F1=%+.2e  F2=%+.2e  (rho=Lambda/8pi const)"
          % (r1, r2))

    print("\nCritical density and the Omega trichotomy (k from Omega_total):")
    H = 1.0
    rc = critical_density(H)
    print("  H=1: rho_c = 3H^2/8pi = %.6f,  Omega(rho_c)=%.4f (flat, k=0)"
          % (rc, omega(rc, H)))
    print("  rho=1.3 rho_c: Omega=%.3f (>1 -> closed),  0.7 rho_c: Omega=%.3f (<1 -> open)"
          % (omega(1.3 * rc, H), omega(0.7 * rc, H)))

    print("\nCosmological redshift  1+z = a_0/a_emit:")
    for ae in (0.5, 0.25, 0.1):
        print("  a_emit=%.2f -> z=%.3f" % (ae, redshift(ae)))


if __name__ == "__main__":
    _demo()
