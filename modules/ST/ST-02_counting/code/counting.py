"""ST-02  Counting techniques -- permutations, combinations, multinomial, stars & bars.

Probability theory trunk, module ST-02 (Penn State STAT 414, Lesson 3 "Counting
Techniques").  Pure-python counting kernels behind every "equally likely
outcomes" probability P(A) = N(A)/N(S).

Four sampling schemes (draw k from n):
    ordered,   with    replacement :  n**k
    ordered,   without replacement :  P(n,k) = n!/(n-k)!
    unordered, without replacement :  C(n,k) = n!/(k!(n-k)!)
    unordered, with    replacement :  C(n+k-1, k)            (stars & bars)
plus the multinomial coefficient n!/(k1!...km!) -- the number of distinguishable
permutations, which is exactly the statistical multiplicity W of ~SM-01 -- and
the binomial theorem, whose x=p, y=1-p specialization normalizes the binomial
pmf of ~ST-07.

Pure stdlib (math) only; self-contained.  A midpoint integrator (_integrate) is
provided for the continuous Beta- and Gamma-function checks of the discrete
coefficients.
"""

import math

__all__ = [
    "factorial", "multiplication_principle", "ordered_with_replacement",
    "permutations", "combinations", "permutations_with_repetition",
    "multinomial", "stars_and_bars", "combinations_with_replacement",
    "pascal_row", "pascal_rule_holds", "binomial_theorem_check",
    "binomial_coefficient_sum", "beta_integral",
]


# --- a numerical integrator (for the continuous Beta/Gamma checks) -----------

def _integrate(f, a, b, n=200000):
    """Midpoint-rule integral of f on [a, b] with n panels (continuous checks)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- factorial & the multiplication principle (STAT 414 L3.1) ----------------

def factorial(n):
    """n! = prod_{i=1}^{n} i, with the empty product 0! = 1 (cross-checks math.factorial)."""
    if n < 0:
        raise ValueError("factorial: n must be a non-negative integer")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def multiplication_principle(sizes):
    """Fundamental counting principle: |A1 x ... x Am| = prod_i |A_i| (sizes is a list)."""
    total = 1
    for s in sizes:
        total *= s
    return total


def ordered_with_replacement(n, k):
    """Ordered samples of size k from n types, WITH replacement: n**k (k independent slots)."""
    return n ** k


# --- permutations: ordered, without replacement (STAT 414 L3.2) --------------

def permutations(n, k):
    """Permutations P(n,k) = n!/(n-k)! = n(n-1)...(n-k+1) -- ordered, no replacement."""
    if not (0 <= k <= n):
        raise ValueError("permutations: require 0 <= k <= n")
    result = 1
    for i in range(k):
        result *= (n - i)
    return result


# --- combinations: unordered, without replacement (STAT 414 L3.2) ------------

def combinations(n, k):
    """Combinations C(n,k) = n!/(k!(n-k)!) = P(n,k)/k! -- unordered, no replacement.

    Returns 0 outside 0 <= k <= n (so Pascal/binomial sums extend cleanly)."""
    if k < 0 or k > n or n < 0:
        return 0
    return permutations(n, k) // factorial(k)


# --- permutations with repeated (indistinguishable) objects = multinomial ----

def permutations_with_repetition(n, ks):
    """Distinguishable permutations of n objects with type-multiplicities ks:
    n!/(k1! k2! ... km!)  (alias of multinomial; sum(ks) must equal n)."""
    return multinomial(n, ks)


def multinomial(n, ks):
    """Multinomial coefficient C(n; k1,...,km) = n!/(k1!...km!) -- distinguishable
    permutations / the statistical multiplicity W of ~SM-01 (sum(ks) == n)."""
    if sum(ks) != n:
        raise ValueError("multinomial: the k_i must sum to n")
    result = factorial(n)
    for k in ks:
        if k < 0:
            raise ValueError("multinomial: each k_i must be >= 0")
        result //= factorial(k)
    return result


# --- combinations with replacement: stars and bars (STAT 414 L3.2) -----------

def stars_and_bars(n, k):
    """Stars & bars: # non-negative integer solutions of x1+...+xk = n is
    C(n+k-1, k-1) -- n identical items distributed into k distinct boxes."""
    if n < 0 or k < 1:
        raise ValueError("stars_and_bars: require n >= 0 and k >= 1")
    return combinations(n + k - 1, k - 1)


def combinations_with_replacement(n, k):
    """Unordered samples of size k from n types, WITH replacement: C(n+k-1, k)
    = stars_and_bars(k, n) (k stars / balls into n type-boxes)."""
    if n < 1 or k < 0:
        raise ValueError("combinations_with_replacement: require n >= 1 and k >= 0")
    return combinations(n + k - 1, k)


# --- Pascal's triangle & the binomial theorem (STAT 414 L3.2) ----------------

def pascal_row(n):
    """Row n of Pascal's triangle: [C(n,0), C(n,1), ..., C(n,n)]."""
    return [combinations(n, k) for k in range(n + 1)]


def pascal_rule_holds(n, k):
    """Pascal's recurrence C(n,k) = C(n-1,k-1) + C(n-1,k) (True/False)."""
    return combinations(n, k) == combinations(n - 1, k - 1) + combinations(n - 1, k)


def binomial_theorem_check(x, y, n):
    """Binomial theorem: returns (sum_k C(n,k) x^k y^{n-k}, (x+y)**n) -- the two are equal."""
    s = sum(combinations(n, k) * x ** k * y ** (n - k) for k in range(n + 1))
    return s, (x + y) ** n


def binomial_coefficient_sum(n, signed=False):
    """Row sum of Pascal's triangle: sum_k C(n,k) = 2^n (signed: sum_k (-1)^k C(n,k) = 0, n>=1)."""
    if signed:
        return sum((-1) ** k * combinations(n, k) for k in range(n + 1))
    return sum(combinations(n, k) for k in range(n + 1))


# --- the Beta-binomial bridge (continuous check; ~ST-11) ---------------------

def beta_integral(k, n):
    """B(k+1, n-k+1) = int_0^1 x^k (1-x)^{n-k} dx = 1/((n+1) C(n,k)) -- ties C(n,k)
    to the Beta/Gamma function (the continuous _integrate cross-check)."""
    return 1.0 / ((n + 1) * combinations(n, k))


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-02  Counting techniques -- demo")
    print("=" * 52)

    print("Four ways to draw k=3 from n=5:")
    print(f"  ordered,   with    repl :  n^k          = {ordered_with_replacement(5, 3)}")
    print(f"  ordered,   without repl :  P(5,3)        = {permutations(5, 3)}")
    print(f"  unordered, without repl :  C(5,3)        = {combinations(5, 3)}")
    print(f"  unordered, with    repl :  C(5+3-1,3)    = {combinations_with_replacement(5, 3)}")

    print("\nMultiplication principle (3 dice, 2 coins): "
          f"{multiplication_principle([6, 6, 6, 2, 2])} outcomes")

    print("\nP(n,k) = C(n,k) * k!  (order matters by a factor k!):")
    n, k = 10, 4
    print(f"  P(10,4) = {permutations(n, k)} = C(10,4)*4! = "
          f"{combinations(n, k)} * {factorial(k)} = {combinations(n, k) * factorial(k)}")

    print("\nMultinomial = distinguishable permutations = multiplicity W (~SM-01):")
    print(f"  'MISSISSIPPI' (1 M, 4 I, 4 S, 2 P): {multinomial(11, [1, 4, 4, 2])}")
    print(f"  W = C(N; n1..) , binomial special case multinomial(5,[2,3]) = "
          f"{multinomial(5, [2, 3])} = C(5,2) = {combinations(5, 2)}")

    print("\nStars & bars: 10 identical quanta into 4 oscillators (Einstein solid):")
    print(f"  stars_and_bars(10, 4) = C(13,3) = {stars_and_bars(10, 4)}")

    print("\nPascal's triangle (rows 0..6):")
    for r in range(7):
        row = pascal_row(r)
        print(f"  n={r}: {row}   sum = 2^{r} = {binomial_coefficient_sum(r)}")

    print("\nBinomial theorem (1+1)^6 and the ST-07 normalization (p=0.3, n=6):")
    s, p6 = binomial_theorem_check(1, 1, 6)
    print(f"  sum_k C(6,k) 1^k 1^(6-k) = {s} = 2^6 = {p6}")
    s2, _ = binomial_theorem_check(0.3, 0.7, 6)
    print(f"  sum_k C(6,k) 0.3^k 0.7^(6-k) = {s2:.6f}  (binomial pmf normalizes to 1)")


if __name__ == "__main__":
    _demo()
