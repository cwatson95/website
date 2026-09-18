"""Tests for MACRO_EM-03 -- every Wilcox Ch. 3 exercise that admits a numeric
check is exercised here (P1-P33), plus the Sec. 3.10 variational bound.

Run directly:   python3 test_bvp_greens.py     (-> "All N tests passed.")
Or with pytest: pytest test_bvp_greens.py

Gaussian units; Green functions obey del^2 G = -4 pi delta (Eq. 3.14).
"""
import numpy as np

from bvp_greens import (
    potential_of_charges, laplacian_fd, laplacian_polar_fd, cauchy_riemann_residual,
    gauss_legendre,
    # Sec. 3.1
    green_plane, green_corner, corner_work, corner_force,
    green_perp_2d, green_perp_2d_images, corner_wall_phi_exact, corner_wall_phi_quad,
    pendulum_energy, pendulum_omega,
    solid_angle_disk, solid_angle_rect, solid_angle_quad, patch_potential,
    # Sec. 3.2
    gf_regulated, gf_regulated_quad, g_reduced_halfspace, green_halfspace_kspace,
    neumann_surface_delta_family, robin_bvp_fd,
    green_plates_images, green_plates_kspace,
    plate_induced_charge, plate_induced_charge_quad, plate_wall_phi_quad,
    # Sec. 3.3
    green_sphere, neutral_shell_phi, green_hemisphere_boss,
    rho_star_total_charge, direct_weighted_charge, image_cloud,
    two_sphere_C, two_sphere_C_matrix, two_sphere_C_system, csys_approx,
    green_cylinder, green_cylinder_images,
    shell_grounded_sphere_phi, shell_grounded_sphere_quad,
    ring_sphere_phi_axis, ring_sphere_phi_axis_quad,
    force_sphere_V, V_zero_force, force_sphere_neutral, energy_sphere_neutral,
    # Sec. 3.5
    box2d_phi, box2d_phi_Ex, solve_laplace_rect,
    strip_An, strip_phi, green_strip_D, strip_phi_from_green, green_strip_N,
    green_2plates_2d_series, green_2plates_2d_closed, green_2plates_2d_images,
    # Sec. 3.6
    green_box3d, madelung_evjen, madelung_from_box_green,
    # Sec. 3.7-3.9
    cyl_delta_series, poisson_kernel, poisson_integral,
    wedge_coeffs, wedge_phi,
    halves_series, halves_closed, halves_axis,
    halves_exterior_series, halves_exterior_closed,
    arctan_series, arctan_series_closed, geometric_cos_sum,
    # Sec. 3.10
    disk_C_variational, disk_C_exact,
    # Sec. 3.11
    map_box_to_halfannulus, semicircle_phi, exterior_from_inversion,
)

RNG = np.random.default_rng(20260706)
M_NACL = -1.747564594  # Eq. (3.108)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- Sec. 3.1: plane, corner, patch (P1-P5) ----------------------------------

def test_p1_plate_images_boundary():
    """Ex. 3.1.1: the image-sum G vanishes on both plates.  With the (2na+z',
    2na-z') grouping the z=0 zero is exact term by term; on z=a the cancelling
    partner straddles the truncation window, so the residual is O(1/N^2)."""
    a = 1.0
    for zp in (0.21, 0.5, 0.83):
        for rho in (0.1, 0.7, 2.3):
            assert abs(green_plates_images(rho, 0.0, zp, a)) < 1e-12
            r200 = abs(green_plates_images(rho, a, zp, a, N=200))
            r800 = abs(green_plates_images(rho, a, zp, a, N=800))
            assert r200 < 1e-4 and r800 < r200 / 10   # -> 0 like 1/N^2


def test_p1_plate_images_absolute_convergence():
    """Ex. 3.1.1: grouped (+,-) image pairs decay ~ 1/n^2 -> absolute convergence."""
    a, zp, z, rho = 1.0, 0.3, 0.6, 0.4
    terms = []
    for n in range(5, 60):
        t = (1 / np.hypot(rho, z - 2 * n * a - zp) - 1 / np.hypot(rho, z - 2 * n * a + zp))
        terms.append(abs(t) * n**2)
    terms = np.array(terms)                       # n^2 |t_n| tends to a constant
    assert terms.max() < 1.0 and abs(terms[-1] - terms[-10]) < 0.01 * terms[-1] + 1e-12
    # symmetry of the Dirichlet Green function
    x = np.array([0.3, -0.2, 0.6]); xp = np.array([-0.1, 0.4, 0.25])
    G1 = green_plates_images(np.hypot(*(x - xp)[:2]), x[2], xp[2], a)
    G2 = green_plates_images(np.hypot(*(x - xp)[:2]), xp[2], x[2], a)
    assert _approx(G1, G2, rel=1e-12)


def test_p1_vs_p8_kspace():
    """Ex. 3.1.1 image sum == Ex. 3.2.3a reduced-Green-function k-integral."""
    a = 1.0
    for (rho, z, zp) in [(0.3, 0.4, 0.7), (0.8, 0.25, 0.6), (0.05, 0.5, 0.31)]:
        Gi = green_plates_images(rho, z, zp, a, N=4000)   # tail ~ zz'/(2N^2 a^3)
        Gk = green_plates_kspace(rho, z, zp, a)
        assert _approx(Gk, Gi, rel=3e-7)


def test_p2_corner_green():
    """Ex. 3.1.2a: G vanishes on both half-plane walls; symmetric in x <-> x'."""
    xp = (0.7, 1.1, 0.2)
    for pt in [(0.0, 0.5, -0.3), (0.0, 2.0, 1.0)]:
        assert abs(green_corner(pt, xp)) < 1e-13
    for pt in [(0.5, 0.0, 0.4), (1.7, 0.0, -2.0)]:
        assert abs(green_corner(pt, xp)) < 1e-13
    assert _approx(green_corner((1.3, 0.4, -0.6), xp),
                   green_corner(xp, (1.3, 0.4, -0.6)), rel=1e-12)


def test_p2_corner_work():
    """Ex. 3.1.2b: W = (1/4)(1/x'+1/y'-1/sqrt(x'^2+y'^2)) equals -int F.dl to inf."""
    x0, y0 = 0.8, 1.3
    # integrate the image force along the straight ray t*(x0,y0), t: 1 -> inf
    # path r(s) = s (x0, y0), s: 1 -> inf; substitute s = 1/t so t: 1 -> 0,
    # ds = -dt/t^2, and W = -int F.dl = -int_0^1 (F . d) dt/t^2
    t, w = gauss_legendre(0.0, 1.0, 400)
    s = 1.0 / t
    d = np.array([x0, y0])
    F = np.array([corner_force(ss * x0, ss * y0) for ss in s])
    W = -np.sum(w * (F @ d) / t**2)
    assert _approx(W, corner_work(x0, y0), rel=1e-6)


def test_p2_corner_wall_potential():
    """Ex. 3.1.2c: Green-surface-integral quadrature == V (1 - 4 phi/pi)."""
    V = 2.0
    for phi in (0.2, np.pi / 4, 1.2):
        got = corner_wall_phi_quad(1.7, phi, V)
        assert _approx(got, corner_wall_phi_exact(phi, V), rel=2e-4, abs_=2e-4)


def test_p3_perp_planes():
    """Ex. 3.1.3: closed form == -2 sum q ln d over four line images; walls at 0."""
    for _ in range(6):
        rho, rhop = RNG.uniform(0.2, 3.0, 2)
        phi, phip = RNG.uniform(0.05, np.pi / 2 - 0.05, 2)
        assert _approx(green_perp_2d(rho, phi, rhop, phip),
                       green_perp_2d_images(rho, phi, rhop, phip), rel=1e-11, abs_=1e-11)
    assert abs(green_perp_2d(1.7, 0.0, 0.9, 0.8)) < 1e-12          # wall phi=0
    assert abs(green_perp_2d(2.4, np.pi / 2, 1.2, 0.3)) < 1e-12    # wall phi=pi/2


def test_p4_pendulum():
    """Ex. 3.1.4: numeric U''(0) = e^2 L/(4(D-L)^2); omega = e/(2(D-L)sqrt(mL))."""
    e, m, L, D = 2.0, 3.0, 1.0, 2.5
    h = 1e-4
    U2 = (pendulum_energy(h, e, L, D) - 2 * pendulum_energy(0.0, e, L, D)
          + pendulum_energy(-h, e, L, D)) / h**2
    assert _approx(U2, e**2 * L / (4 * (D - L) ** 2), rel=1e-6)
    assert _approx(pendulum_omega(e, m, L, D), np.sqrt(U2 / (m * L**2)), rel=1e-6)


def test_p5_solid_angle():
    """Ex. 3.1.5: Phi = (V/2pi)|Omega|: quadrature vs closed forms, both sides."""
    assert _approx(solid_angle_quad((0, 0, 0.6), "disk", R=1.0),
                   solid_angle_disk(0.6, 1.0), rel=1e-8)
    assert _approx(solid_angle_quad((0, 0, -0.6), "disk", R=1.0),
                   solid_angle_disk(0.6, 1.0), rel=1e-8)          # below the plane
    assert _approx(solid_angle_quad((0, 0, 0.8), "rect", wx=1.0, wy=0.5),
                   solid_angle_rect(0.8, 1.0, 0.5), rel=1e-8)
    # under the patch Omega -> 2 pi, so Phi -> V
    V = 3.0
    assert _approx(patch_potential((0, 0, 1e-3), V, patch="disk", R=1.0), V, rel=2e-3)


# --- Sec. 3.2: reduced Green functions (P6-P9) --------------------------------

def test_p6_convergence_factor():
    """Ex. 3.2.1: k-first quadrature == (2/pi R) arctan(R/eps) -> 1/R."""
    R = 1.7
    for eps in (0.5, 0.05, 0.005):
        assert _approx(gf_regulated_quad(R, eps), gf_regulated(R, eps), rel=1e-10)
    assert _approx(gf_regulated(R, 1e-9), 1.0 / R, rel=1e-8)


def test_p7_neumann_halfspace():
    """Ex. 3.2.2a: k-integral of the Neumann reduced G == image form (3.5)."""
    for (rho, z, zp) in [(0.5, 0.8, 0.6), (1.2, 0.4, 1.0)]:
        Gk = green_halfspace_kspace(rho, z, zp, kind="N")
        Gi = green_plane((rho, 0.0, z), (0.0, 0.0, zp), kind="N")
        assert _approx(Gk, Gi, rel=1e-8)
    # Neumann boundary condition dG/dz|_{z=0} = 0 (one-sided difference sees
    # (h/2) G'', so it must vanish linearly in h)
    D = lambda h: (green_plane((0.5, 0, h), (0, 0, 0.7), "N")
                   - green_plane((0.5, 0, 0.0), (0, 0, 0.7), "N")) / h
    assert abs(D(1e-4)) < 1e-3
    assert abs(D(1e-5) / D(1e-4) - 0.1) < 0.02


def test_p7_surface_delta():
    """Ex. 3.2.2b: (1/4pi) dG_N/dn (source on the plane) is a 2-D delta family:
    unit integral for every z, concentrating as z -> 0+ (Eq. 2.115)."""
    for z in (0.5, 0.1, 0.02):
        t, w = gauss_legendre(0.0, np.pi / 2, 200)   # rho = z tan(t) resolves the peak
        r = z * np.tan(t)
        dr = z / np.cos(t) ** 2
        tot = np.sum(w * 2 * np.pi * r * dr * neumann_surface_delta_family(r, z))
        assert _approx(tot, 1.0, rel=1e-10)
    assert (neumann_surface_delta_family(0.0, 0.01)
            > 99 * neumann_surface_delta_family(0.0, 0.1))


def test_p8_induced_charges():
    """Ex. 3.2.3b: Q|z=0 = -(1-z'/a), Q|z=a = -z'/a; they sum to -1."""
    a = 1.0
    for zp in (0.3, 0.62):
        qb = plate_induced_charge_quad(zp, a, "bottom")
        qt = plate_induced_charge_quad(zp, a, "top")
        assert _approx(qb, plate_induced_charge(zp, a, "bottom"), rel=2e-4)
        assert _approx(qt, plate_induced_charge(zp, a, "top"), rel=2e-4)
        assert _approx(qb + qt, -1.0, rel=2e-4)


def test_p8_capacitance():
    """Ex. 3.2.3c: bottom plate at V gives Phi = V(1-z/a), sigma = V/(4 pi a),
    so C = A/(4 pi a)."""
    a, V = 1.0, 2.0
    for z in (0.25, 0.5, 0.75):
        assert _approx(plate_wall_phi_quad(z, a, V), V * (1 - z / a), rel=3e-4)
    sigma = V / (4 * np.pi * a)                    # from the linear profile
    assert _approx(sigma * 1.0 / V, 1.0 / (4 * np.pi * a), rel=1e-12)  # C/A


def test_p9_robin():
    """Ex. 3.2.4: g = (1/2k)[e^{-k|z-z'|} + beta e^{-k(z+z')}],
    beta = (hk-1)/(hk+1): matches an independent FD BVP solve; D/N limits."""
    k, zp, h = 1.3, 0.8, 0.7
    z, g = robin_bvp_fd(k, zp, h)
    for zi in (0.2, 0.5, 1.4):
        i = int(round(zi / (z[1] - z[0])))
        assert _approx(g[i], g_reduced_halfspace(k, zi, zp, "R", h), rel=3e-3)
    # Robin boundary condition g(0) = h g'(0) for the closed form
    dz = 1e-7
    g0 = g_reduced_halfspace(k, 1e-30, zp, "R", h)
    gp = (g_reduced_halfspace(k, dz, zp, "R", h) - g0) / dz
    assert _approx(g0, h * gp, rel=1e-5)
    # h -> 0 Dirichlet, h -> infinity Neumann
    assert _approx(g_reduced_halfspace(k, 0.4, zp, "R", 1e-12),
                   g_reduced_halfspace(k, 0.4, zp, "D"), rel=1e-9)
    assert _approx(g_reduced_halfspace(k, 0.4, zp, "R", 1e12),
                   g_reduced_halfspace(k, 0.4, zp, "N"), rel=1e-9)


# --- Sec. 3.3: spheres and cylinders (P10-P17) --------------------------------

def test_p10_sphere_green():
    """Ex. 3.3.1a: interior image solution vanishes on r=a; total induced -1."""
    a = 1.0
    xp = np.array([0.3, 0.2, 0.4])
    for _ in range(8):
        n = RNG.normal(size=3); n /= np.linalg.norm(n)
        assert abs(green_sphere(a * n, xp, a)) < 1e-12
    # induced surface charge integrates to -1 (all field lines end on the shell)
    ct, w = gauss_legendre(-1.0, 1.0, 400)
    dr = 1e-6
    tot = 0.0
    xp2 = np.array([0.0, 0.0, 0.45])               # axisymmetric source
    for c, ww in zip(ct, w):
        n = np.array([np.sqrt(1 - c**2), 0.0, c])
        # sigma = (1/4pi) dPhi/dn, n = +r-hat (outward normal of the interior volume)
        dGdn = (green_sphere(a * n, xp2, a) - green_sphere((a - dr) * n, xp2, a)) / dr
        tot += ww * 2 * np.pi * a**2 * dGdn / (4 * np.pi)
    assert _approx(tot, -1.0, rel=1e-4)


def test_p10_neutral_shell():
    """Ex. 3.3.1b,c: neutral shell -- continuous at r=a; outside exactly 1/r
    wherever the interior charge sits (its position is invisible)."""
    a = 1.0
    for xp in (np.array([0.0, 0.0, 0.2]), np.array([0.5, 0.1, -0.3])):
        n = np.array([0.36, -0.48, 0.8])
        inn = neutral_shell_phi((a - 1e-9) * n, xp, a)
        out = neutral_shell_phi((a + 1e-9) * n, xp, a)
        assert _approx(inn, out, rel=1e-6)
        assert _approx(neutral_shell_phi(3.0 * n, xp, a), 1.0 / 3.0, rel=1e-12)


def test_p11_hemisphere_boss():
    """Ex. 3.3.2: four images kill G on the plane and on the hemisphere,
    for a source outside the boss (a) and inside the dome (b)."""
    a = 1.0
    for xp in ((1.5, 0.4, 0.9), (0.3, 0.1, 0.5)):   # outside / inside the dome
        for pt in ((2.0, -0.7, 0.0), (1.4, 0.2, 0.0)):
            if np.hypot(*pt[:2]) > a:               # plane outside the boss
                assert abs(green_hemisphere_boss(pt, xp, a)) < 1e-12
        for _ in range(6):
            n = RNG.normal(size=3); n[2] = abs(n[2]); n /= np.linalg.norm(n)
            assert abs(green_hemisphere_boss(a * n, xp, a)) < 1e-12


def test_p12_rho_star():
    """Ex. 3.3.3: rho* = -(a/r)^5 rho(a^2/r): its total charge equals
    -int (a/r') rho d3x' (the point-image rule, element by element), and the
    image cloud zeroes the potential on the sphere."""
    a = 1.0
    rho_f = lambda r, th, ph: np.exp(-((r - 2.0) ** 2) / 0.08) * (1 + 0.5 * np.cos(th))
    Qstar = rho_star_total_charge(rho_f, a, 1.4, 2.6)
    Qrule = direct_weighted_charge(rho_f, a, 1.4, 2.6)
    assert _approx(Qstar, Qrule, rel=1e-8)
    # point-cloud version of the same statement (part b)
    charges = [(RNG.uniform(0.5, 2.0), RNG.normal(size=3) * 0.4 + np.array([2.0, 0, 0]))
               for _ in range(12)]
    cloud = charges + image_cloud(charges, a)
    for _ in range(8):
        n = RNG.normal(size=3); n /= np.linalg.norm(n)
        assert abs(potential_of_charges(a * n, cloud)) < 1e-11


def test_p13_two_spheres():
    """Ex. 3.3.4: C_ab -> -ab/d and C -> ab/(a+b-2ab/d) for d >> a, b."""
    a, b = 1.0, 2.0
    C11, C21 = two_sphere_C(a, b, 40.0)
    assert _approx(C21, -a * b / 40.0, rel=5e-3)
    Cm = two_sphere_C_matrix(a, b, 40.0)
    assert _approx(Cm[0, 1], Cm[1, 0], rel=1e-10)   # symmetry C_ab = C_ba
    for d in (30.0, 60.0):
        exact = two_sphere_C_system(a, b, d)
        assert _approx(csys_approx(a, b, d), exact, rel=2e-3)
    # the asymptotic ratio improves with distance
    r30 = abs(two_sphere_C(a, b, 30.0)[1] / (-a * b / 30.0) - 1)
    r90 = abs(two_sphere_C(a, b, 90.0)[1] / (-a * b / 90.0) - 1)
    assert r90 < r30 / 5


def test_p14_cylinder_green():
    """Ex. 3.3.5: image construction == closed log form; zero on rho=a;
    symmetric; the same expression works outside (part c)."""
    a = 1.0
    for _ in range(6):
        rho, rhop = RNG.uniform(0.15, 0.9, 2)
        phi, phip = RNG.uniform(0, 2 * np.pi, 2)
        assert _approx(green_cylinder(rho, phi, rhop, phip, a),
                       green_cylinder_images(rho, phi, rhop, phip, a), rel=1e-11, abs_=1e-11)
        assert _approx(green_cylinder(rho, phi, rhop, phip, a),
                       green_cylinder(rhop, phip, rho, phi, a), rel=1e-11, abs_=1e-11)
    assert abs(green_cylinder(a, 1.1, 0.6, 2.0, a)) < 1e-12
    assert abs(green_cylinder(a, 0.3, 1.9, 5.1, a)) < 1e-12       # exterior source
    # 2-D Laplacian vanishes away from the source (exterior point, exterior source)
    f = lambda r, p: green_cylinder(r, p, 1.9, 5.1, a)
    assert abs(laplacian_polar_fd(f, 2.6, 1.0, h=1e-4)) < 1e-4


def test_p15_shell_around_grounded_sphere():
    """Ex. 3.3.6: Green-function quadrature over the shell == closed form."""
    a, b, Q = 1.0, 2.0, 3.0
    for r in (1.3, 1.9, 2.5, 4.0):
        assert _approx(shell_grounded_sphere_quad(r, a, b, Q),
                       shell_grounded_sphere_phi(r, a, b, Q), rel=1e-6)
    assert abs(shell_grounded_sphere_phi(a, a, b, Q)) < 1e-12
    assert _approx(shell_grounded_sphere_phi(10.0, a, b, Q), Q * (1 - a / b) / 10.0, rel=1e-12)


def test_p16_ring_around_grounded_sphere():
    """Ex. 3.3.7: on-axis potential closed form == ring quadrature; Phi(+-a)=0;
    induced charge -2 pi a lam; far field (2 pi b lam - 2 pi a lam)/z."""
    a, b, lam = 1.0, 2.0, 0.7
    for z in (1.2, 1.7, 3.0, -2.4):
        assert _approx(ring_sphere_phi_axis_quad(z, a, b, lam),
                       ring_sphere_phi_axis(z, a, b, lam), rel=1e-10, abs_=1e-12)
    assert abs(ring_sphere_phi_axis(a, a, b, lam)) < 1e-12
    assert abs(ring_sphere_phi_axis(-a, a, b, lam)) < 1e-12
    Qring, Qind = 2 * np.pi * b * lam, -2 * np.pi * a * lam
    assert _approx(ring_sphere_phi_axis(500.0, a, b, lam), (Qring + Qind) / 500.0, rel=1e-4)


def test_p17_sphere_forces():
    """Ex. 3.3.8: force from a sphere at V vanishes at V = q d^3/(d^2-a^2)^2;
    neutral-sphere force from the image pair; F = -dU/dd; ~ -2q^2a^3/d^5 far."""
    q, a, d = 2.0, 1.0, 3.0
    assert abs(force_sphere_V(q, V_zero_force(q, a, d), a, d)) < 1e-12
    # neutral force assembled from the two image charges (Coulomb pieces)
    qi, xi = -q * a / d, a**2 / d
    F_pieces = q * (qi / (d - xi) ** 2 + (q * a / d) / d**2)
    assert _approx(force_sphere_neutral(q, a, d), F_pieces, rel=1e-12)
    # F = -dU/dd for U = -q^2 a^3 / (2 d^2 (d^2-a^2))
    h = 1e-6
    F_num = -(energy_sphere_neutral(q, a, d + h) - energy_sphere_neutral(q, a, d - h)) / (2 * h)
    assert _approx(force_sphere_neutral(q, a, d), F_num, rel=1e-7)
    far = 400.0
    assert _approx(force_sphere_neutral(q, a, far), -2 * q**2 * a**3 / far**5, rel=1e-4)


# --- Sec. 3.5: separation of variables (P18-P23) ------------------------------

def test_p18_box_series_vs_fd():
    """Ex. 3.5.1: the odd-sinh series == sparse finite-difference Laplace solve."""
    a, b, V = 1.0, 0.8, 2.0
    x, y, U = solve_laplace_rect(a, b, 81, 65,
                                 bottom=lambda t: 0 * t, top=lambda t: V + 0 * t,
                                 left=lambda t: 0 * t, right=lambda t: 0 * t)
    for (i, j) in [(20, 20), (40, 32), (60, 48), (40, 55)]:
        assert _approx(box2d_phi(x[i], y[j], a, b, V), U[i, j], rel=4e-3, abs_=1e-3)
    assert abs(box2d_phi(0.0, 0.4, a, b, V)) < 1e-12
    assert abs(box2d_phi(a, 0.4, a, b, V)) < 1e-12
    assert abs(box2d_phi(0.5, 0.0, a, b, V)) < 1e-12
    assert abs(laplacian_fd(lambda xx, yy: box2d_phi(xx, yy, a, b, V), 0.43, 0.37)) < 1e-3


def test_p19_strip():
    """Ex. 3.5.2: A_n = -2V/(n pi); boundary data and the y -> inf limit hold."""
    a, V = 1.0, 3.0
    # Fourier check of the coefficients against the y=0 condition
    n = 7
    x, w = gauss_legendre(0.0, a, 400)
    an = (2 / a) * np.sum(w * (-V * (1 - x / a)) * np.sin(n * np.pi * x / a))
    assert _approx(an, strip_An(n, V), rel=1e-10)
    assert _approx(strip_phi(0.0, 0.7, a, V), V, rel=1e-12)        # x=0 wall exactly V
    assert abs(strip_phi(a, 0.7, a, V)) < 1e-12                    # x=a wall
    assert abs(strip_phi(0.31, 0.0, a, V, nmax=20000)) < 2e-3      # y=0 wall (Fourier)
    assert _approx(strip_phi(0.4, 6.0, a, V), V * (1 - 0.4), rel=1e-6)  # far field
    assert abs(laplacian_fd(lambda xx, yy: strip_phi(xx, yy, a, V), 0.37, 0.52)) < 1e-4


def test_p20_green_strip():
    """Ex. 3.5.3: G vanishes on the three walls, is symmetric, carries -4 pi of
    flux, and reproduces the Ex. 3.5.2 potential."""
    a = 1.0
    G = lambda x, y: green_strip_D(x, y, 0.4, 0.6, a)
    assert abs(G(0.0, 0.8)) < 1e-12 and abs(G(a, 0.3)) < 1e-12 and abs(G(0.7, 0.0)) < 1e-12
    assert _approx(green_strip_D(0.2, 0.9, 0.4, 0.6, a),
                   green_strip_D(0.4, 0.6, 0.2, 0.9, a), rel=1e-10)
    # flux of grad G through a small square around the source = -4 pi
    # (large nmax: on the box sides that cross y = y' the series is oscillatory)
    G = lambda x, y: green_strip_D(x, y, 0.4, 0.6, a, nmax=4000)
    s, h = 0.12, 1e-5
    t, w = gauss_legendre(-s, s, 200)
    flux = 0.0
    for (dx, dy, nx, ny) in [(s, None, 1, 0), (-s, None, -1, 0), (None, s, 0, 1), (None, -s, 0, -1)]:
        if dx is not None:
            pts = [(0.4 + dx, 0.6 + tt) for tt in t]
            d = [(G(px + h * nx, py) - G(px - h * nx, py)) / (2 * h) for px, py in pts]
        else:
            pts = [(0.4 + tt, 0.6 + dy) for tt in t]
            d = [(G(px, py + h * ny) - G(px, py - h * ny)) / (2 * h) for px, py in pts]
        flux += np.sum(w * np.array(d))
    assert _approx(flux, -4 * np.pi, rel=1e-4)
    # part (b): the recovered potential == Ex. 3.5.2 potential.  The two forms
    # differ by the sawtooth series (2V/pi) sum sin(n pi x/a)/n = V(1 - x/a),
    # which converges only ~1/N -- hence the large partial sum here.
    a_, V = 1.0, 3.0
    for (x, y) in [(0.3, 0.4), (0.7, 1.1), (0.5, 0.05)]:
        assert _approx(strip_phi_from_green(x, y, a_, V, nmax=60000),
                       strip_phi(x, y, a_, V), rel=3e-4, abs_=3e-4)


def test_p21_green_strip_neumann():
    """Ex. 3.5.4: dG/dn = 0 on all three walls; the -4 pi y>/a term carries the
    mandatory -4 pi of flux out of the open end (Eq. 2.102); symmetric."""
    a = 1.0
    G = lambda x, y: green_strip_N(x, y, 0.35, 0.7, a)
    # one-sided differences see (h/2) G''(0): check they vanish linearly in h
    for D in (lambda h: (G(h, 0.5) - G(0.0, 0.5)) / h,              # x=0 wall
              lambda h: (G(a, 0.5) - G(a - h, 0.5)) / h,            # x=a wall
              lambda h: (G(0.6, h) - G(0.6, 0.0)) / h):             # y=0 wall
        assert abs(D(1e-4)) < 1e-3
        assert abs(D(1e-5) / D(1e-4) - 0.1) < 0.02                  # ~ prop. to h
    assert _approx(green_strip_N(0.2, 0.9, 0.35, 0.7, a),
                   green_strip_N(0.35, 0.7, 0.2, 0.9, a), rel=1e-10)
    # flux through the cross-section y = 3a (only the secular term survives)
    x, w = gauss_legendre(0.0, a, 200)
    h = 1e-6
    dGdy = np.array([(G(xx, 3.0 + h) - G(xx, 3.0 - h)) / (2 * h) for xx in x])
    assert _approx(np.sum(w * dGdy), -4 * np.pi, rel=1e-8)


def test_p22_two_plates_2d():
    """Ex. 3.5.5: g_n = (4/n) e^{-n pi |y-y'|/a}: series == closed form == image
    line charges; G vanishes on x=0 and x=a."""
    a = 1.0
    for _ in range(5):
        x, xp = RNG.uniform(0.1, 0.9, 2)
        y, yp = RNG.uniform(-1.0, 1.0, 2)
        Gs = green_2plates_2d_series(x, y, xp, yp, a)
        Gc = green_2plates_2d_closed(x, y, xp, yp, a)
        Gi = green_2plates_2d_images(x, y, xp, yp, a)
        assert _approx(Gs, Gc, rel=1e-10, abs_=1e-10)
        assert _approx(Gi, Gc, rel=1e-6, abs_=1e-6)
    assert abs(green_2plates_2d_closed(0.0, 0.3, 0.5, -0.2, a)) < 1e-12
    assert abs(green_2plates_2d_closed(a, 0.3, 0.5, -0.2, a)) < 1e-12


def test_p23_box_Ex():
    """Ex. 3.5.6: series with V(x) = -Ex on y=b == finite-difference solve."""
    a, b, E = 1.0, 0.8, 1.5
    x, y, U = solve_laplace_rect(a, b, 81, 65,
                                 bottom=lambda t: 0 * t, top=lambda t: -E * t,
                                 left=lambda t: 0 * t, right=lambda t: 0 * t)
    for (i, j) in [(20, 20), (40, 32), (60, 48)]:
        assert _approx(box2d_phi_Ex(x[i], y[j], a, b, E), U[i, j], rel=5e-3, abs_=2e-3)


# --- Sec. 3.6: box eigenfunction Green function, Madelung (P24) ----------------

def test_p24_box_green_reciprocity():
    """Eq. 3.98 is symmetric: G(x, x') = G(x', x)."""
    x = (0.31, 0.52, 0.63); xp = (0.72, 0.28, 0.44)
    assert _approx(green_box3d(x, xp, nmax=60), green_box3d(xp, x, nmax=60), rel=1e-10)


def test_p24_box_green_point_charge():
    """Eq. 3.98 -> 1/|x-x'| at short distance (the unit source dominates)."""
    x = np.array([0.5, 0.5, 0.5])
    for eps in (0.1, 0.05):
        xp = x + np.array([0.0, 0.0, eps])
        G = green_box3d(x, xp, nmax=400)
        # G = 1/eps + M + O(eps^2) at the centre, with M ~ -1.75 (Ex. 3.6.1)
        assert abs(G * eps - 1.0) < 2.5 * eps
    G1, G2 = [green_box3d(x, x + np.array([0, 0, e]), nmax=400) for e in (0.1, 0.05)]
    assert _approx((G1 - 1 / 0.1), (G2 - 1 / 0.05), rel=0.0, abs_=0.02)


def test_p24_madelung():
    """Ex. 3.6.1: M from the regularized box Green function, to 3+ decimals,
    against the lattice value -1.747564594 (Eq. 3.108); Evjen cross-check."""
    assert abs(madelung_evjen(14) - M_NACL) < 2e-6
    assert abs(madelung_from_box_green() - M_NACL) < 5e-4


# --- Sec. 3.7-3.9: polar problems (P25-P31) -----------------------------------

def test_p25_cylinder_delta_series():
    """Ex. 3.7.1: the Fourier series sums to the Poisson kernel; mean value V0/2pi."""
    b, V0 = 1.0, 2.0
    for (rho, phi) in [(0.3, 0.7), (0.8, 2.4), (0.5, -1.1)]:
        assert _approx(cyl_delta_series(rho, phi, b, V0),
                       V0 * poisson_kernel(rho, phi, b), rel=1e-10)
    assert _approx(cyl_delta_series(0.0, 0.3, b, V0), V0 / (2 * np.pi), rel=1e-12)


def test_p26_wedge():
    """Ex. 3.8.1: manufactured single-mode data is recovered exactly; general
    data is reproduced at rho -> b; the corner field scales as rho^{pi/beta - 1}."""
    b, beta, V = 1.0, 2.0, 0.5
    # manufactured: f(phi) = V + b^{pi/beta} sin(pi phi/beta)  ->  a_1 = 1 only
    f1 = lambda t: V + b ** (np.pi / beta) * np.sin(np.pi * t / beta)
    c = wedge_coeffs(f1, V, b, beta, mmax=12)
    assert _approx(c[0], 1.0, rel=1e-9) and np.all(np.abs(c[1:]) < 1e-9)
    assert _approx(wedge_phi(0.6, 0.9, V, beta, c),
                   V + 0.6 ** (np.pi / beta) * np.sin(np.pi * 0.9 / beta), rel=1e-9)
    # general data: series at rho=0.999b vs the boundary function
    f2 = lambda t: V + np.sin(np.pi * t / beta) ** 3 + 0.2 * np.sin(2 * np.pi * t / beta)
    c2 = wedge_coeffs(f2, V, b, beta, mmax=40)
    for phi in (0.4, 1.0, 1.6):
        assert _approx(wedge_phi(0.999 * b, phi, V, beta, c2), f2(phi), rel=3e-3)
    assert _approx(wedge_phi(0.5, 0.0, V, beta, c2), V, abs_=1e-12)   # side at V
    # corner scaling (Eq. 3.123): log-slope of |Phi - V| ~ pi/beta
    r1, r2 = 1e-3, 2e-3
    s = (np.log(abs(wedge_phi(r2, beta / 2, V, beta, c2) - V))
         - np.log(abs(wedge_phi(r1, beta / 2, V, beta, c2) - V))) / np.log(r2 / r1)
    assert abs(s - np.pi / beta) < 1e-3


def test_p27_poisson_integral():
    """Ex. 3.9.1: the kernel has unit integral, reproduces harmonic data
    (cos phi' -> (rho/b) cos phi), and is harmonic in the interior."""
    b = 1.0
    t, w = gauss_legendre(0.0, 2 * np.pi, 400)
    assert _approx(np.sum(w * poisson_kernel(0.6, 0.9 - t, b)), 1.0, rel=1e-12)
    for (rho, phi) in [(0.3, 0.4), (0.75, 2.0)]:
        got = poisson_integral(rho, phi, b, lambda tt: np.cos(tt))
        assert _approx(got, (rho / b) * np.cos(phi), rel=1e-10)
    f = lambda r, p: poisson_integral(r, p, b, lambda tt: np.sign(np.cos(tt)))
    assert abs(laplacian_polar_fd(f, 0.5, 0.8, h=1e-4)) < 1e-5


def test_p28_halves_via_poisson():
    """Ex. 3.9.2: Poisson integral of the two-valued boundary data == Eq. 3.131."""
    b, V1, V2 = 1.0, 2.0, -1.0
    f = lambda t: np.where(np.cos(t) > 0, V1, V2)
    for (rho, phi) in [(0.3, 0.2), (0.6, 1.0), (0.85, 2.6), (0.5, -0.9)]:
        got = poisson_integral(rho, phi, b, f, breaks=(np.pi / 2, 3 * np.pi / 2))
        assert _approx(got, halves_closed(rho, phi, b, V1, V2), rel=1e-9, abs_=1e-9)


def test_p29_sum_the_series():
    """Ex. 3.9.3: sum Z^{2n+1}/(2n+1) identity -> (3.130) == (3.131); on the
    symmetry axis the closed form collapses to (2/pi)(V1-V2) arctan(rho/b)."""
    for _ in range(6):
        t = RNG.uniform(0.05, 0.95)
        psi = RNG.uniform(-np.pi, np.pi)
        assert _approx(arctan_series(t, psi), arctan_series_closed(t, psi),
                       rel=1e-10, abs_=1e-12)
    b, V1, V2 = 1.0, 3.0, 1.0
    for (rho, phi) in [(0.4, 0.9), (0.7, -2.1), (0.2, 0.0)]:
        assert _approx(halves_series(rho, phi, b, V1, V2),
                       halves_closed(rho, phi, b, V1, V2), rel=1e-10)
    for rho in (0.2, 0.5, 0.9):
        assert _approx(halves_closed(rho, 0.0, b, V1, V2),
                       halves_axis(rho, b, V1, V2), rel=1e-12)


def test_p30_exterior_halves():
    """Ex. 3.9.4: exterior series == closed form; interior <-> exterior by
    rho/b -> b/rho; boundary values match; rho -> inf gives the average."""
    b, V1, V2 = 1.0, 2.0, -0.5
    for (rho, phi) in [(1.3, 0.4), (2.5, 2.0), (5.0, -1.2)]:
        assert _approx(halves_exterior_series(rho, phi, b, V1, V2),
                       halves_exterior_closed(rho, phi, b, V1, V2), rel=1e-10)
        assert _approx(halves_exterior_closed(rho, phi, b, V1, V2),
                       halves_closed(b**2 / rho, phi, b, V1, V2), rel=1e-12)
    assert _approx(halves_exterior_closed(1e6, 1.0, b, V1, V2), (V1 + V2) / 2, rel=1e-5)
    assert _approx(halves_exterior_closed(1.0 + 1e-9, 0.3, b, V1, V2), V1, rel=1e-6)


def test_p31_sum_delta_series():
    """Ex. 3.9.5: 1/2 + sum t^m cos == (1/2)(1-t^2)/(1+t^2-2t cos), so the
    Ex. 3.7.1 series is exactly V0 x Poisson kernel (compare Ex. 3.9.1)."""
    for _ in range(6):
        t = RNG.uniform(0.05, 0.95)
        phi = RNG.uniform(-np.pi, np.pi)
        closed = 0.5 * (1 - t**2) / (1 + t**2 - 2 * t * np.cos(phi))
        assert _approx(geometric_cos_sum(t, phi), closed, rel=1e-10)


# --- Sec. 3.10: variational lower bound (notes check; no exercise) -------------

def test_variational_disk_bound():
    """Thompson bound (3.144): C_var = Q^2/2W <= C_exact = 2R/pi.  The uniform
    trial gives the classic 3 pi R/16; the exact edge density saturates."""
    R = 1.0
    C_u = disk_C_variational(lambda r: np.ones_like(r), R)
    C_star = disk_C_variational(lambda r: 1.0 / np.sqrt(np.clip(R**2 - r**2, 1e-30, None)), R)
    C_ex = disk_C_exact(R)
    assert C_u < 0.97 * C_ex                       # strictly below the true C
    assert abs(C_u - 3 * np.pi * R / 16) < 2e-3    # the classic uniform-trial value
    assert abs(C_star - C_ex) < 0.02 * C_ex        # exact density ~saturates
    assert C_u < C_star                             # better trial, better bound


# --- Sec. 3.11: conformal mapping (P32-P33) ------------------------------------

def test_p32_map_and_boundaries():
    """Ex. 3.11.1a: w = e^{pi z/b} is conformal (Cauchy-Riemann, f' != 0) and
    sends the a x b box boundary onto the half-annulus boundary, the y=b side
    landing on (-r0, -1)."""
    a, b = 1.2, 0.8
    r0 = np.exp(np.pi * a / b)
    f = lambda z: map_box_to_halfannulus(z, b)
    for z in (0.3 + 0.2j, 1.0 + 0.7j, 0.1 + 0.05j):
        assert cauchy_riemann_residual(f, z) < 1e-4
        assert abs(f(z)) > 0
    for x in np.linspace(0.01, a - 0.01, 7):
        w = f(x + 1j * b)                          # the V side
        assert abs(w.imag) < 1e-12 and -r0 < w.real < -1
        w0 = f(x + 0j)                             # grounded bottom
        assert abs(w0.imag) < 1e-12 and 1 < w0.real < r0
    for y in np.linspace(0.01, b - 0.01, 7):
        assert _approx(abs(f(0 + 1j * y)), 1.0, rel=1e-12)      # inner arc
        assert _approx(abs(f(a + 1j * y)), r0, rel=1e-12)       # outer arc


def test_p32_semicircle_potential():
    """Ex. 3.11.1b: the half-annulus series == the box series pulled back
    through the map (x = b ln r/pi, y = b theta/pi); harmonic; V-side data."""
    a, b, V = 1.2, 0.8, 2.0
    r0 = np.exp(np.pi * a / b)
    for (r, th) in [(2.0, 1.0), (5.0, 2.2), (1.5, 0.4)]:
        x, y = b * np.log(r) / np.pi, b * th / np.pi
        assert _approx(semicircle_phi(r, th, r0, V), box2d_phi(x, y, a, b, V),
                       rel=1e-9, abs_=1e-9)
    f = lambda rr, tt: semicircle_phi(rr, tt, r0, V)
    assert abs(laplacian_polar_fd(f, 3.0, 1.2, h=1e-4)) < 1e-5
    assert abs(semicircle_phi(1.0, 1.5, r0, V)) < 1e-12          # inner arc grounded
    assert abs(semicircle_phi(r0, 1.5, r0, V)) < 1e-12           # outer arc grounded
    assert _approx(semicircle_phi(np.sqrt(r0), np.pi - 1e-4, r0, V, nmax=4001), V, rel=2e-3)


def test_p33_inversion_map():
    """Ex. 3.11.2: w = b^2/z pulls the interior solution (3.131) back to the
    exterior -- identical to the Ex. 3.9.4 closed form; harmonic outside."""
    b, V1, V2 = 1.0, 2.0, -1.0
    for (rho, phi) in [(1.4, 0.7), (3.0, 2.5), (8.0, -0.4)]:
        assert _approx(exterior_from_inversion(rho, phi, b, V1, V2),
                       halves_exterior_closed(rho, phi, b, V1, V2), rel=1e-12)
    f = lambda rr, pp: exterior_from_inversion(rr, pp, b, V1, V2)
    assert abs(laplacian_polar_fd(f, 2.0, 1.0, h=1e-4)) < 1e-6
    g = lambda z: b**2 / z
    for z in (1.5 + 0.5j, 2.0 - 1.0j):
        assert cauchy_riemann_residual(g, z) < 1e-6


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import time
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    t0 = time.time()
    for name, fn in tests:
        fn()
        print(f"  {name}: ok")
    print(f"({time.time() - t0:.1f} s)")
    print(f"All {len(tests)} tests passed.")
