"""
RE-05  Minkowski spacetime  --  4-vectors, the invariant interval, light cones,
proper time, and causal structure.

Part of the physics topic network (see modules/topic_network.txt, module RE-05).
Prerequisites: RE-03 (Lorentz transformations), ~MA-16 (tensor analysis: the
metric, raising/lowering indices, the inner product).  Feeds into: ~RE-06
(4-momentum & dynamics), ~RE-08 (covariant formulation), ~RE-09/RE-11 (the curved
generalisation), ~QM-22 (relativistic QM).

THE ONE IDEA.  Special relativity is the geometry of a 4-D space with ONE minus
sign in its metric.  Every frame-independent statement is a statement about the
Minkowski inner product
        u . v  =  eta_{mu nu} u^mu v^nu  =  -u^0 v^0 + u^1 v^1 + u^2 v^2 + u^3 v^3 ,
which RE-03 showed is invariant under every Lorentz transformation.  The sign of
x . x  splits spacetime into timelike / null / spacelike, and that split -- the
**light cone** -- is the causal structure of the universe.

This module *uses MA-16* for the actual index gymnastics: the metric eta is the
input `g`, and lowering/raising/contracting are MA-16's `lower_index`,
`raise_index`, `inner`.  Minkowski space is just MA-16's machinery with the
indefinite metric eta = diag(-1,+1,+1,+1) instead of a positive-definite one.

Conventions: c = 1, event x = (ct, x, y, z), eta = diag(-1,+1,+1,+1) (mostly
plus).  Pure stdlib apart from the MA-16 import.
"""

import os
import sys
import math

# --- consume MA-16 (tensor analysis) by relative path, like CM-01 uses MA-01 ---
_MA16 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-16_tensor_analysis", "code")
if _MA16 not in sys.path:
    sys.path.insert(0, _MA16)
import tensors  # MA-16: lower_index, raise_index, inner, det_levi_civita, ...
# (future: swap for `from physkit.tensors import ...` once physkit is packaged.)

__all__ = [
    "ETA", "ETA_INV",
    "mdot", "interval2", "norm2", "classify",
    "lower", "raise_", "is_future_pointing", "causal_relation",
    "proper_time", "four_velocity", "three_velocity",
    "four_momentum", "invariant_mass",
]

# Minkowski metric (mostly plus). It is its own inverse: eta . eta = I.
ETA = [[-1.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.0, 0.0],
       [0.0, 0.0, 1.0, 0.0],
       [0.0, 0.0, 0.0, 1.0]]
ETA_INV = ETA  # eta^{mu nu} = eta_{mu nu} numerically


# --- the Minkowski inner product (delegated to MA-16) ------------------------

def mdot(u, v):
    """Minkowski inner product  u . v = eta_{mu nu} u^mu v^nu  (via MA-16.inner).
    Lorentz-invariant: equals -u^0 v^0 + u.v(spatial)."""
    return tensors.inner(ETA, u, v)


def interval2(x):
    """Squared spacetime interval  s^2 = x . x.  Mostly-plus: timelike < 0,
    null = 0, spacelike > 0."""
    return mdot(x, x)


def norm2(x):
    """Alias for interval2 (the 'squared Minkowski norm' of a 4-vector)."""
    return mdot(x, x)


def classify(x, tol=1e-12):
    """'timelike' (s^2<0), 'null'/'lightlike' (s^2=0), or 'spacelike' (s^2>0)."""
    s2 = interval2(x)
    if abs(s2) <= tol:
        return "null"
    return "timelike" if s2 < 0.0 else "spacelike"


# --- raising / lowering indices with eta (delegated to MA-16) ----------------

def lower(v_up):
    """v_mu = eta_{mu nu} v^nu  (MA-16.lower_index).  Flips the sign of v^0."""
    return tensors.lower_index(ETA, v_up)


def raise_(v_low):
    """v^mu = eta^{mu nu} v_nu  (MA-16.raise_index).  Inverse of lower()."""
    return tensors.raise_index(ETA_INV, v_low)


# --- causal structure --------------------------------------------------------

def is_future_pointing(x, tol=1e-12):
    """True if x is timelike or null AND points to the future (x^0 > 0)."""
    return interval2(x) <= tol and x[0] > 0.0


def causal_relation(a, b, tol=1e-12):
    """Causal relation of event b relative to event a:

      'future'    -- b is inside/on a's future light cone (b can be affected by a)
      'past'      -- b is inside/on a's past light cone   (b can affect a)
      'elsewhere' -- spacelike separated (no causal contact; order is frame-
                     dependent, so neither precedes the other invariantly).
    """
    d = [b[i] - a[i] for i in range(4)]
    kind = classify(d, tol)
    if kind == "spacelike":
        return "elsewhere"
    if abs(d[0]) <= tol:           # null/timelike with dt~0 only if d==0
        return "elsewhere"
    return "future" if d[0] > 0.0 else "past"


# --- proper time along a worldline -------------------------------------------

def proper_time(events):
    """Proper time elapsed along a timelike worldline sampled at `events`
    (a list of 4-vectors):  tau = sum sqrt(-interval2(segment)).

    This is arc length in the Minkowski metric.  Because of the single minus
    sign, the STRAIGHT (inertial) worldline between two timelike-separated
    events has the LONGEST proper time -- the reversed triangle inequality that
    is the twin paradox."""
    tau = 0.0
    for k in range(len(events) - 1):
        seg = [events[k + 1][i] - events[k][i] for i in range(4)]
        s2 = interval2(seg)
        if s2 > 1e-12:
            raise ValueError("segment %d is spacelike (s^2=%g); not a worldline"
                             % (k, s2))
        tau += math.sqrt(max(0.0, -s2))
    return tau


# --- standard 4-vectors ------------------------------------------------------

def four_velocity(v3):
    """4-velocity  U = dx/dtau = gamma (1, v).  Unit timelike: U . U = -1."""
    v2 = v3[0] ** 2 + v3[1] ** 2 + v3[2] ** 2
    if v2 >= 1.0:
        raise ValueError("|v| must be < 1 (got |v|^2 = %r)" % (v2,))
    g = 1.0 / math.sqrt(1.0 - v2)
    return [g, g * v3[0], g * v3[1], g * v3[2]]


def three_velocity(U):
    """Read the 3-velocity (U^1,U^2,U^3)/U^0 off a 4-velocity."""
    return [U[1] / U[0], U[2] / U[0], U[3] / U[0]]


def four_momentum(mass, v3):
    """4-momentum  p = m U = (E, p_x, p_y, p_z) with c=1.  p^0 = gamma m = E."""
    U = four_velocity(v3)
    return [mass * c for c in U]


def invariant_mass(p):
    """Rest mass from a 4-momentum:  m = sqrt(-p . p)  (the mass shell
    p . p = -m^2).  Frame-independent -- the same in every inertial frame."""
    return math.sqrt(max(0.0, -mdot(p, p)))


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-05  Minkowski spacetime -- demo   (metric via MA-16)")
    print("=" * 54)
    print("eta = diag(-1,+1,+1,+1);  c = 1;  using MA-16 tensors.inner\n")

    for name, x in (("future timelike", [3.0, 1.0, 0.0, 0.0]),
                    ("photon (null)", [1.0, 1.0, 0.0, 0.0]),
                    ("rod (spacelike)", [0.0, 2.0, 0.0, 0.0]),
                    ("past timelike", [-3.0, 1.0, 0.0, 0.0])):
        print("  %-16s s^2=% .2f  %-9s future-pointing? %s"
              % (name, interval2(x), classify(x), is_future_pointing(x)))

    print("\nlower/raise with eta (sign flip on the time component):")
    v = [2.0, 5.0, -1.0, 3.0]
    print("  v^mu =", v, " -> v_mu =", lower(v), " -> raised back =", raise_(lower(v)))

    print("\nproper time -- the twin paradox is the reversed triangle inequality:")
    A, B = [0.0, 0.0, 0.0, 0.0], [10.0, 0.0, 0.0, 0.0]
    straight = proper_time([A, B])
    bent = proper_time([A, [5.0, 4.0, 0.0, 0.0], B])
    print("  inertial A->B           : tau = %.4f" % straight)
    print("  out-and-back via x=4    : tau = %.4f  (younger -- it accelerated)" % bent)

    print("\n4-momentum lives on the mass shell  p.p = -m^2:")
    p = four_momentum(2.0, [0.6, 0.0, 0.0])
    print("  m=2, v=0.6c -> p=(E,px,0,0)=", [round(c, 4) for c in p],
          " invariant_mass=", round(invariant_mass(p), 6))


if __name__ == "__main__":
    _demo()
