"""
RE-08  Covariant formulation of special relativity  --  4-tensors and the index
gymnastics that make a physical law *manifestly* Lorentz-invariant.

Part of the physics topic network (see modules/topic_network.txt, module RE-08).
Prerequisites: RE-03 (Lorentz transformations), RE-05 (Minkowski spacetime),
~MA-16 (tensor analysis: the metric, raising/lowering, contraction).  Feeds into:
~EM-18 (the field tensor F^{mu nu} and covariant Maxwell), ~RE-09 (tensor calculus
on curved manifolds, where eta -> g_{mu nu}(x)).

THE ONE IDEA.  A *tensor* is something that transforms like a tensor (Zee I.4):
an object carrying a definite Lorentz transformation law.  If a tensor equation
holds in one inertial frame it holds in ALL of them -- both sides carry the same
indices and so transform identically -- so writing physics with balanced upper /
lower indices makes Lorentz invariance something you can read straight off the
page.  The laws, by rank:

    scalar       s        -> s                                  (invariant)
    contravariant V^mu    -> Lambda^mu_nu V^nu
    covariant     V_mu    -> (Lambda^{-1})^nu_mu V_nu           (inverse-transpose)
    rank-2     T^{mu nu}  -> Lambda^mu_a Lambda^nu_b T^{ab}

The metric eta = diag(-1,+1,+1,+1) lowers / raises indices (relating the contra-
and covariant versions of one vector), and a FULL contraction -- V^mu V_mu, the
trace T^mu_mu, S_{mu nu} T^{mu nu} -- ties off every index to leave a Lorentz
scalar.  The 4-gradient d_mu = d/dx^mu is naturally COVARIANT (index DOWN, so
d^0 = -d/d(x^0)), and the d'Alembertian box = d^mu d_mu = -d_t^2 + grad^2 is a
Lorentz scalar.

This module *uses MA-16* for the inner product / raising / lowering and *uses
RE-03* for the boosts Lambda -- it re-derives neither.  Conventions: c = 1,
event x = (ct, x, y, z), eta = diag(-1,+1,+1,+1) (mostly plus).  Pure stdlib
apart from those two relative-path imports.
"""

import os
import sys

# --- consume MA-16 (tensor analysis) by relative path, exactly like RE-05 -----
_MA16 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-16_tensor_analysis", "code")
if _MA16 not in sys.path:
    sys.path.insert(0, _MA16)
import tensors  # MA-16: inner, lower_index, raise_index, kronecker_delta, ...

# --- consume RE-03 (Lorentz transformations) for the boosts Lambda ------------
_RE03 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-03_lorentz_transformations", "code")
if _RE03 not in sys.path:
    sys.path.insert(0, _RE03)
import lorentz  # RE-03: boost, general_boost, inverse, apply, ...
# (future: swap both for `from physkit import tensors, lorentz` once packaged.)

__all__ = [
    "ETA", "ETA_INV", "mdot",
    "transform_vector", "transform_covector", "transform_tensor2",
    "lower", "raise_", "trace",
    "symmetric_part", "antisymmetric_part", "double_contract",
    "four_gradient", "dalembertian",
]

# Minkowski metric (mostly plus). It is its own inverse: eta . eta = I, so the
# inverse metric eta^{mu nu} is numerically the same array as eta_{mu nu}.
ETA = [[-1.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.0, 0.0],
       [0.0, 0.0, 1.0, 0.0],
       [0.0, 0.0, 0.0, 1.0]]
ETA_INV = ETA


# --- the Minkowski inner product (delegated to MA-16) ------------------------

def mdot(u, v):
    """Minkowski inner product  u . v = eta_{mu nu} u^mu v^nu  (via MA-16.inner):
    the rank-0 invariant, = -u^0 v^0 + u^1 v^1 + u^2 v^2 + u^3 v^3."""
    return tensors.inner(ETA, u, v)


# --- the Lorentz transformation laws, by tensor rank -------------------------

def transform_vector(L, V_up):
    """Contravariant law  V'^mu = Lambda^mu_nu V^nu  (ONE factor of Lambda).
    How an event, a 4-velocity or a 4-momentum transforms (== lorentz.apply)."""
    return [sum(L[mu][nu] * V_up[nu] for nu in range(4)) for mu in range(4)]


def transform_covector(L, V_low):
    """Covariant law  V'_mu = (Lambda^{-1})^nu_mu V_nu  -- the INVERSE-TRANSPOSE
    of the contravariant law, precisely so the contraction V^mu W_mu is left
    invariant.  Uses RE-03's  lorentz.inverse(L) = eta Lambda^T eta."""
    Linv = lorentz.inverse(L)
    return [sum(Linv[nu][mu] * V_low[nu] for nu in range(4)) for mu in range(4)]


def transform_tensor2(L, T):
    """Rank-2 contravariant law  T'^{mu nu} = Lambda^mu_a Lambda^nu_b T^{ab}
    (one factor of Lambda per index; Griffiths Eq. 12.115).  Returns the 4x4
    transformed array."""
    return [[sum(L[mu][a] * L[nu][b] * T[a][b]
                 for a in range(4) for b in range(4))
             for nu in range(4)] for mu in range(4)]


# --- raising / lowering with eta (delegated to MA-16) ------------------------

def lower(V_up):
    """V_mu = eta_{mu nu} V^nu  (MA-16.lower_index): the covariant partner of a
    contravariant vector.  Here it just flips the sign of the time component."""
    return tensors.lower_index(ETA, V_up)


def raise_(V_low):
    """V^mu = eta^{mu nu} V_nu  (MA-16.raise_index): the inverse of lower()."""
    return tensors.raise_index(ETA_INV, V_low)


# --- contractions that produce Lorentz scalars -------------------------------

def double_contract(S, T):
    """Full contraction of a covariant S_{mu nu} with a contravariant T^{mu nu}:
    S_{mu nu} T^{mu nu}  -- every index tied off, hence a Lorentz scalar."""
    return sum(S[mu][nu] * T[mu][nu] for mu in range(4) for nu in range(4))


def trace(T):
    """Invariant trace  T^mu_mu = eta_{mu nu} T^{mu nu} = double_contract(eta, T)
    = -T^00 + T^11 + T^22 + T^33.  Lorentz-invariant (note: NOT the naive sum of
    the diagonal -- the metric supplies the minus sign on the 00 term)."""
    return double_contract(ETA, T)


# --- symmetric / antisymmetric decomposition ---------------------------------

def symmetric_part(T):
    """T^{(mu nu)} = 1/2 (T^{mu nu} + T^{nu mu}).  Symmetry is a Lorentz-invariant
    property of a tensor (Griffiths Prob. 12.50)."""
    return [[0.5 * (T[i][j] + T[j][i]) for j in range(4)] for i in range(4)]


def antisymmetric_part(T):
    """T^{[mu nu]} = 1/2 (T^{mu nu} - T^{nu mu}).  The home of the field tensor
    F^{mu nu} (EM-18).  Always  T = symmetric_part(T) + antisymmetric_part(T)."""
    return [[0.5 * (T[i][j] - T[j][i]) for j in range(4)] for i in range(4)]


# --- the 4-gradient (naturally COVARIANT) and the d'Alembertian (a scalar) ----

def four_gradient(field, x, eps=1e-5):
    """Covariant 4-gradient  d_mu f = df / dx^mu = (d_0 f, d_1 f, d_2 f, d_3 f),
    a LOWER-index 4-vector (x^0 = ct, so d_0 = d/d(ct) and the raised d^0 = -d_0).
    Central finite difference of the scalar field  `field`: x -> f(x)."""
    g = []
    for mu in range(4):
        xp, xm = list(x), list(x)
        xp[mu] += eps
        xm[mu] -= eps
        g.append((field(xp) - field(xm)) / (2.0 * eps))
    return g


def dalembertian(field, x, eps=1e-4):
    """d'Alembertian (wave operator)  box f = d^mu d_mu f = eta^{mu nu} d_mu d_nu f
    = -d^2f/d(x^0)^2 + sum_i d^2f/d(x^i)^2  -- a Lorentz SCALAR (Griffiths
    Eq. 12.138).  Central second differences of the scalar field `field`."""
    f0 = field(x)
    total = 0.0
    for mu in range(4):
        xp, xm = list(x), list(x)
        xp[mu] += eps
        xm[mu] -= eps
        second = (field(xp) - 2.0 * f0 + field(xm)) / (eps * eps)
        total += ETA_INV[mu][mu] * second   # eta^{mu mu}: -1 on time, +1 on space
    return total


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-08  Covariant formulation of SR -- demo  (tensors via MA-16, boosts via RE-03)")
    print("=" * 80)
    print("eta = diag(-1,+1,+1,+1);  c = 1;  'a tensor is what transforms like a tensor'\n")

    L = lorentz.general_boost((0.3, -0.4, 0.5))     # a real RE-03 boost Lambda

    print("contravariant V^mu and covariant W_mu under the SAME boost -- their")
    print("contraction is invariant (the whole point of the inverse-transpose law):")
    V = [2.0, 5.0, -1.0, 3.0]
    Wlow = lower([1.0, 0.0, 2.0, -2.0])
    before = sum(V[i] * Wlow[i] for i in range(4))
    after = sum(transform_vector(L, V)[i] * transform_covector(L, Wlow)[i]
                for i in range(4))
    print("  V^mu W_mu  before = % .6f      after = % .6f\n" % (before, after))

    print("lower then raise round-trips (eta is its own inverse):")
    print("  V^mu =", V, "-> V_mu =", lower(V), "-> raised =", raise_(lower(V)), "\n")

    etap = transform_tensor2(L, ETA)
    print("eta is an INVARIANT rank-2 tensor  (Lambda^mu_a Lambda^nu_b eta^{ab} = eta):")
    print("  max|transform_tensor2(eta) - eta| = %.2e\n"
          % max(abs(etap[i][j] - ETA[i][j]) for i in range(4) for j in range(4)))

    T = [[float(4 * i + j) for j in range(4)] for i in range(4)]
    S, A = symmetric_part(T), antisymmetric_part(T)
    print("T = symmetric + antisymmetric;  S_{mu nu} A^{mu nu} = 0;  trace invariant:")
    print("  double_contract(S, A) = %.1f" % double_contract(S, A))
    print("  trace(T) = % .4f  ->  trace after boost = % .4f\n"
          % (trace(T), trace(transform_tensor2(L, T))))

    x = [1.0, 2.0, -1.0, 0.5]
    grad = four_gradient(lambda y: mdot(y, y), x)
    print("the 4-gradient is COVARIANT:  d_mu(x.x) = 2 x_mu")
    print("  d_mu(x.x) =", [round(c, 4) for c in grad],
          "   2 x_mu =", [round(2 * c, 4) for c in lower(x)], "\n")

    print("the d'Alembertian box = -d_t^2 + grad^2 is a Lorentz scalar:")
    for name, f, exact in (("box (x^0)^2", lambda y: y[0] ** 2, -2.0),
                           ("box (x^1)^2", lambda y: y[1] ** 2, 2.0),
                           ("box (x . x)", lambda y: mdot(y, y), 8.0)):
        print("  %s = % .4f   (exact % .1f)" % (name, dalembertian(f, x), exact))


if __name__ == "__main__":
    _demo()
