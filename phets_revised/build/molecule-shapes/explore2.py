#!/usr/bin/env python3
"""Throwaway exploration 2: the Riesz s-energy U = sum w_i w_j / |u_i - u_j|^s
on the unit sphere, bonds w = 1, lone pairs w = q.  For every AXE class: is the
VSEPR-seeded equilibrium (a) a true local minimum, (b) the global minimum over
every slot assignment and 24 random starts, (c) distorted in the direction the
measured molecules show?  Scan s and q."""
import itertools, math, sys
import numpy as np
from scipy.optimize import minimize

SQ3 = math.sqrt(3.0)
SLOTS = {
    1: [(1, 0, 0)],
    2: [(1, 0, 0), (-1, 0, 0)],
    3: [(1, 0, 0), (-0.5, SQ3 / 2, 0), (-0.5, -SQ3 / 2, 0)],
    4: [(0, 0, 1)] + [(math.sqrt(8 / 9) * math.cos(a), math.sqrt(8 / 9) * math.sin(a), -1 / 3)
                      for a in (0, 2 * math.pi / 3, 4 * math.pi / 3)],
    5: [(0, 1, 0), (0, -0.5, SQ3 / 2), (0, -0.5, -SQ3 / 2), (1, 0, 0), (-1, 0, 0)],
    6: [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)],
}


def U_and_G(p, w, s):
    n = len(w)
    P = p.reshape(n, 3)
    L = np.linalg.norm(P, axis=1)
    Uu = P / L[:, None]
    E = 0.0
    Gu = np.zeros_like(Uu)
    for i in range(n):
        for j in range(i + 1, n):
            d = Uu[i] - Uu[j]
            r = math.sqrt(d @ d)
            E += w[i] * w[j] * r ** (-s)
            g = -s * w[i] * w[j] * r ** (-s - 2) * d
            Gu[i] += g
            Gu[j] -= g
    # chain rule through u = p/|p|
    Gp = (Gu - (np.sum(Gu * Uu, axis=1))[:, None] * Uu) / L[:, None]
    return E, Gp.ravel()


def relax(P0, w, s):
    r = minimize(U_and_G, np.asarray(P0, float).ravel(), args=(w, s), jac=True, method='BFGS',
                 options={'gtol': 1e-12, 'maxiter': 20000})
    P = r.x.reshape(len(w), 3)
    P /= np.linalg.norm(P, axis=1)[:, None]
    E, G = U_and_G(P.ravel(), w, s)
    return P, E, np.max(np.abs(G))


def hess_eigs(P, w, s, h=1e-4):
    n = len(P)
    frames = []
    for p in P:
        a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(p, a); t1 /= np.linalg.norm(t1)
        t2 = np.cross(p, t1)
        frames.append((t1, t2))

    def g(z):
        Q = []
        for k, p in enumerate(P):
            t1, t2 = frames[k]
            v = p + z[2 * k] * t1 + z[2 * k + 1] * t2
            Q.append(v)
        Q = np.array(Q)
        E, Gp = U_and_G(Q.ravel(), w, s)
        # gradient w.r.t. z: dQ/dz = t (then normalisation handled inside U_and_G)
        Gp = Gp.reshape(n, 3)
        out = []
        for k in range(n):
            t1, t2 = frames[k]
            out += [Gp[k] @ t1, Gp[k] @ t2]
        return np.array(out)

    m = 2 * n
    Hm = np.zeros((m, m))
    for i in range(m):
        z = np.zeros(m); z[i] = h
        gp = g(z); z[i] = -h; gm = g(z)
        Hm[:, i] = (gp - gm) / (2 * h)
    Hm = 0.5 * (Hm + Hm.T)
    return np.sort(np.linalg.eigvalsh(Hm))


def angles_between(P, idx):
    return sorted(math.degrees(math.acos(max(-1.0, min(1.0, float(P[a] @ P[b])))))
                  for a, b in itertools.combinations(idx, 2))


def weights(n, lp):
    return np.array([QQ if k in lp else 1.0 for k in range(n)])


CLASSES = [(2, 1), (2, 2), (3, 1), (4, 1), (3, 2), (5, 1), (2, 3), (4, 2), (3, 3), (2, 4)]
rng = np.random.default_rng(12345)


def study(x, e, q, s, nrand=24):
    global QQ
    QQ = q
    n = x + e
    lp_v = tuple(range(e))
    Pv, Ev, gv = relax(SLOTS[n], weights(n, lp_v), s)
    ev = hess_eigs(Pv, weights(n, lp_v), s)
    # three rotational zero modes; the next one must be positive
    lam = ev[3] if len(ev) > 3 else float('nan')
    zero3 = np.max(np.abs(ev[:3])) if len(ev) >= 3 else 0.0
    best = (Ev, 'vsepr')
    for lp in itertools.combinations(range(n), e):
        P, E, gg = relax(SLOTS[n], weights(n, lp), s)
        if E < best[0] - 1e-9:
            best = (E, 'slots%s' % (lp,))
    for k in range(nrand):
        P0 = rng.normal(size=(n, 3))
        lp = tuple(range(e))
        P, E, gg = relax(P0, weights(n, lp), s)
        if E < best[0] - 1e-9:
            best = (E, 'random%d' % k)
    bidx = list(range(e, n))
    return Ev, lam, zero3, best, angles_between(Pv, bidx)


if __name__ == '__main__':
    svals = [float(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [1, 2, 3, 4, 6]
    qvals = [float(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.2, 1.5, 2.0, 3.0]
    for s in svals:
        for q in qvals:
            print('s = %g  q = %g' % (s, q))
            for (x, e) in CLASSES:
                Ev, lam, z3, best, ang = study(x, e, q, s)
                flag = 'OK ' if best[1] == 'vsepr' and lam > 1e-7 else '!! '
                print('  %s AX%dE%d  E=%.8f  lam_min=%.3e (rot %.1e)  best=%s dE=%.2e  angles %s'
                      % (flag, x, e, Ev, lam, z3, best[1], best[0] - Ev,
                         ' '.join('%.2f' % a for a in sorted(set(round(a, 6) for a in ang)))))
            sys.stdout.flush()
