# 13.4 — Laminar Pipe Flow (notes)  *(~CM, not from Moran 8e)*

Citations: **~CM** = cross-trunk fluid mechanics (**NOT in Moran 8e**); see `refs.md`.
(Moran's Ch.9 treats *compressible* flow; viscous pipe-flow regimes are fluid mechanics.)

## 1. Reynolds number and the laminar regime
The **Reynolds number** is the ratio of inertial to viscous forces:
$$Re=\frac{\rho V D}{\mu}=\frac{V D}{\nu},\qquad \nu=\frac{\mu}{\rho}.$$
For fully developed flow in a round pipe, the flow is **laminar** for `Re ≲ 2300`;
transition to turbulence begins near this value (the exact number depends on inlet
disturbances). Laminar flow is smooth and layered — fluid moves in concentric
cylindrical "laminae" with no macroscopic mixing.

## 2. Parabolic (Hagen–Poiseuille) velocity profile
Solving the steady Navier–Stokes equations for fully developed laminar pipe flow gives a
**parabolic** profile:
$$u(r)=u_{max}\left[1-\left(\frac{r}{R}\right)^2\right],\qquad
V=\frac{u_{max}}{2},$$
i.e. the centerline speed is twice the mean speed. (Contrast the much flatter turbulent
profile of `13.5`.)

## 3. Friction factor and pressure drop
The Darcy friction factor has an **exact closed form** in the laminar regime:
$$f=\frac{64}{Re}.$$
The Darcy–Weisbach pressure drop `ΔP = f(L/D)(ρV²/2)` then reduces algebraically to the
**Hagen–Poiseuille law**
$$\Delta P=\frac{32\,\mu L V}{D^2}\quad\Longleftrightarrow\quad
Q=\frac{\pi R^4\,\Delta P}{8\mu L},$$
which is **linear in `V`** (and in `Q`). *Check:* oil (`ρ=900`, `μ=0.4 Pa·s`) at `V=2 m/s`
in a `D=0.05 m`, `L=10 m` pipe gives `Re=225` (laminar), `f=0.2844`, and both pressure-drop
forms give `ΔP=102.4 kPa` — equal to machine precision.

## Bridge
Raise the velocity (or drop the viscosity) until `Re` climbs past ≈2300–4000 and the
orderly laminae break down into **turbulence**: the profile flattens, mixing dominates,
and `f` no longer follows `64/Re` — module `13.5`.
