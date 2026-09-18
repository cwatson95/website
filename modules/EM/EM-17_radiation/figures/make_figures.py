"""EM-17 figures -- the dipole radiation pattern and the omega^4 power law.

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
from radiation import (                            # noqa: E402
    dipole_angular_power, dipole_radiated_power, total_power_from_pattern,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    p0, omega = 1e-11, 2.0 * np.pi * 1e8           # dipole amplitude, f = 100 MHz

    # Fig 1 -- polar pattern dP/dOmega ~ sin^2(theta): the doughnut lobes.
    th = np.linspace(0.0, 2.0 * np.pi, 361)
    dP = np.array([dipole_angular_power(t, p0, omega) for t in th])
    dP_norm = dP / dP.max()
    fig = plt.figure(figsize=(6.2, 3.7))
    ax = fig.add_subplot(projection="polar")
    ax.plot(th, dP_norm, color=INK, lw=2.2)
    ax.fill(th, dP_norm, color=INK, alpha=0.12)
    ax.set_theta_zero_location("N")                # dipole axis (theta=0) points up
    ax.set_theta_direction(-1)
    ax.set_rticks([0.25, 0.5, 0.75, 1.0])
    ax.set_title(r"Dipole pattern  $\frac{dP}{d\Omega}\propto\sin^{2}\theta$", pad=14)
    _save(fig, "fig1_dipole_pattern.svg")
    caps["fig1_dipole_pattern.svg"] = (
        "Angular distribution of electric-dipole radiation from dipole_angular_power, "
        "normalized to its peak. The two lobes are the cross-section of the doughnut "
        "pattern: power is maximal broadside (theta=90 deg) and vanishes along the "
        "dipole axis (theta=0,180 deg).")

    # Fig 2 -- total radiated power ~ omega^4 (closed form vs pattern integral).
    omegas = 2.0 * np.pi * np.logspace(7, 9, 24)   # 10 MHz .. 1 GHz
    P_closed = np.array([dipole_radiated_power(p0, w) for w in omegas])
    P_int = np.array([total_power_from_pattern(p0, w) for w in omegas])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.loglog(omegas, P_closed, color=INK, lw=2.4,
              label=r"$\langle P\rangle=\frac{\mu_0 p_0^{2}\omega^{4}}{12\pi c}$")
    ax.loglog(omegas, P_int, color=FLOW, lw=0.0, marker="o", ms=4.5,
              label=r"$\int \frac{dP}{d\Omega}\,d\Omega$  (numeric)")
    ax.set_xlabel(r"angular frequency $\omega$  [rad/s]")
    ax.set_ylabel(r"total power  [W]")
    ax.set_title(r"Dipole power scales as $\omega^{4}$")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_power_law.svg")
    caps["fig2_power_law.svg"] = (
        "Total radiated power versus frequency on log-log axes. The closed-form "
        "dipole_radiated_power (line) and the sphere integral of the angular pattern "
        "total_power_from_pattern (dots) agree, and the slope of 4 shows the strong "
        "omega^{4} dependence -- why higher frequencies radiate far more efficiently.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
