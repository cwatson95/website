# RE-06 — Relativistic Dynamics (notes)

Conventions: `c = 1`, mostly-plus η, `β=|v|`, `γ=1/√(1−v²)`. A particle's
worldline is parameterised by its **proper time** τ (RE-05).

## 1. 4-velocity and 4-momentum
Differentiating the worldline by the invariant τ gives the **4-velocity**
`U^μ = dx^μ/dτ = γ(1, 𝐯)` (a unit timelike vector, `U·U = −1`, RE-05). Multiplying
by the rest mass `m` gives the **4-momentum**
$$p^\mu = m\,U^\mu = (E,\ \mathbf p),\qquad E = \gamma m,\quad \mathbf p = \gamma m\,\mathbf v .$$
Its invariant is the **mass shell**
$$\boxed{\,p\cdot p = -m^2 \iff E^2 = \mathbf p^2 + m^2\,}$$
(`four_momentum`, `system_invariant_mass`). The energy `E` and the 3-momentum `𝐩`
are not separate conserved scalars but the **components of one 4-vector** —
which is why a boost mixes them and why their conservation laws merge (§3).

## 2. E = mc² and kinetic energy
Expanding `E = γm` for small `v`:
$$E = m + \tfrac12 m v^2 + \tfrac38 m v^4 + \cdots$$
The leading term is the **rest energy** `E₀ = m` (`= mc²`) — present even at rest,
the energy locked in mass. The next term is the Newtonian kinetic energy, so the
relativistic kinetic energy is
$$T = E - m = (\gamma - 1)m \ \xrightarrow{v\ll 1}\ \tfrac12 m v^2$$
(`kinetic_energy`). And the 3-momentum `γm𝐯 → m𝐯` reduces to `~CM-06`'s Newtonian
`𝐩 = m𝐯` (`test_newtonian_limit_matches_CM06`). Relativity *contains* Newtonian
mechanics as its `v≪c` limit; it adds the rest energy and the `γ`.

**Massless particles.** Take `m→0` with `E` fixed: the mass shell gives `E = |𝐩|`,
and the particle moves at `c` (`photon_four_momentum`, a null 4-vector).

## 3. Conservation of 4-momentum
The one dynamical law of relativistic collisions:
$$\sum_{\text{in}} p^\mu = \sum_{\text{out}} p^\mu \qquad(\texttt{is\_conserved}).$$
All four components: the time part is energy conservation, the space part is
`~CM-06`'s momentum conservation — **inseparable**, because they are one 4-vector.
Total 4-momentum is also the conserved quantity that *defines* an isolated system,
and `∇_μ T^{μν}=0` (RE-13) is its field-theoretic form.

## 4. Invariant mass and the COM frame
For a system of particles the total `P^μ = Σ p^μ` has an invariant
$$M = \sqrt{-P\cdot P}\qquad(\texttt{system\_invariant\_mass}),$$
the **invariant mass** — frame-independent (`test_…_frame_independent`) and equal
to the total energy in the **centre-of-momentum frame**, the frame moving at
`𝐯_COM = 𝐏/E` (`com_velocity`) where the total 3-momentum vanishes. Striking
consequence: **two back-to-back photons** (`m=0` each) have `M = 2E ≠ 0` — a
*massive* system built from massless parts. Mass is a property of systems, not an
additive particle label.

## 5. Creating mass: thresholds and inelastic collisions
Because energy can become rest mass:
- An **inelastic collision** (particles stick) conserves 4-momentum, so the
  product's rest mass is the system invariant mass, which **exceeds** the sum of
  the incoming masses — the lost kinetic energy is now mass (`inelastic_stick`;
  two `m=1` at `±0.8c` → `M = 2γ = 3.33`).
- **Production thresholds.** To make final particles of total rest mass `M` from a
  beam (mass `m_b`) on a target at rest (mass `m_t`), the invariant `s = -P·P`
  must reach `M²`. Since `s = m_b² + m_t² + 2E_b m_t`, the minimum **lab kinetic
  energy** is
  $$T_{\rm thr} = \frac{M^2 - (m_b+m_t)^2}{2\,m_t}\qquad(\texttt{threshold\_kinetic\_energy}).$$
  For `p+p → p+p+p+\bar p` (`M=4m_p`) this is `T = 6m_p` — the antiproton-discovery
  threshold (~5.6 GeV, the Bevatron).

## 6. Compton scattering
A photon scattering off a free electron (mass `m_e`) shifts its wavelength by
$$\Delta\lambda = \frac{\hbar}{m_e c}\,(1-\cos\theta)$$
(`compton_shift`, in natural units `(1−cosθ)/m_e`): zero in the forward direction,
maximal (`2/m_e`) on backscatter — the photon gives energy to the electron. It is
pure 4-momentum conservation between a photon and a massive particle, and it was
direct evidence that light carries momentum `p = E` (→ `~QM-22`, `~QO-01`).
