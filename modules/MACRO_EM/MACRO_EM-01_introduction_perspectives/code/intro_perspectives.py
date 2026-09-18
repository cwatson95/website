"""MACRO_EM-01 -- machine checks for Wilcox & Thron Ch. 1 + Appendix A exercises.

Gaussian units throughout (Table 1.1, printed p.2):
    div E = 4 pi rho,   curl B - (1/c) dE/dt = (4 pi / c) J,
    curl E + (1/c) dB/dt = 0,   div B = 0.

Sections mirror problems/problems.md (P1..P9):
  P1  Ex 1.1.1  vector / Laplacian identities        (residual functions)
  P2  Ex 1.1.2  potentials -> identities + coupled PDEs
  P3  Ex 1.1.3  continuity for a rigidly moving blob
  P4  Ex 1.4.1  oint v . dl = 2A, ellipse area
  P5  Ex 1.4.2  gradient / curl-volume Gauss theorems (box quadrature)
  P6  Ex 1.4.3  surface-gradient Stokes theorem       (disc + hemisphere)
  P7  Ex 1.5.1  2-D point charge E = 2q/rho; 2-D Gauss <-> Stokes
  P8  Ex A.1.1  Tables A.1-A.2 amount-conversion factors (all 30 rows)
  P9  Ex A.1.2  MKS-Gaussian unit sizes, electron-charge round-trip

Derivatives are 5-point 4th-order central stencils -- exact (to rounding) on
fields of polynomial degree <= 4 per variable, so identity checks on the
polynomial test fields below are machine-tight and nothing is differentiated
by hand unless separately validated against the stencils.
"""
import numpy as np

# ---------------------------------------------------------------------------
# constants (Wilcox 2e: Table 1.1 p.2; Appendix A p.860)
# ---------------------------------------------------------------------------
C_GAUSS_CM_S = 2.9979245800e10          # speed of light, cm/s (Table 1.1)
C_NUM = 299792458.0                     # the *pure number* c of Appendix A
ALPHA = 1.0e2                           # cm per m   (p.860)
BETA = 1.0e7                            # erg per J  (p.860)
FOUR_PI_EPS0 = 1.0e7 / C_NUM**2         # 4 pi eps0 in SI numbers (p.860)
EPS0_SI = FOUR_PI_EPS0 / (4.0 * np.pi)  # = 8.854e-12
MU0_SI = 4.0 * np.pi * 1.0e-7           # (p.860)
E_STATC = 4.80320450e-10                # |e| in statcoulombs (printed p.5)
E_CODATA_C = 1.602176634e-19            # CODATA elementary charge, coulomb


# ---------------------------------------------------------------------------
# finite differences: 5-point 4th-order central stencils
# ---------------------------------------------------------------------------
def d1(f, x, h=1e-2):
    """First derivative of callable f at scalar x (array-valued f allowed)."""
    return (np.asarray(f(x - 2*h)) - 8.0*np.asarray(f(x - h))
            + 8.0*np.asarray(f(x + h)) - np.asarray(f(x + 2*h))) / (12.0*h)


def d2(f, x, h=1e-2):
    """Second derivative of callable f at scalar x."""
    return (-np.asarray(f(x - 2*h)) + 16.0*np.asarray(f(x - h))
            - 30.0*np.asarray(f(x)) + 16.0*np.asarray(f(x + h))
            - np.asarray(f(x + 2*h))) / (12.0*h*h)


def _shift(p, i, s):
    q = np.array(p, dtype=float)
    q[i] += s
    return q


def fd_partial(f, p, i, h=1e-2):
    """d f / d x_i at point p (f scalar- or vector-valued)."""
    return d1(lambda s: f(_shift(p, i, s)), 0.0, h)


def fd_grad(f, p, h=1e-2):
    """Gradient of scalar field f at p (any dimension)."""
    p = np.asarray(p, dtype=float)
    return np.array([fd_partial(f, p, i, h) for i in range(p.size)])


def fd_jacobian(F, p, h=1e-2):
    """J[i, j] = d F_i / d x_j for vector field F at p."""
    p = np.asarray(p, dtype=float)
    cols = [fd_partial(F, p, j, h) for j in range(p.size)]
    return np.array(cols).T


def fd_div(F, p, h=1e-2):
    return float(np.trace(fd_jacobian(F, p, h)))


def fd_curl(F, p, h=1e-2):
    J = fd_jacobian(F, p, h)
    return np.array([J[2, 1] - J[1, 2], J[0, 2] - J[2, 0], J[1, 0] - J[0, 1]])


def fd_lap(f, p, h=1e-2):
    """Laplacian of scalar (or componentwise of vector) field f at p."""
    p = np.asarray(p, dtype=float)
    return sum(d2(lambda s, i=i: f(_shift(p, i, s)), 0.0, h) for i in range(p.size))


def fd_dt(g, t, h=1e-2):
    """Time derivative of callable g(t) (array-valued allowed)."""
    return d1(g, t, h)


# ---------------------------------------------------------------------------
# P1 -- Exercise 1.1.1: vector / Laplacian identities
# ---------------------------------------------------------------------------
def bac_cab_residual(a, b, c):
    """A x (B x C) - [B (A.C) - C (A.B)]  (glossary p.23; = 0)."""
    a, b, c = map(np.asarray, (a, b, c))
    return np.cross(a, np.cross(b, c)) - (b * np.dot(a, c) - c * np.dot(a, b))


def jacobi_residual(a, b, c):
    """A x (B x C) + B x (C x A) + C x (A x B)  (Ex 1.1.1a; = 0)."""
    a, b, c = map(np.asarray, (a, b, c))
    return (np.cross(a, np.cross(b, c)) + np.cross(b, np.cross(c, a))
            + np.cross(c, np.cross(a, b)))


def laplacian_product_residual(phi, psi, p, h=1e-2):
    """lap(phi psi) - [phi lap psi + psi lap phi + 2 grad phi . grad psi]
    (Ex 1.1.1b; = 0). Everything by finite differences -- non-circular."""
    prod = lambda q: phi(q) * psi(q)
    lhs = fd_lap(prod, p, h)
    rhs = (phi(p) * fd_lap(psi, p, h) + psi(p) * fd_lap(phi, p, h)
           + 2.0 * np.dot(fd_grad(phi, p, h), fd_grad(psi, p, h)))
    return lhs - rhs


def grad_dot_expansion_residual(A, B, p, h=1e-2):
    """sum_i A_i grad B_i - [grad(A.B) - (B.grad)A - B x (curl A)]
    (Ex 1.1.1c; = 0 vector)."""
    p = np.asarray(p, dtype=float)
    Ap, Bp = A(p), B(p)
    JA, JB = fd_jacobian(A, p, h), fd_jacobian(B, p, h)   # J[i,j] = d_j F_i
    lhs = np.array([np.dot(Ap, JB[:, j]) for j in range(3)])  # A_i d_j B_i
    grad_AdotB = fd_grad(lambda q: np.dot(A(q), B(q)), p, h)
    B_grad_A = JA @ Bp                                       # (B.grad)A_j = B_i d_i A_j
    BxcurlA = np.cross(Bp, fd_curl(A, p, h))
    return lhs - (grad_AdotB - B_grad_A - BxcurlA)


# ---------------------------------------------------------------------------
# P2 -- Exercise 1.1.2: potentials
# ---------------------------------------------------------------------------
def e_from_potentials(Phi, A, p, t, c=1.0, h=1e-2):
    """E = -grad Phi - (1/c) dA/dt   (Ex 1.1.2 definition)."""
    return -fd_grad(lambda q: Phi(q, t), p, h) - fd_dt(lambda s: A(p, s), t, h) / c


def b_from_potentials(A, p, t, h=1e-2):
    """B = curl A."""
    return fd_curl(lambda q: A(q, t), p, h)


def div_b_residual(A, p, t, h=1e-2):
    """div B  (no-monopole; identically 0)."""
    return fd_div(lambda q: b_from_potentials(A, q, t, h), p, h)


def faraday_residual(Phi, A, p, t, c=1.0, h=1e-2):
    """curl E + (1/c) dB/dt  (Faraday; identically 0 vector)."""
    curlE = fd_curl(lambda q: e_from_potentials(Phi, A, q, t, c, h), p, h)
    dBdt = fd_dt(lambda s: b_from_potentials(A, p, s, h), t, h)
    return curlE + dBdt / c


def coulomb_sides(Phi, A, p, t, c=1.0, h=1e-2):
    """(div E,  -[lap Phi + (1/c) d_t div A]) -- the two sides of the derived
    Coulomb PDE  lap Phi + (1/c) d_t(div A) = -4 pi rho  (must be equal)."""
    lhs = fd_div(lambda q: e_from_potentials(Phi, A, q, t, c, h), p, h)
    rhs = -(fd_lap(lambda q: Phi(q, t), p, h)
            + fd_dt(lambda s: fd_div(lambda q: A(q, s), p, h), t, h) / c)
    return lhs, rhs


def ampere_sides(Phi, A, p, t, c=1.0, h=1e-2):
    """(curl B - (1/c) dE/dt,
        -[lap A - (1/c^2) d_tt A - grad(div A + (1/c) d_t Phi)])
    -- the two sides of the derived Ampere-Maxwell PDE (must be equal)."""
    lhs = (fd_curl(lambda q: b_from_potentials(A, q, t, h), p, h)
           - fd_dt(lambda s: e_from_potentials(Phi, A, p, s, c, h), t, h) / c)
    lapA = fd_lap(lambda q: A(q, t), p, h)
    dttA = d2(lambda s: A(p, s), t, h)
    gauge = lambda q: (fd_div(lambda r: A(r, t), q, h)
                       + fd_dt(lambda s: Phi(q, s), t, h) / c)
    rhs = -(lapA - dttA / c**2 - fd_grad(gauge, p, h))
    return lhs, rhs


# ---------------------------------------------------------------------------
# P3 -- Exercise 1.1.3: continuity for rho = e f(r - R(t)), J = e Rdot f
# ---------------------------------------------------------------------------
def continuity_residual(f, R, e, p, t, h=1e-2):
    """d rho/dt + div J for rho = e f(r - R(t)), J = e (dR/dt) f(r - R(t)).
    All derivatives by finite differences (non-circular). Should be ~0."""
    p = np.asarray(p, dtype=float)
    rho = lambda q, s: e * f(np.asarray(q) - np.asarray(R(s)))
    def J(q, s):
        return e * np.asarray(fd_dt(R, s, h)) * f(np.asarray(q) - np.asarray(R(s)))
    drho_dt = fd_dt(lambda s: rho(p, s), t, h)
    divJ = fd_div(lambda q: J(q, t), p, h)
    return drho_dt + divJ, drho_dt, divJ


def gaussian_blob(width=0.8):
    """f(u) = exp(-|u|^2 / 2 width^2) -- a smooth 'point charge' stand-in."""
    return lambda u: float(np.exp(-np.dot(u, u) / (2.0 * width**2)))


# ---------------------------------------------------------------------------
# P4 -- Exercise 1.4.1: oint v . dl = 2A  (v = -y i + x j)
# ---------------------------------------------------------------------------
def v_area(p):
    """The exercise's field v = -y i + x j (2-D)."""
    return np.array([-p[1], p[0]])


def circulation2d(F, curve, dcurve, n=400):
    """oint F . dl over a closed curve gamma(t), t in [0, 2 pi), by periodic
    trapezoid quadrature (spectrally accurate for smooth curves/fields)."""
    ts = np.linspace(0.0, 2.0*np.pi, n, endpoint=False)
    tot = 0.0
    for t in ts:
        tot += float(np.dot(F(curve(t)), dcurve(t)))
    return tot * (2.0*np.pi / n)


def area_by_circulation(curve, dcurve, n=400):
    """A = (1/2) oint (-y dx + x dy)  (Ex 1.4.1a rearranged)."""
    return 0.5 * circulation2d(v_area, curve, dcurve, n)


def circle_curve(r, center=(0.0, 0.0)):
    cx, cy = center
    curve = lambda t: np.array([cx + r*np.cos(t), cy + r*np.sin(t)])
    dcurve = lambda t: np.array([-r*np.sin(t), r*np.cos(t)])
    return curve, dcurve


def ellipse_curve(a, b):
    curve = lambda t: np.array([a*np.cos(t), b*np.sin(t)])
    dcurve = lambda t: np.array([-a*np.sin(t), b*np.cos(t)])
    return curve, dcurve


def polar_curve(rfun, drfun):
    """Closed curve r = rfun(theta) (counterclockwise)."""
    def curve(t):
        r = rfun(t)
        return np.array([r*np.cos(t), r*np.sin(t)])
    def dcurve(t):
        r, dr = rfun(t), drfun(t)
        return np.array([dr*np.cos(t) - r*np.sin(t), dr*np.sin(t) + r*np.cos(t)])
    return curve, dcurve


# ---------------------------------------------------------------------------
# quadrature helpers (Gauss-Legendre)
# ---------------------------------------------------------------------------
def gl_nodes(a, b, n):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5*(b - a)*x + 0.5*(b + a), 0.5*(b - a)*w


# ---------------------------------------------------------------------------
# P5 -- Exercise 1.4.2: gradient / curl-volume forms of Gauss' theorem
# ---------------------------------------------------------------------------
def box_volume_integral(F, box, n=24):
    """integral over box of F(p) d^3x; F may return scalar or vector."""
    (x0, x1), (y0, y1), (z0, z1) = box
    xs, wx = gl_nodes(x0, x1, n)
    ys, wy = gl_nodes(y0, y1, n)
    zs, wz = gl_nodes(z0, z1, n)
    tot = None
    for x, wxi in zip(xs, wx):
        for y, wyi in zip(ys, wy):
            for z, wzi in zip(zs, wz):
                val = np.asarray(F(np.array([x, y, z]))) * (wxi*wyi*wzi)
                tot = val if tot is None else tot + val
    return tot


def box_surface_integral(G, box, n=24):
    """oint over the box surface of G(p, nhat) da (G scalar- or vector-valued)."""
    (x0, x1), (y0, y1), (z0, z1) = box
    lims = [(x0, x1), (y0, y1), (z0, z1)]
    tot = None
    for axis in range(3):
        u_ax, v_ax = [i for i in range(3) if i != axis]
        us, wu = gl_nodes(*lims[u_ax], n=n)
        vs, wv = gl_nodes(*lims[v_ax], n=n)
        for side, coord in zip((-1.0, 1.0), lims[axis]):
            nhat = np.zeros(3)
            nhat[axis] = side
            for u, wui in zip(us, wu):
                for v, wvi in zip(vs, wv):
                    p = np.zeros(3)
                    p[axis], p[u_ax], p[v_ax] = coord, u, v
                    val = np.asarray(G(p, nhat)) * (wui*wvi)
                    tot = val if tot is None else tot + val
    return tot


def gradient_theorem_sides(phi, box, n=24, h=1e-2):
    """(int_V grad phi d^3x,  oint_S da nhat phi)   (Ex 1.4.2a)."""
    vol = box_volume_integral(lambda p: fd_grad(phi, p, h), box, n)
    surf = box_surface_integral(lambda p, nh: nh * phi(p), box, n)
    return vol, surf


def curl_volume_theorem_sides(A, box, n=24, h=1e-2):
    """(int_V curl A d^3x,  oint_S da nhat x A)   (Ex 1.4.2b)."""
    vol = box_volume_integral(lambda p: fd_curl(A, p, h), box, n)
    surf = box_surface_integral(lambda p, nh: np.cross(nh, A(p)), box, n)
    return vol, surf


# ---------------------------------------------------------------------------
# P6 -- Exercise 1.4.3: int_S da nhat x grad phi = oint_C dl phi
# ---------------------------------------------------------------------------
def line_integral_scalar_dl(phi, curve, dcurve, n=512):
    """oint dl phi -> vector (dl = gamma'(t) dt), periodic trapezoid."""
    ts = np.linspace(0.0, 2.0*np.pi, n, endpoint=False)
    tot = np.zeros(3)
    for t in ts:
        tot += np.asarray(dcurve(t), dtype=float) * phi(curve(t))
    return tot * (2.0*np.pi / n)


def disc_integral_vec(G, nr=48, nt=256):
    """int over unit disc (z = 0) of vector integrand G(p) dA (polar GL x trap)."""
    rs, wr = gl_nodes(0.0, 1.0, nr)
    ts = np.linspace(0.0, 2.0*np.pi, nt, endpoint=False)
    dt = 2.0*np.pi / nt
    tot = np.zeros(3)
    for r, wri in zip(rs, wr):
        for t in ts:
            p = np.array([r*np.cos(t), r*np.sin(t), 0.0])
            tot += np.asarray(G(p)) * (r * wri * dt)
    return tot


def hemisphere_integral_vec(G, ntheta=48, nphi=256):
    """int over the unit upper hemisphere of G(p, nhat) da,
    nhat = rhat (outward), da = sin(theta) dtheta dphi."""
    thetas, wth = gl_nodes(0.0, 0.5*np.pi, ntheta)
    phis = np.linspace(0.0, 2.0*np.pi, nphi, endpoint=False)
    dphi = 2.0*np.pi / nphi
    tot = np.zeros(3)
    for th, wt in zip(thetas, wth):
        st, ct = np.sin(th), np.cos(th)
        for ph in phis:
            nhat = np.array([st*np.cos(ph), st*np.sin(ph), ct])
            tot += np.asarray(G(nhat, nhat)) * (st * wt * dphi)
    return tot


def stokes_gradient_sides_disc(phi, grad_phi, nr=48, nt=256, nline=512):
    """(int_disc da zhat x grad phi,  oint dl phi) over the unit circle."""
    lhs = disc_integral_vec(lambda p: np.cross([0.0, 0.0, 1.0], grad_phi(p)), nr, nt)
    curve = lambda t: np.array([np.cos(t), np.sin(t), 0.0])
    dcurve = lambda t: np.array([-np.sin(t), np.cos(t), 0.0])
    rhs = line_integral_scalar_dl(phi, curve, dcurve, nline)
    return lhs, rhs


def stokes_gradient_sides_hemisphere(phi, grad_phi, ntheta=48, nphi=256, nline=512):
    """(int_hemisphere da nhat x grad phi,  oint dl phi) -- same boundary circle,
    different spanning surface (surface-independence check)."""
    lhs = hemisphere_integral_vec(lambda p, nh: np.cross(nh, grad_phi(p)), ntheta, nphi)
    curve = lambda t: np.array([np.cos(t), np.sin(t), 0.0])
    dcurve = lambda t: np.array([-np.sin(t), np.cos(t), 0.0])
    rhs = line_integral_scalar_dl(phi, curve, dcurve, nline)
    return lhs, rhs


# ---------------------------------------------------------------------------
# P7 -- Exercise 1.5.1: 2-D electrodynamics
# ---------------------------------------------------------------------------
def e2d_point_charge(q, r0=(0.0, 0.0)):
    """E = 2 q rhohat / rho  (Table 1.5 normalization: oint E.nhat dl = 4 pi q)."""
    r0 = np.asarray(r0, dtype=float)
    def E(p):
        u = np.asarray(p, dtype=float) - r0
        return 2.0 * q * u / np.dot(u, u)
    return E


def flux2d(F, curve, dcurve, n=800):
    """oint F . nhat dl; for counterclockwise gamma, nhat dl = (y', -x') dt."""
    ts = np.linspace(0.0, 2.0*np.pi, n, endpoint=False)
    tot = 0.0
    for t in ts:
        d = dcurve(t)
        tot += float(np.dot(F(curve(t)), np.array([d[1], -d[0]])))
    return tot * (2.0*np.pi / n)


def square_flux2d(F, half=1.0, n=200):
    """oint F . nhat dl around the square [-half, half]^2 (GL per side)."""
    xs, w = gl_nodes(-half, half, n)
    tot = 0.0
    for x, wi in zip(xs, w):
        tot += wi * (F(np.array([half, x]))[0]        # right, nhat = +x
                     - F(np.array([-half, x]))[0]     # left,  nhat = -x
                     + F(np.array([x, half]))[1]      # top,   nhat = +y
                     - F(np.array([x, -half]))[1])    # bottom, nhat = -y
    return tot


def powerlaw_flux2d(s, r, n=800):
    """Circle-flux of the trial field rho^s rhohat at radius r (analytic:
    2 pi r^(s+1); radius-independent only for s = -1)."""
    F = lambda p: np.dot(p, p)**((s - 1.0)/2.0) * np.asarray(p, dtype=float)
    return flux2d(F, *circle_curve(r), n=n)


def cross_z_2d(F):
    """The rotation map A' = A x zhat = (A_y, -A_x) of P7b."""
    return lambda p: np.array([F(p)[1], -F(p)[0]])


def zcross_2d(F):
    """The inverse map zhat x A = (-A_y, A_x)."""
    return lambda p: np.array([-F(p)[1], F(p)[0]])


def fd_div2d(F, p, h=1e-2):
    p = np.asarray(p, dtype=float)
    return float(fd_partial(F, p, 0, h)[0] + fd_partial(F, p, 1, h)[1])


def fd_curlz2d(F, p, h=1e-2):
    p = np.asarray(p, dtype=float)
    return float(fd_partial(F, p, 0, h)[1] - fd_partial(F, p, 1, h)[0])


def disc2d_integral(g, center=(0.0, 0.0), R=1.0, nr=48, nt=256):
    """int over the disc of scalar g(p) dA (polar GL x trapezoid)."""
    cx, cy = center
    rs, wr = gl_nodes(0.0, R, nr)
    ts = np.linspace(0.0, 2.0*np.pi, nt, endpoint=False)
    dt = 2.0*np.pi / nt
    tot = 0.0
    for r, wri in zip(rs, wr):
        for t in ts:
            p = np.array([cx + r*np.cos(t), cy + r*np.sin(t)])
            tot += g(p) * r * wri * dt
    return tot


def gauss2d_sides(F, R=1.0, h=1e-2, nr=48, nt=256, nline=800):
    """2-D Gauss theorem (Eq. 1.37) over the unit-R disc:
    (int div F dA,  oint F.nhat dl)."""
    area = disc2d_integral(lambda p: fd_div2d(F, p, h), R=R, nr=nr, nt=nt)
    line = flux2d(F, *circle_curve(R), n=nline)
    return area, line


def stokes2d_sides(F, R=1.0, h=1e-2, nr=48, nt=256, nline=800):
    """2-D Stokes theorem (Eq. 1.38) over the unit-R disc:
    (int (curl F).z dA,  oint F.dl)."""
    area = disc2d_integral(lambda p: fd_curlz2d(F, p, h), R=R, nr=nr, nt=nt)
    curve, dcurve = circle_curve(R)
    line = circulation2d(F, curve, dcurve, n=nline)
    return area, line


# ---------------------------------------------------------------------------
# P8 -- Exercise A.1.1: Tables A.1-A.2 amount-conversion factors (30 rows)
# Factor = f(eps0, mu0, alpha, beta); Value = coef * 10^p * c^pc  (book cols 4-5)
# ---------------------------------------------------------------------------
_E, _M, _A, _B, _PI = EPS0_SI, MU0_SI, ALPHA, BETA, np.pi

TABLE_A1 = {  # printed p.863
    'mass':                  (lambda: _A**2 / _B,                        (1.0, -3, 0)),
    'length':                (lambda: 1.0 / _A,                          (1.0, -2, 0)),
    'time':                  (lambda: 1.0,                               (1.0, 0, 0)),
    'force':                 (lambda: _A / _B,                           (1.0, -5, 0)),
    'energy':                (lambda: 1.0 / _B,                          (1.0, -7, 0)),
    'energy density':        (lambda: _A**3 / _B,                        (1.0, -1, 0)),
    'power':                 (lambda: 1.0 / _B,                          (1.0, -7, 0)),
    'power flow density':    (lambda: _A**2 / _B,                        (1.0, -3, 0)),
    'charge':                (lambda: np.sqrt(4*_PI*_E / (_A*_B)),       (1.0, -1, -1)),
    'surface charge density':(lambda: np.sqrt(4*_PI*_E*_A**3 / _B),      (1.0, 3, -1)),
    'charge density':        (lambda: np.sqrt(4*_PI*_E*_A**5 / _B),      (1.0, 5, -1)),
    'current':               (lambda: np.sqrt(4*_PI*_E / (_A*_B)),       (1.0, -1, -1)),
    'current density':       (lambda: np.sqrt(4*_PI*_E*_A**3 / _B),      (1.0, 3, -1)),
    'polarization':          (lambda: np.sqrt(4*_PI*_E*_A**3 / _B),      (1.0, 3, -1)),
    'electric dipole moment':(lambda: np.sqrt(4*_PI*_E / (_A**3*_B)),    (1.0, -3, -1)),
}

TABLE_A2 = {  # printed p.864
    'electric field':        (lambda: np.sqrt(_A**3 / (4*_PI*_E*_B)),    (1.0, -4, 1)),
    'potential':             (lambda: np.sqrt(_A / (4*_PI*_E*_B)),       (1.0, -6, 1)),
    'D-field':               (lambda: np.sqrt(_E*_A**3 / (4*_PI*_B)),    (1.0/(4*_PI), 3, -1)),
    'magnetic field':        (lambda: np.sqrt(_M*_A**3 / (4*_PI*_B)),    (1.0, -4, 0)),
    'vector potential':      (lambda: np.sqrt(_M*_A**5 / (4*_PI*_B)),    (1.0, -2, 0)),
    'H-field':               (lambda: np.sqrt(_A**3 / (4*_PI*_M*_B)),    (1.0/(4*_PI), 3, 0)),
    'magnetization':         (lambda: np.sqrt(4*_PI*_A**3 / (_M*_B)),    (1.0, 3, 0)),
    'magnetic moment':       (lambda: np.sqrt(4*_PI / (_M*_A**3*_B)),    (1.0, -3, 0)),
    'magnetic flux':         (lambda: np.sqrt(_M / (4*_PI*_A*_B)),       (1.0, -8, 0)),
    'conductivity':          (lambda: 4*_PI*_E,                          (1.0, 7, -2)),
    'dielectric constant':   (lambda: _E,                                (1.0/(4*_PI), 7, -2)),
    'magnetic permeability': (lambda: _M,                                (4*_PI, -7, 0)),
    'resistance':            (lambda: _A / (4*_PI*_E),                   (1.0, -5, 2)),
    'inductance':            (lambda: _A / (4*_PI*_E),                   (1.0, -5, 2)),
    'capacitance':           (lambda: 4*_PI*_E / _A,                     (1.0, 5, -2)),
}


def amount_factor(name):
    """Column-4 Factor, computed from eps0/mu0/alpha/beta (P8's recipe)."""
    table = TABLE_A1 if name in TABLE_A1 else TABLE_A2
    return float(table[name][0]())


def book_value(name):
    """Column-5 Value as printed: coef * 10^p * c^pc with c = 299,792,458."""
    table = TABLE_A1 if name in TABLE_A1 else TABLE_A2
    coef, p, pc = table[name][1]
    return float(coef * 10.0**p * C_NUM**pc)


# physical spot checks (independent of the tables)
def statcoulomb_in_C():
    return amount_factor('charge')                    # ~3.3356e-10


def statvolt_in_V():
    return amount_factor('potential')                 # ~299.79


def gauss_in_tesla():
    return amount_factor('magnetic field')            # 1e-4


def maxwell_in_weber():
    return amount_factor('magnetic flux')             # 1e-8


def oersted_in_A_per_m():
    return amount_factor('H-field')                   # 1000/(4 pi) ~ 79.577


def cm_in_farad():
    return amount_factor('capacitance')               # ~1.11265e-12


def s_per_cm_in_ohm():
    return amount_factor('resistance')                # ~8.98755e11


# ---------------------------------------------------------------------------
# P9 -- Exercise A.1.2: MKS units inside the Gaussian system
# ---------------------------------------------------------------------------
def mksg_charge_unit_in_statC():
    """1 MKS-Gaussian charge unit = sqrt(J m / (erg cm)) = sqrt(alpha beta) statC."""
    return np.sqrt(ALPHA * BETA)                      # 10^4.5 ~ 3.16e4


def mksg_charge_unit_in_C():
    """Same unit in coulombs: sqrt(4 pi eps0) (the alpha-beta dust cancels)."""
    return np.sqrt(FOUR_PI_EPS0)                      # ~1.0546e-5


def mksg_field_unit_in_gauss():
    """1 MKS-Gaussian field unit (E or B) = sqrt(J/m^3 / (erg/cm^3)) gauss."""
    return np.sqrt(BETA / ALPHA**3)                   # sqrt(10)


def mksg_bfield_unit_in_tesla():
    """Same unit in tesla: sqrt(mu0 / 4 pi)."""
    return np.sqrt(MU0_SI / (4.0 * np.pi))            # sqrt(1e-7)


def electron_charge_via_mksg():
    """e: statC -> MKS-Gaussian -> C (never uses the direct statC->C factor)."""
    e_mksg = E_STATC / mksg_charge_unit_in_statC()
    return e_mksg * mksg_charge_unit_in_C()


# ---------------------------------------------------------------------------
# demo
# ---------------------------------------------------------------------------
def _demo():
    rng = np.random.default_rng(1)
    a, b, c3 = rng.standard_normal(3), rng.standard_normal(3), rng.standard_normal(3)
    print("P1a  |Jacobi residual|          :", np.max(np.abs(jacobi_residual(a, b, c3))))

    Phi = lambda p, t: p[0]**2*p[1] - 2.0*p[2]*t + t**2
    A = lambda p, t: np.array([p[1]*p[2]*t, p[0]**2 - t*p[2], p[0]*p[1] - p[1]**2*t])
    p0, t0 = np.array([0.3, -0.5, 0.7]), 0.4
    print("P2   |div B|, |Faraday residual|:", abs(div_b_residual(A, p0, t0)),
          np.max(np.abs(faraday_residual(Phi, A, p0, t0, c=2.0))))

    res, dr, dj = continuity_residual(gaussian_blob(), lambda t: np.array(
        [np.cos(t), np.sin(2*t), 0.3*t]), 1.3, [0.4, -0.2, 0.5], 0.7, h=2e-3)
    print("P3   continuity residual        :", res, " (terms ~", dr, ")")

    print("P4   ellipse area (a=3,b=1.5)   :", area_by_circulation(*ellipse_curve(3.0, 1.5)),
          " vs pi a b =", np.pi*3.0*1.5)

    E = e2d_point_charge(1.0, (0.2, -0.1))
    print("P7   2-D flux / 4 pi q          :", flux2d(E, *circle_curve(1.0)) / (4*np.pi))

    print("P8   statC -> C                 :", statcoulomb_in_C(),
          " (book: 10^-1/c =", 0.1/C_NUM, ")")
    print("P9   e via MKS-Gaussian route   :", electron_charge_via_mksg(),
          " C (CODATA", E_CODATA_C, ")")


if __name__ == "__main__":
    _demo()
