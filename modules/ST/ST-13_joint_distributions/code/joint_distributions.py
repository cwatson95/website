"""ST-13  Joint distributions of two random variables -- pmf/pdf, marginals, independence.

Probability-theory trunk, module ST-13 (modules/topic_network.txt).
Source: Penn State STAT 414, Lesson 17 (Two Discrete Random Variables) and
Lesson 20 (Two Continuous Random Variables).  Builds on ~ST-05 (a single discrete
random variable: pmf, cdf, E[X], variance) and leads into ~ST-14 (covariance,
correlation, conditional distributions).

A *joint* distribution describes two random variables X, Y on the same sample
space at once.  Discrete (L17) and continuous (L20) run perfectly parallel:

  discrete                                continuous
  -------------------------------------   -------------------------------------
  joint pmf   f(x,y) = P(X=x, Y=y)        joint pdf   f(x,y) >= 0
  sum_{x,y} f = 1                         int int f dx dy = 1
  marginal    f_X(x) = sum_y f(x,y)       marginal    f_X(x) = int f(x,y) dy
  independent f(x,y) = f_X(x) f_Y(y)      independent f(x,y) = f_X(x) f_Y(y)
  E[g] = sum_{x,y} g(x,y) f(x,y)          E[g] = int int g(x,y) f(x,y) dx dy
  F(x,y) = sum_{u<=x, v<=y} f(u,v)        F(x,y) = int_{-inf}^x int_{-inf}^y f

Sum becomes integral; everything else is identical.  This module implements both
columns and a 1-D / 2-D midpoint integrator so the continuous identities can be
checked numerically against the closed forms.
"""

import math

import numpy as np

__all__ = [
    # discrete (STAT 414 L17)
    "joint_pmf_is_valid", "marginal_x", "marginal_y", "independent_rv_check",
    "expectation_joint", "joint_cdf", "marginal_cdf_x",
    # continuous (STAT 414 L20)
    "joint_pdf_is_valid", "normalize_joint_pdf", "marginal_pdf_x",
    "marginal_pdf_y", "independent_pdf_check", "expectation_joint_continuous",
    "joint_cdf_continuous",
    # integrators
    "_integrate", "_integrate2d",
]


# --- numerical integrators (cf. ~SM-06 _integrate) ---------------------------

def _integrate(f, a, b, n=2000):
    """Midpoint rule for the 1-D integral int_a^b f(x) dx."""
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) for i in range(n)) * h


def _integrate2d(f, ax, bx, ay, by, nx=400, ny=400):
    """Midpoint rule for the 2-D integral int int f(x,y) dx dy over a rectangle.

    f must accept numpy arrays (it is evaluated on a meshgrid)."""
    hx = (bx - ax) / nx
    hy = (by - ay) / ny
    xs = ax + (np.arange(nx) + 0.5) * hx
    ys = ay + (np.arange(ny) + 0.5) * hy
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    return float(np.sum(f(X, Y)) * hx * hy)


# === DISCRETE: two discrete random variables (STAT 414 L17) ==================
# Convention: P is a 2-D array, P[i, j] = f(x_i, y_j); rows index X, cols index Y.

def joint_pmf_is_valid(P, tol=1e-12):
    """Valid joint pmf: f(x,y) >= 0 for all (x,y) and sum_{x,y} f(x,y) = 1."""
    P = np.asarray(P, dtype=float)
    return bool(np.all(P >= -tol) and abs(float(P.sum()) - 1.0) <= 1e-9)


def marginal_x(P):
    """Marginal pmf of X: f_X(x) = sum_y f(x,y)  (sum out y -> sum over columns)."""
    return np.asarray(P, dtype=float).sum(axis=1)


def marginal_y(P):
    """Marginal pmf of Y: f_Y(y) = sum_x f(x,y)  (sum out x -> sum over rows)."""
    return np.asarray(P, dtype=float).sum(axis=0)


def independent_rv_check(P, tol=1e-9):
    """X, Y independent iff f(x,y) = f_X(x) f_Y(y) everywhere (outer product)."""
    P = np.asarray(P, dtype=float)
    outer = np.outer(marginal_x(P), marginal_y(P))
    return bool(np.allclose(P, outer, atol=tol))


def expectation_joint(g, x_vals, y_vals, P):
    """E[g(X,Y)] = sum_{x,y} g(x,y) f(x,y)  (LOTUS for two discrete RVs)."""
    P = np.asarray(P, dtype=float)
    total = 0.0
    for i, x in enumerate(x_vals):
        for j, y in enumerate(y_vals):
            total += g(x, y) * P[i, j]
    return total


def joint_cdf(P, x_vals, y_vals, x, y):
    """Joint cdf F(x,y) = P(X<=x, Y<=y) = sum_{x_i<=x, y_j<=y} f(x_i, y_j)."""
    P = np.asarray(P, dtype=float)
    total = 0.0
    for i, xi in enumerate(x_vals):
        if xi <= x:
            for j, yj in enumerate(y_vals):
                if yj <= y:
                    total += P[i, j]
    return total


def marginal_cdf_x(P, x_vals, x):
    """Marginal cdf F_X(x) = P(X<=x) = sum_{x_i<=x} f_X(x_i) = F(x, +inf)."""
    fx = marginal_x(P)
    return float(sum(fx[i] for i, xi in enumerate(x_vals) if xi <= x))


# === CONTINUOUS: two continuous random variables (STAT 414 L20) ==============
# Convention: f is a callable f(x, y) (numpy-broadcastable) on a rectangle support.

def normalize_joint_pdf(shape, ax, bx, ay, by, n=400):
    """Normalizing constant c with c*shape a valid pdf: c = 1 / int int shape dx dy."""
    total = _integrate2d(shape, ax, bx, ay, by, n, n)
    return 1.0 / total


def joint_pdf_is_valid(f, ax, bx, ay, by, n=400, tol=1e-3):
    """Valid joint pdf: f >= 0 on its support and int int f(x,y) dx dy = 1."""
    total = _integrate2d(f, ax, bx, ay, by, n, n)
    xs = np.linspace(ax, bx, 25)
    ys = np.linspace(ay, by, 25)
    X, Y = np.meshgrid(xs, ys)
    nonneg = bool(np.all(f(X, Y) >= -tol))
    return bool(nonneg and abs(total - 1.0) <= tol)


def marginal_pdf_x(f, x, ay, by, n=2000):
    """Marginal pdf of X: f_X(x) = int f(x,y) dy  (integrate y out)."""
    return _integrate(lambda y: f(x, y), ay, by, n)


def marginal_pdf_y(f, y, ax, bx, n=2000):
    """Marginal pdf of Y: f_Y(y) = int f(x,y) dx  (integrate x out)."""
    return _integrate(lambda x: f(x, y), ax, bx, n)


def independent_pdf_check(f, ax, bx, ay, by, grid=5, tol=1e-3):
    """X, Y independent iff f(x,y) = f_X(x) f_Y(y); tested on a grid of points."""
    xs = [ax + (i + 0.5) * (bx - ax) / grid for i in range(grid)]
    ys = [ay + (j + 0.5) * (by - ay) / grid for j in range(grid)]
    fxs = [marginal_pdf_x(f, x, ay, by) for x in xs]
    fys = [marginal_pdf_y(f, y, ax, bx) for y in ys]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            if abs(float(f(x, y)) - fxs[i] * fys[j]) > tol:
                return False
    return True


def expectation_joint_continuous(g, f, ax, bx, ay, by, n=400):
    """E[g(X,Y)] = int int g(x,y) f(x,y) dx dy  (continuous LOTUS)."""
    return _integrate2d(lambda x, y: g(x, y) * f(x, y), ax, bx, ay, by, n, n)


def joint_cdf_continuous(f, ax, ay, x, y, n=400):
    """Joint cdf F(x,y) = P(X<=x, Y<=y) = int_ax^x int_ay^y f(u,v) dv du."""
    if x <= ax or y <= ay:
        return 0.0
    return _integrate2d(f, ax, x, ay, y, n, n)


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-13 joint distributions of two random variables -- demo")
    print("=" * 60)

    # --- discrete: f(x,y) = (x+y)/32, x in {1,2}, y in {1,2,3,4}  (L17) -------
    x_vals, y_vals = [1, 2], [1, 2, 3, 4]
    P = np.array([[(x + y) for y in y_vals] for x in x_vals], dtype=float) / 32.0
    print("\nDISCRETE  f(x,y) = (x+y)/32,  x in {1,2}, y in {1,2,3,4}")
    print(f"  valid joint pmf?            {joint_pmf_is_valid(P)}")
    print(f"  f_X = {marginal_x(P)}   (sums to {marginal_x(P).sum():.3f})")
    print(f"  f_Y = {marginal_y(P)}   (sums to {marginal_y(P).sum():.3f})")
    print(f"  independent?                {independent_rv_check(P)}")
    EX = expectation_joint(lambda x, y: x, x_vals, y_vals, P)
    EY = expectation_joint(lambda x, y: y, x_vals, y_vals, P)
    EXY = expectation_joint(lambda x, y: x * y, x_vals, y_vals, P)
    print(f"  E[X]={EX:.4f}  E[Y]={EY:.4f}  E[XY]={EXY:.4f}  Cov={EXY-EX*EY:+.4f}")
    print(f"  F(1,2) = P(X<=1,Y<=2) = {joint_cdf(P, x_vals, y_vals, 1, 2):.4f}")
    print(f"  F(2,4) = {joint_cdf(P, x_vals, y_vals, 2, 4):.4f}  (whole mass)")

    # an independent discrete pair (outer product of two marginals)
    Pi = np.outer([0.4, 0.6], [0.5, 0.5])
    print(f"\n  independent example P=outer([.4,.6],[.5,.5]) -> "
          f"independent? {independent_rv_check(Pi)}")

    # --- continuous: independent f=4xy, dependent f=x+y on unit square (L20) --
    print("\nCONTINUOUS  unit square 0<x<1, 0<y<1")
    f_ind = lambda x, y: 4.0 * x * y          # independent
    f_dep = lambda x, y: x + y                # dependent
    print(f"  f=4xy   valid pdf? {joint_pdf_is_valid(f_ind, 0, 1, 0, 1)}   "
          f"independent? {independent_pdf_check(f_ind, 0, 1, 0, 1)}")
    print(f"  f=x+y   valid pdf? {joint_pdf_is_valid(f_dep, 0, 1, 0, 1)}   "
          f"independent? {independent_pdf_check(f_dep, 0, 1, 0, 1)}")
    print(f"  f=4xy   f_X(0.5) = {marginal_pdf_x(f_ind, 0.5, 0, 1):.4f}  "
          f"(closed form 2x = 1.0)")
    print(f"  f=x+y   f_X(0.3) = {marginal_pdf_x(f_dep, 0.3, 0, 1):.4f}  "
          f"(closed form x+1/2 = 0.8)")
    eX = expectation_joint_continuous(lambda x, y: x, f_dep, 0, 1, 0, 1)
    eXY = expectation_joint_continuous(lambda x, y: x * y, f_dep, 0, 1, 0, 1)
    print(f"  f=x+y   E[X]={eX:.4f} (7/12={7/12:.4f})  E[XY]={eXY:.4f} (1/3)")
    print(f"  f=4xy   F(0.5,0.5) = {joint_cdf_continuous(f_ind, 0, 0, 0.5, 0.5):.4f}"
          f"  (x^2 y^2 = 0.0625)")
    print(f"  f=4xy   F(1,1)     = {joint_cdf_continuous(f_ind, 0, 0, 1, 1):.4f}  (=1)")


if __name__ == "__main__":
    _demo()
