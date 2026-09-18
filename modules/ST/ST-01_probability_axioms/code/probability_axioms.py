"""ST-01  Sample spaces & the axioms of probability -- set algebra, the Kolmogorov
axioms, inclusion-exclusion, and equally-likely outcomes.

Probability Theory trunk, module ST-01 (modules/list_ST.txt).  A faithful replica
of Penn State STAT 414, Lessons 1-2 (The Big Picture; Properties of Probability).
Builds on ~MA-19 (the working probability/statistics toolkit this trunk now
deep-dives) and ~SM-01 (equal a priori probabilities = the equally-likely measure
made physical).  The ~QM-02 Born rule  P_i = |psi_i|^2  is exactly these axioms
applied to a quantum amplitude vector -- see born_probabilities.

A probability model is a triple (S, F, P): a SAMPLE SPACE S of outcomes, a
collection F of EVENTS (subsets of S), and a set function P obeying Kolmogorov's
three axioms
    (A1)  P(A) >= 0,     (A2)  P(S) = 1,     (A3)  P(disjoint union) = sum of P.
Everything else -- P(empty)=0, P(A^c)=1-P(A), monotonicity, the addition rule
P(A u B) = P(A)+P(B)-P(A n B), inclusion-exclusion, Boole's bound, and the
classical P(A)=|A|/|S| -- is a THEOREM, derived in notes.md and checked here.

Pure Python stdlib (math, itertools).  Self-validating: inclusion-exclusion is
checked against brute-force counts on explicit dice / card sample spaces, De
Morgan's laws on finite sets, and the continuous addition rule by midpoint
integration (prob_continuous).
"""

import math
from itertools import product

__all__ = [
    "is_valid_probability", "prob_empty", "prob_sure", "complement",
    "prob_equally_likely", "union_disjoint", "union_two",
    "intersection_from_union", "prob_difference", "union_three",
    "inclusion_exclusion", "boole_bound", "monotone",
    "complement_set", "product_sample_space", "event_probability",
    "standard_deck", "uniform_pdf", "prob_continuous", "born_probabilities",
]

_TOL = 1e-12


# --- the axioms and their immediate consequences (STAT 414 L2) ---------------

def is_valid_probability(p, tol=_TOL):
    """Axiom check: a probability satisfies 0 <= P(A) <= 1 (Axiom A1 with the
    normalization A2 forcing the upper bound)."""
    return -tol <= p <= 1.0 + tol


def prob_empty():
    """Consequence of A2/A3:  P(empty set) = 0  (the impossible event)."""
    return 0.0


def prob_sure():
    """Axiom A2:  P(S) = 1  (the certain event is the whole sample space)."""
    return 1.0


def complement(p):
    """Complement rule:  P(A^c) = 1 - P(A)  (from S = A u A^c, disjoint)."""
    return 1.0 - p


def prob_equally_likely(favorable, total):
    """Classical / equally-likely probability:  P(A) = |A| / |S|  (every outcome
    of a finite S carries the same weight 1/|S|)."""
    if total <= 0:
        raise ValueError("total number of equally-likely outcomes must be > 0")
    return favorable / total


# --- additivity: disjoint unions, the addition rule, differences -------------

def union_disjoint(*probs):
    """Axiom A3 (finite additivity):  P(A_1 u ... u A_n) = sum P(A_i)  for
    pairwise-disjoint (mutually exclusive) events."""
    return math.fsum(probs)


def union_two(pa, pb, pab):
    """Addition rule (two events):  P(A u B) = P(A) + P(B) - P(A n B).
    The -P(A n B) corrects the double count of the overlap."""
    return pa + pb - pab


def intersection_from_union(pa, pb, paub):
    """Invert the addition rule:  P(A n B) = P(A) + P(B) - P(A u B)."""
    return pa + pb - paub


def prob_difference(pa, pab):
    """Set difference:  P(A \\ B) = P(A n B^c) = P(A) - P(A n B)."""
    return pa - pab


# --- inclusion-exclusion and Boole's inequality (STAT 414 L2) ----------------

def union_three(pa, pb, pc, pab, pac, pbc, pabc):
    """3-set inclusion-exclusion:
        P(A u B u C) = P(A)+P(B)+P(C)
                       - P(A n B) - P(A n C) - P(B n C)
                       + P(A n B n C)."""
    return (pa + pb + pc) - (pab + pac + pbc) + pabc


def _as_sum(x):
    """Sum a list/tuple of intersection probabilities (or pass a scalar through)."""
    if x is None:
        return 0.0
    if isinstance(x, (list, tuple)):
        return math.fsum(x)
    return float(x)


def inclusion_exclusion(singles, pairs=None, triples=None, quad=None):
    """General inclusion-exclusion (up to 4 events):
        P(union A_i) = S1 - S2 + S3 - S4 + ...,
    where S_k is the sum of all k-fold intersection probabilities.  Each argument
    is the list (or scalar) of k-fold intersection probabilities."""
    return _as_sum(singles) - _as_sum(pairs) + _as_sum(triples) - _as_sum(quad)


def boole_bound(probs):
    """Boole's inequality (union bound / subadditivity):
        P(union A_i) <= sum P(A_i).
    Returns the right-hand side; min(1, .) is the sharpened bound since P <= 1."""
    return math.fsum(probs)


def monotone(p_sub, p_super, tol=_TOL):
    """Monotonicity check: if A subset B then P(A) <= P(B).  Returns True when the
    pair (P(A), P(B)) is consistent with A being a subset of B."""
    return p_sub <= p_super + tol


# --- sample spaces as concrete sets: set algebra & equally-likely measure ----

def complement_set(sample_space, event):
    """Set complement  A^c = S \\ A  within an explicit finite sample space S
    (used to verify De Morgan's laws on real sets)."""
    return set(sample_space) - set(event)


def product_sample_space(outcomes, repeat):
    """Cartesian-product sample space  S = outcomes^repeat  (e.g. rolling
    'repeat' dice), as an explicit list of outcome tuples."""
    return list(product(outcomes, repeat=repeat))


def event_probability(sample_space, predicate):
    """Equally-likely event probability  P(A) = |A| / |S|, where the event
    A = {omega in S : predicate(omega)} is selected by a boolean predicate."""
    total = len(sample_space)
    if total == 0:
        raise ValueError("empty sample space")
    favorable = sum(1 for omega in sample_space if predicate(omega))
    return favorable / total


def standard_deck():
    """The 52-card sample space: every (rank, suit) pair, all equally likely."""
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["clubs", "diamonds", "hearts", "spades"]
    return [(r, s) for s in suits for r in ranks]


# --- continuous sample spaces: probability as an integral --------------------

def uniform_pdf(x, a=0.0, b=1.0):
    """Continuous-uniform density on [a,b]:  f(x) = 1/(b-a) for a<=x<=b, else 0.
    A continuous sample space where P(A) = integral_A f obeys the same axioms."""
    return 1.0 / (b - a) if a <= x <= b else 0.0


def _integrate(f, a, b, n=20000):
    """Midpoint-rule numerical integral of f over [a,b] (continuous-axiom check)."""
    if b <= a:
        return 0.0
    h = (b - a) / n
    return math.fsum(f(a + (i + 0.5) * h) * h for i in range(n))


def prob_continuous(pdf, a, b):
    """Probability of an interval event under a continuous density:
        P([a,b]) = integral_a^b f(x) dx  (the continuous Axiom A2/A3 in action)."""
    return _integrate(pdf, a, b)


# --- the Born rule: the same axioms applied to |psi|^2 (~QM-02) --------------

def born_probabilities(amplitudes):
    """Born rule (~QM-02):  P_i = |psi_i|^2 / sum_j |psi_j|^2  -- Kolmogorov's
    axioms applied to a quantum amplitude vector.  Normalization (Axiom A2) is the
    inner product <psi|psi>; each P_i >= 0 is Axiom A1."""
    weights = [abs(a) ** 2 for a in amplitudes]
    Z = math.fsum(weights)
    if Z <= 0:
        raise ValueError("zero-norm amplitude vector")
    return [w / Z for w in weights]


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-01  sample spaces & the axioms of probability -- demo")
    print("=" * 56)

    # equally-likely: two fair dice
    S2 = product_sample_space(range(1, 7), repeat=2)
    p_sum7 = event_probability(S2, lambda w: w[0] + w[1] == 7)
    p_sum11 = event_probability(S2, lambda w: w[0] + w[1] == 11)
    print(f"two fair dice, |S| = {len(S2)}:")
    print(f"  P(sum = 7)  = {p_sum7:.6f}  = 6/36 = 1/6")
    print(f"  P(sum = 11) = {p_sum11:.6f}  = 2/36 = 1/18")

    # addition rule on a card deck
    deck = standard_deck()
    p_heart = event_probability(deck, lambda c: c[1] == "hearts")
    p_face = event_probability(deck, lambda c: c[0] in ("J", "Q", "K"))
    p_heart_and_face = event_probability(
        deck, lambda c: c[1] == "hearts" and c[0] in ("J", "Q", "K"))
    p_heart_or_face = union_two(p_heart, p_face, p_heart_and_face)
    p_brute = event_probability(
        deck, lambda c: c[1] == "hearts" or c[0] in ("J", "Q", "K"))
    print(f"\nstandard 52-card deck:")
    print(f"  P(heart) = {p_heart:.4f},  P(face) = {p_face:.4f},"
          f"  P(heart n face) = {p_heart_and_face:.4f}")
    print(f"  P(heart u face) = {p_heart_or_face:.6f}  (addition rule)"
          f"  vs brute {p_brute:.6f}")

    # 3-set inclusion-exclusion vs brute force on the dice space
    A = lambda w: w[0] % 2 == 0          # first die even
    B = lambda w: w[0] + w[1] >= 8       # sum at least 8
    C = lambda w: w[1] == 3              # second die is 3
    pa, pb, pc = (event_probability(S2, A), event_probability(S2, B),
                  event_probability(S2, C))
    pab = event_probability(S2, lambda w: A(w) and B(w))
    pac = event_probability(S2, lambda w: A(w) and C(w))
    pbc = event_probability(S2, lambda w: B(w) and C(w))
    pabc = event_probability(S2, lambda w: A(w) and B(w) and C(w))
    ie = union_three(pa, pb, pc, pab, pac, pbc, pabc)
    brute = event_probability(S2, lambda w: A(w) or B(w) or C(w))
    print(f"\ninclusion-exclusion (3 events on the dice space):")
    print(f"  union_three = {ie:.6f}  vs brute {brute:.6f}"
          f"  (Boole bound {boole_bound([pa, pb, pc]):.4f})")

    # De Morgan on a finite sample space
    Sset = set(S2)
    Aset = {w for w in S2 if A(w)}
    Bset = {w for w in S2 if B(w)}
    lhs = complement_set(Sset, Aset | Bset)
    rhs = complement_set(Sset, Aset) & complement_set(Sset, Bset)
    print(f"\nDe Morgan:  (A u B)^c == A^c n B^c  ->  {lhs == rhs}")

    # continuous uniform sample space
    total = prob_continuous(lambda x: uniform_pdf(x, 0.0, 1.0), 0.0, 1.0)
    p_int = prob_continuous(lambda x: uniform_pdf(x, 0.0, 1.0), 0.25, 0.75)
    print(f"\ncontinuous uniform on [0,1]:")
    print(f"  total mass = {total:.6f} (= 1, Axiom A2),  P([0.25,0.75]) = {p_int:.6f}")

    # Born rule: equal superposition of 4 basis states (~QM-02)
    probs = born_probabilities([1.0, 1.0, 1.0, 1.0])
    print(f"\nBorn rule (~QM-02), equal 4-state superposition:")
    print(f"  P_i = {[round(p, 4) for p in probs]},  sum = {math.fsum(probs):.6f}")


if __name__ == "__main__":
    _demo()
