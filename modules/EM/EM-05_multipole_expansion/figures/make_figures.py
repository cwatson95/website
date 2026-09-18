"""EM-05 figures -- the multipole expansion: angular patterns and 1/r^(l+1) falloff.

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
from multipole import dipole_moment, dipole_potential, multipole_potential  # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    q, a = 1e-9, 0.02
    mono = [(q, (0.0, 0.0, 0.0))]                                  # leading: monopole 1/r
    dip = [(q, (0.0, 0.0, a / 2)), (-q, (0.0, 0.0, -a / 2))]       # leading: dipole 1/r^2
    quad = [(q, (0.0, 0.0, a)), (-2 * q, (0.0, 0.0, 0.0)),
            (q, (0.0, 0.0, -a))]                                   # leading: quadrupole 1/r^3
    p = dipole_moment(dip)

    Vmono = multipole_potential(mono, lmax=0)
    Vdip = dipole_potential(p)
    Vquad = multipole_potential(quad, lmax=2)     # monopole, dipole moments vanish -> pure l=2

    # Fig 1 -- angular pattern at fixed radius: P_0, P_1, P_2 lobes (polar plot).
    r0 = 1.0
    th = np.linspace(0.0, 2.0 * np.pi, 361)

    def pattern(Vfun):
        v = np.array([Vfun(r0 * np.sin(t), 0.0, r0 * np.cos(t)) for t in th])
        return np.abs(v) / np.max(np.abs(v))

    fig, ax = plt.subplots(figsize=(6.2, 3.5), subplot_kw={"projection": "polar"})
    ax.plot(th, pattern(Vmono), color=INK, lw=2, label=r"monopole $P_0$")
    ax.plot(th, pattern(Vdip), color=FLOW, lw=2, label=r"dipole $P_1=\cos\theta$")
    ax.plot(th, pattern(Vquad), color=ALT, lw=2,
            label=r"quadrupole $P_2=\frac{1}{2}(3\cos^2\theta-1)$")
    ax.set_rticks([0.5, 1.0]); ax.set_title(r"Angular pattern $|V(\theta)|$ at fixed $r$", pad=14)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), frameon=False, ncol=1)
    _save(fig, "fig1_angular_pattern.svg")
    caps["fig1_angular_pattern.svg"] = (
        "Normalized angular shape of each multipole potential at fixed radius (theta from "
        "the symmetry axis): the monopole is isotropic, the dipole has the cos(theta) "
        "two-lobe pattern, and the linear quadrupole shows the P2 four-lobe pattern, all "
        "evaluated from the module's potential functions.")

    # Fig 2 -- radial falloff on the axis: each term goes as 1/r^(l+1).
    r = np.logspace(np.log10(2.0 * a), np.log10(300.0 * a), 140)
    fm = np.abs([Vmono(0.0, 0.0, z) for z in r])
    fd = np.abs([Vdip(0.0, 0.0, z) for z in r])
    fqd = np.abs([Vquad(0.0, 0.0, z) for z in r])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.loglog(r / a, fm, color=INK, lw=2.2, label=r"monopole $\propto r^{-1}$")
    ax.loglog(r / a, fd, color=FLOW, lw=2.2, label=r"dipole $\propto r^{-2}$")
    ax.loglog(r / a, fqd, color=ALT, lw=2.2, label=r"quadrupole $\propto r^{-3}$")
    ax.set_xlabel(r"$r/a$  (distance, source size $a$)")
    ax.set_ylabel(r"$|V|$  (volts)")
    ax.set_title(r"Successive multipoles fall off as $r^{-(l+1)}$")
    ax.legend(loc="lower left", frameon=False)
    _save(fig, "fig2_radial_falloff.svg")
    caps["fig2_radial_falloff.svg"] = (
        "On-axis magnitude of the monopole, dipole, and quadrupole potentials versus "
        "distance (log-log). The straight lines have slopes -1, -2, -3, so each higher "
        "multipole decays one extra power of r faster -- the 1/r^(l+1) hierarchy that lets "
        "the nearest non-zero moment dominate far away.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
