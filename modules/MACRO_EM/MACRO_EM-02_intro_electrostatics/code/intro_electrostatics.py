"""MACRO_EM-02 -- numeric checks for Wilcox & Thron 2e, Chapter 2
(Introduction to Electrostatics).

Gaussian units throughout, matching the book:
    E = -grad Phi,   div E = 4 pi rho,   Phi = q/r  (point charge).
Equation numbers in comments are the book's (map in ../notes.md).

Sections mirror the exercise blocks P1..P41 of problems/problems.md.
"""
import numpy as np
from scipy.integrate import quad

try:                       # numpy >= 2.0
    trapz = np.trapezoid
except AttributeError:     # older numpy
    trapz = np.trapz


# ---------------------------------------------------------------------------
# generic numeric-derivative helpers
# ---------------------------------------------------------------------------

def numeric_grad(f, x, h=1e-5):
    """Central-difference gradient of scalar f(3-vector)."""
    x = np.asarray(x, float)
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3); e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def numeric_curl(F, x, h=1e-5):
    """Central-difference curl of vector field F(3-vector)->3-vector."""
    x = np.asarray(x, float)
    J = np.zeros((3, 3))                      # J[i,j] = dF_i/dx_j
    for j in range(3):
        e = np.zeros(3); e[j] = h
        J[:, j] = (np.asarray(F(x + e)) - np.asarray(F(x - e))) / (2 * h)
    return np.array([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])


# ---------------------------------------------------------------------------
# P1  (2.1.1)  dipole potential: gradient and curl forms
# ---------------------------------------------------------------------------

def dipole_phi(d, x):
    """Phi = d.x / r^3."""
    d = np.asarray(d, float); x = np.asarray(x, float)
    r = np.linalg.norm(x)
    return float(d @ x) / r**3


def dipole_E(d, x):
    """E = [3(d.xhat)xhat - d]/r^3  (= -grad dipole_phi, r != 0)."""
    d = np.asarray(d, float); x = np.asarray(x, float)
    r = np.linalg.norm(x); xh = x / r
    return (3.0 * (d @ xh) * xh - d) / r**3


def dipole_A(d, x):
    """A = d x vec(x) / r^3  (curl A = E away from origin)."""
    d = np.asarray(d, float); x = np.asarray(x, float)
    r = np.linalg.norm(x)
    return np.cross(d, x) / r**3


# ---------------------------------------------------------------------------
# P2  (2.2.1)  |det M| as parallelepiped volume; scale factors
# ---------------------------------------------------------------------------

def parallelepiped_volume(M):
    """|v3.(v1 x v2)| of the image of the unit cube (columns of M)."""
    M = np.asarray(M, float)
    v1, v2, v3 = M[:, 0], M[:, 1], M[:, 2]
    return abs(v3 @ np.cross(v1, v2))


def jacobian_matrix(fmap, u, h=1e-6):
    """Numeric Jacobian d x_i / d u_j of fmap: R^3 -> R^3."""
    u = np.asarray(u, float)
    J = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3); e[j] = h
        J[:, j] = (np.asarray(fmap(u + e)) - np.asarray(fmap(u - e))) / (2 * h)
    return J


def scale_factors(fmap, u, h=1e-6):
    """Norms of the Jacobian columns (orthogonal systems: product = |det J|)."""
    J = jacobian_matrix(fmap, u, h)
    return np.linalg.norm(J, axis=0)


def spherical_map(u):
    """(r, mu=cos(theta), phi) -> (x, y, z).  |det J| = r^2."""
    r, mu, phi = u
    s = np.sqrt(1.0 - mu * mu)
    return np.array([r * s * np.cos(phi), r * s * np.sin(phi), r * mu])


def oblate_map(u, R=1.0):
    """(xi, mu=cos(theta), phi) -> (x, y, z).  |det J| = R^3 (xi^2 + mu^2)."""
    xi, mu, phi = u
    s = np.sqrt(1.0 - mu * mu)
    A = np.sqrt(xi * xi + 1.0)
    return np.array([R * A * s * np.cos(phi), R * A * s * np.sin(phi), R * xi * mu])


def oblate_det_exact(xi, mu, R=1.0):
    return R**3 * (xi * xi + mu * mu)


# ---------------------------------------------------------------------------
# P3  (2.2.2)  Lorentzian delta sequences
# ---------------------------------------------------------------------------

def lorentzian_delta(x, eps):
    """(1/pi) eps/(x^2+eps^2)  -> delta(x)."""
    return eps / (np.pi * (x * x + eps * eps))


def delta2d_seq(rho, eps):
    """(1/2pi) eps/(rho^2+eps^2)^{3/2}  -> delta^(2)(x) (radial profile)."""
    return eps / (2.0 * np.pi * (rho * rho + eps * eps) ** 1.5)


def smear_1d(g, eps, lim=np.inf):
    """integral  lorentzian_delta(x,eps) g(x) dx  -> g(0)."""
    val, _ = quad(lambda x: lorentzian_delta(x, eps) * g(x), -lim, lim, limit=400)
    return val


def smear_2d(g, eps, rmax=np.inf):
    """integral  delta2d_seq * g(rho) dA (radially symmetric g)  -> g(0)."""
    val, _ = quad(lambda r: 2 * np.pi * r * delta2d_seq(r, eps) * g(r), 0, rmax,
                  limit=400)
    return val


# ---------------------------------------------------------------------------
# P6  (2.4.1)  Gauss law in 2-D and the log potential
# ---------------------------------------------------------------------------

def E2d_point(x, x0=(0.0, 0.0)):
    """Unit 2-D point charge field  (x-x0)/|x-x0|^2."""
    v = np.asarray(x, float) - np.asarray(x0, float)
    return v / (v @ v)


def flux2d(E, center, R, n=4000):
    """Closed-loop flux  oint n.E dl  around circle(center, R)."""
    th = np.linspace(0.0, 2 * np.pi, n, endpoint=False)
    nx, ny = np.cos(th), np.sin(th)
    tot = 0.0
    for cx, cy, nxi, nyi in zip(center[0] + R * nx, center[1] + R * ny, nx, ny):
        Ex, Ey = E((cx, cy))
        tot += (Ex * nxi + Ey * nyi)
    return tot * (2 * np.pi * R / n)


def laplacian2d_log(x, y, h=1e-4):
    """5-point Laplacian of ln r at (x, y) != 0  (should be ~0)."""
    f = lambda a, b: np.log(np.hypot(a, b))
    return (f(x + h, y) + f(x - h, y) + f(x, y + h) + f(x, y - h) - 4 * f(x, y)) / h**2


def E_line3d(rho, lam=1.0):
    """3-D infinite line charge field magnitude 2 lam / rho (Gauss, 4 pi)."""
    return 2.0 * lam / rho


# ---------------------------------------------------------------------------
# P7  (2.4.2)  crossed finite line charges
# ---------------------------------------------------------------------------

def phi_segment(zeta, b, z1, z2, lam=1.0):
    """Potential of a uniform segment [z1,z2] along its axis coordinate,
    field point at axial coord zeta and transverse distance b:
    lam [asinh((z2-zeta)/b) - asinh((z1-zeta)/b)]."""
    return lam * (np.arcsinh((z2 - zeta) / b) - np.arcsinh((z1 - zeta) / b))


def phi_segment_quad(zeta, b, z1, z2, lam=1.0):
    val, _ = quad(lambda t: lam / np.hypot(t - zeta, b), z1, z2, limit=400)
    return val


def phi_plus(x, y, z, L, lam=1.0):
    """'+' of two full lines (length 2L) along x and y axes."""
    b1 = np.hypot(y, z)          # transverse distance to the x-axis line
    b2 = np.hypot(x, z)          # ... to the y-axis line
    return (phi_segment(x, b1, -L, L, lam) + phi_segment(y, b2, -L, L, lam))


def phi_plus_asym(x, y, z, L, lam=1.0):
    """L >> r asymptote:  -lam ln[(x^2+z^2)(y^2+z^2)/16L^4]."""
    return -lam * np.log((x * x + z * z) * (y * y + z * z) / (16.0 * L**4))


def phi_halflines(x, y, z, L, lam=1.0):
    """+lam on 0<=y'<=L (y-axis), -lam on 0<=x'<=L (x-axis)."""
    b1 = np.hypot(y, z)
    b2 = np.hypot(x, z)
    return (phi_segment(y, b2, 0.0, L, lam) - phi_segment(x, b1, 0.0, L, lam))


def phi_halflines_asym(x, y, z, lam=1.0):
    """L >> r asymptote:  -lam ln[(r-y)/(r-x)]."""
    r = np.sqrt(x * x + y * y + z * z)
    return -lam * np.log((r - y) / (r - x))


# ---------------------------------------------------------------------------
# P8  (2.4.3)  charged cylinder, axial field
# ---------------------------------------------------------------------------

def Ez_disk(z, b, sigma=1.0):
    """On-axis field of a uniform disk radius b at z'=0:
    2 pi sigma [sgn z - z/sqrt(z^2+b^2)]."""
    return 2 * np.pi * sigma * (np.sign(z) - z / np.hypot(z, b))


def Ez_cylinder(z, a, b, rho=1.0):
    """On-axis field of a solid cylinder radius b, faces z=+-a/2 (closed form)."""
    if z > a / 2:
        sgn_part = a
    elif z < -a / 2:
        sgn_part = -a
    else:
        sgn_part = 2.0 * z
    f = np.hypot(z + a / 2, b) - np.hypot(z - a / 2, b)
    return 2 * np.pi * rho * (sgn_part - f)


def Ez_cylinder_quad(z, a, b, rho=1.0):
    """Same by stacking disks (quadrature over slab positions)."""
    val, _ = quad(lambda zp: Ez_disk(z - zp, b, rho), -a / 2, a / 2, limit=400)
    return val


def cylinder_center_slope(a, b, rho=1.0):
    """E_z ~ const * z near the center: const = 4 pi rho [1 - a/sqrt(a^2+4b^2)]."""
    return 4 * np.pi * rho * (1.0 - a / np.sqrt(a * a + 4 * b * b))


# ---------------------------------------------------------------------------
# P9  (2.4.4)  ring field, truncated cone
# ---------------------------------------------------------------------------

def Ez_ring(z, R, lam=1.0):
    """2 pi lam R z / (R^2+z^2)^{3/2}."""
    return 2 * np.pi * lam * R * z / (R * R + z * z) ** 1.5


def Ez_ring_quad(z, R, lam=1.0):
    """Direct quadrature over the loop (axial component)."""
    def integrand(phi):
        # element at (R cos, R sin, 0); field point (0,0,z)
        d2 = R * R + z * z
        return lam * R * z / d2 ** 1.5
    val, _ = quad(integrand, 0, 2 * np.pi, limit=200)
    return val


def Ez_cone_tip(alpha, L1, L2, sigma=1.0):
    """Field at the (theoretical) tip of a truncated cone, half-angle alpha,
    surface density sigma, running z' = L1..L2:  -2 pi sigma sin a cos a ln(L2/L1)."""
    return -2 * np.pi * sigma * np.sin(alpha) * np.cos(alpha) * np.log(L2 / L1)


def Ez_cone_tip_quad(alpha, L1, L2, sigma=1.0):
    """Stack rings along the cone (quadrature in the axial coordinate)."""
    ta = np.tan(alpha)

    def integrand(zp):
        rho = zp * ta
        dq_dz = sigma * 2 * np.pi * rho / np.cos(alpha)   # ring charge / dz'
        return dq_dz * (0.0 - zp) / (zp * zp + rho * rho) ** 1.5

    val, _ = quad(integrand, L1, L2, limit=400)
    return val


# ---------------------------------------------------------------------------
# P10  (2.5.1)  Cavendish with 1/r^(1+eps)
# ---------------------------------------------------------------------------

def phi_shell_eps(r, s, q, eps):
    """Uniform shell radius s, charge q, modified potential (2.62)-(2.63):
    q/(1-eps^2) * [(r+s)^(1-eps) - |r-s|^(1-eps)] / (2 s r)."""
    return q / (1.0 - eps * eps) * ((r + s) ** (1 - eps) - abs(r - s) ** (1 - eps)) / (2 * s * r)


def phi_shell_eps_quad(r, s, q, eps):
    """Same by direct quadrature over the shell (mu = cos theta)."""
    sig = q / (4 * np.pi * s * s)

    def integrand(mu):
        u = np.sqrt(r * r + s * s - 2 * r * s * mu)
        return 2 * np.pi * s * s * sig / u ** (1 + eps)

    val, _ = quad(integrand, -1, 1, limit=400)
    return val / (1.0 + eps)


def qa_eps_exact(a, b, qb, eps):
    """Solve Phi(a) = Phi(b) exactly (linear in q_a) for the wired shells."""
    # coefficients of q_a and q_b in Phi(a) - Phi(b) = 0
    ca = phi_shell_eps(a, a, 1.0, eps) - phi_shell_eps(b, a, 1.0, eps)
    cb = phi_shell_eps(a, b, 1.0, eps) - phi_shell_eps(b, b, 1.0, eps)
    return -qb * cb / ca


def qa_eps_approx(a, b, qb, eps):
    """First-order book formula (2.65)."""
    return (qb * eps / (2 * (a - b))) * (b * np.log((b - a) / (a + b))
                                         + a * np.log(4 * b * b / (b * b - a * a)))


# ---------------------------------------------------------------------------
# P11  (2.5.2)  Cavendish with Yukawa exp(-r/R)/r
# ---------------------------------------------------------------------------

def phi_shell_yukawa(r, s, q, R):
    """Uniform shell, Yukawa kernel: (qR/2sr) [e^{-|r-s|/R} - e^{-(r+s)/R}]."""
    return q * R / (2 * s * r) * (np.exp(-abs(r - s) / R) - np.exp(-(r + s) / R))


def phi_shell_yukawa_quad(r, s, q, R):
    sig = q / (4 * np.pi * s * s)

    def integrand(mu):
        u = np.sqrt(r * r + s * s - 2 * r * s * mu)
        return 2 * np.pi * s * s * sig * np.exp(-u / R) / u

    val, _ = quad(integrand, -1, 1, limit=400)
    return val


def qa_yukawa(a, b, qb, R):
    """Book ratio formula for the wired shells (exercise answer)."""
    num = (a / b) * (1 - np.exp(-2 * b / R)) - np.exp((a - b) / R) + np.exp(-(a + b) / R)
    den = (b / a) * (1 - np.exp(-2 * a / R)) - np.exp((a - b) / R) + np.exp(-(a + b) / R)
    return qb * num / den


def qa_yukawa_solve(a, b, qb, R):
    """Independent route: solve Phi(a) = Phi(b) linearly in q_a."""
    ca = phi_shell_yukawa(a, a, 1.0, R) - phi_shell_yukawa(b, a, 1.0, R)
    cb = phi_shell_yukawa(a, b, 1.0, R) - phi_shell_yukawa(b, b, 1.0, R)
    return -qb * cb / ca


def qa_yukawa_approx(a, b, qb, R):
    """R >> a,b:  q_a ~ q_b (ab/6R^2)(1 + a/b)."""
    return qb * a * b / (6 * R * R) * (1 + a / b)


# ---------------------------------------------------------------------------
# P12  (2.6.1)  charged conducting disk
# ---------------------------------------------------------------------------

def phi_disk(rho, z, R, V):
    """Disk (radius R, potential V) potential in cylindrical (rho, z),
    spherical-form expression with A = 2V/pi."""
    r2 = rho * rho + z * z
    inner = (r2 - R * R) + np.sqrt((r2 - R * R) ** 2 + 4 * R * R * z * z)
    A = 2 * V / np.pi
    if inner <= 0:          # on the disk plane inside the rim
        return V
    return A * np.arctan(np.sqrt(2.0) * R / np.sqrt(inner))


def phi_disk_oblate(xi, V):
    """Same in oblate spheroidal form: (2V/pi) atan(1/xi)."""
    return 2 * V / np.pi * np.arctan(1.0 / xi) if xi > 0 else V


def sigma_disk(rho, R, V):
    """Two-sided surface density V / (pi^2 sqrt(R^2-rho^2))."""
    return V / (np.pi ** 2 * np.sqrt(R * R - rho * rho))


def disk_total_charge(R, V):
    """Q = integral sigma dA = 2 R V / pi (closed form via quadrature)."""
    val, _ = quad(lambda r: 2 * np.pi * r * sigma_disk(r, R, V), 0, R,
                  limit=400, points=[R])
    return val


def disk_capacitance(R):
    """C = 2R/pi (isolated thin disk)."""
    return 2 * R / np.pi


# ---------------------------------------------------------------------------
# P13/P14/P15  (2.6.2-2.6.4)  dipole layers
# ---------------------------------------------------------------------------

def phi_disk_monolayer_axis(z, a, sigma=1.0):
    """On-axis potential of a single charged disk: 2 pi sigma (sqrt(a^2+z^2)-|z|)."""
    return 2 * np.pi * sigma * (np.hypot(a, z) - abs(z))


def phi_dipole_disk_axis(z, a, D=1.0):
    """On-axis potential of a dipole disk (normal +z):
    2 pi D [sgn z - z/sqrt(z^2+a^2)]."""
    return 2 * np.pi * D * (np.sign(z) - z / np.hypot(z, a))


def phi_two_disks_axis(z, a, D, d):
    """Two charged disks +-sigma = +-D/d at z = +-d/2 (exact two-layer)."""
    sig = D / d
    return (phi_disk_monolayer_axis(z - d / 2, a, sig)
            - phi_disk_monolayer_axis(z + d / 2, a, sig))


def phi_hemisphere_dipole_axis(z, a, D=1.0):
    """On-axis potential of a uniform dipole hemisphere (radius a, rim at z=0,
    outward normal): 2 pi D [+-1 - z/sqrt(z^2+a^2)], + for z>a, - for z<a."""
    s = 1.0 if z > a else -1.0
    return 2 * np.pi * D * (s - z / np.hypot(z, a))


def phi_cap_dipole_axis_quad(z, a, D=1.0, mu_lo=0.0, mu_hi=1.0):
    """Quadrature of the layer integral D  n'.(x-x')/|x-x'|^3 da' over the
    spherical cap mu in [mu_lo, mu_hi] of radius a (on-axis field point z)."""
    def integrand(mu):
        num = z * mu - a
        den = (z * z + a * a - 2 * a * z * mu) ** 1.5
        return 2 * np.pi * a * a * D * num / den

    val, _ = quad(integrand, mu_lo, mu_hi, limit=400)
    return val


def Ez_dipole_cap_axis(z, a, D=1.0):
    """Axis field of hemisphere or disk dipole layer: 2 pi D a^2/(z^2+a^2)^{3/2}."""
    return 2 * np.pi * D * a * a / (z * z + a * a) ** 1.5


def phi_dipole_sphere(r, a, D=1.0):
    """Uniform dipole sphere (outward normal): -4 pi D inside, 0 outside."""
    return -4 * np.pi * D if r < a else 0.0


def phi_disk_offcenter(field_pt, a, sigma=1.0, n=200):
    """Potential of a uniform disk (radius a, z=0 plane, centered O) at an
    arbitrary field point, by 2-D quadrature (polar grid on the disk)."""
    fx, fy, fz = field_pt
    r = np.linspace(0.0, a, n + 1)[1:] - a / (2 * n)   # midpoints
    th = np.linspace(0.0, 2 * np.pi, 2 * n, endpoint=False)
    Rg, Tg = np.meshgrid(r, th)
    xs, ys = Rg * np.cos(Tg), Rg * np.sin(Tg)
    dA = (a / n) * (2 * np.pi / (2 * n)) * Rg
    dist = np.sqrt((fx - xs) ** 2 + (fy - ys) ** 2 + fz ** 2)
    return sigma * np.sum(dA / dist)


def E_disk_offcenter(field_pt, a, sigma=1.0, n=200, h=1e-4):
    """Field of the uniform disk at a general point (numeric gradient)."""
    f = lambda p: phi_disk_offcenter(p, a, sigma, n)
    p = np.asarray(field_pt, float)
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3); e[i] = h
        g[i] = (f(p + e) - f(p - e)) / (2 * h)
    return -g


def phi_pair_offset(field_pt, a, D, d, xhat, n=200):
    """Two disks +-sigma = +-D/d; the negative copy sits at x' - xhat d, so the
    pair's dipole moment points along +xhat:
    Phi(x) = Phi2(x) - Phi2(x + xhat d) ~= +xhat.E2(x) d."""
    p = np.asarray(field_pt, float)
    xhat = np.asarray(xhat, float)
    sig = D / d
    return (phi_disk_offcenter(p, a, sig, n)
            - phi_disk_offcenter(p + xhat * d, a, sig, n))


# ---------------------------------------------------------------------------
# P16  (2.7.1)  Green's first identity on a ball (radial closed forms)
# ---------------------------------------------------------------------------

def green_identity_sides(phi, dphi, psi, dpsi, ddpsi, R):
    """Both sides of Green's first identity for radial phi(r), psi(r) on the
    ball r <= R.  laplacian psi = psi'' + 2 psi'/r."""
    def lap_psi(r):
        return ddpsi(r) + 2.0 * dpsi(r) / r

    lhs, _ = quad(lambda r: (phi(r) * lap_psi(r) + dphi(r) * dpsi(r)) * 4 * np.pi * r * r,
                  0, R, limit=400)
    rhs = phi(R) * dpsi(R) * 4 * np.pi * R * R
    return lhs, rhs


# ---------------------------------------------------------------------------
# P17  (2.7.2)  reciprocation: point charge between grounded shells
# ---------------------------------------------------------------------------

def induced_charges_shells(q, r, a, b):
    """Reciprocation result: (Q_a, Q_b) for q at radius r between grounded
    concentric shells a < r < b."""
    Qa = -q * a * (b - r) / (r * (b - a))
    Qb = -q * b * (r - a) / (r * (b - a))
    return Qa, Qb


def induced_charges_shells_gauss(q, r, a, b):
    """Independent construction: radial l=0 potential
    Phi = alpha (1/s - 1/a) [s<r],  beta (1/s - 1/b) [s>r];
    Gauss: alpha = Q_a, beta = q + Q_a; continuity at s=r fixes Q_a:
    alpha [(1/r-1/a)-(1/r-1/b)] = q (1/r-1/b)."""
    Qa = q * (1.0 / r - 1.0 / b) / (1.0 / b - 1.0 / a)
    Qb = -q - Qa            # total induced = -q
    return Qa, Qb


# ---------------------------------------------------------------------------
# P18  (2.7.3)  mean value theorem
# ---------------------------------------------------------------------------

def sphere_average(f, center, R, n_mu=48, n_phi=96):
    """Average of f over the sphere |x - center| = R (Gauss-Legendre in mu)."""
    mu, wmu = np.polynomial.legendre.leggauss(n_mu)
    phi = np.linspace(0.0, 2 * np.pi, n_phi, endpoint=False)
    c = np.asarray(center, float)
    tot = 0.0
    for m, w in zip(mu, wmu):
        s = np.sqrt(1 - m * m)
        for p in phi:
            x = c + R * np.array([s * np.cos(p), s * np.sin(p), m])
            tot += w * f(x)
    return tot / (2.0 * n_phi)          # sum w = 2; phi weight 2pi/n / (4pi)


# ---------------------------------------------------------------------------
# P19/P20/P22/P23/P24  (2.8.1-2, 2.9.1-3)  1-D Green functions
# ---------------------------------------------------------------------------

def gd1(x, xp, L):
    """1-D Dirichlet Green function x_<(1 - x_>/L)   (2.136)."""
    lo, hi = min(x, xp), max(x, xp)
    return lo * (1.0 - hi / L)


def dgd1_dnp(end, x, L):
    """Outward-normal derivative of gd1(x', x) in x' at endpoint x'=end."""
    if end == 0:
        return -(1.0 - x / L)      # n' = -d/dx'
    return -x / L                  # n' = +d/dx' at L, dG/dx' = -x/L


def gn1_unsym(x, xp, L):
    """Unsymmetrized 1-D Neumann GF with (2.137) BCs and G(0,x')=0 choice:
    x/2 (x<x'), x'-x/2 (x>x')."""
    return x / 2.0 if x < xp else xp - x / 2.0


def gn1_symm(x, xp, L):
    """Symmetric 1-D Neumann GF  -|x-x'|/2 + L/4   (2.139 with C=L/4)."""
    return -abs(x - xp) / 2.0 + L / 4.0


def gn_gd_identity_rhs(x, xpp, L, gn=gn1_unsym):
    """1-D analog of the P19 identity's right side:
    G_D(x'', x) - sum_endpoints G_N(x', x'') dG_D(x', x)/dn'."""
    s = gd1(xpp, x, L)
    for end in (0.0, L):
        s -= gn(end, xpp, L) * dgd1_dnp(end, x, L)
    return s


def force_gd(xp, L):
    """P22a: F = E_avg q = x'/L - 1/2 (unit charge)."""
    return xp / L - 0.5


def induced_endpoint_charges(xp, L):
    """P22b: (sigma_0, sigma_L) = (x'/L - 1, -x'/L)."""
    return xp / L - 1.0, -xp / L


def phi_dirichlet_rep(x, L, V0, VL, lam_func=None, n=2000):
    """(2.127): Phi = int G_D lam dx' - [Phi dG/dx']_0^L."""
    val = 0.0
    if lam_func is not None:
        xs = np.linspace(0.0, L, n)
        val += trapz(np.array([gd1(x, xp, L) * lam_func(xp) for xp in xs]), xs)
    # boundary term: -[Phi(L) dG/dx'|_L - Phi(0) dG/dx'|_0], dG/dx' at L = -x/L,
    # at 0 = 1 - x/L
    val -= (VL * (-x / L) - V0 * (1.0 - x / L))
    return val


def phi_neumann_rep(x, L, dphi0, dphiL, lam_func=None, mean=0.0, gn=gn1_symm, n=2000):
    """(2.138): Phi = int G_N lam + [G_N dPhi/dx']_0^L + <Phi>."""
    val = mean
    if lam_func is not None:
        xs = np.linspace(0.0, L, n)
        val += trapz(np.array([gn(x, xp, L) * lam_func(xp) for xp in xs]), xs)
    val += gn(x, L, L) * dphiL - gn(x, 0.0, L) * dphi0
    return val


def phi_293(x, L, V, lam):
    """P24 closed form: lam x(L-x)/2 + V(1 - 2x/L)."""
    return lam * x * (L - x) / 2.0 + V * (1.0 - 2.0 * x / L)


# ---------------------------------------------------------------------------
# P21  (2.8.3)  cube relaxation (polyhedron face-average theorem, n=6)
# ---------------------------------------------------------------------------

def cube_center_potential(v_faces, n=25, iters=3000):
    """Solve Laplace in the unit cube with the six faces at v_faces =
    (x0, x1, y0, y1, z0, z1) potentials; return the center value (Jacobi).
    Edge/corner nodes get the *average* of their adjacent faces, so the six
    single-hot-face problems are exact rotations of one another."""
    u = np.zeros((n, n, n))
    S = np.zeros((n, n, n)); cnt = np.zeros((n, n, n))
    slabs = [np.s_[0, :, :], np.s_[-1, :, :], np.s_[:, 0, :],
             np.s_[:, -1, :], np.s_[:, :, 0], np.s_[:, :, -1]]
    for sl, v in zip(slabs, v_faces):
        S[sl] += v
        cnt[sl] += 1.0
    mask = cnt > 0
    u[mask] = S[mask] / cnt[mask]
    for _ in range(iters):
        u[1:-1, 1:-1, 1:-1] = (u[:-2, 1:-1, 1:-1] + u[2:, 1:-1, 1:-1]
                               + u[1:-1, :-2, 1:-1] + u[1:-1, 2:, 1:-1]
                               + u[1:-1, 1:-1, :-2] + u[1:-1, 1:-1, 2:]) / 6.0
    m = n // 2
    return u[m, m, m]


# ---------------------------------------------------------------------------
# P25  (2.9.4)  1-D Helmholtz Green function
# ---------------------------------------------------------------------------

def g_helmholtz(x, xp, L, k0):
    """sin(k0 x_<) sin(k0 (L - x_>)) / (k0 sin k0 L)."""
    lo, hi = min(x, xp), max(x, xp)
    return np.sin(k0 * lo) * np.sin(k0 * (L - hi)) / (k0 * np.sin(k0 * L))


def phi_helmholtz_direct(x, L, k0, lam):
    """Phi'' + k0^2 Phi = -lam (const), Phi(0)=Phi(L)=0:
    (lam/k0^2) [cos(k0(x - L/2))/cos(k0 L/2) - 1]."""
    return lam / k0 ** 2 * (np.cos(k0 * (x - L / 2)) / np.cos(k0 * L / 2) - 1.0)


def phi_helmholtz_gf(x, L, k0, lam, n=4000):
    xs = np.linspace(0.0, L, n)
    return trapz(np.array([g_helmholtz(x, xp, L, k0) * lam for xp in xs]), xs)


# ---------------------------------------------------------------------------
# P26-P29  (2.10.x)  energies
# ---------------------------------------------------------------------------

def energy_sphere_alone(Q, a):
    """W = Q^2/2a (conducting sphere / shell)."""
    return Q * Q / (2 * a)


def energy_sphere_with_neutral_shell(Q, a, b, c):
    """Sphere Q radius a inside a neutral conducting shell (b, c):
    W = Q^2/2 (1/a - 1/b + 1/c)."""
    return Q * Q / 2 * (1.0 / a - 1.0 / b + 1.0 / c)


def energy_field_quad(E_of_r, rmax, rmin=0.0, n=200000):
    """W = (1/8pi) int E^2 4 pi r^2 dr on [rmin, rmax] (scalar E_of_r)."""
    r = np.linspace(rmin, rmax, n)[1:]
    E = np.array([E_of_r(x) for x in r])
    return trapz(E * E * r * r, r) / 2.0


def string_self_energy(a, delta, lam=1.0):
    """Cutoff self-energy of a uniform segment:
    lam^2 [a ln(a/delta) - a + delta]  (exact for the cutoff |x-x'|>delta)."""
    return lam * lam * (a * np.log(a / delta) - a + delta)


def string_self_energy_quad(a, delta, lam=1.0):
    """Direct double quadrature with the same cutoff."""
    def inner(x):                       # int_{|x'-x|>delta, x' in [0,a]} dx'/|x'-x|
        v = 0.0
        if x + delta < a:
            v += np.log((a - x) / delta)
        if x - delta > 0:
            v += np.log(x / delta)
        return v
    val, _ = quad(inner, 0, a, limit=400)
    return lam * lam * val / 2.0        # W = (lam^2/2) * double integral


def square_sheet_coeff_exact():
    """W R / Q^2 for the uniform square sheet:
    2 ln(1+sqrt 2) + (2/3)(1 - sqrt 2) = 1.4866..."""
    return 2 * np.log(1 + np.sqrt(2.0)) + 2.0 / 3.0 * (1 - np.sqrt(2.0))


def square_sheet_coeff_quad(n=400):
    """Quadrature of the reduced integral 2 * int (1-wx)(1-wy)/|w| d2w  (=I/2)."""
    w = (np.arange(n) + 0.5) / n
    WX, WY = np.meshgrid(w, w)
    F = (1 - WX) * (1 - WY) / np.hypot(WX, WY)
    return 2.0 * F.sum() / (n * n)


def ball_self_energy(alpha, Q=1.0, a=1.0):
    """W = (3+alpha)/(5+2 alpha) Q^2/a  for rho = C r^alpha, r <= a."""
    return (3.0 + alpha) / (5.0 + 2.0 * alpha) * Q * Q / a


def ball_self_energy_quad(alpha, Q=1.0, a=1.0, n=200000):
    """Field-energy quadrature: E = Q r^{1+alpha}/a^{3+alpha} in, Q/r^2 out."""
    r_in = np.linspace(0.0, a, n)[1:]
    E_in = Q * r_in ** (1.0 + alpha) / a ** (3.0 + alpha)
    W_in = trapz(E_in ** 2 * r_in ** 2, r_in) / 2.0
    W_out = Q * Q / (2.0 * a)
    return W_in + W_out


def classical_radius_uniform_cm():
    """a = (3/5) e^2/(m c^2) in cm (Gaussian cgs)."""
    e = 4.80320471e-10       # esu
    m = 9.1093837e-28        # g
    c = 2.99792458e10        # cm/s
    return 0.6 * e * e / (m * c * c)


# ---------------------------------------------------------------------------
# P30  (2.11.1)  sphere with rho and sigma; surface force
# ---------------------------------------------------------------------------

def E_sphere_rho_sigma(r, R, rho, sigma):
    """Radial field of a ball (rho) plus surface layer (sigma)."""
    if r < R:
        return 4 * np.pi * rho * r / 3.0
    Q = 4 * np.pi * R ** 3 * rho / 3.0 + 4 * np.pi * R * R * sigma
    return Q / (r * r)


def surface_force_per_area(R, rho, sigma):
    """F/A = sigma (4 pi rho R/3 + 2 pi sigma)  (average-field prescription)."""
    return sigma * (4 * np.pi * rho * R / 3.0 + 2 * np.pi * sigma)


# ---------------------------------------------------------------------------
# P31-P36  (2.12.1-6)  capacitance matrices
# ---------------------------------------------------------------------------

def elastance_shells(a, b, c):
    """P matrix: V_i = sum_j P_ij q_j for concentric shells a < b < c."""
    u, v, w = 1.0 / a, 1.0 / b, 1.0 / c
    return np.array([[u, v, w], [v, v, w], [w, w, w]])


def cap_matrix_shells(a, b, c):
    """Closed-form C matrix for three concentric shells."""
    Caa = a * b / (b - a)
    Cab = -a * b / (b - a)
    Cac = 0.0
    Cbb = b * b * (c - a) / ((b - a) * (c - b))
    Cbc = -b * c / (c - b)
    Ccc = c * c / (c - b)
    return np.array([[Caa, Cab, Cac], [Cab, Cbb, Cbc], [Cac, Cbc, Ccc]])


def cap_two_spheres(a, b):
    """2x2 C matrix for concentric spheres a < b (b hollow, sees infinity)."""
    g = a * b / (b - a)
    return np.array([[g, -g], [-g, g + b]])


def system_capacitance(C2):
    """P35: C = det C / sum_ij C_ij for a 2x2 block."""
    return np.linalg.det(C2) / C2.sum()


def energy_from_caps(C, V):
    """W = (1/2) V.C.V."""
    V = np.asarray(V, float)
    return 0.5 * V @ (C @ V)


def energy_at_charges(C, q):
    """W = (1/2) q.C^{-1}.q  (fixed charges)."""
    q = np.asarray(q, float)
    return 0.5 * q @ np.linalg.solve(C, q)


# ---------------------------------------------------------------------------
# P37-P39  (2.12.7-9)  parallel disks & distant conductors
# ---------------------------------------------------------------------------

def plates_C_small_d(R, d):
    """d << R: C = R^2/(4d)  (= A/4 pi d, A = pi R^2)."""
    return R * R / (4.0 * d)


def plates_C_large_d(R, d, order=1):
    """d >> R monopole model: exact 1/(pi/R - 2/d); order=1 gives
    (R/pi)(1 + 2R/(pi d))."""
    if order == 0:
        return R / np.pi
    if order == 1:
        return R / np.pi * (1.0 + 2.0 * R / (np.pi * d))
    return 1.0 / (np.pi / R - 2.0 / d)


def distant_pair_cap_matrix(C1, C2, d):
    """Invert the monopole elastance P = [[1/C1, 1/d], [1/d, 1/C2]]."""
    P = np.array([[1.0 / C1, 1.0 / d], [1.0 / d, 1.0 / C2]])
    return np.linalg.inv(P)


def C12_approx(C1, C2, d):
    """P39a: C12 ~ -C1 C2/d."""
    return -C1 * C2 / d


def C22_approx(C1, C2, d):
    """P39b: C22 ~ C2/(1 + C12/d)."""
    return C2 / (1.0 + C12_approx(C1, C2, d) / d)


# ---------------------------------------------------------------------------
# P40  (2.12.10)  variational capacitance, cylindrical capacitor
# ---------------------------------------------------------------------------

def cyl_trial_capacitance(a, b, L):
    """C[Psi] with Psi = (b-rho)/(b-a):  L (a+b)/(4(b-a))."""
    return L * (a + b) / (4.0 * (b - a))


def cyl_exact_capacitance(a, b, L):
    """C = L / (2 ln(b/a))."""
    return L / (2.0 * np.log(b / a))


def cyl_functional_quad(psi_prime, a, b, L, n=200000):
    """C[Psi] = (1/4 pi) int |grad Psi|^2 dV for radial Psi(rho)."""
    r = np.linspace(a, b, n)
    g = np.array([psi_prime(x) for x in r])
    return trapz(g * g * 2 * np.pi * r * L, r) / (4 * np.pi)


# ---------------------------------------------------------------------------
# P41  (2.12.11)  three parallel wires
# ---------------------------------------------------------------------------

def wire_potentials(lams, d, a, K=1.0):
    """V_i = -2 lam_i ln(a/K) - 2 sum_{j != i} lam_j ln(d/K)  (equilateral)."""
    lams = np.asarray(lams, float)
    V = np.empty(3)
    for i in range(3):
        V[i] = -2 * lams[i] * np.log(a / K)
        for j in range(3):
            if j != i:
                V[i] -= 2 * lams[j] * np.log(d / K)
    return V


def three_wire_CL(d, a):
    """C_L = 1/(12 ln(d/a))."""
    return 1.0 / (12.0 * np.log(d / a))


def three_wire_energy(lam, d, a):
    """w = 6 lam^2 ln(d/a) = lam^2/(2 C_L)."""
    return 6.0 * lam * lam * np.log(d / a)


# ---------------------------------------------------------------------------
# demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("MACRO_EM-02 demo (Gaussian units)")
    d = np.array([0.3, -1.1, 0.7]); x = np.array([1.2, 0.4, -0.9])
    print("P1  |E + grad Phi|      :", np.linalg.norm(dipole_E(d, x) - (-numeric_grad(lambda p: dipole_phi(d, p), x))))
    print("P6  2-D Gauss flux      :", flux2d(E2d_point, (0.3, -0.2), 1.0), "(expect 2 pi =", 2 * np.pi, ")")
    print("P12 disk capacitance    :", disk_capacitance(1.0), "(2R/pi)")
    print("P21 cube center (1 face):", cube_center_potential((1, 0, 0, 0, 0, 0)), "(expect 1/6)")
    print("P28 square sheet coeff  :", square_sheet_coeff_exact(), "(book: 1.48660)")
    print("P33 shell C matrix      :\n", cap_matrix_shells(1.0, 2.0, 3.0))
    print("P41 three-wire N        :", 1.0 / (three_wire_CL(50.0, 1.0) * np.log(50.0)), "(expect 12)")
