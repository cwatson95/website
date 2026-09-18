"""Tests for QF-04 renormalization & the renormalization group.

Run:  python3 test_renormalization.py     ->  "All N tests passed."
"""
import numpy as np

from renormalization import (
    ALPHA0, M_E, M_Z,
    beta_qed, qed_running_alpha, qed_landau_pole, qed_alpha_sm,
    beta_phi4, phi4_running, phi4_landau_pole,
    beta_qcd, qcd_running_alpha,
    beta_toy, fixed_point,
)


def test_beta_qed_positive_and_formula():
    # beta(alpha) = 2 alpha^2 / 3pi > 0
    a = ALPHA0
    assert beta_qed(a) > 0.0
    assert np.isclose(beta_qed(a), 2.0 * a ** 2 / (3.0 * np.pi), rtol=1e-12)
    # scales with the squared-charge sum S
    assert np.isclose(beta_qed(a, sum_q2=3.0), 3.0 * beta_qed(a, sum_q2=1.0), rtol=1e-12)


def test_qed_alpha_increases_with_Q():
    # alpha(Q0) = alpha0, and alpha grows monotonically with Q (screening weakens)
    assert np.isclose(qed_running_alpha(M_E), ALPHA0, rtol=1e-12)
    Qs = [M_E, 1.0, M_Z, 1.0e3, 1.0e6]
    alphas = [qed_running_alpha(Q) for Q in Qs]
    assert all(a2 > a1 for a1, a2 in zip(alphas, alphas[1:]))
    # the running is small over this range (perturbative): a few percent
    assert 1.0 / alphas[2] < 1.0 / ALPHA0          # 1/alpha(M_Z) < 1/alpha(0)


def test_qed_alpha_electron_only_at_MZ():
    # electron loop alone: 1/alpha(M_Z) ~ 134.5 from 1/137 (the mechanism)
    inv = 1.0 / qed_running_alpha(M_Z)
    assert 134.0 < inv < 135.0


def test_qed_alpha_full_SM_at_MZ_is_128():
    # all charged SM fermions (threshold sum) reproduce the measured alpha(M_Z) ~ 1/128
    inv = 1.0 / qed_alpha_sm(M_Z)
    assert 127.0 < inv < 129.0
    # adding the heavier fermions steepens the running vs electron-only
    assert inv < 1.0 / qed_running_alpha(M_Z)


def test_qed_landau_pole():
    QL = qed_landau_pole()
    # astronomically high, far above the Planck scale ~ 1e19 GeV
    assert QL > 1.0e100
    # at QL the closed-form denominator vanishes (computed in log space, no overflow)
    denom = 1.0 - (ALPHA0 / (3.0 * np.pi)) * 2.0 * np.log(QL / M_E)
    assert abs(denom) < 1.0e-9
    # a larger squared-charge sum lowers the pole
    assert qed_landau_pole(sum_q2=4.0) < QL


def test_phi4_beta_positive_and_running_matches_closed_form():
    assert beta_phi4(0.5) > 0.0
    lam0, mu0, mu = 1.0, 1.0, 1.0e10
    lam = phi4_running(lam0, mu0, mu)
    closed = 1.0 / (1.0 / lam0 - 3.0 / (16.0 * np.pi ** 2) * np.log(mu / mu0))
    assert np.isclose(lam, closed, rtol=1e-6)
    assert lam > lam0                              # beta > 0 -> coupling grows in the UV


def test_phi4_triviality_pole():
    lam0, mu0 = 1.0, 1.0
    mu_pole = phi4_landau_pole(lam0, mu0)
    assert mu_pole > mu0
    # the closed-form denominator vanishes at the pole
    denom = 1.0 / lam0 - 3.0 / (16.0 * np.pi ** 2) * np.log(mu_pole / mu0)
    assert abs(denom) < 1.0e-9


def test_qcd_asymptotic_freedom():
    # beta < 0 (opposite sign to QED): coupling SHRINKS toward the UV
    assert beta_qcd(0.1181, nf=5) < 0.0
    assert np.isclose(qcd_running_alpha(M_Z), 0.1181, rtol=1e-9)   # boundary value
    assert qcd_running_alpha(1.0e3) < qcd_running_alpha(M_Z) < qcd_running_alpha(2.0)
    # below nf = 16.5 the one-loop coefficient b0 = 11 - (2/3)nf is positive
    assert beta_qcd(0.2, nf=16) < 0.0 and beta_qcd(0.2, nf=17) > 0.0


def test_fixed_point_and_stability():
    a, b = 2.0, 4.0
    fp = fixed_point(a, b)
    # non-trivial zero g* = a/b
    assert np.isclose(fp["g_star"], a / b, rtol=1e-12)
    assert np.isclose(beta_toy(fp["g_star"], a, b), 0.0, atol=1e-12)
    assert np.isclose(beta_toy(0.0, a, b), 0.0, atol=1e-12)        # the Gaussian zero
    # beta'(g*) = -a^2/b < 0  -> UV-attractive
    assert np.isclose(fp["beta_prime"], -a ** 2 / b, rtol=1e-12)
    assert fp["uv_attractive"] and fp["stability"] == "UV-attractive"
    # slope matches a finite-difference of beta_toy at g*
    g, h = fp["g_star"], 1.0e-6
    fd = (beta_toy(g + h, a, b) - beta_toy(g - h, a, b)) / (2.0 * h)
    assert np.isclose(fd, fp["beta_prime"], rtol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
