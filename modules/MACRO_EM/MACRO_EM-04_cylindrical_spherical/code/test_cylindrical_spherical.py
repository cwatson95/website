"""Tests for MACRO_EM-04 -- every Wilcox Ch. 4 exercise that admits a numeric
check is exercised here (P1-P49).

Run directly:   python3 test_cylindrical_spherical.py   (-> "All N tests passed.")
Or with pytest: pytest test_cylindrical_spherical.py

Gaussian units; 3-D Green functions obey del^2 G = -4 pi delta (4.73);
2-D (line-charge) reduced Green functions carry the jump dg/drho|_+^- = -1/rho;
the 1-D (2.124) convention has no 4 pi.
"""
import numpy as np
from scipy import special as sp

from cylindrical_spherical import (
    # helpers
    quad_gl, gl_nodes, lap_cyl_axisym_fd, lap_sph_axisym_fd, lap_sph_angular_fd,
    ylm, wronskian_fd, unit_vec, angles_of, sph_quad, rotation_matrix_random,
    # 4.1
    jm_taylor, jn_intrep_413, jn_intrep_415, jn_intrep_416,
    sumrule_jm_sq, sumrule_j0_2t, int_rho_pow_jm, int_rho_pow_jm_quad,
    # 4.2
    Dperp, addition_j0_series, weber_gauss_closed, weber_gauss_quad,
    weber_gauss_lattice, delta2d_gauss_family,
    # 4.3
    bessel_norm_deriv_zero,
    # 4.4
    g_halfspace, G_axisym_from_g, G_wall_images,
    G_halfplane_series, G_halfplane_images,
    phi_capacitor_disk, Ez_capacitor_disk, G_halfinf_cyl, J1m_fn,
    # 4.6
    bessel_zero_asymptotic, phi_cyl_side_V, solve_laplace_axisym,
    # 4.7
    disk_C_var, disk_C_var_best, phi_patch_neumann, phi_patch_axis_closed,
    wronskian_jnu_jmnu, wronskian_jm_nm,
    g_in_cyl, g_out_cyl, g_free_cyl, G_cyl_reduced_rho,
    g_toroid, G_toroid, coulomb_cylJ,
    disk_free_potential_lhs, disk_free_potential_rhs,
    # 4.8
    wedge_series, wedge_closed, g_wedge_annulus, G_wedge_annulus,
    cyl2d_series, cyl2d_image, G_wedge3d, g_concentric_2d, G_concentric_2d,
    # 4.9
    dfact, legendre_explicit, legendre0, dlegendre0, legendre0_seq,
    # 4.11
    integral_PlPl, int_Pl, hemi_C_var, hemi_C_var_best,
    ylm_rotation_coeffs, ylm_rotation_residual, vandermonde_det,
    sphere_int_coulomb, sphere_int_coulomb_costh,
    # 4.12
    caps_terms, caps_C_partial, split_sphere_Al, caps_sigma, caps_Q_top,
    gN_ext_sphere_series, gN_ext_sphere_closed, gN_shell, gN_shell_g0,
    sphere_poisson_kernel, sphere_series_from_V, hemi_basin_phi, concentric_C,
    # 4.13
    E_center_split, E_center_split_fd, Q0_legendre, sphereG_series,
    unequal_caps_V2, unequal_caps_C_book, unequal_caps_C_simple,
    halves_C11_C12, gD_halfspace_sph_series, gD_halfspace_sph_images,
    # 4.14
    sine_delta_action, g_plates_z, G_plates_bessel, G_plates_images,
    G_finite_cyl_79, G_finite_cyl_eigen,
    sumrule_sine, sumrule_sine_closed, g_in_eigen, g1d_eigen, g1d_closed,
    sph_jn_zeros, sph_radial_residual,
)

RNG = np.random.default_rng(20260706)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


def _jump(g, s, h=1e-6):
    """(dg/ds at s+) - (dg/ds at s-) by one-sided differences."""
    return ((g(s + h) - g(s)) - (g(s) - g(s - h))) / h


# --- Sec. 4.1: Bessel functions from the generating function (P1-P4) --------

def test_p1_taylor_series():
    """Ex. 4.1.1: the (4.8) Taylor series == scipy Jm == the (4.13) integral
    representation, incl. J_{-m} = (-1)^m Jm (4.10)."""
    for m in (0, 1, 3, 6):
        for t in (0.3, 1.7, 4.2):
            assert _approx(jm_taylor(m, t), sp.jv(m, t), rel=1e-12, abs_=1e-14)
            assert _approx(jn_intrep_413(m, t), sp.jv(m, t), rel=1e-10, abs_=1e-12)
    for m in (-1, -4):
        assert _approx(jm_taylor(m, 2.6), sp.jv(m, 2.6), rel=1e-12)


def test_p2_sum_rules():
    """Ex. 4.1.2: sum_m Jm^2 = 1 and sum_m (-1)^m Jm^2 = J0(2t)."""
    for t in (0.4, 1.3, 3.1, 6.4):
        assert _approx(sumrule_jm_sq(t), 1.0, rel=1e-12)
        assert _approx(sumrule_j0_2t(t), sp.j0(2 * t), rel=1e-11, abs_=1e-13)


def test_p3_rho_power_integral():
    """Ex. 4.1.3: int_0^a rho^{m+1} Jm = (a^{m+1}/k)(J_{m+1}(ka) - delta_{m,-1}),
    checked against Gauss-Legendre quadrature, incl. the m = -1 delta term."""
    for m in (0, 1, 2, 5, -1):
        for (k, a) in ((1.7, 1.2), (0.6, 2.5), (3.2, 0.8)):
            assert _approx(int_rho_pow_jm(m, k, a),
                           int_rho_pow_jm_quad(m, k, a), rel=1e-10, abs_=1e-12)


def test_p4_integral_representations():
    """Ex. 4.1.4: (4.15) and (4.16) both reproduce Jn(t)."""
    for n in (0, 2, 5):
        for t in (0.9, 2.2, 5.1):
            assert _approx(jn_intrep_415(n, t), sp.jv(n, t), rel=1e-9, abs_=1e-11)
            assert _approx(jn_intrep_416(n, t), sp.jv(n, t), rel=1e-9, abs_=1e-11)


# --- Sec. 4.2: completeness / addition theorem (P5) ---------------------------

def test_p5_addition_theorem():
    """Ex. 4.2.1a: J0(kD) = sum_m Jm(k rho) Jm(k rho') e^{im(phi-phi')}."""
    for (k, r, p, rp, pp) in [(2.3, 1.1, 0.4, 0.7, 2.0), (0.8, 2.4, -1.0, 1.9, 0.3),
                              (4.0, 0.5, 2.8, 1.3, -2.2)]:
        D = Dperp(r, p, rp, pp)
        assert _approx(addition_j0_series(k, r, p, rp, pp), sp.j0(k * D),
                       rel=1e-10, abs_=1e-12)


def test_p5_completeness_delta():
    """Ex. 4.2.1b: the Gaussian-regulated completeness integral: Weber's
    closed form == quadrature == the finite-domain eigen-lattice; the D-space
    family is a unit-mass nascent delta that concentrates as p -> 0."""
    for (nu, r, rp, p) in [(0, 0.9, 1.4, 0.5), (1, 0.9, 1.4, 0.5), (2, 2.0, 1.1, 0.3)]:
        w = weber_gauss_closed(nu, r, rp, p)
        assert _approx(weber_gauss_quad(nu, r, rp, p), w, rel=1e-7)
        assert _approx(weber_gauss_lattice(nu, r, rp, p, a=40.0), w, rel=1e-6)
    # unit mass: int d^2x delta2d = int 2 pi D dD (1/4 pi p^2) e^{-D^2/4p^2} = 1
    for p in (0.3, 0.1):
        mass = quad_gl(lambda D: 2 * np.pi * D * delta2d_gauss_family(D, p),
                       0.0, 30 * p, 2000)
        assert _approx(mass, 1.0, rel=1e-12)
    assert _approx(delta2d_gauss_family(0.0, 0.05),
                   100 * delta2d_gauss_family(0.0, 0.5), rel=1e-12)  # peak ~ 1/p^2


# --- Sec. 4.3: zeros and orthogonality (P6) -----------------------------------

def test_p6_deriv_zero_normalization():
    """Ex. 4.3.1: int_0^a rho Jm(kbar rho)^2 = (a^2/2)(1 - m^2/y^2) Jm(y)^2
    at zeros y of Jm'."""
    for (m, n, a) in [(0, 2, 1.0), (1, 1, 1.5), (2, 3, 1.5), (5, 4, 0.7)]:
        q, closed = bessel_norm_deriv_zero(m, n, a)
        assert _approx(q, closed, rel=1e-11)


# --- Sec. 4.4: reduced G for flat walls, capped cylinder (P7-P10) -------------

def test_p7_wall_green():
    """Ex. 4.4.1: reduced g for the grounded wall: BC, jump -1 in dg/dz, and
    the assembled Hankel form == the image answer."""
    k = 1.3
    assert abs(g_halfspace(k, 0.0, 0.8)) < 1e-15                  # wall BC
    assert _approx(_jump(lambda z: g_halfspace(k, z, 0.8), 0.8), -1.0, rel=1e-5)
    assert _approx(g_halfspace(k, 0.3, 0.9), g_halfspace(k, 0.9, 0.3), rel=1e-14)
    for (D, z, zp) in [(0.8, 0.5, 0.9), (0.2, 1.5, 0.4), (2.0, 0.3, 0.35)]:
        K = 50.0 / max(min(abs(z - zp), z + zp), 0.05)   # e^{-k dz} tail cutoff
        assert _approx(G_axisym_from_g(D, z, zp, g_halfspace, K=K, n=4000),
                       G_wall_images(D, z, zp), rel=1e-6)


def test_p8_halfplane_green():
    """Ex. 4.4.2: the sin(m phi) Bessel form for the conducting z-x plane ==
    the image-pair answer; zero on the plate."""
    for (r, p, z, rp, pp, zp) in [(1.0, 1.2, 0.3, 0.8, 2.1, -0.2),
                                  (0.6, 0.5, 1.0, 1.5, 2.6, 0.7)]:
        assert _approx(G_halfplane_series(r, p, z, rp, pp, zp),
                       G_halfplane_images(r, p, z, rp, pp, zp), rel=1e-6)
    assert abs(G_halfplane_series(1.0, 0.0, 0.3, 0.8, 2.1, -0.2)) < 1e-12
    assert abs(G_halfplane_series(1.0, np.pi, 0.3, 0.8, 2.1, -0.2)) < 1e-12


def test_p9_capacitor_disk():
    """Ex. 4.4.3: k-integral potentials for the disk-driven parallel plates.
    (a) Neumann bottom: Ez(z=0) = 0; (b) Dirichlet bottom: Phi(z=0) = 0.
    Both: harmonic in the gap; -dPhi/dz -> E0 on the top-plate disk (rho < a,
    e^{-eps k}-regulated, eps -> 0); Ez(top) -> 0 for rho > a."""
    a, d, E0 = 1.0, 1.0, 1.0
    assert abs(Ez_capacitor_disk(0.5, 0.0, a, d, E0)) < 1e-14          # (a) bottom
    assert abs(phi_capacitor_disk(0.7, 0.0, a, d, E0, dirichlet_bottom=True)) < 1e-10
    for dirich in (False, True):
        f = lambda r, z: phi_capacitor_disk(r, z, a, d, E0, dirichlet_bottom=dirich)
        assert abs(lap_cyl_axisym_fd(f, 0.6, 0.5, h=2e-4)) < 2e-4
        e1 = Ez_capacitor_disk(0.3, d, a, d, E0, dirichlet_bottom=dirich, eps=0.02)
        e2 = Ez_capacitor_disk(0.3, d, a, d, E0, dirichlet_bottom=dirich, eps=0.01)
        assert abs(2 * e2 - e1 - E0) < 5e-3            # Richardson eps -> 0: E0
        o1 = Ez_capacitor_disk(1.7, d, a, d, E0, dirichlet_bottom=dirich, eps=0.02)
        o2 = Ez_capacitor_disk(1.7, d, a, d, E0, dirichlet_bottom=dirich, eps=0.01)
        assert abs(2 * o2 - o1) < 5e-3                 # off the disk: 0


def test_p10_capped_cylinder_green():
    """Ex. 4.4.4: G for the half-infinite capped cylinder: zero on the cap
    z=0 and the side rho=a; symmetric; == (infinite-cylinder G) - (its image
    in the cap), built from the independent rho-reduced Green function."""
    a = 1.0
    assert abs(G_halfinf_cyl(0.5, 0.3, 0.0, 0.6, 1.0, 0.8, a)) < 1e-10
    assert abs(G_halfinf_cyl(a, 0.3, 0.7, 0.6, 1.0, 0.8, a)) < 1e-12
    args = (0.5, 0.3, 0.9, 0.6, 1.0, 0.4)
    assert _approx(G_halfinf_cyl(*args, a),
                   G_halfinf_cyl(*args[3:], *args[:3], a), rel=1e-11)
    for (r, p, z, rp, pp, zp) in [(0.5, 0.3, 0.9, 0.6, 1.0, 0.4),
                                  (0.3, 2.0, 0.5, 0.7, 0.1, 1.1)]:
        direct = G_cyl_reduced_rho(p - pp, z - zp, lambda m, k: g_in_cyl(m, k, r, rp, a))
        image = G_cyl_reduced_rho(p - pp, z + zp, lambda m, k: g_in_cyl(m, k, r, rp, a))
        assert _approx(G_halfinf_cyl(r, p, z, rp, pp, zp, a, M=30, N=80),
                       direct - image, rel=2e-5, abs_=1e-7)


# --- Sec. 4.6: modified Bessel functions, side at V (P11-P12) -----------------

def test_p11_zero_asymptotics():
    """Ex. 4.6.1 input: x_mn ~ (n + m/2 - 1/4) pi for n large (4.98); the
    residual is McMahon's next order (4m^2-1)/(8 x) -> 0."""
    for m in (0, 1, 4):
        x = sp.jn_zeros(m, 60)
        d15 = abs(bessel_zero_asymptotic(m, 15) - x[14])
        d60 = abs(bessel_zero_asymptotic(m, 60) - x[59])
        assert d60 <= 1.2 * abs(4 * m * m - 1) / (8 * x[59]) + 1e-12
        assert d60 < d15 or m == 0


def test_p11_completeness_limit():
    """Ex. 4.6.1: the finite-domain eigen-sum (4.71) tends to the infinite-
    domain Hankel completeness integral (4.39) as a -> inf (Gaussian-tested):
    the eigen-lattice sum feels the wall at small a (boundary images
    ~ e^{-(2a-rho-rho')^2/4p^2}) and lands on Weber's closed form once
    a covers the Gaussian support."""
    nu, r, rp, p = 1, 0.9, 1.6, 0.35
    w = weber_gauss_closed(nu, r, rp, p)
    err = [abs(weber_gauss_lattice(nu, r, rp, p, a=aa, N=4000) - w)
           for aa in (1.8, 2.2, 5.0, 40.0)]
    assert err[0] > 1e-3 and err[1] > 1e-7          # wall still felt
    assert err[0] > 10 * err[1]                     # ... exponentially less so
    assert err[2] < 1e-12 and err[3] < 1e-12        # limit attained


def test_p12_cylinder_side_at_V():
    """Ex. 4.6.2: Phi = (4V/pi) sum_odd I0(n pi rho/L) sin(n pi z/L)
    / (n I0(n pi a/L)): boundary data, harmonicity, FD cross-check."""
    a, L, V = 1.0, 2.0, 3.0
    assert abs(phi_cyl_side_V(0.5, 0.0, a, L, V)) < 1e-12       # caps grounded
    assert abs(phi_cyl_side_V(0.5, L, a, L, V)) < 1e-12
    assert _approx(phi_cyl_side_V(a, 0.77 * L, a, L, V, N=100001), V, rel=2e-3)
    f = lambda r, z: phi_cyl_side_V(r, z, a, L, V)
    assert abs(lap_cyl_axisym_fd(f, 0.55, 0.9, h=2e-4)) < 1e-5
    rg, zg, P = solve_laplace_axisym(a, L, V, nr=48, nz=96)
    for (i, j) in [(24, 48), (12, 30), (40, 70)]:
        assert _approx(P[i, j], phi_cyl_side_V(rg[i], zg[j], a, L, V),
                       rel=3e-3, abs_=3e-3)


# --- Sec. 4.7: Wronskian technique (P13-P18) ----------------------------------

def test_p13_disk_variational():
    """Ex. 4.7.1: C[sigma] is a lower bound on the disk capacitance.
    beta=0 reproduces the uniform-trial 3pi/16; the optimized quadratic trial
    reaches the book's 0.6213a, still below the exact 2a/pi."""
    assert _approx(disk_C_var(0.0), 3 * np.pi / 16, rel=1e-5)
    Cb, bb = disk_C_var_best()
    assert Cb > 0.62125 and Cb < 2 / np.pi
    assert bb > 0                       # density grows toward the rim


def test_p14_patch_neumann():
    """Ex. 4.7.2: Phi = E0 a int dk/k J0 J1 e^{-kz}: on-axis closed form
    E0(sqrt(a^2+z^2)-z); -dPhi/dz at the wall -> E0 on the patch, 0 off it;
    decays at infinity."""
    a, E0 = 1.0, 2.0
    for z in (0.2, 0.7, 2.0):
        assert _approx(phi_patch_neumann(1e-12, z, a, E0),
                       phi_patch_axis_closed(z, a, E0), rel=1e-7)

    def ez(rho, z):                    # -dPhi/dz = E0 a int dk J0 J1 e^{-kz}
        return E0 * a * quad_gl(lambda k: sp.j0(k * rho) * sp.j1(k * a)
                                * np.exp(-k * z), 1e-9, 80.0 / z, 4000)

    # Ez -> E0 on the patch, 0 off it (approach is O(z); Richardson in z)
    assert abs(2 * ez(0.4, 0.05) - ez(0.4, 0.1) - E0) < 5e-3
    assert abs(2 * ez(1.6, 0.05) - ez(1.6, 0.1)) < 5e-3
    # far field = monopole of the patch charge: Phi -> E0 a^2/2z
    assert _approx(phi_patch_axis_closed(40.0, a, E0), E0 * a**2 / 80.0, rel=2e-4)


def test_p15_wronskians():
    """Ex. 4.7.3: t W[J_nu, J_-nu] is constant = -2 sin(nu pi)/pi;
    W[Jm, Nm] = 2/(pi t)."""
    for nu in (0.3, 0.6, 1.7):
        vals = [t * wronskian_fd(lambda x: sp.jv(nu, x), lambda x: sp.jv(-nu, x), t)
                for t in (0.7, 1.7, 3.9)]
        assert np.ptp(vals) < 1e-7                                  # constant
        assert _approx(vals[1], -2 * np.sin(nu * np.pi) / np.pi, rel=1e-7)
        assert _approx(wronskian_fd(lambda x: sp.jv(nu, x), lambda x: sp.jv(-nu, x), 1.7),
                       wronskian_jnu_jmnu(nu, 1.7), rel=1e-7)
    for m in (0, 2, 5):
        assert _approx(wronskian_fd(lambda x: sp.jv(m, x), lambda x: sp.yv(m, x), 1.7),
                       wronskian_jm_nm(1.7), rel=1e-7)


def test_p16_cylinder_reduced_g():
    """Ex. 4.7.4: exterior/interior reduced Green functions of the grounded
    cylinder: wall BC, decay/regularity, the -1/rho' jump, and the free-space
    A=1 normalization (assembled == 1/|x-x'|)."""
    m, k, a = 2, 1.3, 2.0
    assert abs(g_in_cyl(m, k, a, 1.1, a)) < 1e-15
    assert abs(g_out_cyl(m, k, a, 3.1, a)) < 1e-15
    assert g_out_cyl(m, k, 30.0, 3.1, a) < 1e-12                    # decay
    for (g, rp) in [(lambda r: g_in_cyl(m, k, r, 1.1, a), 1.1),
                    (lambda r: g_out_cyl(m, k, r, 3.1, a), 3.1),
                    (lambda r: g_free_cyl(m, k, r, 1.1), 1.1)]:
        assert _approx(_jump(g, rp) * rp, -1.0, rel=1e-5)
    x1 = np.array([1.1 * np.cos(0.3), 1.1 * np.sin(0.3), 0.4])
    x2 = np.array([0.8 * np.cos(1.5), 0.8 * np.sin(1.5), -0.3])
    assert _approx(G_cyl_reduced_rho(0.3 - 1.5, 0.7,
                                     lambda mm, kk: g_free_cyl(mm, kk, 1.1, 0.8)),
                   1 / np.linalg.norm(x1 - x2), rel=1e-4)
    # interior G vanishes on the wall
    assert abs(G_cyl_reduced_rho(0.9, 0.4, lambda mm, kk: g_in_cyl(mm, kk, a, 0.9, a))) < 1e-12


def test_p17_toroid_green():
    """Ex. 4.7.5: rectangular-section toroid: reduced g vanishes at rho=a,b
    with the -1/rho' jump; assembled G vanishes on all four walls, is
    symmetric, and approaches 1/|x-x'| near the source."""
    a, b, L = 1.0, 3.0, 2.0
    assert abs(g_toroid(1, 1.2, a, 1.5, a, b)) < 1e-15
    assert abs(g_toroid(1, 1.2, b, 1.5, a, b)) < 1e-15
    assert _approx(_jump(lambda r: g_toroid(1, 1.2, r, 1.5, a, b), 1.5) * 1.5,
                   -1.0, rel=1e-5)
    src = (1.7, 0.8, 1.1)
    assert abs(G_toroid(a, 0.5, 0.9, *src, a, b, L)) < 1e-10
    assert abs(G_toroid(2.2, 0.5, 0.0, *src, a, b, L)) < 1e-10      # cap z=0
    assert abs(G_toroid(2.2, 0.5, L, *src, a, b, L)) < 1e-10        # cap z=L
    assert _approx(G_toroid(2.2, 0.5, 0.9, *src, a, b, L),
                   G_toroid(*src, 2.2, 0.5, 0.9, a, b, L), rel=1e-10)
    # near the source G R -> 1 (unit charge): approach is O(R) from the wall
    # images, so Richardson-extrapolate two offset scales
    gr = []
    for s in (1.0, 0.5):
        d = np.array([0.15, 1.7 * 0.10, 0.12]) * s
        x = (1.7 + d[0], 0.8 + 0.10 * s, 1.1 + d[2])
        R = np.linalg.norm(d)
        gr.append(G_toroid(*x, *src, a, b, L, M=140, N=100) * R)
    assert abs(2 * gr[1] - gr[0] - 1.0) < 0.02


def test_p18_coulomb_cylJ():
    """Ex. 4.7.6a: the (4.120) Bessel representation equals 1/|x-x'| (so its
    Laplacian is -4 pi delta by construction of (4.108))."""
    for (r, p, z, rp, pp, zp) in [(1.1, 0.3, 0.4, 0.8, 1.5, -0.3),
                                  (0.4, 2.2, 1.0, 1.7, -0.6, 0.2)]:
        x1 = np.array([r * np.cos(p), r * np.sin(p), z])
        x2 = np.array([rp * np.cos(pp), rp * np.sin(pp), zp])
        assert _approx(coulomb_cylJ(r, p, z, rp, pp, zp),
                       1 / np.linalg.norm(x1 - x2), rel=1e-8)


def test_p18_disk_source_integral():
    """Ex. 4.7.6b: the disk-integrated Coulomb potential == the closed
    Bessel k-integral 2 pi a int dk/k J0 J1 e^{-k|z-z'|}."""
    for (r, z, zp, a) in [(0.7, 0.9, 0.2, 1.0), (1.6, 0.1, 0.5, 1.2),
                          (0.0, 2.0, 0.0, 0.6)]:
        assert _approx(disk_free_potential_lhs(max(r, 1e-12), z, zp, a),
                       disk_free_potential_rhs(max(r, 1e-12), z, zp, a), rel=1e-7)


# --- Sec. 4.8: conducting wedge family (P19-P23) ------------------------------

def test_p19_wedge_closed_form():
    """Ex. 4.8.1: the (4.143) sine series sums to the log closed form; walls
    grounded; beta = pi/2 recovers the quadrant image answer (Ex. 3.1.3)."""
    for beta in (2.2, np.pi / 2, 4.4):
        for (r, p, rp, pp) in [(0.7, 0.3 * beta, 1.4, 0.8 * beta),
                               (2.0, 0.5 * beta, 0.5, 0.1 * beta)]:
            assert _approx(wedge_series(r, p, rp, pp, beta),
                           wedge_closed(r, p, rp, pp, beta), rel=1e-9, abs_=1e-12)
        assert abs(wedge_closed(0.7, 0.0, 1.4, 0.8 * beta, beta)) < 1e-14
        assert abs(wedge_closed(0.7, beta, 1.4, 0.8 * beta, beta)) < 1e-12
    r, p, rp, pp = 0.7, 0.6, 1.1, 0.9
    quadrant = np.log((r**4 + rp**4 - 2 * r**2 * rp**2 * np.cos(2 * (p + pp)))
                      / (r**4 + rp**4 - 2 * r**2 * rp**2 * np.cos(2 * (p - pp))))
    assert _approx(wedge_closed(r, p, rp, pp, np.pi / 2), quadrant, rel=1e-12)


def test_p20_wedge_annulus():
    """Ex. 4.8.2: closed wedge with grounded arcs at rho=a,b: reduced g has
    the wall zeros and -1/rho' jump; assembled G vanishes on all four
    boundaries and is symmetric; a -> 0 recovers the outer-arc wedge (4.142)."""
    beta, a, b = 2.2, 1.0, 3.0
    gam = 1.9
    assert abs(g_wedge_annulus(gam, a, 1.5, a, b)) < 1e-15
    assert abs(g_wedge_annulus(gam, b, 1.5, a, b)) < 1e-15
    assert _approx(_jump(lambda r: g_wedge_annulus(gam, r, 1.5, a, b), 1.5) * 1.5,
                   -1.0, rel=1e-5)
    args = (1.5, 1.2)
    assert abs(G_wedge_annulus(a, 0.9, *args, beta, a, b)) < 1e-12
    assert abs(G_wedge_annulus(b, 0.9, *args, beta, a, b)) < 1e-12
    assert abs(G_wedge_annulus(2.0, 0.0, *args, beta, a, b)) < 1e-12
    assert abs(G_wedge_annulus(2.0, beta, *args, beta, a, b)) < 1e-12
    assert _approx(G_wedge_annulus(2.0, 0.9, *args, beta, a, b),
                   G_wedge_annulus(*args, 2.0, 0.9, beta, a, b), rel=1e-12)
    assert _approx(G_wedge_annulus(2.0, 0.9, 1.5, 1.2, beta, 1e-9, b),
                   wedge_series(2.0, 0.9, 1.5, 1.2, beta, a=b), rel=1e-8)


def test_p21_cylinder_2d_series():
    """Ex. 4.8.3: interior line-charge series == the (Ex. 3.3.5b) image log
    form; grounded at rho = a."""
    a = 1.5
    for (r, p, rp, pp) in [(0.7, 0.4, 1.1, 2.0), (0.2, -1.0, 0.9, 0.5)]:
        assert _approx(cyl2d_series(r, p, rp, pp, a),
                       cyl2d_image(r, p, rp, pp, a), rel=1e-11)
    assert abs(cyl2d_image(a, 0.4, 1.1, 2.0, a)) < 1e-14


def test_p22_wedge3d_point_charge():
    """Ex. 4.8.4: point charge in the wedge-shaped hole: fractional-order
    interior-cylinder reduced g assembled over sin(n pi phi/beta); vanishes on
    the two flats and the arc; for beta = pi it equals the half-cylinder image
    construction (infinite-cylinder G minus its reflection)."""
    a = 1.5
    assert abs(G_wedge3d(0.8, 0.0, 0.2, 0.6, 2.0, -0.15, 2.0, a)) < 1e-12
    assert abs(G_wedge3d(0.8, 2.0, 0.2, 0.6, 2.0, -0.15, 2.0, a)) < 1e-12
    assert abs(G_wedge3d(a, 1.1, 0.2, 0.6, 2.0, -0.15, 2.0, a)) < 1e-12
    args = (0.8, 1.1, 0.2, 0.6, 2.0, -0.15)
    direct = G_cyl_reduced_rho(1.1 - 2.0, 0.35, lambda m, k: g_in_cyl(m, k, 0.8, 0.6, a))
    image = G_cyl_reduced_rho(1.1 + 2.0, 0.35, lambda m, k: g_in_cyl(m, k, 0.8, 0.6, a))
    assert _approx(G_wedge3d(*args, np.pi, a), direct - image, rel=1e-6)


def test_p23_concentric_2d():
    """Ex. 4.8.5: line charge between grounded concentric cylinders:
    log/power reduced modes (wall zeros, -1/rho' jump); assembled G vanishes
    on both cylinders, is symmetric, and -> the single-cylinder interior
    answer as b -> 0 (1/ln(a/b) Richardson-extrapolated)."""
    b, a = 1.0, 3.0                       # inner b, outer a
    assert abs(g_concentric_2d(3, b, 2.0, b, a)) < 1e-16
    assert abs(g_concentric_2d(3, a, 2.0, b, a)) < 1e-16
    for m in (0, 1, 4):
        assert _approx(_jump(lambda r: g_concentric_2d(m, r, 1.7, b, a), 1.7) * 1.7,
                       -1.0, rel=1e-4)
    assert abs(G_concentric_2d(b, 0.5, 1.7, 1.2, b, a)) < 1e-12
    assert abs(G_concentric_2d(a, 0.5, 1.7, 1.2, b, a)) < 1e-12
    assert _approx(G_concentric_2d(1.4, 0.5, 1.7, 1.2, b, a),
                   G_concentric_2d(1.7, 1.2, 1.4, 0.5, b, a), rel=1e-12)
    g1 = G_concentric_2d(0.7, 0.4, 1.1, 2.0, 1e-6, 1.5)
    g2 = G_concentric_2d(0.7, 0.4, 1.1, 2.0, 1e-12, 1.5)
    L1, L2 = np.log(1.5 / 1e-6), np.log(1.5 / 1e-12)   # error ~ 1/ln(a/b)
    assert _approx((g2 * L2 - g1 * L1) / (L2 - L1),
                   cyl2d_series(0.7, 0.4, 1.1, 2.0, 1.5), rel=1e-10)


# --- Sec. 4.9: Legendre polynomials, spherical harmonics (P24-P26) ------------

def test_p24_legendre_explicit():
    """Ex. 4.9.1: the double-factorial explicit series == P_l; P_l(0) and
    (d/dx)^m P_l(0) closed forms == exact polynomial derivatives."""
    x = np.linspace(-1, 1, 9)
    for l in (0, 1, 4, 7, 10):
        assert np.max(np.abs(legendre_explicit(l, x) - sp.eval_legendre(l, x))) < 1e-10
    for l in range(9):
        Pl = np.polynomial.legendre.Legendre.basis(l).convert(
            kind=np.polynomial.Polynomial)
        assert _approx(legendre0(l), Pl(0.0), rel=1e-12, abs_=1e-14)
        for m in range(l + 1):
            assert _approx(dlegendre0(l, m), Pl.deriv(m)(0.0) if m else Pl(0.0),
                           rel=1e-10, abs_=1e-12)
    q = legendre0_seq(6)
    assert np.max(np.abs(q - [sp.eval_legendre(2 * n, 0.0) for n in range(6)])) < 1e-14


def test_p25_ylm_parity():
    """Ex. 4.9.2: parity (theta -> pi - theta, phi -> phi +- pi) multiplies
    Y_lm by (-1)^l."""
    for l in range(5):
        for m in range(-l, l + 1):
            for (th, ph) in [(0.8, 1.1), (2.3, 4.9)]:
                php = ph + np.pi if ph < np.pi else ph - np.pi
                assert abs(ylm(l, m, np.pi - th, php)
                           - (-1) ** l * ylm(l, m, th, ph)) < 1e-12


def test_p26_legendre_orthogonality():
    """Ex. 4.9.3: int_{-1}^{1} P_n P_m = 2 delta_nm/(2n+1) by quadrature."""
    for (n, m) in [(0, 2), (1, 3), (2, 5), (4, 6)]:
        v = quad_gl(lambda t: sp.eval_legendre(n, t) * sp.eval_legendre(m, t),
                    -1.0, 1.0, 200)
        assert abs(v) < 1e-13
    for n in (0, 1, 3, 6):
        v = quad_gl(lambda t: sp.eval_legendre(n, t) ** 2, -1.0, 1.0, 200)
        assert _approx(v, 2.0 / (2 * n + 1), rel=1e-12)


# --- Sec. 4.11: Coulomb expansion, addition theorem (P27-P32) -----------------

def test_p27_generating_function():
    """Ex. 4.11.1: the generating function sums to (1-2xt+t^2)^{-1/2}, and
    its derivatives yield the recursions (4.180) and (4.181)."""
    for (x, t) in [(0.3, 0.5), (-0.7, 0.8), (0.95, 0.4)]:
        s = sum(t ** n * sp.eval_legendre(n, x) for n in range(120))
        assert _approx(s, 1 / np.sqrt(1 - 2 * x * t + t * t), rel=1e-11)
    h = 1e-6
    dP = lambda n, x: (sp.eval_legendre(n, x + h) - sp.eval_legendre(n, x - h)) / (2 * h)
    for n in (1, 3, 6):
        for x in (-0.4, 0.2, 0.8):
            assert _approx(x * dP(n + 1, x) - dP(n, x),
                           (n + 1) * sp.eval_legendre(n + 1, x), rel=1e-6, abs_=1e-8)
            assert _approx((2 * n + 1) * x * sp.eval_legendre(n, x),
                           (n + 1) * sp.eval_legendre(n + 1, x)
                           + n * sp.eval_legendre(n - 1, x), rel=1e-12)


def test_p28_rodrigues():
    """Ex. 4.11.2: Rodrigues-built polynomials satisfy (4.182)
    P'_{n+1} = (2n+1) P_n + P'_{n-1} exactly (coefficient-level), and
    P_n(1) = 1."""
    from math import factorial
    Poly = np.polynomial.Polynomial

    def rodrigues(n):
        p = Poly([-1, 0, 1]) ** n
        for _ in range(n):
            p = p.deriv()
        return p / (2 ** n * factorial(n))

    for n in range(1, 8):
        lhs = rodrigues(n + 1).deriv()
        rhs = (2 * n + 1) * rodrigues(n) + rodrigues(n - 1).deriv()
        assert np.max(np.abs((lhs - rhs).coef)) < 1e-9
        assert _approx(rodrigues(n)(1.0), 1.0, rel=1e-12)


def test_p29_PlPl_integral():
    """Ex. 4.11.3: int dOmega' P_l(u1.n') P_l(n'.u2) = 4pi/(2l+1) P_l(u1.u2)."""
    for l in (1, 3, 5):
        for _ in range(2):
            u1 = RNG.normal(size=3); u1 /= np.linalg.norm(u1)
            u2 = RNG.normal(size=3); u2 /= np.linalg.norm(u2)
            assert _approx(integral_PlPl(l, u1, u2),
                           4 * np.pi / (2 * l + 1) * sp.eval_legendre(l, u1 @ u2),
                           rel=1e-8, abs_=1e-10)


def test_p30_hemisphere_variational():
    """Ex. 4.11.4: hemisphere-bowl variational capacitance: the linear trial
    reaches the book's 0.8052a bound, below the exact (1/2 + 1/pi)a; the
    optimal density increases toward the edge (beta* < 0)."""
    Cb, bb = hemi_C_var_best()
    assert Cb > 0.80515 and Cb < 0.5 + 1 / np.pi
    assert bb < 0                       # sigma(x)=A(1+beta x) largest at edge x=0
    assert hemi_C_var(0.0) < Cb


def test_p31_ylm_rotation():
    """Ex. 4.11.5: Y_lm(rotated) is a linear combination of the Y_lm' at
    fixed l (solved from 2l+1 directions, checked at fresh ones); Vandermonde
    determinant = prod of differences (the invertibility engine); and the
    l-space closure gives the addition theorem (4.223)."""
    for l in (1, 2, 3):
        R = rotation_matrix_random(RNG)
        C = ylm_rotation_coeffs(l, R, RNG)
        assert ylm_rotation_residual(l, R, C, RNG, ntest=20) < 1e-9
    d, p = vandermonde_det(RNG.normal(size=5) + 1j * RNG.normal(size=5))
    assert abs(d - p) < 1e-10 * max(1.0, abs(p))
    for l in (2, 4):
        u1 = RNG.normal(size=3); u1 /= np.linalg.norm(u1)
        u2 = RNG.normal(size=3); u2 /= np.linalg.norm(u2)
        t1, p1 = angles_of(u1); t2, p2 = angles_of(u2)
        s = sum(ylm(l, m, t1, p1) * np.conj(ylm(l, m, t2, p2))
                for m in range(-l, l + 1))
        s *= 4 * np.pi / (2 * l + 1)
        assert abs(s.imag) < 1e-12
        assert _approx(s.real, sp.eval_legendre(l, u1 @ u2), rel=1e-10, abs_=1e-12)


def test_p32_sphere_coulomb_integrals():
    """Ex. 4.11.6: int dOmega'/|r-r'| = 4pi/r_>; the cos(theta')-weighted
    integral = (4pi/3)(r_</r_>^2) cos theta  --  both from the Coulomb
    expansion, checked by quadrature (inside and outside)."""
    for (r, rp) in [(0.7, 1.3), (1.9, 1.3), (0.2, 2.0)]:
        assert _approx(sphere_int_coulomb(r, rp), 4 * np.pi / max(r, rp), rel=1e-10)
    for (r, rp, th) in [(0.7, 1.3, 0.6), (1.9, 1.3, 2.1)]:
        rl, rg = min(r, rp), max(r, rp)
        assert _approx(sphere_int_coulomb_costh(r, rp, th),
                       4 * np.pi / 3 * rl / rg ** 2 * np.cos(th), rel=1e-8, abs_=1e-10)


# --- Sec. 4.12: concentric spheres (P33-P38) ----------------------------------

def test_p33_caps_capacitor():
    """Ex. 4.12.1: hemispherical-caps capacitor: the [P_2n(0)-P_2n+2(0)]^2
    terms equal the double-factorial form; C = Q/V by direct sigma quadrature
    matches the partial series; and the series grows logarithmically (the
    ideal split sphere has divergent gap capacitance)."""
    t_leg, t_dfact = caps_terms(400)
    assert np.max(np.abs(t_leg - t_dfact)) < 1e-15
    assert _approx(caps_Q_top(2.0, 1.5, 399) / 2.0, caps_C_partial(200, 1.5),
                   rel=1e-9)
    # log growth: t_n ~ 4/(pi n), so C(N) ~ (2/pi) ln N: each doubling of N
    # adds (2/pi) ln 2
    inc1 = caps_C_partial(2000) - caps_C_partial(1000)
    inc2 = caps_C_partial(4000) - caps_C_partial(2000)
    assert _approx(inc2, inc1, rel=0.02)
    assert _approx(inc1, 2 * np.log(2) / np.pi, rel=0.01)


def test_p34_neumann_exterior_sphere():
    """Ex. 4.12.2: exterior Neumann Green function: series == image+line-image
    closed form; dGN/dr -> 0 on the sphere; symmetric in r, r'."""
    a = 1.0
    for (r, rp, cg) in [(2.0, 1.4, 0.3), (1.2, 3.0, -0.6), (1.05, 1.5, 0.9)]:
        assert _approx(gN_ext_sphere_series(r, rp, cg, a, L=600),
                       gN_ext_sphere_closed(r, rp, cg, a), rel=1e-9)
        assert _approx(gN_ext_sphere_closed(r, rp, cg, a),
                       gN_ext_sphere_closed(rp, r, cg, a), rel=1e-13)
    h = 1e-5
    for cg in (0.3, -0.5):
        d = (gN_ext_sphere_closed(a + h, 1.7, cg, a)
             - gN_ext_sphere_closed(a, 1.7, cg, a)) / h
        assert abs(d) < 1e-4


def test_p35_neumann_shell():
    """Ex. 4.12.3: Neumann G between concentric spheres: dg_l/dr = 0 at both
    walls (l >= 1), the -1/r'^2 jump, b -> inf recovers Ex. 4.12.2's modes;
    g0 carries the 4pi/S = 1/(a^2+b^2) wall derivative (Sec. 2.8: additive
    constant undetermined); the Sec. 2.8/(2.115) surface delta appears as
    source-on-boundary doubling GN -> 2/|x-x'|."""
    a, b = 1.0, 2.5
    h = 1e-5
    for l in (1, 3):
        assert abs((gN_shell(l, a + h, 2.0, a, b) - gN_shell(l, a, 2.0, a, b)) / h) < 1e-5
        assert abs((gN_shell(l, b, 2.0, a, b) - gN_shell(l, b - h, 2.0, a, b)) / h) < 1e-5
        assert _approx(_jump(lambda r: gN_shell(l, r, 1.5, a, b), 1.5) * 1.5**2,
                       -1.0, rel=1e-4)
        rl, rg = 1.4, 2.0
        ext = (rl**l / rg**(l + 1)
               + l / (l + 1.0) * a**(2 * l + 1) / (rl * rg)**(l + 1)) / (2 * l + 1)
        assert _approx(gN_shell(l, rl, rg, a, 1e7), ext, rel=1e-9)
    # l=0 mode: wall derivative = 4pi/S with S = 4pi(a^2+b^2)
    d0a = (gN_shell_g0(a + h, 1.7, a, b) - gN_shell_g0(a, 1.7, a, b)) / h
    d0b = (gN_shell_g0(b, 1.7, a, b) - gN_shell_g0(b - h, 1.7, a, b)) / h
    assert _approx(d0a, 1.0 / (a**2 + b**2), rel=1e-4)
    assert _approx(d0b, -1.0 / (a**2 + b**2), rel=1e-4)
    # source-on-boundary doubling (surface delta of (2.115))
    def GN(r, cg, rp):
        tot = gN_shell_g0(r, rp, a, b)
        for l in range(1, 500):
            tot += (2 * l + 1) * gN_shell(l, r, rp, a, b) * sp.eval_legendre(l, cg)
        return tot
    for eps in (0.05, 0.025):
        R = eps                                     # field point straight above
        assert _approx(GN(a + eps, 1.0, a), 2.0 / R, rel=0.12)
    r1 = GN(a + 0.05, 1.0, a) / (2 / 0.05)
    r2 = GN(a + 0.025, 1.0, a) / (2 / 0.025)
    assert abs(r2 - 1) < abs(r1 - 1)                # ratio -> 1


def test_p36_sphere_poisson():
    """Ex. 4.12.4: sphere-surface data: the Y_lm mode series == the closed
    Poisson kernel +-a(a^2-r^2)/4pi (...)^{-3/2}, inside and outside; both
    reproduce the boundary data."""
    V = lambda TH, PH: np.cos(TH) ** 2 + 0.3 * np.sin(TH) * np.cos(PH)
    a = 1.0
    for (r, th, ph, inside) in [(0.6, 0.8, 1.2, True), (0.25, 2.0, -0.5, True),
                                (1.7, 0.8, 1.2, False), (4.0, 2.4, 2.9, False)]:
        assert _approx(sphere_poisson_kernel(r, th, ph, a, V, inside=inside),
                       sphere_series_from_V(r, th, ph, a, V, inside=inside),
                       rel=1e-8, abs_=1e-10)
    assert _approx(sphere_series_from_V(0.999, 0.8, 1.2, a, V, inside=True),
                   V(0.8, 1.2), rel=2e-3)
    assert _approx(sphere_series_from_V(1.001, 0.8, 1.2, a, V, inside=False),
                   V(0.8, 1.2), rel=2e-3)


def test_p37_hemisphere_basin():
    """Ex. 4.12.5: hemisphere with dome grounded, base at V: series solution
    meets both boundaries, is harmonic, and gives V at the center."""
    a, V = 1.0, 2.0
    for r in (0.2, 0.5, 0.8):
        assert _approx(hemi_basin_phi(r, np.pi / 2, a, V), V, rel=1e-12)
    assert abs(hemi_basin_phi(0.999, 0.7, a, V, L=4000)) < 2e-3 * V
    assert _approx(hemi_basin_phi(1e-14, 0.3, a, V), V, rel=1e-12)
    f = lambda rr, tt: hemi_basin_phi(rr, tt, a, V)
    assert abs(lap_sph_axisym_fd(f, 0.5, 0.8, h=1e-4)) < 1e-5
    assert abs(lap_sph_axisym_fd(f, 0.7, 1.2, h=1e-4)) < 1e-5


def test_p38_concentric_capacitances():
    """Ex. 4.12.6: capacitance matrix of concentric spheres from the l=0
    mode: check against the explicit two-sphere potential (Laplace solution,
    Gauss-law charges), symmetry, and the b -> inf isolated-sphere limit."""
    a, b = 1.0, 2.5
    Caa, Cab, Cbb = concentric_C(a, b)
    for (Va, Vb) in [(1.0, 0.0), (0.0, 1.0), (2.0, -1.0)]:
        alpha = a * b * (Va - Vb) / (b - a)          # Phi = alpha/r + beta, a<r<b
        Qa = alpha                                   # Gauss: charge inside r
        Qb_out = b * Vb                              # exterior face: Phi = Vb b/r
        Qb = -alpha + Qb_out
        assert _approx(Caa * Va + Cab * Vb, Qa, rel=1e-12, abs_=1e-12)
        assert _approx(Cab * Va + Cbb * Vb, Qb, rel=1e-12, abs_=1e-12)
    assert _approx(concentric_C(1.0, 1e8)[0], 1.0, rel=1e-7)   # isolated sphere
    assert Caa > 0 and Cbb > 0 and Cab < 0 and Caa * Cbb - Cab**2 > 0


# --- Sec. 4.13: split spheres, sphere point-electrostatics (P39-P43) ----------

def test_p39_center_field():
    """Ex. 4.13.1: E at the center of the unequally split +-V sphere:
    E_z = -(3V/2a) sin^2(theta_0), against the FD gradient of the series."""
    for (a, th0, V) in [(1.0, np.pi / 3, 1.0), (2.0, 1.9, -1.5), (1.0, np.pi / 2, 2.0)]:
        assert _approx(E_center_split(a, th0, V), E_center_split_fd(a, th0, V),
                       rel=1e-5, abs_=1e-7)


def test_p40_sphere_point_electrostatics():
    """Ex. 4.13.2: G for antipodal +- unit charges on the unit sphere:
    the odd-l series (coefficient (2l+1)/(l(l+1)) -- the book's extra
    printed factor 2 in (b) is inconsistent with (a)'s -2pi normalization)
    sums to Q0(cos gamma); Q0 is angularly harmonic away from the charges
    and has the -ln(gamma) 2-D Coulomb singularity."""
    for x in (0.5, -0.3, 0.85):
        assert _approx(sphereG_series(x), Q0_legendre(x), rel=1e-6)
    # angular Laplacian of Q0(cos gamma) vanishes away from the two poles
    thp, php = 1.1, 0.7
    np_ = unit_vec(thp, php)
    F = lambda th, ph: Q0_legendre(np.clip(unit_vec(th, ph) @ np_, -1, 1))
    for (th, ph) in [(2.0, 1.5), (0.9, 2.9)]:
        assert abs(lap_sph_angular_fd(F, th, ph, h=1e-4)) < 1e-4
    # near-source: G ~ -ln(gamma) + ln 2 (unit 2-D charge, -2pi normalization)
    for g in (1e-3, 1e-4):
        assert _approx(Q0_legendre(np.cos(g)), -np.log(g) + np.log(2.0), rel=1e-4)


def test_p41_unequal_caps():
    """Ex. 4.13.3: (a) V2 = -[(1-x0)/(1+x0)] V1 == the zero-total-charge
    (zero mean-potential) condition; (b) the printed double-integral series
    == the simplified (a/4) sum (2l+1)^2 I_+^2; (c) x0 = 0 reconnects to
    Ex. 4.12.1 (with C = Q/(V1-V2) = C_{4.12.1}/2)."""
    for x0 in (0.7, 0.0, -0.4):
        V1 = 2.0
        V2 = unequal_caps_V2(V1, np.arccos(x0))
        mean = V1 * (1 - x0) / 2 + V2 * (1 + x0) / 2   # <V> ~ total charge
        assert abs(mean) < 1e-13
        assert _approx(unequal_caps_C_book(x0, 400), unequal_caps_C_simple(x0, 400),
                       rel=1e-12)
    assert _approx(unequal_caps_C_simple(0.0, 800), 0.5 * caps_C_partial(400),
                   rel=1e-12)


def test_p42_halves_capacitance_matrix():
    """Ex. 4.13.4: hemispheres: C11 + C12 = a/2 exactly at every truncation
    (full sphere at V), C11 - C12 == the Ex. 4.12.1 series (only odd l
    survive), and C11 > 0 > C12."""
    for L in (100, 800):
        C11, C12 = halves_C11_C12(L)
        assert _approx(C11 + C12, 0.5, rel=1e-12)
        assert _approx(C11 - C12, caps_C_partial(L // 2), rel=1e-12)
        assert C11 > 0 > C12


def test_p43_halfspace_spherical():
    """Ex. 4.13.5: GD above the conducting plane theta = pi/2 as an
    l+m-odd spherical-harmonic sum == the plane-image answer; zero on the
    plane."""
    for (r, th, ph, rp, thp, php) in [(0.9, 0.7, 0.3, 1.2, 1.1, 2.0),
                                      (0.5, 1.2, -0.8, 2.0, 0.4, 0.9)]:
        assert _approx(gD_halfspace_sph_series(r, th, ph, rp, thp, php, L=80),
                       gD_halfspace_sph_images(r, th, ph, rp, thp, php),
                       rel=2e-4)
    assert abs(gD_halfspace_sph_series(0.9, np.pi / 2, 0.3, 1.2, 1.1, 2.0, L=60)) < 1e-12


# --- Sec. 4.14: eigenfunction expansions (P44-P49) ----------------------------

def test_p44_completeness_action():
    """Ex. 4.14.1: sum_n psi_n(x) psi_n*(x') acts as delta(x-x') on smooth
    test functions (sine basis on [0, L])."""
    L = 2.0
    for (f, x) in [(lambda t: np.sin(np.pi * t / L) * np.exp(-t), 0.7),
                   (lambda t: t * (L - t) ** 2, 1.3)]:
        assert _approx(sine_delta_action(f, x, L, N=300, nq=2000), f(x), rel=1e-6)


def test_p45_plates_bessel_form():
    """Ex. 4.14.2: the (4/a) int k dk J0(kD) sum_n sin sin/(k^2+k_n^2) form
    of the parallel-plate G (built here with the n-sum done, Ex. 4.14.5)
    == the Ex. 3.1.1 image ladder; zero on both plates."""
    a = 1.0
    for (D, z, zp) in [(0.6, 0.4, 0.7), (0.25, 0.8, 0.15), (1.5, 0.5, 0.5)]:
        assert _approx(G_plates_bessel(D, z, zp, a),
                       G_plates_images(D, z, zp, a, N=12000), rel=1e-7)
    assert abs(G_plates_bessel(0.6, 0.0, 0.7, a)) < 1e-12
    assert abs(G_plates_bessel(0.6, a, 0.7, a)) < 1e-9


def test_p46_cylinder_eigen_g():
    """Ex. 4.14.3: the Fourier-Bessel eigen-sum for g_in equals the
    Wronskian-built I,K closed form (Ex. 4.7.4b)."""
    a = 2.0
    for (m, k, r, rp) in [(0, 0.7, 0.5, 1.3), (2, 1.3, 0.8, 1.1)]:
        assert _approx(g_in_eigen(m, k, r, rp, a, N=6000), g_in_cyl(m, k, r, rp, a),
                       rel=2e-6, abs_=1e-12)
    # near the wall g is tiny (r = 1.9, a = 2): relative convergence is slow
    # but steady (~1/N): check value and trend
    ref = g_in_cyl(5, 2.1, 1.9, 0.4, a)
    e1 = abs(g_in_eigen(5, 2.1, 1.9, 0.4, a, N=1500) - ref)
    e2 = abs(g_in_eigen(5, 2.1, 1.9, 0.4, a, N=6000) - ref)
    assert e2 < 5e-4 * abs(ref) and e2 < e1 / 3


def test_p47_g1d_eigen():
    """Ex. 4.14.4: 1-D Dirichlet G (2.124 convention, d^2G/dx^2 = -delta):
    sine eigen-sum == x_<(L-x_>)/L; BCs; unit kink."""
    L = 2.0
    for (x, xp) in [(0.7, 1.4), (0.3, 0.5), (1.9, 0.2)]:
        assert _approx(g1d_eigen(x, xp, L), g1d_closed(x, xp, L), rel=1e-4)
    assert g1d_closed(0.0, 1.4, L) == 0.0 and g1d_closed(L, 1.4, L) == 0.0
    assert _approx(_jump(lambda x: g1d_closed(x, 1.4, L), 1.4, h=1e-7), -1.0, rel=1e-6)


def test_p48_sine_sum_rule():
    """Ex. 4.14.5: sum_n sin sin/(k^2+k_n^2) = (L/2) sinh(k z_<)
    sinh(k(L-z_>))/(k sinh kL); and the full finite-cylinder eigenfunction
    G equals the z-reduced (4.79) form."""
    L = 2.0
    for (k, z, zp) in [(1.3, 0.4, 0.9), (0.4, 1.5, 1.7), (3.0, 1.0, 0.3)]:
        assert _approx(sumrule_sine(k, z, zp, L), sumrule_sine_closed(k, z, zp, L),
                       rel=1e-8)
    a = 1.0
    for pt in [(0.5, 0.3, 0.9, 0.6, 1.2, 1.4), (0.3, 2.0, 0.5, 0.7, 0.1, 1.1)]:
        assert _approx(G_finite_cyl_eigen(*pt, a, L, P=400),
                       G_finite_cyl_79(*pt, a, L), rel=1e-4)


def test_p49_spherical_eigenfunctions():
    """Ex. 4.14.6: j_l(kr) Y_lm are the interior-sphere eigenfunctions:
    the radial ODE residual vanishes; eigenvalues from j_l(ka) = 0; radial
    orthogonality int r^2 j_l(z_n r/a) j_l(z_m r/a) dr = 0 for n != m."""
    for (l, k, r) in [(0, 1.7, 0.8), (2, 2.4, 1.1), (5, 3.0, 2.2)]:
        assert abs(sph_radial_residual(l, k, r, h=1e-4)) < 1e-5
    a = 1.0
    for l in (0, 2):
        z = sph_jn_zeros(l, 3)
        assert np.max(np.abs(sp.spherical_jn(l, z))) < 1e-12
        v = quad_gl(lambda r: r**2 * sp.spherical_jn(l, z[0] * r / a)
                    * sp.spherical_jn(l, z[2] * r / a), 0.0, a, 400)
        assert abs(v) < 1e-14
    assert _approx(sph_jn_zeros(0, 2)[-1], 2 * np.pi, rel=1e-12)  # j0 zeros = n pi


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import time
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    t0 = time.time()
    for name, fn in tests:
        t1 = time.time()
        fn()
        print(f"  {name}: ok ({time.time() - t1:.1f} s)")
    print(f"({time.time() - t0:.1f} s)")
    print(f"All {len(tests)} tests passed.")
