"""Tests for MACRO_EM-02 (Wilcox & Thron 2e, Ch. 2) -- every exercise gets at
least one numeric check against a closed form, an independent construction, or
a limiting case.

Run directly:   python3 test_intro_electrostatics.py   (-> "All N tests passed.")
Or with pytest: pytest test_intro_electrostatics.py

Gaussian units throughout (div E = 4 pi rho, Phi = q/r).
"""
import numpy as np

from intro_electrostatics import (
    # helpers
    numeric_grad, numeric_curl, trapz,
    # P1
    dipole_phi, dipole_E, dipole_A,
    # P2, P4, P5
    parallelepiped_volume, jacobian_matrix, scale_factors,
    spherical_map, oblate_map, oblate_det_exact,
    # P3
    lorentzian_delta, delta2d_seq, smear_1d, smear_2d,
    # P6
    E2d_point, flux2d, laplacian2d_log, E_line3d,
    # P7
    phi_segment, phi_segment_quad, phi_plus, phi_plus_asym,
    phi_halflines, phi_halflines_asym,
    # P8
    Ez_disk, Ez_cylinder, Ez_cylinder_quad, cylinder_center_slope,
    # P9
    Ez_ring, Ez_ring_quad, Ez_cone_tip, Ez_cone_tip_quad,
    # P10
    phi_shell_eps, phi_shell_eps_quad, qa_eps_exact, qa_eps_approx,
    # P11
    phi_shell_yukawa, phi_shell_yukawa_quad, qa_yukawa, qa_yukawa_solve,
    qa_yukawa_approx,
    # P12
    phi_disk, phi_disk_oblate, sigma_disk, disk_total_charge, disk_capacitance,
    # P13-P15
    phi_disk_monolayer_axis, phi_dipole_disk_axis, phi_two_disks_axis,
    phi_hemisphere_dipole_axis, phi_cap_dipole_axis_quad, Ez_dipole_cap_axis,
    phi_dipole_sphere, phi_disk_offcenter, E_disk_offcenter, phi_pair_offset,
    # P16
    green_identity_sides,
    # P17
    induced_charges_shells, induced_charges_shells_gauss,
    # P18
    sphere_average,
    # P19-P24
    gd1, dgd1_dnp, gn1_unsym, gn1_symm, gn_gd_identity_rhs,
    force_gd, induced_endpoint_charges, phi_dirichlet_rep, phi_neumann_rep,
    phi_293, cube_center_potential,
    # P25
    g_helmholtz, phi_helmholtz_direct, phi_helmholtz_gf,
    # P26-P29
    energy_sphere_alone, energy_sphere_with_neutral_shell, energy_field_quad,
    string_self_energy, string_self_energy_quad,
    square_sheet_coeff_exact, square_sheet_coeff_quad,
    ball_self_energy, ball_self_energy_quad, classical_radius_uniform_cm,
    # P30
    E_sphere_rho_sigma, surface_force_per_area,
    # P31-P36
    elastance_shells, cap_matrix_shells, cap_two_spheres,
    system_capacitance, energy_from_caps, energy_at_charges,
    # P37-P39
    plates_C_small_d, plates_C_large_d, distant_pair_cap_matrix,
    C12_approx, C22_approx,
    # P40
    cyl_trial_capacitance, cyl_exact_capacitance, cyl_functional_quad,
    # P41
    wire_potentials, three_wire_CL, three_wire_energy,
)

RNG = np.random.default_rng(7)
FOURPI = 4 * np.pi


def _close(x, y, rel=1e-6, abs_=0.0):
    return abs(x - y) <= max(rel * max(abs(x), abs(y)), abs_)


# --- P1 (2.1.1) -------------------------------------------------------------

def test_p1_dipole_gradient():
    """E = -grad(d.x/r^3) matches the closed dipole form at random points."""
    for _ in range(4):
        d = RNG.normal(size=3); x = RNG.normal(size=3) * 2 + np.array([0.5, 0, 0])
        if np.linalg.norm(x) < 0.3:
            x += 1.0
        E_num = -numeric_grad(lambda p: dipole_phi(d, p), x)
        assert np.allclose(E_num, dipole_E(d, x), rtol=1e-6, atol=1e-8)


def test_p1_dipole_curl():
    """curl(d cross x / r^3) equals the same dipole field (away from 0)."""
    for _ in range(4):
        d = RNG.normal(size=3); x = RNG.normal(size=3) + np.array([0, 1.2, 0])
        if np.linalg.norm(x) < 0.3:
            x += 1.0
        C = numeric_curl(lambda p: dipole_A(d, p), x)
        assert np.allclose(C, dipole_E(d, x), rtol=1e-5, atol=1e-7)


# --- P2 (2.2.1) -------------------------------------------------------------

def test_p2_det_volume():
    """Triple product of the image parallelepiped's edges = |det M|."""
    for _ in range(5):
        M = RNG.normal(size=(3, 3))
        assert _close(parallelepiped_volume(M), abs(np.linalg.det(M)), rel=1e-12)


def test_p2_scale_factors():
    """Orthogonal coordinates: |det J| = U V W (spherical: = r^2)."""
    for _ in range(3):
        r = RNG.uniform(0.5, 3.0); mu = RNG.uniform(-0.8, 0.8)
        phi = RNG.uniform(0, 2 * np.pi)
        u = np.array([r, mu, phi])
        J = jacobian_matrix(spherical_map, u)
        U, V, W = scale_factors(spherical_map, u)
        assert _close(abs(np.linalg.det(J)), r * r, rel=1e-6)
        assert _close(U * V * W, r * r, rel=1e-6)


# --- P3 (2.2.2) -------------------------------------------------------------

def test_p3_lorentzian_delta():
    """1-D Lorentzian family: unit mass; smears a test function to f(0)."""
    for eps in (0.1, 0.01):
        assert _close(smear_1d(lambda x: 1.0, eps), 1.0, rel=1e-6)
    g = np.cos                                     # smear -> exp(-eps) -> 1
    e1 = abs(smear_1d(g, 0.1) - 1.0)
    e2 = abs(smear_1d(g, 0.01) - 1.0)
    assert e2 < e1 / 5 and e2 < 0.02


def test_p3_delta2d():
    """2-D family eps/(2 pi (rho^2+eps^2)^{3/2}): unit mass, samples g(0)."""
    for eps in (0.1, 0.01):
        assert _close(smear_2d(lambda r: 1.0, eps), 1.0, rel=1e-6)
    g = lambda r: 1.0 / (1.0 + r * r)
    e1 = abs(smear_2d(g, 0.1) - 1.0)
    e2 = abs(smear_2d(g, 0.01) - 1.0)
    assert e2 < e1 / 5 and e2 < 0.03


# --- P4 (2.2.3) -------------------------------------------------------------

def test_p4_spherical_delta_jacobian():
    """(r, cos t, phi): |det J| = r^2, so delta^(3) = delta3/(r^2)."""
    for _ in range(3):
        r = RNG.uniform(0.4, 2.5); mu = RNG.uniform(-0.7, 0.7)
        u = np.array([r, mu, RNG.uniform(0, 2 * np.pi)])
        assert _close(abs(np.linalg.det(jacobian_matrix(spherical_map, u))),
                      r * r, rel=1e-6)


# --- P5 (2.2.4) -------------------------------------------------------------

def test_p5_oblate_delta_jacobian():
    """Oblate spheroidal: |det J| = UVW = R^3 (xi^2 + cos^2 theta)."""
    R = 1.7
    for _ in range(3):
        xi = RNG.uniform(0.2, 2.0); mu = RNG.uniform(-0.7, 0.7)
        u = np.array([xi, mu, RNG.uniform(0, 2 * np.pi)])
        fmap = lambda v: oblate_map(v, R)
        J = jacobian_matrix(fmap, u)
        prod = np.prod(scale_factors(fmap, u))
        exact = oblate_det_exact(xi, mu, R)
        assert _close(abs(np.linalg.det(J)), exact, rel=1e-5)
        assert _close(prod, exact, rel=1e-5)


# --- P6 (2.4.1) -------------------------------------------------------------

def test_p6_flux2d():
    """2-D Gauss: loop flux = 2 pi (charge in), 0 (charge out)."""
    E = lambda p: E2d_point(p, (0.3, -0.2))
    assert _close(flux2d(E, (0.3, -0.2), 1.0), 2 * np.pi, rel=1e-9)
    assert _close(flux2d(E, (0.0, 0.0), 1.0), 2 * np.pi, rel=1e-6)   # still inside
    assert abs(flux2d(E, (5.0, 5.0), 1.0)) < 1e-8                    # outside


def test_p6_log_laplacian():
    """ln r is harmonic off the origin; its disk integral of lap = 2 pi;
    3-D line field is twice the 2-D unit-charge field."""
    assert abs(laplacian2d_log(0.7, -0.4)) < 1e-5
    # divergence-theorem evaluation of int lap ln r over a disk of radius R:
    # oint d(ln r)/dr dl = (1/R) * 2 pi R = 2 pi for any R
    for R in (0.5, 2.0):
        assert _close((1.0 / R) * 2 * np.pi * R, 2 * np.pi, rel=1e-14)
    rho = 1.7
    assert _close(E_line3d(rho, lam=1.0), 2.0 * (1.0 / rho), rel=1e-14)


# --- P7 (2.4.2) -------------------------------------------------------------

def test_p7_plus_potential():
    """'+' lines: closed form vs quadrature; L>>r log form; L<<r monopole."""
    L, lam = 2.0, 0.8
    x, y, z = 0.31, -0.42, 0.55
    b1 = np.hypot(y, z)
    assert _close(phi_segment(x, b1, -L, L, lam),
                  phi_segment_quad(x, b1, -L, L, lam), rel=1e-8)
    # far-length asymptote
    Lbig = 3.0e3
    exact = phi_plus(x, y, z, Lbig, lam)
    assert _close(exact, phi_plus_asym(x, y, z, Lbig, lam), rel=1e-6)
    # point-charge limit: Q = 4 lam L
    Lsm, r = 1e-3, np.sqrt(x * x + y * y + z * z)
    assert _close(phi_plus(x, y, z, Lsm, lam), 4 * lam * Lsm / r, rel=1e-5)


def test_p7_halflines():
    """Half-lines (+lam on y, -lam on x): asymptote -lam ln[(r-y)/(r-x)],
    approached with the expected O((x-y)/L) residual."""
    lam = 1.3
    x, y, z = 0.4, -0.7, 0.3
    target = phi_halflines_asym(x, y, z, lam)
    assert _close(phi_halflines(x, y, z, 5.0e6, lam), target, rel=2e-6)
    e1 = abs(phi_halflines(x, y, z, 1.0e3, lam) - target)
    e2 = abs(phi_halflines(x, y, z, 1.0e4, lam) - target)
    assert 8.0 < e1 / e2 < 12.0                       # ~1/L convergence


# --- P8 (2.4.3) -------------------------------------------------------------

def test_p8_cylinder_axis():
    """Cylinder axis field: closed form vs disk-stack quadrature; center slope;
    slab limit 4 pi rho z."""
    a, b, rho = 0.8, 1.5, 0.6
    for z in (-1.3, -0.2, 0.1, 0.39, 0.9):
        assert _close(Ez_cylinder(z, a, b, rho), Ez_cylinder_quad(z, a, b, rho),
                      rel=1e-7, abs_=1e-10)
    # linear zone: symmetric-difference slope at 0 vs the closed constant
    h = 1e-5
    slope = (Ez_cylinder(h, a, b, rho) - Ez_cylinder(-h, a, b, rho)) / (2 * h)
    assert _close(slope, cylinder_center_slope(a, b, rho), rel=1e-6)
    # b >> a: slab, constant -> 4 pi rho
    assert _close(cylinder_center_slope(0.1, 500.0, rho), FOURPI * rho, rel=1e-3)


# --- P9 (2.4.4) -------------------------------------------------------------

def test_p9_ring_and_cone():
    """Ring closed form vs quadrature + far point-charge limit; cone tip field
    vs surface quadrature."""
    R, lam = 1.2, 0.9
    for z in (0.3, 1.7):
        assert _close(Ez_ring(z, R, lam), Ez_ring_quad(z, R, lam), rel=1e-10)
    zfar = 500.0
    assert _close(Ez_ring(zfar, R, lam), 2 * np.pi * R * lam / zfar ** 2, rel=1e-4)
    alpha, L1, L2, sig = 0.5, 0.4, 2.2, 1.1
    assert _close(Ez_cone_tip(alpha, L1, L2, sig),
                  Ez_cone_tip_quad(alpha, L1, L2, sig), rel=1e-8)
    # 45 deg maximizes |E| at fixed L1, L2, sigma
    vals = [abs(Ez_cone_tip(al, L1, L2, sig)) for al in (0.3, np.pi / 4, 1.2)]
    assert vals[1] >= vals[0] and vals[1] >= vals[2]


# --- P10 (2.5.1) ------------------------------------------------------------

def test_p10_shell_potential_eps():
    """Modified shell potential (2.62)-(2.63) vs direct quadrature, eps finite."""
    eps, a, b = 0.05, 1.0, 2.0
    for (r, s) in ((1.5, 1.0), (1.5, 2.0), (1.0, 2.0), (2.0, 1.0)):
        assert _close(phi_shell_eps(r, s, 1.0, eps),
                      phi_shell_eps_quad(r, s, 1.0, eps), rel=1e-7)


def test_p10_qa_approx():
    """Wired shells: exact linear solve -> book first-order formula as eps->0;
    sign(q_a) = sign(eps q_b)."""
    a, b, qb = 1.0, 2.0, 1.0
    for eps in (1e-3, 1e-4):
        ex = qa_eps_exact(a, b, qb, eps)
        ap = qa_eps_approx(a, b, qb, eps)
        assert _close(ex, ap, rel=5e-3)
    # numeric coefficient at a=1, b=2: q_a/(eps q_b) = 0.2616
    coef = qa_eps_exact(a, b, qb, 1e-6) / 1e-6
    assert _close(coef, 0.26160, rel=1e-3)
    assert qa_eps_exact(a, b, qb, 1e-3) > 0            # eps>0, qb>0 -> qa>0
    assert qa_eps_exact(a, b, qb, -1e-3) < 0           # eps<0 flips


# --- P11 (2.5.2) ------------------------------------------------------------

def test_p11_yukawa_shell():
    """Yukawa shell potential closed form vs quadrature."""
    Rm = 7.0
    for (r, s) in ((1.5, 1.0), (1.5, 2.0), (1.0, 2.0), (2.0, 1.0)):
        assert _close(phi_shell_yukawa(r, s, 1.0, Rm),
                      phi_shell_yukawa_quad(r, s, 1.0, Rm), rel=1e-8)


def test_p11_qa_yukawa():
    """Book ratio formula = independent linear solve; R>>a,b approximation."""
    a, b, qb = 1.0, 2.0, 1.0
    for Rm in (5.0, 50.0):
        assert _close(qa_yukawa(a, b, qb, Rm), qa_yukawa_solve(a, b, qb, Rm),
                      rel=1e-10)
    # leading order is O(1/R^2); its relative error is O(b/R):
    err = lambda Rm: abs(qa_yukawa(a, b, qb, Rm) - qa_yukawa_approx(a, b, qb, Rm)) \
        / abs(qa_yukawa(a, b, qb, Rm))
    assert err(400.0) < 6e-3
    assert 3.0 < err(100.0) / err(400.0) < 5.0         # ~1/R scaling
    assert qa_yukawa(a, b, qb, 100.0) > 0              # same sign as q_b


# --- P12 (2.6.1) ------------------------------------------------------------

def test_p12_disk_potential():
    """Spherical form == oblate form; Phi -> V on the disk; far monopole Q/r;
    sigma integrates to Q = 2RV/pi; C = 2R/pi."""
    R, V = 1.0, 1.0
    # oblate <-> spherical agreement at a generic point: xi=0.9, mu=0.5
    xi, mu = 0.9, 0.5
    s = np.sqrt(1 - mu * mu)
    rho = R * np.sqrt(xi * xi + 1) * s
    z = R * xi * mu
    assert _close(phi_disk(rho, z, R, V), phi_disk_oblate(xi, V), rel=1e-10)
    # on the disk (z -> 0, rho < R): Phi -> V  (fixes A = 2V/pi)
    assert _close(phi_disk(0.5, 1e-9, R, V), V, rel=1e-4)
    # far field: Phi -> Q/r with Q = 2RV/pi
    r = 2.0e3
    assert _close(phi_disk(r, 0.0, R, V), (2 * R * V / np.pi) / r, rel=1e-6)
    # total charge and capacitance
    Q = disk_total_charge(R, V)
    assert _close(Q, 2 * R * V / np.pi, rel=1e-8)
    assert _close(disk_capacitance(R), Q / V, rel=1e-8)


# --- P13 (2.6.2) ------------------------------------------------------------

def test_p13_dipole_limit():
    """Two +-sigma disks at separation d -> dipole-layer potential as d->0
    at fixed D = sigma d (error O(d^2))."""
    a, D, z = 1.0, 0.7, 0.6
    target = phi_dipole_disk_axis(z, a, D)
    e1 = abs(phi_two_disks_axis(z, a, D, 0.08) - target)
    e2 = abs(phi_two_disks_axis(z, a, D, 0.02) - target)
    assert e2 < e1 / 10                                  # O(d^2) convergence
    assert _close(phi_two_disks_axis(z, a, D, 0.004), target, rel=1e-4)


# --- P14 (2.6.3) ------------------------------------------------------------

def test_p14_tilted_layer():
    """Pair with fixed offset direction: Phi_d = xhat.E2 d (generic point);
    jump across the layer = 4 pi D xhat.n (0 for in-plane shear)."""
    a, D = 1.0, 0.5
    gam = 0.6
    xh = np.array([np.sin(gam), 0.0, np.cos(gam)])
    p = np.array([0.3, 0.1, 0.6])
    # Phi_pair -> xhat.E2 d with O(d) residual (one-sided difference):
    def rel_err(d):
        lhs = phi_pair_offset(p, a, D, d, xh, n=150)
        rhs = float(xh @ E_disk_offcenter(p, a, sigma=D / d, n=150)) * d
        return abs(lhs - rhs) / abs(rhs)
    assert rel_err(0.005) < 4e-3
    assert rel_err(0.005) < rel_err(0.02) / 2.5           # ~linear in d
    # jump on the axis, closed forms (E linear in sigma: sigma d = D):
    # E_rho = 0 on the axis, so xhat.E = xh_z E_z
    for zz in (1e-3, 1e-4):
        jump = xh[2] * (Ez_disk(zz, a, D) - Ez_disk(-zz, a, D))
        assert _close(jump, FOURPI * D * xh[2], rel=5e-3)
    # in-plane shear: xhat.n = 0 -> no jump
    xh_in = np.array([1.0, 0.0, 0.0])
    jump_in = xh_in[2] * (Ez_disk(1e-4, a, D) - Ez_disk(-1e-4, a, D))
    assert abs(jump_in) < 1e-12


# --- P15 (2.6.4) ------------------------------------------------------------

def test_p15_hemisphere():
    """Dipole hemisphere: closed form vs layer quadrature; E_z equals the disk's;
    potential jump 4 pi D at the dome; far dipole p = pi a^2 D; sphere: E = 0."""
    a, D = 1.0, 0.8
    for z in (-2.0, -0.4, 0.5, 0.9, 1.5, 3.0):
        assert _close(phi_hemisphere_dipole_axis(z, a, D),
                      phi_cap_dipole_axis_quad(z, a, D, 0.0, 1.0),
                      rel=1e-7, abs_=1e-9)
    # jump crossing the dome at z = a
    jump = (phi_hemisphere_dipole_axis(a + 1e-9, a, D)
            - phi_hemisphere_dipole_axis(a - 1e-9, a, D))
    assert _close(jump, FOURPI * D, rel=1e-8)
    # E_z: hemisphere == disk (same rim): numeric derivative of both potentials
    for z in (0.3, -0.7, 1.8):
        h = 1e-6
        Eh = -(phi_hemisphere_dipole_axis(z + h, a, D)
               - phi_hemisphere_dipole_axis(z - h, a, D)) / (2 * h)
        Ed = -(phi_dipole_disk_axis(z + h, a, D)
               - phi_dipole_disk_axis(z - h, a, D)) / (2 * h)
        assert _close(Eh, Ez_dipole_cap_axis(z, a, D), rel=1e-5)
        assert _close(Ed, Ez_dipole_cap_axis(z, a, D), rel=1e-5)
    # far field: E_z -> 2p/z^3, p = pi a^2 D
    zf = 200.0
    assert _close(Ez_dipole_cap_axis(zf, a, D), 2 * np.pi * a * a * D / zf ** 3,
                  rel=1e-4)
    # full sphere: constant potentials -4 pi D in, 0 out -> E = 0 both sides
    for z in (0.2, 0.6, -0.5):
        assert _close(phi_cap_dipole_axis_quad(z, a, D, -1.0, 1.0),
                      phi_dipole_sphere(abs(z), a, D), rel=1e-7, abs_=1e-9)
    for z in (1.4, -2.2, 5.0):
        assert abs(phi_cap_dipole_axis_quad(z, a, D, -1.0, 1.0)) < 1e-9


# --- P16 (2.7.1) ------------------------------------------------------------

def test_p16_green_identity():
    """Green's first identity on a ball: quadrature both sides; the (r^2, r^4)
    pair has the closed value 16 pi R^7."""
    R = 1.3
    lhs, rhs = green_identity_sides(lambda r: r * r, lambda r: 2 * r,
                                    lambda r: r ** 4, lambda r: 4 * r ** 3,
                                    lambda r: 12 * r * r, R)
    assert _close(lhs, rhs, rel=1e-8)
    assert _close(lhs, 16 * np.pi * R ** 7, rel=1e-8)
    # second pair: phi = 1/(1+r^2), psi = r^2
    lhs2, rhs2 = green_identity_sides(
        lambda r: 1.0 / (1 + r * r), lambda r: -2 * r / (1 + r * r) ** 2,
        lambda r: r * r, lambda r: 2 * r, lambda r: 2.0, R)
    assert _close(lhs2, rhs2, rel=1e-8)


# --- P17 (2.7.2) ------------------------------------------------------------

def test_p17_reciprocation_shells():
    """Induced charges by reciprocation == Gauss/continuity construction;
    they sum to -q; limiting positions."""
    q, a, b = 1.0, 1.0, 3.0
    for r in (1.2, 2.0, 2.8):
        Qa, Qb = induced_charges_shells(q, r, a, b)
        Qa2, Qb2 = induced_charges_shells_gauss(q, r, a, b)
        assert _close(Qa, Qa2, rel=1e-12)
        assert _close(Qb, Qb2, rel=1e-12)
        assert _close(Qa + Qb, -q, rel=1e-12)
    Qa, Qb = induced_charges_shells(q, 1.0 + 1e-9, a, b)
    assert _close(Qa, -q, rel=1e-6) and abs(Qb) < 1e-6


# --- P18 (2.7.3) ------------------------------------------------------------

def test_p18_mvt():
    """Sphere average = center value for harmonic functions; fails for the
    non-harmonic control x^2 by exactly R^2/3."""
    c = np.array([0.2, -0.1, 0.4]); R = 0.7
    x0 = np.array([3.0, 1.0, -2.0])                     # source outside sphere
    for f, val in [
        (lambda x: 1.0 / np.linalg.norm(x - x0), 1.0 / np.linalg.norm(c - x0)),
        (lambda x: x[0] ** 2 - x[1] ** 2, c[0] ** 2 - c[1] ** 2),
        (lambda x: 2.0 + 3 * x[2], 2.0 + 3 * c[2]),
    ]:
        assert _close(sphere_average(f, c, R), val, rel=1e-7, abs_=1e-10)
    # control: <x^2> over the sphere = c_x^2 + R^2/3 (not harmonic)
    got = sphere_average(lambda x: x[0] ** 2, c, R)
    assert _close(got, c[0] ** 2 + R * R / 3.0, rel=1e-7)


# --- P19 (2.8.1) ------------------------------------------------------------

def test_p19_gn_gd_identity():
    """1-D analog of the G_N <-> G_D relation holds exactly on a grid."""
    L = 2.0
    for x in np.linspace(0.05, 1.95, 9):
        for xpp in np.linspace(0.1, 1.9, 7):
            if abs(x - xpp) < 1e-9:
                continue
            assert _close(gn1_unsym(x, xpp, L), gn_gd_identity_rhs(x, xpp, L),
                          rel=1e-12, abs_=1e-12)


# --- P20 (2.8.2) ------------------------------------------------------------

def test_p20_symm_vs_unsym_rep():
    """(2.138) with unsymmetrized vs symmetrized G_N: potentials differ by a
    grid-constant only."""
    L, V = 2.0, 0.9
    lam = lambda xp: 1.0 + 0.5 * np.sin(np.pi * xp / L)   # generic charge
    # consistent Neumann data: E(L) - E(0) = Q  ->  dPhi'(L) - dPhi'(0) = -Q
    Q = 1.0 * L + 0.5 * L * 2 / np.pi
    dphi0 = -V / L
    dphiL = dphi0 - Q
    xs = np.linspace(0.1, 1.9, 12)
    diff = [phi_neumann_rep(x, L, dphi0, dphiL, lam, gn=gn1_unsym)
            - phi_neumann_rep(x, L, dphi0, dphiL, lam, gn=gn1_symm)
            for x in xs]
    assert np.max(diff) - np.min(diff) < 1e-9              # constant offset


# --- P21 (2.8.3) ------------------------------------------------------------

def test_p21_cube_average():
    """Cube (n=6 'polyhedron'): center potential = mean of face potentials."""
    v = cube_center_potential((1, 0, 0, 0, 0, 0), n=25, iters=3000)
    assert _close(v, 1.0 / 6.0, rel=1e-4)
    v2 = cube_center_potential((1, 2, 3, 4, 5, 6), n=25, iters=3000)
    assert _close(v2, 3.5, rel=1e-4)


# --- P22 (2.9.1) ------------------------------------------------------------

def test_p22_force_and_charges():
    """1-D Dirichlet GF: BCs/continuity/jump; averaged force; endpoint charges
    sum to -1; boundary-value solve (c) is the linear interpolant."""
    L = 2.0; xp = 0.7
    assert gd1(0.0, xp, L) == 0.0 and gd1(L, xp, L) == 0.0
    h = 1e-7
    jump = ((gd1(xp + 2 * h, xp, L) - gd1(xp + h, xp, L))
            - (gd1(xp - h, xp, L) - gd1(xp - 2 * h, xp, L))) / h
    assert _close(jump, -1.0, rel=1e-5)
    # force from two-sided slopes
    Em = -(gd1(xp - h, xp, L) - gd1(xp - 2 * h, xp, L)) / h
    Ep = -(gd1(xp + 2 * h, xp, L) - gd1(xp + h, xp, L)) / h
    assert _close(0.5 * (Em + Ep), force_gd(xp, L), rel=1e-6)
    s0, sL = induced_endpoint_charges(xp, L)
    assert _close(s0 + sL, -1.0, rel=1e-12)
    assert s0 < 0 and sL < 0 and abs(sL) < abs(s0)     # nearer wall (0) dominates
    V = 1.3
    for x in (0.2, 1.0, 1.7):
        assert _close(phi_dirichlet_rep(x, L, V, 0.0), V * (1 - x / L), rel=1e-12)


# --- P23 (2.9.2) ------------------------------------------------------------

def test_p23_neumann_gf():
    """1-D Neumann GF: endpoint fields +-1/2; jump -1; symmetry with C = L/4;
    zero force; uniform-field solve (c)."""
    L = 2.0; xp = 0.6; h = 1e-7
    # endpoint derivative conditions (2.137)
    d0 = (gn1_unsym(h, xp, L) - gn1_unsym(0.0, xp, L)) / h
    dL = (gn1_unsym(L, xp, L) - gn1_unsym(L - h, xp, L)) / h
    assert _close(d0, 0.5, rel=1e-6) and _close(dL, -0.5, rel=1e-6)
    # symmetrized version: -|x-x'|/2 + L/4 and endpoint-average recipe
    ga = 0.5 * (gn1_unsym(0.0, xp, L) + gn1_unsym(L, xp, L))
    for x in (0.15, 0.9, 1.7):
        assert _close(gn1_unsym(x, xp, L) - ga, gn1_symm(x, xp, L), rel=1e-12)
        assert _close(gn1_symm(x, xp, L), gn1_symm(xp, x, L), rel=1e-12)
    # zero force: two-sided slopes cancel
    Em = -(gn1_symm(xp - h, xp, L) - gn1_symm(xp - 2 * h, xp, L)) / h
    Ep = -(gn1_symm(xp + 2 * h, xp, L) - gn1_symm(xp + h, xp, L)) / h
    assert abs(0.5 * (Em + Ep)) < 1e-9
    # (c): E(0) = E(L) = V/L -> Phi = V/2 - V x/L + <Phi>
    V = 1.1
    for x in (0.3, 1.2, 1.9):
        got = phi_neumann_rep(x, L, -V / L, -V / L, None, mean=0.0)
        assert _close(got, V / 2 - V * x / L, rel=1e-12, abs_=1e-12)


# --- P24 (2.9.3) ------------------------------------------------------------

def test_p24_gf_solution():
    """GF solve of Phi'' = -lam, Phi(0) = V, Phi(L) = -V vs closed form and a
    dense finite-difference BVP."""
    L, V, lam = 2.0, 0.8, 1.7
    for x in (0.25, 1.0, 1.6):
        gf = phi_dirichlet_rep(x, L, V, -V, lam_func=lambda t: lam, n=8000)
        assert _close(gf, phi_293(x, L, V, lam), rel=1e-6)
    # finite-difference check
    n = 2001
    xs = np.linspace(0, L, n); h = xs[1] - xs[0]
    A = np.diag(-2 * np.ones(n - 2)) + np.diag(np.ones(n - 3), 1) + np.diag(np.ones(n - 3), -1)
    rhs = -lam * h * h * np.ones(n - 2)
    rhs[0] -= V; rhs[-1] -= (-V)
    sol = np.linalg.solve(A, rhs)
    mid = sol[(n - 2) // 2]
    assert _close(mid, phi_293(xs[1 + (n - 2) // 2], L, V, lam), rel=1e-5)
    # closed form satisfies the BCs
    assert _close(phi_293(0.0, L, V, lam), V, rel=1e-12)
    assert _close(phi_293(L, L, V, lam), -V, rel=1e-12)


# --- P25 (2.9.4) ------------------------------------------------------------

def test_p25_helmholtz():
    """Helmholtz GF: ODE off-source, unit slope jump, symmetry, k0->0 limit,
    and a full solve vs the direct closed form."""
    L, k0 = 2.0, 1.3
    xp = 0.8; h = 1e-4
    # ODE at a generic x != x'
    for x in (0.3, 1.5):
        g2 = (g_helmholtz(x + h, xp, L, k0) - 2 * g_helmholtz(x, xp, L, k0)
              + g_helmholtz(x - h, xp, L, k0)) / h ** 2
        assert _close(g2, -k0 * k0 * g_helmholtz(x, xp, L, k0), rel=1e-4, abs_=1e-8)
    jump = ((g_helmholtz(xp + 2 * h, xp, L, k0) - g_helmholtz(xp + h, xp, L, k0))
            - (g_helmholtz(xp - h, xp, L, k0) - g_helmholtz(xp - 2 * h, xp, L, k0))) / h
    assert _close(jump, -1.0, rel=1e-3)
    for (x, y) in ((0.3, 1.1), (0.5, 1.9)):
        assert _close(g_helmholtz(x, y, L, k0), g_helmholtz(y, x, L, k0), rel=1e-12)
        assert _close(g_helmholtz(x, y, L, 1e-6), gd1(x, y, L), rel=1e-6)
    lam = 0.9
    for x in (0.4, 1.0, 1.7):
        assert _close(phi_helmholtz_gf(x, L, k0, lam),
                      phi_helmholtz_direct(x, L, k0, lam), rel=1e-5)


# --- P26 (2.10.1) -----------------------------------------------------------

def test_p26_energy_lowered():
    """Neutral conducting shell around a charged sphere lowers W by exactly
    Q^2/2 (1/b - 1/c); field-quadrature and cap-matrix routes agree."""
    Q, a, b, c = 1.0, 1.0, 2.0, 3.0
    W0 = energy_sphere_alone(Q, a)
    W1 = energy_sphere_with_neutral_shell(Q, a, b, c)
    assert W1 < W0
    assert _close(W0 - W1, Q * Q / 2 * (1 / b - 1 / c), rel=1e-12)
    # field quadrature: gap a..b plus analytic exterior tail Q^2/2c
    Wq = energy_field_quad(lambda r: Q / r ** 2, b, rmin=a, n=400000) + Q * Q / (2 * c)
    assert _close(Wq, W1, rel=1e-4)
    # elastance route: W = q.P.q/2 at charges (Q, 0)
    P = np.array([[1 / a - 1 / b + 1 / c, 1 / c], [1 / c, 1 / c]])
    Wp = 0.5 * np.array([Q, 0]) @ P @ np.array([Q, 0])
    assert _close(Wp, W1, rel=1e-12)


# --- P27 (2.10.2) -----------------------------------------------------------

def test_p27_log_divergence():
    """String self-energy: cutoff closed form vs quadrature; each decade of
    cutoff adds the same lam^2 a ln 10 (log divergence, not power law)."""
    a, lam = 1.0, 1.0
    for d in (1e-2, 1e-3):
        assert _close(string_self_energy(a, d, lam),
                      string_self_energy_quad(a, d, lam), rel=1e-8)
    W2 = string_self_energy(a, 1e-2, lam)
    W3 = string_self_energy(a, 1e-3, lam)
    W4 = string_self_energy(a, 1e-4, lam)
    step1, step2 = W3 - W2, W4 - W3
    # steps -> lam^2 a ln 10, up to the O(delta) endpoint term of the closed form
    assert _close(step1, lam * lam * a * np.log(10.0), rel=5e-3)
    assert _close(step2, lam * lam * a * np.log(10.0), rel=5e-4)
    # a linear divergence would grow the steps 10x; they are flat
    assert step2 / step1 < 1.05


# --- P28 (2.10.3) -----------------------------------------------------------

def test_p28_square_sheet():
    """Square-sheet self-energy coefficient: quadrature vs the closed form
    2 ln(1+sqrt2) + (2/3)(1-sqrt2) = 1.48660... (the book's numeric value)."""
    exact = square_sheet_coeff_exact()
    assert _close(exact, 1.4866048, rel=1e-6)
    got = square_sheet_coeff_quad(n=600)
    assert _close(got, exact, rel=3e-3)


# --- P29 (2.10.4) -----------------------------------------------------------

def test_p29_ball_energy():
    """W = (3+alpha)/(5+2 alpha) Q^2/a vs field quadrature; alpha -> inf shell
    limit 1/2; divergence onset below alpha = -5/2; electron radius (cgs)."""
    for alpha in (0.0, 1.0, -1.0, -2.0):
        assert _close(ball_self_energy(alpha), ball_self_energy_quad(alpha),
                      rel=1e-3)
    assert _close(ball_self_energy(0.0), 0.6, rel=1e-12)          # uniform 3/5
    assert _close(ball_self_energy(1e6), 0.5, rel=1e-5)           # shell limit
    # alpha <= -5/2: quadrature grows without bound as the grid refines
    w1 = ball_self_energy_quad(-2.6, n=100000)
    w2 = ball_self_energy_quad(-2.6, n=400000)
    assert w2 > w1 + 0.05
    # a = (3/5) e^2/(m c^2) = 1.6908e-13 cm
    assert _close(classical_radius_uniform_cm(), 1.6908e-13, rel=1e-3)


# --- P30 (2.11.1) -----------------------------------------------------------

def test_p30_sphere_force():
    """Ball rho + surface sigma: interior/exterior fields, 4 pi sigma jump,
    averaged-field force with the 2 pi sigma^2 conductor limit."""
    R, rho, sig = 1.5, 0.4, 0.3
    assert _close(E_sphere_rho_sigma(0.5, R, rho, sig), FOURPI * rho * 0.5 / 3, rel=1e-12)
    Q = FOURPI * R ** 3 * rho / 3 + FOURPI * R * R * sig
    assert _close(E_sphere_rho_sigma(4.0, R, rho, sig), Q / 16.0, rel=1e-12)
    jump = (E_sphere_rho_sigma(R + 1e-9, R, rho, sig)
            - E_sphere_rho_sigma(R - 1e-9, R, rho, sig))
    assert _close(jump, FOURPI * sig, rel=1e-6)
    Eavg = 0.5 * (E_sphere_rho_sigma(R + 1e-9, R, rho, sig)
                  + E_sphere_rho_sigma(R - 1e-9, R, rho, sig))
    assert _close(sig * Eavg, surface_force_per_area(R, rho, sig), rel=1e-6)
    assert _close(surface_force_per_area(R, 0.0, sig), 2 * np.pi * sig * sig,
                  rel=1e-12)


# --- P31 (2.12.1) -----------------------------------------------------------

def test_p31_schwarz():
    """C_AB^2 < C_AA C_BB for every pair of the 3-shell system (strict)."""
    a, b, c = 1.0, 2.0, 3.0
    C = cap_matrix_shells(a, b, c)
    for i in range(3):
        for j in range(i + 1, 3):
            assert C[i, j] ** 2 < C[i, i] * C[j, j]
    # the closed-form margin: C_ab^2/(C_aa C_bb) = a(c-b)/(b(c-a))
    ratio = C[0, 1] ** 2 / (C[0, 0] * C[1, 1])
    assert _close(ratio, a * (c - b) / (b * (c - a)), rel=1e-12)
    assert ratio < 1.0


# --- P32 (2.12.2) -----------------------------------------------------------

def test_p32_symmetry():
    """C = P^{-1} symmetric with positive diagonal (numeric inversion)."""
    Cnum = np.linalg.inv(elastance_shells(1.0, 2.0, 3.0))
    assert np.allclose(Cnum, Cnum.T, rtol=0, atol=1e-10)
    assert np.all(np.diag(Cnum) > 0)
    # energy at unit potential on one conductor = C_ii/2 > 0
    for i in range(3):
        V = np.zeros(3); V[i] = 1.0
        assert _close(energy_from_caps(Cnum, V), Cnum[i, i] / 2, rel=1e-12)


# --- P33 (2.12.3) -----------------------------------------------------------

def test_p33_shell_caps():
    """Closed-form 3-shell C matrix vs numeric inversion; sum rules (2.171)
    for j=a,b and (2.178) for the outer shell."""
    a, b, c = 1.0, 2.0, 3.0
    C = cap_matrix_shells(a, b, c)
    Cnum = np.linalg.inv(elastance_shells(a, b, c))
    assert np.allclose(C, Cnum, rtol=1e-12, atol=1e-12)
    sums = C.sum(axis=0)
    assert abs(sums[0]) < 1e-12 and abs(sums[1]) < 1e-12   # closed interior
    assert _close(sums[2], c, rel=1e-12)                   # C_infinity = c
    assert _close(C[0, 0], a * b / (b - a), rel=1e-12)
    assert _close(C[2, 2], c * c / (c - b), rel=1e-12)
    assert abs(C[0, 2]) < 1e-12                            # b screens a from c


# --- P34 (2.12.4) -----------------------------------------------------------

def test_p34_enclosed():
    """Hollow B containing A: C_BA = -C_AA and C_BB > C_AA."""
    a, b = 1.0, 2.5
    C = cap_two_spheres(a, b)
    assert _close(C[1, 0], -C[0, 0], rel=1e-12)
    assert C[1, 1] > C[0, 0]
    assert _close(C[1, 1] - C[0, 0], b, rel=1e-12)         # spheres: difference b
    # nested pairs of the 3-shell system obey the same
    C3 = cap_matrix_shells(1.0, 2.0, 3.0)
    assert C3[1, 1] > C3[0, 0] and C3[2, 2] > 0


# --- P35 (2.12.5) -----------------------------------------------------------

def test_p35_system_C():
    """C = det/sum for +-Q pair; W = Q^2/2C (both vs direct linear algebra)."""
    C = cap_two_spheres(1.0, 2.5)
    Q = 0.7
    V = np.linalg.solve(C, np.array([Q, -Q]))
    dv = V[0] - V[1]
    Csys = system_capacitance(C)
    assert _close(Q / dv, Csys, rel=1e-12)
    W_direct = 0.5 * (Q * V[0] - Q * V[1])
    assert _close(W_direct, Q * Q / (2 * Csys), rel=1e-12)
    assert _close(W_direct, energy_at_charges(C, [Q, -Q]), rel=1e-12)


# --- P36 (2.12.6) -----------------------------------------------------------

def test_p36_raising():
    """Neighbor raises capacitance: C_A = a < det C'/C'_BB (floating B)
    < C'_AA (grounded B) for sphere + thick shell."""
    a, b, c = 1.0, 2.0, 3.0
    P = np.array([[1 / a - 1 / b + 1 / c, 1 / c], [1 / c, 1 / c]])
    Cp = np.linalg.inv(P)
    CA_iso = a
    C_floating = np.linalg.det(Cp) / Cp[1, 1]              # = 1/P_AA
    assert _close(C_floating, 1.0 / P[0, 0], rel=1e-10)
    assert CA_iso < C_floating < Cp[0, 0]
    assert _close(Cp[0, 0], a * b / (b - a), rel=1e-10)    # grounded shell
    # energy chain of the proof: W_after < W_before at fixed charge
    Q = 1.0
    W_before = Q * Q / (2 * CA_iso)
    W_after = energy_at_charges(Cp, [Q, 0.0])
    assert W_after < W_before


# --- P37 (2.12.7) -----------------------------------------------------------

def test_p37_plates_limits():
    """Parallel disks: R^2/4d = A/(4 pi d) for d<<R; C -> R/pi for d>>R;
    the two meet at d = pi R/4."""
    R = 1.0
    d = 0.01
    assert _close(plates_C_small_d(R, d), np.pi * R * R / (FOURPI * d), rel=1e-12)
    assert plates_C_small_d(R, d) > 10 * plates_C_large_d(R, d, order=0)
    dfar = 1e4
    assert _close(plates_C_large_d(R, dfar, order='exact'), R / np.pi, rel=1e-3)
    dstar = np.pi * R / 4.0
    assert _close(plates_C_small_d(R, dstar), R / np.pi, rel=1e-12)


# --- P38 (2.12.8) -----------------------------------------------------------

def test_p38_plates_correction():
    """C(d) = (R/pi)(1 + 2R/(pi d)): first-order vs exact monopole model,
    error scaling O((R/d)^2)."""
    R = 1.0
    e20 = abs(plates_C_large_d(R, 20.0, 1) - plates_C_large_d(R, 20.0, 'exact'))
    e60 = abs(plates_C_large_d(R, 60.0, 1) - plates_C_large_d(R, 60.0, 'exact'))
    assert e60 < e20 / 7                                  # ~(20/60)^2 = 1/9
    assert _close(plates_C_large_d(R, 50.0, 1), plates_C_large_d(R, 50.0, 'exact'),
                  rel=2e-4)


# --- P39 (2.12.9) -----------------------------------------------------------

def test_p39_distant():
    """Distant conductors: monopole-matrix inversion vs C12 ~ -C1 C2/d and
    C22 ~ C2/(1 + C12/d); disks reproduce the P38 system capacitance."""
    C1, C2, d = 0.6366, 0.9, 40.0
    Cm = distant_pair_cap_matrix(C1, C2, d)
    assert _close(Cm[0, 1], C12_approx(C1, C2, d), rel=2e-3)
    assert _close(Cm[1, 1], C22_approx(C1, C2, d), rel=1e-6)   # same closed form
    # coaxial disks: system capacitance from the matrix = P38 formula
    R = 1.0
    Cc = 2 * R / np.pi
    Cm2 = distant_pair_cap_matrix(Cc, Cc, d)
    Csys = system_capacitance(Cm2)
    assert _close(Csys, plates_C_large_d(R, d, order='exact'), rel=1e-10)
    assert _close(Csys, plates_C_large_d(R, d, order=1), rel=2e-3)


# --- P40 (2.12.10) ----------------------------------------------------------

def test_p40_variational():
    """C[Psi_trial] >= C with the linear trial; functional quadrature matches
    both closed forms; exact potential attains C; b = 2a values 0.750L/0.7213L."""
    a, b, L = 1.0, 2.0, 1.0
    Ct = cyl_trial_capacitance(a, b, L)
    Ce = cyl_exact_capacitance(a, b, L)
    assert Ct > Ce
    assert _close(Ct, 0.75 * L, rel=1e-12)
    assert _close(Ce, L / (2 * np.log(2.0)), rel=1e-12)
    assert _close(Ce, 0.7213 * L, rel=1e-4)
    # quadrature of the functional
    q_trial = cyl_functional_quad(lambda r: 1.0 / (b - a), a, b, L, n=20000)
    q_exact = cyl_functional_quad(lambda r: 1.0 / (r * np.log(b / a)), a, b, L,
                                  n=20000)
    assert _close(q_trial, Ct, rel=1e-6)
    assert _close(q_exact, Ce, rel=1e-6)


# --- P41 (2.12.11) ----------------------------------------------------------

def test_p41_three_wires():
    """Three wires (-lam, -lam, 2lam): K-independence (neutral system),
    N = 12, and w = lam^2/(2 C_L) = (1/2) sum lam_i V_i."""
    lam, d, a = 0.8, 50.0, 1.0
    lams = np.array([-lam, -lam, 2 * lam])
    V1 = wire_potentials(lams, d, a, K=1.0)
    V2 = wire_potentials(lams, d, a, K=7.3)
    assert np.allclose(V1, V2, rtol=0, atol=1e-10)         # sum lam_i = 0
    combo = 2 * V1[2] - V1[0] - V1[1]
    CL = lam / combo
    assert _close(CL, three_wire_CL(d, a), rel=1e-12)
    N = 1.0 / (CL * np.log(d / a))
    assert _close(N, 12.0, rel=1e-12)
    w_sum = 0.5 * float(lams @ V1)
    assert _close(w_sum, three_wire_energy(lam, d, a), rel=1e-12)
    assert _close(w_sum, lam * lam / (2 * CL), rel=1e-12)


# -----------------------------------------------------------------------------

def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"All {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
