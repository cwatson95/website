"""Tests for MACRO_EM-05 -- every Wilcox Ch. 5 exercise (P1-P49) gets a numeric
check here.

Run directly:   python3 test_multipole_dielectrics.py   (-> "All N tests passed.")
Or with pytest: pytest test_multipole_dielectrics.py

Gaussian units; div[eps grad G] = -4 pi delta (Eq. 5.72)."""
import numpy as np

from multipole_dielectrics import (
    gauss_legendre, grad_fd, hess_fd,
    # 5.1
    moments_point_charges, moments_translate, phi_multipole, phi_exact_charges,
    E_exact_charges, cube_moments_Kx, octopole_R, phi_octopole_term,
    octopole_independent_count, linear_quadrupole_phi, dipole_phi,
    dipole_above_plane_phi, sigma_dipole_plane, rho_lm,
    # 5.2-5.3
    quad_energy_in_potential, quad_force_axial, E_dipole, quad_dipole_force_x,
    W_quad_quad_perp, W_quad_quad_axial, linear_quadrupole_charges,
    W_charges_pair, sphere_image_W_sum, sphere_image_W_closed,
    force_multipole, force_exact, torque_multipole, torque_exact,
    point_charge_E_derivs,
    # 5.4
    quad_density_check, bound_from_free, sphere_center_charge_sigma_b,
    cylinder_in_field_phi, polarized_sphere_surface_E,
    solid_angle_square_from_center, clausius_mossotti_alpha, chi_from_alpha,
    # 5.6
    corner_dielectric_G, corner_dielectric_G_region, corner_interface_residuals,
    g_slab_conductor_book, g_slab_conductor_solve, g_slab_swapped_solve,
    oneD_G_dielectric, oneD_G_fd, two_halfspace_phi, slab_finite_solve,
    g_halfspace_dielectric,
    # 5.7
    gm_cyl2d, G_cyl2d, cyl3d_gm_solve, G_cyl3d,
    sphere_G_out, sphere_G_out_induced, sphere_G_in, sphere_gl_solve,
    sphere_uniform_field_phi, sphere_source_inside_coeffs,
    sphere_source_inside_solve, sphere_G_source_inside,
    bubble_G_out, bubble_gl_solve, sphere_dipole_p_eff, sphere_dipole_E_in,
    sphere_in_conductor_solve, grounded_sphere_interior_gl,
    plane_sigma_phi_in, plane_moment_integral,
    ring_sphere_phi_in, ring_sphere_phi_in_points,
    Il_int_P, split_sphere_C, split_sphere_Q1_quad,
    coaxial_cyl_solve, G_coaxial, G_grounded_cylinder_2d,
    induced_quadrupole_sphere, sphere_sigma_b_series, induced_quadrupole_from_sigma,
    # 5.8-5.9
    polarized_sphere_ED_integral, polarized_sphere_Wint,
    halfspace_fields_at_interface, surface_force_from_fields,
    surface_force_from_sigma_b, surface_force_free_bound,
    halfspace_force_image, halfspace_deltaW, halfspace_force_stress,
    rod_force_perp, rod_force_par, rod_W_perp, rod_W_par,
    prolate_depolarization_nz, spheroid_E_in_axial,
    capacitor_C_partial, capacitor_force_fixed_V, capacitor_force_fixed_Q,
    slab_deltaW, slab_force_integral, slab_force_weak,
    plate_sigma_kspace, plate_force_kspace, two_plate_Wind, plate_force_images,
    plate_sigma_images,
    layered_capacitor_force_V, layered_capacitor_force_Q,
    line_cylinder_deltaW, line_cylinder_force,
    # 5.10-5.11
    leading_log_perfect_differential_check, leading_log_d2W_integrand,
    sphere_charge_deltaW_series, sphere_charge_force_far,
    bubble_charge_deltaW_series, bubble_charge_force_far, sphere_deltaW_from_P,
    droplet_inside_force_series, droplet_deltaW,
    sphere_dipole_W, sphere_dipole_force, sphere_dipole_W_exact,
)

RNG = np.random.default_rng(20260706)


def _close(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * max(abs(x), abs(y)), abs_)


def _vclose(x, y, rel=1e-9, abs_=0.0):
    x = np.asarray(x, float); y = np.asarray(y, float)
    return np.linalg.norm(x - y) <= max(rel * max(np.linalg.norm(x),
                                                  np.linalg.norm(y)), abs_)


# --- Sec. 5.1 (P1-P6) --------------------------------------------------------

def test_p01_dipole_killing_origin():
    """Ex. 5.1.1: for q != 0 the shift R = p/q makes p' = 0 (theorem TRUE)."""
    for _ in range(5):
        qs = RNG.normal(size=7); qs[0] += 3.0     # ensure q != 0
        Xs = RNG.normal(size=(7, 3))
        q, p, Q = moments_point_charges(qs, Xs)
        assert abs(q) > 0.1
        _, p2, _ = moments_point_charges(qs, Xs - (p / q)[None, :])
        assert np.linalg.norm(p2) < 1e-12 * np.linalg.norm(Xs)
    # and for q = 0 the dipole moment is origin-independent
    qs = np.array([1.0, -1.0, 2.0, -2.0]); Xs = RNG.normal(size=(4, 3))
    _, pA, _ = moments_point_charges(qs, Xs)
    _, pB, _ = moments_point_charges(qs, Xs - np.array([0.3, -1.2, 0.7]))
    assert _vclose(pA, pB, 1e-12)


def test_p02_moment_translation():
    """Ex. 5.1.2 closed forms vs direct recomputation about the shifted origin."""
    for _ in range(6):
        qs = RNG.normal(size=6); Xs = RNG.normal(size=(6, 3))
        R = RNG.normal(size=3)
        q, p, Q = moments_point_charges(qs, Xs)
        qt, pt, Qt = moments_translate(q, p, Q, R)
        qd, pd, Qd = moments_point_charges(qs, Xs - R[None, :])
        assert _close(qt, qd, 1e-12, 1e-14)
        assert _vclose(pt, pd, 1e-11)
        assert np.max(np.abs(Qt - Qd)) < 1e-10 * max(1.0, np.max(np.abs(Qd)))


def test_p03_cube_rho_Kx():
    """Ex. 5.1.3: rho = Kx in a cube: q=0, p = K L^5/12 xhat, Q = 0; far field
    is the ideal dipole field."""
    K, L = 2.0, 1.3
    q, p, Q = cube_moments_Kx(K, L)
    assert abs(q) < 1e-12
    assert _vclose(p, [K * L ** 5 / 12, 0, 0], 1e-10)
    assert np.max(np.abs(Q)) < 1e-10
    # far field: compare quadrature potential to dipole term
    x = np.array([2.9, -1.7, 2.2]) * 4.0
    n = 20
    xn, wn = gauss_legendre(-L / 2, L / 2, n)
    X, Y, Z = np.meshgrid(xn, xn, xn, indexing='ij')
    W = wn[:, None, None] * wn[None, :, None] * wn[None, None, :]
    d = np.sqrt((x[0] - X) ** 2 + (x[1] - Y) ** 2 + (x[2] - Z) ** 2)
    phi_ex = np.sum(W * K * X / d)
    r = np.linalg.norm(x)
    assert _close(phi_ex, (x @ p) / r ** 3, 2e-4)


def test_p04_octopole():
    """Ex. 5.1.4: R_ijk term reproduces the next correction; 7 independent
    components; symmetric and traceless on every index pair."""
    qs = RNG.normal(size=8); Xs = 0.5 * RNG.normal(size=(8, 3))
    q, p, Q = moments_point_charges(qs, Xs)
    R3 = octopole_R(qs, Xs)
    # symmetry + traces
    assert np.max(np.abs(R3 - np.transpose(R3, (1, 0, 2)))) < 1e-12
    assert np.max(np.abs(R3 - np.transpose(R3, (0, 2, 1)))) < 1e-12
    for k in range(3):
        assert abs(np.trace(R3[:, :, k])) < 1e-10
    # the octopole term captures the residual of the 3-term expansion
    for xhat in ([1, 0.3, -0.2], [0.1, -1, 0.5], [0.4, 0.7, 1.0]):
        xhat = np.array(xhat) / np.linalg.norm(xhat)
        for r in (8.0, 16.0):
            x = r * xhat
            resid = phi_exact_charges(x, qs, Xs) - phi_multipole(x, q, p, Q)
            oct_ = phi_octopole_term(x, R3)
            assert _close(resid, oct_, 0.25)   # next order is O(1/r) smaller
    assert octopole_independent_count() == 7


def test_p05_linear_quadrupole():
    """Ex. 5.1.5: q=0, p=0, Q = diag(-2a^2,-2a^2,4a^2); Phi -> 2a^2 P2/r^3;
    matches the Taylor expansion of the exact potential."""
    a = 0.01
    qs, Xs = linear_quadrupole_charges(a)
    q, p, Q = moments_point_charges(qs, Xs)
    assert abs(q) < 1e-14 and np.linalg.norm(p) < 1e-14
    assert _vclose(np.diag(Q), [-2 * a ** 2, -2 * a ** 2, 4 * a ** 2], 1e-12)
    for th in (0.3, 1.1, 2.4):
        x = 1.0 * np.array([np.sin(th), 0, np.cos(th)])
        phiq = 0.5 * (x @ Q @ x)
        assert _close(phiq, linear_quadrupole_phi(x, a), 1e-12, 1e-18)
        # exact potential agrees to O((a/r)^2) relative
        assert _close(phi_exact_charges(x, qs, Xs), linear_quadrupole_phi(x, a),
                      5e-4, 1e-12)


def test_p06_dipole_over_plane():
    """Ex. 5.1.6: image-dipole potential vanishes on the plane; sigma formula
    matches -(1/4pi) dPhi/dz; total induced charge = 0."""
    p = np.array([0.4, -0.7, 1.2]); d = 1.5
    for rho, ph in ((0.3, 0.2), (1.7, 2.5), (4.0, 4.4)):
        x = np.array([rho * np.cos(ph), rho * np.sin(ph), 0.0])
        assert abs(dipole_above_plane_phi(x, p, d)) < 1e-12
    # sigma for vertical dipole
    pz = 0.8
    for rho in (0.0, 0.7, 2.0, 5.0):
        x0 = np.array([rho, 0, 0])
        h = 1e-6
        dphidz = (dipole_above_plane_phi(x0 + [0, 0, h], [0, 0, pz], d)
                  - dipole_above_plane_phi(x0 + [0, 0, 0], [0, 0, pz], d)) / h
        sig_fd = -dphidz / (4 * np.pi)
        assert _close(sig_fd, sigma_dipole_plane(rho, pz, d), 2e-5, 1e-12)
    # total induced charge -> 0 (cumulative integral to P falls off as pz/P)
    rn = np.linspace(0.0, 2000 * d, 200001)
    Qtot = np.trapezoid(2 * np.pi * rn * sigma_dipole_plane(rn, pz, d), rn)
    assert abs(Qtot) < 1e-3 * pz


def test_p0x_spherical_moments():
    """(5.39) check: (rho)_10 = p_z, (rho)_11 = (-p_x + i p_y)/sqrt(2)."""
    qs = RNG.normal(size=6); Xs = RNG.normal(size=(6, 3))
    _, p, _ = moments_point_charges(qs, Xs)
    r10 = rho_lm(qs, Xs, 1, 0)
    r11 = rho_lm(qs, Xs, 1, 1)
    assert _close(r10.real, p[2], 1e-10, 1e-12) and abs(r10.imag) < 1e-12
    assert _close(r11.real, -p[0] / np.sqrt(2), 1e-10, 1e-12)
    assert _close(r11.imag, p[1] / np.sqrt(2), 1e-10, 1e-12)


# --- Sec. 5.2 (P7-P9) --------------------------------------------------------

def test_p07_quad_energy_and_force():
    """Ex. 5.2.1(a): W = (1/4) Q33 d2Phi/dz2 (= (1/6)Q:HessPhi) and
    F = (1/4) Q33 d2E/dz2; (b): F1 = -3 Q33 px/x1^5, checked microscopically."""
    a = 1e-3
    qs, Xs = linear_quadrupole_charges(a)
    _, _, Q = moments_point_charges(qs, Xs)
    Q33 = Q[2, 2]
    y0 = np.array([2.0, 1.0, 3.0])            # external unit charge here
    E, dE, _ = point_charge_E_derivs(np.zeros((1, 3)), y0)
    HessPhi = -dE[0]                          # Phi = 1/|x-y0|
    W14 = 0.25 * Q33 * HessPhi[2, 2]
    W16 = quad_energy_in_potential(Q, HessPhi)
    assert _close(W14, W16, 1e-12)
    # W formula matches the microscopic energy sum q_i Phi(x_i)
    Wmicro = sum(qi * 1.0 / np.linalg.norm(np.asarray(xi) - y0)
                 for qi, xi in zip(qs, Xs))
    assert _close(W16, Wmicro, 1e-4)
    # force = (1/4) Q33 d2E/dz2 equals -grad W and the microscopic force
    def Wfun(x0):
        _, dEl, _ = point_charge_E_derivs(x0[None, :], y0)
        return 0.25 * Q33 * (-dEl[0][2, 2])
    F_formula = quad_force_axial(Q33, lambda x: point_charge_E_derivs(
        x[None, :], y0)[0][0], np.zeros(3))
    F_gradW = -grad_fd(Wfun, np.zeros(3), h=1e-4)
    assert _vclose(F_formula, F_gradW, 1e-5)
    # (b) dipole at (x1,0,0)
    p = np.array([0.6, -0.3, 0.9]); x1 = 2.0
    F1_formula = quad_dipole_force_x(Q33, p, x1)
    Fvec = quad_force_axial(Q33, lambda x: E_dipole(x, p, [x1, 0, 0]),
                            np.zeros(3), h=1e-3)
    assert _close(Fvec[0], F1_formula, 1e-5)
    # microscopic: quadrupole charges in the field of a 2-charge dipole
    delta = 1e-4
    qd = np.linalg.norm(p) / delta; ph = p / np.linalg.norm(p)
    dq = [qd, -qd]; dX = [np.array([x1, 0, 0]) + 0.5 * delta * ph,
                          np.array([x1, 0, 0]) - 0.5 * delta * ph]
    Fmicro = np.zeros(3)
    for qi, xi in zip(qs, Xs):
        Fmicro += qi * E_exact_charges(np.asarray(xi, float), dq, dX)
    assert _close(Fmicro[0], F1_formula, 5e-4)


def test_p08_quad_quad_energy():
    """Ex. 5.2.2: microscopic point-charge sums confirm W = +(9/16) Q1 Q2/r^5
    (perp config; the book's -9/16 is a sign erratum) and +(3/2) Q1 Q2/r^5
    (axial 'Extra'), with O(a^2) convergence to the formulas."""
    r = 1.0
    for a in (0.05, 0.025):
        qs1, X1 = linear_quadrupole_charges(a)
        qs2, X2 = linear_quadrupole_charges(a, center=(r, 0, 0))
        Wm = W_charges_pair(qs1, X1, qs2, X2)
        Wf = W_quad_quad_perp(4 * a * a, 4 * a * a, r)
        assert Wm > 0 and _close(Wm, Wf, 12 * a * a)
        qs3, X3 = linear_quadrupole_charges(a, center=(0, 0, r))
        Wm3 = W_charges_pair(qs1, X1, qs3, X3)
        Wf3 = W_quad_quad_axial(4 * a * a, 4 * a * a, r)
        assert Wm3 > 0 and _close(Wm3, Wf3, 30 * a * a)


def test_p09_sphere_multipole_sum():
    """Ex. 5.2.3: the (5.32)/(5.37) multipole series sums to the image-charge
    energy -q^2 R/[D^2(1-R^2/D^2)]."""
    q, R, D = 2.0, 1.0, 1.7
    closed = sphere_image_W_closed(q, R, D)
    assert _close(sphere_image_W_sum(q, R, D, 200), closed, 1e-12)
    # geometric convergence: L-term truncation error ~ (R^2/D^2)^{L+1}
    e10 = abs(sphere_image_W_sum(q, R, D, 10) - closed)
    e20 = abs(sphere_image_W_sum(q, R, D, 20) - closed)
    assert e20 < e10 * (R * R / (D * D)) ** 8
    # and W equals the image formula q q'/(D - R^2/D)
    qp = -q * R / D
    assert _close(closed, q * qp / (D - R * R / D), 1e-12)


# --- Sec. 5.3 (P10) ----------------------------------------------------------

def test_p10_force_torque_multipole():
    """Ex. 5.3.1: multipole force (alternate form) and torque vs exact sums for
    a compact random cloud in the field of external charges; error shrinks
    with cloud size (next order is octopole)."""
    src_q = [1.5, -2.0, 0.7]
    src_X = [np.array([3.0, 0.5, -0.2]), np.array([-2.5, 2.0, 1.0]),
             np.array([0.5, -3.0, 2.0])]
    def E_ext(x):
        return E_exact_charges(x, src_q, src_X)
    errs = []
    for s in (0.2, 0.1):
        qs = RNG.normal(size=8)
        Xs = s * RNG.normal(size=(8, 3))
        F_m = force_multipole(qs, Xs, E_ext)
        F_e = force_exact(qs, Xs, E_ext)
        N_m = torque_multipole(qs, Xs, E_ext)
        N_e = torque_exact(qs, Xs, E_ext)
        errs.append(np.linalg.norm(F_m - F_e) / np.linalg.norm(F_e))
        assert _vclose(F_m, F_e, 0.05)
        assert _vclose(N_m, N_e, 0.05)
    assert errs[1] < errs[0]


# --- Sec. 5.4 (P11-P15) ------------------------------------------------------

def test_p11_quadrupole_effective_densities():
    """Ex. 5.4.1: int (1/6) q_ij d_i d_j E = int rho_eff^Q E + oint sigma_eff^Q E
    + oint (P_eff^Q . grad) E, by quadrature for the anisotropic density
    q_ij = x_1 (1+r^2/Rb^2) T_ij."""
    Fdir, Fsum = quad_density_check(Rb=1.0, x0=np.array([2.5, 1.0, 1.8]))
    assert np.linalg.norm(Fdir) > 1e-4          # non-degenerate test density
    assert _vclose(Fdir, Fsum, 2e-4)


def test_p12_bound_free_charge():
    """Ex. 5.4.2: rho_b = ((1-eps)/eps) rho_f; total bound surface charge
    (eps-1)Q_f/eps -- checked on the sphere-with-central-charge solution."""
    eps, q, a = 3.5, 2.0, 1.2
    sig, tot = sphere_center_charge_sigma_b(eps, q, a)
    assert _close(tot, (eps - 1) / eps * q, 1e-12)
    # field solution: E = q/(eps r^2) inside; sigma_b = P.rhat at r=a-
    P_at_a = (eps - 1) / (4 * np.pi) * q / (eps * a * a)
    assert _close(sig, P_at_a, 1e-12)
    # volume bound charge at the point charge: rho_b = (1-eps)/eps q delta
    assert _close(bound_from_free(eps, q), (1 - eps) / eps * q, 1e-15)
    # Gauss check: net charge seen outside = q
    assert _close(q + bound_from_free(eps, q) + tot, q, 1e-12)


def test_p13_cylinder_in_uniform_field():
    """Ex. 5.4.3: BVP solution satisfies continuity of Phi and of D_rho at
    rho=a, solves Laplace, and has the right far field and eps->1 limit."""
    a, eps, E0 = 1.0, 4.0, 2.0
    h = 1e-6
    for ph in (0.3, 1.2, 2.8, 4.1):
        # continuity
        assert _close(cylinder_in_field_phi(a - h, ph, a, eps, E0),
                      cylinder_in_field_phi(a + h, ph, a, eps, E0), 1e-4, 1e-9)
        # D_rho: eps dPhi/drho|in = dPhi/drho|out
        din = (cylinder_in_field_phi(a - h, ph, a, eps, E0)
               - cylinder_in_field_phi(a - 3 * h, ph, a, eps, E0)) / (2 * h)
        dout = (cylinder_in_field_phi(a + 3 * h, ph, a, eps, E0)
                - cylinder_in_field_phi(a + h, ph, a, eps, E0)) / (2 * h)
        assert _close(eps * din, dout, 1e-3, 1e-8)
    # Laplace in polar coords at interior and exterior sample points
    for rho, ph in ((0.5, 0.7), (1.8, 2.1)):
        hh = 1e-3
        f = lambda r_, p_: cylinder_in_field_phi(r_, p_, a, eps, E0)
        lap = ((f(rho + hh, ph) - 2 * f(rho, ph) + f(rho - hh, ph)) / hh ** 2
               + (f(rho + hh, ph) - f(rho - hh, ph)) / (2 * hh * rho)
               + (f(rho, ph + hh) - 2 * f(rho, ph) + f(rho, ph - hh)) / (hh * rho) ** 2)
        assert abs(lap) < 1e-5
    # interior field is uniform 2E0/(eps+1) yhat
    Ein = 2 * E0 / (eps + 1)
    assert _close(cylinder_in_field_phi(0.5, np.pi / 2, a, eps, E0), -Ein * 0.5, 1e-12)
    # eps=1: no disturbance
    assert _close(cylinder_in_field_phi(1.7, 0.9, a, 1.0, E0),
                  -E0 * 1.7 * np.sin(0.9), 1e-12)


def test_p14_bubble_in_polarized_slab():
    """Ex. 5.4.4(b): the bubble-surface bound charge -P0 cos(th) produces a
    uniform field (4pi/3) P0 zhat everywhere inside."""
    P0, a = 1.3, 1.0
    target = np.array([0, 0, 4 * np.pi / 3 * P0])
    for x in (np.zeros(3), np.array([0.3, -0.2, 0.4]), np.array([-0.5, 0.1, -0.6])):
        E = polarized_sphere_surface_E(x, P0, a, nth=80, nph=80)
        assert _vclose(E, target, 2e-4)


def test_p15_cubical_hole():
    """Ex. 5.4.5: solid angle of a cube face = 2pi/3, so E_P(0) = (4pi/3) P0;
    Clausius-Mossotti round-trips."""
    om = solid_angle_square_from_center(2.0)
    assert _close(om, 2 * np.pi / 3, 1e-6)
    P0 = 0.7
    assert _close(2 * P0 * om, 4 * np.pi / 3 * P0, 1e-6)
    for chi in (0.02, 0.4, 3.0):
        N = 0.11
        al = clausius_mossotti_alpha(chi, N)
        assert _close(chi_from_alpha(al, N), chi, 1e-12)
        # E_T consistency: P = chi E and P = N al (E + 4pi P/3)
        E = 1.7; P = chi * E
        assert _close(P, N * al * (E + 4 * np.pi * P / 3), 1e-12)


# --- Sec. 5.6 (P16-P21) ------------------------------------------------------

def test_p16_dielectric_corner():
    """Ex. 5.6.1: the 4-image construction (b, b, b^2) is exact for the
    factorizable medium (1, eps, eps^2, eps): continuity exact on the seams
    and D-matching to FD accuracy.  For the uniform-eps union, continuity
    still holds but the internal-seam D-condition fails at O(b) -- the
    construction is a first-order-in-b approximation there."""
    xp = np.array([0.8, 1.1, 0.0])
    cont, dnc = corner_interface_residuals(1.8, xp, factorized=True)
    assert cont < 1e-12 and dnc < 1e-7
    # uniform medium: continuity exact, D-residual nonzero, scaling like b^1
    res = []
    for eps in (1.1, 1.2):
        b = (1 - eps) / (1 + eps)
        cont_u, dnc_u = corner_interface_residuals(eps, xp, factorized=False)
        assert cont_u < 1e-12
        res.append((b, dnc_u))
    ratio = res[1][1] / res[0][1]
    expected = res[1][0] / res[0][0]              # O(b) scaling
    assert abs(ratio / expected - 1) < 0.15
    # vacuum-quadrant value from the region function matches the simple form
    x = np.array([1.5, 0.6, 0.4])
    assert _close(corner_dielectric_G(x, xp, 1.8),
                  corner_dielectric_G_region(x, xp, 1.8), 1e-12)


def test_p17_slab_over_conductor():
    """Ex. 5.6.2: the book's closed g equals a direct 4-coefficient solve;
    g(0)=0; correct jump; eps->1 gives the conductor-only half-space form."""
    d, eps = 1.0, 3.0
    for k in (0.3, 1.0, 2.7):
        for zp in (0.2, 0.5, 0.9):
            for z in (0.1, 0.4, 0.8, 1.5, 2.5):
                gb = g_slab_conductor_book(z, zp, k, d, eps)
                gs = g_slab_conductor_solve(z, zp, k, d, eps)
                assert _close(gb, gs, 1e-10, 1e-13)
            assert abs(g_slab_conductor_book(0.0, zp, k, d, eps)) < 1e-14
            # jump -[g']_-^+ = 1
            h = 1e-6
            gp_p = (g_slab_conductor_book(zp + 2 * h, zp, k, d, eps)
                    - g_slab_conductor_book(zp + h, zp, k, d, eps)) / h
            gp_m = (g_slab_conductor_book(zp - h, zp, k, d, eps)
                    - g_slab_conductor_book(zp - 2 * h, zp, k, d, eps)) / h
            assert _close(gp_m - gp_p, 1.0, 1e-3)
            # D_n at z=d: g'(d-) = eps g'(d+)
            gd_m = (g_slab_conductor_book(d - h, zp, k, d, eps)
                    - g_slab_conductor_book(d - 3 * h, zp, k, d, eps)) / (2 * h)
            gd_p = (g_slab_conductor_book(d + 3 * h, zp, k, d, eps)
                    - g_slab_conductor_book(d + h, zp, k, d, eps)) / (2 * h)
            assert _close(gd_m, eps * gd_p, 1e-3)
    # eps -> 1: conductor-only half space g = sinh(k z<) e^{-k z>}/k
    for z, zp, k in ((0.3, 0.7, 1.2), (1.6, 0.4, 0.8)):
        g1 = g_slab_conductor_book(z, zp, k, 1.0, 1.0 + 1e-12)
        zl, zg = min(z, zp), max(z, zp)
        assert _close(g1, np.sinh(k * zl) * np.exp(-k * zg) / k, 1e-9)
    # eps -> infinity: g(d) -> 0 (second conductor)
    assert abs(g_slab_conductor_book(1.0, 0.5, 1.0, 1.0, 1e8)) < 1e-7


def test_p18_swap_substitution():
    """Ex. 5.6.3: G_swapped(eps) = (1/eps) G_original(eps -> 1/eps): dielectric
    and vacuum interchanged (Fig. 5.29, charge still between plate and z=d)."""
    d, eps = 0.8, 2.6
    for k in (0.5, 1.4):
        for zp in (0.2, 0.6):                     # inside the (now-)dielectric
            for z in (0.1, 0.45, 0.7, 1.5, 2.4):
                gs = g_slab_swapped_solve(z, zp, k, d, eps)
                gsub = g_slab_conductor_solve(z, zp, k, d, 1.0 / eps) / eps
                assert _close(gs, gsub, 1e-10, 1e-13)
    # eps=1 sanity: both reduce to the conductor-only half-space form
    z, zp, k = 0.5, 0.3, 1.1
    zl, zg = min(z, zp), max(z, zp)
    assert _close(g_slab_swapped_solve(z, zp, k, d, 1.0),
                  np.sinh(k * zl) * np.exp(-k * zg) / k, 1e-10)


def test_p19_oneD_green():
    """Ex. 5.6.4: closed form vs finite-difference interface solve; reduces to
    x<(1-x>/L) when eps=1 or d->0."""
    L = 1.0
    for (d, eps, xp) in ((0.3, 4.0, 0.7), (0.5, 2.0, 0.6), (0.25, 7.5, 0.9)):
        xg, Gfd = oneD_G_fd(xp, d, L, eps, N=4000)
        for x in (0.1, 0.29, 0.45, 0.65, 0.85):
            Gc = oneD_G_dielectric(x, xp, d, L, eps)
            Gi = np.interp(x, xg, Gfd)
            assert _close(Gc, Gi, 2e-3, 1e-6)
    for x, xp in ((0.3, 0.6), (0.8, 0.5)):
        assert _close(oneD_G_dielectric(x, xp, 0.4, L, 1.0),
                      min(x, xp) * (1 - max(x, xp) / L), 1e-12)
        assert _close(oneD_G_dielectric(x, xp, 1e-12, L, 5.0),
                      min(x, xp) * (1 - max(x, xp) / L), 1e-9)


def test_p20_two_halfspace_images():
    """Ex. 5.6.5: the image solution satisfies continuity of Phi and D_z on
    z=0, is harmonic off the charge, and has the right limits."""
    q, zp, e1, e2 = 1.7, 0.9, 3.0, 1.5
    h = 1e-6
    for rho in (0.2, 1.1, 2.7):
        xa = np.array([rho, 0.3, +h]); xb = np.array([rho, 0.3, -h])
        assert _close(two_halfspace_phi(xa, q, zp, e1, e2),
                      two_halfspace_phi(xb, q, zp, e1, e2), 1e-4)
        dza = (two_halfspace_phi([rho, 0.3, 3 * h], q, zp, e1, e2)
               - two_halfspace_phi([rho, 0.3, h], q, zp, e1, e2)) / (2 * h)
        dzb = (two_halfspace_phi([rho, 0.3, -h], q, zp, e1, e2)
               - two_halfspace_phi([rho, 0.3, -3 * h], q, zp, e1, e2)) / (2 * h)
        assert _close(e2 * dza, e1 * dzb, 1e-3)
    # harmonic (FD Laplacian) at a couple of off-axis points
    for x0 in (np.array([0.5, 0.2, 0.4]), np.array([0.4, -0.1, -0.6])):
        hh = 1e-3
        lap = 0.0
        for i in range(3):
            e = np.zeros(3); e[i] = hh
            lap += (two_halfspace_phi(x0 + e, q, zp, e1, e2)
                    - 2 * two_halfspace_phi(x0, q, zp, e1, e2)
                    + two_halfspace_phi(x0 - e, q, zp, e1, e2)) / hh ** 2
        assert abs(lap) < 1e-4
    # eps1 = eps2 = 1: free space
    assert _close(two_halfspace_phi([0.3, 0, 0.2], q, zp, 1, 1),
                  q / np.linalg.norm(np.array([0.3, 0, 0.2 - zp])), 1e-12)


def test_p21_finite_slab():
    """Ex. 5.6.6: 6-coefficient solve is uniquely solvable and satisfies all
    interface/jump conditions; limits: eps->1 free space; large kd half-space."""
    k, zp, d, eps = 1.1, 0.8, 1.5, 3.2
    sol = slab_finite_solve(k, zp, d, eps)
    g = sol['g']
    h = 1e-6
    assert _close(g(0 + h), g(0 - h), 1e-4)              # continuity at 0
    assert _close(g(-d + h), g(-d - h), 1e-4)            # continuity at -d
    dz0p = (g(3 * h) - g(h)) / (2 * h)
    dz0m = (g(-h) - g(-3 * h)) / (2 * h)
    assert _close(dz0p, eps * dz0m, 1e-3)                # D_n at 0
    dzdp = (g(-d + 3 * h) - g(-d + h)) / (2 * h)
    dzdm = (g(-d - h) - g(-d - 3 * h)) / (2 * h)
    assert _close(eps * dzdp, dzdm, 1e-3)                # D_n at -d
    gp = (g(zp + 2 * h) - g(zp + h)) / h
    gm = (g(zp - h) - g(zp - 2 * h)) / h
    assert _close(gm - gp, 1.0, 1e-3)                    # unit jump
    # eps=1: free space
    sol1 = slab_finite_solve(k, zp, d, 1.0)
    for z in (-2.0, -0.5, 0.4, 1.5):
        assert _close(sol1['g'](z), np.exp(-k * abs(z - zp)) / (2 * k), 1e-10)
    # k d >> 1: z>0 region behaves like the half-space (5.104)
    sol2 = slab_finite_solve(4.0, zp, 8.0, eps)
    for z in (0.2, 0.9, 1.7):
        assert _close(sol2['g'](z), g_halfspace_dielectric(z, zp, 4.0, eps), 1e-6)


# --- Sec. 5.7 (P22-P33) ------------------------------------------------------

def test_p22_cylinder_2d_green():
    """Ex. 5.7.1: the quoted g_m satisfy the radial equation, both interface
    conditions at rho=a, the source jump, and sum to -2 ln|x-x'| when eps=1."""
    a, eps, rhop = 1.0, 2.5, 1.7
    h = 1e-6
    for m in (1, 2, 5):
        # interface conditions
        assert _close(gm_cyl2d(m, a - h, rhop, a, eps),
                      gm_cyl2d(m, a + h, rhop, a, eps), 1e-4)
        di = (gm_cyl2d(m, a - h, rhop, a, eps)
              - gm_cyl2d(m, a - 3 * h, rhop, a, eps)) / (2 * h)
        do = (gm_cyl2d(m, a + 3 * h, rhop, a, eps)
              - gm_cyl2d(m, a + h, rhop, a, eps)) / (2 * h)
        assert _close(eps * di, do, 1e-3)
        # jump rho' [g'(-) - g'(+)] = 1
        gp = (gm_cyl2d(m, rhop + 2 * h, rhop, a, eps)
              - gm_cyl2d(m, rhop + h, rhop, a, eps)) / h
        gm_ = (gm_cyl2d(m, rhop - h, rhop, a, eps)
               - gm_cyl2d(m, rhop - 2 * h, rhop, a, eps)) / h
        assert _close(rhop * (gm_ - gp), 1.0, 1e-3)
        # radial ODE away from boundaries: (1/rho)(rho g')' - m^2 g/rho^2 = 0
        for rho in (0.6, 1.3, 2.3):
            hh = 1e-4
            f = lambda r_: gm_cyl2d(m, r_, rhop, a, eps)
            ode = ((f(rho + hh) - 2 * f(rho) + f(rho - hh)) / hh ** 2
                   + (f(rho + hh) - f(rho - hh)) / (2 * hh * rho)
                   - m * m * f(rho) / rho ** 2)
            assert abs(ode) < 1e-4 * max(1.0, abs(f(rho)) / rho ** 2)
    # eps = 1 sum: free 2-D Green function -2 ln|x-x'|
    for (rho, ph) in ((0.7, 0.4), (1.3, 2.0), (2.2, 5.1)):
        Gf = G_cyl2d(rho, ph, rhop, 0.0, a, 1.0, M=600)
        x = np.array([rho * np.cos(ph), rho * np.sin(ph)])
        xp = np.array([rhop, 0.0])
        assert _close(Gf, -2 * np.log(np.linalg.norm(x - xp)), 1e-6, 1e-8)
    # continuity of the eps!=1 sum across rho=a
    for ph in (0.5, 2.2):
        assert _close(G_cyl2d(a - 1e-6, ph, rhop, 0.0, a, eps, M=400),
                      G_cyl2d(a + 1e-6, ph, rhop, 0.0, a, eps, M=400), 1e-5)


def test_p23_cylinder_3d_reduced():
    """Ex. 5.7.2: the I_m/K_m linear system is nonsingular and its solution
    satisfies the interface and jump conditions; at eps=1 the assembled G
    reproduces 1/|x-x'|."""
    a, eps = 1.0, 2.2
    for (m, k, rhop) in ((0, 0.7, 1.6), (1, 1.3, 1.9), (3, 2.1, 1.4)):
        g_, coef = cyl3d_gm_solve(m, k, 1.2, rhop, a, eps)
        h = 1e-6
        ga_m = cyl3d_gm_solve(m, k, a - h, rhop, a, eps)[0]
        ga_p = cyl3d_gm_solve(m, k, a + h, rhop, a, eps)[0]
        assert _close(ga_m, ga_p, 1e-4)
        di = (cyl3d_gm_solve(m, k, a - h, rhop, a, eps)[0]
              - cyl3d_gm_solve(m, k, a - 3 * h, rhop, a, eps)[0]) / (2 * h)
        do = (cyl3d_gm_solve(m, k, a + 3 * h, rhop, a, eps)[0]
              - cyl3d_gm_solve(m, k, a + h, rhop, a, eps)[0]) / (2 * h)
        assert _close(eps * di, do, 1e-3)
        gp = (cyl3d_gm_solve(m, k, rhop + 2 * h, rhop, a, eps)[0]
              - cyl3d_gm_solve(m, k, rhop + h, rhop, a, eps)[0]) / h
        gmm = (cyl3d_gm_solve(m, k, rhop - h, rhop, a, eps)[0]
               - cyl3d_gm_solve(m, k, rhop - 2 * h, rhop, a, eps)[0]) / h
        assert _close(gmm - gp, 1.0 / rhop, 2e-3)
    # eps=1 assembled G = 1/|x-x'|
    x = np.array([1.8, 0.4, 0.9]); xp = np.array([1.5, -0.3, 0.0])
    G1 = G_cyl3d(x, xp, a, 1.0, M=10, nk=400, kmax=25.0)
    assert _close(G1, 1.0 / np.linalg.norm(x - xp), 2e-3)
    # eps!=1: continuity of assembled G across rho=a
    xa = np.array([a - 1e-5, 0.6, 0.5]); xb = np.array([a + 1e-5, 0.6, 0.5])
    xa = np.array([(a - 1e-4) * np.cos(0.3), (a - 1e-4) * np.sin(0.3), 0.7])
    xb = np.array([(a + 1e-4) * np.cos(0.3), (a + 1e-4) * np.sin(0.3), 0.7])
    Ga = G_cyl3d(xa, xp, a, eps, M=10, nk=400, kmax=25.0)
    Gb = G_cyl3d(xb, xp, a, eps, M=10, nk=400, kmax=25.0)
    assert _close(Ga, Gb, 5e-3)


def test_p24_sphere_uniform_field():
    """Ex. 5.7.3: Phi_in/out satisfy the interface conditions and Laplace, and
    emerge from the distant-charge limit of the Green function."""
    a, eps, E0 = 1.0, 5.0, 1.4
    h = 1e-6
    for th in (0.4, 1.2, 2.6):
        n = np.array([np.sin(th), 0, np.cos(th)])
        assert _close(sphere_uniform_field_phi((a - h) * n, a, eps, E0),
                      sphere_uniform_field_phi((a + h) * n, a, eps, E0), 1e-4, 1e-10)
        din = (sphere_uniform_field_phi((a - h) * n, a, eps, E0)
               - sphere_uniform_field_phi((a - 3 * h) * n, a, eps, E0)) / (2 * h)
        dout = (sphere_uniform_field_phi((a + 3 * h) * n, a, eps, E0)
                - sphere_uniform_field_phi((a + h) * n, a, eps, E0)) / (2 * h)
        assert _close(eps * din, dout, 1e-3)
    # distant-charge construction: source q = E0 R^2 at z = -R
    R = 300.0 * a
    q = E0 * R * R
    for x in (np.array([0.4, 0, 0.3]), np.array([1.5, 0, 1.0]), np.array([0, 0.9, -1.2])):
        r = np.linalg.norm(x)
        cosg = -x[2] / r      # angle from the source direction (-z)
        if r < a:
            Phi = q * sphere_G_in(r, R, cosg, a, eps, L=6)
        else:
            Phi = q * sphere_G_out(r, R, cosg, a, eps, L=6)
        Phi0 = q * sphere_G_in(0.0, R, 1.0, a, eps, L=6) if r < a else q / R
        # subtract the constant q/R and compare
        assert _close(Phi - q / R, sphere_uniform_field_phi(x, a, eps, E0),
                      2e-2, 1e-9)
    # induced dipole p = (eps-1)/(eps+2) a^3 E0 (Eq. 5.143-5.144)
    p = (eps - 1) / (eps + 2) * a ** 3 * E0
    x = np.array([0, 0, 3.0])
    assert _close(sphere_uniform_field_phi(x, a, eps, E0), -E0 * 3.0 + p / 9.0, 1e-12)


def test_p25_source_inside_sphere():
    """Ex. 5.7.4: closed coefficients == direct solve; far field has monopole 1
    and dipole 3 rp/(eps+2); total surface polarization charge (eps-1)/eps."""
    a, eps, rp = 1.0, 3.0, 0.55
    for l in range(0, 8):
        Ac, Bc, Cc, Dc = sphere_source_inside_coeffs(l, rp, a, eps)
        As, Bs, Cs, Ds = sphere_source_inside_solve(l, rp, a, eps)
        for u, v in ((Ac, As), (Bc, Bs), (Cc, Cs), (Dc, Ds)):
            assert _close(u, v, 1e-10, 1e-14)
    # eps=1: free space kernel r<^l/r>^{l+1}/(2l+1)
    A1, B1, C1, D1 = sphere_source_inside_coeffs(2, rp, a, 1.0)
    assert _close(D1, rp ** 2 / 5.0, 1e-12) and abs(B1) < 1e-15
    # far field: G -> 1/r + [3 rp/(eps+2)] cos g / r^2
    r = 60.0
    G0 = sphere_G_source_inside(r, rp, 1.0, a, eps)
    G1 = sphere_G_source_inside(r, rp, -1.0, a, eps)
    mono = 0.5 * (G0 + G1) * r
    dip = 0.5 * (G0 - G1) * r * r
    assert _close(mono, 1.0, 1e-3)
    assert _close(dip, 3 * rp / (eps + 2), 1e-3)
    # total bound charge on the surface: oint sigma_b da = (eps-1)/eps
    cn, cw = gauss_legendre(-1.0, 1.0, 300)
    tot = 0.0
    dr = 1e-6
    for c, w in zip(cn, cw):
        Eout = -(sphere_G_source_inside(a + 2 * dr, rp, c, a, eps)
                 - sphere_G_source_inside(a, rp, c, a, eps)) / (2 * dr)
        Ein = -(sphere_G_source_inside(a, rp, c, a, eps)
                - sphere_G_source_inside(a - 2 * dr, rp, c, a, eps)) / (2 * dr)
        tot += w * 2 * np.pi * a * a * (Eout - Ein) / (4 * np.pi)
    assert _close(tot, (eps - 1) / eps, 1e-3)


def test_p26_bubble_green():
    """Ex. 5.7.5: bubble Green function = (1/eps) x [sphere solution with
    eps -> 1/eps]; verified against a direct radial solve and its BCs."""
    a, eps, rp = 1.0, 2.8, 1.9
    for l in (1, 2, 4):
        for r in (0.4, 1.5, 2.5):
            # compare mode functions directly (closed vs radial solve):
            g_direct = bubble_gl_solve(l, r, rp, a, eps)
            # closed mode: (1/eps)[direct Coulomb + induced] for r,rp>a;
            # inside: transmitted
            if r >= a:
                rl, rg = min(r, rp), max(r, rp)
                g_closed = (rl ** l / rg ** (l + 1) / (2 * l + 1)
                            + (eps - 1) * l / (l * (1 + eps) + eps)
                            * a ** (2 * l + 1) / (r * rp) ** (l + 1) / (2 * l + 1)) / eps
            else:
                g_closed = ((2 * l + 1) / (l * (1 / eps + 1) + 1)
                            * r ** l / rp ** (l + 1)) / (eps * (2 * l + 1))
            assert _close(g_direct, g_closed, 1e-9, 1e-13)
    # full sums agree (mode sum vs closed 1/R + induced series)
    from scipy.special import eval_legendre as _Pl
    for cosg in (-0.6, 0.2, 0.9):
        modes = sum((2 * l + 1) * bubble_gl_solve(l, 1.4, 2.6, a, eps)
                    * _Pl(l, cosg) for l in range(160))
        assert _close(bubble_G_out(1.4, 2.6, cosg, a, eps, L=160), modes, 1e-8)


def test_p27_dipole_near_sphere():
    """Ex. 5.7.6: (a) far potential is that of p_eff = p0 + induced dipole;
    (b) interior field is 3/(eps+2) x the dipole's field at the center."""
    a, eps = 1.0, 4.0
    p0 = np.array([0.3, -0.5, 0.8]); xp = np.array([0.0, 0.0, 3.0])
    delta = 1e-4
    qd = np.linalg.norm(p0) / delta; ph = p0 / np.linalg.norm(p0)
    qs = [qd, -qd]
    Xs = [xp + 0.5 * delta * ph, xp - 0.5 * delta * ph]
    # (a) far potential: odd part along each axis isolates the dipole
    p_eff = sphere_dipole_p_eff(p0, xp, a, eps)
    r = 250.0
    for i, n in enumerate(np.eye(3)):
        Phi_p = sum(q * sphere_G_out(r, np.linalg.norm(X), (n @ X) / np.linalg.norm(X),
                                     a, eps, L=6) for q, X in zip(qs, Xs))
        Phi_m = sum(q * sphere_G_out(r, np.linalg.norm(X), (-n @ X) / np.linalg.norm(X),
                                     a, eps, L=6) for q, X in zip(qs, Xs))
        p_i = 0.5 * (Phi_p - Phi_m) * r * r
        assert _close(p_i, p_eff[i], 3e-2, 1e-6)
    # (b) interior field for rp >> a: uniform up to O(r/rp) nonuniformity
    errs = []
    for rp_far in (20.0, 40.0):
        xp_far = np.array([0.0, 0.0, rp_far])
        Xs_far = [xp_far + 0.5 * delta * ph, xp_far - 0.5 * delta * ph]
        def Phi_in(x):
            r_ = np.linalg.norm(x)
            return sum(q * sphere_G_in(r_, np.linalg.norm(X),
                                       (x @ X) / (r_ * np.linalg.norm(X)), a, eps, L=8)
                       for q, X in zip(qs, Xs_far))
        E_num = -grad_fd(Phi_in, np.array([0.1, -0.2, 0.15]), h=1e-4)
        E_th = sphere_dipole_E_in(p0, xp_far, a, eps)
        errs.append(np.linalg.norm(E_num - E_th) / np.linalg.norm(E_th))
        assert _vclose(E_num, E_th, 0.08)
    assert errs[1] < 0.7 * errs[0]     # -> exact as rp grows


def test_p28_sphere_in_conducting_shell():
    """Ex. 5.7.7: the 5-coefficient solve satisfies g(b)=0, both interface
    conditions at a, the jump at rp; eps=1 recovers the grounded-shell kernel."""
    a, b, eps, rp = 0.6, 2.0, 3.5, 1.2
    h = 1e-6
    for l in (0, 1, 3):
        assert abs(sphere_in_conductor_solve(l, b - 1e-12, rp, a, b, eps)) < 1e-10
        ga_m = sphere_in_conductor_solve(l, a - h, rp, a, b, eps)
        ga_p = sphere_in_conductor_solve(l, a + h, rp, a, b, eps)
        assert _close(ga_m, ga_p, 1e-4, 1e-12)
        di = (sphere_in_conductor_solve(l, a - h, rp, a, b, eps)
              - sphere_in_conductor_solve(l, a - 3 * h, rp, a, b, eps)) / (2 * h)
        do = (sphere_in_conductor_solve(l, a + 3 * h, rp, a, b, eps)
              - sphere_in_conductor_solve(l, a + h, rp, a, b, eps)) / (2 * h)
        assert _close(eps * di, do, 1e-3, 1e-10)
        gp = (sphere_in_conductor_solve(l, rp + 2 * h, rp, a, b, eps)
              - sphere_in_conductor_solve(l, rp + h, rp, a, b, eps)) / h
        gm_ = (sphere_in_conductor_solve(l, rp - h, rp, a, b, eps)
               - sphere_in_conductor_solve(l, rp - 2 * h, rp, a, b, eps)) / h
        assert _close(gm_ - gp, 1.0 / rp ** 2, 1e-3)
        for r in (0.3, 0.9, 1.6):
            assert _close(sphere_in_conductor_solve(l, r, rp, a, b, 1.0),
                          grounded_sphere_interior_gl(l, r, rp, b), 1e-10, 1e-14)


def test_p29_sphere_and_charged_plane():
    """Ex. 5.7.8: the plane integrals kill every l except l=1 (I_1 = 2 pi),
    so the interior field is exactly the screened uniform field of Ex. 5.7.3."""
    d = 2.0
    # l=1 integral = 2 pi exactly; l>=2 integrals vanish by parity+orthogonality
    assert _close(plane_moment_integral(1, d), 2 * np.pi, 1e-12)
    for l in (2, 3, 4, 5):
        assert abs(plane_moment_integral(l, d)) < 1e-10
    # interior potential: Phi = 2 pi sigma (3/(eps+2)) z
    eps, sigma, a = 3.0, 0.4, 1.0
    x = np.array([0.2, 0.1, 0.5])
    Phi = plane_sigma_phi_in(x, a, eps, sigma, d)
    l1 = 3.0 / (eps + 2) * sigma * plane_moment_integral(1, d) * x[2]
    assert _close(Phi, l1, 1e-12)
    # E_in = (3/(eps+2)) E_plane
    E_plane = 2 * np.pi * sigma
    E_in = -(plane_sigma_phi_in([0, 0, 0.3], a, eps, sigma, d)
             - plane_sigma_phi_in([0, 0, 0.1], a, eps, sigma, d)) / 0.2
    assert _close(E_in, -3.0 / (eps + 2) * E_plane, 1e-12)


def test_p30_ring_around_sphere():
    """Ex. 5.7.9: the quoted P_2n series equals the ring built from point
    charges and the one-charge kernel."""
    a, b, eps, Q = 1.0, 1.8, 2.5, 1.3
    for (r, th) in ((0.4, 0.7), (0.8, 1.9), (0.6, np.pi / 2)):
        s = ring_sphere_phi_in(r, th, a, b, eps, Q, L=50)
        pts = ring_sphere_phi_in_points(r, th, a, b, eps, Q, Npts=400, L=100)
        assert _close(s, pts, 1e-6)


def test_p31_split_sphere_dielectric():
    """Ex. 5.7.10: C11(eps), C12(eps) sums match direct quadrature of the free
    charge; eps=1 reduces to the (2l+1)^2 forms of Ex. 4.13.4; the eps-shift
    is the book's a(eps-1)/4 sum l(2l+1) I_l^2 with (-1)^l for C12."""
    a, L = 1.0, 40
    for eps in (1.0, 2.0, 4.5):
        C11, C12 = split_sphere_C(eps, a, L)
        Q1_10 = split_sphere_Q1_quad(eps, 1.0, 0.0, a, L)
        Q1_01 = split_sphere_Q1_quad(eps, 0.0, 1.0, a, L)
        assert _close(C11, Q1_10, 1e-8)
        assert _close(C12, Q1_01, 1e-8)
    # eps=1 vs explicit (2l+1)^2 I_l^2 sums
    l = np.arange(1, L + 1)
    Il = np.atleast_1d(Il_int_P(l))
    C11_413 = a / 4 * (1 + np.sum((2 * l + 1) ** 2 * Il ** 2))
    C12_413 = a / 4 * (1 + np.sum((-1.0) ** l * (2 * l + 1) ** 2 * Il ** 2))
    C11_1, C12_1 = split_sphere_C(1.0, a, L)
    assert _close(C11_1, C11_413, 1e-12)
    assert _close(C12_1, C12_413, 1e-12)
    # book's shift formula
    eps = 3.0
    C11_e, C12_e = split_sphere_C(eps, a, L)
    shift11 = a * (eps - 1) / 4 * np.sum(l * (2 * l + 1) * Il ** 2)
    shift12 = a * (eps - 1) / 4 * np.sum((-1.0) ** l * l * (2 * l + 1) * Il ** 2)
    assert _close(C11_e, C11_1 + shift11, 1e-12)
    assert _close(C12_e, C12_1 + shift12, 1e-12)


def test_p32_coaxial_dielectric():
    """Ex. 5.7.11: the 5-coefficient modes satisfy the wall, interface, and
    jump conditions; at eps=1 the sum reproduces the grounded-cylinder image
    Green function."""
    b, a, eps, rhop = 0.5, 2.0, 3.0, 1.2
    h = 1e-6
    for m in (0, 1, 4):
        assert abs(coaxial_cyl_solve(m, a - 1e-12, rhop, b, a, eps)) < 1e-10
        gm_m = coaxial_cyl_solve(m, b - h, rhop, b, a, eps)
        gm_p = coaxial_cyl_solve(m, b + h, rhop, b, a, eps)
        assert _close(gm_m, gm_p, 1e-4, 1e-12)
        di = (coaxial_cyl_solve(m, b - h, rhop, b, a, eps)
              - coaxial_cyl_solve(m, b - 3 * h, rhop, b, a, eps)) / (2 * h)
        do = (coaxial_cyl_solve(m, b + 3 * h, rhop, b, a, eps)
              - coaxial_cyl_solve(m, b + h, rhop, b, a, eps)) / (2 * h)
        assert abs(eps * di - do) < 2e-3 * max(1.0, abs(do))
        gp = (coaxial_cyl_solve(m, rhop + 2 * h, rhop, b, a, eps)
              - coaxial_cyl_solve(m, rhop + h, rhop, b, a, eps)) / h
        gmm = (coaxial_cyl_solve(m, rhop - h, rhop, b, a, eps)
               - coaxial_cyl_solve(m, rhop - 2 * h, rhop, b, a, eps)) / h
        jump_target = 1.0 / rhop if m > 0 else 0.5 / rhop
        assert _close(gmm - gp, jump_target, 1e-3)
    for (rho, ph) in ((0.9, 0.5), (1.6, 2.7)):
        Gsum = G_coaxial(rho, ph, rhop, 0.0, b, a, 1.0, M=300)
        Gimg = G_grounded_cylinder_2d(rho, ph, rhop, 0.0, a)
        assert _close(Gsum, Gimg, 1e-6, 1e-9)


def test_p33_induced_quadrupole():
    """Ex. 5.7.12: Q_ij = 2 a^5 (eps-1)/(3+2eps) (-dE'_j/dx'_i) -- the a^5
    (not the printed a^3) is confirmed by integrating the bound surface
    charge's quadrupole moment; scaling in a is a^5."""
    eps = 2.5
    for a, rp in ((1.0, 2.0), (0.5, 2.0)):
        Qf = induced_quadrupole_sphere(eps, a, [0, 0, rp])
        Q33_sigma = induced_quadrupole_from_sigma(rp, a, eps, L=60, n=200)
        assert _close(Qf[2, 2], Q33_sigma, 2e-3)
        # explicit value: Q33 = -4(eps-1) a^5/[(3+2eps) rp^3]
        assert _close(Qf[2, 2], -4 * (eps - 1) * a ** 5 / ((3 + 2 * eps) * rp ** 3),
                      1e-12)
    # traceless, symmetric, and axisymmetric structure
    Qf = induced_quadrupole_sphere(eps, 1.0, [0, 0, 2.0])
    assert abs(np.trace(Qf)) < 1e-12
    assert _close(Qf[0, 0], -0.5 * Qf[2, 2], 1e-12)


# --- Sec. 5.8 (P34) ----------------------------------------------------------

def test_p34_permanent_polarization_energy():
    """Ex. 5.8.1: int E.D = 0 for the uniformly polarized sphere (permanent P,
    no free charge), and W_int = -(1/2) int P.E = (1/8pi) int E^2."""
    num, exact = polarized_sphere_ED_integral(P0=1.1, a=1.3)
    scale = (4 * np.pi / 3 * 1.1) ** 2 * (4 * np.pi * 1.3 ** 3 / 3)
    assert abs(exact) < 1e-10 * scale
    assert abs(num) < 2e-2 * scale          # radial quadrature truncation
    W1, W2 = polarized_sphere_Wint(P0=1.1, a=1.3)
    assert _close(W1, W2, 1e-12)


# --- Sec. 5.9 (P35-P44) ------------------------------------------------------

def test_p35_surface_force_formulas():
    """Ex. 5.9.1: (E2n^2-E1n^2)/8pi == 2 pi sigma_b^2 (1+eps)/(eps-1) pointwise
    on the charge-above-half-space interface; the free+bound Extra formula
    reduces to it at sigma_f = 0 and factors correctly."""
    eps, zp = 2.7, 0.8
    for rho in (0.0, 0.5, 1.4, 3.0):
        E1n, E2n, sb = halfspace_fields_at_interface(rho, zp, eps)
        f1 = surface_force_from_fields(E1n, E2n)
        f2 = surface_force_from_sigma_b(sb, eps)
        f3 = surface_force_free_bound(sb, 0.0, eps)
        assert _close(f1, f2, 1e-10)
        assert _close(f1, f3, 1e-10)
    # Extra with sigma_f: check against (sigma_f+sigma_b)(sigma_f+sigma_b(eps+1)/(eps-1))
    sb, sf = 0.3, 0.7
    lhs = surface_force_free_bound(sb, sf, eps)
    rhs = 2 * np.pi * (sf + sb) * (sf + sb * (eps + 1) / (eps - 1))
    assert _close(lhs, rhs, 1e-12)


def test_p36_halfspace_force_three_ways():
    """Ex. 5.9.2: image force == -d(DeltaW)/dzp == integrated surface stress."""
    eps, zp = 3.2, 0.9
    F_img = halfspace_force_image(zp, eps)
    h = 1e-6
    F_en = -(halfspace_deltaW(zp + h, eps) - halfspace_deltaW(zp - h, eps)) / (2 * h)
    F_st = halfspace_force_stress(zp, eps)
    # F_en is the force on the *charge* (negative: pulled toward slab);
    # the force on the dielectric is +F_img toward the charge.
    assert _close(-F_en, F_img, 1e-6)
    assert _close(F_st, F_img, 1e-4)


def test_p37_p38_rod_forces():
    """Ex. 5.9.3/5.9.4: transverse and longitudinal thin-rod forces from the
    induced-dipole energies (virtual work); parallel/perp ratio (eps+1)/2;
    needle depolarization factor -> 0 justifies E_in = E0."""
    eps, a, Lr, z = 3.0, 0.05, 2.0, 15.0
    h = 1e-4
    Fp = -(rod_W_perp(eps, a, Lr, z + h) - rod_W_perp(eps, a, Lr, z - h)) / (2 * h)
    assert _close(-Fp, rod_force_perp(eps, a, Lr, z), 1e-6)   # attraction toward charge
    Fl = -(rod_W_par(eps, a, Lr, z + h) - rod_W_par(eps, a, Lr, z - h)) / (2 * h)
    assert _close(-Fl, rod_force_par(eps, a, Lr, z), 1e-6)
    assert _close(rod_force_par(eps, a, Lr, z) / rod_force_perp(eps, a, Lr, z),
                  (eps + 1) / 2, 1e-12)
    # needle limit
    assert prolate_depolarization_nz(3.0) > prolate_depolarization_nz(30.0)
    assert prolate_depolarization_nz(300.0) < 1e-4
    assert _close(spheroid_E_in_axial(eps, 1e4, 1.0), 1.0, 1e-5)
    # sphere check of the machinery: aspect->1 gives n_z=1/3
    e = 1e-4
    assert _close(prolate_depolarization_nz(1.0 + e), 1.0 / 3, 1e-3)


def test_p39_partial_capacitor():
    """Ex. 5.9.5: F = +(V^2/2) dC/dx (fixed V) and (Q^2/2C^2) dC/dx (fixed Q),
    both by virtual work; equal at the insertion point where V matches."""
    eps, Lc, Wc, D, V = 4.0, 3.0, 1.0, 0.1, 2.0
    h = 1e-6
    for x in (0.5, 1.5, 2.5):
        dCdx = (capacitor_C_partial(x + h, eps, Lc, Wc, D)
                - capacitor_C_partial(x - h, eps, Lc, Wc, D)) / (2 * h)
        FV = capacitor_force_fixed_V(x, eps, Lc, Wc, D, V)
        assert _close(FV, 0.5 * V * V * dCdx, 1e-8)
        assert FV > 0
        # fixed Q: W = Q^2/2C; F = -dW/dx
        Q = Lc * Wc * V / (4 * np.pi * D)
        WQ = lambda xx: Q * Q / (2 * capacitor_C_partial(xx, eps, Lc, Wc, D))
        FQ_fd = -(WQ(x + h) - WQ(x - h)) / (2 * h)
        FQ = capacitor_force_fixed_Q(x, eps, Lc, Wc, D, V)
        assert _close(FQ, FQ_fd, 1e-7)
        assert FQ > 0
    # at x=0 (dielectric just entering) both give the same instantaneous force
    assert _close(capacitor_force_fixed_Q(0.0, eps, Lc, Wc, D, V),
                  capacitor_force_fixed_V(0.0, eps, Lc, Wc, D, V), 1e-12)


def test_p40_slab_force_integral():
    """Ex. 5.9.6: the closed k-integral force on the dielectric equals
    -d(DeltaW)/dd by finite differences."""
    eps, zp, d = 2.5, 0.45, 1.0
    F_int = slab_force_integral(zp, d, eps)
    h = 1e-4
    F_fd = -(slab_deltaW(zp, d + h, eps) - slab_deltaW(zp, d - h, eps)) / (2 * h)
    assert _close(F_int, F_fd, 1e-4)
    assert F_int < 0        # pulled toward the charge (downward) for eps > 1


def test_p41_weak_dielectric():
    """Ex. 5.9.7: the exact integral converges to the three-image-term weak
    form as eps->1 (error O((eps-1)^2)); the weak form is the image assembly."""
    zp, d = 0.45, 1.0
    errs = []
    for eps in (1.05, 1.025):
        Fw = slab_force_weak(zp, d, eps)
        Fe = slab_force_integral(zp, d, eps)
        errs.append(abs(Fe - Fw) / abs(Fw))
        assert _close(Fe, Fw, 0.05)
    assert errs[1] < 0.6 * errs[0]
    # image assembly: force on dielectric = -(sum of forces on the vacuum
    # sources from the first-order dielectric images)
    eps = 1.04; b = (1 - eps) / (1 + eps)
    F_src = (-b / (4 * (d - zp) ** 2) + b / (4 * d ** 2)          # on +1 at zp
             + b / (4 * d ** 2) - b / (4 * (d + zp) ** 2))        # on -1 at -zp
    assert _close(-F_src, slab_force_weak(zp, d, eps), 1e-12)


def test_p42_conducting_limit():
    """Ex. 5.9.8: sigma(rho) and the plate force from the eps->infinity Green
    function match the image-ladder results, and the force is the eps->inf
    limit of Ex. 5.9.6."""
    zp, d = 0.45, 1.0
    for rho in (0.1, 0.5, 1.2):
        s_k = plate_sigma_kspace(rho, zp, d)
        s_i = plate_sigma_images(rho, zp, d)
        assert _close(s_k, s_i, 1e-5, 1e-10)
    F_k = plate_force_kspace(zp, d)
    F_i = plate_force_images(zp, d)
    assert _close(F_k, F_i, 1e-4)
    F_lim = slab_force_integral(zp, d, 1e9)
    assert _close(F_k, F_lim, 1e-6)
    assert F_k < 0
    # total induced charge on the plate = -(fraction) of unit charge: -zp/d
    rn, wn = gauss_legendre(0.0, 40.0, 1200)
    Qp = np.sum(wn * 2 * np.pi * rn * np.array([plate_sigma_images(r, zp, d, N=800)
                                                for r in rn]))
    assert _close(Qp, -zp / d, 2e-3)


def test_p43_layered_capacitor():
    """Ex. 5.9.9: series-capacitor forces at fixed V and after disconnecting
    at separation L; virtual-work cross-checks."""
    eps, d, dV, L = 5.0, 0.3, 2.0, 1.0
    # (a) fixed V: W/A = C' dV^2/2, C' = 1/(4 pi [d/eps + x - d]); F = -dW... battery:
    # F = +dW/dx|_V (Eq. 5.179) -- attraction means negative.
    h = 1e-7
    for x in (0.5, 0.8):
        Cp = lambda xx: 1.0 / (4 * np.pi * (d / eps + (xx - d)))
        F_th = layered_capacitor_force_V(x, d, eps, dV)
        F_fd = +0.5 * dV * dV * (Cp(x + h) - Cp(x - h)) / (2 * h)
        assert _close(F_th, F_fd, 1e-6)
        assert F_th < 0
    # (b) fixed Q from disconnect at x=L: F = -dW/dx|_Q with W = 2 pi sigma^2 [x-d+d/eps]
    sigma = dV / (4 * np.pi * (d / eps + (L - d)))
    for x in (0.5, 0.8):
        WQ = lambda xx: 2 * np.pi * sigma ** 2 * (d / eps + (xx - d))
        F_fd = -(WQ(x + h) - WQ(x - h)) / (2 * h)
        F_th = layered_capacitor_force_Q(x, d, eps, dV, L)
        assert _close(F_th, F_fd, 1e-9)
        assert _close(F_th, -2 * np.pi * sigma ** 2, 1e-12)


def test_p44_line_charge_cylinder():
    """Ex. 5.9.10: the coincidence series sums to -beta ln(1-a^2/rho0^2); the
    force is attractive and equals -d(DeltaW)/drho0."""
    a, eps = 1.0, 3.0
    for rho0 in (1.3, 1.9, 3.0):
        s, c = line_cylinder_deltaW(rho0, a, eps)
        assert _close(s, c, 1e-10)
        h = 1e-6
        F_fd = -(line_cylinder_deltaW(rho0 + h, a, eps)[1]
                 - line_cylinder_deltaW(rho0 - h, a, eps)[1]) / (2 * h)
        F = line_cylinder_force(rho0, a, eps)
        assert _close(F, F_fd, 1e-6)
        assert F < 0
    # DeltaW is (1/2)[G - G0] at coincidence built from the P22 modes
    rho0 = 1.6
    dW_modes = 0.5 * sum(4.0 * (gm_cyl2d(m, rho0, rho0, a, eps)
                                - gm_cyl2d(m, rho0, rho0, a, 1.0))
                         for m in range(1, 300))
    assert _close(dW_modes, line_cylinder_deltaW(rho0, a, eps)[1], 1e-6)


# --- Sec. 5.10 (P45) ---------------------------------------------------------

def test_p45_leading_log_variational():
    """Ex. 5.10.1: (1/2)E.D + alpha E^2 is the perfect differential of E.dD,
    and the second variation is positive in the confinement region E^2 > K^2."""
    for _ in range(6):
        E = RNG.normal(size=3) * 3.0
        while E @ E < 1.5:                      # keep E^2 > K^2 = 1
            E = RNG.normal(size=3) * 3.0
        dE = RNG.normal(size=3)
        lhs, rhs = leading_log_perfect_differential_check(E, dE)
        assert _close(lhs, rhs, 1e-6)
        assert leading_log_d2W_integrand(E, dE) > 0


# --- Sec. 5.11 (P46-P49) -----------------------------------------------------

def test_p46_bubble_repulsion():
    """Ex. 5.11.1: the bubble-charge force is repulsive for eps>1 and the
    series force matches the adapted-(5.202) far formula at large r0."""
    a, eps = 1.0, 2.0
    r0 = 12.0
    h = 1e-4
    F_fd = -(bubble_charge_deltaW_series(r0 + h, a, eps)
             - bubble_charge_deltaW_series(r0 - h, a, eps)) / (2 * h)
    F_far = bubble_charge_force_far(r0, a, eps)
    assert F_fd > 0 and F_far > 0
    assert _close(F_fd, F_far, 2.5e-2)      # l=2 correction ~ (a/r0)^2
    # sphere counterpart is attractive with the same machinery (sanity)
    F_s = sphere_charge_force_far(r0, a, eps)
    assert F_s < 0


def test_p47_energy_from_polarization():
    """Ex. 5.11.2: -(1/2) int P.E0 over the sphere reproduces (5.202)'s
    DeltaW = -((eps-1)/(eps+2)) a^3/(2 r0^4) and hence the same force; the
    exact series (5.201) converges to it at large r0."""
    a, eps = 1.0, 3.0
    for r0 in (6.0, 10.0):
        dW_P = sphere_deltaW_from_P(r0, a, eps)
        assert _close(dW_P, -(eps - 1) / (eps + 2) * a ** 3 / (2 * r0 ** 4), 1e-14)
        dW_series = sphere_charge_deltaW_series(r0, a, eps)
        assert _close(dW_series, dW_P, 2.5 * (a / r0) ** 2)
        h = 1e-4
        F = -(sphere_deltaW_from_P(r0 + h, a, eps)
              - sphere_deltaW_from_P(r0 - h, a, eps)) / (2 * h)
        assert _close(F, sphere_charge_force_far(r0, a, eps), 1e-6)


def test_p48_charge_in_droplet():
    """Ex. 5.11.3: F_r series == -d(DeltaW)/dr0 (finite difference), is
    negative (pushed toward the center), and the DeltaW coefficients come from
    the P25 interior solution."""
    a, eps = 1.0, 2.0
    for r0 in (0.2, 0.5, 0.8):
        h = 1e-5
        F_fd = -(droplet_deltaW(r0 + h, a, eps) - droplet_deltaW(r0 - h, a, eps)) / (2 * h)
        F = droplet_inside_force_series(r0, a, eps)
        assert _close(F, F_fd, 1e-5)
        assert F < 0
    # DeltaW from the solved interior coefficients: (1/2) sum (2l+1) B_l r0^{2l}
    r0 = 0.5
    dW_coeffs = 0.5 * sum((2 * l + 1) * sphere_source_inside_coeffs(l, r0, a, eps)[1]
                          * r0 ** l for l in range(0, 400))
    assert _close(dW_coeffs, droplet_deltaW(r0, a, eps), 1e-10)


def test_p49_dipole_sphere_force():
    """Ex. 5.11.4: closed force components == -grad W (finite differences);
    consistent with the exact induced-kernel energy of a physical dipole at
    large d; attractive along -z."""
    a, eps = 1.0, 4.0
    p = np.array([0.5, -0.3, 0.7]); d = 6.0
    F = sphere_dipole_force(d, p, a, eps)
    F_fd = -grad_fd(lambda x: sphere_dipole_W(x, p, a, eps),
                    np.array([0.0, 0.0, d]), h=1e-4)
    assert _vclose(F, F_fd, 1e-5)
    assert F[2] < 0
    # exact two-charge energy: W_exact ~ W(d) at large d
    W_th = sphere_dipole_W(np.array([0, 0, d]), p, a, eps)
    W_ex = sphere_dipole_W_exact(np.array([0, 0, d]), p, a, eps, delta=1e-3)
    assert _close(W_ex, W_th, 4 * (a / d) ** 2)
    # i = 1,2 components: F_i = 3 alpha p3 p_i/d^7
    alpha = (eps - 1) / (eps + 2) * a ** 3
    assert _close(F[0], 3 * alpha * p[2] * p[0] / d ** 7, 1e-12)
    assert _close(F[2], -3 * alpha * (3 * p[2] ** 2 + p @ p) / d ** 7, 1e-12)


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    import time
    verbose = os.environ.get('VERBOSE_TESTS', '')
    t0 = time.perf_counter()
    tests = [(k, v) for k, v in sorted(globals().items())
             if k.startswith('test_') and callable(v)]
    failed = []
    for name, fn in tests:
        t1 = time.perf_counter()
        try:
            fn()
        except AssertionError as exc:
            failed.append((name, 'assert', exc))
        except Exception as exc:                                # noqa: BLE001
            failed.append((name, type(exc).__name__, exc))
        if verbose:
            print(f"  {name}: {time.perf_counter() - t1:.2f} s", flush=True)
    dt = time.perf_counter() - t0
    if failed:
        for name, kind, exc in failed:
            print(f"FAIL {name}: {kind}: {exc}")
        print(f"{len(failed)}/{len(tests)} tests FAILED ({dt:.1f} s)")
        raise SystemExit(1)
    print(f"All {len(tests)} tests passed. ({dt:.1f} s)")
