# RE-16 — Gravitational Waves (notes)

Conventions: geometrized units `G = c = 1`; mostly-plus metric
`η = diag(−1,+1,+1,+1)`; weak field `g_{μν} = η_{μν} + h_{μν}` with `|h| ≪ 1`.
Greek indices run 0..3, `x⁰ = t`, `(x¹,x²,x³) = (x,y,z)`; Latin indices are
spatial. The d'Alembertian is `□ = η^{μν}∂_μ∂_ν = −∂_t² + ∇²`. Indices on the
small field `h` are raised/lowered with `η` (corrections are `O(h²)`).

## 1. Linearized gravity and the wave equation
Expand the metric about flat space, `g_{μν} = η_{μν} + h_{μν}`, and keep terms
linear in `h`. The Ricci tensor reduces (RE-13; Zee §VI.5) to
$$R_{\mu\nu} = -\tfrac12\big(\Box h_{\mu\nu} - \partial_\mu\partial^\lambda h_{\lambda\nu}
 - \partial_\nu\partial^\lambda h_{\lambda\mu} + \partial_\mu\partial_\nu h\big),
 \qquad h \equiv \eta^{\mu\nu}h_{\mu\nu}.$$
Define the **trace-reversed** perturbation
$$\boxed{\,\bar h_{\mu\nu} = h_{\mu\nu} - \tfrac12\eta_{\mu\nu}h\,}\qquad(\bar h = -h),$$
so called because reversing its trace gives back `h`. The linearized Einstein
equation `G_{μν} = 8πT_{μν}` then collapses, once the **Lorenz (harmonic) gauge**
$$\partial^\mu \bar h_{\mu\nu} = 0$$
is imposed, to a decoupled wave equation per component:
$$\boxed{\,\Box \bar h_{\mu\nu} = -16\pi\,T_{\mu\nu}\,.}$$
The gauge is always reachable: under an infinitesimal coordinate change
`x^μ → x^μ + ξ^μ` the field transforms as `h_{μν} → h_{μν} − ∂_μξ_ν − ∂_νξ_μ`
(structurally identical to the electromagnetic `A_μ → A_μ − ∂_μΛ`), and solving
`□ξ_ν = ∂^μ h_{μν} − ½∂_ν h` enforces Lorenz gauge. This is the gravitational
analogue of `□A_μ = −J_μ` in EM — gravity is a (spin-2) radiation field.

## 2. Vacuum: gravity propagates at the speed of light
Away from sources `T_{μν} = 0`, so `□\bar h_{μν} = 0`: the ordinary relativistic
wave equation. Plane-wave solutions `\bar h_{μν} = ε_{μν}\cos(k_λ x^λ)` require
`k_λ k^λ = 0` — the wavevector is **null**, `ω² = |\mathbf k|²`. Hence the phase
speed `ω/|\mathbf k| = 1 = c`: **gravitational waves travel at the speed of
light** (`dispersion_omega(k) = |k|`). `wave_equation_residual` makes this exact —
acting with `□` on the plane wave returns `(ω² − k²)\bar h_{μν}`, which is the
zero tensor *iff* `ω = |k|` and nonzero off the light cone. A massless field is
the statement that the graviton is massless; the `ω = |k|` line is its mass shell.

## 3. The transverse-traceless gauge — only two polarizations
A symmetric `h_{μν}` has 10 components. Lorenz gauge is 4 conditions (→ 6), and
there is *residual* gauge freedom — any `ξ^μ` with `□ξ^μ = 0` preserves Lorenz
gauge — giving 4 more conditions. Spend them to impose, for a wave along `z`,
$$h_{0\mu} = 0,\qquad h^i{}_i = 0,\qquad k^\mu h_{\mu\nu}=0,$$
the **transverse-traceless (TT) gauge** (here `\bar h = h` since `h` is now
traceless). Two physical degrees of freedom survive. For `k^μ = ω(1,0,0,1)` the
conditions force the time row/column and the entire `z` row/column to vanish and
`h_{xx} = −h_{yy}`, leaving the `2×2` transverse block
$$h_{ij}^{\rm TT} = \begin{pmatrix} h_+ & h_\times \\ h_\times & -h_+ \end{pmatrix}
\cos\omega(t-z),$$
i.e. `h_xx = −h_yy = h_+`, `h_xy = h_yx = h_×` (`tt_wave`,
`is_transverse_traceless`). These are the **plus** and **cross** polarizations.
The basis tensors `e_+ = diag(1,−1,0)` and `e_× = (off-diagonal 1)` are
trace-free and **orthogonal**, `Σ_{ij}e_+^{ij}e_×^{ij} = 0` — independent
polarizations (`polarization_tensors`). Quantum-mechanically they are the two
helicity-±2 states of the massless **graviton**; the `45°` (not `90°`) angle
between `+` and `×` is the signature of a **spin-2** field.

## 4. Effect on matter — a ring of free particles, area-preserving
A single free particle initially at rest stays at rest in TT gauge (`Γ^ρ_{00} = 0`
there): one point cannot detect a wave, because spacetime is locally flat. You
must compare *neighbours*. The proper separation of two nearby free particles with
coordinate separation `ξ^i` is modulated, and to linear order each particle is
displaced by
$$\boxed{\,\delta\xi^i = \tfrac12\,h^i{}_j\,\xi^j\,}$$
(`ring_response`). For a `+z` wave this rocks the transverse plane: at one phase
`h_+` **stretches** `x` by `+\tfrac12 h_+` while **squeezing** `y` by `−\tfrac12
h_+` (equal and opposite — `test_plus_stretches_x_squeezes_y_equally`); half a
period later they swap. A ring of test masses oscillates between a `+`-shaped and
a `×`-shaped ellipse — the classic detector picture, and how a laser
interferometer (LIGO) senses a wave as a differential arm-length change. Because
`h` is **traceless**, the deformation matrix `D = I + \tfrac12 h` has
`\det D = 1 - \tfrac14(h_+^2 + h_\times^2)\cos^2 = 1 + O(h^2)`: the ring's **area
is preserved to linear order** (`area_change`). What stretches one direction
squeezes the perpendicular one by the same fraction — a pure **shear**, the
defining geometric fingerprint of a quadrupolar wave. (The tidal field doing the
stretching is the linearized Riemann tensor `R_{i0j0} = −\tfrac12\ddot h_{ij}^{\rm
TT}`, tying this straight back to geodesic deviation in RE-11.)

## 5. Generation — the quadrupole formula, no monopole or dipole
Solving `□\bar h_{μν} = −16πT_{μν}` with the retarded Green's function (the *same*
one as EM, propagating on the light cone) gives `\bar h_{μν}(t,\mathbf x) =
4\!\int d^3y\,T_{μν}(t-|\mathbf x-\mathbf y|,\mathbf y)/|\mathbf x-\mathbf y|`.
Multipole-expanding the far field and using conservation `∂_μT^{μν}=0` to trade
`T^{ij}` for `T^{00}`, the radiative part is set by the **mass quadrupole moment**
$$Q_{ij}(t) = \int d^3y\;y_i y_j\,T^{00},\qquad
  \bar h_{ij}(t,\mathbf x) = \frac{2}{r}\,\ddot Q_{ij}(t_R).$$
The lower multipoles **cannot radiate**: the monopole `∫T^{00} = M` is conserved
(mass), and the dipole `∫y_iT^{00}` is the center of mass, whose first derivative
is the total momentum — also conserved. So `\ddot{(\text{monopole})} =
\ddot{(\text{dipole})} = 0` and gravitational radiation starts at the
**quadrupole**. Consequence: a **spherically symmetric** source (even pulsating —
Birkhoff's theorem) has constant exterior field and is gravitationally **silent**
(`reduced_quadrupole` of a symmetric octahedron `= 0`,
`test_spherical_source_has_zero_quadrupole_and_zero_luminosity`). The power
carried off (Einstein's **quadrupole luminosity**) is, with the *trace-free*
reduced moment `\bar Q_{ij}`,
$$\boxed{\,P = \frac{1}{5}\Big\langle \dddot{\bar Q}_{ij}\,\dddot{\bar Q}^{ij}\Big\rangle\,}$$
(`quadrupole_luminosity`). There is no dipole `1/c³` term as in EM — the lowest
gravitational radiation is `1/c⁵`, which is why it is so weak.

## 6. Binary inspiral — the chirp and the chirp mass
Two masses `m₁, m₂` in a circular orbit of separation `r` and total mass
`M = m₁+m₂` orbit at the Kepler rate `ω_{\rm orb}^2 = M/r^3`. Their quadrupole
returns to the same shape **twice** per orbit, so
$$f_{\rm GW} = 2 f_{\rm orb} = \frac1\pi\sqrt{\frac{M}{r^3}}$$
(`gw_frequency = 2·orbital_frequency`). Radiating energy shrinks the orbit, raising
`f` — the **chirp**. Equating the quadrupole luminosity to the orbital energy loss
gives the frequency sweep
$$\boxed{\,\dot f = \frac{96}{5}\,\pi^{8/3}\,\mathcal M_c^{5/3}\,f^{11/3}\,}$$
(`chirp_rate`, `CHIRP_RATE_CONST = (96/5)π^{8/3}`), in which the masses enter
*only* through the **chirp mass**
$$\mathcal M_c = \frac{(m_1 m_2)^{3/5}}{(m_1+m_2)^{1/5}}$$
(`chirp_mass`; symmetric in the masses, `= m/2^{1/5}` for equal masses). Measuring
`f` and `\dot f` from the waveform therefore reads off `\mathcal M_c` directly —
this is exactly how LIGO determined `\mathcal M_c ≈ 30\,M_\odot` for **GW150914**
(2015), the first direct detection (`36+29\,M_\odot`), and earlier how the
Hulse–Taylor binary pulsar's measured orbital decay confirmed the quadrupole
formula indirectly. The strong `f^{11/3}` and `\mathcal M_c^{5/3}` powers are the
audible rising "chirp" that gives the effect its name.
