"""Tests for SM-01 probability foundations & ensembles. Reuses MA-19.

Run:  python3 test_probability_ensembles.py     ->  "All N tests passed."
"""
import math

# own module first: chains MA-19 onto sys.path
from probability_ensembles import (
    K_B, multiplicity_two_state, multiplicity_einstein_solid,
    boltzmann_entropy, stirling_ln_factorial, stirling_factorial,
    two_state_probability, most_probable_n, fractional_width,
    gaussian_approx_two_state,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_multiplicities():
    assert multiplicity_two_state(4, 2) == 6              # C(4,2)
    assert multiplicity_two_state(10, 0) == 1             # one microstate
    assert multiplicity_two_state(10, 10) == 1
    # Einstein solid: 3 quanta in 3 oscillators = C(5,3) = 10
    assert multiplicity_einstein_solid(3, 3) == 10


def test_boltzmann_entropy_additive():
    # S = k ln Omega, and entropy of a compound system adds
    o1, o2 = 1000, 250
    assert _approx(boltzmann_entropy(o1, k=1.0), math.log(o1))
    assert _approx(boltzmann_entropy(o1 * o2, 1.0),
                   boltzmann_entropy(o1, 1.0) + boltzmann_entropy(o2, 1.0))
    # with the SI constant
    assert _approx(boltzmann_entropy(math.e, k=K_B), K_B)


def test_stirling_accuracy():
    # refined Stirling -> very accurate for ln(n!); leading term less so
    for n in (50, 200, 1000):
        exact = math.lgamma(n + 1)
        assert abs(stirling_ln_factorial(n) - exact) / exact < 1e-4
        # refined is much better than leading-only
        assert (abs(stirling_ln_factorial(n) - exact)
                < abs(stirling_ln_factorial(n, True) - exact))


def test_two_state_distribution_normalized_and_peaked():
    N = 20
    total = sum(two_state_probability(N, n) for n in range(N + 1))
    assert _approx(total, 1.0)                            # probabilities sum to 1
    # the n = N/2 macrostate is the most probable
    peak = two_state_probability(N, N // 2)
    assert peak > two_state_probability(N, N // 2 - 3)
    assert peak > two_state_probability(N, 0)
    assert most_probable_n(N) == 10.0


def test_fractional_width_scales_as_inverse_sqrt_N():
    # width(N)/width(4N) = 2  (the 1/sqrt(N) sharpening)
    assert _approx(fractional_width(100) / fractional_width(400), 2.0)
    assert _approx(fractional_width(1_000_000), 1e-3)


def test_gaussian_matches_binomial_near_peak():
    # de Moivre-Laplace: Gaussian approx ~ exact binomial near the centre
    N = 200
    for n in (90, 100, 110):
        exact = two_state_probability(N, n)
        approx = gaussian_approx_two_state(N, n)
        assert abs(exact - approx) / exact < 0.02         # within 2%


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
