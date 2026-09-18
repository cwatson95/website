"""Tests for QM-14 identical particles -- every claim checked against a closed
form (the symmetry eigenvalue +-1, the Pauli zero vector, the sqrt(N!)
normalization of the Slater determinant, and the analytic exchange-force numbers
of Griffiths Problems 5.6 and 5.7).

Run directly:   python3 test_identical.py     (-> "All N tests passed.")
Or with pytest: pytest test_identical.py
"""
import numpy as np

from identical import (
    tensor, swap_operator, apply_pair_swap, levi_civita_sign,
    symmetrize, antisymmetrize,
    slater_determinant,
    well_state, ho_state, position_moments, exchange_dx2,
    spin_up, spin_down, singlet, triplet,
    norm,
)


def _close(a, b, tol=1e-9):
    return np.allclose(np.asarray(a), np.asarray(b), atol=tol, rtol=0.0)


# --- 1. the exchange operator P_12 -------------------------------------------

def test_swap_operator_involution_and_eigenvalues():
    """P_12^2 = I, so the eigenvalues of P_12 are exactly +-1 -- the symmetric
    and antisymmetric subspaces (Griffiths Sec. 5.1.4, p.264)."""
    for d in (2, 3, 4):
        P = swap_operator(d)
        assert _close(P @ P, np.eye(d * d))            # involution
        assert _close(P, P.T)                          # symmetric (Hermitian)
        w = np.linalg.eigvalsh(P)
        assert np.all(np.isclose(np.abs(w), 1.0))      # eigenvalues are +-1


def test_swap_acts_as_factor_exchange():
    """P_12 |a>(x)|b> = |b>(x)|a>  (the defining action, Eq. 5.30, p.264)."""
    a = np.array([1.0, 2.0, -1.0])
    b = np.array([0.0, 1.0, 3.0])
    P = swap_operator(3)
    assert _close(P @ tensor(a, b), tensor(b, a))


# --- 2. bosons (symmetric) vs fermions (antisymmetric) -----------------------

def test_boson_state_is_symmetric_and_normalized():
    """The boson combination is a +1 eigenstate of P_12 and is normalized
    (Griffiths Eq. 5.17, +; Sec. 5.1.1, p.256)."""
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])           # orthonormal -> norm factor 1/sqrt2
    P = swap_operator(3)
    psi = symmetrize(a, b)
    assert abs(norm(psi) - 1.0) < 1e-12
    assert _close(P @ psi, +psi)                       # P_12 psi = +psi
    # for orthonormal a,b the normalization is exactly 1/sqrt(2):
    assert _close(psi, (tensor(a, b) + tensor(b, a)) / np.sqrt(2.0))


def test_fermion_state_is_antisymmetric_and_normalized():
    """The fermion combination is a -1 eigenstate of P_12 and is normalized
    (Griffiths Eq. 5.17, -; Sec. 5.1.1, p.256)."""
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])
    P = swap_operator(3)
    psi = antisymmetrize(a, b)
    assert abs(norm(psi) - 1.0) < 1e-12
    assert _close(P @ psi, -psi)                       # P_12 psi = -psi
    assert _close(psi, (tensor(a, b) - tensor(b, a)) / np.sqrt(2.0))


def test_pauli_exclusion_two_identical_orbitals():
    """PAULI EXCLUSION (Griffiths p.256): the antisymmetric combination of two
    IDENTICAL one-particle states is the zero vector -- "we are left with no
    wave function at all." """
    a = np.array([0.3, 0.4, -0.5, 0.7])
    a = a / norm(a)
    psi = antisymmetrize(a, a)
    assert _close(psi, np.zeros_like(psi))             # identically zero
    assert norm(psi) < 1e-15


def test_bosons_may_share_a_state():
    """Contrast with Pauli: the SYMMETRIC combination of two identical states is
    nonzero and normalized (two bosons can occupy the same state)."""
    a = np.array([0.3, 0.4, -0.5, 0.7])
    a = a / norm(a)
    psi = symmetrize(a, a)
    assert abs(norm(psi) - 1.0) < 1e-12
    assert _close(psi, tensor(a, a))                   # just |a>(x)|a>


def test_general_normalization_nonorthogonal():
    """For NON-orthogonal (but normalized) orbitals with overlap s = <a|b>, the
    norms are sqrt(2(1 +- |s|^2)); the code divides by them, so the returned
    states are unit-norm and still exact P_12 eigenstates (+-1)."""
    a = np.array([1.0, 0.0])
    b = np.array([1.0, 1.0]) / np.sqrt(2.0)            # <a|b> = 1/sqrt2, |s|^2=1/2
    s2 = abs(np.vdot(a, b)) ** 2
    raw_sym = tensor(a, b) + tensor(b, a)
    raw_anti = tensor(a, b) - tensor(b, a)
    assert abs(norm(raw_sym) - np.sqrt(2.0 * (1.0 + s2))) < 1e-12
    assert abs(norm(raw_anti) - np.sqrt(2.0 * (1.0 - s2))) < 1e-12
    P = swap_operator(2)
    assert abs(norm(symmetrize(a, b)) - 1.0) < 1e-12
    assert abs(norm(antisymmetrize(a, b)) - 1.0) < 1e-12
    assert _close(P @ symmetrize(a, b), +symmetrize(a, b))
    assert _close(P @ antisymmetrize(a, b), -antisymmetrize(a, b))


# --- 3. the Slater determinant: N fermions -----------------------------------

def test_levi_civita_sign():
    """Parity of permutations: identity +1, a single swap -1, a 3-cycle +1."""
    assert levi_civita_sign((0, 1, 2)) == 1
    assert levi_civita_sign((1, 0, 2)) == -1
    assert levi_civita_sign((2, 0, 1)) == 1            # 3-cycle = two swaps


def test_slater_two_particles_equals_antisymmetrize():
    """For N=2 the Slater determinant reduces to the fermion pair state."""
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])
    assert _close(slater_determinant([a, b]), antisymmetrize(a, b))


def test_slater_antisymmetric_under_any_pair_swap():
    """The Slater determinant is totally antisymmetric: swapping ANY two
    particles flips the sign (Griffiths Eq. 5.34, p.264; Problem 5.8, p.262)."""
    # N = 3 in C^3
    e = np.eye(3)
    Psi = slater_determinant([e[0], e[1], e[2]])
    for (p, q) in [(0, 1), (0, 2), (1, 2)]:
        assert _close(apply_pair_swap(Psi, 3, 3, p, q), -Psi)
    # N = 4 in C^4 -- include a non-adjacent pair (0,3)
    e4 = np.eye(4)
    Psi4 = slater_determinant([e4[0], e4[1], e4[2], e4[3]])
    for (p, q) in [(0, 1), (1, 2), (2, 3), (0, 3), (1, 3)]:
        assert _close(apply_pair_swap(Psi4, 4, 4, p, q), -Psi4)


def test_slater_vanishes_if_two_orbitals_coincide():
    """A Slater determinant with two equal rows is zero -- Pauli for N fermions."""
    e = np.eye(3)
    Psi = slater_determinant([e[0], e[1], e[0]])        # orbital 0 repeated
    assert norm(Psi) < 1e-15
    assert _close(Psi, np.zeros_like(Psi))


def test_slater_normalization_is_sqrt_N_factorial():
    """For ORTHONORMAL orbitals the raw antisymmetric sum has norm sqrt(N!), so
    dividing by it gives a unit state (the 1/sqrt(N!) prefactor)."""
    import math
    for N in (2, 3, 4):
        e = np.eye(N)
        raw = slater_determinant([e[i] for i in range(N)], normalize_state=False)
        assert abs(norm(raw) - np.sqrt(math.factorial(N))) < 1e-9
        unit = slater_determinant([e[i] for i in range(N)])
        assert abs(norm(unit) - 1.0) < 1e-12


def test_slater_with_general_orbitals_is_antisymmetric():
    """Antisymmetry holds for arbitrary (here random, linearly independent)
    orbitals, not just basis vectors."""
    rng = np.random.default_rng(0)
    orbs = [rng.standard_normal(3) for _ in range(3)]
    Psi = slater_determinant(orbs)
    for (p, q) in [(0, 1), (0, 2), (1, 2)]:
        assert _close(apply_pair_swap(Psi, 3, 3, p, q), -Psi)


# --- 4. one-particle orbitals on the grid (so the quadrature is trustworthy) --

def test_orbitals_orthonormal_on_grid():
    """The infinite-well and HO grid orbitals used below are orthonormal under
    the trapezoid rule, so the exchange-force integrals are reliable."""
    f = getattr(np, "trapezoid", None) or np.trapz
    x = np.linspace(0.0, 1.0, 4001)
    w1, w2 = well_state(1, x), well_state(2, x)
    assert abs(f(w1 * w1, x) - 1.0) < 1e-4
    assert abs(f(w2 * w2, x) - 1.0) < 1e-4
    assert abs(f(w1 * w2, x)) < 1e-4                   # orthogonal
    xh = np.linspace(-8.0, 8.0, 4001)
    h0, h1 = ho_state(0, xh), ho_state(1, xh)
    assert abs(f(h0 * h0, xh) - 1.0) < 1e-4
    assert abs(f(h1 * h1, xh) - 1.0) < 1e-4
    assert abs(f(h0 * h1, xh)) < 1e-4


# --- 5. the exchange force ----------------------------------------------------

def test_exchange_force_ordering_infinite_well():
    """The headline result (Griffiths Eq. 5.25, p.260): for OVERLAPPING orbitals,
    bosons end up closer and fermions farther apart than distinguishable
    particles:  <(Dx)^2>_boson  <  distinguishable  <  <(Dx)^2>_fermion."""
    x = np.linspace(0.0, 1.0, 4001)
    r = exchange_dx2(well_state(1, x), well_state(2, x), x)
    assert r["boson"] < r["distinguishable"] < r["fermion"]
    assert r["exchange_term"] > 0.0


def test_exchange_force_infinite_well_closed_form():
    """Closed form for the infinite well, n=1 & n=2, L=1 (Griffiths Problem 5.6):
        <x>_12        = -16/(9 pi^2)
        distinguishable<(Dx)^2> = 1/6 - 5/(8 pi^2)
        exchange term 2|<x>_12|^2 = 512/(81 pi^4)."""
    x = np.linspace(0.0, 1.0, 8001)
    m = position_moments(well_state(1, x), well_state(2, x), x)
    assert abs(m["x_a"] - 0.5) < 1e-4                  # <x>_n = L/2
    assert abs(m["x_b"] - 0.5) < 1e-4
    assert abs(m["x2_a"] - (1.0 / 3 - 1.0 / (2 * np.pi ** 2))) < 1e-4
    assert abs(m["x2_b"] - (1.0 / 3 - 1.0 / (8 * np.pi ** 2))) < 1e-4
    assert abs(m["x_ab"].real - (-16.0 / (9 * np.pi ** 2))) < 1e-4
    assert abs(m["x_ab"].imag) < 1e-12                 # real orbitals
    r = exchange_dx2(well_state(1, x), well_state(2, x), x)
    assert abs(r["distinguishable"] - (1.0 / 6 - 5.0 / (8 * np.pi ** 2))) < 1e-4
    assert abs(r["exchange_term"] - 512.0 / (81 * np.pi ** 4)) < 1e-4


def test_exchange_force_harmonic_oscillator_closed_form():
    """Closed form for the HO, ground + first excited (Griffiths Problem 5.7),
    natural units hbar=m=omega=1:
        <x>_a=<x>_b=0,  <x^2>_0=1/2, <x^2>_1=3/2,  <x>_01 = 1/sqrt(2),
        distinguishable=2, boson=1, fermion=3."""
    x = np.linspace(-9.0, 9.0, 8001)
    m = position_moments(ho_state(0, x), ho_state(1, x), x)
    assert abs(m["x_a"]) < 1e-6 and abs(m["x_b"]) < 1e-6
    assert abs(m["x2_a"] - 0.5) < 1e-5
    assert abs(m["x2_b"] - 1.5) < 1e-5
    assert abs(abs(m["x_ab"]) - 1.0 / np.sqrt(2.0)) < 1e-5
    r = exchange_dx2(ho_state(0, x), ho_state(1, x), x)
    assert abs(r["distinguishable"] - 2.0) < 1e-5
    assert abs(r["boson"] - 1.0) < 1e-5
    assert abs(r["fermion"] - 3.0) < 1e-5


def test_exchange_term_is_pm_two_overlap_squared():
    """The whole identical-particle effect is the single exchange term
    -+2|<x>_ab|^2 (Griffiths Eq. 5.26): boson = distinguishable - 2|<x>_ab|^2,
    fermion = distinguishable + 2|<x>_ab|^2 (exactly)."""
    x = np.linspace(0.0, 1.0, 4001)
    r = exchange_dx2(well_state(1, x), well_state(2, x), x)
    assert abs(r["boson"] - (r["distinguishable"] - r["exchange_term"])) < 1e-12
    assert abs(r["fermion"] - (r["distinguishable"] + r["exchange_term"])) < 1e-12
    assert abs(r["exchange_term"] - 2.0 * abs(r["x_ab"]) ** 2) < 1e-12


def test_no_exchange_force_without_overlap():
    """If the orbitals don't overlap (<x>_ab = 0) the exchange term vanishes and
    all three cases coincide -- "an electron in Chicago and an electron in
    Seattle" (Griffiths p.260): non-overlapping electrons act distinguishable."""
    x = np.linspace(0.0, 3.0, 9001)
    a = np.where(x <= 1.0, well_state(1, x, L=1.0), 0.0)          # lives on [0,1]
    b = np.where((x >= 2.0) & (x <= 3.0), well_state(1, x - 2.0, L=1.0), 0.0)  # [2,3]
    r = exchange_dx2(a, b, x)
    assert abs(r["x_ab"]) < 1e-6
    assert r["exchange_term"] < 1e-10
    assert abs(r["boson"] - r["distinguishable"]) < 1e-8
    assert abs(r["fermion"] - r["distinguishable"]) < 1e-8


# --- 6. spin & the helium ground state (spin-statistics capstone) ------------

def test_spin_singlet_antisymmetric_triplet_symmetric():
    """Singlet (|ud>-|du>)/sqrt2 is antisymmetric (P=-1); the three triplet
    states are symmetric (P=+1) (Griffiths Sec. 5.1.3, p.263)."""
    P = swap_operator(2)
    s = singlet()
    assert abs(norm(s) - 1.0) < 1e-12
    assert _close(P @ s, -s)                           # antisymmetric
    assert _close(s, antisymmetrize(spin_up(), spin_down()))
    for t in triplet():
        assert _close(P @ t, +t)                       # symmetric


def test_helium_ground_state_requires_singlet():
    """Helium 1s^2 ground state (Griffiths Sec. 5.1.3, p.263): both electrons in
    the SAME (symmetric) spatial orbital, so the spin state must be the
    ANTISYMMETRIC singlet -- "both spin up" (antisymmetrize of identical spins)
    is forbidden by Pauli (zero vector).  The product of the spatial (+1) and
    spin (-1) exchange eigenvalues makes the FULL state antisymmetric (-1)."""
    # both electrons in spatial 1s (modelled as level 0 of a 2-level space):
    o = np.array([1.0, 0.0])
    spatial = tensor(o, o)
    Pspace = swap_operator(2)
    spatial_eig = float(np.vdot(spatial, Pspace @ spatial).real)
    assert abs(spatial_eig - (+1.0)) < 1e-12           # symmetric spatial part
    # allowed spin state = singlet (antisymmetric); "both up" is forbidden:
    spin = singlet()
    spin_eig = float(np.vdot(spin, swap_operator(2) @ spin).real)
    assert abs(spin_eig - (-1.0)) < 1e-12
    assert norm(antisymmetrize(spin_up(), spin_up())) < 1e-15   # both-up forbidden
    # full two-electron state is antisymmetric under simultaneous exchange:
    assert abs(spatial_eig * spin_eig - (-1.0)) < 1e-12


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
