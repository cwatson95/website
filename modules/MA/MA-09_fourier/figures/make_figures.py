"""MA-09 figures — square-wave Fourier partial sums (Gibbs) and a DFT spectrum.

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
from fourier import (                              # noqa: E402
    dft, dft_freqs, fourier_series_coeffs, series_value,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Fourier partial sums of a square wave: the Gibbs phenomenon.
    # Coefficients from the module's fourier_series_coeffs (b_n = 4/(n*pi), odd n);
    # the truncated series is evaluated by series_value.
    sq = lambda t: 1.0 if (t % 1.0) < 0.5 else -1.0          # period P = 1
    xs = np.linspace(0.0, 2.0, 2000)
    ref = np.array([sq(t) for t in xs])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xs, ref, color="#bbbbbb", lw=1.0, label="square wave")
    overshoot = 0.0
    for M, col in [(3, STEEL), (11, ALT), (51, FLOW)]:
        a0, a, b = fourier_series_coeffs(sq, 1.0, M)
        S = np.array([series_value(a0, a, b, 1.0, t) for t in xs])
        overshoot = max(overshoot, float(S.max()))
        ax.plot(xs, S, color=col, lw=1.6, label=fr"$S_{{{M}}}$  ({M} terms)")
    ax.axhline(1.0, color="#dddddd", lw=0.8, ls=":")
    ax.set_xlim(0.0, 2.0); ax.set_ylim(-1.5, 1.85)
    ax.set_xlabel("$x$  (periods)"); ax.set_ylabel("partial sum $S_M(x)$")
    ax.set_title(r"Fourier partial sums of a square wave: $b_n=\frac{4}{n\pi}$ (odd $n$)")
    ax.legend(loc="upper center", frameon=False, fontsize=9, ncol=2)
    _save(fig, "fig1_square_gibbs.svg")
    caps["fig1_square_gibbs.svg"] = (
        "Truncated Fourier series $S_M$ of a square wave, coefficients from "
        "fourier_series_coeffs and summed by series_value (only odd harmonics, "
        "$b_n=4/n\\pi$). Adding terms ($M=3,11,51$) sharpens the edges but the "
        f"overshoot at each jump persists at ~9% of the jump height (here $S_{{51}}$ peaks "
        f"at {overshoot:.3f}, above the true $1$) — the Gibbs phenomenon.")

    # Fig 2 — a two-tone signal and its DFT amplitude spectrum.
    # X = dft(x); the bin frequencies come from dft_freqs. With dt = 1/N the
    # frequency axis is integer "cycles per window", so peaks land on the inputs.
    N = 64
    n = np.arange(N)
    f1, f2, A1, A2 = 4, 11, 1.0, 0.5
    sig = A1 * np.cos(2 * np.pi * f1 * n / N) + A2 * np.cos(2 * np.pi * f2 * n / N)
    X = dft(list(sig))
    freqs = np.array(dft_freqs(N, 1.0 / N))                  # integer cycles/window
    amp = np.array([2.0 * abs(v) / N for v in X])            # amplitude spectrum
    order = np.argsort(freqs)
    fr, am = freqs[order], amp[order]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.6))
    ax1.plot(n, sig, color=INK, lw=1.2, marker="o", ms=2.6)
    ax1.axhline(0, color="#cccccc", lw=0.6)
    ax1.set_xlim(0, N - 1)
    ax1.set_xlabel("sample $n$"); ax1.set_ylabel("$x_n$")
    ax1.set_title(r"Two-tone signal $x_n$:  $4$ and $11$ cycles per window")
    markerline, stemlines, baseline = ax2.stem(fr, am, basefmt=" ")
    plt.setp(stemlines, color=STEEL, lw=1.5)
    plt.setp(markerline, color=INK, ms=4)
    for fpk, apk in [(f1, A1), (f2, A2)]:
        ax2.annotate(f"$\\pm{fpk}$", xy=(fpk, apk), xytext=(fpk + 1.5, apk + 0.06),
                     fontsize=9, color=FLOW)
    ax2.axhline(0, color="#cccccc", lw=0.6)
    ax2.set_xlim(-N // 2, N // 2)
    ax2.set_xticks([-11, -4, 0, 4, 11])
    ax2.set_xlabel("frequency $k$  (cycles per window)")
    ax2.set_ylabel(r"amplitude  $2|X_k|/N$")
    ax2.set_title("Its DFT spectrum: peaks at the input frequencies")
    fig.tight_layout()
    _save(fig, "fig2_dft_spectrum.svg")
    caps["fig2_dft_spectrum.svg"] = (
        "A two-tone signal (top) and its discrete Fourier transform from dft, with "
        "bin frequencies from dft_freqs (bottom). The amplitude spectrum $2|X_k|/N$ "
        "shows clean lines at $\\pm4$ and $\\pm11$ cycles per window with heights $1$ "
        "and $\\tfrac12$ — the real signal's energy splits between positive and "
        "negative frequencies, recovering the exact amplitudes.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
