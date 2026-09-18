"""
RE-03  Lorentz transformations  --  boosts, rapidity, relativistic velocity
addition, and the Lorentz group.

Part of the physics topic network (see modules/topic_network.txt, module RE-03).
Prerequisites: RE-02 (postulates of SR).  Feeds into: ~RE-04 (time dilation &
length contraction are read off a boost), ~RE-05 (Minkowski 4-vectors), ~RE-07
(Doppler & aberration), ~RE-08 (covariant formulation), ~CM-03 (Galilean limit).

CONVENTIONS (used consistently across the whole RE trunk)
  * Natural units  c = 1.  The time component of an event is  x^0 = c t,  so an
    event is the 4-tuple  x = (ct, x, y, z).  Restore c by  t -> c t.
  * beta = v/c  is the dimensionless velocity (|beta| < 1);  gamma = 1/sqrt(1-b^2).
  * Metric signature  eta = diag(-1, +1, +1, +1)  ("mostly plus", the GR / Zee /
    MTW convention).  The invariant interval is  s^2 = -(ct)^2 + x^2 + y^2 + z^2;
    timelike  s^2 < 0,  null  s^2 = 0,  spacelike  s^2 > 0.  (Particle-physics
    texts use the opposite sign; only the overall sign of s^2 changes.)
  * A boost Lambda acts on column 4-vectors:  x' = Lambda x.  The sign is the
    *active* boost to a frame moving at velocity +beta:  x' = gamma(x - beta ct),
    ct' = gamma(ct - beta x).

THE ONE IDEA.  A boost along a fixed axis is a *hyperbolic rotation* by the
rapidity  phi = artanh(beta)  (so gamma = cosh phi,  gamma*beta = sinh phi).
Collinear boosts therefore add by rapidity, and that single fact *is* Einstein's
velocity-addition rule:
        boost(b1) . boost(b2) = boost( (b1+b2)/(1+b1 b2) )      because
        artanh(b1) + artanh(b2) = artanh( (b1+b2)/(1+b1 b2) ).
Velocities don't add; rapidities do.  c is the unreachable rapidity-infinity.

No third-party dependencies: pure-stdlib (math only); 4-vectors are length-4
lists, Lorentz transformations are 4x4 lists of lists.
"""

import math

__all__ = [
    "C", "ETA",
    "gamma", "rapidity", "beta_from_rapidity",
    "boost", "general_boost", "identity4", "apply", "compose", "inverse",
    "dot4", "interval2", "classify",
    "velocity_add", "four_velocity", "three_velocity", "velocity_add_3d",
    "preserves_eta", "is_proper", "is_orthochronous",
]

C = 1.0  # natural units; an event is (ct, x, y, z) with this c
ETA = [[-1.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.0, 0.0],
       [0.0, 0.0, 1.0, 0.0],
       [0.0, 0.0, 0.0, 1.0]]


# --- tiny matrix helpers (kept local so the module is self-contained) ---------

def identity4():
    """The 4x4 identity (the trivial Lorentz transformation)."""
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def _matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]


def _matvec(A, x):
    return [sum(A[i][k] * x[k] for k in range(4)) for i in range(4)]


def _transpose(A):
    return [[A[j][i] for j in range(4)] for i in range(4)]


def _det(M):
    """Determinant of a square matrix by Laplace expansion (small M only)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    total = 0.0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += ((-1.0) ** j) * M[0][j] * _det(minor)
    return total


# --- the Lorentz factor and rapidity -----------------------------------------

def gamma(beta):
    """Lorentz factor  gamma = 1 / sqrt(1 - beta^2),  beta = v/c in (-1, 1)."""
    if abs(beta) >= 1.0:
        raise ValueError("beta = v/c must satisfy |beta| < 1 (got %r)" % (beta,))
    return 1.0 / math.sqrt(1.0 - beta * beta)


def rapidity(beta):
    """Rapidity  phi = artanh(beta).  Additive under collinear boosts;
    gamma = cosh phi,  gamma*beta = sinh phi."""
    return math.atanh(beta)


def beta_from_rapidity(phi):
    """Inverse of rapidity():  beta = tanh(phi).  As phi -> +-inf, beta -> +-1."""
    return math.tanh(phi)


# --- boosts -------------------------------------------------------------------

def boost(beta, axis=1):
    """4x4 Lorentz boost with velocity beta along a spatial axis.

    axis is the 4-vector spatial index: 1 = x (default), 2 = y, 3 = z.
    In the (ct, x_axis) block this is the hyperbolic rotation
        [[cosh phi, -sinh phi], [-sinh phi, cosh phi]],  phi = artanh(beta),
    i.e. [[gamma, -gamma beta], [-gamma beta, gamma]]; other axes untouched.
    """
    if axis not in (1, 2, 3):
        raise ValueError("axis must be 1, 2, or 3 (got %r)" % (axis,))
    g = gamma(beta)
    L = identity4()
    L[0][0] = g
    L[axis][axis] = g
    L[0][axis] = -g * beta
    L[axis][0] = -g * beta
    return L


def general_boost(beta_vec):
    """4x4 boost for an arbitrary velocity 3-vector beta = (bx, by, bz), |beta|<1.

        Lambda^0_0 = gamma,
        Lambda^0_i = Lambda^i_0 = -gamma b_i,
        Lambda^i_j = delta_ij + (gamma - 1) b_i b_j / |beta|^2.
    Reduces to boost(b, axis) when beta points along that axis, and to the
    identity when beta = 0.
    """
    bx, by, bz = beta_vec
    b2 = bx * bx + by * by + bz * bz
    if b2 == 0.0:
        return identity4()
    if b2 >= 1.0:
        raise ValueError("|beta| must be < 1 (got |beta|^2 = %r)" % (b2,))
    g = 1.0 / math.sqrt(1.0 - b2)
    b = [bx, by, bz]
    L = identity4()
    L[0][0] = g
    for i in range(3):
        L[0][i + 1] = -g * b[i]
        L[i + 1][0] = -g * b[i]
        for j in range(3):
            L[i + 1][j + 1] = (1.0 if i == j else 0.0) + (g - 1.0) * b[i] * b[j] / b2
    return L


def apply(L, event):
    """Transform a 4-vector / event:  x' = L x."""
    return _matvec(L, event)


def compose(*Ls):
    """Product of Lorentz transformations, applied right-to-left:
    compose(A, B) acts as A(B(x)), i.e. returns the matrix A.B."""
    out = identity4()
    for L in Ls:
        out = _matmul(out, L)
    return out


def inverse(L):
    """Inverse of a Lorentz transformation, from the defining property
    L^T eta L = eta  =>  L^{-1} = eta^{-1} L^T eta  (eta^{-1} = eta here).
    Cheaper and exact compared with a generic matrix inverse."""
    return _matmul(_matmul(ETA, _transpose(L)), ETA)


# --- the invariant interval (developed fully in RE-05) ------------------------

def dot4(a, b):
    """Minkowski inner product  a . b = eta_{mu nu} a^mu b^nu
    = -a^0 b^0 + a^1 b^1 + a^2 b^2 + a^3 b^3.  Invariant under every Lambda."""
    return -a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]


def interval2(x):
    """Squared interval  s^2 = x . x  (mostly-plus: timelike < 0, null = 0)."""
    return dot4(x, x)


def classify(x, tol=1e-12):
    """'timelike' (s^2<0), 'null' (s^2=0), or 'spacelike' (s^2>0)."""
    s2 = interval2(x)
    if abs(s2) <= tol:
        return "null"
    return "timelike" if s2 < 0.0 else "spacelike"


# --- velocity addition --------------------------------------------------------

def velocity_add(u, v):
    """Collinear relativistic velocity addition  w = (u + v) / (1 + u v)  [c=1].

    This *is* rapidity addition:  artanh(w) = artanh(u) + artanh(v).  Hence
    |u|,|v| < 1  =>  |w| < 1, and  v = 1 (light) gives w = 1 in every frame."""
    return (u + v) / (1.0 + u * v)


def four_velocity(v_vec):
    """4-velocity  U = gamma_v (1, vx, vy, vz)  of a particle with 3-velocity v
    (|v| < 1).  Satisfies U . U = -1."""
    vx, vy, vz = v_vec
    v2 = vx * vx + vy * vy + vz * vz
    g = 1.0 / math.sqrt(1.0 - v2)
    return [g, g * vx, g * vy, g * vz]


def three_velocity(U):
    """3-velocity (vx, vy, vz) = (U^1, U^2, U^3) / U^0 read off a 4-velocity."""
    return [U[1] / U[0], U[2] / U[0], U[3] / U[0]]


def velocity_add_3d(u_vec, vprime_vec):
    """General (non-collinear) velocity addition.

    Frame S' moves at 3-velocity u relative to S; an object moves at v' in S'.
    Its velocity in S is obtained by carrying the object's 4-velocity from S'
    back to S with the inverse boost  Lambda(-u):
        v = three_velocity( Lambda(-u) . U'(v') ).
    Reduces to velocity_add() when u and v' are collinear; |v| stays < 1, and a
    light ray (|v'| = 1) maps to |v| = 1.
    """
    minus_u = (-u_vec[0], -u_vec[1], -u_vec[2])
    return three_velocity(apply(general_boost(minus_u), four_velocity(vprime_vec)))


# --- predicates: which 4x4 matrices are Lorentz transformations? --------------

def preserves_eta(L, tol=1e-9):
    """True iff  L^T eta L = eta  -- the definition of a Lorentz transformation
    (it leaves the interval, hence the speed of light, invariant)."""
    M = _matmul(_matmul(_transpose(L), ETA), L)
    return all(abs(M[i][j] - ETA[i][j]) <= tol for i in range(4) for j in range(4))


def is_proper(L, tol=1e-9):
    """True iff det L = +1 (proper: no spatial reflection / no time reversal)."""
    return abs(_det(L) - 1.0) <= tol


def is_orthochronous(L):
    """True iff L^0_0 >= 1 (orthochronous: preserves the direction of time)."""
    return L[0][0] >= 1.0


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-03  Lorentz transformations -- demo")
    print("=" * 38)
    print("signature eta = diag(-1,+1,+1,+1),  c = 1,  event = (ct, x, y, z)\n")

    for b in (0.1, 0.6, 0.9, 0.99):
        print("  beta=%.2f   gamma=%7.4f   rapidity=%.4f" % (b, gamma(b), rapidity(b)))

    print("\nrapidity adds, velocity doesn't:  0.7c (+) 0.7c =")
    w = velocity_add(0.7, 0.7)
    print("    velocity_add(0.7,0.7) = %.4f c   (NOT 1.4c; rapidity %.4f+%.4f=%.4f)"
          % (w, rapidity(0.7), rapidity(0.7), rapidity(w)))
    same = compose(boost(0.7), boost(0.7))
    print("    boost(0.7).boost(0.7) == boost(%.4f) ?  %s"
          % (w, preserves_eta(same) and
             all(abs(same[i][j] - boost(w)[i][j]) < 1e-9
                 for i in range(4) for j in range(4))))

    print("\ninterval & light cone are invariant under a random-direction boost:")
    L = general_boost((0.3, -0.4, 0.5))
    for name, ev in (("timelike (clock)", [2.0, 0.5, 0.0, 0.0]),
                     ("null (photon)", [1.0, 1.0, 0.0, 0.0]),
                     ("spacelike (rod)", [0.5, 2.0, 0.0, 0.0])):
        ev2 = apply(L, ev)
        print("    %-17s s^2: % .4f -> % .4f   (%s)"
              % (name, interval2(ev), interval2(ev2), classify(ev)))

    print("\nLambda is a Lorentz transformation:  L^T eta L = eta? %s   "
          "proper? %s   orthochronous? %s"
          % (preserves_eta(L), is_proper(L), is_orthochronous(L)))
    print("Galilean limit (beta<<1):  boost(0.001) top-left 2x2 ~ [[1,-0.001],[-0.001,1]]")
    b = boost(0.001)
    print("    ", [[round(b[i][j], 6) for j in range(2)] for i in range(2)])


if __name__ == "__main__":
    _demo()
