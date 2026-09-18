"""PK-02 figures — MHD characteristic speeds & the 0th-moment continuity law.

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
from fluid_mhd import (                            # noqa: E402
    sound_speed, alfven_speed, fast_magnetosonic_speed,
    plasma_beta, continuity_residual,
    K_B, M_P, MU0,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the three MHD speeds vs B for a fixed plasma, with plasma beta on a
    # twin axis.  Speeds from sound_speed/alfven_speed/fast_magnetosonic_speed,
    # beta from plasma_beta — all the module's own functions.  As B grows the gas
    # gives way to the magnetic field: v_fast = sqrt(c_s^2+v_A^2) follows c_s where
    # beta>1 (gas-pressure dominated) and merges onto v_A where beta<1 (magnetic).
    n, T, gamma = 1.0e19, 1.16e6, 5.0 / 3.0          # ~1e19 /m^3, ~100 eV, monatomic
    rho = n * M_P
    p = n * K_B * T
    B = np.logspace(-3.0, 0.5, 400)                  # 1 mT .. ~3 T
    c_s = sound_speed(gamma, p, rho)                 # scalar (B-independent)
    v_A = alfven_speed(B, rho)
    v_f = fast_magnetosonic_speed(c_s, v_A)
    beta = plasma_beta(n, T, B)
    B_cross = c_s * np.sqrt(MU0 * rho)               # B where v_A = c_s  (beta = 2/gamma)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.set_xscale("log"); ax.set_yscale("log")
    l_cs = ax.axhline(c_s, color=INK, lw=2, ls="--",
                      label=r"$c_s=\sqrt{\gamma p/\rho}$ (sound)")
    (l_va,) = ax.plot(B, v_A, color=FLOW, lw=2,
                      label=r"$v_A=B/\sqrt{\mu_0\rho}$ (Alfven)")
    (l_vf,) = ax.plot(B, v_f, color=ALT, lw=2.4,
                      label=r"$v_{\mathrm{fast}}=\sqrt{c_s^2+v_A^2}$")
    ax.axvline(B_cross, color="#aaaaaa", lw=0.8, ls=":")
    ax.set_xlabel(r"magnetic field $B$  [T]")
    ax.set_ylabel(r"speed  [m/s]")
    ax.set_title(r"MHD speeds vs $B$: $v_{\mathrm{fast}}$ bridges sound and Alfven")

    ax2 = ax.twinx()
    ax2.set_yscale("log")
    (l_b,) = ax2.plot(B, beta, color=STEEL, lw=1.6, ls="-.", label=r"$\beta=p/(B^2/2\mu_0)$")
    ax2.axhline(1.0, color=STEEL, lw=0.7, ls=":")
    ax2.set_ylabel(r"plasma $\beta$", color=STEEL)
    ax2.tick_params(axis="y", colors=STEEL)
    ax2.annotate(r"$v_A=c_s$", xy=(B_cross, c_s), xytext=(B_cross * 1.3, c_s * 0.18),
                 color="#555555", fontsize=9)
    ax2.annotate(r"$\beta>1$ gas", xy=(2.5e-3, 30), color=STEEL, fontsize=9)
    ax2.annotate(r"$\beta<1$ magnetic", xy=(0.25, 4e-3), color=STEEL, fontsize=9)

    lines = [l_cs, l_va, l_vf, l_b]
    ax.legend(lines, [ln.get_label() for ln in lines],
              loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_mhd_speeds_beta.svg")
    caps["fig1_mhd_speeds_beta.svg"] = (
        r"MHD characteristic speeds for a fixed plasma ($n=10^{19}\,$m$^{-3}$, "
        r"$T\approx100\,$eV, $\gamma=\tfrac53$) versus magnetic field $B$, from "
        r"sound_speed, alfven_speed and fast_magnetosonic_speed. The Alfven speed "
        r"$v_A\propto B$ rises out of the constant sound speed $c_s$; the fast "
        r"magnetosonic speed $v_{\mathrm{fast}}=\sqrt{c_s^2+v_A^2}$ tracks $c_s$ in "
        r"the gas-dominated regime ($\beta>1$, dotted line) and merges onto $v_A$ "
        r"once the field takes over ($\beta<1$). Crossover $v_A=c_s$ at $\beta=2/\gamma$.")

    # Fig 2 — the 0th velocity moment is continuity (KEY BRIDGE B2): a rigidly
    # advected density rho=f(x-ut) is carried at speed u while d_t rho + d_x(rho u)
    # stays ~0.  Profiles plotted at two times; the residual from continuity_residual
    # is on a twin axis, flat at ~0 to discretization precision.
    x = np.linspace(-20.0, 20.0, 400)
    dx = x[1] - x[0]
    u = 0.5
    bump = lambda xx: np.exp(-((xx) / 2.0) ** 2)
    t0, t1 = 0.0, 24.0                               # display advection: shift = u*t1 = 12
    rho_t0 = bump(x - u * t0)
    rho_t1 = bump(x - u * t1)
    dt = 1.0e-3                                       # small step for the residual check
    rho_a = bump(x - u * t0)
    rho_b = bump(x - u * (t0 + dt))
    res = continuity_residual(rho_a, rho_b, u, dx, dt)
    drho_dt = (rho_b - rho_a) / dt
    mr, md = float(np.max(np.abs(res))), float(np.max(np.abs(drho_dt)))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, rho_t0, color=INK, lw=2, label=fr"$\rho(x,\,t=0)$")
    ax.plot(x, rho_t1, color=FLOW, lw=2,
            label=fr"$\rho(x,\,t={t1:.0f})$  (shift $=ut={u*t1:.0f}$)")
    ax.fill_between(x, rho_t0, color=INK, alpha=0.06)
    ax.fill_between(x, rho_t1, color=FLOW, alpha=0.06)
    ax.set_xlabel(r"position $x$")
    ax.set_ylabel(r"density $\rho=f(x-ut)$")
    ax.set_title(r"0th moment = continuity: $\partial_t\rho+\partial_x(\rho u)=0$")
    ax.set_ylim(-0.05, 1.15)

    ax2 = ax.twinx()
    (l_res,) = ax2.plot(x, res, color=STEEL, lw=1.4,
                        label=r"residual $\partial_t\rho+\partial_x(\rho u)$")
    ax2.axhline(0.0, color="#bbbbbb", lw=0.6)
    ax2.set_ylabel(r"continuity residual", color=STEEL)
    ax2.tick_params(axis="y", colors=STEEL)
    rmax = max(mr * 4.0, 1e-12)
    ax2.set_ylim(-rmax, rmax)
    ax2.annotate(fr"$\max|\mathrm{{res}}|={mr:.1e}$" + "\n"
                 + fr"$\ll \max|\partial_t\rho|={md:.2f}$",
                 xy=(0.02, 0.80), xycoords="axes fraction", color="#444444", fontsize=9)

    h1, lab1 = ax.get_legend_handles_labels()
    ax.legend(h1 + [l_res], lab1 + [l_res.get_label()],
              loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_continuity_advection.svg")
    caps["fig2_continuity_advection.svg"] = (
        r"The $0^{\mathrm{th}}$ velocity moment of the kinetic equation is the "
        r"continuity law $\partial_t\rho+\partial_x(\rho u)=0$ (KEY BRIDGE B2, the "
        r"same conservation law as mass/charge/probability). A rigidly advected "
        r"density $\rho=f(x-ut)$ is simply carried at the fluid speed $u$ (blue "
        r"$\to$ orange); continuity_residual returns the local imbalance (grey), "
        r"flat at $\sim0$ — orders of magnitude below $\max|\partial_t\rho|$, so the "
        r"particle number is conserved locally and globally.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
