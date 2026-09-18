"""EM-04 figures -- boundary-value problems: the image charge and the slot.

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
from boundary_value import (                        # noqa: E402
    image_potential_plane, image_field_plane, slot_potential_closed,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- method of images: q above a grounded plane z=0.
    q, d = 1e-9, 1.0
    V = image_potential_plane(q, d)                 # valid in z > 0
    Efield = image_field_plane(q, d)
    xs = np.linspace(-2.6, 2.6, 100)
    zs = np.linspace(-1.4, 3.0, 96)
    Vg = np.full((zs.size, xs.size), np.nan)
    for j, z in enumerate(zs):
        if z <= 0.0:
            continue                                # conductor interior: not physical
        for i, x in enumerate(xs):
            Vg[j, i] = V(x, 0.0, z)
    vlim = np.nanpercentile(np.abs(Vg), 92)
    Vc = np.clip(Vg, 0.0, vlim)

    xq = np.linspace(-2.3, 2.3, 17)
    zq = np.linspace(0.18, 2.7, 11)
    Ex = np.zeros((zq.size, xq.size)); Ez = np.zeros((zq.size, xq.size))
    for j, z in enumerate(zq):
        for i, x in enumerate(xq):
            ex, _, ez = Efield(x, 0.0, z)
            n = np.hypot(ex, ez) or 1.0
            Ex[j, i], Ez[j, i] = ex / n, ez / n

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    cmap = plt.get_cmap("magma").copy(); cmap.set_bad(alpha=0.0)
    im = ax.imshow(np.ma.masked_invalid(Vc), extent=[xs[0], xs[-1], zs[0], zs[-1]],
                   origin="lower", cmap=cmap, vmin=0.0, vmax=vlim, aspect="equal",
                   interpolation="bilinear")            # raster fill -> compact SVG
    ax.contour(xs, zs, Vc, levels=np.linspace(0.05 * vlim, vlim, 9),
               colors="white", linewidths=0.5, alpha=0.7)
    ax.quiver(xq, zq, Ex, Ez, color="white", scale=24, width=0.004, alpha=0.9)
    ax.axhspan(zs[0], 0.0, color="#cfcfcf")          # grounded conductor
    ax.axhline(0.0, color="#444444", lw=2.0)
    ax.plot(0, d, "o", color=FLOW, ms=11, mec="white", label=r"real $+q$")
    ax.plot(0, -d, "o", mfc="none", mec=STEEL, mew=2.0, ms=11, label=r"image $-q$")
    ax.text(-2.4, -0.95, "grounded conductor  $V=0$", fontsize=9, color="#333333")
    ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(zs[0], zs[-1]); ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$z$")
    ax.set_title("Method of images: charge above a grounded plane")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_image_charge.svg")
    caps["fig1_image_charge.svg"] = (
        "Potential of a point charge a height d above a grounded plane, from "
        "image_potential_plane: the real +q plus a fictitious image -q at -d reproduce V=0 "
        "on the conductor. White arrows (E from image_field_plane) strike the plane at "
        "right angles, as they must on an equipotential surface.")

    # Fig 2 -- separation of variables: the semi-infinite slot (closed form).
    V0, a = 10.0, 1.0
    Vc2 = slot_potential_closed(V0, a)
    xg = np.linspace(0.0, 1.7, 120)
    yg = np.linspace(0.0, a, 80)
    Vs = np.array([[Vc2(x, y) for x in xg] for y in yg])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    im = ax.imshow(Vs, extent=[xg[0], xg[-1], yg[0], yg[-1]], origin="lower",
                   cmap="viridis", vmin=0.0, vmax=V0, aspect="auto",
                   interpolation="bilinear")            # raster fill -> compact SVG
    ax.contour(xg, yg, Vs, levels=np.linspace(1.0, 9.0, 9),
               colors="white", linewidths=0.5, alpha=0.7)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Separation of variables: semi-infinite slot")
    ax.text(0.02, 0.5, r"$V_0$", color="white", fontsize=12, rotation=90, va="center")
    ax.text(0.8, 1.02, r"$V=0$ plate", fontsize=9, ha="center")
    ax.text(0.8, -0.07, r"$V=0$ plate", fontsize=9, ha="center")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("$V$  (volts)")
    _save(fig, "fig2_slot_separation.svg")
    caps["fig2_slot_separation.svg"] = (
        "Closed-form Fourier solution of Laplace's equation in a semi-infinite slot "
        "(slot_potential_closed): grounded plates at y=0 and y=a, the end strip held at V0, "
        "and V decaying to zero down the channel. White curves are equipotentials of the "
        "unique boundary-value solution.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
