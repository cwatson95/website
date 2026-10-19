## 2026-09-22 — sound-waves: PhET's Sound Waves remade, with the image source and the ideal gas made explicit

### Added
- `docs/phets_revised/sound-waves.html` (208 KB, 3172 lines) — a clean-room remake of PhET
  Interactive Simulations' **Sound Waves 1.1.11** (CC-BY 4.0; new code, no PhET code or assets).
  Six views: **the speaker** (PhET's Intro), **the bench** (Measure), **two speakers** (Two
  Sources), **the wall** (Reflection), **thin air** (Air Pressure) and **wavelength and speed**
  (this file's own analysis view). Build: `build/sound-waves/`.
- **The lattice.** PhET's scheme — u_tt = v²∇²u as a 5-point leapfrog at Courant number C = ½
  with Mur's second-order absorbing edge — copied from the engine built and pinned for
  `wave-interference.html` (`build/wave-interference/p2_engine.js`, SHA-256 `393cdd8f…`, API in
  its `ENGINE.md`) into this build's own `p2_engine.js`, with its two changes named in its
  header. `assemble.py` re-checks the three genuinely-unchanged copies (`p1_utils.js`,
  `p4_helpers.js`, `p7_shot.js`) against wave-interference's own SHA-256 in **both** directions
  on every assembly, so neither side can drift unnoticed. Nothing in
  `build/wave-interference/` or `build/waves-intro/` was touched.
- **The stencil is falsified independently**, not just inherited: `derive.py` puts an exact
  lattice plane wave exp(i(kₓi + k_yj − Ωn)) with Ω = latOmega(kₓ,k_y) through one update and
  measures the residual — 4.4e-16 to 1.1e-14 at four wavevectors. The suite repeats it.
- **The time step is solved from the lattice's own dispersion relation at every frequency**
  (Ω = 2 asin(C sin(π/N_λ)), Δt = Ω/2πf), so λ = v/f and T = 1/f are exact along the lattice
  axes. **Measured** on the lattice — a least-squares fit of a sin/cos/constant/drift model
  against the drive's own phase at every cell of a 181-cell tank, then the slope of the
  unwrapped phase over cells 30–120 — λ agrees with v/f to **0.05 %** from 325 Hz to 1000 Hz
  and to **0.35 %** at 100 Hz, where the fit window holds only 1.4 wavelengths. PhET's single
  fixed step instead leaves its wavelengths **1.3 % short at 100 Hz and 12.8 % short at
  1000 Hz**; both curves are drawn side by side in the analysis view.
- **A 231-cell lattice, not PhET's 151**, and the analysis view says why: on PhET's own lattice
  the top of this sim's slider has 3.81 cells per wavelength against 6.55 here. The square
  lattice is still not isotropic, and that is drawn and labelled rather than hidden — at
  1000 Hz a wave along the diagonal is 2.04 % longer than one along an axis and the group speed
  is 8.8 % below v itself (6.1 % below the phase speed the lattice really carries; 0.59 % and
  2.6 % at the default 550 Hz).
- **The second speaker and the reflecting wall are exact superpositions of ONE lattice field**,
  which is also PhET's own construction: a source one row down contributes u shifted one row
  down (the equation is linear), and mirroring is an isometry, so u read at the mirror of P *is*
  the field of the image source at P. The consequences are checked, not assumed:
  - the angles of incidence and reflection agree to **2.7e-15** over 14 rays,
  - the reflected path equals Fermat's shortest, |SQ| + |QP| = |S′P|, to **5.3e-15**,
  - the normal derivative of the drawn field vanishes on the wall to **4.8e-13**,
  - mirroring twice is the identity to 3.6e-15 and agrees with PhET's own projection form.
- **The quiet hyperbolae** |r₁ − r₂| = (m + ½)λ in closed form, cross-checked against
  root-solving the path difference directly (worst 6.4e-13 over 16 points), with their
  far-field asymptotes equal to asin((m + ½)λ/d) to 1e-16, and `nodeX` inverting `nodeY`.
  The lattice's own quiet lines sit up to **2.45 cells** outside those curves at 550 Hz — and
  that is not noise: replacing the single λ by the lattice's own k(θ), which is smaller off the
  axes, brings the prediction back to within **0.16 of a cell**. Both numbers are pinned.
- **The air, honestly.** Removing the air scales the drive with the density, as PhET does (it
  multiplies its source cell by its pressure property), which is the right law for a cone of
  fixed velocity, p = ρcu. The twin shows the consequence is *exact*: at ρ = 0.25 the whole
  lattice is a quarter of the ρ = 1 lattice, cell for cell, to 8.9e-16 after 220 steps. What
  does **not** change is the speed: c = √(γp/ρ) = √(γRT/M), identical to 1e-13 at 1, 0.5, 0.1,
  0.01 and 10⁻⁴ atm, and that is drawn as a flat orange line against the falling green
  amplitude in a panel of its own under the picture. PhET's 343 m/s is the ideal gas at
  **19.60 °C** (343.235 m/s at 20.00 °C, 0.068 % higher); γ = 7/5, R = 8.314462618 J/mol/K
  exactly, M = 28.9647 g/mol for standard dry air. The mean free path (65.7 nm at 1 atm) and the
  density at which it reaches one wavelength (1.9×10⁻⁷ atm at 1000 Hz) are printed as the point
  where the model stops being physics.
- Verification: `derive.py` → `refvals.txt` (279 reference lines) → `p7_refs.js`;
  **selfTest 1338 passed, 0 failed** under both `jsc` and `osascript`; **UI drive 228 passed,
  0 failed**; display-list capture at 1400×820, 1100×700 and 560×380 → `audit.py`
  **0 layout problems** at all three → `raster.py`, every view's PNG looked at.
  `mutants.json` holds **82** mutants (74 physics, 8 UI).

### Fixed (during the build)
- **A rigid-wall model must not mask the field it is proving a property of.** The first
  Neumann check fed `fieldAtModel` two points either side of the wall, and that function
  returns 0 behind it — so the "derivative" was (something − 0)/2h and the check failed at
  5e+1 instead of 5e-13. The image construction is defined by the *unmasked* sum u(P) + u(P′),
  which is even about the wall; the mask is what the sim *draws*. Split into `mirrorSum` (the
  field) and `fieldAtModel` (the picture), and the check passes at 4.8e-13.
- **A mode switch that leaves the source running makes the button a stop button.** Coming back
  from pulse to continuous set `R.on = cont`, so the speaker was already going and the next
  press switched it off. PhET's `soundModeProperty` link stops everything; `setWaveMode` now
  sets `R.on = false` either way and the button starts it, which is what both the UI drive and
  PhET expect.
- **A label hung under a draggable object has nowhere safe to go.** The ruler's
  "metres — 8.02 wavelengths long here" caption was pushed by `lab()`'s collision dodge onto the
  ruler's own tick numbers, which are painted straight and cannot move. The unit now sits where
  PhET puts it (on the last major tick, `unitsMajorTickIndex`), the wavelength count moved to
  the readout, and the ruler's whole rectangle is **reserved in `LABELS` before any overlay
  label is placed** — otherwise an overlay lands on tick numbers that have nothing to dodge.
- **Two more collisions of the same family**, both found by the panel sweep rather than by eye:
  the image-speaker label ran off the right edge of the box over the listener's chart (it now
  hangs to the left when the marker is within 150 px of that edge), and the bounce-angle label
  sat on the graph's title when the wall is laid flat and the bounce is on the floor of the box
  (it now goes above the bounce point there).
- **A y tick at 0 collides with the x tick at 0 in the corner** of the new air panel
  ("0.00" vs "0.0"), at every panel size. The panel's y ticks are given explicitly, starting at
  0.25.
- **The listener's chart title ran under the floating readout at 1100×700.** The panel started
  at y = 486 and its title sits 24 px above it, i.e. at 462 — inside the audit's readout box
  (y < 470). Moved to 502.
- **Two survivors of the first mutation sweep, both real findings.** (1) `TONE_MAX` could be
  changed freely: the only assertion on it compared `toneLevel(...)` with `TONE_MAX` itself —
  a test that re-derives the thing it is testing. Pinned against the absolute 0.3. (2) Swapping
  the two arguments of `atan2` inside `latKofDir` survived, and had to: a square lattice is
  symmetric about its diagonal, so k(θ) = k(90° − θ) identically. That mutant was replaced by
  one on the part that *is* load-bearing (the cells-to-metres conversion), and the symmetry is
  now **asserted deliberately** — with k(θ) along the axis pinned against 2π/λ and the
  anisotropy asserted to be non-zero, so neither the symmetry nor the conversion is a blind
  spot. Second sweep: **74 of 74 physics mutants caught, 0 survivors.**
- **A shared probe buffer mixes two views' pictures.** The listener's one-period ring buffer is
  filled from whichever composition is on show; switching from two speakers to the wall left up
  to a period of the other view's field in it. The buffer now records which composition filled
  it and empties itself when that changes.
- The parcels' exaggeration was raised from 0.3 to 0.45 of the parcel spacing after looking at
  the PNG: at 0.3 the largest real push was 0.125 of the spacing and the bunching the view
  exists to show was barely visible. At 0.45 it is 0.187 — still far below the spacing that
  would make rows cross. The parcels are also drawn dark over the lit field and light on the
  black one (white-on-mid-grey was unreadable), and the marked parcel was moved off the middle
  of the grid, where the listener stands.

### Known-bad candidates
- **A field function that masks its output cannot be used to test a property of the
  unmasked field.** The image-source construction satisfies ∂p/∂n = 0 because u(P) + u(P′) is
  *even* about the wall; the sim draws only the near half of that. Testing the boundary
  condition through the drawing function measures the mask, not the physics, and it fails by
  fourteen orders of magnitude — which reads like a broken derivation rather than a broken
  test. Keep the model function and the picture function separate, and test the model one.
- **A square lattice is symmetric about its diagonal, so any mutant that only swaps x and y in
  a direction is EQUIVALENT.** latK(Ω, θ) = latK(Ω, 90° − θ) identically, because latOmega is
  symmetric in kₓ and k_y. Expect such a mutant to survive; replace it with one on the unit
  conversion beside it, and assert the symmetry as a stated property plus one absolute pin on
  the conversion.
- **Reserve a drawn instrument's rectangle in `LABELS` BEFORE placing any overlay label.**
  `lab()` dodges only what is already registered, and an instrument whose numbers are painted
  straight (a ruler's tick marks, a scale) cannot dodge back. Registering it at the end — where
  it is drawn — is too late for anything drawn before it.
- **PhET's Sound Waves fades its own drawn field with a linear taper (85 − r)/85 in lattice
  cells** (`MAX_SOUND_DISTANCE`), so its sound visibly dies 7.66 m from the speaker whatever the
  physics does. That is a display trick, not absorption; this remake draws the field the lattice
  actually has (whose 2-D spreading is already 1/√r, measured exponent −0.46 to −0.51) and says
  so in the header. Do not reintroduce it as if it were a model.
- **PhET's listener interference uses λ = 36/f MODEL UNITS, not v/f** — 4.96 % longer than the
  real wavelength and 9.5 % longer than the one its own lattice carries at the default
  frequency. It is a hand-tuned constant in `updateListenerSound`. Read the field the lattice
  holds at the listener instead; the difference is printed in the analysis so it cannot be
  mistaken for agreement.
- At **560×380** (`isNarrow`), the layout deliberately uses the full stage width and the
  floating readout covers part of the caption and the analysis plane — 46 advisory
  `under-readout` lines in the audit, none at 1100 or 1400. This is the same choice the
  siblings make (`wave-interference`, `waves-intro`); the audit reports 0 layout problems at
  every size.
