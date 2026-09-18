"""MA-04 figures -- eigenvectors as the axes of an ellipse, and the Jacobi
rotation algorithm driving the off-diagonal norm to zero.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from linalg import matvec, eig_symmetric           # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _off_norm(a, n):
    """Frobenius norm of the strict upper off-diagonal (as in eig_symmetric)."""
    return math.sqrt(sum(a[p][q] ** 2 for p in range(n) for q in range(p + 1, n)))


def _jacobi_history(A, max_sweeps=10):
    """Cyclic Jacobi sweeps (the algorithm `eig_symmetric` uses), recording the
    off-diagonal norm before each sweep. Returns (history, sorted diagonal)."""
    n = len(A)
    a = [row[:] for row in A]
    hist = []
    for _ in range(max_sweeps):
        off = _off_norm(a, n)
        hist.append(off)
        if off <= 1e-16:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                app, aqq, apq = a[p][p], a[q][q], a[p][q]
                a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
                a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
                a[p][q] = a[q][p] = 0.0
                for k in range(n):
                    if k != p and k != q:
                        akp, akq = a[k][p], a[k][q]
                        a[k][p] = a[p][k] = c * akp - s * akq
                        a[k][q] = a[q][k] = s * akp + c * akq
    return hist, sorted(a[i][i] for i in range(n))


def main():
    caps = {}

    # Fig 1 -- a symmetric A maps the unit circle to an ellipse whose principal
    # axes are the eigenvectors (lengths = eigenvalues), from eig_symmetric.
    A = [[2.0, 0.8], [0.8, 1.4]]
    vals, vecs = eig_symmetric(A)                # vals ascending; vecs = columns
    th = np.linspace(0, 2 * math.pi, 361)
    circ = np.array([[math.cos(a), math.sin(a)] for a in th])
    ell = np.array([matvec(A, [math.cos(a), math.sin(a)]) for a in th])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(circ[:, 0], circ[:, 1], color=STEEL, lw=1.4, ls="--",
            label="unit circle")
    ax.plot(ell[:, 0], ell[:, 1], color=INK, lw=2.2,
            label=r"image $A\,x$ (ellipse)")
    for lam, v, col in zip(vals, vecs, (ALT, FLOW)):
        ax.annotate("", xy=(lam * v[0], lam * v[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
        ax.text(lam * v[0] * 1.08 + 0.05, lam * v[1] * 1.08,
                fr"$\lambda={lam:.2f}$", color=col, fontsize=11)
    ax.axhline(0, color="0.85", lw=0.6); ax.axvline(0, color="0.85", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"Eigenvectors as principal axes: $A v_i=\lambda_i v_i$")
    ax.legend(loc="lower right", frameon=False, fontsize=9.5)
    _save(fig, "fig1_eigen_ellipse.svg")
    caps["fig1_eigen_ellipse.svg"] = (
        r"Eigenvectors as the axes of an ellipse. A symmetric "
        r"$A=\begin{bmatrix}2&0.8\\0.8&1.4\end{bmatrix}$ maps the unit circle "
        r"(dashed) to an ellipse (solid); its principal semi-axes lie along the "
        r"orthonormal eigenvectors $v_1,v_2$ with lengths equal to the eigenvalues "
        r"$\lambda_1\approx" + f"{vals[0]:.2f}" + r",\ \lambda_2\approx"
        + f"{vals[1]:.2f}" + r"$ (from `eig_symmetric`), since $A v_i=\lambda_i v_i$.")

    # Fig 2 -- Jacobi rotations zero the off-diagonal norm (super-linearly).
    S = [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]]   # eigs 2, 2 +/- sqrt2
    hist, diag = _jacobi_history(S)
    vals_mod, _ = eig_symmetric(S)               # cross-check via the module
    exact = sorted([2 - math.sqrt(2), 2.0, 2 + math.sqrt(2)])
    assert max(abs(d - e) for d, e in zip(diag, exact)) < 1e-9
    assert max(abs(d - m) for d, m in zip(diag, vals_mod)) < 1e-9

    floor = 1e-17
    yy = [max(h, floor) for h in hist]
    sweeps = list(range(len(yy)))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogy(sweeps, yy, "o-", color=INK, lw=2, ms=7, mfc="white", mew=1.6)
    ax.axhline(2.2e-16, color=ALT, lw=1.0, ls=":")
    ax.text(0.02, 2.6e-16, "machine precision", color=ALT, fontsize=9,
            transform=ax.get_yaxis_transform(), va="bottom")
    ax.set_xlabel("Jacobi sweep")
    ax.set_ylabel(r"off-diagonal norm  $\sqrt{\sum_{p<q}a_{pq}^2}$")
    ax.set_xticks(sweeps)
    ax.set_title("Jacobi diagonalization: off-diagonal norm collapses")
    eigtxt = r"eigenvalues $\to\ 2,\ 2\pm\sqrt{2}$" + "\n" + \
        f"= {diag[0]:.4f}, {diag[1]:.4f}, {diag[2]:.4f}"
    ax.text(0.97, 0.95, eigtxt, transform=ax.transAxes, va="top", ha="right",
            fontsize=9.5, bbox=dict(boxstyle="round", fc="white", ec="0.7",
                                    alpha=0.9))
    _save(fig, "fig2_jacobi_convergence.svg")
    caps["fig2_jacobi_convergence.svg"] = (
        r"How `eig_symmetric` works: cyclic Jacobi rotations drive the off-diagonal "
        r"Frobenius norm of $S=\mathrm{tridiag}(1,2,1)$ to zero. The decay is "
        r"super-linear (note the log scale), reaching machine precision within a few "
        r"sweeps; the converged diagonal reproduces the exact eigenvalues "
        r"$2,\,2\pm\sqrt2$, matching the module's `eig_symmetric`.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
