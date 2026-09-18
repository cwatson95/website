"""Module 5.2 figures — superheated-vapour isobars from Table A-4, and the double
interpolation that reaches a state sitting between four table entries.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import collections
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
from vapor_tables import (                        # noqa: E402
    load_A4, superheated, pressures, enthalpy, linear_interp,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    rows = load_A4()

    # Fig 1 — the isobars.  Each pressure block of A-4 is one curve of h against
    # T; the markers are the actual tabulated entries, so the spacing shows how
    # coarse the table really is.  The saturated-vapour states (sat flag) trace
    # the dome edge the blocks start from -- drawn in grey as a reference line,
    # not as a fourth series.
    by_p = collections.defaultdict(list)
    for r in rows:
        by_p[float(r["P_bar"])].append((float(r["T_C"]), float(r["h_kJkg"]),
                                        int(r["sat"])))
    sat_pts = sorted((t, h) for p in by_p for (t, h, s) in by_p[p] if s)

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot([t for t, _ in sat_pts], [h for _, h in sat_pts], color="0.5",
            lw=1.6, ls="-.", label=r"saturated vapour $h_g$ (dome edge)")
    for p, c, ls in ((1.0, INK, "-"), (10.0, FLOW, "--"), (40.0, ALT, ":")):
        pts = sorted(by_p[p])
        T = [t for t, _, _ in pts]
        h = [superheated(p, t, "h") for t in T]
        ax.plot(T, h, color=c, lw=2.1, ls=ls, label=r"$p=%g$ bar" % p)
        ax.plot(T, h, ls="none", marker="o", ms=4.2, mfc="white", mec=c, mew=1.2)
    ax.set_xlim(80, 620)
    ax.set_xlabel(r"temperature $T$ ($^\circ$C)")
    ax.set_ylabel(r"specific enthalpy $h$ (kJ/kg)")
    ax.set_title(r"Superheated-vapour isobars (Table A-4)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_superheat_isobars.svg")
    caps["fig1_superheat_isobars.svg"] = (
        r"Three pressure blocks of Table A-4 (load_A4, superheated), with a "
        r"marker at every tabulated entry. Each isobar begins on the "
        r"saturated-vapour line and climbs almost linearly as the steam is "
        r"superheated — the slope is $c_p$ — while raising the pressure at fixed "
        r"temperature LOWERS the enthalpy, which is why the 40 bar curve sits "
        r"beneath the 1 bar one. The markers also show the practical problem: "
        r"entries are 40 $^\circ$C apart, so almost every real state falls "
        r"between them and has to be interpolated. The table carries "
        + "%d" % len(pressures()) + r" pressure blocks in all.")

    # Fig 2 — the double interpolation, drawn.  A state at 12 bar / 260 C sits
    # inside a rectangle of four tabulated entries: interpolate in T along both
    # bracketing isobars, then in p between those two results.
    p_lo, p_hi, T_lo, T_hi = 10.0, 15.0, 240.0, 280.0
    p_q, T_q = 12.0, 260.0
    corners = {(p, t): superheated(p, t, "h")
               for p in (p_lo, p_hi) for t in (T_lo, T_hi)}
    h_lo = linear_interp(T_q, T_lo, T_hi, corners[(p_lo, T_lo)], corners[(p_lo, T_hi)])
    h_hi = linear_interp(T_q, T_lo, T_hi, corners[(p_hi, T_lo)], corners[(p_hi, T_hi)])
    h_q = linear_interp(p_q, p_lo, p_hi, h_lo, h_hi)
    h_direct = superheated(p_q, T_q, "h")

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for (p, t), h in corners.items():
        ax.plot([t], [p], marker="s", ms=9, mfc="white", mec=INK, mew=1.8,
                ls="none")
        ax.annotate("%.1f" % h, xy=(t, p), xytext=(t, p + 0.55), fontsize=9,
                    color=INK, ha="center")
    ax.plot([T_q, T_q], [p_lo, p_hi], color="0.75", lw=1.0, ls=":")
    ax.plot([T_lo, T_hi], [p_lo, p_lo], color="0.75", lw=1.0, ls=":")
    ax.plot([T_lo, T_hi], [p_hi, p_hi], color="0.75", lw=1.0, ls=":")
    for p, h in ((p_lo, h_lo), (p_hi, h_hi)):
        ax.plot([T_q], [p], marker="o", ms=8, mfc="white", mec=FLOW, mew=1.8,
                ls="none")
        ax.annotate("%.1f" % h, xy=(T_q, p), xytext=(T_q + 3.5, p - 0.25),
                    fontsize=9, color=FLOW)
    ax.plot([T_q], [p_q], marker="*", ms=17, mfc=ALT, mec=ALT, ls="none")
    ax.annotate(r"$h=%.1f$ kJ/kg" % h_q, xy=(T_q, p_q),
                xytext=(T_q - 5, p_q + 1.1), fontsize=10.5, color=ALT,
                ha="right")
    ax.set_xlim(232, 292)
    ax.set_ylim(8.6, 16.6)
    ax.set_xlabel(r"temperature $T$ ($^\circ$C)")
    ax.set_ylabel(r"pressure $p$ (bar)")
    ax.set_title(r"Double interpolation to 12 bar, 260 $^\circ$C")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_double_interpolation.svg")
    caps["fig2_double_interpolation.svg"] = (
        r"How superheated() reaches a state the table does not contain. The "
        r"target 12 bar / 260 $^\circ$C lies inside a rectangle of four A-4 "
        r"entries (squares). Interpolating first in temperature along each "
        r"bracketing isobar gives the two circled values, and interpolating "
        r"between those in pressure gives "
        + "%.1f" % h_q + r" kJ/kg (star) — matching the module's own "
        r"superheated(12, 260, 'h') to "
        + "%.2g" % abs(h_q - h_direct) + r" kJ/kg. The order does not matter; "
        r"bilinear interpolation is symmetric. enthalpy() supplies the "
        r"independent check $h=u+pv$ on any entry.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
