#!/usr/bin/env python3
"""Throwaway exploration (not the reference generator): how does a weighted
Coulomb repulsion on the unit sphere behave for every AXE class?

  U = sum_{i<j} w_i w_j / |u_i - u_j|,   w = 1 for a bond, q for a lone pair.

Questions: the bond angles against q; which slot assignment (isomer) is the
global minimum for each (x, e); where that stops being the VSEPR one; whether
each seeded equilibrium is a true local minimum (Hessian); random-start search.
"""
import itertools, math
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


def energy(P, w):
    E = 0.0
    n = len(P)
    for i in range(n):
        for j in range(i + 1, n):
            E += w[i] * w[j] / np.linalg.norm(P[i] - P[j])
    return E


def grad(P, w):
    n = len(P)
    G = np.zeros_like(P)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = P[i] - P[j]
            r = np.linalg.norm(d)
            G[i] -= w[i] * w[j] * d / r ** 3      # dU/du_i
    return G


def tangential(P, G):
    return G - (np.sum(G * P, axis=1))[:, None] * P


def relax(P, w, eta=0.05, tol=1e-13, itmax=200000):
    P = P / np.linalg.norm(P, axis=1)[:, None]
    for it in range(itmax):
        F = -tangential(P, grad(P, w))
        m = np.max(np.linalg.norm(F, axis=1))
        if m < tol:
            return P, it, m
        P = P + eta * F
        P = P / np.linalg.norm(P, axis=1)[:, None]
    return P, itmax, m


def angles(P, idx):
    out = []
    for a, b in itertools.combinations(idx, 2):
        out.append(math.degrees(math.acos(max(-1, min(1, float(P[a] @ P[b]))))))
    return sorted(out)


def seeded(x, e, q):
    n = x + e
    P = np.array(SLOTS[n], float)
    w = np.array([q] * e + [1.0] * x)
    P, it, m = relax(P, w)
    return P, w, it, m


def hessian_min_nonzero(P, w, h=1e-5):
    """eigenvalues of the Hessian of U in local tangent coordinates"""
    n = len(P)
    frames = []
    for p in P:
        a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
        t1 = np.cross(p, a); t1 /= np.linalg.norm(t1)
        t2 = np.cross(p, t1)
        frames.append((t1, t2))

    def Pof(z):
        Q = []
        for k, p in enumerate(P):
            t1, t2 = frames[k]
            v = p + z[2 * k] * t1 + z[2 * k + 1] * t2
            Q.append(v / np.linalg.norm(v))
        return np.array(Q)

    f = lambda z: energy(Pof(z), w)
    m = 2 * n
    Hm = np.zeros((m, m))
    z0 = np.zeros(m)
    for i in range(m):
        for j in range(i, m):
            zpp = z0.copy(); zpp[i] += h; zpp[j] += h
            zpm = z0.copy(); zpm[i] += h; zpm[j] -= h
            zmp = z0.copy(); zmp[i] -= h; zmp[j] += h
            zmm = z0.copy(); zmm[i] -= h; zmm[j] -= h
            Hm[i, j] = Hm[j, i] = (f(zpp) - f(zpm) - f(zmp) + f(zmm)) / (4 * h * h)
    ev = np.sort(np.linalg.eigvalsh(Hm))
    return ev


def isomers(x, e):
    """distinct LP-slot subsets for steric number n = x + e, by relaxed energy"""
    n = x + e
    subs = list(itertools.combinations(range(n), e))
    return subs


def relax_from(n, lp_slots, q):
    P = np.array(SLOTS[n], float)
    w = np.array([q if k in lp_slots else 1.0 for k in range(n)])
    P, it, m = relax(P, w)
    return P, w, energy(P, w)


if __name__ == '__main__':
    CLASSES = [(2, 1), (2, 2), (3, 1), (4, 1), (3, 2), (5, 1), (2, 3), (4, 2), (3, 3), (2, 4)]
    for q in (1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0):
        print('q = %.2f' % q)
        for (x, e) in CLASSES:
            P, w, it, m = seeded(x, e, q)
            bidx = list(range(e, x + e))
            print('   AX%dE%d  angles %s   (it %d, |F| %.1e)' % (x, e, ['%.3f' % a for a in angles(P, bidx)], it, m))
    print()
    # isomer energies
    for (x, e) in [(4, 1), (3, 2), (2, 3), (4, 2), (3, 3), (2, 4), (5, 1)]:
        n = x + e
        for q in (1.1, 1.5, 2.0, 2.5, 3.0, 4.0):
            res = []
            for lp in isomers(x, e):
                P, w, E = relax_from(n, lp, q)
                res.append((E, lp))
            res.sort()
            vsepr = tuple(range(e))
            Ev = [E for E, lp in res if lp == vsepr][0]
            distinct = []
            for E, lp in res:
                if not any(abs(E - d[0]) < 1e-9 for d in distinct):
                    distinct.append((E, lp))
            print('AX%dE%d q=%.1f  VSEPR E=%.10f  distinct: %s' % (x, e, q, Ev, ', '.join('%s:%.6f' % (lp, E - Ev) for E, lp in distinct)))
