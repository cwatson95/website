"""
RE-04  Time dilation, length contraction & the relativity of simultaneity --
the three geometrical consequences of a single Lorentz boost.

Part of the physics topic network (see modules/topic_network.txt, module RE-04).
Prerequisites: RE-03 (Lorentz transformations -- every effect here is read off a
boost).  Feeds into: ~RE-05 (Minkowski 4-vectors & the invariant interval, where
proper time becomes the timelike "arc length"), ~RE-06 (relativistic dynamics),
~RE-07 (Doppler & aberration).

CONVENTIONS (used consistently across the whole RE trunk)
  * Natural units  c = 1.  An event is the 4-tuple  x = (ct, x, y, z); times and
    lengths share a unit, so a ratio like  distance / (beta*tau)  is dimensionless.
    Restore c by  t -> c t  (measure e.g. lengths in light-microseconds, times in
    microseconds).
  * beta = v/c  (|beta| < 1);  gamma = 1/sqrt(1 - beta^2) >= 1.
  * Metric  eta = diag(-1, +1, +1, +1)  ("mostly plus").  Frame S' moves at
    +beta x_hat relative to S; the boost S -> S' is
        ct' = gamma(ct - beta x),     x' = gamma(x - beta ct),     y'=y, z'=z.
  * "Proper" quantities are measured in the rest frame of the object: proper time
    tau (a clock sitting at one place) and rest/proper length L0 (a rod at rest).

THE ONE IDEA.  Time dilation, length contraction, and the relativity of
simultaneity are not three independent effects -- they are one Lorentz boost read
three ways.  Feed pairs of events into  ct' = gamma(ct - beta x),
x' = gamma(x - beta ct):
  * two ticks of one clock      (same x')  ->  Dt  = gamma * Dtau   time dilation
  * two ends of a rod at one t  (same ct)  ->  L   = L0 / gamma     length contraction
  * two synced clocks at one t  (same ct)  ->  lag = beta * L0      simultaneity
The gamma that *stretches* time is the same gamma that *shrinks* length; the
"beta*x" cross-term that *desynchronises* clocks is exactly what makes the
barn-pole and twin "paradoxes" evaporate.

No third-party dependencies: pure-stdlib (math only); events and 2-D diagram
directions are short lists [ct, x, ...].
"""

import math

__all__ = [
    "gamma",
    "time_dilation", "proper_time",
    "length_contraction", "rest_length",
    "leading_clocks_lag",
    "muon_fraction",
    "twin_ages",
    "pole_in_barn",
    "boosted_axes",
]


# --- the Lorentz factor (shared by every effect below) -----------------------

def gamma(beta):
    """Lorentz factor  gamma = 1 / sqrt(1 - beta^2),  beta = v/c in (-1, 1).
    gamma >= 1, with gamma = 1 only at beta = 0; gamma -> inf as |beta| -> 1."""
    if abs(beta) >= 1.0:
        raise ValueError("beta = v/c must satisfy |beta| < 1 (got %r)" % (beta,))
    return 1.0 / math.sqrt(1.0 - beta * beta)


# --- time dilation: moving clocks run slow -----------------------------------

def time_dilation(dtau, beta):
    """Dilated coordinate time  Dt = gamma * Dtau  for a clock moving at beta.

    A clock at rest ticks off proper time Dtau between two events at the *same
    place* in its own frame (same x').  Seen from a frame where the clock moves at
    beta, those two ticks are separated by the *larger* coordinate time
    gamma*Dtau: the moving clock runs slow (you wait longer for each of its ticks).
    Inverse of proper_time()."""
    return gamma(beta) * dtau


def proper_time(dt, beta):
    """Proper time  Dtau = Dt / gamma  logged by a clock that moves at beta for
    coordinate time Dt.  The moving clock reads *less* than the coordinate clocks
    it flies past (Dtau < Dt for beta != 0): it is the longest-lived twin's loss.
    Inverse of time_dilation()."""
    return dt / gamma(beta)


# --- length contraction: moving rods are shorter -----------------------------

def length_contraction(L0, beta):
    """Contracted length  L = L0 / gamma  of a rod of rest (proper) length L0,
    measured in a frame where the rod moves at beta *along its length*.

    Operationally L is got by marking both ends *simultaneously* in the measuring
    frame and subtracting; the moving rod comes out shorter than L0 by 1/gamma.
    Only the longitudinal dimension shrinks -- transverse lengths are unchanged.
    Inverse of rest_length()."""
    return L0 / gamma(beta)


def rest_length(L, beta):
    """Rest (proper) length  L0 = gamma * L  of an object whose length, measured
    while it moves at beta, is L.  Inverse of length_contraction()."""
    return gamma(beta) * L


# --- relativity of simultaneity: leading clocks lag --------------------------

def leading_clocks_lag(L0, beta):
    """Clock desynchronisation  Dt = beta * L0  from the relativity of simultaneity.

    Two clocks a rest-distance L0 apart and synchronised in their *own* frame are
    NOT synchronised in a frame where they move at beta: at any single instant of
    that frame the *leading* clock (the one in front, in the direction of motion)
    reads beta*L0 *behind* the trailing one -- "leading clocks lag."  This is the
    boost's "beta*x" cross-term, and the seed of every special-relativity
    "paradox."  (c = 1, so beta*L0 is a time.)"""
    return beta * L0


# --- muon decay: the canonical experimental confirmation ---------------------

def muon_fraction(tau0, beta, distance):
    """Surviving fraction of muons after a flight path `distance` -- relativistic
    vs naive  ->  ( exp(-distance/(gamma*beta*tau0)),  exp(-distance/(beta*tau0)) ).

    A muon of rest-frame mean life tau0 moves at beta in (0, 1) and so covers
    `distance` in lab time distance/beta (c = 1).
      * RELATIVISTIC: its internal clock is time-dilated, so its lab-frame mean
        life is gamma*tau0 -> the first (larger) fraction survives.
      * NAIVE (no time dilation): the mean life stays tau0 -> the second fraction.
    Because gamma > 1 the relativistic fraction always exceeds the naive one: far
    more muons reach the ground than Newton allows, exactly as observed
    (Rossi-Hall 1941; Griffiths Ex. 12.1)."""
    g = gamma(beta)
    relativistic = math.exp(-distance / (g * beta * tau0))
    naive = math.exp(-distance / (beta * tau0))
    return (relativistic, naive)


# --- the twin paradox --------------------------------------------------------

def twin_ages(beta, T_home):
    """Ages of the (home, travelling) twins after a round trip  ->
    ( T_home,  T_home / gamma ).

    The stay-at-home twin ages by the coordinate time T_home of the whole journey.
    The travelling twin's clock runs slow the entire way, so she ages only
    T_home/gamma and returns the *younger* of the two.  The asymmetry is genuine
    (it is NOT "each sees the other run slow") because only the traveller switches
    inertial frames at the turnaround; it vanishes only as beta -> 0.
    (Griffiths Ex. 12.2 / Prob. 12.16.)"""
    return (T_home, T_home / gamma(beta))


# --- the barn-and-ladder (pole-in-barn) paradox ------------------------------

def pole_in_barn(L0_pole, L_barn, beta):
    """The barn-and-ladder ("pole-in-barn") paradox, resolved by simultaneity.

    A pole of rest length L0_pole runs at beta through a barn of (rest) length
    L_barn with a door at each end.  Returns a dict:
      'contracted_pole'    -- L0_pole/gamma, the pole's length in the BARN frame;
      'fits_in_barn_frame' -- True iff that contracted pole fits, L0_pole/gamma <=
                              L_barn, so both doors may be shut at once with the
                              whole pole inside;
      'door_gap_barn'      -- 0.0: in the BARN frame the two door-shut events are
                              simultaneous (that IS what "it fits" means);
      'door_gap_pole'      -- gamma*beta*L_barn: in the POLE frame those *same two
                              events* are NOT simultaneous -- the far door shuts
                              (and reopens) before the near one, so the now
                              un-contracted pole is never actually enclosed.
    Both observers agree on every local event; they disagree only on which pair of
    door-shuts is "simultaneous."  "Fits" is therefore frame-dependent.
    (Griffiths Ex. 12.3.)"""
    g = gamma(beta)
    contracted = L0_pole / g
    return {
        "contracted_pole": contracted,
        "fits_in_barn_frame": contracted <= L_barn,
        "door_gap_barn": 0.0,
        "door_gap_pole": g * beta * L_barn,
    }


# --- Minkowski diagram: the scissoring of the boosted axes -------------------

def boosted_axes(beta):
    """Directions of the boosted axes (ct'-axis, x'-axis) drawn in the (ct, x)
    Minkowski diagram of frame S  ->  ( [1, beta], [beta, 1] )  in (ct, x) order.

    The ct'-axis is the worldline of the moving origin x' = 0, i.e. the line
    x = beta*ct, with direction (ct, x) = (1, beta) and slope ct/x = 1/beta.
    The x'-axis is the locus of events S' calls simultaneous (ct' = 0), i.e. the
    line ct = beta*x, with direction (beta, 1) and slope beta.  The two axes
    "scissor" *toward* the light line ct = x (slope 1) through the same angle
    arctan(beta) -- the diagram in which time dilation, length contraction, and
    the relativity of simultaneity are all visible at once.  (Zee Sec. III.4.)"""
    return ([1.0, beta], [beta, 1.0])


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-04  Time dilation, length contraction & simultaneity -- demo")
    print("=" * 62)
    print("c = 1,  event = (ct, x, y, z),  eta = diag(-1,+1,+1,+1),  S' at +beta x_hat\n")

    print("one gamma stretches time and shrinks length by the SAME factor:")
    for b in (0.1, 0.6, 0.9, 0.99):
        g = gamma(b)
        print("  beta=%.2f  gamma=%7.4f   1 s tick -> %.4f s (dilated)   1 m rod -> %.4f m (contracted)"
              % (b, g, time_dilation(1.0, b), length_contraction(1.0, b)))

    b = 0.6
    print("\none boost, three readings  (beta=%.1f, gamma=%.4f):" % (b, gamma(b)))
    dt = time_dilation(1.0, b)
    print("  time dilation:  proper Dtau=1 -> coordinate Dt = %.4f   (and back: %.4f)"
          % (dt, proper_time(dt, b)))
    L = length_contraction(1.0, b)
    print("  contraction:    rest L0=1     -> measured L  = %.4f   (and back: %.4f)"
          % (L, rest_length(L, b)))
    print("  simultaneity:   two clocks L0=1 apart -> leading one lags by %.4f"
          % leading_clocks_lag(1.0, b))

    print("\nmuon decay -- the canonical confirmation (tau0=2.2 us, ~33 light-us of air):")
    rel, naive = muon_fraction(2.2, 0.98, 33.0)
    print("  beta=0.98:  relativistic survive %.3g  vs naive %.3g  (~ %.0f x more)"
          % (rel, naive, rel / naive))

    print("\ntwin paradox (beta=0.8, home logs 30 yr):")
    home, trav = twin_ages(0.8, 30.0)
    print("  home twin ages %.1f yr,  traveller ages %.1f yr  (younger by %.1f yr)"
          % (home, trav, home - trav))

    print("\nbarn-and-ladder (pole L0=10, barn=10, beta=0.6):")
    d = pole_in_barn(10.0, 10.0, 0.6)
    print("  pole contracts to %.1f  ->  fits in barn frame? %s"
          % (d["contracted_pole"], d["fits_in_barn_frame"]))
    print("  door-shut gap:  barn frame %.1f (simultaneous)  vs  pole frame %.1f (NOT)"
          % (d["door_gap_barn"], d["door_gap_pole"]))

    print("\nMinkowski diagram -- the boosted axes scissor toward the light line ct=x:")
    ct_ax, x_ax = boosted_axes(0.6)
    print("  beta=0.6:  ct'-axis %s slope %.4f,  x'-axis %s slope %.4f,  equal tilt %.2f deg"
          % (ct_ax, ct_ax[0] / ct_ax[1], x_ax, x_ax[0] / x_ax[1],
             math.degrees(math.atan(0.6))))


if __name__ == "__main__":
    _demo()
