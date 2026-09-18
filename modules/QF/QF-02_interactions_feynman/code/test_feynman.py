"""Tests for QF-02 interactions & Feynman diagrams.

Run:  python3 test_feynman.py     ->  "All N tests passed."
"""
import numpy as np

from feynman import (
    minkowski_dot, minkowski_square, on_shell_energy,
    cm_energy, cm_momentum,
    mandelstam, mandelstam_sum,
    phi4_amplitude_squared, phi4_differential_cross_section,
    phi4_cross_section, propagator,
)

M = 1.0


# --- kinematics --------------------------------------------------------------

def test_mandelstam_sum_rule():
    # s + t + u = 4 m^2 for every energy and angle (the Mandelstam identity)
    for E_cm in [2.5, 4.0, 7.0]:
        for theta in np.linspace(0.0, np.pi, 7):
            s, t, u = mandelstam(E_cm, theta, M)
            assert abs((s + t + u) - mandelstam_sum(M)) < 1e-9
            assert abs((s + t + u) - 4.0 * M * M) < 1e-9


def test_s_is_cm_energy_squared():
    for E_cm in [2.1, 3.3, 9.0]:
        s, t, u = mandelstam(E_cm, 0.7, M)
        assert abs(s - E_cm ** 2) < 1e-12


def test_t_u_nonpositive_in_physical_region():
    # above threshold t, u <= 0 (spacelike momentum transfer)
    s, t, u = mandelstam(5.0, np.pi / 3.0, M)
    assert t <= 1e-12 and u <= 1e-12
    # forward (theta = 0): t = 0;  backward (theta = pi): u = 0
    _, t0, _ = mandelstam(5.0, 0.0, M)
    assert abs(t0) < 1e-12
    _, _, up = mandelstam(5.0, np.pi, M)
    assert abs(up) < 1e-12


def test_cm_energy_from_four_momenta():
    # equal-mass pair back-to-back: sqrt(s) = 2 E
    p = 3.0
    E = on_shell_energy([p, 0.0, 0.0], M)
    p1 = np.array([E, p, 0.0, 0.0])
    p2 = np.array([E, -p, 0.0, 0.0])
    assert abs(cm_energy(p1, p2) - 2.0 * E) < 1e-12
    # both at rest: sqrt(s) = 2 m (the threshold)
    r = np.array([M, 0.0, 0.0, 0.0])
    assert abs(cm_energy(r, r) - 2.0 * M) < 1e-12


def test_cm_momentum_threshold_and_formula():
    assert cm_momentum(2.0 * M, M) == 0.0          # exactly at threshold
    assert cm_momentum(1.5 * M, M) == 0.0          # below threshold
    assert cm_momentum(4.0, M) > 0.0               # above threshold
    E_cm = 5.0
    assert abs(cm_momentum(E_cm, M) - 0.5 * np.sqrt(E_cm ** 2 - 4.0 * M * M)) < 1e-12


def test_minkowski_metric():
    # on-shell square = m^2; a light-like vector squares to 0
    E = on_shell_energy([1.0, 2.0, 2.0], M)        # |p| = 3, E = sqrt(10)
    p = np.array([E, 1.0, 2.0, 2.0])
    assert abs(minkowski_square(p) - M * M) < 1e-12
    null = np.array([5.0, 5.0, 0.0, 0.0])
    assert abs(minkowski_square(null)) < 1e-12
    assert abs(minkowski_dot([1, 0, 0, 0], [1, 0, 0, 0]) - 1.0) < 1e-12


# --- phi^4 amplitude & cross section -----------------------------------------

def test_phi4_amplitude_squared():
    for lam in [0.1, 0.5, 2.0]:
        assert abs(phi4_amplitude_squared(lam) - lam * lam) < 1e-15


def test_phi4_cross_section_positive_and_formula():
    lam, E_cm = 0.3, 5.0
    sig = phi4_cross_section(E_cm, lam, M)
    assert sig > 0.0
    assert abs(sig - lam * lam / (32.0 * np.pi * E_cm ** 2)) < 1e-18


def test_phi4_cross_section_scales_as_lambda_squared():
    E_cm = 5.0
    s1 = phi4_cross_section(E_cm, 0.2, M)
    s2 = phi4_cross_section(E_cm, 0.4, M)          # double lambda -> 4x sigma
    assert abs(s2 / s1 - 4.0) < 1e-12


def test_phi4_threshold():
    lam = 0.3
    assert phi4_cross_section(1.99 * M, lam, M) == 0.0   # below 2 m
    assert phi4_cross_section(2.0 * M, lam, M) > 0.0     # at threshold: finite
    assert phi4_cross_section(3.0 * M, lam, M) > 0.0


def test_phi4_total_is_dsigma_times_solid_angle_over_two():
    # total = (1/2) * 4 pi * (d sigma/d Omega): the identical-particle factor
    lam, E_cm = 0.7, 6.0
    dsig = phi4_differential_cross_section(E_cm, lam, M)
    assert abs(phi4_cross_section(E_cm, lam, M) - 0.5 * 4.0 * np.pi * dsig) < 1e-18


def test_phi4_cross_section_falls_with_energy():
    lam = 0.3
    assert phi4_cross_section(3.0, lam, M) > phi4_cross_section(6.0, lam, M)


# --- the Feynman propagator --------------------------------------------------

def test_propagator_on_shell_pole():
    # on shell p^2 = m^2: |D_F| ~ 1/eps blows up
    p_vec = [2.0, 0.0, 0.0]
    p = np.array([on_shell_energy(p_vec, M)] + p_vec)
    assert abs(minkowski_square(p) - M * M) < 1e-12       # genuinely on shell
    eps = 1e-6
    z = propagator(p, M, eps)
    assert abs(z) > 1e5                                    # ~ 1/eps
    assert abs(abs(z) - 1.0 / eps) < 1e-3 * (1.0 / eps)


def test_propagator_off_shell_is_imaginary():
    # far off shell, eps -> 0: D_F ~ i/(p^2 - m^2), nearly pure imaginary
    p = np.array([3.0, 0.0, 0.0, 0.0])                    # p^2 = 9
    x = minkowski_square(p) - M * M                        # = 8
    z = propagator(p, M, eps=1e-12)
    assert abs(z - 1j / x) < 1e-9
    assert abs(z.imag - 1.0 / x) < 1e-6
    assert abs(z.real) < 1e-6


def test_propagator_real_part_nonnegative():
    # Re D_F = eps/((p^2 - m^2)^2 + eps^2) >= 0 everywhere (Feynman i eps)
    for p0 in [0.5, 1.0, 2.0, 3.0]:
        p = np.array([p0, 0.5, 0.0, 0.0])
        assert propagator(p, M, eps=1e-3).real >= 0.0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
