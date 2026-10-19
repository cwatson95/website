#!/usr/bin/env python3
"""Throwaway exploration 3: the RADIUS model.  Bonds sit on the unit sphere,
lone pairs on a sphere of radius rho < 1 (PhET's repulsion puts them at 7
against 10); every pair repels as 1/d^s with d the 3-D distance.  Same audit
as explore2: local minimum (Hessian), global minimum (all slot seeds + random
starts), angles."""
import itertools, math, sys
import numpy as np
from scipy.optimize import minimize
from explore2 import SLOTS, angles_between, CLASSES

rng = np.random.default_rng(777)


def U_and_G(p, R, s):
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
            E += r ** (-s)
            g = -s * r ** (-s - 2) * d
            Gx[i] += g
            Gx[j] -= g
    Gu = Gx * R[:, None]
    Gp = (Gu - (np.sum(Gu * Uu, axis=1))[:, None] * Uu) / L[:, None]
    return E, Gp.ravel()


def relax(P0, R, s):
    r = minimize(U_and_G, np.asarray(P0, float).ravel(), args=(R, s), jac=True, method='BFGS',
                 options={'gtol': 1e-12, 'maxiter': 40000})
    P = r.x.reshape(len(R), 3)
    P /= np.linalg.norm(P, axis=1)[:, None]
    E, G = U_and_G(P.ravel(), R, s)
    return P, E, np.max(np.abs(G))


def hess_eigs(P, R, s, h=1e-4):
    n = len(P)
    frames = []
    for p in P:
        a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(p, a); t1 /= np.linalg.norm(t1)
        frames.append((t1, np.cross(p, t1)))

    def g(z):
        Q = np.array([P[k] + z[2 * k] * frames[k][0] + z[2 * k + 1] * frames[k][1] for k in range(n)])
        E, Gp = U_and_G(Q.ravel(), R, s)
        Gp = Gp.reshape(n, 3)
        return np.array([v for k in range(n) for v in (Gp[k] @ frames[k][0], Gp[k] @ frames[k][1])])

    m = 2 * n
    Hm = np.zeros((m, m))
    for i in range(m):
        z = np.zeros(m); z[i] = h
        gp = g(z); z[i] = -h; gm = g(z)
        Hm[:, i] = (gp - gm) / (2 * h)
    return np.sort(np.linalg.eigvalsh(0.5 * (Hm + Hm.T)))


def radii(n, lp, rho):
    return np.array([rho if k in lp else 1.0 for k in range(n)])


def study(x, e, rho, s, nrand=24):
    n = x + e
    lp_v = tuple(range(e))
    Pv, Ev, gv = relax(SLOTS[n], radii(n, lp_v, rho), s)
    ev = hess_eigs(Pv, radii(n, lp_v, rho), s)
    lam = ev[3] if len(ev) > 3 else float('nan')
    best = (Ev, 'vsepr')
    for lp in itertools.combinations(range(n), e):
        P, E, gg = relax(SLOTS[n], radii(n, lp, rho), s)
        if E < best[0] - 1e-9:
            best = (E, 'slots%s' % (lp,))
    for k in range(nrand):
        P, E, gg = relax(rng.normal(size=(n, 3)), radii(n, lp_v, rho), s)
        if E < best[0] - 1e-9:
            best = (E, 'random%d' % k)
    return Ev, lam, best, angles_between(Pv, list(range(e, n)))


if __name__ == '__main__':
    svals = [float(a) for a in sys.argv[1].split(',')]
    rvals = [float(a) for a in sys.argv[2].split(',')]
    for s in svals:
        for rho in rvals:
            print('s = %g  rho = %g' % (s, rho))
            for (x, e) in CLASSES:
                Ev, lam, best, ang = study(x, e, rho, s)
                flag = 'OK ' if best[1] == 'vsepr' and lam > 1e-7 else '!! '
                print('  %s AX%dE%d  E=%.8f  lam_min=%.3e  best=%s dE=%.2e  angles %s'
                      % (flag, x, e, Ev, lam, best[1], best[0] - Ev,
                         ' '.join('%.2f' % a for a in sorted(set(round(a, 6) for a in ang)))))
            sys.stdout.flush()
