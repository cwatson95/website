"""
CM-20  Poisson brackets & canonical transformations.

Part of the physics topic network (modules/topic_network.txt, module CM-20).
Builds on ~CM-19 (Hamiltonian); the bracket {.,.} is the classical shadow of the
quantum commutator (the {,} -> (1/i hbar)[,] bridge to ~QM-05).

For one degree of freedom (q, p) the Poisson bracket is
   {f, g} = df/dq dg/dp - df/dp dg/dq.
The fundamental bracket is {q, p} = 1; the equation of motion of any quantity is
df/dt = {f, H}; and a change of variables is **canonical** iff {Q, P} = 1. Pure stdlib.
"""

__all__ = ["poisson_bracket", "time_derivative", "is_canonical"]


def _dq(f, q, p, h):
    return (f(q + h, p) - f(q - h, p)) / (2.0 * h)


def _dp(f, q, p, h):
    return (f(q, p + h) - f(q, p - h)) / (2.0 * h)


def poisson_bracket(f, g, q, p, h=1e-6):
    """{f, g} = df/dq dg/dp - df/dp dg/dq, evaluated at (q, p). f, g are f(q, p)."""
    return _dq(f, q, p, h) * _dp(g, q, p, h) - _dp(f, q, p, h) * _dq(g, q, p, h)


def time_derivative(f, H, q, p, h=1e-6):
    """The equation of motion in bracket form:  df/dt = {f, H}  (f with no explicit t)."""
    return poisson_bracket(f, H, q, p, h)


def is_canonical(Q, P, q, p, h=1e-6, tol=1e-4):
    """A transformation (q, p) -> (Q(q,p), P(q,p)) is canonical iff {Q, P} = 1."""
    return abs(poisson_bracket(Q, P, q, p, h) - 1.0) < tol


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-20 Poisson brackets -- demo")
    print("=" * 32)
    q_, p_ = (lambda q, p: q), (lambda q, p: p)
    print("fundamental brackets at (q,p)=(1.3,0.7):")
    print(f"  {{q,p}} = {poisson_bracket(q_, p_, 1.3, 0.7):.6f}  (= 1)")
    print(f"  {{q,q}} = {poisson_bracket(q_, q_, 1.3, 0.7):.6f}  (= 0)")

    w = 2.0
    H = lambda q, p: 0.5 * p * p + 0.5 * w * w * q * q
    print("\nequation of motion df/dt = {f,H} for H = p^2/2 + 1/2 w^2 q^2 at (q,p)=(1,0.5):")
    print(f"  qdot = {{q,H}} = {time_derivative(q_, H, 1.0, 0.5):.4f}  (= p = 0.5)")
    print(f"  pdot = {{p,H}} = {time_derivative(p_, H, 1.0, 0.5):.4f}  (= -w^2 q = -4)")

    print("\ncanonical transformations (test {Q,P}=1):")
    print(f"  Q=2q, P=p/2 : {is_canonical(lambda q, p: 2 * q, lambda q, p: p / 2, 1.0, 1.0)}")
    print(f"  Q=p, P=-q   : {is_canonical(lambda q, p: p, lambda q, p: -q, 1.0, 1.0)}")
    print(f"  Q=q, P=2p   : {is_canonical(lambda q, p: q, lambda q, p: 2 * p, 1.0, 1.0)}  (not canonical)")


if __name__ == "__main__":
    _demo()
