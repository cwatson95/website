"""MACRO_EM-06 -- Magnetostatics (Wilcox & Thron 2e, Ch. 6): code library.

Backs every exercise of Sec. 6.15 (P1-P38 in problems/problems.md).

GAUSSIAN units throughout, with the numerical convention c = 1 (module
constant C below), so e.g. the Biot-Savart law reads B = (I/C) dl x r/r^3
(Eq. 6.7) and the dipole moment of a loop is m = I S / C (Eq. 6.134).

Contents (by chapter section):
  helpers   : gauss_legendre, finite-difference div/curl/grad, loop fields
              (elliptic-integral, Bessel-integral, 3-D polygon quadrature)
  Sec. 6.1-6.4 : partially-immersed circuit force, wire pinch pressure,
              spinning+sliding cylinder, current sheet
  Sec. 6.5  : Stokes-transform identity, solid angles (disk axis/off-axis,
              rectangle, closed surfaces)
  Sec. 6.6  : solenoid / spinning disk / spinning cylinder Bessel forms,
              I1*K1 vector potential, spinning cone
  Sec. 6.7  : disk solid-angle Legendre series, loop Br/Btheta series,
              rotating shells and solid sphere
  Sec. 6.8  : magnetic moments (directed area), point dipole delta-field,
              magnetic quadrupole tensor and fields
  Sec. 6.9  : forces/torques on dipoles (wire+dipole, loop quadrature)
  Sec. 6.10 : surface-current torque, dipole in cavity / in permeable sphere
  Sec. 6.11 : permeable sphere in uniform field
  Sec. 6.12 : image currents at plane interfaces (both embeddings), solid
              angle / Green-function representations, conducting-sphere image
  Sec. 6.13 : magnetization vector potential, split-sphere magnet, bar
              magnets (monopole ends, Bessel forms), closed shell
"""
import numpy as np
from functools import lru_cache
from scipy import integrate, special

C = 1.0  # speed of light in the chosen units (keep formulas' 1/c explicit)

TWO_PI = 2.0 * np.pi
FOUR_PI = 4.0 * np.pi


# ============================================================ small helpers

@lru_cache(maxsize=None)
def _leggauss(n):
    return np.polynomial.legendre.leggauss(n)


def gauss_legendre(n, a, b):
    x, w = _leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def dfact(n):
    """Double factorial with (-1)!! = 0!! = 1."""
    if n <= 0:
        return 1.0
    out = 1.0
    while n > 0:
        out *= n
        n -= 2
    return out


def grad_fd(f, x, h=1e-5):
    x = np.asarray(x, float)
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3); e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def div_fd(F, x, h=1e-5):
    x = np.asarray(x, float)
    s = 0.0
    for i in range(3):
        e = np.zeros(3); e[i] = h
        s += (F(x + e)[i] - F(x - e)[i]) / (2 * h)
    return s


def curl_fd(F, x, h=1e-5):
    x = np.asarray(x, float)
    J = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3); e[j] = h
        J[:, j] = (F(x + e) - F(x - e)) / (2 * h)
    return np.array([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])


# ==================================================== circular loop fields
# Loop of radius a in the z=0 plane, centered on the z axis, current I
# circulating along +e_phi (moment +z).

def loop_Bz_axis(z, a, I):
    """Eq. (6.62): on-axis field of a circular loop."""
    return TWO_PI * I * a**2 / (C * (a**2 + z**2) ** 1.5)


def loop_B_elliptic(rho, z, a, I):
    """(B_rho, B_z) of the loop via complete elliptic integrals.

    Standard closed form (Gaussian units); equals the Bessel forms
    (6.83)-(6.84) and the series (6.119)/(6.121)."""
    rho = float(rho); z = float(z)
    if rho < 1e-14:
        return 0.0, loop_Bz_axis(z, a, I)
    d1 = (a + rho) ** 2 + z**2
    d2 = (a - rho) ** 2 + z**2
    m = 4 * a * rho / d1
    K, E = special.ellipk(m), special.ellipe(m)
    Bz = (2 * I / C) / np.sqrt(d1) * (K + E * (a**2 - rho**2 - z**2) / d2)
    Brho = (2 * I / C) * z / (rho * np.sqrt(d1)) * (-K + E * (a**2 + rho**2 + z**2) / d2)
    return Brho, Bz


def loop_B_bessel(rho, z, a, I, kmax=None, n=400):
    """Eqs. (6.83)-(6.84): B_rho, B_z as Bessel k-integrals (z != 0)."""
    az = abs(z)
    if kmax is None:
        kmax = 60.0 / max(az, 1e-3)
    k, w = gauss_legendre(n, 0.0, kmax)
    e = np.exp(-k * az)
    Brho = TWO_PI * a * I / C * np.sign(z) * np.sum(w * k * special.j1(k * a) * special.j1(k * rho) * e)
    Bz = TWO_PI * a * I / C * np.sum(w * k * special.j1(k * a) * special.j0(k * rho) * e)
    return Brho, Bz


def loop_A_bessel(rho, z, a, I, n=400):
    """Eq. (6.227): A_phi = (2 pi I a/c) Int dk e^{-k|z|} J1(ka) J1(k rho)."""
    az = max(abs(z), 1e-3)
    k, w = gauss_legendre(n, 0.0, 60.0 / az)
    return TWO_PI * I * a / C * np.sum(w * np.exp(-k * abs(z)) * special.j1(k * a) * special.j1(k * rho))


def loop_A_IK(rho, z, a, I, n=600):
    """Exercise 6.6.4: A_phi = (4 I a/c) Int dk cos(kz) I1(k rho_<) K1(k rho_>)."""
    rl, rg = min(rho, a), max(rho, a)
    kmax = 40.0 / max(rg - rl, 0.05 * a)
    k, w = gauss_legendre(n, 1e-9, kmax)
    return 4 * I * a / C * np.sum(w * np.cos(k * z) * special.i1(k * rl) * special.k1(k * rg))


def loop_B_3d(x, center, nhat, a, I, N=256):
    """Biot-Savart polygon quadrature for a circular loop anywhere (Eq. 6.7)."""
    x = np.asarray(x, float); center = np.asarray(center, float)
    nhat = np.asarray(nhat, float) / np.linalg.norm(nhat)
    t = np.array([1.0, 0, 0]) if abs(nhat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(nhat, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    ph = (np.arange(N) + 0.5) * TWO_PI / N
    pts = center + a * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
    dl = a * (TWO_PI / N) * (-np.sin(ph)[:, None] * e1 + np.cos(ph)[:, None] * e2)
    r = x - pts
    return I / C * np.sum(np.cross(dl, r) / np.linalg.norm(r, axis=1)[:, None] ** 3, axis=0)


def loop_A_3d(x, center, nhat, a, I, N=512):
    """A = (I/c) closed-int dl'/|x-x'|  (Eq. 6.42 for a line current)."""
    x = np.asarray(x, float); center = np.asarray(center, float)
    nhat = np.asarray(nhat, float) / np.linalg.norm(nhat)
    t = np.array([1.0, 0, 0]) if abs(nhat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(nhat, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    ph = (np.arange(N) + 0.5) * TWO_PI / N
    pts = center + a * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
    dl = a * (TWO_PI / N) * (-np.sin(ph)[:, None] * e1 + np.cos(ph)[:, None] * e2)
    return I / C * np.sum(dl / np.linalg.norm(x - pts, axis=1)[:, None], axis=0)


def dipole_B(x, m):
    """Point-dipole field away from the origin: (3 x (m.x) - r^2 m)/r^5 (6.152)."""
    x = np.asarray(x, float); m = np.asarray(m, float)
    r2 = x @ x
    return (3 * x * (m @ x) - r2 * m) / r2**2.5


def loop_B_spherical(r, th, a, I):
    """(B_r, B_theta) of the loop from the elliptic closed form -- the
    benchmark for the series (6.119)/(6.121)."""
    rho, z = r * np.sin(th), r * np.cos(th)
    Brho, Bz = loop_B_elliptic(rho, z, a, I)
    Br = Brho * np.sin(th) + Bz * np.cos(th)
    Bth = Brho * np.cos(th) - Bz * np.sin(th)
    return Br, Bth


# ====================================== P1 (6.1.1): partially immersed loop

def circuit_force_partial(pts, Bvec, inside):
    """F = (I/c) sum dl x B over the part of a closed polyline inside the
    field region; current I=1.  pts: (N,3) closed polygon vertices;
    inside(midpoint)->bool ; Bvec constant vector in the region."""
    pts = np.asarray(pts, float)
    seg = np.roll(pts, -1, axis=0) - pts
    mid = pts + 0.5 * seg
    F = np.zeros(3)
    for s, mp in zip(seg, mid):
        if inside(mp):
            F += np.cross(s, Bvec) / C
    return F


def chord_force(entry, exit_, Bvec):
    """Closed form of Ex. 6.1.1: F = (I/c) L x B with L the chord vector from
    the entry point (current entering the field region) to the exit point --
    the net displacement of the immersed arc."""
    L = np.asarray(exit_, float) - np.asarray(entry, float)
    return np.cross(L, np.asarray(Bvec, float)) / C


# ============================ P2 (6.3.1): pinch pressure in a straight wire

def wire_B_phi(rho, a, I):
    """Ampere's law: B_phi = 2 I rho/(c a^2) inside, 2 I/(c rho) outside."""
    rho = np.asarray(rho, float)
    return np.where(rho <= a, 2 * I * rho / (C * a**2), 2 * I / (C * rho))


def pinch_pressure(rho, a, I):
    """P(rho) = (I^2/(pi c^2 a^2)) (1 - rho^2/a^2) inside, 0 outside (inward)."""
    rho = np.asarray(rho, float)
    return np.where(rho <= a, I**2 / (np.pi * C**2 * a**2) * (1 - rho**2 / a**2), 0.0)


def pinch_pressure_quad(rho, a, I, n=400):
    """Integrate dP/drho = -J B_phi / c from rho to a (P(a)=0)."""
    if rho >= a:
        return 0.0
    J = I / (np.pi * a**2)
    r, w = gauss_legendre(n, rho, a)
    return np.sum(w * J * wire_B_phi(r, a, I) / C)


# ==================== P3 (6.3.2): spinning + sliding charged hollow cylinder

def spinning_cylinder_B(rho, R, sigma, omega, v0):
    """Closed form: inside B = (4 pi sigma omega R/c) zhat; outside
    B = (4 pi sigma R v0/(c rho)) e_phi.  Returns (B_phi, B_z)."""
    if rho < R:
        return 0.0, FOUR_PI * sigma * omega * R / C
    return FOUR_PI * sigma * R * v0 / (C * rho), 0.0


def spinning_cylinder_B_quad(rho, R, sigma, omega, v0, L=400.0, nz=400, nw=240):
    """Direct Biot-Savart check at mid-height z=0, point (rho,0,0):
    azimuthal sheet = stack of loops (elliptic closed form) on a sinh-graded
    grid out to |z| = L; axial sheet = nw straight (finite, long) wires
    around the circumference."""
    # loops, K_phi = sigma*omega*R, loop current per height dz
    umax = np.arcsinh(L)
    u, wu = gauss_legendre(nz, -umax, umax)
    z0, wz = np.sinh(u), np.cosh(u) * wu
    Bz = 0.0
    for zz, ww in zip(z0, wz):
        _, bz = loop_B_elliptic(rho, -zz, R, sigma * omega * R * ww)
        Bz += bz
    # axial wires, each carries I_w = sigma*v0*R*dphi ; finite-length formula
    Bphi = 0.0
    ph = (np.arange(nw) + 0.5) * TWO_PI / nw
    dph = TWO_PI / nw
    for p in ph:
        wx, wy = R * np.cos(p), R * np.sin(p)
        dx, dy = rho - wx, -wy
        d = np.hypot(dx, dy)
        Iw = sigma * v0 * R * dph
        # B of finite wire along z, |z|<L, at perpendicular distance d, z=0
        Bmag = (2 * Iw / (C * d)) * (L / np.sqrt(L**2 + d**2))
        # direction zhat x dvec / d
        Bphi_vec = np.array([-dy, dx]) / d * Bmag
        # e_phi at field point (rho,0,0) is +yhat
        Bphi += Bphi_vec[1]
    return Bphi, Bz


# ================================= P4 (6.4.1): infinite sheet K = K0 zhat

def sheet_B(x, K0):
    """Sheet in the y-z plane (x=0), K = K0 zhat: B = +-(2 pi K0/c) yhat."""
    return np.array([0.0, TWO_PI * K0 / C * np.sign(x), 0.0])


def sheet_B_wires(x, K0, Y=1e7, n=400):
    """Superpose infinite straight wires along z at (0, y'): B = sum 2 I/(c d)
    e_phi, on a sinh-graded grid out to |y| = Y (the integrand is a Lorentzian
    of width |x|, so grade the nodes toward y = 0)."""
    umax = np.arcsinh(Y)
    u, wu = gauss_legendre(n, -umax, umax)
    y, w = np.sinh(u), np.cosh(u) * wu
    d2 = x**2 + y**2
    # zhat x (x, -y)/d = (y, x)/d ; magnitude 2 K0 dy/(c d)
    Bx = np.sum(w * 2 * K0 / C * y / d2)
    By = np.sum(w * 2 * K0 / C * x / d2)
    return np.array([Bx, By, 0.0])


# ===================== P5 (6.5.1): Stokes transform  oint dl x A = int (ds x grad) x A

def stokes_transform_lhs(Afun, curve, N=2000):
    """oint dl x A around curve(t), t in [0,1)."""
    t = (np.arange(N) + 0.5) / N
    dt = 1.0 / N
    out = np.zeros(3)
    for ti in t:
        xp = (curve(ti + 1e-6) - curve(ti - 1e-6)) / 2e-6
        out += np.cross(xp, Afun(curve(ti))) * dt
    return out


def stokes_transform_rhs(Afun, surf, n=60):
    """int (ds x grad) x A = int [sum_i ds_i grad A_i - ds (div A)] over
    surf(u,v), (u,v) in [0,1]^2 (ds from the cross product of tangents)."""
    u, wu = gauss_legendre(n, 0.0, 1.0)
    v, wv = gauss_legendre(n, 0.0, 1.0)
    out = np.zeros(3)
    for ui, wui in zip(u, wu):
        for vi, wvi in zip(v, wv):
            h = 1e-6
            xu = (surf(ui + h, vi) - surf(ui - h, vi)) / (2 * h)
            xv = (surf(ui, vi + h) - surf(ui, vi - h)) / (2 * h)
            ds = np.cross(xu, xv) * wui * wvi
            x0 = surf(ui, vi)
            # grad A_i and div A by FD
            JA = np.zeros((3, 3))
            for j in range(3):
                e = np.zeros(3); e[j] = 1e-6
                JA[:, j] = (Afun(x0 + e) - Afun(x0 - e)) / 2e-6
            out += JA.T @ ds - ds * np.trace(JA)
    return out


# ================================================= solid angles (Secs. 6.5-6.7)

def solid_angle_disk_axis(z, a):
    """Eq. (6.60): Omega on the axis of a disk of radius a at z'=0,
    normal +zhat: Omega = 2 pi (z/sqrt(z^2+a^2) - sign z)."""
    return TWO_PI * (z / np.hypot(z, a) - np.sign(z))


def solid_angle_disk_bessel(rho, z, a, n=400):
    """Eq. (6.73): Omega = -2 pi a sign(z) Int dk J1(ka) J0(k rho) e^{-k|z|}."""
    az = max(abs(z), 1e-6)
    k, w = gauss_legendre(n, 0.0, 80.0 / max(az, 0.02))
    val = np.sum(w * special.j1(k * a) * special.j0(k * rho) * np.exp(-k * az))
    return -TWO_PI * a * np.sign(z) * val


def solid_angle_disk_quad(x, a, center=(0, 0, 0), nhat=(0, 0, 1), nr=120, nph=120):
    """Omega(x) = int da' n'.(x'-x)/|x-x'|^3 (book convention, Eq. 6.67)."""
    x = np.asarray(x, float)
    center = np.asarray(center, float)
    nhat = np.asarray(nhat, float) / np.linalg.norm(np.asarray(nhat, float))
    t = np.array([1.0, 0, 0]) if abs(nhat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(nhat, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    r, wr = gauss_legendre(nr, 0.0, a)
    ph, wp = gauss_legendre(nph, 0.0, TWO_PI)
    out = 0.0
    for ri, wri in zip(r, wr):
        pts = center + ri * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2)
        d = x - pts
        dn = np.linalg.norm(d, axis=1) ** 3
        out += ri * wri * np.sum(wp * (-(d @ nhat)) / dn)
    return out


def solid_angle_rect(x, hx, hy, z0=0.0):
    """Book-convention solid angle (6.67)-(6.68) of the rectangle |x'|<=hx,
    |y'|<=hy in the plane z'=z0, normal n' = +zhat, seen from x (closed
    arctan form).  Omega < 0 above the sheet (n'.(x'-x) < 0 there), > 0
    below; |Omega| -> 2 pi on approaching a point of the sheet."""
    X, Y, Z = float(x[0]), float(x[1]), float(x[2]) - z0
    if abs(Z) < 1e-14:
        return 0.0

    def f(x1, y1):
        return np.arctan(x1 * y1 / (Z * np.sqrt(x1**2 + y1**2 + Z**2)))

    return -(f(hx - X, hy - Y) + f(hx - X, hy + Y)
             + f(hx + X, hy - Y) + f(hx + X, hy + Y))


def solid_angle_square_center(b):
    """|Omega| of one face of a cube of side b from its center = 2 pi/3."""
    return 4 * np.arctan(1 / np.sqrt(3.0))


def solid_angle_sphere_quad(x, a, MA=1.0, nth=200, nph=200):
    """Phi_m of a closed spherical shell with outward area magnetization MA:
    Phi_m = MA * int da' n'.(x-x')/|x-x'|^3 = -MA * Omega_closed (P38)."""
    x = np.asarray(x, float)
    th, wt = gauss_legendre(nth, 0.0, np.pi)
    ph, wp = gauss_legendre(nph, 0.0, TWO_PI)
    out = 0.0
    for t, w1 in zip(th, wt):
        n = np.array([np.sin(t) * np.cos(ph), np.sin(t) * np.sin(ph), np.cos(t) * np.ones_like(ph)]).T
        pts = a * n
        d = x - pts
        dn = np.linalg.norm(d, axis=1) ** 3
        out += a**2 * np.sin(t) * w1 * np.sum(wp * np.einsum('ij,ij->i', n, d) / dn)
    return MA * out


def solid_angle_cube_quad(x, b, MA=1.0, n=80):
    """Same as above for the surface of a cube of side b centered at origin."""
    x = np.asarray(x, float)
    u, wu = gauss_legendre(n, -b / 2, b / 2)
    total = 0.0
    for axis in range(3):
        for s in (+1.0, -1.0):
            nvec = np.zeros(3); nvec[axis] = s
            for ui, wi in zip(u, wu):
                for vi, wj in zip(u, wu):
                    p = np.zeros(3)
                    p[axis] = s * b / 2
                    p[(axis + 1) % 3] = ui
                    p[(axis + 2) % 3] = vi
                    d = x - p
                    total += wi * wj * (nvec @ d) / np.linalg.norm(d) ** 3
    return MA * total


# ======================================= Sec. 6.6: solenoid / spinning things

def solenoid_B_inside_bessel(rho, z, a, d, nI, n=600):
    """Ex. 6.6.1: for |z| < d/2,
    B_rho = (4 pi a nI/c) Int dk J1(ka) J1(k rho) e^{-kd/2} sinh(kz)
    B_z   = (4 pi nI/c) H(a-rho) - (4 pi a nI/c) Int dk J1(ka) J0(k rho) e^{-kd/2} cosh(kz)."""
    k, w = gauss_legendre(n, 0.0, 120.0 / d)
    damp = np.exp(-k * d / 2)
    Brho = FOUR_PI * a * nI / C * np.sum(w * special.j1(k * a) * special.j1(k * rho) * damp * np.sinh(k * z))
    corr = FOUR_PI * a * nI / C * np.sum(w * special.j1(k * a) * special.j0(k * rho) * damp * np.cosh(k * z))
    Bz = FOUR_PI * nI / C * (1.0 if rho < a else 0.0) - corr
    return Brho, Bz


def solenoid_Bz_outside_bessel(rho, z, a, d, nI, n=600):
    """Ex. 6.8.1(a): |z| > d/2:
    B_z = (4 pi a nI/c) Int dk J1(ka) J0(k rho) e^{-k|z|} sinh(kd/2)."""
    az = abs(z)
    k, w = gauss_legendre(n, 0.0, 80.0 / (az - d / 2 + 0.1))
    return FOUR_PI * a * nI / C * np.sum(w * special.j1(k * a) * special.j0(k * rho) * np.exp(-k * az) * np.sinh(k * d / 2))


def solenoid_Bz_axis(z, a, d, nI):
    """Exact on-axis solenoid field (superposed loops, any z):
    B = (2 pi nI/c)[ (z+d/2)/sqrt(a^2+(z+d/2)^2) - (z-d/2)/sqrt(a^2+(z-d/2)^2) ]."""
    zp, zm = z + d / 2, z - d / 2
    return TWO_PI * nI / C * (zp / np.hypot(a, zp) - zm / np.hypot(a, zm))


def solenoid_corr_axis(a, d, nI, n=800):
    """Ex. 6.6.1(b): the correction term of Bz at the center (rho=0, z=0):
    (4 pi a nI/c) Int dk J1(ka) e^{-kd/2}."""
    k, w = gauss_legendre(n, 0.0, 400.0 / d)
    return FOUR_PI * a * nI / C * np.sum(w * special.j1(k * a) * np.exp(-k * d / 2))


def solenoid_corr_axis_asym(a, d, nI):
    """Ex. 6.6.1(b) asymptote for d >> a: J1(ka) ~ ka/2 gives
    (4 pi a nI/c)(a/2)(2/d)^2 = 8 pi a^2 nI/(c d^2) -- a 1/d^2 falloff."""
    return 8 * np.pi * a**2 * nI / (C * d**2)


def solenoid_B_loops(rho, z, a, d, nI, n=800):
    """Brute-force loop stack (elliptic closed form per loop)."""
    z0, w = gauss_legendre(n, -d / 2, d / 2)
    Brho = Bz = 0.0
    for zz, ww in zip(z0, w):
        br, bz = loop_B_elliptic(rho, z - zz, a, nI * ww)
        Brho += br; Bz += bz
    return Brho, Bz


def spinning_disk_B_bessel(rho, z, R, sigma, omega, n=600):
    """Ex. 6.6.2:
    B_rho = sign(z) (2 pi omega sigma R^2/c) Int dk e^{-k|z|} J2(kR) J1(k rho)
    B_z   =        (2 pi omega sigma R^2/c) Int dk e^{-k|z|} J2(kR) J0(k rho)."""
    az = abs(z)
    k, w = gauss_legendre(n, 0.0, 80.0 / max(az, 0.02))
    pref = TWO_PI * omega * sigma * R**2 / C
    e = np.exp(-k * az)
    Brho = np.sign(z) * pref * np.sum(w * e * special.jv(2, k * R) * special.j1(k * rho))
    Bz = pref * np.sum(w * e * special.jv(2, k * R) * special.j0(k * rho))
    return Brho, Bz


def spinning_disk_B_rings(rho, z, R, sigma, omega, n=800):
    """Ring superposition: annulus rho0 carries dI = sigma omega rho0 drho0.
    For field points close to the disk plane the integrand is near-singular at
    rho0 = rho, so the radial integral is split there."""
    edges = [0.0, R] if not (0.0 < rho < R) else [0.0, rho, R]
    Brho = Bz = 0.0
    for lo, hi in zip(edges, edges[1:]):
        r0, w = gauss_legendre(n, lo, hi)
        for rr, ww in zip(r0, w):
            br, bz = loop_B_elliptic(rho, z, rr, sigma * omega * rr * ww)
            Brho += br; Bz += bz
    return Brho, Bz


def spinning_disk_moment(R, sigma, omega):
    """m_z = pi sigma omega R^4/(4c)  (from B_z ~ pi sigma omega R^4/(2 c |z|^3) = 2m/|z|^3)."""
    return np.pi * sigma * omega * R**4 / (4 * C)


def spinning_cylinder_solid_Bz_bessel(rho, z, R, d, rho0, omega, n=800):
    """Ex. 6.6.3, |z| < d/2:
    B_z = (2 pi rho0 omega/c)(R^2-rho^2) H(R-rho)
          - (4 pi rho0 omega R^2/c) Int dk/k e^{-kd/2} cosh(kz) J2(kR) J0(k rho)."""
    k, w = gauss_legendre(n, 1e-9, 150.0 / d)
    corr = FOUR_PI * rho0 * omega * R**2 / C * np.sum(
        w / k * np.exp(-k * d / 2) * np.cosh(k * z) * special.jv(2, k * R) * special.j0(k * rho))
    main = TWO_PI * rho0 * omega / C * (R**2 - rho**2) * (1.0 if rho < R else 0.0)
    return main - corr


def spinning_cylinder_solid_Bz_disks(rho, z, R, d, rho0, omega, nz=200, nr=200):
    """Stack of spinning disks (each by ring superposition).  For interior
    field points the source disk through z0 = z is (log-)singular, so the
    z-integral is split there; Gauss nodes then cluster toward the split."""
    edges = [-d / 2, d / 2] if not (-d / 2 < z < d / 2) else [-d / 2, z, d / 2]
    tot = 0.0
    for lo, hi in zip(edges, edges[1:]):
        z0, wz = gauss_legendre(nz, lo, hi)
        for zz, ww in zip(z0, wz):
            _, bz = spinning_disk_B_rings(rho, z - zz, R, rho0 * ww, omega, n=nr)
            tot += bz
    return tot


def weber_schafheitlin(rho, R, n=200000, kmax=None):
    """Int_0^inf dk J2(kR) J0(k rho)/k = (R^2-rho^2)/(2R^2) for rho<R, else 0."""
    if kmax is None:
        kmax = 4000.0 / R
    k = np.linspace(1e-8, kmax, n)
    f = special.jv(2, k * R) * special.j0(k * rho) / k
    return np.trapezoid(f, k)


def cone_Bz_tip(alpha, L1, L2, sigma, omega):
    """Ex. 6.6.5: B_z(0) = (2 pi sigma omega/c)(L2-L1) sin^3(alpha)/cos(alpha)."""
    return TWO_PI * sigma * omega / C * (L2 - L1) * np.sin(alpha) ** 3 / np.cos(alpha)


def cone_Bz_tip_quad(alpha, L1, L2, sigma, omega, n=600):
    z0, w = gauss_legendre(n, L1, L2)
    tot = 0.0
    for zz, ww in zip(z0, w):
        a0 = zz * np.tan(alpha)
        dI = sigma * omega * a0 * ww / np.cos(alpha)
        tot += TWO_PI * dI * a0**2 / (C * (a0**2 + zz**2) ** 1.5)
    return tot


# ===================== Sec. 6.7: Legendre series for the disk solid angle etc.

def solid_angle_disk_series(r, th, a, N=120):
    """Ex. 6.7.1 series, r>=a and r<=a branches (book forms).  Coefficients
    built by the stable recursions (2n+1)!!/(2n+2)!! and (2n-1)!!/(2n)!!.
    NOTE: the interior branch carries the conditionally convergent constant
    part that resums to -2 pi sign(z) (see solid_angle_disk_series_split), so
    it converges only ~ 1/N; the split form converges geometrically."""
    x = np.cos(th)
    s = 0.0
    if r >= a:
        cn = 0.5                              # (2n+1)!!/(2n+2)!! at n=0
        for n in range(N):
            s += (-1) ** n * cn * (a / r) ** (2 * n + 2) * special.eval_legendre(2 * n + 1, x)
            cn *= (2 * n + 3) / (2 * n + 4)
        return -TWO_PI * s
    cn = 1.0                                  # (2n-1)!!/(2n)!! at n=0
    for n in range(N):
        s += (-1) ** n * cn * ((4 * n + 3) / (2 * n + 2) - (r / a) ** (2 * n + 1)) \
            * special.eval_legendre(2 * n + 1, x)
        cn *= (2 * n + 1) / (2 * n + 2)
    return -TWO_PI * s


def solid_angle_disk_series_split(r, th, a, N=120):
    """Ex. 6.7.1 sign-split interior form:
    Omega = -2 pi sign(z) + 2 pi sum (-1)^n ((2n-1)!!/(2n)!!) (r/a)^{2n+1} P_{2n+1}."""
    x = np.cos(th)
    s, cn = 0.0, 1.0
    for n in range(N):
        s += (-1) ** n * cn * (r / a) ** (2 * n + 1) * special.eval_legendre(2 * n + 1, x)
        cn *= (2 * n + 1) / (2 * n + 2)
    return -TWO_PI * np.sign(np.cos(th)) + TWO_PI * s


def loop_Br_series(r, th, a, I, N=100):
    """Eq. (6.119): B_r = (2 pi I a/(c r)) sum (-1)^n ((2n+1)!!/(2n)!!) r_<^{2n+1}/r_>^{2n+2} P_{2n+1}."""
    rl, rg = min(r, a), max(r, a)
    s, cn = 0.0, 1.0                          # (2n+1)!!/(2n)!! at n=0
    for n in range(N):
        s += (-1) ** n * cn * (rl / rg) ** (2 * n + 1) / rg \
            * special.eval_legendre(2 * n + 1, np.cos(th))
        cn *= (2 * n + 3) / (2 * n + 2)
    return TWO_PI * I * a / (C * r) * s


def loop_Bth_series(r, th, a, I, N=100):
    """Eq. (6.121) with P^1 in the Condon-Shortley convention (scipy lpmv)."""
    s, cn = 0.0, 1.0                          # (2n+1)!!/(2n)!! at n=0
    for n in range(N):
        coef = (-1) ** n * cn / (n + 1)
        P1 = special.lpmv(1, 2 * n + 1, np.cos(th))
        if r > a:
            rad = (a / r) ** (2 * n) / r**3
        else:
            rad = -(2 * n + 2) / (2 * n + 1) * (r / a) ** (2 * n) / a**3
        s += coef * P1 * rad
        cn *= (2 * n + 3) / (2 * n + 2)
    return -np.pi * I * a**2 / C * s


def rotating_shell_B(x, a, sigma, omega):
    """Ex. 6.7.3: uniform rotating shell.
    inside: (8 pi a sigma omega/(3c)) zhat; outside: dipole m = 4 pi sigma omega a^4/(3c)."""
    x = np.asarray(x, float)
    r = np.linalg.norm(x)
    m = FOUR_PI * sigma * omega * a**4 / (3 * C)
    if r < a:
        return np.array([0.0, 0.0, 8 * np.pi * a * sigma * omega / (3 * C)])
    return dipole_B(x, np.array([0.0, 0.0, m]))


def rotating_shell_B_quad(x, a, sigma, omega, n=1200):
    """Biot-Savart ring stack over the shell: K = sigma omega a sin th e_phi."""
    th, w = gauss_legendre(n, 0.0, np.pi)
    B = np.zeros(3)
    for t, ww in zip(th, w):
        dI = sigma * omega * a * np.sin(t) * a * ww
        B += loop_B_3d(x, np.array([0, 0, a * np.cos(t)]), np.array([0, 0, 1.0]), a * np.sin(t), dI, N=180)
    return B


def rotating_solid_sphere_B(x, a, rhoq, omega):
    """Ex. 6.7.4: outside pure dipole m=4 pi a^5 omega rhoq/(15 c); inside
    dipole with m(r) plus zhat (4 pi rhoq omega/(3c))(a^2-r^2)."""
    x = np.asarray(x, float)
    r = np.linalg.norm(x)
    if r >= a:
        m = FOUR_PI * a**5 * omega * rhoq / (15 * C)
        return dipole_B(x, np.array([0, 0, m]))
    mr = FOUR_PI * r**5 * omega * rhoq / (15 * C)
    return dipole_B(x, np.array([0, 0, mr])) + np.array(
        [0, 0, FOUR_PI * rhoq * omega / (3 * C) * (a**2 - r**2)])


def rotating_solid_sphere_B_quad(x, a, rhoq, omega, n=90):
    """Shell superposition of rotating_shell_B (exact per shell).  The
    integrand switches branch at shell radius = |x|, so integrate piecewise
    on [0, |x|] and [|x|, a] to keep Gauss-Legendre accuracy."""
    r = min(np.linalg.norm(np.asarray(x, float)), a)
    B = np.zeros(3)
    for (lo, hi) in ((0.0, r), (r, a)):
        if hi - lo < 1e-14:
            continue
        r0, w = gauss_legendre(n, lo, hi)
        for rr, ww in zip(r0, w):
            B += rotating_shell_B(x, rr, rhoq * ww, omega)
    return B


def costheta_shell_B(x, a, sigma0, omega):
    """Ex. 6.7.5 closed forms (pure interior linear field / exterior quadrupole)."""
    x = np.asarray(x, float)
    r2 = x @ x; r = np.sqrt(r2)
    if r < a:
        return FOUR_PI * sigma0 * omega / (5 * C) * np.array([-x[0], -x[1], 2 * x[2]])
    pref = FOUR_PI * sigma0 * a**5 * omega / (5 * C * r**7)
    return pref * np.array([x[0] * (5 * x[2] ** 2 - r2),
                            x[1] * (5 * x[2] ** 2 - r2),
                            -x[2] * (5 * (x[0] ** 2 + x[1] ** 2) - 2 * r2)])


def costheta_shell_B_quad(x, a, sigma0, omega, n=1200):
    th, w = gauss_legendre(n, 0.0, np.pi)
    B = np.zeros(3)
    for t, ww in zip(th, w):
        dI = omega * a * sigma0 * np.cos(t) * np.sin(t) * a * ww
        B += loop_B_3d(x, np.array([0, 0, a * np.cos(t)]), np.array([0, 0, 1.0]), a * np.sin(t), dI, N=180)
    return B


# ============================= Sec. 6.8: moments, dipole delta, quadrupoles

def circuit_moment(pts):
    """m = (1/(2c)) oint x x dl for a closed polyline with unit current."""
    pts = np.asarray(pts, float)
    seg = np.roll(pts, -1, axis=0) - pts
    mid = pts + 0.5 * seg
    return np.sum(np.cross(mid, seg), axis=0) / (2 * C)


def saddle_circuit(R, L, N=4000):
    """Fig. 6.30(a) circuit (P18): semicircle (radius R) in the y-z plane at
    x=0 from the origin to (0,2R,0) bulging +z; straight leg to (-L,2R,0);
    semicircle at x=-L bulging -z back to (-L,0,0); straight leg to origin."""
    n1 = N // 4
    ph = np.linspace(0, np.pi, n1, endpoint=False)
    c1 = np.stack([np.zeros_like(ph), R - R * np.cos(ph), R * np.sin(ph)], axis=1)
    t = np.linspace(0, L, n1, endpoint=False)
    w2 = np.stack([-t, 2 * R * np.ones_like(t), np.zeros_like(t)], axis=1)
    ps = np.linspace(0, np.pi, n1, endpoint=False)
    c2 = np.stack([-L * np.ones_like(ps), R + R * np.cos(ps), -R * np.sin(ps)], axis=1)
    w1 = np.stack([-L + t, np.zeros_like(t), np.zeros_like(t)], axis=1)
    return np.vstack([c1, w2, c2, w1])


def saddle_moment(R, L, I=1.0):
    """P18(a) closed form: m = (I/c)(-pi R^2 xhat + 2 R L zhat)."""
    return I / C * np.array([-np.pi * R**2, 0.0, 2 * R * L])


def bent_loop_circuit(R, N=4000):
    """Fig. 6.30(b): circle of radius R bent 90 deg along the x axis: the
    y>0 half stays in the x-y plane, the y<0 half is folded up to +z."""
    ph = np.linspace(0, TWO_PI, N, endpoint=False)
    pts = np.zeros((N, 3))
    up = ph <= np.pi
    pts[up] = np.stack([R * np.cos(ph[up]), R * np.sin(ph[up]), np.zeros(up.sum())], axis=1)
    pts[~up] = np.stack([R * np.cos(ph[~up]), np.zeros((~up).sum()), -R * np.sin(ph[~up])], axis=1)
    return pts


def bent_loop_moment(R, I=1.0):
    """P18(b): m = (I pi R^2/(2c)) (yhat + zhat), |m| = pi I R^2/(sqrt2 c) --
    each half contributes a half-disk area, normals zhat and yhat for the
    fold direction of bent_loop_circuit (y<0 half rotated up about the
    x axis).  The opposite fold flips the yhat sign; |m| is unchanged."""
    return I * np.pi * R**2 / (2 * C) * np.array([0.0, 1.0, 1.0])


def gradgrad_1r_box(i, j, a=0.35, n=80):
    """Int over the cube (2a)^3 of grad_i grad_j (1/r) = -4pi/3 delta_ij
    (Eq. 6.139): the away-from-origin piece integrates to zero over the
    symmetric box, so the box integral isolates the delta term.  Computed as
    the surface flux of grad_j(1/r) = -x_j/r^3 through the two i-faces."""
    x2, w2 = gauss_legendre(n, -a, a)
    tot = 0.0
    for s in (+1.0, -1.0):
        for p, wp_ in zip(x2, w2):
            for q, wq_ in zip(x2, w2):
                v = np.zeros(3)
                v[i] = s * a
                v[(i + 1) % 3] = p
                v[(i + 2) % 3] = q
                r = np.linalg.norm(v)
                tot += s * wp_ * wq_ * (-(v[j]) / r**3)
    return tot


def dipole_ball_integral(m, Rball=0.8, n=40):
    """Int_ball B d^3x for A = m x r/r^3 via Int curl A = oint n x A da:
    should equal (8 pi/3) m (the delta term of Eq. 6.152)."""
    m = np.asarray(m, float)
    th, wt = gauss_legendre(n, 0.0, np.pi)
    ph, wp = gauss_legendre(2 * n, 0.0, TWO_PI)
    out = np.zeros(3)
    for t, w1 in zip(th, wt):
        for p, w2 in zip(ph, wp):
            nv = np.array([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)])
            x = Rball * nv
            A = np.cross(m, x) / Rball**3
            out += w1 * w2 * Rball**2 * np.sin(t) * np.cross(nv, A)
    return out


def jm_moment_smeared(m, eps=0.12, n=48, L=1.0):
    """(1/2c) Int x x J_m with J_m = -c m x grad(delta_eps): should equal m."""
    m = np.asarray(m, float)
    u, w = gauss_legendre(n, -L, L)
    out = np.zeros(3)
    for xi, wi in zip(u, w):
        for yi, wj in zip(u, w):
            for zi, wk in zip(u, w):
                x = np.array([xi, yi, zi])
                r2 = x @ x
                gd = -x / eps**2 * np.exp(-r2 / (2 * eps**2)) / (TWO_PI * eps**2) ** 1.5
                Jm = -C * np.cross(m, gd)
                out += wi * wj * wk * np.cross(x, Jm)
    return out / (2 * C)


def slab_equiv_current(M0, dthick):
    """Ex. 6.8.2: a thin slab of uniform perpendicular magnetization M0 and
    thickness d is equivalent to a rim circuit with I = c M0 d (K_eff =
    c M x n lives only on the rim; the faces have M || n)."""
    return C * M0 * dthick


def slab_B_charges(x, R, dthick, M0):
    """B outside a thin uniformly magnetized disk-slab (radius R, thickness
    d, M = M0 zhat, faces at z = +-d/2) from the magnetic-charge picture:
    B = H = -grad Phi_m with two charged disks sigma_m = +-M0 (exact for any
    d; used to verify the Ex. 6.8.2 rim-current equivalence as d -> 0)."""
    return bar_H_exact(x, R, dthick, M0)


# ----- magnetic quadrupole machinery (Exs. 6.8.5, 6.8.6)

def make_divfree_J(w=0.25, kind=0):
    """Return an exactly divergence-free localized current J = curl(g V),
    g = exp(-r^2/2w^2), V polynomial: J = g [curl V - (x/w^2) x V] (analytic
    curl).  Accepts a single point (3,) or a batch (N, 3)."""
    def J(x):
        x = np.asarray(x, float)
        single = x.ndim == 1
        X = x[None, :] if single else x
        r2 = np.einsum('...i,...i->...', X, X)
        g = np.exp(-r2 / (2 * w * w))
        x1, y1, z1 = X[..., 0], X[..., 1], X[..., 2]
        one = np.ones_like(x1)
        if kind == 0:
            V = np.stack([y1, z1**2, x1 * y1], axis=-1)
            curlV = np.stack([x1 - 2 * z1, -y1, -one], axis=-1)
        else:
            V = np.stack([0.3 + z1, x1, -y1 * z1], axis=-1)
            curlV = np.stack([-z1, one, one], axis=-1)
        out = g[..., None] * (curlV - np.cross(X, V) / (w * w))
        return out[0] if single else out
    return J


# quadrature box for the Sec. 6.8.5-6.8.6 moment integrals: chosen so the
# Gaussian tail of make_divfree_J at the faces (e^{-L^2/2w^2} ~ 1e-8) cannot
# pollute the surface terms the identities rely on
QUAD_L, QUAD_N = 1.5, 42


def _grid_pts(L, n):
    u, w = gauss_legendre(n, -L, L)
    X, Y, Z = np.meshgrid(u, u, u, indexing='ij')
    pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=-1)
    W = (w[:, None, None] * w[None, :, None] * w[None, None, :]).ravel()
    return pts, W


def grid_integrate(f, L=1.2, n=26):
    """Int f(x) d^3x over the cube [-L,L]^3 for a per-point f -> scalar/vector."""
    u, w = gauss_legendre(n, -L, L)
    out = None
    for xi, wi in zip(u, w):
        for yi, wj in zip(u, w):
            for zi, wk in zip(u, w):
                v = f(np.array([xi, yi, zi])) * (wi * wj * wk)
                out = v if out is None else out + v
    return out


def moment_vector(J, L=QUAD_L, n=QUAD_N):
    """m = (1/2c) Int x x J d^3x (6.129), vectorized."""
    pts, W = _grid_pts(L, n)
    return np.einsum('n,ni->i', W, np.cross(pts, J(pts))) / (2 * C)


def quad_moment_mij(J, L=QUAD_L, n=QUAD_N):
    """m_ij = (2/(3c)) Int (x x J)_i x_j d^3x (Ex. 6.8.5b), vectorized."""
    pts, W = _grid_pts(L, n)
    return 2.0 / (3 * C) * np.einsum('n,ni,nj->ij', W, np.cross(pts, J(pts)), pts)


def cyclic_integral(J, i, j, k, L=QUAD_L, n=QUAD_N):
    """Int (x_i x_j J_k + x_i J_j x_k + J_i x_j x_k) d^3x (Ex. 6.8.5a)."""
    pts, W = _grid_pts(L, n)
    Jv = J(pts)
    return np.sum(W * (pts[:, i] * pts[:, j] * Jv[:, k]
                       + pts[:, i] * Jv[:, j] * pts[:, k]
                       + Jv[:, i] * pts[:, j] * pts[:, k]))


def xxJ_integral(J, i, j, k, L=QUAD_L, n=QUAD_N):
    pts, W = _grid_pts(L, n)
    return np.sum(W * pts[:, i] * pts[:, j] * J(pts)[:, k])


EPS3 = np.zeros((3, 3, 3))
for _i, _j, _k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
    EPS3[_i, _j, _k] = 1.0
    EPS3[_i, _k, _j] = -1.0


def A_quadrupole(x, mij):
    """Ex. 6.8.5(c): A^(q)_k = -(1/(2 c r^5)) sum eps_{kir} Q_ij m_rj,
    Q_ij = 3 x_i x_j - r^2 delta_ij."""
    x = np.asarray(x, float)
    r2 = x @ x
    Q = 3 * np.outer(x, x) - r2 * np.eye(3)
    A = np.zeros(3)
    for k in range(3):
        s = 0.0
        for i in range(3):
            for r in range(3):
                if EPS3[k, i, r] == 0:
                    continue
                for j in range(3):
                    s += EPS3[k, i, r] * Q[i, j] * mij[r, j]
        A[k] = -s / (2 * C * r2**2.5)
    return A


def B_quadrupole(x, sij):
    """Ex. 6.8.6(a): B^(q)_k = (3/(2 r^7)) sum s_ij (5 x_i x_j x_k
    - delta_ik r^2 x_j - delta_jk r^2 x_i)."""
    x = np.asarray(x, float)
    r2 = x @ x
    B = np.zeros(3)
    for k in range(3):
        s = 0.0
        for i in range(3):
            for j in range(3):
                s += sij[i, j] * (5 * x[i] * x[j] * x[k]
                                  - (r2 * x[j] if i == k else 0.0)
                                  - (r2 * x[i] if j == k else 0.0))
        B[k] = 1.5 * s / r2**3.5
    return B


def A_exact_from_J(x, J, L=QUAD_L, n=QUAD_N):
    """A(x) = (1/c) Int J(x')/|x-x'| d^3x' (6.42), vectorized."""
    pts, W = _grid_pts(L, n)
    d = np.linalg.norm(np.asarray(x, float) - pts, axis=1)
    return np.einsum('n,ni->i', W / d, J(pts)) / C


def costheta_shell_sij(a, sigma0, omega):
    """P21(c): s_11=s_22=-8 pi sigma0 a^5 omega/(45 c), s_33 = +16 pi .../(45c)."""
    s1 = -8 * np.pi * sigma0 * a**5 * omega / (45 * C)
    return np.diag([s1, s1, -2 * s1])


def costheta_shell_mij_quad(a, sigma0, omega, n=400):
    """Direct m_ij = (2/(3c)) oint (x x K)_i x_j da over the shell."""
    th, w = gauss_legendre(n, 0.0, np.pi)
    out = np.zeros((3, 3))
    ph, wp = gauss_legendre(2 * n, 0.0, TWO_PI)
    for t, w1 in zip(th, w):
        st, ct = np.sin(t), np.cos(t)
        for p, w2 in zip(ph, wp):
            x = a * np.array([st * np.cos(p), st * np.sin(p), ct])
            eph = np.array([-np.sin(p), np.cos(p), 0.0])
            K = omega * a * sigma0 * ct * st * eph
            out += w1 * w2 * a**2 * st * np.outer(np.cross(x, K), x)
    return 2.0 / (3 * C) * out


# ============================== Sec. 6.9: forces and torques on dipoles

def wire_dipole_force(m, I, x0):
    """Ex. 6.9.1: F = -(2 I/(c x0^2)) (m_y xhat + m_x yhat)."""
    return -2 * I / (C * x0**2) * np.array([m[1], m[0], 0.0])


def wire_dipole_torque(m, I, x0):
    """Ex. 6.9.1: N = (2 I/(c x0)) (-m_z xhat + m_x zhat)."""
    return 2 * I / (C * x0) * np.array([-m[2], 0.0, m[0]])


def wire_B(x, I):
    """Infinite wire along z: B = (2I/c) e_phi/rho."""
    x = np.asarray(x, float)
    rho2 = x[0] ** 2 + x[1] ** 2
    return 2 * I / C * np.array([-x[1], x[0], 0.0]) / rho2


def small_loop_force(Bfun, center, nhat, eps, I, N=400):
    """F = (I/c) oint dl x B(x), quadrature over a small loop."""
    center = np.asarray(center, float)
    nhat = np.asarray(nhat, float) / np.linalg.norm(nhat)
    t = np.array([1.0, 0, 0]) if abs(nhat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(nhat, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    ph = (np.arange(N) + 0.5) * TWO_PI / N
    F = np.zeros(3)
    for p in ph:
        x = center + eps * (np.cos(p) * e1 + np.sin(p) * e2)
        dl = eps * (TWO_PI / N) * (-np.sin(p) * e1 + np.cos(p) * e2)
        F += I / C * np.cross(dl, Bfun(x))
    return F


def small_loop_torque(Bfun, center, nhat, eps, I, N=400):
    """N = (1/c) oint x x (I dl x B), about the loop center."""
    center = np.asarray(center, float)
    nhat = np.asarray(nhat, float) / np.linalg.norm(nhat)
    t = np.array([1.0, 0, 0]) if abs(nhat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(nhat, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(nhat, e1)
    ph = (np.arange(N) + 0.5) * TWO_PI / N
    Nq = np.zeros(3)
    for p in ph:
        rrel = eps * (np.cos(p) * e1 + np.sin(p) * e2)
        dl = eps * (TWO_PI / N) * (-np.sin(p) * e1 + np.cos(p) * e2)
        Nq += np.cross(rrel, I / C * np.cross(dl, Bfun(center + rrel)))
    return Nq


def loop_force_quad(Bfun, pts, I=1.0):
    """F = (I/c) oint dl x B over a closed polyline."""
    pts = np.asarray(pts, float)
    seg = np.roll(pts, -1, axis=0) - pts
    mid = pts + 0.5 * seg
    return I / C * np.sum([np.cross(s, Bfun(mp)) for s, mp in zip(seg, mid)], axis=0)


def force_grad_mB(Bfun, m, x, h=1e-4):
    """F = grad (m.B) by finite differences (Eq. 6.170)."""
    return grad_fd(lambda y: np.asarray(m) @ Bfun(y), x, h)


# ==================== Sec. 6.10: surface torque; dipole in a cavity / sphere

def hemisphere_torque_quad(a, M0, B0vec, n=200):
    """Ex. 6.10.1(b): N = (1/c) oint da x x (K_eff x B0), K_eff = c M x n,
    over the hemisphere r=a, z>0 (flat face has K_eff = 0)."""
    th, wt = gauss_legendre(n, 0.0, np.pi / 2)
    ph, wp = gauss_legendre(2 * n, 0.0, TWO_PI)
    Mv = np.array([0, 0, M0])
    out = np.zeros(3)
    for t, w1 in zip(th, wt):
        for p, w2 in zip(ph, wp):
            nv = np.array([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)])
            x = a * nv
            K = C * np.cross(Mv, nv)
            out += w1 * w2 * a**2 * np.sin(t) * np.cross(x, np.cross(K, B0vec)) / C
    return out


def hemisphere_torque(a, M0, B0vec):
    """N = m x B0 with m = (2 pi a^3/3) M0 zhat."""
    m = 2 * np.pi * a**3 / 3 * np.array([0, 0, M0])
    return np.cross(m, np.asarray(B0vec, float))


def cavity_C1C2(mu):
    """Ex. 6.10.2(a): A_in = m x r/r^3 + (C1/a^3) m x r, A_out = C2 m x r/r^3:
    C1 = (mu-1)/(2 mu+1), C2 = 3 mu/(2 mu+1)."""
    return (mu - 1) / (2 * mu + 1), 3 * mu / (2 * mu + 1)


def sphere_C1C2(mu):
    """Ex. 6.10.2(b): dipole at center of a permeable sphere in vacuum:
    C1' = (1-mu)/(2+mu), C2' = 3/(mu+2) (the (a) result with mu -> 1/mu)."""
    return (1 - mu) / (2 + mu), 3.0 / (mu + 2)


def cavity_fields(x, m, a, mu):
    """B inside/outside for the cavity problem (m along z)."""
    x = np.asarray(x, float)
    r = np.linalg.norm(x)
    C1, C2 = cavity_C1C2(mu)
    mv = np.array([0, 0, m])
    if r < a:
        return dipole_B(x, mv) + 2 * C1 * m / a**3 * np.array([0, 0, 1.0])
    return C2 * dipole_B(x, mv)


def cavity_Kb_coefficient(m, a, mu):
    """Ex. 6.10.2(c): K_b = c M_theta e_phi at r=a with
    M_theta = ((mu-1)/4pi)(C2/mu)(m/a^3) sin th; the sigma-omega-a map is
    sigma omega a <-> (3 c m/(4 pi a^3)) (mu-1)/(2 mu+1)."""
    return 3 * C * m / (FOUR_PI * a**3) * (mu - 1) / (2 * mu + 1)


# ========================= Sec. 6.11: permeable sphere in a uniform field

def perm_sphere_phim(x, a, mu, B0):
    """Ex. 6.11.1: Phi_m with H = -grad Phi_m, B0 = B0 zhat:
    inside: -(3/(mu+2)) B0 r cos th; outside: -B0 r cos th + (mu-1)/(mu+2) a^3 B0 cos th/r^2."""
    x = np.asarray(x, float)
    r = np.linalg.norm(x)
    if r < a:
        return -3 / (mu + 2) * B0 * x[2]
    return -B0 * x[2] + (mu - 1) / (mu + 2) * a**3 * B0 * x[2] / r**3


def perm_sphere_B(x, a, mu, B0):
    """B = mu H inside, H outside."""
    x = np.asarray(x, float)
    H = -grad_fd(lambda y: perm_sphere_phim(y, a, mu, B0), x)
    return mu * H if np.linalg.norm(x) < a else H


def perm_sphere_M(mu, B0):
    """Ex. 6.11.1(b): M = (3/4pi) (mu-1)/(mu+2) B0."""
    return 3 / FOUR_PI * (mu - 1) / (mu + 2) * B0


# =========================== Sec. 6.12: image method at a plane interface

def image_coeffs_vacuum_source(mu):
    """Ex. 6.12.1: source in vacuum z>0, medium mu at z<0:
    J* = (a J_x, a J_y, b J_z)(x,y,-z), a = -b = (mu-1)/(mu+1);
    J** = c J with c = 2 mu/(mu+1)."""
    a = (mu - 1) / (mu + 1)
    return a, -a, 2 * mu / (mu + 1)


def image_coeffs_embedded_source(mu):
    """Ex. 6.12.2: source embedded in medium mu at z>0, vacuum z<0:
    J* = (a J_x, a J_y, b J_z)(x,y,-z) with a = -(mu-1)/(mu+1) = -b,
    (its field carries the medium factor mu), and J** = c J with
    c = 2 mu/(mu+1) evaluated with the vacuum kernel."""
    a = -(mu - 1) / (mu + 1)
    return a, -a, 2 * mu / (mu + 1)


def mirror_loop(center, nhat):
    """Proper mirror (z -> -z) of a current loop: center reflected, normal
    (pseudovector) -> (-nx, -ny, +nz).  The image current (aJ_par, aJ_par, -aJ_z)
    is a times this mirrored loop."""
    center = np.asarray(center, float); nhat = np.asarray(nhat, float)
    return center * np.array([1, 1, -1.0]), nhat * np.array([-1, -1, 1.0])


def interface_BC_residual_vacuum_source(mu, center, nhat, a_loop, xy, I=1.0, N=256):
    """P27 check: BC residuals (B_z jump, H_par jump) at z=0, source in vacuum."""
    acoef, bcoef, ccoef = image_coeffs_vacuum_source(mu)
    cm, nm = mirror_loop(center, nhat)
    xpt = np.array([xy[0], xy[1], 0.0])
    B2 = loop_B_3d(xpt, center, nhat, a_loop, I, N) + loop_B_3d(xpt, cm, nm, a_loop, acoef * I, N)
    B1 = loop_B_3d(xpt, center, nhat, a_loop, ccoef * I, N)   # medium side field
    dBz = B2[2] - B1[2]
    dHt = B2[:2] - B1[:2] / mu
    return dBz, np.max(np.abs(dHt))


def interface_BC_residual_embedded_source(mu, center, nhat, a_loop, xy, I=1.0, N=256):
    """P28 check: source embedded in the medium (z>0), vacuum below."""
    acoef, bcoef, ccoef = image_coeffs_embedded_source(mu)
    cm, nm = mirror_loop(center, nhat)
    xpt = np.array([xy[0], xy[1], 0.0])
    B2 = mu * (loop_B_3d(xpt, center, nhat, a_loop, I, N) + loop_B_3d(xpt, cm, nm, a_loop, acoef * I, N))
    B1 = loop_B_3d(xpt, center, nhat, a_loop, ccoef * I, N)
    dBz = B2[2] - B1[2]
    dHt = B2[:2] / mu - B1[:2]
    return dBz, np.max(np.abs(dHt))


def loop_image_force(a, d, mu, I, n=400):
    """Sec. 6.12 worked example / P32 warm-up, Eq. (6.237):
    F_z = -(4 pi^2 I^2 a^2/c^2) ((mu-1)/(mu+1)) Int dk k e^{-2kd} J1(ka)^2."""
    k, w = gauss_legendre(n, 0.0, 60.0 / d)
    val = np.sum(w * k * np.exp(-2 * k * d) * special.j1(k * a) ** 2)
    return -4 * np.pi**2 * I**2 * a**2 / C**2 * (mu - 1) / (mu + 1) * val


# ---- P29/P30: solid-angle and Green-function representations

def solid_angle_B(x, a, d, I, coef_img=0.0):
    """B = (I/c)[grad Omega_src + coef_img grad Omega_img] for a loop of
    radius a at height z=d (normal +z), image at z=-d (P29, z>0 side)."""
    def om(y):
        return (solid_angle_disk_quad(y, a, center=(0, 0, d))
                + coef_img * solid_angle_disk_quad(y, a, center=(0, 0, -d)))
    return I / C * grad_fd(om, x, h=2e-4)


def greens_phim(x, a, d, mu):
    """P30: Phi_m = (I/c) Int_S' da' d/dn' G(x,x';mu) over the dipole surface
    S' (disk of radius a at z=d>0, n' = +zhat), with the half-space
    dielectric-analog Green function, I=1:
    z>0: G = 1/g - lam/g_im ; z<0: G = (2/(mu+1))/g, lam = (mu-1)/(mu+1).
    Int da' dn'(1/g) = -Omega_src(x) (6.68); the image kernel gives
    Int da' dn'(1/g_im) = -Omega_src(x_mirror) = +Omega_img(x) when Omega_img
    is computed with n' = +zhat on the image disk (mirroring flips the
    normal).  Hence Phi_m = -(I/c)[Omega_src + lam Omega_img] for z > 0 and
    H = -grad Phi_m = (I/c) grad[Omega_src + lam Omega_img] = B there."""
    lam = (mu - 1) / (mu + 1)
    if x[2] > 0:
        return -1.0 / C * (solid_angle_disk_quad(x, a, center=(0, 0, d))
                           + lam * solid_angle_disk_quad(x, a, center=(0, 0, -d)))
    return -1.0 / C * (2 / (mu + 1)) * solid_angle_disk_quad(x, a, center=(0, 0, d))


# ---- P31: perfectly conducting sphere image

def sphere_image_ring(r0, th0, asph, I):
    """Image of a coaxial ring (r0, th0, current I along +e_phi) in the
    perfect conductor r=a: ring at (a^2/r0, th0), current I* = -(r0/a) I."""
    return asph**2 / r0, th0, -(r0 / asph) * I


# ---- P32: dipole near a permeable slab

def dipole_slab_force(m, d, mu, theta):
    """Ex. 6.12.6: F = -zhat 3 m^2 (1+cos^2 th) (mu-1)/((mu+1) 16 d^4)
    (toward the slab for mu>1; independent of phi)."""
    return -3 * m**2 * (1 + np.cos(theta) ** 2) * (mu - 1) / ((mu + 1) * 16 * d**4)


def dipole_slab_force_quad(m, d, mu, theta, phi=0.3, eps=1e-2, N=600):
    """Model the dipole as a small loop (radius eps, I = m c/(pi eps^2)) and
    integrate F = (I/c) oint dl x B_image with the P27 image loop."""
    nhat = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
    acoef, _, _ = image_coeffs_vacuum_source(mu)
    center = np.array([0, 0, d])
    cm, nm = mirror_loop(center, nhat)
    I = m * C / (np.pi * eps**2)
    Bimg = lambda y: loop_B_3d(y, cm, nm, eps, acoef * I, N=200)
    return small_loop_force(Bimg, center, nhat, eps, I, N=N)


# ================== Sec. 6.13: magnetization potentials, magnets, shells

def A_magnetized_sphere(x, a, M0):
    """Ex. 6.13.1 check case: uniformly magnetized sphere (M = M0 zhat):
    A_phi = (4 pi M0/3) r sin th (r<a), (4 pi M0 a^3/3) sin th/r^2 (r>a)."""
    x = np.asarray(x, float)
    r = np.linalg.norm(x)
    rho = np.hypot(x[0], x[1])
    if r < 1e-12 or rho < 1e-12:
        return np.zeros(3)
    eph = np.array([-x[1], x[0], 0.0]) / rho
    st = rho / r
    Aphi = FOUR_PI * M0 / 3 * (r * st if r < a else a**3 * st / r**2)
    return Aphi * eph


def A_magnetization_surface(x, a, M0, n=400):
    """A = -oint da' (n' x M)/|x-x'| for the uniform sphere (grad' x M = 0)."""
    x = np.asarray(x, float)
    th, wt = gauss_legendre(n, 0.0, np.pi)
    ph, wp = gauss_legendre(2 * n, 0.0, TWO_PI)
    Mv = np.array([0, 0, M0])
    out = np.zeros(3)
    for t, w1 in zip(th, wt):
        nv = np.stack([np.sin(t) * np.cos(ph), np.sin(t) * np.sin(ph), np.cos(t) * np.ones_like(ph)], axis=1)
        pts = a * nv
        d = np.linalg.norm(x - pts, axis=1)
        integrand = -np.cross(nv, np.broadcast_to(Mv, nv.shape)) / d[:, None]
        out += w1 * a**2 * np.sin(t) * np.sum(wp[:, None] * integrand, axis=0)
    return out


def A_direct_dipole_sum(x, Mfun, L=1.0, n=40):
    """A = Int M(x') x (x-x')/|x-x'|^3 d^3x' on a grid (Ex. 6.13.1 LHS).
    Mfun must accept a batch of points (N, 3)."""
    pts, W = _grid_pts(L, n)
    d = np.asarray(x, float) - pts
    dn = np.linalg.norm(d, axis=1) ** 3
    return np.einsum('n,ni->i', W / dn, np.cross(Mfun(pts), d))


def A_curl_plus_surface(x, Mfun, L=1.0, n=40, curlM=None):
    """A = Int (grad' x M)/|x-x'| d^3x' (Ex. 6.13.1 RHS; the surface term
    -oint (n' x M)/g vanishes for M negligible on the box faces).  Pass the
    analytic curl as curlM (batch) for speed/accuracy; otherwise a per-point
    finite-difference curl of Mfun is used."""
    if curlM is not None:
        pts, W = _grid_pts(L, n)
        d = np.linalg.norm(np.asarray(x, float) - pts, axis=1)
        return np.einsum('n,ni->i', W / d, curlM(pts))

    def f(xp):
        cm = curl_fd(lambda y: Mfun(y), xp, h=1e-5)
        return cm / np.linalg.norm(np.asarray(x) - xp)
    return grid_integrate(f, L, n)


# ---- P34: split-sphere magnet

def split_sphere_Cn(n):
    """Ex. 6.13.2(b): C_0 = 0, C_n = (-1)^{n+1} 2n (2n-3)!!/(2n+2)!! (n>=1),
    built by a stable ratio recursion (|C_{n+1}|/|C_n| =
    (2n+2)(2n-1)/((2n)(2n+4)))."""
    if n == 0:
        return 0.0
    c = 0.25                       # C_1 = 2 * (-1)!!/4!! = 1/4
    for k in range(1, n):
        c *= (2 * k + 2) * (2 * k - 1) / ((2 * k) * (2 * k + 4))
    return (-1) ** (n + 1) * c


def split_sphere_phim_exterior(r, th, a, M0, N=50):
    """Phi_m(r>a) = 4 pi M0 a^2 sum C_n (a^{2n}/r^{2n+1}) P_{2n}(cos th)."""
    s = 0.0
    for n in range(N):
        s += split_sphere_Cn(n) * a ** (2 * n) / r ** (2 * n + 1) * special.eval_legendre(2 * n, np.cos(th))
    return FOUR_PI * M0 * a**2 * s


def split_sphere_phim_interior(r, th, a, M0, N=80):
    """Correct interior potential (shell + equatorial-disk sources):
    shell: 4 pi M0 a^2 sum_n I_{2n}/2 (r^{2n}/a^{2n+1}) P_{2n},
    disk (sigma = -2 M0): -4 pi M0 P_{2n}(0) g_{2n}(r) P_{2n},
    g_l(r) = r/(l+2) + r[1-(r/a)^{l-1}]/(l-1) (l>=2), g_0 = a - r/2."""
    x = np.cos(th)
    tot = 0.0
    for n in range(N):
        l = 2 * n
        # I_{2n} = 2 (-1)^{n+1} (2n-3)!!/(2n+2)!! = C_n/n  (I_0 = 1)
        I2n = 1.0 if n == 0 else split_sphere_Cn(n) / n
        shell = TWO_PI * M0 * a**2 * I2n * r**l / a ** (l + 1)
        if l == 0:
            gl = a - r / 2
        else:
            gl = r / (l + 2) + r * (1 - (r / a) ** (l - 1)) / (l - 1)
        disk = -FOUR_PI * M0 * special.eval_legendre(l, 0.0) * gl
        tot += (shell + disk) * special.eval_legendre(l, x)
    return tot


def split_sphere_phim_quad(r, th, a, M0):
    """Direct quadrature: shell sigma_m = M0 |cos th'| plus disk sigma = -2 M0."""
    x = np.array([r * np.sin(th), 0.0, r * np.cos(th)])

    def shell_ig(tp, pp):
        xs = a * np.array([np.sin(tp) * np.cos(pp), np.sin(tp) * np.sin(pp), np.cos(tp)])
        return M0 * abs(np.cos(tp)) * a**2 * np.sin(tp) / np.linalg.norm(x - xs)
    s1, _ = integrate.dblquad(shell_ig, 0, TWO_PI, 0, np.pi, epsabs=1e-9, epsrel=1e-9)

    def disk_ig(rp, pp):
        xs = np.array([rp * np.cos(pp), rp * np.sin(pp), 0.0])
        return -2 * M0 * rp / np.linalg.norm(x - xs)
    s2, _ = integrate.dblquad(disk_ig, 0, TWO_PI, 0, a, epsabs=1e-9, epsrel=1e-9)
    return s1 + s2


# ---- P35: bar magnet far field = two magnetic monopoles

def disk_phim_quad(x, R, z0, sig, nr=200, nph=200):
    """Potential of a uniformly 'charged' disk (magnetic charge density sig)."""
    x = np.asarray(x, float)
    r, wr = gauss_legendre(nr, 0.0, R)
    ph, wp = gauss_legendre(nph, 0.0, TWO_PI)
    out = 0.0
    for ri, wi in zip(r, wr):
        pts = np.stack([ri * np.cos(ph), ri * np.sin(ph), z0 * np.ones_like(ph)], axis=1)
        out += ri * wi * np.sum(wp / np.linalg.norm(x - pts, axis=1))
    return sig * out


def bar_H_exact(x, R, Lbar, M0):
    """H of a cylindrical bar magnet (faces at z=+-L/2): two charged disks."""
    f = lambda y: (disk_phim_quad(y, R, +Lbar / 2, +M0) + disk_phim_quad(y, R, -Lbar / 2, -M0))
    return -grad_fd(f, x, h=2e-4)


def bar_H_monopoles(x, R, Lbar, M0):
    """Ex. 6.13.3(b): H = M0 pi R^2 [ (x-x+)/|x-x+|^3 - (x-x-)/|x-x-|^3 ]."""
    x = np.asarray(x, float)
    q = M0 * np.pi * R**2
    xp = np.array([0, 0, +Lbar / 2]); xm = np.array([0, 0, -Lbar / 2])
    dp = x - xp; dm = x - xm
    return q * (dp / np.linalg.norm(dp) ** 3 - dm / np.linalg.norm(dm) ** 3)


# ---- P36: Hz = -M0 Omega

def square_face_omega(x, b, z0):
    """Omega (z-derivative convention, Eq. 6.69) of the square face
    |x'|,|y'| <= b/2 at height z0, from point x: Omega = d/dz Int da'/g."""
    def pot(y):
        u, w = gauss_legendre(120, -b / 2, b / 2)
        tot = 0.0
        for ui, wi in zip(u, w):
            pts = np.stack([ui * np.ones_like(u), u, z0 * np.ones_like(u)], axis=1)
            tot += wi * np.sum(w / np.linalg.norm(y - pts, axis=1))
        return tot
    return (pot(np.asarray(x) + [0, 0, 1e-4]) - pot(np.asarray(x) - [0, 0, 1e-4])) / 2e-4


def cube_Hz(x, b, M0):
    """Ex. 6.13.4(b): Hz = -M0 [Omega_top - Omega_bottom] (faces at +-b/2)."""
    return -M0 * (square_face_omega(x, b, +b / 2) - square_face_omega(x, b, -b / 2))


def cube_Hz_direct(x, b, M0, n=140):
    """Direct two-charged-square-face computation of H_z."""
    u, w = gauss_legendre(n, -b / 2, b / 2)
    x = np.asarray(x, float)
    tot = 0.0
    for s, z0 in [(+M0, b / 2), (-M0, -b / 2)]:
        for ui, wi in zip(u, w):
            pts = np.stack([ui * np.ones_like(u), u, z0 * np.ones_like(u)], axis=1)
            d = x - pts
            r3 = np.linalg.norm(d, axis=1) ** 3
            tot += s * wi * np.sum(w * d[:, 2] / r3)
    return tot


# ---- P37: rod magnet in Bessel form

def rod_H_bessel(rho, z, a, d, M0, n=600):
    """Ex. 6.13.5 (|z| < d/2):
    H_rho = 4 pi M0 a Int dk J1(ka) J1(k rho) e^{-kd/2} sinh(kz)
    H_z   = -4 pi M0 a Int dk J1(ka) J0(k rho) e^{-kd/2} cosh(kz)."""
    k, w = gauss_legendre(n, 0.0, 120.0 / d)
    damp = np.exp(-k * d / 2)
    Hrho = FOUR_PI * M0 * a * np.sum(w * special.j1(k * a) * special.j1(k * rho) * damp * np.sinh(k * z))
    Hz = -FOUR_PI * M0 * a * np.sum(w * special.j1(k * a) * special.j0(k * rho) * damp * np.cosh(k * z))
    return Hrho, Hz


def rod_H_disks(rho, z, a, d, M0):
    """Direct: two charged disks at z=+-d/2 with sigma_m = +-M0."""
    x = np.array([rho, 0.0, z])
    f = lambda y: (disk_phim_quad(y, a, +d / 2, +M0) + disk_phim_quad(y, a, -d / 2, -M0))
    H = -grad_fd(f, x, h=2e-4)
    return H[0], H[2]


# ---- P38: closed shell with normal area magnetization

def closed_shell_phim_sphere(x, a, MA):
    return solid_angle_sphere_quad(x, a, MA)


def closed_shell_phim_cube(x, b, MA):
    return solid_angle_cube_quad(x, b, MA)


# ================================================================== demo

if __name__ == "__main__":
    print("MACRO_EM-06 magnetostatics demo (Gaussian units, c=1)")
    print(f"  on-axis loop Bz(0)              = {loop_Bz_axis(0.0, 1.0, 1.0):.6f}  (2 pi I a^2/c... = 2 pi)")
    print(f"  pinch pressure P(0)             = {pinch_pressure(0.0, 1.0, 1.0):.6f}  (I^2/pi c^2 a^2)")
    br, bz = loop_B_elliptic(0.6, 0.4, 1.0, 1.0)
    print(f"  loop (elliptic) at rho=.6,z=.4  = ({br:.6f}, {bz:.6f})")
    br2, bz2 = loop_B_bessel(0.6, 0.4, 1.0, 1.0)
    print(f"  loop (Bessel 6.83/6.84)         = ({br2:.6f}, {bz2:.6f})")
    print(f"  cone Bz closed vs quad          = {cone_Bz_tip(0.5, 1, 2, 1, 1):.8f} vs {cone_Bz_tip_quad(0.5, 1, 2, 1, 1):.8f}")
    print(f"  saddle moment (R=1, L=2)        = {saddle_moment(1.0, 2.0)}")
    print(f"  quadrature moment               = {circuit_moment(saddle_circuit(1.0, 2.0))}")
    print(f"  cavity C1,C2 (mu=2.6)           = {cavity_C1C2(2.6)}")
    print(f"  split-sphere C1 (book C_n)      = {split_sphere_Cn(1):.6f}  (= 1/4)")
    print(f"  dipole-slab force (m=1,d=1,mu=3,th=0) = {dipole_slab_force(1, 1, 3, 0):.6f}")
