"""
MA-15  The Dirac delta & distributions -- delta as a limit of nascent sequences
and as a linear functional (the sifting map phi -> phi(0)): the sifting property,
the composition rule delta(g(x)) = sum delta(x-x_i)/|g'(x_i)|, the derivative
delta', the Heaviside relation H' = delta, and the Fourier representation
delta(x) = (1/2pi) integral e^{ikx} dk.

Part of the physics topic network (modules/topic_network.txt, module MA-15).
Boas keeps the delta in the ODE chapter (Ch.8 §11) next to Green functions.
Underlies ~MA-14 (the point source L G = delta), ~MA-09 (Fourier completeness),
and ~QM-02/~QM-05 (position eigenstates, <x|x'> = delta(x-x')).

Pure Python (math), dependency-free. Every distributional identity is realized as
the small-width limit of an explicit nascent sequence and verified by quadrature.
"""

import math

__all__ = [
    "gaussian_delta", "lorentzian_delta", "box_delta", "sinc_delta",
    "gaussian_delta_prime", "heaviside",
    "simpson", "sift", "delta_compose_rhs", "delta_compose_integral",
    "delta_prime_sift", "fourier_delta_kernel",
]


# --- nascent delta sequences  (each integrates to 1; -> delta as a -> 0) -----

def gaussian_delta(x, a):
    """(1/(a sqrt(pi))) exp(-(x/a)^2)."""
    return math.exp(-(x / a) ** 2) / (a * math.sqrt(math.pi))


def lorentzian_delta(x, a):
    """(1/pi) a / (x^2 + a^2)  -- the Cauchy/Lorentzian (heavy tails)."""
    return a / (math.pi * (x * x + a * a))


def box_delta(x, a):
    """1/a on |x| < a/2, else 0  -- the simplest nascent delta."""
    return 1.0 / a if abs(x) < a / 2.0 else 0.0


def sinc_delta(x, a):
    """sin(x/a)/(pi x)  -- the Dirichlet/Fourier kernel with cutoff K = 1/a."""
    if x == 0.0:
        return 1.0 / (math.pi * a)
    return math.sin(x / a) / (math.pi * x)


def gaussian_delta_prime(x, a):
    """d/dx of the Gaussian nascent delta = nascent delta'(x)."""
    return gaussian_delta(x, a) * (-2.0 * x / a ** 2)


def heaviside(x):
    """Heaviside step (1/2 at the origin); its distributional derivative is delta."""
    return 0.0 if x < 0.0 else (0.5 if x == 0.0 else 1.0)


# --- quadrature --------------------------------------------------------------

def simpson(f, a, b, N=4000):
    """Composite Simpson's rule for int_a^b f dx."""
    if N % 2:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return s * h / 3.0


# --- the defining property: sifting ------------------------------------------

def sift(phi, x0, kind, a):
    """int delta_a(x - x0) phi(x) dx  -- the sifting integral. As a -> 0 it
    returns phi(x0). `kind` in {'gaussian','lorentzian','box','sinc'}. The window
    and point count adapt to the width a so a very narrow nascent delta is still
    resolved; the box is integrated exactly across its support (no discontinuity
    inside a Simpson panel). The lorentzian/sinc converge slowly (heavy tails)."""
    if kind == "box":
        return simpson(phi, x0 - a / 2.0, x0 + a / 2.0, 2000) / a
    d = {"gaussian": gaussian_delta, "lorentzian": lorentzian_delta, "sinc": sinc_delta}[kind]
    W = {"gaussian": 8.0 * a, "lorentzian": 200.0, "sinc": 80.0}[kind]
    N = min(200000, max(4000, int(60.0 * W / a)))        # keep step well below a
    return simpson(lambda x: d(x - x0, a) * phi(x), x0 - W, x0 + W, N)


# --- composition: delta(g(x)) ------------------------------------------------

def delta_compose_rhs(phi, roots, gprime):
    """The closed form  sum_i phi(x_i)/|g'(x_i)|  for int delta(g(x)) phi(x) dx,
    summed over the simple roots x_i of g (where g'(x_i) != 0)."""
    return sum(phi(xi) / abs(gprime(xi)) for xi in roots)


def delta_compose_integral(phi, g, a, lo, hi, N=20000):
    """int delta_a(g(x)) phi(x) dx with the Gaussian nascent -- should approach
    delta_compose_rhs as a -> 0. This is the numerical witness for
    delta(g(x)) = sum_i delta(x - x_i)/|g'(x_i)|."""
    return simpson(lambda x: gaussian_delta(g(x), a) * phi(x), lo, hi, N)


# --- the derivative delta' ---------------------------------------------------

def delta_prime_sift(phi, a, half_width=6.0, N=4000):
    """int delta_a'(x) phi(x) dx  -- approaches  -phi'(0)  (integration by parts:
    <delta', phi> = -<delta, phi'> = -phi'(0))."""
    return simpson(lambda x: gaussian_delta_prime(x, a) * phi(x), -half_width, half_width, N)


# --- Fourier representation ---------------------------------------------------

def fourier_delta_kernel(x, K):
    """(1/2pi) int_{-K}^{K} e^{ikx} dk = sin(Kx)/(pi x).  As K -> inf this is a
    nascent delta (the Fourier/Dirichlet kernel) -- the basis of ~MA-09 completeness."""
    if x == 0.0:
        return K / math.pi
    return math.sin(K * x) / (math.pi * x)


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-15 Dirac delta & distributions -- demo")
    print("=" * 42)

    # bounded phi so the heavy-tailed lorentzian sifts cleanly too (a growing phi
    # is not integrable against its 1/x^2 tail -- the lorentzian has no 2nd moment)
    phi = lambda x: math.cos(x) + 0.3 * math.sin(2 * x)
    print("\nsifting  int delta_a(x - 1.2) phi(x) dx -> phi(1.2) =", round(phi(1.2), 6))
    for kind in ("gaussian", "box", "lorentzian"):
        for a in (0.2, 0.05, 0.01):
            print(f"  {kind:10s} a={a:<5}: {sift(phi, 1.2, kind, a):.6f}")

    print("\nnormalization  int delta_a dx (expect 1):")
    print(f"  gaussian  : {sift(lambda x: 1.0, 0.0, 'gaussian', 0.05):.6f}")
    print(f"  box       : {sift(lambda x: 1.0, 0.0, 'box', 0.05):.6f}")
    print(f"  lorentzian: {sift(lambda x: 1.0, 0.0, 'lorentzian', 0.1):.6f}")

    print("\ncomposition  delta(x^2 - c^2), c=1.5:  sum phi(x_i)/|g'(x_i)| with g'=2x")
    c = 1.5
    g = lambda x: x * x - c * c
    gp = lambda x: 2 * x
    rhs = delta_compose_rhs(phi, [c, -c], gp)
    print(f"  closed form = [phi(c)+phi(-c)]/(2c) = {rhs:.6f}")
    for a in (0.05, 0.01, 0.004):
        print(f"  integral a={a:<5}: {delta_compose_integral(phi, g, a, -4.0, 4.0):.6f}")

    print("\nderivative  int delta_a'(x) phi(x) dx -> -phi'(0)  (phi'=-sin x+0.6cos2x; -phi'(0)=-0.6)")
    for a in (0.2, 0.05, 0.02):
        print(f"  a={a:<5}: {delta_prime_sift(phi, a):.6f}")
    psi = lambda x: math.exp(-x)                       # psi'(0) = -1 -> answer +1
    print("  for psi=e^{-x},  -psi'(0)=+1:")
    for a in (0.1, 0.03):
        print(f"    a={a:<5}: {delta_prime_sift(psi, a):.6f}")

    # the sinc kernel must act on a DECAYING test function (it is not integrable
    # against the growing 0.5 x^2 above): use psi = e^{-x^2} cos x, psi(0)=1.
    print("\nFourier kernel  sin(Kx)/(pi x) -> delta:  int kernel*psi, psi=e^{-x^2}cos x")
    psi = lambda x: math.exp(-x * x) * math.cos(x)
    for K in (20.0, 60.0, 150.0):
        val = simpson(lambda x: fourier_delta_kernel(x, K) * psi(x), -15.0, 15.0, 30000)
        print(f"  K={K:<6}: {val:.6f}   (-> psi(0) = {psi(0.0):.6f})")


if __name__ == "__main__":
    _demo()
