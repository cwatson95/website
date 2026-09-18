"""MA-01 figures -- the scalar triple product as a volume, and operations lifted
to vector-valued functions.

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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from vector_algebra import (                       # noqa: E402
    dot, cross, scalar_triple, box_volume, norm,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _add(*vs):
    """Componentwise sum of 3-vectors."""
    return tuple(sum(v[i] for v in vs) for i in range(3))


def main():
    caps = {}

    # Fig 1 -- scalar triple product = signed volume of the parallelepiped a,b,c.
    a = (2.0, 0.35, 0.25)
    b = (0.45, 1.8, 0.30)
    c = (0.35, 0.55, 1.6)
    V = box_volume(a, b, c)               # |a.(b x c)|  via the module
    Vsigned = scalar_triple(a, b, c)      # a.(b x c)    (signed)
    base_area = norm(cross(b, c))         # |b x c| = area of the b,c parallelogram

    O = (0.0, 0.0, 0.0)
    A, B, C = a, b, c
    AB, AC, BC = _add(a, b), _add(a, c), _add(b, c)
    ABC = _add(a, b, c)
    faces = [
        [O, A, AB, B], [C, AC, ABC, BC],     # a,b faces
        [O, A, AC, C], [B, AB, ABC, BC],     # a,c faces
        [A, AB, ABC, AC],                    # far b,c face
    ]
    base_face = [O, B, BC, C]                # near b,c face -> highlighted base

    fig = plt.figure(figsize=(6.2, 3.7))
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(faces, facecolor=INK, edgecolor=INK,
                                         alpha=0.10, linewidths=1.0))
    ax.add_collection3d(Poly3DCollection([base_face], facecolor=ALT, edgecolor=ALT,
                                         alpha=0.28, linewidths=1.2))
    for vec, col, lab in ((a, INK, "a"), (b, FLOW, "b"), (c, STEEL, "c")):
        ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=col, lw=2.4,
                  arrow_length_ratio=0.10)
        ax.text(vec[0] * 1.06, vec[1] * 1.06, vec[2] * 1.06, lab,
                color=col, fontsize=13, fontweight="bold")
    ax.text(*[BC[i] * 0.5 for i in range(3)],
            "base $b{,}c$", color=ALT, fontsize=10)

    ax.set_xlim(0, 2.4); ax.set_ylim(0, 2.4); ax.set_zlim(0, 2.0)
    ax.set_box_aspect((2.4, 2.4, 2.0))
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.view_init(elev=20, azim=33)
    ax.set_title(r"Scalar triple product: $V=|a\cdot(b\times c)|=$ "
                 + f"{V:.3f}\n"
                 + r"(base area $|b\times c|=$ " + f"{base_area:.3f}"
                 + r"$,\ $ height $=V/|b\times c|$)", fontsize=11)
    _save(fig, "fig1_triple_product_volume.svg")
    caps["fig1_triple_product_volume.svg"] = (
        r"The scalar triple product as a signed volume. Vectors $a,b,c$ span a "
        r"parallelepiped and $a\cdot(b\times c)=\det[a\,b\,c]$ equals its (signed) "
        r"volume, computed here by the module's `scalar_triple` / `box_volume` "
        r"($V=" + f"{V:.3f}" + r"$). The shaded base on $b,c$ has area "
        r"$|b\times c|=" + f"{base_area:.3f}" + r"$, so $V=$ base area $\times$ "
        r"height; the product vanishes exactly when $a,b,c$ are coplanar.")

    # Fig 2 -- lift: with r(t),v(t) callables, dot/norm/cross RETURN functions.
    r = lambda t: (math.cos(t), math.sin(t), t)        # a helix
    v = lambda t: (-math.sin(t), math.cos(t), 1.0)     # r'(t)
    rv = dot(r, v)                # FUNCTION  t |-> r(t).v(t)        (= t)
    speed = norm(v)              # FUNCTION  t |-> |v(t)|           (= sqrt 2)
    Lmag = norm(cross(r, v))     # FUNCTION  t |-> |r(t) x v(t)|    (= sqrt(2+t^2))

    t = np.linspace(0.0, 4.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, [rv(tt) for tt in t], color=INK, lw=2, label=r"$r\cdot v=t$")
    ax.plot(t, [speed(tt) for tt in t], color=FLOW, lw=2, label=r"$|v|=\sqrt{2}$")
    ax.plot(t, [Lmag(tt) for tt in t], color=ALT, lw=2,
            label=r"$|r\times v|=\sqrt{2+t^2}$")
    ax.set_xlim(0, 4); ax.set_ylim(0, 4.6)
    ax.set_xlabel("parameter $t$"); ax.set_ylabel("value")
    ax.set_title(r"Lifted operations on a helix $r(t)=(\cos t,\sin t,t)$, "
                 r"$v=r'$")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_lifted_functions.svg")
    caps["fig2_lifted_functions.svg"] = (
        r"Operations lifted to vector-valued functions. For the helix "
        r"$r(t)=(\cos t,\sin t,t)$ and $v=r'$, the module's `dot`, `norm`, `cross` "
        r"each return a function of $t$: $r\cdot v=t$, the speed $|v|=\sqrt2$, and "
        r"the specific angular momentum magnitude $|r\times v|=\sqrt{2+t^2}$ -- the "
        r"single `lift` decorator that seeds kinematics and angular momentum.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
