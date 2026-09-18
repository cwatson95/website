"""Tests for MACRO_EM-01 -- every Wilcox Ch.1 / App.A exercise gets a check.

Run directly:   python3 test_intro_perspectives.py   (-> "All N tests passed.")
Or with pytest: pytest test_intro_perspectives.py

Gaussian units (Table 1.1): div E = 4 pi rho, curl B - (1/c) dE/dt = (4pi/c) J,
curl E + (1/c) dB/dt = 0, div B = 0. The polynomial test fields have degree
<= 2 per variable, so the 5-point 4th-order stencils are exact and identity
residuals are pure rounding.
"""
import numpy as np

from intro_perspectives import (
    C_GAUSS_CM_S, C_NUM, ALPHA, BETA, FOUR_PI_EPS0, EPS0_SI, MU0_SI,
    E_STATC, E_CODATA_C,
    fd_grad, fd_div, fd_curl, fd_lap,
    bac_cab_residual, jacobi_residual,
    laplacian_product_residual, grad_dot_expansion_residual,
    e_from_potentials, b_from_potentials, div_b_residual, faraday_residual,
    coulomb_sides, ampere_sides,
    continuity_residual, gaussian_blob,
    v_area, circulation2d, area_by_circulation,
    circle_curve, ellipse_curve, polar_curve,
    gradient_theorem_sides, curl_volume_theorem_sides,
    stokes_gradient_sides_disc, stokes_gradient_sides_hemisphere,
    e2d_point_charge, flux2d, square_flux2d, powerlaw_flux2d,
    cross_z_2d, zcross_2d, fd_div2d, fd_curlz2d, gauss2d_sides, stokes2d_sides,
    TABLE_A1, TABLE_A2, amount_factor, book_value,
    statcoulomb_in_C, statvolt_in_V, gauss_in_tesla, maxwell_in_weber,
    oersted_in_A_per_m, cm_in_farad, s_per_cm_in_ohm,
    mksg_charge_unit_in_statC, mksg_charge_unit_in_C,
    mksg_field_unit_in_gauss, mksg_bfield_unit_in_tesla,
    electron_charge_via_mksg,
)

RNG = np.random.default_rng(20260706)


def _pts(n=20, lo=-1.5, hi=1.5, dim=3):
    return RNG.uniform(lo, hi, size=(n, dim))


# --- polynomial test fields (degree <= 2 per variable: FD stencils exact) ----

def poly_phi(p):
    x, y, z = p
    return x*x*y - 3.0*z*z*x + 2.0*y*y*z + x - 0.7*y*z

def poly_psi(p):
    x, y, z = p
    return x*z*z - y*y + 0.5*x*x*z + 2.0*y - 1.0

def poly_A(p):
    x, y, z = p
    return np.array([y*z + x*x, z*z*x - y, x*y - z*z + 0.3*y*y])

def poly_B(p):
    x, y, z = p
    return np.array([x*y - z, y*y + x*z, z*y + 0.5*x*x])

def trig_phi(p):
    x, y, z = p
    return np.sin(x)*np.cos(y) + np.exp(0.3*z)*y

def trig_psi(p):
    x, y, z = p
    return np.cos(0.7*x + y) + z*np.sin(y)

def trig_A(p):
    x, y, z = p
    return np.array([np.sin(y)*z, np.cos(x) + y*z, np.exp(0.2*x)*np.sin(z)])


# =========================== P1 -- Exercise 1.1.1 ===========================

def test_bac_cab_and_jacobi():
    """1.1.1(a): A x (B x C) + cyc. = 0 (via three BAC-CABs) on 500 triples."""
    for _ in range(500):
        a, b, c = RNG.standard_normal(3), RNG.standard_normal(3), RNG.standard_normal(3)
        assert np.max(np.abs(bac_cab_residual(a, b, c))) < 1e-13
        assert np.max(np.abs(jacobi_residual(a, b, c))) < 1e-13


def test_laplacian_product_poly():
    """1.1.1(b): lap(phi psi) = phi lap psi + psi lap phi + 2 grad.grad --
    exact on polynomial fields (residual = rounding)."""
    for p in _pts(15):
        assert abs(laplacian_product_residual(poly_phi, poly_psi, p, h=0.25)) < 1e-9


def test_laplacian_product_trig():
    """1.1.1(b) again on transcendental fields (4th-order truncation level)."""
    for p in _pts(10):
        assert abs(laplacian_product_residual(trig_phi, trig_psi, p, h=0.02)) < 1e-6


def test_grad_dot_expansion_poly():
    """1.1.1(c): sum_i A_i grad B_i = grad(A.B) - (B.grad)A - B x curl A --
    exact on polynomial fields."""
    for p in _pts(15):
        r = grad_dot_expansion_residual(poly_A, poly_B, p, h=0.25)
        assert np.max(np.abs(r)) < 1e-9


def test_grad_dot_expansion_trig():
    """1.1.1(c) on transcendental fields."""
    B = lambda p: np.array([np.cos(p[1]), np.sin(p[2]) + p[0], np.exp(0.1*p[1])])
    for p in _pts(8):
        r = grad_dot_expansion_residual(trig_A, B, p, h=0.02)
        assert np.max(np.abs(r)) < 1e-5


# =========================== P2 -- Exercise 1.1.2 ===========================

def _Phi(p, t):
    x, y, z = p
    return x*x*y - 2.0*z*t + t*t + 0.5*y*z

def _A(p, t):
    x, y, z = p
    return np.array([y*z*t + x, x*x - t*z + y*y, x*y - y*y*t + z*t*t])


def test_potentials_no_monopole_identity():
    """1.1.2: div B = div curl A = 0 identically (nested FD, exact on polys)."""
    for p in _pts(10):
        t = float(RNG.uniform(-1, 1))
        assert abs(div_b_residual(_A, p, t, h=0.2)) < 1e-9


def test_potentials_faraday_identity():
    """1.1.2: curl E + (1/c) dB/dt = 0 identically -- for a toy c AND for the
    true Gaussian c = 2.9979e10 cm/s (the identity is c-independent)."""
    for c in (2.0, C_GAUSS_CM_S):
        for p in _pts(6):
            t = float(RNG.uniform(-1, 1))
            r = faraday_residual(_Phi, _A, p, t, c=c, h=0.2)
            assert np.max(np.abs(r)) < 1e-9


def test_potentials_coulomb_pde():
    """1.1.2: div E == -[lap Phi + (1/c) d_t div A]  (the derived Coulomb PDE:
    both sides evaluated independently, so this checks the simplification)."""
    for p in _pts(8):
        t = float(RNG.uniform(-1, 1))
        lhs, rhs = coulomb_sides(_Phi, _A, p, t, c=2.0, h=0.2)
        assert abs(lhs - rhs) < 1e-9


def test_potentials_ampere_pde():
    """1.1.2: curl B - (1/c) dE/dt == -[lap A - (1/c^2) d_tt A
    - grad(div A + (1/c) d_t Phi)]  (the derived Ampere-Maxwell PDE)."""
    for p in _pts(8):
        t = float(RNG.uniform(-1, 1))
        lhs, rhs = ampere_sides(_Phi, _A, p, t, c=2.0, h=0.2)
        assert np.max(np.abs(lhs - rhs)) < 1e-9


# =========================== P3 -- Exercise 1.1.3 ===========================

def test_continuity_moving_blob():
    """1.1.3: d rho/dt + div J = 0 for rho = e f(r - R(t)), J = e Rdot f --
    Gaussian blob on a curved trajectory; both terms O(1), sum ~ 0."""
    f = gaussian_blob(0.8)
    R = lambda t: np.array([np.cos(t), np.sin(2.0*t), 0.3*t])
    saw_big_term = False
    for _ in range(20):
        p = RNG.uniform(-1.2, 1.2, 3)
        t = float(RNG.uniform(0.0, 2.0))
        res, drdt, divj = continuity_residual(f, R, 1.3, p, t, h=2e-3)
        assert abs(res) < 1e-8
        if abs(drdt) > 0.05:
            saw_big_term = True
    assert saw_big_term      # the cancellation is between genuinely big terms


def test_continuity_second_trajectory():
    """1.1.3 with a different f-width and trajectory (arbitrariness of f, R)."""
    f = gaussian_blob(0.5)
    R = lambda t: np.array([t*t, -t, np.sin(t)])
    for _ in range(15):
        p = RNG.uniform(-1.0, 1.0, 3)
        t = float(RNG.uniform(0.0, 1.5))
        res, _, _ = continuity_residual(f, R, -0.7, p, t, h=1e-3)
        assert abs(res) < 1e-8


# =========================== P4 -- Exercise 1.4.1 ===========================

def test_circulation_circle():
    """1.4.1(a): oint v.dl = 2A for circles: 2 pi r^2."""
    for r in (0.7, 1.0, 2.5):
        got = circulation2d(v_area, *circle_curve(r))
        assert abs(got - 2.0*np.pi*r*r) < 1e-10 * max(1.0, r*r)


def test_ellipse_area():
    """1.4.1(b): the ellipse x^2/a^2 + y^2/b^2 = 1 has A = (1/2) oint = pi a b."""
    for a, b in ((3.0, 1.5), (2.0, 0.4), (1.0, 1.0)):
        got = area_by_circulation(*ellipse_curve(a, b))
        assert abs(got - np.pi*a*b) < 1e-10 * max(1.0, a*b)


def test_star_curve_area():
    """1.4.1(a) holds for ANY planar boundary: r = 1 + 0.3 cos(3 theta) has
    A = (1/2) int r^2 dtheta = pi (1 + 0.3^2/2)."""
    eps = 0.3
    curve, dcurve = polar_curve(lambda t: 1.0 + eps*np.cos(3.0*t),
                                lambda t: -3.0*eps*np.sin(3.0*t))
    got = area_by_circulation(curve, dcurve, n=1024)
    assert abs(got - np.pi*(1.0 + 0.5*eps*eps)) < 1e-10


# =========================== P5 -- Exercise 1.4.2 ===========================

_BOX = ((-1.0, 1.3), (-0.7, 1.1), (-1.2, 0.9))


def test_gradient_theorem_box():
    """1.4.2(a): int_V grad phi d3x = oint_S da nhat phi (asymmetric box)."""
    phi = lambda p: np.sin(p[0])*np.cos(p[1]) + p[2]*p[2]*np.exp(p[0]/3.0)
    vol, surf = gradient_theorem_sides(phi, _BOX, n=20, h=0.005)
    assert np.max(np.abs(vol - surf)) < 1e-8
    assert np.max(np.abs(vol)) > 0.1        # not trivially zero


def test_curl_volume_theorem_box():
    """1.4.2(b): int_V curl A d3x = oint_S da nhat x A."""
    A = lambda p: np.array([p[1]*p[1] + np.sin(p[2]),
                            p[2]*p[0] + np.cos(p[0]),
                            p[0]*p[1]*p[1]])
    vol, surf = curl_volume_theorem_sides(A, _BOX, n=20, h=0.005)
    assert np.max(np.abs(vol - surf)) < 1e-8
    assert np.max(np.abs(vol)) > 0.1


# =========================== P6 -- Exercise 1.4.3 ===========================

def _phi6(p):
    x, y, z = p
    return x*x*y - 3.0*z + np.cos(y)

def _grad_phi6(p):
    x, y, z = p
    return np.array([2.0*x*y, x*x - np.sin(y), -3.0])


def test_stokes_gradient_disc():
    """1.4.3: int_disc da nhat x grad phi = oint dl phi (unit circle boundary).
    Also validates the hand-coded grad against FD."""
    for p in _pts(5, lo=-0.8, hi=0.8):
        assert np.max(np.abs(_grad_phi6(p) - fd_grad(_phi6, p, h=0.02))) < 1e-7
    lhs, rhs = stokes_gradient_sides_disc(_phi6, _grad_phi6)
    assert np.max(np.abs(lhs - rhs)) < 1e-9
    assert np.max(np.abs(rhs)) > 0.1
    assert abs(lhs[2]) < 1e-9 and abs(rhs[2]) < 1e-9   # planar: z-components vanish


def test_stokes_gradient_hemisphere_matches():
    """1.4.3, surface-independence: the hemisphere spanning the same circle
    gives the same vector as the flat disc (only the boundary matters)."""
    lhs_h, rhs = stokes_gradient_sides_hemisphere(_phi6, _grad_phi6)
    lhs_d, _ = stokes_gradient_sides_disc(_phi6, _grad_phi6)
    assert np.max(np.abs(lhs_h - rhs)) < 1e-9
    assert np.max(np.abs(lhs_h - lhs_d)) < 1e-9


# =========================== P7 -- Exercise 1.5.1 ===========================

def test_e2d_flux_circles():
    """1.5.1(a): oint E.nhat dl = 4 pi q for E = 2q rhohat/rho -- circles of
    several radii, charge centered and off-center."""
    q = 1.7
    E = e2d_point_charge(q)
    for r in (0.5, 1.0, 2.3):
        assert abs(flux2d(E, *circle_curve(r)) - 4.0*np.pi*q) < 1e-9
    E_off = e2d_point_charge(q, (0.2, -0.1))
    assert abs(flux2d(E_off, *circle_curve(1.0)) - 4.0*np.pi*q) < 1e-9


def test_e2d_flux_square():
    """1.5.1(a): the same 4 pi q through a square contour (contour-shape
    independence, as Gauss' theorem demands)."""
    q = -0.6
    E = e2d_point_charge(q, (0.2, -0.1))
    assert abs(square_flux2d(E) - 4.0*np.pi*q) < 1e-9


def test_e2d_nonenclosing_zero():
    """1.5.1(a): a contour NOT enclosing the charge captures zero flux."""
    E = e2d_point_charge(1.0, (3.0, 0.0))
    assert abs(flux2d(E, *circle_curve(1.0))) < 1e-9


def test_e2d_only_inverse_r():
    """1.5.1(a) uniqueness: for a trial rho^s rhohat the circle flux is
    2 pi r^(s+1) -- radius-independent ONLY for s = -1."""
    for r in (0.5, 1.0, 2.0):
        assert abs(powerlaw_flux2d(-1.0, r) - 2.0*np.pi) < 1e-9
    f1, f2 = powerlaw_flux2d(-0.5, 1.0), powerlaw_flux2d(-0.5, 2.0)
    assert abs(f2/f1 - 2.0**0.5) < 1e-6     # grows like r^{1/2}
    g1, g2 = powerlaw_flux2d(-2.0, 1.0), powerlaw_flux2d(-2.0, 2.0)
    assert abs(g2/g1 - 0.5) < 1e-6          # falls like r^{-1}


def test_e2d_div_free_away():
    """1.5.1(a): away from the charge, div E = 0 (the 2-D Coulomb law with
    sigma = 0 there)."""
    E = e2d_point_charge(1.3)
    for p in ((1.0, 0.4), (-0.8, 0.9), (0.3, -1.5)):
        assert abs(fd_div2d(E, np.array(p), h=1e-3)) < 1e-8


def _F2d(p):
    x, y = p
    return np.array([x*y - y*y + np.sin(y), x + x*x*y - np.cos(x)])


def test_2d_gauss_stokes_pointwise():
    """1.5.1(b), differential layer: div(A x zhat) = (curl A).zhat and
    (curl(zhat x A)).zhat = div A at random points."""
    Fr, Fz = cross_z_2d(_F2d), zcross_2d(_F2d)
    for p in _pts(12, dim=2):
        assert abs(fd_div2d(Fr, p, h=0.01) - fd_curlz2d(_F2d, p, h=0.01)) < 1e-8
        assert abs(fd_curlz2d(Fz, p, h=0.01) - fd_div2d(_F2d, p, h=0.01)) < 1e-8


def test_2d_gauss_stokes_integral():
    """1.5.1(b), integral layer: on the unit disc, 2-D Gauss holds for A x zhat
    and equals 2-D Stokes for A term by term:
    int div(A x zhat) = oint (A x zhat).nhat dl = oint A.dl = int (curl A).z."""
    Fr = cross_z_2d(_F2d)
    g_area, g_line = gauss2d_sides(Fr)
    s_area, s_line = stokes2d_sides(_F2d)
    assert abs(g_area - g_line) < 1e-8      # 2-D Gauss theorem itself
    assert abs(s_area - s_line) < 1e-8      # 2-D Stokes theorem itself
    assert abs(g_line - s_line) < 1e-10     # rotated flux IS the circulation
    assert abs(g_area - s_area) < 1e-8      # rotated divergence IS the curl
    assert abs(s_line) > 0.3                # nontrivial value (~0.376)


# =========================== P8 -- Exercise A.1.1 ===========================

def test_table_a1_values():
    """A.1.1: all 15 Table A.1 Factors, computed from alpha/beta/eps0, equal
    the printed Values (10^p c^pc)."""
    for name in TABLE_A1:
        f, v = amount_factor(name), book_value(name)
        assert abs(f - v) < 1e-12 * abs(v), name


def test_table_a2_values():
    """A.1.1: all 15 Table A.2 Factors equal the printed Values."""
    for name in TABLE_A2:
        f, v = amount_factor(name), book_value(name)
        assert abs(f - v) < 1e-12 * abs(v), name


def test_known_unit_conversions():
    """A.1.1 physical spot checks: the factors are the SI sizes of the
    Gaussian units."""
    assert abs(statcoulomb_in_C() - 3.33564095e-10) < 1e-17
    assert abs(statvolt_in_V() - 299.792458) < 1e-9
    assert abs(gauss_in_tesla() - 1e-4) < 1e-19
    assert abs(maxwell_in_weber() - 1e-8) < 1e-22
    assert abs(oersted_in_A_per_m() - 1000.0/(4.0*np.pi)) < 1e-9
    assert abs(cm_in_farad() - 1.11265006e-12) < 1e-19
    assert abs(s_per_cm_in_ohm() - 8.98755179e11) < 1e3


# =========================== P9 -- Exercise A.1.2 ===========================

def test_mks_gaussian_unit_sizes():
    """A.1.2: the MKS-Gaussian unit sizes close consistently both ways:
    charge sqrt(alpha beta) statC <-> sqrt(4 pi eps0) C reproduces the direct
    statC->C factor; field sqrt(10) G <-> sqrt(mu0/4pi) T reproduces G->T."""
    assert abs(mksg_charge_unit_in_statC() - 10.0**4.5) < 1e-6
    assert abs(mksg_charge_unit_in_C() - 10.0**3.5/C_NUM) < 1e-19
    # two-step route == direct Table A.1 charge factor
    two_step = mksg_charge_unit_in_C() / mksg_charge_unit_in_statC()
    assert abs(two_step - amount_factor('charge')) < 1e-22
    # field: sqrt(10) G at 1e-4 T/G == sqrt(mu0/4pi) T
    assert abs(mksg_field_unit_in_gauss() - np.sqrt(10.0)) < 1e-12
    assert abs(mksg_field_unit_in_gauss()*1e-4 - mksg_bfield_unit_in_tesla()) < 1e-16


def test_electron_charge_roundtrip():
    """A.1.2: e = 4.80320450e-10 statC -> MKS-Gaussian -> coulombs lands on
    CODATA 1.602176634e-19 C (path never uses the direct statC->C factor)."""
    e_si = electron_charge_via_mksg()
    assert abs(e_si - E_CODATA_C) / E_CODATA_C < 1e-7
    # and agrees exactly with the direct Table A.1 route
    assert abs(e_si - E_STATC * amount_factor('charge')) < 1e-30


# ---------------------------------------------------------------------------

def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
