#!/usr/bin/env python3
"""derive.py -- the Python twin of docs/phets_revised/molecule-shapes.html and
molecule-shapes-basics.html.  Writes refvals.json (read by gen_ref.py into the
selfTest's REF table) and prints refvals.txt.  Read the printed output IN FULL.

THE MODEL (the thing the sims implement)
  Electron domains around a central atom: bonds on the unit sphere, lone pairs
  on a sphere of radius rho (PhET puts its lone pairs at LONE_PAIR_DISTANCE 7
  against BONDED_PAIR_DISTANCE 10, so rho_PhET = 0.7).  Every pair repels with
  energy 1/d^2, d = |R_i u_i - R_j u_j| (3-D distance).  The shape is the
  arrangement of least energy.  Single, double and triple bonds act alike
  (PhET: "currently the single/double/triple bonds act identically").

WHAT THIS FILE CHECKS, INDEPENDENTLY OF THE JS
  A. the ideal geometries exactly (angles, closed-form energies of N equal
     domains);
  B. the relaxation: the JS's projected gradient descent twinned here, and
     checked against scipy BFGS on an unconstrained parametrisation;
  C. random starts (mulberry32, the JS's PRNG) converge to the exact ideal
     geometries for N = 2..6 equal domains;
  D. every AXE class at rho = 0.70, 0.85, 1.00: angles and energies;
  E. the AUDIT that justifies the model: for every class and every rho on a
     grid, the VSEPR arrangement is the global minimum over every slot
     assignment and random starts, keeps its shape, and is a true local
     minimum (Hessian); and the same audit for Coulomb 1/d and for charge
     weights, which fail;
  F. PhET's real-molecule table (verbatim primary numbers) -> bond angles,
     lone-pair placement by a Horn fit, model-vs-measured directions;
  G. Horn's quaternion fit against scipy's Rotation.align_vectors;
  H. the AXE naming table (PhET's getConfiguration rules);
  I. the squeeze curves (angle against rho) and the rho each measured angle
     would need.
"""
import io, itertools, json, math, os, sys
import numpy as np
from scipy.optimize import minimize, brentq
from scipy.spatial.transform import Rotation

here = os.path.dirname(os.path.abspath(__file__))
OUT = {}
LINES = []


def put(path, val):
    d = OUT
    for k in path[:-1]:
        d = d.setdefault(k, {})
    d[path[-1]] = val


def say(s=''):
    LINES.append(s)
    print(s)


D2R = math.pi / 180.0
EXP = 2.0                      # the model's pair energy 1/d^EXP
RHO_PHET = 7.0 / 10.0          # PhET's LONE_PAIR_DISTANCE / BONDED_PAIR_DISTANCE
ETA = 0.1                      # the JS's gradient step
TOL = 1e-13                    # converged when every tangential gradient < TOL
ITMAX = 200000
SQ3 = math.sqrt(3.0)

# ---------------------------------------------------------------- A. slots
# the ideal electron geometries, principal axis along z; LONE PAIRS FILL THE
# FIRST SLOTS (the VSEPR rule PhET's model notes state: the higher-repulsion
# slots first -- equatorial in the bipyramid, trans in the octahedron)
T8 = math.sqrt(8.0 / 9.0)
SLOTS = {
    1: [(0.0, 0.0, 1.0)],
    2: [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0)],
    3: [(0.0, 0.0, 1.0), (SQ3 / 2, 0.0, -0.5), (-SQ3 / 2, 0.0, -0.5)],
    4: [(0.0, 0.0, 1.0), (T8, 0.0, -1.0 / 3.0), (-T8 / 2, T8 * SQ3 / 2, -1.0 / 3.0), (-T8 / 2, -T8 * SQ3 / 2, -1.0 / 3.0)],
    5: [(1.0, 0.0, 0.0), (-0.5, SQ3 / 2, 0.0), (-0.5, -SQ3 / 2, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, -1.0)],
    6: [(0.0, 0.0, 1.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, -1.0, 0.0)],
}
TET = math.degrees(math.acos(-1.0 / 3.0))
IDEAL_ANGLES = {2: [180.0], 3: [120.0] * 3, 4: [TET] * 6, 5: [90.0] * 6 + [120.0] * 3 + [180.0],
                6: [90.0] * 12 + [180.0] * 3}


def pair_angles(P, idx=None):
    idx = range(len(P)) if idx is None else idx
    out = []
    for a, b in itertools.combinations(idx, 2):
        # atan2(|a x b|, a.b): acos is ill-conditioned near 0 and 180 deg (the JS twin does the same)
        cr = np.cross(P[a], P[b])
        out.append(math.degrees(math.atan2(math.sqrt(float(cr @ cr)), float(np.dot(P[a], P[b])))))
    return sorted(out)


def ang2(a, b):
    """the angle between two vectors, atan2(|a x b|, a.b) in degrees (the JS angleDeg)"""
    cr = np.cross(a, b)
    return math.degrees(math.atan2(math.sqrt(float(cr @ cr)), float(np.dot(a, b))))


def energy_equal(n, s=EXP):
    """closed form: sum over pairs of the ideal geometry of (2 - 2 cos t)^(-s/2)"""
    return sum((2.0 - 2.0 * math.cos(a * D2R)) ** (-s / 2) for a in IDEAL_ANGLES[n])


# --------------------------------------------------- B. energy, relaxation
def energy(U, R, s=EXP):
    X = U * R[:, None]
    E = 0.0
    n = len(R)
    for i in range(n):
        for j in range(i + 1, n):
            d = X[i] - X[j]
            E += float(d @ d) ** (-s / 2)
    return E


def grad(U, R, s=EXP):
    """dE/du_i (not yet projected): R_i * sum_j -s (x_i - x_j) |x_i - x_j|^(-s-2)"""
    X = U * R[:, None]
    n = len(R)
    G = np.zeros_like(U)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = X[i] - X[j]
            G[i] += -s * d * float(d @ d) ** (-s / 2 - 1)
        G[i] *= R[i]
    return G


def tangential(U, G):
    return G - np.sum(G * U, axis=1)[:, None] * U


def relax_gd(U0, R, s=EXP, eta=ETA, tol=TOL, itmax=ITMAX):
    """THE JS TWIN: u <- normalise(u - eta * grad_t) until max |grad_t| < tol"""
    U = np.array(U0, float)
    U /= np.linalg.norm(U, axis=1)[:, None]
    for it in range(itmax):
        Gt = tangential(U, grad(U, R, s))
        m = float(np.max(np.linalg.norm(Gt, axis=1)))
        if m < tol:
            return U, it, m
        U = U - eta * Gt
        U /= np.linalg.norm(U, axis=1)[:, None]
    return U, itmax, m


def _EG(p, R, s):
    n = len(R)
    P = p.reshape(n, 3)
    L = np.linalg.norm(P, axis=1)
    U = P / L[:, None]
    E = energy(U, R, s)
    Gu = grad(U, R, s)
    Gp = (Gu - np.sum(Gu * U, axis=1)[:, None] * U) / L[:, None]
    return E, Gp.ravel()


def relax_bfgs(U0, R, s=EXP):
    """INDEPENDENT: BFGS on unconstrained 3-vectors p_i, u_i = p_i/|p_i|"""
    r = minimize(_EG, np.asarray(U0, float).ravel(), args=(R, s), jac=True, method='BFGS',
                 options={'gtol': 1e-13, 'maxiter': 50000})
    U = r.x.reshape(len(R), 3)
    return U / np.linalg.norm(U, axis=1)[:, None]


def hessian_eigs(U, R, s=EXP, h=1e-4):
    n = len(U)
    frames = []
    for p in U:
        a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(p, a); t1 /= np.linalg.norm(t1)
        frames.append((t1, np.cross(p, t1)))

    def g(z):
        Q = np.array([U[k] + z[2 * k] * frames[k][0] + z[2 * k + 1] * frames[k][1] for k in range(n)])
        E, Gp = _EG(Q.ravel(), R, s)
        Gp = Gp.reshape(n, 3)
        return np.array([v for k in range(n) for v in (Gp[k] @ frames[k][0], Gp[k] @ frames[k][1])])

    m = 2 * n
    H = np.zeros((m, m))
    for i in range(m):
        z = np.zeros(m); z[i] = h
        gp = g(z); z[i] = -h; gm = g(z)
        H[:, i] = (gp - gm) / (2 * h)
    return np.sort(np.linalg.eigvalsh(0.5 * (H + H.T)))


def radii(x, e, rho, lp=None):
    n = x + e
    lp = tuple(range(e)) if lp is None else lp
    return np.array([rho if k in lp else 1.0 for k in range(n)])


def seeded(x, e, rho, s=EXP, lp=None):
    n = x + e
    U, it, m = relax_gd(np.array(SLOTS[n]), radii(x, e, rho, lp), s)
    return U, it, m


# ---------------------------------------------------- G. Horn's quaternion fit
def jacobi_eig4(A):
    """cyclic Jacobi on a symmetric 4x4 (the JS twin); returns (evals, evecs cols)"""
    A = [row[:] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for sweep in range(60):
        off = sum(A[i][j] ** 2 for i in range(4) for j in range(4) if i != j)
        if off < 1e-30:
            break
        for p in range(3):
            for q in range(p + 1, 4):
                if abs(A[p][q]) < 1e-300:
                    continue
                th = (A[q][q] - A[p][p]) / (2 * A[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1); sn = t * c
                for k in range(4):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - sn * akq
                    A[k][q] = sn * akp + c * akq
                for k in range(4):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - sn * aqk
                    A[q][k] = sn * apk + c * aqk
                for k in range(4):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - sn * vkq
                    V[k][q] = sn * vkp + c * vkq
    return [A[i][i] for i in range(4)], V


def horn(Asrc, Bdst):
    """rotation R (3x3) minimising sum |R a_k - b_k|^2 (Horn 1987, unit quaternion)"""
    S = np.zeros((3, 3))
    for a, b in zip(Asrc, Bdst):
        S += np.outer(a, b)
    Sxx, Sxy, Sxz = S[0]; Syx, Syy, Syz = S[1]; Szx, Szy, Szz = S[2]
    N = [[Sxx + Syy + Szz, Syz - Szy, Szx - Sxz, Sxy - Syx],
         [Syz - Szy, Sxx - Syy - Szz, Sxy + Syx, Szx + Sxz],
         [Szx - Sxz, Sxy + Syx, -Sxx + Syy - Szz, Syz + Szy],
         [Sxy - Syx, Szx + Sxz, Syz + Szy, -Sxx - Syy + Szz]]
    ev, V = jacobi_eig4(N)
    k = int(np.argmax(ev))
    q0, qx, qy, qz = (V[i][k] for i in range(4))
    return np.array([[q0 * q0 + qx * qx - qy * qy - qz * qz, 2 * (qx * qy - q0 * qz), 2 * (qx * qz + q0 * qy)],
                     [2 * (qy * qx + q0 * qz), q0 * q0 - qx * qx + qy * qy - qz * qz, 2 * (qy * qz - q0 * qx)],
                     [2 * (qz * qx - q0 * qy), 2 * (qz * qy + q0 * qx), q0 * q0 - qx * qx - qy * qy + qz * qz]])


def fit_assign(E, Ucur, types):
    """best rotation AND assignment of equilibrium slots E (types in slot order)
    onto the current directions Ucur (types): permutations only within a type"""
    kinds = sorted(set(types))
    best = None
    slot_by = {k: [i for i, t in enumerate(types) if t == k] for k in kinds}
    groups = [slot_by[k] for k in kinds]
    for perms in itertools.product(*[itertools.permutations(g) for g in groups]):
        sigma = [None] * len(types)
        for g, p in zip(groups, perms):
            for i_cur, i_slot in zip(g, p):
                sigma[i_cur] = i_slot
        A = [E[sigma[i]] for i in range(len(types))]
        Rm = horn(A, Ucur)
        res = sum(float(np.sum((Rm @ a - b) ** 2)) for a, b in zip(A, Ucur))
        if best is None or res < best[0] - 1e-12:
            best = (res, sigma, Rm)
    return best


# ------------------------------------------------------- C. mulberry32 (twin)
M32 = 0xFFFFFFFF


def mulberry32(seed):
    st = [seed & M32]

    def rnd():
        st[0] = (st[0] + 0x6D2B79F5) & M32
        t = st[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & M32
        t = (((t + (((t ^ (t >> 7)) * (t | 61)) & M32)) & M32) ^ t)
        return ((t ^ (t >> 14)) & M32) / 4294967296
    return rnd


def random_dirs(rnd, n):
    out = []
    for _ in range(n):
        z = 2 * rnd() - 1
        ph = 2 * math.pi * rnd()
        r = math.sqrt(max(0.0, 1 - z * z))
        out.append((r * math.cos(ph), r * math.sin(ph), z))
    return np.array(out)


# ------------------------------------------------------------ H. AXE names
def mol_geometry(x, e):
    """PhET's MoleculeGeometry.getConfiguration(x, e), as read from its build 1.6.19"""
    if x == 0: return 'empty'
    if x == 1: return 'diatomic'
    if x == 2: return 'linear' if e in (0, 3, 4) else 'bent'
    if x == 3: return {0: 'trigonalPlanar', 1: 'trigonalPyramidal', 2: 'tShaped', 3: 'tShaped'}[e]
    if x == 4: return {0: 'tetrahedral', 1: 'seesaw', 2: 'squarePlanar'}[e]
    if x == 5: return {0: 'trigonalBipyramidal', 1: 'squarePyramidal'}[e]
    if x == 6: return 'octahedral'


EL_GEOM = {0: 'empty', 1: 'diatomic', 2: 'linear', 3: 'trigonalPlanar', 4: 'tetrahedral',
           5: 'trigonalBipyramidal', 6: 'octahedral'}
# PhET's English labels (inventory.json, MOLECULE_SHAPES shape.* / geometry.*)
LABEL = {'empty': '', 'diatomic': 'Linear', 'linear': 'Linear', 'bent': 'Bent',
         'trigonalPlanar': 'Trigonal Planar', 'trigonalPyramidal': 'Trigonal Pyramidal',
         'tShaped': 'T-shaped', 'tetrahedral': 'Tetrahedral', 'seesaw': 'Seesaw',
         'squarePlanar': 'Square Planar', 'trigonalBipyramidal': 'Trigonal Bipyramidal',
         'squarePyramidal': 'Square Pyramidal', 'octahedral': 'Octahedral'}

# ------------------------------------------------------- F. real molecules
# PhET's RealMoleculeShape table, build 1.6.19 (docs/phets/molecule-shapes_en.html):
# primary numbers verbatim; directions built from them here as PhET's constructor does.
PHET_UP = -19.471220333        # PhET's tetrahedral elevation, degrees, as printed
PHET_NH3_POLAR = 1.202623030417028   # radians, as printed


def phet_tetra():
    up = PHET_UP * D2R
    v = [(0.0, 0.0, 1.0)]
    for k in range(3):
        a = 2 * math.pi * k / 3
        v.append((math.cos(a) * math.cos(up), math.sin(a) * math.cos(up), math.sin(up)))
    return v


def real_molecules():
    M = {}

    def add(key, formula, centre, clp, L, outer, olp, order, bonds):
        M[key] = dict(formula=formula, centre=centre, clp=clp, L=L, outer=outer, olp=olp, order=order,
                      bonds=[(tuple(np.array(v) / np.linalg.norm(v)), float(l)) for v, l in bonds])
    t3 = 2 * math.pi / 3
    add('BeCl2', 'BeCl2', 'Be', 0, 1.8, 'Cl', 3, 1, [((1, 0, 0), 1.8), ((-1, 0, 0), 1.8)])
    add('BF3', 'BF3', 'B', 0, 1.313, 'F', 3, 1, [((math.cos(k * t3), math.sin(k * t3), 0), 1.313) for k in range(3)])
    t = 84.8 * D2R
    add('BrF5', 'BrF5', 'Br', 1, 1.774, 'F', 3, 1,
        [((0, -1, 0), 1.689), ((math.sin(t), -math.cos(t), 0), 1.774), ((0, -math.cos(t), math.sin(t)), 1.774),
         ((-math.sin(t), -math.cos(t), 0), 1.774), ((0, -math.cos(t), -math.sin(t)), 1.774)])
    add('CH4', 'CH4', 'C', 0, 1.087, 'H', 0, 1, [(v, 1.087) for v in phet_tetra()])
    t = 87.5 * D2R
    add('ClF3', 'ClF3', 'Cl', 2, 1.698, 'F', 3, 1,
        [((0, -1, 0), 1.598), ((math.sin(t), -math.cos(t), 0), 1.698), ((-math.sin(t), -math.cos(t), 0), 1.698)])
    add('CO2', 'CO2', 'C', 0, 1.163, 'O', 2, 2, [((-1, 0, 0), 1.163), ((1, 0, 0), 1.163)])
    t = 104.5 / 2 * D2R
    add('H2O', 'H2O', 'O', 2, 0.957, 'H', 0, 1, [((math.sin(t), -math.cos(t), 0), 0.957), ((-math.sin(t), -math.cos(t), 0), 0.957)])
    th = PHET_NH3_POLAR
    add('NH3', 'NH3', 'N', 1, 1.017, 'H', 0, 1,
        [((math.sin(th) * math.cos(k * t3), -math.cos(th), math.sin(th) * math.sin(k * t3)), 1.017) for k in range(3)])
    add('PCl5', 'PCl5', 'P', 0, 2.02, 'Cl', 3, 1,
        [((1, 0, 0), 2.14), ((-1, 0, 0), 2.14)] + [((0, math.cos(k * t3), math.sin(k * t3)), 2.02) for k in range(3)])
    ta, te = 173.1 / 2 * D2R, 101.6 / 2 * D2R
    add('SF4', 'SF4', 'S', 1, 1.595, 'F', 3, 1,
        [((math.sin(ta), -math.cos(ta), 0), 1.646), ((-math.sin(ta), -math.cos(ta), 0), 1.646),
         ((0, -math.cos(te), math.sin(te)), 1.545), ((0, -math.cos(te), -math.sin(te)), 1.545)])
    add('SF6', 'SF6', 'S', 0, 1.564, 'F', 3, 1,
        [((0, 0, 1), 1.564), ((0, 0, -1), 1.564), ((0, 1, 0), 1.564), ((0, -1, 0), 1.564), ((1, 0, 0), 1.564), ((-1, 0, 0), 1.564)])
    t = 119 / 2 * D2R
    add('SO2', 'SO2', 'S', 1, 1.431, 'O', 2, 2, [((math.sin(t), -math.cos(t), 0), 1.431), ((-math.sin(t), -math.cos(t), 0), 1.431)])
    add('XeF2', 'XeF2', 'Xe', 3, 1.977, 'F', 3, 1, [((1, 0, 0), 1.977), ((-1, 0, 0), 1.977)])
    add('XeF4', 'XeF4', 'Xe', 2, 1.953, 'F', 3, 1,
        [((1, 0, 0), 1.953), ((-1, 0, 0), 1.953), ((0, 0, 1), 1.953), ((0, 0, -1), 1.953)])
    return M


FULL_LIST = ['H2O', 'CO2', 'SO2', 'XeF2', 'BF3', 'ClF3', 'NH3', 'CH4', 'SF4', 'XeF4', 'BrF5', 'PCl5', 'SF6']
BASICS_LIST = ['BeCl2', 'BF3', 'CH4', 'PCl5', 'SF6']


def fmt(v):
    return '%.12f' % v


# ======================================================================== main
def main():
    # ---- A. ideal geometries and equal-domain energies
    say('== A. ideal geometries (exact) ==')
    put(['ideal', 'tet_deg'], TET)
    say('tetrahedral angle arccos(-1/3) = %.14f deg' % TET)
    for n in range(2, 7):
        P = np.array(SLOTS[n])
        ang = pair_angles(P)
        err = max(abs(a - b) for a, b in zip(ang, IDEAL_ANGLES[n]))
        E = energy_equal(n)
        put(['ideal', 'E%d' % n], E)
        say('N=%d  slots unit %.1e  angle multiset error %.1e   E_equal(1/d^2) = %.15f   (1/d: %.15f)'
            % (n, max(abs(np.linalg.norm(P, axis=1) - 1)), err, E, energy_equal(n, 1.0)))
        put(['ideal', 'E%d_coulomb' % n], energy_equal(n, 1.0))
        assert err < 1e-12
    # the slot energies as the code evaluates them
    for n in range(2, 7):
        Ec = energy(np.array(SLOTS[n]), np.ones(n))
        assert abs(Ec - energy_equal(n)) < 1e-12, (n, Ec)
    say('closed forms: N=2 1/4, N=3 1, N=4 9/4, N=5 17/4, N=6 27/4 (sum over pairs of 1/(2-2cos t))')
    for n, v in ((2, 0.25), (3, 1.0), (4, 2.25), (5, 4.25), (6, 6.75)):
        assert abs(energy_equal(n) - v) < 1e-12
    # a two-point absolute pin and the gradient against a finite difference
    U2 = np.array([[1.0, 0, 0], [0, 1.0, 0]])
    put(['pins', 'E_two_90'], energy(U2, np.array([1.0, 1.0])))
    put(['pins', 'E_two_90_rho'], energy(U2, np.array([0.7, 1.0])))
    say('two domains at 90 deg: E = %.15f (1/2); one a lone pair at rho 0.7: E = %.15f (1/1.49)'
        % (energy(U2, np.array([1.0, 1.0])), energy(U2, np.array([0.7, 1.0]))))
    rng = np.random.default_rng(3)
    Ur = rng.normal(size=(5, 3)); Ur /= np.linalg.norm(Ur, axis=1)[:, None]
    Rr = np.array([0.7, 0.7, 1, 1, 1.0])
    G = grad(Ur, Rr)
    h = 1e-6
    err = 0
    for i in range(5):
        for k in range(3):
            Up = Ur.copy(); Up[i, k] += h
            Um = Ur.copy(); Um[i, k] -= h
            fd = (energy(Up, Rr) - energy(Um, Rr)) / (2 * h)
            err = max(err, abs(fd - G[i, k]))
    say('gradient vs central difference (unnormalised coordinates): max err %.2e' % err)
    assert err < 1e-6

    # ---- B/D. every class at three rho values: GD twin vs BFGS
    say('\n== B/D. every AXE class: GD twin (eta %.2f, tol %.0e) against BFGS ==' % (ETA, TOL))
    classes = [(x, e) for x in range(0, 7) for e in range(0, 7 - x) if x + e >= 1]
    for rho in (0.70, 0.85, 1.00):
        for (x, e) in classes:
            n = x + e
            Rv = radii(x, e, rho)
            U, it, m = seeded(x, e, rho)
            Ub = relax_bfgs(np.array(SLOTS[n]), Rv)
            E, Eb = energy(U, Rv), energy(Ub, Rv)
            bidx = list(range(e, n))
            ab = pair_angles(U, bidx)
            abb = pair_angles(Ub, bidx)
            dang = max([abs(a - b) for a, b in zip(ab, abb)] + [0.0])
            lb = []
            for i in range(e):
                for j in bidx:
                    lb.append(ang2(U[i], U[j]))
            ll = pair_angles(U, list(range(e)))
            key = 'AX%dE%d' % (x, e)
            put(['eq', '%.2f' % rho, key], dict(E=E, it=it, bb=ab, lb=sorted(lb), ll=ll, U=U.tolist()))
            say('rho %.2f %-6s it %6d  E %.12f (BFGS %.12f, dE %.1e, dAngle %.1e)  bond angles %s'
                % (rho, key, it, E, Eb, E - Eb, dang, ' '.join('%.9f' % a for a in sorted(set(round(a, 9) for a in ab)))))
            assert abs(E - Eb) < 1e-11 and dang < 1e-7, (rho, key)
            assert it < ITMAX

    # stability margin of the fixed step: eta * lambda_max < 2 everywhere
    lam_max = 0.0
    for rho in (0.70, 0.85, 1.00):
        for (x, e) in classes:
            if x + e < 2:
                continue
            U, it, m = seeded(x, e, rho)
            ev = hessian_eigs(U, radii(x, e, rho))
            lam_max = max(lam_max, ev[-1])
    put(['gd', 'lam_max'], lam_max)
    say('largest Hessian eigenvalue over all classes and three rho: %.4f; eta*lam = %.3f (< 2 is stable)' % (lam_max, ETA * lam_max))
    assert ETA * lam_max < 2

    # ---- C. random starts, N equal domains: the exact ideal geometries
    say('\n== C. random starts (mulberry32, the JS PRNG) relax to the ideal geometry ==')
    r0 = mulberry32(20260918)
    first = [r0() for _ in range(4)]
    put(['prng', 'first4'], first)
    say('mulberry32(20260918) first four: ' + ' '.join('%.17g' % v for v in first))
    rs = []
    for n in range(2, 7):
        for seed in (101, 202, 303):
            rnd = mulberry32(seed * 10 + n)
            U0 = random_dirs(rnd, n)
            U, it, m = relax_gd(U0, np.ones(n))
            ang = pair_angles(U)
            err = max(abs(a - b) for a, b in zip(ang, IDEAL_ANGLES[n]))
            E = energy(U, np.ones(n))
            rs.append(dict(n=n, seed=seed * 10 + n, it=it, err=err, E=E, U0=U0.tolist()))
            say('N=%d seed %d: %5d steps, max angle error vs ideal %.2e deg, E - E_ideal %.1e' % (n, seed * 10 + n, it, err, E - energy_equal(n)))
            assert err < 1e-8 and abs(E - energy_equal(n)) < 1e-12
    put(['random'], rs)

    # ---- E. the audit
    say('\n== E. audit: VSEPR arrangement = global minimum, same shape, local minimum ==')
    lp_classes = [(x, e) for (x, e) in classes if e >= 1 and x >= 1]

    def audit(rho, s=EXP, nrand=16):
        """returns list of (class, ok, detail)"""
        rows = []
        for (x, e) in lp_classes:
            n = x + e
            U = relax_bfgs(np.array(SLOTS[n]), radii(x, e, rho), s)
            Ev = energy(U, radii(x, e, rho), s)
            # same shape: aligned (identity assignment) to the seed within 30 deg per domain
            Rm = horn(np.array(SLOTS[n]), U)
            dev = max(math.degrees(math.acos(max(-1, min(1, float((Rm @ a) @ b))))) for a, b in zip(np.array(SLOTS[n]), U))
            best = Ev
            for lp in itertools.combinations(range(n), e):
                Ul = relax_bfgs(np.array(SLOTS[n]), radii(x, e, rho, lp), s)
                best = min(best, energy(Ul, radii(x, e, rho, lp), s))
            rr = mulberry32(int(rho * 1000) * 100 + n * 10 + e)
            for k in range(nrand):
                Ul = relax_bfgs(random_dirs(rr, n), radii(x, e, rho), s)
                best = min(best, energy(Ul, radii(x, e, rho), s))
            ev = hessian_eigs(U, radii(x, e, rho), s)
            lam = ev[3]
            ok = bool((best > Ev - 1e-9) and dev < 30 and lam > 1e-6)
            rows.append(((x, e), ok, dict(E=float(Ev), best=float(best), dev=float(dev), lam=float(lam))))
        return rows

    grid = [round(0.60 + 0.02 * k, 2) for k in range(21)]
    first_ok = {}
    audit_rows = {}
    for rho in grid:
        rows = audit(rho)
        bad = [('AX%dE%d' % c) for c, ok, d in rows if not ok]
        audit_rows['%.2f' % rho] = {('AX%dE%d' % c): dict(ok=ok, **d) for c, ok, d in rows}
        say('rho %.2f: %s' % (rho, 'all %d lone-pair classes pass' % len(rows) if not bad else 'FAIL ' + ' '.join(bad)))
        for c, ok, d in rows:
            if not ok:
                say('     %s  E_vsepr %.10f  best %.10f  shape dev %.1f deg  lam %.2e' % ('AX%dE%d' % c, d['E'], d['best'], d['dev'], d['lam']))
    put(['audit', 'grid'], audit_rows)
    # the rho window used by the slider must pass everywhere
    for rho in grid:
        if rho >= 0.70 - 1e-9:
            assert all(v['ok'] for v in audit_rows['%.2f' % rho].values()), rho
    # at rho = 1 every arrangement ties (lone pairs ARE bonds): the audit is trivially ok there

    # ---- E2. why 1/d^2: the same audit for Coulomb 1/d at rho 0.70, and for charge weights
    say('\n== E2. the alternatives fail ==')
    rows = audit(0.70, s=1.0)
    bad = [(c, d) for c, ok, d in rows if not ok]
    for c, d in bad:
        say('Coulomb 1/d at rho 0.70: AX%dE%d fails: E_vsepr %.10f, best %.10f, shape dev %.1f' % (c[0], c[1], d['E'], d['best'], d['dev']))
    assert bad, 'expected Coulomb to fail somewhere at rho 0.7'
    # AX3E2 under Coulomb: T-shaped (lone pairs equatorial) against trigonal planar (lone pairs axial)
    x, e = 3, 2
    UT = relax_bfgs(np.array(SLOTS[5]), radii(3, 2, 0.70, (0, 1)), 1.0)
    UP = relax_bfgs(np.array(SLOTS[5]), radii(3, 2, 0.70, (3, 4)), 1.0)
    ET, EP = energy(UT, radii(3, 2, 0.70, (0, 1)), 1.0), energy(UP, radii(3, 2, 0.70, (3, 4)), 1.0)
    put(['coulomb', 'AX3E2_T'], ET); put(['coulomb', 'AX3E2_planar'], EP)
    say('Coulomb 1/d, rho 0.70, AX3E2: lone pairs equatorial (T) %.12f, axial (trigonal planar) %.12f -> %s wins'
        % (ET, EP, 'planar' if EP < ET else 'T'))
    UT2 = relax_bfgs(np.array(SLOTS[5]), radii(3, 2, 0.70, (0, 1)))
    UP2 = relax_bfgs(np.array(SLOTS[5]), radii(3, 2, 0.70, (3, 4)))
    ET2, EP2 = energy(UT2, radii(3, 2, 0.70, (0, 1))), energy(UP2, radii(3, 2, 0.70, (3, 4)))
    put(['coulomb', 'AX3E2_T_d2'], ET2); put(['coulomb', 'AX3E2_planar_d2'], EP2)
    say('1/d^2,      rho 0.70, AX3E2: lone pairs equatorial (T) %.12f, axial (trigonal planar) %.12f -> %s wins'
        % (ET2, EP2, 'planar' if EP2 < ET2 else 'T'))
    # charge weights (all on the unit sphere, lone pair weight q): the octahedral family fails
    def wenergy(U, w, s):
        E = 0.0
        for i in range(len(w)):
            for j in range(i + 1, len(w)):
                d = U[i] - U[j]
                E += w[i] * w[j] * float(d @ d) ** (-s / 2)
        return E

    def wEG(p, w, s):
        n = len(w); P = p.reshape(n, 3); L = np.linalg.norm(P, axis=1); U = P / L[:, None]
        G = np.zeros_like(U)
        for i in range(n):
            for j in range(n):
                if i != j:
                    d = U[i] - U[j]
                    G[i] += -s * w[i] * w[j] * d * float(d @ d) ** (-s / 2 - 1)
        Gp = (G - np.sum(G * U, axis=1)[:, None] * U) / L[:, None]
        return wenergy(U, w, s), Gp.ravel()

    def wrelax(U0, w, s):
        r = minimize(wEG, np.asarray(U0, float).ravel(), args=(w, s), jac=True, method='BFGS', options={'gtol': 1e-13, 'maxiter': 50000})
        U = r.x.reshape(len(w), 3); return U / np.linalg.norm(U, axis=1)[:, None]
    for s in (1.0, 2.0, 6.0):
        wt = np.array([1.5, 1.5, 1, 1, 1, 1.0]); wc = np.array([1.5, 1, 1.5, 1, 1, 1.0])
        Etr = wenergy(wrelax(np.array(SLOTS[6]), wt, s), wt, s)
        Eci = wenergy(wrelax(np.array(SLOTS[6]), wc, s), wc, s)
        put(['weights', 's%g' % s], dict(trans=Etr, cis=Eci))
        say('charge weights q = 1.5, 1/d^%g, AX4E2: trans (square planar) %.10f, cis %.10f -> %s wins'
            % (s, Etr, Eci, 'cis' if Eci < Etr else 'trans'))
        assert Eci < Etr

    # ---- rate of approach to rho = 1: deviation is O(1 - rho)
    say('\n== the approach to rho = 1 ==')
    rates = {}
    for (x, e, pair) in ((2, 2, (2, 3)), (3, 1, (1, 2)), (2, 1, (1, 2)), (4, 1, (3, 4)), (3, 2, (2, 3)), (5, 1, (1, 2))):
        d1 = pair_angles(seeded(x, e, 0.99)[0], list(pair))[0] - pair_angles(seeded(x, e, 1.0)[0], list(pair))[0]
        d2 = pair_angles(seeded(x, e, 0.98)[0], list(pair))[0] - pair_angles(seeded(x, e, 1.0)[0], list(pair))[0]
        rates['AX%dE%d' % (x, e)] = dict(d99=d1, d98=d2, ratio=d2 / d1)
        say('AX%dE%d  angle(0.99) - ideal = %.10f, angle(0.98) - ideal = %.10f, ratio %.6f (-> 2 for a linear approach)' % (x, e, d1, d2, d2 / d1))
    put(['approach'], rates)

    # ---- the named angles the views print (rho 0.70)
    say('\n== named angles at rho 0.70 (the squeeze view and the directions) ==')
    named = {}

    def named_angles(rho):
        out = {}
        U = seeded(2, 1, rho)[0]; out['AX2E1'] = pair_angles(U, [1, 2])[0]
        U = seeded(2, 2, rho)[0]; out['AX2E2'] = pair_angles(U, [2, 3])[0]
        U = seeded(3, 1, rho)[0]; out['AX3E1'] = pair_angles(U, [1, 2])[0]
        U = seeded(4, 1, rho)[0]; out['AX4E1_ax'] = pair_angles(U, [3, 4])[0]; out['AX4E1_eq'] = pair_angles(U, [1, 2])[0]
        out['AX4E1_axeq'] = pair_angles(U, [1, 3])[0]
        U = seeded(3, 2, rho)[0]; out['AX3E2_axeq'] = pair_angles(U, [2, 3])[0]; out['AX3E2_ax'] = pair_angles(U, [3, 4])[0]
        U = seeded(5, 1, rho)[0]; out['AX5E1_axb'] = pair_angles(U, [1, 2])[0]; out['AX5E1_bb'] = pair_angles(U, [2, 4])[0]
        U = seeded(3, 3, rho)[0]; out['AX3E3_short'] = pair_angles(U, [3, 4])[0]; out['AX3E3_ax'] = pair_angles(U, [4, 5])[0]
        U = seeded(2, 3, rho)[0]; out['AX2E3'] = pair_angles(U, [3, 4])[0]
        U = seeded(4, 2, rho)[0]; out['AX4E2'] = pair_angles(U, [2, 4])[0]
        U = seeded(2, 4, rho)[0]; out['AX2E4'] = pair_angles(U, [4, 5])[0]
        return out
    for rho in (0.70, 0.85, 1.00):
        nm = named_angles(rho)
        named['%.2f' % rho] = nm
        say('rho %.2f: ' % rho + '  '.join('%s %.9f' % (k, v) for k, v in nm.items()))
    put(['named'], named)
    n7 = named['0.70']
    # the directions the brief asks for (and the one the model gets wrong)
    assert n7['AX2E1'] < 120 and n7['AX2E2'] < TET and n7['AX3E1'] < TET and n7['AX4E1_ax'] < 180
    assert n7['AX3E2_axeq'] < 90 and n7['AX5E1_axb'] < 90 and n7['AX4E1_eq'] > 120
    assert abs(n7['AX2E3'] - 180) < 1e-9 and abs(n7['AX4E2'] - 90) < 1e-9 and abs(n7['AX2E4'] - 180) < 1e-9

    # squeeze curves on a grid (the view draws them; the pins sample them)
    grid2 = [round(0.70 + 0.01 * k, 2) for k in range(31)]
    curves = {k: [] for k in n7}
    for rho in grid2:
        nm = named_angles(rho)
        for k in curves:
            curves[k].append(nm[k])
    put(['curves'], dict(rho=grid2, **curves))

    # ---- F. real molecules
    say('\n== F. real molecules (PhET 1.6.19 data) ==')
    RM = real_molecules()
    real_out = {}
    MEAS = {'SO2': ('AX2E1', 119.0), 'H2O': ('AX2E2', 104.5), 'NH3': ('AX3E1', None), 'SF4': ('AX4E1', None),
            'ClF3': ('AX3E2', None), 'BrF5': ('AX5E1', None)}
    for key, m in RM.items():
        U = np.array([b[0] for b in m['bonds']])
        ang = pair_angles(U)
        x, e = len(U), m['clp']
        n = x + e
        # lone pairs: Horn fit of the ideal bond slots onto the real bonds (assignment among bonds)
        types = ['b'] * x
        Eb = np.array(SLOTS[n][e:]) if n > 0 else np.zeros((0, 3))
        res, sigma, Rm = fit_assign(Eb, U, types)
        LP = [(Rm @ np.array(SLOTS[n][k])).tolist() for k in range(e)]
        lpb = sorted(ang2(np.array(l), b) for l in LP for b in U)
        # the model at rho 0.70 fitted onto the real bonds
        Um = seeded(x, e, 0.70)[0]
        resm, sigm, Rmm = fit_assign(Um[e:], U, types)
        model_bb = pair_angles(Um, list(range(e, n)))
        rms = math.sqrt(resm / x) if x else 0.0
        real_out[key] = dict(angles=ang, distinct=sorted(set(round(a, 9) for a in ang)), lp=LP, lpb=lpb, x=x, e=e,
                             order=m['order'], olp=m['olp'], centre=m['centre'], outer=m['outer'],
                             geom=mol_geometry(x, e), elgeom=EL_GEOM[n], fitres=res, model_bb=model_bb,
                             model_fit_rms=rms, lengths=[b[1] for b in m['bonds']])
        say('%-6s AX%dE%d %-20s angles %s   lone-pair fit residual %.3e   model-vs-real rms chord %.5f'
            % (key, x, e, LABEL[mol_geometry(x, e)], ' '.join('%.9f' % a for a in sorted(set(round(a, 9) for a in ang))), res, rms))
    put(['real'], real_out)
    # the NH3 angle PhET's polar angle encodes
    th = PHET_NH3_POLAR
    hnh = math.degrees(math.acos(math.sin(th) ** 2 * math.cos(2 * math.pi / 3) + math.cos(th) ** 2))
    put(['real_named', 'NH3'], hnh)
    say('NH3: H-N-H from PhET polar angle 1.202623030417028 rad = %.12f deg' % hnh)
    put(['real_named', 'CH4'], real_out['CH4']['distinct'][0])
    say('CH4 with PhET elevation -19.471220333 deg: %.12f deg (exact tetrahedral %.12f)' % (real_out['CH4']['distinct'][0], TET))
    # the measured angles against ideal, and the model's direction for each (rho 0.70)
    compare = [('SO2', 'AX2E1', 119.0, 120.0), ('H2O', 'AX2E2', 104.5, TET), ('NH3', 'AX3E1', hnh, TET),
               ('SF4', 'AX4E1_ax', 173.1, 180.0), ('SF4', 'AX4E1_eq', 101.6, 120.0), ('ClF3', 'AX3E2_axeq', 87.5, 90.0),
               ('BrF5', 'AX5E1_axb', 84.8, 90.0)]
    comp = []
    for mol, key, meas, ideal in compare:
        model = n7[key]
        agree = (meas - ideal) * (model - ideal) > 0
        # the rho at which the model angle would equal the measured one (if any in [0.60, 1.00])
        f = lambda r: named_angles(r)[key] - meas
        try:
            fa, fb = f(0.60), f(0.999)
            rfit = brentq(f, 0.60, 0.999, xtol=1e-12) if fa * fb < 0 else None
        except Exception:
            rfit = None
        comp.append(dict(mol=mol, key=key, meas=meas, ideal=ideal, model=model, agree=bool(agree), rfit=rfit))
        say('%-5s %-10s measured %.4f ideal %.4f  model(0.70) %.6f  same direction: %s   rho that fits: %s'
            % (mol, key, meas, ideal, model, agree, 'none in [0.60, 1)' if rfit is None else '%.6f' % rfit))
    put(['compare'], comp)

    # ---- G. Horn against scipy
    say('\n== G. Horn quaternion fit against scipy Rotation.align_vectors ==')
    Rt = Rotation.from_euler('zyx', [37.0, -21.0, 58.0], degrees=True).as_matrix()
    A = np.array(SLOTS[6]); perm = [3, 0, 5, 1, 4, 2]
    B = np.array([Rt @ A[perm[i]] for i in range(6)])
    Rh = horn(np.array([A[perm[i]] for i in range(6)]), B)
    Rs, rssd = Rotation.align_vectors(B, np.array([A[perm[i]] for i in range(6)]))
    say('recovered rotation error %.2e (scipy %.2e), det %.15f' % (np.max(np.abs(Rh - Rt)), np.max(np.abs(Rs.as_matrix() - Rt)), np.linalg.det(Rh)))
    assert np.max(np.abs(Rh - Rt)) < 1e-12
    res, sigma, Rf = fit_assign(A, B, ['b'] * 6)
    # the octahedron maps onto itself 48 ways, so the recovered (R, sigma) need not be (Rt, perm):
    # the residual is the test
    say('fit_assign on the permuted octahedron: residual %.2e (any of its 48 symmetries fits)' % res)
    assert res < 1e-20
    put(['horn'], dict(Rt=Rt.tolist(), perm=perm, euler=[37.0, -21.0, 58.0]))
    # a noisy fit, against scipy: a generic tetrahedral target
    rng = np.random.default_rng(11)
    A4 = np.array(SLOTS[4]); B4 = np.array([Rt @ a for a in A4]) + 0.05 * rng.normal(size=(4, 3))
    B4 /= np.linalg.norm(B4, axis=1)[:, None]
    Rh4 = horn(A4, B4); Rs4, _ = Rotation.align_vectors(B4, A4)
    say('noisy tetrahedron: Horn vs scipy max diff %.2e' % np.max(np.abs(Rh4 - Rs4.as_matrix())))
    assert np.max(np.abs(Rh4 - Rs4.as_matrix())) < 1e-10
    put(['horn', 'noisy'], dict(B=B4.tolist(), R=Rh4.tolist()))

    # ---- H. names
    say('\n== H. the AXE table (PhET getConfiguration) ==')
    names = {}
    for (x, e) in classes + [(0, 0)]:
        names['%d,%d' % (x, e)] = [mol_geometry(x, e), EL_GEOM[x + e]]
    put(['names'], names)
    for n in range(2, 7):
        say('steric %d (%s): ' % (n, LABEL[EL_GEOM[n]]) + ', '.join('AX%dE%d %s' % (n - e, e, LABEL[mol_geometry(n - e, e)]) for e in range(0, n - 1)))

    # ---- isomer ladder at rho 0.70 (the relaxation view)
    say('\n== isomers at rho 0.70: distinct relaxed energies over every slot assignment ==')
    ladders = {}
    for rho_l, key_l in ((0.70, 'ladder'), (0.99, 'ladder99')):
        lad_r = {}
        for (x, e) in lp_classes:
            n = x + e
            found = []
            for lp in itertools.combinations(range(n), e):
                Ul = relax_bfgs(np.array(SLOTS[n]), radii(x, e, rho_l, lp))
                El = energy(Ul, radii(x, e, rho_l, lp))
                if not any(abs(El - f) < 1e-8 for f in found):
                    found.append(El)
            found.sort()
            lad_r['AX%dE%d' % (x, e)] = found
            say('rho %.2f AX%dE%d: %s' % (rho_l, x, e, ' '.join('%.10f' % v for v in found)))
        put([key_l], lad_r)
        if rho_l == 0.70:
            ladders = lad_r

    # ---- the relaxation view's own starts: seed k -> mulberry32(20260918 + 7919 k), lone pairs first
    say('\n== the relaxation view: random starts at rho 0.70, plain descent (the JS twin) ==')
    starts = {}
    for (x, e) in [(2, 2), (3, 1), (4, 1), (3, 2), (2, 3), (4, 2), (3, 3), (2, 4), (5, 1), (1, 4), (6, 0), (5, 0)]:
        n = x + e
        lad = ladders.get('AX%dE%d' % (x, e), None)
        if lad is None:
            lad = [energy(seeded(x, e, 0.70)[0], radii(x, e, 0.70))]
        # Hessian class of every ladder entry: a minimum or a saddle
        kinds = []
        for lp in itertools.combinations(range(n), e):
            Ul = relax_bfgs(np.array(SLOTS[n]), radii(x, e, 0.70, lp))
            El = energy(Ul, radii(x, e, 0.70, lp))
            ev = hessian_eigs(Ul, radii(x, e, 0.70, lp))
            k = min(range(len(lad)), key=lambda i: abs(lad[i] - El))
            if abs(lad[k] - El) < 1e-7 and not any(kk[0] == k for kk in kinds):
                kinds.append((k, 'min' if ev[3] > 1e-6 else 'saddle', float(ev[3])))
        kinds.sort()
        rows, count = [], [0] * (len(lad) + 1)
        for kseed in range(100):
            rnd = mulberry32(20260918 + 7919 * kseed)
            U0 = random_dirs(rnd, n)
            U, it, m = relax_gd(U0, radii(x, e, 0.70), tol=1e-10)
            E = energy(U, radii(x, e, 0.70))
            rank = next((i for i, f in enumerate(lad) if abs(f - E) < 1e-7 * max(1, f)), -1)
            count[rank if rank >= 0 else len(lad)] += 1
            if kseed < 6:
                rows.append(dict(seed=kseed, it=it, E=E, rank=rank))
        starts['AX%dE%d' % (x, e)] = dict(first=rows, count=count, kinds=kinds, ladder=lad)
        say('AX%dE%d  ladder %s  kinds %s  100 starts -> %s   first six: %s'
            % (x, e, ' '.join('%.8f' % v for v in lad), kinds, count, ' '.join('%d:%d(%d)' % (r['seed'], r['rank'], r['it']) for r in rows)))
    put(['starts'], starts)

    io.open(os.path.join(here, 'refvals.json'), 'w', encoding='utf-8').write(json.dumps(OUT, indent=1))
    io.open(os.path.join(here, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(LINES) + '\n')
    say('\nwrote refvals.json and refvals.txt')


if __name__ == '__main__':
    main()
