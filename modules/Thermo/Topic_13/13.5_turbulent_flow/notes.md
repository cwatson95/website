# 13.5 — Turbulent Pipe Flow (notes)  *(~CM, not from Moran 8e)*

Citations: **~CM** = cross-trunk fluid mechanics (**NOT in Moran 8e**); see `refs.md`.
(Moran's Ch.9 treats *compressible* flow and never defines the Reynolds number; viscous
pipe-flow regimes are fluid mechanics. This is the turbulent companion to `13.4`.)

## 1. Reynolds number and the turbulent regime
The same group that governs `13.4` sets the regime:
$$Re=\frac{\rho V D}{\mu}=\frac{V D}{\nu}.$$
For round-pipe flow the rough boundaries are
$$Re<2300\ \text{laminar},\quad 2300\lesssim Re\lesssim 4000\ \text{transitional},\quad
Re>4000\ \text{fully turbulent}.$$
Turbulence is chaotic and three-dimensional: eddies mix momentum across the pipe, so the
flow is **not** the orderly laminae of `13.4`.

## 2. The flatter turbulent profile
Empirically the time-mean profile follows a **1/n power law** (`n≈7` near `Re≈10⁵`):
$$\frac{u(r)}{u_{max}}=\left(1-\frac{r}{R}\right)^{1/n},\qquad
\frac{V}{u_{max}}=\frac{2n^2}{(n+1)(2n+1)}.$$
For `n=7` the mean-to-peak ratio is `0.817` — far flatter than the laminar `0.5` (the
parabola of `13.4`). The steep near-wall gradient is where the large wall shear comes from.

## 3. Friction factor: Moody / Colebrook
The exact laminar `f=64/Re` no longer holds. The Darcy friction factor now depends on
`Re` **and** the relative roughness `ε/D`, summarized by the **Moody chart** and its
implicit fit, the **Colebrook equation**:
$$\frac{1}{\sqrt f}=-2\log_{10}\!\left(\frac{\varepsilon/D}{3.7}+\frac{2.51}{Re\sqrt f}\right).$$
Two useful explicit forms:
- **Blasius** (smooth wall, `4\times10^3<Re<10^5`): $f=0.316\,Re^{-1/4}$.
- **Haaland** (explicit, within ~1.5% of Colebrook):
  $\tfrac{1}{\sqrt f}=-1.8\log_{10}\!\big[(\varepsilon/D/3.7)^{1.11}+6.9/Re\big]$.

At very high `Re` the `2.51/(Re\sqrt f)` term vanishes and `f` becomes **roughness-only**
(fully rough, `Re`-independent): `1/\sqrt f = -2\log_{10}(\varepsilon/D/3.7)` (Nikuradse).
*Check:* water (`ρ=1000`, `μ=10⁻³`) at `V=2 m/s` in a `D=0.05 m` pipe gives `Re=10⁵`
(turbulent); Blasius `f=0.0178`, Colebrook-smooth `f=0.0180`, and at `ε/D=0.001` the
roughness raises it to `f=0.0222`.

## 4. Pressure drop / head loss
The **form** of Darcy–Weisbach is unchanged from `13.4`:
$$\Delta P=f\,\frac{L}{D}\,\frac{\rho V^2}{2}=\rho g\,h_L,\qquad
h_L=f\,\frac{L}{D}\,\frac{V^2}{2g};$$
only `f` is now the turbulent `f(Re,\varepsilon/D)` rather than `64/Re`. Because turbulent
`f` is much larger than the laminar value at the same `Re`, and `ΔP∝V^2` (vs `∝V`
laminar), turbulent pipe losses climb steeply with speed.

## Bridge
Drop `Re` back below ≈2300 (slower flow, smaller pipe, more viscous fluid) and the eddies
die out: the profile sharpens to the parabola and `f` returns to the exact `64/Re` —
module `13.4`. The Moran-trunk compressible-flow modules are `13.1`–`13.3`.
