"""SM-01  Probability foundations & ensembles -- multiplicity, entropy, peaks.

Physics topic network, module SM-01 (modules/topic_network.txt).
Source: Pathria 3e, Ch. 1-2 (Schroeder Ch. 2, image-only).  Builds on ~MA-19
(binomial / normal distributions, sample moments).

Statistical mechanics rests on counting microstates.  A macrostate's
**multiplicity** Omega is the number of microstates realizing it; the
**fundamental postulate** (equal a priori probabilities) makes every microstate
equally likely, so the probability of a macrostate is Omega/Omega_total.  The
**Boltzmann entropy** S = k ln(Omega) (Pa Sect. 1.2) turns multiplication of
multiplicities into addition of entropies.  For large N the macrostate
distribution is fantastically sharp -- its fractional width ~ 1/sqrt(N) -- which
is why thermodynamics looks deterministic.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA19 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-19_probability_statistics", "code"))
if _MA19 not in sys.path:
    sys.path.insert(0, _MA19)

from probability import binomial_pmf, normal_pdf, sample_moments  # noqa: E402

__all__ = [
    "K_B", "multiplicity_two_state", "multiplicity_einstein_solid",
    "boltzmann_entropy", "stirling_ln_factorial", "stirling_factorial",
    "two_state_probability", "most_probable_n", "fractional_width",
    "gaussian_approx_two_state",
]

K_B = 1.380649e-23        # Boltzmann constant [J/K] (exact, SI)


# --- multiplicities (Pa Sect. 1.2) -------------------------------------------

def multiplicity_two_state(N, n):
    """Multiplicity of a two-state paramagnet / coin system: Omega(N,n) = C(N,n)
    (n of N spins up).  The number of microstates with that macrostate."""
    return math.comb(N, n)


def multiplicity_einstein_solid(N, q):
    """Multiplicity of an Einstein solid: q energy quanta shared among N
    oscillators, Omega = C(q + N - 1, q)."""
    return math.comb(q + N - 1, q)


# --- Boltzmann entropy (Pa Sect. 1.2) ----------------------------------------

def boltzmann_entropy(omega, k=K_B):
    """Boltzmann entropy  S = k ln(Omega).  With k=1 this is the entropy in nats.
    Additive: S(Omega_1 * Omega_2) = S_1 + S_2."""
    return k * math.log(omega)


# --- Stirling's approximation (Pa Sect. 1.4; Sch Ch. 2) ----------------------

def stirling_ln_factorial(n, leading_only=False):
    """ln(n!) by Stirling: n ln n - n  (leading), plus 1/2 ln(2 pi n) (refined)."""
    if n == 0:
        return 0.0
    s = n * math.log(n) - n
    if not leading_only:
        s += 0.5 * math.log(2.0 * math.pi * n)
    return s


def stirling_factorial(n, leading_only=False):
    """n! via Stirling (exp of stirling_ln_factorial)."""
    return math.exp(stirling_ln_factorial(n, leading_only))


# --- the two-state macrostate distribution (Pa Sect. 1.2) --------------------

def two_state_probability(N, n):
    """Probability of the macrostate 'n up out of N' for a fair two-state system:
        P(N,n) = C(N,n)/2^N.  Reuses MA-19 binomial_pmf with p = 1/2."""
    return binomial_pmf(n, N, 0.5)


def most_probable_n(N):
    """The most probable (and mean) number of up-spins: N/2."""
    return N / 2.0


def fractional_width(N):
    """Relative width of the macrostate peak: sigma/mean = (sqrt(N)/2)/(N/2)
    = 1/sqrt(N).  Shrinks with system size -> sharp thermodynamic limit."""
    return 1.0 / math.sqrt(N)


def gaussian_approx_two_state(N, n):
    """de Moivre-Laplace Gaussian approximation to P(N,n): a normal of mean N/2
    and variance N/4 (reuses MA-19 normal_pdf).  Excellent near the peak."""
    return normal_pdf(n, mu=N / 2.0, sigma=math.sqrt(N) / 2.0)


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-01 probability foundations & ensembles -- demo")
    print("=" * 50)

    N = 100
    print(f"two-state system, N = {N} spins:")
    print(f"  Omega(N, N/2) = C(100,50) = {multiplicity_two_state(N, N // 2):.3e}  (most microstates)")
    print(f"  Omega(N, 0)   = {multiplicity_two_state(N, 0)} (all down, a single microstate)")
    print(f"  S/k at the peak = ln Omega = {boltzmann_entropy(multiplicity_two_state(N, N//2), k=1.0):.4f} nats")

    print("\nentropy is additive (S of a combined system = sum):")
    o1, o2 = multiplicity_two_state(60, 30), multiplicity_einstein_solid(40, 25)
    s_sum = boltzmann_entropy(o1, 1.0) + boltzmann_entropy(o2, 1.0)
    s_join = boltzmann_entropy(o1 * o2, 1.0)
    print(f"  S1 + S2 = {s_sum:.5f},  S(Omega1*Omega2) = {s_join:.5f}  (equal)")

    print("\nStirling's approximation for ln(n!):")
    for n in (10, 100, 1000):
        exact = math.lgamma(n + 1)
        print(f"  n={n:>4}: exact={exact:12.4f}  Stirling={stirling_ln_factorial(n):12.4f}  "
              f"leading={stirling_ln_factorial(n, True):12.4f}")

    print("\nsharpness of the macrostate peak (fractional width 1/sqrt(N)):")
    for N in (100, 10_000, 1_000_000):
        print(f"  N={N:>9}: width = {fractional_width(N):.3e}")
    print("  -> at N ~ 1e23 the distribution is a delta function: thermodynamics.")


if __name__ == "__main__":
    _demo()
