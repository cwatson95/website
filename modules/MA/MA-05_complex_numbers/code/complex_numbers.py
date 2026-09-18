"""
MA-05  Complex numbers -- polar form, Euler's formula, De Moivre, roots, and
the principal branch of sqrt/log.

Part of the physics topic network (modules/topic_network.txt, module MA-05).
Root module; feeds ~MA-06 (complex analysis), ~EM-12/~CM-15 (AC circuits &
oscillations via e^{iwt}), ~QM-02 (complex wavefunctions), and complex
eigenvalues from ~MA-04.

Python already has `complex` and `cmath`; this module exposes the *mechanics*
(modulus/argument, r e^{i theta}, De Moivre, nth roots, the principal branch)
explicitly, the way you would derive them by hand. Pure stdlib.
"""

import math

__all__ = [
    "modulus", "argument", "to_polar", "from_polar", "conjugate",
    "euler", "de_moivre", "power", "nth_roots", "roots_of_unity",
    "principal_sqrt", "principal_log",
]


def modulus(z):
    """|z| = sqrt(x^2 + y^2)."""
    return math.hypot(z.real, z.imag)


def argument(z):
    """Principal argument arg(z) in (-pi, pi]  (the angle from the +real axis)."""
    return math.atan2(z.imag, z.real)


def to_polar(z):
    """z -> (r, theta) with r = |z|, theta = arg(z)."""
    return (modulus(z), argument(z))


def from_polar(r, theta):
    """(r, theta) -> r(cos theta + i sin theta) = r e^{i theta}."""
    return complex(r * math.cos(theta), r * math.sin(theta))


def conjugate(z):
    """Complex conjugate x - iy."""
    return complex(z.real, -z.imag)


def euler(theta):
    """Euler's formula: e^{i theta} = cos theta + i sin theta  (a point on the unit circle)."""
    return complex(math.cos(theta), math.sin(theta))


def de_moivre(theta, n):
    """De Moivre: (cos theta + i sin theta)^n = cos(n theta) + i sin(n theta)."""
    return complex(math.cos(n * theta), math.sin(n * theta))


def power(z, n):
    """z^n via polar form: r^n e^{i n theta}  (n may be any real exponent)."""
    r, theta = to_polar(z)
    return from_polar(r ** n, n * theta)


def nth_roots(z, n):
    """All n distinct n-th roots of z:  r^{1/n} e^{i(theta + 2 pi k)/n}, k=0..n-1.
    They sit on a circle of radius |z|^{1/n}, equally spaced by 2 pi / n."""
    r, theta = to_polar(z)
    rn = r ** (1.0 / n)
    return [from_polar(rn, (theta + 2.0 * math.pi * k) / n) for k in range(n)]


def roots_of_unity(n):
    """The n n-th roots of 1:  e^{2 pi i k / n}, k = 0..n-1  (they sum to 0 for n>=2)."""
    return nth_roots(complex(1.0, 0.0), n)


def principal_sqrt(z):
    """Principal square root: sqrt(r) e^{i theta/2} with theta = principal arg.
    Branch cut on the negative real axis (arg jumps by 2 pi across it)."""
    r, theta = to_polar(z)
    return from_polar(math.sqrt(r), theta / 2.0)


def principal_log(z):
    """Principal logarithm: Log z = ln|z| + i arg(z),  arg in (-pi, pi].
    (Boas: the "principal value"; same branch cut on the negative real axis.)"""
    if z == 0:
        raise ValueError("log(0) is undefined")
    return complex(math.log(modulus(z)), argument(z))


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-05 complex numbers -- demo")
    print("=" * 32)

    z = complex(1.0, 1.0)
    r, th = to_polar(z)
    print(f"z = 1+i  ->  r={r:.4f}, theta={math.degrees(th):.1f} deg;  back = {from_polar(r, th):.4f}")

    print("\nEuler's formula:")
    print("  e^{i pi}   =", complex(round(euler(math.pi).real, 6), round(euler(math.pi).imag, 6)), "(= -1)")
    print("  e^{i pi/2} =", complex(round(euler(math.pi / 2).real, 6), round(euler(math.pi / 2).imag, 6)), "(=  i)")

    print("\nDe Moivre vs direct power, z=1+i, n=8:")
    print("  power(z,8)            =", power(z, 8))
    print("  (1+i)^8 (python)      =", z ** 8, " (= 16)")

    print("\ncube roots of unity:")
    for w in roots_of_unity(3):
        print(f"    {w:+.4f}")
    s = sum(roots_of_unity(3))
    print("  sum of cube roots of unity =", complex(round(s.real, 6), round(s.imag, 6)), "(= 0)")

    print("\nprincipal branch on the negative real axis:")
    print("  sqrt(-1)       =", principal_sqrt(complex(-1.0, 0.0)), "(=  i)")
    print("  Log(-1)        =", principal_log(complex(-1.0, 0.0)), "(= i*pi)")
    print("  sqrt(-1-eps i) =", principal_sqrt(complex(-1.0, -1e-9)), "(~ -i  -> the jump across the cut)")


if __name__ == "__main__":
    _demo()
