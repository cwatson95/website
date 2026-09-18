"""Tests for QM-07 uncertainty -- every bound is checked against a closed form.

Run directly:   python3 test_uncertainty.py        (-> "All N tests passed.")
Or with pytest: pytest test_uncertainty.py

Natural units hbar = m = 1, so the position-momentum bound is sigma_x sigma_p
>= 1/2 and the spin bound is sigma_Sx sigma_Sy >= (1/2)|<Sz>|.
"""
import math
import numpy as np

from uncertainty import (
    HBAR, M,
    grid, normalize, gaussian_packet, ho_eigenstate,
    apply_p, mean_x, mean_p, sigma_x, sigma_p, uncertainty_product,
    spin_ops, expval, variance, std, commutator, generalized_bound,
    inner, schwarz_gap, schwarz_residual_identity,
    split_step_evolve, classical_sho,
)

HALF = HBAR / 2.0


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- position-momentum uncertainty ------------------------------------------

def test_normalize():
    """normalize() makes integral |psi|^2 dx = 1."""
    x, dx = grid(40.0, 2048)
    psi = normalize(gaussian_packet(x, sigma=1.7) * 3.0, dx)
    assert _approx(np.sum(np.abs(psi) ** 2) * dx, 1.0, abs_=1e-12)


def test_momentum_operator_planewave():
    """p-hat exp(i k0 x) = hbar k0 exp(i k0 x): the spectral operator is right."""
    x, dx = grid(2.0 * math.pi, 256)          # k0 must be an integer on this box
    k0 = 5.0
    psi = np.exp(1j * k0 * x)
    assert np.allclose(apply_p(psi, dx), HBAR * k0 * psi, atol=1e-10)


def test_gaussian_components():
    """A Gaussian has the analytic moments <x>=x0, <p>=p0, sigma_x=sigma,
    sigma_p=hbar/(2 sigma)."""
    x, dx = grid(40.0, 2048)
    x0, sig, p0 = 1.5, 1.3, 0.8
    g = gaussian_packet(x, x0=x0, sigma=sig, p0=p0)
    assert _approx(mean_x(g, x, dx), x0, abs_=1e-6)
    assert _approx(mean_p(g, dx), p0, abs_=1e-6)
    assert _approx(sigma_x(g, x, dx), sig, rel=1e-5)
    assert _approx(sigma_p(g, dx), HBAR / (2.0 * sig), rel=1e-5)


def test_gaussian_saturates():
    """The Gaussian is the minimum-uncertainty packet: sigma_x sigma_p = hbar/2
    for every width and boost (Griffiths 3e Sec.3.5.2)."""
    x, dx = grid(60.0, 4096)
    for sig in (0.6, 1.0, 2.5):
        for p0 in (0.0, 1.3):
            g = gaussian_packet(x, x0=0.4, sigma=sig, p0=p0)
            assert _approx(uncertainty_product(g, x, dx), HALF, abs_=1e-5)


def test_ho_eigenstates_product():
    """HO eigenstate n has sigma_x sigma_p = (n + 1/2) hbar exactly: the ground
    state saturates the bound, the excited states exceed it (cross-link ~QM-09)."""
    x, dx = grid(40.0, 2048)
    for n in range(4):
        prod = uncertainty_product(ho_eigenstate(x, n), x, dx)
        assert _approx(prod, (n + 0.5) * HBAR, rel=1e-5)
    # ground state == bound, first excited strictly above it
    assert _approx(uncertainty_product(ho_eigenstate(x, 0), x, dx), HALF, abs_=1e-6)
    assert uncertainty_product(ho_eigenstate(x, 1), x, dx) > HALF + 0.5


def test_uncertainty_lower_bound_holds():
    """sigma_x sigma_p >= hbar/2 for non-Gaussian states, and is strictly larger
    for them (a Schroedinger-cat in x and a two-momentum cat)."""
    x, dx = grid(60.0, 4096)
    cat_x = gaussian_packet(x, x0=-3.0, sigma=1.0) + gaussian_packet(x, x0=3.0, sigma=1.0)
    cat_p = gaussian_packet(x, sigma=1.0, p0=-2.0) + gaussian_packet(x, sigma=1.0, p0=2.0)
    skew = gaussian_packet(x, x0=0.0, sigma=1.0) + 0.5 * gaussian_packet(x, x0=2.0, sigma=0.7)
    for psi in (cat_x, cat_p, skew):
        assert uncertainty_product(psi, x, dx) >= HALF - 1e-9       # the law
        assert uncertainty_product(psi, x, dx) > HALF * (1.0 + 1e-3)  # strictly, non-Gaussian


# --- generalized (matrix / spin) uncertainty --------------------------------

def test_pauli_commutators():
    """Spin-1/2 closes the algebra [Sx,Sy]=i hbar Sz (and cyclic) -- the nonzero
    RHS of the generalized bound (see ~QM-05)."""
    Sx, Sy, Sz = spin_ops()
    assert np.allclose(commutator(Sx, Sy), 1j * HBAR * Sz)
    assert np.allclose(commutator(Sy, Sz), 1j * HBAR * Sx)
    assert np.allclose(commutator(Sz, Sx), 1j * HBAR * Sy)
    assert not np.allclose(commutator(Sx, Sy), 0.0)     # incompatible observables


def test_eigenstate_zero_variance():
    """An eigenstate has zero spread in that observable: sigma_Sz(|up_z>) = 0."""
    Sx, Sy, Sz = spin_ops()
    up = [1.0, 0.0]
    assert _approx(std(Sz, up), 0.0, abs_=1e-12)
    assert _approx(expval(Sz, up).real, HALF, abs_=1e-12)   # eigenvalue +hbar/2


def test_spin_bound_holds():
    """sigma_A sigma_B >= (1/2)|<[A,B]>| for many random complex states: spin-1/2
    (Sx,Sy) and random 3-level Hermitian pairs."""
    Sx, Sy, Sz = spin_ops()
    rng = np.random.default_rng(12345)
    for _ in range(500):
        v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        assert std(Sx, v) * std(Sy, v) >= generalized_bound(Sx, Sy, v) - 1e-12
    for _ in range(500):
        A = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
        B = rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))
        A = A + A.conj().T                              # Hermitian
        B = B + B.conj().T
        v = rng.standard_normal(3) + 1j * rng.standard_normal(3)
        assert std(A, v) * std(B, v) >= generalized_bound(A, B, v) - 1e-12


def test_spin_saturation_upz():
    """|up_z> saturates the spin bound: sigma_Sx sigma_Sy = (1/2)|<[Sx,Sy]>|
    = (hbar/2)|<Sz>| = hbar^2/4."""
    Sx, Sy, Sz = spin_ops()
    up = [1.0, 0.0]
    prod = std(Sx, up) * std(Sy, up)
    bound = generalized_bound(Sx, Sy, up)
    assert _approx(prod, bound, abs_=1e-12)
    assert _approx(bound, 0.5 * HBAR * abs(expval(Sz, up)), abs_=1e-12)
    assert _approx(prod, HBAR ** 2 / 4.0, abs_=1e-12)


def test_spin_strict_case():
    """An off-Bloch-plane (complex) state makes the Robertson bound strict:
    sigma_Sx sigma_Sy > (1/2)|<[Sx,Sy]>|."""
    Sx, Sy, Sz = spin_ops()
    st = [math.cos(0.5), math.sin(0.5) * np.exp(0.7j)]
    assert std(Sx, st) * std(Sy, st) > generalized_bound(Sx, Sy, st) + 1e-3


def test_bound_zero_for_commuting():
    """Commuting (compatible) observables have a vanishing bound: their spreads
    may both be nonzero, yet sigma_A sigma_B >= 0 is the only constraint."""
    A = np.diag([1.0, 2.0, 3.0]).astype(complex)
    B = np.diag([5.0, 7.0, 11.0]).astype(complex)
    assert np.allclose(commutator(A, B), 0.0)
    v = [1.0, 1.0, 1.0]
    assert _approx(generalized_bound(A, B, v), 0.0, abs_=1e-12)
    assert std(A, v) > 0.0 and std(B, v) > 0.0          # still spread out
    assert std(A, v) * std(B, v) >= generalized_bound(A, B, v) - 1e-12


# --- the Schwarz inequality: every step of the derivation --------------------

def test_schwarz_inequality_random():
    """<f|f><g|g> >= |<f|g>|^2 (Griffiths 3e Eq. 3.7 / A.27) for random complex
    kets of several dimensions AND for grid wavefunctions."""
    rng = np.random.default_rng(7)
    for n in (2, 3, 5):
        for _ in range(200):
            f = rng.standard_normal(n) + 1j * rng.standard_normal(n)
            g = rng.standard_normal(n) + 1j * rng.standard_normal(n)
            assert schwarz_gap(f, g) >= -1e-12
    x, dx = grid(40.0, 512)
    f = gaussian_packet(x, x0=-1.0, sigma=0.8, p0=0.3)
    g = gaussian_packet(x, x0=2.0, sigma=1.7, p0=-1.1)
    assert schwarz_gap(f, g, dx) >= -1e-12


def test_schwarz_projection_identity():
    """Steps 3-4 of the derivation (notes Sec.2.1): with h = g - (<f|g>/<f|f>) f,
    (i) <f|h> = 0 (h is the part of g orthogonal to f), and
    (ii) <f|f><g|g> - |<f|g>|^2 = <f|f><h|h> EXACTLY -- so the Schwarz
    inequality is nothing more than <h|h> >= 0."""
    rng = np.random.default_rng(11)
    for _ in range(300):
        f = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        g = rng.standard_normal(4) + 1j * rng.standard_normal(4)
        gap, ffhh, fh = schwarz_residual_identity(f, g)
        assert abs(fh) < 1e-10                    # h is orthogonal to f
        assert _approx(gap, ffhh, rel=1e-9, abs_=1e-9)   # the identity
        assert ffhh >= -1e-12                     # hence the inequality


def test_schwarz_saturation():
    """Step 5's equality condition: g = c f (any complex c) closes the gap to
    zero; adding an orthogonal piece w reopens it by exactly <f|f><w|w>."""
    rng = np.random.default_rng(23)
    f = rng.standard_normal(3) + 1j * rng.standard_normal(3)
    c = 2.0 - 0.7j
    assert _approx(schwarz_gap(f, c * f), 0.0, abs_=1e-9)
    e = rng.standard_normal(3) + 1j * rng.standard_normal(3)
    w = e - (inner(f, e) / inner(f, f).real) * f          # <f|w> = 0
    ff, ww = inner(f, f).real, inner(w, w).real
    assert _approx(schwarz_gap(f, c * f + w), ff * ww, rel=1e-9, abs_=1e-9)
    assert schwarz_gap(f, c * f + w) > 1e-6               # strictly above


def test_uncertainty_chain_stepwise():
    """The full Sec.2.2 proof chain, one link at a time, on random spin states:
    sigma_A^2 sigma_B^2 = <f|f><g|g>      (Step 1: variances are norms)
                       >= |<f|g>|^2       (Step 2: Schwarz)
                       >= (Im<f|g>)^2     (Step 3: drop Re z)
                        = (<[A,B]>/2i)^2  (Steps 4-6: the commutator)."""
    Sx, Sy, Sz = spin_ops()
    eye = np.eye(2, dtype=complex)
    rng = np.random.default_rng(31)
    for _ in range(300):
        v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        v = v / math.sqrt(float(np.real(np.vdot(v, v))))
        a = expval(Sx, v).real
        b = expval(Sy, v).real
        f = (Sx - a * eye) @ v
        g = (Sy - b * eye) @ v
        ff, gg, fg = inner(f, f).real, inner(g, g).real, inner(f, g)
        # Step 1: sigma^2 = <f|f> (hermiticity moves one deviation factor left)
        assert _approx(variance(Sx, v), ff, abs_=1e-12)
        assert _approx(variance(Sy, v), gg, abs_=1e-12)
        # Step 2: the Schwarz inequality
        assert ff * gg >= abs(fg) ** 2 - 1e-12
        # Step 3: |z|^2 >= (Im z)^2
        assert abs(fg) ** 2 >= fg.imag ** 2 - 1e-12
        # Steps 4-5: <f|g> - <g|f> = <[A,B]>, i.e. Im<f|g> = <[A,B]>/2i
        comm = expval(commutator(Sx, Sy), v)
        assert abs(comm.real) < 1e-12             # anti-Hermitian: pure imaginary
        assert _approx(fg.imag, (comm / 2j).real, abs_=1e-12)
        # Step 6 chained: the Robertson bound itself
        assert std(Sx, v) * std(Sy, v) >= generalized_bound(Sx, Sy, v) - 1e-12


# --- Ehrenfest's theorem -----------------------------------------------------

def test_ehrenfest_free():
    """Free particle: d<x>/dt = <p>/m, <p> conserved, mean force <-V'> = 0
    (Griffiths 3e Sec.1.5)."""
    x, dx = grid(160.0, 2048)
    psi = gaussian_packet(x, x0=0.0, sigma=2.0, p0=1.5)
    t, xs, ps, Fs, _ = split_step_evolve(psi, x, V=0.0, dt=0.02, nsteps=120)
    dxdt = np.gradient(xs, t)
    s = slice(2, -2)                                     # interior (skip one-sided ends)
    assert np.max(np.abs(dxdt[s] - ps[s] / M)) < 1e-4   # d<x>/dt = <p>/m
    assert (ps.max() - ps.min()) < 1e-9                 # momentum conserved
    assert np.max(np.abs(Fs)) < 1e-12                   # no force


def test_ehrenfest_harmonic():
    """Harmonic well: both Ehrenfest rates hold along the whole trajectory --
    d<x>/dt = <p>/m and d<p>/dt = -<V'(x)>."""
    x, dx = grid(40.0, 1024)
    omega, x0, p0 = 1.0, 3.0, 0.5
    psi = gaussian_packet(x, x0=x0, sigma=1.0, p0=p0)
    V = 0.5 * M * omega ** 2 * x ** 2
    dt = 0.01
    nsteps = int(2.0 * math.pi / dt)                    # one classical period
    t, xs, ps, Fs, _ = split_step_evolve(
        psi, x, V=V, dt=dt, nsteps=nsteps, dVdx=lambda xx: M * omega ** 2 * xx)
    dxdt = np.gradient(xs, t)
    dpdt = np.gradient(ps, t)
    s = slice(2, -2)
    assert np.max(np.abs(dxdt[s] - ps[s] / M)) < 1e-4          # d<x>/dt = <p>/m
    assert np.max(np.abs(dpdt[s] - Fs[s])) < 2e-3             # d<p>/dt = -<V'(x)>


def test_sho_classical_limit():
    """The harmonic potential is the exact classical limit: <x>(t) traces
    x0 cos(wt) + (p0/m w) sin(wt) (the SHO oscillation)."""
    x, dx = grid(40.0, 1024)
    omega, x0, p0 = 1.0, 3.0, 0.5
    psi = gaussian_packet(x, x0=x0, sigma=1.0, p0=p0)
    V = 0.5 * M * omega ** 2 * x ** 2
    dt = 0.01
    nsteps = int(2.0 * math.pi / dt)
    t, xs, ps, Fs, _ = split_step_evolve(
        psi, x, V=V, dt=dt, nsteps=nsteps, dVdx=lambda xx: M * omega ** 2 * xx)
    assert np.max(np.abs(xs - classical_sho(t, x0, p0, omega))) < 1e-3


def test_norm_conserved():
    """The split-step propagator is unitary: norm is preserved to machine
    precision."""
    x, dx = grid(40.0, 1024)
    psi = gaussian_packet(x, x0=3.0, sigma=1.0, p0=0.5)
    V = 0.5 * x ** 2
    _, _, _, _, psf = split_step_evolve(psi, x, V=V, dt=0.01, nsteps=300)
    assert _approx(np.sum(np.abs(psf) ** 2) * dx, 1.0, abs_=1e-10)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
