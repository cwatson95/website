"""Tests for ST-02 counting techniques.

Asserts the headline combinatorial identities -- factorial recurrence, the
permutation/combination link P = C*k!, Pascal's rule, the binomial &
multinomial theorems, stars & bars, Vandermonde, and the continuous
Beta/Gamma cross-checks of the discrete coefficients.

Run:  python3 test_counting.py     ->  "All N tests passed."
"""
import math

from counting import (
    factorial, multiplication_principle, ordered_with_replacement,
    permutations, combinations, permutations_with_repetition, multinomial,
    stars_and_bars, combinations_with_replacement, pascal_row,
    pascal_rule_holds, binomial_theorem_check, binomial_coefficient_sum,
    beta_integral, _integrate,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _compositions(n, m):
    """All m-tuples of non-negative ints summing to n (for the multinomial theorem)."""
    if m == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in _compositions(n - first, m - 1):
            yield (first,) + rest


# 1 -------------------------------------------------------------------------
def test_factorial_matches_stdlib_and_recurrence():
    for n in range(0, 12):
        assert factorial(n) == math.factorial(n)
    assert factorial(0) == 1                      # empty product
    for n in range(1, 12):
        assert factorial(n) == n * factorial(n - 1)   # n! = n*(n-1)!


# 2 -------------------------------------------------------------------------
def test_permutations_formula_and_stdlib():
    for n in range(0, 10):
        for k in range(0, n + 1):
            assert permutations(n, k) == math.perm(n, k)
            assert permutations(n, k) == factorial(n) // factorial(n - k)
    assert permutations(7, 0) == 1               # one empty arrangement
    assert permutations(7, 7) == factorial(7)    # full arrangement = n!


# 3 -------------------------------------------------------------------------
def test_combinations_match_stdlib_symmetry_boundaries():
    for n in range(0, 11):
        for k in range(0, n + 1):
            assert combinations(n, k) == math.comb(n, k)
            assert combinations(n, k) == combinations(n, n - k)   # symmetry
        assert combinations(n, 0) == 1 and combinations(n, n) == 1
    assert combinations(5, 6) == 0 and combinations(5, -1) == 0   # out of range


# 4 -------------------------------------------------------------------------
def test_permutation_combination_link():
    # P(n,k) = C(n,k) * k!  -- ordering multiplies by k!
    for n in range(0, 10):
        for k in range(0, n + 1):
            assert permutations(n, k) == combinations(n, k) * factorial(k)


# 5 -------------------------------------------------------------------------
def test_pascal_rule_and_row_properties():
    for n in range(1, 15):
        for k in range(0, n + 1):
            assert pascal_rule_holds(n, k)                        # C(n,k)=C(n-1,k-1)+C(n-1,k)
        row = pascal_row(n)
        assert row == row[::-1]                                   # symmetric
        assert sum(row) == 2 ** n                                 # row sum = 2^n


# 6 -------------------------------------------------------------------------
def test_binomial_theorem_and_row_sums():
    for (x, y, n) in [(1, 1, 6), (2, 3, 5), (0.3, 0.7, 8), (5, -2, 7)]:
        s, direct = binomial_theorem_check(x, y, n)
        assert _approx(s, direct, tol=1e-9)
    # special cases: x=y=1 -> 2^n ; alternating -> 0 (n>=1)
    for n in range(1, 12):
        assert binomial_coefficient_sum(n) == 2 ** n
        assert binomial_coefficient_sum(n, signed=True) == 0


# 7 -------------------------------------------------------------------------
def test_binomial_pmf_normalization_feeds_ST07():
    # the x=p, y=1-p binomial theorem IS the binomial pmf summing to 1 (~ST-07)
    for n, p in [(6, 0.3), (10, 0.5), (20, 0.85)]:
        total, _ = binomial_theorem_check(p, 1.0 - p, n)
        assert _approx(total, 1.0, tol=1e-9)


# 8 -------------------------------------------------------------------------
def test_multinomial_reduces_and_alias():
    # binomial is the two-class multinomial
    for n in range(0, 11):
        for k in range(0, n + 1):
            assert multinomial(n, [k, n - k]) == combinations(n, k)
    # the alias permutations_with_repetition agrees
    assert permutations_with_repetition(11, [1, 4, 4, 2]) == multinomial(11, [1, 4, 4, 2])
    assert multinomial(11, [1, 4, 4, 2]) == 34650          # 'MISSISSIPPI'


# 9 -------------------------------------------------------------------------
def test_multinomial_theorem():
    # sum over all compositions of n into m parts of n!/(k1!...km!) = m^n
    for n, m in [(4, 3), (5, 3), (6, 2), (3, 4)]:
        total = sum(multinomial(n, comp) for comp in _compositions(n, m))
        assert total == m ** n


# 10 ------------------------------------------------------------------------
def test_stars_and_bars_and_with_replacement():
    # x1+...+xk = n has C(n+k-1, k-1) solutions
    for n in range(0, 8):
        for k in range(1, 6):
            assert stars_and_bars(n, k) == math.comb(n + k - 1, k - 1)
            # explicit enumeration for k = 3
            if k == 3:
                count = sum(1 for a in range(n + 1) for b in range(n + 1 - a))
                assert stars_and_bars(n, 3) == count
    # dual: choose k from n types with replacement = place k balls in n boxes
    for n in range(1, 7):
        for k in range(0, 7):
            assert combinations_with_replacement(n, k) == stars_and_bars(k, n)
    # Einstein-solid multiplicity W = C(q+N-1, q) (~SM-01)
    N, q = 4, 10
    assert stars_and_bars(q, N) == math.comb(q + N - 1, q)


# 11 ------------------------------------------------------------------------
def test_multiplication_principle_and_ordered_with_replacement():
    assert multiplication_principle([6, 6, 6]) == 216
    assert multiplication_principle([26, 26, 10, 10, 10]) == 26 ** 2 * 10 ** 3
    assert multiplication_principle([]) == 1                # empty product
    for n in range(1, 7):
        for k in range(0, 6):
            assert ordered_with_replacement(n, k) == n ** k
            assert ordered_with_replacement(n, k) == multiplication_principle([n] * k)


# 12 ------------------------------------------------------------------------
def test_vandermonde_identity():
    # sum_j C(m,j) C(n,k-j) = C(m+n, k)
    for m in range(0, 7):
        for nn in range(0, 7):
            for k in range(0, m + nn + 1):
                lhs = sum(combinations(m, j) * combinations(nn, k - j) for j in range(0, k + 1))
                assert lhs == combinations(m + nn, k)


# 13 ------------------------------------------------------------------------
def test_beta_integral_continuous_check():
    # int_0^1 x^k (1-x)^{n-k} dx = 1/((n+1) C(n,k))  (Beta-binomial bridge)
    for n in range(1, 7):
        for k in range(0, n + 1):
            num = _integrate(lambda x: x ** k * (1.0 - x) ** (n - k), 0.0, 1.0, n=40000)
            assert _approx(num, beta_integral(k, n), tol=1e-5)


# 14 ------------------------------------------------------------------------
def test_gamma_integral_recovers_factorial():
    # n! = Gamma(n+1) = int_0^inf t^n e^{-t} dt   (cut off at t = 60)
    for n in range(0, 7):
        val = _integrate(lambda t: t ** n * math.exp(-t), 0.0, 60.0, n=120000)
        assert _approx(val, factorial(n), tol=1e-4)
        assert _approx(val, math.gamma(n + 1), tol=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
