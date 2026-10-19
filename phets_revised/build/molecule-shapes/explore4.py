#!/usr/bin/env python3
"""Throwaway exploration 4: radius rho AND weight q AND exponent s together.
Report, per (s, rho, q): whether all ten lone-pair classes rank VSEPR first and
are local minima, and the angles that the measured molecules test:
AX2E1 (SO2 119.0), AX2E2 (H2O 104.5), AX3E1 (NH3 107.8), AX4E1 ax-ax / eq-eq
(SF4 173.1 / 101.6), AX3E2 ax-eq (ClF3 87.5), AX5E1 ax-basal (BrF5 84.8)."""
import itertools, math, sys
import numpy as np
from scipy.optimize import minimize
from explore2 import SLOTS, CLASSES

rng = np.random.default_rng(99)


def U_and_G(p, R, w, s):
    n = len(R)
    P = p.reshape(n, 3)
    L = np.linalg.norm(P, axis=1)
    Uu = P / L[:, None]
    X = Uu * R[:, None]
    E = 0.0
    Gx = np.zeros_like(X)
    for i in range(n):
        for j in range(i + 1, n):
            d = X[i] - X[j]
            r = math.sqrt(d @ d)
            E += w[i] * w[j] * r ** (-s)
            g = -s * w[i] * w[j] * r ** (-s - 2) * d
            Gx[i] += g
            Gx[j] -= g
    Gu = Gx * R[:, None]
    Gp = (Gu - (np.sum(Gu * Uu, axis=1))[:, None] * Uu) / L[:, None]
    return E, Gp.ravel()


def relax(P0, R, w, s):
    r = minimize(U_and_G, np.asarray(P0, float).ravel(), args=(R, w, s), jac=True, method='BFGS',
                 options={'gtol': 1e-12, 'maxiter': 40000})
    P = r.x.reshape(len(R), 3)
    P /= np.linalg.norm(P, axis=1)[:, None]
    return P, U_and_G(P.ravel(), R, w, s)[0]


def ang(P, a, b):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(P[a] @ P[b])))))


def run(s, rho, q, nrand=16):
    allok = True
    info = {}
    for (x, e) in CLASSES:
        n = x + e
        R = np.array([rho] * e + [1.0] * x)
        w = np.array([q] * e + [1.0] * x)
        Pv, Ev = relax(SLOTS[n], R, w, s)
        best = Ev
        for lp in itertools.combinations(range(n), e):
            R2 = np.array([rho if k in lp else 1.0 for k in range(n)])
            w2 = np.array([q if k in lp else 1.0 for k in range(n)])
            P, E = relax(SLOTS[n], R2, w2, s)
            best = min(best, E)
        for k in range(nrand):
            P, E = relax(rng.normal(size=(n, 3)), R, w, s)
            best = min(best, E)
        ok = best > Ev - 1e-9
        allok = allok and ok
        info[(x, e)] = (Pv, ok)
    P = info[(2, 1)][0]; a21 = ang(P, 1, 2)
    P = info[(2, 2)][0]; a22 = ang(P, 2, 3)
    P = info[(3, 1)][0]; a31 = ang(P, 1, 2)
    P = info[(4, 1)][0]; eqeq = ang(P, 1, 2); axax = ang(P, 3, 4)
    P = info[(3, 2)][0]; axeq = ang(P, 2, 3)
    P = info[(5, 1)][0]; axb = ang(P, 1, 2)     # slot 1 is trans to the LP (slot 0): the axial bond
    bad = [k for k, v in info.items() if not v[1]]
    return allok, bad, (a21, a22, a31, axax, eqeq, axeq, axb)


if __name__ == '__main__':
    svals = [float(a) for a in sys.argv[1].split(',')]
    rvals = [float(a) for a in sys.argv[2].split(',')]
    qvals = [float(a) for a in sys.argv[3].split(',')]
    print('   s   rho    q  | SO2 119.0  H2O 104.5  NH3 107.8 | SF4 173.1 / 101.6 | ClF3 87.5 | BrF5 84.8 | rank')
    for s in svals:
        for rho in rvals:
            for q in qvals:
                ok, bad, A = run(s, rho, q)
                print('%5.2f %5.2f %5.2f | %9.2f %9.2f %9.2f | %8.2f / %6.2f | %9.2f | %9.2f | %s'
                      % (s, rho, q, A[0], A[1], A[2], A[3], A[4], A[5], A[6],
                         'all VSEPR' if ok else 'FAIL ' + ' '.join('AX%dE%d' % k for k in bad)))
                sys.stdout.flush()
