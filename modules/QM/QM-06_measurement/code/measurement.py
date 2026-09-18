"""
QM-06  Measurement postulates  --  what a measurement *is*, as linear algebra you
can evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-06).
Builds on ~QM-02 (Born rule) and ~QM-05 (Hilbert space, Hermitian operators,
commutators); feeds ~QM-07 (incompatible observables -> uncertainty), and points
forward to ~QM-11 (spin) and ~QM-20 (density matrix / mixed states).

The measurement postulates, each a function group below (Griffiths 3e Ch. 3):

  1. Observable  <->  Hermitian operator.  An observable A is represented by a
     Hermitian operator; its real eigenvalues {a_n} are the only possible
     measured values, and its eigenvectors form an orthonormal basis (eigh).
     (is_hermitian, eigensystem, eigenspaces)

  2. Generalized statistical interpretation.  Measuring A on |psi> yields the
     eigenvalue a_n with probability  P(a_n) = |<a_n|psi>|^2  (= ||P_n psi||^2
     for a degenerate eigenspace).  The P(a_n) sum to 1.
     (outcome_probabilities)

  3. Expectation value.  <A> = sum_n a_n P(a_n) = <psi|A|psi>  -- two routes to
     the SAME number; the function computes both and verifies they agree.
     (expectation, variance, standard_deviation)

  4. Collapse.  Immediately after a measurement returning a_n, the state jumps
     to the normalized projection of |psi> onto the a_n eigenspace.  A repeat
     measurement then returns a_n with probability 1 (the collapse is
     idempotent: measurement makes the result reproducible).
     (collapse, measure)

  5. Compatible vs incompatible.  Commuting observables share an eigenbasis, so
     A then B then A returns the original A-value (no disturbance).
     Non-commuting observables (e.g. sigma_x and sigma_z) do not: an intervening
     measurement randomizes the first outcome.
     (commutator, commute, + the spin example in _demo)

Linear algebra via numpy (QM is matrix-heavy; cf. ~MA-04).  Natural units hbar=1,
so spin-1/2 operators have eigenvalues +/-1/2 (i.e. +/-hbar/2).

Convention: every measurement routine takes the STATE first, then the OBSERVABLE
-- outcome_probabilities(psi, A), expectation(psi, A), collapse(psi, A, n) --
reading like "what A does to psi".
"""

import numpy as np

__all__ = [
    # constants / operators
    "HBAR", "I2", "sigma_x", "sigma_y", "sigma_z", "Sx", "Sy", "Sz",
    # operator predicates / algebra
    "is_hermitian", "commutator", "commute", "eigensystem", "eigenspaces",
    # the postulates
    "outcome_probabilities", "expectation", "variance", "standard_deviation",
    "collapse", "measure", "index_of",
    # spin helpers (the Stern-Gerlach example)
    "spin_state", "spin_operator",
    # utility
    "normalize",
]

HBAR = 1.0  # natural units

# --- spin-1/2 toolkit (the canonical 2-level observables) --------------------
I2      = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
# spin operators  S = (hbar/2) sigma  (eigenvalues +/- hbar/2)
Sx = 0.5 * HBAR * sigma_x
Sy = 0.5 * HBAR * sigma_y
Sz = 0.5 * HBAR * sigma_z

_TOL = 1e-9


# --- 0. plumbing -------------------------------------------------------------

def normalize(psi):
    """Return |psi> rescaled to unit norm <psi|psi> = 1 (complex column vector).

    The statistical interpretation only makes sense for a normalized state
    (Griffiths 3e Sec.1.4), so every routine here normalizes its input first."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    nrm = np.sqrt(np.vdot(psi, psi).real)
    if nrm < _TOL:
        raise ValueError("zero (or near-zero) vector cannot be normalized")
    return psi / nrm


def is_hermitian(A, tol=1e-10):
    """True iff A is square and Hermitian, A = A^dagger.

    Observables are represented by Hermitian operators precisely because their
    expectation values come out real (Griffiths 3e Sec.3.2.1)."""
    A = np.asarray(A, dtype=complex)
    return A.ndim == 2 and A.shape[0] == A.shape[1] and \
        np.allclose(A, A.conj().T, atol=tol)


def commutator(A, B):
    """The commutator [A, B] = A B - B A (a matrix).

    [A,B] = 0 means A and B are *compatible* observables (Griffiths 3e Sec.3.5.1)."""
    A = np.asarray(A, dtype=complex)
    B = np.asarray(B, dtype=complex)
    return A @ B - B @ A


def commute(A, B, tol=1e-9):
    """True iff [A, B] = 0 to within tol -- i.e. A, B are compatible observables."""
    return np.allclose(commutator(A, B), 0.0, atol=tol)


# --- 1. observable <-> Hermitian operator; its eigenstructure ----------------

def eigensystem(A):
    """Eigenvalues (ascending, real) and orthonormal eigenvectors (columns) of a
    Hermitian A, via numpy.linalg.eigh.

    For a Hermitian operator the eigenvalues are real and the eigenvectors form a
    complete orthonormal basis (Griffiths 3e Sec.3.3) -- the spectral theorem
    (~MA-04, ~QM-05).  Returns (vals, vecs) with A @ vecs[:,k] = vals[k]*vecs[:,k]."""
    A = np.asarray(A, dtype=complex)
    if not is_hermitian(A):
        raise ValueError("observable must be a Hermitian operator")
    vals, vecs = np.linalg.eigh(A)
    return vals.real, vecs


def eigenspaces(A, tol=1e-9):
    """Group the spectrum of Hermitian A into its DISTINCT eigenvalues.

    Returns a list of (eigenvalue, projector) pairs, sorted by eigenvalue
    ascending, where `projector` P_n = sum |a><a| over the degenerate eigenspace
    of that eigenvalue.  The P_n are orthogonal projectors that resolve the
    identity (sum_n P_n = I), which is what makes the probabilities below sum to
    one.  Degeneracy is handled correctly: a d-fold eigenvalue contributes one
    rank-d projector, not d separate outcomes."""
    vals, vecs = eigensystem(A)
    spaces = []
    n = len(vals)
    i = 0
    while i < n:
        j = i + 1
        while j < n and abs(vals[j] - vals[i]) <= tol * (1.0 + abs(vals[i])):
            j += 1
        block = vecs[:, i:j]                 # orthonormal columns of the eigenspace
        val = float(np.mean(vals[i:j]))
        P = block @ block.conj().T           # projector onto the eigenspace
        spaces.append((val, P))
        i = j
    return spaces


def index_of(A, value, tol=1e-6):
    """Index n (into eigenspaces / outcome_probabilities) of a target eigenvalue.

    Convenience for forcing a particular measurement branch in the examples,
    e.g. index_of(sigma_z, +1) is the 'spin-up-along-z' outcome."""
    for n, (val, _) in enumerate(eigenspaces(A)):
        if abs(val - value) <= tol * (1.0 + abs(value)):
            return n
    raise ValueError("%g is not an eigenvalue of the operator" % value)


# --- 2. generalized statistical interpretation: P(a_n) = |<a_n|psi>|^2 -------

def outcome_probabilities(psi, A):
    """The measurement outcomes of observable A on state |psi>.

        P(a_n) = |<a_n|psi>|^2          (non-degenerate)
        P(a_n) = <psi|P_n|psi> = ||P_n psi||^2   (general / degenerate)

    This is the generalized statistical interpretation (Griffiths 3e Sec.3.4,
    Eq. 3.43): a measurement is *certain* to yield one of the eigenvalues a_n,
    with the probabilities returned here.  Returns (values, probs) as real
    arrays aligned with eigenspaces(A); the probs are non-negative and sum to 1.
    """
    psi = normalize(psi)
    spaces = eigenspaces(A)
    vals = np.array([v for v, _ in spaces], dtype=float)
    probs = np.empty(len(spaces))
    for k, (_, P) in enumerate(spaces):
        proj = P @ psi
        probs[k] = np.vdot(proj, proj).real      # ||P_k psi||^2  >= 0
    s = probs.sum()
    if abs(s - 1.0) > 1e-8:                       # the P_n resolve the identity
        raise AssertionError("probabilities sum to %.12g, not 1" % s)
    return vals, probs


# --- 3. expectation value: <A> = sum a_n P(a_n) = <psi|A|psi> ----------------

def expectation(psi, A):
    """Expectation value <A> of observable A in state |psi>, computed BOTH ways
    and verified to agree:

        spectral :  <A> = sum_n a_n P(a_n)
        sandwich :  <A> = <psi|A|psi>

    These are equal identically (Griffiths 3e Eqs. 3.48-3.51); for a Hermitian A
    the result is real.  The agreement is asserted internally, so a passing call
    is itself a proof of the identity for this (psi, A).  Returns the real number.
    """
    psi = normalize(psi)
    A = np.asarray(A, dtype=complex)
    sandwich = np.vdot(psi, A @ psi)             # <psi|A psi>
    vals, probs = outcome_probabilities(psi, A)
    spectral = float(np.sum(vals * probs))
    if abs(sandwich.imag) > 1e-8:
        raise AssertionError("non-real expectation -> operator not Hermitian")
    if abs(sandwich.real - spectral) > 1e-8 * (1.0 + abs(spectral)):
        raise AssertionError("the two expectation routes disagree: %.12g vs %.12g"
                             % (sandwich.real, spectral))
    return sandwich.real


def variance(psi, A):
    """Variance  sigma_A^2 = <A^2> - <A>^2 >= 0 in state |psi>.

    Zero iff |psi> is an eigenstate of A -- a 'determinate state' for which every
    measurement gives the same value with certainty (Griffiths 3e Sec.3.2.2).
    The square root feeds the uncertainty principle (~QM-07)."""
    A = np.asarray(A, dtype=complex)
    mean = expectation(psi, A)
    mean_sq = expectation(psi, A @ A)
    return mean_sq - mean**2


def standard_deviation(psi, A):
    """Standard deviation sigma_A = sqrt(<A^2> - <A>^2) (clamped at 0 for tiny
    negative round-off)."""
    return np.sqrt(max(0.0, variance(psi, A)))


# --- 4. collapse: the state jumps to the measured eigenstate -----------------

def collapse(psi, A, n):
    """State immediately after measuring A and obtaining the n-th eigenvalue:
    the normalized projection of |psi> onto that eigenspace,

        |psi'> = P_n |psi> / || P_n |psi> ||                     (Griffiths 3e Sec.3.4)

    `n` indexes eigenspaces(A) (ascending eigenvalue; use index_of for a value).
    Raises if outcome n has probability ~0 (you cannot collapse onto a result
    that can't occur).  Re-measuring A on |psi'> returns a_n with probability 1
    -- the postulate is idempotent (see measure / the tests)."""
    psi = normalize(psi)
    spaces = eigenspaces(A)
    _, P = spaces[n]
    proj = P @ psi
    nrm = np.sqrt(np.vdot(proj, proj).real)
    if nrm < 1e-9:
        raise ValueError("outcome n=%d has ~zero probability; cannot collapse" % n)
    return proj / nrm


def measure(psi, A, outcome=None, rng=None):
    """Perform a measurement of A on |psi>: return (eigenvalue, collapsed_state).

    If `outcome` is None the result is *sampled* from P(a_n) (a real, random
    measurement); pass an integer `outcome` (an eigenspaces index) to force a
    particular branch -- handy for building deterministic sequential examples.
    The returned state is the post-collapse |psi'>, ready to feed the next
    measurement (this is how sequential-measurement disturbance is demonstrated).
    """
    psi = normalize(psi)
    vals, probs = outcome_probabilities(psi, A)
    if outcome is None:
        rng = np.random.default_rng() if rng is None else rng
        outcome = int(rng.choice(len(vals), p=probs / probs.sum()))
    return vals[outcome], collapse(psi, A, outcome)


# --- 5. spin helpers: the Stern-Gerlach example ------------------------------

def spin_state(theta, phi=0.0):
    """Spin-1/2 state |+n> pointing along the direction (theta, phi) on the Bloch
    sphere -- the eigenstate of n.sigma with eigenvalue +1:

        |+n> = ( cos(theta/2),  e^{i phi} sin(theta/2) ).

    theta=0 is spin-up along z (|0>); theta=pi/2, phi=0 is spin-up along x (|+x>)."""
    return np.array([np.cos(theta / 2.0),
                     np.exp(1j * phi) * np.sin(theta / 2.0)], dtype=complex)


def spin_operator(nx, ny, nz):
    """Spin observable along the (not necessarily unit) direction (nx,ny,nz):
    S_n = (hbar/2) n.sigma / |n|, with eigenvalues +/- hbar/2.  Measuring this is
    a Stern-Gerlach magnet oriented along n."""
    n = np.array([nx, ny, nz], dtype=float)
    n = n / np.linalg.norm(n)
    return 0.5 * HBAR * (n[0] * sigma_x + n[1] * sigma_y + n[2] * sigma_z)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-06 Measurement postulates -- a spin-1/2 Stern-Gerlach cascade\n")

    up_z = spin_state(0.0)                 # |0>, spin-up along z
    print("State: spin-up along z,  |0> = (1, 0)\n")

    print("Measure S_z (a z-oriented SG magnet):")
    vals, probs = outcome_probabilities(up_z, Sz)
    for v, p in sorted(zip(vals, probs), reverse=True):
        print("   outcome %+.1f hbar : P = %.3f" % (v, p))
    print("   -> determinate: +hbar/2 with certainty, <S_z> = %+.3f hbar,"
          " sigma = %.3f\n" % (expectation(up_z, Sz), standard_deviation(up_z, Sz)))

    print("Now rotate the magnet to x and measure S_x on that same |0>:")
    vals, probs = outcome_probabilities(up_z, Sx)
    for v, p in sorted(zip(vals, probs), reverse=True):
        print("   outcome %+.1f hbar : P = %.3f" % (v, p))
    print("   -> 50/50: S_x is INcompatible with S_z (they don't commute).\n")

    print("Sequential disturbance  S_x -> S_z -> S_x  starting from |+x>:")
    plus_x = spin_state(np.pi / 2.0, 0.0)
    a1, st = measure(plus_x, Sx, outcome=index_of(Sx, +0.5))    # force +hbar/2
    print("   1) measure S_x: got %+.1f hbar (certain, the prepared value)" % a1)
    a2, st = measure(st, Sz, outcome=index_of(Sz, +0.5))        # force +hbar/2
    print("   2) measure S_z: got %+.1f hbar (collapses to |0>)" % a2)
    vals, probs = outcome_probabilities(st, Sx)
    pplus = probs[index_of(Sx, +0.5)]
    print("   3) measure S_x again: P(+hbar/2) = %.3f" % pplus)
    print("      -> the intervening S_z RANDOMIZED the once-certain S_x outcome.\n")

    print("A bigger Hermitian observable (3-level), expectation two ways agree:")
    A = np.array([[2, 1j, 0], [-1j, 2, 1j], [0, -1j, 2]], dtype=complex)
    psi = np.array([1, 1, 1], dtype=complex)
    vals, probs = outcome_probabilities(psi, A)
    print("   eigenvalues :", np.round(vals, 4))
    print("   P(a_n)      :", np.round(probs, 4), " (sum = %.6f)" % probs.sum())
    print("   <A> = %.6f  (= sum a_n P(a_n) = <psi|A|psi>)" % expectation(psi, A))


if __name__ == "__main__":
    _demo()
