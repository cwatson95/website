"""Tests for SM-06 kinetic theory. Reuses SM-01 (K_B).

Run:  python3 test_kinetic_theory.py     ->  "All N tests passed."
"""
import math

# own module first: chains SM-01 (and MA-19) onto sys.path
from kinetic_theory import (
    K_B, maxwell_speed_pdf, most_probable_speed, mean_speed, rms_speed,
    mean_kinetic_energy, mean_free_path, collision_rate, effusion_flux,
    diffusion_coefficient, einstein_relation_diffusion,
)

M = 4.652e-26      # N2 mass [kg]
T = 300.0


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=20000):
    dv = (b - a) / n
    return sum(f(a + (i + 0.5) * dv) * dv for i in range(n))


def test_distribution_normalized():
    vmax = 12.0 * most_probable_speed(M, T)
    total = _integrate(lambda v: maxwell_speed_pdf(v, M, T), 0.0, vmax)
    assert _approx(total, 1.0, tol=1e-4)


def test_characteristic_speed_formulas_and_ordering():
    vp, vbar, vrms = most_probable_speed(M, T), mean_speed(M, T), rms_speed(M, T)
    assert _approx(vp, math.sqrt(2 * K_B * T / M))
    assert _approx(vbar, math.sqrt(8 * K_B * T / (math.pi * M)))
    assert _approx(vrms, math.sqrt(3 * K_B * T / M))
    # strict ordering v_p < <v> < v_rms
    assert vp < vbar < vrms
    # fixed ratios 1 : sqrt(4/pi) : sqrt(3/2)
    assert _approx(vbar / vp, math.sqrt(4.0 / math.pi))
    assert _approx(vrms / vp, math.sqrt(1.5))


def test_moments_match_distribution():
    # <v> and <v^2> from integrating the pdf match the closed forms
    vmax = 12.0 * most_probable_speed(M, T)
    vbar_int = _integrate(lambda v: v * maxwell_speed_pdf(v, M, T), 0.0, vmax)
    v2_int = _integrate(lambda v: v * v * maxwell_speed_pdf(v, M, T), 0.0, vmax)
    assert _approx(vbar_int, mean_speed(M, T), tol=1e-3)
    assert _approx(v2_int, rms_speed(M, T) ** 2, tol=1e-3)
    # equipartition: <1/2 m v^2> = 3/2 kT
    assert _approx(0.5 * M * v2_int, mean_kinetic_energy(T), tol=1e-3)


def test_pdf_peaks_at_most_probable_speed():
    vp = most_probable_speed(M, T)
    f_peak = maxwell_speed_pdf(vp, M, T)
    assert f_peak > maxwell_speed_pdf(0.6 * vp, M, T)
    assert f_peak > maxwell_speed_pdf(1.5 * vp, M, T)


def test_mean_free_path_and_collision_rate():
    n, d = 2.5e25, 3.7e-10
    lam = mean_free_path(n, d)
    assert _approx(lam, 1.0 / (math.sqrt(2) * n * math.pi * d ** 2))
    # z = <v>/lambda
    assert _approx(collision_rate(n, d, M, T), mean_speed(M, T) / lam)
    # denser gas -> shorter free path
    assert mean_free_path(2 * n, d) < lam


def test_effusion_flux():
    n = 2.5e25
    assert _approx(effusion_flux(n, M, T), 0.25 * n * mean_speed(M, T))


def test_diffusion_kinetic_and_einstein():
    n, d = 2.5e25, 3.7e-10
    D = diffusion_coefficient(n, d, M, T)
    assert _approx(D, mean_speed(M, T) * mean_free_path(n, d) / 3.0)
    assert D > 0
    # Einstein relation D = mu kT, linear in mobility and temperature
    assert _approx(einstein_relation_diffusion(1e11, T), 1e11 * K_B * T)
    assert _approx(einstein_relation_diffusion(1e11, 2 * T)
                   / einstein_relation_diffusion(1e11, T), 2.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
