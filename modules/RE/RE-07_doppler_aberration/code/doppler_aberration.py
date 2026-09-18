"""
RE-07  Relativistic Doppler effect & aberration  --  the Lorentz transformation
of a light ray's null 4-wavevector.

Part of the physics topic network (see modules/topic_network.txt, module RE-07).
Prerequisites: RE-03 (Lorentz transformations), RE-05 (Minkowski 4-vectors, the
null cone).  Feeds into: ~RE-06 (relativistic dynamics; the photon 4-momentum is
hbar k), ~RE-08 (covariant formulation), ~EM-18 (relativistic electrodynamics).

THE ONE IDEA.  A monochromatic light ray is carried by a single null 4-vector,
the 4-wavevector
        k^mu = (omega/c, k_vec) = (omega, omega n_hat)      [c = 1],
null because |k_vec| = omega (so k.k = -omega^2 + omega^2 = 0).  EVERYTHING about
how a light ray looks to a moving observer is just the Lorentz transformation of
this one object:
  * its TIME component omega transforms  ->  the relativistic Doppler shift,
  * its SPATIAL direction n_hat transforms  ->  aberration (the headlight effect).
Doppler and aberration are not two effects; they are the two halves of  k' = Lambda k.
(Zee derives exactly this from k = (omega, k_vec); printed 185, PDF 208.)

CONVENTIONS (whole RE trunk).  c = 1; an event is x = (ct, x, y, z); metric
eta = diag(-1, +1, +1, +1) (mostly plus); beta = v/c with |beta| < 1;
gamma = 1/sqrt(1 - beta^2).  Boosts are along +x by the *active* RE-03 boost
        ct' = gamma(ct - beta x),   x' = gamma(x - beta ct),
i.e. into a frame S' moving at velocity +beta x_hat relative to S.

ANGLE CONVENTION.  theta is the angle of the ray's *propagation direction*
n_hat = k_vec/|k_vec| measured from the boost axis (+x), in the frame in which the
ray is given.  Then:
        theta = 0    ray travels along +x   (source approaching)  -> blueshift,
        theta = pi   ray travels along -x   (source receding)     -> redshift,
        theta = pi/2 transverse                                   -> 1/gamma (pure
                                                                     time dilation).

No third-party dependencies: pure stdlib (math).  The one optional cross-trunk
import is RE-03's tested boost machinery (lorentz.boost / .apply / .dot4), used so
that transform_wavevector() literally boosts k with the same Lambda as the rest of
the relativity trunk -- making "Doppler & aberration = a Lorentz transformation"
not a slogan but the actual call.  4-wavevectors are length-4 lists [k0,k1,k2,k3].
"""

import os
import sys
import math

# --- consume RE-03 (Lorentz transformations) by relative path, like RE-05 -----
_RE03 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-03_lorentz_transformations", "code")
if _RE03 not in sys.path:
    sys.path.insert(0, _RE03)
import lorentz  # RE-03: boost, apply, dot4, gamma, ...

__all__ = [
    "gamma", "bondi_k",
    "doppler_longitudinal", "doppler_general", "doppler_transverse",
    "aberration",
    "four_wavevector", "transform_wavevector", "wavevector_frequency",
    "wavevector_angle",
    "headlight_halfangle",
]


# --- the Lorentz factor -------------------------------------------------------

def gamma(beta):
    """Lorentz factor  gamma = 1/sqrt(1 - beta^2),  beta = v/c in (-1, 1)."""
    if abs(beta) >= 1.0:
        raise ValueError("beta = v/c must satisfy |beta| < 1 (got %r)" % (beta,))
    return 1.0 / math.sqrt(1.0 - beta * beta)


def bondi_k(beta):
    """Bondi k-factor  k = sqrt((1+beta)/(1-beta))  (|beta| < 1).

    The factor by which an *approaching* source's signal period is COMPRESSED at
    the observer (frequency multiplied by k).  For a receding source replace beta
    by -beta, i.e. divide by k; hence  doppler_longitudinal(beta) = 1/bondi_k(beta).
    Composing radar echoes off a receding then re-approaching mirror multiplies the
    k-factors -- Bondi's "k-calculus" route to the Lorentz transformation.
    """
    if abs(beta) >= 1.0:
        raise ValueError("|beta| must be < 1 (got %r)" % (beta,))
    return math.sqrt((1.0 + beta) / (1.0 - beta))


# --- the relativistic Doppler shift ------------------------------------------

def doppler_longitudinal(beta):
    """Longitudinal Doppler factor  f_obs/f_src = sqrt((1-beta)/(1+beta)).

    Source and observer separating along the line of sight at speed beta > 0 =>
    factor < 1 (redshift); beta < 0 (approaching) => factor > 1 (blueshift).
    Equals  1/bondi_k(beta), and equals doppler_general(beta, pi).
    """
    if abs(beta) >= 1.0:
        raise ValueError("|beta| must be < 1 (got %r)" % (beta,))
    return math.sqrt((1.0 - beta) / (1.0 + beta))


def doppler_general(beta, theta):
    """Angular relativistic Doppler factor  f_obs/f_src = 1/(gamma(1 - beta cos theta)).

    theta is the ray's propagation angle from the boost (+x) axis measured in the
    OBSERVER's frame (see module header).  Limits:
        theta = 0    -> 1/(gamma(1-beta)) = sqrt((1+beta)/(1-beta))   (blueshift),
        theta = pi   -> 1/(gamma(1+beta)) = sqrt((1-beta)/(1+beta))   (redshift),
        theta = pi/2 -> 1/gamma                                       (transverse).
    The first two reproduce doppler_longitudinal exactly; the third is the purely
    relativistic transverse effect.  Equivalent to Zee's emitter-angle form
    omega' = gamma omega (1 + beta cos theta_emit) after aberration relates the two
    angles (Zee printed 185-186, Eq. 9).
    """
    return 1.0 / (gamma(beta) * (1.0 - beta * math.cos(theta)))


def doppler_transverse(beta):
    """Transverse Doppler factor  f_obs/f_src = 1/gamma  (theta = 90 deg).

    A uniquely relativistic redshift: the source has NO radial velocity at the
    instant of reception, yet the observed frequency drops by exactly the
    time-dilation factor 1/gamma < 1.  Equals doppler_general(beta, pi/2).
    """
    return 1.0 / gamma(beta)


# --- aberration: how the ray's direction transforms ---------------------------

def aberration(theta, beta):
    """Relativistic aberration:  cos theta' = (cos theta - beta)/(1 - beta cos theta).

    theta is the ray's propagation angle in frame S; the return value theta' is its
    angle in frame S' moving at +beta x_hat relative to S (RE-03's active boost).
    Both lie in [0, pi]; theta = 0 and theta = pi are fixed points.

    Sign of the swing.  Under this +beta boost the ray bends towards theta = pi
    (the direction the *source* appears to move in S'): aberration(theta, beta) >
    theta for 0 < theta < pi, beta > 0.  The familiar forward "headlight"/beaming
    -- a source moving in +x bunching its light towards +x in the lab -- is the
    SAME formula run the other way (rest-frame -> lab is a -beta boost), so it is
    aberration(theta, -beta) < theta; see headlight_halfangle().
    """
    c = math.cos(theta)
    cp = (c - beta) / (1.0 - beta * c)
    if cp > 1.0:                 # guard tiny floating-point overshoot
        cp = 1.0
    elif cp < -1.0:
        cp = -1.0
    return math.acos(cp)


# --- the 4-wavevector: Doppler and aberration in one object -------------------

def four_wavevector(omega, theta):
    """Null 4-wavevector of a light ray:  k^mu = (omega, omega cos theta,
    omega sin theta, 0)  [c = 1].

    Spatial part has magnitude omega (|k_vec| = omega), so k is null: k.k =
    -omega^2 + omega^2 = 0.  theta is the propagation angle from +x; omega > 0 is
    the (angular) frequency in the frame where k is written.
    """
    return [omega, omega * math.cos(theta), omega * math.sin(theta), 0.0]


def transform_wavevector(beta, k):
    """Boost a 4-wavevector along x into the frame moving at +beta:  k' = Lambda k.

    Uses RE-03's tested boost, so this is the *same* Lambda that transforms every
    other 4-vector in the trunk.  The single returned k' carries both effects:
        wavevector_frequency(k')  -> the Doppler-shifted frequency omega',
        wavevector_angle(k')      -> the aberrated direction theta'  (= aberration).
    k' stays null (a light ray is a light ray in every frame).
    """
    return lorentz.apply(lorentz.boost(beta, axis=1), k)


def wavevector_frequency(k):
    """Angular frequency omega = k^0 read off a 4-wavevector."""
    return k[0]


def wavevector_angle(k):
    """Propagation angle theta = atan2(k_y, k_x) of a 4-wavevector, in (-pi, pi].

    For a ray in the x-y plane with k_y >= 0 (theta in [0, pi]) this matches the
    aberration() convention, so it equals aberration(theta, beta) after a boost.
    """
    return math.atan2(k[2], k[1])


# --- the headlight / beaming effect ------------------------------------------

def headlight_halfangle(beta):
    """Forward-cone half-angle  theta_c = arccos(beta)  of the relativistic
    headlight effect.

    A source that radiates ISOTROPICALLY in its own rest frame, moving at speed
    beta in the lab, beams HALF of its photons (the rest-frame forward hemisphere,
    theta_rest < 90 deg) into the lab-frame forward cone theta < arccos(beta):
    the rest-frame transverse ray (90 deg) aberrates to arccos(beta) in the lab,
    so  headlight_halfangle(beta) = aberration(pi/2, -beta).
    theta_c = pi/2 at beta = 0 (isotropic) and -> 0 as beta -> 1 (a tight pencil).
    """
    if abs(beta) >= 1.0:
        raise ValueError("|beta| must be < 1 (got %r)" % (beta,))
    return math.acos(beta)


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-07  Relativistic Doppler & aberration -- demo")
    print("=" * 48)
    print("c=1, event=(ct,x,y,z), eta=diag(-1,+1,+1,+1);  light ray k^mu=(omega,k) is null.\n")

    print("Longitudinal Doppler  f_obs/f_src   (beta>0 = receding => redshift):")
    for b in (0.1, 0.5, 0.9, 0.99):
        print("  beta=%.2f   recede=%.4f   approach=%.4f   (Bondi k=%.4f)"
              % (b, doppler_longitudinal(b), 1.0 / doppler_longitudinal(b), bondi_k(b)))

    print("\nTransverse Doppler at theta=90deg is a PURE time-dilation redshift, 1/gamma:")
    for b in (0.1, 0.5, 0.9):
        print("  beta=%.2f   f_obs/f_src=%.4f = 1/gamma=%.4f" % (b, doppler_transverse(b), 1.0 / gamma(b)))

    print("\nAngular Doppler 1/(gamma(1-beta cos th)) sweeps blue->red as th:0->pi  (beta=0.6):")
    for deg in (0, 45, 90, 135, 180):
        print("  theta=%3ddeg   f_obs/f_src=%.4f" % (deg, doppler_general(0.6, math.radians(deg))))

    print("\nAberration / headlight beaming (source moving at beta=0.9): rest-frame -> lab angle")
    for deg in (0, 30, 60, 90, 120, 180):
        lab = math.degrees(aberration(math.radians(deg), -0.9))
        print("  rest %3ddeg -> lab %6.2fdeg" % (deg, lab))
    print("  forward half-cone holding half the photons:  arccos(beta) = %.2f deg"
          % math.degrees(headlight_halfangle(0.9)))

    print("\nONE Lorentz boost of k^mu encodes BOTH Doppler and aberration (beta=0.6, theta=50deg):")
    b, th = 0.6, math.radians(50.0)
    k = four_wavevector(1.0, th)
    kp = transform_wavevector(b, k)
    print("  k.k = % .2e   k'.k' = % .2e   (both null: a ray stays a ray)"
          % (lorentz.dot4(k, k), lorentz.dot4(kp, kp)))
    print("  omega/omega' = %.6f   vs  doppler_general = %.6f"
          % (wavevector_frequency(k) / wavevector_frequency(kp), doppler_general(b, th)))
    print("  emergent angle = %.6f rad   vs  aberration = %.6f rad"
          % (wavevector_angle(kp), aberration(th, b)))


if __name__ == "__main__":
    _demo()
