"""Tests for MACRO_EM-06 -- every Wilcox Ch. 6 exercise that admits a numeric
check is exercised here (P1-P38).

Run directly:   python3 test_magnetostatics.py     (-> "All N tests passed.")
Or with pytest: pytest test_magnetostatics.py

Gaussian units with c = 1 (module constant C); Biot-Savart carries the 1/c
explicitly (Eq. 6.7); grad x B = 4 pi J / c (6.35); div B = 0 (6.27).
"""
import numpy as np

from magnetostatics import (
    C, gauss_legendre, dfact, grad_fd, div_fd, curl_fd,
    # loop fields
    loop_Bz_axis, loop_B_elliptic, loop_B_bessel, loop_A_bessel, loop_A_IK,
    loop_B_3d, loop_A_3d, dipole_B, loop_B_spherical,
    # Secs. 6.1-6.4
    circuit_force_partial, chord_force,
    wire_B_phi, pinch_pressure, pinch_pressure_quad,
    spinning_cylinder_B, spinning_cylinder_B_quad,
    sheet_B, sheet_B_wires,
    # Sec. 6.5
    stokes_transform_lhs, stokes_transform_rhs,
    solid_angle_disk_axis, solid_angle_disk_bessel, solid_angle_disk_quad,
    solid_angle_rect, solid_angle_square_center,
    solid_angle_sphere_quad, solid_angle_cube_quad,
    # Sec. 6.6
    solenoid_B_inside_bessel, solenoid_Bz_outside_bessel, solenoid_Bz_axis,
    solenoid_B_loops, solenoid_corr_axis, solenoid_corr_axis_asym,
    spinning_disk_B_bessel, spinning_disk_B_rings, spinning_disk_moment,
    spinning_cylinder_solid_Bz_bessel, spinning_cylinder_solid_Bz_disks,
    weber_schafheitlin, cone_Bz_tip, cone_Bz_tip_quad,
    # Sec. 6.7
    solid_angle_disk_series, solid_angle_disk_series_split,
    loop_Br_series, loop_Bth_series,
    rotating_shell_B, rotating_shell_B_quad,
    rotating_solid_sphere_B, rotating_solid_sphere_B_quad,
    costheta_shell_B, costheta_shell_B_quad,
    # Sec. 6.8
    circuit_moment, saddle_circuit, saddle_moment,
    bent_loop_circuit, bent_loop_moment,
    gradgrad_1r_box, dipole_ball_integral, jm_moment_smeared,
    make_divfree_J, grid_integrate, moment_vector, quad_moment_mij,
    cyclic_integral, xxJ_integral, EPS3, A_quadrupole, B_quadrupole,
    A_exact_from_J,
    costheta_shell_sij, costheta_shell_mij_quad,
    slab_equiv_current, slab_B_charges,
    # Sec. 6.9
    wire_dipole_force, wire_dipole_torque, wire_B,
    small_loop_force, small_loop_torque, loop_force_quad, force_grad_mB,
    # Secs. 6.10-6.11
    hemisphere_torque_quad, hemisphere_torque,
    cavity_C1C2, sphere_C1C2, cavity_fields, cavity_Kb_coefficient,
    perm_sphere_phim, perm_sphere_B, perm_sphere_M,
    # Sec. 6.12
    image_coeffs_vacuum_source, image_coeffs_embedded_source, mirror_loop,
    interface_BC_residual_vacuum_source, interface_BC_residual_embedded_source,
    loop_image_force, solid_angle_B, greens_phim, sphere_image_ring,
    dipole_slab_force, dipole_slab_force_quad,
    # Sec. 6.13
    A_magnetized_sphere, A_magnetization_surface, A_direct_dipole_sum,
    A_curl_plus_surface, split_sphere_Cn, split_sphere_phim_exterior,
    split_sphere_phim_interior, split_sphere_phim_quad,
    disk_phim_quad, bar_H_exact, bar_H_monopoles,
    square_face_omega, cube_Hz, cube_Hz_direct,
    rod_H_bessel, rod_H_disks,
    closed_shell_phim_sphere, closed_shell_phim_cube,
)

RNG = np.random.default_rng(20260706)


def _approx(x, y, rel=1e-9, abs_=0.0):
    x, y = np.asarray(x, float), np.asarray(y, float)
    return np.all(np.abs(x - y) <= rel * np.abs(y) + abs_)


# ------------------------------- global Maxwell checks (Secs. 6.2, 6.3, 6.5)

def test_div_curl_ampere():
    """div B = 0 (6.27) and curl B = 0 off the sources for the loop field;
    curl B = 4 pi J/c (6.35) inside a uniform wire; Ampere's law (6.36)/(6.58)
    for a path linking the circular loop."""
    Bf = lambda y: loop_B_3d(y, [0, 0, 0], [0, 0, 1], 1.0, 1.0, N=512)
    for x in ([0.3, 0.2, 0.5], [1.6, -0.4, 0.2], [0.1, 0.0, -0.9]):
        assert abs(div_fd(Bf, x, h=1e-4)) < 2e-6
        assert np.max(np.abs(curl_fd(Bf, x, h=1e-4))) < 2e-5
    # uniform wire: curl of the closed-form field = 4 pi J/c inside, 0 outside
    a, I = 1.0, 2.0
    Bw = lambda y: np.array([-y[1], y[0], 0.0]) / np.hypot(y[0], y[1]) \
        * wire_B_phi(np.hypot(y[0], y[1]), a, I)
    Jz = I / (np.pi * a**2)
    assert _approx(curl_fd(Bw, [0.4, 0.2, 0.0], h=1e-5),
                   [0, 0, 4 * np.pi * Jz / C], rel=1e-6, abs_=1e-8)
    assert np.max(np.abs(curl_fd(Bw, [1.5, 0.9, 0.0], h=1e-5))) < 1e-8
    # Ampere: circulate B around a small circle threading the loop wire; the
    # x->z sense links the +e_phi current negatively, so (6.58) gives -4piI/c
    n, r0, eps = 400, 1.0, 0.35
    t = (np.arange(n) + 0.5) * 2 * np.pi / n
    circ = 0.0
    for ti in t:
        x = np.array([r0 + eps * np.cos(ti), 0.0, eps * np.sin(ti)])
        dl = eps * (2 * np.pi / n) * np.array([-np.sin(ti), 0.0, np.cos(ti)])
        circ += Bf(x) @ dl
    assert _approx(circ, -4 * np.pi * 1.0 / C, rel=2e-3)
    # a path that does not link the wire encloses zero current
    circ0 = 0.0
    for ti in t:
        x = np.array([2.5 + 0.3 * np.cos(ti), 0.0, 0.3 * np.sin(ti)])
        dl = 0.3 * (2 * np.pi / n) * np.array([-np.sin(ti), 0.0, np.cos(ti)])
        circ0 += Bf(x) @ dl
    assert abs(circ0) < 1e-6


# ------------------------------------------------ P1 (6.1.1) immersed circuit

def test_p1_partial_circuit_force():
    """Ex. 6.1.1: force on the immersed part = (I/c) L x B, L = entry->exit
    chord; independent of the in-field wiggles of the circuit."""
    B = np.array([0.0, 0.0, 1.3])          # field in y > 0 (perp to plane z=0)
    inside = lambda p: p[1] > 0.0
    entry, exit_ = np.array([0.8, 0.0, 0.0]), np.array([-0.6, 0.0, 0.0])
    # two different irregular circuits with the same entry/exit points
    path1 = np.array([entry, [0.9, 0.7, 0], [0.2, 1.4, 0], [-0.5, 0.8, 0],
                      exit_, [-0.9, -0.8, 0], [0.3, -1.1, 0]])
    path2 = np.array([entry, [1.5, 0.3, 0], [1.2, 1.9, 0], [-0.2, 0.6, 0],
                      [-0.8, 1.3, 0], exit_, [0.1, -0.7, 0]])
    Fc = chord_force(entry, exit_, B)
    for pts in (path1, path2):
        F = circuit_force_partial(pts, B, inside)
        assert _approx(F, Fc, rel=1e-12, abs_=1e-12)
    assert abs(Fc @ B) < 1e-15                      # F perpendicular to B
    # refine path1 by inserting midpoints on in-field edges: force unchanged
    dense = []
    for i in range(len(path1)):
        p, q = path1[i], path1[(i + 1) % len(path1)]
        dense += [p, 0.5 * (p + q) + (0.03 if inside(0.5 * (p + q)) else 0.0)
                  * np.array([0, 1.0, 0])]
    F3 = circuit_force_partial(np.array(dense), B, inside)
    assert _approx(F3, Fc, rel=1e-12, abs_=1e-12)


# ------------------------------------------------------- P2 (6.3.1) the pinch

def test_p2_pinch_pressure():
    """Ex. 6.3.1: P(rho) = (I^2/(pi c^2 a^2))(1 - rho^2/a^2), inward, built by
    integrating dP/drho = -J B_phi/c; B_phi from Ampere's law."""
    a, I = 1.3, 2.1
    for rho in (0.0, 0.4, 0.9, 1.2):
        assert _approx(pinch_pressure(rho, a, I), pinch_pressure_quad(rho, a, I),
                       rel=1e-10, abs_=1e-14)
    assert _approx(pinch_pressure(0.0, a, I), I**2 / (np.pi * C**2 * a**2))
    assert pinch_pressure(a, a, I) == 0.0 and pinch_pressure(2 * a, a, I) == 0.0
    assert np.all(np.diff(pinch_pressure(np.linspace(0, a, 30), a, I)) < 0)
    # Ampere check on B_phi: 2 pi rho B_phi = (4 pi/c) I_enc
    for rho in (0.5, 1.0, 2.0):
        Ienc = I * min(rho, a) ** 2 / a**2
        assert _approx(2 * np.pi * rho * wire_B_phi(rho, a, I),
                       4 * np.pi * Ienc / C, rel=1e-12)


# --------------------------------------- P3 (6.3.2) spinning+sliding cylinder

def test_p3_spinning_sliding_cylinder():
    """Ex. 6.3.2: B = (4 pi sigma omega R/c) zhat inside, (4 pi sigma R v0/c)
    e_phi/rho outside -- Ampere closed forms vs direct Biot-Savart."""
    R, sig, om, v0 = 1.0, 0.8, 1.7, 1.1
    for rho in (0.3, 0.75):
        bp, bz = spinning_cylinder_B(rho, R, sig, om, v0)
        bp_q, bz_q = spinning_cylinder_B_quad(rho, R, sig, om, v0)
        assert _approx(bz, bz_q, rel=2e-3) and abs(bp_q) < 2e-3 * abs(bz)
        assert _approx(bz, 4 * np.pi * sig * om * R / C, rel=1e-12)
    for rho in (1.4, 2.5):
        bp, bz = spinning_cylinder_B(rho, R, sig, om, v0)
        bp_q, bz_q = spinning_cylinder_B_quad(rho, R, sig, om, v0)
        assert _approx(bp, bp_q, rel=2e-3) and abs(bz_q) < 2e-3 * abs(bp)
        assert _approx(bp, 4 * np.pi * sig * R * v0 / (C * rho), rel=1e-12)


# --------------------------------------------------- P4 (6.4.1) current sheet

def test_p4_current_sheet():
    """Ex. 6.4.1: K = K0 zhat in the y-z plane gives B = +-(2 pi K0/c) yhat;
    jump obeys n x (B2 - B1) = 4 pi K/c (6.43)."""
    K0 = 1.9
    for x in (0.5, 2.0):
        assert _approx(sheet_B(x, K0), sheet_B_wires(x, K0), rel=1e-6, abs_=1e-9)
        assert _approx(sheet_B(-x, K0), -sheet_B(x, K0), rel=1e-15)
    jump = sheet_B(1e-6, K0) - sheet_B(-1e-6, K0)      # B2 - B1, n = +xhat
    assert _approx(np.cross([1.0, 0, 0], jump),
                   4 * np.pi / C * np.array([0, 0, K0]), rel=1e-12)


# ---------------------------------------------- P5 (6.5.1) Stokes transform

def test_p5_stokes_transform():
    """Ex. 6.5.1: oint dl x A = Int (ds x grad) x A for a smooth random A,
    on a flat disk and on a curved (paraboloid) cap with the same boundary."""
    def A(x):
        x, y, z = x
        return np.array([x * y - z**2, np.sin(x) + y * z, x + y * y - 0.3 * z])
    curve = lambda t: np.array([np.cos(2 * np.pi * t), np.sin(2 * np.pi * t), 0.0])
    lhs = stokes_transform_lhs(A, curve)
    # u radial, v azimuthal so ds = x_u x x_v points along +zhat, matching the
    # right-hand rule for the counterclockwise boundary
    disk = lambda u, v: np.array([u * np.cos(2 * np.pi * v), u * np.sin(2 * np.pi * v), 0.0])
    cap = lambda u, v: np.array([u * np.cos(2 * np.pi * v), u * np.sin(2 * np.pi * v),
                                 0.7 * (1 - u**2)])
    assert _approx(stokes_transform_rhs(A, disk), lhs, rel=1e-5, abs_=1e-6)
    assert _approx(stokes_transform_rhs(A, cap), lhs, rel=1e-5, abs_=1e-6)


# ------------------------------------------------- P6 (6.6.1) solenoid inside

def test_p6_solenoid_bessel_inside():
    """Ex. 6.6.1(a): the Bessel-integral B_rho, B_z (|z| < d/2) match the
    brute-force loop stack and the exact on-axis form."""
    a, d, nI = 1.0, 4.0, 1.0
    for (rho, z) in [(0.4, 0.7), (0.9, -1.2), (1.3, 0.5), (0.0, 1.6)]:
        br, bz = solenoid_B_inside_bessel(rho, z, a, d, nI)
        br_q, bz_q = solenoid_B_loops(rho, z, a, d, nI)
        assert _approx(br, br_q, rel=2e-6, abs_=1e-8)
        assert _approx(bz, bz_q, rel=2e-6, abs_=1e-8)
    for z in (0.0, 1.1):
        _, bz = solenoid_B_inside_bessel(0.0, z, a, d, nI)
        assert _approx(bz, solenoid_Bz_axis(z, a, d, nI), rel=1e-8)


def test_p6_correction_term_falloff():
    """Ex. 6.6.1(b): the Bz correction at the center falls like 1/d^2:
    d^2 * corr -> 8 pi a^2 nI/c."""
    a, nI = 1.0, 1.0
    ratios = [solenoid_corr_axis(a, d, nI) / solenoid_corr_axis_asym(a, d, nI)
              for d in (10.0, 20.0, 40.0, 80.0)]
    assert abs(ratios[-1] - 1) < 5e-4
    assert all(abs(r2 - 1) < abs(r1 - 1) for r1, r2 in zip(ratios, ratios[1:]))


# --------------------------------------------------- P7 (6.6.2) spinning disk

def test_p7_spinning_disk():
    """Ex. 6.6.2: Bessel forms vs ring superposition; B_rho odd in z."""
    R, sig, om = 1.0, 0.9, 1.4
    for (rho, z) in [(0.3, 0.5), (0.8, -0.4), (1.5, 0.8)]:
        br, bz = spinning_disk_B_bessel(rho, z, R, sig, om)
        br_q, bz_q = spinning_disk_B_rings(rho, z, R, sig, om)
        assert _approx(br, br_q, rel=5e-6, abs_=1e-9)
        assert _approx(bz, bz_q, rel=5e-6, abs_=1e-9)
    brp, _ = spinning_disk_B_bessel(0.5, 0.6, R, sig, om)
    brm, _ = spinning_disk_B_bessel(0.5, -0.6, R, sig, om)
    assert _approx(brp, -brm, rel=1e-12)


def test_p7_disk_far_field_moment():
    """Ex. 6.6.2 extra: Bz -> (pi sigma omega/2c) R^4/|z|^3, i.e. a dipole of
    moment m_z = pi sigma omega R^4/(4c)."""
    R, sig, om = 1.0, 0.9, 1.4
    m = spinning_disk_moment(R, sig, om)
    assert _approx(m, np.pi * sig * om * R**4 / (4 * C), rel=1e-15)
    for z in (8.0, 16.0):
        _, bz = spinning_disk_B_bessel(0.0, z, R, sig, om, n=800)
        # exact axis expansion: Bz = (2m/z^3)(1 - R^2/z^2 + ...)
        assert _approx(bz, 2 * m / z**3, rel=1.2 * (R / z) ** 2)
        assert _approx(bz, 2 * m / z**3 * (1 - (R / z) ** 2), rel=2e-3)


# ------------------------------------------- P8 (6.6.3) spinning solid cylinder

def test_p8_spinning_solid_cylinder():
    """Ex. 6.6.3: Bz Bessel form (|z| < d/2) vs stacked spinning disks; the
    Weber-Schafheitlin integral behind the H(R - rho) step term."""
    R, d, r0, om = 1.0, 3.0, 0.8, 1.2
    for (rho, z) in [(0.4, 0.6), (0.9, -0.9), (1.4, 0.3)]:
        bz = spinning_cylinder_solid_Bz_bessel(rho, z, R, d, r0, om)
        bz_q = spinning_cylinder_solid_Bz_disks(rho, z, R, d, r0, om, nz=120, nr=120)
        assert _approx(bz, bz_q, rel=3e-4, abs_=1e-6)
    # Int_0^inf dk J2(kR) J0(k rho)/k = (R^2 - rho^2)/(2 R^2) inside, 0 outside
    assert _approx(weber_schafheitlin(0.5, 1.0), (1 - 0.25) / 2, rel=2e-3)
    assert abs(weber_schafheitlin(1.5, 1.0)) < 2e-3


# --------------------------------------------- P9 (6.6.4) I1 K1 loop potential

def test_p9_loop_A_IK():
    """Ex. 6.6.4: A_phi = (4Ia/c) Int dk cos(kz) I1(k rho<) K1(k rho>) equals
    the (6.227) Laplace form and the direct Biot-Savart line integral."""
    a, I = 1.0, 1.0
    for (rho, z) in [(0.5, 0.4), (1.6, 0.7), (0.8, -1.1)]:
        A1 = loop_A_IK(rho, z, a, I)
        A2 = loop_A_bessel(rho, z, a, I)
        A3 = loop_A_3d([rho, 0.0, z], [0, 0, 0], [0, 0, 1], a, I)[1]  # e_phi = +y
        assert _approx(A1, A2, rel=2e-6)
        assert _approx(A1, A3, rel=2e-6)


# ------------------------------------------------- P10 (6.6.5) truncated cone

def test_p10_cone_tip_field():
    """Ex. 6.6.5: Bz(0) = (2 pi sigma omega/c)(L2 - L1) sin^3 a/cos a."""
    for (al, L1, L2) in [(0.4, 0.5, 2.0), (0.9, 1.0, 3.0)]:
        assert _approx(cone_Bz_tip(al, L1, L2, 1.1, 0.9),
                       cone_Bz_tip_quad(al, L1, L2, 1.1, 0.9), rel=1e-10)
    # small-alpha limit ~ alpha^3
    r = cone_Bz_tip(1e-3, 1, 2, 1, 1) / cone_Bz_tip(2e-3, 1, 2, 1, 1)
    assert _approx(r, 1 / 8, rel=1e-5)


# --------------------------------------- P11 (6.7.1) disk solid-angle series

def test_p11_solid_angle_series():
    """Ex. 6.7.1: Legendre series for Omega (r >= a, r <= a, and the sign-split
    interior form) against quadrature, the Bessel form (6.73), and the on-axis
    closed form (6.60)."""
    a = 1.0
    for (r, th) in [(1.5, 0.4), (2.2, 1.9), (1.05, 2.6)]:
        x = np.array([r * np.sin(th), 0.0, r * np.cos(th)])
        Om = solid_angle_disk_series(r, th, a)
        assert _approx(Om, solid_angle_disk_quad(x, a), rel=2e-6, abs_=1e-7)
        assert _approx(Om, solid_angle_disk_bessel(r * np.sin(th), r * np.cos(th), a),
                       rel=2e-6, abs_=1e-7)
    for (r, th) in [(0.5, 0.3), (0.8, 2.1), (0.95, 1.2)]:
        x = np.array([r * np.sin(th), 0.0, r * np.cos(th)])
        q = solid_angle_disk_quad(x, a)
        # split form: geometric convergence
        assert _approx(solid_angle_disk_series_split(r, th, a, N=300), q,
                       rel=1e-6, abs_=1e-6)
        # plain interior branch: conditionally convergent constant part -> ~1/N
        e1 = abs(solid_angle_disk_series(r, th, a, N=100) - q)
        e2 = abs(solid_angle_disk_series(r, th, a, N=800) - q)
        assert e2 < 2e-2 and e2 < e1
    # the two 6.7.1 branches agree termwise at r = a, by the coefficient
    # identity (2n+1)!!/(2n+2)!! = ((2n-1)!!/(2n)!!)[(4n+3)/(2n+2) - 1]:
    # evaluating each branch a hair to either side of r = a gives the same sum
    for th in (0.7, 2.2):
        d = abs(solid_angle_disk_series(1.0, th, a, N=300)          # r>=a branch
                - solid_angle_disk_series(1.0 - 1e-12, th, a, N=300))  # r<=a branch
        assert d < 1e-9
    # on-axis closed form (6.60): exterior branch directly, interior via the
    # geometrically convergent split form
    assert _approx(solid_angle_disk_axis(-1.3, a),
                   solid_angle_disk_series(1.3, np.pi, a), rel=1e-9)
    assert _approx(solid_angle_disk_axis(0.4, a),
                   solid_angle_disk_series_split(0.4, 0.0, a, N=300), rel=1e-9)


# ------------------------------------------ P12 (6.7.2) loop Br/Btheta series

def test_p12_loop_field_series():
    """Ex. 6.7.2: the (6.119)/(6.121) series from the solid angle reproduce
    the elliptic-integral loop field, r < a and r > a."""
    a, I = 1.0, 1.3
    for (r, th) in [(1.6, 0.5), (2.4, 1.8), (0.55, 0.9), (0.75, 2.3)]:
        Br_s = loop_Br_series(r, th, a, I, N=200)
        Bt_s = loop_Bth_series(r, th, a, I, N=200)
        Br_e, Bt_e = loop_B_spherical(r, th, a, I)
        assert _approx(Br_s, Br_e, rel=1e-8, abs_=1e-10)
        assert _approx(Bt_s, Bt_e, rel=1e-8, abs_=1e-10)


# --------------------------------------------- P13 (6.7.3) rotating shell

def test_p13_rotating_shell():
    """Ex. 6.7.3: B = (8 pi a sigma omega/3c) zhat inside; pure dipole with
    m = 4 pi sigma omega a^4/(3c) outside -- vs Biot-Savart over the shell."""
    a, sig, om = 1.0, 0.7, 1.2
    for x in ([0.3, 0.1, 0.2], [0.0, 0.0, -0.6]):
        assert _approx(rotating_shell_B(x, a, sig, om),
                       rotating_shell_B_quad(x, a, sig, om, n=400),
                       rel=1e-6, abs_=1e-8)
    for x in ([1.8, 0.0, 0.9], [0.4, -0.3, 1.5]):
        assert _approx(rotating_shell_B(x, a, sig, om),
                       rotating_shell_B_quad(x, a, sig, om, n=400),
                       rel=1e-6, abs_=1e-8)
    Bin = rotating_shell_B([0.5, -0.2, 0.1], a, sig, om)
    assert _approx(Bin, [0, 0, 8 * np.pi * a * sig * om / (3 * C)], rel=1e-14)


# ------------------------------------------ P14 (6.7.4) rotating solid sphere

def test_p14_rotating_solid_sphere():
    """Ex. 6.7.4: outside a pure dipole m = 4 pi a^5 omega rho/(15 c); inside
    an m(r) dipole plus a zhat field vanishing at r = a -- vs shell stack."""
    a, rq, om = 1.0, 0.8, 1.1
    for x in ([0.4, 0.2, 0.3], [1.5, -0.4, 0.8], [0.0, 0.0, 0.7]):
        assert _approx(rotating_solid_sphere_B(x, a, rq, om),
                       rotating_solid_sphere_B_quad(x, a, rq, om),
                       rel=1e-8, abs_=1e-10)
    m = 4 * np.pi * a**5 * om * rq / (15 * C)
    x = np.array([0.9, 0.5, 1.1])
    assert _approx(rotating_solid_sphere_B(x, a, rq, om), dipole_B(x, [0, 0, m]),
                   rel=1e-12)
    # the extra zhat piece vanishes at r = a: field is continuous there
    xs = np.array([0.6, 0.0, 0.8])       # |x| = 1
    Bi = rotating_solid_sphere_B(0.999999 * xs, a, rq, om)
    Bo = rotating_solid_sphere_B(1.000001 * xs, a, rq, om)
    assert _approx(Bi, Bo, rel=1e-4, abs_=1e-6)


# ------------------------------------------- P15 (6.7.5) cos-theta shell

def test_p15_costheta_shell():
    """Ex. 6.7.5: interior B = (4 pi sigma0 omega/5c)(-x, -y, 2z); exterior
    the quoted quadrupole form -- vs Biot-Savart over the shell."""
    a, s0, om = 1.0, 0.9, 1.3
    for x in ([0.3, 0.2, 0.4], [0.0, 0.5, -0.3], [1.4, 0.2, 0.6], [0.5, -0.8, 1.2]):
        assert _approx(costheta_shell_B(x, a, s0, om),
                       costheta_shell_B_quad(x, a, s0, om, n=400),
                       rel=2e-6, abs_=1e-8)
    # exterior falls like 1/r^4 (quadrupole, no dipole term)
    B1 = np.linalg.norm(costheta_shell_B([0, 0, 4.0], a, s0, om))
    B2 = np.linalg.norm(costheta_shell_B([0, 0, 8.0], a, s0, om))
    assert _approx(B1 / B2, 16.0, rel=1e-12)


# --------------------------------------------- P16 (6.8.1) solenoid outside

def test_p16_solenoid_outside_dipole():
    """Ex. 6.8.1: outside Bessel form vs loop stack; far field
    Bz -> 2 pi a^2 I N/(c |z|^3) = dipole of moment N I pi a^2/c."""
    a, d, nI = 1.0, 2.0, 1.0
    for (rho, z) in [(0.3, 1.6), (0.8, -1.4), (1.5, 2.0)]:
        bz = solenoid_Bz_outside_bessel(rho, z, a, d, nI)
        _, bz_q = solenoid_B_loops(rho, z, a, d, nI)
        assert _approx(bz, bz_q, rel=2e-6, abs_=1e-9)
    N = d * nI
    for z in (12.0, 24.0):
        bz = solenoid_Bz_outside_bessel(0.0, z, a, d, nI, n=800)
        assert _approx(bz, 2 * np.pi * a**2 * 1.0 * N / (C * z**3), rel=2e-2)
        m = np.pi * a**2 * N / C          # multipole view: pure dipole term
        assert _approx(bz, dipole_B([0, 0, z], [0, 0, m])[2], rel=2e-2)


# ------------------------------------------------ P17 (6.8.2) shaved magnet

def test_p17_shaved_magnet_rim_current():
    """Ex. 6.8.2: a thin slab magnetized perpendicular to its faces equals a
    rim circuit with I = c M0 d: charge-picture B vs Biot-Savart loop, with
    O(d^2) convergence as the slab thins."""
    R, M0 = 1.0, 2.0
    for x in ([1.4, 0.3, 0.5], [0.4, -0.2, 0.9], [0.0, 1.8, -0.6]):
        errs = []
        for dt in (0.08, 0.04, 0.02):
            Bs = slab_B_charges(np.asarray(x), R, dt, M0)
            Bl = loop_B_3d(np.asarray(x), [0, 0, 0], [0, 0, 1], R,
                           slab_equiv_current(M0, dt), N=512)
            errs.append(np.max(np.abs(Bs - Bl)) / np.max(np.abs(Bl)))
        assert errs[-1] < 2e-4
        assert errs[2] < errs[0] / 8       # ~ d^2 shrinkage


# -------------------------------------------------- P18 (6.8.3) two moments

def test_p18_saddle_and_bent_moments():
    """Ex. 6.8.3: m = (I/2c) oint x x dl quadrature vs the closed forms for
    the saddle circuit and the 90-degree bent loop; origin independence."""
    R, L = 1.0, 2.0
    assert _approx(circuit_moment(saddle_circuit(R, L)), saddle_moment(R, L),
                   rel=1e-5, abs_=1e-6)
    assert _approx(circuit_moment(bent_loop_circuit(R)), bent_loop_moment(R),
                   rel=1e-5, abs_=1e-6)
    assert _approx(np.linalg.norm(bent_loop_moment(R)),
                   np.pi * R**2 / (np.sqrt(2) * C), rel=1e-12)
    shifted = saddle_circuit(R, L) + np.array([0.7, -1.1, 0.4])
    assert _approx(circuit_moment(shifted), saddle_moment(R, L), rel=1e-5, abs_=1e-6)


# ----------------------------------------- P19 (6.8.4) point dipole delta term

def test_p19_dipole_delta_field():
    """Ex. 6.8.4: grad_i grad_j (1/r) carries -(4 pi/3) delta_ij delta(x)
    (6.139); Int_ball B d^3x = (8 pi/3) m; J_m = -c m x grad delta reproduces
    m through (6.129); B is curl-free away from the origin."""
    assert _approx(gradgrad_1r_box(0, 0), -4 * np.pi / 3, rel=1e-6)
    assert _approx(gradgrad_1r_box(2, 2), -4 * np.pi / 3, rel=1e-6)
    assert abs(gradgrad_1r_box(0, 1)) < 1e-12 and abs(gradgrad_1r_box(1, 2)) < 1e-12
    m = np.array([0.3, -0.5, 0.8])
    assert _approx(dipole_ball_integral(m), 8 * np.pi / 3 * m, rel=1e-6, abs_=1e-9)
    assert _approx(jm_moment_smeared(m), m, rel=1e-6, abs_=1e-9)
    for x in ([0.4, 0.1, 0.3], [-0.2, 0.5, -0.7]):
        assert np.max(np.abs(curl_fd(lambda y: dipole_B(y, m), x, h=1e-5))) < 1e-6


# --------------------------------------- P20 (6.8.5) magnetic quadrupole moment

def test_p20_cyclic_identity_and_mij():
    """Ex. 6.8.5(a,b): the cyclic integral vanishes for div-free localized J,
    and (1/c) Int x_i x_j J_k = -(1/2) sum_r (eps_kir m_rj + eps_kjr m_ri)."""
    for kind in (0, 1):
        J = make_divfree_J(kind=kind)
        mij = quad_moment_mij(J)
        scale = np.max(np.abs(mij)) + max(
            abs(xxJ_integral(J, i, j, k)) for (i, j, k)
            in [(0, 1, 2), (2, 2, 0), (0, 0, 1), (2, 1, 1)])
        for (i, j, k) in [(0, 1, 2), (0, 0, 1), (2, 1, 1)]:
            assert abs(cyclic_integral(J, i, j, k)) < 1e-5 * scale
        assert abs(np.trace(mij)) < 1e-12 + 1e-9 * np.max(np.abs(mij))
        for (i, j, k) in [(0, 1, 2), (1, 2, 0), (0, 0, 2), (2, 1, 0)]:
            lhs = xxJ_integral(J, i, j, k) / C
            rhs = -0.5 * sum(EPS3[k, i, r] * mij[r, j] + EPS3[k, j, r] * mij[r, i]
                             for r in range(3))
            assert abs(lhs - rhs) < 1e-5 * scale


def test_p20_quadrupole_potential():
    """Ex. 6.8.5(c): A - A_dipole ~ A^(q) far away."""
    J = make_divfree_J(kind=0)
    mvec = moment_vector(J)
    mij = quad_moment_mij(J)
    for r in (6.0, 9.0):
        x = r * np.array([0.4, 0.5, 0.76]) / np.linalg.norm([0.4, 0.5, 0.76])
        A_ex = A_exact_from_J(x, J)
        A_d = np.cross(mvec, x) / r**3
        A_q = A_quadrupole(x, mij)
        # the quadrupole term explains the dipole residual
        assert np.linalg.norm(A_ex - A_d - A_q) < 0.05 * np.linalg.norm(A_q)


# ----------------------------------------- P21 (6.8.6) magnetic quadrupole field

def test_p21_quadrupole_field():
    """Ex. 6.8.6: B^(q) = curl A^(q) with s_ij = sym(m_ij); s is symmetric
    traceless (5 components); the cos-theta shell of P15 is a pure quadrupole
    with s_11 = s_22 = -8 pi sigma0 a^5 omega/(45 c) = -s_33/2."""
    J = make_divfree_J(kind=1)
    mij = quad_moment_mij(J)
    sij = 0.5 * (mij + mij.T)
    assert abs(np.trace(sij)) < 1e-9 * np.max(np.abs(sij))
    Af = lambda y: A_quadrupole(y, mij)
    for x in ([1.5, 0.4, 0.8], [-0.9, 1.1, 0.5]):
        assert _approx(B_quadrupole(np.asarray(x), sij), curl_fd(Af, x, h=1e-5),
                       rel=1e-5, abs_=1e-9)
    a, s0, om = 1.0, 0.9, 1.3
    s_shell = costheta_shell_sij(a, s0, om)
    s_quad = 0.5 * (costheta_shell_mij_quad(a, s0, om, n=200)
                    + costheta_shell_mij_quad(a, s0, om, n=200).T)
    assert _approx(s_shell, s_quad, rel=1e-8, abs_=1e-10)
    for x in ([1.6, 0.3, 0.9], [0.5, -1.2, 1.4]):
        assert _approx(B_quadrupole(np.asarray(x), s_shell),
                       costheta_shell_B(x, a, s0, om), rel=1e-10, abs_=1e-12)


# ------------------------------------------------ P22 (6.9.1) dipole near wire

def test_p22_wire_dipole_force_torque():
    """Ex. 6.9.1: F = -(2I/c x0^2)(m_y, m_x, 0), N = (2I/c x0)(-m_z, 0, m_x)
    -- vs small-loop quadrature in the wire field."""
    I, x0 = 1.7, 1.3
    for m in (np.array([0.6, -0.4, 0.9]), np.array([-1.1, 0.5, 0.2])):
        F = wire_dipole_force(m, I, x0)
        N = wire_dipole_torque(m, I, x0)
        eps = 1e-4      # the loop torque carries a real O(eps) finite-size term
        Iloop = np.linalg.norm(m) * C / (np.pi * eps**2)
        nhat = m / np.linalg.norm(m)
        Bw = lambda y: wire_B(y, I)
        Fq = small_loop_force(Bw, [x0, 0, 0], nhat, eps, Iloop)
        Nq = small_loop_torque(Bw, [x0, 0, 0], nhat, eps, Iloop)
        assert _approx(F, Fq, rel=1e-5, abs_=1e-8)
        assert _approx(N, Nq, rel=5e-4, abs_=1e-8)
        assert _approx(N, np.cross(m, Bw(np.array([x0, 0, 0]))), rel=1e-12)


# --------------------------------------------- P23 (6.9.2) force from expansion

def test_p23_force_is_grad_mB():
    """Ex. 6.9.2: F = (I/c) oint dx x B on a small loop equals grad(m.B) for
    an external (curl-free) field."""
    msrc = np.array([0.7, -0.3, 1.1])
    Bext = lambda y: dipole_B(np.asarray(y) - np.array([3.0, 1.0, -2.0]), msrc)
    center, nhat, eps, I = np.array([0.2, -0.4, 0.3]), np.array([0.36, 0.48, 0.8]), 5e-3, 40.0
    m = I * np.pi * eps**2 / C * nhat
    Fq = small_loop_force(Bext, center, nhat, eps, I, N=800)
    Fg = force_grad_mB(Bext, m, center)
    assert _approx(Fq, Fg, rel=2e-5, abs_=1e-10)
    # polygon version of the same loop
    ph = (np.arange(2000) + 0.5) * 2 * np.pi / 2000
    e1 = np.array([0.8, -0.6, 0.0]); e2 = np.cross(nhat, e1)
    pts = center + eps * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
    assert _approx(loop_force_quad(Bext, pts, I), Fg, rel=2e-5, abs_=1e-10)


# ------------------------------------------- P24 (6.10.1) torque on hemisphere

def test_p24_hemisphere_torque():
    """Ex. 6.10.1: N = oint da x x (K_eff x B0)/c = m x B0; hemisphere with
    M = M0 khat in B0 = B0 xhat gives N = (2 pi a^3 M0 B0/3) yhat."""
    a, M0, B0 = 1.2, 0.9, 1.5
    Nq = hemisphere_torque_quad(a, M0, [B0, 0, 0], n=120)
    Nc = hemisphere_torque(a, M0, [B0, 0, 0])
    assert _approx(Nq, Nc, rel=1e-8, abs_=1e-10)
    assert _approx(Nc, [0, 2 * np.pi * a**3 * M0 * B0 / 3, 0], rel=1e-12)
    # generic B0 direction
    B0v = np.array([0.4, -0.7, 1.1])
    assert _approx(hemisphere_torque_quad(a, M0, B0v, n=120),
                   hemisphere_torque(a, M0, B0v), rel=1e-8, abs_=1e-10)


# ------------------------------------------ P25 (6.10.2) dipole in cavity/sphere

def test_p25_dipole_cavity_and_sphere():
    """Ex. 6.10.2: C1 = (mu-1)/(2mu+1), C2 = 3mu/(2mu+1) satisfy the BCs;
    the mu -> 1/mu map gives the permeable-sphere pair; K_b matches the
    rotating-sphere K_f with sigma omega a <-> (3cm/4pi a^3)(mu-1)/(2mu+1)."""
    mu, a, m = 2.6, 1.0, 1.0
    C1, C2 = cavity_C1C2(mu)
    assert _approx(C1, (mu - 1) / (2 * mu + 1)) and _approx(C2, 3 * mu / (2 * mu + 1))
    assert _approx(1 + C1, C2, rel=1e-14)                    # B_r continuity
    assert _approx(1 - 2 * C1, C2 / mu, rel=1e-14)           # H_theta continuity
    for th in (0.4, 1.2, 2.5):
        xs = a * np.array([np.sin(th), 0, np.cos(th)])
        Bi = cavity_fields(0.999999 * xs, m, a, mu)
        Bo = cavity_fields(1.000001 * xs, m, a, mu)
        rh = xs / a; tv = np.array([np.cos(th), 0, -np.sin(th)])
        assert _approx(Bi @ rh, Bo @ rh, rel=1e-4)           # B_n continuous
        assert _approx(Bi @ tv, (Bo @ tv) / mu, rel=1e-4)    # H_t continuous
    C1p, C2p = sphere_C1C2(mu)
    D1, D2 = cavity_C1C2(1 / mu)
    assert _approx(C1p, D1, rel=1e-14) and _approx(C2p, D2, rel=1e-14)
    assert _approx(1 + C1p, C2p, rel=1e-14)                  # B_r continuity
    assert _approx((1 - 2 * C1p) / mu, C2p, rel=1e-14)       # H_t continuity
    assert _approx(cavity_Kb_coefficient(m, a, mu),
                   3 * C * m / (4 * np.pi * a**3) * (mu - 1) / (2 * mu + 1))


# ------------------------------------------ P26 (6.11.1) permeable sphere in B0

def test_p26_permeable_sphere():
    """Ex. 6.11.1: Phi_m gives uniform B_in = 3 mu B0/(mu+2), external dipole
    (mu-1)/(mu+2) a^3 B0; BCs hold; M = (3/4pi)(mu-1)/(mu+2) B0."""
    mu, a, B0 = 3.5, 1.0, 1.2
    Bi = perm_sphere_B([0.2, 0.1, 0.3], a, mu, B0)
    assert _approx(Bi, [0, 0, 3 * mu * B0 / (mu + 2)], rel=1e-6, abs_=1e-8)
    x = np.array([0.9, 0.4, 1.3])
    mind = (mu - 1) / (mu + 2) * a**3 * B0
    assert _approx(perm_sphere_B(x, a, mu, B0),
                   np.array([0, 0, B0]) + dipole_B(x, [0, 0, mind]),
                   rel=1e-6, abs_=1e-8)
    for th in (0.5, 1.1, 2.2):
        xs = a * np.array([np.sin(th), 0, np.cos(th)])
        Bi = perm_sphere_B(0.99999 * xs, a, mu, B0)
        Bo = perm_sphere_B(1.00001 * xs, a, mu, B0)
        rh = xs / a; tv = np.array([np.cos(th), 0, -np.sin(th)])
        assert _approx(Bi @ rh, Bo @ rh, rel=1e-4)
        assert _approx((Bi @ tv) / mu, Bo @ tv, rel=1e-4, abs_=1e-8)
    assert _approx(perm_sphere_M(mu, B0), 3 / (4 * np.pi) * (mu - 1) / (mu + 2) * B0)
    # Phi_m continuity at r=a
    for th in (0.7, 1.9):
        xs = a * np.array([np.sin(th), 0, np.cos(th)])
        assert _approx(perm_sphere_phim(0.999999 * xs, a, mu, B0),
                       perm_sphere_phim(1.000001 * xs, a, mu, B0), rel=1e-4)


# ------------------------------------- P27/P28 (6.12.1-2) plane-interface images

def test_p27_image_source_in_vacuum():
    """Ex. 6.12.1: J* = ((mu-1)/(mu+1))(J_par, -J_z) mirrored and J** =
    2mu/(mu+1) J satisfy both BCs at z = 0 for a tilted loop source."""
    mu = 3.0
    acoef, bcoef, ccoef = image_coeffs_vacuum_source(mu)
    assert _approx(acoef, (mu - 1) / (mu + 1)) and _approx(bcoef, -acoef)
    assert _approx(ccoef, 2 * mu / (mu + 1))
    center, nhat, aloop = np.array([0.2, -0.1, 0.8]), np.array([0.3, 0.4, 0.87]), 0.5
    for xy in [(0.4, 0.3), (-0.6, 0.9), (1.2, -0.5)]:
        dBz, dHt = interface_BC_residual_vacuum_source(mu, center, nhat, aloop, xy)
        Bmag = np.linalg.norm(loop_B_3d(np.array([xy[0], xy[1], 0.0]), center, nhat, aloop, 1.0))
        assert abs(dBz) < 1e-10 * Bmag and dHt < 1e-10 * Bmag
    # image force on a parallel loop: attraction for mu > 1, repulsion mu < 1
    assert loop_image_force(0.5, 1.0, 3.0, 1.0) < 0
    assert loop_image_force(0.5, 1.0, 0.3, 1.0) > 0


def test_p28_image_source_embedded():
    """Ex. 6.12.2: source in the medium: a' = -(mu-1)/(mu+1), c' = 2mu/(mu+1)
    (medium-kernel fields on the source side) satisfy the BCs."""
    mu = 2.2
    acoef, bcoef, ccoef = image_coeffs_embedded_source(mu)
    assert _approx(acoef, -(mu - 1) / (mu + 1)) and _approx(bcoef, -acoef)
    assert _approx(ccoef, 2 * mu / (mu + 1))
    center, nhat, aloop = np.array([-0.3, 0.2, 0.7]), np.array([0.48, -0.6, 0.64]), 0.45
    for xy in [(0.5, 0.2), (-0.8, -0.4)]:
        dBz, dHt = interface_BC_residual_embedded_source(mu, center, nhat, aloop, xy)
        Bmag = np.linalg.norm(loop_B_3d(np.array([xy[0], xy[1], 0.0]), center, nhat, aloop, 1.0))
        assert abs(dBz) < 1e-10 * Bmag and dHt < 1e-10 * Bmag


# ------------------------------- P29/P30 (6.12.3-4) solid-angle and Green forms

def test_p29_solid_angle_representation():
    """Ex. 6.12.3: B = (I/c)[grad Om_src + lam grad Om_img] (z>0) and
    (I/c)(2mu/(1+mu)) grad Om_src (z<0) equal the image-current fields."""
    mu, aloop, d, I = 3.0, 0.7, 0.9, 1.0
    lam = (mu - 1) / (mu + 1)
    x = np.array([0.35, 0.15, 0.75])
    Bdir = (loop_B_3d(x, [0, 0, d], [0, 0, 1], aloop, I)
            + loop_B_3d(x, [0, 0, -d], [0, 0, 1], aloop, lam * I))
    assert _approx(solid_angle_B(x, aloop, d, I, coef_img=lam), Bdir,
                   rel=2e-4, abs_=1e-6)
    x2 = np.array([0.25, -0.2, -0.55])
    Bdir2 = loop_B_3d(x2, [0, 0, d], [0, 0, 1], aloop, 2 * mu / (mu + 1) * I)
    assert _approx(2 * mu / (mu + 1) * solid_angle_B(x2, aloop, d, I, coef_img=0.0),
                   Bdir2, rel=2e-4, abs_=1e-6)


def test_p30_green_function_representation():
    """Ex. 6.12.4: Phi_m = (I/c) Int_S' da' dG/dn' gives H = -grad Phi_m with
    H = B in vacuum (z>0) and H = B/mu in the medium (z<0)."""
    mu, aloop, d, I = 3.0, 0.7, 0.9, 1.0
    lam = (mu - 1) / (mu + 1)
    x = np.array([0.4, 0.2, 0.8])
    H = -grad_fd(lambda y: greens_phim(y, aloop, d, mu), x, h=2e-4)
    Bdir = (loop_B_3d(x, [0, 0, d], [0, 0, 1], aloop, I)
            + loop_B_3d(x, [0, 0, -d], [0, 0, 1], aloop, lam * I))
    assert _approx(H, Bdir, rel=2e-4, abs_=1e-6)
    x2 = np.array([0.3, -0.1, -0.6])
    H2 = -grad_fd(lambda y: greens_phim(y, aloop, d, mu), x2, h=2e-4)
    B2 = loop_B_3d(x2, [0, 0, d], [0, 0, 1], aloop, 2 * mu / (mu + 1) * I)
    assert _approx(mu * H2, B2, rel=2e-4, abs_=1e-6)   # B = mu H in the medium


# ------------------------------------ P31 (6.12.5) superconducting-sphere image

def test_p31_conducting_sphere_image():
    """Ex. 6.12.5: J* = -(a/r)^5 J(a^2/r) -- for a coaxial ring at (r0, th0)
    the image ring at (a^2/r0, th0) with I* = -(r0/a) I kills B.n on r = a."""
    asph, r0, th0, I = 1.0, 1.8, 0.7, 1.0
    rst, thst, Ist = sphere_image_ring(r0, th0, asph, I)
    assert _approx(rst, asph**2 / r0) and _approx(Ist, -(r0 / asph) * I)
    c1 = np.array([0, 0, r0 * np.cos(th0)]); a1 = r0 * np.sin(th0)
    c2 = np.array([0, 0, rst * np.cos(thst)]); a2 = rst * np.sin(thst)
    for th in (0.3, 0.9, 1.6, 2.4):
        for ph in (0.0, 1.1):
            n = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
            x = asph * n
            B = (loop_B_3d(x, c1, [0, 0, 1], a1, I, N=512)
                 + loop_B_3d(x, c2, [0, 0, 1], a2, Ist, N=512))
            Bscale = np.linalg.norm(loop_B_3d(x, c1, [0, 0, 1], a1, I, N=512))
            assert abs(B @ n) < 1e-6 * Bscale


# ---------------------------------------- P32 (6.12.6) dipole-slab force

def test_p32_dipole_slab_force():
    """Ex. 6.12.6: F_z = -3 m^2 (1+cos^2 th)(mu-1)/((mu+1) 16 d^4): attractive
    for mu > 1, repulsive for mu < 1, phi-independent -- vs image-loop
    quadrature."""
    m, d = 1.0, 1.0
    for (mu, th) in [(3.0, 0.0), (3.0, 1.0), (5.0, np.pi / 2)]:
        Fc = dipole_slab_force(m, d, mu, th)
        Fq = dipole_slab_force_quad(m, d, mu, th, phi=0.4)
        assert _approx(Fq[2], Fc, rel=2e-4, abs_=1e-9)
        assert np.max(np.abs(Fq[:2])) < 2e-5 * abs(Fc)
    assert dipole_slab_force(m, d, 3.0, 0.7) < 0 < dipole_slab_force(m, d, 0.4, 0.7)
    assert _approx(dipole_slab_force_quad(m, d, 3.0, 0.9, phi=0.0)[2],
                   dipole_slab_force_quad(m, d, 3.0, 0.9, phi=1.3)[2], rel=1e-6)


# ---------------------------------- P33 (6.13.1) magnetization vector potential

def test_p33_magnetization_potential_split():
    """Ex. 6.13.1: Int M x (x-x')/g^3 = Int (grad' x M)/g - oint (n' x M)/g:
    checked for a smooth compact M (surface term zero) and for the uniformly
    magnetized sphere (volume term zero), where A matches the closed form."""
    w = 0.2      # tight Gaussian: tails at the box face ~ e^-15, so the
                 # dropped surface term really is negligible

    def Mfun(xp):
        xp = np.atleast_2d(np.asarray(xp, float))
        g = np.exp(-np.einsum('ni,ni->n', xp, xp) / (2 * w * w))
        V = np.stack([0.2 + xp[:, 1], -xp[:, 0] * xp[:, 2],
                      0.5 * np.ones(len(xp))], axis=-1)
        return g[:, None] * V

    def curlM(xp):      # curl(gV) = g[curl V - (x/w^2) x V], curl V = (x,0,-z-1)
        xp = np.atleast_2d(np.asarray(xp, float))
        g = np.exp(-np.einsum('ni,ni->n', xp, xp) / (2 * w * w))
        V = np.stack([0.2 + xp[:, 1], -xp[:, 0] * xp[:, 2],
                      0.5 * np.ones(len(xp))], axis=-1)
        cV = np.stack([xp[:, 0], np.zeros(len(xp)), -xp[:, 2] - 1.0], axis=-1)
        return g[:, None] * (cV - np.cross(xp, V) / (w * w))

    for x in ([1.6, 0.4, 0.9], [0.8, -1.1, 1.3]):
        assert _approx(A_direct_dipole_sum(x, Mfun, L=1.1, n=40),
                       A_curl_plus_surface(x, Mfun, L=1.1, n=40, curlM=curlM),
                       rel=1e-5, abs_=3e-7)
    a, M0 = 1.0, 0.9
    for x in ([0.5, 0.2, 0.3], [1.3, -0.4, 0.8]):
        assert _approx(A_magnetization_surface(np.asarray(x), a, M0, n=200),
                       A_magnetized_sphere(np.asarray(x), a, M0),
                       rel=1e-5, abs_=1e-8)
    # B = curl A: uniform (8 pi/3) M inside, dipole m = 4 pi a^3 M/3 outside
    Af = lambda y: A_magnetized_sphere(y, a, M0)
    assert _approx(curl_fd(Af, [0.25, 0.1, 0.2], h=1e-5),
                   [0, 0, 8 * np.pi * M0 / 3], rel=1e-7)
    xo = np.array([0.9, 0.3, 1.1])
    mm = 4 * np.pi * a**3 * M0 / 3
    assert _approx(curl_fd(Af, xo, h=1e-5), dipole_B(xo, [0, 0, mm]), rel=1e-6)


# --------------------------------------------- P34 (6.13.2) split-sphere magnet

def test_p34_split_sphere():
    """Ex. 6.13.2: exterior Phi_m = 4 pi M0 a^2 sum C_n (a^2n/r^2n+1) P_2n
    with C_n = (-1)^(n+1) 2n (2n-3)!!/(2n+2)!! (shell |cos| charge plus the
    -2 M0 equatorial disk) -- vs direct quadrature; corrected interior form;
    far field is the pure P_2 term."""
    a, M0 = 1.0, 1.0
    assert split_sphere_Cn(0) == 0.0
    assert _approx(split_sphere_Cn(1), 0.25, rel=1e-14)
    assert _approx(split_sphere_Cn(2), -1.0 / 12.0, rel=1e-14)  # -4*1!!/6!! = -4/48
    for (r, th) in [(1.8, 0.6), (2.5, 1.2), (1.3, 2.3)]:
        assert _approx(split_sphere_phim_exterior(r, th, a, M0),
                       split_sphere_phim_quad(r, th, a, M0), rel=1e-8, abs_=1e-10)
    for (r, th) in [(0.45, 0.7), (0.8, 2.0), (0.3, 1.4)]:
        assert _approx(split_sphere_phim_interior(r, th, a, M0),
                       split_sphere_phim_quad(r, th, a, M0), rel=2e-3, abs_=2e-3)
    # Phi_m(0) = -2 pi M0 a (shell 2 pi M0 a, disk -4 pi M0 a): the book's
    # shell-form interior branch (which would give 0 there) misses the disk
    # source; Phi_m has an O(r) slope at the centre, hence the small r probe
    assert _approx(split_sphere_phim_interior(1e-8, 0.3, a, M0),
                   -2 * np.pi * M0 * a, rel=1e-7)
    for r in (6.0, 12.0):
        lead = 4 * np.pi * M0 * a**4 * 0.25 / r**3   # = pi M0 a^4 P2/r^3
        x = np.cos(0.5)
        P2 = 0.5 * (3 * x * x - 1)
        assert _approx(split_sphere_phim_exterior(r, 0.5, a, M0), lead * P2,
                       rel=3e-2 * (a / r) ** 2 / 0.1)


# ------------------------------------------ P35 (6.13.3) bar-magnet monopoles

def test_p35_bar_magnet_monopoles():
    """Ex. 6.13.3: far from an end, H = M0 S (x - x'')/|x - x''|^3 -- the rod
    is two magnetic monopoles +-M0 pi R^2 at its faces."""
    R, L, M0 = 0.2, 6.0, 1.5
    for x in ([1.5, 0.0, 3.6], [0.8, 0.9, -4.2], [0.0, 2.5, 3.4]):
        He = bar_H_exact(np.asarray(x, float), R, L, M0)
        Hm = bar_H_monopoles(np.asarray(x, float), R, L, M0)
        # normwise O(R^2/s^2) residual
        assert np.max(np.abs(He - Hm)) < 1e-2 * np.max(np.abs(Hm))
    # the residual is the finite-disk correction: it dies ~ 1/s^2 as the
    # field point recedes from the face along a fixed direction
    def relerr(scale):
        x = np.array([0.0, 0.0, L / 2]) + scale * np.array([0.5, 0.2, 0.8])
        He = bar_H_exact(x, R, L, M0)
        Hm = bar_H_monopoles(x, R, L, M0)
        return np.max(np.abs(He - Hm)) / np.max(np.abs(Hm))
    e1, e2 = relerr(1.0), relerr(2.0)
    assert e2 < e1 / 3.0
    # single-pole 1/s^2 falloff near one face, along the axis outside
    q = M0 * np.pi * R**2
    for s in (2.0, 4.0):
        Hz = bar_H_monopoles(np.array([0, 0, L / 2 + s]), R, L, M0)[2]
        assert _approx(Hz, q / s**2 - q / (s + L) ** 2, rel=1e-12)


# ----------------------------------------------- P36 (6.13.4) Hz = -M0 Omega

def test_p36_cube_solid_angle():
    """Ex. 6.13.4: Hz = -M0 [Omega_top - Omega_bot]; at the center of a cube
    each face subtends 2pi/3, so Hz = -4 pi M0/3 and Bz = +8 pi M0/3."""
    b, M0 = 1.0, 1.2
    assert _approx(solid_angle_square_center(b), 2 * np.pi / 3, rel=1e-12)
    assert _approx(solid_angle_rect([0, 0, 0], b / 2, b / 2, z0=b / 2),
                   2 * np.pi / 3, rel=1e-12)
    for x in ([0.1, 0.05, 0.2], [0.3, -0.2, 0.1], [0.2, 0.1, 0.8], [1.2, 0.4, 0.3]):
        assert _approx(cube_Hz(np.asarray(x), b, M0),
                       cube_Hz_direct(np.asarray(x), b, M0), rel=1e-4, abs_=1e-6)
        Om = (solid_angle_rect(x, b / 2, b / 2, z0=b / 2)
              - solid_angle_rect(x, b / 2, b / 2, z0=-b / 2))
        assert _approx(cube_Hz_direct(np.asarray(x), b, M0), -M0 * Om,
                       rel=1e-6, abs_=1e-8)
    Hc = cube_Hz_direct(np.array([0.0, 0.0, 0.0]), b, M0)
    assert _approx(Hc, -4 * np.pi * M0 / 3, rel=1e-8)
    assert _approx(Hc + 4 * np.pi * M0, 8 * np.pi * M0 / 3, rel=1e-8)


# ------------------------------------------------ P37 (6.13.5) rod magnet

def test_p37_rod_magnet_bessel():
    """Ex. 6.13.5: H_rho, H_z Bessel integrals (|z| < d/2) vs the two-disk
    charge picture; harmonization with the Ex. 6.6.1 solenoid via
    K_eff = c M x n (nI <-> c M0): B_sol = H_rod + 4 pi M0 zhat inside."""
    a, d, M0 = 1.0, 3.0, 0.8
    for (rho, z) in [(0.4, 0.6), (0.9, -0.8), (1.5, 0.4)]:
        hr, hz = rod_H_bessel(rho, z, a, d, M0)
        hr_q, hz_q = rod_H_disks(rho, z, a, d, M0)
        assert _approx(hr, hr_q, rel=2e-4, abs_=1e-6)
        assert _approx(hz, hz_q, rel=2e-4, abs_=1e-6)
    nI = C * M0            # equivalent solenoid surface current
    for (rho, z) in [(0.5, 0.7), (1.3, -0.5)]:
        br, bz = solenoid_B_inside_bessel(rho, z, a, d, nI / C)   # nI in units of c
        hr, hz = rod_H_bessel(rho, z, a, d, M0)
        assert _approx(br, hr, rel=2e-6, abs_=1e-8)
        step = 4 * np.pi * M0 * (1.0 if rho < a else 0.0)
        assert _approx(bz, hz + step, rel=2e-6, abs_=1e-8)


# --------------------------------------- P38 (6.13.6) shell with normal MA

def test_p38_closed_shell_normal_magnetization():
    """Ex. 6.13.6: Phi_m = -MA Omega_closed = -4 pi MA inside, 0 outside,
    for a sphere and for a cube."""
    MA = 1.3
    for x in ([0.2, 0.1, 0.3], [0.0, 0.0, -0.5]):
        assert _approx(closed_shell_phim_sphere(np.asarray(x), 1.0, MA),
                       -4 * np.pi * MA, rel=1e-8)
    for x in ([1.5, 0.2, 0.1], [0.4, 1.2, -0.9]):
        assert abs(closed_shell_phim_sphere(np.asarray(x), 1.0, MA)) < 1e-8
    assert _approx(closed_shell_phim_cube(np.array([0.1, -0.15, 0.2]), 1.0, MA),
                   -4 * np.pi * MA, rel=1e-6)
    assert abs(closed_shell_phim_cube(np.array([1.1, 0.3, 0.2]), 1.0, MA)) < 1e-6


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
