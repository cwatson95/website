"""
MA-13  Calculus of variations -- extremizing a functional J[y] = int L(x,y,y') dx,
the Euler-Lagrange equation, the Beltrami first integral (when L has no explicit
x), constraints, and the classic problems (geodesic, brachistochrone, catenary).

Part of the physics topic network (modules/topic_network.txt, module MA-13).
This is the mathematical core of ~CM-17 (Lagrangian mechanics: action int L dt) and
~RE-12 (geodesics in spacetime); it is bridge B1 of the network.

Pure Python, dependency-free. The functional is discretized segment-by-segment;
partial derivatives of L(x,y,y') are taken by central differences, so any L works.
A coordinate-Newton minimizer recovers extremals (e.g. the straight-line geodesic),
and the Euler-Lagrange / Beltrami diagnostics are checked on analytic solutions.
"""

import math

__all__ = [
    "functional", "euler_lagrange_residual", "beltrami", "minimize_path",
    "cycloid_brachistochrone", "catenary",
]

_D = 1e-6   # finite-difference step for L's partials


def _Ly(L, x, y, p):
    return (L(x, y + _D, p) - L(x, y - _D, p)) / (2 * _D)


def _Lp(L, x, y, p):
    return (L(x, y, p + _D) - L(x, y, p - _D)) / (2 * _D)


# --- the functional ----------------------------------------------------------

def functional(L, xs, ys):
    """J[y] = int L(x, y, y') dx evaluated on the sampled path (xs, ys) by the
    midpoint rule on each segment (x, y at the midpoint, y' = slope)."""
    J = 0.0
    for i in range(len(xs) - 1):
        h = xs[i + 1] - xs[i]
        xm = 0.5 * (xs[i] + xs[i + 1])
        ym = 0.5 * (ys[i] + ys[i + 1])
        p = (ys[i + 1] - ys[i]) / h
        J += L(xm, ym, p) * h
    return J


# --- Euler-Lagrange and Beltrami diagnostics ---------------------------------

def euler_lagrange_residual(L, xs, ys):
    """Euler-Lagrange residual  dL/dy - d/dx(dL/dy')  at each interior node, with
    y' centred and d/dx(dL/dy') by differencing L_p between adjacent midpoints.
    ~0 along a true extremal."""
    n = len(xs)
    res = []
    for i in range(1, n - 1):
        hL = xs[i] - xs[i - 1]
        hR = xs[i + 1] - xs[i]
        # midpoints left/right of node i
        xmL, ymL, pL = 0.5 * (xs[i - 1] + xs[i]), 0.5 * (ys[i - 1] + ys[i]), (ys[i] - ys[i - 1]) / hL
        xmR, ymR, pR = 0.5 * (xs[i] + xs[i + 1]), 0.5 * (ys[i] + ys[i + 1]), (ys[i + 1] - ys[i]) / hR
        dLp_dx = (_Lp(L, xmR, ymR, pR) - _Lp(L, xmL, ymL, pL)) / (0.5 * (hL + hR))
        Ly = _Ly(L, xs[i], ys[i], 0.5 * (pL + pR))
        res.append(Ly - dLp_dx)
    return res


def beltrami(L, x, y, p):
    """Beltrami integrand  B = L - y' (dL/dy').  When L has no explicit x
    dependence, B is constant along an extremal (the 'first integral' /
    conserved 'energy' -- the variational ancestor of the Hamiltonian, ~CM-19)."""
    return L(x, y, p) - p * _Lp(L, x, y, p)


# --- recovering an extremal numerically --------------------------------------

def minimize_path(L, xa, ya, xb, yb, N=15, sweeps=400, tol=1e-12):
    """Minimize J[y] over interior nodes by coordinate-wise Newton sweeps (each
    node depends only on its two adjacent segments). Endpoints are fixed. Returns
    (xs, ys). For a convex L (e.g. arclength) this converges to the extremal."""
    xs = [xa + (xb - xa) * i / (N + 1) for i in range(N + 2)]
    ys = [ya + (yb - ya) * (x - xa) / (xb - xa) for x in xs]   # straight-line start
    # nudge the interior so we can watch it relax back
    for i in range(1, N + 1):
        ys[i] += 0.3 * math.sin(math.pi * (xs[i] - xa) / (xb - xa))

    def local_J(i, yi):
        hL = xs[i] - xs[i - 1]
        hR = xs[i + 1] - xs[i]
        xmL, ymL, pL = 0.5 * (xs[i - 1] + xs[i]), 0.5 * (ys[i - 1] + yi), (yi - ys[i - 1]) / hL
        xmR, ymR, pR = 0.5 * (xs[i] + xs[i + 1]), 0.5 * (yi + ys[i + 1]), (ys[i + 1] - yi) / hR
        return L(xmL, ymL, pL) * hL + L(xmR, ymR, pR) * hR

    d = 1e-5
    for _ in range(sweeps):
        change = 0.0
        for i in range(1, N + 1):
            yi = ys[i]
            f0 = local_J(i, yi)
            g = (local_J(i, yi + d) - local_J(i, yi - d)) / (2 * d)
            H = (local_J(i, yi + d) - 2 * f0 + local_J(i, yi - d)) / (d * d)
            step = -g / H if H > 1e-12 else -0.01 * g
            if step > 0.5:
                step = 0.5
            elif step < -0.5:
                step = -0.5
            ys[i] += step
            change = max(change, abs(step))
        if change < tol:
            break
    return xs, ys


# --- analytic reference solutions --------------------------------------------

def cycloid_brachistochrone(a, thetas):
    """Brachistochrone solution: a cycloid x=a(t-sin t), y=a(1-cos t). Returns
    (xs, ys) for the given parameter values. The brachistochrone Lagrangian is
    L=sqrt((1+y'^2)/y); along this curve Beltrami B = 1/sqrt(y(1+y'^2)) = 1/sqrt(2a)."""
    xs = [a * (t - math.sin(t)) for t in thetas]
    ys = [a * (1 - math.cos(t)) for t in thetas]
    return xs, ys


def catenary(c, xs):
    """Minimal surface of revolution: y = c cosh(x/c). Lagrangian L = y sqrt(1+y'^2);
    along the catenary Beltrami B = y/sqrt(1+y'^2) = c (constant)."""
    return [c * math.cosh(x / c) for x in xs]


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-13 calculus of variations -- demo")
    print("=" * 38)

    arclen = lambda x, y, p: math.sqrt(1 + p * p)
    print("\nshortest path (geodesic), L = sqrt(1+y'^2):")
    xs, ys = minimize_path(arclen, 0.0, 0.0, 1.0, 1.0, N=15)
    line = [x for x in xs]                                   # exact: y = x
    maxdev = max(abs(ys[i] - line[i]) for i in range(len(xs)))
    print(f"  J[min] = {functional(arclen, xs, ys):.6f}   (exact sqrt(2) = {math.sqrt(2):.6f})")
    print(f"  max |y - x| over the recovered path = {maxdev:.2e}  (started bent by 0.3)")
    res = euler_lagrange_residual(arclen, xs, ys)
    print(f"  max |Euler-Lagrange residual| = {max(abs(r) for r in res):.2e}")

    print("\nBeltrami first integral along the analytic curves:")
    Lb = lambda x, y, p: math.sqrt((1 + p * p) / y)          # brachistochrone
    a = 1.0
    th = [0.4 + 0.3 * k for k in range(1, 8)]
    xb, yb = cycloid_brachistochrone(a, th)
    # exact slope on the cycloid: y' = dy/dx = sin t / (1 - cos t)
    Bvals = [beltrami(Lb, xb[k], yb[k], math.sin(th[k]) / (1 - math.cos(th[k])))
             for k in range(len(th))]
    print(f"  brachistochrone  B = {[round(b,5) for b in Bvals]}")
    print(f"    -> ~ 1/sqrt(2a) = {1/math.sqrt(2*a):.5f}")

    Lc = lambda x, y, p: y * math.sqrt(1 + p * p)            # catenary
    c = 1.3
    xc = [-1.0 + 0.3 * k for k in range(8)]
    yc = catenary(c, xc)
    # exact slope on the catenary: y' = sinh(x/c)
    Bc = [beltrami(Lc, xc[k], yc[k], math.sinh(xc[k] / c)) for k in range(len(xc))]
    print(f"  catenary        B = {[round(b,5) for b in Bc]}   -> ~ c = {c}")


if __name__ == "__main__":
    _demo()
