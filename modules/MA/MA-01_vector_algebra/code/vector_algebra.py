"""
MA-01  Vector algebra  --  dot, cross, scalar & vector triple products.

Part of the physics topic network (see modules/topic_network.txt, module MA-01).
Cross-links: ~MA-02 (vector calculus), ~CM-01 (kinematics), ~CM-09 (angular
momentum / torque), ~CM-13 (inertia tensor), ~EM-02 (flux).

A "vector" here is any length-3 sequence of components (list, tuple, numpy
array, row of a sympy Matrix, ...). Components may be:

  * numbers (Python float / numpy)      -> ordinary numeric vector algebra
  * sympy expressions                   -> exact symbolic algebra & proofs
  * vector-valued FUNCTIONS  f(*args)   -> the operation is *lifted*: it returns
                                           a new function. e.g. with r(t), v(t)
                                           callables, cross(r, v) is the function
                                           t |-> r(t) x v(t).

Constants and functions may be mixed: dot(n_hat, E) with E(x,y,z) callable and
n_hat a constant triple returns the scalar field (x,y,z) |-> n_hat . E(x,y,z).

No third-party dependencies: the core is pure component arithmetic, so the same
functions serve numeric, symbolic and functional inputs.
"""

from functools import wraps

__all__ = [
    "lift", "dot", "cross", "scalar_triple", "triple", "vector_triple",
    "norm", "unit", "angle", "projection", "rejection",
    "are_parallel", "are_perpendicular", "are_coplanar", "box_volume",
]


def _call(x, *args, **kwargs):
    """Evaluate x at the given arguments if it is callable, else return it as-is."""
    return x(*args, **kwargs) if callable(x) else x


def lift(op):
    """Decorator: let a vector operation accept vector-valued FUNCTIONS.

    If any argument is callable, return a function that, when called, evaluates
    every argument at those same arguments and applies `op` to the results;
    otherwise apply `op` directly. This is what makes dot/cross/triple work on
    "input functions" such as a trajectory r(t). Constant operands are broadcast.
    """
    @wraps(op)
    def wrapper(*vs):
        if any(callable(v) for v in vs):
            def lifted(*args, **kwargs):
                return op(*[_call(v, *args, **kwargs) for v in vs])
            return lifted
        return op(*vs)
    return wrapper


# --- core products -----------------------------------------------------------

@lift
def dot(a, b):
    """Scalar (dot) product  a . b = a0 b0 + a1 b1 + a2 b2."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@lift
def cross(a, b):
    """Vector (cross) product  a x b  (returns a 3-tuple of components)."""
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


@lift
def scalar_triple(a, b, c):
    """Scalar triple product  a . (b x c) = det[a b c].

    The signed volume of the parallelepiped spanned by a, b, c; zero iff the
    three vectors are coplanar. Cyclic:  a.(bxc) = b.(cxa) = c.(axb).
    """
    return dot(a, cross(b, c))


triple = scalar_triple  # common alias


@lift
def vector_triple(a, b, c):
    """Vector triple product  a x (b x c) = b (a.c) - c (a.b)   (BAC-CAB rule)."""
    return cross(a, cross(b, c))


# --- magnitudes, directions, angles ------------------------------------------

@lift
def norm(a):
    """Euclidean length |a| = sqrt(a.a). For an exact symbolic length use
    sympy.sqrt(dot(a, a))."""
    return dot(a, a) ** 0.5


@lift
def unit(a):
    """Unit vector a / |a|  (returns a 3-tuple)."""
    n = dot(a, a) ** 0.5
    return (a[0] / n, a[1] / n, a[2] / n)


@lift
def angle(a, b):
    """Angle between a and b in radians, via atan2(|a x b|, a.b).

    Stable across the whole range [0, pi]; the textbook acos(a.b/|a||b|) loses
    precision near 0 and pi where arccos has an infinite slope.
    """
    import math
    return math.atan2(norm(cross(a, b)), dot(a, b))


@lift
def projection(a, b):
    """Vector projection of a onto b:  (a.b / b.b) b   (returns a 3-tuple)."""
    s = dot(a, b) / dot(b, b)
    return (s * b[0], s * b[1], s * b[2])


@lift
def rejection(a, b):
    """Component of a perpendicular to b:  a - proj_b(a)   (returns a 3-tuple)."""
    s = dot(a, b) / dot(b, b)
    return (a[0] - s * b[0], a[1] - s * b[1], a[2] - s * b[2])


# --- predicates / scalars ----------------------------------------------------

def are_parallel(a, b, tol=1e-9):
    """True if a x b ~ 0 (a and b parallel or antiparallel)."""
    x, y, z = cross(a, b)
    return (x * x + y * y + z * z) ** 0.5 <= tol


def are_perpendicular(a, b, tol=1e-9):
    """True if a . b ~ 0."""
    return abs(dot(a, b)) <= tol


def are_coplanar(a, b, c, tol=1e-9):
    """True if the scalar triple product ~ 0 (a, b, c lie in one plane)."""
    return abs(scalar_triple(a, b, c)) <= tol


def box_volume(a, b, c):
    """Volume of the parallelepiped spanned by a, b, c = |a.(b x c)|."""
    return abs(scalar_triple(a, b, c))


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("MA-01 vector algebra -- demo")
    print("=" * 32)

    a = (1.0, 2.0, 3.0)
    b = (4.0, 5.0, 6.0)
    c = (2.0, -1.0, 1.0)
    print("a =", a, " b =", b, " c =", c)
    print("a . b        =", dot(a, b))
    print("a x b        =", cross(a, b))
    print("a . (b x c)  =", scalar_triple(a, b, c), " (signed volume)")
    print("a x (b x c)  =", vector_triple(a, b, c))
    print("|a|          =", norm(a))
    print("angle(a,b)   =", math.degrees(angle(a, b)), "deg")

    print("\nfunction inputs -- a helix r(t) and its velocity v(t)=r'(t):")
    r = lambda t: (math.cos(t), math.sin(t), t)
    v = lambda t: (-math.sin(t), math.cos(t), 1.0)
    speed = norm(v)            # FUNCTION  t |-> |v(t)|
    L = cross(r, v)            # FUNCTION  t |-> r(t) x v(t)   (specific ang. momentum)
    rv = dot(r, v)             # FUNCTION  t |-> r(t) . v(t)
    for t in (0.0, math.pi / 2):
        Lt = tuple(round(x, 4) for x in L(t))
        print(f"  t={t:5.3f}:  speed={speed(t):.4f}  r.v={rv(t):+.4f}  r x v={Lt}")

    try:
        import sympy as sp
    except ImportError:
        print("\n(install sympy to also see symbolic identity proofs)")
        return
    print("\nsymbolic identity proofs (sympy):")
    A = sp.symbols('a0 a1 a2'); B = sp.symbols('b0 b1 b2'); C = sp.symbols('c0 c1 c2')
    lhs = vector_triple(A, B, C)
    rhs = tuple(B[i] * dot(A, C) - C[i] * dot(A, B) for i in range(3))
    print("  BAC-CAB   a x (b x c) = b(a.c) - c(a.b) :",
          all(sp.simplify(lhs[i] - rhs[i]) == 0 for i in range(3)))
    jac = tuple(vector_triple(A, B, C)[i] + vector_triple(B, C, A)[i]
                + vector_triple(C, A, B)[i] for i in range(3))
    print("  Jacobi    cyclic sum of a x (b x c) = 0 :",
          all(sp.simplify(jac[i]) == 0 for i in range(3)))
    lag = sp.simplify(dot(cross(A, B), cross(A, B))
                      - (dot(A, A) * dot(B, B) - dot(A, B) ** 2))
    print("  Lagrange  |a x b|^2 = |a|^2|b|^2-(a.b)^2 :", lag == 0)
    cyc = sp.simplify(scalar_triple(A, B, C) - scalar_triple(B, C, A))
    print("  cyclic    a.(bxc) = b.(cxa)             :", cyc == 0)


if __name__ == "__main__":
    _demo()
