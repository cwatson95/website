"""Tests for QM-19 propagators & path integrals -- every formula checked against
a closed form, an independent integrator, or an imported MA-14 result.

Run directly:   python3 test_propagator.py        (-> "All N tests passed.")
Or with pytest: pytest test_propagator.py

Natural units hbar = m = 1.  The real-time oscillatory integrals (delta limit,
composition, sum rule) carry ~1e-3 truncation error because the kernel has
CONSTANT modulus and never damps -- this is the genuine difficulty of real-time
path integrals, reflected honestly in the tolerances.
"""
import numpy as np

import propagator as P
# imported MA-14 Green's function (verified API) -- used in the resolvent link test
from greens_function import green_series, green_dirichlet


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * (1.0 + abs(b))


# --- 1. free propagator: modulus, and phase = classical action ----------------

def test_free_propagator_closed_form():
    x, xp, t = 1.0, -0.5, 0.8
    K = complex(P.free_propagator(np.array([x]), xp, t)[0])
    # |K0| = 1/sqrt(2 pi hbar t / m)
    assert _approx(abs(K), 1.0 / np.sqrt(2.0 * np.pi * t), tol=1e-12)
    # the EXPONENT's phase is exactly the classical action S_cl = m (x-x')^2 / 2t,
    # so K0 = prefactor * exp(i S_cl / hbar) with prefactor = exp(-i pi/4)/sqrt(2 pi t)
    pref = np.sqrt(1.0 / (2j * np.pi * t))
    Scl = P.classical_action_free(x, xp, t)
    assert _approx(K, pref * np.exp(1j * Scl), tol=1e-12)
    # the prefactor contributes the Maslov phase -pi/4: arg(K0) = S_cl - pi/4
    assert _approx((np.angle(K) - (Scl - np.pi / 4) + np.pi) % (2 * np.pi) - np.pi, 0.0, tol=1e-9)


# --- 2. initial condition: K0 -> delta(x-x') as t -> 0 ------------------------

def test_free_propagator_delta_limit():
    """integral K0(x,t;x') g(x') dx' -> g(x) as t -> 0 (K0 is a nascent delta)."""
    g = lambda xp: np.exp(-xp ** 2 / 2.0) / np.sqrt(2 * np.pi)
    xq = 0.4
    xp = np.linspace(-30, 30, 200001)
    dx = xp[1] - xp[0]
    errs = []
    for t in (0.2, 0.1, 0.05, 0.02):
        val = np.sum(P.free_propagator(xq, xp, t) * g(xp)) * dx
        errs.append(abs(val - g(xq)))
    assert errs[0] > errs[1] > errs[2] > errs[3]      # converging to g(xq)
    assert errs[-1] < 1e-2


# --- 3. composition / semigroup: K0 . K0 = K0 --------------------------------

def test_free_propagator_composition():
    """integral K0(x,t2;y) K0(y,t1;x') dy = K0(x,t1+t2;x')  (semigroup law)."""
    x, xp, t1, t2 = 1.0, -0.5, 0.5, 0.3
    y = np.linspace(-50, 50, 200001)
    dy = y[1] - y[0]
    conv = np.sum(P.free_propagator(x, y, t2) * P.free_propagator(y, xp, t1)) * dy
    exact = complex(P.free_propagator(np.array([x]), xp, t1 + t2)[0])
    assert abs(conv - exact) < 1e-2


# --- 4. unitarity: sum rule + norm conservation ------------------------------

def test_free_propagator_unitarity():
    # sum rule: integral K0(x,t;x') dx' = 1
    y = np.linspace(-200, 200, 400001)
    s = np.sum(P.free_propagator(0.3, y, 0.7)) * (y[1] - y[0])
    assert abs(s - 1.0) < 1e-2
    # propagation conserves the L2 norm (unitary evolution)
    xs = np.linspace(-40, 40, 4096)
    dx = xs[1] - xs[0]
    psi0 = P.gaussian_packet(xs, x0=0.0, p0=2.0, sigma=1.0)
    psit = P.propagate(psi0, xs, 1.5)
    n0 = np.sum(np.abs(psi0) ** 2) * dx
    nt = np.sum(np.abs(psit) ** 2) * dx
    assert _approx(nt, n0, tol=1e-6) and _approx(n0, 1.0, tol=1e-6)


# --- 5. the propagator IS the time-domain Green's function of Schrodinger -----

def test_free_satisfies_schrodinger():
    """For t>0 the free kernel solves the homogeneous TDSE i dK/dt = -1/2 d2K/dx2;
    with the theta(t) of free_retarded_propagator it is the retarded Green's
    function (i d_t - H)G^R = i delta(x-x')delta(t) -- cf. MA-14's causal Green."""
    x, xp, t, h = 0.7, 0.0, 0.8, 1e-4
    dKdt = (P.free_propagator(x, xp, t + h) - P.free_propagator(x, xp, t - h)) / (2 * h)
    d2K = (P.free_propagator(x + h, xp, t) - 2 * P.free_propagator(x, xp, t)
           + P.free_propagator(x - h, xp, t)) / h ** 2
    assert abs(1j * dKdt - (-0.5 * d2K)) < 1e-6


def test_retarded_propagator_causal():
    x = np.array([0.5, 1.0])
    assert np.allclose(P.free_retarded_propagator(x, 0.0, -0.5), 0.0)   # t<0: nothing
    assert np.allclose(P.free_retarded_propagator(x, 0.0, 0.0), 0.0)    # t=0 boundary
    assert np.allclose(P.free_retarded_propagator(x, 0.0, 0.7),
                       P.free_propagator(x, 0.0, 0.7))                  # t>0: K0


# --- 6-7. evolve a Gaussian: propagator == direct spectral evolution ---------

def test_gaussian_packet_vs_spectral():
    """propagate(K0, .) must reproduce a direct (split-step FFT) evolution of the
    free Schrodinger equation -- two independent algorithms, same Psi(x,t)."""
    xs = np.linspace(-40, 40, 4096)
    psi0 = P.gaussian_packet(xs, x0=0.0, p0=2.0, sigma=1.0)
    for t in (0.5, 2.0):
        psi_prop = P.propagate(psi0, xs, t)
        psi_spec = P.evolve_free_spectral(psi0, xs, t)
        assert np.max(np.abs(psi_prop - psi_spec)) < 1e-6


def test_gaussian_packet_spreading():
    """The propagated free packet's centre drifts at the group velocity p0/m and
    its width spreads as sigma sqrt(1 + (hbar t / 2 m sigma^2)^2)."""
    xs = np.linspace(-40, 40, 3000)
    x0, p0, sigma = -3.0, 1.5, 1.0
    psi0 = P.gaussian_packet(xs, x0=x0, p0=p0, sigma=sigma)
    for t in (1.0, 3.0):
        psit = P.propagate(psi0, xs, t)
        c, w = P.packet_center_width(psit, xs)
        assert _approx(c, x0 + p0 * t, tol=1e-4)
        assert _approx(w, sigma * np.sqrt(1.0 + (t / (2.0 * sigma ** 2)) ** 2), tol=1e-4)


# --- 8-10. harmonic oscillator propagator ------------------------------------

def test_harmonic_free_limit():
    """As omega -> 0 the Mehler kernel reduces to the free propagator K0."""
    x, xp, t = 1.0, -0.5, 0.7
    KH = complex(P.harmonic_propagator(np.array([x]), xp, t, omega=1e-5)[0])
    K0 = complex(P.free_propagator(np.array([x]), xp, t)[0])
    assert abs(KH - K0) < 1e-6


def test_harmonic_satisfies_schrodinger():
    """Mehler kernel solves the oscillator TDSE i dK/dt = (-1/2 d2/dx2 + 1/2 w^2 x^2)K."""
    w, x, xp, t, h = 1.0, 0.7, 0.2, 0.6, 1e-4
    dKdt = (P.harmonic_propagator(x, xp, t + h, w) - P.harmonic_propagator(x, xp, t - h, w)) / (2 * h)
    d2K = (P.harmonic_propagator(x + h, xp, t, w) - 2 * P.harmonic_propagator(x, xp, t, w)
           + P.harmonic_propagator(x - h, xp, t, w)) / h ** 2
    HK = -0.5 * d2K + 0.5 * w ** 2 * x ** 2 * P.harmonic_propagator(x, xp, t, w)
    assert abs(1j * dKdt - HK) < 1e-6


# --- 11. real-time path integral reconstructs K0 -----------------------------

def test_path_integral_free_realtime():
    """The literal real-time time-sliced sum-over-paths reconstructs K0 for the
    free particle: N=1 is exact, N=2 (one intermediate integration) matches K0."""
    x, xp, t = 1.0, -0.5, 0.8
    K0 = complex(P.free_propagator(np.array([x]), xp, t)[0])
    assert abs(P.path_integral_realtime_free(x, xp, t, 1) - K0) < 1e-12   # single slice
    assert abs(P.path_integral_realtime_free(x, xp, t, 2) - K0) < 1e-2    # one intermediate pt


# --- 12-13. imaginary-time (Wick) Trotter path integral converges ------------

def test_path_integral_euclidean_free():
    """Trotter product for V=0 reproduces the Euclidean free propagator (the
    heat kernel) -- the discretised sum over paths equals the closed form."""
    xs = np.linspace(-8, 8, 801)
    i, j = 425, 375                      # x = +0.5, x' = -0.5
    exact = P.free_propagator_euclidean(xs[i], xs[j], 1.0)
    for N in (1, 2, 8):
        K = P.path_integral_euclidean(xs, 1.0, N, lambda z: 0.0 * z, j)[i]
        assert abs(K - exact) < 1e-9


def test_path_integral_euclidean_harmonic_converges():
    """For V = x^2/2 the Trotter sum-over-paths converges to the Mehler kernel as
    the number of slices N -> infinity (Trotter error O(1/N^2))."""
    xs = np.linspace(-6, 6, 601)
    i, j = 350, 250                      # x = +1.0, x' = -1.0
    exact = P.harmonic_propagator_euclidean(xs[i], xs[j], 1.0, omega=1.0)
    errs = []
    for N in (1, 4, 16, 64):
        K = P.path_integral_euclidean(xs, 1.0, N, lambda z: 0.5 * z ** 2, j)[i]
        errs.append(abs(K - exact))
    assert errs[0] > errs[1] > errs[2] > errs[3]     # monotone convergence
    assert errs[-1] < 1e-3


# --- 14. eigenfunction-sum propagator (particle in a box) --------------------

def test_box_eigensum_propagates():
    """K = sum psi_n(x) psi_n(x') exp(-iE_n t) (Griffiths Eq.6.79): at t=0 it is
    completeness (-> delta), and it carries an eigenstate psi_m by exp(-iE_m t)."""
    Lx = np.linspace(0, 1, 801)
    dx = Lx[1] - Lx[0]
    # completeness at t=0: integral K(x,x',0) g(x') dx' -> g(x), improving with nmax
    g = lambda z: z * (1.0 - z)
    xq = 0.55
    e_lo = abs(np.sum(P.box_propagator(xq, Lx, 0.0, 20) * g(Lx)) * dx - g(xq))
    e_hi = abs(np.sum(P.box_propagator(xq, Lx, 0.0, 400) * g(Lx)) * dx - g(xq))
    assert e_hi < e_lo and e_hi < 1e-6
    # propagation: integral K(x,x',t) psi_m(x') dx' = exp(-iE_m t) psi_m(x)
    for m in (1, 2, 3):
        for t in (0.0, 0.5):
            val = np.sum(P.box_propagator(0.4, Lx, t, 60) * P.box_eigenfunction(m, Lx)) * dx
            exact = np.exp(-1j * P.box_energy(m) * t) * P.box_eigenfunction(m, 0.4)
            assert abs(val - exact) < 1e-6


# --- 15. the ~MA-14 link: propagator eigen-sum  <->  Green's-function eigen-sum

def test_ma14_resolvent_link():
    """The box Hamiltonian's static Green's function (the E->0 resolvent / H^{-1}
    kernel) is the propagator's eigen-sum with exp(-iE_n t) -> 1/E_n:

        G_H(x,x') = sum_n psi_n(x) psi_n(x') / E_n.

    With hbar=m=1, H_box = -(1/2)d^2/dx^2 = (1/2) L_op where L_op = -d^2/dx^2 is
    MA-14's operator, so G_H = 2 * G_{MA-14}.  We verify term-by-term against the
    IMPORTED green_series, and the closed form against the IMPORTED green_dirichlet."""
    for (x, xp) in [(0.3, 0.7), (0.5, 0.25), (0.8, 0.4)]:
        for N in (10, 100, 1000):
            assert abs(P.box_resolvent_static(x, xp, N) - 2.0 * green_series(x, xp, N)) < 1e-10
        # the spectral sum converges to MA-14's closed-form tent (x2)
        assert abs(P.box_resolvent_static(x, xp, 5000) - 2.0 * green_dirichlet(x, xp)) < 1e-3


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
