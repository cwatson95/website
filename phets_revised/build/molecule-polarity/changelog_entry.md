## 2026-09-22 — molecule-polarity: bond dipoles from electronegativity, the vector sum that cancels exactly, a damped rotor in the field, and nineteen real molecules against measurement

### Added
`docs/phets_revised/molecule-polarity.html`, a clean-room remake of PhET
Interactive Simulations' **Molecule Polarity** (build 2.0.2, CC-BY 4.0; no PhET
code or assets). Six views: **two atoms**, **three atoms** and **real
molecules** are PhET's three screens; **the vector sum**, **the field** and
**the dipole atlas** are the analysis views. Build dir
`build/molecule-polarity/` (Python twin `derive.py`, `gen_ref.py`,
`gen_mutants.py`, `make_head.py`, `assemble.py`, the UI drive, the capture
tail, 69 mutants).

**Exact, and pinned to `derive.py`:**

- **PhET's model, read out of its own build, not recalled.** The bond dipole is
  `Vector2.createPolar(|ΔEN|, bond angle)` with π added when ΔEN < 0; those two
  branches are exactly `ΔEN · u(atom1→atom2)`, which is how the file writes it,
  and the two forms are asserted equal over the whole 1573-case slider grid
  (3.1e−16). So the bond dipole is **linear in ΔEN with coefficient 1** in
  PhET's own units — not debye, and the file says so on the canvas.
  Partial charges are PhET's: `q_A = +ΔEN`, `q_B = −ΔEN` on the diatomic;
  `q_A = EN_B − EN_A`, `q_C = EN_B − EN_C`, `q_B = (EN_A−EN_B)+(EN_C−EN_B)` on
  the triatomic, so neutrality is an identity (0 over the whole 11³ grid).
- **The molecular dipole is the exact vector sum at every bond angle.** The
  closed form |μ|² = Δ_AB² + Δ_BC² − 2Δ_AB Δ_BC cos θ (signed ΔENs) agrees with
  the componentwise sum to 2.7e−15 over 47 916 (EN, EN, EN, θ) combinations,
  and for a symmetric triatomic |μ| = 2|ΔEN||cos(θ/2)| to 2.2e−15. **At
  θ = 180° the cancellation is identically zero** — 7.3e−16 over all 121
  electronegativity pairs, which is rounding in the trigonometry and nothing
  else. The two ends of the curve are |Δ_AB − Δ_BC| at 0° and |Δ_AB + Δ_BC| at
  180°, both asserted, the second against a 0.01°-resolution brute-force scan.
- **The surfaces are PhET's gradient, stop for stop, asserted against the model
  rather than by eye.** Surface width 150 + 2 × 2.25 × 50 = 375; gradient width
  `linear(1, 0, W, 5W, |ΔEN|/2)` for electron density and `linear(1, 0, W/2,
  5W, |ΔEN|/2)` for electrostatic potential (PhET's
  `SURFACE_GRADIENT_WIDTH_MULTIPLIER` = 5), so at ΔEN = 0 the gradient is five
  times the surface and the whole surface reads neutral. 50 sampled colours
  match the twin to 1e−9; black is **more** electron density and red is a
  **negative** potential, both asserted at the ends, and the potential's
  midpoint is white for every ΔEN. PhET's 35-stop rainbow and its
  `(8e+1)/2` mapping are reproduced and pinned.
- **The field is a damped rotor, derived rather than imitated.** A dipole in
  the plate field has energy −μE cos ψ, hence torque −μE sin ψ:
  `I ψ̈ = −μE sin ψ − bψ̇`, `b = 2ζ√(IμE)`, `ω₀ = √(μE/I)`. ψ = 0 is the
  stable equilibrium and ψ = π the unstable one (from ψ = π exactly nothing
  moves, to 0 in double precision; from π − 1e−3 it falls to 2.9e−4 in 30 s).
  The energy ½Iψ̇² + μE(1−cos ψ) never rises along any integrated orbit
  (max rise 1.1e−16), the fixed-step RK4 agrees with `scipy.solve_ivp` to
  2.3e−12 at t = 3 s, the small-angle orbit reproduces the linear solution to
  2e−8 relative, and the zero-crossing count is 9 at ζ = 0.2 and 0 at ζ ≥ 1.
- **PhET's own kinematic rule is kept beside it and pinned.** Its
  `MoleculePolarityModel.step` moves the dipole angle
  `|linear(0, 2, 0, 0.17, |μ|)| = 0.085|μ|` radians per frame toward alignment,
  the short way round: 16 frames from 150° at |μ| = 2, 31 at |μ| = 1, 77 at
  |μ| = 0.4, and from 210° the angle *increases*. All asserted. Which model
  runs is a chip; the header says plainly that PhET's is frame-rate dependent
  and is not a dynamical model.
- **PhET's plate order is read out of its own `HBox`: negative plate left,
  positive plate right**, so the field points in −x and the chemist's
  positive-to-negative arrow settles pointing at the + plate. That is the
  physically right answer, and it is stated on the canvas.
- **PhET's real-molecule table, extracted from the build**: PubChem geometry
  in ångström, ORCA Hirshfeld charges, Psi4 molecular dipoles, and the Pauling
  electronegativities its element table carries. Basic mode uses |ΔEN|;
  Advanced uses |q₁−q₂|/2 × d / 0.208194 debye and PhET's
  `getDipoleArrowScale` rescaling. Every molecule's bond dipoles, vector sums,
  arrow scale, bond lengths and bond angles are pinned; the Hirshfeld charges
  sum to zero to 7e−6; the nine symmetric molecules cancel to 1.2e−3 D or
  better. Where the molecular dipole *points* is asserted in 3-D (water,
  ammonia, HF, CH₃F, HCN, CH₂O point at the most negative atom; chloroform's
  runs from the H toward the three chlorines), so the assertion is about the
  model and not about the camera.
- **Measured data, retrieved and cited, not recalled.** Dipole moments from
  NIST CCCBDB "Experimental Dipole Moments" (`cccbdb.nist.gov/diplistx.asp`,
  retrieved 2026-09-22) to the three decimals it prints, each with CCCBDB's own
  source code; bond angles from its "Experimental bond angles" (release 22,
  May 2022). Borane is **absent** from the dipole table and is shown as absent,
  not as zero.

**Two findings worth recording.**

1. **PhET's PubChem geometry is not the measured geometry, and it costs its
   water dipole 0.34 D.** The stored H–O–H angle is 97.920° against CCCBDB's
   104.48°, and the stored H–N–H is 95.082° against 106.67° — 6.6° and 11.6°
   too narrow. The symmetric molecules are right to the last digit (CO₂ 180°,
   CH₄ 109.470°, BF₃ 119.994°), because symmetry fixes them. Over the 18
   molecules with a measured value the mean |Psi4 − measured| is 0.104 D, and
   the two worst are ozone (+0.431 D, stored angle 2.7° wide) and water
   (−0.341 D).
2. **Basic mode cannot describe ozone, and that is the model's boundary, not a
   bug.** Three oxygens give ΔEN = 0 on both bonds, so the electronegativity
   model calls O₃ exactly non-polar; it measures 0.530 D. On the ten polar
   molecules the Spearman rank correlation with measurement is 0.188 for the
   basic model and 0.782 for the quantum column. Both numbers are computed in
   the twin and pinned, and the lower panel of the atlas view draws the
   failure.

**One stated deviation.** PhET's rainbow surface colouring is a preference it
applies to the Real Molecules surface only, and that surface is a per-vertex
MSMS mesh with Psi4 potentials — 400 kB of data this file does not carry. So
that the chip means something and the colour key always matches the surface
above it, the rainbow re-colours the same gradient **position** through PhET's
own `roygb(e)` with e = (0.5 − s)/4, which maps the two ends of the ramp onto
the two ends of the gradient. The blue-white-red path is PhET's `surfaceColour`
untouched, asserted identical over 205 (ΔEN, position) pairs, and the canvas
says which scheme is PhET's and where PhET applies it.

**Suites.** `selfTest` 914/0 (about 0.5 s). UI drive 389/0
(`build/molecule-polarity/ui_drive_molecule-polarity.js`). Display-list
capture: 30 configurations, `audit.py` 0 layout problems, every PNG looked at.
69 mutants (59 physics, 10 UI), every anchor checked unique by
`gen_mutants.py`. Measured, not assumed: a 27-mutant spot check during the
build caught 24 and left 3 survivors; the full 69-mutant sweep on the shipped
file then caught 68 and left 1. All four survivors were real test gaps, are
written up below, and were re-run individually after the fix — the last one
with its five nearest neighbours, 6 caught / 0 survived. The definitive full
sweep after these fixes is the coordinator's, not a number measured here.

### Fixed (during the build)
- **The real-molecule view drew its molecules at half the size the fit asked
  for.** Symptom: water occupied about a fifth of a 1038 × 660 stage and its
  labels piled on top of each other. Root cause: the camera distance was fitted
  to `extent × 1.35` while the target fill was `0.80` of the box, so the two
  paddings multiplied — the *padded* extent filled 80 %, leaving the molecule
  at 0.80/1.35 = 59 % of that. Fitted to `extent × 1.04` at 0.94 fill, and the
  camera now aims at the **centroid** while PhET's origin atom stays the origin
  the dipoles are drawn from, so an off-centre molecule (HCN, formaldehyde) is
  not pushed against one wall.
- **Three label placements that the layout audit could not see.** The audit
  only inspects text-against-text, so a label sitting on a *ball* or on an
  *arrow* passes it. (a) The triatomic's central-atom charge label was placed
  8 px from the atom centre, i.e. underneath the atom, because the outward
  direction was computed as `(P − B)` for B itself and collapsed to the
  fallback; it now goes along the outward bisector, pushed 30 px across the
  molecular dipole that is drawn along that same line. (b) At a 180° bond angle
  the bisector is degenerate and the fallback put the label into the
  bond-angle arc; it now goes straight up, and the 30 px side-step is dropped
  because there is no dipole to avoid. (c) The real view's molecular-dipole
  label chased the arrow head into the central atom; it is now a fixed legend
  at the top of the box.
- **Every plot view failed its own "draws substance" floor.** Symptom: the
  three plot views reported 3–6 fills against a floor of 8. Root cause: the
  floor counted `fill()` operations, and a line plot is made of `stroke()`s —
  the check was measuring the wrong thing, not a thin drawing. The floors are
  now on total ops (measured per configuration, set ~20 % below), with
  `texts ≥ 1` and `fills ≥ 1` kept as separate conditions.
- **Four entities reached `fillText` verbatim.** `&psi;`, `&zeta;`, `&aring;`
  and `&ouml;` are not in the shared `ENTS` table, and `plain()` returns an
  unknown entity unchanged. The first two are added to the table in
  `make_head.py` (with `&Aring;` and `&xi;`); the ångström is written in ASCII
  instead. Two combining diacritics (`&#775;`, `&#776;` — the dots of ψ̇ and
  ψ̈) were removed from canvas strings altogether and written `dψ/dt`; they
  stay in the HTML panels, where a browser composes them properly.
- **A colour chip that changed the key and not the surface.** Symptom: picking
  the rainbow scheme drew a rainbow colour key above a blue-white-red surface.
  Root cause: PhET's preference only reaches a surface this file does not ship,
  so the chip had nothing to act on and the key was drawn from the preference
  while the surface was drawn from the fixed RWB stops. The gradient position is
  now re-coloured through PhET's own rainbow mapping (see above), and the two
  always agree.
- **Charge labels over a pale surface lost their contrast.** The house accents
  (orange for δ+, cyan for δ−) are chosen against a #070b18 background and are
  nearly illegible on PhET's white-centred surface. They are mixed 62 % toward
  the background colour whenever a surface is drawn, which keeps the hue that
  carries the sign.
- **A surviving mutant that no picture could ever have caught: `surfacePos`'s
  clamp.** Symptom: deleting `clamp(..., 0, 1)` from the gradient-position
  helper changed nothing in a suite that already asserted the rainbow surface's
  colours at both ends, its midpoint, and its behaviour under a sign flip. Root
  cause: the only consumer feeds the position into PhET's own `roygb(e)`, which
  clamps `(8e+1)/2` to [0, 1] itself, so an out-of-range position lands on the
  same end stop — measured max channel difference **0** over 16 441 samples
  covering every ΔEN on the 0.2 grid and the whole drawn x-range. The clamp is
  nevertheless load-bearing, because the value is a *fraction*: at |ΔEN| = 2 the
  potential gradient is 187.5 wide over a 375-wide surface, so the raw ratio
  runs **−0.5 … 1.5** and 660 of those 16 441 samples (4 %) sit outside [0, 1].
  `selfTest` now asserts the helper's own contract against absolute numbers — 0
  and 1 at the ends, 0 and 1 a million units past them, both surfaces, and the
  span over every sample `drawSurface` takes — **and** asserts the colour
  invariance deliberately, so the redundancy is a stated property rather than a
  blind spot that a later reader might "tidy away".
- **Three mutants survived the spot-check sweep, and all three were real test
  gaps.** *Camera theta frozen* and *camera phi frozen* survived because every
  drag test ran on the **two atoms** view, which rotates the molecule and never
  touches the camera — the camera only exists on the real-molecule view. The UI
  drive now drags each axis separately on that view from a proven-idle
  baseline and asserts both that the drawing moved and that `ST.camTheta` /
  `ST.camPhi` changed. *The electronegativity slider stops snapping* survived
  because the slider's own `step` is already 0.2, so every value the harness
  fed it was already on PhET's grid and the `snapEN` call could be deleted
  unseen; the drive now pushes 3.31 and 2.09 into each of the three sliders and
  asserts they land on 3.4 and 2.0.

### Known-bad candidates
- **A downstream clamp makes an upstream clamp an equivalent mutant — for the
  OUTPUT, not for the contract.** `surfacePos` clamps a gradient position to
  [0, 1]; its one consumer hands that to PhET's `roygb()`, which clamps again,
  so deleting the first clamp changes no pixel anywhere (0 difference over
  16 441 samples) and survives every colour assertion. Exactly the shape of the
  `plain()` numeric-entity entry already on this list. The rule that closes it:
  when a helper's value is a *fraction*, a *count* or an *index*, assert that
  contract directly against absolute numbers — at the limits and past them —
  instead of only asserting what the picture does with it; then assert the
  invariance deliberately so nobody removes the guard believing it is dead
  code. Check first whether the out-of-range region is actually reached: here
  it is, 4 % of the drawn surface at |ΔEN| = 2, and that number is pinned too,
  so if the gradient law ever changes and the clamp stops mattering the suite
  says so.
- **A "draws substance" floor counted in `fill()` operations is blind to a line
  plot.** `polyline`, `axes` and every curve emit `stroke()`, not `fill()`, so a
  perfectly healthy plot view reports 3 fills and a molecule view reports 190.
  A single floor cannot serve both. Count total ops per configuration, measure
  the floors from a run rather than guessing them, and keep `texts ≥ 1` and
  `fills ≥ 1` as separate conditions so a genuinely blank view is still caught.
- **Two independent paddings applied to the same camera fit multiply.** Fitting
  the distance to `extent × k` and then asking the projection to fill a
  fraction `f` of the box leaves the subject at `f/k` of the box, not `f`. In
  this build `f = 0.80`, `k = 1.35` put the molecule at 59 % of what was asked.
  Choose one padding, or state the product.
- **A drag test on a view with no camera in it cannot catch a frozen camera.**
  Both camera mutants survived a UI drive that dragged only the first tab. When
  the same gesture drives different state on different views, every one of those
  states needs its own drag test — asserting on the *state variable*, not only
  on "the picture changed".
- **A constrain-on-input rule is invisible to a harness that only feeds it legal
  values.** The electronegativity slider's `step` attribute is PhET's snap
  interval, so the sweep never produced an off-grid value and deleting the snap
  changed nothing any test could see. Any clamp, snap or round on an input has
  to be driven with a value that violates it.
- **A layout audit that inspects text against text is blind to text on a ball or
  on an arrow.** Three labels here sat on top of the drawing with the audit
  reporting zero collisions. The PNGs are the only check for that, and they have
  to be looked at.
- **PhET's Molecule Polarity real-molecule geometry is PubChem's, not the
  measured one.** H–O–H 97.92° against 104.48° and H–N–H 95.08° against 106.67°.
  Anything quoted from that table as "the measured geometry" is wrong; PhET's
  *Molecule Shapes* table, which does carry measured angles, is a different data
  set in a different sim. Check which one a number came from before reusing it.
