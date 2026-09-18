"""QM-05 figures — Hermitian observables have real spectra, and the canonical
commutator [x,p] in the harmonic-oscillator number basis (with its honest
finite-dimension truncation artifact).

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
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
from formalism import (                            # noqa: E402
    random_hermitian, random_matrix, spectral_decomposition,
    canonical_commutator,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — why observables are HERMITIAN operators: their eigenvalues are real.
    # The eigenvalues of a random Hermitian matrix (spectral_decomposition) lie
    # exactly on the real axis; those of a generic (non-Hermitian) random_matrix
    # scatter across the complex plane.
    n = 24
    wH, _ = spectral_decomposition(random_hermitian(n, seed=3))   # real, ascending
    wG = np.linalg.eigvals(random_matrix(n, seed=7))              # generic, complex

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axhline(0.0, color="#aaaaaa", lw=0.7)
    ax.scatter(wG.real, wG.imag, s=34, color=ALT, alpha=0.85,
               edgecolor="white", linewidth=0.5,
               label="generic matrix:  complex eigenvalues")
    ax.scatter(wH, np.zeros_like(wH), s=42, color=INK, marker="D",
               edgecolor="white", linewidth=0.5,
               label=r"Hermitian observable:  real ($\mathrm{Im}\,\lambda=0$)")
    ax.set_xlabel(r"$\mathrm{Re}\,\lambda$")
    ax.set_ylabel(r"$\mathrm{Im}\,\lambda$")
    ax.set_title(r"Hermitian $\Rightarrow$ real spectrum: the spectral theorem")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_hermitian_real_spectrum.svg")
    caps["fig1_hermitian_real_spectrum.svg"] = (
        "Why observables are represented by Hermitian operators: their eigenvalues "
        "are real. The blue diamonds are the eigenvalues of a random Hermitian "
        "matrix (random_hermitian -> spectral_decomposition) -- every one sits "
        "exactly on the real axis (Im=0), so each is a legitimate measured value. A "
        "generic non-Hermitian random_matrix instead has eigenvalues scattered "
        "across the complex plane (purple). Real spectrum = the spectral theorem.")

    # Fig 2 — the canonical commutator [x,p] built from ladder operators in the
    # N-level number basis (canonical_commutator).  Shown as Im[x,p]: it equals
    # +1 (= hbar) all along the interior diagonal -- i.e. [x,p]=i hbar -- and is
    # exactly 0 off-diagonal, but the bottom-right corner reads -(N-1), the
    # unavoidable truncation artifact of a finite-dimensional representation.
    N = 8
    M = canonical_commutator(N).imag               # [x,p] = i * M, with hbar = 1
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    vmax = N - 1
    im = ax.imshow(M, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    for i in range(N):
        v = M[i, i]
        ax.text(i, i, f"{v:.0f}", ha="center", va="center", fontsize=9,
                color="white" if abs(v) > 3 else "#222222")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label(r"$\mathrm{Im}\,[\hat x,\hat p]$")
    ax.set_xticks(range(N)); ax.set_yticks(range(N))
    ax.set_xlabel(r"number state $n$")
    ax.set_ylabel(r"number state $n$")
    ax.set_title(r"$[\hat x,\hat p]=i\hbar$ on the interior;  corner $=-(N{-}1)$ artifact")
    _save(fig, "fig2_canonical_commutator.svg")
    caps["fig2_canonical_commutator.svg"] = (
        "The canonical commutator [x,p] assembled from ladder operators in the N=8 "
        "number basis (canonical_commutator), displayed as Im[x,p]. It equals +1 "
        "(= hbar in natural units) all along the interior diagonal -- i.e. "
        "[x,p]=i hbar -- and is exactly 0 off-diagonal. The single bottom-right "
        "corner reads -(N-1)=-7: the honest truncation artifact. No finite matrices "
        "can satisfy [x,p]=i hbar everywhere, because every commutator is traceless "
        "while tr(i hbar I) is not.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
