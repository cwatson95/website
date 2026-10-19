## 2026-09-21 — diffusion: PhET's Diffusion screen, with the mixing bracketed between its two limits and the flow measured against kinetic theory

### Added

`docs/phets_revised/diffusion.html` (180 KB, 3156 lines), a clean-room remake of
PhET Interactive Simulations' **Diffusion** 1.1.7 (CC-BY 4.0; new code, no PhET
code or assets). Built on the finished `gas-properties` remake: the
event-driven hard-disk engine (`build/gas-properties/p2_engine.js`, documented
in its `ENGINE.md`), the shared house layer, the drawing helpers and the
container/plot layer are taken **unchanged** by `make_shared.py`, which asserts
every block it slices.

**Four views of one experiment.** PhET's Diffusion is a single screen, so all
four views share one gas and one clock — the tabs change the instrument, not the
run. `the divided box` is PhET's screen; `the mixing` adds the concentration
profiles and the left–right imbalance between its two limits; `the flow`
measures the crossing rate and the pair-collision rate against kinetic theory;
`the speeds` watches PhET's one-speed start relax to Maxwell–Boltzmann.

**What is exact.**

- PhET's constants and control grids, read out of `docs/phets/diffusion_en.html`:
  BOLTZMANN 8316, KG_PER_AMU 1.66e-27, ATM_PER_KPA 0.00986923; `widthRange
  new B(16e3,16e3,16e3)` and `dividerThickness = 100`;
  `DIFFUSION_NUMBER_OF_PARTICLES_RANGE new B(0,200,0)`, `MASS new B(4,32,28)`,
  `RADIUS new B(50,250,125)`, `INITIAL_TEMPERATURE new B(50,500,300)`; and
  `DELTAS {numberOfParticles:10, mass:1, radius:5, initialTemperature:50}`.
- **Each species' centre of mass starts at exactly −(W + d)/4 = −4025 pm from
  the middle, independent of the particle radius.** PhET scatters species 1
  uniformly in [left, mid − d/2] and the engine keeps centres a radius inside,
  so the occupied interval is [left + r, mid − d/2 − r] and its midpoint loses
  the r: both ends move in by the same amount. Asserted at r = 50 and r = 250,
  and measured over 24 fresh boxes against the sampling spread L/√(12N) = 222 pm
  (itself checked against 4000 Monte-Carlo draws).
- The one-sided flux ⟨vₓ⁺⟩ = √(kT₂/2πm) by scipy quadrature, and ⟨vₓ⁺⟩ = ⟨v⟩/π
  exactly. The crossing rate is n⟨vₓ⁺⟩(H − 2r); the height cancels, leaving
  N⟨vₓ⁺⟩/(W/2 − r) — 1.852/ps for 100 heavy at 300 K, 4.878/ps for 100 light,
  their ratio Graham's √(m₁/m₂) times the excluded-width ratio.
- **The imbalance is not a single exponential, and the reason is physical.** The
  two-box effusion model gives τ = (W − 2r)/4⟨vₓ⁺⟩ = 27.0 ps and assumes each
  half stays internally mixed. With collisions **off** nothing mixes them and
  the decay is ballistic: `derive.py` computes that curve exactly from four
  million folded trajectories (ΔN/N = 0.8325, 0.6437, 0.2863, 0.0115, −0.0006 at
  5, 10, 20, 40, 80 ps, against the effusion model's 0.8309, 0.6905, 0.4767,
  0.2273, 0.0517), and `selfTest` runs the simulation with collisions off and
  reproduces it. With collisions **on** the box is 22 mean free paths across and
  the Fickian estimate τ_D = W²/π²D, D ≈ ⟨v⟩λ/2, is 5.8 times the effusion time.
  Both are drawn, both are labelled, and the sim does not claim a diffusion
  coefficient it has not derived.
- The mixture's collision frequency z_k = Σⱼ nⱼ 2(r_k + rⱼ) ⟨v_rel,kⱼ⟩, with
  ⟨v_rel⟩ = √(π/2 · (kT₂ᵏ/m_k + kT₂ʲ/mⱼ)) checked against two million
  Monte-Carlo velocity pairs and reducing to √(πkT₂/2μ) at equal temperature and
  to √2⟨v⟩ for identical disks. It predicts **73.4 pair collisions per ps** in
  the default box; the simulation counts 74.2.
- PhET's start is a delta in speed (every particle at √(3kT/m) = the rms), so
  relaxing to Maxwell–Boltzmann at constant energy must multiply the mean speed
  by exactly √(π/4) = 0.886227 — an 11.377 % fall, the same for any mass.
  Measured for both species. Two species started at different temperatures reach
  the number-weighted mean.

The only canvas gesture PhET's Diffusion screen offers is Remove Divider, so it
is given as a handle on top of the divider: lifting it the full travel takes the
divider out, anything less snaps back, and the bar is **never** drawn short
while it is still in the model — a gap the particles do not use would be a lie.

`selfTest` **523 passed, 0 failed** (11.6 s); UI drive **128 passed, 0 failed**;
mutation sweep **64 mutants (54 physics, 10 UI), 64 caught, 0 survivors** — the
first pass left 6 alive and all six are written up below
(`_out/mutation_log.txt`, then `mutation_log_fix.txt` and
`mutation_log_final.txt`, the last of which is the sweep of the file that
ships). `derive.py` writes `refvals.txt` and `p7a_refs.js`, so no pinned value
is retyped.

### Fixed (during the build)

- **The collision-frequency derivation was a factor of 2 low, and the simulation
  found it.** The first draft of `derive.py` wrote z_k = Σⱼ nⱼ (r_k + rⱼ)
  ⟨v_rel⟩, which predicted 36.7 pair collisions per ps; the engine's own pair
  counter measured 74.2 over a 10-ps window — a ratio of 2.05, far outside any
  counting error. Root cause: the **swath width**. Two disks collide when their
  centres come within d = r_k + rⱼ, so a moving disk sweeps a strip of
  *half*-width d — width 2d, not d. (Check it in 3-D, where the same argument
  gives a cylinder of radius d and the textbook cross-section πd² with d the
  *diameter*.) Corrected everywhere: z, the mean free path (λ = 1/(2√2 nσ) for
  one species, now cross-checked against the mixture formula with the other
  species absent), D, τ_D, and the on-canvas numbers. The corrected theory is
  within 1.1 % of the measurement, and the halved form is now a named mutant.
  **This is what a measurement view is for**: a derivation nobody measures is
  just a formula on a page.
- **The "no overlaps" invariant was being tested against PhET's own overlapping
  placement.** The first version filled the box with `gasScatter` at 200 + 200
  disks of 250 pm — an area fraction of 0.56, where PhET's no-rejection
  placement starts hundreds of overlapping pairs, which the engine deliberately
  lets pass through each other. The test was therefore measuring the documented
  overlap *rule*, not the dynamics. Split in two: the dynamics are checked from
  a non-overlapping `gasFill` at η = 0.14 (400 disks, 2 ps, every pair every
  frame, closest approach > −1e-6 pm), and PhET's placement gets its own
  assertion that it *does* start overlapped and that those disks pass through
  each other with the energy untouched.
- **The Maxwell–Boltzmann bin probabilities disagreed with `derive.py` by up to
  3.8e-4 in the tail.** Root cause: catastrophic cancellation, not physics —
  the page computes F(hi) − F(lo) as two `expm1` calls and the derivation
  computed it as two `exp` calls, and at a bin probability of 6e-14 the two
  differ in every digit. `derive.py` now writes the bins the way the page does,
  and the assertion carries an absolute floor as well as a relative one.
- **The relative-momentum tolerance was normalised by a quantity that can
  cancel.** Dividing the momentum change by |Σp| fails when the two disks
  happen to nearly cancel. Normalised by the momentum *carried*
  (Σ m(|vₓ| + |v_y|)) instead; the worst error over 5000 random collisions is
  then below 1e-15.
- **A legend collided with a y-axis tick, and the label registry could not see
  it.** `axes()` draws its tick labels without registering them, so `lab()`'s
  overlap avoidance has nothing to avoid; a right-aligned legend inside the plot
  box therefore sat on the "120" of the axis. Moved to the left edge inside the
  box, where the ticks are outside.
- **`restart` kept whatever divider state was current.** Pressing `r` after
  lifting the divider out restarted with no divider, which is not what PhET's
  reset does and made the run unrepeatable. `restart` now puts the divider back.
- **The flow arrows were drawn under the tab bar.** They sat at
  `G.yT − 12` and `− 24` with a label at `− 38`; the scene starts at
  `stageTop() + 30 = 76`, so the label landed at y = 38 and the tab bar owns
  everything above `stageTop() = 46`. Invisible to the display-list audit,
  which only checks the canvas bounds — the rasterised PNG is what showed it.
  The arrows are now inside the top of the box, and the divider handle's travel
  was cut from 60 px to 34 for the same reason.
- **Three in-plot labels were struck through by the very curves they
  annotated, and three more covered the first 200 px of a trace.** The audit
  cannot see either (it compares text boxes with text boxes), so again the PNGs
  were what showed it. All in-plot keys now go through `keyAt()`, which paints
  a patch of the canvas ground first — the same trick `plotNote` already used —
  and `keyText()` takes the corner to sit in, chosen per plot: the imbalance
  key went to the bottom left (every curve there starts at 1 and decays), the
  centres-of-mass key to the middle (its two traces start at the top and the
  bottom, so only the reference line is covered), and the mean-speed key to the
  middle (the light species runs along the top).
- **Empty panels were a sentence floating in blank canvas.** `emptyNote` draws
  the note and nothing else, so the flow view with the divider in was two
  thirds empty stage with two lines of text in it. `emptyPanel` draws the frame
  too, and the panel reads as a chart waiting for data.
- **The concentration profile's key sat on the profile.** Its axis headroom was
  1.2× the tallest slice, and a half-mixed state reaches 11 of 12; 1.35× now.
- **The flow view looked wrong and was right.** The measured crossing rates
  exceed the flux built from the current side counts while the gas is still
  settling, for two reasons worth stating rather than hiding: the bars are a
  300-frame (12.5 ps) average of a state that is still changing, and a particle
  that has just crossed the line is still beside it and often crosses straight
  back, so the count exceeds what a uniform half would give. The caption now
  says so and the panel carries a one-line note.
- **The pair-collision panel had the same problem with a different cause, and
  it is the sharper one.** With one species only, 15 ps after the divider comes
  out the disks are still bunched in the left half, and they meet each other
  where they actually are — 60 % more often than
  Σⱼ nⱼ 2(rᵢ+rⱼ)⟨v_rel⟩ with n the BOX-AVERAGE density predicts. That is 5 σ,
  and reads as a wrong formula unless the panel says otherwise. It now prints
  "not uniform yet: theory uses the box-average density" whenever the gap
  exceeds 3 σ. (The default two-species box, where both species have spread,
  agrees to 6 %.)

**The mutation sweep.** 58 of 64 caught on the first pass; all six survivors
were missing assertions of the same two kinds. Three were **engine functions
this sim does not happen to use** — `GAS.STEP`, `gasPressureOf` (PhET's
Diffusion screen has no gauge) and `mbModeSpeed` — which are now pinned anyway,
because this suite re-asserts the shared engine and inert is not the same as
free to drift. Two were **values asserted off a retyped formula instead of off
the built model**: Graham's ratio was checked as `Math.sqrt(28/4)` rather than
as `buildModel().graham`, and the common temperature was only ever checked with
equal counts, where the number-weighted mean and the plain mean coincide (it
now uses 100 at 500 K with 50 at 100 K, where they differ by 67 K). The sixth
was the profile's bin count, whose test was written in terms of `NPROF` and so
moved with it; the binning is now pinned absolutely — 32 bins of 500 pm, with a
particle placed a hair right of the middle asserted to land in bin 16.
**64 caught, 0 survivors.**

### Known-bad candidates

- **In 2-D, the collision swath is 2(rᵢ + rⱼ) wide, not (rᵢ + rⱼ).** The
  natural-looking `n σ ⟨v_rel⟩` halves every collision rate, every mean free
  path is doubled, and every diffusion coefficient is doubled with it. The
  giveaway is a measured rate at almost exactly twice the prediction. The 3-D
  analogue is the familiar one: the cross-section is πd² with d the *diameter*,
  not πr².
- **Do not test a no-overlap invariant on a configuration whose own placement
  overlaps.** PhET's Diffusion placement has no rejection, and the engine's rule
  is that overlapping disks pass through each other until they separate. A
  "disks never overlap" assertion started from that placement is testing the
  rule, not the dynamics, and fails for the right reason in the wrong place.
  Start non-overlapping (`gasFill`), and assert the overlap rule separately.
- **A tail probability is where two libraries' `exp` and `expm1` part company.**
  F(hi) − F(lo) written as `exp − exp` and as `expm1 − expm1` agree to rounding
  at p ~ 1 and disagree by parts in 1e4 at p ~ 1e-14. Write the reference the
  way the implementation writes it, and put an absolute floor on the tolerance.
- **`axes()` does not register its tick labels with the `lab()` registry**, so
  the registry cannot shift a label out of a tick's way. Anything placed inside
  a plot box on the same side as the y-axis labels will collide unnoticed by
  the label logic — the display-list audit is what catches it. Put in-plot
  legends at the left edge, inside the frame.
- **A drag affordance must never draw a state the model is not in.** Lifting the
  divider handle part way shows the handle moving and nothing else; drawing the
  bar retracting would show a gap the particles are still confined by. Move the
  handle, switch the model at the threshold, and snap back otherwise.
- **The house stage begins at `stageTop() + 30` and the tab bar owns everything
  above `stageTop()`.** Anything a view draws *above* its scene — flow arrows,
  a handle with travel, a callout — has 30 px to work in and will otherwise
  land under the tabs. The display-list audit cannot see it (the ops are inside
  the canvas, just hidden by HTML that sits over it); only the rasterised PNG
  shows it. Draw above the scene only within that 30 px, or draw inside it.
- **The layout audit compares text with text, so a curve or a reference line
  running through a label is invisible to it.** Every in-plot annotation should
  paint a patch of the canvas ground first (`plotNote` already did; `keyAt`
  now does it for keys and callouts). The PNGs are the only check that catches
  this, which is why the brief says to look at them.
- **A quantity the sim never displays can still be wrong, and the shared engine
  is exactly where that happens.** `gasPressureOf`, `GAS.STEP` and
  `mbModeSpeed` are all but inert in this sim, so three mutants of them
  survived a 64-mutant sweep. A suite that re-asserts a shared engine has to
  pin what it re-asserts, not only what its own views read.
