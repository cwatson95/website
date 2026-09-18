"""PK-01 figures — phase-space free streaming (Liouville) & plasma coupling Lambda.

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
from kinetic_description import (                  # noqa: E402
    free_stream, vlasov_residual, plasma_parameter,
    debye_length, plasma_frequency, thermal_speed,
    E_CHARGE, K_B, M_E,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # ---- Fig 1 — phase-space free streaming: Liouville shear & filamentation.
    # The module's own free_stream advects f(x,v) -> f(x - v t, v) (the exact
    # characteristic of df/dt + v df/dx = 0).  A density ripple in x phase-mixes
    # into fine diagonal velocity structure, yet f is only transported: the
    # velocity marginal INT f dx is frozen and the Vlasov residual ~ 0.
    Nx, Nv = 256, 256
    L = 2.0 * np.pi
    x = np.linspace(0.0, L, Nx, endpoint=False)
    v = np.linspace(-5.0, 5.0, Nv)                 # natural units, v_T = 1
    M = np.exp(-v ** 2 / 2.0)                       # Maxwellian background in v
    g = 1.0 + 0.5 * np.cos(x)                       # density ripple in x
    f0 = M[:, None] * g[None, :]                    # (Nv, Nx) phase-space density
    t_final = 2.0
    fT = free_stream(f0, x, v, t_final)             # one exact spectral step

    # quantify Liouville: residual of df/dt + v df/dx = 0 over a small step
    dt_small = 1.0e-3
    f1 = free_stream(f0, x, v, dt_small)
    res = vlasov_residual(f0, f1, x, v, dt_small)
    dx = x[1] - x[0]
    stream = v[:, None] * (np.roll(f0, -1, 1) - np.roll(f0, 1, 1)) / (2.0 * dx)
    ratio = np.max(np.abs(res)) / np.max(np.abs(stream))
    marg_err = np.max(np.abs(f0.sum(1) - fT.sum(1))) / f0.sum(1).max()

    extent = [0.0, 2.0, v.min(), v.max()]          # x in units of pi
    vmax = float(f0.max())
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6.9, 3.2), sharey=True)
    for ax, f, ttl in ((ax0, f0, r"$t=0$"), (ax1, fT, fr"$t={t_final:.0f}/\omega$")):
        im = ax.imshow(f, origin="lower", aspect="auto", extent=extent,
                       cmap="magma", vmin=0.0, vmax=vmax, rasterized=True)
        ax.set_title(ttl)
        ax.set_xlabel(r"position $x\;/\;\pi$")
        ax.set_xticks([0.0, 1.0, 2.0])
    ax0.set_ylabel(r"velocity $v\;/\;v_T$")
    cb = fig.colorbar(im, ax=(ax0, ax1), pad=0.02, fraction=0.046)
    cb.set_label(r"$f(x,v)$")
    fig.suptitle(r"Free streaming shears phase space: $f(x{-}vt,\,v)$, "
                 r"$df/dt=0$", y=1.00)
    _save(fig, "fig1_phase_space_streaming.svg")
    caps["fig1_phase_space_streaming.svg"] = (
        r"Collisionless phase mixing from the module's free_stream: a density "
        r"ripple $f=e^{-v^2/2}(1+\tfrac12\cos x)$ (left) is advected to "
        r"$f(x-vt,v)$ at $t=2/\omega$ (right). Fast and slow velocities shear at "
        r"different rates, winding the ripple into fine diagonal filaments — yet "
        r"$f$ is merely transported along orbits (Liouville, $df/dt=0$): the "
        r"velocity marginal $\int f\,dx$ is frozen to "
        + ("%.0e" % marg_err) +
        r" and the Vlasov residual $\partial_t f+v\partial_x f$ is "
        + ("%.0e" % ratio) +
        r" of the streaming term.")

    # ---- Fig 2 — plasma coupling phase diagram: Lambda = n lambda_D^3.
    # The defining inequality of a plasma.  Lambda >> 1 (many particles per Debye
    # sphere) -> weak coupling, collective behaviour, mean-field Vlasov holds;
    # Lambda < 1 -> strongly coupled.  Computed straight from plasma_parameter.
    n_grid = np.logspace(14.0, 26.0, 260)          # density [m^-3]
    TeV_grid = np.logspace(-2.0, 4.0, 220)         # temperature [eV]
    NN, TeV = np.meshgrid(n_grid, TeV_grid)
    TT = TeV * E_CHARGE / K_B                       # eV -> kelvin
    Lam = plasma_parameter(NN, TT)                  # (T, n) grid of Lambda

    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    pcm = ax.pcolormesh(NN, TeV, np.log10(Lam), cmap="viridis",
                        shading="auto", rasterized=True)
    cs = ax.contour(NN, TeV, Lam, levels=[1.0], colors=[FLOW], linewidths=2.0)
    ax.clabel(cs, fmt={1.0: r"$\Lambda=1$"}, fontsize=9)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"number density $n\;[\mathrm{m^{-3}}]$")
    ax.set_ylabel(r"temperature $T\;[\mathrm{eV}]$")
    ax.set_title(r"Plasma coupling: $\Lambda=n\lambda_D^3$ "
                 r"(particles per Debye sphere)")
    cb = fig.colorbar(pcm, ax=ax, pad=0.02)
    cb.set_label(r"$\log_{10}\Lambda$")
    ax.text(3e15, 2e3, "collective\n(weak coupling,\nVlasov holds)",
            color="white", fontsize=8.5, ha="left", va="center")
    ax.text(3e24, 3e-2, "strongly\ncoupled", color="white",
            fontsize=8.5, ha="center", va="center")
    # representative plasma from the module demo: n=1e18 m^-3, T=1 eV
    n0, T0eV = 1.0e18, 1.0
    Lam0 = plasma_parameter(n0, T0eV * E_CHARGE / K_B)
    ax.plot(n0, T0eV, marker="*", ms=14, color="white",
            markeredgecolor=INK, label=fr"$n=10^{{18}},\,T=1$ eV: $\Lambda={Lam0:.0f}$")
    ax.legend(loc="lower left", frameon=False, fontsize=8.5, labelcolor="white")
    _save(fig, "fig2_plasma_coupling.svg")
    caps["fig2_plasma_coupling.svg"] = (
        r"Plasma coupling parameter $\Lambda=n\lambda_D^3$ over the density–"
        r"temperature plane, evaluated by the module's plasma_parameter / "
        r"debye_length. $\Lambda$ counts particles in a Debye sphere: above the "
        r"$\Lambda=1$ line (orange) the plasma is weakly coupled and collective, "
        r"so screening is statistically meaningful and the mean-field Vlasov "
        r"equation holds ($\nu_{ei}/\omega_p\sim\ln\Lambda/\Lambda\ll1$); below "
        r"it is strongly coupled. The star marks the demo plasma "
        r"($n=10^{18}\,\mathrm{m^{-3}}$, $T=1$ eV, $\Lambda\approx411$). Since "
        r"$\Lambda\propto T^{3/2}/\sqrt n$, hotter and thinner plasmas are more ideal.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
