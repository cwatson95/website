"""MACRO_EM-05 -- Multipoles, macroscopic media, dielectrics (Wilcox 2e Ch. 5).

Library backing problems/problems.md (all 49 exercises of Sec. 5.13).
Gaussian units throughout: unit point charge has Phi = 1/r, the dielectric
Green equation is div[eps(x) grad G] = -4 pi delta (Eq. 5.72), D = eps E =
E + 4 pi P (5.64), and bound charge is rho_b = -div P (5.58), sigma_b =
P.n (5.59).

numpy + scipy.special only; no plotting.  Every closed form here is exercised
by code/test_multipole_dielectrics.py.
"""
import numpy as np
from scipy.special import eval_legendre, iv, kv

try:                                    # scipy >= 1.15
    from scipy.special import sph_harm_y

    def _Ylm(m, l, phi, theta):
        return sph_harm_y(l, m, theta, phi)
except ImportError:                     # older scipy
    from scipy.special import sph_harm

    def _Ylm(m, l, phi, theta):
        return sph_harm(m, l, phi, theta)

# ----------------------------------------------------------------------------
# generic helpers
# ----------------------------------------------------------------------------

_GL_CACHE = {}


def gauss_legendre(a, b, n):
    """Nodes/weights of n-point Gauss-Legendre quadrature on [a, b]
    (raw nodes cached per n -- leggauss is O(n^2) and shows up everywhere)."""
    if n not in _GL_CACHE:
        _GL_CACHE[n] = np.polynomial.legendre.leggauss(n)
    x, w = _GL_CACHE[n]
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def grad_fd(f, x, h=1e-5):
    """Central-difference gradient of scalar f at 3-vector x."""
    x = np.asarray(x, float)
    g = np.zeros(3)
    for i in range(3):
        e = np.zeros(3); e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def hess_fd(f, x, h=1e-4):
    """Central-difference Hessian of scalar f at 3-vector x."""
    x = np.asarray(x, float)
    H = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            ei = np.zeros(3); ei[i] = h
            ej = np.zeros(3); ej[j] = h
            H[i, j] = (f(x + ei + ej) - f(x + ei - ej)
                       - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return 0.5 * (H + H.T)


# ----------------------------------------------------------------------------
# Sec. 5.1 -- Cartesian & spherical multipole moments  (P1-P6)
# ----------------------------------------------------------------------------

def moments_point_charges(qs, Xs):
    """(q, p, Qij) of point charges qs at rows of Xs (Eq. 5.12 definitions)."""
    qs = np.asarray(qs, float); Xs = np.atleast_2d(np.asarray(Xs, float))
    q = qs.sum()
    p = (qs[:, None] * Xs).sum(axis=0)
    r2 = (Xs ** 2).sum(axis=1)
    Q = np.einsum('n,ni,nj->ij', qs, Xs, Xs) * 3.0 - np.eye(3) * (qs * r2).sum()
    return q, p, Q


def moments_translate(q, p, Q, R):
    """Moments about a new origin at R (parallel axes) -- Ex. 5.1.2 closed form.

    q' = q;  p' = p - q R;
    Q'_ij = Q_ij - 3(R_i p_j + R_j p_i) + 2 delta_ij R.p + q(3 R_i R_j - R^2 d_ij).
    """
    R = np.asarray(R, float); p = np.asarray(p, float); Q = np.asarray(Q, float)
    qp = p - q * R
    Qp = (Q - 3.0 * (np.outer(R, p) + np.outer(p, R))
          + 2.0 * np.eye(3) * (R @ p)
          + q * (3.0 * np.outer(R, R) - np.eye(3) * (R @ R)))
    return q, qp, Qp


def phi_multipole(x, q, p, Q):
    """Monopole+dipole+quadrupole potential (5.12) at field point x."""
    x = np.asarray(x, float); r = np.linalg.norm(x)
    return q / r + (x @ p) / r ** 3 + 0.5 * (x @ Q @ x) / r ** 5


def phi_exact_charges(x, qs, Xs):
    """Exact potential of the point set at x."""
    x = np.asarray(x, float); Xs = np.atleast_2d(Xs)
    d = np.linalg.norm(x[None, :] - Xs, axis=1)
    return float(np.sum(np.asarray(qs, float) / d))


def E_exact_charges(x, qs, Xs):
    """Exact E of the point set at x."""
    x = np.asarray(x, float); Xs = np.atleast_2d(Xs)
    d = x[None, :] - Xs
    r = np.linalg.norm(d, axis=1)
    return (np.asarray(qs, float)[:, None] * d / r[:, None] ** 3).sum(axis=0)


def cube_moments_Kx(K, L, n=24):
    """(q, p, Q) of rho = K x inside the cube |x|,|y|,|z| < L/2, by quadrature
    (Ex. 5.1.3; analytic: q = 0, p = (K L^5/12) xhat, Q = 0)."""
    xn, wn = gauss_legendre(-L / 2, L / 2, n)
    X, Y, Z = np.meshgrid(xn, xn, xn, indexing='ij')
    W = wn[:, None, None] * wn[None, :, None] * wn[None, None, :]
    rho = K * X
    q = np.sum(rho * W)
    p = np.array([np.sum(rho * X * W), np.sum(rho * Y * W), np.sum(rho * Z * W)])
    r2 = X ** 2 + Y ** 2 + Z ** 2
    co = [X, Y, Z]
    Q = np.array([[np.sum(rho * (3 * co[i] * co[j] - (i == j) * r2) * W)
                   for j in range(3)] for i in range(3)])
    return q, p, Q


def octopole_R(qs, Xs):
    """R_ijk = sum_n q_n [15 x_i x_j x_k - 3 r^2 (x_i d_jk + x_j d_ik + x_k d_ij)]
    (Ex. 5.1.4)."""
    qs = np.asarray(qs, float); Xs = np.atleast_2d(np.asarray(Xs, float))
    r2 = (Xs ** 2).sum(axis=1)
    R = 15.0 * np.einsum('n,ni,nj,nk->ijk', qs, Xs, Xs, Xs)
    d = np.eye(3)
    R -= 3.0 * (np.einsum('n,ni,jk->ijk', qs * r2, Xs, d)
                + np.einsum('n,nj,ik->ijk', qs * r2, Xs, d)
                + np.einsum('n,nk,ij->ijk', qs * r2, Xs, d))
    return R


def phi_octopole_term(x, R):
    """(1/6) sum R_ijk x_i x_j x_k / r^7 -- the next term in (5.12)."""
    x = np.asarray(x, float); r = np.linalg.norm(x)
    return np.einsum('ijk,i,j,k->', R, x, x, x) / (6.0 * r ** 7)


def octopole_independent_count(n_samples=40, seed=1):
    """Dimension of the span of octopole tensors R_ijk from random charge sets
    (should be 7: symmetric rank-3 has 10 components, minus 3 trace conditions)."""
    rng = np.random.default_rng(seed)
    vecs = []
    for _ in range(n_samples):
        qs = rng.normal(size=6); Xs = rng.normal(size=(6, 3))
        vecs.append(octopole_R(qs, Xs).ravel())
    return np.linalg.matrix_rank(np.array(vecs), tol=1e-8)


def linear_quadrupole_phi(x, a):
    """Quadrupole-term potential of +1 at (0,0,+-a), -2 at origin:
    Phi = 2 a^2 P2(cos th)/r^3  (Ex. 5.1.5)."""
    x = np.asarray(x, float); r = np.linalg.norm(x)
    return 2.0 * a * a * eval_legendre(2, x[2] / r) / r ** 3


def dipole_phi(x, p, x0):
    """Point-dipole potential p.(x-x0)/|x-x0|^3."""
    d = np.asarray(x, float) - np.asarray(x0, float)
    return (np.asarray(p) @ d) / np.linalg.norm(d) ** 3


def dipole_above_plane_phi(x, p, d):
    """Ex. 5.1.6(a): dipole p at (0,0,d) above grounded plane z=0; image dipole
    (-px,-py,+pz) at (0,0,-d).  Valid z>0."""
    p = np.asarray(p, float)
    pim = np.array([-p[0], -p[1], p[2]])
    return dipole_phi(x, p, [0, 0, d]) + dipole_phi(x, pim, [0, 0, -d])


def sigma_dipole_plane(rho, pz, d):
    """Ex. 5.1.6(b): induced surface density for p = pz zhat at height d:
    sigma = (pz/2 pi) (2 d^2 - rho^2) / (rho^2 + d^2)^(5/2)."""
    return pz * (2 * d * d - rho ** 2) / (2 * np.pi * (rho ** 2 + d * d) ** 2.5)


def rho_lm(qs, Xs, l, m):
    """Spherical multipole moment (5.19):
    rho_lm = sum q r^l sqrt(4pi/(2l+1)) Y*_lm(theta,phi)."""
    qs = np.asarray(qs, float); Xs = np.atleast_2d(np.asarray(Xs, float))
    r = np.linalg.norm(Xs, axis=1)
    th = np.arccos(np.clip(Xs[:, 2] / np.where(r == 0, 1, r), -1, 1))
    ph = np.arctan2(Xs[:, 1], Xs[:, 0])
    Y = _Ylm(m, l, ph, th)
    return np.sum(qs * r ** l * np.sqrt(4 * np.pi / (2 * l + 1)) * np.conj(Y))


# ----------------------------------------------------------------------------
# Sec. 5.2 -- multipole interaction energies  (P7-P9)
# ----------------------------------------------------------------------------

def quad_energy_in_potential(Q, hessPhi):
    """W_Q = (1/6) sum Q_ij d^2Phi/dx_i dx_j at the quadrupole (from 5.25;
    equals (1/4) Q33 Phi_zz for the cylindrically symmetric case)."""
    return np.einsum('ij,ij->', np.asarray(Q, float), np.asarray(hessPhi, float)) / 6.0


def quad_force_axial(Q33, E_func, x0, h=1e-3):
    """F = (1/4) Q33 d^2 E/dz^2 at x0 for a cylindrically symmetric quadrupole
    (Ex. 5.2.1(a)); E_func(x) -> 3-vector."""
    x0 = np.asarray(x0, float)
    e = np.array([0, 0, h])
    return 0.25 * Q33 * (E_func(x0 + e) - 2 * E_func(x0) + E_func(x0 - e)) / h ** 2


def E_dipole(x, p, x0):
    """Field of point dipole p at x0: [3(p.n)n - p]/s^3."""
    s = np.asarray(x, float) - np.asarray(x0, float)
    r = np.linalg.norm(s); n = s / r
    return (3.0 * (np.asarray(p) @ n) * n - np.asarray(p)) / r ** 3


def quad_dipole_force_x(Q33, p, x1):
    """Ex. 5.2.1(b): force (1-component) on the symmetric quadrupole at the
    origin from dipole p at (x1,0,0):  F1 = -3 Q33 px / x1^5."""
    return -3.0 * Q33 * p[0] / x1 ** 5


def W_quad_quad_perp(Q1, Q2, r):
    """Ex. 5.2.2: both symmetry axes along 3, separation along 1:
    W = +(9/16) Q1 Q2 / r^5.   (Book prints -9/16: sign erratum; the
    microscopic check below settles it.)"""
    return 9.0 * Q1 * Q2 / (16.0 * r ** 5)


def W_quad_quad_axial(Q1, Q2, r):
    """Ex. 5.2.2 Extra: axes and separation all along 3: W = (3/2) Q1 Q2/r^5."""
    return 1.5 * Q1 * Q2 / r ** 5


def linear_quadrupole_charges(a, center=(0, 0, 0), axis=(0, 0, 1)):
    """Microscopic model: +1 at c +- a n, -2 at c;  Q33(about axis) = 4 a^2."""
    c = np.asarray(center, float); n = np.asarray(axis, float)
    n = n / np.linalg.norm(n)
    return np.array([1.0, 1.0, -2.0]), np.array([c + a * n, c - a * n, c])


def W_charges_pair(qs1, X1, qs2, X2):
    """Exact interaction energy between two point sets."""
    W = 0.0
    for qa, xa in zip(qs1, X1):
        for qb, xb in zip(qs2, X2):
            W += qa * qb / np.linalg.norm(np.asarray(xa) - np.asarray(xb))
    return W


def sphere_image_W_sum(q, R, D, L):
    """Ex. 5.2.3: spherical-multipole interaction sum (5.32)/(5.37) between the
    image system of a grounded sphere (radius R) and charge q at D:
    partial sum_l=0..L of q'(R^2/D)^l q/D^(l+1),  q' = -qR/D."""
    qp = -q * R / D
    l = np.arange(L + 1)
    return float(np.sum(qp * (R * R / D) ** l * q / D ** (l + 1)))


def sphere_image_W_closed(q, R, D):
    """Closed form: W = -q^2 (R/D^2) / (1 - R^2/D^2)."""
    return -q * q * R / D ** 2 / (1.0 - (R / D) ** 2)


# ----------------------------------------------------------------------------
# Sec. 5.3 -- forces and torques on multipole distributions  (P10)
# ----------------------------------------------------------------------------

def force_multipole(qs, Xs, E_func, h=1e-3):
    """Multipole force (Ex. 5.3.1(a) form) through quadrupole about origin:
    F = q E(0) + (p.grad)E + (1/6) Q_ij d2E/dxi dxj."""
    q, p, Q = moments_point_charges(qs, Xs)
    E0 = E_func(np.zeros(3))
    F = q * E0
    # (p.grad)E
    for i in range(3):
        e = np.zeros(3); e[i] = h
        F += p[i] * (E_func(e) - E_func(-e)) / (2 * h)
    # (1/6) Q_ij d_i d_j E
    for i in range(3):
        for j in range(3):
            ei = np.zeros(3); ei[i] = h
            ej = np.zeros(3); ej[j] = h
            d2 = (E_func(ei + ej) - E_func(ei - ej)
                  - E_func(-ei + ej) + E_func(-ei - ej)) / (4 * h * h)
            F += Q[i, j] * d2 / 6.0
    return F


def force_exact(qs, Xs, E_func):
    """Exact F = sum q_n E(x_n)."""
    return sum(q * E_func(np.asarray(x, float)) for q, x in zip(qs, Xs))


def torque_multipole(qs, Xs, E_func, h=1e-3):
    """Ex. 5.3.1(b): N = p x E(0) + (1/3) eps_ijk Q_jm dE_k/dx_m|_0."""
    _, p, Q = moments_point_charges(qs, Xs)
    E0 = E_func(np.zeros(3))
    N = np.cross(p, E0)
    dE = np.zeros((3, 3))  # dE[k, m] = dE_k/dx_m
    for m in range(3):
        e = np.zeros(3); e[m] = h
        dE[:, m] = (E_func(e) - E_func(-e)) / (2 * h)
    eps = np.zeros((3, 3, 3))
    eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1
    eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1
    N += np.einsum('ijk,jm,km->i', eps, Q, dE) / 3.0
    return N


def torque_exact(qs, Xs, E_func):
    """Exact N = sum q_n x_n x E(x_n)."""
    return sum(q * np.cross(np.asarray(x, float), E_func(np.asarray(x, float)))
               for q, x in zip(qs, Xs))


# ----------------------------------------------------------------------------
# Sec. 5.4 -- polarization, bound charge, D  (P11-P15)
# ----------------------------------------------------------------------------

def point_charge_E_derivs(P, x0):
    """E of a unit charge at x0 evaluated at rows of P, with first and second
    derivatives (all analytic):
      E_k       = s_k / s^3,            s = x - x0
      dE[.,i,k] = d_i E_k = d_ik/s^3 - 3 s_i s_k/s^5
      d2E[.,i,j,k] = d_i d_j E_k
                 = -3(d_ij s_k + d_ik s_j + d_jk s_i)/s^5 + 15 s_i s_j s_k/s^7."""
    P = np.atleast_2d(np.asarray(P, float))
    s = P - np.asarray(x0, float)[None, :]
    r = np.linalg.norm(s, axis=1)
    E = s / r[:, None] ** 3
    d = np.eye(3)
    dE = (d[None, :, :] / r[:, None, None] ** 3
          - 3 * s[:, :, None] * s[:, None, :] / r[:, None, None] ** 5)
    d2E = (-3.0 * (d[None, :, :, None] * s[:, None, None, :]
                   + d[None, :, None, :] * s[:, None, :, None]
                   + d[None, None, :, :] * s[:, :, None, None])
           / r[:, None, None, None] ** 5
           + 15.0 * s[:, :, None, None] * s[:, None, :, None] * s[:, None, None, :]
           / r[:, None, None, None] ** 7)
    return E, dE, d2E


_T_P11 = np.array([[1.0, 0.3, -0.2], [0.3, -0.5, 0.4], [-0.2, 0.4, 0.7]])


def quad_density_check(Rb, x0, nr=28, nth=28, nph=28):
    """Ex. 5.4.1 check with the smooth anisotropic density
    q_ij(x) = s(x) T_ij,  s = x_1 (1 + r^2/Rb^2),  T a fixed symmetric tensor,
    in the ball r<=Rb; external field from a unit charge at x0 (|x0|>Rb).
    Analytic pieces (g = 1 + r^2/Rb^2 has Hess g = (2/Rb^2) delta):
      d_k s = delta_k1 g + x_1 (2 x_k/Rb^2)
      sum_ij T_ij d_i d_j s = (2/Rb^2)[2 (T x)_1 + x_1 tr T]
      sigma_eff = -(1/6) nhat.(T grad s),   (P_eff)_j = (1/6)(T nhat)_j s.
    Returns (F_direct, F_vol + F_sigma + F_P), equal by Ex. 5.4.1:
      F_direct = int (1/6) q_ij d_i d_j E
      F_vol    = int (1/6)(d_i d_j q_ij) E          [rho_eff^Q]
      F_sigma  = oint sigma_eff E                   [sigma_eff^Q]
      F_P      = oint (P_eff^Q . grad) E.
    """
    T = _T_P11
    rn, rw = gauss_legendre(0.0, Rb, nr)
    cn, cw = gauss_legendre(-1.0, 1.0, nth)
    phn = np.linspace(0, 2 * np.pi, nph, endpoint=False)
    phw = 2 * np.pi / nph
    # volume grid
    Rg, Cg, Pg = np.meshgrid(rn, cn, phn, indexing='ij')
    Wg = (rw[:, None, None] * cw[None, :, None] * phw * Rg ** 2).ravel()
    Sg = np.sqrt(1 - Cg ** 2)
    X = np.stack([(Rg * Sg * np.cos(Pg)).ravel(),
                  (Rg * Sg * np.sin(Pg)).ravel(),
                  (Rg * Cg).ravel()], axis=1)
    r = np.linalg.norm(X, axis=1)
    s = X[:, 0] * (1.0 + (r / Rb) ** 2)
    E, dE, d2E = point_charge_E_derivs(X, x0)
    Td2E = np.einsum('ij,nijk->nk', T, d2E)
    Fdir = np.einsum('n,n,nk->k', Wg, s, Td2E) / 6.0
    Tx1 = X @ T[:, 0]                       # (T x)_1  (T symmetric)
    div2q = (2.0 / Rb ** 2) * (2.0 * Tx1 + X[:, 0] * np.trace(T))
    Fvol = np.einsum('n,n,nk->k', Wg, div2q, E) / 6.0
    # surface grid r = Rb
    Cs, Ps = np.meshgrid(cn, phn, indexing='ij')
    Ws = np.repeat(cw * phw * Rb ** 2, len(phn))
    Ss = np.sqrt(1 - Cs ** 2)
    N = np.stack([(Ss * np.cos(Ps)).ravel(), (Ss * np.sin(Ps)).ravel(),
                  Cs.ravel()], axis=1)
    Xs = Rb * N
    ss = Xs[:, 0] * 2.0                     # s on r=Rb (g(Rb) = 2)
    grads = 2.0 * np.eye(3)[0][None, :] + Xs[:, 0][:, None] * (2.0 * Xs / Rb ** 2)
    Es, dEs, _ = point_charge_E_derivs(Xs, x0)
    sig = -np.einsum('nj,nj->n', N, grads @ T) / 6.0   # -(1/6) n.(T grad s)
    Fsig = np.einsum('n,n,nk->k', Ws, sig, Es)
    Pj = (N @ T) * ss[:, None] / 6.0
    FP = np.einsum('n,nj,njk->k', Ws, Pj, dEs)
    return Fdir, Fvol + Fsig + FP


def bound_from_free(eps, rho_free):
    """Ex. 5.4.2(a): rho_bound = ((1-eps)/eps) rho_free in a linear dielectric."""
    return (1.0 - eps) / eps * rho_free


def sphere_center_charge_sigma_b(eps, q, a):
    """Dielectric sphere with free charge q at center: sigma_b on r=a and its
    total (Ex. 5.4.2(b) instance): sigma_b = (eps-1) q/(4 pi eps a^2),
    total = (eps-1) q/eps."""
    sig = (eps - 1.0) * q / (4 * np.pi * eps * a * a)
    return sig, 4 * np.pi * a * a * sig


def cylinder_in_field_phi(rho, phi, a, eps, E0):
    """Ex. 5.4.3: dielectric cylinder radius a in uniform field E0 yhat.
    Returns Phi(rho, phi) (2-D, y = rho sin phi):
      in : -2 E0 rho sin(phi)/(eps+1)
      out: -E0 rho sin(phi) + E0 (eps-1)/(eps+1) a^2 sin(phi)/rho."""
    rho = np.asarray(rho, float)
    inside = rho < a
    out = -E0 * rho * np.sin(phi) + E0 * (eps - 1) / (eps + 1) * a * a * np.sin(phi) / np.where(rho == 0, 1, rho)
    inn = -2.0 * E0 * rho * np.sin(phi) / (eps + 1)
    return np.where(inside, inn, out)


def polarized_sphere_surface_E(x, P0, a, nth=200, nph=200):
    """Field at interior point x from the bound charge sigma_b = -P0 cos(th)
    on the bubble surface r=a (vacuum bubble in medium polarized P0 zhat):
    quadrature of E = -oint sigma_b (x-x')/|x-x'|^3 ... sign so that
    E = +(4 pi/3) P0 zhat inside (Ex. 5.4.4(b))."""
    cn, cw = gauss_legendre(-1.0, 1.0, nth)
    phn = np.linspace(0, 2 * np.pi, nph, endpoint=False)
    phw = 2 * np.pi / nph
    x = np.asarray(x, float)
    E = np.zeros(3)
    for c, wc in zip(cn, cw):
        s = np.sqrt(1 - c * c)
        zs = a * c
        for ph in phn:
            xs = np.array([a * s * np.cos(ph), a * s * np.sin(ph), zs])
            sig = -P0 * c        # P.n_out-of-material, n = -rhat on bubble wall
            d = x - xs
            E += wc * phw * a * a * sig * d / np.linalg.norm(d) ** 3
    return E


def solid_angle_square_from_center(L):
    """Solid angle of one face of a cube of side L seen from the center = 2 pi/3;
    computed as int over face of z da / r^3 with z = L/2 (Ex. 5.4.5(b))."""
    n = 400
    xn, wn = gauss_legendre(-L / 2, L / 2, n)
    X, Y = np.meshgrid(xn, xn, indexing='ij')
    W = np.outer(wn, wn)
    z = L / 2
    r3 = (X ** 2 + Y ** 2 + z ** 2) ** 1.5
    return float(np.sum(W * z / r3))


def clausius_mossotti_alpha(chi, N):
    """Ex. 5.4.5(c): alpha_mol = (1/N) chi / (1 + 4 pi chi/3)."""
    return chi / (N * (1.0 + 4 * np.pi * chi / 3.0))


def chi_from_alpha(alpha, N):
    """Invert Clausius-Mossotti: chi = N alpha / (1 - 4 pi N alpha / 3)."""
    return N * alpha / (1.0 - 4 * np.pi * N * alpha / 3.0)


# ----------------------------------------------------------------------------
# Sec. 5.6 -- plane-interface Green functions  (P16-P21)
# ----------------------------------------------------------------------------

def corner_dielectric_G(x, xp, eps):
    """Ex. 5.6.1: 4-image Green function for the dielectric corner, evaluated in
    the vacuum quadrant x,y>0:
       G = 1/R + b/Rx + b/Ry + b^2/Rxy,   b = (1-eps)/(1+eps).
    Exact when the media factorize eps(x,y)=e(x)e(y) (quadrants 1,eps,eps^2,eps);
    correct to O(b) for the uniform-eps union region."""
    b = (1.0 - eps) / (1.0 + eps)
    x = np.asarray(x, float); xp = np.asarray(xp, float)
    def d(sx, sy):
        im = np.array([sx * xp[0], sy * xp[1], xp[2]])
        return np.linalg.norm(x - im)
    return 1 / d(1, 1) + b / d(-1, 1) + b / d(1, -1) + b * b / d(-1, -1)


def corner_dielectric_G_region(x, xp, eps):
    """Piecewise 4-image solution in all four quadrants (factorized medium):
      Q1 (x,y>0, eps=1):      1/R + b/Rx + b/Ry + b^2/Rxy
      Q2 (x<0,y>0, eps):      t (1/R + b/Ry)
      Q4 (x>0,y<0, eps):      t (1/R + b/Rx)
      Q3 (x,y<0, eps^2):      t^2 / R
    with b=(1-eps)/(1+eps), t=2/(1+eps)."""
    b = (1.0 - eps) / (1.0 + eps); t = 2.0 / (1.0 + eps)
    x = np.asarray(x, float); xp = np.asarray(xp, float)
    def d(sx, sy):
        im = np.array([sx * xp[0], sy * xp[1], xp[2]])
        return np.linalg.norm(x - im)
    if x[0] >= 0 and x[1] >= 0:
        return 1 / d(1, 1) + b / d(-1, 1) + b / d(1, -1) + b * b / d(-1, -1)
    if x[0] < 0 and x[1] >= 0:
        return t * (1 / d(1, 1) + b / d(1, -1))
    if x[0] >= 0 and x[1] < 0:
        return t * (1 / d(1, 1) + b / d(-1, 1))
    return t * t / d(1, 1)


def _corner_branch(x, xp, eps, region):
    """Evaluate a specific quadrant branch of the 4-image construction at any
    point (used to test interface conditions exactly on the seams).
    region in {1,2,3,4} = quadrant."""
    b = (1.0 - eps) / (1.0 + eps); t = 2.0 / (1.0 + eps)
    x = np.asarray(x, float); xp = np.asarray(xp, float)
    def d(sx, sy):
        im = np.array([sx * xp[0], sy * xp[1], xp[2]])
        return np.linalg.norm(x - im)
    if region == 1:
        return 1 / d(1, 1) + b / d(-1, 1) + b / d(1, -1) + b * b / d(-1, -1)
    if region == 2:
        return t * (1 / d(1, 1) + b / d(1, -1))
    if region == 4:
        return t * (1 / d(1, 1) + b / d(-1, 1))
    return t * t / d(1, 1)


def corner_interface_residuals(eps, xp, factorized=True, n=7):
    """Max residuals of [continuity, D-matching] on the two seams x=0 (y>0:
    Q1|Q2 vacuum-dielectric; y<0: Q4|Q3 internal) for the 4-image ansatz.
    Continuity is evaluated exactly on the seam (branch formulas at x=0);
    D-matching by central differences of each branch.  factorized: medium
    (1, eps, eps^2, eps) -> all residuals vanish; uniform eps in the union
    (eQ3 = eps) -> the internal-seam D-condition fails at O(b)."""
    h = 1e-5
    eQ2 = eps; eQ4 = eps
    eQ3 = eps ** 2 if factorized else eps
    cont = 0.0; dnc = 0.0
    for y in np.linspace(0.3, 2.5, n):
        for z in (0.0, 0.7):
            # Q1|Q2 seam (x=0, y>0): media 1 | eQ2
            x0 = np.array([0.0, y, z])
            Ga = _corner_branch(x0, xp, eps, 1)
            Gb = _corner_branch(x0, xp, eps, 2)
            cont = max(cont, abs(Ga - Gb))
            dGa = (_corner_branch([h, y, z], xp, eps, 1)
                   - _corner_branch([-h, y, z], xp, eps, 1)) / (2 * h)
            dGb = (_corner_branch([h, y, z], xp, eps, 2)
                   - _corner_branch([-h, y, z], xp, eps, 2)) / (2 * h)
            dnc = max(dnc, abs(1.0 * dGa - eQ2 * dGb))
            # Q4|Q3 seam (x=0, y<0): media eQ4 | eQ3
            x0 = np.array([0.0, -y, z])
            Ga = _corner_branch(x0, xp, eps, 4)
            Gb = _corner_branch(x0, xp, eps, 3)
            cont = max(cont, abs(Ga - Gb))
            dGa = (_corner_branch([h, -y, z], xp, eps, 4)
                   - _corner_branch([-h, -y, z], xp, eps, 4)) / (2 * h)
            dGb = (_corner_branch([h, -y, z], xp, eps, 3)
                   - _corner_branch([-h, -y, z], xp, eps, 3)) / (2 * h)
            dnc = max(dnc, abs(eQ4 * dGa - eQ3 * dGb))
    return cont, dnc


def g_slab_conductor_book(z, zp, k, d, eps):
    """Ex. 5.6.2 closed form (conductor z=0, dielectric z>d, unit charge at
    0<zp<d):
      z<d: g = f(z>) sinh(k z<);  z>d: g = K(zp) e^{k(2d-z)}
      f(zs) = (e^{k zs}/k) [1 + c e^{2k(d-zs)}]/[1 + c e^{2kd}],
      K(zp) = (2/(1-eps)) (sinh(k zp)/k)/(1 + c e^{2kd}),  c = (1+eps)/(1-eps)."""
    c = (1.0 + eps) / (1.0 - eps)
    if z <= d:
        zl, zg = min(z, zp), max(z, zp)
        f = np.exp(k * zg) / k * (1 + c * np.exp(2 * k * (d - zg))) / (1 + c * np.exp(2 * k * d))
        return f * np.sinh(k * zl)
    K = (2.0 / (1.0 - eps)) * np.sinh(k * zp) / k / (1 + c * np.exp(2 * k * d))
    return K * np.exp(k * (2 * d - z))


def g_slab_conductor_solve(z, zp, k, d, eps):
    """Same reduced Green function by direct linear solve of the ansatz
      0<z<zp:  A sinh(kz)             (g(0)=0)
      zp<z<d:  B e^{kz} + C e^{-kz}
      z>d:     D e^{-kz}              (decay)
    with continuity at zp, d; jump -[g']_{zp-}^{zp+} = 1; and D_n continuity
    g'(d-) = eps g'(d+)."""
    ekz, emkz = np.exp(k * zp), np.exp(-k * zp)
    ekd, emkd = np.exp(k * d), np.exp(-k * d)
    M = np.zeros((4, 4)); rhs = np.zeros(4)
    # continuity at zp: A sinh(k zp) - B e^{kzp} - C e^{-kzp} = 0
    M[0] = [np.sinh(k * zp), -ekz, -emkz, 0]
    # jump: -(g'(zp+)-g'(zp-)) = 1: -(kB e^{kzp} - kC e^{-kzp}) + kA cosh = 1
    M[1] = [k * np.cosh(k * zp), -k * ekz, k * emkz, 0]; rhs[1] = 1.0
    # continuity at d: B e^{kd} + C e^{-kd} - D e^{-kd} = 0
    M[2] = [0, ekd, emkd, -emkd]
    # D_n: (B k e^{kd} - C k e^{-kd}) = eps (-k D e^{-kd})
    M[3] = [0, k * ekd, -k * emkd, eps * k * emkd]
    A, B, C, D = np.linalg.solve(M, rhs)
    if z <= zp:
        return A * np.sinh(k * z)
    if z <= d:
        return B * np.exp(k * z) + C * np.exp(-k * z)
    return D * np.exp(-k * z)


def g_slab_swapped_solve(z, zp, k, d, eps):
    """Ex. 5.6.3 geometry (Fig. 5.29): dielectric slab attached to the
    conductor (0<z<d), vacuum above, unit charge INSIDE the dielectric at
    0<zp<d.  Direct solve of div[eps grad G] = -4 pi delta:
      0<z<zp:  A sinh(kz)          (eps region, wall at 0)
      zp<z<d:  B e^{kz} + C e^{-kz} (eps region)
      z>d:     D e^{-kz}           (vacuum, decay)
    continuity at zp and d; source jump in the dielectric
    eps[g'(zp-)-g'(zp+)] = 1; D_n at d: eps g'(d-) = g'(d+)."""
    ekz, emkz = np.exp(k * zp), np.exp(-k * zp)
    ekd, emkd = np.exp(k * d), np.exp(-k * d)
    M = np.zeros((4, 4)); rhs = np.zeros(4)
    M[0] = [np.sinh(k * zp), -ekz, -emkz, 0]                      # cont at zp
    M[1] = [eps * k * np.cosh(k * zp), -eps * k * ekz, eps * k * emkz, 0]
    rhs[1] = 1.0                                                  # eps jump
    M[2] = [0, ekd, emkd, -emkd]                                  # cont at d
    M[3] = [0, eps * k * ekd, -eps * k * emkd, k * emkd]          # D_n at d
    A, B, C, D = np.linalg.solve(M, rhs)
    if z <= zp:
        return A * np.sinh(k * z)
    if z <= d:
        return B * np.exp(k * z) + C * np.exp(-k * z)
    return D * np.exp(-k * z)


def oneD_G_dielectric(x, xp, d, L, eps):
    """Ex. 5.6.4: 1-D Dirichlet Green function, walls at 0 and L, dielectric
    slab in 0<x<d, charge at d<xp<L, -(d/dx)[eps(x) dG/dx] = delta(x-xp) with
    the exercise's vacuum-region normalization  -G'' = delta  for x>d.
    Closed form (module-derived):
      x<d:        G = A x,                A = (L-xp)/[L - d(1-1/eps)]
      d<x<xp:     G = A d + eps A (x-d)
      xp<x<L:     G = B (L-x),            B = [d/eps + (xp-d)] / [L - d(1-1/eps)]
    reduces to x<(1-x>/L) when eps=1 or d=0."""
    Delta = L - d * (1.0 - 1.0 / eps)
    A = (L - xp) / Delta / eps
    # continuity of eps G' at x=d: eps*A = C (slope in vacuum region)
    C = eps * A
    B = (d / eps + (xp - d)) / Delta
    x = np.asarray(x, float)
    out = np.where(x <= d, A * x,
                   np.where(x <= xp, A * d + C * (x - d), B * (L - x)))
    return float(out) if out.ndim == 0 else out


def oneD_G_fd(xp, d, L, eps, N=4000):
    """Finite-difference solve of -(d/dx)[eps(x) G'] = delta(x-xp), G(0)=G(L)=0,
    on a uniform grid (flux form, banded solve).  Returns (xgrid, G)."""
    from scipy.linalg import solve_banded
    x = np.linspace(0, L, N + 1)
    hx = x[1] - x[0]
    epsf = np.where((x[:-1] + hx / 2) < d, eps, 1.0)   # eps at cell faces
    main = (epsf[:-1] + epsf[1:]) / hx
    off = -epsf[1:-1] / hx
    ab = np.zeros((3, N - 1))
    ab[0, 1:] = off          # superdiagonal
    ab[1, :] = main
    ab[2, :-1] = off         # subdiagonal
    rhs = np.zeros(N - 1)
    j = int(round(xp / hx))
    rhs[j - 1] = 1.0
    G = np.zeros(N + 1)
    G[1:-1] = solve_banded((1, 1), ab, rhs)
    return x, G


def two_halfspace_phi(x, q, zp, eps1, eps2):
    """Ex. 5.6.5: media eps1 (z<0), eps2 (z>0); free charge q at (0,0,zp>0).
      z>0: Phi = (1/eps2)[q/R1 + q'/R2],  q' = q (eps2-eps1)/(eps2+eps1)
      z<0: Phi = (1/eps1) q''/R1,         q'' = 2 q eps1/(eps2+eps1)."""
    x = np.asarray(x, float)
    R1 = np.linalg.norm(x - np.array([0, 0, zp]))
    R2 = np.linalg.norm(x + np.array([0, 0, zp]))
    qp = q * (eps2 - eps1) / (eps2 + eps1)
    qpp = 2 * q * eps1 / (eps2 + eps1)
    if x[2] >= 0:
        return (q / R1 + qp / R2) / eps2
    return qpp / (eps1 * R1)


def slab_finite_solve(k, zp, d, eps):
    """Ex. 5.6.6: slab occupying -d<z<0, vacuum outside, charge at zp>0.
    Solve the 6-coefficient reduced problem; returns dict of coefficients and
    a callable g(z).  Regions:
      z>zp: A e^{-kz}; 0<z<zp: B e^{kz}+C e^{-kz};
      -d<z<0: D e^{kz}+E e^{-kz}; z<-d: F e^{kz}."""
    M = np.zeros((6, 6)); rhs = np.zeros(6)
    ez, emz = np.exp(k * zp), np.exp(-k * zp)
    ed, emd = np.exp(-k * d), np.exp(k * d)
    # unknown order: A,B,C,D,E,F
    M[0] = [emz, -ez, -emz, 0, 0, 0]                       # cont at zp
    M[1] = [-k * emz, -k * ez, k * emz, 0, 0, 0]; rhs[1] = -1.0  # g'(zp+)-g'(zp-)=-1
    M[2] = [0, 1, 1, -1, -1, 0]                            # cont at 0
    M[3] = [0, k, -k, -eps * k, eps * k, 0]                # D_n at 0 (vac above)
    M[4] = [0, 0, 0, ed, emd, -ed]                         # cont at -d
    M[5] = [0, 0, 0, eps * k * ed, -eps * k * emd, -k * ed]  # D_n at -d
    A, B, C, D, E, F = np.linalg.solve(M, rhs)
    def g(z):
        if z >= zp: return A * np.exp(-k * z)
        if z >= 0:  return B * np.exp(k * z) + C * np.exp(-k * z)
        if z >= -d: return D * np.exp(k * z) + E * np.exp(-k * z)
        return F * np.exp(k * z)
    return dict(A=A, B=B, C=C, D=D, E=E, F=F, g=g)


def g_halfspace_dielectric(z, zp, k, eps):
    """Book Eq. (5.101)-(5.104): dielectric fills z<0, charge at zp>0:
      z>0: (1/2k)[e^{-k|z-zp|} - ((eps-1)/(eps+1)) e^{-k(z+zp)}]
      z<0: (2/(eps+1)) (1/2k) e^{-k(zp-z)}."""
    if z >= 0:
        return (np.exp(-k * abs(z - zp)) - (eps - 1) / (eps + 1) * np.exp(-k * (z + zp))) / (2 * k)
    return (2 / (eps + 1)) * np.exp(-k * (zp - z)) / (2 * k)


# ----------------------------------------------------------------------------
# Sec. 5.7 -- dielectric cylinders and spheres  (P22-P33)
# ----------------------------------------------------------------------------

def gm_cyl2d(m, rho, rhop, a, eps, K=1.0):
    """Ex. 5.7.1 reduced Green function (line source at rhop>a outside a
    dielectric cylinder of radius a):
      m=0: -(1/2) ln(rho>/K)
      m>=1, rho<a:  (1/(m(1+eps))) (rho/rhop)^m
      m>=1, rho>a:  (1/2m)(rho</rho>)^m [1 + ((1-eps)/(1+eps))(a/rho<)^{2m}]."""
    if m == 0:
        return -0.5 * np.log(max(rho, rhop) / K)
    if rho < a:
        return (rho / rhop) ** m / (m * (1 + eps))
    rl, rg = min(rho, rhop), max(rho, rhop)
    b = (1 - eps) / (1 + eps)
    return (rl / rg) ** m * (1 + b * (a / rl) ** (2 * m)) / (2 * m)


def G_cyl2d(rho, phi, rhop, phip, a, eps, M=120, K=1.0):
    """Ex. 5.7.1 sum: G = 4 sum_m cos(m dphi) g_m."""
    G = 4.0 * gm_cyl2d(0, rho, rhop, a, eps, K)
    for m in range(1, M + 1):
        G += 4.0 * np.cos(m * (phi - phip)) * gm_cyl2d(m, rho, rhop, a, eps, K)
    return G


def cyl3d_gm_solve(m, k, rho, rhop, a, eps):
    """Ex. 5.7.2: reduced g_m(rho,rhop;k) for a point charge outside a
    dielectric cylinder, from the modified-Bessel ansatz
      rho<a:        A I_m(k rho)
      a<rho<rhop:   B I_m(k rho) + C K_m(k rho)
      rho>rhop:     D K_m(k rho)
    with continuity at a, rhop; eps g'(a-) = g'(a+); jump
    -[g']_{rhop-}^{rhop+} = 1/rhop (book normalization (2/pi) int dk cos ...)."""
    Ia, Ka = iv(m, k * a), kv(m, k * a)
    dIa = 0.5 * k * (iv(m - 1, k * a) + iv(m + 1, k * a))
    dKa = -0.5 * k * (kv(m - 1, k * a) + kv(m + 1, k * a))
    Ip, Kp = iv(m, k * rhop), kv(m, k * rhop)
    dIp = 0.5 * k * (iv(m - 1, k * rhop) + iv(m + 1, k * rhop))
    dKp = -0.5 * k * (kv(m - 1, k * rhop) + kv(m + 1, k * rhop))
    M4 = np.zeros((4, 4)); rhs = np.zeros(4)
    M4[0] = [Ia, -Ia, -Ka, 0]              # cont at a
    M4[1] = [eps * dIa, -dIa, -dKa, 0]     # D_n at a
    M4[2] = [0, Ip, Kp, -Kp]               # cont at rhop
    M4[3] = [0, dIp, dKp, -dKp]; rhs[3] = 1.0 / rhop  # -[g'] jump
    A, B, C, D = np.linalg.solve(M4, rhs)
    if rho < a:
        g = A * iv(m, k * rho)
    elif rho < rhop:
        g = B * iv(m, k * rho) + C * kv(m, k * rho)
    else:
        g = D * kv(m, k * rho)
    return g, (A, B, C, D)


def _cyl3d_gm_batch(m, kn, rho, rhop, a, eps):
    """g_m(rho, rhop; k) for an array of k values (batched 4x4 solves)."""
    kn = np.asarray(kn, float)
    def dI(mm, xx):
        return 0.5 * (iv(mm - 1, xx) + iv(mm + 1, xx))
    def dK(mm, xx):
        return -0.5 * (kv(mm - 1, xx) + kv(mm + 1, xx))
    Ia, Ka = iv(m, kn * a), kv(m, kn * a)
    dIa, dKa = kn * dI(m, kn * a), kn * dK(m, kn * a)
    Ip, Kp = iv(m, kn * rhop), kv(m, kn * rhop)
    dIp, dKp = kn * dI(m, kn * rhop), kn * dK(m, kn * rhop)
    n = len(kn)
    M4 = np.zeros((n, 4, 4)); rhs = np.zeros((n, 4))
    M4[:, 0] = np.stack([Ia, -Ia, -Ka, np.zeros(n)], axis=1)
    M4[:, 1] = np.stack([eps * dIa, -dIa, -dKa, np.zeros(n)], axis=1)
    M4[:, 2] = np.stack([np.zeros(n), Ip, Kp, -Kp], axis=1)
    M4[:, 3] = np.stack([np.zeros(n), dIp, dKp, -dKp], axis=1)
    rhs[:, 3] = 1.0 / rhop
    sol = np.linalg.solve(M4, rhs[:, :, None])[:, :, 0]
    A, B, C, D = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
    if rho < a:
        return A * iv(m, kn * rho)
    if rho < rhop:
        return B * iv(m, kn * rho) + C * kv(m, kn * rho)
    return D * kv(m, kn * rho)


def G_cyl3d(x, xp, a, eps, M=8, nk=200, kmax=12.0):
    """Assemble Ex. 5.7.2's G = (2/pi) sum_m e^{im dphi} int dk cos(k dz) g_m
    numerically (real cos form, batched over k)."""
    rho = np.hypot(x[0], x[1]); rhop = np.hypot(xp[0], xp[1])
    phi = np.arctan2(x[1], x[0]); phip = np.arctan2(xp[1], xp[0])
    dz = x[2] - xp[2]
    kn, kw = gauss_legendre(1e-6, kmax, nk)
    G = 0.0
    for m in range(0, M + 1):
        gm = _cyl3d_gm_batch(m, kn, rho, rhop, a, eps)
        fac = 1.0 if m == 0 else 2.0
        G += fac * (2 / np.pi) * np.cos(m * (phi - phip)) * np.sum(
            kw * np.cos(kn * dz) * gm)
    return G


def sphere_G_out(r, rp, cosg, a, eps, L=80):
    """Eq. (5.141): r, rp > a:
    G = 1/|x-x'| - sum_{l>=1} (eps-1)l/[l(1+eps)+1] a^{2l+1}/(r rp)^{l+1} P_l."""
    R = np.sqrt(r * r + rp * rp - 2 * r * rp * cosg)
    l = np.arange(1, L + 1)
    Pl = eval_legendre(l, cosg)
    return 1.0 / R - float(np.sum((eps - 1) * l / (l * (1 + eps) + 1)
                                  * a ** (2 * l + 1) / (r * rp) ** (l + 1) * Pl))


def sphere_G_out_induced(r, rp, cosg, a, eps, L=80):
    """Induced part only of (5.141) (regular at r=rp)."""
    l = np.arange(1, L + 1)
    Pl = eval_legendre(l, cosg)
    return -float(np.sum((eps - 1) * l / (l * (1 + eps) + 1)
                         * a ** (2 * l + 1) / (r * rp) ** (l + 1) * Pl))


def sphere_G_in(r, rp, cosg, a, eps, L=80):
    """Eq. (5.140): r<a<rp:
    G = sum_l (2l+1)/[l(1+eps)+1] r^l/rp^{l+1} P_l(cos g)."""
    l = np.arange(0, L + 1)
    Pl = eval_legendre(l, cosg)
    return float(np.sum((2 * l + 1) / (l * (1 + eps) + 1)
                        * r ** l / rp ** (l + 1) * Pl))


def sphere_gl_solve(l, r, rp, a, eps):
    """Direct solve of the radial system (5.121)-(5.131) for rp>a; returns
    g_l(r,rp) with the (5.116) normalization [g_l = rl^l/rg^{l+1}/(2l+1) free]."""
    M4 = np.zeros((4, 4)); rhs = np.zeros(4)
    # unknowns A (r<a), B, C (a<r<rp), D (r>rp)
    M4[0] = [a ** l, -a ** l, -a ** (-l - 1), 0]
    M4[1] = [eps * l * a ** (l - 1), -l * a ** (l - 1), (l + 1) * a ** (-l - 2), 0]
    M4[2] = [0, rp ** l, rp ** (-l - 1), -rp ** (-l - 1)]
    M4[3] = [0, l * rp ** (l - 1), -(l + 1) * rp ** (-l - 2), (l + 1) * rp ** (-l - 2)]
    rhs[3] = 1.0 / rp ** 2   # g'(rp-) - g'(rp+) = 1/rp^2  (i.e. -rp^2[g'] = 1)
    A, B, C, D = np.linalg.solve(M4, rhs)
    if r < a:
        return A * r ** l
    if r < rp:
        return B * r ** l + C * r ** (-l - 1)
    return D * r ** (-l - 1)


def sphere_uniform_field_phi(x, a, eps, E0):
    """Ex. 5.7.3: dielectric sphere in uniform field E0 zhat:
      out: -E0 z + p z/r^3, p = (eps-1)/(eps+2) a^3 E0;  in: -3 E0 z/(eps+2)."""
    x = np.asarray(x, float); r = np.linalg.norm(x)
    if r >= a:
        p = (eps - 1) / (eps + 2) * a ** 3 * E0
        return -E0 * x[2] + p * x[2] / r ** 3
    return -3.0 * E0 * x[2] / (eps + 2)


def sphere_source_inside_coeffs(l, rp, a, eps):
    """Ex. 5.7.4: source at rp<a inside the dielectric sphere.  Returns
    (A, B, C, D) for   r<rp: A r^l;  rp<r<a: B r^l + C r^{-l-1};  r>a: D r^{-l-1}.
    Module-derived closed forms:
      C = rp^l/[eps(2l+1)],
      B = (l+1)(eps-1) rp^l / {eps(2l+1)[l(1+eps)+1] a^{2l+1}},
      A = B + C rp^{-2l-1},   D = rp^l/[l(1+eps)+1]."""
    C = rp ** l / (eps * (2 * l + 1))
    B = (l + 1) * (eps - 1) * rp ** l / (eps * (2 * l + 1) * (l * (1 + eps) + 1) * a ** (2 * l + 1))
    A = B + C * rp ** (-2 * l - 1)
    D = rp ** l / (l * (1 + eps) + 1)
    return A, B, C, D


def sphere_source_inside_solve(l, rp, a, eps):
    """Same coefficients by direct linear solve (validates the closed forms)."""
    M4 = np.zeros((4, 4)); rhs = np.zeros(4)
    M4[0] = [rp ** l, -rp ** l, -rp ** (-l - 1), 0]                       # cont at rp
    M4[1] = [eps * l * rp ** (l - 1), -eps * l * rp ** (l - 1),
             eps * (l + 1) * rp ** (-l - 2), 0]; rhs[1] = 1.0 / rp ** 2   # eps[g'-]-eps[g'+]=1/rp^2
    M4[2] = [0, a ** l, a ** (-l - 1), -a ** (-l - 1)]                    # cont at a
    M4[3] = [0, eps * l * a ** (l - 1), -eps * (l + 1) * a ** (-l - 2),
             (l + 1) * a ** (-l - 2)]                                     # D_n at a
    return tuple(np.linalg.solve(M4, rhs))


def sphere_G_source_inside(r, rp, cosg, a, eps, L=80):
    """Ex. 5.7.4 Green function, source at rp<a (any r)."""
    G = 0.0
    for l in range(L + 1):
        A, B, C, D = sphere_source_inside_coeffs(l, rp, a, eps)
        if r <= rp:
            gl = A * r ** l
        elif r <= a:
            gl = B * r ** l + C * r ** (-l - 1)
        else:
            gl = D * r ** (-l - 1)
        G += (2 * l + 1) * gl * eval_legendre(l, cosg)
    return G


def bubble_G_out(r, rp, cosg, a, eps, L=80):
    """Ex. 5.7.5: vacuum bubble radius a in medium eps, charge at rp>a (in the
    medium), both points outside:
    G = (1/eps)[1/|x-x'| + sum_{l>=1} (eps-1)l/[l(1+eps)+eps] a^{2l+1}/(r rp)^{l+1} P_l]
    (= (1/eps) x sphere solution with eps -> 1/eps)."""
    R = np.sqrt(r * r + rp * rp - 2 * r * rp * cosg)
    G = 1.0 / R
    for l in range(1, L + 1):
        G += ((eps - 1) * l / (l * (1 + eps) + eps)) * a ** (2 * l + 1) \
             / (r * rp) ** (l + 1) * eval_legendre(l, cosg)
    return G / eps


def bubble_gl_solve(l, r, rp, a, eps):
    """Direct radial solve for the bubble (vacuum r<a, eps r>a, source rp>a)."""
    M4 = np.zeros((4, 4)); rhs = np.zeros(4)
    M4[0] = [a ** l, -a ** l, -a ** (-l - 1), 0]
    M4[1] = [l * a ** (l - 1), -eps * l * a ** (l - 1), eps * (l + 1) * a ** (-l - 2), 0]
    M4[2] = [0, rp ** l, rp ** (-l - 1), -rp ** (-l - 1)]
    M4[3] = [0, eps * l * rp ** (l - 1), -eps * (l + 1) * rp ** (-l - 2),
             eps * (l + 1) * rp ** (-l - 2)]
    rhs[3] = 1.0 / rp ** 2   # eps [g'(rp-) - g'(rp+)] = 1/rp^2 (source in medium)
    A, B, C, D = np.linalg.solve(M4, rhs)
    if r < a:
        return A * r ** l
    if r < rp:
        return B * r ** l + C * r ** (-l - 1)
    return D * r ** (-l - 1)


def sphere_dipole_p_eff(p0, xp, a, eps):
    """Ex. 5.7.6(a): distant-observer effective dipole = p0 + induced:
    p_eff = p0 + (eps-1)/(eps+2) a^3 E_dip(0), E_dip(0) = [3(p0.n)n - p0]/rp^3."""
    xp = np.asarray(xp, float); rp = np.linalg.norm(xp); n = xp / rp
    Ed0 = (3 * (np.asarray(p0) @ n) * n - np.asarray(p0)) / rp ** 3
    return np.asarray(p0, float) + (eps - 1) / (eps + 2) * a ** 3 * Ed0


def sphere_dipole_E_in(p0, xp, a, eps):
    """Ex. 5.7.6(b): field inside the sphere for rp >> a:
    E_in = 3/(eps+2) E_dip(0)."""
    xp = np.asarray(xp, float); rp = np.linalg.norm(xp); n = xp / rp
    Ed0 = (3 * (np.asarray(p0) @ n) * n - np.asarray(p0)) / rp ** 3
    return 3.0 / (eps + 2) * Ed0


def sphere_in_conductor_solve(l, r, rp, a, b, eps):
    """Ex. 5.7.7: dielectric sphere radius a inside grounded shell radius b,
    source at a<rp<b.  Regions r<a: A r^l; a<r<rp: B r^l + C r^{-l-1};
    rp<r<b: D r^l + E r^{-l-1} with g(b)=0.  Returns g_l(r)."""
    M5 = np.zeros((5, 5)); rhs = np.zeros(5)
    # unknowns A,B,C,D,E
    M5[0] = [a ** l, -a ** l, -a ** (-l - 1), 0, 0]
    M5[1] = [eps * l * a ** (l - 1), -l * a ** (l - 1), (l + 1) * a ** (-l - 2), 0, 0]
    M5[2] = [0, rp ** l, rp ** (-l - 1), -rp ** l, -rp ** (-l - 1)]
    M5[3] = [0, l * rp ** (l - 1), -(l + 1) * rp ** (-l - 2),
             -l * rp ** (l - 1), (l + 1) * rp ** (-l - 2)]
    rhs[3] = 1.0 / rp ** 2   # g'(rp-) - g'(rp+) = 1/rp^2
    M5[4] = [0, 0, 0, b ** l, b ** (-l - 1)]
    A, B, C, D, E = np.linalg.solve(M5, rhs)
    if r < a:
        return A * r ** l
    if r < rp:
        return B * r ** l + C * r ** (-l - 1)
    return D * r ** l + E * r ** (-l - 1)


def grounded_sphere_interior_gl(l, r, rp, b):
    """Eq. (4.234)-type interior kernel (no dielectric):
    g_l = (1/(2l+1)) [rl^l/rg^{l+1} - (r rp)^l / b^{2l+1}]."""
    rl, rg = min(r, rp), max(r, rp)
    return (rl ** l / rg ** (l + 1) - (r * rp) ** l / b ** (2 * l + 1)) / (2 * l + 1)


def plane_sigma_phi_in(x, a, eps, sigma, d):
    """Ex. 5.7.8: potential inside a dielectric sphere from a uniform plane of
    charge sigma at z=d>a, with the (divergent) l=0 constant dropped:
    Phi_in = 2 pi sigma (3/(eps+2)) z  =>  E = -(3/(eps+2)) 2 pi sigma zhat."""
    return 2 * np.pi * sigma * 3.0 / (eps + 2) * np.asarray(x, float)[2]


def plane_moment_integral(l, d, n=500):
    """int over the plane z'=d of P_l(cos th')/r'^{l+1} da' = 2 pi d^{1-l} I_l,
    I_l = int_0^1 P_l(t) t^{l-2} dt  (t = d/r' substitution -- no radial
    cutoff).  I_1 = 1; I_l = 0 for l>=2 (parity + orthogonality); the l=0
    integral diverges (infinite-plane constant) and is not represented."""
    t, w = gauss_legendre(0.0, 1.0, n)
    return float(2 * np.pi * d ** (1 - l)
                 * np.sum(w * eval_legendre(l, t) * t ** (l - 2)))


def ring_sphere_phi_in(r, th, a, b, eps, Q=1.0, L=60):
    """Ex. 5.7.9: ring (radius b, charge Q, equator plane) around dielectric
    sphere radius a; potential inside:
    Phi = Q sum_n (-1)^n (4n+1)/[2n(1+eps)+1] ((2n-1)!!/(2n)!!) r^{2n}/b^{2n+1} P_2n."""
    tot = 0.0
    for n in range(L + 1):
        l = 2 * n
        # (2n-1)!!/(2n)!!  (= P_2n(0) up to the (-1)^n)
        num = 1.0; den = 1.0
        for k in range(1, n + 1):
            num *= (2 * k - 1); den *= (2 * k)
        dfact = num / den if n > 0 else 1.0
        tot += ((-1) ** n * (4 * n + 1) / (2 * n * (1 + eps) + 1) * dfact
                * r ** l / b ** (l + 1) * eval_legendre(l, np.cos(th)))
    return Q * tot


def ring_sphere_phi_in_points(r, th, a, b, eps, Q=1.0, Npts=240, L=60):
    """Same potential by superposing Npts point charges around the ring, each
    with the one-charge interior kernel (5.140)."""
    x = np.array([r * np.sin(th), 0.0, r * np.cos(th)])
    tot = 0.0
    for j in range(Npts):
        ph = 2 * np.pi * j / Npts
        xp = np.array([b * np.cos(ph), b * np.sin(ph), 0.0])
        cosg = (x @ xp) / (np.linalg.norm(x) * b) if np.linalg.norm(x) > 0 else 0.0
        tot += (Q / Npts) * sphere_G_in(np.linalg.norm(x), b, cosg, a, eps, L)
    return tot


def Il_int_P(l, n=800):
    """I_l = int_0^1 P_l(x) dx (closed: I_0=1, odd l: (-1)^((l-1)/2)(l-2)!!/(l+1)!!,
    even l>=2: 0).  Numeric here; accepts array l."""
    xn, wn = gauss_legendre(0.0, 1.0, n)
    l = np.atleast_1d(l)
    out = np.array([float(np.sum(wn * eval_legendre(li, xn))) for li in l])
    return out if out.size > 1 else float(out[0])


def split_sphere_C(eps, a=1.0, L=60):
    """Ex. 5.7.10: hemispheres at V1, V2; dielectric eps inside r<a.
    Returns (C11, C12):
      C11 = a/4 [1 + sum_{l>=1} (2l+1)((l+1)+eps l) I_l^2]
      C12 = a/4 [1 + sum_{l>=1} (-1)^l (2l+1)((l+1)+eps l) I_l^2].
    (At eps=1 these collapse to Ex. 4.13.4's (2l+1)^2 sums; the eps-dependent
    piece is the book's a(eps-1)/4 sum_l l(2l+1) I_l^2 with alternating sign
    for C12.)"""
    l = np.arange(1, L + 1)
    Il = Il_int_P(l)
    t = (2 * l + 1) * ((l + 1) + eps * l) * Il ** 2
    return a / 4 * (1.0 + np.sum(t)), a / 4 * (1.0 + np.sum((-1.0) ** l * t))


def split_sphere_Q1_quad(eps, V1, V2, a=1.0, L=60, n=300):
    """Free charge on the upper hemisphere by direct quadrature of
    4 pi sigma_f = -d Phi_out/dr + eps d Phi_in/dr at r=a (series potential):
    Q1 = (a/2) int_0^1 dc sum_l V_l [(l+1) + eps l] P_l(c)."""
    cn, cw = gauss_legendre(0.0, 1.0, n)
    ls = np.arange(0, L + 1)
    Ils = Il_int_P(ls)
    Vl = np.where(ls == 0, 0.5 * (V1 + V2),
                  0.5 * (2 * ls + 1) * (V1 + (-1.0) ** ls * V2) * Ils)
    fac = Vl * ((ls + 1) + eps * ls)
    Pl = np.array([eval_legendre(li, cn) for li in ls])   # (L+1, n)
    return float(a / 2 * np.sum(cw * (fac @ Pl)))


def coaxial_cyl_solve(m, rho, rhop, b, a, eps):
    """Ex. 5.7.11(a): grounded conducting cylinder radius a containing a
    dielectric core radius b; unit line charge at b<rhop<a.  2-D reduced modes:
      m>=1:  rho<b: A rho^m; b<rho<rhop: B rho^m + C rho^-m;
             rhop<rho<a: D rho^m + E rho^-m,  G(a)=0
      m=0 :  log ladder.
    Returns g_m(rho) with the P22 normalization (jump rho' [g'] = -1 for m>=1,
    -1/2 for m=0)."""
    if m == 0:
        # regions: rho<b: A;  b<rho<rhop: B + C ln rho;  rhop<rho<a: D + E ln rho
        M5 = np.zeros((5, 5)); rhs = np.zeros(5)
        lb, lp, la = np.log(b), np.log(rhop), np.log(a)
        M5[0] = [1, -1, -lb, 0, 0]                    # cont at b
        M5[1] = [0, 0, 1.0 / b, 0, 0]                 # D_n at b: eps*0 = C/b
        M5[2] = [0, 1, lp, -1, -lp]                   # cont at rhop
        M5[3] = [0, 0, 1.0 / rhop, 0, -1.0 / rhop]
        rhs[3] = 0.5 / rhop                           # g'(-)-g'(+) = 1/(2 rhop)
        M5[4] = [0, 0, 0, 1, la]                      # g(a)=0
        A, B, C, D, E = np.linalg.solve(M5, rhs)
        if rho < b: return A
        if rho < rhop: return B + C * np.log(rho)
        return D + E * np.log(rho)
    M5 = np.zeros((5, 5)); rhs = np.zeros(5)
    M5[0] = [b ** m, -b ** m, -b ** (-m), 0, 0]
    M5[1] = [eps * m * b ** (m - 1), -m * b ** (m - 1), m * b ** (-m - 1), 0, 0]
    M5[2] = [0, rhop ** m, rhop ** (-m), -rhop ** m, -rhop ** (-m)]
    M5[3] = [0, m * rhop ** (m - 1), -m * rhop ** (-m - 1),
             -m * rhop ** (m - 1), m * rhop ** (-m - 1)]
    rhs[3] = 1.0 / rhop      # g'(-)-g'(+) = 1/rhop
    M5[4] = [0, 0, 0, a ** m, a ** (-m)]
    A, B, C, D, E = np.linalg.solve(M5, rhs)
    if rho < b:
        return A * rho ** m
    if rho < rhop:
        return B * rho ** m + C * rho ** (-m)
    return D * rho ** m + E * rho ** (-m)


def G_coaxial(rho, phi, rhop, phip, b, a, eps, M=100):
    """Assemble Ex. 5.7.11's G = 4 sum_m cos(m dphi) g_m."""
    G = 4.0 * coaxial_cyl_solve(0, rho, rhop, b, a, eps)
    for m in range(1, M + 1):
        G += 4.0 * np.cos(m * (phi - phip)) * coaxial_cyl_solve(m, rho, rhop, b, a, eps)
    return G


def G_grounded_cylinder_2d(rho, phi, rhop, phip, a):
    """2-D grounded-cylinder Dirichlet Green function (interior), the eps=1
    anchor: G = -2 ln |x-x'| + 2 ln (rho' |x - a^2/rho'^2 x'| / a)."""
    x = np.array([rho * np.cos(phi), rho * np.sin(phi)])
    xp = np.array([rhop * np.cos(phip), rhop * np.sin(phip)])
    xim = (a ** 2 / (rhop ** 2)) * xp
    return -2 * np.log(np.linalg.norm(x - xp)) + 2 * np.log(
        np.linalg.norm(x - xim) * rhop / a)


def induced_quadrupole_sphere(eps, a, xp):
    """Ex. 5.7.12: quadrupole induced in a dielectric sphere by a unit charge
    at xp (rp>a):  Q_ij = [2 a^5 (eps-1)/(3+2eps)] (-dE'_j(0)/dx'_i),
    dE'_j/dx'_i = (3 x'_i x'_j - r'^2 d_ij)/r'^5.
    (Book prints a^3: dimensional erratum -- a^5 verified numerically.)"""
    xp = np.asarray(xp, float); rp = np.linalg.norm(xp)
    T = (3 * np.outer(xp, xp) - rp ** 2 * np.eye(3)) / rp ** 5
    return 2 * a ** 5 * (eps - 1) / (3 + 2 * eps) * (-T)


def sphere_sigma_b_series(th, rp, a, eps, L=80):
    """Bound surface charge on the dielectric sphere (source outside on +z):
    sigma_b = (1/4pi)(E_r(a+) - E_r(a-)) from the (5.140)/(5.141) series."""
    dr = 1e-6 * a
    cg = np.cos(th)
    Eout = -(sphere_G_out(a + 2 * dr, rp, cg, a, eps) - sphere_G_out(a, rp, cg, a, eps)) / (2 * dr)
    Ein = -(sphere_G_in(a, rp, cg, a, eps) - sphere_G_in(a - 2 * dr, rp, cg, a, eps)) / (2 * dr)
    return (Eout - Ein) / (4 * np.pi)


def induced_quadrupole_from_sigma(rp, a, eps, L=80, n=400):
    """Q_33 = int (3 z^2 - r^2) sigma_b da over the sphere (z-axis toward the
    charge) -- the numeric cross-check of Ex. 5.7.12."""
    cn, cw = gauss_legendre(-1.0, 1.0, n)
    Q33 = 0.0
    for c, w in zip(cn, cw):
        sig = sphere_sigma_b_series(np.arccos(c), rp, a, eps, L)
        Q33 += w * 2 * np.pi * a * a * sig * (3 * (a * c) ** 2 - a * a)
    return Q33


# ----------------------------------------------------------------------------
# Sec. 5.8 -- field energy with dielectrics  (P34)
# ----------------------------------------------------------------------------

def polarized_sphere_ED_integral(P0=1.0, a=1.0, nr=200):
    """Ex. 5.8.1(a) instance: uniformly polarized sphere (P = P0 zhat):
    int E.D over all space (analytic pieces integrated radially/angularly):
      inside: E = -(4pi/3) P0 zhat, D = (8pi/3) P0 zhat -> -(32 pi^2/9) P0^2 V
      outside: E = D = dipole field of p = (4pi/3) a^3 P0."""
    V = 4 * np.pi * a ** 3 / 3
    inside = -(4 * np.pi / 3) * (8 * np.pi / 3) * P0 ** 2 * V
    p = (4 * np.pi / 3) * a ** 3 * P0
    # int_{r>a} |E_dip|^2 = p^2 * 8pi/(3 a^3)
    rn, rw = gauss_legendre(a, 60.0 * a, nr)
    radial = np.sum(rw / rn ** 4)          # int r^2 dr / r^6
    ang = 8 * np.pi                         # int dOmega (3cos^2+1) = 8pi
    outside = p * p * ang * radial
    outside_exact = p * p * 8 * np.pi / (3 * a ** 3)
    return inside + outside, inside + outside_exact


def polarized_sphere_Wint(P0=1.0, a=1.0):
    """W_int = -(1/2) int P.E  and  (1/8pi) int E^2, both closed forms for the
    uniformly polarized sphere; Ex. 5.8.1(b) says they're equal."""
    V = 4 * np.pi * a ** 3 / 3
    W_PE = -0.5 * P0 * (-(4 * np.pi / 3) * P0) * V          # -(1/2) int P.E (inside only)
    p = (4 * np.pi / 3) * a ** 3 * P0
    E2 = (4 * np.pi / 3 * P0) ** 2 * V + p * p * 8 * np.pi / (3 * a ** 3)
    return W_PE, E2 / (8 * np.pi)


# ----------------------------------------------------------------------------
# Sec. 5.9 -- forces on dielectrics  (P35-P44)
# ----------------------------------------------------------------------------

def halfspace_fields_at_interface(rho, zp, eps):
    """For the P20 image solution (medium eps at z<0, vacuum above, unit charge
    at zp>0), return (E1n, E2n, sigma_b) at transverse radius rho on z=0, with
    n = +zhat (out of the dielectric).  Phi_2 = 1/R1 + q'/R2 (vacuum side,
    q' = (1-eps)/(1+eps)); Phi_1 = (2/(1+eps))/R1 (dielectric side).
    E_z = -dPhi/dz:  E2n = (1-q') zp/R^3 evaluated with signs below."""
    qp = (1 - eps) / (1 + eps)
    R = np.sqrt(rho ** 2 + zp ** 2)
    # Phi_2 = 1/R1 + q'/R2, R1^2 = rho^2+(z-zp)^2, R2^2 = rho^2+(z+zp)^2:
    # E_z(0+) = -d/dz = [ (z-zp)/R1^3 + q'(z+zp)/R2^3 ]_{z=0} = (q'-1) zp/R^3
    E2n = (qp - 1.0) * zp / R ** 3
    # Phi_1 = (2/(1+eps))/R1: E_z(0-) = (2/(1+eps)) (z-zp)/R1^3|_0 = -(2/(1+eps)) zp/R^3
    E1n = -(2.0 / (1 + eps)) * zp / R ** 3
    sigma_b = (E2n - E1n) / (4 * np.pi)
    return E1n, E2n, sigma_b


def surface_force_from_fields(E1n, E2n):
    """Ex. 5.9.1(a): F.n per area = (E2n^2 - E1n^2)/(8 pi)."""
    return (E2n ** 2 - E1n ** 2) / (8 * np.pi)


def surface_force_from_sigma_b(sigma_b, eps):
    """Ex. 5.9.1(b): F.n per area = 2 pi sigma_b^2 (1+eps)/(eps-1)."""
    return 2 * np.pi * sigma_b ** 2 * (1 + eps) / (eps - 1)


def surface_force_free_bound(sigma_b, sigma_f, eps):
    """Ex. 5.9.1 Extra: F.n = 2 pi [ (sigma_b eps/(eps-1) + sigma_f)^2
                                     - sigma_b^2/(1-eps)^2 ]."""
    return 2 * np.pi * ((sigma_b * eps / (eps - 1) + sigma_f) ** 2
                        - sigma_b ** 2 / (1 - eps) ** 2)


def halfspace_force_image(zp, eps):
    """Ex. 5.9.2(a): force on the dielectric half-space from unit charge at zp:
    attraction of magnitude (eps-1)/(eps+1)/(4 zp^2) (directed toward charge)."""
    return (eps - 1) / (eps + 1) / (4 * zp ** 2)


def halfspace_deltaW(zp, eps):
    """Ex. 5.9.2(b): Delta W = (1/2)[G-G0]|coincident = -(eps-1)/(eps+1)/(4 zp)."""
    return -(eps - 1) / (eps + 1) / (4 * zp)


def halfspace_force_stress(zp, eps, n=1200):
    """Ex. 5.9.2(c): integrate 2 pi sigma_b^2 (1+eps)/(eps-1) over the interface
    (vectorized; the integrand falls as rho^-5 so the cutoff tail is tiny)."""
    rn, rw = gauss_legendre(0.0, 200.0 * zp, n)
    _, _, sb = halfspace_fields_at_interface(rn, zp, eps)
    return float(np.sum(rw * 2 * np.pi * rn * surface_force_from_sigma_b(sb, eps)))


def rod_force_perp(eps, a, Lrod, z):
    """Ex. 5.9.3: rod perpendicular to the line to the unit charge (transverse
    field): |F| = (eps-1)/(eps+1) a^2 L / z^5, attractive.  Signed (z-comp,
    charge at +z from rod): F_rod->charge attraction => on rod +z:"""
    return (eps - 1) / (eps + 1) * a * a * Lrod / z ** 5


def rod_force_par(eps, a, Lrod, z):
    """Ex. 5.9.4: rod pointing at the charge (longitudinal field, needle limit
    E_in = E0): |F| = (eps-1) a^2 L / (2 z^5), attractive."""
    return (eps - 1) * a * a * Lrod / (2 * z ** 5)


def rod_W_perp(eps, a, Lrod, z):
    """Energy route: W = -(1/2) int P.E0 with P = (eps-1)/(2pi(eps+1)) E0:
    W = -(eps-1) a^2 L/(4(eps+1) z^4)."""
    return -(eps - 1) * a * a * Lrod / (4 * (eps + 1) * z ** 4)


def rod_W_par(eps, a, Lrod, z):
    """W = -(1/2)(eps-1)/(4pi) E0^2 V = -(eps-1) a^2 L/(8 z^4)."""
    return -(eps - 1) * a * a * Lrod / (8 * z ** 4)


def prolate_depolarization_nz(aspect):
    """Depolarization factor along the long axis of a prolate spheroid with
    aspect ratio c/a = aspect > 1:  n_z = ((1-e^2)/e^3)(atanh(e) - e),
    e = sqrt(1-1/aspect^2).  n_z -> 0 as aspect -> inf (P38's needle limit)."""
    e = np.sqrt(1.0 - 1.0 / aspect ** 2)
    return (1 - e * e) / e ** 3 * (np.arctanh(e) - e)


def spheroid_E_in_axial(eps, aspect, E0):
    """E inside a prolate spheroid in an axial uniform field:
    E_in = E0 / (1 + n_z (eps-1)) with the Gaussian-rationalized n_z in [0,1/3]."""
    nz = prolate_depolarization_nz(aspect)
    return E0 / (1.0 + nz * (eps - 1.0))


def capacitor_C_partial(x, eps, Lc, Wc, D):
    """Ex. 5.9.5: C(x) = (W/(4 pi D)) [eps x + (L - x)] (parallel slabs)."""
    return Wc * (eps * x + (Lc - x)) / (4 * np.pi * D)


def capacitor_force_fixed_V(x, eps, Lc, Wc, D, V):
    """(a): F_x = +dW/dx|_V = (V^2/2) dC/dx = V^2 W (eps-1)/(8 pi D) > 0."""
    return V * V * Wc * (eps - 1) / (8 * np.pi * D)


def capacitor_force_fixed_Q(x, eps, Lc, Wc, D, V):
    """(b): charge fixed at Q = L W V/(4 pi D); F = (Q^2/2C^2) dC/dx
    = (eps-1) W V^2 L^2 / [8 pi D (L + (eps-1)x)^2]."""
    return (eps - 1) * Wc * V * V * Lc ** 2 / (8 * np.pi * D * (Lc + (eps - 1) * x) ** 2)


def slab_deltaW(zp, d, eps, nk=1200, kmax=None):
    """Delta W(zp, d) = int_0^inf k dk [g - g0](zp,zp;k) for the Ex. 5.6.2
    system (g0 = conductor-only half-space)."""
    if kmax is None:
        kmax = 80.0 / d
    kn, kw = gauss_legendre(1e-9, kmax, nk)
    tot = 0.0
    for k, w in zip(kn, kw):
        g = g_slab_conductor_book(zp, zp, k, d, eps)
        g0 = np.sinh(k * zp) * np.exp(-k * zp) / k
        tot += w * k * (g - g0)
    return tot


def slab_force_integral(zp, d, eps, nk=1200, kmax=None):
    """Ex. 5.9.6: F_z on the dielectric =
    4 ((1+eps)/(1-eps)) int_0^inf dk k e^{2kd} sinh^2(k zp) / [1 + c e^{2kd}]^2,
    c = (1+eps)/(1-eps)."""
    c = (1 + eps) / (1 - eps)
    if kmax is None:
        kmax = 80.0 / d
    kn, kw = gauss_legendre(1e-9, kmax, nk)
    integ = kn * np.exp(2 * kn * d) * np.sinh(kn * zp) ** 2 / (1 + c * np.exp(2 * kn * d)) ** 2
    return 4 * c * float(np.sum(kw * integ))


def slab_force_weak(zp, d, eps):
    """Ex. 5.9.7: weak-dielectric force on the dielectric:
    F = (1/4)((1-eps)/(1+eps)) [1/(d+zp)^2 + 1/(d-zp)^2 - 2/d^2]."""
    b = (1 - eps) / (1 + eps)
    return 0.25 * b * (1 / (d + zp) ** 2 + 1 / (d - zp) ** 2 - 2 / d ** 2)


def plate_sigma_kspace(rho, zp, d, nk=1200, kmax=None):
    """Ex. 5.9.8(a): sigma(rho) on the z=d conductor (two-plate system):
    sigma = -(1/2pi) int_0^inf dk k [sinh(k zp)/sinh(k d)] J0(k rho)."""
    from scipy.special import j0
    if kmax is None:
        kmax = 120.0 / d
    kn, kw = gauss_legendre(1e-9, kmax, nk)
    return -np.sum(kw * kn * np.sinh(kn * zp) / np.sinh(kn * d) * j0(kn * rho)) / (2 * np.pi)


def plate_force_kspace(zp, d, nk=1200, kmax=None):
    """Ex. 5.9.8(b): F_z = -int_0^inf dk k [sinh(k zp)/sinh(k d)]^2."""
    if kmax is None:
        kmax = 120.0 / d
    kn, kw = gauss_legendre(1e-9, kmax, nk)
    return -float(np.sum(kw * kn * (np.sinh(kn * zp) / np.sinh(kn * d)) ** 2))


def two_plate_Wind(zp, d, N=20000):
    """Interaction energy U(zp,d) = (1/2) Phi_ind(zp) of a unit charge between
    grounded plates z=0, z=d, from the image ladder (+1 at 2nd+zp, -1 at
    2nd-zp), grouped for absolute convergence:
    Phi_ind = -1/(2 zp) + sum_{n>=1} [1/(nd) - 1/(2nd-2zp)... ] assembled
    pairwise below."""
    n = np.arange(1, N + 1)
    tot = -1.0 / (2 * zp)                                   # n=0 image (-1 at -zp)
    tot += np.sum(1.0 / (2 * n * d) - 1.0 / (2 * n * d - 2 * zp))
    tot += np.sum(1.0 / (2 * n * d) - 1.0 / (2 * n * d + 2 * zp))
    return 0.5 * tot


def plate_force_images(zp, d, N=20000):
    """Force on the z=d plate = -dU/dd at fixed charge (grounded conductors,
    no battery work): finite difference of the image-ladder energy."""
    h = 1e-6 * d
    return -(two_plate_Wind(zp, d + h, N) - two_plate_Wind(zp, d - h, N)) / (2 * h)


def plate_sigma_images(rho, zp, d, N=400):
    """sigma(rho) on the z=d plate from the full image ladder (+1 at 2nd+zp,
    -1 at 2nd-zp): sigma = (1/4pi) E.n with n = -zhat out of the conductor:
    sigma = -(1/4pi) sum_i q_i (d - z_i)/(rho^2 + (d-z_i)^2)^{3/2}."""
    n = np.arange(-N, N + 1)
    zp_ = 2 * n * d + zp
    zm_ = 2 * n * d - zp
    tot = (np.sum((d - zp_) / (rho ** 2 + (d - zp_) ** 2) ** 1.5)
           - np.sum((d - zm_) / (rho ** 2 + (d - zm_) ** 2) ** 1.5))
    return -tot / (4 * np.pi)


def layered_capacitor_force_V(x, d, eps, dV):
    """Ex. 5.9.9(a): battery connected: F/A = -(1/8pi) dV^2/[d/eps + (x-d)]^2."""
    return -dV ** 2 / (8 * np.pi * (d / eps + (x - d)) ** 2)


def layered_capacitor_force_Q(x, d, eps, dV, L):
    """Ex. 5.9.9(b): battery disconnected at plate distance L:
    F/A = -2 pi sigma^2 = -(1/8pi) dV^2/[d/eps + (L-d)]^2 (x-independent)."""
    return -dV ** 2 / (8 * np.pi * (d / eps + (L - d)) ** 2)


def line_cylinder_deltaW(rho0, a, eps, M=400):
    """Ex. 5.9.10: Delta W(rho0) = beta sum_m (1/m)(a/rho0)^{2m}
    = -beta ln(1 - a^2/rho0^2),  beta = (1-eps)/(1+eps).  Returns (series, closed)."""
    b = (1 - eps) / (1 + eps)
    x = (a / rho0) ** 2
    series = b * sum(x ** m / m for m in range(1, M + 1))
    closed = -b * np.log(1 - x)
    return series, closed


def line_cylinder_force(rho0, a, eps):
    """F = -d DeltaW/d rho0 = ((1-eps)/(1+eps)) 2 a^2/[rho0 (rho0^2-a^2)]
    (negative = attraction toward the cylinder for eps>1)."""
    b = (1 - eps) / (1 + eps)
    return b * 2 * a * a / (rho0 * (rho0 ** 2 - a ** 2))


# ----------------------------------------------------------------------------
# Sec. 5.10 -- leading-logarithm model  (P45)
# ----------------------------------------------------------------------------

def leading_log_energy_density(E, K2=1.0, alpha=1.0):
    """w = (1/4pi)[(1/2) E.D + alpha E^2], D = 2 alpha ln(E^2/K^2) E."""
    E = np.asarray(E, float)
    E2 = E @ E
    D = 2 * alpha * np.log(E2 / K2) * E
    return (0.5 * (E @ D) + alpha * E2) / (4 * np.pi)


def leading_log_perfect_differential_check(E, dE, K2=1.0, alpha=1.0, h=1e-6):
    """Verify d[(1/2)E.D + alpha E^2] = E.dD along direction dE (Eq. 5.193):
    returns (lhs, rhs) finite-difference vs analytic."""
    E = np.asarray(E, float); dE = np.asarray(dE, float)
    def u(Ev):
        E2 = Ev @ Ev
        D = 2 * alpha * np.log(E2 / K2) * Ev
        return 0.5 * (Ev @ D) + alpha * E2
    lhs = (u(E + h * dE) - u(E - h * dE)) / (2 * h)
    E2 = E @ E
    D = 2 * alpha * np.log(E2 / K2) * E
    dD = 2 * alpha * np.log(E2 / K2) * dE + 4 * alpha * (E @ dE) / E2 * E
    rhs = E @ dD
    return lhs, rhs


def leading_log_d2W_integrand(E, dE, K2=1.0, alpha=1.0):
    """Second-variation integrand (module-derived):
    (1/4pi)[ (ln(E^2/K^2) + 2) 2 alpha? ] -- we use the exact expansion:
    delta2 w = (alpha/4pi)[(ln(E2/K2)+2)|dE|^2 + 2 (E.dE)^2/E2], positive for
    E^2 > K^2."""
    E = np.asarray(E, float); dE = np.asarray(dE, float)
    E2 = E @ E
    return (alpha / (4 * np.pi)) * ((np.log(E2 / K2) + 2) * (dE @ dE)
                                    + 2 * (E @ dE) ** 2 / E2)


# ----------------------------------------------------------------------------
# Sec. 5.11 -- force examples  (P46-P49)
# ----------------------------------------------------------------------------

def sphere_charge_deltaW_series(r0, a, eps, L=200):
    """Eq. (5.201): Delta W = -((eps-1)/(2 r0)) sum_l l/(l(1+eps)+1) (a/r0)^{2l+1}."""
    l = np.arange(1, L + 1)
    return -(eps - 1) / (2 * r0) * np.sum(l / (l * (1 + eps) + 1) * (a / r0) ** (2 * l + 1))


def sphere_charge_force_far(r0, a, eps):
    """Eq. (5.202): F_r = -(eps-1)/(eps+2) 2 a^3/r0^5 (attractive for eps>1)."""
    return -(eps - 1) / (eps + 2) * 2 * a ** 3 / r0 ** 5


def bubble_charge_deltaW_series(r0, a, eps, L=150):
    """Ex. 5.11.1: Delta W for the bubble =
    (1/(2 eps)) sum_l (eps-1) l/[l(1+eps)+eps] a^{2l+1}/r0^{2l+2}
    (computed with (a/r0)^{2l} ratios to avoid overflow)."""
    l = np.arange(1, L + 1)
    return (eps - 1) / (2 * eps) * (a / r0 ** 2) * np.sum(
        l / (l * (1 + eps) + eps) * (a / r0) ** (2 * l))


def bubble_charge_force_far(r0, a, eps):
    """Leading force on the charge: F_r = +2(eps-1) a^3/[eps(1+2eps) r0^5]
    (repulsive for eps>1)."""
    return 2 * (eps - 1) * a ** 3 / (eps * (1 + 2 * eps) * r0 ** 5)


def sphere_deltaW_from_P(r0, a, eps):
    """Ex. 5.11.2: W - W0 = -(1/2) int_V P.E0 with P = ((eps-1)/4pi)(3/(eps+2))E0:
    = -((eps-1)/(eps+2)) a^3/(2 r0^4)."""
    return -(eps - 1) / (eps + 2) * a ** 3 / (2 * r0 ** 4)


def droplet_inside_force_series(r0, a, eps, L=200):
    """Ex. 5.11.3: unit charge at r0 inside a dielectric droplet radius a:
    F_r = -((eps-1)/eps) sum_l l(l+1)/[l(1+eps)+1] r0^{2l-1}/a^{2l+1}."""
    l = np.arange(1, L + 1)
    return -(eps - 1) / eps * np.sum(
        l * (l + 1) / (l * (1 + eps) + 1) * r0 ** (2 * l - 1) / a ** (2 * l + 1))


def droplet_deltaW(r0, a, eps, L=400):
    """Delta W = ((eps-1)/(2 eps)) sum_l (l+1)/[l(1+eps)+1] r0^{2l}/a^{2l+1}
    (reference: charge in unbounded eps)."""
    l = np.arange(0, L + 1)
    return (eps - 1) / (2 * eps) * np.sum(
        (l + 1) / (l * (1 + eps) + 1) * r0 ** (2 * l) / a ** (2 * l + 1))


def sphere_dipole_W(xd, p, a, eps):
    """Ex. 5.11.4 energy: W(xd) = -(alpha/2)|E_p(sphere center)|^2,
    alpha = ((eps-1)/(eps+2)) a^3, E_p(0) = [3(p.n)n - p]/r^3, n = -xd/r ...
    |E_p(0)|^2 = (3(p.xhat)^2 + p^2)/r^6."""
    xd = np.asarray(xd, float); p = np.asarray(p, float)
    r = np.linalg.norm(xd); n = xd / r
    alpha = (eps - 1) / (eps + 2) * a ** 3
    return -0.5 * alpha * (3 * (p @ n) ** 2 + p @ p) / r ** 6


def sphere_dipole_force(d, p, a, eps):
    """Closed form (dipole at (0,0,d)):
    F_i = 3 alpha p3 p_i/d^7 (i=1,2);  F_3 = -3 alpha (3 p3^2 + p^2)/d^7."""
    p = np.asarray(p, float)
    alpha = (eps - 1) / (eps + 2) * a ** 3
    F = np.empty(3)
    F[0] = 3 * alpha * p[2] * p[0] / d ** 7
    F[1] = 3 * alpha * p[2] * p[1] / d ** 7
    F[2] = -3 * alpha * (3 * p[2] ** 2 + p @ p) / d ** 7
    return F


def sphere_dipole_W_exact(xd, p, a, eps, delta=1e-3, L=120):
    """'Exact' interaction energy of a physical dipole (two charges +-q at
    xd +- delta/2 phat, q = |p|/delta) with the dielectric sphere, from the
    (5.141) induced kernel: W = (1/2) sum_ij q_i q_j G_ind(x_i, x_j)."""
    p = np.asarray(p, float); xd = np.asarray(xd, float)
    pm = np.linalg.norm(p); ph = p / pm
    q = pm / delta
    pts = [xd + 0.5 * delta * ph, xd - 0.5 * delta * ph]
    qs = [q, -q]
    W = 0.0
    for i in range(2):
        for j in range(2):
            xi, xj = pts[i], pts[j]
            ri, rj = np.linalg.norm(xi), np.linalg.norm(xj)
            cg = (xi @ xj) / (ri * rj)
            W += 0.5 * qs[i] * qs[j] * sphere_G_out_induced(ri, rj, cg, a, eps, L)
    return W


if __name__ == '__main__':
    print("MACRO_EM-05 demo (Gaussian units)")
    qs, Xs = linear_quadrupole_charges(0.05)
    q, p, Q = moments_point_charges(qs, Xs)
    print(f"  linear quadrupole a=0.05: Q33 = {Q[2,2]:.6f} (= 4a^2 = {4*0.05**2})")
    qs2, X2 = linear_quadrupole_charges(0.05, center=(1.0, 0, 0))
    print(f"  W_QQ(perp) micro = {W_charges_pair(qs, Xs, qs2, X2):+.6e}"
          f"   formula +9/16 Q1Q2/r^5 = {W_quad_quad_perp(Q[2,2], Q[2,2], 1.0):+.6e}")
    print(f"  sphere-charge far force (eps=3,a=1,r0=4): {sphere_charge_force_far(4.,1.,3.):+.6e}")
    s, c = line_cylinder_deltaW(1.7, 1.0, 2.5)
    print(f"  line-cylinder DeltaW series {s:.8f} vs closed {c:.8f}")
    print(f"  droplet force (eps=2, r0=0.3, a=1): {droplet_inside_force_series(0.3,1.,2.):+.6f}")
