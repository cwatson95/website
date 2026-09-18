"""MACRO_EM-03 -- Boundary-value problems in electrostatics (Wilcox & Thron 2e, Ch. 3).

Numeric companions to the 33 exercises of Wilcox Sec. 3.13 (printed pp. 120-134).

Conventions (the book's, GAUSSIAN units):
  * potential of a unit point charge  Phi = 1/|x - x'|          (Eq. 3.1)
  * Green function equation           del^2 G = -4 pi delta     (Eq. 3.14)
  * Dirichlet representation (2.98):
        Phi(x) = int rho G_D d3x' - (1/4pi) oint Phi dG_D/dn' da'
  * surface charge on a conductor     sigma = (1/4pi) dPhi/dn   (Eq. 2.92)
  * 2-D (line-charge) free Green fn   G = -2 ln(rho/L)          (Eq. 3.11)

All reduced Green functions g follow the book's normalization
G = 4 pi int d2k/(2pi)^2 e^{i k.(x-x')_perp} g(k; z, z')  (Eqs. 3.23, 3.31).
"""
from functools import lru_cache

import numpy as np
from scipy import special
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

# ----------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------

def potential_of_charges(x, charges):
    """Phi(x) = sum_i q_i / |x - x_i|.  charges: list of (q, position)."""
    x = np.asarray(x, dtype=float)
    return sum(q / np.linalg.norm(x - np.asarray(p, dtype=float)) for q, p in charges)


def laplacian_fd(f, x, y, h=1e-4):
    """5-point numeric Laplacian of a callable f(x, y)."""
    return (f(x + h, y) + f(x - h, y) + f(x, y + h) + f(x, y - h) - 4.0 * f(x, y)) / h**2


def laplacian_polar_fd(f, rho, phi, h=1e-4):
    """Numeric polar Laplacian  f_rr + f_r/r + f_pp/r^2  of f(rho, phi)."""
    frr = (f(rho + h, phi) - 2 * f(rho, phi) + f(rho - h, phi)) / h**2
    fr = (f(rho + h, phi) - f(rho - h, phi)) / (2 * h)
    fpp = (f(rho, phi + h) - 2 * f(rho, phi) + f(rho, phi - h)) / h**2
    return frr + fr / rho + fpp / rho**2


def cauchy_riemann_residual(f, z, h=1e-6):
    """|u_x - v_y| + |u_y + v_x| for a complex map f(z), by central differences."""
    ux = (f(z + h) - f(z - h)).real / (2 * h)
    vx = (f(z + h) - f(z - h)).imag / (2 * h)
    uy = (f(z + 1j * h) - f(z - 1j * h)).real / (2 * h)
    vy = (f(z + 1j * h) - f(z - 1j * h)).imag / (2 * h)
    return abs(ux - vy) + abs(uy + vx)


@lru_cache(maxsize=32)
def _leggauss(n):
    """Cached raw Gauss-Legendre nodes (numpy's leggauss is O(n^3))."""
    return np.polynomial.legendre.leggauss(n)


def gauss_legendre(a, b, n):
    t, w = _leggauss(n)
    return 0.5 * (b - a) * t + 0.5 * (a + b), 0.5 * (b - a) * w


def gauss_panels(a, b, n_panels, n_per=64):
    """Composite Gauss rule: n_panels equal panels of n_per nodes each."""
    edges = np.linspace(a, b, n_panels + 1)
    xs, ws = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        x, w = gauss_legendre(lo, hi, n_per)
        xs.append(x); ws.append(w)
    return np.concatenate(xs), np.concatenate(ws)

# ----------------------------------------------------------------------------
# Sec. 3.1 -- conducting plane and corner images (P1-P5)
# ----------------------------------------------------------------------------

def green_plane(x, xp, kind="D"):
    """Half-space z>0 Green function, images (3.2)/(3.5): 1/|x-x'| -/+ 1/|x-x''|."""
    x = np.asarray(x, float); xp = np.asarray(xp, float)
    xm = xp * np.array([1.0, 1.0, -1.0])
    s = -1.0 if kind == "D" else +1.0
    return 1.0 / np.linalg.norm(x - xp) + s / np.linalg.norm(x - xm)


def corner_images(xp):
    """Unit charge in the quadrant x>0, y>0 bounded by grounded planes x=0, y=0
    (Ex. 3.1.2): three images."""
    xq, yq, zq = xp
    return [(+1.0, (xq, yq, zq)), (-1.0, (-xq, yq, zq)),
            (+1.0, (-xq, -yq, zq)), (-1.0, (xq, -yq, zq))]


def green_corner(x, xp):
    """Dirichlet Green function for the 3-D right-angle corner (Ex. 3.1.2a)."""
    return potential_of_charges(x, corner_images(xp))


def corner_work(xq, yq):
    """Work to pull the unit charge from (x', y') to infinity (Ex. 3.1.2b):
    W = (1/4) (1/x' + 1/y' - 1/sqrt(x'^2+y'^2))."""
    return 0.25 * (1.0 / xq + 1.0 / yq - 1.0 / np.hypot(xq, yq))


def corner_force(xq, yq):
    """Force on the unit charge from its corner images (full field, no 1/2)."""
    F = np.zeros(2)
    src = np.array([xq, yq])
    for q, p in [(-1.0, (-xq, yq)), (+1.0, (-xq, -yq)), (-1.0, (xq, -yq))]:
        d = src - np.array(p)
        F += q * d / np.linalg.norm(d) ** 3
    return F


def green_perp_2d(rho, phi, rhop, phip):
    """2-D Dirichlet Green function for perpendicular grounded planes phi=0, pi/2
    (Ex. 3.1.3 closed form):  ln[(r^4+r'^4-2r^2r'^2 cos 2(f+f')) /
                                 (r^4+r'^4-2r^2r'^2 cos 2(f-f'))]."""
    num = rho**4 + rhop**4 - 2 * rho**2 * rhop**2 * np.cos(2 * (phi + phip))
    den = rho**4 + rhop**4 - 2 * rho**2 * rhop**2 * np.cos(2 * (phi - phip))
    return np.log(num / den)


def green_perp_2d_images(rho, phi, rhop, phip):
    """Same Green function from the four image line charges, G = -2 sum q ln d."""
    x, y = rho * np.cos(phi), rho * np.sin(phi)
    xq, yq = rhop * np.cos(phip), rhop * np.sin(phip)
    out = 0.0
    for q, (px, py) in [(+1, (xq, yq)), (-1, (-xq, yq)), (+1, (-xq, -yq)), (-1, (xq, -yq))]:
        out += -2.0 * q * np.log(np.hypot(x - px, y - py))
    return out


def corner_wall_phi_exact(phi, V):
    """Quadrant with wall phi=0 at +V and wall phi=pi/2 at -V (Ex. 3.1.2c):
    Phi = V (1 - 4 phi/pi)  [the beta=pi/2 case of Eq. 3.152]."""
    return V * (1.0 - 4.0 * phi / np.pi)


def corner_wall_phi_quad(rho, phi, V, n=400):
    """Ex. 3.1.2c by quadrature of Phi = -(1/4pi) oint Phi_s dG/dn' dl' using the
    2-D corner Green function (the z' integral is already absorbed)."""
    t, w = gauss_legendre(1e-6, np.pi / 2 - 1e-6, n)
    rp = rho * np.tan(t)                     # maps (0, pi/2) -> (0, inf)
    drp = rho / np.cos(t) ** 2
    r2, rp2 = rho**2, rp**2
    # dG/dphi' at phi'=0 and phi'=pi/2 (analytic; N=D on the walls)
    dG0 = 8 * r2 * rp2 * np.sin(2 * phi) / (rho**4 + rp**4 - 2 * r2 * rp2 * np.cos(2 * phi))
    dGp = -8 * r2 * rp2 * np.sin(2 * phi) / (rho**4 + rp**4 + 2 * r2 * rp2 * np.cos(2 * phi))
    # wall phi'=0 (potential +V, outward normal -phi-hat):  dG/dn' = -(1/r') dG/dphi'
    # wall phi'=pi/2 (potential -V, outward normal +phi-hat): dG/dn' = +(1/r') dG/dphi'
    integ = (+V) * (-dG0 / rp) + (-V) * (+dGp / rp)
    return -np.sum(w * integ * drp) / (4 * np.pi)


def pendulum_energy(theta, e=1.0, L=1.0, D=2.0):
    """Image potential energy of the charged pendulum (Ex. 3.1.4):
    U = -e^2 / (4 h),  h = D - L cos(theta)."""
    return -e**2 / (4.0 * (D - L * np.cos(theta)))


def pendulum_omega(e=1.0, m=1.0, L=1.0, D=2.0):
    """Small-oscillation frequency (Ex. 3.1.4): omega = e / (2 (D-L) sqrt(m L))."""
    return e / (2.0 * (D - L) * np.sqrt(m * L))


def solid_angle_disk(z, R):
    """|Omega| subtended by a disk of radius R at height z on its axis."""
    return 2 * np.pi * (1.0 - abs(z) / np.hypot(z, R))


def solid_angle_rect(z, wx, wy):
    """|Omega| subtended by a rectangle |x|<wx, |y|<wy at (0,0,z) (closed form)."""
    return 4 * np.arctan(wx * wy / (abs(z) * np.sqrt(wx**2 + wy**2 + z**2)))


def solid_angle_quad(x, patch="disk", R=1.0, wx=1.0, wy=1.0, n=400):
    """|Omega(x)| = |int_patch z da' / r^3| by Gauss-Legendre quadrature (Ex. 3.1.5)."""
    X, Y, Z = x
    if patch == "disk":
        r, wr = gauss_legendre(0.0, R, n)
        t, wt = gauss_legendre(0.0, 2 * np.pi, n)
        Rg, Tg = np.meshgrid(r, t, indexing="ij")
        W = np.outer(wr, wt) * Rg
        xs, ys = Rg * np.cos(Tg), Rg * np.sin(Tg)
    else:
        xs1, wx1 = gauss_legendre(-wx, wx, n)
        ys1, wy1 = gauss_legendre(-wy, wy, n)
        xs, ys = np.meshgrid(xs1, ys1, indexing="ij")
        W = np.outer(wx1, wy1)
    r3 = ((X - xs) ** 2 + (Y - ys) ** 2 + Z**2) ** 1.5
    return abs(np.sum(W * Z / r3))


def patch_potential(x, V, **kw):
    """Ex. 3.1.5:  Phi(x) = (V / 2 pi) |Omega(x)|."""
    return V * solid_angle_quad(x, **kw) / (2 * np.pi)

# ----------------------------------------------------------------------------
# Sec. 3.2 -- reduced Green functions for flat conductors (P6-P9)
# ----------------------------------------------------------------------------

def gf_regulated(R, eps):
    """Free Green function with convergence factor e^{-k eps} (Ex. 3.2.1):
    G_eps(R) = (2/(pi R)) arctan(R/eps)  ->  1/R as eps -> 0+."""
    return 2.0 / (np.pi * R) * np.arctan(R / eps)


def gf_regulated_quad(R, eps, n=40):
    """Ex. 3.2.1 done in the stated order: k-integral first (analytic,
    int_0^inf e^{k(i R mu - eps)} dk = 1/(eps - i R mu)), then numeric mu-integral."""
    mu, w = gauss_panels(-1.0, 1.0, n)
    return np.sum(w * (eps / (eps**2 + R**2 * mu**2))) / np.pi


def g_reduced_halfspace(k, z, zp, kind="D", h=None):
    """Reduced Green function for the half space z>0 (Eq. 3.30 and Ex. 3.2.2/3.2.4):
    g = (1/2k) [e^{-k|z-z'|} + s e^{-k(z+z')}], s = -1 (D), +1 (N),
    (hk-1)/(hk+1) (Robin, Ex. 3.2.4)."""
    if kind == "D":
        s = -1.0
    elif kind == "N":
        s = 1.0
    else:
        s = (h * k - 1.0) / (h * k + 1.0)
    return (np.exp(-k * abs(z - zp)) + s * np.exp(-k * (z + zp))) / (2 * k)


def green_halfspace_kspace(rho, z, zp, kind="D", h=None, kmax=80.0, n=60):
    """G = 2 int_0^inf k J0(k rho) g(k; z, z') dk  (Fourier inversion of 3.31)."""
    k, w = gauss_panels(1e-9, kmax, n)
    return 2.0 * np.sum(w * k * special.j0(k * rho) * g_reduced_halfspace(k, z, zp, kind, h))


def neumann_surface_delta_family(rho, z):
    """(1/4pi) dG_N/dn with the source moved onto the plane first (Ex. 3.2.2b):
    (1/4pi) * 2 z / (rho^2 + z^2)^{3/2}  -- a delta family as z -> 0+ (Eq. 2.115)."""
    return 2.0 * z / (rho**2 + z**2) ** 1.5 / (4 * np.pi)


def robin_bvp_fd(k, zp, h, zmax=12.0, n=6000):
    """Finite-difference solve of (k^2 - d^2/dz^2) g = delta(z-z') on z>0 with
    Robin condition g(0) = h g'(0) (i.e. (G + h dG/dn)|_S = 0 with n = -z-hat).
    Returns (grid, g)."""
    dz = zmax / n
    z = np.arange(n + 1) * dz
    A = lil_matrix((n + 1, n + 1))
    rhs = np.zeros(n + 1)
    for i in range(1, n):
        A[i, i - 1] = -1.0 / dz**2
        A[i, i] = 2.0 / dz**2 + k**2
        A[i, i + 1] = -1.0 / dz**2
    j = int(round(zp / dz))
    rhs[j] = 1.0 / dz
    # Robin row: g0 - h (g1 - g0)/dz = 0  (first order suffices at this dz)
    A[0, 0] = 1.0 + h / dz
    A[0, 1] = -h / dz
    A[n, n] = 1.0                                  # far Dirichlet g(zmax)=0
    return z, spsolve(csr_matrix(A), rhs)

# ----------------------------------------------------------------------------
# Sec. 3.1/3.2 -- parallel grounded plates z=0, z=a (P1, P8)
# ----------------------------------------------------------------------------

def plate_images(zp, a, N=60):
    """Image charges for a unit charge at height z' between grounded plates
    (Ex. 3.1.1): +1 at 2na+z', -1 at 2na-z', n in Z."""
    out = []
    for n in range(-N, N + 1):
        out.append((+1.0, 2 * n * a + zp))
        out.append((-1.0, 2 * n * a - zp))
    return out


def green_plates_images(rho, z, zp, a, N=60):
    """Parallel-plate Dirichlet Green function as the image sum (grouped by n)."""
    n = np.arange(-N, N + 1)[:, None]
    rho = np.atleast_1d(rho)[None, :]
    term = (1.0 / np.sqrt(rho**2 + (z - 2 * n * a - zp) ** 2)
            - 1.0 / np.sqrt(rho**2 + (z - 2 * n * a + zp) ** 2))
    out = term.sum(axis=0)
    return out[0] if out.size == 1 else out


def g_reduced_plates(k, z, zp, a):
    """Reduced Green function between plates (Ex. 3.2.3a):
    g = sinh(k z<) sinh(k (a - z>)) / (k sinh k a)   [exp-stable form]."""
    k = np.asarray(k, dtype=float)
    zl, zg = min(z, zp), max(z, zp)
    return (np.exp(-k * (zg - zl)) * (1 - np.exp(-2 * k * zl))
            * (1 - np.exp(-2 * k * (a - zg))) / (2 * k * (1 - np.exp(-2 * k * a))))


def green_plates_kspace(rho, z, zp, a, kmax=None, n=80):
    """G_D between plates via 2 int k J0(k rho) g dk -- cross-check of Ex. 3.1.1/3.2.3."""
    if kmax is None:
        scale = min(abs(z - zp), 2 * min(z, zp, a - z, a - zp))
        kmax = min(80.0 / max(scale, 1e-3), 2000.0)
    k, w = gauss_panels(1e-9, kmax, n)
    g = g_reduced_plates(k, z, zp, a)
    return 2.0 * np.sum(w * k * special.j0(k * rho) * g)


def plate_induced_charge(zp, a, plate="bottom"):
    """Ex. 3.2.3b:  Q|z=0 = -(1 - z'/a),  Q|z=a = -z'/a."""
    return -(1.0 - zp / a) if plate == "bottom" else -zp / a


def plate_induced_charge_quad(zp, a, plate="bottom", rho_max=None, n=600, N=1500):
    """Total induced charge by radial quadrature of sigma = (1/4pi) dPhi/dn over
    the plate, using the image-sum Green function.  rho_max stays modest: the
    true sigma is exponentially screened (~e^{-pi rho/a}) while the truncated
    image sum leaves an O(1/N^2) plateau that 2 pi rho would amplify."""
    if rho_max is None:
        rho_max = 6.0 * a
    rho, w = gauss_legendre(0.0, rho_max, n)
    dz = 1e-5 * a
    if plate == "bottom":       # outward normal of the gap volume is -z-hat
        dGdn = -(green_plates_images(rho, dz, zp, a, N)
                 - green_plates_images(rho, 0.0, zp, a, N)) / dz
    else:
        dGdn = (green_plates_images(rho, a, zp, a, N)
                - green_plates_images(rho, a - dz, zp, a, N)) / dz
    sigma = dGdn / (4 * np.pi)
    return np.sum(w * 2 * np.pi * rho * sigma)


def plate_wall_phi_quad(z, a, V, rho_max=None, n=600, N=1500):
    """Potential between plates with the z=0 plate at V, z=a grounded, via
    Phi = -(1/4pi) int da' V dG/dn'  ->  V (1 - z/a)  (used for C = A/(4 pi a)).
    Same rho_max/N considerations as plate_induced_charge_quad."""
    if rho_max is None:
        rho_max = 6.0 * a
    rho, w = gauss_legendre(0.0, rho_max, n)
    dz = 1e-5 * a
    dGdn = -(green_plates_images(rho, z, dz, a, N)
             - green_plates_images(rho, z, 0.0, a, N)) / dz
    return -np.sum(w * 2 * np.pi * rho * dGdn) * V / (4 * np.pi)

# ----------------------------------------------------------------------------
# Sec. 3.3 -- spheres and cylinders by images (P10-P17)
# ----------------------------------------------------------------------------

def sphere_image(q, rp, a):
    """Image of charge q at position vector rp for a grounded sphere of radius a
    (Eq. 3.46): q' = -q a/r' at (a^2/r'^2) rp.  Works inside and outside."""
    rp = np.asarray(rp, float)
    r = np.linalg.norm(rp)
    return -q * a / r, (a**2 / r**2) * rp


def green_sphere(x, xp, a):
    """Grounded-sphere Dirichlet Green function (Eq. 3.48), inside or outside."""
    qi, xi = sphere_image(1.0, xp, a)
    return potential_of_charges(x, [(1.0, xp), (qi, xi)])


def neutral_shell_phi(x, xp, a):
    """Ex. 3.3.1b: unit charge at xp inside a NEUTRAL thin conducting shell r=a.
    Inside: image solution + 1/a; outside: 1/r, independent of xp."""
    r = np.linalg.norm(np.asarray(x, float))
    if r <= a:
        return green_sphere(x, xp, a) + 1.0 / a
    return 1.0 / r


def hemisphere_boss_images(xp, a):
    """Images for a grounded plane z=0 with a grounded hemispherical boss r=a
    (Ex. 3.3.2): sphere image, plane image, sphere image of the plane image."""
    xp = np.asarray(xp, float)
    xm = xp * np.array([1.0, 1.0, -1.0])
    qs, xs = sphere_image(1.0, xp, a)
    qsm, xsm = sphere_image(-1.0, xm, a)
    return [(1.0, xp), (qs, xs), (-1.0, xm), (qsm, xsm)]


def green_hemisphere_boss(x, xp, a):
    return potential_of_charges(x, hemisphere_boss_images(xp, a))


def rho_star(rho_func, r, th, ph, a):
    """Image charge density of Ex. 3.3.3a: rho*(r,th,ph) = -(a/r)^5 rho(a^2/r,th,ph)."""
    return -((a / r) ** 5) * rho_func(a**2 / r, th, ph)


def image_cloud(charges, a):
    """Point-charge image cloud (per-element image rule) for a grounded sphere."""
    return [sphere_image(q, p, a) for q, p in charges]


def rho_star_total_charge(rho_func, a, r1, r2, nr=400, nt=200):
    """Q* = int rho* d3x  by quadrature -- must equal -int (a/r') rho d3x'."""
    # image cloud occupies a^2/r2 .. a^2/r1
    s, ws = gauss_legendre(a**2 / r2, a**2 / r1, nr)
    ct, wt = gauss_legendre(-1.0, 1.0, nt)
    S, CT = np.meshgrid(s, ct, indexing="ij")
    W = np.outer(ws, wt) * 2 * np.pi
    TH = np.arccos(CT)
    vals = rho_star(rho_func, S, TH, 0.0, a) * S**2
    return np.sum(W * vals)


def direct_weighted_charge(rho_func, a, r1, r2, nr=400, nt=200):
    """-int (a/r) rho(r,th,ph) d3x over r1<r<r2 (axisymmetric rho)."""
    r, wr = gauss_legendre(r1, r2, nr)
    ct, wt = gauss_legendre(-1.0, 1.0, nt)
    R, CT = np.meshgrid(r, ct, indexing="ij")
    W = np.outer(wr, wt) * 2 * np.pi
    TH = np.arccos(CT)
    return -np.sum(W * (a / R) * rho_func(R, TH, 0.0) * R**2)


def two_sphere_C(a, b, d, niter=200):
    """Iterated-image capacitance coefficients for spheres (radius a at 0, radius
    b at d, d > a+b).  Returns (C11, C21): total charges with sphere 1 at V=1,
    sphere 2 at V=0.  (Ex. 3.3.4 checks the d >> a,b asymptotics.)"""
    C11, C21 = 0.0, 0.0
    q, x = a, 0.0                       # seed: isolated sphere 1 at V=1
    C11 += q
    for _ in range(niter):
        q, x = -b * q / (d - x), d - b**2 / (d - x)   # image in sphere 2
        C21 += q
        q, x = -a * q / x, a**2 / x                    # image back in sphere 1
        C11 += q
        if abs(q) < 1e-16:
            break
    return C11, C21


def two_sphere_C_matrix(a, b, d, niter=200):
    C11, C21 = two_sphere_C(a, b, d, niter)
    C22, C12 = two_sphere_C(b, a, d, niter)
    return np.array([[C11, 0.5 * (C12 + C21)], [0.5 * (C12 + C21), C22]])


def two_sphere_C_system(a, b, d, niter=200):
    """Capacitance C = |Q/DV| for charges +Q/-Q on the two spheres (exact via P^-1)."""
    P = np.linalg.inv(two_sphere_C_matrix(a, b, d, niter))
    return 1.0 / (P[0, 0] - 2 * P[0, 1] + P[1, 1])


def csys_approx(a, b, d):
    """Ex. 3.3.4b:  C ~ ab / (a + b - 2ab/d)."""
    return a * b / (a + b - 2 * a * b / d)


def green_cylinder(rho, phi, rhop, phip, a):
    """2-D Dirichlet Green function for a grounded cylinder rho=a (Ex. 3.3.5b):
    G = ln[(a^4 + r^2 r'^2 - 2 a^2 r r' cos df) / (a^2 (r^2 + r'^2 - 2 r r' cos df))].
    Valid inside AND outside (Ex. 3.3.5c)."""
    c = np.cos(phi - phip)
    num = a**4 + rho**2 * rhop**2 - 2 * a**2 * rho * rhop * c
    den = a**2 * (rho**2 + rhop**2 - 2 * rho * rhop * c)
    return np.log(num / den)


def green_cylinder_images(rho, phi, rhop, phip, a):
    """Same from the image construction: -2 ln d + 2 ln d'' + 2 ln(rho'/a)."""
    c = np.cos(phi - phip)
    d1 = np.sqrt(rho**2 + rhop**2 - 2 * rho * rhop * c)
    rim = a**2 / rhop
    d2 = np.sqrt(rho**2 + rim**2 - 2 * rho * rim * c)
    return -2 * np.log(d1) + 2 * np.log(d2) + 2 * np.log(rhop / a)


def shell_grounded_sphere_phi(r, a, b, Q):
    """Ex. 3.3.6: uniform shell (radius b, charge Q) around a grounded sphere a:
    Phi = 0 (r<=a);  (Q/b)(1 - a/r) (a<=r<=b);  Q (1 - a/b)/r (r>=b)."""
    r = np.asarray(r, float)
    return np.where(r <= a, 0.0,
                    np.where(r <= b, (Q / b) * (1 - a / r), Q * (1 - a / b) / r))


def shell_grounded_sphere_quad(r_obs, a, b, Q, n=400):
    """Same by quadrature of sigma_b * G_sphere over the shell surface."""
    sig = Q / (4 * np.pi * b**2)
    ct, w = gauss_legendre(-1.0, 1.0, n)
    x = np.array([0.0, 0.0, r_obs])
    tot = 0.0
    for c, ww in zip(ct, w):
        xp = b * np.array([np.sqrt(1 - c**2), 0.0, c])
        tot += ww * 2 * np.pi * b**2 * sig * green_sphere(x, xp, a)
    return tot


def ring_sphere_phi_axis(z, a, b, lam):
    """Ex. 3.3.7b: ring (radius b, density lam) around a grounded sphere a, on-axis:
    Phi(z) = 2 pi b lam / sqrt(z^2+b^2) - 2 pi a lam / sqrt(z^2 + a^4/b^2)."""
    return (2 * np.pi * b * lam / np.hypot(z, b)
            - 2 * np.pi * a * lam / np.sqrt(z**2 + a**4 / b**2))


def ring_sphere_phi_axis_quad(z, a, b, lam, n=400):
    """Same by quadrature of lam b dphi' G_sphere along the ring."""
    t, w = gauss_legendre(0.0, 2 * np.pi, n)
    x = np.array([0.0, 0.0, z])
    tot = 0.0
    for tt, ww in zip(t, w):
        xp = np.array([b * np.cos(tt), b * np.sin(tt), 0.0])
        tot += ww * lam * b * green_sphere(x, xp, a)
    return tot


def force_sphere_V(q, V, a, d):
    """Ex. 3.3.8a: radial force on q at distance d from a sphere held at V:
    F = q V a / d^2 - q^2 a d / (d^2 - a^2)^2."""
    return q * V * a / d**2 - q**2 * a * d / (d**2 - a**2) ** 2


def V_zero_force(q, a, d):
    """Potential that makes the Ex. 3.3.8a force vanish: V = q d^3/(d^2-a^2)^2."""
    return q * d**3 / (d**2 - a**2) ** 2


def force_sphere_neutral(q, a, d):
    """Ex. 3.3.8b: force from a neutral isolated sphere:
    F = q^2 a [1/d^3 - d/(d^2-a^2)^2]  = -q^2 a^3 (2d^2-a^2) / (d^3 (d^2-a^2)^2)."""
    return q**2 * a * (1.0 / d**3 - d / (d**2 - a**2) ** 2)


def energy_sphere_neutral(q, a, d):
    """Interaction energy for the neutral case: U = -q^2 a^3 / (2 d^2 (d^2-a^2))."""
    return -q**2 * a**3 / (2 * d**2 * (d**2 - a**2))

# ----------------------------------------------------------------------------
# Sec. 3.5 -- separation of variables in Cartesian 2-D (P18-P23)
# ----------------------------------------------------------------------------

def box2d_phi(x, y, a, b, V, nmax=200):
    """Ex. 3.5.1: box 0<x<a, 0<y<b, Phi=V on y=b, 0 elsewhere:
    Phi = (4V/pi) sum_odd (1/m) sinh(m pi y/a)/sinh(m pi b/a) sin(m pi x/a)."""
    m = np.arange(1, nmax + 1, 2)[:, None]
    k = m * np.pi / a
    with np.errstate(over="ignore"):
        rad = np.exp(k * (np.atleast_1d(y) - b)) * (1 - np.exp(-2 * k * np.atleast_1d(y))) \
              / (1 - np.exp(-2 * k * b))
    out = (4 * V / np.pi) * np.sum(np.sin(k * np.atleast_1d(x)) * rad / m, axis=0)
    return float(out) if out.size == 1 else out


def box2d_phi_Ex(x, y, a, b, E, nmax=200):
    """Ex. 3.5.6: same box but Phi(x, b) = -E x:
    Phi = (2Ea/pi) sum_m ((-1)^m/m) sinh(m pi y/a)/sinh(m pi b/a) sin(m pi x/a)."""
    m = np.arange(1, nmax + 1)[:, None]
    k = m * np.pi / a
    rad = np.exp(k * (y - b)) * (1 - np.exp(-2 * k * y)) / (1 - np.exp(-2 * k * b))
    return float((2 * E * a / np.pi) * np.sum(((-1.0) ** m / m) * rad * np.sin(k * x), axis=0))


def solve_laplace_rect(a, b, nx, ny, bottom, top, left, right):
    """Sparse 5-point Dirichlet Laplace solve on (0,a)x(0,b); bc's are callables."""
    x = np.linspace(0, a, nx)
    y = np.linspace(0, b, ny)
    hx, hy = x[1] - x[0], y[1] - y[0]
    U = np.zeros((nx, ny))
    U[:, 0] = bottom(x); U[:, -1] = top(x)
    U[0, :] = left(y); U[-1, :] = right(y)
    idx = -np.ones((nx, ny), int)
    c = 0
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            idx[i, j] = c; c += 1
    A = lil_matrix((c, c)); rhs = np.zeros(c)
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            k = idx[i, j]
            A[k, k] = -2.0 / hx**2 - 2.0 / hy**2
            for (ii, jj, hh) in [(i - 1, j, hx), (i + 1, j, hx), (i, j - 1, hy), (i, j + 1, hy)]:
                if idx[ii, jj] >= 0:
                    A[k, idx[ii, jj]] = 1.0 / hh**2
                else:
                    rhs[k] -= U[ii, jj] / hh**2
    sol = spsolve(csr_matrix(A), rhs)
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            U[i, j] = sol[idx[i, j]]
    return x, y, U


def strip_An(n, V):
    """Ex. 3.5.2 coefficients: A_n = -2V/(n pi) (all n >= 1)."""
    return -2 * V / (n * np.pi)


def strip_phi(x, y, a, V, nmax=400):
    """Ex. 3.5.2: strip 0<x<a, y>0; x=0 wall at V, x=a and y=0 grounded:
    Phi = V(1 - x/a) - (2V/pi) sum (1/n) e^{-n pi y/a} sin(n pi x/a)."""
    n = np.arange(1, nmax + 1)[:, None]
    k = n * np.pi / a
    s = np.sum(np.exp(-k * y) * np.sin(k * x) / n, axis=0)
    return float(V * (1 - x / a) - (2 * V / np.pi) * s)


def green_strip_D(x, y, xp, yp, a, nmax=400):
    """Ex. 3.5.3a: G = 8 sum (1/n) sin(n pi x/a) sin(n pi x'/a)
                         sinh(n pi y</a) e^{-n pi y>/a}."""
    n = np.arange(1, nmax + 1)[:, None]
    k = n * np.pi / a
    yl, yg = min(y, yp), max(y, yp)
    rad = 0.5 * (np.exp(-k * (yg - yl)) - np.exp(-k * (yg + yl)))
    return float(8 * np.sum(np.sin(k * x) * np.sin(k * xp) * rad / n, axis=0))


def strip_phi_from_green(x, y, a, V, nmax=400):
    """Ex. 3.5.3b: the wall integral collapses to
    Phi = (2V/pi) sum (1/n) sin(n pi x/a) (1 - e^{-n pi y/a})."""
    n = np.arange(1, nmax + 1)[:, None]
    k = n * np.pi / a
    return float((2 * V / np.pi) * np.sum(np.sin(k * x) * (1 - np.exp(-k * y)) / n, axis=0))


def green_strip_N(x, y, xp, yp, a, nmax=400):
    """Ex. 3.5.4: Neumann Green function of the same strip:
    G = 8 sum (1/n) cos cos' cosh(n pi y</a) e^{-n pi y>/a} - 4 pi y>/a."""
    n = np.arange(1, nmax + 1)[:, None]
    k = n * np.pi / a
    yl, yg = min(y, yp), max(y, yp)
    rad = 0.5 * (np.exp(-k * (yg - yl)) + np.exp(-k * (yg + yl)))
    s = np.sum(np.cos(k * x) * np.cos(k * xp) * rad / n, axis=0)
    return float(8 * s - 4 * np.pi * yg / a)


def green_2plates_2d_series(x, y, xp, yp, a, nmax=400):
    """Ex. 3.5.5: two grounded planes x=0, x=a (2-D):  g_n = (4/n) e^{-n pi |y-y'|/a},
    G = sum sin(n pi x/a) sin(n pi x'/a) g_n."""
    n = np.arange(1, nmax + 1)[:, None]
    k = n * np.pi / a
    return float(np.sum((4.0 / n) * np.sin(k * x) * np.sin(k * xp)
                        * np.exp(-k * abs(y - yp)), axis=0))


def green_2plates_2d_closed(x, y, xp, yp, a):
    """Closed form of the Ex. 3.5.5 sum:
    G = ln[(cosh(pi dy/a) - cos(pi(x+x')/a)) / (cosh(pi dy/a) - cos(pi(x-x')/a))]."""
    c = np.cosh(np.pi * (y - yp) / a)
    return np.log((c - np.cos(np.pi * (x + xp) / a)) / (c - np.cos(np.pi * (x - xp) / a)))


def green_2plates_2d_images(x, y, xp, yp, a, N=2000, richardson=True):
    """Image-line-charge sum, G = -2 sum q ln d.  The symmetric truncation has
    an O(1/N) tail; one Richardson step (2 G_{2N} - G_N) removes it."""
    def partial(NN):
        n = np.arange(-NN, NN + 1)
        dp = np.hypot(x - (2 * n * a + xp), y - yp)
        dm = np.hypot(x - (2 * n * a - xp), y - yp)
        return float(np.sum(-2 * np.log(dp) + 2 * np.log(dm)))
    if not richardson:
        return partial(N)
    return 2.0 * partial(2 * N) - partial(N)

# ----------------------------------------------------------------------------
# Sec. 3.6 -- eigenfunction Green function for the box; Madelung (P24)
# ----------------------------------------------------------------------------

def _g_box_stable(gam, z, zp, c):
    """sinh(g z<) sinh(g (c - z>)) / (g sinh g c), exp-stable for large g."""
    zl = np.minimum(z, zp); zg = np.maximum(z, zp)
    return (np.exp(-gam * (zg - zl)) * (1 - np.exp(-2 * gam * zl))
            * (1 - np.exp(-2 * gam * (c - zg))) / (2 * gam * (1 - np.exp(-2 * gam * c))))


def green_box3d(x, xp, dims=(1.0, 1.0, 1.0), nmax=60):
    """Eigenfunction Dirichlet Green function of the box (Eq. 3.98)."""
    a, b, c = dims
    n = np.arange(1, nmax + 1)
    m = np.arange(1, nmax + 1)
    N, M = np.meshgrid(n, m, indexing="ij")
    gam = np.pi * np.sqrt((N / a) ** 2 + (M / b) ** 2)
    g = _g_box_stable(gam, x[2], xp[2], c)
    S = (np.sin(N * np.pi * x[0] / a) * np.sin(N * np.pi * xp[0] / a)
         * np.sin(M * np.pi * x[1] / b) * np.sin(M * np.pi * xp[1] / b))
    return float(16 * np.pi / (a * b) * np.sum(S * g))


def madelung_evjen(N=10):
    """M_NaCl = sum' (-1)^{i+j+k} / sqrt(i^2+j^2+k^2), Evjen cube weighting
    (fractional boundary charges) -> -1.747564594... (Eq. 3.108)."""
    i = np.arange(-N, N + 1)
    I, J, K = np.meshgrid(i, i, i, indexing="ij")
    w = lambda A: np.where(np.abs(A) == N, 0.5, 1.0)
    W = w(I) * w(J) * w(K)
    R = np.sqrt(I**2 + J**2 + K**2)
    R[N, N, N] = 1.0
    S = W * (-1.0) ** (np.abs(I + J + K)) / R
    S[N, N, N] = 0.0
    return S.sum()


def madelung_from_box_green(eps_list=(0.2, 0.1, 0.05), nmax=251):
    """Ex. 3.6.1: Madelung constant from the unit-box Green function (3.98):
    M = lim_{x'->x} [G_D(x, x') - 1/|x-x'|] at the box center (a=1), the 1/eps
    subtraction removing the reference charge's self-energy.  Richardson-
    extrapolated in eps^2."""
    n = np.arange(1, nmax + 1, 2)          # even modes vanish at the center
    N, M = np.meshgrid(n, n, indexing="ij")
    gam = np.pi * np.sqrt(N**2 + M**2)
    S = []
    for eps in eps_list:
        z, zp = 0.5 + eps / 2, 0.5 - eps / 2
        g = _g_box_stable(gam, z, zp, 1.0)
        G = 16 * np.pi * np.sum(g)         # sin^2 = 1 on odd modes at center
        S.append(G - 1.0 / eps)
    S = np.array(S)
    # two Richardson steps in eps^2 (eps halves along the list)
    A = (4 * S[1] - S[0]) / 3.0
    B = (4 * S[2] - S[1]) / 3.0
    return (16 * B - A) / 15.0

# ----------------------------------------------------------------------------
# Sec. 3.7-3.9 -- polar separation, wedges, Poisson integral, halves (P25-P31)
# ----------------------------------------------------------------------------

def cyl_delta_series(rho, phi, b, V0, mmax=2000):
    """Ex. 3.7.1: Phi(b,phi)=V0 delta(phi) on a cylinder:
    Phi = V0/(2 pi) + (V0/pi) sum (rho/b)^m cos(m phi)."""
    m = np.arange(1, mmax + 1)
    return V0 / (2 * np.pi) + (V0 / np.pi) * np.sum((rho / b) ** m * np.cos(m * phi))


def poisson_kernel(rho, phi, b):
    """(1/2pi) (b^2 - rho^2)/(rho^2 + b^2 - 2 b rho cos phi)  (Ex. 3.9.1/3.9.5)."""
    return (b**2 - rho**2) / (rho**2 + b**2 - 2 * b * rho * np.cos(phi)) / (2 * np.pi)


def poisson_integral(rho, phi, b, f, n=16, breaks=None):
    """Ex. 3.9.1: Phi(rho,phi) = int dphi' f(phi') P(rho, phi-phi', b).
    `breaks`: interior discontinuities of f (the integral is split there so the
    Gauss panels see smooth pieces)."""
    edges = [0.0] + sorted(breaks or []) + [2 * np.pi]
    tot = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        t, w = gauss_panels(lo, hi, n)
        tot += np.sum(w * f(t) * poisson_kernel(rho, phi - t, b))
    return tot


def wedge_coeffs(fb, V, b, beta, mmax=60, n=800):
    """Ex. 3.8.1 coefficients: a_m b^{m pi/beta}
    = (2/beta) int_0^beta [f(phi) - V] sin(m pi phi/beta) dphi."""
    t, w = gauss_legendre(0.0, beta, n)
    return np.array([(2.0 / beta) * np.sum(w * (fb(t) - V) * np.sin(m * np.pi * t / beta))
                     / b ** (m * np.pi / beta) for m in range(1, mmax + 1)])


def wedge_phi(rho, phi, V, beta, coeffs):
    """Phi = V + sum a_m rho^{m pi/beta} sin(m pi phi/beta)  (Eq. 3.119)."""
    m = np.arange(1, len(coeffs) + 1)
    return V + np.sum(coeffs * rho ** (m * np.pi / beta) * np.sin(m * np.pi * phi / beta))


def halves_series(rho, phi, b, V1, V2, nmax=4000):
    """Interior of a split cylinder, halves at V1 (|phi|<pi/2) and V2 (Eq. 3.130):
    Phi = (V1+V2)/2 - (2(V1-V2)/pi) sum (rho/b)^{2n+1} sin[(2n+1)(phi-pi/2)]/(2n+1)."""
    n = np.arange(0, nmax)
    p = 2 * n + 1
    s = np.sum((rho / b) ** p * np.sin(p * (phi - np.pi / 2)) / p)
    return (V1 + V2) / 2 - (2 * (V1 - V2) / np.pi) * s


def halves_closed(rho, phi, b, V1, V2):
    """Eq. 3.131: Phi = (V1+V2)/2 + ((V1-V2)/pi) arctan[2 (rho/b) cos phi / (1-(rho/b)^2)]."""
    t = rho / b
    return (V1 + V2) / 2 + (V1 - V2) / np.pi * np.arctan2(2 * t * np.cos(phi), 1 - t**2)


def halves_axis(rho, b, V1, V2):
    """On the symmetry axis phi=0 the double angle collapses:
    Phi = (V1+V2)/2 + (2 (V1-V2)/pi) arctan(rho/b)."""
    return (V1 + V2) / 2 + 2 * (V1 - V2) / np.pi * np.arctan(rho / b)


def halves_exterior_series(rho, phi, b, V1, V2, nmax=4000):
    """Ex. 3.9.4a: exterior solution -- replace (rho/b)^{2n+1} by (b/rho)^{2n+1}."""
    n = np.arange(0, nmax)
    p = 2 * n + 1
    s = np.sum((b / rho) ** p * np.sin(p * (phi - np.pi / 2)) / p)
    return (V1 + V2) / 2 - (2 * (V1 - V2) / np.pi) * s


def halves_exterior_closed(rho, phi, b, V1, V2):
    """Ex. 3.9.4b / 3.11.2: Phi_out(rho,phi) = Phi_in(b^2/rho, phi)."""
    return halves_closed(b**2 / rho, phi, b, V1, V2)


def arctan_series(t, psi, nmax=4000):
    """Ex. 3.9.3 lemma: sum t^{2n+1} sin((2n+1) psi)/(2n+1)
    = (1/2) arctan(2 t sin psi / (1 - t^2)) = Im arctanh(t e^{i psi})."""
    n = np.arange(0, nmax)
    p = 2 * n + 1
    return np.sum(t**p * np.sin(p * psi) / p)


def arctan_series_closed(t, psi):
    return 0.5 * np.arctan2(2 * t * np.sin(psi), 1 - t**2)


def geometric_cos_sum(t, phi, mmax=4000):
    """Ex. 3.9.5 lemma: 1/2 + sum t^m cos(m phi) = (1/2)(1-t^2)/(1+t^2-2t cos phi)."""
    m = np.arange(1, mmax + 1)
    return 0.5 + np.sum(t**m * np.cos(m * phi))

# ----------------------------------------------------------------------------
# Sec. 3.10 -- variational bound on capacitance (notes check; no exercise)
# ----------------------------------------------------------------------------

def disk_energy(sig_of_rho, R, n=400):
    """W[sigma] = (1/2) int int sigma sigma'/|x-x'| for an axisymmetric disk,
    reduced with the elliptic kernel  oint dphi/|..| = 4 K(m)/(rho+rho'),
    m = 4 r r'/(r+r')^2; radial quadrature in rho = R sin t (edge-regular)."""
    t = (np.arange(n) + 0.5) * (np.pi / 2) / n
    tp = (np.arange(n) + 0.23) * (np.pi / 2) / n       # staggered vs t
    dt = (np.pi / 2) / n
    r, rp = R * np.sin(t), R * np.sin(tp)
    wr = R**2 * np.sin(t) * np.cos(t) * dt              # rho drho
    wrp = R**2 * np.sin(tp) * np.cos(tp) * dt
    Rg, Rp = np.meshgrid(r, rp, indexing="ij")
    m = 4 * Rg * Rp / (Rg + Rp) ** 2
    Kk = special.ellipk(np.clip(m, 0.0, 1.0 - 1e-14))
    S = sig_of_rho(Rg) * sig_of_rho(Rp) * Kk / (Rg + Rp)
    return 0.5 * 2 * np.pi * 4 * np.sum(np.outer(wr, wrp) * S)


def disk_charge(sig_of_rho, R, n=400):
    t, w = gauss_legendre(0.0, np.pi / 2, n)
    r = R * np.sin(t)
    return np.sum(w * 2 * np.pi * sig_of_rho(r) * R**2 * np.sin(t) * np.cos(t))


def disk_C_variational(sig_of_rho, R, n=400):
    """C_var = Q^2 / (2 W[sigma])  <=  C_exact = 2R/pi  (Eq. 3.144 lower bound)."""
    Q = disk_charge(sig_of_rho, R)
    return Q**2 / (2 * disk_energy(sig_of_rho, R, n))


def disk_C_exact(R):
    return 2 * R / np.pi

# ----------------------------------------------------------------------------
# Sec. 3.11 -- conformal mapping (P32-P33)
# ----------------------------------------------------------------------------

def map_box_to_halfannulus(z, b):
    """w = exp(pi z / b): the a x b box -> upper half-annulus 1 < |w| < e^{pi a/b}."""
    return np.exp(np.pi * z / b)


def semicircle_phi(r, theta, r0, V, nmax=200):
    """Ex. 3.11.1b: potential in the half-annulus 1<r<r0, 0<theta<pi with the
    segment (-r0,-1) at V:  (4V/pi) sum_odd (1/m) sinh(m pi theta/ln r0)
    / sinh(m pi^2/ln r0) sin(m pi ln r/ln r0)."""
    L = np.log(r0)
    m = np.arange(1, nmax + 1, 2)
    k = m * np.pi / L
    rad = np.exp(k * (theta - np.pi)) * (1 - np.exp(-2 * k * theta)) / (1 - np.exp(-2 * k * np.pi))
    return (4 * V / np.pi) * np.sum(rad * np.sin(k * np.log(r)) / m)


def exterior_from_inversion(rho, phi, b, V1, V2):
    """Ex. 3.11.2: w = b^2/z maps rho>b onto rho_w<b; pulling (3.131) back gives
    Phi_out(rho, phi) = Phi_in(b^2/rho, -phi) (= same, by the phi-symmetry)."""
    w = b**2 / (rho * np.exp(1j * phi))
    return halves_closed(abs(w), np.angle(w), b, V1, V2)


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    print("MACRO_EM-03 demo (Gaussian units)")
    print(f"  corner work at (1,2):          {corner_work(1.0, 2.0):+.6f}   (Ex. 3.1.2b)")
    print(f"  Madelung, Evjen N=10:          {madelung_evjen(10):+.9f} (Eq. 3.108)")
    print(f"  Madelung from box G (3.98):    {madelung_from_box_green():+.9f} (Ex. 3.6.1)")
    C11, C21 = two_sphere_C(1.0, 2.0, 30.0)
    print(f"  two-sphere C_ab (a=1,b=2,d=30): {C21:+.6f}  vs  -ab/d = {-2/30:+.6f}")
    print(f"  neutral-sphere force q=1,a=1,d=3: {force_sphere_neutral(1, 1, 3):+.6f}")
    print(f"  disk C bounds: uniform {disk_C_variational(lambda r: np.ones_like(r), 1.0):.5f}"
          f" < exact {disk_C_exact(1.0):.5f}")
    print(f"  halves axis check:  {halves_closed(0.5, 0.0, 1.0, 1.0, -1.0):.6f}"
          f" = {halves_axis(0.5, 1.0, 1.0, -1.0):.6f}")
