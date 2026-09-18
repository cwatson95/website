"""MACRO_EM-04 -- Electrostatics in cylindrical and spherical coordinates
(Wilcox & Thron 2e, Ch. 4).

Numeric companions to the 49 exercises of Wilcox Sec. 4.16 (printed
pp. 180-202).  Conventions (the book's, GAUSSIAN units):

  * unit point charge        Phi = 1/|x - x'|
  * Green equation           del^2 G = -4 pi delta^3        (4.73)
  * 2-D line charge          G_f = -2 ln(rho/L);  del^2 G = -4 pi delta^2
  * 1-D Green function       d^2 G/dx^2 = -delta(x - x')    (2.124, no 4 pi)
  * normalized Fourier-Bessel functions
        J1m(k_mn rho) = (sqrt(2)/a) Jm(k_mn rho)/J_{m+1}(x_mn)   (4.67/4.286)
        with k_mn = x_mn/a, Jm(x_mn) = 0                        (4.46)
  * reduced Green functions from the Wronskian recipe
        g = C psi_1(x_<) psi_2(x_>),  C = D(x)/W_x[psi_1, psi_2]  (4.128-4.130)
  * spherical harmonics: Schwinger construction (4.167) == scipy's Y_lm
    (Condon-Shortley phase); Coulomb expansion (4.215)/(4.225);
    addition theorem (4.223).

Every reduced Green function here is checked in test_cylindrical_spherical.py
against boundary conditions, the jump (Wronskian) condition, symmetry, and --
where one exists -- an independent closed form or image solution.
"""
from functools import lru_cache

import numpy as np
from scipy import special as sp
from scipy.optimize import brentq
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

# ----------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------

@lru_cache(maxsize=64)
def _leggauss(n):
    return np.polynomial.legendre.leggauss(n)


def gl_nodes(lo, hi, n):
    """Gauss-Legendre nodes/weights on [lo, hi].  For n > 400 a composite
    rule of 200-point panels is used (leggauss(n) is O(n^2)-slow; the
    composite rule has the same node count and comparable accuracy)."""
    if n <= 400:
        x, w = _leggauss(n)
        return 0.5 * (hi - lo) * x + 0.5 * (hi + lo), 0.5 * (hi - lo) * w
    npan = int(np.ceil(n / 200))
    xb, wb = _leggauss(200)
    edges = np.linspace(lo, hi, npan + 1)
    h = np.diff(edges)
    xs = (0.5 * h[:, None] * xb[None, :]
          + 0.5 * (edges[:-1] + edges[1:])[:, None]).ravel()
    ws = (0.5 * h[:, None] * wb[None, :]).ravel()
    return xs, ws


def quad_gl(f, lo, hi, n=200):
    """integral of a vectorized f on [lo, hi] by Gauss-Legendre."""
    x, w = gl_nodes(lo, hi, n)
    return np.sum(w * f(x))


def lap_polar_fd(f, rho, phi, h=1e-4):
    """2-D polar Laplacian f_rr + f_r/r + f_pp/r^2 of f(rho, phi)."""
    frr = (f(rho + h, phi) - 2 * f(rho, phi) + f(rho - h, phi)) / h**2
    fr = (f(rho + h, phi) - f(rho - h, phi)) / (2 * h)
    fpp = (f(rho, phi + h) - 2 * f(rho, phi) + f(rho, phi - h)) / h**2
    return frr + fr / rho + fpp / rho**2


def lap_cyl_axisym_fd(f, rho, z, h=1e-4):
    """axisymmetric cylindrical Laplacian f_rr + f_r/r + f_zz of f(rho, z)."""
    frr = (f(rho + h, z) - 2 * f(rho, z) + f(rho - h, z)) / h**2
    fr = (f(rho + h, z) - f(rho - h, z)) / (2 * h)
    fzz = (f(rho, z + h) - 2 * f(rho, z) + f(rho, z - h)) / h**2
    return frr + fr / rho + fzz


def lap_cyl3d_fd(f, rho, phi, z, h=1e-4):
    """full cylindrical Laplacian of f(rho, phi, z)."""
    frr = (f(rho + h, phi, z) - 2 * f(rho, phi, z) + f(rho - h, phi, z)) / h**2
    fr = (f(rho + h, phi, z) - f(rho - h, phi, z)) / (2 * h)
    fpp = (f(rho, phi + h, z) - 2 * f(rho, phi, z) + f(rho, phi - h, z)) / h**2
    fzz = (f(rho, phi, z + h) - 2 * f(rho, phi, z) + f(rho, phi, z - h)) / h**2
    return frr + fr / rho + fpp / rho**2 + fzz


def lap_sph_axisym_fd(f, r, th, h=1e-4):
    """axisymmetric spherical Laplacian of f(r, theta)."""
    frr = (f(r + h, th) - 2 * f(r, th) + f(r - h, th)) / h**2
    fr = (f(r + h, th) - f(r - h, th)) / (2 * h)
    ftt = (f(r, th + h) - 2 * f(r, th) + f(r, th - h)) / h**2
    ft = (f(r, th + h) - f(r, th - h)) / (2 * h)
    return frr + 2 * fr / r + (ftt + ft / np.tan(th)) / r**2


def lap_sph_angular_fd(F, th, ph, h=1e-4):
    """angular Laplacian (r x grad)^2 F on the unit sphere (Ex. 4.13.2)."""
    ftt = (F(th + h, ph) - 2 * F(th, ph) + F(th - h, ph)) / h**2
    ft = (F(th + h, ph) - F(th - h, ph)) / (2 * h)
    fpp = (F(th, ph + h) - 2 * F(th, ph) + F(th, ph - h)) / h**2
    return ftt + ft / np.tan(th) + fpp / np.sin(th)**2


def ylm(l, m, th, ph):
    """spherical harmonic Y_lm(theta, phi), book convention (4.167)/(4.185)."""
    if hasattr(sp, "sph_harm_y"):
        return sp.sph_harm_y(l, m, th, ph)
    return sp.sph_harm(m, l, ph, th)


def wronskian_fd(f, g, t, h=1e-6):
    """W_t[f, g] = f g' - g f' by central differences."""
    fp = (f(t + h) - f(t - h)) / (2 * h)
    gp = (g(t + h) - g(t - h)) / (2 * h)
    return f(t) * gp - g(t) * fp


# ----------------------------------------------------------------------------
# Sec. 4.1  Bessel functions from the generating function  (P1-P4)
# ----------------------------------------------------------------------------

def jm_taylor(m, t, nterms=80):
    """Taylor series (4.8)/(4.25): Jm(t) = sum (-1)^n (t/2)^{m+2n}/(n!(m+n)!).
    Negative m via J_{-m} = (-1)^m Jm (4.10)."""
    if m < 0:
        return (-1) ** (-m) * jm_taylor(-m, t, nterms)
    n = np.arange(nterms)
    scalar = np.isscalar(t)
    t = np.atleast_1d(np.asarray(t, dtype=float))
    logs = ((m + 2 * n[:, None]) * np.log(np.abs(t[None, :]) / 2.0)
            - sp.gammaln(n[:, None] + 1) - sp.gammaln(m + n[:, None] + 1))
    terms = (-1.0) ** n[:, None] * np.exp(logs)
    out = terms.sum(axis=0)
    return float(out[0]) if scalar else out


def jn_intrep_413(n, t, npts=4000):
    """integral representation (4.13): Jn = i^{-n} int dphi/2pi e^{i(t cos-n phi)}."""
    ph = np.linspace(0.0, 2 * np.pi, npts, endpoint=False)
    val = np.mean(np.exp(1j * (t * np.cos(ph) - n * ph)))
    return ((-1j) ** n * val).real


def jn_intrep_415(n, t, npts=4000):
    """(4.15): Jn = (1/2pi) int_{-pi}^{pi} dphi e^{i t sin phi - i n phi}."""
    ph = np.linspace(-np.pi, np.pi, npts, endpoint=False)
    return np.mean(np.exp(1j * (t * np.sin(ph) - n * ph))).real


def jn_intrep_416(n, t, npts=4000):
    """(4.16): Jn = (1/pi) int_0^pi dphi cos(t sin phi - n phi)."""
    ph = np.linspace(0.0, np.pi, npts, endpoint=False) + 0.5 * np.pi / npts
    return np.mean(np.cos(t * np.sin(ph) - n * ph))


def sumrule_jm_sq(t, M=60):
    """Ex. 4.1.2a: sum_m Jm(t)^2 (should be 1)."""
    m = np.arange(-M, M + 1)
    return np.sum(sp.jv(m, t) ** 2)


def sumrule_j0_2t(t, M=60):
    """Ex. 4.1.2b: sum_m (-1)^m Jm(t)^2 (should be J0(2t))."""
    m = np.arange(-M, M + 1)
    return np.sum((-1.0) ** m * sp.jv(m, t) ** 2)


def int_rho_pow_jm(m, k, a):
    """Ex. 4.1.3 closed form: int_0^a rho^{m+1} Jm(k rho) drho
    = (a^{m+1}/k) (J_{m+1}(ka) - delta_{m,-1})."""
    return a ** (m + 1) / k * (sp.jv(m + 1, k * a) - (1.0 if m == -1 else 0.0))


def int_rho_pow_jm_quad(m, k, a, n=800):
    return quad_gl(lambda r: r ** (m + 1) * sp.jv(m, k * r), 0.0, a, n)


# ----------------------------------------------------------------------------
# Sec. 4.2  completeness / addition theorem  (P5)
# ----------------------------------------------------------------------------

def Dperp(rho, phi, rhop, phip):
    """D = |(x - x')_perp|."""
    return np.hypot(rho * np.cos(phi) - rhop * np.cos(phip),
                    rho * np.sin(phi) - rhop * np.sin(phip))


def addition_j0_series(k, rho, phi, rhop, phip, M=60):
    """Ex. 4.2.1a RHS: sum_m Jm(k rho) Jm(k rho') e^{im(phi-phi')}."""
    m = np.arange(-M, M + 1)
    return np.sum(sp.jv(m, k * rho) * sp.jv(m, k * rhop)
                  * np.exp(1j * m * (phi - phip))).real


def weber_gauss_closed(nu, rho, rhop, p):
    """Weber's second exponential integral (Watson 13.31):
    int_0^inf k e^{-p^2 k^2} J_nu(k rho) J_nu(k rho') dk
      = (1/2p^2) exp(-(rho^2+rho'^2)/4p^2) I_nu(rho rho'/2p^2).
    Gaussian-regulated form of the completeness relation (4.39)."""
    x = rho * rhop / (2 * p**2)
    return (0.5 / p**2 * sp.ive(nu, x)
            * np.exp(x - (rho**2 + rhop**2) / (4 * p**2)))


def weber_gauss_quad(nu, rho, rhop, p, K=None, n=2000):
    if K is None:
        K = 12.0 / p
    return quad_gl(lambda k: k * np.exp(-(p * k) ** 2)
                   * sp.jv(nu, k * rho) * sp.jv(nu, k * rhop), 0.0, K, n)


def weber_gauss_lattice(nu, rho, rhop, p, a, N=4000):
    """same integral as a Riemann sum over the finite-domain completeness
    lattice (4.71): sum_n J1m(k_n rho) J1m(k_n rho') e^{-p^2 k_n^2}
    -> the [0, a] eigen-sum limits onto the Hankel integral as a -> inf
    (Ex. 4.6.1)."""
    x = sp.jn_zeros(nu, N)
    k = x / a
    w = 2.0 / (a * sp.jv(nu + 1, x)) ** 2
    return np.sum(w * np.exp(-(p * k) ** 2) * sp.jv(nu, k * rho)
                  * sp.jv(nu, k * rhop))


def delta2d_gauss_family(D, p):
    """Ex. 4.2.1b nascent delta: int (k dk/2pi) J0(kD) e^{-p^2k^2}
    = (1/4 pi p^2) e^{-D^2/4p^2}  (unit-mass 2-D Gaussian)."""
    return np.exp(-D**2 / (4 * p**2)) / (4 * np.pi * p**2)


# ----------------------------------------------------------------------------
# Sec. 4.3  zeros and orthogonality  (P6)
# ----------------------------------------------------------------------------

def bessel_norm_deriv_zero(m, n, a, nq=2000):
    """Ex. 4.3.1: (quad, closed) for int_0^a rho Jm(kbar rho)^2 drho with
    kbar = y_mn/a, Jm'(y_mn) = 0; closed = (a^2/2)(1 - m^2/y^2) Jm(y)^2 (4.52)."""
    y = sp.jnp_zeros(m, n)[-1]
    kb = y / a
    q = quad_gl(lambda r: r * sp.jv(m, kb * r) ** 2, 0.0, a, nq)
    closed = 0.5 * a**2 * (1 - m**2 / y**2) * sp.jv(m, y) ** 2
    return q, closed


# ----------------------------------------------------------------------------
# Sec. 4.4  reduced Green functions for flat walls / capped cylinder (P7-P10)
# ----------------------------------------------------------------------------

def g_halfspace(k, z, zp):
    """Ex. 4.4.1 answer: reduced g for the grounded wall at z=0 (z, z' > 0):
    g = (e^{-k|z-z'|} - e^{-k(z+z')})/2k  == sinh(k z_<) e^{-k z_>}/k (3.30)."""
    return (np.exp(-k * abs(z - zp)) - np.exp(-k * (z + zp))) / (2 * k)


def G_axisym_from_g(D, z, zp, gfun, K=60.0, n=1200):
    """G = 2 int_0^inf k dk g(k; z, z') J0(kD)   (Ex. 4.4.1 second form)."""
    return 2.0 * quad_gl(lambda k: k * gfun(k, z, zp) * sp.j0(k * D), 1e-9, K, n)


def G_wall_images(D, z, zp):
    """image solution for the grounded wall: 1/|x-x'| - 1/|x-x''|."""
    return 1 / np.hypot(D, z - zp) - 1 / np.hypot(D, z + zp)


def G_halfplane_series(rho, phi, z, rhop, phip, zp, M=80, K=None, n=1600):
    """Ex. 4.4.2: conducting plate = z-x plane, free space y>0 (0<phi<pi):
    GD = 4 int_0^inf dk sum_{m>=1} Jm(k rho) Jm(k rho') sin m phi sin m phi'
         e^{k(z_< - z_>)}."""
    dz = abs(z - zp)
    if K is None:
        K = 40.0 / max(dz, 0.2)
    ms = np.arange(1, M + 1)

    def f(k):
        kk = np.atleast_1d(k)
        t = (sp.jv(ms[:, None], kk[None, :] * rho)
             * sp.jv(ms[:, None], kk[None, :] * rhop)
             * (np.sin(ms * phi) * np.sin(ms * phip))[:, None])
        return t.sum(axis=0) * np.exp(-kk * dz)

    return 4.0 * quad_gl(f, 1e-9, K, n)


def G_halfplane_images(rho, phi, z, rhop, phip, zp):
    """image pair for the plate: reflection y' -> -y' i.e. phi' -> -phi'."""
    x, y = rho * np.cos(phi), rho * np.sin(phi)
    xp, yp = rhop * np.cos(phip), rhop * np.sin(phip)
    d = np.sqrt((x - xp) ** 2 + (y - yp) ** 2 + (z - zp) ** 2)
    di = np.sqrt((x - xp) ** 2 + (y + yp) ** 2 + (z - zp) ** 2)
    return 1 / d - 1 / di


def phi_capacitor_disk(rho, z, a, d, E0, dirichlet_bottom=False, K=80.0, n=2000):
    """Ex. 4.4.3: Neumann top plate at z=d with Ez = E0 on rho<a.
    (a) Neumann bottom (Ez=0 at z=0):
        Phi = -a E0 int dk/k J0(k rho) J1(ka) cosh(kz)/sinh(kd);
    (b) Dirichlet bottom (Phi=0 at z=0): cosh(kz)/sinh(kd) -> sinh(kz)/cosh(kd)."""
    def f(k):
        rad = (np.sinh(k * z) / np.cosh(k * d) if dirichlet_bottom
               else np.cosh(k * z) / np.sinh(k * d))
        return sp.j0(k * rho) * sp.j1(k * a) * rad / k
    return -a * E0 * quad_gl(f, 1e-9, K, n)


def Ez_capacitor_disk(rho, z, a, d, E0, dirichlet_bottom=False, K=80.0,
                      n=2000, eps=0.0):
    """E_z = -dPhi/dz of phi_capacitor_disk (optionally e^{-eps k} regulated)."""
    def f(k):
        rad = (np.cosh(k * z) / np.cosh(k * d) if dirichlet_bottom
               else np.sinh(k * z) / np.sinh(k * d))
        return sp.j0(k * rho) * sp.j1(k * a) * rad * np.exp(-eps * k)
    return a * E0 * quad_gl(f, 1e-9, K, n)


@lru_cache(maxsize=256)
def _jzeros(m, N):
    return sp.jn_zeros(m, N)


def J1m_fn(m, n, a, rho):
    """normalized Fourier-Bessel function J1m(k_mn rho) of (4.67)/(4.286)."""
    x = _jzeros(m, n)[-1]
    return np.sqrt(2.0) / a * sp.jv(m, x * rho / a) / sp.jv(m + 1, x)


def G_halfinf_cyl(rho, phi, z, rhop, phip, zp, a, M=25, N=60):
    """Ex. 4.4.4: Dirichlet G inside the half-infinite capped cylinder
    (rho<a, z>0):
    GD = 2 sum_{m,n} e^{im dphi} J1m(k_mn rho) J1m(k_mn rho')
                     sinh(k z_<) e^{-k z_>}/k     with  k = k_mn = x_mn/a."""
    tot = 0.0
    for m in range(-M, M + 1):
        x = _jzeros(abs(m), N)
        k = x / a
        j1m = (2.0 / a**2 * sp.jv(abs(m), k * rho) * sp.jv(abs(m), k * rhop)
               / sp.jv(abs(m) + 1, x) ** 2)
        gz = np.sinh(k * min(z, zp)) * np.exp(-k * max(z, zp)) / k
        tot += np.cos(m * (phi - phip)) * np.sum(j1m * gz)
    return 2.0 * tot


# ----------------------------------------------------------------------------
# Sec. 4.6  modified Bessel functions; cylinder with side at V  (P11-P12)
# ----------------------------------------------------------------------------

def bessel_zero_asymptotic(m, n):
    """(4.98) => x_mn ~ (n + m/2 - 1/4) pi for large n."""
    return (n + m / 2.0 - 0.25) * np.pi


def phi_cyl_side_V(rho, z, a, L, V, N=400):
    """Ex. 4.6.2: caps (z=0, L) grounded, side rho=a at V:
    Phi = (4V/pi) sum_{odd n} (1/n) I0(n pi rho/L)/I0(n pi a/L) sin(n pi z/L).
    I0 ratio computed with scaled ive for stability."""
    ns = np.arange(1, N + 1, 2)
    k = ns * np.pi / L
    ratio = sp.ive(0, k * rho) / sp.ive(0, k * a) * np.exp(k * (rho - a))
    return 4 * V / np.pi * np.sum(np.sin(k * z) * ratio / ns)


def solve_laplace_axisym(a, L, Vside, nr=48, nz=96):
    """FD solve of the axisymmetric Laplace equation on [0,a]x[0,L] with
    Phi(rho,0)=Phi(rho,L)=0, Phi(a,z)=Vside; regularity at rho=0
    (Phi_rr term doubled).  Returns (rho_grid, z_grid, Phi)."""
    hr, hz = a / nr, L / nz
    idx = lambda i, j: i * (nz - 1) + j          # i: 0..nr-1 (rho), j: 0..nz-2
    Nun = nr * (nz - 1)
    A = lil_matrix((Nun, Nun))
    b = np.zeros(Nun)
    for i in range(nr):                          # rho index (rho = i*hr)
        rho = i * hr
        for j in range(1, nz):                   # z index (z = j*hz)
            row = idx(i, j - 1)
            if i == 0:                           # axis: 4(Phi_1 - Phi_0)/hr^2
                A[row, row] += -4.0 / hr**2 - 2.0 / hz**2
                A[row, idx(1, j - 1)] += 4.0 / hr**2
            else:
                cp = 1.0 / hr**2 + 1.0 / (2 * rho * hr)
                cm = 1.0 / hr**2 - 1.0 / (2 * rho * hr)
                A[row, row] += -2.0 / hr**2 - 2.0 / hz**2
                if i + 1 <= nr - 1:
                    A[row, idx(i + 1, j - 1)] += cp
                else:
                    b[row] -= cp * Vside         # boundary rho=a
                A[row, idx(i - 1, j - 1)] += cm
            if j + 1 <= nz - 1:
                A[row, idx(i, j)] += 1.0 / hz**2
            if j - 1 >= 1:
                A[row, idx(i, j - 2)] += 1.0 / hz**2
    u = spsolve(A.tocsr(), b)
    Phi = np.zeros((nr + 1, nz + 1))
    for i in range(nr):
        for j in range(1, nz):
            Phi[i, j] = u[idx(i, j - 1)]
    Phi[nr, 1:nz] = Vside
    return (np.arange(nr + 1) * hr, np.arange(nz + 1) * hz, Phi)


# ----------------------------------------------------------------------------
# Sec. 4.7  Wronskian technique: free space, disk capacitance, patches
# (P13-P18)
# ----------------------------------------------------------------------------

def disk_C_var(beta, a=1.0, tmax=3000.0, nt=600001):
    """Ex. 4.7.1: variational capacitance of the unit disk with trial
    sigma = A(1 + beta (rho/a)^2).  Uses
      C^{-1}[sigma] = (4 pi^2/Q^2) int_0^inf dk [int_0^a rho J0 sigma]^2
    with the radial integrals in closed form:
      int rho J0 = a J1(t)/k,  int rho (rho/a)^2 J0 = (a/k)(J1 - 2 J2/t),
    t = ka.  Returns C(beta)."""
    t = np.linspace(1e-6, tmax, nt)
    fA = sp.j1(t) / t
    fB = sp.j1(t) / t - 2 * sp.jn(2, t) / t**2
    h = fA + beta * fB                            # (1/a^2) * F(k) * (k/a)...
    # F(k) = a^2 f(t); int dk F^2 = a^3 int dt f^2
    I = np.trapezoid(h * h, t) * a**3
    Q = np.pi * a**2 * (1 + beta / 2.0)
    return Q**2 / (4 * np.pi**2 * I)


def disk_C_var_best(a=1.0):
    """maximize C(beta); returns (C*, beta*)."""
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda b: -disk_C_var(b, a), bounds=(-0.9, 60.0),
                        method="bounded")
    return -r.fun, r.x


def phi_patch_neumann(rho, z, a, E0, K=200.0, n=4000):
    """Ex. 4.7.2: Phi = E0 a int dk/k J0(k rho) J1(ka) e^{-kz} (half-space,
    Neumann wall with Ez = E0 on the disk rho<a)."""
    return E0 * a * quad_gl(
        lambda k: sp.j0(k * rho) * sp.j1(k * a) * np.exp(-k * z) / k,
        1e-9, K, n)


def phi_patch_axis_closed(z, a, E0):
    """on-axis closed form: Phi(0,z) = E0 (sqrt(a^2+z^2) - z)."""
    return E0 * (np.hypot(a, z) - z)


def wronskian_jnu_jmnu(nu, t):
    """Ex. 4.7.3b closed form: W[J_nu, J_-nu](t) = -2 sin(nu pi)/(pi t)."""
    return -2 * np.sin(nu * np.pi) / (np.pi * t)


def wronskian_jm_nm(t):
    """W[Jm, Nm](t) = 2/(pi t)."""
    return 2 / (np.pi * t)


def g_in_cyl(nu, k, rho, rhop, a):
    """Ex. 4.7.4b / 4.8.4: interior reduced Green function of a grounded
    cylinder rho=a (order nu may be fractional):
      g = I(k r_<)[K(k r_>) - I(k r_>) K(ka)/I(ka)].
    Scaled (ive/kve) evaluation, stable for large ka; the k -> 0 (or large
    nu) power-law limit [(r_</r_>)^nu - (r_< r_>/a^2)^nu]/2nu covers ive
    underflow."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    k = np.asarray(k, dtype=float)
    with np.errstate(invalid="ignore", over="ignore"):
        t1 = sp.ive(nu, k * rl) * sp.kve(nu, k * rg) * np.exp(-k * (rg - rl))
        t2 = (sp.ive(nu, k * rl) * sp.ive(nu, k * rg)
              * sp.kve(nu, k * a) / sp.ive(nu, k * a)
              * np.exp(k * (rl + rg - 2 * a)))
        val = t1 - t2
    bad = ~np.isfinite(val)
    if np.any(bad) and nu > 0:
        lim = ((rl / rg) ** nu - (rl * rg / a**2) ** nu) / (2 * nu)
        val = np.where(bad, lim, val)
    return float(val) if val.ndim == 0 else val


def g_out_cyl(m, k, rho, rhop, a):
    """Ex. 4.7.4a: exterior reduced Green function (rho, rho' > a):
      g = [I(k r_<) - K(k r_<) I(ka)/K(ka)] K(k r_>)."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    k = np.asarray(k, dtype=float)
    with np.errstate(invalid="ignore", over="ignore"):
        t1 = sp.ive(m, k * rl) * sp.kve(m, k * rg) * np.exp(-k * (rg - rl))
        t2 = (sp.kve(m, k * rl) * sp.kve(m, k * rg)
              * sp.ive(m, k * a) / sp.kve(m, k * a)
              * np.exp(k * (2 * a - rl - rg)))
        val = t1 - t2
    bad = ~np.isfinite(val)
    if np.any(bad) and m > 0:
        lim = ((rl / rg) ** m - (a * a / (rl * rg)) ** m) / (2 * m)
        val = np.where(bad, lim, val)
    return float(val) if val.ndim == 0 else val


def g_free_cyl(m, k, rho, rhop):
    """free-space reduced g (4.125 with A=1): I_m(k r_<) K_m(k r_>)."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    k = np.asarray(k, dtype=float)
    with np.errstate(invalid="ignore", over="ignore"):
        val = sp.ive(m, k * rl) * sp.kve(m, k * rg) * np.exp(-k * (rg - rl))
    bad = ~np.isfinite(val)
    if np.any(bad) and m > 0:
        val = np.where(bad, (rl / rg) ** m / (2 * m), val)
    return float(val) if val.ndim == 0 else val


def G_cyl_reduced_rho(dphi, dz, gfun, M=40, K=60.0, n=1200):
    """assembler for the (4.122) form:
    G = (2/pi) int_0^inf dk cos(k dz) sum_m e^{im dphi} g_m(k).
    The k = t^2 substitution absorbs the m = 0 log endpoint (I0 K0 ~ -ln k)."""
    tot = 0.0
    for m in range(-M, M + 1):
        val = quad_gl(lambda t: 2 * t * np.cos(t * t * dz) * gfun(abs(m), t * t),
                      1e-6, np.sqrt(K), n)
        tot += np.cos(m * dphi) * val
    return 2.0 / np.pi * tot


def g_toroid(m, k, rho, rhop, a, b):
    """Ex. 4.7.5: reduced g in rho for the rectangular-section toroid
    (a <= rho <= b walls grounded), order m, separation constant k:
      psi1 = I(k rho)K(ka) - K(k rho)I(ka)   (zero at a)
      psi2 = I(k rho)K(kb) - K(k rho)I(kb)   (zero at b)
      g = psi1(r_<) psi2(r_>)/[I(ka)K(kb) - K(ka)I(kb)]
    evaluated in overflow-safe scaled form."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    A1 = sp.ive(m, k * rl) * sp.kve(m, k * a)
    B1 = sp.kve(m, k * rl) * sp.ive(m, k * a)
    A2 = sp.ive(m, k * rg) * sp.kve(m, k * b)
    B2 = sp.kve(m, k * rg) * sp.ive(m, k * b)
    Ad = sp.ive(m, k * a) * sp.kve(m, k * b)
    Bd = sp.kve(m, k * a) * sp.ive(m, k * b)
    num = ((A1 - np.exp(-2 * k * (rl - a)) * B1)
           * (B2 - np.exp(-2 * k * (b - rg)) * A2))
    den = (Bd - np.exp(-2 * k * (b - a)) * Ad)
    val = np.exp(-k * (rg - rl)) * num / den
    if not np.isfinite(val):
        # m >> k b: ive underflows / kve overflows; I_m(x)K_m(y) ->
        # (x/y)^m/2m and g collapses onto the 2-D power-law annulus modes
        return g_concentric_2d(m, rho, rhop, a, b)
    return val


def G_toroid(rho, phi, z, rhop, phip, zp, a, b, L, M=30, N=40):
    """Ex. 4.7.5 assembled: G = (4/L) sum_{m,n} e^{im dphi}
    sin(k_n z) sin(k_n z') g_m(k_n; rho, rho'), k_n = n pi/L."""
    tot = 0.0
    for m in range(-M, M + 1):
        for n in range(1, N + 1):
            kn = n * np.pi / L
            tot += (np.cos(m * (phi - phip)) * np.sin(kn * z)
                    * np.sin(kn * zp) * g_toroid(abs(m), kn, rho, rhop, a, b))
    return 4.0 / L * tot


def coulomb_cylJ(rho, phi, z, rhop, phip, zp, M=60, K=None, n=2000):
    """(4.120): 1/|x-x'| = int dk sum_m e^{im dphi} Jm Jm e^{-k(z_>-z_<)}."""
    dz = abs(z - zp)
    if K is None:
        K = 50.0 / max(dz, 0.25)
    ms = np.arange(-M, M + 1)

    def f(k):
        kk = np.atleast_1d(k)
        t = (sp.jv(np.abs(ms)[:, None], kk[None, :] * rho)
             * sp.jv(np.abs(ms)[:, None], kk[None, :] * rhop)
             * np.cos(ms * (phi - phip))[:, None])
        return t.sum(axis=0) * np.exp(-kk * dz)

    return quad_gl(f, 1e-9, K, n)


def disk_free_potential_lhs(rho, z, zp, a, nr=400, nphi=400):
    """Ex. 4.7.6b LHS: int_0^a rho' drho' int dphi' 1/|x-x'| by quadrature
    (source disk at height z'; field point at (rho, z), phi=0)."""
    r, wr = gl_nodes(0.0, a, nr)
    ph = np.linspace(0, 2 * np.pi, nphi, endpoint=False)
    dph = 2 * np.pi / nphi
    R = np.sqrt(rho**2 + r[:, None]**2
                - 2 * rho * r[:, None] * np.cos(ph[None, :]) + (z - zp)**2)
    return np.sum(wr[:, None] * r[:, None] / R) * dph


def disk_free_potential_rhs(rho, z, zp, a, K=300.0, n=6000):
    """Ex. 4.7.6b RHS: 2 pi a int dk/k J0(k rho) J1(ka) e^{-k|z-z'|}."""
    return 2 * np.pi * a * quad_gl(
        lambda k: sp.j0(k * rho) * sp.j1(k * a) * np.exp(-k * abs(z - zp)) / k,
        1e-9, K, n)


# ----------------------------------------------------------------------------
# Sec. 4.8  conducting wedge family  (P19-P23)
# ----------------------------------------------------------------------------

def wedge_series(rho, phi, rhop, phip, beta, N=4000, a=None):
    """(4.142)/(4.143): G = sum_n (4/n) u^gamma [1 - (rho_>/a)^{2 gamma}]
    sin(n pi phi/beta) sin(n pi phi'/beta), gamma = n pi/beta, u = rho_</rho_>.
    a=None gives the open wedge (4.143)."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    ns = np.arange(1, N + 1)
    gam = ns * np.pi / beta
    u = (rl / rg) ** gam
    if a is not None:
        u = u * (1 - (rg / a) ** (2 * gam))
    return np.sum(4.0 / ns * u * np.sin(ns * np.pi * phi / beta)
                  * np.sin(ns * np.pi * phip / beta))


def wedge_closed(rho, phi, rhop, phip, beta):
    """Ex. 4.8.1 closed form:
    G = ln[ (1 + u^{2q} - 2u^q cos(q(phi+phi'))) /
            (1 + u^{2q} - 2u^q cos(q(phi-phi'))) ],  q = pi/beta, u = r_</r_>."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    q = np.pi / beta
    u = (rl / rg) ** q
    num = 1 + u**2 - 2 * u * np.cos(q * (phi + phip))
    den = 1 + u**2 - 2 * u * np.cos(q * (phi - phip))
    return np.log(num / den)


def g_wedge_annulus(gam, rho, rhop, a, b):
    """Ex. 4.8.2: reduced g_n for the closed wedge a <= rho <= b
    (both arcs grounded), gamma = n pi/beta; ratio-stable form."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    num = ((rl / rg) ** gam + (a**2 * rg / (b**2 * rl)) ** gam
           - (rl * rg / b**2) ** gam - (a**2 / (rl * rg)) ** gam)
    return num / (2 * gam * (1 - (a / b) ** (2 * gam)))


def G_wedge_annulus(rho, phi, rhop, phip, beta, a, b, N=400):
    """Ex. 4.8.2 assembled: G = (8 pi/beta) sum_n sin sin g_n  (4.133)."""
    tot = 0.0
    for nn in range(1, N + 1):
        gam = nn * np.pi / beta
        tot += (np.sin(nn * np.pi * phi / beta) * np.sin(nn * np.pi * phip / beta)
                * g_wedge_annulus(gam, rho, rhop, a, b))
    return 8 * np.pi / beta * tot


def cyl2d_series(rho, phi, rhop, phip, a, M=2000):
    """Ex. 4.8.3: GD = -ln(rho_>^2/a^2)
    + 2 sum_m cos(m dphi)/m rho_<^m (1/rho_>^m - rho_>^m/a^{2m})."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    m = np.arange(1, M + 1)
    term = ((rl / rg) ** m - (rl * rg / a**2) ** m) / m
    return (-np.log(rg**2 / a**2)
            + 2 * np.sum(np.cos(m * (phi - phip)) * term))


def cyl2d_image(rho, phi, rhop, phip, a):
    """Ex. 4.8.3 Extra / Ex. 3.3.5b image form:
    GD = ln[(a^4 + rho^2 rho'^2 - 2 a^2 rho rho' cos dphi)
            /(a^2 (rho^2 + rho'^2 - 2 rho rho' cos dphi))]."""
    c = np.cos(phi - phip)
    num = a**4 + rho**2 * rhop**2 - 2 * a**2 * rho * rhop * c
    den = a**2 * (rho**2 + rhop**2 - 2 * rho * rhop * c)
    return np.log(num / den)


def G_wedge3d(rho, phi, z, rhop, phip, zp, beta, a, N=30, K=None, n=1200):
    """Ex. 4.8.4: point charge in the wedge-shaped hole (radius a, angle
    beta):  G = (8/beta) sum_n sin(n pi phi/beta) sin(n pi phi'/beta)
    int_0^inf dk cos(k(z-z')) g_nu(k), nu = n pi/beta, with g_nu the interior
    cylinder reduced Green function of fractional order (g_in_cyl)."""
    dz = abs(z - zp)
    dr = abs(rho - rhop)
    if K is None:
        K = 45.0 / max(min(dr + 1e-12, 2 * a - rho - rhop + 1e-12, dz + dr),
                       0.25)
    tot = 0.0
    for nn in range(1, N + 1):
        nu = nn * np.pi / beta
        val = quad_gl(lambda k: np.cos(k * dz) * g_in_cyl(nu, k, rho, rhop, a),
                      1e-9, K, n)
        tot += np.sin(nn * np.pi * phi / beta) * np.sin(nn * np.pi * phip / beta) * val
    return 8.0 / beta * tot


def g_concentric_2d(m, rho, rhop, b, a):
    """Ex. 4.8.5 reduced g_m, grounded concentric cylinders b <= rho <= a
    (inner b, outer a).  m = 0: -ln(r_</b) ln(r_>/a)/ln(a/b); m >= 1
    power-law analog (ratio-stable)."""
    rl, rg = min(rho, rhop), max(rho, rhop)
    if m == 0:
        return -np.log(rl / b) * np.log(rg / a) / np.log(a / b)
    num = ((rl / rg) ** m + (b**2 * rg / (a**2 * rl)) ** m
           - (rl * rg / a**2) ** m - (b**2 / (rl * rg)) ** m)
    return num / (2 * m * (1 - (b / a) ** (2 * m)))


def G_concentric_2d(rho, phi, rhop, phip, b, a, M=800):
    """Ex. 4.8.5 assembled: G = 2 g_0 + 4 sum_{m>=1} cos(m dphi) g_m."""
    tot = 2.0 * g_concentric_2d(0, rho, rhop, b, a)
    for m in range(1, M + 1):
        tot += 4.0 * np.cos(m * (phi - phip)) * g_concentric_2d(m, rho, rhop, b, a)
    return tot

# ----------------------------------------------------------------------------
# Sec. 4.9  Legendre polynomials / spherical harmonics  (P24-P26)
# ----------------------------------------------------------------------------

def dfact(N):
    """double factorial with (0)!! = (-1)!! = 1."""
    if N <= 0:
        return 1.0
    out = 1.0
    while N > 0:
        out *= N
        N -= 2
    return out


def legendre_explicit(l, x):
    """Ex. 4.9.1a: P_l(x) = sum_r (-1)^r (2l-2r-1)!!/[(2r)!! (l-2r)!] x^{l-2r}."""
    from math import factorial
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    for r in range(l // 2 + 1):
        out += ((-1) ** r * dfact(2 * l - 2 * r - 1)
                / (dfact(2 * r) * factorial(l - 2 * r)) * x ** (l - 2 * r))
    return out


def legendre0(l):
    """Ex. 4.9.1b: P_l(0) = 0 (l odd), (-1)^{l/2} (l-1)!!/l!! (l even)."""
    if l % 2 == 1:
        return 0.0
    return (-1) ** (l // 2) * dfact(l - 1) / dfact(l)


def dlegendre0(l, m):
    """Ex. 4.9.1c: (d/dx)^m P_l at x=0 = 0 (l-m odd),
    (-1)^{(l-m)/2} (l+m-1)!!/(l-m)!! (l-m even)."""
    if (l - m) % 2 == 1:
        return 0.0
    return (-1) ** ((l - m) // 2) * dfact(l + m - 1) / dfact(l - m)


def legendre0_seq(N):
    """P_{2n}(0), n = 0..N-1, by the stable recursion q_n = -q_{n-1}(2n-1)/2n."""
    q = np.empty(N)
    q[0] = 1.0
    for n in range(1, N):
        q[n] = -q[n - 1] * (2 * n - 1) / (2.0 * n)
    return q


# ----------------------------------------------------------------------------
# Sec. 4.11  Coulomb expansion / addition theorem / hemisphere bound
# (P27-P32)
# ----------------------------------------------------------------------------

def sph_quad(nth=120, nph=240):
    """product quadrature on the sphere: GL in cos(theta) x trapezoid in phi.
    Returns (theta, phi, w2d) with sum(w2d) = 4 pi."""
    x, wx = _leggauss(nth)
    th = np.arccos(x)
    ph = np.linspace(0, 2 * np.pi, nph, endpoint=False)
    w2 = wx[:, None] * (2 * np.pi / nph) * np.ones((1, nph))
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    return TH, PH, w2


def unit_vec(th, ph):
    return np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph),
                     np.cos(th)])


def integral_PlPl(l, u1, u2, nth=120, nph=240):
    """Ex. 4.11.3: int dOmega' P_l(u1.n') P_l(n'.u2)
    (should be 4pi/(2l+1) P_l(u1.u2))."""
    TH, PH, W = sph_quad(nth, nph)
    n = np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH),
                  np.cos(TH)])
    c1 = np.einsum("i,ijk->jk", u1, n)
    c2 = np.einsum("i,ijk->jk", u2, n)
    return np.sum(W * sp.eval_legendre(l, c1) * sp.eval_legendre(l, c2))


def int_Pl(l, x0):
    """int_{x0}^1 P_l dx = [P_{l-1}(x0) - P_{l+1}(x0)]/(2l+1) (l>=1);
    l=0: 1-x0.  (from (4.182))"""
    if l == 0:
        return 1.0 - x0
    return (sp.eval_legendre(l - 1, x0) - sp.eval_legendre(l + 1, x0)) / (2 * l + 1)


def _cl_dl(L):
    """c_l = int_0^1 P_l dx and d_l = int_0^1 x P_l dx for l = 0..L,
    via P(0) recursion and x P_l = [(l+1)P_{l+1} + l P_{l-1}]/(2l+1)."""
    q = legendre0_seq(L // 2 + 3)                 # P_{2n}(0)
    P0 = np.zeros(L + 4)
    P0[0::2] = q[: len(P0[0::2])]
    ls = np.arange(L + 1)
    c = np.zeros(L + 1)
    c[0] = 1.0
    c[1:] = (P0[ls[1:] - 1] - P0[ls[1:] + 1]) / (2 * ls[1:] + 1)
    cext = np.zeros(L + 3)
    cext[: L + 1] = c
    cext[L + 1] = (P0[L] - P0[L + 2]) / (2 * (L + 1) + 1)
    cext[L + 2] = (P0[L + 1] - P0[L + 3]) / (2 * (L + 2) + 1)
    d = np.zeros(L + 1)
    d[0] = 0.5
    d[1:] = ((ls[1:] + 1) * cext[ls[1:] + 1] + ls[1:] * cext[ls[1:] - 1]) \
        / (2 * ls[1:] + 1)
    return c, d


def hemi_C_var(beta, a=1.0, L=6000):
    """Ex. 4.11.4: variational capacitance of the hemispherical bowl with
    sigma = A(1 + beta x), x = cos theta:
      C^{-1} = (4 pi^2 a^3/Q^2) sum_l [int_0^1 P_l sigma dx]^2,
      Q = 2 pi a^2 A (1 + beta/2).  Returns C(beta)."""
    c, d = _cl_dl(L)
    S = np.sum((c + beta * d) ** 2)
    Q = 2 * np.pi * a**2 * (1 + beta / 2.0)
    return Q**2 / (4 * np.pi**2 * a**3 * S)


def hemi_C_var_best(a=1.0, L=6000):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda b: -hemi_C_var(b, a, L), bounds=(-0.999, 2.0),
                        method="bounded")
    return -r.fun, r.x


def rotation_matrix_random(rng):
    """random proper rotation via QR."""
    Q, R = np.linalg.qr(rng.normal(size=(3, 3)))
    Q *= np.sign(np.diag(R))
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q


def angles_of(v):
    th = np.arccos(np.clip(v[2] / np.linalg.norm(v), -1, 1))
    ph = np.arctan2(v[1], v[0])
    return th, ph


def ylm_rotation_coeffs(l, R, rng):
    """Ex. 4.11.5: solve Y_lm(R^T n) = sum_m' C_{mm'} Y_lm'(n) from 2l+1
    sample directions; returns C (rows m)."""
    npts = 2 * l + 1
    us, A, B = [], np.zeros((npts, npts), complex), np.zeros((npts, npts), complex)
    while len(us) < npts:
        v = rng.normal(size=3)
        v /= np.linalg.norm(v)
        us.append(v)
    for j, u in enumerate(us):
        th, ph = angles_of(u)
        thr, phr = angles_of(R.T @ u)
        for i, m in enumerate(range(-l, l + 1)):
            A[j, i] = ylm(l, m, th, ph)
            B[j, i] = ylm(l, m, thr, phr)
    # columns of B give Y_lm(R^T n) at sample points; solve A x = B_col
    C = np.linalg.solve(A, B).T          # C[m, m'] with Y_lm(rot) = sum C Y_lm'
    return C


def ylm_rotation_residual(l, R, C, rng, ntest=30):
    """max residual of Y_lm(R^T n) - sum_m' C_{mm'} Y_lm'(n) at fresh points."""
    worst = 0.0
    for _ in range(ntest):
        v = rng.normal(size=3)
        v /= np.linalg.norm(v)
        th, ph = angles_of(v)
        thr, phr = angles_of(R.T @ v)
        Yv = np.array([ylm(l, m, th, ph) for m in range(-l, l + 1)])
        for i, m in enumerate(range(-l, l + 1)):
            worst = max(worst, abs(ylm(l, m, thr, phr) - C[i] @ Yv))
    return worst


def vandermonde_det(t):
    """det of V_{jm} = t_j^m, m = 0..n-1 equals prod_{i<j}(t_j - t_i)."""
    t = np.asarray(t, dtype=complex)
    n = len(t)
    V = t[:, None] ** np.arange(n)[None, :]
    prod = 1.0 + 0j
    for i in range(n):
        for j in range(i + 1, n):
            prod *= (t[j] - t[i])
    return np.linalg.det(V), prod


def sphere_int_coulomb(r, rp, nth=200, nph=1):
    """Ex. 4.11.6a: int dOmega'/|r - r'| (should be 4 pi/r_>).
    Azimuthal symmetry: do the cos(theta') integral x 2 pi."""
    x, w = _leggauss(nth)
    R = np.sqrt(r**2 + rp**2 - 2 * r * rp * x)
    return 2 * np.pi * np.sum(w / R)


def sphere_int_coulomb_costh(r, rp, th, nth=200):
    """Ex. 4.11.6b: int cos(theta') dOmega'/|r-r'|
    (should be (4pi/3)(r_</r_>^2) cos theta).  Field point at polar angle
    theta; do the full sphere quadrature."""
    TH, PH, W = sph_quad(nth, 2 * nth)
    u = unit_vec(th, 0.0)
    n = np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)])
    cg = np.einsum("i,ijk->jk", u, n)
    R = np.sqrt(r**2 + rp**2 - 2 * r * rp * cg)
    return np.sum(W * np.cos(TH) / R)


# ----------------------------------------------------------------------------
# Sec. 4.12  concentric spheres  (P33-P38)
# ----------------------------------------------------------------------------

def caps_terms(N):
    """Ex. 4.12.1: series terms t_n = [P_{2n}(0) - P_{2n+2}(0)]^2 and the
    double-factorial form [(4n+3)(2n-1)!!/(2n+2)!!]^2, n = 0..N-1.
    C = (a/2) sum t_n  (log-divergent: the ideal split-sphere capacitor has
    infinite gap capacitance)."""
    q = legendre0_seq(N + 2)
    t_leg = (q[:N] - q[1:N + 1]) ** 2
    r = np.empty(N)                                # (2n-1)!!/(2n+2)!!
    r[0] = 0.5
    for n in range(1, N):
        r[n] = r[n - 1] * (2 * n - 1) / (2 * n + 2.0)
    t_dfact = ((4 * np.arange(N) + 3) * r) ** 2
    return t_leg, t_dfact


def caps_C_partial(N, a=1.0):
    t, _ = caps_terms(N)
    return 0.5 * a * np.sum(t)


def split_sphere_Al(l, x0, V1, V2):
    """coefficient A_l = ((2l+1)/2)[V1 int_{x0}^1 P_l + V2 int_{-1}^{x0} P_l]
    of the interior expansion for a sphere at V1 above x0, V2 below."""
    Ip = int_Pl(l, x0)
    Iall = 2.0 if l == 0 else 0.0     # int_{-1}^{1} P_l dx
    Im = Iall - Ip                    # int_{-1}^{x0} P_l dx
    return 0.5 * (2 * l + 1) * (V1 * Ip + V2 * Im)


def caps_sigma(x, V, a, L):
    """Ex. 4.12.1: surface charge density of the +-V hemisphere capacitor,
    sigma = (1/4 pi a) sum_l (2l+1) A_l P_l(x), truncated at L."""
    tot = 0.0
    for l in range(1, L + 1, 2):
        A = split_sphere_Al(l, 0.0, V, -V)
        tot += (2 * l + 1) * A * sp.eval_legendre(l, x)
    return tot / (4 * np.pi * a)


def caps_Q_top(V, a, L, nq=400):
    """charge on the top cap by direct quadrature of caps_sigma."""
    x, w = gl_nodes(0.0, 1.0, nq)
    return 2 * np.pi * a**2 * np.sum(w * caps_sigma(x, V, a, L))


def gN_ext_sphere_series(r, rp, cosg, a, L=200):
    """Ex. 4.12.2: Neumann Green function outside a sphere of radius a:
    GN = 1/r_> + sum_{l>=1} [r_<^l/r_>^{l+1}
         + (l/(l+1)) a^{2l+1}/(r r')^{l+1}] P_l(cos gamma)."""
    rl, rg = min(r, rp), max(r, rp)
    tot = 1.0 / rg
    u = rl / rg                      # ratio-stable: r_<^l/r_>^{l+1} = u^l/r_>
    t = a * a / (r * rp)             # a^{2l+1}/(r r')^{l+1} = t^{l+1}/a
    for l in range(1, L + 1):
        tot += ((u ** l / rg + l / (l + 1.0) * t ** (l + 1) / a)
                * sp.eval_legendre(l, cosg))
    return tot


def gN_ext_sphere_closed(r, rp, cosg, a):
    """closed form (image + line-image):
    GN = 1/R + (a/r')/R_a - (1/a) ln[(t - x + sqrt(1-2tx+t^2))/(1-x)],
    R_a = |x - a^2 rhat'/r'|, t = a^2/(r r'), x = cos gamma."""
    R = np.sqrt(r**2 + rp**2 - 2 * r * rp * cosg)
    ra = a**2 / rp
    Ra = np.sqrt(r**2 + ra**2 - 2 * r * ra * cosg)
    t = a**2 / (r * rp)
    T = np.sqrt(1 - 2 * t * cosg + t**2)
    return 1 / R + a / (rp * Ra) - np.log((t - cosg + T) / (1 - cosg)) / a


def gN_shell(l, r, rp, a, b):
    """Ex. 4.12.3 (l >= 1): interior Neumann reduced Green function between
    concentric spheres a < r < b:
      g_l = l(l+1)/[(2l+1)(b^{2l+1}-a^{2l+1})]
            [r_<^l/l + a^{2l+1}/((l+1) r_<^{l+1})]
            [r_>^l/l + b^{2l+1}/((l+1) r_>^{l+1})]."""
    rl, rg = min(r, rp), max(r, rp)
    # ratio-stable expansion of C p1 p2 (every power base is <= 1):
    u, w, s = rl / rg, rg / b, a / b
    t1 = (u * w * w) ** l / (l * l * b)
    t2 = u ** l / (l * (l + 1.0) * rg)
    t3 = (a * a * rg / (rl * b * b)) ** l * a / (l * (l + 1.0) * rl * b)
    t4 = (a * a / (rl * rg)) ** l * a / ((l + 1.0) ** 2 * rl * rg)
    return l * (l + 1.0) / ((2 * l + 1) * (1 - s ** (2 * l + 1))) \
        * (t1 + t2 + t3 + t4)


def gN_shell_g0(r, rp, a, b):
    """the l = 0 mode fixed by d(g0)/dr = +-(4 pi/S)/(1) at r=a,b
    (S = 4 pi (a^2+b^2)) and symmetrized: g0 = 1/r_> - C1 (1/r + 1/r')+const,
    C1 = a^2/(a^2+b^2); the additive constant is NOT determined (Sec. 2.8)."""
    C1 = a**2 / (a**2 + b**2)
    return 1.0 / max(r, rp) - C1 * (1.0 / r + 1.0 / rp)


def sphere_poisson_kernel(r, th, ph, a, Vfun, inside=True, nth=200, nph=256):
    """Ex. 4.12.4b: Phi = +-a(a^2-r^2)/4pi oint dO' V/(a^2+r^2-2ar cosg)^{3/2}
    (+ inside, - outside)."""
    TH, PH, W = sph_quad(nth, nph)
    u = unit_vec(th, ph)
    n = np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)])
    cg = np.einsum("i,ijk->jk", u, n)
    ker = (a**2 - r**2) / (a**2 + r**2 - 2 * a * r * cg) ** 1.5
    s = 1.0 if inside else -1.0
    return s * a / (4 * np.pi) * np.sum(W * Vfun(TH, PH) * ker)


def sphere_series_from_V(r, th, ph, a, Vfun, inside=True, L=12,
                         nth=200, nph=256):
    """Ex. 4.12.4a: Phi = sum_lm (r/a)^l or (a/r)^{l+1} Y_lm B_lm,
    B_lm = oint dO' V Y*_lm."""
    TH, PH, W = sph_quad(nth, nph)
    Vg = Vfun(TH, PH)
    tot = 0.0 + 0j
    for l in range(L + 1):
        rad = (r / a) ** l if inside else (a / r) ** (l + 1)
        for m in range(-l, l + 1):
            B = np.sum(W * Vg * np.conj(ylm(l, m, TH, PH)))
            tot += rad * B * ylm(l, m, th, ph)
    return tot.real


def hemi_basin_phi(r, th, a, V, L=400):
    """Ex. 4.12.5: interior of the hemisphere 0<theta<pi/2, dome (r=a) at 0,
    base (theta=pi/2) at V:
    Phi = V [1 - sum_{l odd} (P_{l-1}(0)-P_{l+1}(0)) (r/a)^l P_l(cos th)]."""
    q = legendre0_seq(L // 2 + 2)                 # q[n] = P_{2n}(0), stable
    tot = 1.0
    for l in range(1, L + 1, 2):
        coef = q[(l - 1) // 2] - q[(l + 1) // 2]  # P_{l-1}(0) - P_{l+1}(0)
        tot -= coef * (r / a) ** l * sp.eval_legendre(l, np.cos(th))
    return V * tot


def concentric_C(a, b):
    """Ex. 4.12.6: capacitance matrix of concentric spheres (inner a, outer
    b) from the l=0 Dirichlet Green function modes:
    Caa = ab/(b-a), Cab = Cba = -ab/(b-a), Cbb = ab/(b-a) + b."""
    core = a * b / (b - a)
    return core, -core, core + b


# ----------------------------------------------------------------------------
# Sec. 4.13  split spheres, sphere point-electrostatics  (P39-P43)
# ----------------------------------------------------------------------------

def E_center_split(a, th0, V):
    """Ex. 4.13.1: E_z at the center of a sphere with cap (theta<th0) at V,
    rest at -V:  E_z = -(3V/2a) sin^2 th0  (from the l=1 coefficient)."""
    return -1.5 * V * np.sin(th0) ** 2 / a


def E_center_split_fd(a, th0, V, L=800, dr=1e-4):
    """same by FD gradient of the truncated interior series along z."""
    x0 = np.cos(th0)

    def phi(z):
        r, th = abs(z), (0.0 if z >= 0 else np.pi)
        tot = 0.0
        for l in range(1, L + 1):
            A = split_sphere_Al(l, x0, V, -V)
            tot += A * (r / a) ** l * sp.eval_legendre(l, np.cos(th))
        return tot

    return -(phi(dr) - phi(-dr)) / (2 * dr)


def Q0_legendre(x):
    """Legendre function of the second kind, Q0 = (1/2) ln((1+x)/(1-x))."""
    return 0.5 * np.log((1 + x) / (1 - x))


def sphereG_series(cosg, L=4001):
    """Ex. 4.13.2b: sum_{l odd} (2l+1)/(l(l+1)) P_l(cos gamma); equals
    Q0(cos gamma).  (The book's printed prefactor 2 in (b) is inconsistent
    with its own part (a): the PDE normalization gives coefficient
    (2l+1)/(l(l+1)) exactly.)  Cesaro-averaged partial sums for convergence."""
    ls = np.arange(1, L + 1, 2)
    terms = (2 * ls + 1) / (ls * (ls + 1.0)) * sp.eval_legendre(ls, cosg)
    csum = np.cumsum(terms)
    # average the last quarter of partial sums (oscillatory tail)
    tail = csum[3 * len(csum) // 4:]
    return tail.mean()


def unequal_caps_V2(V1, th0):
    """Ex. 4.13.3a: V2 = -[(1-cos th0)/(1+cos th0)] V1 (zero total charge)."""
    return -(1 - np.cos(th0)) / (1 + np.cos(th0)) * V1


def unequal_caps_C_book(x0, L, a=1.0):
    """Ex. 4.13.3b exactly as printed:
    C = (a/8) sum_l (2l+1)^2 I_+ [(1+x0) I_+ + (x0-1) I_-],
    I_+ = int_{x0}^1 P_l dx, I_- = int_{-1}^{x0} P_l dx."""
    tot = 0.0
    for l in range(1, L + 1):
        Ip = int_Pl(l, x0)
        Im = -Ip                      # int_{-1}^{1} P_l = 0 for l >= 1
        tot += (2 * l + 1) ** 2 * Ip * ((1 + x0) * Ip + (x0 - 1) * Im)
    return a / 8.0 * tot


def unequal_caps_C_simple(x0, L, a=1.0):
    """same series, simplified with I_- = -I_+: C = (a/4) sum (2l+1)^2 I_+^2."""
    tot = 0.0
    for l in range(1, L + 1):
        tot += ((2 * l + 1) * int_Pl(l, x0)) ** 2
    return a / 4.0 * tot


def halves_C11_C12(L, a=1.0):
    """Ex. 4.13.4: C11 = (a/4) sum_l (2l+1)^2 [int_0^1 P_l]^2,
    C12 = same with (-1)^l.  Partial sums to l = L."""
    C11 = C12 = 0.0
    for l in range(0, L + 1):
        t = ((2 * l + 1) * int_Pl(l, 0.0)) ** 2
        C11 += t
        C12 += (-1) ** l * t
    return a / 4.0 * C11, a / 4.0 * C12


def gD_halfspace_sph_series(r, th, ph, rp, thp, php, L=60):
    """Ex. 4.13.5: GD above the conducting plane theta = pi/2, as a spherical
    harmonic sum: GD = sum_{l+m odd} (8 pi/(2l+1)) (r_<^l/r_>^{l+1})
    Y_lm(th,ph) Y*_lm(th',ph')."""
    rl, rg = min(r, rp), max(r, rp)
    tot = 0.0 + 0j
    for l in range(L + 1):
        rad = 8 * np.pi / (2 * l + 1) * rl ** l / rg ** (l + 1)
        for m in range(-l, l + 1):
            if (l + m) % 2 == 1:
                tot += rad * ylm(l, m, th, ph) * np.conj(ylm(l, m, thp, php))
    return tot.real


def gD_halfspace_sph_images(r, th, ph, rp, thp, php):
    x1 = r * unit_vec(th, ph)
    x2 = rp * unit_vec(thp, php)
    x2i = rp * unit_vec(np.pi - thp, php)
    return 1 / np.linalg.norm(x1 - x2) - 1 / np.linalg.norm(x1 - x2i)


# ----------------------------------------------------------------------------
# Sec. 4.14  eigenfunction expansions  (P44-P49)
# ----------------------------------------------------------------------------

def sine_delta_action(f, x, L, N=400, nq=800):
    """Ex. 4.14.1: int dx' f(x') sum_n^N psi_n(x) psi_n(x') with
    psi_n = sqrt(2/L) sin(n pi x/L)  ->  f(x)."""
    xq, wq = gl_nodes(0.0, L, nq)
    n = np.arange(1, N + 1)
    cn = np.sum(wq * f(xq) * np.sqrt(2 / L) * np.sin(n[:, None] * np.pi
                                                     * xq[None, :] / L), axis=1)
    return np.sum(cn * np.sqrt(2 / L) * np.sin(n * np.pi * x / L))


def g_plates_z(k, z, zp, a):
    """reduced g between grounded plates z=0,a (3.97/4.78):
    sinh(k z_<) sinh(k(a - z_>))/(k sinh(ka)), overflow-safe."""
    zl, zg = min(z, zp), max(z, zp)
    # = [e^{-k(zg-zl)} - e^{-k(zg+zl)} - e^{-k(2a-zg-zl)} + e^{-k(2a+zl-zg)}]
    #   / (2k(1 - e^{-2ka}))
    e = np.exp
    num = (e(-k * (zg - zl)) - e(-k * (zg + zl))
           - e(-k * (2 * a - zg - zl)) + e(-k * (2 * a - zg + zl)))
    return num / (2 * k * (1 - e(-2 * k * a)))


def G_plates_bessel(D, z, zp, a, K=None, n=2000):
    """Ex. 4.14.2 (k-integral done over the (4.79)-type reduced g):
    GD = 2 int k dk J0(kD) g_plates(k)   == (4/a) int k dk J0(kD)
         sum_n sin sin/(k^2 + (n pi/a)^2)  by the Ex. 4.14.5 sum rule.
    The free part e^{-k|z-z'|}/2k of g is split off and integrated exactly
    (-> 1/|x-x'|); the remainder decays like e^{-k min(z+z', 2a-z-z')}, so
    the truncated quadrature converges absolutely (needed at z = z')."""
    if K is None:
        K = 60.0 / max(min(z + zp, 2 * a - z - zp), 0.15)
    reg = quad_gl(lambda k: (k * g_plates_z(k, z, zp, a)
                             - 0.5 * np.exp(-k * abs(z - zp))) * sp.j0(k * D),
                  1e-13, K, n)
    return 1.0 / np.hypot(D, z - zp) + 2.0 * reg


def G_plates_images(D, z, zp, a, N=600):
    """image-ladder Green function between grounded plates (Ex. 3.1.1)."""
    ns = np.arange(-N, N + 1)
    return np.sum(1 / np.sqrt(D**2 + (z - 2 * ns * a - zp) ** 2)
                  - 1 / np.sqrt(D**2 + (z - 2 * ns * a + zp) ** 2))


def G_finite_cyl_79(rho, phi, z, rhop, phip, zp, a, L, M=20, N=40):
    """(4.79): Dirichlet G inside the finite grounded cylinder (rho<a,
    0<z<L):  G = 2 sum_{m,n} e^{im dphi} J1m(k_mn rho) J1m(k_mn rho')
    sinh(k z_<) sinh(k(L - z_>))/(k sinh(kL)),  k = k_mn = x_mn/a."""
    tot = 0.0
    for m in range(-M, M + 1):
        x = _jzeros(abs(m), N)
        k = x / a
        j1m = (2.0 / a**2 * sp.jv(abs(m), k * rho) * sp.jv(abs(m), k * rhop)
               / sp.jv(abs(m) + 1, x) ** 2)
        gz = np.array([g_plates_z(kk, z, zp, L) for kk in k])
        tot += np.cos(m * (phi - phip)) * np.sum(j1m * gz)
    return 2.0 * tot


def G_finite_cyl_eigen(rho, phi, z, rhop, phip, zp, a, L, M=20, N=40, P=60):
    """Ex. 4.14.5: the same G as a full eigenfunction expansion (4.268):
    G = 4 pi sum psi(x) psi*(x')/k^2 with psi = J1m(k_mn rho)
    (e^{im phi}/sqrt(2 pi)) sqrt(2/L) sin(p pi z/L),
    k^2 = k_mn^2 + (p pi/L)^2."""
    ps = np.arange(1, P + 1)
    kz = ps * np.pi / L
    zfac = np.sin(kz * z) * np.sin(kz * zp) * (2.0 / L)
    tot = 0.0
    for m in range(-M, M + 1):
        x = _jzeros(abs(m), N)
        kmn = x / a
        j1m = (2.0 / a**2 * sp.jv(abs(m), kmn * rho) * sp.jv(abs(m), kmn * rhop)
               / sp.jv(abs(m) + 1, x) ** 2)
        lam = kmn[:, None] ** 2 + kz[None, :] ** 2
        tot += (np.cos(m * (phi - phip)) / (2 * np.pi)
                * np.sum(j1m[:, None] * zfac[None, :] / lam))
    return 4.0 * np.pi * tot


def sumrule_sine(k, z, zp, L, N=20000):
    """Ex. 4.14.5 LHS: sum_n sin(k_n z) sin(k_n z')/(k^2 + k_n^2)."""
    n = np.arange(1, N + 1)
    kn = n * np.pi / L
    return np.sum(np.sin(kn * z) * np.sin(kn * zp) / (k**2 + kn**2))


def sumrule_sine_closed(k, z, zp, L):
    """Ex. 4.14.5 RHS: (L/2) sinh(k z_<) sinh(k(L-z_>))/(k sinh kL)."""
    return 0.5 * L * g_plates_z(k, z, zp, L) * 1.0


def g_in_eigen(m, k, rho, rhop, a, N=400):
    """Ex. 4.14.3: eigen-expansion of the interior cylinder reduced g:
    g = sum_n J1m(k_mn rho) J1m(k_mn rho')/(k^2 + k_mn^2)."""
    x = _jzeros(m, N)
    kmn = x / a
    j1 = (np.sqrt(2) / a) * sp.jv(m, kmn * rho) / sp.jv(m + 1, x)
    j2 = (np.sqrt(2) / a) * sp.jv(m, kmn * rhop) / sp.jv(m + 1, x)
    return np.sum(j1 * j2 / (k**2 + kmn**2))


def g1d_eigen(x, xp, L, N=20000):
    """Ex. 4.14.4: G = (2/L) sum_n sin sin/k_n^2 (conventions of (2.124))."""
    n = np.arange(1, N + 1)
    kn = n * np.pi / L
    return 2.0 / L * np.sum(np.sin(kn * x) * np.sin(kn * xp) / kn**2)


def g1d_closed(x, xp, L):
    """1-D Dirichlet Green function x_<(L - x_>)/L (Sec. 2.9)."""
    return min(x, xp) * (L - max(x, xp)) / L


def sph_jn_zeros(l, nz):
    """first nz zeros of the spherical Bessel function j_l (Ex. 4.14.6b:
    eigenvalues k = z_{ln}/a)."""
    zeros = []
    x = max(2.0, l)
    while len(zeros) < nz:
        f = lambda t: sp.spherical_jn(l, t)
        a_, b_ = x, x + 0.5
        while f(a_) * f(b_) > 0:
            a_, b_ = b_, b_ + 0.5
        zeros.append(brentq(f, a_, b_))
        x = zeros[-1] + 2.0
    return np.array(zeros)


def sph_radial_residual(l, k, r, h=1e-5):
    """Ex. 4.14.6a: residual of (1/r^2)(r^2 j')' + (k^2 - l(l+1)/r^2) j = 0."""
    f = lambda rr: sp.spherical_jn(l, k * rr)
    d2 = (f(r + h) - 2 * f(r) + f(r - h)) / h**2
    d1 = (f(r + h) - f(r - h)) / (2 * h)
    return d2 + 2 * d1 / r + (k**2 - l * (l + 1) / r**2) * f(r)


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    print("MACRO_EM-04 demo (Gaussian units)")
    print("  disk variational C (uniform trial, Ex. 4.7.1):",
          f"{disk_C_var(0.0):.6f}  (3 pi/16 = {3*np.pi/16:.6f})")
    Cb, bb = disk_C_var_best()
    print(f"  disk optimal trial: C = {Cb:.5f} a at beta = {bb:.3f} "
          f"(book 0.6213, exact 2/pi = {2/np.pi:.5f})")
    Ch, bh = hemi_C_var_best()
    print(f"  hemisphere bowl:    C = {Ch:.5f} a at beta = {bh:.3f} "
          f"(book 0.8052, exact 1/2+1/pi = {0.5+1/np.pi:.5f})")
    t, _ = caps_terms(4000)
    print(f"  split-sphere capacitor C_N/a at N=4000: {0.5*np.sum(t):.3f} "
          "(log-divergent series)")
    print("  E center of split sphere (th0=60deg, V=1, a=1):",
          f"{E_center_split(1.0, np.pi/3, 1.0):+.6f}")
    print("  Q0(0.5) =", f"{Q0_legendre(0.5):.6f}",
          " series:", f"{sphereG_series(0.5):.6f}")

