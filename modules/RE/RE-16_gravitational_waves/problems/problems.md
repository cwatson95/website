# RE-16 — Problems

Work them by hand, then check with `code/gravitational_waves.py`. Sources in
`../refs.md` (Zee §IX.4, §VI.5). Units `G = c = 1`, η = diag(−1,+1,+1,+1).

### P1. Trace-reverse and back  *(Zee §IX.4; notes §1)*
From `h̄_{μν} = h_{μν} − ½η_{μν}h`, show `h̄ ≡ η^{μν}h̄_{μν} = −h`, and hence that
reversing the trace again, `h_{μν} = h̄_{μν} − ½η_{μν}h̄`, recovers `h`. Why is
this the natural variable for the field equation?
*Answer:* `h̄ = h − ½·4·h = −h`; substituting gives back `h_{μν}`. In Lorenz gauge
`∂^μh̄_{μν}=0` the linearized `G_{μν}` is just `−½□h̄_{μν}`, so the field equation
becomes `□h̄_{μν} = −16πT_{μν}` — one wave equation per component.

**Solution.** Contract $\bar h_{\mu\nu}=h_{\mu\nu}-\tfrac12\eta_{\mu\nu}h$ with $\eta^{\mu\nu}$, using $\eta^{\mu\nu}\eta_{\mu\nu}=\delta^\mu_\mu=4$:
$$\bar h=\eta^{\mu\nu}h_{\mu\nu}-\tfrac12(\eta^{\mu\nu}\eta_{\mu\nu})h=h-\tfrac12\cdot4\,h=-h.$$
Feeding this into the reverse map recovers the original, so trace-reversal is an involution:
$$\bar h_{\mu\nu}-\tfrac12\eta_{\mu\nu}\bar h=h_{\mu\nu}-\tfrac12\eta_{\mu\nu}h-\tfrac12\eta_{\mu\nu}(-h)=h_{\mu\nu}.$$
It is the natural variable because in Lorenz gauge $\partial^\mu\bar h_{\mu\nu}=0$ the linearized Einstein tensor collapses to $G_{\mu\nu}=-\tfrac12\Box\bar h_{\mu\nu}$, turning $G_{\mu\nu}=8\pi T_{\mu\nu}$ into one decoupled wave equation per component, $\Box\bar h_{\mu\nu}=-16\pi T_{\mu\nu}$ (notes §1). No code check — structural.

### P2. The wave is null  *(Zee §IX.4; notes §2)*
A plane wave `h̄_{μν} = ε_{μν}cos(k_λx^λ)` solves the vacuum equation `□h̄=0`. Show
this forces `k_λk^λ = 0` and therefore `ω = |𝐤|` — gravitational waves move at
`c`.
*Answer:* `□cos(k·x) = −(k_λk^λ)cos(k·x)`; vanishing requires `k²=0`, i.e.
`−ω²+|𝐤|²=0`.
*Check:* `wave_equation_residual(0.1,0.05, dispersion_omega(1.0), 1.0)` ≈ 0; with
`ω=1.3, k=1.0` it is `≈0.069 ≠ 0` (off the light cone).

**Solution.** Acting with $\Box=\eta^{\mu\nu}\partial_\mu\partial_\nu$ on $\bar h_{\mu\nu}=\varepsilon_{\mu\nu}\cos(k_\lambda x^\lambda)$, each $\partial_\mu$ pulls down a factor $k_\mu$:
$$\Box\cos(k\cdot x)=-(\eta^{\mu\nu}k_\mu k_\nu)\cos(k\cdot x)=-(k_\lambda k^\lambda)\cos(k\cdot x).$$
So $\Box\bar h_{\mu\nu}=-(k_\lambda k^\lambda)\bar h_{\mu\nu}$ vanishes for all $x$ only if $k_\lambda k^\lambda=0$. With $k^\mu=(\omega,\mathbf k)$ in mostly-plus signature, $k_\lambda k^\lambda=-\omega^2+|\mathbf k|^2=0$, i.e. $\omega=|\mathbf k|$ and phase speed $\omega/|\mathbf k|=1=c$. The code's residual coefficient is exactly $\omega^2-k^2$: `wave_equation_residual(0.1,0.05,dispersion_omega(1.0),1.0)` $=0$ on-shell, while $\omega=1.3,\,k=1$ gives $\approx0.069\neq0$ (off the light cone).

### P3. Counting polarizations  *(Zee §IX.4; notes §3)*
Start from 10 components of symmetric `h_{μν}`. Subtract the 4 Lorenz conditions,
then the 4 residual-gauge conditions. How many physical polarizations remain?
Write the TT block for a `+z` wave.
*Answer:* `10 − 4 − 4 = 2`. With `h_{0μ}=0`, `h^i_i=0`, `k^μh_{μν}=0` and
`k^μ=ω(1,0,0,1)`: `h_{xx}=−h_{yy}=h_+`, `h_{xy}=h_{yx}=h_×`, all else 0.
*Check:* `is_transverse_traceless(tt_wave(h_+,h_×,ω,t,z))` → `True`; spatial trace
`= 0` exactly.

**Solution.** A symmetric $h_{\mu\nu}$ has $10$ independent components. Lorenz gauge $\partial^\mu\bar h_{\mu\nu}=0$ imposes $4$ linear conditions ($\to6$); the residual freedom — any $\xi^\mu$ with $\Box\xi^\mu=0$ preserves Lorenz gauge — supplies $4$ more ($\to2$). For $k^\mu=\omega(1,0,0,1)$, the condition $h_{0\mu}=0$ together with transversality $k^\mu h_{\mu\nu}=0$ kills the time and $z$ rows/columns, and tracelessness $h^i{}_i=0$ forces $h_{xx}=-h_{yy}$, leaving
$$h^{\rm TT}_{ij}=\begin{pmatrix}h_+&h_\times\\ h_\times&-h_+\end{pmatrix}\cos\omega(t-z).$$
Thus $10-4-4=2$ physical polarizations. `is_transverse_traceless(tt_wave(h_+,h_×,ω,t,z))` returns `True`, with spatial trace $h_{xx}+h_{yy}+h_{zz}=0$ exactly.

### P4. The `+` and `×` patterns and area  *(Zee §IX.4; notes §4)*
Using `δξ^i = ½h^i_jξ^j` at phase 0, find where the unit points `(1,0)` and
`(0,1)` go under a pure `h_+`, and `(1,±1)/√2` under a pure `h_×`. Then show the
ring's area is unchanged to linear order.
*Answer:* `h_+`: `(1,0)→(1+h_+/2, 0)`, `(0,1)→(0, 1−h_+/2)` — stretch `x`, squeeze
`y`. `h_×`: the diagonals scale by `1±h_×/2`. Area factor `det(I+½h) = 1 −
¼(h_+²+h_×²)cos² = 1 + O(h²)` — traceless ⇒ area-preserving.
*Check:* `ring_response(0.2,0,0,[(1,0),(0,1)])` → `[(1.1,0),(0,0.9)]`;
`area_change(0.2,0,0)` ≈ `−0.01` (`O(h²)`).

**Solution.** At phase $0$ ($\cos=1$) the geodesic-deviation shift is $\delta\xi^i=\tfrac12 h^i{}_j\xi^j$. Pure $h_+$ has $h^x{}_x=h_+,\,h^y{}_y=-h_+$, so $(1,0)\to(1+\tfrac12 h_+,\,0)$ and $(0,1)\to(0,\,1-\tfrac12 h_+)$ — $x$ stretched, $y$ squeezed; for $h_+=0.2$ these are $(1.1,0)$ and $(0,0.9)$. Pure $h_\times$ has $h^x{}_y=h^y{}_x=h_\times$, so the diagonal $(1,1)/\sqrt2$ scales by $1+\tfrac12 h_\times$ and $(1,-1)/\sqrt2$ by $1-\tfrac12 h_\times$. The area factor is
$$\det\!\big(I+\tfrac12 h\big)=1-\tfrac14(h_+^2+h_\times^2)\cos^2(\text{phase})=1+O(h^2),$$
zero at linear order because $h$ is traceless. `ring_response(0.2,0,0,[(1,0),(0,1)])`$\to[(1.1,0),(0,0.9)]$ and `area_change(0.2,0,0)`$\approx-0.01=-\tfrac14(0.2)^2$ — second order.

### P5. A spherical source is silent  *(Zee §IX.4; notes §5)*
Explain why mass conservation kills monopole radiation and momentum conservation
kills dipole radiation, so a spherically symmetric (even pulsating) source emits
no gravitational waves. Confirm the trace-free quadrupole of a symmetric
octahedron vanishes.
*Answer:* monopole `∫T⁰⁰=M` (`M̈=0`); dipole `∫y_iT⁰⁰` has `d/dt = P_i` conserved
(`d²/dt²=0`). Radiation starts at the quadrupole `Q_{ij}=∫y_iy_jT⁰⁰`. A symmetric
shell has isotropic `Q_{ij} ∝ δ_{ij}`, so the trace-free part `Q̄_{ij}=0`.
*Check:* `reduced_quadrupole([(2,±R,0,0),(2,0,±R,0),(2,0,0,±R)])` ≈ 0 ⇒
`quadrupole_luminosity` ≈ 0; a bar `[(1,2,0,0),(1,−2,0,0)]` gives `|Q̄|>0`.

**Solution.** Far-field $\bar h_{ij}$ is built from time derivatives of the moments of $T^{00}$. The monopole $\int T^{00}d^3y=M$ is the total mass — conserved, so $\ddot M=0$: no monopole radiation. The dipole $\int y_i T^{00}d^3y$ is the center of mass; its first derivative is the total momentum $P_i$, conserved, so its second derivative vanishes: no dipole radiation. Radiation therefore starts at the quadrupole $Q_{ij}=\int y_iy_jT^{00}d^3y$. A spherically symmetric shell has isotropic $Q_{ij}\propto\delta_{ij}$, whose trace-free part $\bar Q_{ij}=Q_{ij}-\tfrac13\delta_{ij}Q$ vanishes. `reduced_quadrupole` of the symmetric octahedron gives $\max|\bar Q_{ij}|\approx1.3\times10^{-15}$ (luminosity $\approx6.7\times10^{-31}\approx0$), whereas a bar along $x$ gives $\bar Q_{xx}=+5.33,\ \bar Q_{yy}=\bar Q_{zz}=-2.67\neq0$ and radiates.

### P6. The chirp mass  *(notes §6)*
For a circular binary, show `f_GW = 2f_orb = (1/π)√(M/r³)`. Given the inspiral law
`ḟ = (96/5)π^{8/3}M_c^{5/3}f^{11/3}`, what single mass combination does a measured
`(f, ḟ)` determine? Evaluate it for GW150914's `36 + 29 M_⊙`.
*Answer:* the quadrupole repeats twice per orbit ⇒ `f_GW=2f_orb`; `ω_orb²=M/r³`
(Kepler). `(f,ḟ)` fixes the **chirp mass** `M_c=(m₁m₂)^{3/5}/(m₁+m₂)^{1/5}`. For
`36+29`: `M_c ≈ 28 M_⊙`.
*Check:* `gw_frequency(36,29,r) == 2*orbital_frequency(36,29,r)`;
`chirp_mass(36,29)` ≈ `28.10`; `chirp_mass(30,30)` = `30/2^{1/5}` ≈ `26.12`.

**Solution.** A binary's mass quadrupole is invariant under a half-turn $\varphi\to\varphi+\pi$, so it returns to the same shape twice per orbit: $f_{\rm GW}=2f_{\rm orb}$. Kepler's third law for total mass $M$ at separation $r$ gives $\omega_{\rm orb}^2=M/r^3$, hence $f_{\rm orb}=\tfrac1{2\pi}\sqrt{M/r^3}$ and $f_{\rm GW}=\tfrac1\pi\sqrt{M/r^3}$. Equating the quadrupole luminosity to the orbital energy loss yields $\dot f=\tfrac{96}{5}\pi^{8/3}\mathcal M_c^{5/3}f^{11/3}$, in which the masses enter only through the chirp mass $\mathcal M_c=(m_1m_2)^{3/5}/(m_1+m_2)^{1/5}$ — so a measured $(f,\dot f)$ determines $\mathcal M_c$ alone. For $36+29\,M_\odot$, `chirp_mass(36,29)`$\approx28.10\,M_\odot$; the equal-mass check `chirp_mass(30,30)`$\approx26.12=30/2^{1/5}$, and `gw_frequency(36,29,r)`$=2\cdot$`orbital_frequency(36,29,r)`.

### P7. Why is gravitational radiation so weak?  *(conceptual; notes §5)*
Electromagnetic radiation starts at the **dipole** (`∼1/c³`); gravitational
radiation starts at the **quadrupole** (`∼1/c⁵`). Argue from the conservation laws
why gravity has no dipole term, and what that implies for detectability.
*Answer:* there is no negative gravitational "charge," and the mass dipole's
derivative is the conserved total momentum — so the dipole cannot radiate. The
leading `1/c⁵` suppression is why even `M_⊙`-scale compact binaries produce strains
`h ∼ 10^{−21}`, requiring km-scale interferometers. *(No code check — structural.)*

**Solution.** Both points follow from conservation laws. Electromagnetism has charges of both signs, so the charge dipole $\int\rho\,\mathbf x\,d^3x$ can oscillate freely and radiates at order $1/c^3$. Gravity has only positive mass — no negative gravitational charge — and the mass dipole $\int\rho\,\mathbf x\,d^3x=M\,\mathbf x_{\rm cm}$ has time derivative equal to the total momentum $\mathbf P$, which is conserved; its second derivative therefore vanishes and the dipole cannot source radiation. Radiation is pushed up to the quadrupole, costing a further $1/c^2$ for an overall $1/c^5$. Since $G/c^5\approx10^{-53}$ in SI units, even $M_\odot$-scale compact binaries produce strains $h\sim10^{-21}$, which is why detection demands km-scale interferometers. No code check — structural.
