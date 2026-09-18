"""Tests for QM-08 one_dim -- every claim checked against a closed form.

Run directly:   python3 test_one_dim.py        (-> "All N tests passed.")
Or with pytest: pytest test_one_dim.py

The finite-difference eigensolver is validated against the exact infinite- and
finite-square-well spectra; the scattering coefficients are validated both against
their analytic formulae and against an independent transfer-matrix solve, and the
delta well is recovered as the zero-width limit of a finite well (Griffiths 3e
Problem 2.31).
"""
import numpy as np

from one_dim import (
    HBAR, MASS,
    bound_states, infinite_well_energy, finite_square_well_bound_count,
    delta_well_energy,
    transmission_barrier, reflection_barrier, step_RT, scatter_piecewise,
    free_particle_omega, phase_velocity, group_velocity, gaussian_packet_sigma,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- bound states: the infinite square well ----------------------------------

def test_infinite_well_eigenvalues():
    """FD eigensolver recovers E_n = n^2 pi^2 hbar^2 / (2 m L^2) for low n."""
    L = 1.0
    x = np.linspace(0.0, L, 2001)                 # walls = Dirichlet endpoints
    E, _ = bound_states(np.zeros_like(x), x, n_states=5)
    for n in range(1, 5):
        assert _approx(E[n - 1], infinite_well_energy(n, L), rel=1e-3)


def test_infinite_well_orthonormal():
    """The returned eigenfunctions are orthonormal: int psi_m psi_n dx = delta_mn."""
    L = 1.0
    x = np.linspace(0.0, L, 2001)
    _, psi = bound_states(np.zeros_like(x), x, n_states=4)
    for m in range(4):
        for n in range(4):
            overlap = np.trapezoid(psi[m] * psi[n], x)
            assert _approx(overlap, 1.0 if m == n else 0.0, abs_=1e-6)


# --- bound states: the finite square well ------------------------------------

def test_finite_well_count_matches_formula_and_solver():
    """Bound-state count = ceil(2 z0/pi); the FD solver finds exactly that many
    states with energy below the well top (E < 0)."""
    V0, a = 15.0, 1.0
    z0 = a * np.sqrt(2.0 * MASS * V0) / HBAR
    n_analytic = finite_square_well_bound_count(V0, a)
    assert n_analytic == int(np.ceil(2.0 * z0 / np.pi)) == 4

    X = np.linspace(-25.0, 25.0, 5001)            # box >> decay length
    V = np.where(np.abs(X) < a, -V0, 0.0)
    E, _ = bound_states(V, X, n_states=10)
    n_fd = int(np.sum(E < 0.0))
    assert n_fd == n_analytic


def test_finite_well_energies_below_depth():
    """Every bound state sits below the well top and above the well bottom:
    -V0 < E < 0 (binding energy smaller than the well depth)."""
    V0, a = 15.0, 1.0
    X = np.linspace(-25.0, 25.0, 5001)
    V = np.where(np.abs(X) < a, -V0, 0.0)
    E, _ = bound_states(V, X, n_states=10)
    bound = E[E < 0.0]
    assert bound.size == 4
    assert np.all(bound > -V0) and np.all(bound < 0.0)


# --- the delta-function well -------------------------------------------------

def test_delta_well_one_bound_state():
    """The delta well has exactly one bound state at E = -m alpha^2 / 2 hbar^2.
    A finite well in the 'weak' (z0 < pi/2) regime likewise has exactly one."""
    assert _approx(delta_well_energy(2.0), -2.0, rel=1e-12)        # -alpha^2/2
    assert _approx(delta_well_energy(1.0), -0.5, rel=1e-12)
    # a shallow/narrow finite well (the delta well is its limit) has 1 bound state
    assert finite_square_well_bound_count(V0=0.5, a=0.5) == 1


def test_delta_well_as_finite_square_well_limit():
    """Griffiths 3e Problem 2.31: a finite well of depth V0=alpha/d and width d
    approaches the delta well as d -> 0; its FD ground state -> -alpha^2/2,
    converging monotonically."""
    alpha = 2.0
    target = delta_well_energy(alpha)
    X = np.linspace(-10.0, 10.0, 20001)
    errs = []
    for d in (0.2, 0.1, 0.05):
        V0 = alpha / d
        V = np.where(np.abs(X) < d / 2.0, -V0, 0.0)
        E, _ = bound_states(V, X, n_states=1)
        assert E[0] < 0.0                                   # is bound
        errs.append(abs(E[0] - target))
    assert errs[0] > errs[1] > errs[2]                       # monotone convergence
    assert errs[2] < 0.2 * abs(target)                       # within 20% at d=0.05


# --- the rectangular barrier: tunnelling -------------------------------------

def test_barrier_tunnelling_is_positive():
    """For E < V0 the transmission is exponentially small but strictly positive --
    classically forbidden, quantum-mechanically allowed (tunnelling)."""
    for E in (1.0, 3.0, 5.0, 9.0):
        T = transmission_barrier(E, V0=10.0, a=1.0)
        assert 0.0 < T < 1.0


def test_barrier_analytic_formula():
    """Direct check of T = [1 + V0^2 sinh^2(kappa a)/(4 E (V0-E))]^-1 for E<V0."""
    E, V0, a = 5.0, 10.0, 1.0
    kappa = np.sqrt(2.0 * MASS * (V0 - E)) / HBAR
    expected = 1.0 / (1.0 + V0**2 * np.sinh(kappa * a)**2 / (4.0 * E * (V0 - E)))
    assert _approx(transmission_barrier(E, V0, a), expected, rel=1e-12)


def test_barrier_matches_transfer_matrix():
    """The analytic T equals an independent transfer-matrix solve, for both
    tunnelling (E<V0) and over-barrier (E>V0) energies."""
    V0, a = 10.0, 1.0
    for E in (2.0, 5.0, 9.0, 10.5, 12.0, 20.0):
        T_analytic = transmission_barrier(E, V0, a)
        T_tm, R_tm = scatter_piecewise(E, [0.0, V0, 0.0], [0.0, a])
        assert _approx(T_tm, T_analytic, rel=1e-9)
        assert _approx(T_tm + R_tm, 1.0, rel=1e-9)           # current conserved


def test_barrier_R_plus_T():
    """Barrier reflection + transmission = 1 (same medium both sides)."""
    for E in (2.0, 6.0, 15.0):
        assert _approx(transmission_barrier(E, 10.0, 1.0)
                       + reflection_barrier(E, 10.0, 1.0), 1.0, rel=1e-12)


def test_barrier_over_barrier_resonances():
    """For E > V0, T = 1 exactly at the resonances k2 a = n pi
    (E = V0 + n^2 pi^2 hbar^2 / 2 m a^2), and T < 1 between them."""
    V0, a = 10.0, 1.0
    for n in (1, 2, 3):
        E_res = V0 + (n * np.pi * HBAR)**2 / (2.0 * MASS * a**2)
        assert _approx(transmission_barrier(E_res, V0, a), 1.0, rel=1e-9)
    # halfway between the first two resonances transmission dips below 1
    E1 = V0 + (np.pi * HBAR)**2 / (2.0 * MASS * a**2)
    E2 = V0 + (2 * np.pi * HBAR)**2 / (2.0 * MASS * a**2)
    assert transmission_barrier(0.5 * (E1 + E2), V0, a) < 1.0


def test_barrier_limits():
    """Thick/high barrier -> T -> 0; vanishing width -> T -> 1; E >> V0 -> T -> 1."""
    assert transmission_barrier(1.0, V0=20.0, a=5.0) < 1e-6        # thick: opaque
    assert transmission_barrier(5.0, V0=10.0, a=1e-4) > 0.999      # thin: transparent
    assert transmission_barrier(1e4, V0=10.0, a=1.0) > 0.999       # E >> V0


def test_barrier_E_equals_V0_continuity():
    """At E = V0 the formula uses the sinh->linear limit T=[1+m V0 a^2/2hbar^2]^-1,
    and joins the E<V0 and E>V0 branches continuously."""
    V0, a = 10.0, 1.0
    T_at = transmission_barrier(V0, V0, a)
    assert _approx(T_at, 1.0 / (1.0 + MASS * V0 * a**2 / (2.0 * HBAR**2)), rel=1e-12)
    assert _approx(transmission_barrier(V0 * (1 - 1e-7), V0, a), T_at, rel=1e-4)
    assert _approx(transmission_barrier(V0 * (1 + 1e-7), V0, a), T_at, rel=1e-4)


# --- the step potential ------------------------------------------------------

def test_step_R_plus_T_and_transfer_matrix():
    """For E > V0: R + T = 1 (current-weighted), matching the transfer matrix."""
    V0 = 1.0
    for E in (1.5, 2.0, 4.0, 25.0):
        R, T = step_RT(E, V0)
        assert _approx(R + T, 1.0, rel=1e-12)
        T_tm, R_tm = scatter_piecewise(E, [0.0, V0], [0.0])
        assert _approx(T_tm, T, rel=1e-9) and _approx(R_tm, R, rel=1e-9)


def test_step_total_reflection_below_barrier():
    """For E <= V0 the step reflects everything: R = 1, T = 0 (evanescent)."""
    R, T = step_RT(0.5, 1.0)
    assert _approx(R, 1.0, rel=1e-12) and _approx(T, 0.0, abs_=1e-12)
    # the transfer matrix agrees: no transmitted current
    T_tm, R_tm = scatter_piecewise(0.5, [0.0, 1.0], [0.0])
    assert _approx(T_tm, 0.0, abs_=1e-9) and _approx(R_tm, 1.0, rel=1e-6)


def test_step_high_energy_limit():
    """E >> V0: the step becomes nearly invisible, T -> 1."""
    R, T = step_RT(1e6, 1.0)
    assert T > 0.999 and R < 1e-3


# --- free particle / wave packets --------------------------------------------

def test_free_particle_dispersion_and_velocities():
    """omega = hbar k^2/2m; group velocity = 2 x phase velocity = hbar k/m = p/m."""
    k = 3.0
    assert _approx(free_particle_omega(k), HBAR * k**2 / (2.0 * MASS), rel=1e-12)
    assert _approx(group_velocity(k), 2.0 * phase_velocity(k), rel=1e-12)
    assert _approx(group_velocity(k), HBAR * k / MASS, rel=1e-12)   # classical p/m


def test_gaussian_packet_spreads():
    """A free Gaussian packet is narrowest at t=0 and spreads symmetrically."""
    s0 = 1.0
    assert _approx(gaussian_packet_sigma(0.0, s0), s0, rel=1e-12)   # minimum at t=0
    assert gaussian_packet_sigma(2.0, s0) > s0                       # spreads
    assert _approx(gaussian_packet_sigma(2.0, s0),
                   gaussian_packet_sigma(-2.0, s0), rel=1e-12)       # symmetric in t
    assert gaussian_packet_sigma(5.0, s0) > gaussian_packet_sigma(2.0, s0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
