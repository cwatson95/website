"""
RE-02  Postulates of special relativity  --  the two postulates, Einstein clock
synchronization, the relativity of simultaneity, the Bondi k-calculus (radar
method), and the transverse light clock that DERIVES time dilation.

Part of the physics topic network (see modules/topic_network.txt, module RE-02).
Prerequisites: RE-01 (Galilean relativity & its failure -- Michelson-Morley, the
ether).  Feeds into: RE-03 (Lorentz transformations -- the boost is the unique
linear map honouring these postulates), ~RE-04 (time dilation & length
contraction made quantitative), ~RE-07 (the Bondi k IS the relativistic Doppler
factor), ~CM-03 (the Galilean c -> infinity limit).

CONVENTIONS (used consistently across the whole RE trunk)
  * Natural units  c = 1.  An event is the 4-tuple  x = (ct, x, y, z);  the time
    component is  x^0 = c t,  so "time" and "ct" coincide.  Restore c by  t -> ct
    and  beta L -> beta L / c  in the dimensional formulas.
  * beta = v/c  is the dimensionless velocity (|beta| < 1);  gamma = 1/sqrt(1-b^2).
  * Metric signature  eta = diag(-1, +1, +1, +1)  ("mostly plus").  A boost to a
    frame moving at +beta acts as  ct' = gamma(ct - beta x),  x' = gamma(x - beta ct)
    -- the same active convention RE-03 uses.

THE ONE IDEA.  Demote *time*, not the speed of light.  Once you accept that c is
the same in every inertial frame (postulate 2), the only way to keep the
principle of relativity (postulate 1) is to give up absolute simultaneity:
clocks that are synchronized in one frame are NOT synchronized in another.  Time
dilation, length contraction and the whole Lorentz transformation are then forced
-- they are *consequences* of the postulates, not extra assumptions.  This module
shows the two cleanest derivations:
  * the transverse LIGHT CLOCK turns "c is constant" directly into  gamma  (a
    Pythagorean triangle), and
  * the RADAR / Bondi k-calculus assigns time and distance to a far-away event
    using nothing but a local clock and light echoes, with  k = sqrt((1+b)/(1-b)).

No third-party dependencies: pure-stdlib (math only); events / coordinate pairs
are returned as plain tuples.
"""

import math

__all__ = [
    "C",
    "gamma",
    "bondi_k", "beta_from_k",
    "radar_coordinates",
    "light_clock_gamma",
    "leading_clocks_lag",
    "simultaneity_breakdown",
]

C = 1.0  # natural units; an event is (ct, x, y, z) with this c


def _check_beta(beta):
    if abs(beta) >= 1.0:
        raise ValueError("beta = v/c must satisfy |beta| < 1 (got %r)" % (beta,))


# --- the Lorentz factor -------------------------------------------------------

def gamma(beta):
    """Lorentz factor  gamma = 1 / sqrt(1 - beta^2),  beta = v/c in (-1, 1).

    Not assumed here -- it is *derived* from the constancy of c by
    light_clock_gamma() below.  Used by simultaneity_breakdown()."""
    _check_beta(beta)
    return 1.0 / math.sqrt(1.0 - beta * beta)


# --- Bondi k: the Doppler / radar stretch factor ------------------------------

def bondi_k(beta):
    """Bondi k-factor  k = sqrt((1 + beta) / (1 - beta)),  beta = v/c in (-1, 1).

    If observer A flashes a light signal every proper time T, an observer B
    receding at speed beta receives the flashes every  k T  (k > 1, redshift);
    for an approaching B (beta < 0) the interval is  k T  with k < 1 (blueshift).
    k is exactly the relativistic Doppler factor (developed in ~RE-07), and it is
    its own inverse under  beta -> -beta:   k(beta) * k(-beta) = 1.
    A radar pulse that reflects off a worldline moving at beta returns stretched
    by  k^2  (one factor of k each way) -- see radar_coordinates()."""
    _check_beta(beta)
    return math.sqrt((1.0 + beta) / (1.0 - beta))


def beta_from_k(k):
    """Recover the velocity from a measured Bondi/Doppler factor:
        beta = (k^2 - 1) / (k^2 + 1).
    Inverse of bondi_k() for k > 0;  maps (0, inf) onto beta in (-1, 1)."""
    if k <= 0.0:
        raise ValueError("Bondi factor k must be > 0 (got %r)" % (k,))
    k2 = k * k
    return (k2 - 1.0) / (k2 + 1.0)


# --- the radar method: assign coordinates to a distant event ------------------

def radar_coordinates(t_send, t_echo):
    """Bondi k-calculus / radar coordinates of a distant event.

    An observer carrying a single clock sends a light pulse at clock-time
    t_send; it reflects off the event and the echo returns at clock-time t_echo.
    Because light travels out and back at the same speed c = 1, the observer
    assigns to the event
        t_event = (t_send + t_echo) / 2,      x_event = (t_echo - t_send) / 2.
    This is *Einstein synchronization* applied to a reflection: the event is
    placed at the temporal midpoint of emission and reception, a distance equal
    to half the round-trip light time.  Returns the pair (t_event, x_event)."""
    t_event = 0.5 * (t_send + t_echo)
    x_event = 0.5 * (t_echo - t_send)
    return (t_event, x_event)


# --- the transverse light clock: c -> gamma -----------------------------------

def light_clock_gamma(beta, gap=1.0):
    """DERIVE the time-dilation factor gamma from the transverse light clock.

    A light clock has two mirrors a distance D = `gap` apart, perpendicular to
    the line of motion.  In the clock's REST frame one half-tick is the light
    crossing the gap once, taking proper time  tau_0 = D  (c = 1; a full tick is
    2D).  In a frame where the clock moves at speed beta, during a half-tick of
    duration tau the far mirror slides forward to horizontal position beta*tau,
    so the light -- still travelling at c = 1, hence covering a path of length
    tau -- must run along the HYPOTENUSE of a right triangle with vertical leg D
    and horizontal leg beta*tau:

        tau^2 = D^2 + (beta*tau)^2      (equivalently  (2*tau)^2 = (2D)^2 + (beta*2tau)^2).

    Solving the quadratic  (1 - beta^2) tau^2 - D^2 = 0  for the positive root
    and forming the ratio of the moving tick to the proper tick gives

        Delta t / (2D) = tau / D = 1 / sqrt(1 - beta^2) = gamma.

    The factor is built here from the geometry (not returned as a closed form);
    the test checks it equals 1/sqrt(1-beta^2).  Independent of D, as it must be.
    """
    _check_beta(beta)
    D = float(gap)
    # quadratic  a*tau^2 + b*tau + c0 = 0  with  a = 1 - beta^2,  b = 0,  c0 = -D^2
    a = 1.0 - beta * beta
    b = 0.0
    c0 = -D * D
    disc = b * b - 4.0 * a * c0                      # = 4 (1 - beta^2) D^2 >= 0
    tau = (-b + math.sqrt(disc)) / (2.0 * a)         # positive root: moving half-tick
    proper_half = D                                  # rest-frame half-tick (light crosses D)
    return tau / proper_half                         # = Delta t / (2D) = gamma


# --- relativity of simultaneity -----------------------------------------------

def leading_clocks_lag(beta, L):
    """"Leading clocks lag."  Two clocks a rest-distance L apart along the line of
    motion, synchronized in their OWN rest frame, are seen to be out of sync in a
    frame where they move at speed beta: the front ("leading") clock reads BEHIND
    the rear ("trailing") one by

        Delta t_offset = beta * L        (= v L / c^2 with units restored).

    Returns that offset beta*L: positive means the rear clock is ahead / the
    leading clock lags.  Reverse the motion (beta -> -beta) and the roles swap
    sign.  Vanishes when beta = 0 (no motion) or L = 0 (coincident clocks) -- the
    direct fingerprint of the relativity of simultaneity, and the reason a single
    'now' cannot be shared between frames."""
    _check_beta(beta)
    return beta * L


def simultaneity_breakdown(beta, dt, dx):
    """Time gap in S' between two events separated by (dt, dx) = (Delta(ct), Delta x)
    in S, under a boost to a frame moving at +beta:

        Delta t' = gamma (Delta t - beta * Delta x).

    Two events SIMULTANEOUS in S (dt = 0, dx != 0) have
        Delta t' = -gamma * beta * dx  !=  0,
    so they are NOT simultaneous in S' unless beta = 0 or dx = 0.  This is the
    time row of the Lorentz boost (RE-03); the relativity of simultaneity is the
    statement that this expression depends on dx."""
    return gamma(beta) * (dt - beta * dx)


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-02  Postulates of special relativity -- demo")
    print("=" * 47)
    print("c = 1;  postulate 1 = principle of relativity,  postulate 2 = c is universal\n")

    print("Bondi / Doppler factor  k = sqrt((1+b)/(1-b))  (interval stretch, ~RE-07):")
    for b in (-0.6, -0.2, 0.0, 0.2, 0.6, 0.8):
        k = bondi_k(b)
        print("  beta=%+.2f   k=%6.4f   k(b)*k(-b)=%.3f   beta_from_k(k)=%+.4f"
              % (b, k, k * bondi_k(-b), beta_from_k(k)))

    print("\nRadar method (a clock + light echoes assign coordinates to an event):")
    t, x = 5.0, 3.0                       # truth: event at (t=5, x=3)
    t_send, t_echo = t - x, t + x         # emit at t-x, echo back at t+x
    t_ev, x_ev = radar_coordinates(t_send, t_echo)
    print("  send@%.1f, echo@%.1f  ->  (t,x) = (%.1f, %.1f)   [placed (%.1f, %.1f)]"
          % (t_send, t_echo, t_ev, x_ev, t, x))
    b = 0.5                               # radar off a worldline moving at beta
    t1 = 2.0
    t2 = bondi_k(b) ** 2 * t1             # echo stretched by k^2
    t_ev, x_ev = radar_coordinates(t1, t2)
    print("  reflect off beta=%.1f worldline: echo/send = k^2 = %.4f,  x/t = %.4f"
          % (b, t2 / t1, x_ev / t_ev))

    print("\nLight clock DERIVES time dilation from 'c is constant':")
    for b in (0.1, 0.6, 0.9, 0.99):
        g_geom = light_clock_gamma(b)
        g_closed = 1.0 / math.sqrt(1.0 - b * b)
        print("  beta=%.2f   gamma(geometry)=%8.4f   1/sqrt(1-b^2)=%8.4f   match=%s"
              % (b, g_geom, g_closed, abs(g_geom - g_closed) < 1e-12))
    # the triangle really closes: light path length == hypotenuse
    b, D = 0.8, 1.0
    tau = light_clock_gamma(b, D) * D
    print("  path closes? hypot(beta*tau, D)=%.6f  vs  light path tau=%.6f"
          % (math.hypot(b * tau, D), tau))

    print("\nRelativity of simultaneity:")
    b, L = 0.6, 2.0
    print("  two clocks rest-distance L=%.1f, synced in their frame, moving at beta=%.1f:"
          % (L, b))
    print("    leading clock lags by beta*L = %.3f" % leading_clocks_lag(b, L))
    print("  two events simultaneous in S (dt=0) at dx=%.1f:" % L)
    print("    dt' = %.4f  (= -gamma*beta*dx, nonzero -> not simultaneous in S')"
          % simultaneity_breakdown(b, 0.0, L))
    print("  Galilean limit beta->0:  k->1, gamma->1, offset->0  (absolute time, ~CM-03)")


if __name__ == "__main__":
    _demo()
