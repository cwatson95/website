"""Tests for QM-06 measurement -- every postulate checked against a closed form.

Run directly:   python3 test_measurement.py      (-> "All N tests passed.")
Or with pytest: pytest test_measurement.py

Each test pins one measurement postulate to an analytic result:
  * observables are Hermitian (real spectrum, orthonormal complete eigenbasis),
  * P(a_n) = |<a_n|psi>|^2 and sum_n P(a_n) = 1,
  * <A> = sum a_n P(a_n) = <psi|A|psi>,
  * an eigenstate is determinate (variance 0); collapse is idempotent,
  * commuting observables don't disturb each other; non-commuting ones do.
"""
import math
import numpy as np

from measurement import (
    sigma_x, sigma_y, sigma_z, I2, Sx, Sz, HBAR,
    is_hermitian, commutator, commute, eigensystem, eigenspaces, index_of,
    outcome_probabilities, expectation, variance, standard_deviation,
    collapse, measure, spin_state, spin_operator, normalize,
)


def _approx(x, y, rel=1e-9, abs_=1e-12):
    return abs(x - y) <= max(rel * abs(y), abs_)


def _rand_hermitian(n, rng):
    """A random n x n Hermitian matrix  (M + M^dagger)/2."""
    M = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return 0.5 * (M + M.conj().T)


def _rand_state(n, rng):
    return rng.standard_normal(n) + 1j * rng.standard_normal(n)


# --- 1. observable <-> Hermitian operator ------------------------------------

def test_hermitian_real_eigenvalues():
    """Observables are Hermitian; their eigenvalues are real (Griffiths 3.2.1).
    Cross-check eigh's reals against the general complex eigensolver, and confirm
    a non-Hermitian operator is rejected."""
    rng = np.random.default_rng(1)
    for n in (2, 3, 5):
        A = _rand_hermitian(n, rng)
        assert is_hermitian(A)
        vals, _ = eigensystem(A)
        w = np.linalg.eigvals(A)               # general (could be complex) solver
        assert np.allclose(np.sort(w.real), np.sort(vals), atol=1e-9)
        assert np.allclose(w.imag, 0.0, atol=1e-9)
    # a non-Hermitian operator is not a valid observable
    bad = np.array([[0, 1], [0, 0]], dtype=complex)
    assert not is_hermitian(bad)
    try:
        eigensystem(bad)
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_eigenbasis_orthonormal_and_complete():
    """Eigenvectors of a Hermitian operator are orthonormal and complete
    (Griffiths 3.3): V^dagger V = I and sum_n |a_n><a_n| = V V^dagger = I."""
    rng = np.random.default_rng(2)
    for n in (2, 4):
        A = _rand_hermitian(n, rng)
        _, V = eigensystem(A)
        assert np.allclose(V.conj().T @ V, np.eye(n), atol=1e-9)   # orthonormal
        assert np.allclose(V @ V.conj().T, np.eye(n), atol=1e-9)   # complete
        # A is rebuilt from its spectral decomposition  A = sum a_n |a_n><a_n|
        vals, _ = eigensystem(A)
        recon = sum(val * P for val, P in eigenspaces(A))
        assert np.allclose(recon, A, atol=1e-9)


def test_pauli_commutators():
    """The spin algebra [sigma_i, sigma_j] = 2 i eps_ijk sigma_k -- the source of
    incompatibility (Griffiths 3.5.1). Compatible operators commute, sigma_x and
    sigma_z do not."""
    assert np.allclose(commutator(sigma_x, sigma_y), 2j * sigma_z)
    assert np.allclose(commutator(sigma_y, sigma_z), 2j * sigma_x)
    assert np.allclose(commutator(sigma_z, sigma_x), 2j * sigma_y)
    assert not commute(sigma_x, sigma_z)        # incompatible
    assert commute(sigma_z, sigma_z)            # trivially compatible
    assert commute(sigma_z, I2)                 # everything commutes with I


# --- 2. generalized statistical interpretation -------------------------------

def test_probabilities_sum_to_one():
    """sum_n P(a_n) = 1 for any state and any Hermitian observable (the P_n
    resolve the identity) -- Griffiths 3.4."""
    rng = np.random.default_rng(3)
    for n in (2, 3, 6):
        A = _rand_hermitian(n, rng)
        psi = _rand_state(n, rng)
        vals, probs = outcome_probabilities(psi, A)
        assert np.all(probs >= -1e-12)
        assert _approx(float(probs.sum()), 1.0)


def test_born_rule_nondegenerate():
    """For a non-degenerate spectrum, P(a_n) = |<a_n|psi>|^2 exactly
    (Griffiths 3.4, Eq. 3.43)."""
    rng = np.random.default_rng(4)
    # distinct eigenvalues -> non-degenerate
    A = np.diag([-2.0, 0.0, 1.0, 3.0]).astype(complex)
    Q = np.linalg.qr(_rand_hermitian(4, rng) + 4 * np.eye(4))[0]   # random unitary
    A = Q @ A @ Q.conj().T
    psi = _rand_state(4, rng)
    psin = normalize(psi)
    vals, vecs = eigensystem(A)
    born = np.array([abs(np.vdot(vecs[:, k], psin)) ** 2 for k in range(4)])
    _, probs = outcome_probabilities(psi, A)
    assert np.allclose(probs, born, atol=1e-9)   # aligned (both eigh-ascending)


def test_degenerate_projector_weight_and_collapse():
    """Degeneracy: P(a) = ||P_a psi||^2 sums over the eigenspace, and collapse
    lands on a state that is still an eigenstate of A with that value."""
    A = np.diag([1.0, 1.0, 4.0]).astype(complex)   # eigenvalue 1 is two-fold
    psi = np.array([1.0, 2.0, 2.0], dtype=complex)  # |.|^2 = 1,4,4  (norm^2 = 9)
    vals, probs = outcome_probabilities(psi, A)
    # ascending: value 1 (proj onto first two), value 4 (third)
    assert _approx(vals[0], 1.0) and _approx(vals[1], 4.0)
    assert _approx(probs[0], 5.0 / 9.0)            # (1+4)/9
    assert _approx(probs[1], 4.0 / 9.0)
    s = collapse(psi, A, 0)                         # collapse onto the degenerate space
    assert np.allclose(A @ s, 1.0 * s, atol=1e-9)  # A s = 1 * s  (still an eigenstate)
    _, p2 = outcome_probabilities(s, A)
    assert _approx(p2[0], 1.0)                      # now determinate for value 1


# --- 3. expectation value ----------------------------------------------------

def test_expectation_two_ways():
    """<A> = sum_n a_n P(a_n) = <psi|A|psi>, and it is real for Hermitian A
    (Griffiths Eqs. 3.48-3.51). expectation() asserts the two routes internally;
    here we also recompute the sandwich form independently."""
    rng = np.random.default_rng(5)
    for n in (2, 3, 5):
        A = _rand_hermitian(n, rng)
        psi = _rand_state(n, rng)
        psin = normalize(psi)
        sandwich = np.vdot(psin, A @ psin)
        vals, probs = outcome_probabilities(psi, A)
        spectral = float(np.sum(vals * probs))
        ev = expectation(psi, A)
        assert _approx(sandwich.imag, 0.0, abs_=1e-9)   # real
        assert _approx(ev, sandwich.real)
        assert _approx(ev, spectral)


def test_spin_expectation_law():
    """For the spin pointing at (theta, phi):  <sigma_z> = cos theta,
    <sigma_x> = sin theta cos phi, <sigma_y> = sin theta sin phi -- the
    Stern-Gerlach projection law (the spin-1/2 analogue of Malus's law)."""
    for theta, phi in [(0.0, 0.0), (math.pi / 2, 0.0), (math.pi / 2, math.pi / 2),
                       (math.pi / 3, math.pi / 4), (math.pi, 0.0)]:
        s = spin_state(theta, phi)
        assert _approx(expectation(s, sigma_z), math.cos(theta), abs_=1e-9)
        assert _approx(expectation(s, sigma_x),
                       math.sin(theta) * math.cos(phi), abs_=1e-9)
        assert _approx(expectation(s, sigma_y),
                       math.sin(theta) * math.sin(phi), abs_=1e-9)


def test_variance_nonneg_and_determinacy():
    """variance >= 0 always; it is ZERO iff the state is an eigenstate (a
    determinate state, Griffiths 3.2.2), and positive for a genuine superposition.
    |+x> has <sigma_z>=0, <sigma_z^2>=1, so variance(sigma_z)=1."""
    rng = np.random.default_rng(6)
    for n in (2, 4):
        A = _rand_hermitian(n, rng)
        psi = _rand_state(n, rng)
        assert variance(psi, A) >= -1e-12
    up_z = spin_state(0.0)                          # eigenstate of sigma_z
    assert standard_deviation(up_z, sigma_z) < 1e-9
    assert _approx(variance(up_z, sigma_z), 0.0, abs_=1e-9)
    plus_x = spin_state(math.pi / 2, 0.0)           # superposition in z-basis
    assert _approx(variance(plus_x, sigma_z), 1.0)
    assert variance(plus_x, sigma_z) > 0.0


# --- 4. collapse / determinate states ----------------------------------------

def test_eigenstate_is_determinate():
    """A measurement on an eigenstate returns that eigenvalue with probability 1
    (Griffiths 3.2.2): the eigenstate is determinate, sigma = 0."""
    rng = np.random.default_rng(7)
    A = _rand_hermitian(4, rng)
    vals, vecs = eigensystem(A)
    for k in range(4):
        ek = vecs[:, k]
        v, p = outcome_probabilities(ek, A)
        # the eigenvalue vals[k] sits at some eigenspace index; its prob is 1
        j = index_of(A, vals[k])
        assert _approx(p[j], 1.0)
        assert _approx(expectation(ek, A), vals[k])
        assert standard_deviation(ek, A) < 1e-8


def test_collapse_idempotent():
    """After measuring A and getting a_n, the state collapses so a REPEAT
    measurement returns a_n with probability 1 (Griffiths 3.4): measurement is
    reproducible / idempotent."""
    rng = np.random.default_rng(8)
    A = _rand_hermitian(5, rng)
    psi = _rand_state(5, rng)
    spaces = eigenspaces(A)
    _, probs = outcome_probabilities(psi, A)
    for n in range(len(spaces)):
        if probs[n] < 1e-6:
            continue
        s = collapse(psi, A, n)
        _, p2 = outcome_probabilities(s, A)
        assert _approx(p2[n], 1.0)                  # certain on the same outcome
        assert _approx(expectation(s, A), spaces[n][0])  # = the eigenvalue a_n
        assert standard_deviation(s, A) < 1e-7


# --- 5. compatible vs incompatible observables -------------------------------

def test_compatible_no_disturbance():
    """Commuting observables share an eigenbasis: measuring A, then a compatible
    B, then A again recovers the ORIGINAL A-value with certainty -- no
    disturbance (Griffiths 3.5.1: compatible observables admit simultaneous
    eigenstates)."""
    rng = np.random.default_rng(9)
    # A, B Hermitian, diagonal in the SAME random basis with distinct spectra
    Q = np.linalg.qr(_rand_hermitian(4, rng) + 4 * np.eye(4))[0]
    A = Q @ np.diag([1.0, 2.0, 3.0, 4.0]) @ Q.conj().T
    B = Q @ np.diag([10.0, 20.0, 30.0, 40.0]) @ Q.conj().T
    assert commute(A, B)
    psi = _rand_state(4, rng)
    _, pa = outcome_probabilities(psi, A)
    k = int(np.argmax(pa))
    a1, sA = measure(psi, A, outcome=k)             # collapse to an A-eigenstate
    _, pb = outcome_probabilities(sA, B)
    assert _approx(float(pb.max()), 1.0)            # B is determinate on sA
    _, sB = measure(sA, B, outcome=int(np.argmax(pb)))
    _, pa2 = outcome_probabilities(sB, A)
    k2 = int(np.argmax(pa2))
    assert _approx(float(pa2[k2]), 1.0)             # A still determinate ...
    assert _approx(eigenspaces(A)[k2][0], a1)       # ... and the SAME value


def test_incompatible_randomized():
    """Non-commuting observables DO disturb: prepare |+x| (sigma_x = +1 for
    sure), measure sigma_z in between, then sigma_x again -- the once-certain +1
    is now 50/50 (Griffiths 3.5.1: incompatible observables share no eigenbasis)."""
    plus_x = spin_state(math.pi / 2, 0.0)
    i_xplus = index_of(sigma_x, +1.0)
    i_xminus = index_of(sigma_x, -1.0)
    _, px = outcome_probabilities(plus_x, sigma_x)
    assert _approx(px[i_xplus], 1.0)                # sigma_x is determinate: +1
    a1, s1 = measure(plus_x, sigma_x, outcome=i_xplus)
    assert _approx(float(a1), 1.0)
    # intervening sigma_z measurement collapses to |0>
    _, s2 = measure(s1, sigma_z, outcome=index_of(sigma_z, +1.0))
    # re-measure sigma_x: the original +1 outcome is no longer certain
    _, px2 = outcome_probabilities(s2, sigma_x)
    assert _approx(px2[i_xplus], 0.5)
    assert _approx(px2[i_xminus], 0.5)


def test_spin_born_probabilities():
    """Concrete spin Born probabilities: |+x> gives 50/50 on sigma_z and |0>
    gives 50/50 on sigma_x -- mutually unbiased bases."""
    plus_x = spin_state(math.pi / 2, 0.0)
    _, pz = outcome_probabilities(plus_x, sigma_z)
    assert _approx(pz[0], 0.5) and _approx(pz[1], 0.5)
    up_z = spin_state(0.0)
    _, px = outcome_probabilities(up_z, sigma_x)
    assert _approx(px[0], 0.5) and _approx(px[1], 0.5)
    # the spin_operator helper has eigenvalues +/- hbar/2
    vals, _ = eigensystem(spin_operator(1, 1, 0))
    assert np.allclose(np.sort(vals), [-0.5 * HBAR, 0.5 * HBAR])


def test_measure_sampling_frequencies():
    """Operationally: sampling measure() many times reproduces the Born
    probabilities. sigma_x on |0> should give +1 about half the time."""
    rng = np.random.default_rng(2024)
    up_z = spin_state(0.0)
    N = 10000
    plus = 0
    for _ in range(N):
        val, _ = measure(up_z, sigma_x, rng=rng)
        if val > 0:
            plus += 1
    freq = plus / N
    assert abs(freq - 0.5) < 0.03                   # ~4 sigma band for N=10^4


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
