# Changelog — phets_revised

Remakes of the 46 PhET Interactive Simulations kept in `docs/phets/` (the
official builds, left untouched as the originals), rebuilt as single-file sims
in the house style of `projects/simulations/` (its `PLAYBOOK.md`). New code; no
PhET code or assets. PhET's sims are CC-BY 4.0 (University of Colorado
Boulder), and every remake credits its original in the header and on the page.

Layout: `<stem>.html` per remake (the PhET file name minus `_en.html`);
`build/<stem>/` holds its part files, Python twin and test harnesses;
`build/BRIEF.md` is the brief every build followed; `build/_survey/` holds the
decoded inventory of the originals. Generated artifacts go to
`build/<stem>/_out/`, which is gitignored.

Dated entries, newest first. The Known-bad list is permanent — check it before
editing or resurrecting files.

## Known-bad — do not reintroduce
- **The site-nav links are absolute (`https://cooper-watson.net/…`) on purpose.**
  The house sims' relative `../website/` and `../modules/` hrefs are dead from
  `docs/phets_revised/`. Do not "restore" the relative form.

## 2026-09-23 — atomic-interactions: two atoms, the Lennard-Jones well between them, and the motion it produces

### Added

`docs/phets_revised/atomic-interactions.html` (175 KB, 3238 lines), a clean-room
remake of PhET Interactive Simulations' **Atomic Interactions** (build 1.2.21,
`docs/phets/atomic-interactions_en.html`). Six views: **the two atoms** (PhET's
single screen — a pinned atom, a draggable one, the seven pairs, the potential
curve sharing the atoms' own r axis, PhET's hidden/total/components force
arrows, Return Atom), **the well** (V and F = −dV/dr with their three exact
landmarks and the residual against a numerical derivative), **the motion**
(r(t), the exact turning points, the energy ledger, the phase portrait and its
E = 0 separatrix), **small oscillations** (the harmonic fit and how fast the
period leaves 2π/ω), **the atom pairs** (PhET's seven wells against the
literature's, the combining rules), **the integrator** (the order and the
boundedness of three time-steppers).

**Exact, and pinned to `build/atomic-interactions/derive.py`** (963 selfTest
assertions, 421 UI-drive assertions; 88 mutants, all caught):

- V(r) = 4ε[(σ/r)¹² − (σ/r)⁶]; V(σ) = 0 and V(2^(1/6)σ) = −ε to machine
  precision; values pinned at eight multiples of σ for two pairs.
- F(r) = −dV/dr = (24ε/r)[2(σ/r)¹² − (σ/r)⁶], checked **three ways**: the
  closed form, a 60-digit `Decimal` Richardson-extrapolated central difference
  (the definition of a derivative), and `scipy.differentiate.derivative`. Worst
  disagreement 4.3e-15 of the force scale 24ε/r. Same treatment for V″.
  PhET's own halves (48ε′σ¹²/r¹³ and 24ε′σ⁶/r⁷) are reproduced and asserted to
  difference to exactly −dV/dr.
- V″(r_min) = 72ε/(2^(1/3)σ²) exactly, and the strongest pull at
  (26/7)^(1/6)σ = 1.2444550602598 σ, confirmed against a 4001-point scan.
- ω = √(V″(r_min)/μ) with the reduced mass: the movable atom's own mass while
  the other is pinned (PhET's default), m₁m₂/(m₁+m₂) when both move — which
  shortens a like pair's period by exactly √2, asserted.
- The turning points of a bound orbit in closed form: with u = (σ/r)⁶ the
  condition V = E is a quadratic, so u_in + u_out = 1 exactly.
- The period by **three independent routes**: a regularised Gauss–Legendre
  quadrature, velocity-Verlet integration of the real trajectory (they agree to
  5e-7 at 8000 steps per period), and 2π/ω in the small-amplitude limit — which
  the quadrature approaches at the rate Landau & Lifshitz's anharmonic formula
  predicts, T = T₀[1 + (91/4)a²/r_min²]. The 91/4 is derived, not fitted: the
  LJ well's Taylor coefficients at its minimum are exactly 72, −1512 and 26712
  in units of ε/r_min^n, checked by 90-digit finite differences, and Landau's
  κ = ω₀(371/16 − 2205/48)/r_min² follows. Measured/predicted = 1.000000 at
  a = 0.03 pm and 0.99997 at a = 2 pm.
- Velocity Verlet: measured order **1.99999**, energy error **bounded** (20
  periods cost no more than one, to 1e-9). PhET's own stepper (semi-implicit
  Euler) measured at order 1.00161 and also bounded; forward Euler measured at
  1.01 over one period and 275× worse over 100.
- Constants from `scipy.constants` (CODATA 2022) — k_B, m_u, e — and the unit
  system pm/ps/u, in which speed is m/s exactly.

**Modelled, PhET's choices reproduced and cited as PhET's:** its ε/k_B table
(35.8, 111.84, 1000, 59.5, 51, 85 K), its σ table (308, 376, 200, 343, 306,
340 pm), the van der Waals radii (154, 188, 152 pm) and masses (20.1797,
39.948, 15.9994 u) from its `nitroglycerin` element table, the adjustable
pair's 75–500 pm and 20–450 K sliders snapped to 5, and its Return Atom.

**Literature values beside them, both retrieved and cited in the file:** Ne and
Ar (σ 278.9 / 341.8 pm, r_min 313.1 / 383.7 pm, ε/k_B 35.7 / 124.0 K) from
Attard, arXiv:1702.00096 Table I, after van Sciver, *Helium Cryogenics* 2nd ed.
(Springer 2012); Ar and O₂ (σ 343.2 / 343.3 pm, ε/k_B 122.4 / 113 K) from Bird,
Stewart & Lightfoot, *Transport Phenomena* 2nd ed. (2007) pp. 864–865. Argon
has two retrieved sets 1.31 % apart in ε; that spread is printed as the honest
uncertainty. **The sim uses PhET's values by default** so that it reproduces
PhET, with a "literature ε, σ" switch; which set is live is on every canvas.

**The finding the comparison view exists for:** PhET's σ is the literature
**r_min**, not the literature σ. 308 pm against 313.1 (−1.6 %) for neon and 376
against 383.7 (−2.0 %) for argon, where the literature σ is +10.4 % and +10.0 %
away — because PhET sets σ = twice the van der Waals radius, and a van der
Waals radius is measured at the bottom of the well, a factor 2^(1/6) = 1.1225
further out. PhET's wells are therefore about 12 % too wide. The oxygen pair
matches nothing: 1000 K and 200 pm against the literature's 113 K and 343 pm
and against **PhET's own** States-of-Matter constants (113 K, 365 pm), and at
200 pm the minimum lies 79 pm inside the two drawn spheres, which the
two-atoms view shows and the readout states. The source table checks itself:
its printed r_min/σ reproduces 2^(1/6) to 1.6e-4 for all three of its rows.

### Fixed (during the build)

- **A pin copied from an earlier run of the twin is a pin against superseded
  code.** Three of the seven period pins were taken from a `refvals.txt`
  written before the quadrature was regularised, and disagreed with the JS by
  1e-11 … 9e-10 — at exactly the small amplitudes where the *old* integrand was
  wrong. Re-read the file after every change to `derive.py`; the JS was right
  and the pins were stale.
- **`E − V(r)` formed as a difference is catastrophic cancellation over most of
  a small orbit, and the fix is closed form, not a tolerance.** With
  u = (σ/r)⁶ and u_in + u_out = 1, E − V = 4ε(u_in − u)(u − u_out); factoring
  x⁶ − y⁶ = (x − y)Σxᵏy⁵⁻ᵏ against the substitution r = a − b cos θ leaves an
  exact sin θ that cancels the dr = b sin θ dθ of the numerator. The integrand
  is then analytic **and** cancellation-free, converging by n = 96 panels. The
  naive form is 1.6e-4 wrong at a = 0.002 pm and fine at a = 7 pm; `selfTest`
  asserts it is **still** bad, so the regularisation cannot be quietly replaced
  by the obvious integrand.
- **Four reference values were pasted out of a table printed for reading.**
  `derive.py` prints its comparison section at 4–6 significant figures; four
  pins (the Ne–Ar reduced mass, two σ ratios and the Berthelot mean) were typed
  from those rounded numbers and failed at 1e-4 … 1e-7. A number that was
  rounded for a human to read is a number nobody computed. `derive.py` now
  prints a section 11 at `%.17g` for exactly the values `selfTest` quotes.
- **A geometry rebuilt at a different stage height maps r somewhere else.** The
  two-atoms drag test built its hit geometry at 1100×700 while the scene's own
  H was 712; once the axis origin came to depend on the band height (see the
  next entry) the two mappings differed by 0.4 pm and the follow-the-pointer
  assertion failed. Build the geometry from `S.W`/`S.H`, never from literals.
- **The pinned atom was drawn half off the stage.** Its centre is r = 0, the
  left edge of the axis. The axis now starts at −1.06 × the drawn radius, which
  depends on the scale, which depends on the span — resolved by two passes,
  each of which only shrinks the atom.
- **A band sized from the atom's diameter but with its centre at 0.56 of the
  height let the atom overflow the band and land on the graph title below.**
  Centre the band and size the reduction from the *smaller* half, with room for
  the two force labels above the atom.
- **An arrow clipped at a fixed 420 px still left the stage.** A 46 pN
  attraction at 28.9 px/pN is 1338 px; clipped to 420 it still ran off the
  left-hand edge. The cap is now min(300 px, 0.36 of the panel) and a clipped
  arrow gets a chevron at its tip, so a cut arrow cannot be read as a short one.
- **An op count is not a proxy for "the arrow appeared".** The UI harness
  compared the op count with the forces hidden against the count with them
  shown, and the count went *down*: the hidden state's note is a different
  sentence, so it wraps to more text ops, which shortens the graph, which
  changes its tick count. Even a stroke count moved the wrong way. The test now
  looks for the arrow itself — a stroked path along the band's centre line,
  which nothing else in that view draws — and asserts exactly one for TOTAL,
  none for HIDDEN and two eleven pixels either side of the centre for
  COMPONENTS.
- **A force axis fitted to the repulsive wall hides the attraction it exists to
  show.** The wall reaches 130 pN where the deepest pull is 3.85 pN, so the
  minimum was a flat line on the axis. Fit the axis to the attractive extreme,
  let the wall run off the top, and say so on the canvas.
- **An energy ledger fitted to the whole well shows none of the trade.**
  Released 10 pm out, K only ever reaches 0.025 ε; a −1.15 … 0.35 axis made
  both curves flat lines. Fit the three curves.
- **A legend entry for a curve that was not drawn is a false statement about
  the picture.** The motion view named "this orbit (closed)" and "turning
  points (exact)" for an *unbound* release, which has neither. Both legends are
  now built from what was emitted.
- **A caption note anchored below a panel collides with whatever is under the
  panel, and a hard floor on the shrink hides it.** Notes are now measured
  first, the panel is shrunk by the measured height, and the note is drawn only
  if the room was actually available — otherwise a short form, otherwise
  nothing. What it must stay above is the stage caption when there is no bottom
  row and the bottom row's own title when there is.
- **`axes()` draws the leftmost x-tick label and the lowest y-tick label in the
  same corner and neither knows about the other.** Found twice at
  σ = 500 pm, where both axes start on round numbers. Fixed by a `noCornerTick`
  helper that drops a floor when a tick lands on it, plus 6 % of x margin on
  the two bottom panels.
- **Two stacked panels under ~110 px each put their rotated y-axis titles on
  top of one another whatever the gap**, because a rotated title is as long as
  its text and is centred on its panel. The integrator view now draws one panel
  on a narrow stage — the boundedness one, which carries the point — and names
  the orders it is no longer plotting.
- **A panel that cannot place a legend says nothing about its colours.** With
  three curves across a narrow box (and with seven wells on one axis)
  `legendAuto` correctly draws nothing; each curve is now tagged at its own end
  (or at its own minimum) when, and only when, no legend was placed.
- **Entities in a control label are drawn literally.** `h()` appends child
  strings as text nodes, so `'left atom pinned (PhET&rsquo;s)'` would have
  rendered the entity verbatim in a browser — the canvas rule, one layer out.
  Three labels fixed; the UI harness now scans every panel label, button and
  heading for `&word;` and `<tag>`.
- **A step count derived from a period is only as finite as that period.** A
  mutant that broke the turning points would have given the integrator view
  `Math.round(Infinity/dt)` steps and hung the sweep for days. The quadrature
  period now falls back to the harmonic one, `energyExcursion` clamps to
  `MAX_STEPS`, and `selfTest` asserts both — a bound that is computed and not
  applied is not a bound.
- **A drag test that pumps only after `pointerup` passes with the move
  handler's dirty flag deleted**, because `pointerup` calls `refresh()`
  unconditionally. The test now proves the loop idle with the atom grabbed and
  unmoved, then asserts the *move* repaints. Its partner is the discriminating
  case: a purely vertical drag must leave the separation alone, which a handler
  reading the wrong axis fails.
- **Every assertion that touched the drawn r window was written in terms of the
  constant under test, so the window was pinned by nothing.** Found by the full
  82-mutant sweep, which reported one survivor: `R_LO_FAC` 0.72 → 0.50. Three
  assertions read `R_LO_FAC * sigma` / `R_HI_FAC * sigma`, which move with the
  constant, so the suite could not see it. **The mutant is not equivalent.**
  Measured (`_out/probe_window.py`, both variants run under `jsc` and their
  display lists hashed): the inward end of a drag moves 221.76 → 154.00 pm for
  neon (270.72 → 188.00 argon, 144 → 100 oxygen), and the wall the atom is
  pushed against goes from **177.384 ε to 16128 ε**, 91 times deeper. It is
  invisible to the *picture* for a reason worth stating: the plot box runs to
  V/ε = 2.4, which the curve reaches at r = 0.943016 σ, so every sample below
  that is clipped away by `polyline` — six of eight captured views hash
  identically under the mutant and the two two-atoms views differ only in where
  their 261 samples fall. The window floor is a **drag** contract, not a
  drawing contract, which is why no picture check could ever have caught it.
  Closed by pinning, off the built model and in absolute picometres: both ends
  for all seven pairs, what an inward and an outward drag land on, that the
  drawn curve's first and last samples *are* those two ends and are evenly
  spaced between them, that V at the floor is 177.384 ε (the only reason 0.72
  is 0.72) against 16128 ε at half a sigma, the clip radius 0.943016 σ in
  closed form, and — deliberately — the invariance itself, that both floors lie
  inside the clipped region. Plus: no release setting comes within 40 pm of the
  floor, so the floor is reachable only by dragging.
- **The same blind spot, swept for rather than patched once.** Six more
  constants appeared only inside assertions written in terms of themselves:
  `R_HI_FAC`, `MAX_STEPS`, `PS_PER_SEC`, `SLOW_FACTOR`, `DT_INT` and
  `TRAIL_MAX` (the UI drive's slow-switch check read
  `|t_slow/t − SLOW_FACTOR| < 1e-9`). Each now has one absolute pin and, where
  there is a reason for its value, an assertion of that reason —
  `MAX_STEPS` above the longest run any view asks for, `DT_INT` under 2 % of
  the shortest period the pairs reach, and the trail proved to grow one sample
  a frame and stop at exactly 900. Six new mutants cover them; all six are
  caught.

### Known-bad candidates

- **A constant asserted only in terms of itself is pinned by nothing, and the
  mutation sweep is the only thing that will tell you.** `rel(ST.r,
  R_LO_FAC*sigma, …)` moves with `R_LO_FAC`, so it is a tautology wearing the
  shape of a test. Seven constants in this file were in that state and one of
  them survived an 82-mutant sweep. The rule that closes it: **every constant
  needs one pin that does not mention it** — an absolute number, off the built
  model — and, where the value was chosen for a reason, an assertion of the
  reason (a wall depth, a margin above the longest run, a fraction of the
  shortest period). Grep the suite for each constant's own name before
  believing it is covered.
- **"Invisible to the picture" is not "equivalent" — measure before deciding.**
  The window floor changed no pixel in six of eight views, which is exactly the
  argument for calling a survivor equivalent and moving on. It moved a
  *reachable* contract: what an inward drag is allowed to reach, and a wall
  91 times deeper. Run both variants, hash the display lists, and enumerate
  what each control can now reach; then assert whichever half is real and
  assert the invariance for the other half deliberately, so the next reader
  knows the silence was checked rather than assumed.
- **A quantity clipped out of the plot cannot be defended by looking at the
  plot.** Anything below r = 0.943 σ here is above the box ceiling and is
  discarded by `polyline`'s data-space clip, so the whole of the window floor's
  neighbourhood is unobservable in the picture by construction. When a
  parameter lives in a region the drawing throws away, the assertion has to be
  on the model or the interaction, never on the canvas.
- **A reference value printed for reading is not a reference value.** A twin
  that prints `%.6g` for a table and `%.17g` for its pins needs both, and the
  pins must come from the second. Four wrong pins in one build, each of them a
  plausible-looking number.
- **A pin is against a *version* of the twin.** After changing the twin's
  method — not merely its inputs — re-read `refvals.txt` in full before
  trusting any pin already pasted. Three period pins survived a regularisation
  that changed the values in their tenth digit.
- **Removing a cancellation is a closed-form problem, not a tolerance
  problem.** Where two quantities agree to fifteen digits over most of a
  domain, factor the difference analytically; and keep the naive form with an
  assertion that it is *worse*, or the next reader will simplify it back.
- **Counting canvas ops to prove a feature appeared measures the captions
  too.** A longer note wraps to more lines, shortens the panel and changes its
  tick count, so the op count can move either way. Assert the thing itself.
- **`axes()`'s two corner labels collide and neither knows about the other.**
  The leftmost x tick and the lowest y tick share the bottom-left corner
  whenever both ranges start on round numbers. It is in the shared helper, so
  every sim in this family can hit it; the local remedy is a floor nudge plus a
  little x margin.
- **A rotated y-axis title is as long as its text and centred on its panel**, so
  two stacked panels shorter than the title collide however wide the gutter is.
  Below about 110 px per panel, draw one.

## 2026-09-23 — masses-and-springs-basics: mg/k over every state the sim allows, and the damped oscillator in closed form

### Added
- `docs/phets_revised/masses-and-springs-basics.html` — a clean-room remake of
  PhET Interactive Simulations' **Masses and Springs: Basics** (build 1.0.28,
  CC-BY 4.0). Six views: *the stretch*, *the bounce* and *the lab* are PhET's
  three screens; *the period law*, *the damping* and *the energy* are the
  analysis views. New code; no PhET code or assets.
- **Exact.** The sim advances the state with the **exact propagator** of
  m u″ + b u′ + k u = 0 — u = e^(−γt)[u₀(C + γS) + v₀S],
  v = e^(−γt)[−ω₀²u₀S + v₀(C − γS)] with C = cos(√s t), S = sin(√s t)/√s,
  s = ω₀² − γ², continued to cosh/sinh below s = 0 and to their series at
  s = 0 — so the drawn trajectory is the closed form at any frame rate and in
  every regime, which is also how PhET advances its springs (its doc/model.md
  gives the characteristic equation ms² + bs + k = 0 and its `Spring.step`
  solves it with complex arithmetic). An RK4 of the same equation runs beside
  it in `selfTest` and is **measured** to be fourth order (error ratios
  16.03–16.44 per halving at three dampings); scipy's `solve_ivp` agrees with
  the propagator to 2.4e−12 over 80 (m, k, b) states.
- **Pinned** in `selfTest` (1731 assertions, all against `derive.py`'s printed
  `refvals.txt`): mg/k over all **10040** (mass, spring constant, planet)
  states the sim can reach (checksum 3549.219863636362 m); u and v at four
  times in six (m, k, b) cases including the critical and overdamped ones; the
  propagator's group property; that the solution satisfies its own equation
  (central differences); the C/Sn series **at its join** from both sides;
  T = 2π√(m/k), T_d = 2π/√(ω₀² − γ²), the logarithmic decrement and
  Q = 1/(2ζ); the period **measured** from the drawn motion by bisecting for
  two crossings (1e−12 of the closed form, and amplitude-independent); that
  released from rest the velocity vanishes **exactly** at ωd t = nπ and
  |u_n| = u₀e^(−nδ/2), so E(nT_d/2) = E₀e^(−nδ); that a release from the
  unstretched end swings exactly 2mg/k; energy conservation in the undamped
  limit (5.8e−16 relative over 2000 steps, against RK4's 6.0e−6 at 2000);
  dE/dt = −bv²; and the ledger KE + PE_elastic + PE_gravity constant to 1e−16 J.
- **Which regimes are reachable, stated plainly.** Critical damping needs
  b = 2√(km), which over PhET's own box (k 3–12 N/m, m 50–300 g) never falls
  below **0.7745966692 N s/m**, above the top of its damping range 0.7 — so
  **every state the sim can reach is underdamped**, ζ ≤ 0.9036961141. Swept
  over 7000+ (m, k, b) states in `selfTest`. The damping view runs b past
  PhET's range to draw the critical and overdamped cases and labels them
  "beyond PhET".
- **PhET's data, cited as PhET's**, read out of the minified build:
  gravities Moon 1.6, Earth 9.8, **Planet X 14.2** (its invented mystery value
  — no solar-system body has it; Neptune 11.15 and Saturn 10.44 are the
  nearest), Jupiter 24.8 m/s², slider 0–30; spring constant 3–12 N/m (integers,
  default 6); damping 0–0.7 N s/m; per-screen damping 0.7 / 0 / 0; masses
  250/100/50 g plus mystery 200/100/75 g, lab slider 50–300 g plus mystery
  180/120 g; ceiling 1.47 m, natural length 0.5 m, hook 0.037/0.0185 m, slow
  motion ×1/8; the block size rule r = 4√(m/(80·2.5π)). **PhET's gravities are
  what the sim uses**; the real surface values (1.62, 9.81, 24.79) are printed
  beside them in the readout.
- Verification: `selfTest` **1741 passed, 0 failed**; UI drive **213 passed,
  0 failed** (six tabs, 17 inputs, five chip rows, three real drags through the
  frame loop from proven-idle baselines); `audit.py` 0 layout problems on 25
  captures at 1400×820 and 6 at 820×520; every view's PNG read.
  `mutants.json` holds 82 mutants (70 physics, 12 UI), every pattern verified
  unique. The first full sweep returned **79 caught, 3 survived**; all three
  were diagnosed, fixed and re-checked (below), and the targeted re-run is
  **9 caught, 0 survived** over the three and their six neighbours.

### Fixed (during the build)
- **`legendAuto` takes `[colour, text]` pairs, not `{col, txt}` objects**, and
  the object form drew the literal word "undefined" as every legend label —
  `plain(it[1])` on an object. Symptom: 30-odd "text clean (NaN/undefined)"
  failures across four views; root cause: the item shape was guessed rather
  than read out of `p1_utils.js`.
- **`&zeta;` is not in the shared `ENTS` table**, so it reached the canvas
  verbatim in three captions and the damping legend. Canvas strings now use the
  glyph ζ; the HTML readout and info keep the entity.
- **A stage drawn at true shape is tall and thin, and stacked under a plot it
  used a quarter of the width.** PhET's own geometry is 1.47 m of ceiling over
  0.3 m between the springs, so at equal aspect the drawing was 241 px wide in a
  1000 px box. The three PhET screens now use a two-column layout (`splitLayout`)
  with the stage in a column of its own beside the analysis panel, which
  raised the scale from 2.33 to 3.70 px/cm.
- **The gravitational share measured from the unstretched end put the ledger's
  SUM on the zero line, where it is invisible** — and the five-curve legend was
  dropped entirely because every corner was crossed. The datum moved to the
  bottom of the swing (y_bot = 2mg/k): all three shares are now non-negative,
  the sum is 2(mg)²/k, and a wider top pad leaves the legend a corner.
- **Per-screen damping lived only in the tab handler, so every headless
  configuration ran the Lab screen at the Stretch screen's 0.7.** The lab
  capture showed a motion dying away that PhET's Lab screen does not have.
  `withState` and `capState` now apply `VIEW_DAMPING` exactly as a tab click
  does.
- **A dying exponential keeps changing sign, so the period trace filled with
  crossings long after the spring had visibly stopped** (eight marks across a
  strip at |u| ~ 1e−9 m). A crossing now counts only above 1 mm/s, which is
  what PhET's own `thresholdReached` does.
- **Tick labels with a fixed two decimals collided** ("0.00" five times over a
  0.01 range) and a seven-character energy label ran into the rotated y-axis
  title 34 px to its left. `ax2()` now takes the tick COUNT from the panel size
  and the decimals from the tick SPACING, and the energy axes are in mJ.
- **A selfTest line indexed `prop()`'s return pair as a number** (`prop(...)/
  prop(...)` on two arrays) and reported NaN; and the ODE residual check used a
  relative tolerance where dv/dt passes through zero, so it was measuring a
  cancellation. Both fixed (absolute tolerance at the natural scale).
- **A UI-harness visibility check that reads only the row's own `hidden` flag
  tests nothing**, because `syncPanel` hides whole groups. `visU()` walks the
  tree carrying a hidden-ancestor flag.
- Labels: the spring-constant labels sat on the coils (moved above the ceiling);
  the resting-position labels landed on the blocks and then, hung off the right,
  on the analysis panel beside the stage (they now hang off the LEFT end of
  their own line); the full-width rules start clear of the ruler; the "true
  shape, N px per cm" note moved from the caption's line to the stage's top-left.

- **Two series coefficients and a drawing constant survived the first full
  sweep — all three because of the tests, not the physics.**
  - *The x² terms of the C and Sn series* (`s²t⁴/24`, `s²t⁴/120`) were
    **provably equivalent** at the shipped join: with the branch taken only
    below |s|t² = 1e−8, those terms are worth 4.167e−18 and 8.333e−19 of the
    leading 1, **below half an ulp (1.11e−16)**, so the double came out
    bit-identical with or without them and no assertion anywhere could reach
    them (measured in `_out/diag.py`; the bit-identity is now asserted with
    `eq()` so the fact is on the record). The join moved to |s|t² < 1e−5, where
    the three-term series still matches `cos` and `sin(w t)/w` **exactly**
    (its next term is x³/720 = 1.4e−18) while the x² terms are worth 4.167e−12
    and 8.333e−13 — so the join assertions, tightened to 1e−14, now fail by 83×
    or more on a wrong coefficient. `derive.py` moved with it and `refvals.txt`
    is byte-identical, which is the check that the join is a free choice.
  - *The coil radius* survived because its only test compared the measured coil
    width against `COIL_R` itself — the Known-bad "a test that re-derives the
    thing it is testing". It is now pinned to the **absolute** 0.045 m at two
    sampling rates, and separately **off the display list**: `drawSpring` now
    samples 20 points a turn (so one sample lands exactly on each quarter and
    the drawn peak IS the radius, where 18 a turn gave 0.985 of it) and records
    every edge, and `selfTest` measures the emitted geometry's span as
    2 × 4.5 cm in pixels and its centre on the spring axis.

### Known-bad candidates
- **`legendAuto`'s items are ARRAYS `[colour, text]`.** Passing `{col, txt}`
  objects is silent: `plain(undefined)` renders the word "undefined" as every
  label, and a colour-format check cannot see it. Only a text-content audit can.
- **A ledger whose sum lands on the zero line is a ledger with no visible
  total**, and the legend goes with it (every corner is crossed once the sum
  runs the width of the panel). Choose the potential's datum so the total is a
  positive constant — for a hanging spring, the bottom of the swing.
- **Per-screen state that lives in the tab handler is invisible to every
  headless harness.** PhET gives each screen its own model; a remake that
  applies the screen's value only in `setView` runs `selfTest`, the layout sweep
  and the capture at the wrong value, and the pictures quietly show the wrong
  physics. Put it in one table and have every harness apply it.
- **A damped oscillator's sign changes never stop**, so any crossing counter
  needs a speed threshold or it fills with marks the reader cannot see.
- **A true-shape stage that is much taller than it is wide belongs in a column
  of its own.** Stacking it above a wide plot wastes three quarters of the
  width at equal aspect, and equal aspect is not negotiable when the thing
  drawn IS a shape.
- **A series term below half an ulp over the whole branch it lives in is dead
  code wearing a coefficient, and mutation testing is the only thing that says
  so.** Before adding or keeping a term, compute its size at the TOP of its
  branch against eps/2: if the branch is narrower than the term needs, either
  widen the join until the term is load-bearing (and check the reference values
  do not move, which proves the join was free) or delete the term. Choosing the
  join for "safety" alone buys nothing and hides a coefficient from every test
  that will ever be written.
- **A measured extent compared against the constant that produced it moves both
  sides together.** Pin drawing constants to absolute numbers AND to what they
  control in the emitted display list — and check the sampling first: a helix
  sampled 18 times a turn never visits its own peak, so the measured width is
  0.985 of the radius and any pin written from it is a fact about the loop.

## 2026-09-23 — under-pressure: PhET's four pools, with the hydrostatic law and the unit definitions taken exactly

### Added
- **`docs/phets_revised/under-pressure.html`** — a clean-room remake of PhET
  Interactive Simulations' *Under Pressure* (build 1.1.36, the
  FLUID_PRESSURE_AND_FLOW repo), in the house six-view form. PhET's single
  screen carries four scenes and those are the first four views; the last two
  are analysis. New code; no PhET code or assets.
  - **the pool** — PhET's square pool at true proportion (3.7 × 3 m, and 2 m
    out of the page, so 22 200 L full), a faucet and a drain, two draggable
    gauges, the fluid-density and gravity sliders with PhET's named ticks, the
    atmosphere switch, the grid and the ruler, and the three unit chips. Beside
    it the same law as a line: intercept p_atm, slope ρg, both gauges on it.
  - **the shapes** — PhET's trapezoid pool. Two chambers tapering in opposite
    directions, joined along the floor: a gauge in each at the same depth reads
    the same number with 1.35× (at half fill) to 2.83× (at 0.5 m) as much fluid
    standing over one as the other. The side panel shows why the level is so
    well behaved — the two widths are equal and opposite linear functions of
    height and **sum to a constant 3.85 m**.
  - **the press** — PhET's chamber pool: a 1.00 m² piston and a 4.60 m² one,
    Pascal's principle solved rather than scripted, with displacement against
    load drawn as two straight lines whose slopes are in the ratio of the areas.
  - **the mystery** — PhET's mystery pool, with what each of the three
    candidates would read at every depth, and the inversion that names the
    answer.
  - **the paradox** — four vessels, one base, one depth, 3.1 to 8.4 m³ of
    fluid, one base force; with the difference tracked into the slanted walls
    by an integral that never uses the force balance.
  - **the column** — the whole sim as one straight line, and the same pressure
    on all three of PhET's scales at once.
- **What is exact.** The hydrostatic law p = p_atm(y_surface) + ρgh with no
  approximation, asserted against `build/under-pressure/derive.py` for every
  fluid tick × gravity tick × depth {0, 1.5, 3} m with the atmosphere on and
  off, at the surface and at the floor, and swept over 11 466 points of the two
  continuous sliders (all finite, none negative, max 363 522.2142857142 Pa).
  A second, independent route — integrating dp/dy = −ρg in 4000 slabs — agrees
  to 5e-13 relative.
- **The unit conversions are the definitions, not rounded factors.** 1 atm =
  101 325 Pa exactly; 1 psi = (0.45359237 kg × 9.80665 m/s²)/(0.0254 m)² =
  6894.7572931683608 Pa; 1 ft = 0.3048 m. So 1 atm = 14.69594877551345 psi and
  every round trip over 0–4 MPa is exact to **1.434e-16**. PhET 1.1.36 stores
  9.8692e-6 atm/Pa and 1.4504e-4 psi/Pa; the panel prints how far those are
  from the definitions (3.31e-6 atm, 2.29e-4 psi at one atmosphere).
- **The trapezoid's volume-to-level map is exact**, where PhET's is a linear
  stand-in: the cross-section is 5.145 m wide through the floor channel and
  3.85 m above it, so the level is piecewise linear with one kink, inverted
  exactly (round trip 1e-12) and cross-checked against `scipy.integrate.quad`.
- **Pascal is derived, not asserted.** Matching the pressure at one point by
  the two routes (down from the loaded surface, down from the free one) gives
  Δp = (ρg + λ)Δh with λ the air's own lapse, and because Δp = Mg/A₁ and λ both
  carry g, **g cancels**: Δh = M/(A₁(ρ + λ/g_earth)) with the atmosphere on and
  the classical M/(ρA₁) exactly with it off. The air simply subtracts its own
  1.2482993197278909 kg/m³. selfTest asserts both closed forms and asserts that
  a gauge reads the same pressure whichever surface you come down from, to
  1e-9 Pa, at every mass × fluid × atmosphere setting.
- **The paradox is computed twice.** The weight is the exact integral of a
  piecewise-linear width profile; the vertical pressure on the walls is the
  separate integral ∫p(y)w′(y)D dy done term by term; the identity
  F_wall,z = W − F_base is then a *check*, not a definition (worst residual
  6.5e-11 N). F_base/W = 1, 0.5714285714285714, 1.5483870967741937,
  0.67377877596855684, independent of the fluid and the gravity (asserted).
- **The memo key is complete, and that is now a stated property.** Every view
  caches its model under a key built from the state it reads; selfTest changes
  each of **51 (view, input) pairs** with no `clearAll()` in between and
  asserts the key notices, and separately asserts the memo really does cache.
  That makes the two surviving UI mutants equivalent *by construction* rather
  than by luck.
- **Verification.** `selfTest` **785 passed, 0 failed** under `osascript` and
  under `jsc`; the UI drive `build/under-pressure/ui_drive_under-pressure.js`
  **324 passed, 0 failed**; `tools/audit.py` reports **0 layout problems** on
  both the 1400 × 820 capture (29 configurations) and the 820 × 520 one; every
  view's PNG was rasterised and looked at. `mutants.json` carries **81 mutants
  (66 physics, 15 UI)**, each pattern checked unique in the shipped file by
  `gen_mutants.py`. A confidence run in `_out/quickcheck.py` (not the
  definitive sweep — the orchestrator runs that) has **66/66 physics caught**
  and **13/15 UI caught**, the two survivors explained below.

### Fixed (during the build)
- **PhET's own trapezoid pool has a 7 cm gap in it, and its own
  `isPointInsidePool` agrees.** Its `bottomChamber` runs to x = 6.0 while the
  right chamber's foot is at x = 6.07, leaving a wedge that closes only at
  y = −2.8286; 5948 sampled points inside that wedge are reported as *outside*
  the pool, so a gauge dropped there reads air rather than fluid
  (`build/under-pressure/_out/gap.py` is the evidence). Root cause: the channel
  and the chamber borders were authored from different constants and never
  reconciled. This file runs the channel to x = 6.2 and asserts connectivity at
  41 heights of the band — and asserts that PhET's 6.0 really does leave the
  gap, so the fix cannot be quietly undone.
- **The drawn trapezoid held 3.2 % more fluid than the model said.** Symptom:
  `polyAreaW(fluidPolys) × DEPTH_OUT` was 12.202 m³ against a model volume of
  11.822. Root cause: the fluid was drawn as three polygons — two chamber
  trapezia running the full height plus the floor channel — which **overlap**
  inside the channel band, and the cavity outline was three overlapping
  rectangles whose strokes cut through both chambers. Rebuilt as
  non-overlapping pieces (one sliding band below the channel top, two chamber
  trapezia above it) and one U-shaped cavity outline; selfTest now asserts the
  drawn area *is* the model volume at 3 %, 50 % and 100 % full, and that the
  chamber pool holds the same fluid loaded and unloaded.
- **A gauge in the air above the ground read "no reading".** PhET's
  `getPressureAtCoords` returns the air pressure for any y > 0 and so does
  physics; `probeFlat` tested "is it inside the pool?" first and reported
  everything outside as unreadable. Root cause: one predicate doing two jobs.
  Split into three cases — air above the ground, solid ground, pool cavity —
  in both `probeFlat` and `chamberPressure`, with the readout now saying
  "buried in the ground" only where that is true. Six assertions added.
- **Pascal's Δh = M/(ρA₁) is not the equilibrium when the air has weight.**
  Symptom: a gauge at y = −2.5 in the chamber read 4894 Pa differently
  depending on which surface it was reached from — in a *connected* fluid, so
  one of them had to be wrong. Root cause: Δh was taken as Δp/(ρg) while the
  two free surfaces sit at different heights and PhET's air pressure lapses
  with height, so the air column between them carries part of the load. The
  exact solve (above) drops the residual to 0 and gives a closed form in which
  g still cancels.
- **The house legend takes `[colour, text]` arrays, not `{c, t}` objects.**
  Four panels passed objects, so `legendBox` drew the literal string
  `undefined` three or four times per panel — and the *physics* suite could not
  see it, because nothing there inspects canvas text. Found by the text audit
  in the layout sweep.
- **`legendAuto` records its box in `LEGEND_RECTS`, which `lab()` never
  consults**, so a note placed in "the empty corner" landed on the legend.
  Added `legendReg()`, which registers the returned box in `LABELS`.
- **The word "undefined" in ordinary prose trips the panels-clean scan.** Two
  strings ("undefined at the surface", "undefined at h = 0") were reworded
  rather than excepted — the pulsar Known-bad says the check should stay blunt.
- **A picture contradicting its own caption: the "flask" was not a flask.** The
  profile is a narrow cylinder stepping out to a wide one, i.e. the neck is at
  the *bottom*. Renamed "stepped" everywhere (JS, derive.py, the tests, the
  capture list) rather than redrawing it.
- **The mystery panel drew its three candidates on top of each other.** A few
  kPa of separation on an axis running from zero is invisible, which is exactly
  the thing that view exists to show. The axis is now fitted to the fan, with
  "the axis starts at … not at zero" printed on the canvas (the house rule for
  any scale distortion).
- **The column view's title named three fluids when one was drawn.** It now
  names the slider's fluid when the three-fluid checkbox is off.
- **The weight arrow in the paradox ran out through the base** at shallow
  depths (it was anchored at the fluid surface and scaled by the largest weight
  in the row), and at full depth the two arrows crossed. Anchored at the top of
  the vessel, with a horizontal offset clamped to the *narrowest* of the two
  heights the arrows are drawn at, so the tapered vessel's arrow stays inside
  its own wall.
- Layout, all found by the audit or by looking: the chamber world gave away a
  third of its height to empty sky (ymax 1.35 → 0.62); the grid's labels sat on
  the ruler's (moved to the right edge); the gauge boxes stacked on each other
  when two gauges were at the same height (they now dodge through eight
  candidate positions); the gauge's probe dot was not in the label registry;
  the column's three unit scales interleaved on a short stage (one scale is
  drawn there instead, and says so) and their names sat on their own first tick
  (a 54 px gutter); a marker callout in the last third of a plot landed under
  the floating readout (it flips); the "slope ρg" note was quoted in kPa/m on
  an axis drawn in atm.
- **The gauge's own reading — the number the whole sim exists to print — was
  pinned by nothing.** A mutant that reversed the probe's depth
  (`pressureAt(ySurf-y…)` → `pressureAt(y-ySurf…)`) survived: every assertion
  on the gauges compared A against B, and both flipped together, while every
  absolute pressure pin went through `pressureAt` directly rather than through
  the probe. Root cause: the same quantity reached by two code paths, only one
  of which was pinned. Now the default gauge reading is asserted absolutely in
  all three units (110163.35 Pa = 110.16335 kPa = 1.0872277325 atm =
  15.977843065 psi), at the surface, in honey on Jupiter and with the
  atmosphere off.
- **`G_MARS` survived a sweep.** The hydrostatic table passes the literal
  `3.71`, the slider sweep only asserts finiteness, and Δh in the press is
  independent of g — so nothing anywhere would have moved if Mars's gravity
  were wrong. Root cause: a constant used only as a range endpoint. All six of
  PhET's named values are now pinned absolutely *and* reached through
  `G_TICKS`/`G_RANGE`/`RHO_RANGE`, which is how the UI gets to them.
- **Pressing a draggable marker dead on its centre makes the grab radius
  untestable.** `dx*dx+dy*dy <= 26*26` mutated to `<= 0` survived, because the
  harness pressed at exactly the marker's mapped position and `0 <= 0` holds.
  Every drag now presses 8 px off-centre, and a press 40 px away is asserted
  to grab nothing.
- **Two guards on one path, again.** The pointermove handler's `dirty = true`
  and its `S.pointer(...)` return value both survived, because `pointerdown`
  had already set the flag. The drag tests now press, drain the flag, prove
  the loop idle, and only then fire the move.
- **The drag clamp was never exercised.** Every test drag stayed inside the
  world, so deleting the clamp changed nothing. A drag 4000 px off the stage
  now has to land exactly on the world's left edge and floor.
- **A stale audit read as a pass.** After one edit the capture aborted (the
  self-test failed inside `cap_run.js`) and `audit.py` silently re-read the
  *previous* `display_narrow.json`, reporting the identical collision after a
  change that provably removed it. Exactly the Known-bad; the tell is that the
  audit output does not move at all. The capture's exit code is checked now.

### Mutants that survive, and why they are equivalent
- **`a slider marks the frame dirty`** — the slider, checkbox and chip handlers
  all call `refresh()`, which calls `S.draw()` unconditionally, so the
  frame-loop `dirty` flag is redundant on the control path and deleting it
  changes nothing visible. It is load-bearing only on the pointer path, which
  has its own proven-idle test (and whose mutant is caught).
- **`a tab change clears the memo`** — each view memoises under a key built
  from every input it reads, so a stale entry can never be returned; selfTest
  proves this over 51 (view, input) pairs with no `clearAll()` in between.
  `clearAll()` is therefore redundant everywhere it appears. It is kept because
  it is the family idiom and costs nothing, and the redundancy is now a stated,
  asserted property rather than an accident.

### Known-bad candidates
- **The house legend helpers take POSITIONAL pairs, `[colour, text]`.**
  `legendBox`/`legendAuto` read `it[0]` and `it[1]`; an object `{c, t}` yields
  `undefined` from `plain(it[1])` and draws that word, silently, once per entry.
  No physics assertion can see it — only a canvas-text audit can. Check the
  helper's signature before passing it anything.
- **`legendAuto`'s box is NOT in the `LABELS` registry.** It records into
  `LEGEND_RECTS`, which only the polyline-crossing check reads, so every later
  `lab()` is free to land on top of it. Wrap it (`legendReg`) or push the
  returned box yourself.
- **Drawing one region as several overlapping polygons makes "the drawn area
  is the model volume" fail by the overlap**, and the overlap is invisible at
  a glance because the fills are translucent and identically coloured. Build
  fluid/cavity geometry as a partition, not a union, whenever a test multiplies
  its area by anything.
- **A vessel whose free surfaces sit at different heights has an air column
  between them, and that column has weight.** Any two-surface hydrostatic
  balance (a manometer, a hydraulic press, a U-tube) written as Δp = ρgΔh is
  wrong by λ/(ρg) ≈ 0.12 % in water as soon as the model's atmosphere varies
  with height. The tell is a pressure that depends on which surface you came
  down from. Solve Δp = (ρg + λ)Δh, and note that g cancels out of Δh either
  way.
- **"Is it inside the container?" is not the same question as "is there
  anything here to measure?"** A probe above the ground is in the air and reads
  the atmosphere; only a probe inside solid matter reads nothing. Collapsing
  the two into one `inside()` test silently turns the whole sky into a dead
  zone.
- **An axis from zero hides any effect that rides on a large offset.** Three
  fluids differing by 4 kPa on top of 101 kPa are one line at that scale. Fit
  the axis to the structure and print the fact that it is not zero-based —
  which is the same house rule as printing any other scale distortion.
- **Check the exit code of the display-list capture before believing the
  audit.** `cap_run.js` contains the sim's own `selfTest`, so a failing suite
  aborts the capture *before* it writes the JSON, and the next `audit.py` reads
  the previous run's file and reports the previous run's problems. The tell is
  an audit whose output does not change at all after an edit that provably
  changed the drawing.
- **PhET's trapezoid pool (build 1.1.36) is not watertight.** Its bottom
  chamber ends at x = 6.0 and its right chamber's foot is at x = 6.07. Anyone
  porting that geometry gets a 7 cm dead wedge at the floor. Do not "restore"
  the 6.0.
- **A pair of readings that must agree pins neither of them.** "Gauge A equals
  gauge B" survives any error that moves both — here, reversing the sign of the
  probe's depth. Whenever a view's headline number is reached by a second code
  path (a probe, a picker, a formatter), pin that path against an absolute
  value, not only against its twin.
- **A constant that is only ever a RANGE ENDPOINT is invisible.** `G_MARS`
  appears in a slider range, a tick list and a sweep that checks only
  finiteness; every physics assertion passed the literal 3.71 instead. Pin such
  constants absolutely *and* evaluate something through the range object, or a
  wrong value ships.
- **Pressing a draggable marker at exactly its own centre makes its grab
  radius untestable** — `dx² + dy² <= 0` is true there, so the threshold can be
  mutated to zero and every drag test still passes. Press off-centre, and
  assert separately that a press outside the radius grabs nothing.

## 2026-09-23 — center-and-variability: PhET's three screens, with every statistic exact and its quartile convention given a name

### Added
`docs/phets_revised/center-and-variability.html` (200 KB, 3362 lines), a clean-room
remake of PhET Interactive Simulations' **Center and Variability** (v1.2.6). Six views:
*the kicks* (PhET's Median screen — a kicker, a dot plot that the field already is, a
draggable ball, sortable cards, the median), *mean and median* (the mean drawn as a
fulcrum with the two moments under it, and PhET's two prediction thumbs), *the spread*
(PhET's Variability screen — range, IQR with a box-and-whisker and the 1.5 × IQR outlier
rule, MAD, the interval tool and the pointer, one field per kicker as PhET keeps them),
then three house views: *which quartile*, *the balance point* and *the long run*.

**What is exact.** Every statistic is checked against numpy on 27 data sets that include
the degenerate ones the brief names — n = 1, all values equal, two values, fifteen
identical values, heavy ties and the empty set — plus 14 random ones; the quartiles are
computed twice, once by PhET's slicing and once from explicit indices, and the two routes
asserted equal. `selfTest` is **1243 passed, 0 failed** and the UI drive **215 passed, 0 failed**.
The 73-mutant sweep run on the first shipped file was **67 caught, 6 survived**; all six
are closed below and the seven-mutant re-sweep (those six plus the two that replace the
one whose target the fix removed) is **7 caught, 0 survived**. `mutants.json` now holds 74.

Five results the file exists for, each derived rather than asserted:

* **PhET's quartile rule has a name — in fact two.** Its `VariabilitySceneModel` splits
  the sorted data at `floor(n/2)`, discards the overall median when n is odd, and takes
  the median of each half. Written as an order statistic that is h = (n+1)/4 at odd n and
  h = n/4 + ½ at even n — i.e. **exactly Hyndman & Fan type 6 (Weibull) at odd n and type
  5 (Hazen) at even n**, and at even n it also coincides with **Tukey's hinges**, because
  an even split has no middle value to include or exclude. Proved by counting positions in
  each half, then checked on 4000 data sets in `derive.py` (uniform, heavy-tie and
  three-value) and 1040 more inside `selfTest`, with **zero** disagreements. It differs
  from numpy's DEFAULT (`linear`, Excel's QUARTILE.INC) on 1207 of 2000 random data sets,
  and the rate falls only from 98 % at n = 5 to 68 % at n = 30. The *which quartile* view
  draws that sweep and pins it to `derive.py` inside the binomial tolerance of its own
  400-trial estimate.
* **PhET's displayed MAD is not the MAD.** It rounds each deviation to 0.1 m, rounds the
  sum to 0.1 m, then rounds the quotient to 0.1 m. The ceiling is derivable — 0.05 +
  0.05/n + 0.05 = **0.1 + 0.05/n** — and it is reached: the worst gap over 8000 random
  data sets is exactly 0.100 m. The sim draws and asserts the exact MAD and prints PhET's
  beside it.
* **The sample MAD is biased, and NOT always downward.** g(c) = E|X − c| is convex with
  g′(c) = 2F(c) − 1, so it has a KINK at every atom. Kickers 1 and 2 have their population
  mean exactly on a support point (8 m) and their sample MAD comes out **high** (+2.4 %
  and +0.6 % at n = 30); kickers 3 and 4, whose means are 5.044 and 10.956 m, come out low
  at every n. The first draft of `derive.py` asserted "biased down at every n" and was
  falsified by its own 20000-sample Monte Carlo.
* **The mean is the balance point as an identity.** Σ(xᵢ − x̄) is machine zero (worst
  7.1e-15 over the 27 pinned cases, and exactly 0 in integer arithmetic), and the two
  moments — the pull of the kicks below the mean and of those above — are equal to 1e-12
  on every one. Moving one ball moves the mean by exactly 1/n metres per metre at all
  fifteen positions and moves the median at **one** of the fourteen steps on the pinned
  n = 9 set.
* **PhET's kickers are closed distributions.** `Random.sampleProbabilities` returns the
  first index whose cumulative weight reaches S·u, so P(x = i+1) = wᵢ/S exactly. A
  chi-square of 10⁶ draws against each weight array gives p = 0.94, 0.47, 0.30 and 0.46;
  no zero-weight distance is ever drawn; at 5000 draws every bin is within 4 binomial sd.
  σ/√n is checked against 20000 Monte-Carlo samples at n = 5, 10, 15 and 30 for all four
  kickers (worst 1.5 %).

The random stream is mulberry32 driven through PhET's own sampler and is **bit-identical**
to `derive.py`: the page and the Python twin draw the same kicks from the same seed, and
every opening data set's mean, median, quartiles, IQR, range and both MADs are pinned
against them. PhET's rounding (`roundSymmetric` half away from zero, `roundToInterval`
through `toFixedNumber`) is pinned on eleven cases in both languages, including the four
"halves" whose direction is decided by the binary value rather than the decimal one
(0.15 → 0.1 and 0.35 → 0.3 round DOWN; 0.25 → 0.3 and 0.45 → 0.5 round up).

Build dir `build/center-and-variability/`: `derive.py` (the twin, `refvals.txt` its printed
output, `p7a_refs.js` the machine half — no number is retyped), the part files,
`ui_drive_center-and-variability.js`, `capture_tail_center-and-variability.js`,
`gen_mutants.py` → `mutants.json` (74 mutants, 60 physics + 14 UI, every `old` verified to
occur exactly once in the built file).

### Fixed (during the build)
- **`&#8341;` is U+2095, LATIN SUBSCRIPT SMALL LETTER **h** — not the subscript i it was
  meant to be.** Eighteen of them, in the readout, the equation bar, the info prose and
  two canvas captions, so a deviation sum read "Σ(xₕ − x̄)". In HTML they became
  `<sub>i</sub>`; on the canvas they became ASCII, because letter subscripts are not safe
  there at all (the rasteriser's font has no full set) and x-with-a-macron is no safer.
- **CPython's `sum()` has used Neumaier compensated summation for floats since 3.12, so it
  disagrees with a plain JavaScript accumulation loop in the last few ulps.** The worst
  |Σ signed deviations| over the pinned data sets is 2.7e-15 by `sum()` and 1.3e-14 by a
  loop — a factor of five, and the bit-level pin was measuring the two languages'
  summation rather than the statistic. `derive.py` now has `jsum()`, a left-to-right
  accumulator, and uses it for every float sum (integer sums stay on `sum()`, which is
  exact for them).
- **Labels passed as TEXT CHILDREN of `h()` become text nodes, so an HTML entity in one is
  drawn literally.** `checkbox('lBands','the &plusmn;2&sigma;/&radic;n band')` would have
  rendered as `the &plusmn;2&sigma;...` in the browser; two `.tag` divs had the same shape.
  The `.tag` blocks set through `innerHTML` are fine — the distinction is the API, not the
  string. Found by the UI drive, which could not locate the checkbox by its label.
- **`axes()` and the number line draw their tick labels and axis titles straight to the
  canvas, outside the label registry, so `lab()` and `legendAuto()` could not see them.**
  An axis title landed under a panel note, a legend over a tick label, a median label over
  a tick. `axesQ()` now wraps `axesR()` and registers every tick label, axis title and axis
  name; `drawNumberLine` and `drawCards` register theirs too. The caption is registered by
  `cavLayout` before anything is drawn, because it is drawn LAST but occupies its space
  from the start — without that, every panel note landed on it at all four canvas sizes.
- **The band under the number line was 22 px and the measures need 76.** The IQR's Q1/Q3
  labels and its summary line fell out of the plot box and into the caption at every canvas
  size (32 collisions). The band is now laid out once as named constants — ticks at +0..+5,
  tick labels at +7..+19, the measure's bars at +23..+45, its labels from +46 — instead of
  each measure choosing its own offsets.
- **A two-column bottom row collapses below ~430 px of column**, and its axis titles then
  land in the caption and under the `#hint`. The three analysis views now have a
  narrow-stage mode: the main panel takes the whole stage and the canvas names what was
  dropped.
- **The deviation "loads" all sat on one row**, so thirty strokes composited into two lines
  and the picture said nothing. Replaced by the two MOMENTS, drawn at their own printed
  scale; they are equal by the identity, so the picture IS the statement, and `cavMoments()`
  makes it assertable rather than something only the eye can check.
- **The field box was three times taller than its content** at every stack height the sim
  reaches, and the dot plot took all the rest, so half the stage was empty. The field is now
  sized from the tallest stack and the plot from the kick LIMIT (the stack's ceiling), with
  the pair centred in what is left.
- **The running-mean panel started at n = 1**, where the mean is far off scale, so the curve
  entered the box from the top and read as a broken plot. It starts at the tenth kick, where
  its ±2σ/√n band starts.
- **A view that could not draw its measure said nothing on the canvas.** An empty field and a
  four-kick field both rendered as a bare number line. Both now carry a one-line note
  ("IQR = ? — PhET needs at least five kicks, and this field has 4").
- **The pointer's triangle sat on a tick label and its text landed inside the IQR box** — a
  fill, which the label registry cannot see. It now hangs from the top of the plot and points
  down at the line, as PhET's does.
- **Two of my own expectations were wrong, not the code**: `roundToInterval(0.35, 0.1)` is
  0.3 (0.35/0.1 is 3.4999999999999996, below the tie), and `cavMedian([2,2,2,3])` is 2, not
  2.25 — both middles are 2. The demonstration of "a median can land where nothing was
  kicked" needed `[3,3,4,4] → 3.5` instead.
- **Three mutants survived a spot-check sweep and all three were missing assertions, not
  bugs.** `cavStacks` (which ball sits on which row of a stack) had no assertion anywhere, so
  doubling its row step changed only pixels; and the two flight-arc pins asserted the
  function against `CAV.T_FLY[...]` and `CAV.APEX` — the constants the mutants were changing
  — which is the "a test that re-derives the thing it is testing" shape exactly. Both are now
  pinned against absolute numbers (0.9 s, 1.5 s, 4.2 m) and against the stack's contiguity
  from row 0. All three are caught after the fix.

- **The full 73-mutant sweep found six survivors after the build reported clean; all six are
  closed, and one of them was a real bug.** Recorded here because the distinction between "a
  test gap" and "a bug" is the whole point of running the sweep:
  1. *the standard deviation ignores its ddof* — **test gap and dead code.** The sim displays
     and compares the ddof = 0 standard deviation, which is right beside a population σ it
     knows exactly; with ddof = 0 the `n − d` divisor IS the identity, so the mutant could
     only ever be caught through the n − 1 convention — and `sd1` was computed in `statsOf`
     and used nowhere. It is now printed beside `sd` on the long-run view (the contrast is
     what a statistics sim is for) and both are pinned against numpy, with the ratio asserted
     to be exactly √(n/(n−1)) so that pinning two numbers is not a tautology about one.
  2. *the spread view's per-kicker seed offset* — **test gap.** `selfTest` pinned the opening
     data sets by calling `cavDrawSet` with a seed lifted out of `REF`, so `fieldSeed()` was
     executed by no assertion at all; the mutant is tagged `p`, so the UI drive that does
     check it never ran. `selfTest` now reaches every field through `fieldOf`/`curField`, the
     way the sim does, and asserts the four kickers get four different seeds.
  3. *a slider forgets to repaint* — **the flag really was redundant.** `refresh()` calls
     `S.draw()` unconditionally, so `dirty=true; refresh();` asks for one extra identical
     frame and nothing else. Twelve handlers had it. Deleted where `refresh()` follows
     immediately, kept in the two pointer handlers where it is the only thing that repaints,
     and the mutant replaced by one on `refresh()`'s own draw.
  4. *the predict-median thumb stops snapping to half a metre* — **test gap that uncovered a
     REAL BUG.** The UI drive checked the slider's `step` attribute and never dragged the
     thumb on the canvas, which is where the snap lives. Writing that drag exposed
     `plotGeomOf` still returning `ly: b.y1 − 22` — the number the line sat at before
     `NL_BELOW` (76) was introduced. **Both prediction thumbs and the balance view's movable
     ball were grabbable 54 px below where they are drawn, i.e. not grabbable at all in a
     browser.** The balance drag test had passed only because it recomputed the same stale
     geometry the hit test used, so test and code agreed with each other while both disagreed
     with the picture. Fixed at the source: one `nlLineY()` and one `dotGeomOf()` used by the
     drawing *and* the hit test, with the per-view headroom in a single `DOT_HEADROOM` table
     (the hit test had hard-coded a 12 px row height and 5.2 px radius that `drawDots`
     computes from the box). Both thumbs are now dragged on the canvas and the two PhET
     conventions asserted against each other: the median thumb snaps (6.3 → 6.5, 6.2 → 6.0,
     9.75 → 10.0, and every reachable value is a whole number of half metres) and the mean
     thumb does not (9.37 stays 9.37).
  5. *a landed ball never joins the data set* — **test gap.** The ball lands at t ≥ T
     correctly; the mutant doubles T and the UI drive's wait loop sat through it. The flight
     time is now pinned in `selfTest` (in the air at T − one frame, down at T, landing on the
     exact frame `ceil(T/dt)`) and in the UI drive.
  6. *the kicks group is shown on every view* — **test gap.** Nothing asserted which control
     groups a view shows, only which slider rows. The UI drive now checks all seven groups on
     all six views against an explicit table.
  The re-sweep of those six plus the two replacements is **7 caught, 0 survived**.

### Known-bad candidates
- **`&#8341;` is a subscript **h**, not a subscript i.** The subscript i is U+1D62 (`&#7522;`)
  and it is not safe on this collection's canvas either. Any numeric entity for a letter
  subscript deserves a second look: `plain()` decodes it happily and the glyph that reaches
  the canvas is whatever the number actually says. Write letter subscripts as ASCII on the
  canvas and as `<sub>i</sub>` in HTML.
- **CPython 3.12+ `sum()` is compensated; a JavaScript accumulation loop is not.** Any
  Python twin that pins a float sum at machine precision must accumulate the way the page
  does, or the pin measures the difference between two languages' summation. It shows up as
  a tolerance failure of about 5× on quantities that should be identical.
- **A label passed as a text child of `h()` is a text node and will not decode an HTML
  entity**, while the same string assigned through `innerHTML` will. Both forms sit side by
  side in every sim built from this scaffold. A UI harness that looks a control up by its
  label is what catches it.
- **The shared `axes()` draws tick labels and axis titles outside `LABELS`**, so `lab()` and
  `legendAuto()` place things on top of them. Every sim in this collection has the hole; the
  wrapper is four lines (`axesQ` here) and it turned 32 layout failures into 0.
- **A quantity the picture is BUILT from is a model quantity and needs a model assertion.**
  The dot plot's stacking survived a sweep because nothing asserted it — not because it was
  drawing-only. If a mutant can only be caught by looking at the picture, the quantity is in
  the wrong layer or has no pin.
- **Asserting a function against the constant it uses asserts nothing.** Both flight-arc
  mutants survived `close(cavFlightTime(CAV.VMIN), CAV.T_FLY[0], …)`. A leading constant needs
  one assertion against an absolute number written out in full.
- **PhET's quartiles are undefined below five kicks and its MAD is triple-rounded.** Anyone
  comparing this sim against numpy's default quartiles, or against an exact MAD, will find
  differences that are conventions rather than errors. Both are named on the canvas and in
  the readout; do not "fix" either toward numpy.
- **At 560 px the stage runs under the floating readout** (the house's `stageLayout`
  behaviour for a narrow stage, kept here). `tools/audit.py` reports 11–19 tick labels
  "under the readout panel" in the narrow capture; that is advisory, not a defect, and
  reserving 300 px there would leave 234 px of usable stage.
- **A geometry used by BOTH the drawing and the pointer hit test will drift, and the drag
  test will not notice** — because the obvious way to write that test is to recompute the
  geometry the hit test uses, so the two agree with each other while both disagree with the
  picture. Here `plotGeomOf` kept `b.y1 − 22` for 54 px after the drawing moved to
  `b.y1 − NL_BELOW`, and the thumbs were undraggable in a browser while the harness was
  green. One function for the line's y, one for the dot stack, used by both layers; and aim
  a drag test at a coordinate derived from the DRAWING constant, not from the hit test's.
- **`dirty=true` beside a `refresh()` is redundant in this scaffold**, because `refresh()`
  draws unconditionally. Twelve handlers carried it here and the mutation sweep reported the
  slider's as a survivor — correctly: deleting it changes nothing anyone can see. The flag is
  load-bearing only in handlers that do NOT call `refresh()` (the two pointer handlers). The
  sibling sims all have the redundant form; it is harmless but it makes every one of those
  handlers an equivalent mutant.
- **With ddof = 0 the `n − d` divisor is the identity, so a mutant that drops `d` is invisible
  to every assertion on the population standard deviation.** If a file offers both
  conventions, it must display and pin both, or delete the one it does not use.

## 2026-09-22 — calculus-grapher: draw f by hand, and a discrete calculus whose two operators are exact inverses

`docs/phets_revised/calculus-grapher.html` (build/calculus-grapher/), a
clean-room remake of PhET Interactive Simulations' **Calculus Grapher** 1.1.1
(CC-BY 4.0; no PhET code or assets). Six views: *the derivative* and *the
integral* are PhET's two screens of those names, *the lab* is its Lab and
Advanced screens (all four curves, the reference line, Predict, the
Lagrange/Leibniz and x/t preferences), and *the corners*, *the theorem* and
*the grid* are this file's own analysis views.

### Added

- **A discrete calculus that is exact rather than accurate.** f is stored at
  PhET's 1251 nodes and DRAWN as the polyline through them, so the object on
  screen is the piecewise-linear interpolant. Its own derivative is constant
  on each cell (plotted at the cell midpoints) and its own integral is the
  cumulative trapezium at the nodes, and those two are inverse in floating
  point: `∫f′ = f − f(0)` to 4.9e-15 and `d/dx ∫f = f at the cell midpoints`
  to 7.1e-15 over random curves (derive.py; selfTest re-measures both in JS).
  The second line is the mean value theorem with the mean value known — on a
  straight segment it sits at the midpoint — so nothing is approximated.
- **PhET's own pair, and the difference named rather than hidden.** PhET puts
  f′ on the nodes as the mean of the two one-sided slopes. That is a good
  teaching choice and it is *not* the inverse of its own trapezium integral:
  `D_central(I_trap(f))` is identically the [1,2,1]/4 smoothing of f (proved
  to 6.2e-15), so it returns f + O(dx² f″) — 3.3e-3 on the shipped curve.
  *the theorem* view draws that residual beside the exact one.
- **Every analytic mode against its closed form**, at PhET's 1250 cells:
  triangle derivative exact to 1.1e-13 (piecewise linear), parabola to
  1.7e-13 (a cell-centred difference is exact on any quadratic), and for the
  smooth shapes the measured Euler–Maclaurin term — hill 4.4e-5, sinusoid
  2.7e-6, pedestal 1.1e-3 on the derivative; 1.0e-5, 1.0e-5, 2.4e-5 on the
  integral. Halving dx quarters each (measured 4.000, 4.000, 3.999), which is
  the claim the *grid* view makes rather than the numbers. The parabola's
  trapezium error IS the Euler–Maclaurin term `+dx²/12 [g′(b) − g′(a)]`, to
  7.1e-16, because the expansion terminates on a quadratic.
- **Corners treated as corners.** At a corner the derivative does not exist;
  what the file draws and asserts are the two one-sided limits, read off cells
  lying wholly on one side. For the triangle they are EXACT (±TYPICAL_Y/(w/2),
  1e-13), and the integral of the second difference over any window containing
  the apex is exactly the slope jump because the sum telescopes. The
  *corners* view says which of the two cases it is in: for a shape that is
  curved at the corner the clean cells sit ~1.5 dx away and the reading falls
  short (parabola: 1.879 measured against an exact 1.893). The hill and the
  pedestal have no corner at all — PhET's "smooth transitions" — and the view
  shows the slope-step everywhere instead, with the falsifier that a smooth
  edge's largest step halves with the grid while a corner's does not.
- **The two tools cross-checked against the curves, by different arithmetic.**
  The tangent's slope is the derivative curve's value at the same x (0.0 over
  ten probes) and the line it draws passes through both nodes of its cell; the
  area tool splits every cell at its own zero crossing and counts the halves
  separately, and its net still equals the integral curve to 2.8e-16.
- PhET's eight curve-manipulation modes reproduced from its build — hill
  (a Gaussian of sd w/4), triangle, pedestal (plateau w − 2·edgeSlopeFactor
  with an exp(−u⁴) edge), parabola, sinusoid (period 2πw/2, seven half-periods,
  cos² taper of λ/8), freeform, tilt (refused past maxTilt) and shift — plus
  its Gaussian smoothing (σ = 0.05, 3σ, 18 taps each side, renormalised so a
  constant survives exactly), its 20-deep undo, its 1e-8 blend threshold and
  its two barometers.
- `derive.py` reads every one of those constants out of
  `docs/phets/calculus-grapher_en.html` by regex (and confirms the shape
  formulas themselves are present), then re-derives the mathematics with
  numpy/scipy — erf, the incomplete gamma for the pedestal's antiderivative,
  Gauss–Legendre quadrature — and prints 120 reference values that
  `make_refs.py` turns into `p7_refs.js`.
- Verification: selfTest **289/0**, UI drive **618/0**, `tools/audit.py`
  **0 layout problems** at 1400×820 and at 860×560, 27 captured scenes looked
  at as PNGs, and a **73-mutant sweep with 0 survivors**.

### Fixed (during the build)

- **Python's `round()` is banker's rounding and JavaScript's `Math.round` is
  not**, so the Python twin put a shape's centre one node left of where the
  sim put it whenever the index landed on a half. Symptom: the two-hill test
  curve's areas differed between derive.py and selfTest by 3.2e-7 — small,
  consistent, and nothing to do with the physics. Root cause: `round(312.5)`
  is 312 in Python and 313 in JS (PhET rounds half away from zero). derive.py
  now uses `floor(t·(n−1) + 0.5)`.
- **A closed form built on the shipped grid is centred somewhere else on a
  coarser one.** `shapeClosed()` snapped the shape's centre with the global
  1251-point grid while `gridError()` built the discrete shape on the grid
  under test, so the refinement ladder reported 1.9e-2 at 313 cells against
  4.4e-5 at 1250 — the error *rising* with refinement. `shapeClosed` now takes
  the grid.
- **Two sign errors in the closed forms, both caught by the comparison rather
  than by reading.** The sinusoid's derivative was `−yk sin(k(x₀−x))` (the
  check reported exactly 2.000 = twice the slope amplitude), and the
  Euler–Maclaurin trapezium term was written `−dx²/12 [g′(b) − g′(a)]` when
  T − I is `+`. Neither would have been visible without an independent value
  to compare against.
- **A layout derived from the caption moves the panels under the pointer.**
  These captions quote the corner count and the tangent slope, so their
  wrapped line count changes as the curve is dragged; the second half of a
  drag then landed at the wrong y. The caption band is now reserved from
  (W, H, panel count) alone and the caption is truncated to fit it, and a drag
  keeps the map it started with.
- Four layout defects found by the inline sweep and the audit, each fixed at
  its cause rather than by moving one label: the x-axis label hangs 21 px
  below a panel (the bottom reserve is 42 px, and stacked panels need a 46 px
  gutter or the next panel's title lands on it); tick labels must be thinned
  by their measured screen spacing, for supplied lists as well as generated
  ones; PhET's barometers sit in the 336 px the floating readout owns unless
  the panel reserves 76 px of right margin; and a scrubber's label has to go
  through the label registry, and above the frame, or it lies on the tangent.
- **Seven mutants survived the first sweep and every one was a blind spot,
  not a brittle test.** (1) The second-difference end convention was probed on
  a curve that is flat at both ends, where "copies its neighbour" and "writes
  a zero" are the same thing. (2, 3) Every sinusoid test used w = 2 on an
  empty curve — a packet wider than the whole domain, where PhET also drops
  the taper — so the seven-half-period extent and the λ/8 taper were untested;
  both are now pinned at w = 0.6 on a constant base. (4) `valueAt`'s
  interpolation had no assertion of its own; it is now pinned where the answer
  is exact (at a cell midpoint it is the mean of the two nodes). (5) The drag
  test pumped the loop after the press but not after a move. (6) "reset all
  zeroes the prediction" was vacuous because the prediction was already zero.
  (7) The lay-it-down button was tested with the width slider at its default,
  so a mutant substituting that default was invisible.
- **An empty curve made the theorem view tell three lies in one caption**, and
  only the PNG showed it: with f ≡ 0 every residual is exactly zero, and the
  caption called that "floating-point rounding", reported its largest value as
  being "at a corner" there were none of, and then said "and not zero" of a
  zero — while the bottom panel's axis, fitted to a zero range, printed five
  ticks reading 0 and one reading −0. The view now has an explicit empty-curve
  branch, and a tick whose magnitude is far below the tick spacing prints as 0.
- **PhET's `1/(σ√2π)` cancels exactly in `acc/tot`**, which makes a mutant on
  it an equivalent mutant rather than a finding. `smoothCurve` now returns the
  peak weight and the weight sum, and selfTest pins both against derive.py and
  against the midpoint rule for the truncated Gaussian — which also pins the
  3σ window.

### Known-bad candidates

- **Python's `round()` and JavaScript's `Math.round` disagree on every half.**
  A twin that indexes a grid by rounding will be one node out wherever the
  index lands on `.5`, and the symptom is a small, stable disagreement in an
  integral rather than anything that looks like an indexing bug. Use
  `math.floor(v + 0.5)` in the Python twin whenever the JS uses `Math.round`
  (and note PhET's `Utils.roundSymmetric` is half-away-from-zero, which is the
  same thing for non-negative indices).
- **A closed form used as the reference for a refinement study must be built
  on the grid under test.** Anything the discretisation snaps — a centre, an
  edge, an envelope end — is a *different number* on a coarser grid, and a
  reference that snapped it on the fine grid makes the error rise as the grid
  is refined. The tell is a convergence table that is not monotone at its
  coarse end.
- **A caption that quotes the model makes the layout depend on the model.**
  If panel geometry is derived from a measured caption and the caption's
  wording changes with the state, the panels move while the user is dragging,
  and a pointer-to-model map read after the move is wrong. Reserve the caption
  band from the canvas size alone, and let a drag keep the map it began with.
- **An end-condition, a taper or an envelope tested only where it is inactive
  is tested nowhere.** Three of the seven survivors here were that shape: a
  second-difference end probed on a flat end, and a sinusoid's extent and
  taper probed at a width whose packet is wider than the domain (where PhET
  drops the taper anyway). Before believing a parameter is pinned, check that
  the configuration under test actually reaches the code that uses it.
- **A normalisation divided by its own sum is an equivalent mutant unless the
  weights themselves are returned.** PhET's Gaussian kernel is renormalised,
  so its `1/(σ√2π)` cannot be seen in the smoothed curve at all. Return the
  weights (or delete the constant) — a survivor that is provably equivalent is
  telling you the code carries meaning the tests do not.

## 2026-09-22 — molecules-and-light: PhET's photon-and-molecule chamber, its response table beside the real spectroscopy, and the normal modes derived from symmetry and mass

### Added

- `docs/phets_revised/molecules-and-light.html` (241 KB, six views:
  *the chamber*, *the spectrum*, *what responds*, *the normal modes*,
  *the statistics*, *the atmosphere*), a clean-room
  remake of PhET Interactive Simulations' **Molecules and Light** (build 1.5.33,
  CC-BY 4.0). No PhET code or assets; PhET's own PNG photon sprites are replaced
  by four house accents, and every number marked "PhET's value" is read out of
  the minified build in `docs/phets/molecules-and-light_en.html` or out of its
  `doc/model.md`.
- **the chamber** — PhET's single screen, rule for rule. The light source at
  x = −1350 firing photons at 3000 model units/s; the 100-unit absorption
  radius; **exactly one** absorption trial per photon at p = ½ (PhET's
  pass-through list makes the first failed trial final, so four frames inside
  the radius still buy one coin flip); a hold time uniform on 1.1–1.3 s; a
  re-emission in a direction uniform on the circle; a 0.2 s refusal window
  afterwards; 5 Hz vibration, 1.1 Hz rotation, the 0.8 s emission period, the
  half-rate slow motion, the 0.2 s frame ceiling and the break-apart speeds 990
  and 0.67 × 3000. The strip under the chamber is the molecule's state against
  time, recorded by the simulation rather than by the drawing.
- **the spectrum** — PhET's Light Spectrum Diagram with the seven band edges its
  own accessibility text states, its four source wavelengths marked with their
  exact energies, and two zooms carrying every measured transition of these nine
  molecules on the same logarithmic axis.
- **what responds** — PhET's 8 × 4 response table, read straight out of its
  `setPhotonAbsorptionStrategy` calls, beside the real answer computed here.
- **the normal modes** — the vibrations, diagonalised from a valence force field
  fitted to the measured wavenumbers, animated at their true displacement ratios,
  with the exact symmetry statements checked against the eigenvectors beside them.
- **the statistics** — PhET's three random rules measured over a seeded
  generator against the standard error each is entitled to, with a deliberately
  biased generator shown being rejected by the same test.
- **the atmosphere** — Earth at 288 K per unit wavenumber, the measured
  IR-active fundamentals drawn on it, the 8–13 µm window, and the composition
  bar that shows 99.966 % of dry air absorbing nothing.
- `build/molecules-and-light/derive.py`, the Python twin: 199 reference values,
  every one of them asserted in `selfTest`. `gen_ref.py` turns its `refvals.json`
  into `p7a_ref.js` and `p2b_fields.js`, so no reference number is hand-typed.
- Verification: `selfTest` 749/0 and the UI drive 310/0 under `osascript`
  (0.5 s and 1 s); `tools/audit.py` clean on 19 captured configurations;
  99 mutants in `mutants.json`, every pattern checked to match exactly once
  by `gen_mutants.py`.

### What is exact

- **Photon energies.** The 2019 SI fixes h, c and e by definition, so
  hc = 1.986445857148929e-25 J m and hc/e = 1239.841984332002 eV nm are exact
  rational numbers. Every energy, frequency and wavenumber the file prints is
  that identity, computed two ways and asserted to agree at 1e-14.
- **The mode shapes symmetry alone fixes.** For a linear symmetric XY₂ the
  symmetric stretch is (1, 0, −1) with the central atom *exactly* at rest
  (3.8e-16 here) and the antisymmetric stretch and the bend are both
  (1, −2m_Y/m_X, 1); for a bent XY₂ the B₂ antisymmetric stretch has
  v/u = cot(θ/2) from zero linear and zero angular momentum. None of the four
  depends on a force constant or on a bond length. The JS re-diagonalises the
  Hessian with its own Jacobi solver and reproduces all of them to 7e-15.
- **The infrared selection rule, two independent ways.** Rigid point charges
  give |∂μ/∂Q| = 0 to 4e-15 for all six inactive modes — and the zero survives
  rescaling every charge by 2.7, so it is the mode shape and not the charge.
  The inversion character decides the same six centrosymmetric modes with no
  numbers at all, and the two agree on every one.
- **PhET's two columns ARE the two selection rules.** Its microwave column is
  exactly the four molecules with a permanent dipole (CO, H₂O, NO₂, O₃) and its
  infrared column is exactly the six with an IR-active fundamental (all but N₂
  and O₂). Both are asserted as properties, not spot-checked.
- **The CO J = 1 ← 0 line, derived rather than quoted.** B_e from the measured
  r_e and the reduced mass reproduces the tabulated constant to 3.5e-7, and
  2B₀ lands at 115.2719 GHz against the 115.2712018 GHz radio astronomers use —
  6e-6 out, in the direction and of the size centrifugal distortion demands.
- **The stochastic layer.** The generator is a 32-bit mulberry32 and the Python
  twin reproduces every draw bit for bit, so the 60-second and 600-second
  chamber runs are pinned photon for photon (76/28/47/28 and 751/256/494/255)
  rather than statistically.

### What is modelled, and what is not

- The A₁ pair of a bent triatomic mixes, and the mixing angle needs a force
  field. Three measured wavenumbers do not determine the four symmetry constants
  of a bent XY₂, so the fit returns the solution of **smallest stretch–bend
  interaction** that still reproduces all three exactly — a stated choice, and
  the reason those two shapes are labelled MODEL on the canvas. Ozone needs
  f_rθ = 0.087 aJ/Å²; water and NO₂ come out at zero.
- Line strengths, line shapes, rotational fine structure, overtones, Fermi
  resonance (CO₂'s ν₁ is quoted as its deperturbed 1333 cm⁻¹), excited-state
  photolysis products, collisions and quenching are not modelled. The atmosphere
  view marks band POSITIONS and never strengths, and says so.
- Bond dissociation energies are QUOTED (Active Thermochemical Tables) and were
  not re-derived; the canvas and the credit line both say so.

### Fixed (during the build)

- **The NIST WebBook prints O₂'s rotational constant in square brackets, and in
  Huber & Herzberg that means B₀, not B_e.** Taking the fetched `Be = 1.4376766`
  at face value disagreed with the same row's `re = 1.20752` by 0.55 %, which is
  what caught it; B_e computed from r_e minus α_e/2 reproduces the bracketed
  number to 1.1e-5, a factor of 504 better, which is what settled it. CO and N₂
  are unbracketed and agree as B_e to 3.5e-7 and 5.0e-7. The file now asserts
  the RATIO both ways, so the bracket convention is pinned rather than assumed.
- **A finite-difference Hessian is only translationally and rotationally
  invariant to O(h²), and the residual leaks into the eigenvectors.** Water's
  modes carried 2.2e-8 of spurious centre-of-mass drift and 1.3e-8 of spin. An
  acoustic-sum-rule patch on the diagonal blocks fixed the translations and
  broke the symmetry (the two row sums S_i^{αβ} and S_i^{βα} differ, so
  re-symmetrising undoes it); the Eckart projection P H P with P = I − ΣBBᵀ
  fixes both at once and takes every residual to 1e-14.
- **A linear molecule's bend cannot be written as (π − θ)².** `arccos` has
  infinite gradient at θ = π, so a Cartesian finite difference of it is
  garbage. Writing the bend energy as f_θ r² (1 + cos θ) — identically the same
  harmonic form to leading order — is smooth in the Cartesians and gives CO₂'s
  667 cm⁻¹ to 5e-15.
- **`&micro;` is not in the shared entity table**, so three captions drew
  `&micro;m` verbatim on the canvas. `&ldquo;`/`&rdquo;` were missing too. Both
  added in `make_head.py`, so a regeneration keeps them.
- **`stageLayout` floors its main box at 80 px, and on a short stage that floor
  pushes the main panel straight over the bottom row.** At 560 × 380 the
  atmosphere view's axis title and the composition panel's summary overlapped,
  and the normal-modes view drew its molecule below its own box and over the
  footnote. A `stage()` wrapper now re-lays the stage with NO bottom row when
  the floor bites: one honest panel beats two overlapping ones.
- **The house `#hint` sits on the last line of a bottom-anchored caption.**
  Every view passes `H − HINT_H` (18 px) to `stageLayout`, as
  `build/wave-on-a-string` and `build/molecule-polarity` do.
- **The O₃ fragments' atom labels flew off the canvas.** After dissociation the
  pieces leave the observation window and were still being drawn at −1023 px.
  A fragment outside the window is now dropped, and the view *says* the pieces
  have left rather than going quietly blank.
- **`legendAuto` avoids curves, and the zoom panels draw their transitions with
  raw strokes**, so `POLY_SEGS` was empty and it thought every corner was clear:
  both legends landed on the data. Replaced by one shared legend in the main
  panel's empty middle, drawn only when it fits clear of everything above it.
- **`const DRAG` collides with `p4a_helpers.js`.** The extracted house helper
  block already declares it; a second `const DRAG` is a hard SyntaxError, not a
  subtle bug. Extended the existing object instead.
- **A renewal estimate of the duty cycle is 6 % low, and it is not noise.**
  T/2 + (1/p − 1)T + busy predicts the molecule excited 46.2 % of the time; five
  1200-second runs measure 49.1 % with a spread of 0.021, and the estimate is
  below *every* seed. The source is exactly periodic and the busy time nearly
  deterministic (σ = 0.058 s on 1.4 s), so the phase never decorrelates. The
  file prints both and names the assumption that fails.
- **The eigenvector arrows were buried inside the atoms.** At some phases every
  arrow points inward, and a CPK-radius sphere swallowed it. The spheres are
  drawn at 0.78 of the CPK radius, the arrow starts at the sphere's edge, and
  every arrow is drawn after every sphere.
- **Eight defects the mutation sweep found, every one a masked assertion.**
  (1) `pointerdown` sets the dirty flag too, so a drag fired in one go could
  not test whether the MOVE handler sets it -- the pumped frame repainted
  either way, and the mutant that deletes it survived. The drag now presses,
  drains to idle, proves it, and only then moves. (2) `reset all` restored the
  camera twice -- `Object.assign(st, DEFAULTS)` already carries `camTheta`,
  `camPhi` and `zoom` -- so a mutant on either path was equivalent; the
  redundant `S.resetCam()` is gone and `resetCam` is pinned where it is the
  only path. (3) "the molecule chip rewinds the mode index" was vacuous
  because the index was already 0; a sentinel of 5 is set first. (4) The
  re-emitted photon was created with `pass: true` AND the molecule set a 0.2 s
  hysteresis -- two guards on one path, so deleting the hysteresis changed
  nothing. PhET emits an ordinary photon and relies on the hysteresis alone;
  this file now does the same, and the mutant is caught. (5) `nubarToUm` was
  printed by the readout and the canvas and asserted by nothing; it is now
  round-tripped through `photonOf`, which reaches a wavenumber by a different
  route. (6) Only the `'asym'` branch of `linearExact` was ever evaluated, so
  the symmetric-stretch and bend branches could be mutated freely; all three
  are now checked against the eigenvectors. (7) The emission direction was
  measured through `ensembleDirection`, a different code path from the
  chamber's own emission, so the chamber's `rng() * 2 * Math.PI` was untested;
  400 seeded re-emissions are now measured directly. (8) The Jacobi rotation
  ANGLE is an equivalent mutant -- halving it fails to annihilate A[p][q] in
  one rotation but the cyclic sweep still converges to the same
  eigen-decomposition -- so it was replaced by the sweep cap and the
  convergence test, which are the load-bearing parts. (9) CO2's measured bond
  length survived, correctly: with the force field fitted in the coordinates
  r*dtheta and |r| - r_e, the bond LENGTH cancels out of every wavenumber and
  every mode shape, so no amount of spectroscopy can see it. Every measured
  geometry now has an absolute pin, and the invariance is asserted
  deliberately (to 5e-8, the residual being the fixed finite-difference step
  against a rescaled geometry) rather than left as a blind spot.
- **The house z-up camera cannot look down z** (`right = cross(fwd, [0,0,1])` is
  degenerate at φ = π/2), so a planar molecule built in the x–y plane was always
  seen edge-on-ish. The molecules are mapped onto the world x–z plane instead,
  where φ ≈ 0 looks straight at them and a drag still orbits normally.

### Known-bad candidates

- **A rotational constant in SQUARE BRACKETS in Huber & Herzberg (and in the
  NIST WebBook that reproduces them) is the value for the stated vibrational
  level, not the equilibrium one.** Reading O₂'s `[1.4376766]` as B_e is wrong
  by 0.55 %; it is B₀. The tell is that the same row's r_e disagrees with it,
  and the test that settles it is the RATIO of the two readings' residuals
  (504× here), not an absolute tolerance — r_e is printed to six figures, which
  alone accounts for 4e-6 of the 1.1e-5 that remains.
- **A finite-difference Hessian needs an Eckart projection, and the obvious
  acoustic-sum-rule fix breaks the symmetry it is applied to.** Setting
  H[3i+α,3i+β] = −Σ_j H[3i+α,3j+β] satisfies the row sums but makes the
  diagonal block non-symmetric, and re-symmetrising undoes the sum rule.
  Project instead: P = I − Σ B Bᵀ over the mass-weighted rigid motions, then
  P H P. Both residuals go to machine precision in one step.
- **`(π − θ)²` is not a usable bend coordinate for a linear molecule.** Use
  2(1 + cos θ), which equals it to leading order and is smooth in the
  Cartesians where `arccos` is not.
- **`&micro;` is NOT in the shared `ENTS` table** (`&mu;` is). A micrometre
  written as an entity reaches the canvas verbatim. So do `&ldquo;`/`&rdquo;`.
- **`stageLayout`'s 80-px floor on the main box silently overlaps the bottom
  row on a short stage.** When `L.main.h <= 82` and there are bottom boxes, lay
  the stage out again with none.
- **A renewal estimate assuming a decorrelated phase is systematically wrong
  against an exactly periodic source with a nearly deterministic busy time.**
  Measure it, sweep the seed to separate sampling spread from the systematic
  gap, and print both.
- **Two guards on one path make each other's mutant equivalent, and a
  re-emitted photon is where it happens here.** PhET's molecule emits an
  ordinary photon AT its own position, inside the absorption radius, and the
  only thing that stops it swallowing it again on the next frame is the 0.2 s
  hysteresis. Marking that photon `pass: true` as well is a second owner of
  the same behaviour and makes the hysteresis untestable.
- **A number that only the readout and the canvas print is covered by
  nothing.** `nubarToUm`'s 1e4 survived a sweep for exactly that reason. Pin
  such a conversion by ROUND-TRIPPING it through an independent route rather
  than restating it.
- **A closed form with a `which` argument needs every branch evaluated.**
  `linearExact(mol, 'sym'|'asym'|'bend')` had two branches no assertion ever
  reached.
- **A bond length CANCELS out of a valence force field fitted in r*dtheta and
  |r| - r_e.** Every wavenumber and every mode shape is invariant to it, so a
  spectroscopy suite cannot see a wrong bond length however many assertions it
  carries. Pin the geometry absolutely and assert the invariance deliberately.
- **A Jacobi rotation angle is not a physical constant.** Any angle that
  reduces the off-diagonal norm converges to the same eigen-decomposition, so
  mutating it is equivalent; mutate the sweep cap and the convergence test
  instead.
- **`p4a_helpers.js` (the extracted house block) already declares `const DRAG`
  as well as `const LABELS`, `CAP_FONT` and the camera.** A sim that declares
  `DRAG` again fails to parse.

## 2026-09-22 — build-an-atom: PhET's Build an Atom remade, with its stability table checked against an independent one

### Added

`docs/phets_revised/build-an-atom.html` — a clean-room remake of PhET
Interactive Simulations' **Build an Atom** 1.9.3 (University of Colorado
Boulder, CC-BY 4.0; new code, no PhET code or assets). Six views: *the atom*
(PhET's first screen — the three buckets, the nucleus, orbits or cloud, and
the four things the counts determine), *the symbol* (its second screen),
*the game* (its third: four levels of five challenges scored 2 and 1),
*the counting* (all 1694 bucket configurations, with the census that makes
the rules checkable), *chart of nuclides* (PhET's whole stability table on
the (N, Z) plane beside an independent one), and *mass and binding*
(measured isotope masses and abundances, their mean, and the binding energy
they imply).

**What is exact.** The three rules are arithmetic on three integers and are
checked *everywhere*: `selfTest` walks all 11 × 14 × 11 = 1694 configurations
the buckets allow and compares the element, the mass number, the charge and
the stability of each against an independently written expression (counting
loops rather than arithmetic, a Set of keys rather than `indexOf`). The
census that follows is pinned to `derive.py`: 153 neutral, 1540 ions, 220
with a stable nucleus — which is 20 distinct stable nuclides × 11 electron
counts, exactly, because stability does not depend on electrons. Those 20
are every stable nuclide with Z ≤ 10 that exists, and PhET's 13-neutron
bucket is exactly one more than neon-22 needs.

**PhET's own values, read out of the minified original** by
`build/build-an-atom/extract_phet.py`: the 10/13/10 buckets, MAX_ELECTRONS,
the 85 and 130 shell radii, the ten electron slots (two at ±85, eight at
130 starting at π/8 × 1.2 and stepping 2π/8), the cloud law
r(e) = 42.5 + 8.75 e (which puts ten electrons exactly on the outer shell),
the 100 and 1.1 × 130 capture radii, both charge-sign conventions,
`stableElementTable`, `numNeutronsInMostCommonIsotope`, `standardMassTable`,
the isotope table, the symbol and element-name strings, the atomic radii, the
four `AtomValuePool` challenge pools, the four level type lists and the
5-challenges / 2 / 1 scoring.

**Stability is measured data, and it is cross-checked.** PhET's table holds
**244** nuclides, Z = 1 to 82. It is compared here against an independent
one built from NUBASE half-lives and NIST isotopic compositions (by way of
this repo's own `projects/simulations/periodic_table.html`) under the
criterion "occurs in nature and has never been observed to decay": **253**
nuclides, also stopping at lead. **They agree on 243.** PhET alone counts
germanium-76, whose double-beta half-life of 1.9 × 10²¹ yr has actually been
measured; the independent table alone counts ten (Cr-50, Zn-70, Te-123,
Xe-124, Xe-134, Ba-132, Ce-138, Ce-142, W-183, Pb-204), every one a nuclide
whose predicted decay has never been seen. **Below Z = 24 the two sets are
identical**, so nothing this sim can build is in dispute. Neither counts
bismuth-209 (α, 2.0 × 10¹⁹ yr, measured 2003). Both give technetium and
promethium no stable isotope at all. Asserted: the 244, the 253, the 243
agreement, the two exception lists nuclide by nuclide, the heaviest (Pb-208),
the two empty rows, and the Z below which the two are identical.

**Other measured results, all pinned to `derive.py`.** PhET's isotope masses
agree with the independent mass excesses to 1.6 × 10⁻⁶ u and its abundances
with NIST to 3.2 × 10⁻³ percentage points. Σ(abundance × mass) reproduces
PhET's published standard atomic weight to 1.4 × 10⁻⁴ relative, worst at
lithium — which is not an error in either, because lithium's isotopic
composition varies enough between natural sources that IUPAC gives it an
interval. Binding energies come from the masses by
B = [Z m(¹H) + N mₙ − m(A, Z)]c², with no mass formula and no fit; the curve
peaks at **nickel-62** (8.7945 MeV/nucleon) just above iron-56 (8.7903), and
the two data sources give the same B/A to 1.6 × 10⁻⁴ MeV. Hydrogen-1's
binding energy is zero to the keV the table is rounded to. The even/odd
census of the stable set is 140 / 52 / 48 / 4, and the four odd-odd nuclides
(H-2, Li-6, B-10, N-14) are all inside what the buckets can build. Four of
the five commonest neutron numbers are magic, and N = 82 carries six stable
isotones against one on each side.

**The game** reproduces PhET's rules exactly — its four type lists, its four
atom pools, no type twice in a row, schematic challenges restricted to Z < 3
and every other type to Z ≥ 4, a charged atom asked for about half the time
on charge questions — with a seeded mulberry32 that is reproduced bit for bit
in Python. `selfTest` generates 16 000 levels and checks that every one of
the 80 000 challenges is answerable, that no type repeats and that the Z
rules hold. PhET's fallback (reuse a used atom when the filtered pool is
empty) is reachable exactly once in those 16 000 — level 2 at seed 2691,
whose five all-schematic challenges exhaust the four charged atoms with
Z < 3 — and that rate is asserted rather than forbidden.

Verification: `selfTest` **2330 passed, 0 failed**; UI drive
**437 passed, 0 failed**; mutation sweep **86 of 86 caught, 0 survivors,
0 skipped** (68 physics + 18 UI mutants — every leading constant, every
unit conversion, every sign, PhET's bucket sizes and shell radii, the PRNG,
the challenge-selection rules, the scoring, and the dirty flag on every
interaction); `tools/audit.py` clean on all three captures (1400 × 820,
820 × 520, 560 × 380); 32 captured configurations rasterised and looked at.
The first sweep had four survivors, all real gaps, all now pinned (below).

### Fixed (during the build)

- **A finder that matches a word drives the wrong control.** The game's
  answer sliders were first labelled `protons` / `neutrons` / `electrons`,
  the same as the atom group's. Renamed `answer: protons` and so on before
  the harness could silently drive the wrong one.
- **A pointer handler that refreshes the whole view masks the dirty flag.**
  `pointerup` called `refresh()`, which draws unconditionally, so the
  frame-loop drag test would have passed with the flag deleted. Split
  `refresh()` into `panels()` (the HTML) and the draw; the handlers update
  the panels and set `dirty`, and only the frame loop draws.
- **A click and the picture disagreeing.** The atom view's periodic table and
  the game's level cards were positioned inside the draw and the pointer
  recomputed them, so the two could drift. Both are now produced by
  `atomGeo` / `gameGeo`, which draw nothing.
- **`axes()` draws its tick labels outside the label registry**, so a
  `labelIfClear` label lands on a tick. Added `axesR`, which registers every
  piece of text `axes()` draws — including the y title's *rotated* box.
- **A panel title wider than its panel.** "N/Z along the valley" ran out of
  the right-hand chart panel and under the floating readout at 820 px.
  `panelTitleFit` measures and falls back to a short title.
- **A long key beside a right-aligned value.** The counting view's census
  rows collided ("odd-odd" through "4: H-2, Li-6, B-10, N-14") at 820 px.
  `kvRow` now puts the value on its own line when the pair does not fit;
  squeezing the key into whatever the value left was the first, worse, fix.
- **`legendAuto` dodges polylines and labels, and the nuclides are
  fillRects**, so the chart's legend was placed over the top of the stable
  band. It is now placed by a function that tests each corner against the
  *drawn* squares, and `selfTest` re-measures that over the whole Z-range
  slider (37 settings).
- **An annotation over the data it describes.** The isotope panel's
  "Σ ab × m" block sat on the tallest abundance bar. `annotate()` is given
  the bars' rectangles and picks a clear corner.
- **A fixed question height pushes the answer onto the caption.** At
  560 × 380 the game's "set them in the panel" line landed on the stage
  caption. The question box now gives up exactly the height the answer needs,
  and the inline sweep was extended to draw every challenge of every level at
  three sizes — the first sweep sat in the game's *idle* phase and could not
  see it.
- **The corner captions of the symbol box overlapped its numbers**, because
  their offset was a fixed fraction of the box rather than the number's own
  measured height.
- **The element name landed on a bucket caption.** The atom view now reserves
  a band for the three labels PhET puts under the atom and shrinks the
  picture into what is left.
- **A drawing test that reads ambient state.** The display capture runs after
  `selfTest` (the entry block calls it when there is no document), and
  `gameReset` deliberately does not clear the best scores — so every level
  card read "best 10/10" in the first capture. The capture tail resets them.
- **Four mutation survivors, all real gaps.** `signed()` (the charge
  formatter) and PhET's `ELECTRON_RADIUS` only ever reached a drawing, so
  swapping the signs and shrinking the radius changed nothing any assertion
  could see; both now have absolute pins, and the one test that *mentioned*
  the radius ("no two electron slots overlap") still passed at 7 px, which is
  the lesson. The level-seed mixing was an argument to `makeChallengeSet`,
  and dropping it was invisible because the challenge sets differ between
  levels anyway (the type lists differ) — it is now a named function whose
  result is stored in `GAME.seed` and pinned against `derive.py`. And the
  reset-all test ran from the default view, so "it leaves the view where you
  were" was vacuous; it now resets from the chart view.
- **A capture that names a state it is not in.** `gameCheck()` returns
  without doing anything while the phase is `wrong`, so the `game_shown`
  capture (wrong twice) sat in the one-more-try state under a name that said
  the answer had been shown. The capture tail retries between the two checks.
- **An empty type name in the finished-level caption.** `gameCaption` read
  `gameCurrent()`, which is null once the level is over, and printed
  `type ""`. The done phase has its own caption.
- **A longer caption breaks a two-panel layout whose panels have minimum
  heights.** Adding one sentence to the mass caption pushed the binding
  panel's axis title onto it at 820 × 520, because `layout()` only reserves
  120 px of stage before keeping the long caption and the `Math.max` floors
  then overflow. `layoutMin()` takes the view's own floor, so a long caption
  is traded for the short one instead of for a collision.

### Known-bad candidates

- **Never reconcile PhET's atomic radii against `periodic_table.html`'s
  radius column.** They are different quantities: PhET ships the *Clementi
  calculated* radii (hydrogen 53 pm, which is the Bohr radius) and
  `periodic_table.html` column 15 is mendeleev's `atomic_radius` (hydrogen
  154 pm). A first version of `derive.py` reported 94 "mismatches" and they
  were all definitional. What IS checkable is the definition — hydrogen's
  Clementi radius is a₀ to the printed precision — and that is what the
  suite asserts.
- **"Half-life is null" is not "stable".** The NUBASE table carries no
  half-life for 569 nuclides, most of them drip-line nuclides whose
  half-life is unmeasured because it is ~10⁻²¹ s (Li-12, B-16). Abundance
  alone is no better: it admits K-40 and U-238. The criterion that works is
  *both* — occurs in nature AND no decay ever observed — which gives 253,
  all with Z ≤ 82.
- **A generator's documented fallback must be asserted as a rate, not
  forbidden.** PhET reuses an already-posed atom when the filtered pool is
  empty, and that path is reachable: 1 level in 16 000. A test that demanded
  "no atom is ever repeated" failed on correct code.
- **A canvas quantity used only in drawing is invisible to every
  assertion, and a test that *mentions* it is not a test of it.** Two of the
  sweep's four survivors were `signed()` (the charge formatter, used only in
  captions and the charge strip) and PhET's `ELECTRON_RADIUS` — whose only
  assertion, "no two electron slots overlap", still passed at 7 px because
  the slots are 99 px apart. Absolute pins, always.
- **A value that only ever appears as a function ARGUMENT cannot be
  asserted.** The level seed was `makeChallengeSet(level - 1, (gseed +
  level * 7919) | 0)`, and deleting the mixing changed no challenge set that
  any test compared, because different levels have different type lists and
  so produce different sets either way. Lift such a value into named state
  (`GAME.seed`) and pin it — which also made it honest on the canvas, where
  the finished-level card prints the seed the level actually ran on.
- **`layout()`'s 120 px stage floor is not enough for a view whose panels
  have minimum heights.** One extra sentence in a caption pushed the lower
  panel's axis title onto it. Use a per-view floor (`layoutMin`).

## 2026-09-22 — rutherford-scattering: PhET's Rutherford Scattering remade, with the closed form beside every trajectory

### Added
`docs/phets_revised/rutherford-scattering.html` (215 KB, 4 078 lines) — a
clean-room remake of PhET Interactive Simulations' **Rutherford Scattering**
(University of Colorado Boulder, CC-BY 4.0), built against its minified build
**1.1.29** in `docs/phets/`. New code; no PhET code or assets. Both of PhET's
screens (Rutherford Atom, Plum Pudding Atom) and both of the Rutherford
screen's scenes (the zoomed-out atomic view and the zoomed-in nuclear view),
its gun, its Energy / Protons / Neutrons sliders, its Traces checkbox and its
legend.

Six views: **the nucleus** (PhET's nuclear-scale scene), **the foil** (its
atomic-scale scene, five atoms), **plum pudding** (its second screen, with the
number that killed the model on a logarithmic axis beside it), **the
hyperbola** (the closed form with an RK4 integration of Newton's equations laid
over it), **the cross section** (1/sin⁴(θ/2) three independent ways) and
**gold, for real** (PhET's scaled numbers against the real ones).

**What is exact.** The whole Coulomb problem. Every drawn particle is on the
exact hyperbola `r(φ) = b²/[b sinφ + (D/2)(cosφ − 1)]` at every step — only its
timing along the conic is integrated (RK4 on `dφ/dt = v∞ b/r²`, fourth order,
measured: 1.65e-4 → 6.6e-7 → 2.6e-9 for 15 / 60 / 240 steps). From it:
`tan(θ/2) = D/2b`, `r_min = D/2 + √(D²/4 + b²)`, the asymptote offsets, the
eccentricity `1/sin(θ/2)`, and `dσ/dΩ = (D/4)²/sin⁴(θ/2)` obtained as the
Jacobian `(b/sinθ)|db/dθ|` rather than quoted. Checked against `scipy`
independently: the deflection integral `θ = π − 2b∫dr/(r²√(1 − U/E − b²/r²))`
reproduces `2 atan(D/2b)` to 2e-11; `solve_ivp` on the equations of motion
conserves energy to 8e-13 and angular momentum to 2e-13 and reaches the same
deflection, with a residual of **1.505/r_final²** — a truncation whose rate is
measured at three distances, not waved at. The head-on case `b = 0` is exact
too (`r_min = D`, `θ = π`), and the radial motion has the closed parametric
solution `r = (D/2)(cosh η + 1)`, `t = (D/2)(sinh η + η)`, which satisfies
`v² = 1 − D/r` identically. The seeded beam is a `mulberry32` reproduced bit
for bit in Python — the JS and Python samples are the *same* sample, so the
binned cross section is asserted against derive.py's counts exactly and against
the exact solid-angle average to **the model's own 1/√N**, a tolerance taken
from the sampling law and not chosen.

Thomson's atom is a uniform ball of `+Ze` of radius `R` with the electron
charge on its surface, so the atom is neutral outside and the field inside is
the ball's alone: `θ(b) = D b √(R² − b²)/R³`, `θ_max = D/2R` at `b = R/√2`,
`⟨θ²⟩ = D²/6R²`. The impulse form is checked against the full deflection
integral and its error is shown to be a real O(θ) departure (0.082 % → 0.041 %
→ 0.020 % as D halves), not zero. Electrons are not deflectors: a free electron
can turn an alpha by at most `asin(m_e/m_α) = 1.371e-4 rad`.

**PhET's values, read out of the minified original** and labelled PhET's
throughout: `RSConstants` (energy 50–100 default 80, protons 20–100 default 79,
neutrons 20–150 default 118, traces off, `SPACE_NODE_WIDTH` 510),
`RSBaseModel` (bounds ±127.5), `RutherfordAtomSpace` (five atoms of width 30 at
±n/2, ±n and −n/2 with n = 127.5), `RutherfordNucleusSpace` (one atom whose box
is the whole bounds), `RutherfordAtom.moveParticle`
(`D = (L/8)(protons/79)(80/energy)²`), `Gun.step` (one particle every
`width/energy/20` s, a uniformly random x, nudged away from any atom centre it
comes within 4 % of the bounds width of), and both scale captions
(6.0×10⁻¹⁰ m atomic, 1.5×10⁻¹³ m nuclear). The element names on the proton
slider are PhET's own SHRED strings, emitted from `inventory.json` by
`gen_elements.py` — not one was typed. Writing PhET's D as `2α/s₀²` makes the
Coulomb strength `α = 400 L (Z/79)` independent of the gun setting, as it must
be, and both spellings are asserted equal over the whole slider space.

**The scale distortions are printed on the canvas**, as the house rule
requires: PhET's two captions are 4000× apart while its two scenes are only
8.5× apart geometrically, and a real gold atom is **20 623** nuclear diameters
across; at PhET's own nuclear-scale caption a real gold nucleus would be 9.3 %
of the frame and D 19.7 %, against the drawn 12.5 %.

Verification: `derive.py` (scipy.constants CODATA 2022, `quad`, `solve_ivp`,
`brentq`, `minimize_scalar`, a bit-for-bit Python `mulberry32`) prints 401
reference values into `refvals.txt`, which `make_refs.py` emits into
`p7_refs.js`; **973 selfTest assertions, 0 failed**; **234 UI-drive assertions,
0 failed**; **104 mutants, 104 caught, 0 survived**; the layout audit is clean
at 1400×820, 820×520 and 560×380 over 28 captured configurations.

### Fixed (during the build)
- **`asin(C/R)` is the wrong way to invert a conic, and it fails silently at
  small b.** Solving `b sinφ + (D/2) cosφ = b²/r + D/2` as `R sin(φ + θ/2) = C`
  is algebraically right and numerically useless: at b = 1e-6 and D = 31.875,
  `C` and `R` agree to fifteen digits, the arcsine has no correct digits left,
  and `phiAtRadius` returned **φ = 0 for every radius** — which made the b = 0
  button produce NaN in the readout. In the half-angle variable `t = tan(φ/2)`
  the same equation is the plain quadratic `(D + q)t² − 2bt + q = 0` with
  `q = b²/r`, which returns 8.4e-9 and 1.2e-7, the right answers.
- **The velocity angle needed the conic's derivative, and the derivative has a
  closed form the radius cancels out of.** `atan2(dX/dφ, dY/dφ)` built from
  `r(φ)` and `r′(φ)` is NaN at φ = 0, where the radius is infinite — and φ = 0
  is exactly where every incoming particle is. Differentiating properly, the
  `b²/den²` factor cancels and the whole thing collapses to
  `χ(φ) = atan2((D/2)(1 − cosφ), b − (D/2) sinφ)`, with the versine written as
  `2sin²(φ/2)` (Known-bad, brachistochrone). It has no singularity anywhere,
  `χ(0) = 0` and `χ(φ_∞) = θ` exactly, and selfTest checks it against the
  brute-force derivative.
- **The plum pudding was ATTRACTIVE.** `puddingKick` rotated the velocity with
  the counter-clockwise matrix and a sign taken from the side, which pushed
  *both* sides of the beam inward. No bound on the deflection SIZE could see
  it, because the size is the same either way, and the first three rounds of
  tests were all bounds. Found by the assertion written to close a mutation
  survivor: `p(x>0).vx > 0 && p(x<0).vx < 0`.
- **A formula written out twice is a mutant waiting to survive.**
  `puddingKick` re-derived `θ(b) = (D/R)(b/R)√(1 − (b/R)²)` instead of calling
  `thomsonTheta`, and a mutant that dropped the square root survived a
  102-mutant sweep. It now calls the pinned function with `D_model = (D/R)·R`,
  which is the same number by construction. (Known-bad: the drum's group
  velocity, written out three times.)
- **A release test built from the current velocity lets a particle leave and
  re-enter the same atom on alternate ticks.** Once a particle is on its orbit
  its velocity has turned, so the box test has to use the frame the orbit was
  SET UP in, not a fresh one; and a particle released at the boundary must not
  be re-captured by the atom it just left.
- **`Math.floor(dtWall/DT_TICK)` throws the leftover away, and a browser frame
  is 16.6 ms against a 16.67 ms tick** — so the floor is zero on most frames
  and the sim crawls or stops outright. The leftover accumulates now, capped at
  0.2 s and at six ticks a frame so the loop always terminates.
- **Nothing in the orbit views was clipped to its box.** The hyperbola view
  drew its whole family from ±3 Rw and the lines ran across the caption and off
  the stage; the live views drew particles thrown back down the beam line over
  the gun and the census strip. Everything is clipped in DATA space now
  (a `ctx.clip()` would fix the browser and not the display-list audit, which
  records `clip()` as a no-op — Known-bad).
- **A canvas gradient records as an object, not a colour string.** The plum
  pudding's ball was filled with a `createLinearGradient`; the display-list
  audit cannot read it and `raster.py` paints an unparseable colour magenta, so
  the whole atom came out solid magenta. A flat premixed fill is what the
  capture can see — and the same objection applies to the browser's audit
  trail, not just the rasteriser's.
- **The family of orbits ran up the +x side only**, so three quarters of the
  frame was empty and the picture read as a spray out of the nucleus rather
  than a beam passing it — the same failure as drawing each conic in its own
  frame (Known-bad, `differential_scattering.html`). Both sides now.
- **`sigf()` was drawing `3.7x10^-14` on the canvas.** The shared formatter's
  exponent used a literal caret; canvas has no markup. Digit superscripts are
  safe in the rasteriser's font (letter ones are not), so it builds one.
- **A tick that lands exactly on the bottom-left corner of a plot box grazes
  the leftmost x-tick label by 7×1 px** — which `tools/audit.py`'s half-pixel
  rule reports and the eye reads as smear. `ticksNoFloor()` drops the edge
  tick; dropping it is cheaper than moving either label.
- **The stacked cross-section panels needed 64 px between them, not 30**: the
  upper panel's x-axis title ends 33 px below its frame and the lower panel's
  title starts 24 px above its own. And at a stacked width the two rotated
  y-axis titles overlapped each other, so they shorten.
- **A gold-ruler label that only dodges what it collides with still runs off
  the canvas** — "PhET's atomic-scale caption" ended at x = 597 on a 560 px
  stage. `sideLabel()` picks the side with room inside the panel first. Ten
  labels also need ten rows: with four they landed on each other and half of
  them were dropped.
- **The launch of a head-on orbit was checked against the wrong quantity.**
  derive.py's first `b = 0` integration started at `v = −1` from `r = 400`
  instead of `v = −√(1 − D/r₀)` and turned at 2.9777 for D = 3 — an 0.74 %
  "error" that was the right answer to the wrong question (that orbit really
  does have E = 0.50375 and turns at (D/2)/E). Same file, same day: the elapsed
  time along a conic was integrated from φ = 1e-12, where the integrand goes as
  1/φ² and the integral diverges, so the "RK4 error" it reported was entirely
  the lower limit.
- **Twelve mutation survivors, each a real gap.** The Poisson sigma (the bin
  test recomputed `3/√n` locally instead of reading the model's own — Known-bad:
  assert off a BUILT model); PhET's 4 % nudge window (doubling it leaves the
  smallest reachable |x| unchanged, so only the DENSITY it doubles can see it);
  `dφ/dt` and the speed law (every earlier assertion measured a *direction*,
  which the timing and the speed cannot change — now pinned against derive's
  quadrature of the elapsed time, and by the energy of every particle the
  engine is carrying); the orbit frame's j component (identically zero in the
  nuclear scene, so no straight-up launch could see it — now checked in a frame
  rotated by 0.7 rad); the beam's uniform x (nothing asserted it was symmetric
  or as wide as the box); the five atoms' positions; `DT_TICK`; and the
  Thomson kick's D, its charge and its direction.

### Known-bad candidates
- **A conic inverted through an arcsine loses every digit at small impact
  parameter, and it fails by returning zero rather than by throwing.**
  `b sinφ + (D/2) cosφ = C` written as `R sin(φ + δ) = C` has `C/R → 1` as
  `b → 0`; at b = 1e-6 and D = 31.875 it returned φ = 0 for every radius, which
  propagated NaN into the readout of the one case the view has a button for.
  The half-angle substitution `t = tan(φ/2)` turns the same equation into a
  quadratic with no cancellation. Generally: before inverting a trigonometric
  sum, check what its amplitude and its right-hand side do in the limit the UI
  can reach.
- **A deflection with the right magnitude and the wrong sign is invisible to
  every bound you will think to write.** The plum-pudding kick pulled both
  sides of the beam inward for three rounds of testing, because every assertion
  was of the form `|θ| < x` or `|θ| > y`. Any scattering angle needs one
  assertion about which WAY it goes, on both sides of the axis.
- **A canvas gradient is invisible to the display-list audit and reads as the
  rasteriser's error colour.** `createLinearGradient` records as an object, not
  a colour string; `tools/raster.py` paints an unparseable colour magenta, so a
  gradient-filled shape comes out as a solid magenta blob that looks
  deliberate. Premix the colour and fill flat, or the capture is not showing
  you what the sim draws.
- **The house `sigf()` writes its exponent with a literal caret**, which is
  fine in the readout's HTML and draws `3.7x10^-14` on the canvas. The copy in
  `build/rutherford-scattering/p1_utils.js` builds a digit superscript instead;
  the other sims in the collection still have the caret.
- **`Math.floor(dtWall/dt)` in a frame loop is a sim that does not run.** A
  browser frame is 16.6 ms and a 60 Hz tick is 16.67 ms, so the floor is zero
  on most frames. Accumulate the remainder (capped, and with a bounded number
  of catch-up ticks).
- **A timing law and a speed law leave no trace in any angle.** Every geometric
  assertion about a trajectory — the deflection, the closest approach, the
  asymptotes — is invariant to how fast the particle moves along it. Pin the
  elapsed time against a quadrature and the energy against its own definition,
  or `dφ/dt = L/mr²` and `v = v∞√(1 − D/r)` can be anything.
- **A frame whose second basis vector is (0,1) hides every mutation of its own
  j component.** In a scene where everything is launched straight up, `p.jx` is
  identically zero and a sign error in `pos = a + i·X + j·Y` changes nothing.
  Test placement in a deliberately rotated frame.
- **PhET's `atan2(X0, −Y0)` and its entry quadratic are safe only because its
  tracking region is a SQUARE rotated to the particle's direction.** On a
  bounding circle the discriminant `X0² − 2D(Y0 + r0)` goes negative for a
  grazing entry once `2D > R`, which the proton and energy sliders reach; on
  the square it stays positive over the whole slider space. The sim counts
  clamps and selfTest asserts the count is zero.

## 2026-09-22 — gravity-and-orbits: four systems and one inverse-square law, drawn big enough to see and then drawn true

### Added
- `docs/phets_revised/gravity-and-orbits.html` — a clean-room remake of PhET
  Interactive Simulations' **Gravity and Orbits** (1.6.28; CC-BY 4.0,
  University of Colorado Boulder). New code; no PhET code or assets. Five
  views: *the model*, *to scale*, *the circular orbit*, *the exact orbit*,
  *what is conserved*. Build dir `build/gravity-and-orbits/`; Python twin
  `derive.py`; the engine, the utilities and the 2-D layer are read from
  `build/keplers-laws/` by `assemble.py`, so the three sims of this family
  (keplers-laws, my-solar-system, gravity-and-orbits) share one solver.
- **PhET's two screens are the first two views.** The Model screen with its
  four systems (Sun and Planet, Sun Planet and Moon, Planet and Moon, Planet
  and Space Station), the gravity switch, the half-to-double mass sliders,
  the velocity and gravity-force arrows, the path, the grid, the measuring
  tape, the mass readout and the clock in Earth days (Earth minutes on the
  station scene). To Scale is the same four with every radius true.
- **What is exact**, all asserted against `derive.py`:
  - v = √(GM/r) and T = 2π√(r³/GM) at all three real radii to 1e-14, each
    also re-derived from `m v²/r = GMm/r²` and from `2πr/v`.
  - Kepler's third law, with the masses in it: T²/a³ = 4π²/G(M+m) to 1e-13
    for both Earth satellites, so the space station's constant is 1.23 %
    larger than the Moon's — a bigger total mass gives a smaller constant —
    and that 1.23 % is exactly the Moon's own mass as a fraction of the
    Earth's. (That (T_m/T_s)² = (r_m/r_s)³ for two circular
    orbits about the same mass is an *identity* of T = 2π√(r³/GM), not a
    measurement; it is asserted, and labelled as the identity it is.)
  - Each period is separately measured by integrating the orbit until it
    closes, and agrees with the Kepler period to 2e-9.
  - Every two-body run tracks the closed-form Kepler solution — elements from
    the state vector, then E − e sin E = M by safeguarded Newton to 1e-15 in
    the step. After 400 frames the integration is 2.5e-12 of r from Kepler on
    the Sun–Earth scene and 1.6e-8 of r on the station scene; `derive.py`
    checks both against scipy's `brentq` and `solve_ivp` (DOP853, rtol 1e-13).
  - **Gravity off is exactly a drift:** one frame is bit-for-bit
    `r + v dt`, 600 frames change no speed **at all** (asserted `=== 0`, not
    "small"), and the path leaves the straight line by ≤ 1.2e-14 of its own
    length. The gravity-on control leaves it by 0.3 of the distance travelled.
  - Momentum and angular momentum are conserved to rounding on the To Scale
    screen (|Δp|/p ≤ 8.7e-15, |ΔL/L| ≤ 1.3e-14 over 4,000 frames); the energy
    to |ΔE/E| ≤ 2.1e-10.
- **PhET's two deliberate distortions of the Model screen are kept and
  measured**, because they are its model: the star is nailed down, and in
  Sun-Planet-Moon the moon's pull from the planet is multiplied by 10,200
  **one-sidedly** (PhET's `adjustMoonOrbit`), so Newton's third law does not
  hold there. Measured: the drawn moon sits 23.85× its real distance at 21×
  its real speed; a circular orbit there needs 214.5 m/s unboosted and
  21,662 m/s with the boost, and the boost that would make it exactly
  circular is 11,223, not 10,200. The one-sidedness costs 89 % of the
  momentum in 600 frames. The conservation view draws all of it.
- **PhET's data against the measurement**, both columns on the page, each
  measured value at the precision its source prints (NASA planetary fact
  sheets; NASA's ISS Facts and Figures):
  - PhET's Moon radius is **1,727.4 km against the measured 1,737.4 km** —
    0.58 % low, and the shape of a transposed digit. Every other radius it
    ships is the fact-sheet value exactly.
  - Sun 1.989e30 vs 1.9884e30 kg (+0.030 %), Earth 5.9724e24 vs 5.9722e24
    (+0.0033 %), Moon mass and the 419,725-kg station exact, Sun and Earth
    radii exact, perihelion +0.0021 %, max speeds +0.033 % / exact.
  - PhET's own numbers give a year of 365.558 d (measured sidereal 365.256),
    a month of 27.249 d (27.3217) and a 91.45-min station orbit at 347.0 km,
    against NASA's "about 90 minutes" for a station nearer 420 km.
- **The integrator.** PEFRL (Omelyan, Mryglod & Folk 2002) — PhET's own
  choice, and its three coefficients are read out of PhET's build — four
  force evaluations a step, substepped so no step exceeds 0.02 of the
  shortest pairwise crossing or free-fall time. Its order is measured by
  halving the step: **4.00** against **1.00** for PhET's step as shipped,
  which carries the same coefficients but evaluates the acceleration once and
  reuses it for all four kicks (that composition is exactly
  r + vh + ½ah², v + ah). Over PhET's own 600 frames its energy drifts
  8.7e-3 against our 1.3e-13, and the two runs end 9.3e8 m apart.
- **PhET's own interface details, kept and asserted:** its mass readouts
  ("1 Earth mass", "333 thousand Earth masses", "14 billion billion Space
  Station masses") with its own thresholds; its rule that a body whose drawn
  diameter falls to 12 px or less gets a leader line and its name; its clock
  in Earth days and, on the station scene, Earth minutes; its 0.5–1.3 zoom;
  its 1/4/7 substeps a frame; its grid steps; and its Sun-Planet-Moon moon
  built with `massSettable` false, so that slider is dead there.
- Verification: `selfTest` **1,150 passed, 0 failed**; UI drive
  **194 passed, 0 failed**; 25 captured configurations through
  `tools/audit.py` (0 layout problems) and `tools/raster.py`, every PNG read.
  Mutation sweep, 99 mutants (84 physics, 15 UI): **88 caught, 11 survived**
  on the first full pass; every survivor was a missing assertion, all eleven
  are closed, and each was re-verified as caught on the final file.

### Fixed (during the build)
- **The order sweep measured saturation, not order, on the Model screen.**
  Symptom: the conservation view's title read "order: 3.99 vs 0.58" on
  Sun-Planet-Moon. Root cause: the sweep ran over a fixed 40 days, which is
  more than a whole *boosted* lunar orbit, so PhET's first-order step at 20
  steps was already wrong by the size of the system and its error stopped
  falling. Fix: the window is now a ninth of the closest pair's reference
  period (39.6 d for Sun-and-Planet, 3.2 d for the Model moon), which reads
  3.98 vs 1.00. `derive.py` pins both windows and both orders.
- **The `(derive)` reference errors for PEFRL flattened at N = 1600.**
  Symptom: measured order 1.573 on correct code, with ratios 16.0, 1.36,
  1.22. Root cause: positions are ~1.5e11 m, so one ulp is 3e-5 m and a
  25,600-step reference run random-walks to ~3e-3 m — which *is* PEFRL's own
  truncation error at N = 1600. The step counts are now 20–160, where every
  error is above 1 m, and the reason is written where the constants are.
- **A bar-chart label written across its own bar.** The "lengths on a log
  axis" panels put each label after the bar's end; a bar reaching 90 % of the
  axis leaves no room, `labIn` clamped it back inside the box, and it landed
  on the bar it names. Labels now go *above* their own bar, left-aligned at
  the frame.
- **The centre-of-mass label was written inside the Sun.** For a star and its
  planet the centre of mass is inside the star — and the Model screen's star
  is drawn 50× too big — so magenta text landed on a yellow disc. Pushed
  clear of the nearest body along the line between them (the same fix
  `my-solar-system.html` needed, for the same reason).
- **Notes drawn after `legendR` get dropped, not the legend.** `legendR`
  rejects a corner that covers a *registered label*, so a note drawn
  afterwards has no claim: on the Model conservation view both notes vanished
  entirely. The notes now go on first and the legend dodges them. They also
  pick the half of the box the curves are not in (measured from the current
  drift level), because on the Model screen the curves run along the top.
- **A UI-harness finder matching on a word drove the wrong control.**
  `findLabelledU('PhET')` matched the *gravity* checkbox ("gravity acts
  (PhET's on/off switch)") before the comparison one, so the test switched
  gravity off and then failed an assertion about the shadow integrator. Both
  finders now match the whole decoded label, never a substring.
- Three labels overflowed a 560-px canvas (the Model screen's
  bends-the-physics note, the three-body "no closed form" sentence, the
  central-body note in the circular-orbit view). Each now has a measured
  short form, or is split into two lines.
- The circular-orbit view drew its central body at 2.5 % of the *orbit*,
  which is one pixel once a near-escape conic widens the view six-fold. The
  floor is now 2.8 % of the *view*, and the factor it amounts to is printed.
- **Cutting gravity rewound the clock, which threw away the one thing the
  switch is for.** The toggle called `sysSaveStart`, which restores the start
  state — so a planet halfway round its orbit jumped back to the beginning
  instead of flying off along the tangent from where it was. Root cause: the
  straight-line residual needs an anchor, and the anchor was being taken by
  re-saving the whole start. Split apart: `coastAnchor` records position,
  velocity and speed at the instant gravity was cut, and nothing else moves.
  The UI drive now runs 200 frames, cuts gravity mid-orbit, and asserts the
  clock is unchanged, the planet has not moved, and it then leaves along the
  tangent *at the cut*.
- **The third-law statement was the wrong way round, and the suite caught
  it.** T²/a³ = 4π²/G(M+m), so a *bigger* total mass gives a *smaller*
  constant: it is the space station's constant that exceeds the Moon's by
  1.23 %, not the other way about. Written as the inverse, the assertion
  failed at 2.4e-2 — which is what an assertion against an absolute value is
  for.
- **Two analysis views opened on a degenerate axis.** Before the clock has
  run, the error, separation and drift panels have a time range of zero, and
  the tick formatter then prints six identical "0" labels along the bottom —
  the first thing a reader sees on those tabs. They now draw the frame and
  say what will appear there, and the order panel (which needs no run) is
  still drawn. `selfTest`'s layout sweep and the capture both gained a
  zero-frame configuration for each, so it cannot come back unseen.
- **A mutant that is caught can still stall the whole sweep.** `r³ → r²` in
  the step-limit's free-fall time asks for 74,000 substeps a frame; the suite
  caught it in its third section but does not abort on a failed assertion, so
  it ground on through 4,000-frame conservation runs for the best part of an
  hour. Four mutants were re-aimed so that every one of them makes the sim
  *faster*, not slower (the exponent up not down, the distance out not in,
  the step short not long).

- **The mutation sweep found eleven missing assertions and no wrong physics.**
  Each is now closed, and each was re-run individually against the final file
  to confirm it is caught:
  1. *the step limit's free-fall branch.* It takes the shorter of the crossing
     time `r/|dv|` and the free-fall time, and in **every** scene PhET ships
     the crossing time is the shorter one — so no shipped scene reaches the
     free-fall branch at all. It is reachable (drag a velocity arrow to zero)
     and is now pinned there, together with its r^(3/2) scaling.
  2. *the Planet-and-Moon hand split.* PhET computes it by hand **and** then
     calls `center()` on it, so a mutant on the hand split is undone by the
     centring. Pinned by its own contract instead: it already leaves zero
     momentum before the centring runs.
  3–4. *the two Earth-mass readout thresholds.* Nothing was ever evaluated
     between 1.01 and 1000 Earth masses, so both branch points could move
     freely. Pinned at 500, 1500 and 1.05 Earth masses.
  5. *the length units.* Only the unit **string** was checked, so the
     megametre's divisor could become 1e5. Each divisor now has its own value.
  6–7. *the two arrow scales.* The drawn length was compared against the
     constant that drew it — a tautology (the Prandtl-2/π trap again). Now
     against the literal 90 px and 60 px.
  8. *the reference speed.* Taking each body's own speed instead of its speed
     relative to the primary differs by the primary's recoil, 3e-6 here — far
     inside any pixel tolerance. Pinned against PhET's own typed speeds.
  9. *the dragging class.* Every pointer-move the harness fired carried
     `buttons: 1`, so the class that lets a drag survive a no-button move was
     never exercised. The harness now fires one.
  10. *the tab-selects-its-screen link.* Tested from the chips, never from the
     tabs.
  11. *the too-small-to-see pointer.* The check matched one canvas op reading
     `Earth` — which the **legend** also draws. It now requires two.
  One survivor was not an assertion at all: `dirty = true` in the
  pointer-down handler, redundant beside the `refresh()` on the same path.
  Removed, and the mutant retargeted at the `dragging` class, which is not.

### Known-bad candidates
- **A fixed window for an order sweep measures saturation on any system whose
  own timescale is shorter than the window.** A first-order method run at a
  step comparable to the orbit does not have an order at all — its error is
  bounded by the size of the system — and the measured slope then reports the
  bound. Scale the window to the system's own shortest reference period, and
  say in the code why the step counts are coarse.
- **A roundoff floor looks exactly like a wrong order.** At 1e11-metre
  coordinates one ulp is 3e-5 m, so any reference run of N steps carries
  ~√N ulps of noise; when the method's truncation error reaches that, the
  halving ratio collapses toward 1 on perfectly correct code. Check the error
  against the ulp scale before believing a measured order.
- **`legendR` dodges registered labels, so draw every label BEFORE the
  legend.** The existing Known-bad entry ("legendAuto avoids curves, not
  labels — draw the legend first and let labels dodge it") is the rule for
  `legendAuto`; `legendR` is the other way round, and following the older
  rule silently deletes the notes instead of moving the legend.
- **An identity of the formula is not a measurement, however many digits it
  agrees to.** `(T₁/T₂)² = (r₁/r₂)³` for two circular orbits about the same
  mass follows from `T = 2π√(r³/GM)` by algebra, so quoting twelve figures of
  agreement as "two orbits nothing else connects" is a rubber stamp. The
  measurable third law has the masses in it (`T²/a³ = 4π²/G(M+m)`), and the
  independent check is a period *measured by integrating the orbit*. Both are
  in the file now, and the identity is labelled as one.
- **A mutant that terminates can still stall a sweep, because the suite does
  not abort on a failed assertion.** `mutate.py` has no per-mutant timeout,
  and a mutant that makes the integrator take 10⁴ times as many substeps runs
  for an hour before reporting a mutant the suite caught in its first minute.
  Aim every mutant so that it makes the model *cheaper*: exponents up,
  distances out, steps shorter.
- **A branch that every shipped configuration misses is covered by nothing,
  and the `min()` of two timescales is exactly that shape.** The adaptive step
  takes `min(crossing time, free-fall time)`, and in all eight scenes here the
  crossing time is the smaller — so the free-fall exponent could be anything.
  Whenever a limit is a `min` or a `max`, find the state that selects the
  *other* argument and pin it there.
- **Comparing a drawing against the constant that drew it is a tautology.**
  `velScale(sys) * vRef(sys)` IS `VEL_PX` by construction, and so is the
  drawn arrow's length; both survived a halving of the constant. Measure the
  emitted geometry against a LITERAL.
- **A canvas-text check that matches one op matches whichever op comes
  first — and the legend draws body names too.** "the canvas names the Earth"
  passed with the too-small-to-see pointer deleted, because the legend entry
  also reads exactly `Earth`. Count the ops, or match on something only the
  feature under test emits.
- **Angular momentum about the origin loses four digits when the system sits
  1 AU away from it.** The Planet-and-Moon scene is built at the Earth's
  heliocentric position, so `x v_y − y v_x` is a large number minus a large
  number and |ΔL/L| reads 4.4e-12 where the same scene at the origin reads
  1e-14. That is the coordinate, not the physics — assert it at the tolerance
  the coordinate allows and say which is which.

## 2026-09-22 — fourier-making-waves: PhET's three screens, with every coefficient re-derived from the waveform it belongs to and the Gibbs constant measured

### Added

`docs/phets_revised/fourier-making-waves.html` — a remake of PhET Interactive
Simulations' **Fourier: Making Waves** (build 1.1.5), in six views. THE
HARMONICS is PhET's Discrete screen: eleven harmonics whose amplitudes you drag
on the canvas, drawn one per colour on the house NEON ramp, their sum below,
PhET's five presets (sinusoid, triangle, square, sawtooth, wave packet) plus
custom, sines or cosines, the domain switched between space, time and space &
time, the waveform the infinite series converges to, and PhET's
wavelength/period caliper. THE WAVE GAME is PhET's Wave Game screen: five
levels, a hidden waveform in magenta, the amplitudes to find, and PhET's own
rule that a guess counts only when every one of the eleven matches exactly.
THE WAVE PACKET is PhET's Wave Packet screen: a Gaussian in k with PhET's
centre, width and four component spacings, its components, its sum and its
envelope, with the 2σ_k and 2σ_x width markers. THE CONVERGENCE, THE SPECTRUM
and THE TRANSFORM PAIR are this file's own analysis views.

**What is exact.** Almost all of it; this sim is arithmetic, not a solver.

- **The preset coefficients are checked against the waveforms they belong to,
  not quoted.** `build/fourier-making-waves/derive.py` integrates `sgn(sin u)`,
  `(2/π)asin(sin u)` and `u/π` against `sin nu` and `cos nu` with
  `scipy.integrate.quad` broken at every corner, and the closed forms 4/(πn),
  8/(π²n²) and 2/(πn) come back to **2.2e-16**. The coefficients of the *wrong*
  parity come back zero to 2.5e-16, which is what says the sine forms are odd
  and the cosine forms even — and is why PhET refuses to build a sawtooth out
  of cosines.
- **PhET's wave-packet preset is a Gaussian, and its table has one typo.** That
  preset is 66 hard-coded numbers in PhET's build. derive.py fits σ from PhET's
  own numbers at every N and gets N/5 to 2e-5, and 65 of the 66 entries are
  `exp(-(n-c)²/2σ²)` with c = (N+1)/2, σ = N/5 to **4.9e-7**, PhET's own printed
  precision. The exception is N = 10, n = 2 and its mirror n = 9, where PhET
  reads 0.216255 and the Gaussian gives 0.216265 — a transposed digit. This
  file uses the closed form; selfTest pins both numbers so the difference
  cannot be lost.
- **Parseval both ways.** `⟨F²⟩ = ½ΣA_n²` is asserted against the trapezium
  rule on the square of the actual sum for every preset and eight random
  amplitude sets in both parities, worst residual **1e-13** — and the quadrature
  is *exact* rather than converged, which selfTest states by checking that 32
  and 4096 samples agree to 1e-14 while 16 (below 2N) do not. The complete
  series reproduce the exact mean squares 1, 1/3 and 1/3.
- **The Gibbs overshoot is the Wilbraham–Gibbs constant.** The peak of the
  M-odd-term square partial sum sits at u = π/2M exactly and equals
  `(2/π)Si(π) = 1.1789797444721672` in the limit, so the overshoot is
  **8.948987223608 %** of the jump. derive.py finds the peak by a dense scan
  plus Brent refinement and confirms the closed form to 1e-13 at M = 1, 2, 3, 6,
  12, 50, 400; the approach to the limit is O(1/M²) (measured ratio 4.0094
  between M = 6 and 12). The triangle, being continuous, never exceeds 1 — the
  falsifier for "series always overshoot" — and the sawtooth's jump is also 2,
  so it tends to the same fraction (0.08899 at 1000 terms).
- **The wave packet's transform pair is done, not approximated.** The Fourier
  transform of `A(k) = exp(-(k-k0)²/2σ_k²)/(σ_k√(2π))` is
  `exp(-σ_k²x²/2)cos(k0x)`, so σ_x σ_k = 1 **exactly** and the envelope is
  1/√e at x = σ_x, which is why the width markers sit at that height. Checked
  against quadrature over the whole line in Python (3.8e-16) and in JS (1e-12).
- **The discrete packet IS the continuous one, repeated.** By Poisson summation
  the two-sided sum over k_n = n k1 equals `Σ_m F(x − mλ1)`, λ1 = 2π/k1 —
  verified to 6.8e-16 in Python and 1e-12 in JS — and the truncated one-sided
  sum PhET draws is exactly periodic with period λ1 (residual 5.5e-15). What
  separates it from the continuous packet inside one period is only the
  Gaussian tail below k = 0 and above 24π, bounded by erfc at 6.3e-5 and
  measured at 5.3e-5. At PhET's own default (k1 = π, window ±2 m) the copies
  sit exactly at the window edges and stand at full height, which the readout
  reports as a separate number rather than hiding in the "error".
- **Analysis closes on synthesis.** Projecting a sum back onto sin nu and cos nu
  returns the amplitudes to 1e-15, by a radix-2 FFT written here, checked
  against a direct O(N²) DFT on an arbitrary (non-series) signal to 1e-12 and
  against `numpy.fft` in derive.py to 5e-16.

**What is modelled rather than exact.** The drawn curves are sampled at PhET's
own 1000 points; every number in the readout comes from a closed form, with two
stated exceptions (the measured peak of a partial sum and its position, found
on a refined grid, whose grid error selfTest bounds against the closed form).
The game's challenges are random, following PhET's generator exactly.

**What is not modelled.** Sound (PhET's Discrete screen can play the series);
PhET's per-screen zoom buttons and its equation-form dropdown; its keyboard-only
amplitude editing, info dialogs and PhET-iO instrumentation.

**Verification.** `selfTest` 6212 passed / 0 failed; UI drive 465 / 0; the
layout audit clean on 30 captured configurations at 1400×820 (and 6 at
860×560, where the panels run under the floating readout as the siblings
do); every view's PNG looked at; mutation sweep **95 / 95 caught, 0 survivors**
(85 physics, 10 UI; two survivors of the first full pass were fixed and
re-swept, see below).

### Fixed (during the build)

- **Two mutants survived the first full sweep, and both were missing
  assertions rather than bugs.** (1) `stepOnce(){ ST.t += 0.05 }` — PhET's
  step button — was exercised only by the UI drive, so the physics suite let
  0.05 become 0.1. `selfTest` now drives the clock directly: the step button's
  0.05 ms, the play rate of 1 ms of model time per second, a paused clock that
  does not move, and the fact that neither runs outside the space & time domain.
  (2) `setView` writes `className = 'active'` on the chosen tab, and nothing in
  the harness ever read the tab classes; the UI drive now asserts that exactly
  one tab is marked active after every switch. Both were re-swept and are
  caught.

- **The time domain drew a flat line in every view that used it.** *Symptom:*
  THE HARMONICS with "function of: time" showed three empty panels — the sum, the
  eleven harmonics and the caliper all at zero. `selfTest` (6188 assertions) and
  the layout audit were both green; the PNG was what showed it. *Root cause:*
  the phase is `phaseOf(domain, x, t)`, and the three curve builders passed the
  DRAWN abscissa as `x` for all three domains. In the time domain the abscissa
  *is* t, and `phaseOf('time', s, t)` ignores `s` entirely, so every sample got
  the same phase. Fixed by a separate `phaseAt(domain, s, t)` that routes the
  abscissa to the right argument, with every curve builder going through it and
  selfTest asserting, for each domain, that the drawn sum and its fundamental
  actually vary (range > 1.5 and > 2) and that the window holds a whole number
  of periods. The lesson is the general one: a model function with a correct
  signature can still be called with the arguments in the wrong roles, and only
  a test of the DRAWN curve sees it.
- **One amplitude array for the Discrete screens and the Wave Game wiped the
  preset at boot.** *Symptom:* the sim started with every amplitude zero instead
  of PhET's A₁ = 1; caught by the UI drive, not by selfTest. *Root cause:*
  `boot()` calls `applyPreset()` and then `GAME.reset()`, and the game's reset
  zeroed the same shared array. Fixed by two arrays, `AMPS` and `GUESS`, with
  `ampArray()` choosing by view — which is PhET's own arrangement (a
  fourierSeries per screen, and answerSeries/guessSeries in the game). selfTest
  now asserts both directions of the separation.
- **The convergence view's "terms kept M" meant two different things.** The
  slider keeps harmonics 1..M, but `squarePeakClosed(M)` is written in the count
  of ODD harmonics, so at M = 6 the view compared a three-odd-harmonic sum with
  a six-term closed form and was out by 0.6 %. Fixed with an explicit
  `oddCount(N) = ceil(N/2)`, shown in the readout, and the overshoot panel's
  x axis relabelled "odd harmonics kept".
- **A whole-half-period scan for the Gibbs peak lands on its MIRROR.** A square
  wave's partial sum is symmetric about u = π/2 (only odd harmonics survive
  u → π − u), so a scan of (0, π) finds the mirror of the first ear as often as
  the ear — same height, wrong position, and the readout then printed a peak
  position that disagreed with its own π/2M. Fixed with a per-waveform
  `peakWindow()` that looks next to the jump: (0, π/2) for a square, (π/2, π)
  for a sawtooth, the whole half period for a continuous waveform. selfTest
  asserts the symmetry AND that the wide scan still lands on the mirror, so the
  reason the window exists is itself a test.
- **The wave-packet components panel was an aliased hairball.** Across PhET's
  ±2 m window the highest component runs 48 cycles; drawn at 240 samples that is
  5 points per cycle, so the curves shown were not the components. The panel now
  draws over ±3σ_x with the sample count set from the phase excursion
  (16 points per cycle of k_max), prints the zoom factor, and the sum panel
  below carries a cyan bracket showing which slice it is.
- **Two panel-stack gaps were too small for the labels they had to clear.** A
  36 px gap put an upper panel's x tick labels (bottom + 5) under the next
  panel's title (top − 9), and 14 px of clearance above the caption put the
  bottom panel's axis label on the caption's first line. Both were found by
  selfTest's collision check across 26 configurations × 3 sizes; the gaps are
  now 46 px (50–62 where an axis label is involved) and 48 px above the caption,
  with the arithmetic written down beside them.
- **`logTicks` leaves a single label on an axis spanning under two decades.**
  The rms-error panel showed one "0.1". Added `logTicksFine`, which subdivides
  1-2-5 per decade below 2.2 decades, and `logLab`, which writes plain decimals
  because a superscript minus is not safe on the canvas.
- **A limit line drawn UNDER the curve converging onto it is invisible.** The
  Wilbraham–Gibbs line was drawn first and the green peak curve sat exactly on
  it. It is now drawn last, dashed, so both show.
- **The peak label ran under the floating readout for a sawtooth.** Its ear is
  at u = πN/(N+1), hard against the right edge of the panel; the label now goes
  on the side away from the edge.
- **The amplitude bars drew their harmonic numbers twice.** The x ticks are the
  harmonic numbers already, and a second row on the same baseline read as 11
  text collisions in the audit.

### Known-bad candidates

- **A model function with a correct signature can still be called with its
  arguments in the wrong roles, and no assertion on the function catches it.**
  `phaseOf(domain, x, t)` is right; passing the time axis's abscissa as `x` is
  wrong, and produced a flat line in three views while 6188 assertions stayed
  green. Assert something about the DRAWN curve — that it varies, that it is
  periodic over the window — not only about the function it came from.
- **Two screens sharing one state array is a reset bug waiting to happen.**
  PhET keeps a separate Fourier series per screen for a reason. Here one shared
  amplitude array meant the game's reset wiped the Discrete screen's preset at
  boot; the UI drive caught it only because it asserted PhET's start state
  explicitly.
- **A partial sum's symmetry can hand a peak-finder the wrong extremum.** Only
  odd harmonics survive u → π − u, so a square wave's Gibbs ear has an exact
  mirror at the same height. Search next to the jump, not over the half period,
  and assert the symmetry so the reason is testable.
- **Sampling a drawn curve coarser than its own structure is an alias, not a
  simplification.** 5 samples per cycle draws a curve that is not the one asked
  for. Set the sample count from the phase excursion, or narrow the window and
  print the zoom.
- **PhET's hard-coded tables can carry typos.** The wave-packet preset's N = 10,
  n = 2 entry is 1.0e-5 off the Gaussian every other entry follows. Pin both
  numbers rather than matching the table.

## 2026-09-22 — bending-light: PhET's Bending Light remade, with Snell, the Fresnel equations, PhET's dispersion model and a prism ray tracer all solved exactly

### Added
- **`docs/phets_revised/bending-light.html`** (227 KB, 4 149 lines) — a clean-room
  remake of PhET Interactive Simulations' *Bending Light* 1.2.5
  (`docs/phets/bending-light_en.html`), in the house six-view form. PhET's three
  screens map to the first three views; the last three are the analysis views.
  - **the boundary** — PhET's Intro screen. A laser you swing about the origin
    (drag its body) onto the interface between two media, with the reflected and
    transmitted rays drawn in the true CIE colour of their wavelength at their
    own share of the power, the normal, the angle arcs, PhET's protractor, PhET's
    intensity meter and the critical-angle line. White light draws the incident
    and reflected rays ONCE, in white — reflection does not disperse — and fans
    only the transmitted ray.
  - **the wave** — PhET's wave view and the two More Tools meters. Crest lines of
    the incident, reflected and transmitted waves; the time-averaged intensity
    painted behind them, which is the standing-wave pattern above the boundary
    and the (decaying) transmitted intensity below; ticks on the boundary at the
    crest positions, whose spacing IS Snell's law; a field profile on the cut
    x = 0 with its envelope; and PhET's wave sensor as two probes against time.
    The evanescent tail past the critical angle is drawn and labelled; PhET
    draws nothing there.
  - **the prism** — PhET's Prisms screen. PhET's own five prism prototypes at
    PhET's own size, traced by exact ray/polygon and ray/circle intersection with
    vector Snell at every face, total internal reflection where the geometry
    demands it, PhET's optional partial reflections and normals, and white light
    dispersed into a spectrum.
  - **the reflected fraction** — the Fresnel equations drawn: R and T for s and p
    against the angle of incidence, Brewster's angle where R_p is exactly zero,
    the critical angle where R becomes exactly one, the phase of the reflected
    amplitude (the pi jump at Brewster, the Goos–Hänchen slide past theta_c), and
    R(0) against the index ratio.
  - **the spectrum** — PhET's dispersion model made visible: n(lambda) − n(650 nm)
    for every substance (every curve the same shape, scaled), the CIE 1931 colour
    of each wavelength under the axis, the deviation of a 60-degree prism against
    wavelength, and the exit fan with its exaggeration printed.
  - **the rainbow** — Descartes' stationary deviation in a sphere of water: the
    caustic drawn from the rays themselves (both signs of the impact parameter),
    D(theta_i) for one and two internal reflections with the stationary points
    marked, the primary bow at 42.13 degrees and the secondary at 50.79,
    Alexander's dark band, and the Fresnel weights that say why a bow is faint and
    polarised.
- **What is exact**, all pinned in `selfTest` against printed lines of
  `build/bending-light/refvals.txt` (the output of `derive.py`, an independent
  Python solve with `scipy.minimize_scalar` on the prism and the rainbow):
  - Snell's law over eight medium pairs × eight angles to 1e-12 deg, in both
    directions; theta_2 = 90 deg EXACTLY at the critical angle and no solution one
    part in 1e12 past it; every refraction round-trips to 1e-14 rad; the cubic
    term of the small-angle limit measured and matched to −(r − r³)/6 (a limit
    asserted by its rate of approach, not its destination).
  - The Fresnel equations in both polarisations: R + T = 1 to 5e-15 over eight
    pairs × 601 angles; R_p = 0 at Brewster to 1e-30 and theta_B + theta_2 = 90 deg
    to 1e-12; R = 1 exactly at and past theta_c; R(0) = ((n1−n2)/(n1+n2))²; the
    beam-width factor (n2 c2)/(n1 c1) shown to be 0.32 of T at 50 deg, so it is
    not a normalisation; T(1→2) = T(2→1) to 1e-13.
  - The wave: lambda_0/n, c/n, the frequency invariant, the crest spacing along the
    boundary matched to 1e-15, 1 + r_s = t_s and the magnetic-field condition to
    1e-14, the PAINTED field continuous across y = 0 over 16 geometries × 5 places,
    and the painted intensity equal to a 720-point time average of the drawn field.
  - The prism: the traced deviation against the two-surface closed form at four
    entry angles and against n = sin((A+D_min)/2)/sin(A/2) to 1e-11 deg — two
    routes that share no arithmetic; a slab shown to displace without deviating;
    a ray through the centre of the circle undeviated; the semicircle aimed at its
    centre leaving at exactly the Snell angle of its flat face; five traced-ray
    references (segment counts, total lengths, exit directions, branch powers) with
    and without the partial reflections.
  - The rainbow: cos²theta = (n²−1)/(k²+2k) against scipy's minimiser to 3e-7 deg
    for k = 1, 2, 3, with dD/dtheta = 0 there and D larger on both sides; the bow
    angles of five wavelengths at both orders; and **two exact identities** derived
    here and asserted: at the stationary ray the internal reflectance is
    R_s = (k/(k+2))², *independent of the index*, and the whole s-polarised
    throughput of the k-th bow is (1−R)²R^k — 64/729 for the primary, 9/256 for the
    secondary.
  - The colour path: `derive.py` parses the CIE 1931 table back out of `p2_cie.js`
    and re-evaluates it in Python, so the eight monoLinear triples, the eight sRGB
    byte strings and the seven monoLevel values are pinned against an independent
    evaluation of the same published numbers rather than against themselves.
  - The world's wavenumber and the evanescent decay, both pinned absolutely and
    then MEASURED off the drawn field: `k0` per world unit at five wavelengths;
    the crest spacing along the boundary read off `waveAt` by bisected zero
    crossings; the standing-fringe period read off `meanIntensity` by
    parabola-refined maxima; kappa/k0 and 1/kappa in nanometres at three angles
    for three medium pairs at two wavelengths, with the decay rate recovered
    from the ratio of the drawn field at two depths; and, below the critical
    angle, the contract that there is no decay at all.
- `selfTest` **866 passed, 0 failed**; UI drive **432 passed, 0 failed**; layout
  audit clean over 32 captured configurations; 32 PNGs looked at.
- `mutants.json` carries **113 mutants (95 physics, 18 UI)**, every `old` checked
  unique by `check_mutants.py`. Full sweep by the orchestrator: **113 caught,
  0 survived** (the first 109-mutant sweep found two survivors, both closed
  below and each re-verified caught).

### Fixed (during the build)
- **The prism tracer's ray/segment parameter had the wrong sign, and the copy of
  the formula inside `shape_hit` was fixed a second time.** `u = (q×d)/(−den)`
  instead of `/den` made the semicircle's flat face unreachable: a ray aimed at
  its centre crossed the curved face and then missed the shape entirely,
  emerging undeviated. Symptom: two segments instead of three and an exit angle
  of −20 deg where Snell demands −30.86. Root cause: the same eight lines written
  twice (polygon edge and flat face), so fixing one left the other wrong — the
  drum's group-velocity lesson again.
- **A white beam drawn as thirty translucent strokes is not white.** Source-over
  compositing is not addition, so whichever end of the spectrum is painted last
  simply wins: the prism's white light came out crimson, and re-ordering the
  wavelengths outward-in only changed it to green. Root cause: the same defect as
  `lenses.html`'s four Fraunhofer lines reading as one red beam, thirty layers
  deep. Fixed with a geometric rule that is also a true statement —
  `mergeMask()` asks, per segment, whether the thirty wavelengths still lie within
  a line width of one another; where they do the beam is drawn ONCE in white,
  where they do not it is drawn one wavelength at a time. It is a model function,
  so `selfTest` asserts that the beam arriving at the prism merges and the beam
  leaving it does not, and that the rule tightens and loosens with the scale.
- **The prism's default beam sat on a constant-deviation path.** At tilt −7 deg the
  ray entered the left face, total-internally reflected off the right face and
  left through the bottom — an arrangement whose deviation is nearly achromatic
  (0.037 deg of spread against 1.6 deg at minimum deviation). The tracer was right
  and the picture was useless. The default is now aimed at the left face near the
  minimum-deviation angle; `selfTest` asserts both spreads, so the achromatic path
  is recorded as physics rather than forgotten as a bug.
- **The rainbow's emergent ray was drawn by turning the incoming direction through
  D, in the wrong sense.** The exit rays left up-and-right instead of back toward
  the antisolar direction. Root cause: a drawing that re-implements the model's
  arithmetic instead of using the model. `dropPath` now refracts at the exit face
  and returns that direction, and `selfTest` asserts it equals −D (mod 2 pi) over
  three orders × four impact angles — which is what ties the picture to `rainDev`.
- **The wave field painted on a cell grid aliased into a checkerboard and drowned
  the crest lines**, and cost 7 400 fillRects at 1400×820. Replaced by the
  time-averaged intensity, which depends on y alone and is therefore 140
  horizontal bands, smooth, and physically the standing-wave pattern; the crest
  lines carry the instantaneous phase on top of it.
- **Rays were not clipped to the world box**, so the prism and boundary views drew
  over the caption and off the canvas. Clipped in DATA space (Liang–Barsky), never
  `ctx.clip()`, because the recorder stubs `clip` and the audit would still lie.
- **The op-count floor of the layout sweep was copied in from a field-map sim.** A
  ray diagram is a dozen strokes and almost no fills, so a fills-only floor of 6
  failed five correct views. Floors are now counted over fills PLUS strokes and
  derived per configuration from what the sim actually emits (`opcount.js`).
- **Two dirty flags on one path made each other's mutant equivalent.** The
  `pointerdown` handler set `dirty` as well as the `pointermove` handler, so
  either could be deleted with no test failing. The down handler no longer sets it
  (a down changes nothing on screen); and the drag test now measures the repaint
  BETWEEN the move and the up, because the `pointerup` handler calls `refresh()`,
  which draws unconditionally — and re-proves idleness after its own baseline
  draw, because `forceDrawU()` is a tab click and `setView` sets `dirty` itself.
- **A drag test that only checks "the value changed" passes a mutant that pins the
  value to a constant.** The prism beam drag compared against the default, and a
  mutant that froze the beam at 1.3 differed from the default by more than the
  threshold. The test now drags twice, in opposite directions, and asserts the
  beam follows the pointer both times.
- **`fresnel()` carried an evanescent decay constant that nothing read** — the
  full sweep's first survivor. Every consumer (`waveAt`, `meanIntensity`, the
  readout, the drawing) takes kappa from `fresnelSComplex`, so mutating
  `fresnel()`'s copy from `n2 g` to `n1 g` provably could not change any output.
  Root cause: the same quantity computed in two places, one of them unreachable.
  Deleted, with `fresnelSComplex` named in a comment as the only owner — and,
  because that is the shallow half of the finding, the LIVE kappa was pinned
  properly: its old check compared `exp(-kappa|y|)` against a ratio of `waveAt`
  to itself, both sides built from the same kappa, so it was blind to a wrong
  one as well. It is now asserted absolutely against `derive.py` (kappa/k0 and
  1/kappa in nm, three angles x three pairs x two wavelengths), recovered by
  measurement from the drawn field (under total internal reflection the
  transmitted phase does not depend on depth, so the ratio at two depths IS
  exp(kappa dy)), and the readout's printed decay length is asserted to contain
  "124.8". Four new mutants cover it, including one that gives a PROPAGATING
  transmitted wave a decay — which no ratio of the field to itself could see,
  and which is caught by the flat-intensity contract.
- **Every wave assertion was taken at 650 nm, where `k0` is 2 pi whichever way
  round the ratio is written** — the sweep's second survivor. `k0 = 2 pi
  (lambda_red/lambda)` per world unit inverted to `2 pi (lambda/lambda_red)`
  and 866 assertions stayed green, because one world unit IS one red
  wavelength and the reference wavelength is the default. Root cause: exactly
  the w = -1 dark-energy exponent on this list — a parameter has a value at
  which it stops mattering, and the whole suite was sitting on it. Fixed by
  pinning `k0` at 380, 400, 500, 650 and 700 nm against `derive.py`, asserting
  that halving the wavelength doubles it, measuring the crest spacing and the
  standing-fringe period off the drawn field at 400, 500 and 650 nm, walking
  the field-continuity and mean-intensity sweeps across the band instead of
  parking them at 650, and adding violet and deep-red wave configurations to
  the layout sweep.
- Smaller ones: the caption ran under the house `#hint` (fixed with
  `stageLayoutH`, reserving HINT_H); notes under a panel landed on the axis
  labels or on a legend (`axesRB` registers the two tick strips, `legendA`
  registers the legend box, `noteIn` puts the note inside the plot); the
  intensity meter's "100.0%" ran into its polarisation tag (three lines now, and
  it picks a corner that no label occupies); the spectrum's colour strip covered
  its own tick row (drawn inside the box); the spectrum's main panel plotted n
  itself, on which every curve looks flat (it plots n(lambda) − n(650) now, with the
  absolute index in the legend); the rainbow's info block was unreadable over the
  ray fan (it has a pad, which is deliberately NOT registered — registering it
  made `lab()` dodge it and put the first line outside the panel).

### Known-bad candidates
- **Source-over compositing is not addition, so N translucent strokes on one path
  can never make white.** Ordering them does not help: with alpha a, the last
  five of thirty layers carry 1 − (1−a)⁵ of the result whatever the order, so the
  pile takes the colour of whichever end was painted last (crimson if red is last,
  green if the luminous middle is). Drawing each layer with alpha 1/k makes the
  composite the exact average but leaves the last layer at 3 % where the paths
  separate. The fix that works is geometric: decide per segment whether the
  wavelengths are still within a line width of each other, draw white where they
  are and one at a time where they are not — and make that decision a model
  function so it can be asserted rather than looked at.
- **A prism geometry can be achromatic, and the tracer will be right while the
  picture says nothing.** In-left, TIR-right, out-bottom of an equilateral prism
  is a constant-deviation arrangement: the reflection undoes most of the entry
  dispersion, leaving 0.037 deg of spread instead of 1.6. A default that lands
  there makes "white light through a prism" draw a single white line. Check the
  spread the default geometry actually produces, and assert it.
- **The same eight lines of ray/segment intersection written twice will be fixed
  once.** The polygon edge loop and the semicircle's flat face carried the same
  sign error in the parameter along the edge; correcting the first left the
  second silently returning "no hit", which reads as a ray passing through a
  surface rather than as a bug in a formula.
- **A drawing that re-derives the model's own arithmetic will disagree with it.**
  The rainbow's emergent ray was constructed by rotating the incoming direction
  through the deviation, and got the sense wrong; the fix was to refract at the
  exit face — i.e. to let the drawing ASK the model — and to assert that the two
  agree. Same family as the Mach-cone tangency: assert on the objects the view
  draws, not on the formula beside them.
- **An op-count floor must be derived from what the file emits.** A ray diagram is
  a dozen strokes and five fills; a floor tuned on a sim that paints a field map
  fails it for being efficient, and counting only fills fails it twice over.
- **Two dirty flags on one path, and a `pointerup` that calls `refresh()`, make a
  drag test blind.** Measure the repaint between the move and the up, keep one
  flag, and re-prove idleness after any forced baseline draw — a tab click is a
  forced draw.
- **A drag test must assert the control FOLLOWS the pointer, not merely that it
  differs from its default.** A mutant that freezes it at any other constant
  passes the weaker test.
- **A decay constant checked by comparing exp(-kappa y) against a ratio of the
  field to itself is not checked at all** — both sides are built from the same
  kappa, so the comparison is an identity. Pin it against an outside number, and
  recover it by MEASUREMENT from the drawn field: past the critical angle the
  transmitted phase does not depend on depth, so the ratio of the field at two
  depths is exactly exp(kappa dy) and its logarithm gives kappa back. The other
  half of the contract needs stating too: BELOW the critical angle there is no
  decay at all, which only a flat-in-depth assertion can see.
- **A world whose unit is the reference wavelength makes the reference
  wavelength the one place a wavenumber cannot be wrong.** `k0 = 2 pi
  (lambda_ref/lambda)` per unit is 2 pi at lambda = lambda_ref whichever way the
  ratio is written, so a suite that takes every wave assertion at the default
  wavelength is blind to the inversion. Same family as the w = -1 dark-energy
  exponent: spread the assertions across the band, and assert the SCALING
  (halving the wavelength doubles the wavenumber) as well as the values.
- **The quantity computed in two places will be pinned in the place nothing
  calls.** `fresnel()` and `fresnelSComplex()` both derived the evanescent
  kappa; the dead one is what the mutation sweep flagged, and the live one
  turned out to be unpinned too. Delete the copy, name the owner in a comment,
  and check that the surviving one is asserted against something outside
  itself.

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

## 2026-09-22 — concentration: PhET's Concentration screen on beers-law-lab's engine, with the mole ledger drawn as a ledger and the nine solutes against their sources

### Added
- **`docs/phets_revised/concentration.html`** — a remake of PhET Interactive Simulations'
  Concentration (concentration 1.8.6, CC-BY 4.0), which is the Concentration screen of
  Beer's Law Lab shipped on its own. Four views: **the beaker** (nine solutes, a shaker and
  a dropper, a water faucet, a drain, an evaporator, the concentration meter on a draggable
  probe reading mol/L or mass percent, and the saturation point where solid appears),
  **the ledger**, **the solutes** and **true colour**.
- **The same engine as `beers-law-lab.html`, not a copy of it.** `build/concentration/`
  holds exactly two files of its own — `p1_head.html` (its header and tagline) and
  `p2b_id.js` (its identity and its four tabs, and the `SHOW_BEERS = false` that switches
  the cuvette off). Everything else is read from `build/beers-law-lab/` **by path** at
  assemble time: the data, the chemistry, the state, the beaker, the ledger and colour
  views, boot, the reference table and the whole selfTest. The UI drive is the same harness
  too, copied rather than shared only because `_tools/verify_one.py` insists on the name
  `ui_drive_<stem>.js`, and the copy is rewritten on every assemble so the two cannot drift.
- **The solutes view** is this sim's own, and is where the literature comparison the family
  owes its data lives: PhET's nine saturation points against the Wikipedia chemical
  infoboxes (fetched 2026-09-22, quoted to their own printed precision), with the
  temperature each source states printed beside every row, and the molar masses below. PhET
  matches the literature to **5.6e-5** relative on molar mass and to 0.0–0.6 % on saturation
  for the four sources that quote a room-temperature figure; the worst gap is cobalt(II)
  nitrate at 23 %, whose only usable figure is at 0 °C, and the row says so rather than
  hiding it.
- Everything the shared engine asserts is asserted here too — the exact mole and volume
  ledgers, saturation, the evaporation hyperbola, PhET's colour interpolation and its
  `Math.floor`, the transmitted colour over the CIE 1931 observer — and the pieces that
  belong to the Beer's Law bench are skipped by `SHOW_BEERS`. See
  `build/beers-law-lab/changelog_entry.md` for the derivation and the sources.
- **Verification**: `selfTest` 510 assertions, 0 failed; UI drive 205, 0 failed; display-list
  capture at 1400x820, 1100x700 and 560x380, `audit.py` clean at all three, every view's PNG
  looked at. `mutants.json` carries **61 mutants (52 physics, 9 UI)**, and the sweep run here
  caught **61 of 61** with no survivors.

### Fixed (during the build)
- **The solutes view was laid out for a 1400 x 820 stage and nowhere else.** Nine rows of
  two lines need about 30 px a row; at 1100 x 700 the panel gives 22 and every row landed on
  its neighbour (95 collisions). It now measures what it has: two lines a row above 30 px,
  one line with the numbers pushed right below that, and bars only below 15 px, with the
  molar-mass table dropped entirely at narrow widths so the rows get the whole stage.
- **Its row labels were painted ON the bars**, so a green name sat on a green bar and the
  numbers on an orange one. The text has the top of each row to itself now.
- **Its rows ran bottom to top**, putting PhET's first solute at the foot of a list whose
  own narrow-stage note said "top to bottom in PhET's order".
- **A legend had nowhere to go.** At one line a row the text fills the panel edge to edge,
  so any legend sits on top of it; the two colour roles moved into the axis title, which is
  always there and needs no space of its own.
- **With no bottom row, the main panel ran to the caption** and its x tick labels (which
  hang 21 px below the box) landed in it. `layoutPanels` now shaves 30 px when it builds no
  bottom row.
- **Five mutants survive this sim's sweep for a reason that is not a gap**: the beam's
  width, the sensor's, the cuvette's snap interval, the preset wavelength and the
  per-solution default concentration belong to the Beer's Law bench, which this sim does not
  build. They are swept in `beers-law-lab`, where they are live, and are excluded here with
  that written into `gen_mutants.py` rather than reported as survivors.

### Known-bad candidates
- **A trimmed variant built on a shared engine will carry code it cannot reach, and a
  mutation sweep will call every constant in it a survivor.** Either split the part files so
  the variant does not ship the code (which is what was done for the cuvette, the spectrum,
  the law and the solutes views here), or exclude those mutants by name with the reason
  written down. A survivor that is "this sim has no cuvette" looks exactly like a survivor
  that is a missing assertion.
- The rest of this family's traps are on `build/beers-law-lab/changelog_entry.md` and apply
  to both files, because both files are the same code.

## 2026-09-22 — beers-law-lab: PhET's two screens, with the mole ledger closed to the last bit and the transmitted colour worked out over the CIE observer

### Added
- **`docs/phets_revised/beers-law-lab.html`** — a remake of PhET Interactive Simulations'
  Beer's Law Lab (beers-law-lab 1.8.7, CC-BY 4.0), six views: **the beaker** (PhET's
  Concentration screen: nine solutes, a shaker and a dropper, a water faucet, a drain, an
  evaporator, the concentration meter on a draggable probe, and the saturation point where
  solid appears), **the cuvette** (its Beer's Law screen, drawn to scale in centimetres,
  with a draggable cuvette wall that snaps to PhET's 0.1 cm on release and a draggable
  detector probe), **the spectrum**, **the law**, **the ledger** and **true colour** (this
  file's own analysis).
- **Exact, and asserted as exact.** `A = eps l c` and `T = 10^-A` against 50-digit
  `decimal` over 8 solutions x 4 path lengths x 4 concentrations: worst relative error
  2.7e-16 on the product, 4.7e-16 on the power, 1.4e-16 on the round trip
  `-log10(10^-A) = A`. The end-to-end error in T is deliberately **larger** (1.2e-15) and
  the suite asserts the `ln10 * A` amplification that explains it rather than pretending it
  is not there. Both extremes are pinned: `A = 0` gives `T = 1` exactly, `A = 1` and `A = 2`
  give exactly 10 % and 1 %, `10^-A` underflows a double to exactly zero at **A = 324** (found
  by search, not assumed) and the value one below it is a denormal, and a detector reading
  0 % T inverts to `+Infinity` — no finite absorbance produces it.
- **The beaker is a mole ledger and it closes.** PhET's five mechanisms in PhET's order
  (faucet, drain, dropper, evaporator, shaker), each returning what ACTUALLY moved.
  `derive.py` runs a 900-frame script through all five twice — once in doubles, once in
  exact `fractions.Fraction` — and both ledgers close, the rational one identically and the
  double one to **0.0 mol and 0.0 L**, with the two runs agreeing to 4.4e-15. The JS runs
  the same script and reaches the twin's 1.14375 mol once the last grain lands. The ledger
  closes **through** the clamps too (a beaker filled past the brim, a drain asked for more
  than is there, the 7 mol ceiling).
- **Saturation, exactly**: `C = min(Csat, n/V)`, `solid = max(0, n - V Csat)`, and
  evaporating a fixed n climbs the exact hyperbola `n/V` to `V = n/Csat` and is flat after
  it. The drain is the subtle one and is asserted: it removes SOLUTION, so it carries
  solute at the DISSOLVED concentration and leaves the precipitate behind (0.138 mol out of
  a saturated CuSO4 beaker against a naive 0.200).
- **PhET's data, read out of the original and never typed.** `extract_phet.py` parses the
  minified build for the nine solutes (molar mass, stock, saturation, all three colour
  stops), the eight Beer's Law solutions, the **eight molar-absorptivity spectra at one
  value per nanometre from 380 to 780 nm**, the beaker's 1 L, the 0–7 mol and 0–1 L ranges,
  the 0.5–2 cm cuvette and its 0.1 cm snap, the flow rates and every decimal-place count;
  `make_data.py` writes them into the file.
- **Literature beside PhET's** (Wikipedia chemical infoboxes, fetched 2026-09-22, quoted to
  their own printed precision, converted on the stated assumption that a litre of water
  makes a litre of solution): PhET's molar masses match to **5.6e-5** relative, and its
  saturation points to 0.0–0.6 % for the four whose sources quote a room-temperature figure
  (K2CrO4, KMnO4, NiCl2, K2Cr2O7). The worst gap is cobalt(II) nitrate at 23 %, whose only
  usable infobox figure is at 0 °C, and the view says so. PhET's "drink mix" carries
  **sucrose's** molar mass to a milligram per mole.
- **No molar-absorptivity literature value could be sourced offline.** Three sources were
  tried and all three carry only qualitative colour: Wikipedia's "Molar attenuation
  coefficient" (no numerical example for any substance), "Metal aquo complex" (a colour
  column, no wavelengths and no coefficients) and "Permanganate" (a spectrum figure, no
  printed lambda_max and no epsilon). The spectra therefore stand as PhET's own digitised
  data, are labelled that way on the canvas and in the panel, and no comparison is invented
  for them. "Still unverified" is the honest answer for those eight curves, and the file
  says so.
- **The true transmitted colour**: `T(lambda) = 10^-eps(lambda) l c` at every nanometre,
  integrated against the CIE 1931 2° observer **on the same 1 nm grid the spectra live on**
  (CIE_xyz_1931_2deg.csv, DOI 10.25039/CIE.DS.xvudnb9b) — nothing interpolated, nothing
  resampled — then adapted so the illuminant itself renders exactly white, which needs no
  white-point constant and makes an empty cuvette rgb(255,255,255) under either illuminant.
  Two illuminants, because no D65 spectrum could be sourced offline: equal energy (flat by
  definition) and CIE standard illuminant A from the CIE's own formula. PhET's ramp is
  nowhere within **68 of 255** on its worst channel, and the sharpest difference is not
  brightness: PhET's ramp has no path length in it at all.
- Findings worth keeping, each derived rather than recalled: PhET's `Color.interpolateRGBA`
  **floors** each channel, so halfway from (224,255,255) to (255,225,225) is (239,240,240);
  the Beer's Law ramp has a genuine **step at c = 0**; `eps(lambda)` is a LOOKUP indexed by
  `floor(lambda - 380)`, so 500.0 nm and 500.9 nm read the same cell; copper sulfate's
  lambda_max is the LAST sample (780 nm) because its band is in the infrared and PhET's
  table stops where the eye does; **every one of PhET's nine stock solutions is below its
  own saturation point**, so the dropper can never saturate a beaker and a drop of stock
  into a saturated one dissolves solid; and PhET's own `doc/model.md` disagrees with PhET's
  own code twice (it clamps the concentration against the STOCK concentration where the code
  clamps against the SATURATED one, and writes the precipitate as a difference of
  concentrations where the code takes a difference of moles) — the code is what is
  implemented here.
- **Verification**: `selfTest` 552 assertions, 0 failed; UI drive 323, 0 failed (every tab,
  every visible slider at its ends, every checkbox, every chip, every button, the keys,
  resize, three custom drags each proven-idle-first and one axis at a time, and reset-all
  against a fully disturbed state including the beaker, which is not a slider value);
  display-list capture at 1400x820, 1100x700 and 560x380, `audit.py` clean at all three, and
  every view's PNG looked at. `mutants.json` carries **71 mutants (57 physics, 14 UI)**, and the sweep run here
  caught **71 of 71** with no survivors.

### Fixed (during the build)
- **The shaker's over-delivery was blamed on the wrong half of PhET's expression.** PhET
  makes `round(max(1, rate * particlesPerMole * dt))` grains a frame. The first draft said
  the `max(1, ...)` FLOOR is what makes it deliver 0.30 mol/s against its nominal 0.20 at
  60 fps. It is not: the bracket is 0.6667 there and `Math.round` takes that to 1 with or
  without the floor — the ROUNDING does it. The floor bites only above about 80 frames a
  second, where the same shaker delivers **0.60 mol/s**. Both are now derived and pinned at
  60 fps, 120 fps and a whole-second step, which is also what makes the mutant that deletes
  the floor catchable: while the only frame rates asserted were ones at which the floor does
  nothing, that mutant survived.
- **Six survivors of the first 58-mutant physics sweep, one at a time.** (1)+(2) Nothing
  drained or evaporated a beaker PAST empty, so the floor clamp in `bkRemoveSolvent` and the
  use of the actually-moved volume in the drain were both untested — they differ from their
  mutants only when the clamp bites. (3) EQUIVALENT: every one of PhET's nine solutes has
  `cMin = 0` and a minColor equal to the water colour, so two of `SoluteColorScheme`'s four
  branches cannot fire; the data property is asserted instead and the two mutants are left
  out with that as the stated reason. (4) `srgbGamma`'s LINEAR segment was reached by no
  assertion — every colour the suite checked was either black or far above the knee. (5)
  **Two guards on one path** (Known-bad, buoyancy.html): `trueRGB` clamped its linear
  channels at zero and `srgbGamma` clamps again, so each made the other's mutant equivalent;
  one guard now, in the function that owns the transfer curve. (6) The ledger view's drawn
  curve is capped at Csat and only its finiteness was asserted, not the cap.
- **`bezierCurveTo` is not in the display-list recorder**, so the meter's wire, the
  detector's wire and the evaporation squiggles recorded as nothing at all and threw under
  the selfTest stub. Drawn as explicit polylines — the same rule as the `ellipse()` entry on
  the Known-bad list.
- **The beam was painted UNDER the cuvette's own fill**, so the one thing the Beer's Law
  view exists to show — the beam dying as it crosses the solution — was hidden. And when
  that was fixed the beam's slabs were still drawn at bench positions 0–2 cm rather than
  inside the cuvette, because the bench's `X(cm)` had been re-based on the bench origin and
  the slab loop had not followed. Fill, then beam, then glass; slabs at `CUV0 + d`.
- **There was nothing to compare the outgoing beam WITH.** The source sat 14 px from the
  cuvette, so the undimmed run was invisible. The bench is now 8.4 cm at up to 120 px/cm
  with the source at one end and a real two-centimetre run before the glass.
- **Ninety text collisions, in four causes.** The caption is drawn LAST but owns the bottom
  of the stage from the moment it is measured, and nothing registered it, so every label
  that dodges collisions was dodging everything except the largest block of text on the
  screen. `legendAuto` dodges CURVES and not LABELS (Known-bad, pupil_plane), so every
  legend was free to land on one. The shared `axes()` takes a tick COUNT, and the count that
  suits a 1400 px stage puts eleven y labels in a 90 px panel at 560. And several labels
  were placed with `lab(rc, 1e5, 1e5, ...)`, which switches off the helper's own clamp to
  the canvas. Fixed by `noteCaption`, `legendFit` (both registries, and it records its own
  box), `axesFit` (counts from the panel's own size, and it drops the x tick sitting exactly
  on the left edge because the y label at that corner is a pixel away from it), and real
  W/H everywhere.
- **The solutes view was laid out for one stage size.** Nine rows of two lines need 30 px a
  row and at 1100x700 it has 22; its row labels were painted ON the bars, so green text sat
  on a green bar; and its rows ran bottom to top, putting PhET's first solute at the foot of
  a list the narrow-stage note called "top to bottom in PhET's order". Now: text above the
  bars, PhET's order downwards, one line a row below 30 px, bars only below 15 px, the
  molar-mass table's column count from the panel's height and its numbers measured against
  the column before they are drawn.
- **Saturated! was dark orange on a bright blue solution**, over the grains. It has a pad of
  its own above the liquid now. The precipitate was drawn in the solute's own saturated
  colour on top of a solution of very nearly that colour — at 1.38 M of copper sulfate the
  grains were invisible; drawn dark with a light speckle.
- **The beaker sat in the bottom third of an 820 px stage** with four hundred pixels of
  nothing above it, because its height was capped at 250 and it was pinned to the floor.
- **The errbox showed a stack and no message.** JavaScriptCore's `Error.stack` carries only
  the frames, so the harness was told where and not what; `fail()` now prints both, which is
  how the two `bezierCurveTo` faults were found in one run each instead of by bisection.

### Known-bad candidates
- **The rasteriser has no letter super/subscripts, and `10^-A` written with U+1D2C is
  tofu.** The BRIEF already says letter subscripts are unsafe; superscript capital A
  (U+1D2C), superscript small c (U+1D9C) and U+141F are not in DejaVu Sans either, so
  `10⁻ᴬ` and `10⁻ᴱᐟᴸᶜ` render as boxes. Digit superscripts are fine. Write exponents on the
  canvas as `10^-A`.
- **`bezierCurveTo`, `quadraticCurveTo` and `ellipse()` are all invisible to
  `tools/recorder.js` and absent from the selfTest stub.** A curve drawn with one records as
  nothing and throws headlessly. Draw them as explicit polylines (the same lesson the
  mosquito's body taught in `pupil_plane_interferometry.html`, one primitive wider).
- **The caption is drawn last and occupies the stage the whole time.** Register its measured
  rectangle in `LABELS` at layout time or every dodging label will dodge everything except
  it. Ninety collisions in this file came from that one omission.
- **`legendAuto()` checks `POLY_SEGS` and not `LABELS`, and records nothing of its own.**
  Use a wrapper that tests both registries and pushes its own text box, or legends and
  labels will keep landing on each other in both directions.
- **One tick COUNT cannot serve a 1400 px stage and a 560 px one.** Derive `nx`/`ny` from
  the panel's own width and height. And the x tick that sits exactly on the left edge
  collides with the y tick label at the same corner by about a pixel — drop it.
- **A frame-rate-dependent particle rule is a rate you did not choose.**
  `round(max(1, rate * n * dt))` delivers `rate` only when `rate * n * dt` is a whole number:
  at 60 fps PhET's shaker is 50 % fast and at 120 fps it is 200 % fast. Before blaming a
  floor or a rounding for an over-delivery, evaluate the expression at more than one frame
  rate — the half that does it changes.
- **Two guards on one path make each other's mutant equivalent** (already on the list from
  `buoyancy.html`, and it happened again here between `trueRGB`'s `Math.max(0, ...)` and
  `srgbGamma`'s own clamp). One guard, in the function that owns the quantity.
- **A branch that cannot be reached with the shipped data is not covered by anything, and
  the honest fix is to assert the data property rather than to delete PhET's branch.** Two
  of `SoluteColorScheme`'s four are unreachable because every solute has `cMin = 0` and a
  minColor equal to water.
- **PhET's `doc/model.md` is not PhET's code.** For beers-law-lab it writes the concentration
  clamp against the stock concentration (the code uses the saturated one) and the precipitate
  as a difference of concentrations (the code takes a difference of moles). Read the
  minified build, not the prose.

## 2026-09-22 — geometric-optics: PhET's lens and mirror benches, with the thin-optic equation solved exactly and every ray traced to agree with it

### Added

`docs/phets_revised/geometric-optics.html` (188 KB, six views), a clean-room
remake of PhET Interactive Simulations' **Geometric Optics** (build 1.3.16;
University of Colorado Boulder, CC-BY 4.0). New code; no PhET code or assets.

- **the lens bench** — PhET's Lens screen. Drag the object (pencil, penguin,
  star, arrow or a point light source) in front of a convex or concave lens;
  PhET's four ray modes (marginal, principal, many, none), F and 2F on both
  sides, a second point of interest, a virtual-image toggle, PhET's guides, the
  260 cm ruler, and — with the light source — the projection screen with its two
  light spots.
- **the mirror bench** — PhET's Mirror screen: concave, convex or flat, with F
  and 2F on the side the mirror actually has them (left for concave, right for
  convex, neither for flat — PhET's own `doc/model.md`).
- **the conjugate curve** — d_i against d_o as the rectangular hyperbola it is,
  with the asymptotes d_o = f and d_i = f, the magnification below it, and the
  pole at d_o = f where the equation has no answer.
- **the lens maker** — the (n, R) plane with the contours of f = R/2(n−1), which
  are straight lines through n = 1; PhET's two focal-length models and the
  hand-off between them; and the shape PhET's artwork draws against the sphere
  its numbers name.
- **the guides** — PhET's own construction, reproduced exactly and then measured.
- **the real lens** — the same index, radius and diameter built as two real
  spherical surfaces and traced with exact vector Snell.

**What is exact.** The thin-optic equation and everything that follows from it:
d_i = f d_o/(d_o − f) and m = −d_i/d_o are solved, and `selfTest` asserts the
residual 1/d_o + 1/d_i − 1/f against zero over 100 (f, d_o) pairs and against a
scipy `brentq` root of the same equation (3.4e-15 over 15 pairs); Newton's form
(d_o − f)(d_i − f) = f² holds to 4.5e-16 over 35 pairs. Ray tracing is not a
separate drawing: every outgoing ray is built from the one-line paraxial law
u′ = u − h/f, and the suite asserts that a ray leaving the object at **any**
height h on the optic lands on the image point the equation gives — worst
residual **1.79e-13 over 1200 configurations**, and that number is the lever arm
(at f = 80, d_o = 79.5 the image is 12 720 cm away), not the algebra. The three
principal rays meet at the image pairwise to **1.04e-15 over 360
configurations**. The lens maker's equation reduces to PhET's f = R/2(n−1) to
1.42e-16 over twenty (n, R) pairs. The light spot on the screen is the exact
cone from the lens rim through the image, D|x_s − d_i|/d_i, agreeing with the
two-ray construction to 0. The real lens's trace uses a closed-form sphere root
cross-checked against Newton on the sag (1.42e-14 cm over five heights), and its
longitudinal spherical aberration is shown to be O(h²) by **measured** ratios
(4.0091, 4.0023, 4.0006, 4.0001 per halving) rather than asserted to be. Every
reference value in `selfTest` is a printed line of
`build/geometric-optics/refvals.txt`, the output of `derive.py`.

**What is PhET's, and where it came from.** Read out of the minified build: the
40–120 cm focal-length and radius ranges and the 60–120 cm diameter for the lens,
75–150 and 150–300 cm for the mirror, the 1.2–1.8 index, the n = 1.5 the direct
lens model pins and the n = 2 that turns the lens maker's equation into the
paraxial mirror formula, the flat mirror's f = 100 000 cm stand-in, the object
positions, the −56.5 cm second point, the screen at 200 cm, the 120° fan and its
20·(⌊d_o/300⌋+1) ray count, the guides' own arithmetic, and the softened lens sag
(D/2)²/2(|R|+100) the artwork uses. PhET's `doc/model.md` prints the lens maker's
equation as f = R/2(1−n); its code computes the magnitude as |R|/2(n−1) and puts
the sign on from the surface type, which is what is implemented here.

**Three things this file measured about PhET that are worth recording.**

1. **Its guides are the thin-optic construction to second order and no
   further.** A guide rotates the ray through a fixed angle 2 arctan(D/4f) where
   a thin optic changes its *slope* by −h/f. At PhET's defaults the two
   transmitted arms cross **6.73 cm short of a 151.11 cm image — 4.40 %** — and
   shrinking the lens alone takes that to **4.548 %, not to zero**, because the
   surviving error is the u² of the ray's own inclination. Shrink the lens and
   the object's inclination together and the miss falls as e² (measured ratio
   3.996 per halving). Its two branches, 2 arctan r and arctan 3r − arctan r,
   differ by exactly 3 arctan r − arctan 3r = 8r³ + O(r⁵).
2. **Its flat mirror is not a plane.** f = 100 000 cm puts the image of an object
   at 150 cm at −150.2253 cm rather than −150, and m = 1.0015 rather than 1.
   Both numbers are printed rather than rounded away.
3. **Its artwork is not its model.** The drawn lens uses a softened sag, so at
   R = 80, D = 80 it draws 4.444 cm of half-thickness where the sphere it names
   has a 10.718 cm sag — and at R = 40, D = 120 it draws a lens whose surfaces
   could not meet. Taking PhET's default lens at face value as a real biconvex
   glass element (n = 1.5, R = ±80 cm, 80 cm across, 2 cm edge) makes it an f/1
   lens whose rim ray crosses **43.47 cm inside the paraxial focus, 51.7 % of the
   focal length**.

### Fixed (during the build)

- **The rays ran across the caption.** Symptom: in every bench capture the
  outgoing rays crossed the prose at the bottom of the stage and left the canvas
  sideways. Root cause: the drawn segments were emitted at a `reach` of 1.6 world
  widths with no clip — the house rule that everything drawn inside a frame is
  clipped to it had been read as covering axis-derived lines only, and a ray is
  data. Fixed with a Liang–Barsky clip in **world** space (`clipSeg`/`segW`); a
  canvas `ctx.clip()` would have fixed the browser and not the display-list
  audit, which records `clip()` as a no-op. `selfTest` now asserts that no
  emitted segment reaches the caption band or leaves the canvas, over ten
  configurations at two sizes, and the assertion was checked against the
  reintroduced defect (24 failures).
- **The concave mirror was drawn as a convex one.** Symptom: the arc's vertex sat
  nearer the light than its rim. Root cause: a sign — a concave mirror is the
  *inside* of a sphere whose centre of curvature is in front of it, so its rim
  reaches back toward the source (x < 0) and its vertex is the deepest point;
  the outline wrote `s*(-sag)` with s = −1 for concave. The physics was right
  throughout and only the picture was wrong, so nothing but a PNG could see it.
  The backing was wrong for the same reason (it is behind the mirror, +x, for
  both kinds). Pinned by asserting the rim's sign for both surfaces.
- **A flat mirror stretched the frame to 1640 cm for a 170 cm scene.** Root
  cause: the world extent reserved room for ±f and ±2f whether or not those
  marks were drawn, and PhET's flat mirror has f = 100 000 cm. The extent now
  takes only the focal points that are actually drawn, and the *side* they are
  drawn on is computed once in the model and used by both the extent and the
  drawing (it had been written in two places, and a number written twice is two
  numbers of which only one gets mutated).
- **`legendAuto` avoids curves, not labels.** It put the colour key on top of
  "Virtual Image" at 620 × 420 and on "r = D/4f" at 900 × 600. `legendSafe`
  checks both registries and then registers its own rectangle; where every
  corner is taken it draws nothing and the caption names the colours.
- **A caption that said "equal aspect" twice**, and three labels that landed on
  the thing they describe (the axis label on the object standing on the axis,
  the glass's own label across the lens, the dashed-reference note on the curve
  it names). The floating notes above the caption also collided with the bottom
  panel's axis label at every size that has one — every note is now folded into
  the caption itself, which is where a scale factor belongs.
- **Two UI-harness lookups found the wrong control.** Both the lens group and the
  mirror group carry a slider labelled "focal length", "radius R" and
  "diameter D", and a whole-panel walk returns the *mirror's* every time; four
  assertions failed for reasons that had nothing to do with the sim. Every
  lookup in `ui_drive_geometric-optics.js` is now group-scoped.
- **Three survivors of the physics pre-sweep, each fixed at its cause.** (i) The
  aperture test `|h| ≤ D/2` survived because the ray-count check re-typed the
  condition instead of reading `traceRay`'s own `missed` flag, and no probe sat
  between D/2 and D. (ii) `slopeCross`'s heights survived because *any* two
  distinct rays from one object point meet at the image, so the crossing cannot
  see which heights were used — the function now returns them and the suite pins
  that they are the guides' own fulcrum heights. (iii) The rim's x-coordinate in
  `spotEdge` survived because it is identically zero: the optic is at (0, 0) by
  construction. That is dead generality, so it was deleted rather than excused.
- **Two reference values had been read off the wrong row of `derive.py`.** The
  h² ratio labelled "1 to 0.5" is derive's 2→1 ratio, and the real-lens readout
  prints `84.106`, not `84.11` (four significant figures, not two decimals).
  Both are the same mistake: quoting a printed table without checking which line
  the number is on.
- **PhET signs a mirror's radius and its focal length by different rules**, which
  showed up as a failing assertion rather than as a bug here: a concave mirror
  gets R = −180 cm (convex-is-positive) and f = +90 cm (converging-is-positive),
  so for a mirror f and R/2 disagree in sign while their magnitudes agree. The
  suite asserts both halves of that.

- **Two silhouettes that did not survive being drawn.** The penguin was an
  octagonal blob at 80 cm tall, which defeats the point of an object whose top
  and bottom differ — an inverted image has to be recognisably upside down. The
  ruler's own name was drawn inside its band, on top of the zero tick, which is
  exactly where the eye goes first. Both found only by looking.

**Verification.** `selfTest` 901 passed / 0 failed (0.1 s under `jsc`, 0.4 s
under `osascript`); the UI drive 400 / 0; `tools/audit.py` reports 0 layout
problems at 1400 x 820 over 35 captured configurations and 0 at 820 x 520 over
six; every view's PNG was looked at. `mutants.json` carries **77 mutants (64
physics, 13 UI)**, every `old` pattern checked to occur exactly once by
`gen_mutants.py`; a pre-sweep in this build's own scratch directory
(`_out/presweep.py`, `jsc` for the physics suite and `osascript` for the UI one)
reports **77 caught, 0 survived**, and three separate hand-reintroduced defects
were each confirmed to fail their own assertion. The authoritative sweep is the
orchestrator's.

### Known-bad candidates

- **A ray is data, and data inside a frame gets clipped to it.** The rule on this
  list about clipping reference curves was read as covering lines drawn from
  *axis limits*; an optical bench draws rays from the model and they sprawl
  across the caption just the same. Clip in world space, not with `ctx.clip()` —
  the display-list recorder treats `clip()` as a no-op, so the captured geometry
  would still lie. The assertion that closes it is on the emitted geometry: no
  segment may reach the caption band.
- **A concave mirror's rim is NEARER the light than its vertex.** It is the
  inside of a sphere whose centre of curvature is in front of it. Getting this
  backwards draws a convex mirror under a concave label, with every number on
  the page correct, and no physics assertion can see it. Pin the sign of the
  drawn rim, for both surfaces, whenever a curved optic is drawn.
- **A frame sized from marks that are not drawn.** PhET's flat mirror carries
  f = 100 000 cm as a stand-in for infinity; reserving room for it squeezed a
  170 cm scene into 1640 cm of frame. Size the extent from what the view will
  actually paint, and compute "which side is F on" ONCE — it was written in the
  extent and again in the drawing, and only one of them would have been mutated.
- **Two panel groups that share a slider label defeat a whole-panel lookup.** The
  harness's `sliderU('radius R')` walked the whole panel and took the last
  match — the mirror's — so four assertions about the lens failed for unrelated
  reasons. When two groups can carry the same label, address the control by
  group and index, never by label alone (this is the `sliderU('offset')` entry
  from `lagrange_points`, one step worse: here the labels are *identical*).
- **Any two distinct rays from one object point meet at the image, so a
  crossing-point assertion cannot pin WHICH rays were used.** `slopeCross`'s
  ±D/2 survived a sweep for exactly that reason. When a construction's identity
  matters (here: it must be the guides' own fulcrum heights), return the inputs
  and assert them; the output is invariant to them by construction.
- **`legendAuto()` avoids curves and not labels** (already on this list from
  `pupil_plane`) — and the fix has to *register* the legend's own rectangle too,
  or the next label drawn lands on it instead.
- **PhET's guides are exact to second order in the ANGLE, not in D/f.** Shrinking
  the lens alone leaves a 4.5 % miss. A "small parameter" argument has to name
  which parameter: here rotating by a fixed angle where a thin optic changes a
  slope leaves an error of order u², the ray's own inclination, which no amount
  of shrinking the aperture touches.

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

## 2026-09-22 — models-of-the-hydrogen-atom: six historical atoms in one box, and the spectrum that decides between them

### Added

`docs/phets_revised/models-of-the-hydrogen-atom.html` — a remake of PhET
Interactive Simulations' *Models of the Hydrogen Atom* (build 1.0.9, CC-BY 4.0).
New code; no PhET code or assets. Both PhET screens, all six of its atomic
models, its Experiment-vs-Model switch, its white/monochromatic source, its
spectrometer, its electron-energy-level diagram, its three de Broglie
representations and its (n, l, m) quantum numbers, in six views: **the box**
(PhET's Spectra screen), **the levels** (its Energy Levels screen, drawn on
PhET's compressed ladder *and* on the true one side by side), **the standing
wave**, **the orbitals**, **the series** and **the rates**.

**What is exact** — everything about the atom itself, pinned in `selfTest` to
`build/models-of-the-hydrogen-atom/derive.py` (2196 assertions, 935 printed
reference lines):

- `E_n = −R_H hc/n²` and every transition wavelength from CODATA 2022
  (`scipy.constants`) with the electron–proton reduced mass; `r_n = n²a₀`;
  `v_n = αc/n`. The reduced mass is not decoration: it moves H-α by 0.36 nm,
  350 times the residual against NIST.
- The de Broglie closure `nλ_dB = 2πr_n` is an identity and holds to
  **5.178×10⁻¹²** here — which is exactly how consistent CODATA's separately
  rounded `a₀`, `α` and `m_e` are with each other (the same number as
  `a₀ − ℏ/(m_e αc)`), and is asserted as such rather than as "zero".
- The seam mismatch when ν wavelengths are wrapped round one turn has a closed
  form: matching both height and slope costs `√(sin²2πν + (1−cos2πν)²) =
  **2|sin πν|**`, zero only at the integers. Asserted against the two-term
  expression over 400 ν.
- The hydrogen wavefunctions are the analytic ones. The radial functions are
  built from exact polynomial coefficients and agree with the Laguerre
  recurrence to 1×10⁻¹⁴ and with `scipy.special.genlaguerre` to 4×10⁻¹⁷; the
  angular parts match `scipy.special.sph_harm_y`/`lpmv` to 2×10⁻¹⁶.
  Normalisation, ⟨r⟩, ⟨r²⟩, ⟨1/r⟩, the n−l−1 radial nodes and the l−|m| angular
  nodes are each asserted twice — once against the closed form and once against
  an independent Simpson quadrature.
- The drawn cloud is `∫|ψ|²dy`, the column density along the line of sight,
  pinned against `scipy.integrate.quad` to 1×10⁻¹⁴.
- The **Einstein A coefficients** come from the dipole radial integrals
  evaluated in closed form (both radial functions are a polynomial times
  `e^{−r/n}`, so the integrand is a polynomial times `e^{−sr}` and every term
  integrates exactly). They agree with scipy quad to 2×10⁻¹³:
  A(2p→1s) = 6.26832×10⁸ s⁻¹, τ(2p) = 1.5953 ns, τ(2s) = ∞.
- The stochastic parts run on a seeded mulberry32 whose stream is reproduced
  **bit for bit** in Python, and the cascade ensembles are asserted hop by hop
  against derive.py and against the distributions they are drawn from (|z| < 3).

**The finding worth recording:** PhET's transition-strength table
`[[12.53], [3.34, 0.87], [1.36, 0.24, 0.07], …]` — the weights its Schrödinger
atom picks a lower n with — has a first column that is **twice the Einstein A
coefficient for np → 1s in units of 10⁸ s⁻¹**, to between 0.05 % and 1.2 %
(12.5366, 3.3469, 1.3645, 0.6879, 0.3948). The other columns match no average
of the real rates and are PhET's own; both tables are drawn side by side in
*the rates* view and the difference is stated on the canvas.

**Measured data.** NIST, *Handbook of Basic Atomic Spectroscopic Data*, "Strong
Lines of Hydrogen (H I)" (`physics.nist.gov/PhysRefData/Handbook/Tables/
hydrogentable2.htm`, fetched 2026-09-21): all 8 vacuum rows and all 22 air rows,
used verbatim, with Edlén 1966 (*Metrologia* **2**, 71) for the vacuum→air
conversion. Every line is reproduced to better than 3×10⁻⁵, and the eight Lyman
lines miss by 1.10–1.33×10⁻⁵ — which is **α²/4 = 1.331×10⁻⁵**, the relativistic
shift of the 1s level. The residual is the physics the model does not contain,
measured, and it is drawn as such.

**What is PhET's model, not physics** (read out of the minified build and
labelled PhET's throughout): the 475-unit box, the 300 units/s photon, one
photon every 0.0792 s, the drawn orbit radii 15/44/81/124/174/233 (not n²), the
energy-diagram heights 0.025/0.6/0.73/0.81/0.86/0.9 (not 1 − 1/n²), the
`round(1240/(13.6(1/n₁²−1/n₂²)))` integer wavelengths, the 0.75 s and 1.0 s
waits, the flat 0.5 emission chance, the 150 nm plum-pudding line, the classical
spiral (220 units/s, ×1.008 a frame, dead in 0.659 s), the 0.4 white-light bias
toward the n = 1 lines, and the metastable (2,0,0) handler. PhET's probabilities
are per animation frame; this file fixes the frame at **1/60 s**, PhET's own
rate on a 60 Hz display, so a seeded run is reproducible — and says so.

`selfTest` 2196/0, UI drive 250/0; 125 mutants, 0 survivors after the fix
round; `tools/audit.py` clean at 1400x820, 820x520 and 560x380.

### Fixed (during the build)

- **`&ouml;` is not in `ENTS`, so `plain()` returned it unchanged and the canvas
  drew `Schr&ouml;dinger` verbatim.** Symptom: the model name in the box view
  came out as a literal entity in the display-list smoke test. Root cause: the
  shared entity table has no Latin-1 letters at all, and `plain()` passes an
  unknown named entity through unchanged by design. Fixed by writing the glyph
  (`Schrödinger`) in the model list and adding `&ouml;`, `&eacute;`, `&micro;`
  and `&thinsp;` to the table.
- **`h(tag, attrs, 'text')` makes a TEXT node, so an HTML entity in a control
  label is drawn literally.** Three buttons and one checkbox read
  `Lyman &alpha; 122`, `H&alpha; 656` and `the true n&sup2; radii` in the panel.
  Root cause: only the `html:` attribute decodes; a string child does not. Found
  because the UI drive could not find the buttons by their rendered label.
- **A node that lands exactly on a grid sample is lost by a strict
  sign-change test.** `R_20` vanishes at exactly r = 2 a₀, and 2 is a grid
  point, so `sign(prev)×sign(v) < 0` was false on both sides of it and the 2s
  orbital was drawn with zero radial nodes instead of one. The same shape had
  already bitten derive.py's angular-node counter, which missed every node at
  cos θ = 0 (P₁⁰ counted 0 nodes instead of 1) because the sample grid had an
  odd number of points. Both now track the last **non-zero** sign and treat an
  exact zero as a node in its own right; the angular scan samples at midpoints.
- **A fixed panel count in the column integral is 40× too coarse at n = 1.**
  `∫|ψ|²dy` varies on the scale of n a₀, so a panel count tuned at n = 6 left
  the 1s column 1×10⁻⁵ low. The step now follows n; `selfTest` asserts the
  accurate version against scipy quad **and** asserts the coarse one is still
  visibly wrong, so the fix cannot be quietly undone.
- **The caption's last line sat in the `#hint` corner.** `fitCaption` anchored
  the caption 12 px from the bottom, where the HTML `#hint` is drawn at
  `bottom:11px` — and the canvas capture cannot see the hint, so nothing
  reported it. Every view now reserves `HINT_H = 27` px and `selfTest` asserts
  the bottom-left 340×27 corner carries no canvas text, at five stage sizes.
- **A plot box with no room under it puts its own x-axis title on the
  caption.** The first narrow-stage layout clamped the lower panel's height with
  a `Math.max` floor, which pushed the axis labels past the frame. `stackFit()`
  now shrinks the upper panel until the lower one is guaranteed
  `AXIS_BOT = 38` px of clearance, and a stage narrower than 430 px of usable
  width stacks its panels instead of putting them side by side.
- **`legendAuto` places a legend OUTSIDE a panel it does not fit in.** On a
  110 px rates panel at 560×380 the legend was 110 px wide, no candidate corner
  was inside the frame, and it landed on the neighbouring axis's tick labels. A
  legend that does not fit is now not drawn.
- **`legendAuto` dodges curves, not labels** (already on the Known-bad list, hit
  again): the ⟨r⟩ label and the branching bars' value labels landed on legends.
  The ⟨r⟩ value moved into the legend itself; the bar labels now dodge
  `LEGEND_RECTS` and sit inside the bar when it reaches the frame.
- **A rotated axis title runs DOWN the screen.** The 150 px-long
  `(model − NIST)/NIST, ×10⁻⁵` on a 46 px-tall panel stuck out 50 px past the
  frame and onto the caption. It shortens to `×10⁻⁵` below 120 px of panel.
- **Tick labels crowd on a short axis, and a decade label crowds on a narrow
  one.** Five y ticks need 60 px of frame (`nyFor()`); the series view's decade
  labels are now thinned by measured width, which is what `5.0 µm` and `7.0 µm`
  needed at 820 px.
- A general fix for the above class: every label this file draws registers its
  rectangle, and `labelIfClear()` refuses to draw one that would land on an
  existing rectangle. Mandatory text (panel titles, axis titles, the caption,
  the wavelength marker) goes down first; optional text dodges it or is dropped.
  The true energy ladder really does crowd n = 4, 5 and 6 into the top 3 % of
  the axis, so it now labels what fits and prints *"N levels too close to
  label"* — which is the point the view is making.

### Fixed (from the mutation sweep — 125 mutants, 23 survivors in the first pass)

Every survivor is listed with what closed it. Three shapes recur: a pin that
recomputed the constant it was pinning (so it moved *with* the mutant), a rule
written out more than once (so either copy's mutant was equivalent), and a
repaint asserted against a forced draw rather than through the frame loop.

1. **PhET white-light bias** (0.4 → 0.7) — nothing measured what the source
   fires. Now: 20 000 photons drawn off `firePhoton` and the fraction on an
   n = 1 line asserted at 0.4044 ± 0.04, with an explicit "and not 70 %".
2. **Legendre P_m^m sign** — **equivalent, and now stated as such.** The
   Condon–Shortley phase (−1)^m cancels in `|Y|²`, which is the only thing this
   file ever asks `legendreP` for. `selfTest` asserts the invariance
   deliberately (|Y_l^m|² = |Y_l^{−m}|² to 1e-15 at four (l, m)) so it is a
   property rather than a blind spot, and the mutant is out of the sweep.
3. **selection rule Δl** (`!== 1` → `> 1`) — unreachable through every caller,
   because `decayRate` and `rateNtoN` only ever offer l ± 1, and for s → s the
   `l_max = max(l_u, l_l)` factor is zero anyway. Now asserted directly at
   l ≥ 1: A(3p→2p) = A(4d→3d) = 0.
4. **weighted choice normalisation** (`acc += w/tot` → `acc += w`) — every
   distribution the sim passes already sums to 1, so the division cancelled in
   every call. Now tested with 3:1 weights (0.75 ± 0.02), plus the empty and
   all-zero cases.
5. **PhET lower-n floor** — two guards on one path (`Math.max(l, 1)` followed by
   `if(l === 0) lo = 2`), so either mutant was equivalent. Written as one
   decision, `const lo = (l === 0) ? 2 : l`, and both of its mutants are caught.
6. **PhET choose_m thirds** — `phetChooseL`/`phetChooseM` were declarative only;
   `setNLM` (the live atom) and `cascadeSchrodinger` (the ensemble) each
   reimplemented the rule. Three copies of one rule, so the declarative one's
   mutant was invisible. Both callers now **draw from the distribution**, so
   there is one statement of it; derive.py was changed in the same commit and
   the bit-for-bit cascade pins moved with it. That alone did *not* close it,
   and the reason is worth recording: **m is causally inert in PhET's model.**
   `phetLowerDist` reads only (n, l), `phetChooseL` does not read m, and
   `phetChooseM` can only return m, m+1 or m−1 — so |Δm| is never 2 and the
   (1,0,0) fallback is never reached through m either. Nothing about which n
   the atom lands on, or which wavelength comes out, depends on it. The
   distribution is now asserted directly (each of the three outcomes at 1/3
   over 60 000 draws), and the inertness asserted deliberately, so it is a
   stated property rather than the reason a mutant lived.
7. **PhET state validity** (`l <= n-1` → `l <= n`) — the boundary was never
   probed. Now: `validState(2,2,0)`, `validState(2,1,2)` and `validState(7,0,0)`
   are each asserted false.
8, 9, 18. **photon radius, electron radius, the quantum collision radius** — the
   absorb counts moved but every assertion on them was a bound, not a value.
   Now the collision geometry is asserted directly: a Bohr photon collides at
   19.9 units and not at 20.1 (15 + 5, PhET's), a de Broglie one at 22.9 and not
   23.1 (15 + 8), and on the far side of the ring, which a point electron would
   not.
10, 11. **the absorb wait, the emit wait** — `ATOM.absorbed > 3` survived both.
    Now: a photon arriving 0.70 s after the last transition is refused and one
    at 0.80 s is absorbed; and nothing is emitted before the state is 1 s old.
12. **the plum-pudding line** (150 → 160) — the pin read `PHET.puddingLam`, so
    it moved with the mutant. Pinned against the literal `'150'`.
13, 14, 15. **the classical collapse rate, spin-up and start radius** — all
    three pins recomputed themselves from `PHET.*`. Pinned against PhET's
    literals (150, 220, 5, 600, ×1.008) and against the measured collapse time
    (150−5)/220 = 0.6591 s, plus a linearity check on r(t) at two times.
16. **the emission direction below n = 5** (`n < 5` → `n < 4`) — the isotropy
    test was run at n = 3, which is below either threshold. Moved to n = 4, and
    paired with an n = 5 check that the direction is *not* isotropic.
17. **the tick length** (1/60 → 1/30) — nothing observable depended on it. Now:
    a 300-unit/s photon moves exactly 300 units in 60 ticks, and crosses the
    475-unit box in 95 of them.
19. **the metastable light mode** — the old pin read `ATOM.metaT`, which the
    mutant reset anyway by exciting the atom. Now: under a monochromatic lamp
    **no** `meta` photon is ever created and a 2s atom stays at n = 2.
20. **the pointer never marks the canvas dirty** — `pointermove` sets the flag
    itself, so a down–move–up sequence could not test the `pointerdown`
    handler. Firing the pointerdown alone did not close it either: the
    `pointerup` that tidied up afterwards calls `refresh()`, which draws
    unconditionally, and that draw landed in the same capture. The capture now
    happens **after the pointerdown and before any pointerup**, on a box view
    whose clock has been stopped and proved idle.
21. **a slider stops repainting** — `refresh()` draws unconditionally, so the
    immediate draw said nothing about the dirty flag. The assertion now takes a
    second capture **through the frame loop** and a third proving it goes quiet.
22. **l is no longer clamped to n − 1** — clamped in the slider handler *and* in
    `syncPanel`. One clamp now, in `syncPanel`, which runs after every change;
    the `m` clamp joins it and both mutants are caught.
23. **the seed slider does not restart the run** — masked by the lazy
    `atomKey` check inside `atomAdvance`, which resets on the next frame anyway.
    Now asserted **immediately**: `ATOM.t === 0` the moment the slider fires,
    before any frame is pumped.

### Fixed (from looking at the PNGs — the audit is blind to all of it)

Three capture sizes (1400x820, 820x520, 560x380), 46 pictures, `tools/audit.py`
clean on all three. Everything below was found by looking, not by the audit,
which inspects text only.

- **The proton was drawn 12.5 px across and swallowed its own n = 1 orbit**
  (14.7 px at the default fit), so the ground state was invisible and n = 2 was
  crowded. 7 view units now.
- **The classical spiral's trail was a path the electron never took.** It was
  reconstructed forwards from r = 150 using TODAY'S angular speed for the whole
  history, which draws an arc, not a spiral. The forward step is invertible
  (r += 220 dt, a += w dt, w /= 1.008); stepping it backwards gives the true
  path, and it now visibly tightens as it falls in.
- **The small Schrodinger cloud was drawn at a fixed screen size whatever n
  was**, so it contradicted the orbit ladder drawn behind it — the one thing
  that ladder says is that the atom grows with n. Scaled so that <r> lands on
  PhET's drawn radius for that n.
- **The de Broglie wave on the standing-wave view was invisible.** Its
  amplitude was 0.45 of the n = 1 radius, which on the true n<sup>2</sup> ladder
  is 6 px on a 55 px ring, times a sin(phase) that a still frame can catch near
  zero. It is now 0.24 of the ring being drawn, the panel is fitted to that
  ring rather than to n = 6 (the house rule: fit each axis to the structure it
  contains, and print what runs off), and the full-amplitude shape is drawn
  faintly behind the live wave so the nodes stay visible while it breathes. The
  brightness picture gained node ticks for the same reason.
- **A legend entry for something that was not drawn.** The lifetime panel's
  orange "no allowed drop" entry named the 2s state, whose marker was under the
  legend box — because `legendAuto` dodges POLY_SEGS (curves) and nothing else.
  It now also dodges the label registry, the 2s state is drawn on its own rule
  at the top of the axis with a mandatory note, and the bars of both bar charts
  are registered so the legends stop landing on them.
- **The ensemble panel's y axis ran 0 to 1 for bars of 0.2**, and its mean-hops
  note was behind the first bar. Auto-ranged; the note moved to the top.
- **A `Math.max` floor on the box's side does not make it fit.** At 560x380 the
  floor of 120 px pushed the light source onto the spectrometer's title — and
  the light source is a FILL, so neither the audit nor the inline sweep could
  see it. Below 105 px of room the spectrometer is now dropped and the box
  keeps the space, which the caption says.
- The caption promised "faint green rings" in configurations that do not draw
  them; the model's 55-character claim ran three times the width of a 130 px
  box; "1 levels too close to label"; the short fallback captions were in ASCII
  while the long ones used the glyphs.

### Known-bad candidates

- **An HTML entity in a string passed as a `h()` CHILD is drawn literally** —
  only the `html:` attribute decodes. Canvas has no entity parser and neither
  does a DOM text node, so `btn('H&alpha; 656')` puts seven characters in the
  button. Write the glyph, or use `html:`. (Found here on three buttons and one
  checkbox; the UI harness caught it only because its finders match on the
  rendered label.)
- **`plain()`'s table has no Latin-1 letters**, so `&ouml;`, `&eacute;` and
  `&micro;` reach the canvas unchanged. Extended here; check the table before
  writing a new glyph on a canvas.
- **A node that lands exactly on a sample is invisible to a strict sign-change
  test** — `sign(a)·sign(b) < 0` is false when either is zero, so the node is
  skipped *and* the sign tracker is poisoned. R₂₀ vanishes at exactly r = 2 a₀,
  and P_l^m at exactly cos θ = 0 for every odd l − |m|. Track the last
  **non-zero** sign, treat an exact zero as a node, and sample an even grid (or
  at midpoints) so the symmetric zero is never hit.
- **The HTML `#hint` sits under the last line of a bottom-anchored caption and
  the canvas capture cannot see it.** Reserve ~27 px and assert the bottom-left
  340×27 corner is clear of canvas text. (Already recorded from
  `wave-on-a-string`; hit again here, and again the audit was silent.)
- **A `Math.max` floor on a bottom panel's height does not make it fit — it
  pushes its axis labels off the frame.** When a stack cannot fit, shrink the
  panel *above* it (`stackFit`), or drop the lower panel; never clamp.
- **`legendAuto` will place a legend outside a panel too small to hold it.** Add
  the `bw > b.w − 16 || bh > b.h − 16` guard; a legend that does not fit is not
  drawn.
- **A rotated axis title's LENGTH runs down the screen**, so a long one on a
  short panel overruns the frame vertically. Shorten it below a height
  threshold.
- **A pin that reads the constant it is pinning moves with the mutant.** Six of
  the 23 survivors here were this: `rel(tDead, (PHET.classicalR0 −
  PHET.classicalRmin)/PHET.classicalDrdt, …)` cannot fail. Pin against a
  literal, or against a measurement the constant controls.
- **A rule written out three times has two invisible copies.** PhET's
  `choose_l`/`choose_m` lived as a declarative distribution and twice inline;
  mutating the declarative copy changed nothing the sim drew. One statement,
  every caller draws from it.
- **`pointermove` sets the dirty flag by itself, so a down–move–up sequence
  cannot test the `pointerdown` handler's flag.** Test a pointerdown-only action
  (here, a click that toggles the lamp) against a proven-idle loop.
- **A slider repaint asserted on the immediate draw tests `refresh()`, not the
  dirty flag** — `refresh()` draws unconditionally. Take the second capture
  through the frame loop.
- **A lazy "has the key changed?" reset masks the explicit one.** Changing the
  seed restarts the atom twice over — once in the slider callback and once in
  `atomAdvance` — so the callback's mutant survived. Assert the immediate
  behaviour (state reset *before* any frame is pumped), not the eventual one.
- **A `pointerup` handler that calls `refresh()` masks the `pointerdown`
  handler's dirty flag** — `refresh()` draws unconditionally, so the draw it
  forces lands in the same capture. Capture between the down and the up.
- **`legendAuto` dodges curves only, and a scatter or a bar chart is not a
  curve.** Register a short segment per point and per bar edge in POLY_SEGS
  before placing the legend — and teach legendAuto to dodge the label registry
  as well, or it will sit on the very marker its own entry is naming.
- **A quantity that cannot change any observable is not testable through them.**
  PhET's magnetic quantum number m is drawn and printed but changes nothing
  about which level the atom lands on or which photon comes out, so its
  distribution has to be asserted directly. Assert the inertness too, so it is
  a stated property rather than a silent excuse for a survivor.
- **The audit's half-pixel overlap rule is the real one.** An inline sweep run
  at 3 px passed pictures the audit then failed; the two now use the same 0.5 px
  threshold, and so does the label registry that decides which labels to drop.

## 2026-09-22 — ph-scale-basics: PhET's Macro screen as its own sim, on ph-scale's engine

### Added
- `docs/phets_revised/ph-scale-basics.html` (157 KB), a clean-room remake of PhET's
  **pH Scale: Basics** 1.7.5 (CC-BY 4.0; new code, no PhET code or assets). PhET's Basics
  sim is the Macro screen of pH Scale on its own — pick one of twelve everyday liquids,
  pour it from the dropper, dip the meter, run the tap, open the drain — and it shows a pH
  and a volume and nothing else. Four views: **the beaker** (PhET's screen), **the
  liquids** (this file's own table of the twelve), **dilution** and **the scale**.
- **The same engine as `ph-scale.html`, taken by path and pinned by SHA-256.** The
  chemistry (`build/ph-scale/p2_chem.js`), the state, the clock and the readout
  (`p3_state.js`), three of the four views (`p4_views.js`) and the reference values
  derive.py printed (`p7_refs.js`) are the same files, never copied; `assemble.py` asserts
  each one's hash, so a change in either directory cannot reach this sim unnoticed. The
  head is generated from ph-scale's by `make_head.py` (only the title, the `h1` and the
  `.sub` differ, which is what the PLAYBOOK allows), and the UI harness by `make_ui.py`,
  which carries 440 of its 465 lines across and asserts every substitution matches exactly
  once. What is genuinely this build's own: the identity (`p2b_id.js` — four tabs, and
  `SHOW_CONC = false`), the liquids table (`p5b_views.js`), the boot and the suite.
- **The trim is PhET's own.** The particle picture, the concentration graph and My Solution
  are simply absent, which is the difference between PhET's two sims; and the beaker
  readout prints a pH, a volume and acidic/neutral/basic with no concentration, no moles
  and no molecule count, as PhET's Basics does. The scale view keeps the two
  concentrations, because they are what that view exists to explain.
- **The liquids table**, the one view ph-scale does not have: the twelve sorted by pH with
  a swatch of each liquid's own colour, PhET's pH, acidic/neutral/basic, the measured range
  and its source where one could be sourced, and the same pour — 0.1 L topped up to the
  beaker's 1.2 L — worked out both ways. They agree to a hundredth of a unit down the list
  and part company at chicken soup (6.73 exact against 6.65 by PhET's rule), which sits
  near the pH where the gap is largest. Twelvefold dilution is log10(12) = 1.079 pH and no
  more, which is the table's point.
- **The chemistry, exact, and the dilution law done properly** — the same as ph-scale's and
  asserted here again, because this file has to stand on its own: Kw = 1.000e-14 at 25 °C
  (pKw = 14.000 exactly), `[H3O+] = 10^-pH`, `[OH-] = Kw/[H3O+]` (not PhET's
  `10^-(14-pH)`, which is out by up to 2.1e-15 because pH − 14 is inexact in a double
  whenever pH < 7). Dilution mixes moles of the net strong acid
  `C = [H3O+] − [OH-] = −2√Kw·sinh(ln10(pH−7))` and re-solves `[H3O+] − Kw/[H3O+] = C`;
  diluting f-fold divides C by exactly f, C is odd about pH 7, and the textbook quadratic
  root is out by 11 % at pH 15, so the rationalised branch is load-bearing. PhET's own rule
  is a chip beside it; the two never differ by more than 0.0948 pH anywhere this beaker
  can reach, and averaging the pH is wrong by up to 4.42.
- **Measured pH ranges for four of the twelve**, with their sources named in the panel and
  the other eight drawn with no range rather than an invented one; PhET's value lies inside
  all four.
- Verification: `selfTest` **1594 passed, 0 failed** (osascript and jsc); UI drive
  **184 passed, 0 failed**; display-list capture at 1400×820, 1100×700 and 560×380 audited
  clean (0 layout problems, 51 PNGs) with every view looked at. `mutants.json` carries
  **101 mutants** (90 of ph-scale's, all of which apply to this build, plus 11 of its own);
  every one of the 101 was spot-checked individually with `spot_mutants.py` and caught. The
  definitive sweep is `sweep.sh`, run against a copy inside `_out/`.

### Fixed (during the build)
- **A reference value typed from the head, wrong in its fourth digit.** The suite asserted
  orange juice diluted twelvefold at `4.5828239616268092`; it is `4.579175035770364`. Root
  cause: the constant was written out rather than read off derive.py's output — exactly the
  Known-bad "a reference value you computed in your head is not a reference value". The
  assertion now pins what the sim PRINTS (`4.58`, which is what the prose claims), the
  agreement of the two independent implementations, and that the shift is log10(12).
- **Seventeen mutants alive inside a file that called itself verified.** The Basics suite
  started as a trim of ph-scale's, so it dropped the assertions on everything the shared
  engine carries but this build never draws: PhET's particle rule, the graph's exponent
  ranges, My Solution's volume range, the unknown-solute fallback, `phFromH3O`/`phFromOH`
  and `molesOf`. All seventeen constants are still in the bundle a reader downloads, so
  they are now asserted here too. Root cause: trimming the VIEWS is not a reason to trim
  the assertions — the code ships either way.
- **The liquids table's two right-hand columns were pinned by one liquid, and it was the
  wrong one.** Orange juice reads 4.58 under both laws, so a check on it passed with the
  PhET column replaced by the exact one, and with the dilution changed under the exact
  column alone. Both survived a spot check until chicken soup — the liquid at which the two
  laws part company, 6.73 against 6.65 — was pinned instead.
- **The table's sort was asserted by membership only**, so reversing it changed nothing any
  test could see. The rows are emitted in order, so their order in the display list is the
  sort, and that is now asserted.
- **`autofill()` could have filled the beaker with water** and the suite would not have
  noticed: the trimmed version kept "autofill puts 0.5 L back" and dropped "of the liquid
  alone".
- **"Picking another liquid redraws the table" passed on a table that had not changed.**
  Two faults at once: the view's only response to the chip was a text COLOUR, which the
  display-list recorder does not capture; and the assertion compared `sigU`, which is
  length-plus-count and is identical for two different rows of the same table. The selected
  row now gets a band (a real `fillRect`) and the comparison is on the geometry.
- **Three layout defects found only by the inline sweep.** The two right-hand headers
  ("0.1 L in 1.2 L" and "by PhET's rule") are 76 px each in an 84 px column at 1100×700 and
  collided — they are now "diluted 12x" and "PhET's rule" in wider columns. The table's
  title is 649 px and ran off a 560 px stage — there is a short form. And the table was
  capped at 26 px a row, which used a third of a 1400×820 picture and left the rest empty.
- **The narrow table painted its "measured range" column green.** Root cause: the colour
  rule was "the last two columns are the computed ones", which is true of the seven-column
  layout and false of the four-column one, where the measured column IS second from last.
  The columns are now coloured by named role.

### Known-bad candidates
- **Trimming a sim's VIEWS is not a reason to trim its ASSERTIONS.** A build that shares an
  engine still ships every constant in that engine, and a suite cut down to the views it
  draws left seventeen live mutants in a file reported as verified. Assert what the bundle
  contains, not what the bundle displays.
- **A table pinned by one row is pinned by the row you happened to choose.** Pick the row
  where the two quantities being compared actually differ; a row where they agree passes on
  a table that computes one of them twice.
- **A view whose only response to a control is a text COLOUR cannot be tested through the
  display list** — the recorder captures text content and position, not fill style. Give the
  selection a geometric mark as well, or no capture-based test can see it.
- **`sigU` (JSON length plus op count) is a weak signature**: two different rows of the same
  table produce the same length and the same count, so "the picture changed" passes when it
  did not. Compare the geometry.
- **A column-colour rule stated as "the last N columns" inverts when the layout narrows.**
  Colour by named role, not by position from the end.

## 2026-09-22 — buoyancy-basics: PhET's Explore and Compare screens on density.html's engine, with the upthrust taken from the pressure on the faces

### Added
- `docs/phets_revised/buoyancy-basics.html` (160 KB, 2821 lines), a clean-room
  remake of PhET Interactive Simulations' **Buoyancy: Basics** (build 1.2.11)
  and the companion of `density.html`. Five views: **the pool** (PhET's Explore
  screen), **the sets** (Compare), **the faces**, **the scale** and **float or
  sink**. No PhET code or assets.
- **One engine, two sims.** `p2_physics.js` is byte-identical to
  `build/density/p2_physics.js` apart from its banner, and both files are pinned
  against the same `build/density/derive.py` and the same `refvals.txt`. What
  this sim adds is what PhET's Buoyancy adds: six fluids instead of water alone
  (gasoline 680, oil 920, water 1000, seawater 1029, honey 1440, mercury 13593
  — PhET's values), a scale on the ground and a scale in the pool, and the three
  forces drawn as arrows.
- **The two scales, and what they mean together.** The ground scale reads
  `ρ_b g V`, the pool scale reads `W − ρ_f g V_sub`, and the difference between
  them is asserted to be exactly the weight of the fluid the block pushed aside
  (118.44 N against 132.30 N for PhET's aluminium block). The pool scale is
  PhET's own 0.15 × 0.06 × 0.2 m box, displacing 1.8 L of fluid itself, and its
  height runs PhET's 0 to 1 — at 0 it stands on the floor and at 1 its top is
  level with the ground, both pinned. Raised, it holds a floating block *above*
  its own waterline, so the block rests on it and the reading is real: that is
  asserted rather than treated as a bug.
- **The faces view derives the upthrust instead of asserting it.** The
  hydrostatic pressure is drawn to scale on all six faces, the four sides cancel
  in pairs to exactly zero, and `(p_bot − p_top) A = ρ_f g (y_t − y_b) A =
  ρ_f g V` is checked three ways — the face integral, the per-edge polygon
  closed form and a 2000-point perimeter sum — with the residual printed in the
  readout. The net force is asserted **unchanged** when the block is taken twice
  as deep, while the pressure on its bottom face doubles.
- **The scale view draws the whole descent.** 241 solved points: the reading
  falls in a straight line while the block enters, then goes exactly flat at
  `(ρ_b − ρ_f) g V` once the top face is under — every one of the fully
  submerged points pinned to 49.000 N for a 5 L brick — and reaches zero with
  the string slack for anything that floats. The entering leg carries the real
  tilt, because the fluid rises to meet the block as it goes in.
- **Float or sink** is all 27 materials against all 6 fluids at once, ordered by
  density, with every cell's fraction checked against `min(1, ρ_b/ρ_f)` computed
  a second way. 23 of the 27 float in mercury (all but mercury itself, tantalum
  and gold and platinum); only styrofoam and wood float in gasoline.
- Provenance as in `density.html`: PhET's value beside the handbook value from
  Wikipedia's "Densities of various materials" (fetched 2026-09-21), with "no
  row" said for the six materials that table does not carry; gravity PhET's 9.8;
  PhET's "vacuum assumption" (air buoyancy ignored) stated, and the 0.06 % it
  costs a 5 L block quoted in the readout.
- Verification: `selfTest` **708 passed, 0 failed**; UI drive
  (`ui_drive_buoyancy-basics.js`) **189 passed, 0 failed**; mutation sweep
  **76 caught, 0 survived, 0 skipped** over 66 physics and 10 UI mutants;
  `audit.py` clean at 1400×820 and 820×520; 28 + 5 PNGs rasterised and looked at.

### Fixed (during the build)
- **The same registry gaps as `density.html`**, since the file carries the same
  helpers: block tags and scale readings drawn with a raw `fillText` were
  invisible to `lab()`'s dodging, `axes()` draws its tick labels, axis names and
  title outside any registry, the caption band was not reserved, and the
  right-column panels were painted after the stage. Fixed the same way —
  `labFixed()`, `axesReg()`, the caption rectangle pushed in `layout()`, panels
  drawn first, and each block's own rectangle registered.
- **The "ground scale" label collided with the block standing on it.** The name
  was placed above the platform, which is exactly where a block on the pan goes.
  It now moves under the scale when the scale is occupied.
- **Two axis ticks that will not fit.** "1000" and "1440" collided on the
  fluid-density strip at 900×600 and below; the strip now drops to two ticks
  under 300 px of panel.
- **Twenty-seven row names in 250 px.** The float-or-sink grid stacked its
  labels at 620×420. They are now thinned by *measured* spacing with the picked
  row drawn first so it is never the one dropped, and the canvas prints how many
  of the 27 are named.
- **Labels dodged into the block they were describing.** "fully submerged" and
  "the bottom is pressed hardest" were placed just outside the block's faces,
  which is where the pressure arrows are, so `lab()` moved them inside it. They
  are now placed beyond the arrow tips.
- **An axis fixed at 60 cm for a block 8 cm down.** The pressure-against-depth
  panel had a floor of 0.6 m whatever the block's depth, so at shallow settings
  both markers clustered in the top centimetre of the plot. It now fits the
  depth the block is at.
- **A caption that was wrong about its own picture, and a fix that silently
  did not apply.** "everything on the list floats in mercury except tantalum
  and platinum" — gold (19320) does not float in it either, nor does mercury
  itself. The first correction was written as a Python string replace whose
  pattern did not match the file (the source carries the literal glyph rho,
  not a \u escape) and it was not asserted, so it reported success and changed
  nothing; the PNG pass caught that the old text was still on the canvas.
  Corrected, and the claim is now pinned: the test computes which materials do
  not float in mercury and asserts the caption names each of them and none of
  the ones that do.
- **A 99.9 % cell printed as "100%"**, which reads as fully submerged in a grid
  whose whole point is the difference between floating and not. Cells above
  99.5 % now carry a decimal.
- **A caption naming a panel the view does not draw.** The sets caption
  described "the bars beside the pool"; the panel beside the pool is the
  mass–volume plane.
- **A marker silently clamped to the axis floor.** Wood's 400 kg/m³ line on the
  fluid-density strip was drawn hard against the left edge, where it reads as
  the axis. The floor is now 300 and a marker that still clamps says "(off the
  axis)".
- **Two test-side errors of my own.** Two assertions read `b.m` off
  `compareBlocks()`, which returns volume and density and no mass, so both
  compared "—,—"; and the mercury assertion in the scale view pinned the
  *held* block's submerged fraction (1, because it is being held on the floor)
  where it meant the free-floating one (0.1986).
- **A mutation sweep that could not see what only the UI exercises.** The
  mass/volume coupling, the two scales and the lowering curve were all reached
  only through the panel, so physics-only mutants on them survived. Each got its
  own `selfTest` coverage off the model — including the pool scale's support,
  which a mutant had quietly moved back to the pool floor.
- **An equivalent mutant, explained rather than patched.** "the ground scale
  reads `A.W − A.F_b`" cannot change anything, because a block on the ground
  scale is out of the pool and its buoyancy is exactly zero; it was replaced by
  a mutant that is not equivalent (reading the contact force instead).

### Known-bad candidates
- **A scale raised above a floating block's waterline makes the block REST on
  it, and the reading is not zero.** It looks like a bug (wood "pressing" on a
  scale) and is the physics: the scale holds the block higher than it would
  float, so it is only partly submerged and the scale takes `W − F_b`. Assert
  it, do not silence it.
- **A mutation sweep that runs only `selfTest` is blind to everything only the
  UI reaches.** Mass/volume coupling, a scale's support, a lowering curve — if
  the model's own tests never call them, physics mutants on them survive while
  the UI drive would have caught them. Either mark such mutants `u`, or (better)
  give the model its own assertions, because a model quantity that only the
  panel exercises is in the wrong layer.
- **A cell that rounds to 100 % in a table about floating.** 99.9 % under and
  fully submerged are the two states the table exists to distinguish; a
  zero-decimal formatter erases the distinction exactly where it matters.
- **A caption that counts.** "everything except tantalum and platinum" was
  wrong by two entries, and no assertion could see it because it was prose.
  Any caption that states a count should have that count asserted — the fix
  here was to make the test name the exceptions, not just the number.
- **A scripted edit that does not match reports success and changes nothing.**
  A `str.replace()` with no `assert s.count(old)==1` beside it is a silent
  no-op when the pattern is wrong — here the patch was written with `\u03c1`
  where the file carries the glyph rho — and the build then goes on believing
  the fix landed. Every scripted patch in these two builds asserts its pattern
  matched exactly once; the one that did not was the one that failed, and only
  the PNG pass caught it, because prose is invisible to every other check.
- **A marker clamped to an axis edge reads as the axis.** If a reference line
  can fall outside the range, either widen the range or say on the canvas that
  it has been clamped.

## 2026-09-22 — density: PhET's Intro, Compare and Mystery screens, with Archimedes' principle solved rather than approximated

### Added
- `docs/phets_revised/density.html` (169 KB, 2942 lines), a clean-room remake of
  PhET Interactive Simulations' **Density** (build 1.2.10). Five views: **the
  pool** (PhET's Intro screen), **the sets** (Compare), **the mystery**
  (Mystery), **mass and volume** and **the waterline**. No PhET code or assets;
  the house scaffold, 2-D layer and world helpers are extracted from
  `build_lagr/p1_head.html`, `build_lagr/p1_utils.js` and
  `build_buoy/p4_views.js` by `make_head.py`, and `fluidRect()`/`forceArrow()`
  come from the house's own `buoyancy.html`, which wrote them for this job.
- **Archimedes exactly, not approximately.** The free surface solves
  `G(y) = A_pool (y + H) − (every solid below y) = V_fluid` by bisection on a
  function proved non-decreasing (swept over 4001 levels), and the level taken
  is the **smallest** root, so a body spanning the pool's cross-section puts
  the surplus fluid above itself instead of inside itself. A floating cube's
  draft is `d = s ρ_b/ρ_f` and its submerged fraction `ρ_b/ρ_f` exactly, pinned
  against `scipy.brentq` on the force balance at 1.4e-17. A floating body
  raises the level by its own **mass**/(ρ_f A) and a sunk one by its own
  **volume**/A — two different laws, both asserted off the solver as well as
  from the closed form.
- **The upthrust computed twice.** The hydrostatic pressure integrated over the
  cube's six faces (bottom minus top, sides cancelling to exactly zero, one
  side face pinned to 59.0782 N from a 4000-strip integral) and round the
  polygon cross-section edge by edge with the linear-load closed form; the two
  agree with `ρ_f g V_sub` to 3e-16 relative, and the per-edge form agrees with
  a 2000-point perimeter sum to 1e-6.
- **The three awkward cases asserted, not assumed.** A block denser than the
  fluid (rests, `N = (ρ_b − ρ_f) g V`, submerged fraction exactly 1); one
  exactly at neutral buoyancy (fraction exactly 1, N = 0, a spring scale reads
  zero, and the hand force is unchanged at two different depths, so no depth is
  preferred); and one **wider than the pool's free surface** — a 216 L cube
  whose 0.36 m² footprint equals the pool's — where the fluid stands entirely
  above it at `−H + s + V_f/A`, and its floating counterpart rides on all of
  the fluid at `−H + V_f/A`.
- **PhET's measured data, with provenance.** Every material density is read out
  of PhET's own build and marked as PhET's; beside it is the handbook value
  from Wikipedia's "Densities of various materials" (fetched 2026-09-21), with
  **"no row"** said plainly for the six materials that table does not carry
  (brick, pyrite, apple, human, gasoline, honey). The four numbers that are
  teaching choices rather than measurements are named on screen: styrofoam 150
  against 75, concrete 3150 against 2400, PVC 1440 against 1175, and glass,
  which is simply aluminium's 2700 reused. Gravity is PhET's 9.8, not 9.80665,
  and the file says so.
- **The Mystery screen's claim is checked.** That the printed numbers identify
  the material is asserted rather than assumed: all fifteen blocks of PhET's
  three fixed sets are named correctly from mass and displaced volume rounded
  to the two decimals the sim shows, with a worst reading error of 0.17 % and a
  smallest gap to the runner-up of 3.30 %; and all 130 material × whole-litre
  combinations of the shuffled set, plus 1000 blocks over 200 seeds, come out
  right. PhET's set 2 A is built at 11340 where its own table says lead is
  11342 — a 0.018 % mismatch that is pinned rather than smoothed over.
- **The floating trap, made a control.** A floating block displaces its own
  *weight*, not its own volume, so left alone every floater measures as water
  whatever it is made of. "Hold them under" switches between the two, and the
  wrong answer is drawn (the floaters pile onto the water line on the density
  axis) rather than described.
- Verification: `selfTest` **872 passed, 0 failed**; UI drive
  (`ui_drive_density.js`) **179 passed, 0 failed**; mutation sweep **72 caught,
  0 survived, 0 skipped** over 63 physics and 9 UI mutants; `audit.py` clean at
  1400×820 and 820×520; 28 + 5 PNGs rasterised and looked at.
  `derive.py` (scipy) is the Python twin and `refvals.txt` its printed output.

### Fixed (during the build)
- **A block tag drawn with a raw `fillText` is invisible to the label
  registry.** The waterline caption ("water 102.0 L") landed on block A's "A" at
  900×600 and below. Root cause: `lab()` dodges only what is in `LABELS`, and
  the tags were painted straight to the canvas. Added `labFixed()`, which paints
  unconditionally *and* registers, and put every must-draw label through it.
- **`axes()` draws its tick labels, axis names and title outside any
  registry**, so dodging labels landed on them — "0.0" on "gasoline" in the
  waterline view, "400" on a note in the mystery view. The house `axesR`
  registers only the title; added `axesReg()`, which registers the tick labels,
  both axis names and the title.
- **The caption is painted last but occupies its band from the moment the
  layout is known.** At 620×420 a force label ("hand 29.4 N") was dodged down
  onto the prose. `layout()` now pushes the caption rectangle into `LABELS`
  before it returns.
- **Panels drawn after the stage cannot be dodged.** The right-column plots were
  painted after the pool, so stage labels had no way to avoid their axes. The
  three pool views now draw the right column first.
- **A wide stage drawing an equal-aspect square picture wastes two thirds of
  its width.** The pool was rendering about 350 px across in a 1244 px stage,
  and 0.30 m of empty sky above the pool took another 38 % of the height. Root
  cause: a pool is a *shape*, so its two axes must share a scale (the house
  rule), and a one-box layout then fits it by the smaller dimension. Added
  `splitMain()` — pool on the left, analysis panels down the right — and cut
  the world's top to `POOL_YTOP = 0.22`, with the drag clamped by
  `holdCeiling(s)` so a lifted block's top stays inside it.
- **Force arrows and their labels were painted over the block they belong to.**
  Arrows now run from the block's centre to its edges with labels beside it, and
  the block's own rectangle is registered, because with two blocks 26 px apart
  there is no room for a label between them.
- **A drawing scale computed at the call site cannot be pinned.** A mutant that
  handed each block its own weight as the arrow reference survived the sweep:
  `selfTest` was asserting `forceLengths()` while the draw call passed its own
  `Fref`. Root cause: the quantity was in the wrong layer. `forceScale()` now
  returns `{len, Fref}` together and the sweep catches every mutation of either.
- **A clamp enforcing a property the solve already guarantees is dead code.**
  `N = Math.max(0, W − F_b)` was unreachable: a block only ever rests when the
  upthrust cannot lift it, so `W − F_b ≥ 0` there by construction. Mutation
  testing correctly reported it as an equivalent mutant. The clamp is deleted
  and the property is swept instead — 84 configurations, minimum N exactly 0.
- **`cubeBelow` saturated at `s³`, not at `V`.** `s = V^(1/3)` is inexact in
  binary, so a fully submerged block reported a submerged fraction of
  1.0000000000000004. It now returns `V` exactly, and a test asserts that
  `s*s*s !== V`, which is why it has to.
- **A continuity assertion that asserted the wrong thing.** "G is continuous
  across the float/rest switch" was written as `ΔG = 2εA` and failed on correct
  code: G is continuous but its *slope* jumps there, from `A − s²` below to `A`
  above. Replaced by the true statements — the displaced volume is continuous
  (the gap across ±ε is exactly `s²ε`, and grows 100× when the probe does), and
  the two one-sided slopes are each pinned.
- **The mystery screen's scale was drawn buried.** Its platform was placed from
  −SCALE_H to 0, i.e. below ground level, so the block being weighed appeared to
  stand on the earth. The platform now stands *on* the ground with the block on
  its pan.
- **A horizontal log axis in a tall, narrow column.** The mystery density table
  was drawn across the bottom; after the layout change its column is 400 px wide
  and 600 tall, so the axis is now vertical, with the table's thirteen materials
  naming its left and the five readings pointing at its right.
- **Four anonymous dashed rays.** The mass–volume plane drew a handbook ray for
  every Intro material, unlabelled, so wood's 700 sat above wood's 400 with no
  way to tell which was which. Only the picked material now gets its handbook
  ray, labelled, and a material with no handbook row says so on the canvas.
- **Twenty-five labels stacked on a fifth of an axis.** In mercury every
  material's density ratio is below 0.4, so the waterline view's names piled up.
  Labels are now thinned by measured spacing, every material is still a dot, and
  the canvas prints how many of how many are named.
- **The draft panel drew a fraction it was not printing.** A resting block was
  placed on the tank floor at `−0.95 s`, which is shallower than the block is
  tall, so its top stood *above* the surface: the panel showed a neutrally
  buoyant block half out of the water under a readout saying 100 % under, and
  the dimension line measured that false draft ("15.62 cm of 17.10 cm"). Root
  cause: the tank depth had been chosen for a floating block and never checked
  against a resting one; the same constant then cut the top off a barely-wetted
  floater (styrofoam in gasoline floats with 78 % of its side in the air, against
  0.55 s of sky). The geometry is lifted out of the draw call into
  `draftGeom(M, h)` and asserted both ways — the drawn draft equals the model's
  submerged fraction over six material/fluid cases at three panel heights, and
  the old 0.95 s tank is re-run and shown to still get it wrong by 0.41.
- **A caption that named a panel the view no longer draws.** The sets caption
  still said "the panel below" after the plot moved to the right.
- **Prose claims that no assertion could see.** The mass-volume caption and its
  info paragraph state a count ("six materials have no handbook row") and name
  four of PhET's teaching choices; nothing checked that the prose and the data
  agreed. `selfTest` now pins the count against the table and asserts the
  paragraph names styrofoam, concrete, PVC and glass.
- **Two chip rows with the same seven labels.** The UI harness found the block-A
  material chip by label and arity and drove **block B**, because a label-only
  walk takes the last match. Chip rows are now addressed by group and row index.
- **A test that re-derived what it was testing.** The UI drive checked the
  lifted-block clamp against `holdCeiling()`, the same function the sim uses, so
  a mutant on it was invisible; pinned against an absolute 0.037 m instead.

### Known-bad candidates
- **A label painted with a raw `fillText` is invisible to the dodging
  registry, and so is everything `axes()` draws.** `lab()` avoids only what is
  in `LABELS`; `axesR` registers the plot title and nothing else. Tick labels,
  axis names, block tags, scale readings and the caption band all have to be
  registered explicitly, and the must-draw ones have to be registered *first* —
  which also means panels must be drawn before the stage whose labels should
  dodge them. Four separate collisions in one build came from this one gap.
- **A wide stage drawing an equal-aspect picture wastes most of its width, and
  empty sky above the subject wastes the rest.** A pool must be drawn at equal
  aspect because it is a shape, so a single full-width box fits it by height and
  leaves two thirds of the width empty. Split the stage (subject left, analysis
  panels right) and cut the world to what is actually drawn — then clamp any
  drag so the subject cannot leave the world it was cut to.
- **A tank sized for a floating body is too shallow for a resting one.** A block
  placed on the floor of a tank less than one block deep pokes out of the
  surface, and every quantity read off that drawing — the draft dimension, the
  submerged wash — then contradicts the readout beside it. The same constant is
  wrong at the other end for a body that barely dips in (78 % of a styrofoam
  cube is above the surface in gasoline). Size the drawn tank from the block,
  and assert that the DRAWN fraction equals the model's over both regimes.
- **A drawing scale computed at the call site cannot be mutation-tested.** If a
  view computes its own reference value and passes it to a helper, a mutant on
  the call site changes only pixels and survives. Return the scale and its
  reference together from one function, and assert the lengths off that.
- **A clamp that enforces what the solve already guarantees is dead code, and
  the sweep will say so.** `max(0, W − F_b)` on a contact force is unreachable
  because a block only rests when the upthrust cannot lift it. Delete it and
  sweep the property instead; a surviving mutant on a guard is usually telling
  you the guard is unreachable, not that the test is weak.
- **Saturating a submerged volume at `s³` instead of `V`.** `s = V^(1/3)` is
  inexact, so "fully submerged" prints 1.0000000000000004 and every `=== 1`
  assertion has to be loosened. Saturate at the quantity you were given.
- **"Continuous" and "smooth" are different claims.** The displaced volume is
  continuous across the float/rest switch; the free-surface function's slope is
  not (it jumps from `A − s²` to `A`). Asserting the second as though it were
  the first fails on correct code.
- **A UI harness that finds a chip by label and arity still finds the wrong
  one** when two groups carry the same list. Address chip rows by group and row
  index, not by what is written on them.

## 2026-09-21 — projectile-data-lab: PhET's Projectile Data Lab remade, with the landing distance's distribution derived rather than sampled

### Added
- `docs/phets_revised/projectile-data-lab.html` (197 KB, single file, no network,
  works from `file://`). Six views: **the field** (PhET's Variability screen —
  six mystery launchers, six independent fields, single and continuous fire, the
  landing histogram on the field's own x axis), **the sources** (PhET's Sources
  screen — the custom launcher's mechanism and angle stabiliser, the three
  projectiles, the four orientations, with the two input Gaussians drawn beside
  the output), **the measures** (PhET's Measures screen — the mean, the n − 1
  standard deviation, the values, and the interval tool, draggable on the
  canvas), **the sampling** (PhET's Sampling screen — samples of n = 2, 5, 15, 40,
  one mean each, and the four thumbnails on one axis), **the exact law** and
  **the limit theorem** (house additions).
- **What is exact.** PhET's two closed forms for the range and the flight time,
  re-derived in `build/projectile-data-lab/derive.py` and checked against the
  root of y(t) = 0 by brentq (1e-16) and against a marched trajectory (1e-11,
  the accumulated rounding of 4×10⁵ additions); the maximum-range angle from a
  height, cos2θ* = gh/(v²+gh), against a numerical argmax. The random stream is
  mulberry32 + Box-Muller with one pair of uniforms per value, bit-identical to
  derive.py, so the page and the Python twin generate the SAME 500 landing
  distances and the page's mean, median, standard deviations (both conventions),
  standard error and every histogram bin count at every bin width are pinned
  against numpy's on that sample.
- **The distribution, computed rather than sampled.** PhET's mechanism is two
  independent Gaussians — a launch speed and a launch angle — re-drawn while the
  angle falls outside (0°, 90°) and while the speed is ≤ 0, so both are truncated
  normals. The moments come from a 96×96 Gauss-Legendre product rule over the
  truncated z-ranges, the same rule in the page and in derive.py, checked there
  against scipy's adaptive quadrature (1e-15), against an 8×10⁶-draw Monte Carlo
  of the actual re-draw mechanism, and against the closed form of the untruncated
  model. The density f(r) = ∫f_θ(θ)f_v(v*(r,θ))/|∂x/∂v| dθ integrates to 1 and to
  the exact mean to 1e-9 and matches the Monte-Carlo histogram at worst |z| = 2.25
  over 24 bins.
- **The results the file exists for.** (i) The exact mean is
  (1 + σ_v²/μ_v²)·e^(−2σ_θ²) times the no-jitter value v²sin2θ/g, exactly, at all
  18 launcher × angle settings: the speed spread LENGTHENS the mean range and the
  angle spread SHORTENS it, and neither wins everywhere — twelve of the eighteen
  land short and six (launchers 3 and 5, whose speed spread beats their angle
  spread) land long. (ii) PhET's own delta-method standard deviation, which sets
  its Sampling thumbnails' x-range, is below the exact σ in four of the five flat
  cases, by 0.68 % at worst, and ABOVE it at 45° by 5×10⁻⁶, where cos2θ = 0 kills
  the angle term. (iii) A launcher at 30° and the same launcher at 60° have
  exactly the same distribution of landing distance — sin2θ is symmetric about
  45° and so is the 0–90° truncation — while their flight times differ by 73 %.
  (iv) The truncation of the two Gaussians is worth 5.5×10⁻⁸ m on the mean at
  worst, measured, not assumed. (v) The central limit theorem is asserted, not
  illustrated: over 4000 samples the measured standard error matches σ/√n at
  n = 2, 5, 15 and 40, each inside its own sampling spread σ_n√((κ_n+2)/4M).
- Verification: `selfTest` 479 assertions green under `osascript`
  (8 s); UI drive `ui_drive_projectile-data-lab.js` 182 green (drag the interval
  tool's two edges and its middle, every chip row found by its `data-key`, every
  slider at min/max/mid on every tab, the keyboard, the resize); layout audit 0
  problems at 1400×820 and at 560×380; mutation sweep 95 caught of 97 with the
  two survivors proven equivalent (below).

### Fixed (during the build)
- **A tolerance of zero on a cross-language float is luck, not a pin.** The first
  suite asserted the Box-Muller values and the 500 landing distances against
  Python at tolerance 0, and they passed — but only `mulberry32.next()` is
  integer arithmetic all the way and therefore provably bit-identical; everything
  downstream goes through `log`, `cos` and `sqrt`, where JavaScriptCore's libm
  and CPython's may differ in the last bit. The min and max of the 500 duly
  differed by 1 ulp. `next()` keeps its zero; the rest are pinned at 1e-15, which
  is four ulp, with the reason written beside them.
- **Assembling μ₃ from the raw moments cancels five to seven digits, and the two
  languages round the cancellation differently.** m₃ ≈ 2×10⁵ against μ₃ ≈ 0.02
  for launcher 5 at 45°: the JS and Python answers differed by 3×10⁻⁸ relative
  while both were "correct". Both now take two passes — the mean, then the
  central moments about it — and agree to 1e-15. `selfTest` keeps the raw-moment
  form alive purely to measure the cancellation, so the shortcut cannot come back.
- **PhET's range formula loses digits for a downward launch from a height.**
  `v sinθ + √(v²sin²θ + 2gh)` adds two nearly equal numbers of opposite sign when
  sinθ < 0: at 10⁹ m/s from 12 m it is 3.9 % out, where the conjugate form
  2gh/(√(v²sin²θ+2gh) − v sinθ) is at 7×10⁻¹⁶. Nothing the sliders reach goes
  near it (the two agree to 1e-13 over the whole slider space, asserted), so
  PhET's form is kept — it is the one derive.py evaluates and the bit-level pins
  need — and the conjugate form sits beside it as the second implementation.
- **v*(r, θ) has no solution above h/tan|θ| for a downward launch, and Newton
  divides by a vanishing derivative trying to find one.** From a height the range
  of a downward launch saturates as the path straightens; the first density run
  crashed on exactly that. It now returns null past the ceiling, which is
  asserted from both sides (v* exists 2 % below it and refuses 2 % above).
- **"Angle jitter shortens the mean range" was false for two launchers.** The
  first suite asserted it at all 18 settings and failed at six. The true statement
  factorises — the speed spread lengthens, the angle spread shortens — and is now
  asserted as the exact identity plus the count of each sign.
- **"PhET's delta method is below the exact σ" was false at 45°.** Four of five,
  not five of five; at 45° cos2θ = 0 leaves only the speed term and the estimate
  is high by 5×10⁻⁶. The measured statement replaced the tidy one.
- **A histogram bin averages the density, it does not sample it at the midpoint.**
  Comparing the exact density against an 8×10⁶-draw Monte-Carlo histogram at the
  bin midpoints gave a worst |z| of 3.5, because the midpoint rule is 2.6×10⁻³ of
  f while the noise is only 1.1×10⁻³ — the test was measuring the midpoint rule.
  Averaging f over each bin brings it to 2.25.
- **`axes()` draws its tick labels with a bare `fillText`, so nothing placed
  afterwards can dodge them.** The measures overlay's "s = … (n−1)" landed on a
  y-tick at 560×380, and a "values" label on a ground marker at 1400×820. `axesT`
  now registers every tick label and the x-axis title in the label registry, the
  field's ground markers register theirs, and the six-field strip reserves its box
  BEFORE the field draws over it.
- **A stage laid out top-down pushes its bottom panel's tick labels into the
  caption.** The first `labStage` gave the histogram a fixed fraction and let the
  remainder fall where it might; at 560×380 the x-axis title landed two pixels
  into the caption. It now lays out from the bottom up — the axis labels first,
  then the histogram, then whatever is left for the field — and a narrow stage
  drops a four-panel bottom row rather than drawing four 24-px boxes.
- **The field strip was two thirds empty sky.** A 30° trajectory tops out at 10 m
  over a 100 m field, so at true aspect it needs a tenth of the width; giving it
  half the stage wasted the picture. The view now says how tall it wants to be
  and the histogram takes the rest, and the aspect ratio is printed on the canvas
  either way.
- **"Blocks" drew as one solid bar.** PhET's block representation is one cell per
  projectile; a fixed 1.2 px gap between 40 px cells is invisible, so the block
  and bar representations were the same picture under different names. The gap is
  now a fraction of the cell.
- **The n = 40 sampling histogram was drawn in the reference orange** — the same
  colour as the σ/√n curve it was being compared against. The four sample sizes
  have their own colour slots now, none of them a role colour.
- **Two panels showing "the exact mean" and "the no-jitter mean" as absolute bars
  said nothing**: the two differ by 0.05 % to 1.5 % and the bars were
  indistinguishable. They are signed percentage differences now, with the value
  printed on each bar and a visible stub where the difference is too small to see
  — a bar that is not drawn reads as a missing datum.
- **The interval tool's drag was 5.4 m out.** `x * metresPerPixel` instead of
  `(x − box.x) * metresPerPixel`: the histogram box starts 54 px in. Caught by
  the UI drive, which asserts the dragged edge lands where the pointer is.
- **A sample of 40 took a minute and a half.** The first state machine fired one
  projectile and waited for it to land; PhET's `SamplingField.totalSampleTime`
  spreads the n launches evenly over 0.75, 2, 5 or 9 s and lets the flights
  overlap. Now it does the same, and `selfTest` asserts both the table and the
  behaviour (half the launches away half way through).
- **A field's own capacity broke a test, not the code.** A 20000-draw tolerance
  was written against `fieldBatch`, which stops at PhET's 500 projectiles. The
  sampler is now drawn from directly, and the 500 is asserted as PhET's ceiling.
- **A view was drawing its picture from a control it does not show.** The
  exact-law view took its bin width from the histogram chip row, which only the
  three PhET screens display; at the raised launcher (σ = 0.40 m) the last
  setting of 1 m put the whole density in three bars. Its bins now follow the
  distribution (σ/4, rounded to a 1-2-5 step), and the caption and readout say so.
- **Two comparison panels drew an empty axis with a legend over it.** The raised
  orientation has neither v²sin2θ/g nor a delta-method σ — both are derived for
  a launch from the ground — so the panels had nothing to plot and said nothing.
  They now carry the sentence explaining why, the caption stops claiming a
  comparison the picture does not make, and `selfTest` asserts both halves (the
  sentence appears from 12 m and does not appear from the ground).
- **A relative tolerance on a derivative that is exactly zero asserts the
  roundoff floor, not the derivative.** PhET's delta-method angle coefficient
  2v²cos2θ/g is checked against a central difference of the range itself; at 45°
  the true value is 0 and the difference quotient returns 2×10⁻⁸, which is
  eps·x/(2h) and nothing else. The tolerance is now max(relative, that floor),
  so the assertion still bites where the derivative is finite and says what it
  can where it is not.
- Mutation sweep findings (95 caught of 97): five mutants survived the first
  sweep and each was a real gap — PhET's 0.7 s minimum between launches (nothing
  in the physics suite touched it), the projectile speed multiplier inside the
  SAMPLER as opposed to the quadrature, PhET's angle re-draw window (a 10-sigma
  guard that cannot be reached by waiting: it is now pinned with a deterministic
  stub stream that puts a draw at exactly 85°, 90° and −0.5°), and the total-bins
  width 100/n. Two survivors remain and are proven equivalent, not merely
  argued: the Gauss-Legendre Newton seed 0.75 → 0.50 converges to bit-identical
  nodes (asserted, along with the fact that 0.25 does not, so the seed is not
  free), and the median's sort direction cannot change a value read from
  symmetric positions (asserted both parities).

### Known-bad candidates
- **A zero tolerance against another language's floats is a coin toss.** Only
  integer arithmetic crosses languages bit-exactly. Anything through `log`, `cos`,
  `exp` or `sqrt` can differ by an ulp between JavaScriptCore and CPython, and a
  pin at 0 that passes today is luck: it passed on 6 Box-Muller values and 500
  landing distances, and failed on the min and max of the same 500.
- **A central moment assembled from raw moments is a cancellation, and the two
  languages round it differently.** μ₃ from m₃ − 3m₁m₂ + 2m₁³ lost seven digits
  where μ₃ ≈ σ³/40. Two passes — the mean, then the central sums — cost one extra
  loop and agree to 1e-15. Keep the one-pass form alive in the test purely to
  measure what it loses.
- **`v sinθ + √(v²sin²θ + 2gh)` is a cancellation for a downward launch.** The
  conjugate form 2gh/(√(…) − v sinθ) is a quotient of positives and cannot lose a
  digit. Where a published formula must be kept for parity, keep it and assert the
  stable form beside it over the whole reachable domain.
- **A histogram bin AVERAGES a density; comparing it against f at the midpoint
  measures the midpoint rule.** At 24 bins over ±3σ the midpoint bias was 2.4×
  the Monte-Carlo noise, so a correct density looked 3.5σ wrong.
- **`axes()` (the shared house helper) draws tick labels and the x-axis title with
  a bare `fillText`, outside the label registry**, so anything placed afterwards
  through `lab()` cannot dodge them. Wrap it (this sim's `axesT`) and register the
  tick boxes, or stage labels will land on ticks at some canvas size. The same
  applies to any marker row a view draws itself — register it BEFORE the panel
  that will place labels over it.
- **Lay a stage out from the bottom up.** Reserving a fraction for the top panel
  and letting the bottom one take the remainder puts its tick labels and axis
  title into the caption at small sizes; the axis furniture has to be subtracted
  first.
- **A "blocks, one per item" representation needs a gap that is a FRACTION of the
  cell.** A fixed 1.2 px gap is invisible at a 40 px cell, so the blocks and bars
  representations become the same picture with two names — and a mutation sweep
  will not catch it, because both are correct drawings of the same data.
- **A pixel-to-world drag map must subtract the box's own origin.** `x * per`
  rather than `(x − box.x) * per` is off by the left margin, which looks like a
  calibration error and is a missing term.
- **A set of "auto" ladder rungs borrowed from the source sim can be too coarse.**
  PhET's histogram zoom rungs start at 25 samples because its fields hold 200; at
  two dozen samples the tightest of them still leaves the data a sliver. Extend
  the ladder BELOW the source's smallest rung rather than leaving a default that
  hides the data.

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

## 2026-09-21 — gases-intro: PhET's two intro screens, plus the P–V plane and the four gas laws measured off the simulation

### Added

`docs/phets_revised/gases-intro.html` (197 KB, 3424 lines), a clean-room remake
of PhET Interactive Simulations' **Gases Intro** 1.1.7 (CC-BY 4.0; new code, no
PhET code or assets). Built on the finished `gas-properties` remake: the
event-driven hard-disk engine (`build/gas-properties/p2_engine.js`, documented
in its `ENGINE.md`), the shared house layer, the drawing helpers and the
container/plot layer are taken **unchanged** by `make_shared.py`, which asserts
every block it slices.

**Four views.** `the box` is PhET's Intro screen, `the laws` its Laws screen,
`P against V` is the Laws screen's own gas on the pressure–volume plane, and
`the four laws` measures Boyle, Charles, Gay-Lussac and Avogadro by running the
simulation.

**What is exact.**

- PhET's Gases Intro is its Ideal screen twice over, and the minified original
  says so outright: `class wb extends vb{ … hasHoldConstantFeature:!1 }` is
  registered as `IntroScreen` and `class Sb extends vb{ …
  hasHoldConstantFeature:!0 }` as `LawsScreen`, both extending `IdealScreen`.
  The two screens therefore differ in exactly one thing — the Hold Constant
  panel — and the UI drive asserts that the Intro view hides it and the Laws
  view shows it.
- PhET's constants, read out of `docs/phets/gases-intro_en.html`: BOLTZMANN
  8316 AMU pm² ps⁻² K⁻¹ (+1.849e-4 against CODATA k_B/u = 8314.4626), KG_PER_AMU
  1.66e-27, ATM_PER_KPA 0.00986923, the box (8750 × 4000 pm, 5–15 nm wide), the
  masses and radii, the lid, the limits, the counter periods. Every one pinned
  absolutely.
- The 2-D Maxwell–Boltzmann one-sided flux ⟨vₓ⁺⟩ = √(kT₂/2πm), by scipy
  quadrature, and the identity ⟨vₓ⁺⟩ = ⟨v⟩/π exactly.
- The hard-disk contact measure M = 2πσab − 4σ²(a+b) + 2σ³ **term by term**:
  the edge integral ∫₀^σ 2 arccos(x/σ) dx = 2σ, and the corner term, which is
  where the +2σ³ comes from — the two edge arcs overlap exactly on the quarter
  disc x² + y² < σ², and that overlap integrates to σ²/2 per corner
  (analytically π²/16 + 1/4 twice, minus π²/8). Cross-checked against an
  8-million-sample Monte Carlo of the whole measure.
- PhET's heater as a rate: v → v(1 + a/800) per 60-fps frame, so 300 K → 1000 K
  takes 20.0788 ps at full heat — computed in closed form and frame by frame.

**The one falsifiable number on these screens** is the Collision Counter.
Nothing in PhET *defines* how often the disks strike the walls; kinetic theory
says the rate is 2 n Z ⟨v⟩/π (a + b) with a = W − 2r, b = H − 2r and n = N/ab.
For 100 heavy disks at 300 K in the 10 nm box that is **6.4234/ps** with Z = 1
and **7.2178/ps** with the hard-disk Z. `derive.py` gets that three independent
ways (the flux form, the per-particle free-flight form |vₓ|/a, and a
free-flight simulation of 4000 disks), and `selfTest` measures it off the
engine:

- collisions **off**, 200 disks, 60 ps: the measured count equals the
  closed-form free-flight count particle by particle, **exactly** (`eq`, not
  `close`), and the rate formula reproduces that realisation's mean;
- collisions **on**, 120 disks, 120 ps (~1000 hits, 3 % Poisson): the measured
  rate matches theory-with-Z within 3.5 σ and sits more than 2 σ **above** the
  Z = 1 value, so the measurement can tell the two apart.

`the four laws` runs a real sweep: it engages PhET's hold, steps the controlled
variable to five targets, settles 2 ps, then counts wall hits for the window.
The sim says plainly on the canvas and in the equation bar that the *law* line
is exact by construction (PhET defines P = NkT/V), so what the sweep tests is
the **controller** — and that the invariant holds to about 1e-9, which is PhET
rounding the held-pressure width to five decimals. The hit-rate panel beside it
is the half that could come out wrong.

`selfTest` **659 passed, 0 failed** (14 s); UI drive **149 passed, 0 failed**;
mutation sweep **75 mutants (64 physics, 11 UI), 75 caught, 0 survivors** — the
first pass left 17 alive and every one of them is written up below
(`_out/mutation_log.txt`, then `mutation_log_fix.txt`, `mutation_log_fix2.txt`
and `mutation_log_final.txt`, the last of which is the sweep of the file that
ships). `derive.py` writes `refvals.txt` and `p7a_refs.js`, so no pinned value
is retyped.

### Fixed (during the build)

- **A contact-measure "cross-check" that double-subtracted the corners.** The
  first quadrature subtracted each edge's removed arc independently, which
  over-counts on the quarter disc where two of them overlap, and it disagreed
  with the closed form by 2.5e-4 — looking exactly like a wrong closed form.
  Root cause: the four removed arcs are not disjoint. Replaced by a term-by-term
  check (edge integral, corner overlap integral, then the sum) plus a
  whole-measure Monte Carlo, which agree to 1.5e-12 and 9.5e-5 respectively.
- **The theory kept its Z with collisions switched off.** `hitRateTheory(g,true)`
  applied the hard-disk Z whatever `g.collisions` said, so the "with Z" curve
  would have claimed a crowding correction that is not there. Root cause: Z *is*
  the pair collisions; the flag has to reach the theory. Fixed, and both
  branches are now asserted (`useZ && g.collisions !== false`), with a mutant
  that removes the guard.
- **The Avogadro sweep measured a clump, not a gas, and read 38 % low.**
  Stepping N with PhET's pump puts every new disk at one point (−r, H/5), and
  fifty of them take tens of picoseconds to spread across a 10 nm box; the
  wall-hit rate measured 2 ps later is the rate of a clump near the entry
  point. Root cause: a *measurement* sweep needs a homogeneous gas, which the
  pump does not give. The sweep now changes the count with `gasFill` (uniform,
  non-overlapping) and says so in the code and the captions; the pump is still
  PhET's, on the screens where PhET uses it. A mutant restores the pump.
- **The Avogadro sweep ran to an area fraction where B₃ is not enough.** Its
  top target was 2.5 × the starting count (η = 0.14), where the truncated
  virial series under-predicts Z by more than the counting error. Capped at
  2 × (η = 0.112) and stated.
- **The Charles targets could round past the container's end.** PhET's
  hold-pressure controller solves w = NkT/(P H D) and rounds it to five
  decimals; a target that asks for exactly 15000 pm can round to 15000.00001
  and raise "Volume would be too large". The targets are now clamped a hair
  inside, and the derivation records that at P = 1183.248 kPa and N = 100 the
  container's 5–15 nm range is exactly 150–450 K.
- **The energy-ledger assertion normalised by a field that does not exist.**
  `gasLedger()` returns `{E, pred, resid}`; the test divided by `led.scale`,
  which is `undefined`, so `(led.scale||1)` made it an *absolute* 1e-12 bound on
  a residual of order 1e-7 on an energy of 1.5e9 — i.e. 1.6e-16 relative, which
  is rounding. It passed in one sim by luck and failed in the other. Now
  normalised by `led.E` in both.

**Seven drawing defects the PNGs caught and the audit could not.** The layout
audit compares text boxes with text boxes, so a curve running through a label,
a key covering the start of a trace, and a degenerate axis are all invisible to
it. Rasterising every view and looking at it found:

1. The hit-rate panel's three labels were struck through by the bars and lines
   they annotated. Every in-plot key now paints a patch of the canvas ground
   first (`keyAt`), the way `plotNote` already did.
2. **A hold makes two of P, V, T proportional, so they are drawn as the same
   line and one disappears under the other** — Charles's law and Gay-Lussac's
   law made invisible by being exactly true. Each series now has its own dash
   as well as its own colour, and the panel names the coincidence: "P and T
   move together: that IS Gay-Lussac's law".
3. Keys sat on the first 200 px of the very curves they described (the P–V
   key, both sweep keys). `keyText` now takes a corner, chosen per plot — and
   for the sweeps per *law*, since Boyle and Avogadro decay away from the top
   right while Charles and Gay-Lussac rise away from the top left.
4. The held-invariant axis auto-ranged onto a residual that is pure rounding,
   so all four ticks printed as "-0.0000". Below a thousandth of a ppm the axis
   is now fixed there and the key states the actual figure ("flat to 6.7e-10
   ppm — the controller is exact to rounding").
5. The hottest isotherm only clips the top-right corner of the P–V box, and the
   label search ran left to right and gave up, so it was drawn unlabelled. It
   now falls back to the entry point and hangs the label leftwards — and the
   mutant that removes the leftward hang survived the first sweep, because at
   the DEFAULT axis the label fits whichever way it hangs. Pinning it needed a
   state where it does not: cooled to 290 K the isotherm enters 0.1 nm³ from
   the right edge, and a rightward label runs off the plot. **A fallback has to
   be tested at the state that triggers it, not at the state you happen to be
   looking at.**
6. An empty P–V box auto-ranged to a 0.01 atm axis, which means nothing. It now
   falls back to the scale the default gas would set and says "there is no gas
   in the box yet".
7. The lone trace marker survived an erase and contradicted the readout beside
   it (12 atm on the plot, "—" in the panel). Re-seeded on draw, and pinned —
   the same fix the gas-properties remake needed.

One more, not a defect but a silence: after pumping, the measured wall-hit rate
can be tens of sigma below kinetic theory, because PhET's pump puts every
particle at one point and the theory assumes a uniform gas. The panel now says
how many sigma apart they are and that the gas may not be uniform yet, instead
of leaving the reader to conclude the theory is wrong.

**The mutation sweep, and the seventeen holes it found.** The first pass caught
54 of 71 and left 17 alive. Every survivor was a missing assertion, and the list
is worth reading as a list, because the *kinds* repeat:

- **Nothing pinned PhET's pump.** The π/2 fan, the √(3kT/m) speed and the
  restored Gaussian mean all mutated freely. Now: 1000 injections span the fan
  to FAN/1000 and are centred on π; with collisions off every speed is exactly
  √(3kT/m); with collisions on 200 injected at 437 K leave T at exactly 437
  while the individual speeds are visibly spread.
- **Dead code in the shared engine.** `hdZ1` is not called by this sim (`hdZ`
  computes the same thing by summing over pairs), so mutating it changed
  nothing. Rather than delete a function the engine owns, the test now asserts
  the two agree at N = 2, 50, 100, 400 — the identity, not a retyped formula.
- **The overlap branch of the contact quadratic had no boundary test.**
  `c < 0` → `c < −1` lets a pair overlapping by 0.002 pm collide, which no
  bulk statistic sees. Pinned at the join, the way the diffraction sim's
  small-argument series had to be.
- **PhET's five-decimal rounding of the held-pressure width was invisible**
  because every sweep target is a round number. Asserted on a width that is
  not: 137 disks going 317 K → 200 K ask for 6309.148… pm, and V/T can only
  hold to 8e-10 if the rounding really is at the fifth decimal.
- **The hold-T restore after a *partial* removal was untested** — the only
  removal any test did was "erase everything", which takes the empty-box Oops
  branch instead.
- **The Ideal wall's redistribution was untested**, in the model *and* in the
  pointer handler. Without it a narrowing leaves disks outside their own box;
  `gasWidthTo` moves the wall and nothing puts them back.
- **The lid's blow-off gap and the gauge's 0.75-ps refresh** had no test at all.
- **Two sweep knobs were self-consistent and therefore invisible**: the settle
  (now asserted to be exactly long enough for the overlaps a halving resize
  creates to separate) and the counting window (now asserted to equal what the
  slider says).
- **The P–V isotherm was computed inside the draw call**, so a mutant that drew
  it at 2T could only be caught by looking at the picture. Lifted into
  `pvIsotherm()` — the Known-bad rule that "if a mutant can only be caught by
  looking at the picture, the quantity is in the wrong layer".
- **A pointer-DOWN that repaints nothing** was invisible because the harness's
  recorder does not capture colours, and the grab's only effect is that the grip
  turns magenta. Assert that a frame was *drawn* from a proven-quiet loop, not
  that the geometry moved.

Two of the seventeen survived a second time, and both for the same reason —
**the test was written in terms of the thing it was meant to pin**:

- the lid-gap test set its gaps as `LID_WIDE ± 200`, so mutating `LID_WIDE`
  moved the test with it. Absolute gaps (1700 pm and 1200 pm) now.
- the Avogadro-clump test called `sweepSetCount` directly, while the mutant
  changes the *call site* inside `sweepApply`. The test now drives the real
  sweep.

And the third, the Charles clamp, survived because nothing asserted what the
guard guards; it now asserts that the extreme targets ask for a width strictly
inside the container (and only just). **73 caught, 0 survivors.**

### Known-bad candidates

- **A sweep that changes the particle count with the pump is measuring a clump
  for the first tens of picoseconds.** PhET's `addParticles` puts every new
  particle at one point; the gas needs roughly W²/(π²D) to homogenise (≈ 36 ps
  for 200 heavy disks in the 10 nm box, longer when it is cold). Any
  measurement taken over a settle shorter than that is of the injection, not of
  the gas — it read 38 % low here. Use a uniform fill for measurements and keep
  the pump for the screens that are about the pump.
- **A "cross-check" of a closed form by re-integrating its terms independently
  can be wrong in exactly the place the closed form is right.** Removed arcs,
  excluded areas and shadowed regions overlap near corners; subtracting them
  one at a time over-counts. Check term by term against the *derivation's own*
  decomposition, or Monte-Carlo the whole thing, and say which you did.
- **A flag that switches the physics must reach the theory curve as well as the
  model.** Switching particle collisions off makes the gas ideal, so a theory
  curve that keeps its compressibility factor is drawing a correction that the
  simulation no longer has. Assert both branches.
- **`gasLedger()` has no `scale` field.** `{E, pred, resid}` only. An assertion
  written as `1e-12*(led.scale||1)` is an absolute bound of 1e-12 on a quantity
  of order 1e9, i.e. 1e-21 relative — unreachable, and it passes only when the
  residual happens to be tiny in absolute terms. Normalise by `led.E`.
- **A test whose own SETUP is written in terms of the constant it is meant to
  pin cannot see that constant change.** The lid test built its gaps as
  `LID_WIDE + 200` and `LID_WIDE − 300`, so doubling `LID_WIDE` moved the gaps
  with it and every assertion still held. Two of seventeen survivors were this,
  and it is invisible on reading — the test looks careful. Write the setup in
  absolute numbers and pin the constant separately.
- **A test that exercises the HELPER does not test the CALL SITE.** The
  Avogadro-clump assertion called `sweepSetCount` directly while the mutant
  swapped the call inside `sweepApply` for PhET's pump; the helper was perfect
  and the sweep was wrong. When the defect you are guarding against is "somebody
  calls the other function", the test has to go through the caller.
- **A defensive clamp with nothing asserting what it guards is indistinguishable
  from dead code.** The Charles targets are held a hair inside the container so
  the controller's `toFixed(5)` cannot round past the end; removing the clamp
  changed no outcome at any reachable setting. Either assert the property the
  clamp provides (here: the extreme targets ask for a width strictly inside the
  range, and only just) or delete it.
- **A pointer-DOWN must repaint, and the display-list harness cannot see why.**
  Grabbing a handle changes only its colour, and the recorder captures geometry,
  not styles — so "the picture changed" is the wrong assertion. Assert that a
  frame was *emitted at all* from a proven-quiet loop.
- **A law that is exactly true draws two curves on top of each other, and the
  law disappears.** Hold V and P/T is constant, so the normalised P and T
  traces are the same line; hold P and so are T and V. Whichever is drawn
  second hides the first, and the screen that exists to show the law shows one
  curve. Give every series its own DASH as well as its own colour, and say on
  the canvas that they coincide — the coincidence is the result.
- **An auto-ranged axis on a residual that is pure rounding prints every tick
  as "-0.0000".** The house `tickFmt` caps at four decimals, so an axis a
  billionth of a ppm wide has four identical labels and tells the reader
  nothing. Fix the axis at a readable floor and print the real figure in the
  key. (Related to the existing Known-bad about `ticksFor` spinning on a span
  below its endpoints' rounding — `niceRange` stops the hang, not the
  meaninglessness.)
- **A fallback branch must be tested at the state that triggers it.** The
  P–V isotherm label falls back to hanging leftwards when its curve enters near
  the right edge; at the default axis it fits either way, so the mutant that
  removed the fallback survived a 75-mutant sweep with the drawing asserted and
  the label present. The assertion only bites at 290 K, where the isotherm
  enters a tenth of a nm³ from the edge. Same shape as the Known-bad about
  series branches that no test argument reaches — but for *layout*, where the
  triggering state is a range of the axis rather than a range of the argument.
- **The layout audit cannot see a line crossing a label, a key covering the
  start of a trace, or an axis whose ticks are all the same.** All three shipped
  past a clean audit here and were found only by rasterising every view and
  looking at it. The audit is necessary and it is not sufficient; the brief's
  "then actually look at the PNGs" is load-bearing.

## 2026-09-21 — projectile-sampling-distributions: PhET's sampling screen on its own, with σ/√n derived and the theorem separated from the algebra

### Added
- `docs/phets_revised/projectile-sampling-distributions.html` (152 KB, single
  file, no network, works from `file://`). PhET's Projectile Sampling
  Distributions is the Sampling screen of Projectile Data Lab on its own, and it
  ships the same bundled model, so this file runs the SAME engine as
  `projectile-data-lab.html` — `build/projectile-sampling-distributions/make_engine.py`
  copies it and edits exactly the blocks PhET's own build branches on the sim
  name for (bin widths 0.5/1/2/5 m with 0.5 the default rather than 1, no
  total-bins strategy, a zoom ladder to 250 samples rather than 500 projectiles,
  a speed-mean range floor of 20 m/s rather than 15), plus the two tables the
  Sampling screen trims to one row each (the launcher orientation, fixed at 30°,
  and the projectile type, cannonballs only). The picture layer is likewise
  extracted from the data lab's by `make_views.py` and asserted, not retyped.
- Four views: **the field** (PhET's screen — six mystery launchers, samples of
  n = 2, 5, 15 or 40, the sample mean joining the histogram below), **the four
  sample sizes** (PhET's thumbnail row at full size, all four distributions on
  one axis), **one launch** (the parent the samples come from, against its exact
  density — a standard error means nothing without the σ it divides), **the limit
  theorem** (the measured standard errors against σ/√n on log axes, and the same
  four residuals in units of their own sampling spread).
- **What is exact.** The trajectory (PhET's closed form, checked against
  v² sin2θ/g and an independent route in `derive.py`); the random stream
  (mulberry32 + Box-Muller, bit-identical to derive.py, so the page and the
  Python twin generate the same sample means and the page's means, standard
  deviations at ddof 1 and 0, medians and every histogram bin count are pinned
  against numpy's at all four sample sizes); the parent distribution (a 96×96
  Gauss-Legendre product rule over the two truncated normals, checked against
  scipy's adaptive quadrature at 1e-15 and against a 6×10⁶-draw Monte Carlo of
  PhET's actual re-draw mechanism, for all six launchers).
- **The result the file exists for: the theorem has two halves, and this sim
  keeps them apart.** sd(x̄) = σ/√n is exact for every n and every parent with a
  variance and follows from independence alone — it is asserted here at n = 2,
  where no theorem applies, from 20000 pairs. The central limit theorem is the
  further claim about SHAPE, and it is asserted separately: the skewness of the
  sample mean falls as 1/√n, from −0.098 for one launch to −0.0155 at n = 40. A
  sim that only shows the widths narrowing has demonstrated the algebra and
  called it the theorem.
- Verification: `selfTest` 314 assertions green under `osascript`; UI drive
  `ui_drive_projectile-sampling-distributions.js` 133 green (the launcher-barrel
  drag that scrubs through the six launchers, every chip row by `data-key`, every
  slider at min/max/mid on every tab, the keyboard, the resize); layout audit 0
  problems at 1400×820 and at 560×380; mutation sweep (below).

### Fixed (during the build)
- **PhET's zoom ladder starts at 25 samples because its fields hold 200, and at
  two dozen samples its tightest rung still leaves the histogram a sliver along
  the bottom of an empty panel.** Opening on PhET's default (0–50) drew 24
  samples with a tallest bin of 5 against a ceiling of 50. The default is now an
  auto rung that picks the tightest ceiling that holds the tallest bin, with a
  finer ladder (4, 6, 8, 10, 15, 20) below PhET's own; every rung PhET offers is
  still reachable by hand, and `selfTest` asserts the auto rung never crops a bin
  up to PhET's 200-sample ceiling.
- **A sample of 40 took a minute and a half.** The first state machine fired one
  projectile and waited for it to land. PhET's `SamplingField.totalSampleTime`
  spreads the n launches evenly over 0.75, 2, 5 or 9 s and lets the flights
  overlap; the model now does the same, in both this sim and the data lab, and
  the table and the behaviour are both asserted.
- **A drag measured from the pivot rather than from the grab point jumps before
  the pointer moves.** Grabbing the barrel eight pixels above its pivot stepped
  the launcher on immediately. The offset is taken from where the pointer went
  down.
- **Four stacked panels need room for their own tick labels.** In the
  four-sample-sizes view, panel i's x-tick labels landed in panel i+1's title;
  and at 560×380 four panels of 24 px each pushed the last one's axis title into
  the caption. Each panel now reserves its title and tick bands explicitly, and a
  narrow stage shows the two ends of the range (n = 2 and n = 40) with the reason
  written into the caption.
- **A 20000-draw tolerance written against `fieldBatch` fails on correct code**,
  because a field stops at PhET's 500 projectiles. The sampler is drawn from
  directly, and the 500 is asserted as PhET's own ceiling.
- **A "p pauses" assertion is vacuous when the clock was already paused.** The
  UI drive asserted it after an earlier `pauseU()`; it now sets the state
  explicitly first, which is the same discipline as a proven-idle baseline
  pointed at state instead of repaints.
- **Op-count floors copied from the sibling sim punished this one for being
  smaller.** They are derived from what this file emits (85, 147, 425, 109 ops at
  the four tabs), not from the data lab's.
- **A "+50 launches" button sat live on the screen whose datum is a whole
  sample**, where it did nothing. It is hidden there, shown on the parent view,
  and the UI drive asserts both.
- **"It is visibly not a normal" was false for two of the six launchers.** The
  parent view's caption said it unconditionally; launcher 5's parent has
  skewness 0.028 and excess kurtosis 0.001, which is as normal as anything in
  the sim. The clause is conditioned on the launcher's own shape now, says what
  IS true in the quiet cases, and `selfTest` asserts both branches.

### Known-bad candidates
- **A ladder of "zoom" or "scale" rungs taken from the source sim can be too
  coarse for this one.** PhET's histogram rungs start at 25 because its fields
  hold 200 samples; at two dozen the data is a sliver. Extend the ladder BELOW
  the source's smallest rung rather than shipping a default that hides the data —
  and step it, so the axis does not jitter as the data arrive.
- **"One at a time, wait for it to land" is not how a sampling sim paces
  itself.** PhET gives a sample a total time and spreads its launches over it, so
  a bigger sample fires FASTER per shot, not slower. A queue that waits for each
  landing turns a sample of 40 into ninety seconds and the screen into a
  stopwatch.
- **A drag offset must be taken from the pointer-down position, not from the
  object's anchor**, or the first pointermove jumps by the grab offset. The
  symptom is an off-by-one in a discrete drag, which reads as a rounding choice.
- **A stack of panels is not a stack of boxes.** Each one owns a title band above
  it and a tick band below; laying them out on (height − gaps)/n puts panel i's
  ticks in panel i+1's title, and the sweep only sees it at one canvas size.

## 2026-09-21 — ph-scale: the beaker, the particles, the graph, and dilution done by mixing moles

### Added
- `docs/phets_revised/ph-scale.html` (171 KB), a clean-room remake of PhET's **pH Scale**
  1.7.6 (CC-BY 4.0; new code, no PhET code or assets). Six views: **the beaker** (PhET's
  Macro screen — twelve liquids, the dropper, the water faucet, the drain, and the pH
  meter whose probe you drag in and out), **the particles** and **the graph** (its Micro
  screen), **my solution** (its third screen), and two of this file's own: **dilution**
  and **the scale**.
- **Exact chemistry.** K<sub>w</sub> = 1.000e-14 at 25 °C (pK<sub>w</sub> = 14.000 — the
  conventional value, and the one PhET's hard-coded `14` encodes), so neutral is pH 7.000
  exactly. `[H3O+] = 10^-pH` and `[OH-] = Kw/[H3O+]`, both asserted against 50-digit
  `decimal` evaluation over the whole scale *including its ends*. `[OH-]` is written as a
  division on purpose: PhET's spelling `10^-(14-pH)` is out by up to 2.1e-15 because
  `pH - 14` is inexact in a double whenever pH < 7, while the division is out by 2.1e-16
  and keeps `[H3O+][OH-] = Kw` to a rounding. Molecule counts use the exact SI 2019
  N<sub>A</sub>; PhET's 6.023e23 is 1.43e-4 high and both are printed.
- **The dilution law, done properly — the point of the build.** What dilutes is not the pH
  and not either ion but the net strong acid
  `C = [H3O+] − [OH-] = −2√Kw·sinh(ln10(pH−7))`, a difference of *analytical*
  concentrations whose moles are conserved on mixing; water carries exactly none of it.
  So `C = (C1V1 + C2V2)/(V1+V2)`, then re-solve `[H3O+] − Kw/[H3O+] = C`, which is the
  water autoionisation PhET's rule leaves out. Implemented twice (the asinh closed form
  and the stable branch of the quadratic root) and asserted against a Decimal mole ledger
  plus a scipy `brentq` root of the charge balance. Two structural facts fall out and are
  pinned: diluting f-fold divides C by **exactly** f (0.0 relative error), and C is an
  **odd** function about pH 7 — so pH 2 and pH 12 are exactly as strong as each other and
  equal volumes of them are exactly neutral (the instinct that the acid wins is wrong).
- **PhET's own rule beside it, and the size of the gap.** A chip switches the model to
  PhET's `computePH` (mix the majority ion linearly, take a log, never re-solve). Over
  everything this beaker can reach — pH −1..15 × 0.015..1.2 L in 1.2 L — the two laws
  never differ by more than **0.0948 pH**, at pH 4.91 with 0.015 L in the beaker; at
  PhET's own liquids the worst is 0.0815 (chicken soup, 0.1 L in 1.2 L). Volume-averaging
  the pH, the mistake the view exists to rule out, is wrong by up to **4.42 pH**. The
  dilution view draws all three laws and the envelope of the exact-minus-PhET gap.
- **PhET's constants and rules, read from the minified original** and cited as PhET's: the
  twelve liquids' pH values and colours, the beaker's 1.2 L and 0.015 L minimum, the
  pH range −1..15 at two decimals, the dropper's 0.05 L/s and the faucets' 0.25 L/s, the
  0.5 L autofill at 0.45 L/s, water at 55 mol/L, the graph's 18 decades, the solute colour
  law (water → colour-stop over the first quarter, then → stock) and the particle rule
  (50 dots per 1e-7 mol/L inside pH 6–8, floor 5, the minority ramping to 3000 outside).
  At pH 13 the drawn ratio is 457:1 against a true 1e12:1, and the canvas prints both.
- **Measured pH ranges for four of the twelve**, quoted to their sources' own precision:
  blood 7.37–7.43 (Merck Manual Professional, "Acid-Base Regulation", J. L. Lewis III);
  orange juice 3.30–4.19, milk 6.40–6.80 and chicken broth 5.80 (FDA, "Approximate pH of
  Foods and Food Products"). **PhET's value lies inside every one of the four.** No range
  could be sourced for the other eight; they are drawn with no bar at all and the canvas
  says so rather than inventing one.
- Verification: `selfTest` **1957 passed, 0 failed**; UI drive **208 passed, 0 failed**;
  mutation sweep **90 caught, 0 survived**; display-list capture at 1400×820, 1100×700 and
  560×380 audited clean (0 layout problems) with every PNG looked at.

### Fixed (during the build)
- **The naive `[H3O+] − [OH-]` and the textbook quadratic root both lose their digits
  inside PhET's own range, and derive.py asserts that they still do.** The difference
  cancels near neutral (1.9e-11 relative at pH 6.999999, 1.7e-13 at 6.9999) and the
  textbook root `(C+√(C²+4Kw))/2` cancels for *every base*: 3.6e-5 at pH 13, 8.0e-4 at
  pH 14, **11 % at pH 15**. Root cause: both are differences of nearly equal quantities.
  The sinh and the rationalised branch `2Kw/(√(C²+4Kw)−C)` are exact, and the twin asserts
  the naive forms are *still* that bad so the branches cannot be quietly deleted.
- **Two of my own assumptions were wrong and the twin caught them.** (i) "Equal volumes of
  pH 2 and pH 12 come out acidic" — false: C is odd about 7, so they neutralise exactly.
  (ii) "PhET's N_A is 1.3e-4 high" — it is 1.43e-4. Both were written as checks, failed,
  and were corrected rather than loosened.
- **A pH round trip costs eight digits at high dilution, so the model keeps volumes.** A
  double holds `7 − ε` to an absolute 8.9e-16, so ε itself keeps only what is left:
  recovering C from a stored pH after a millionfold dilution is out by 4.0e-9 against
  2.2e-12 at a thousandfold. `beakerIons()` therefore builds *both* ion concentrations
  from C and never from the printed pH — pinned bit for bit at all 4104 reachable states.
- **The pH strip was never drawn at any stage size.** Symptom: the acidic/neutral/basic
  scale was simply absent from the beaker view. Root cause: it was sized from the height
  *left over* after the beaker, and there never was any; the guard `sy > bk.y1+10` was
  false at every size. The strip is now part of the layout, reserved before the beaker is
  sized.
- **The pH meter sat on top of the glass at 560×380.** Root cause: the meter was placed at
  `right − 140` while the beaker had already been sized from the whole span. Its width now
  comes out of the span *before* the beaker is sized.
- **The beaker was 600 × 420 and read as a tank.** Root cause: it filled whatever box was
  left instead of keeping PhET's 450 × 300 aspect. Same fault in `my solution`, where the
  beaker came out taller than it was wide and the strip above it was asked for at a y
  above the stage top.
- **The water pipe did not reach the spout it feeds** — drawn from the beaker's right wall
  outwards, it was a floating bar with nothing under it.
- **The particle view printed `drawn 0.00 : 1` for every base.** Root cause: both ratios
  were written hydronium-per-hydroxide. They are now majority-per-minority, with the names
  printed, which is also the number derive.py pins (457.20 : 1 at pH 13).
- **The "dots are capped" note was drawn in the liquid's dark ink above the liquid**, where
  the background is the page: invisible. Also, the dots were scattered across the volume
  label at the foot of the glass, which is drawn before them.
- **The difference panel was flat at zero at the default state.** Root cause: it plotted
  the gap at the beaker's *current* dilution, which is 1.0× when nothing has been diluted.
  It now plots the worst gap over every dilution the beaker can hold — whose peak is
  derive.py's headline 0.0948 pH — with the beaker's own value marked on top of it.
- **Five layout defects found only by the inline sweep and three only by looking at the
  PNGs**: the strip's words and numbers on one line ("0" under "acidic" at every size);
  labels pushed down onto the strip because its rectangle was not in the registry (`spit
  7.4` inside `neutral`); the x-axis label running into the caption in three views because
  `axesR` registers the *title* only; the linear graph's `4.0e-14` tick reaching the
  rotated y-axis title (fixed by drawing that axis in units of 10^exponent, PhET's own
  0–8 mantissa, with the factor printed in the title); and the meter's reading and its
  "probe is out" note on top of each other in every body under 82 px.
- **Five mutation survivors, each a real blind spot.** (i) The no-stop colour law was
  tested only at r = 0.5, the one ratio where `lerp(a,b,r)` and `lerp(b,a,r)` agree.
  (ii) The probe's wall margin was probed only far outside it. (iii) The dilution
  envelope's reach was never read off the model. (iv) The grab's repaint flag survived
  because the *previous* `pointerup` had called `refresh()` and re-armed `dirty` — the
  Known-bad "anything that forces a draw between an idle proof and the action" one layer
  out. (v) `[OH-] = Kw/h` versus a pH round trip agrees exactly at 1579 of the 4104
  reachable states, so a single-point equality pin lands on one of them; the sweep across
  the grid (2525 states differ, by up to 2.2e-15) is what kills it.

### Known-bad candidates
- **`lerp(a, b, 0.5)` is symmetric, so a two-colour ramp tested only at its midpoint is
  tested by nothing.** The no-stop solute colour survived a 90-mutant sweep with its two
  endpoints swapped. Probe any interpolation off its midpoint.
- **A panel sized from "whatever is left over" can be allocated zero and vanish without a
  single test noticing.** The pH strip was absent from every stage size of a shipped view
  because its guard was `if there is room`, and there never was. Reserve a fixture's space
  *before* sizing the thing next to it, and assert that the fixture is drawn.
- **A quantity written majority-per-minority one way round prints `0.00 : 1` for half its
  domain.** Ratios that can invert need the names of both ends printed with them.
- **`axesR` registers the plot TITLE and nothing else**, so a label placed under a panel
  lands on the *x-axis* label, and the rotated *y-axis* title (drawn at `b.x − 40`, about
  13 px wide) is invisible to every registry — a y-tick label wider than 34 px will reach
  it. Wrap `axesR` to register the x label, and keep linear tick labels short by drawing
  the axis in units of a stated power of ten.
- **An equality pin on a floating-point code path must be swept, not sampled.** Two
  spellings of `[OH-]` agree bit for bit at 38 % of the reachable states; a single-state
  `===` lands on one of those with 38 % probability and proves nothing.
- **A difference panel drawn "at the current setting" is empty whenever the current
  setting is the default.** Plot the envelope over the parameter instead, and mark the
  current setting on it.

## 2026-09-21 — wave-interference: captions clear the HTML hint (re-landed)
### Fixed
- Its captions were fitted to the full canvas height, so the bottom-left caption
  line shared pixels with the HTML hint (`#hint{bottom:11px}`) — the trap the
  `wave-on-a-string` build found and `waves-intro` confirmed against this file.
  Neither the capture nor the audit can see it, because the hint is HTML, not
  canvas. The four call sites now fit to `H − HINT_H` (18 px) and the layout
  sweep asserts the bottom-left corner is clear, exactly as the sibling builds
  do. The assertion was run against the unfixed file first and failed all 148
  configuration × size cases; after the fix the lowest canvas text clears by
  4 px at every size.
- Two narrow-stage consequences of the reservation, fixed rather than left to
  collide (11 collisions at 560×380 on the first rebuild): below 300 px of tank
  the far field's cut plot is dropped with a note and its two squares take the
  height, and the tank's "needs a taller window" notes take short forms.
### Verified
- Rebuilt file 209.2 KB: selfTest 1453/0 (was 1305; the 148 new checks are the
  corner assertion), UI drive 257/0, mutation sweep 81/81 in one pass on a copy
  `cmp`-equal to the shipped file, audit 0 problems at 1400×820, 1100×700 and
  560×380, affected PNGs looked at again at all three sizes.
- The five part files `build/waves-intro/assemble.py` pins are byte-identical
  (SHA-256 re-checked), so `waves-intro` is unaffected: re-verified 968/0, 164/0.

## 2026-09-21 — generator: water turns a magnet beside a pickup coil, and the flux integral that makes the EMF, in six views

Remake of PhET's Generator 1.0.7 (`docs/phets/generator_en.html`; its single
screen comes from the shared FARADAYS_ELECTROMAGNETIC_LAB repo) as
`generator.html`. Third sim cut by `family.py` from the engine in
`build/magnets-and-electromagnets/`: the electromagnet (`#emag`), the bar-magnet
screen (`#bar`) and the far-field view (`#far`) are stripped, the coil DRAWING
(`#coil`) and the generator (`#gen`) are kept, and the build asserts that no
symbol of a stripped feature is left in the file. New code; no PhET code or
assets.

### Added
- **the generator** — PhET's screen: a faucet whose flow turns a water wheel
  carrying the bar magnet; a pickup coil of 1–4 loops whose area runs over
  PhET's 20–100 % of 70685 mm²; a light bulb or a voltmeter; electrons whose
  speed shows the induced current (with PhET's electron/conventional Current
  Flow preference); the wheel's speed written in its hub, as PhET's RPMDisplay
  does; the field as PhET's 40-mm needle grid; a compass, which here rides a
  TURNING field and lags it; the field meter.
  **flux and EMF** — Φ(θ) over one turn of the wheel against the single cosine
  a distant magnet would give, and below it the EMF, −Nω dΦ/dθ, with its peak
  marked (it is not at 90°). **the coil face** — the two ways of adding the
  field over the coil's disc, drawn as integrands whose AREAS are the two flux
  estimates: the exact strip (B integrated along the chord, off the page as
  well as in it) against PhET's (the in-page value carried across the chord,
  with its own 5-mm samples), and below, their ratio across the area slider.
  **field lines**, **on the axis**, **the needle** — the family's views of the
  magnet the wheel carries.
- What is exact: the magnet is the family's uniformly magnetised cylinder in
  closed form. **The flux is the AREA integral of B over the coil's disc** —
  16-point Gauss–Legendre in radius by 32-point trapezoid in angle, the field
  taken in 3-D off the page, asserted against scipy's `dblquad` to 1e-10 G·mm²
  at every angle and unchanged when both rules are doubled. One turn is sampled
  at 128 angles and kept as a Fourier series, so Φ(θ) and dΦ/dθ are exact
  between the samples; only odd cosines survive (Φ is even in θ and reverses
  every half turn) — asserted, not assumed, to 1e-11. **The EMF is Faraday's
  law**, −N dΦ/dt = −Nω dΦ/dθ: linear in N and in ω, reversed by reversing
  either, zero where the flux is stationary, checked against a finite
  difference of Φ itself AND against −dΦ/dt taken by stepping the page's own
  clock (whose midpoint error is checked for ORDER — halving the step quarters
  it — rather than pretended away).
- **Two findings about the original, both drawn on the page.** (i) Because the
  flux is not a cosine, the EMF does not peak with the magnet across the coil:
  it peaks at 24.79° for the smallest coil and 37.95° for the largest (python,
  bounded maximiser), the value at 90° being 0.29–0.60 of the peak. (ii) PhET's
  own flux is a line sample — B_x every 5 mm along the coil's vertical diameter
  in the page, each weighted by its chord, with the field off the page taken to
  be the field in it — which overestimates the flux by 13 % for the smallest
  coil and 57 % for the largest. That is not an error in PhET: its EMF is
  deliberately a relative number against its own full scale (maxEMF = 1.2e5 in
  its units), and a fast line sample is the sensible choice for it. This page's
  volts are volts only because the integral is done.
- PhET's values carried: the turbine and coil positions, 60 RPM at full flow,
  the drag rule (rpm = flow/100 × (1 − drag) × 60, drag a linear ramp in
  N × area from 0.01 to 0.2 scaled by the magnet's strength — phenomenological,
  and labelled so: a real back-torque needs the circuit's resistance, which
  neither PhET nor this page models), maxEMF, the 5-mm sample spacing, the
  1–4 loops and 20–100 % area, and the layout. The water falls on the LEFT of
  the wheel here so the magnet's angle increases; PhET steps its own the other
  way, which only reverses the sign of the EMF (said in the header).
- Verification: `derive.py` (the family's) grew section 7 — the flux against
  `dblquad`, its harmonics by numpy's FFT over 256 angles, the peak by a
  bounded maximiser, PhET's line sample, and the drag rule — plus
  `gen.drag`/`gen.drag.default`; selfTest 1162 assertions including a
  24-configuration × 5-size layout sweep; UI drive 198; mutation sweep 112 of
  112 caught (78 physics, 34 UI; 106 of 106 on the previous build, after the
  survivors below were pinned); display-list audit 0 problems over 23
  captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **The EMF peak came out at 155° instead of 24.8°.** Root cause: with only odd
  harmonics, |dΦ/dθ| is symmetric about 90°, so there are always TWO peaks and
  the coarse scan took whichever floating-point noise made larger. The search
  runs over the first quarter turn, as `derive.py`'s does.
- **The coil-face view drew two curves that lay exactly on top of each other.**
  Root cause: with the magnet in line with the coil — the view's own default —
  the field over the face depends only on the distance from the axis, so the
  ring average and the in-page value are equal BY SYMMETRY, and PhET's error at
  that angle is not a difference between them at all but a difference of
  weights. The panel now draws the two flux integrands strip by strip, whose
  areas are the two estimates; the exact one is asserted to integrate to
  `flux1` and PhET's, summed at its own 5-mm spacing, to `fluxPhet1`.
- **The pickup coil read as a copper barrel and the bulb sat behind it.** The
  turns are 44 mm apart now with a thinner wire, the leads are drawn before the
  front turns and the indicator after them, 92 mm above the coil's top.
- **The bulb looked dark when it was working.** PhET's brightness rule is
  |EMF|/full scale and this generator's peak is only 0.57 of full scale, so the
  glass is painted through a NAMED display mapping, `bulbShade` = sqrt — the
  same kind of thing PhET does to the needles' alpha. The model number is
  untouched and the readout prints it.
- **Every flux tick label read "0.0000".** Root cause: the flux is ~1e-6 Wb and
  `tickFmt` caps at four decimals. The flux axis is in microwebers.
- **Two stacked panels cannot both carry an x label**: the house layout leaves
  46 px between them and the lower panel's title starts 24 px above its own
  box, so the upper x label and the lower title collided at 560 × 380. The
  upper panel's x quantity went into its title.
- **14 mutants survived the first sweep.** The real ones: nothing pinned the
  clamp on the normalised current (and it turns out nothing can REACH it here —
  the largest EMF the sliders allow is 0.57 of full scale, now asserted, where
  PhET's larger flux estimate is what its clamp is for); nothing pinned the
  bar's dipole moment or m = M V on a page with no far-field view (the axis
  view's dipole curve is now asserted against the exact field at 4 m); nothing
  measured the flux view's live marker, the drawn turns' centring, the
  indicator's clearance from the coil, or the water landing on the wheel's rim;
  the compass was grabbed at its exact centre (so a lost drag offset made no
  difference) and its own motion masked the repaint after a move (the meter,
  grabbed off-centre with the compass away, tests both now); and the "tools are
  not in this view" check looked for a slider in a group that has none, so it
  passed everywhere. Two were equivalent and were replaced rather than excused:
  the Fourier normalisation differs only for k = 0 and the Nyquist term, and
  the series' sine terms are zero — both facts are asserted, so no mutation of
  them can change a number.
- **The wheel's speed was written under the magnet that is bolted across it**,
  so the capture showed a hub with nothing in it — which is the whole reason to
  look at the PNGs. It is drawn after the magnet now, on its own disc, and a
  test measures which fill is last at the hub.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **A test that compared the drawn water with the function that drew it.** The
  water's landing point is now a property: the bottom of the column lies ON the
  wheel's rim, at WHEEL_R from its hub, on the upper LEFT, which is why the
  wheel turns the way it does.

### Known-bad candidates
- **A view whose default setting hides its own point.** The coil-face panel was
  correct and useless at θ = 0. When a comparison collapses by symmetry at the
  default, either the default or the comparison is wrong.
- **Sampling a field along one line and calling it an area integral.** PhET's
  own rule, and the reason this page's flux had to be integrated properly; the
  error grows with the coil (13 → 57 %).
- **A display mapping must be named and kept out of the model.** `bulbShade` is
  a drawing constant with its own test; the brightness the readout prints is
  PhET's |EMF|/full scale.
- **`|dΦ/dθ| has two peaks`** — any extremum search over a symmetric function
  must state which half it is searching.

## 2026-09-21 — magnet-and-compass: PhET's Bar Magnet screen as its own sim, on the family engine, in five views

Remake of PhET's Magnet and Compass 1.0.7
(`docs/phets/magnet-and-compass_en.html`; its single screen is PhET's Bar
Magnet screen from the shared FARADAYS_ELECTROMAGNETIC_LAB repo) as
`magnet-and-compass.html`. Built from the same engine as
`magnets-and-electromagnets.html` and `generator.html`: the shared parts, the
Python twin and the mutant list live in `build/magnets-and-electromagnets/`,
and `family.py` cuts this page from them. New code; no PhET code or assets.

The electromagnet is **stripped**, not hidden: the `#coil`, `#emag` and `#gen`
blocks are removed at build time and the build asserts that no symbol of them
(`coilField`, `loopB`, `I_MAX`, `drawBattery`, `projectPsi`, `fluxSeries`, …)
is left anywhere in the file. 2390 lines against the full sim's 2858.

### Added
- **the bar magnet** — PhET's screen, entire: drag and flip the magnet, set its
  strength (0–300 G, 75 % at start), the field as PhET's 40-mm needle grid with
  its 2(|B|/300 G)^(1/2.7) brightness rule, a compass that swings and settles,
  the field meter (B, Bx, By, θ; gauss or tesla, PhET's formats), see inside,
  the Earth. **field lines** — exact lines of B in the page, seeded at equal
  flux, and the magnet's bound surface current. **on the axis** — B and μ₀H in
  closed form against the point dipole, μ₀H drawn in three pieces so nothing
  joins its branches across a pole face. **the far field** — |B| on the axis
  and the bisector against the dipole on log axes, and the octupole approach.
  **the needle** — the compass as a damped rotor, its period against |B|.
- What is exact: as the family's — the uniformly magnetised cylinder's field in
  closed form (Derby & Olbert through Bulirsch's `cel`), exact field lines,
  numerically taken dipole limits, the octupole coefficient 2(b² − 3R²/4).
  What is modelled: the compass rotor, with PhET's constants converted from
  per-frame to per-second (κ = 6.25 /(G s²), γ = 2 /s, flip kick 0.75 rad/s at
  25 frames/s) — said on the page. The Earth adds no field, as in PhET.
- Verification: selfTest 775 assertions (the shared engine suites plus this
  page's model, panels and a 17-configuration × 5-size layout sweep); UI drive
  147; mutation sweep 67 of 67 caught (49 physics, 18 UI) — the family's list,
  filtered to the patterns that are actually in this page (26 dropped with the
  electromagnet, each named by `gen_mutants.py` rather than skipped in
  silence), plus four of its own; display-list audit 0 problems over 16
  captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **The page would not parse after the electromagnet was stripped**
  (`SyntaxError: Return statements are only valid inside functions`, line 499).
  Root cause: the `#coil` block that was meant to hold `projectPsi` alone ran
  from its comment to the next function definition, swallowing a nested
  `#endcoil` inside `psiMid`; the strip then cut at that inner marker and left
  the rest of `psiMid`'s body — including its `return` — outside any function.
  Fixed by ending the block at `projectPsi`'s own closing brace and marking its
  two call sites separately.
- **Four mutants survived this page's first sweep**, each a real finding:
  (i) the Newton projection onto Ψ was unreachable here (coil-only) yet still
  in the file — it is now inside `#emag`; (ii) nothing proved the frame loop
  drove the model rather than the tests — both UI drives now pump frames and
  watch the needle turn; (iii) nothing pinned that μ₀H is drawn in three
  pieces — asserted on the drawn strokes (no segment straddles a pole face);
  (iv) an equivalent slider mutant, replaced by a family-level one that bites.
- **My first version of (iii) was wrong in premise**: it asserted that the μ₀H
  curve is drawn only inside the magnet. Outside the magnet μ₀H = B and the
  page draws it deliberately. Replaced by the straddle test.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **Two dimmed boxes and a readout in gauss under the tesla chip** — both the
  ordinary kind of UI slip; the sweep found them through the "a dead control is
  dimmed" and "the unit chips reach the readout" mutants.

### Known-bad candidates
- **Trimming a family page is not finished until a mechanical check says so.**
  A stripped page that still names a stripped symbol is code the tests cannot
  reach; `family.py`'s `FEATURE_SYMBOLS` assertion is what catches it, and it
  has caught three separate leaks (an unmarked branch in `sourceField`, a REF
  key, and the axis view's coil branch).
- **Never assert a page's behaviour against a formula retyped in the test.**
  Two survivors here were tests that recomputed the constant they were
  checking; the fix is always a `REF` value or a drawn measurement.
- Branch-scoped group lookups: `groupU('tools')` matched the hidden screen's
  identically-named group in the full sim. A control lookup must prefer the
  visible group, or the test drives a control the user cannot see.

## 2026-09-21 — magnets-and-electromagnets: a bar magnet and an electromagnet, their exact fields, in six views

Remake of PhET's Magnets and Electromagnets 1.0.7
(`docs/phets/magnets-and-electromagnets_en.html`, screens from the shared
FARADAYS_ELECTROMAGNETIC_LAB repo) as `magnets-and-electromagnets.html`, in
the house form: the scaffold, palette, `h()`, 2-D layer and view helpers
extracted from `projects/simulations/build_buoy` by `family.py`, which asserts
every function it carries and rewrites only the title, header comment,
accents, `<h1>`, tagline and site-nav hrefs. New code; no PhET code or assets.

This is the FAMILY's home build dir: one engine (`e1_core.js` … `e5_gen.js`),
one set of drawing primitives (`v_common.js`, `v_screens.js`, `v_analysis.js`),
one Python twin (`derive.py`) and one mutant list, from which `family.py` also
cuts `magnet-and-compass.html` and `generator.html`. Each page carries only
what it uses: five feature markers (`#bar`, `#coil`, `#emag`, `#far`, `#gen`)
are stripped at build time, and the build then asserts that no symbol of a
stripped feature is left anywhere in the page.

### Added
- **the bar magnet** — PhET's screen: drag and flip the magnet, set its
  strength (0–300 G, 75 % at start); the field as PhET's 40-mm needle grid with
  its 2(|B|/300 G)^(1/2.7) brightness rule; a compass (a damped rotor, so it
  swings and settles); the field meter reading B, Bx, By and θ in gauss or
  tesla with PhET's own formats ("~ 0 G" below 0.01 G, scientific tesla); see
  inside; the Earth. **the electromagnet** — a coil of 1–4 loops driven by a DC
  battery (±10 V) or an AC supply (0–110 V, 0–1.25 Hz), electrons whose speed
  shows the current, the same field display, compass and meter. **field lines**
  — exact lines of B in the page, seeded at equal flux, with the magnet's bound
  surface current. **on the axis** — B and μ₀H along the axis in closed form
  against the point dipole; for the coil, the loop sum against the continuous
  sheet of the same ampere-turns. **the far field** — |B| on the axis and the
  bisector on log axes against the dipole, and the approach to it as the
  octupole C/r². **the needle** — the compass as a damped rotor, its period
  against |B| (Gauss's method), with an energy ledger.
- What is exact: the magnet is a uniformly magnetised cylinder (PhET's
  250 × 50 bar), so its B field is exactly that of an ideal finite solenoid
  carrying the bound current K = M × n̂ — Derby & Olbert's closed form (Am. J.
  Phys. 78, 229 (2010)) through Bulirsch's generalized complete elliptic
  integral, in 3-D, everywhere. The coil is N thin loops by Biot–Savart, exact
  on and off the axis. Field lines are RK4 along B/|B| with the magnet's side
  wall crossed exactly (secant landing) and, for the coil, a Newton projection
  onto its closed-form flux function; they close to ~2e-5 mm (magnet) and
  1.5e-4 mm (coil). The far-field limits are taken NUMERICALLY (Richardson at
  2, 4, 8 m) and come out 1 to ~4e-9; the approach matches the octupole
  coefficients 2(b² − 3R²/4) and 6⟨x²⟩ − 3a²/2 in closed form. One measured
  number: μ₀ = 1.25663706127e-6 N/A² (CODATA 2022, NIST).
- **PhET's precomputed grid is a sampling of this same field.** `derive.py`
  reads all 15,971 grid points out of the 1.0.7 build and compares: median
  2.2e-7 G per G of strength, 97.9 % within 1e-4, worst 4.6e-3 beside the
  pole-face rim where the exact field has its logarithmic edge singularity.
  Said on the page, and asserted point by point in selfTest.
- Verification: `derive.py` → `refvals.txt` (scipy dblquad over the current
  sheet, quad, ellipkm1, brentq, solve_ivp; 198 reference lines), emitted into
  the page as literals by `family.py` — never retyped; selfTest 1150
  assertions including a 17-configuration × 5-size layout sweep; UI drive 228;
  mutation sweep 89 of 89 caught (70 physics, 19 UI); display-list audit 0
  problems over 19 captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **Field lines stalled on the axis at z = −125.10 mm.** Symptom: one line of
  ten never closed. Root cause: the side-wall correction (B_u jumps by μ₀M
  across the bound-current sheet) was applied on the END faces too, where there
  is no sheet, because the test only looked at ρ; the line then followed a
  field that does not exist. Fixed by applying it only when both ends of the
  step lie within |z| < b on opposite sides of ρ = a, with a secant landing on
  the wall and a nudge across it.
- **Coil lines closed to 1.2e-2 mm, not to rounding.** Root cause: RK4 alone
  accumulates. The coil has a closed-form flux function, so every vertex is now
  pulled back onto its own level set by Newton along ∇Ψ; closure fell to
  1.5e-4 mm. (The magnet's Ψ needs a quadrature, so its lines still rely on
  RK4 — stated in the page's comment.)
- **The loop field was 11 % wrong at ρ = 1e-6 a.** Root cause: the textbook
  K, E form of the off-axis loop field subtracts two nearly equal terms. Both
  B_ρ and Ψ are now the cancellation-free `cel` forms.
- **The electromagnet read as a copper blob with the electrons in a lattice.**
  Fixed by drawing all the turns' dark rims in one pass and their copper in a
  second, reducing the perspective tilt 0.36 → 0.28, and staggering the
  electron phases turn by turn.
- **The magnet painted over its own field lines** in the lines view: the body
  now goes down first, translucent.
- **Mixed tick decimals, two x labels in the far view, and raw logarithms when
  the field was zero.** Root causes: `fmt(t,2)` regardless of the tick spacing;
  `ticksFor` given the full width on a log axis; and the zero case returning
  before the second frame was drawn. Fixed with `tickFmt` (decimals from the
  spacing), `logTicksFine` and an empty-case path that keeps both frames.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **Four mutants survived the first sweep** — the AC full scale, the AC
  frequency, the pendulum period and the "~ 0 G" threshold — because the tests
  recomputed the same constants they were checking. All four are now pinned to
  `derive.py`'s printed values. **Four more survived the second**: a
  centre-grab that hid both a lost drag offset and a shrunken hit box (the
  magnet is now grabbed by its north END), a repaint masked by the compass's
  own motion (the compass is switched off for that test), a provably dead
  `rest=false` (removed, and its mutant replaced by one on the rest criterion),
  and a readout that did not change when the magnet moved with the tools hidden
  (the readout now carries the magnet's position — a page fix, not a test fix).

### Known-bad candidates
- **A feature marker that spans more than its feature.** Marking `projectPsi`
  as coil-only wrapped the block from its comment to the next function, which
  swallowed a nested `#endcoil` and left an orphaned `return` in the stripped
  page (`SyntaxError: Return statements are only valid inside functions`).
  Same-feature markers must not nest, and a block must end at its own
  function's closing brace.
- **A registry entry is safer than a ternary** when code is cut at build time:
  `A.kind==='magnet'?x:y` cannot be stripped in half, so per-source values
  (the axis curve, the view's title) live on `ANA_SRC` instead.
- **A mutant on a quantity that is provably zero is equivalent.** The Fourier
  sine terms and the k = 0 normalisation in the generator, and any drag-offset
  test that grabs an object by its centre: pin the consequence, or replace the
  mutant.
- The `og-pyfiles` rule of this repo applies here too: `derive.py` is the
  authority, and every JS constant that matters is emitted from it rather than
  typed into the page.

## 2026-09-21 — waves-intro: PhET's three screens on the landed wave-interference engine, PhET's own light screen and tone, and v = fλ measured on the lattice by least squares
### Added
- `waves-intro.html` (183 KB, 2775 lines), a remake of PhET's Waves Intro 1.1.24 in four views:
  *water*, *sound*, *light* — PhET's three screens, one view each — and *the three media*,
  an analysis view of the law that ties them together. Credit line in the header and on the
  page; site nav absolute; no network.
- **PhET's three screens.** One hard source five cells in from the left edge of PhET's
  151 × 151 lattice, with frequency, amplitude and PhET's green wave-generator button
  (continuous: it switches the source on and off and restarts its phase at zero; pulse: it
  fires one period and pops back up, and is dead while that pulse runs — PhET's
  `handleButton1Toggled`, and its `disturbanceTypeProperty` link, which stops everything when
  the mode changes). Each screen keeps its own lattice, as each PhET screen keeps its own
  model. Water adds PhET's top and side views, sound its air parcels (waves / particles /
  both) and PhET's tone, light the screen at the right-hand edge. Graph of the centre line,
  tape measure, stopwatch, two-probe wave meter, normal and slow speed, pause, one step,
  clear, reset all; the button, the tape's ends and the probes are dragged on the canvas.
- **Built on the landed engine, which is not re-derived.**
  `build/wave-interference/p2_engine.js` ships unchanged (its SHA-256 is pinned in
  `assemble.py`, with the four other house parts taken from that build), and the lines this
  sim needs from its proof — the dispersion relation, the calibration of the three media,
  Mur's coefficients — are read from `build/wave-interference/refvals.txt` rather than derived
  again. This build's own numpy twin reproduces that file's tank and pulse scenarios to
  **1e-13** before adding its own: sound at 0.2937 per ms, light, a source switched off at
  step 150 and on again at 190, and the light screen.
- **Exact:**
  - the lattice's dispersion relation and the time step solved from it at every frequency, so
    λ = v/f and T = 1/f hold along the lattice axes at all nine settings (three media × fmin,
    default, fmax) — PhET's one fixed step per medium leaves its wavelengths 0.7 % to 3.2 %
    short, which the readout prints for the current setting;
  - the engine's point-source path against the numpy twin at 1e-11 over five scenarios;
  - PhET's light screen as Waves Intro draws it, read from the minified original: the mean
    square of the last column over whole periods, a 3-row smoothing, a ±39-row box average
    (`lightScreenAveragingWindowSize` 40, against Wave Interference's 3) and PhET's
    piecewise-linear brightness table, pinned knot by knot;
  - PhET's tone: 1000 f Hz at output level 0.3 A/10, as a looped buffer of whole cycles whose
    samples are computed here rather than taken from an OscillatorNode, so the suite can check
    the pitch, the level and the seam.
- **New here — the wavelength measured on the lattice.** At every cell of the tank's axis a
  least-squares fit against the drive's own phase (sin, cos, a constant and a drift, the last
  two to absorb the 2-D wake of the switch-on, which dies only as 1/ωt); the wavelength is the
  slope of the unwrapped phase over cells 30 to 100, the envelope's power the slope of log
  amplitude against log r. The JS and the numpy twin agree to **4e-16**. What it finds:
  - λ within **0.03 %** (light), **0.08 %** (water) and **0.15 %** (sound) of v/f at PhET's
    default frequencies, and an envelope power of **−0.47 to −0.54** against the −½ that 2-D
    spreading demands;
  - at water's 0.25 Hz, where the tank is 1.4 wavelengths long, **1.6 % short** — of which the
    2-D near field (the phase of H₀(kr), scipy, fitted over the same cells) is 0.46 % and the
    rest is the tank: on a 401-cell lattice the same fit returns 0.49 %;
  - the light screen departs from the 1/r of a point source by up to **9 %**: a ripple of about
    one wavelength's period that the edges reflect back (rms 2.0 % on PhET's 151 cells, 1.5 %
    on 401, 0.75 % on 601) on a smooth **6 %** tilt that is the square lattice's own
    anisotropy. PhET's ±39-row average smooths the ripple away, which is why it is there.
- **Verification:** selfTest 968 passed, 0 failed under osascript (a layout sweep of 15
  configurations × 4 sizes, every slider end in every medium at both amplitude ends and both
  modes, and the #hint corner asserted clear). UI drive 164 passed, 0 failed: three custom
  pointer actions (PhET's button, a tape end, a probe), each through the frame loop from a
  proven-idle baseline, every tab, slider, checkbox, chip, button and key, resize, the tone
  against a stub AudioContext, and reset-all against a fully disturbed state. Mutation sweep:
  98 mutants (79 physics, 19 UI), every one on a copy inside `_out/`. All 79 physics mutants
  were swept under jsc against the shipped file — **79 caught, 0 survived** — after proving the
  runner can see a failure; `tools/mutate.py` itself, under osascript, swept all 19 UI mutants
  and a 29-mutant physics cross-section covering every layer of the file and all three
  first-round survivors — **48 caught, 0 survived** — and the two runners agree on every mutant
  they share. Audit: 0 layout problems at 1400×820, 1100×700 and 560×380 (at 560 the
  under-readout advisory only). All fifteen captured views were looked at.
- **Sources:** PhET's values, read from `docs/phets/waves-intro_en.html` (1.1.24): the lattice
  (151, pad 20, C = ½, source column 25, row 75), 20 × 111/61 steps per second, the amplitude
  calibration 1.2 and range 0–10 with 8 initial, the colour scale 2.14, the three media
  (widths, speeds, frequency ranges starting mid-range, scale bars, time scales), the 90-step
  intensity history and its 3-row smoothing, the screen's ±39-row window and brightness table,
  and the tone's 1000 f Hz and 0.3 A/10. PhET's model note for waves-intro ("a subset of the
  Wave Interference simulation, which shows one scene per screen") was fetched from GitHub.
  Colour: the CIE 1931 2° table (DOI 10.25039/CIE.DS.xvudnb9b), via the file the
  blackbody-spectrum build fetched.
### Fixed (during the build)
- **A claim about a drawing's scaling was true only where the field is inside the colour
  scale.** The parcel displacement is scaled so that a wave at PhET's full colour (2.14) moves
  a parcel 0.3 of its spacing — but beside a point source the field is four times that, and
  the largest push is really 0.39 of the spacing. The caption, the derivation and the header
  all said 0.3. They now say what derive.py measures, and the parcels are pinned against the
  twin position by position.
- **Three sliders are labelled "amplitude", one per medium, and the UI harness found the wrong
  one** — the hidden light slider rather than the visible water one, so two assertions failed
  for a reason that had nothing to do with the sim. The finder now takes the visible row.
- **A silent tone cannot be shown to be stopped.** The tone tests ran with the clock paused
  from an earlier block, so "switching the source off stops the tone" passed vacuously on the
  stop count and failed on the assertion that could see it. The clock now runs through the
  whole tone sequence — the dual of a proven-idle baseline.
- **An HTML entity in a checkbox label.** `intensity graph (not in PhET&rsquo;s Waves Intro)`
  is built from a text node, where a browser draws the entity verbatim. The UI harness now
  walks every label, button and heading for `&…;` (and deliberately not the `.tag` and `.src`
  blocks, which are set through innerHTML, where entities are right).
- **Op-count floors, three times over.** One floor for every configuration failed the side
  view (10 fills, honestly) and the analysis view (curves, not fields), and would have passed a
  blank field view. Each configuration now carries its own floor at 70 % of what it emits at
  its leanest size, and the tab floors come from the first draw, which is a tank with no waves
  in it yet.
- **A caption long enough to squeeze out the panel it explains.** At 1100 × 700 the full
  caption left 30 px under the plane, so the three measurement strips — the point of the view —
  were dropped. The layout now falls back to the short caption when that is what keeps them.
- **Three significant figures hid the difference a row exists to show.** The analysis readout
  printed "104 cm" for v/f and "104 cm" for the measured wavelength. Both are now at four
  figures (103.9 against 103.8).
- **`sigf` renders 2.998e8 as "2.998×10^+8".** The speed of light appears in the readout, the
  caption and a canvas label, so there are now `sciTxt` (superscript glyphs) and `sciHTML`
  (`<sup>`), asserted against both forms.
- **A label hung to the left of a marker lies along the line it names.** The light line's
  label cannot go above-right (it would run under the floating readout), and below the marker
  it collided with the axis ticks at 560 px — caught by the layout sweep. It now clears the
  line's own rise, falls back to the medium's name alone, and is dropped if even that will not
  fit; the caption and readout still carry all three speeds.
- **The side view's source spike ran to the floor of the picture.** The source cell swings 1.2
  × the amplitude — 9.6 lattice units at the default, four and a half times the colour scale of
  2.14. The surface is clipped at ±1.8 of that scale and the caption says so.
- **The marked air parcel was magenta**, which in this sim already means the source, its
  button, the tape's ends and the probes. It is cyan, and the caption names it.
- **The wave meter's window was 2.5 periods of the medium's SLOWEST frequency** (inherited from
  wave-interference), so at the default the chart was 60 % empty. It is 2.5 periods of the
  frequency on show.
- **The tone's rounding was pinned only where rounding cannot be caught.** At 0.33 and 0.44 per
  ms the cycle count and the buffer length come out exact, and at 0.2937 both fractions are
  above ½ — so round → floor and round → ceil would both have survived, exactly as
  wave-interference's Known-bad predicts. A fourth case at 0.301 per ms (150.5 cycles,
  22123.25 samples) pins both.
- **The sweep's three survivors were all test gaps, and one was dead code.**
  - *a new medium restarts the clock* (`R.t = 0` in `runSetScene`): only the UI suite could see
    it, because the physics suite never reset a run that had been **stepped**. It now asserts
    that `resetRuns` puts t, n, the lattice, the amplitude, the mode and the stopwatch back.
  - *the unwrap's second branch*: this wave travels outward, so its phase only ever falls and
    the `d < −π` branch is reached by no measurement in the file. The unwrap is now a function
    of its own (`unwrapPhase`), asserted in both directions — including a rising ramp of
    0.41 rad a step through every wrap, which nothing in the sim produces.
  - *solve4's pivot search* (largest → smallest pivot): a well-conditioned 4 × 4 is solved to
    1e-12 whichever pivot is taken, so no measurement could see it. It is now given a system
    whose first pivot is zero, which only a row swap can solve.
- **A mutant that turns a correction loop into an infinite loop hangs the sweep, and the
  runner's timeout takes the whole run down with it.** The first draft mutated
  `while (d > π) d −= 2π` into `d += 2π`, which never terminates — `tools/mutate.py` has no
  per-mutant timeout handler, so the sweep stalled there and would have aborted 30 minutes
  later. The pattern now changes the correction from 2π to π, which still changes the answer
  and still ends, and the other branch is mutated the same way.
- **`capture_all.sh` would have audited one size while looking as though it audited three.**
  `SIZES=(${@:-1400x820 1100x700 560x380})` puts the whole default into ONE word in zsh when the
  script is run with no arguments, so it makes a single directory called
  `c1400x820 1100x700 560` and captures once. Every run here passed the three sizes explicitly,
  so the captures were right, but the trap was live (another build in this batch hit it). The
  default is now its own array, and the script was re-run with no arguments to prove it: three
  directories, three audits, 0 problems.
- **A second estimator was added for the wavelength, not a second assertion.** The phase-slope
  fit is now checked against the spacing of the snapshot's own zero crossings, which shares no
  code with it: they agree to 0.008–0.024 % at four settings. At water's 0.25 Hz the fit window
  holds only **two** crossings, so that estimator is a single spacing there — which is pinned
  too, because it is the reason the hard case is hard.
### Known-bad candidates
- **A scaling described "at full colour" is not a bound near a source.** A displacement scaled
  so that a full-colour wave moves a marker 0.3 of a spacing will move it further wherever the
  field exceeds full colour — beside a hard source it always does. State what the sweep
  measures, not what the scale factor was chosen for.
- **A caption can squeeze out the panel it is explaining.** Where a layout puts a measured
  caption and the panels in the same column, the caption must be allowed to shorten, or the
  first thing lost at a middling window size is the content.
- **Three significant figures hide the difference a comparison row exists to show.** When a row
  prints a measurement beside the theory it is being compared with, give both enough figures
  for the difference to survive the rounding.
- **A label beside a marker on a sloped line must clear the line's own rise, not just the
  marker.** Hung to the left of a marker on a line of slope −1 in screen pixels, a horizontal
  label lies along the line unless it is lifted by (its own length) × (the line's slope).
- **A harness finder must pick the VISIBLE control when several share a label.** Three sliders
  labelled "amplitude", one per medium, and only one on show: matching the last one found is
  matching the wrong one (the same family as wave-interference's "achromat" chip).
- **A tone that is already silent cannot be shown to be stopped.** Any test that an action
  stops something needs that thing demonstrably running first, the way a repaint test needs a
  proven-idle baseline.
- **`SIZES=(${@:-a b c})` is one word in zsh, not three.** A capture script whose default sizes
  are written that way silently captures a single size named after all of them, and its audit
  then covers one picture while reading as though it covered every size. Give the default its
  own array, and run the script once with no arguments to see what it really does.
- **`wave-interference.html` fits its captions to H, not H − 18**, so the last line of its
  bottom-anchored captions shares pixels with the house `#hint` — the trap `BRIEF.md` records
  from wave-on-a-string, which the display-list capture cannot see because the hint is HTML.
  This build reserves the 18 px (`HINT_H`) and asserts that no canvas text enters the hint's
  corner, at four sizes and fifteen configurations. That build was not touched.
- **PhET's Waves Intro can never show its intensity graph**: the screen is built with
  `showIntensityCheckbox: false`, so `showIntensityGraphProperty` stays false forever. Reading
  Wave Interference's controls as Waves Intro's would put a control on the page that PhET's
  own build cannot reach.

## 2026-09-21 — my-solar-system: PhET's eleven orbital systems on a fourth-order symplectic integrator, the two-body case against its closed form, and what the method keeps
### Added
- `my-solar-system.html` (192 KB), a remake of PhET's My Solar System 1.3.16 in four views:
  *two bodies*, *the lab*, *the exact orbit*, *conservation*. Credit line in the header and on the page;
  site nav absolute; no network. Engine, utilities and drawing kit are read from
  `build/keplers-laws/` — one source for the family.
- **PhET's two screens are the first two views**, with its controls: the mass sliders (0.1–300 × 10²⁸ kg,
  showing "≤ 0.1" for a test body as PhET does), one to four bodies, all eleven orbital systems, the
  values table, the centre of mass, the paths (capped at PhET's 20 AU), the velocity and gravity arrows
  with its ×10ⁿ control, the grid, the measuring tape, the zoom ladder (25–125 view units per AU), the
  play/step/restart controls, "return the bodies" and the centre-of-mass frame.
- **The analysis pair**: *the exact orbit* draws the closed-form two-body solution (the relative Kepler
  conic about μ = G(m₁+m₂), the two similar conics about the centre of mass, which drifts in a straight
  line) against the integration, with their difference and the separation plotted below; *conservation*
  plots |ΔE/E|, |ΔL/L| and |Δp|/p along the run, runs PhET's own shipped step beside ours on the same
  system, and measures both orders by halving the step four times.
- **Exact:** two-body runs against Kepler's equation (the browser tracks the closed form to 1e-9 AU over
  120 frames and the Python twin to 2e-9 AU over 300); momentum and angular momentum are conserved by
  construction and measured at |Δp|/p ≤ 7e-15, |ΔL/L| ≤ 1.3e-14 over 2,000 frames of four systems, with
  |ΔE/E| ≤ 6.1e-10; the four-star ballet is asserted to be the homographic solution it is (measured over
  a whole period: the square stays square to 2.2e-14 of a side and the configuration returns to its start
  within 1e-11 AU, each star on an ellipse of e = 0.3837 about μ_eff = Gm(1/√2 + ¼)). Everything is pinned to `derive.py`,
  which integrates each system with scipy's solve_ivp at rtol 1e-12.
- **Verification:** selfTest 1135 passed, 0 failed under osascript (23 s; a 15-configuration × 4-size
  layout sweep); UI drive 150 passed, 0 failed (a body and a velocity-arrow tip dragged through the frame
  loop from a proven-idle baseline with their exact values pinned); mutation sweep 52 of 52 caught on a
  copy in `_out/`; display-list audit 0 problems over 20 captures; every PNG looked at.
- **What this file measured about PhET** (all in `derive.py`, all stated on the page):
  - **PhET's integrator is not the PEFRL it is named after.** It carries PEFRL's three coefficients but
    evaluates the acceleration ONCE per step and reuses it for all four kicks, which composes to exactly
    x + vh + ½ah², v + ah: first order. Measured by halving the step: error ratios 1.9, 2.0, 2.0
    (order 0.97) against 16.0, 16.0, 16.6 (order 4.02) for the real thing. Its 4,000/N substeps a frame
    hide it — but its energy still drifts 3.7e-6 in the first second of running, where ours drifts 1e-10.
  - **PhET's G = 4.4567 is 0.107 % below** the 4.46149 that CODATA's G gives in its own units, and PhET
    solves its time unit from its G, so its "km/s" is 1.000538 true km/s. Kept, so the presets move as
    PhET's do; the readout gives both.
  - **PhET's "Hyperbolic" system is not hyperbolic.** Its three test bodies pass the star at 0.878, 0.929
    and 0.995 of the escape speed on ellipses of e = 0.954, 0.926 and 0.990, returning after 12.6, 32.5
    and 1,791 years.
- **Where this differs from PhET, deliberately:** a collision merges the pair keeping mass, momentum and
  the centre of mass; PhET keeps the heavier body's mass and hands it the lighter one's momentum, which
  conserves momentum but loses the mass. Both are stated in the readout.
### Fixed (during the build)
- **The saved "start" state was captured before PhET's centre-of-mass subtraction**, so "return the
  bodies" handed the system a net drift it had never started with. The start is now saved after the
  subtraction, which is also what the exact-orbit view anchors on.
- **A named orbital system was being trimmed by the stale body count**: loading the four-star ballet with
  the count still at 2 gave two stars. A named system now brings its own count.
- **An HTML entity reached the canvas**: the "hyperbolic" system's name carried `&ldquo;`, which `plain()`
  cannot decode (its table has no smart double quotes), so the stage title drew it raw in four captures.
  The name now carries the literal glyphs.
- **The gravity arrows ran off the stage** (418 px of arrow at the default system) because the reference
  force was a round number rather than a real one. The reference is now the pull between PhET's own star
  and planet at their starting separation, and the shared kit caps an arrow at 0.42 of the box, draws the
  cut end hollow and says so on the canvas.
- **A five-digit tick label reached the rotated axis title** in the energy panel (the ballet's energies are
  −1.2e5); the panel now draws in whatever power of ten keeps the numbers short and names it on the axis.
- **The chaos note was pushed out of the stage and into the caption** by the label registry when it sat at
  the foot of the box (nine captures, found by the audit); it now sits under the title.
- **The exact orbit was anchored at the start state but read from t = 0.** The centre-of-mass button saves
  a new start WITHOUT stopping the clock, so after pressing it at t = 0.4 the closed-form solution was
  evaluated 0.4 ahead of the bodies and the drift readout jumped by most of an orbit. A saved start now
  carries the clock reading it was taken at (`sys.t0`), and the exact orbit is read at `sys.t − t0`.
- **The scene was not clipped to its stage.** A body whose centre is one pixel inside the view still draws
  a disc and a velocity arrow past the frame: the capture of "hyperbolic" had both out on the page
  background, where the audit cannot see them (it checks text, and a body is not text). Everything drawn
  in world coordinates now goes through `withClip`, and the labels that ride on a body are collected and
  written after the clip is lifted so none of them is cut.
- **The centre-of-mass label was written across the star.** In a star-and-planet pair the centre of mass
  sits on the star, and a label offset by a fixed (12, 14) px lands on its disc (three captures). It is
  now pushed along the line from the nearest body through the cross, by that body's drawn radius plus
  13 px, with its alignment chosen from the direction.
- **The mutation sweep found three blind spots**, each now an assertion: every PhET preset loads with its
  centre of mass at rest, so deleting the drift term of the exact two-body solution changed nothing any
  test could see (a system with a moving centre of mass is now in the suite); PhET's 20-AU path cap
  (MAX_PATH_DISTANCE) could be raised a hundredfold unnoticed (the path bookkeeping is now walked by hand
  and both caps asserted); and `ehistReset` could be made to rebuild the exact orbit from wherever the
  bodies had got to rather than from the saved start (its contract is now tested directly, mid-run, which
  is what turned up the clock bug above). The clip and the label placement carry mutants of their own.
### Known-bad candidates
- **A "start state" must be saved after every normalisation the loader applies.** Saving it before PhET's
  centre-of-mass subtraction made the restart button hand the system a drift it never had.
- **`plain()` has no smart quotes.** `&ldquo;`/`&rdquo;` pass through unchanged and land on the canvas.
  Write canvas strings as literal glyphs (the wave_fronts rule, one entity wider).
- **An inverse-square arrow has no natural maximum.** Cap it to the box, mark the cut end, and say so;
  and make the reference length a named physical force, not a round number.
- **A conserved-quantity test on presets that all start at rest cannot see a drift term.** Include one
  system whose centre of mass is moving.
- **A label at the foot of a stage box can be shifted INTO the caption by the label registry.** Put
  persistent notes under the title, where the registry's shifts stay inside the box.
- **A saved "start" is not always at t = 0.** Anything that re-saves the start without stopping the clock
  (here the centre-of-mass button) breaks every calculation that treats the start as the epoch. Save the
  clock reading with the state.
- **A window test on a body's CENTRE does not keep the body inside the box.** Its disc, its velocity arrow
  and its marker rings all reach past the frame, and the display-list audit cannot see it: the audit
  checks text. Clip the whole world-coordinate pass, and collect the labels that ride on a body so they
  are written outside the clip.
- **A label pinned to a point can land inside a body that is drawn at that point.** Push it out along the
  line from the body's centre through the point, by the body's drawn radius plus a margin, and choose the
  alignment from the direction.

## 2026-09-21 — keplers-laws: the ellipse from its state vector, equal areas by mean anomaly, T² against a³, and Kepler's equation solved in front of you
### Added
- `keplers-laws.html` (197 KB), a remake of PhET's Kepler's Laws 1.2.12 in five views:
  *the first law*, *the second law*, *the third law*, *all laws*, *Kepler's equation*. Credit line in the
  header and on the page; site nav absolute; no network. It shares its engine with
  `my-solar-system.html`: `build/keplers-laws/p2_engine.js` (Kepler's equation, the conic from a state,
  the sector areas, the N-body integrator) and `p1_utils.js`, `p4a_helpers.js`, `p4b_kit.js` are read by
  both assemblers, so the two sims cannot drift.
- **PhET's four screens are the first four views**, with every control its inventory lists: the star mass
  (0.5–2 M☉, snapping to our Sun within 5 % as PhET's does), "always circular", the target orbits
  (PhET's Mercury to Jupiter, enabled only for our Sun, as PhET enables them), foci + string, axes +
  semiaxes, eccentricity, apoapsis and periapsis (disabled below e = 0.01, PhET's own threshold),
  period divisions 2–6 with PhET's swept-area bar chart and its eraser, the a and T overlays with the
  power chips a/a²/a³ and T/T²/T³, speed, velocity, gravity with its ×10ⁿ control, grid, measuring tape,
  stopwatch, the play/step/restart controls and PhET's three speeds (¼, 1, 7/4).
- **House additions, named as such**: a log–log panel on which every orbit about one star lies on a line
  of slope exactly 3/2 with PhET's five planets on it; a panel of T²/a³ against the star's mass; a "put
  the planet on it" button for the target orbits; and *Kepler's equation* — the auxiliary circle with the
  mean, eccentric and true anomalies, the three plotted over one period, and Newton's iteration drawn on
  f(E) = E − e sin E − M from PhET's own starting guess E₀ = M.
- **Exact:** the elements come from the state vector in closed form (vis-viva for a, the eccentricity
  vector for e and the periapsis direction, the sign of xv_y − yv_x for the sense of travel) and the
  position in time from Kepler's equation by Newton safeguarded with the bracket [M − e, M + e].
  `derive.py` checks E against scipy's brentq at 120 (M, e) pairs (worst 8.9e-16) and the whole orbit
  against solve_ivp at rtol 1e-13 (the Kepler position stays within 8e-12 a over 2.3 periods); the sector
  areas are πab/N in closed form, re-derived by scipy quad (worst 1.3e-15) and again in the browser by
  32 panels of 8-point Gauss–Legendre, which knows nothing of Kepler's equation; T = 2π√(a³/GM).
  Units: AU (IAU 2012), the Julian year, GM☉ = 1.32712440042e20
  m³s⁻² (Wikipedia, the value `lagrange_points.html` already carries) → K = 39.4769264 AU³yr⁻² per M☉ and
  1 AU/yr = 4.740470464 km/s.
- **Verification:** selfTest 1031 passed, 0 failed under osascript (with an 18-configuration × 4-size
  layout sweep); UI drive 171 passed, 0 failed (the planet and the velocity-arrow tip dragged through the
  frame loop from a proven-idle baseline, one axis at a time, with the drag's exact value pinned; every
  view idle while the clock is paused); mutation sweep 71 caught of 72 on a copy in `_out/`; display-list
  audit 0 problems over 20 captures; every PNG looked at. The one survivor is equivalent and is named so
  in `mutants.json`: flipping the sign of f′ = 1 − e cos E in the solver's PRE-LOOP line only. That value
  is used for the first safeguard test and the first step; the iteration is bracketed, so a wrong first
  step is recovered from — the loop recomputes f′ correctly and the root stays inside [M − e, M + e].
  Measured over an 8,241-point (M, e) grid (e to 0.999, M over three turns each way): 7,861 answers
  bit-identical, worst |ΔE| 3.6e-15 rad at |E| ≈ 17 (one ulp), iteration count −9 to +5. Only the step
  count moves, and the step counts on the page come from the anomaly view's own Newton panel, not from
  this solver. The same flip INSIDE the loop is a separate mutant, and it is caught.
- **Where this differs from PhET, deliberately** (each measured in `derive.py`, each stated on the page):
  PhET's μ = 4.45669 M is 0.24 % away from its own year, so a circular orbit at 1 AU reads 29.855 km/s
  where 2π AU in its 1.000-yr period is 29.785; here the measured constants agree (29.7847). PhET's clock
  advances the mean anomaly 6.3/T rad per year rather than 2π/T, so one revolution reads 0.99733 T on its
  stopwatch; here the clock is exact. PhET stops Newton once a step falls below 0.01 rad, which leaves the
  planet up to 2.4e-5 AU (3,559 km) off on the default orbit; here the step is driven to 1e-15.
### Fixed (during the build)
- **The safeguarded Newton stalled at high eccentricity.** The obvious safeguard — reject a step that is
  not strictly inside the bracket — rejects the CONVERGED step, because it lands exactly on the bracket
  end it has just set. Measured at e = 0.99, M = 0.3: 5 Newton steps, then 46 bisections. Replaced with
  Numerical Recipes' rtsafe rule (bisect only when the step leaves the bracket or fails to halve the
  interval); the same case now takes 5 steps and the worst case over the whole grid is 15.
- **A planet dropped exactly on the star had no direction to be pushed back along.** The drag clamped
  r ≥ 1.4 R_star by scaling the position vector, which is (0, 0) there, so the planet stayed at the centre.
  It now keeps the direction it had. Found by the selfTest drag case, not by the UI drive.
- **Pressing play through the checkbox never erased the sectors.** `setRunning` guarded on
  `on && !ST.running`, and the checkbox had already written `ST.running = true` before calling it, so the
  guard was false and PhET's "the areas disappear and the planet starts swiping" did not happen. One
  function (`onPlay`) now owns that work and both paths call it exactly once.
- **The mutation sweep found three blind spots in selfTest and three in the UI drive**, all fixed by
  assertions rather than by code changes: the "treat it as a circle" threshold could be raised to 0.1
  (which would flatten Venus, Earth and Jupiter — PhET's own target orbits are e = 0.0068, 0.0167, 0.0484)
  without failing anything; `conicPoint`, which draws the orbit, the sectors and the apsis markers, was
  tested by nothing; the anomaly view's clock could be detached from the sim's; the velocity drag passed
  with a wrong scale and with a flipped sign because the test only asserted "it went down"; and "the drag
  restarts the clock" was vacuous because the clock was already at zero.
- **Seen in the PNGs:** the measuring tape was not part of `simReset`, so a tape dragged in one test was
  still there in the next capture; the string labels d₁ and d₂ collided when the planet sits at an apsis
  (both strings lie along one line there) and are now pushed off their own segments in opposite
  directions; the c = ae label sat inside the star's disc; "a = 1.500 AU" was drawn twice when both the
  semiaxes and the third law's own overlay were on; the apsis labels ran into the star and now sit
  outward along their own direction; the velocity label was struck through by its own arrow; the anomaly
  view's stage title overflowed a 560-px canvas; and the ν curve had a false vertical line down the right
  edge of its panel, from taking it mod 360 when it already runs 0 → 360.
- **The stage title was pushed outside its own box** when the label registry found that corner taken (by
  the velocity label, at the sizes where the stage is short). The title and the scale note are now drawn
  FIRST, before anything that can claim their place; measured after the fix: 0 titles above the frame over
  the 20 captures.
- **The gravity arrow was unclipped** — an inverse-square force grows without bound as the planet
  approaches the star, and the arrow left the stage. It is now capped to 0.42 of the box, drawn with a
  hollow tip, and the canvas says so. (Found in the sibling sim, fixed in the shared kit for both.)
### Known-bad candidates
- **A bracket-safeguarded Newton must not reject the converged step.** The step that ends the iteration
  lands exactly on the bracket end it has just set, so "strictly inside (lo, hi)" rejects it and the solver
  falls back to bisection — 51 iterations instead of 5, with no wrong answer to show for it. Use rtsafe's
  test (bisect when the step leaves the bracket or is not halving the interval).
- **A "treat it as a circle" threshold is invisible to any test whose orbits are eccentric.** Pin a small
  but nonzero eccentricity explicitly: the sims' own presets (Venus 0.0068, Earth 0.0167) are the cases
  that a sloppy threshold would flatten.
- **Anything computed inside a draw call needs a model function to assert against.** `conicPoint` drew the
  orbit, the swept sectors and the apsis markers, and the sweep could break it freely; the fix is to assert
  it against the state at the time that true anomaly is reached.
- **A state that two controls can set needs its guard in ONE place.** A handler that writes the state and
  then calls a guard reading that same state (`if(on && !ST.running)`) can never fire.
- **A clamp that scales a vector has no direction at the origin.** Keep the previous direction (or a
  fixed one) rather than multiplying zero by a scale factor.
- **Draw the title and the scale note FIRST.** Drawn last, the label registry pushes them out of the box
  when something else has taken that corner, and they end up on the page background.

## 2026-09-21 — greenhouse-effect: PhET's three screens on one exactly solvable layer model, and the line between its fit and its physics

### Added
- **`docs/phets_revised/greenhouse-effect.html`** (181 KB, 3179 lines) — a remake of PhET
  Interactive Simulations' *Greenhouse Effect* 1.3.13 in the house style. Five views:
  **the waves** and **the photons** (PhET's Waves and Photons screens: twelve sheets,
  concentration by slider or by date, the cloud, the glaciated ice-age ground, the
  thermometer in K / °C / °F, the energy-balance meter and the flux meter), **the layers**
  (PhET's Layer Model screen: 0–3 explicit sheets, their absorbance, ½–2 suns, the surface
  albedo, each sheet's temperature), and two analysis views of this file's own, **the
  ladder** and **the record**.
- **The whole model is exact, and derived rather than asserted.** For N sheets of infrared
  absorbance a_i over a ground of albedo α under an absorbed solar flux F, each sheet
  conserving energy makes the net upward flux the same at every level, so
  `U_i = U_{i−1} − F a_i/(2 − a_i)`, and with `U_N = F` at the top

      sigma T_s^4 = F [ 1 + Σ_i a_i/(2 − a_i) ].

  It is implemented **twice** — that recursion, and a dense Gaussian solve of the full
  13-unknown flux system that never uses the net-flux invariant — and the two agree to
  4e-15 over 131 stacks. Energy balance holds at every sheet, at the ground and at the top
  to 9e-13 W/m², and the net flux is constant with altitude to the same. For a_i = 1 it
  collapses to the textbook `T_s = (N+1)^(1/4) T_eff`, asserted at every N from 0 to 12,
  and the general law at 24 (N, a) pairs.
- **σ two ways and the Earth's 255 K.** `scipy.constants.Stefan_Boltzmann` and
  `2π⁵k⁴/15h³c²` built from CODATA h, c, k agree to 1e-15; PhET's ten-digit rounding
  (5.670374419e-8, the constant the sim carries throughout) is 3.25e-11 away, worth 2e-9 K
  on a 300 K planet. `T_eff = 254.578 K` from the 2015 IAU nominal irradiance 1361 W/m²
  and a Bond albedo of 0.30 (254.03 K at NASA's 0.306), against the conventional 288 K
  surface — 33.4 K of greenhouse warming, which one perfectly absorbing sheet would
  overshoot (302.7 K). The real atmosphere is worth Σ = 0.638, i.e. **two thirds of one
  perfect sheet, or a single pane at a = 0.779**.
- **The photon picture tied to the flux solution exactly.** The chance an infrared photon
  leaving the ground escapes to space — absorbed with probability a_i on crossing sheet i,
  then re-emitted up or down at even odds — is `F / σT_s^4`, proved three ways: as a
  Markov chain (a linear solve over the 2N up/down states), as the closed form
  `1/(1 + Σ a_i/(2−a_i))`, and by a 200 000-walk Monte Carlo. The sim and `derive.py`
  share one 32-bit linear congruential generator (`s = (1664525 s + 1013904223) mod 2^32`,
  every product below 2^53 so both languages carry it exactly), and the suite pins the
  generator's stream, the walk's crossing/absorption/up counts and the escape fraction
  **bit for bit** against the Python twin, not merely within the sampling error.
- **PhET's own convention, and what it costs.** PhET's sheet absorbs a fraction a but
  radiates a full σT⁴ in *each* direction, which is not Kirchhoff's law. It makes no
  difference whatever to the fluxes or to the surface temperature — the emitted flux per
  direction is `a(U+D)/2` either way — and changes every sheet's reported temperature by
  exactly `a^(−1/4)` (19 % at a = ½, 50 % at a = 0.2). Both are asserted, and a tick box
  shows both.
- **PhET's fit named as a fit.** The concentration screens' `a_i = 0.85 c e^(−z/8400 m)` on
  twelve sheets at `i·50000/13 m`, the four dates' c = 0.625 / 0.7147 / 0.7182 / 0.7446,
  the sun's 343.6 W/m², the albedos 0.2 / 0.225 / 0.3, the cloud's 12.5 %
  (`0.125 × 85000/18000 × 18000/85000`, exactly), the 245 K and 125 K floors, the heat
  capacities 1250/1250 and 2500/840 with the 3e-7 volume coefficient, the photon rules and
  rates, and the CO₂/CH₄/N₂O printed beside each date were all read out of the minified
  original and are quoted as PhET's. Solving them exactly shows what PhET tuned: its 1750
  surface is **296.48 K (23.3 °C), 8.48 K above the real Earth**, while the *differences*
  are good — ice age −6.29 K against about −6 K observed, 2020 +1.32 K against about
  +1.2 K. The page says so in the caption, the readout and the header.
- **An independent check that this really is PhET's model, not a look-alike:** the hottest
  state its concentration screens can reach is **309.13 K** by this solve, and PhET
  hard-codes **309** as its thermometer's `EXPECTED_MAX_TEMPERATURE`.
- The temperature is integrated with PhET's own heat capacities (the ground's response is
  exactly 32/15 K per J/m², a glass sheet's 1.5873) from PhET's own cold start (ground at
  its floor, every sheet at 0 K) in four forward-Euler sub-steps of a 1/60 s frame, inside
  the ODE's own stability bound `h < 2/(8 K σ T³)` = 0.0198 s at 520 K, which the stepper
  **clamps against**. The march is pinned frame by frame against the numpy twin at frames
  1, 6, 60, 300 and 1800.
- Verification: `selfTest` **1333 passed, 0 failed**; UI drive **174 passed, 0 failed**;
  mutation sweep **91 caught, 0 survived, 0 skipped** (85 physics + 6 UI); display-list
  capture at 1400×820, 1100×700 and 560×380, **0 layout problems** at all three, every
  view's PNG looked at. `derive.py` runs 82 of its own checks. Reference values are printed
  at `%.17g` so the JavaScript is pinned to the twin at full double precision.

### Fixed (during the build)
- **The flux meter read the steady state while the picture showed the live model.** With
  the sun switched off the exact solve is identically zero, yet the ground sits at its
  245 K floor radiating 204 W/m² and the infrared waves are still drawn — and the sensor
  read `up 0.0`. Root cause: the meter and the probe were wired to `solveClosed`'s profile
  rather than to `fluxesNow`'s. Both now read the LIVE model, as PhET's do, and the panel
  draws the exact steady profile beside them; `selfTest` asserts they coincide to
  1e-8 W/m² once settled and that they part company with the sun off.
- **Altitude zero was the bottom of the window, not the top of the ground.** Every photon
  below about 2 km was drawn inside the soil. The map now takes the ground band's height.
- **`new Array(1.5)` is a RangeError, not a rounding error.** The sheet-count slider has
  step 1, but the UI harness drives every slider to its midpoint, and 1.5 sheets took the
  ladder view down with a bare `viewLadder@` stack and no message. The count goes through
  `nSheets()`, which rounds and clamps.
- **The ladder's "stack you have loaded" read the wrong atmosphere.** `atmosphere()`
  special-cases only `view === 'layers'`, so on the ladder view it returned the twelve-sheet
  concentration stack and the absorbance slider did nothing to the readout. The ladder now
  builds the layer model's stack explicitly. A second, subtler half of the same bug: the
  marker must sit on the family the panel *draws* (PhET's F, albedo 0.2, one sun) while the
  readout carries the same sheets at the albedo and intensity actually set — two different
  questions, and the suite now asserts both and asserts they differ by 3 K at albedo 0.3.
- **`makeThermal` always started at the 245 K night floor**, so "reset all" left the layer
  model's ground 120 K above its own 125 K floor and the reset test failed. It takes the
  floor as an argument.
- **Three mutation survivors, each a real blind spot.** (1) The solar-intensity slider could
  be disconnected from the model and every layer-model assertion still passed, because they
  all recomputed F beside the model instead of reading `M.S.F` off it — the `drum_head`
  rule, again. (2) The ladder's equivalent-uniform-absorbance was never asserted off the
  built model. (3) The flux sensor's 14-px hit test could be narrowed to zero and the drag
  test still passed, because the harness clicked the sensor's *exact* pixel; it now clicks
  6 px off and asserts that 40 px away does not grab.
- **`&thinsp;` is not in the shared `ENTS` table**, so "F a/(2−a)" reached the canvas as
  `F&thinsp;a/(2−a)` in every caption. The table is extended from this sim's own part file
  (the shared helper is sha-pinned and must not change under the other builds), and the
  extension is asserted.
- **A stripped `<sup>` turns 10¹³ into 1013.** `plain()` removes tags, so `10<sup>13</sup>`
  in a canvas caption reads as one thousand and thirteen — a wrong number, not a cosmetic
  loss. Every superscript in canvas text is now a literal glyph (⁴, ¹³).
- **The energy-balance box's labels escaped it.** The "net" figure was positioned from the
  bars rather than from the box, so on a narrow window it landed in the thermometer column;
  and the box is drawn with `ctx.fillText`, which the label registry cannot see, so
  "redirected down" sat under "top of atmosphere" at every size until the box's rectangle
  was pushed into `LABELS` before anything else was labelled. The box now refuses to draw
  at all below 128 × 76 px, where it cannot hold its own labels.
- **The floating readout is invisible to the canvas.** The ladder's "Earth ≈ one sheet at
  a = 0.779" sat underneath it. `drawView` now registers the readout's rectangle
  (336 × 548, top right) in `LABELS` whenever the stage is wide enough that the layout
  keeps clear of it.
- **Two legend swatches of the same colour meaning different things.** The ice-age ring was
  drawn in the structure cyan to mark that it sits off the curve, and the legend then had
  cyan for both "with PhET's cloud" and "ice age (glaciated ground)" — the `sbs_sims`
  Known-bad in a new place. The ring is now the dates' own magenta and the gap is drawn as
  a dashed connector up to where that concentration would sit over a green meadow, with the
  connector's length asserted to be exactly what albedo 0.2 → 0.225 is worth.
- Layout: the analysis panels keep a measured 76 px below their frames for the axis title
  and the per-panel caption (the x-axis label sat inside the main caption at every size);
  per-panel captions are drawn only if they clear it; the thermometer's reading and scale
  note were overlapping its bulb; the record view's two closest dates (1750 and 1950, 0.0035
  apart in c) alternate above and below.
- **`SIZES=(${@:-a b c})` expands as ONE word in zsh when `$@` is empty**, so
  `capture_all.sh` with no arguments made a directory called `c1400x820 1100x700 560` and
  audited a file that was not there. (The same line is in `build/waves-intro/capture_all.sh`.)

### Known-bad candidates
- **Subscript LETTERS are not safe on the canvas: there is no subscript f in Unicode at
  all, and the ones that exist are not all in the rasteriser's font.** `T&#8337;&#8335;&#8335;`
  for T_eff came out as `T₆⃞⃞` — two tofu boxes — in `tools/raster.py`'s output, and
  nothing in the text audit can see it (the string is well formed and the entity decoded).
  Digit subscripts (a₁, CO₂, CH₄) and superscripts (⁴, ¹³) are fine. Write letter
  subscripts as ASCII (`T_s`, `T_eff`, `a_i`) on the canvas, and keep `<sub>` for the
  readout and the equation bar, which are HTML.
- **A quantity that has both a "now" value and a "steady" value must say which one every
  instrument reads, and the awkward case is the one where they differ.** Here the flux
  meter reads the live model and the panel draws the exact profile beside it; the test
  that matters is not the settled one (where they agree trivially) but the sun-off one,
  where the steady solve is identically zero and the model is still radiating 204 W/m².
- **PhET's grey layer is a grey absorber and a BLACK emitter**, which is not Kirchhoff's
  law. Do not "fix" it: the fluxes and the surface temperature are identical either way
  (the emitted flux per direction is a(U+D)/2 in both), and only the sheet temperatures
  differ, by exactly a^(−1/4). Both conventions are implemented and asserted; the file
  says which is which.
- **PhET's absolute temperatures are about 8.5 K high and its differences are right.**
  Anyone comparing this remake's 296.48 K at 1750 with the real 288 K should reach for the
  caption before reaching for the solver: it is PhET's concentration fit, faithfully
  solved, and the page says so in four places.

## 2026-09-21 — the four sweeps that ran during a cross-agent process kill, re-run
### Verified
- On 2026-09-18 one build agent killed stray `osascript` processes by matching
  `_mutant.js`, and at least two of them belonged to other agents' mutation
  sweeps. `tools/mutate.py` records a killed run as a **caught** mutant, so any
  sweep that was live then could have held a false kill — which is exactly how a
  real survivor hides. The four sims whose sweeps were running
  (`wave-interference`, `energy-forms-and-changes`, `quantum-measurement`,
  `quantum-coin-toss`) were therefore re-swept from their shipped files by
  `build/_tools/resweep.py`, each in its own scratch directory.
- All four reproduce what their builds reported, so no finding was hidden:
  wave-interference 81 caught / 0 survived; energy-forms-and-changes 110 / 1
  (the "no displacement cap" survivor already argued equivalent, and asserted);
  quantum-measurement 79 / 0; quantum-coin-toss 35 / 0.
- `build/BRIEF.md` now forbids pattern-killing processes: kill only PIDs you
  started yourself.

## 2026-09-21 — molecule-shapes-basics: the same repulsion engine with the lone pairs taken out, and the five shapes equal pairs make
### Added
- `molecule-shapes-basics.html` (205 KB), a remake of PhET's Molecule Shapes: Basics 1.6.19 in four
  views: *the model*, *real molecules*, *the shapes* and *the relaxation*. The credit line is in the
  header and on the page, the site nav is absolute, nothing touches the network.
- It is `molecule-shapes.html`'s engine, trimmed the way PhET trims its own Basics: no lone pairs
  anywhere — no lone-pair button, no Show Lone Pairs, no outer lone pairs, no electron-geometry
  name, no ρ slider — and PhET's five Basics molecules, the ones whose central atom has none
  (BeCl₂, BF₃, CH₄, PCl₅, SF₆). Its `assemble.py` copies the nine shared part files from
  `build/molecule-shapes/` and checks them byte for byte, so the two sims cannot drift; what differs
  is the header, a ten-line variant file (four views, PhET's Basics molecule list, no lone pairs)
  and the squeeze view, which Basics does not carry and which is simply left out of the parts list.
- *The model* is PhET's Basics Model screen: single, double and triple bonds round the central atom,
  six at most; remove the last of a kind or all of them; drag an atom round the atom and let it
  slide back; Show Bond Angles and the molecule-geometry name. *Real molecules* is its second
  screen, with the measured geometry of the five. *The shapes* lays the five ideal geometries side
  by side with their angles, and clicking one builds it. *The relaxation* runs plain gradient
  descent from a random start, which for equal pairs always ends in the ideal shape.
- What is exact is the whole content of this sim: linear 180°, trigonal planar 120°, tetrahedral
  arccos(−1/3) = 109.4712206…°, bipyramidal 90/120/180, octahedral 90/180, and the energies 1/4, 1,
  9/4, 17/4, 27/4 of two to six equal pairs. `derive.py` (the twin the two sims share) lands 100 of
  100 seeded random starts of five and of six pairs on the ideal shape; the JS reproduces each to
  1e-9° from the same seeds.
- PhET's data, verbatim: the five molecules' geometry and bond lengths, the tetrahedron's elevation
  −19.471220333° (so its CH₄ is 109.47122033°, not quite ideal), the bond orders, six pairs at most
  and the arc-brightness thresholds; the AXE names are PhET's rules.
- Verification: `selfTest` 1798 assertions green under osascript (the same suite as the full sim,
  its lone-pair sections skipped where Basics cannot reach them and replaced by the Basics
  behaviour: a lone pair is refused outright, six bonds go octahedral); the UI drive 117; 59
  mutants, all killed; 17 captured configurations audited (0 layout problems) and every PNG looked
  at.

### Fixed (during the build)
- **A shared suite that assumes the richer variant fails the trimmed one.** The first Basics run
  had ten failures, all from the model-view block adding a lone pair and then asserting on it. The
  suite now branches once on the variant: in Basics a lone pair is *refused* (which is itself the
  assertion PhET's Basics deserves) and the six-pair molecule is an octahedron rather than a square
  pyramid, with the expected angles read off the shared engine's equilibrium either way.
- **An assertion that hard-codes a count from the other variant.** "The last single bond added
  went" also checked that two singles remained — true for the full sim's mixture, wrong for Basics'
  four. It now counts the singles before the removal and expects one fewer.
- **One row of cells inherits five rows' height.** The AXE table's cell height came from
  `(box height)/rows`, so the Basics table drew five glyphs in cells twice as tall as they were
  wide. The height is capped at 1.45 × the cell width and the row is centred.
- **A trimmed sim is where an untested constant shows up.** Mutating the ideal angle AX₂E₂ is
  compared against (the tetrahedral angle → 120°) survived Basics' sweep and was caught in the full
  sim only through a layout failure in the squeeze view, which Basics does not carry. Both suites
  now pin each named angle's ideal to the angle its two slots actually make — the shared engine got
  a better test because the trimmed variant could not hide behind a drawing.
- **The same sweep found the button-repaint gap in both sims:** dropping `refresh()` from the panel
  buttons survived, because the adding buttons start the relaxation and the loop repaints anyway.
  `reset view` starts nothing; both drives now click it from a proven-idle baseline.

### Known-bad candidates
- **A variant is not a copy.** Basics shares nine part files with `molecule-shapes` and copies them
  at build time with a byte-for-byte check; editing them in the Basics directory is silently undone
  by the next build. Edit them in `build/molecule-shapes/` and rebuild both.
- **A trimmed sim still ships the engine's untrimmed tests, and that is deliberate.** The Basics
  suite still exercises lone-pair classes through the shared engine (they are reachable in code,
  not through its UI), which is what keeps the two sims' physics identical. A mutant in lone-pair
  code is therefore caught by both sweeps; a mutant in a control Basics does not build (its ρ
  slider) can only survive, and is excluded from its mutant list rather than left to look like a
  finding.

## 2026-09-21 — molecule-shapes: PhET's two screens on an explicit repulsion energy, the AXE table as its global minima, and the one measured angle it gets backwards
### Added
- `molecule-shapes.html` (213 KB), a remake of PhET's Molecule Shapes 1.6.19 in five views: *the
  model*, *real molecules*, *the AXE table*, *the squeeze* and *the relaxation*. The credit line is
  in the header and on the page, the site nav is absolute, nothing touches the network.
- *The model* is PhET's Model screen: add single, double and triple bonds and lone pairs round the
  central atom (six pairs at most, PhET's `maxConnections`), remove the last of a kind or all of
  them, drag any pair round the atom and let it slide back, turn the molecule, wheel to zoom;
  Show Lone Pairs, Show Bond Angles, and the molecule-geometry and electron-geometry names, in
  PhET's wording. It opens on PhET's own two single bonds along (8, 0, 3) and (2, 8, −5).
- *Real molecules* is PhET's second screen: its thirteen molecules with their measured geometry,
  the Real / Model switch (animated between the two), Show Outer Lone Pairs, the same options and
  names. Every angle and length shown is computed from PhET's stored numbers.
- THE MODEL. Every electron pair is a point on a sphere — a bond on the unit sphere, a lone pair on
  one of radius ρ (PhET's value 0.7: its lone pairs sit at 7 against 10 for its bonds) — and every
  pair repels every other with energy 1/d², d the 3-D separation. The shape drawn is the
  arrangement of least total energy. Single, double and triple bonds act alike, as PhET's notes say
  its own do. The ρ slider runs from PhET's 0.7 to 1, where a lone pair is a bond and every angle
  is exactly ideal.
- **No attractor.** PhET's model notes describe a Coulomb-like repulsion *steered* toward ideal
  slots, because plain Coulomb repulsion has locally-stable arrangements that are not the VSEPR
  one. `derive.py` audits this file's law instead: for every lone-pair class and every ρ from 0.60
  to 1.00 it relaxes every assignment of the pairs to the slots plus sixteen random starts, checks
  the shape and takes the Hessian. The VSEPR arrangement (lone pairs equatorial in the bipyramid,
  trans in the octahedron) is the global minimum, keeps its shape and is a true local minimum for
  **ρ ≥ 0.64** — the slider starts at 0.70, with room to spare. The same audit rejects the
  alternatives: with Coulomb's 1/d at ρ = 0.7, ClF₃ comes out trigonal planar (7.36173 against the
  T-shape's 7.36450), and charge-weighted lone pairs on one sphere make XeF₄ *cis* at every
  exponent tried (1, 2 and 6).
- WHAT IS EXACT. The ideal geometries (linear 180°, trigonal planar 120°, tetrahedral
  arccos(−1/3) = 109.4712206…°, bipyramidal 90/120/180, octahedral 90/180) and the equal-pair
  energies 1/4, 1, 9/4, 17/4, 27/4; plain descent from seeded random starts reaches each of them to
  1e-9° and the closed-form energy to 1e-12. Every class at ρ = 0.70, 0.85 and 1.00 is pinned to
  the Python twin (angles to 1e-8°, energies to 1e-11), which is itself checked against scipy's
  BFGS. Horn's quaternion fit is checked against scipy's `Rotation.align_vectors` (1e-12 on a
  known rotation, 1e-10 on a noisy one). The lone-pair directions asserted: AX₂E below 120°, AX₂E₂
  and AX₃E below 109.47°, the seesaw's axial pair below 180°, the T-shape's and the square
  pyramid's arms below 90°, while AX₂E₃, AX₄E₂ and AX₂E₄ stay exactly 180°, 90°, 180° by symmetry.
  The departure from ideal is linear in 1 − ρ (ratios 1.96–2.00 between ρ = 0.98 and 0.99).
- WHERE IT FAILS, ON THE CANVAS. Of the seven measured lone-pair angles in PhET's table the model
  bends six the right way and **SF₄'s equatorial F–S–F the wrong way**: point pairs open it to
  121.2° where the molecule closes it to 101.6°. *The squeeze* view plots all seven against ρ and
  says so in words; three (H₂O 104.5°, ClF₃ 87.5°, BrF₅ 84.8°) need more squeeze than ρ = 0.70
  gives, and three are matched at a fitted ρ (SO₂ 0.954, NH₃ 0.833, SF₄'s axial pair 0.792, each
  found by bisection on the relaxation itself and pinned against `brentq`).
- *The AXE table* draws all fifteen classes of steric number 2 to 6 relaxed at the current ρ, each
  turned lone-pairs-up; clicking one builds it in the model view. *The relaxation* runs plain
  gradient descent from a seeded random start with no steering, and plots how far the energy stands
  above the VSEPR minimum against the other arrangements' energies: it is where PhET's warning about
  locally-stable configurations becomes visible, and `derive.py` counts how often it bites — 65 of
  100 random AX₄E₂ starts stall with the lone pairs cis, 66 of 100 AX₂E₄ starts end bent, while
  every one of 100 starts of five or six equal pairs reaches the ideal shape.
- PhET's data, verbatim: the thirteen molecules' bond angles as the numbers its constructor is
  given (104.5° for H₂O, 119° for SO₂, 87.5° for ClF₃, 84.8° for BrF₅, 173.1° and 101.6° for SF₄,
  NH₃'s polar angle 1.202623030417028 rad = 107.8°, the tetrahedron's elevation −19.471220333°,
  which leaves CH₄ at 109.47122033° and 109.47122094°, not quite ideal), the bond lengths in
  ångström, the lone-pair counts, the bond orders, the 7-to-10 lone-pair radius, six pairs at most,
  the lone-pair slot order, the arc-brightness thresholds and all 22 AXE names.
- Verification: `selfTest` 1937 assertions green under osascript; the UI drive 170; 61 mutants, all
  killed; 23 captured configurations audited (0 layout problems) and every PNG looked at.

### Fixed (during the build)
- **A bond pointing straight at the camera hides behind the central atom, and every class loaded
  from the table did it.** Water's second bond and the seesaw's equatorial bond were invisible at
  the default camera: `liveLoad` dropped a class in the raw slot frame, whose axes happen to line
  up with the default line of sight. Root cause: the same one the Known-bad list records for
  `bloch_sphere` — a default camera pointed along the thing the view exists to show. `displayFrame`
  now puts the lone pairs up and then picks, from 72 turns about the vertical, the one that keeps
  *every* pair furthest from the default line of sight; the reference is the default camera, not
  the current one, so the shapes do not re-orient while being turned. `selfTest` asserts no pair of
  any class comes within 72° of that line.
- **`acos` is ill-conditioned at 0° and 180°: one ulp of the dot product is 1.2e-6°.** Two pins
  failed at exactly that value (a two-pair random start and BrF₅'s lone pair, both 180° angles).
  Both the JS and the Python twin now take angles as `atan2(|a×b|, a·b)`, which is accurate
  everywhere; the pins hold at 1e-8°.
- **A display merge tolerance swallowed CH₄'s two distinct angles.** PhET's rounded tetrahedral
  elevation leaves CH₄ with 109.47122033° and 109.47122094°, 6e-7° apart; `distinctAngles` merged
  anything within 1e-6° and the test compared 1 value against the twin's 2. The tolerance is now a
  parameter: 1e-6° for the readout, 1e-10° for the pins.
- **Two panels do not fit a 560×380 stage, and the lower axis ran into the caption.** The squeeze
  view now reserves 44 px below the lower panel and falls back to its one primary panel (the
  curves) with its own caption when the stage is short — the Known-bad remedy for collapsing
  two-column layouts. Its curve labels moved into a column clear of the tick labels, and the
  rotated y-axis title came off that panel.
- **`dirty = true` before `refresh()` was dead code in eight handlers.** Mutation testing killed a
  mutant that removed it from the tab click and nothing else changed: `refresh()` draws
  unconditionally. The flag now survives only where it is load-bearing — the pointer and the wheel,
  which do not refresh — and the UI drive pumps the pointer-down and the pointer-move through
  separate frames, because pointer-up calls `refresh()` and masked the move's flag.
- **A button whose action starts no motion must repaint on its own, and only one does.** The
  sweep's last survivor dropped `refresh()` from every panel button and lived: the adding buttons
  set the flow going, so the loop redrew anyway. `reset view` does not, and its click was
  therefore invisible until the next interaction. The drive now clicks it from a proven-idle
  baseline after turning the camera and asserts ops came out of the click itself.
- **The ideal angle each class is compared against was data no test pinned.** Mutating AX₂E₂'s
  ideal from the tetrahedral angle to 120° survived the Basics sweep outright (only the full sim's
  squeeze view draws it, and there it showed up as a layout failure rather than a wrong number).
  Both suites now assert that each named angle's ideal IS the angle its two slots make.
- **Five more test gaps the sweep found, each closed:** a display-frame assertion that took a minimum
  where it meant a maximum (vacuous); the isomer ladder's *length* unpinned, which matters only at
  ρ = 0.99 where the gaps fall to 1e-4 (AX₃E₂ and AX₂E₃ have three distinct minima there and two at
  0.70 — pinned per ρ now); PhET's bond orders and outer-lone-pair counts unpinned as data, and a
  double bond's two sticks unpinned in the drawing; the ρ a drag sets probed only at values that
  are already on the slider's 0.01 step; and the display flow's repulsion term, now pinned by the
  property it actually has (it changes the path the pairs take by more than a degree, and not where
  they end).
- The camera fitter used the near-point approximation `fR/(D − R)`, which frames a ball at 0.82 of
  the size it claims (Known-bad, `polyhedra`); it is the exact tangent cone `fR/√(D² − R²)`, and
  the claimed fraction is asserted.

### Known-bad candidates
- **A points-on-a-sphere model of VSEPR gets SF₄'s equatorial angle backwards, whatever the law.**
  Charge weights (exponents 1, 3 and 6) and lone-pair radii (exponents 0.5 to 4, ρ 0.6 to 0.9) were
  all tried in the build: every one of them opens the seesaw's equatorial F–S–F past 120° where the
  molecule closes it to 101.6°. The equatorial lone pair pushes the two axial bonds (90° away) much
  harder than the two equatorial ones (120° away); the axial bonds bend toward the equatorial pair
  and lever it open. Do not "fix" it by tuning ρ — say it on the canvas, which this file does.
- **Coulomb's 1/d is the wrong exponent for a two-sphere VSEPR model, and the failure is a shape,
  not an error term.** At PhET's ρ = 0.7 a 1/d law makes ClF₃ trigonal planar (the lone pairs go
  axial); 1/d² ranks every class correctly for ρ ≥ 0.64. Any change to the exponent or to the ρ
  range must re-run `derive.py`'s audit, which is what pins the claim.
- **Product charge weights cannot separate cis from trans.** With w_L = q on one sphere, the
  unrelaxed cis–trans gap of AX₄E₂ is (f(90°) − f(180°))(q − 1)² — second order in q − 1, and the
  cis arrangement's relaxation gain beats it at every exponent tried. If lone pairs are ever
  modelled as stronger charges rather than closer ones, XeF₄ will come out cis.
- **A relaxation from a random start is not a model of VSEPR.** Plain descent stalls in a higher
  local minimum for most AX₄E₂ and AX₂E₄ starts. The model view avoids it by starting from the
  VSEPR slots and steering; the relaxation view exists to show the trap rather than hide it.

## 2026-09-18 — gas-properties: PhET's four screens on an exact event-driven hard-disk engine, and where the gauge's pressure and the Maxwell–Boltzmann law come from
### Added
- `gas-properties.html` (216 KB), a remake of PhET's Gas Properties 1.1.10 in six views: *the gas
  law*, *the moving wall*, *the energy*, *diffusion*, *the pressure* and *equilibrium*. The credit
  line is in the header and on the page, the site nav is absolute, and nothing touches the network.
- *The gas law* is PhET's Ideal screen, with every control PhET's has:
  - the pump, heavy or light, where a full stroke adds 50, as in PhET;
  - the particle counts (0–1000 each);
  - the heater, which springs back to zero when released;
  - the left-wall grip: the sim pauses while it is dragged and the disks are spread over the new
    width;
  - the lid knob, PhET's blow-off rule (above 20,000 kPa unless the gap is ≥ 1500 pm), return lid
    and erase;
  - Hold Constant (Nothing, V, T, P↕V, P↕T), with PhET's enabling rules and all six of its Oops
    cases;
  - the thermometer (K/°C), the gauge (atm/kPa, with PhET's 0.75-ps refresh and optional noise
    law), the stopwatch, the collision counter (5/10/20 ps) and the width ruler.

  House additions: P and T traces over time, and the readout prints the invariant the chosen hold
  keeps (P/T, PV, V/T, NT).
- *The moving wall* is PhET's Explore screen. The wall does work elastically (v′ = 2u − v) at no
  more than a speed limit (PhET's 800 m/s by default, adjustable from 10 to 800). The view shows the
  wall's velocity arrow, T against the width set against the hard-disk adiabat and the point law,
  T over the adiabat (the irreversibility), and the wall speed as a Mach number.
- *The energy* is PhET's Energy screen: the 1-ps histograms (19 bins of 170 m/s and of 1.33 zJ)
  for heavy, light and all particles, the zoom levels, the average speeds, the injection
  temperature (match the container, or set 50–1000 K) and the collisions switch. The exact 2-D
  Maxwell–Boltzmann counts are drawn over the bars.
- *Diffusion* is PhET's Diffusion screen:
  - two species in a 16 × 8.75 nm box, each with its number, mass, radius and starting
    temperature on PhET's grids;
  - PhET's quirks kept: a new mass or temperature resets every particle of that species to
    √(3kT/m), and putting the divider back restarts both sides;
  - the centres of mass, the 300-frame flow rates, the scale, and normal or slow time;
  - a house trace of the centres of mass.
- *The pressure* (house view) sets the momentum the walls actually receive against PhET's gauge.
  It breaks the ratio into (3/2) · W/(W−2r) · Z and plots Z against the area fraction beside the
  exact hard-disk B₂ and B₃.
- *Equilibrium* (house view) starts from one speed, from hot heavy and cold light disks, or from
  the pump. It shows the log energy histogram against e^(−E/kT₂), Boltzmann's H with its sampling
  floor, and equipartition.
- The gas engine is its own part, `build/gas-properties/p2_engine.js`, documented in `ENGINE.md`
  (API and invariants) for the `gases-intro` and `diffusion` jobs. It uses PhET's units (pm, ps,
  AMU) and PhET's frame (origin at the box's bottom-right corner).
- **Exact:**
  - Every collision inside a substep happens at its exact contact time, in time order. For two
    disks that is the earlier root of |dp + t dv|² = σ², in the cancellation-free form
    c/(−b + √(b² − ac)); for a moving wall it is linear. `derive.py` checks both in exact rational
    arithmetic.
  - Over 5000 random collisions with masses from 1 to 40, momentum is conserved to 3.4e-16 and
    energy to 1.5e-15.
  - Four brute-force event-driven runs in `derive.py` (O(N²), no grid, no substeps) are matched
    to 7e-8, 1.6e-7, 7e-7 and 7e-10 pm, with identical event counts. That includes a moving wall
    whose work, 23,040,000 AMU pm²/ps², matches to the last digit. A fifth run (R5) puts three
    stale predictions inside one substep: a pair event stale in its partner, one stale in its
    owner, and a wall event whose disk was struck first. It matches to 2e-11 pm, and the engine
    reports exactly three skipped events.
  - The energy ledger closes to 1e-15. The virial ledger, Δ(Σ m r·v) = ∫2KE dt + Σ r·J (walls)
    + Σ σ|J| (pairs) + heater + escapes, closes to about 1e-15 of its terms.
  - The injection is bit-exact against a mulberry32 and Box–Muller twin.
  - PhET's constants are pinned absolutely.
- **Statistics, with tolerances from the exact sampling law** (a closed box of hard disks has no
  potential energy, so the energy shares are Dirichlet(1,…,1), whatever the masses):
  - ⟨E²⟩/⟨E⟩² = 1.958 against 2N/(N+1) = 1.967 ± 0.038;
  - the mean √share is within 0.4 sd;
  - χ² = 13.0 against its exact-ensemble 99.99 % point of 35.8;
  - equipartition from a 6:1 split: D = 0.008 ± 0.040;
  - Z − 1 = 0.1102 against B₂+B₃ theory 0.11024 (B₂ alone, 0.1018, is excluded);
  - wall hits carry 1.481 × the mean energy against 2-D effusion's 3/2;
  - a slow push (20 m/s) ends at T·w/T₀w₀ = 1.0694 against the hard-disk adiabat's 1.0691
    (the point law gives 1.0111).
- **Verification:**
  - selfTest: 834 passed, 0 failed under osascript, in 13 s.
  - UI drive: 165 passed, 0 failed. Each of the three canvas drags moves the drawing through
    the frame loop from a proven-idle baseline.
  - Mutation sweep, on a copy inside `_out/sweep/`: 80 mutants (69 physics, 11 UI), 78 caught.
    The two survivors are equivalent and say so in their labels: `b >= 0 → b > 0` in the contact
    test (b = 0 leaves d = −ac ≤ 0, so the root is `Infinity` or `NaN` and no event is pushed
    either way), and halving the substep count (a speed knob: the event order inside a substep is
    exact for any h, and the grid's cells grow with h).
  - Audit: 0 layout problems at 1400×820, 1100×700 and 560×380.
  - Every view's PNG was looked at.
- **Sources:**
  - PhET's constants, read from `docs/phets/gas-properties_en.html`: BOLTZMANN 8316,
    KG_PER_AMU 1.66e-27, ATM_PER_KPA 0.00986923, the box 5–15 × 8.75 × 4 nm, the lid insets, the
    limits, the time transform, the histogram bins and the diffusion grids.
  - PhET's `doc/model.md` (raw.githubusercontent.com/phetsims/gas-properties/main/doc/model.md), fetched with curl on 2026-09-18 and followed; not copied into the build.
  - CODATA k_B/u, for the comparison only.
### Fixed (during the build)
- **The suite hung, drawing a flat curve.** The two species' mean-energy ratios were both 1 to the
  last bit, so the auto-ranged axis spanned about 2e-16 of its endpoints. The shared `ticksFor`
  steps `t += step`, and at that span t never advances, so the loop spun for ever. `niceRange()`
  now widens any sub-rounding span before ticks are asked for, and selfTest draws a series flat to
  the last bit.
- **Every plot threw.** `plotSeries` was defined without the short-title parameter its callers
  passed, so the series array landed in the options slot.
- **The wall-pressure plot showed 1 ps of a 5-ps run.** Passing `x0` skipped measuring the data,
  and the far end fell back to 1.
- **"Push slowly and T·V = const" was the point-particle law, and it was false for these disks.**
  A 20-m/s push of 100 heavy disks measured 1.07, not 1.011. The cause is finite size: Z > 1 and
  the excluded strip W − 2r. The quasi-static hard-disk adiabat, ln T₁/T₀ = ∫Z dW/(W − 2r), gives
  1.0691, which the engine reproduces, and the page now claims that. The same probe showed PhET's
  800 m/s limit is Mach 1.55 in the heavy gas, a shock that heats the gas to about 3× the adiabat.
- **Evaporation was predicted at 3/2 kT₂ and measured 1.95.** 3/2 is effusion, which needs a hole
  much smaller than the mean free path. The lid's widest gap is about twenty mean free paths, so
  the gas leaves as a jet carrying its enthalpy, 2kT₂. The test now brackets the escapees between
  the two limits, and pins the exact 3/2 on the wall hits of a closed box.
- **An Oops cleared itself.** Erasing while T was held raised PhET's Oops, and the button's
  after-action refresh cleared it the same instant. Controls now clear the *previous* Oops before
  they act.
- **The pressure view's Z marker used the wall-side Z.** That estimate carries the finite-run
  boundary term Δ(Σ m r·v)/2Et, about ±0.2 at 5 ps. The marker now uses the collision-side Z,
  which converges far faster, and a collisions-off gas sits on Z = 1.
- **A guessed 25 % tolerance on the collisions-off pressure** was replaced by a closed form. With
  collisions off, every bounce is periodic, so each wall's momentum is Σ 2m|vₓ| × (a closed-form
  hit count), and it matches to 2.6e-16.
- **At 560×380 the long caption squeezed the box** until the thermometer and gauge hung off the
  canvas and the dial covered the thermometer's label. The audit could not see this, because the
  covered text was still on the canvas. A scene with gauges now needs 330 px above its caption or
  takes the short one, and the instruments keep 170 px.
- **A narrow stage printed a caption describing plots it had dropped.** There is now a third,
  no-plots caption for that case.
- **The captions ran into the page's `#hint` line.** The hint is HTML (`bottom: 11px`, 11px
  type) over the canvas's bottom-left corner, so neither the capture nor the audit can see it,
  and every caption ended 23 px above the canvas bottom — inside it. Captions now reserve
  `HINT_H = 18` px (the fix the wave-on-a-string build found), and the layout sweep asserts that
  no canvas text reaches within 27 px of the bottom in the left 340 px, at four sizes.
- **The gas law's lone trace marker contradicted the readout.** The trace is seeded at t = 0, and
  an edit made while paused (a resize, the pump, erase) moves the state it describes: after
  halving the width the marker still read 11.6 atm beside a readout of 23.6. The seed is now
  re-taken while the trace is a single point and no time has passed.
- **A dashed reference line struck through an empty plot's note.** The diffusion view's
  centre-of-mass plot draws its zero line through the middle, where "run the clock to trace the
  centres of mass" sits. The audit could not see it: both were on the canvas. Notes are now
  drawn on a patch of the canvas ground.
- **Smaller defects in the pictures:**
  - the default gas-law view's plot row was blank at t = 0;
  - the centre-of-mass markers touched the plot title;
  - a narrow heater's label overflowed it;
  - the Energy screen's default zoom was 0–200, where PhET's is 0–100;
  - the gas law's "PV/NkT" row was 1 by construction, and is replaced by the hold's own invariant.
- **The first suite took 87 s.** Every configuration was rebuilt once per canvas size, and one of
  them held 1800 disks injected at a point. Configurations are now built once per size sweep, and
  sections throw at their boundary after a failure, with the 12-s statistics last, so a caught
  mutant costs seconds.
- **Defects in `derive.py`:**
  - numpy 2's repr leaked `np.float64(...)` into the generated JS;
  - the Dirichlet moments from gammaln were good only to 3e-14, and are now exact rationals;
  - the first moving-wall reference never hit the wall, so it pinned no work.
- **The first full mutation sweep left seven survivors.** Two are equivalent (see Verification).
  The other five were holes in the tests:
  - *Deleting the stamp check survived.* No test put a stale prediction inside a substep. Stale
    events only arise when a disk is struck by a third party before its predicted event, and
    none of the parity runs did that. R5 now does, in three ways.
  - *The lid's whole-disk escape rule survived being cut to the centre.* The rule was written
    twice, once in the opening prediction and once in the re-prediction, and every test reached
    only the first copy. The two routines are now one, `gasPredict(…, half)`, and a disk whose
    centre is in the gap but whose edge is under the lid must bounce.
  - *Shrinking the grid cell from σ + 2v_b·h to σ + 0.2v_b·h survived.* No test had fast pairs
    across a cell boundary. Now 20 head-on pairs at 3000 m/s, stepped across the cells, must
    all bounce in one frame.
  - *The overlap test survived c < −1 in place of c < 0.* Only deep overlaps were tested. A
    hair's overlap (c = −0.5 pm²) is now asserted.
  - *Deleting the Ideal wall's pause survived.* The pause is guarded twice, in the frame loop
    and in the model step, so each copy covered for the other. Each now has its own test: a
    grip held still costs no frames, and the step key does not step.
- **A mutant added after that sweep, re-predicting pairs only with higher indices, survived
  too.** No test checked that the disks never overlap. When a collision is missed, the two disks
  slide into each other and PhET's overlap rule lets them pass through. The energy and the
  statistics do not notice. selfTest now checks every pair of 400 disks (area fraction 0.22)
  every frame for 4 ps, through 1828 collisions. The closest approach is 1.25e-3 pm outside
  contact, and the mutant makes 602 overlaps.
### Known-bad candidates
- **The shared `ticksFor` spins for ever when an axis span is below the rounding of its
  endpoints.** `t += step` does not advance. Guard every auto-ranged axis, as `niceRange()` in
  `build/gas-properties/p4_views.js` does, or carry the guard into the shared layer.
- **PhET's T = (2/3)⟨KE⟩/k in a 2-D box means the walls feel 3/2 of the gauge,** and more through
  W/(W − 2r) and Z. Never compare a measured wall pressure with NkT/V without those factors.
- **PhET's moving wall (v′ = u − v) is not elastic** and does half the work. Its 800 m/s limit is
  supersonic in the heavy gas at 300 K, so a quasi-static (adiabatic) push needs about 20 m/s.
- **The energy per escaping particle depends on the Knudsen number:** 3/2 kT₂ for a hole much
  smaller than the mean free path (effusion), 2kT₂ for a jet. Say which regime a lid is in.
- **A time-averaged wall pressure carries a 1/t boundary term** (Δ(Σ m r·v)/2Et). The
  collisional virial converges far faster. Use it for a live estimate.
- **Hard disks are stiffer than points, even dilute:** 6.9 % above T·w = const (1.1 % from the excluded strip W − 2r, the rest from Z) at an area
  fraction of 0.05–0.07.
- **In an event-driven engine with a grid built at the substep's start, search neighbours from the
  cell a particle was registered in, not the one it has moved to.** Two disks that can still touch
  started within one cell width of each other.
- **A rule written twice hides from a mutation sweep.** The event engine's escape rule lived in
  both its opening prediction and its re-prediction. The tests reached one copy, so a mutant of
  the other survived. Keep one routine per rule, or test every copy.
- **PhET's overlap rule hides a missed collision.** The two disks pass through each other, energy
  is conserved, and the statistics barely move. Assert that disks started apart never overlap.
- **An event-driven engine needs a stale-event test.** Parity runs can pass with the stamp check
  deleted, because a stale event needs a third party to strike a disk before its predicted
  event. R5 in `build/gas-properties/derive.py` is a template.
- **Kill only your own processes, by full path.** A `ps | grep _mutant.js | kill` during this
  build killed osascript processes of other agents' concurrent mutation sweeps; every agent's
  scratch file has that name. Their `mutate.py` then logs the killed mutant as "caught".

## 2026-09-21 — quantum-coin-toss: PhET's Coins screen on the quantum-measurement engine, and the sideways measurement that tells a hidden face from a superposition
### Added
- `quantum-coin-toss.html` (158 KB), a remake of PhET's Quantum Coin Toss 1.0.4 (the Coins screen of Quantum
  Measurement) in four views: *the classical coin*, *the quantum coin*, *the binomial*, *the hidden difference*.
  Credit line in the header and on the page; site nav absolute; no network. It runs on the engine of
  `quantum-measurement.html`: its assembler reads `p2_engine.js`, `p4_coins.js`, `p5_binom.js` and the shared test
  library from `build/quantum-measurement/`, so the two files cannot drift. PhET's 1.0.4 build carries the same
  coin model as Quantum Measurement's 1.0.5 (checked in the minified source):
  - N ∈ {10, 100, 10⁴};
  - the 1-s flip;
  - bias steps of 0.05;
  - the draw `nextDouble() < bias ? heads : tails`;
  - the start-hidden preference.
- *The classical coin* and *the quantum coin* are PhET's two scenes, one tab each with its own state:
  - prepare (heads or tails; ↑, ↓ or a superposition with P(↑) = |α|²) and send to measure;
  - flip, hide and reveal, or reprepare and observe, for one coin or 10, 100 or 10 000;
  - the counts against Np ± √(Np(1−p)), and the single coin's last 48 outcomes;
  - click a coin on the canvas to reveal or observe it.
- *The binomial* is the quantum-measurement view: seeded sets against the exact pmf, the spread √(p(1−p)/N)
  log–log, and one long run inside its ±2σ funnel.
- *The hidden difference* answers what PhET's screen asserts but, measuring face-on only, cannot show.
  - Face-on, a hidden classical face and a superposition give identical odds, P(up) = p.
  - Sideways, along x, the hidden face (a mixture, diag(p, 1−p)) gives ½. The superposition (off-diagonal
    √(p(1−p))) gives (1 + 2√(p(1−p)))/2, which is 1 at p = ½.
  - Seeded runs go through the engine's own draws; the two states are drawn on the Bloch disc (the mixture
    inside, the superposition on the edge); P(+x) is plotted against p.
- **Exact:**
  - the Born rule;
  - the binomial (Stirling lnFact against math.lgamma, the pmf against scipy);
  - both density matrices, their P(z), P(+x), purity and coherence at seven biases against numpy;
  - pureBloch(p) = ⟨ψ|σ|ψ⟩ over 21 biases.

  Every seeded count is pinned bit for bit to the Python twins (`build/quantum-measurement/derive.py` for the
  engine, `build/quantum-coin-toss/derive.py` for this view, which imports the first's PRNG). Each count is also
  held within 4σ of its law.
- **Verification:**
  - selfTest 988 checks, 0 failed under osascript;
  - UI drive 91 checks, 0 failed. Every click and flip goes through the frame loop from a proven-idle baseline, and every reset
    is checked against a sentinel;
  - mutation sweep 35 of 35 caught (28 physics, 7 UI), no survivors, on a copy in `build/quantum-coin-toss/_out/`;
  - audit: 0 layout problems at 1400×820 (no advisories) and 820×520 (under-readout advisories only: at that
    width the house's floating readout covers the top right, as in every sibling sim);
  - every captured view (15 + 4 narrow) was looked at;
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET:**
  - the two scenes are two tabs rather than a switch;
  - the coins are not animated flying into the test boxes;
  - the sideways measurement (the fourth view) is not in PhET's screen;
  - no sounds and no screen-reader descriptions.
### Fixed (during the build)
- **A mutant of the quantum coin's collapse survived this sim's sweep.** Root cause: the assertion that observing a
  superposition leaves the coin in the observed basis state lived in `quantum-measurement`'s own suite, so the
  shared engine went into this build with that contract unguarded. It now lives in the shared `engineTests`, which
  both suites run.
- **`COINS.classical.p === 0.35` failed** after seven bias steps. Root cause: 7 × 0.05 = 0.35000000000000003.
  `snapBias` rounds to k/20, and selfTest pins the exact value in both sims.
- **The preference check passed while the control was visible.** Root cause: it read the checkbox's label rather
  than the row that is hidden, so "hidden" was never actually tested. It now reads the row.
- **A flip animation test compared a repaint against a possibly EMPTY frame** (the same weak pattern the parent
  sim's sweep exposed): `animatesU()` drains the dirty repaint and requires two consecutive drawn, different
  frames.
- **The "classical: mixed" label sat on the Bloch disc's x axis** at p = ½. Root cause: the mixture is always on
  the z axis, r = (0, 0, 2p − 1), so at p = ½ it is at the origin, where the label's own height is the axis.
  Lifted 10 px off it.
- Shared-engine fixes made in `quantum-measurement` and inherited here, each with its own regression test: the
  negative zero from `toFixed` (`fmt0`, plus a layout rule), value labels landing on the law's mark (`barValY`,
  plus a layout rule), the empty-box note landing on a mark (`freeY`), legends naming what is not drawn, a legend
  silently lost when an entry grows, and captions naming panels the layout skips (`layoutNamed`). The coins' short
  caption named the histogram's orange marks at 560 × 380, where the histogram is not drawn; the binomial's named
  its long-run panel at the same size.
### Known-bad candidates
- An engine contract exercised by only one sim's suite: the other sim's mutation sweep finds it unprotected. Put
  shared-engine assertions in the shared test library.
- k × 0.05 is not exact (7 × 0.05 = 0.35000000000000003): snap to k/20.
- A UI check that reads a control's label instead of the row that is hidden tests nothing.
- "Compare two frames and assert they differ" passes when the second frame is empty.
- A label placed at a point that can be the origin of its own axes (the mixture at p = ½).
- `toFixed` keeps the sign of a negative zero; a value label above its bar alone lands on the law's mark; a legend
  or a caption written as a constant beside a conditional drawing (all shared with `quantum-measurement`).

## 2026-09-21 — quantum-measurement: coins, photons, spins and the Bloch sphere on one bit-exact engine, the Born rule both ways, and the binomial
### Added
- `quantum-measurement.html` (254 KB), a remake of PhET's Quantum Measurement 1.0.5 in six views:
  *the coins*, *the photons*, *the spins*, *the Bloch sphere*, *the Born rule*, *the binomial*. Credit line in the
  header and on the page; site nav absolute; no network. Its engine is shared with `quantum-coin-toss.html`
  (`build/quantum-coin-toss/assemble.py` reads `p2_engine.js`, `p4_coins.js`, `p5_binom.js` and the test library
  from `build/quantum-measurement/`), so the two files cannot drift.
- **PhET's four screens, with PhET's values read from the build** (every one marked "PhET's value" in the code):
  - *The coins*: a classical coin and a quantum "coin" in separate scenes. Prepare heads or tails, or up, down or a
    superposition, with the bias in steps of 0.05, then send the coin to be measured. The classical coin flips
    (1 s), hides and reveals; the quantum coin is reprepared and observed. This works for one coin at a time or
    for 10, 100 or 10 000 identical coins, and PhET's "classical coins start hidden" preference is included. The
    seeded draw is PhET's rule, u < p for heads or up, one coin at a time. The set's counts are drawn against
    Np ± √(Np(1−p)), and the single coin's last 48 outcomes are shown with their running fraction.
  - *The photons*: PhET's bench at true aspect in its own model units. The laser sits at −0.15 and sends a
    0.04-wide beam at 0.3 units a second into the 0.07 splitter cube, whose diagonal is y = x. The mirror is
    x + y = 0.11, and the detector lines are y = 0.2 and −0.09.
    - Photons arrive one at a time (click the laser) or as a beam of up to 200 a second.
    - Presets are V, H, 45° and unpolarized, plus a custom angle (0–90° in 5° steps) that can be dragged on
      the polarization dial.
    - Behaviour is classical (the path is chosen at the splitter) or quantum (the photon rides both paths
      until the detectors).
    - Counts are capped at 999; the rates use PhET's 1-s average in 0.5-s samples; slow motion is ×0.4 and
      the step is 2/60 s.
    - The display shows the average polarization (N_V − N_H)/N against −cos 2θ, and Malus's law with the
      measured fraction ±1σ.
  - *The spins*: PhET's six Stern–Gerlach experiments and its custom one. Single particles (click the source; a
    dial shows the spin at each stage) or a continuous beam (5 × amount per 60-Hz frame), with blockers on
    magnet 1's exits and each magnet's up percentage against its projection. In the custom experiment either
    magnet can be clicked to turn it, and the prepared spin can be dragged. A products-of-projections table
    sits beside it.
  - *The Bloch sphere*: prepare θ and φ in 15° steps or from six presets, and measure one atom or ten (PhET's
    3-2-3-2) along X, Y or Z.
    - Optionally a field along z turns the state during a 0–1 ns delay (default 0.75). The field is PhET's
      unit made real: an electron in B₀ = 35.68 mT turns once a nanosecond.
    - The state can be written in the Z, X or Y basis, with or without the global phase. Drag to orbit.
    - Beside PhET's screen, a fringe panel plots P(up) against the delay for this field, with the measured
      fraction at the current delay.
- **Two analysis views:**
  - *The Born rule* sets the spin's cos²(Θ/2) against the photon's cos²θ at 13 angles. Each point is 2000 seeded
    shots through the same measurement code the other views run, χ² 8.39 on 16. The view also shows the middle
    measurement (¼sin²α for spins, ¼sin²2α for photons) and a chain of N magnets passing [cos²(π/2N)]^N → 1 as
    1 − π²/4N.
  - *The binomial* repeats N-coin sets against the exact pmf (binned when N = 10 000). It also shows the spread
    of k/N against √(p(1−p)/N) on log–log axes, and one long run of 10 000 flips inside its ±2σ funnel.
- **Exact:**
  - the Born rule four ways (projector trace, (1 + r·n)/2, |⟨n|ψ⟩|², cos²(Θ/2));
  - the sequential Stern–Gerlach probabilities as products of projections, against 2×2 complex projectors in
    numpy for all seven experiments × four sources, plus a [z, x, z] layout PhET cannot build (it links its
    second-stage magnets), so the beam routing is pinned too;
  - Larmor precession as an exact rotation of the prepared vector, against scipy `expm` on the ket (vector, U
    and P(up) on three axes, three cases) and against a 4000-step RK4 integration of the Schrödinger equation.
    The sign is pinned: +X after 0.75 ns is −Y, so a y measurement is always down;
  - the ket ↔ Bloch vector ↔ angles round trip over 169 states, and every printed equation rebuilt into its ket;
  - ln n! (Stirling above 30) against math.lgamma to 2e-15, and the pmf against scipy to 1e-10.
- **Every random draw is one mulberry32 stream**, mirrored bit for bit in `derive.py`. Every seeded count in
  selfTest is an integer pinned exactly AND tested against its law with a tolerance from its own variance:
  - 4σ on counts;
  - 4σ/√M on sample means;
  - the fourth moment for the sample variance;
  - χ² below scipy's 99.9 % quantile;
  - 4/√(2(M−1)) on a measured spread.
- **Verification:**
  - selfTest 1775 checks, 0 failed under osascript;
  - UI drive 219 checks, 0 failed. Every canvas interaction goes through the frame loop from a proven-idle baseline: the coin
    clicks, the laser click, the dial drag, the source click, the magnet click, the spin-disc drag, the camera
    one axis at a time, and the Born cursor. Every reset is checked against a sentinel;
  - mutation sweep 79 of 79 caught (63 physics, 16 UI), no survivors, on a copy in `build/quantum-measurement/_out/`;
  - audit: 0 layout problems at 1400×820 (no advisories) and 820×520 (under-readout advisories only);
  - every captured view (26 + 6 narrow) was looked at;
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - PhET's custom spin state uses θ = π(1 − |α|²), so its own equation disagrees with its |α|² slider except at 0,
    ½ and 1 (0.854 at 0.75). Here θ = 2 arccos|α| and the slider IS P(↑z).
  - PhET's Y-basis equation prints 1.5π for +X, which rebuilds −X with PhET's own +Y. Here it prints 0.5π.
  - PhET turns its spheres a frame at a time and measures after the frame that reaches the delay, up to 1.5°
    late at 60 Hz and full field. Here the rotation lands exactly on the delay.
  - The beam starts at 60/s (PhET: 0), and an unpolarized beam shows its expectation value 0.
  - The two photon scenes share one set of controls, and the blocker is one setting (PhET keeps them per scene
    and per experiment).
  - There is no flying-coin animation, PhET's display toggles are always on, and its 10 000-coin easter egg is
    absent.
  - No sounds and no screen-reader descriptions.
### Fixed (during the build)
- **The Python twin disagreed with the engine on one seeded count** (the middle measurement's spins: 955 vs 951).
  Root cause: `derive.py` drew the complementary event (`u < ½(1 − cos α)`, a down) where the engine counts "not
  up" — the same probability, a different draw off the same stream. A bit-exact twin must mirror the EVENT, not an
  equivalent probability.
- **Panels were drawn under the caption and the HTML #hint at 560 × 380.** Root cause: the lower rows had floors on
  their heights, so they kept their size instead of vanishing when the space ran out. The floors are gone: a row
  that does not fit is not drawn, and selfTest asserts the hint band (18 px) is clear of canvas text.
- **Titles sat on their own frames, the Bloch titles collided with the axis labels, B collided with Z, the mirror
  label ran into the histogram's ticks, and corner ticks collided.** Root cause: labels were positioned from the
  box rather than measured against their neighbours. Titles moved above their boxes, the field label went left of
  its tip, the mirror label left of the ticks, and a tick at zero is written as a bare "0".
- **selfTest took 18.4 s under osascript.** Root cause: the test helper `fresh()` cleared the memo, so every
  binomial drawing in the layout sweep recomputed 2.5 M seeded draws. The memo keys carry all their inputs (the
  functions are pure), so it is never cleared; `binSpread` also caps a point at 1e6 draws. 5 s now.
- **Four test bugs that hid or faked a result**: an emission counter hooked onto an array `photonAdvance` replaces;
  a particle-rate expectation written per second for a 9-s run; a dial probe 3 px off the axis it meant to hit; and
  a classical-timing test that assumed every photon's splitter distance is 0.15 (it is 0.13–0.17 across the beam's
  width, so the test now reads the photon's own `d1`).
- **The UI drive passed 8 checks it should have failed.** Root cause: its button finder matched hidden buttons, so
  clicks on a panel group that was not shown "worked". It now walks the ancestors for `hidden`. Idle proofs were
  added before every interaction, and one pump was too short to reach the state it asserted.
- **The atoms chip reset the counts**, which PhET does not do: it reprepares without clearing the histogram.
- **Mutation survivors, each fixed rather than excused**: a Stirling series re-typed inside a test (now the
  engine's own `lnFactStirling`); the `quantumInit` threshold and the Stern–Gerlach beam routing (now pinned off
  PhET's domain); the collapse assertion, which only the parent sim's suite ran (moved into the shared
  `engineTests`); and "the precession does not repaint", which survived because the animation test compared a
  repaint against a possibly EMPTY second frame — `animatesU()` now drains the dirty repaint and requires two
  consecutive animation frames, both drawn and different.
- **`COINS.classical.p === 0.35` failed** after seven bias steps. Root cause: 7 × 0.05 = 0.35000000000000003.
  `snapBias` rounds to k/20 and selfTest pins the exact value.
- **The photon view printed a negative zero**: "(expected -0.000)" on the canvas and "−cos 2θ  -0.0000" in the
  readout at 45°. Root cause: ⟨P⟩ = −cos 2θ is −6.1e-17 in floating point and `toFixed` keeps the sign.
  `p1_utils.js` is a verbatim house extract, so the fix is `fmt0()` at the call sites; `layoutCheck` and both
  panel sweeps now reject any negative zero on the canvas or in the readout, equation bar and tag.
- **Value labels sat on the law's orange mark** ("28.1/s" on the 0.5 mark, "45%", "97.5/s", the coins' "46").
  Root cause: `barVal` placed the label 9 px above the BAR and knew nothing of the mark, so a bar stopping just
  short of its mark put the label on it. `barValY` now takes the mark's pixel y and picks the first place that
  clears it by 8 px (above the bar, above a higher mark, inside the bar's top, inside under the mark), checked
  over 6363 bar × mark pairs in three box heights; `layoutCheck` rejects any text crossing a short horizontal
  orange stroke, which is how the last three were found.
- **The empty-box note ("nothing yet") sat on a high mark** in the custom spin state. Root cause: it was pinned to
  the box top. `freeY` takes the top, then the middle, then the first line clearing every mark.
- **Legends named things that were not drawn.** The Malus legend listed "measured V fraction ± 1σ" in the beam and
  unpolarized views, where no point is drawn; the Bloch fringe legend listed the measured point before any
  observation with the field on, and never listed it with the field off although it draws one. Root cause: the
  legend was a constant while the drawing was conditional. Both are now built from what is drawn, and the beam's
  measured point (the rates' fraction, where the counts' σ does not apply) is drawn.
- **A legend vanished with no error** when the beam's entry grew longer. Root cause: the house `legendAuto` draws
  NO legend rather than a lying one when every candidate spot is crossed by a curve. The entry is short again, and
  selfTest wraps `legendAuto` during the layout sweep and fails if any legend is lost at 1100 px or wider — which
  immediately caught a second one, the Born view's middle-measurement legend at 1100 × 700: its y-axis ran to 0.3
  against curves peaking at 0.25, leaving a sixth of the box. The axis now runs to 0.4.
- **Captions named panels that were not drawn**: the Bloch caption's "the panel below draws it against the delay"
  at 820 × 520 and 700 × 450, and at 560 × 380 the coins' "Orange: Np ± √(Np(1−p))", the Born view's "the chain
  → 1" and the binomial's "one long run". Root cause: the caption is fixed text, but the panel it names survives
  only in the height the caption itself leaves. `layoutNamed()` lays out with the naming caption; if the panel
  does not fit it lays out again with the caption that does not name it and keeps the panel off.
- **The "after magnet 2" dial sat on the upper magnet's up beam** (28 px of overlap at 1400 × 820). Root cause: all
  three stage dials were placed at the same height, which is inside the second stage's beams. It now sits on the
  midline between the second magnets' inner beams with its label to the right; selfTest measures every dial
  against every beam band (7 experiments × 4 sizes, worst clearance 6.9 px).
- **The magnets' exit labels (↑z, +x) were covered by particles.** Root cause: they were drawn on the beams, and
  the particles are drawn over the beams. They now sit inside the magnet at its exit face, where the particles
  pass underneath.
- **Found by looking at the PNGs**: the coin strip ran under the floating readout; "10000" instead of "10 000";
  photon dots large enough to cover the detectors' letters; a full bar hid its own green-on-green count;
  particles covered the magnet labels; blocked beams were drawn past the blocker; "none yet" sat on the 0.5 marks;
  the equation rows lost their alignment; and the Bloch view's lower half was empty (it is now the fringe panel).
### Known-bad candidates
- **PhET's custom spin state θ = π(1 − |α|²)** disagrees with PhET's own printed equation except at 0, ½ and 1
  (0.854 against 0.750 at |α|² = 0.75), and **PhET's Y-basis phase** prints 1.5π for +X, which rebuilds −X. Do not
  copy either into a remake; both are pinned here as PhET's values with the correct ones beside them.
- A bit-exact twin that draws the complementary event is not bit-exact: mirror the event, not the probability.
- A button finder that ignores hidden ancestors turns "not shown" into "clicked".
- Floors on derived panel heights: a floor keeps a panel alive under the caption and the hint instead of dropping it.
- Clearing a pure memo inside a test helper (18 s of recomputation for nothing).
- "Compare two frames and assert they differ" passes when the second frame is empty: drain the dirty repaint and
  require two consecutive drawn frames.
- An engine contract that only one sim's suite exercises belongs in the shared `engineTests`, or the other sim's
  sweep finds it unprotected.
- k × 0.05 is not exact (7 × 0.05 = 0.35000000000000003): snap to k/20.
- `toFixed` keeps the sign of a negative zero, so an exact zero built from a cosine prints "-0.000".
- A value label placed above its bar alone lands on the law's mark whenever the bar stops just short of it.
- A legend written as a constant beside a conditional drawing, and `legendAuto`'s silent "no legend at all" when
  every spot is crossed — a longer entry can remove a legend with no error.
- A caption that names a panel the layout is allowed to skip.
- Labels and dials placed where the beams and particles are drawn (the particles are drawn last).
- One splitter cannot distinguish classical which-path from quantum collapse: with one photon at a time both give
  identical seeded counts, so the difference must be asserted on the timing, not on the counts.

## 2026-09-18 — energy-forms-and-changes: PhET's bench and energy systems, with every joule on a ledger that closes
### Added
- `energy-forms-and-changes.html` (236.7 KB), a remake of PhET's Energy Forms and Changes 1.4.24 in five views:
  *the bench*, *the systems*, *the heat ledger*, *the energy flow*, *equilibrium*.
  Credit line in the header and on the page; site nav absolute; no network.
- *The bench* is PhET's Intro screen. It has the iron and brick blocks, the water and olive-oil
  beakers, PhET's six spots and stacking rules (no beaker on or in a beaker), and two heat/cool
  burners with draggable levers and "link heaters". It also has four thermometers in a tray (they
  stick to what they are dropped on, and read PhET's steam and flame temperatures), energy symbols,
  play, step and ×4, and five presets (PhET's start, heat the iron, hot iron into water, brick on
  iron cooling, boil the water).
- *The systems* is PhET's Systems screen, with every source, converter and user in PhET's carousels:
  - sources: the cyclist (21 chunks of food, "feed me"), the faucet, the sun with clouds, and the
    teapot on a burner;
  - converters: the water-wheel generator (belted to the cyclist) and the solar panel;
  - users: the beaker heater, the incandescent bulb, the fluorescent bulb and the fan.
  Energy chunks are drawn by form (mechanical, electrical, thermal, light, chemical) under PhET's
  "forms of energy" key.
- *The heat ledger* records the bench. It draws each body's temperature, and the first law as three
  accounts: the burners did = the bodies gained + the room took. The halo and the sum coincide to
  the last digit. A panel beside them sets each body's chunks against PhET's map g(E).
- *The energy flow* is the chain as a Sankey diagram to scale in watts, with its stores (the falling
  water, the kettle, the wheel, the heater's water) and every loss. Below it runs the cumulative
  ledger, IN = OUT + LOST + STORED.
- *Equilibrium* takes one of five pairs. It lays PhET's stepped model over the exact solution of the
  linear pair-and-room system: a closed-form 2×2 matrix exponential, checked against
  `scipy.linalg.expm` and against its own ODE. It draws T_eq = (C₁T₁ + C₂T₂)/(C₁ + C₂), the gap in
  mK, and PhET's heat capacities against the real ones.
- **The model is PhET's**, read out of the build:
  - EFACConstants: the specific heats and densities 450/7800, 840/3300, 3000/1000 and 1411/916;
    4.5-cm blocks; 8.5-cm beakers, 1.1× tall and half full; the 120-per-m² displacement.
  - HeatTransferConstants: k = 1000 W/(m·K) between bodies and 30 W/(m·K) with the air.
  - ThermalContactArea's contact length, with PhET's operator precedence kept.
  - The burners' 5000 and 1500 W, the 620-K and boiling-point caps, and the 1e-6-K threshold.
  - The air as an infinite 296-K bath.
  - The chunk map (brick at 0 °C = 1.25 chunks, at 296 K = 2.4), so ENERGY_PER_CHUNK = 5019.022 J.
  - The Systems rates: 10 kW; the crank's 3π rad/s and π/2 rad/s²; the 0.4-s fall; the sun at
    0.1 + 0.9(1 − clouds); the 10-s teapot and the 5/3-s wheel; the 68 % panel; the heater's
    5000 W and 0.5/s ramp; the bulbs' 65/35 and 80/20; the fan's 0.0051 rad/s per W.
  - PhET's own pre-distributed chunk tables (6, 2, 34, 8, 20 chunks) are reproduced exactly: an
    independent check of the masses and the map.
- **Real materials** (in *equilibrium*), each from its source:
  - water: NIST Chemistry WebBook (IAPWS-95) at 296 K, 4182.32 J/(kg·K) and 997.577 kg/m³;
  - iron: NIST-JANAF Cp 25.094 J/(mol·K) over 55.845 g/mol, and 7874 kg/m³ (Arblaster 2018);
  - brick: 840 J/(kg·K) (Wikipedia's table) and 1900 kg/m³ (Engineering ToolBox's 1400–2400);
  - olive oil: 1970 J/(kg·K) (Engineering ToolBox) and 911 kg/m³ (USDA).
- **Exact:**
  - the bench's first law every step to rounding (≤ 8ε of the energies; 1e-8 J summed over 1800
    steps);
  - the chunk identity E + Σ(energy in transit on a body's links) − EPC·chunks = constant,
    ≤ 1e-12 at every step of every scenario, with |chunks − g(E)| < 1 always;
  - every Systems element's in = out + losses + Δstore every step (≤ 4ε), and the global ledger
    across chain swaps and feeding;
  - every channel's chunks = floor(E/EPC);
  - equilibria against expm to 1e-11;
  - eleven bench scenarios, eleven chains and every equilibrium pair (both materials) pinned to
    `derive.py`, an independent Python twin, through `refvals.txt` → `p7a_refs.js` (679
    references, none typed by hand).
- **PhET's own numbers that do not close, each pinned in derive.py and corrected here:**
  - the teapot makes steam at 20 kW × heat, twice its burner's power below its cap;
  - the cyclist puts out 10 kW × crank/max while his chunks send one in six to heat;
  - the generator's efficiency depends on the frame rate: 69 % at 60 frames/s, while at
    30 frames/s it puts out 1.38× what it takes in;
  - the heater puts half its power into the water and says nothing of the rest.
- **Verification:**
  - selfTest: 2037 passed, 0 failed under osascript. It includes a layout sweep of 31
    configurations × 4 sizes with the #hint-corner check.
  - UI drive: 250 passed, 0 failed. The lever, body and thermometer drags are all tested through
    the frame loop from proven-idle baselines, and every reset against a sentinel.
  - Mutation sweep: 110 of 111 mutants caught (97 physics, 14 UI). It ran on the copy in
    `build/energy-forms-and-changes/_out/`. The last mutant, the right slider’s link, was added
    after the full sweep and ran in its own pass on the same html. The one survivor,
    `no displacement cap`, is equivalent. PhET’s min(0.5 + 120·area, 1) cannot bind, because
    only the two 4.5-cm blocks displace, and together they lift the water to 0.986 at most
    (asserted in scenario I).
  - Audit: 0 layout problems at 1400×820, 1100×700 and 820×520. The narrow size shows only the
    under-readout advisory.
  - Every captured PNG (28 + 5 + 6) was looked at.
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - One fixed 1/60-s step.
  - Drops snap to PhET's spots at once; PhET lets bodies fall.
  - The levers stay where they are left; PhET's spring back unless `stickyBurners` is set.
  - ×4 is shown; PhET hides it behind `showSpeedControls`.
  - One play/pause for both screens.
  - The Systems screen opens on the faucet running; PhET opens on the cyclist, not pedalling.
  - Energy symbols start shown.
  - Thermometers print °C.
  - Blocks are drawn with their front face on the model's rectangle; PhET centres the cube on it.
  - Chunks are the ledger quantised, not PhET's random paths.
  - The fan's heat is PhET's full-power 1/14 at every power.
  - No sounds, no keyboard dragging, no screen-reader descriptions.
### Fixed (during the build)
- **The cyclist's 21 food chunks lay on one diagonal.** Their jitter was (k·0.618 mod 1,
  k·0.382 mod 1), and the two sequences sum to 1, so every point sat on a line. They now sit on a
  grid along the torso.
- **The iron vanished when it was dropped into the water.** Two causes:
  - the water's chunks were painted over it;
  - PhET's oblique cube, centred on the model rectangle, hung 5.6 mm through the floor of a beaker
    that is drawn flat.
  The bench now paints by depth: the liquid, its chunks, the block and its chunks, then a
  translucent liquid front and the glass. Every box draws its front face on the model rectangle,
  and the pick and sensing shapes follow what is drawn.
- **Hot blocks were given a glow, which is unphysical.** Iron does not visibly glow below about
  800 K, and PhET caps blocks at 620 K. The glow was removed.
- **The ice and flames poked above the burner into the block,** and at full heat the lever's knob sat
  on the flame. Both now stay in the burner's mouth, and the lever's track runs below them. The
  drawing and the pointer share one pair of constants, so the two cannot drift apart.
- **At 820×520 and 560×380 tick labels ran into the caption.** The two-row layout squeezed its main
  panel below 80 px, and its no-row fallback ran the panel to 16 px above the caption, where its
  ticks hang. The fallback (`layoutFit`) drops the row only when the main panel would be under
  100 px, and then leaves the 34 px its ticks and axis title need.
- **Captions described panels the narrow layout does not draw.** Each view now carries full, two,
  solo and short captions, and draws the one that matches its panels.
- **Labels were shifted into the caption and onto legends.** `lab()` avoids only registered boxes.
  The captions and every legend are now registered before any label is placed.
- **The per-element ledger check failed on correct code (6e-12).** It judged each step's residual
  against that step's flows alone. A 1.6e5-J store of water rounds at 3e-11 J, which is 1e-9 of a
  0.02-J step. The check now includes the store it touches, and holds at ≤ 4ε.
- **Six tests could not fail, found by pre-screening the mutants:**
  - the chunk-speed check compared CHUNK_V with CHUNK_V;
  - the corrective pass's shedding branch never ran (a hot iron under the brick, losing heat on
    two links, now runs both branches);
  - the heater's 0.5/s ramp never bound (switching the heater into a running chain makes it bind);
  - a converter swap with a full wheel was never tried;
  - PhET's substeps, a block straddling the glass and the 1e-6-K threshold were unreachable at the
    fixed 1/60-s step, and each now has a direct pin;
  - the room's box only showed its size with a beaker held at the bench's end.
- **Two prose claims were wrong against the measurements:**
  - "a few tenths of a kelvin at most" for PhET's step against the exact solution: the gap is
    1.33 K at the extreme settings, always under 0.4 % of the starting difference, and that is now
    asserted;
  - "100 % at ×4" for PhET's generator: the Systems screen has no ×4. At 30 frames/s the
    generator puts out 1.38× what it takes in. Now pinned in derive.py.
- **"link heaters" worked through two mechanisms, so cutting either changed nothing.** The first
  mutation sweep’s "linking the heaters does nothing" survived. The sliders copied the left level
  into the right while linked, and the level reader also used the left level for both. The reader
  now returns the two levels as stored, every writer (both sliders, the lever drag, the link box)
  keeps them equal, and one UI mutant cuts each writer.
- **What the converter cannot use was drawn twice.** The source's own chunks carry on past it, and
  the `x.miss` channel spawned a second set. The channel is now counted but not drawn.
- **The thermometer drop test aimed at the wrong pixels,** and the grab-offset and linked-lever
  tests assumed levels that the previous steps had changed. Each test now computes its target from
  the current state.
### Known-bad candidates
- **PhET's Systems screen does not close its own ledger.** A remake that copies its rates verbatim
  inherits three faults: a teapot that makes steam at 2× its burner's power below its cap, a
  generator whose output depends on the frame rate (1.38× its input at 30 frames/s), and a cyclist
  whose numeric output disagrees with his chunks by one in six. Choose rates that close, and pin
  each PhET discrepancy in the Python twin.
- **(k·φ mod 1, k·(1 − φ) mod 1) is a line, not a scatter.** A golden-ratio jitter in x paired with
  its complement in y puts every point on one diagonal.
- **An oblique box centred on its model rectangle, drawn next to flat containers, hangs through the
  containers' floors.** Draw its front face on the rectangle.
- **`stageLayout` with no bottom row leaves 16 px under the main panel,** so its ticks and axis
  title land on the caption. A fallback that drops the row must shrink the panel about 34 px.
- **`lab()` avoids only what is registered.** Register captions and legends before placing labels.
- **A per-element ledger residual must be judged against the store it touches, not just the
  step's flows.** Otherwise a correct element holding a large store reads 1e-9.
- **A heuristic transfer rule gains an exact, testable invariant if every transfer moves its
  link's balance by exactly one quantum.** Energy plus the balances still in transit, less
  EPC × chunks, is then conserved to rounding.
- **PhET's own spots are asymmetric:** spot 0 is −0.241 and spot 5 is +0.242, because
  −241.4999… rounds down. Copy the arithmetic, not the intent.
- **PhET's burner clamps its displayed temperature at 273.15 K for any level below −0.23,**
  although the cooling it applies still scales with the level.

## 2026-09-18 — wave-interference: PhET's lattice with its time step solved from its own dispersion relation, two sources against their hyperbolae, slits against Rayleigh–Sommerfeld, and the far field as an FFT checked against Airy, sinc² and the Gaussian
### Added
- `wave-interference.html` (208 KB), a remake of PhET's Wave Interference 2.0.22 in six
  views: *the ripple tank*, *two sources*, *the slits*, *the far field*, *path difference*,
  *the lattice*. Credit line in the header and on the page; site nav absolute; no network.
- **PhET's four screens, one view each:**
  - *The ripple tank* is the Waves screen. It has water, sound and light, frequency and
    amplitude, and continuous or pulse. Water has top and side views; sound has waves,
    particles or both; light has the screen and its intensity graph. It also has the
    centre-line graph, the tape measure, the stopwatch and the two-probe wave meter (both
    probes and the tape end drag), normal and slow speed, pause, one step, and clear.
  - *Two sources* is the Interference screen. Each source switches separately, the separation
    is set per medium, and the nodal hyperbolae are drawn over the lattice.
  - *The slits* is the Slits screen: a plane wave with no barrier, one slit or two; slit width
    and separation; a barrier you drag by its handle. Moving the barrier clears only its right,
    as PhET's does. The light screen is compared with the Rayleigh–Sommerfeld sum and with the
    Fraunhofer formula.
  - *The far field* is the Diffraction screen. It has PhET's five apertures (ellipse,
    rectangle, circle & square, disorder, and a waving figure), plus a Gaussian and N slits for
    the closed-form checks. It has PhET's λ₀/λ rescaling, PhET's log(0.01|F| + 1) display or
    linear |F|², and the horizontal cut against the closed form.
- **The engine is its own part file** (`build/wave-interference/p2_engine.js`, API in
  `ENGINE.md`) for the waves-intro follow-up. It has:
  - PhET's lattice: 151 × 151 cells, a 20-cell pad and C = ½;
  - Mur's second-order absorbing edge;
  - point and plane sources, the screen and the probes.
- **Exact:**
  - The lattice's dispersion relation sin²(ωΔt/2) = C²[sin²(kₓΔx/2) + sin²(k_yΔx/2)]: Ω(k),
    k(Ω, θ) by bisection against scipy brentq, and phase and group speeds.
  - The time step is solved from that relation at every frequency. So λ = v/f and T = 1/f hold
    exactly along the lattice axes in all three media. PhET fixes one step per medium, which
    makes its wavelengths 0.7 % to 3.2 % short (derive.py; plotted on *the lattice*).
  - The driven plane wave is an exact lattice solution (5e-15 over 20 steps, axis and
    diagonal).
  - The engine agrees with a numpy twin that repeats every operation to 1e-11, over five
    scenarios of 150–400 steps.
  - Mur's reflection, from the plane-wave ansatz, is checked against a packet simulation to
    2 %: ≤ 3 % to 45° against 17 % for first order.
  - Two sources: the hyperbolae, their count 2⌈d/λ − ½⌉, and exact against far-field screen
    positions.
  - The far field:
    - |FFT| of the drawn aperture against numpy.fft.fft2 (eight apertures, six bins each) and
      against a direct DFT;
    - the pixel-snapped rectangle against the Dirichlet kernel (1e-15);
    - the sampled Gaussian against its continuous transform (5e-16);
    - the disc against [2J₁(v)/v]² (1.2e-3 of the peak for k ≤ 10, first ring on bin 16 of
      16.26);
    - J₀, J₁, sinc² and the N-slit factor against scipy.
  - Colour is the CIE 1931 table, every 5 nm, read from the CIE's file.
- **Findings (derive.py, stated on the page):**
  - At steady state the lattice's light screen follows the 2-D Rayleigh–Sommerfeld sum to 6 %
    (3 % rms) but misses the Fraunhofer formula by 26 %. PhET's screen sits 2.5 µm behind slits
    1.5 µm apart, where d²/λ is 4.4 µm. The first minimum falls 10 rows out on the lattice and
    in the Rayleigh–Sommerfeld sum, but 9 in the Fraunhofer formula.
  - The lattice's nodal lines sit 0.85 cells outside the continuum hyperbolae on average, 1.4
    at worst, always outward. The continuum 1/√r formula puts them within 0.08. The cause is
    the lattice's anisotropy: k(θ) differs by about 1 % between axis and diagonal at 11 cells
    per wavelength.
- **Verification:**
  - selfTest: 1305 passed, 0 failed under osascript. It includes a layout sweep of 37
    configurations × 4 sizes, and every slider end across all media and apertures, finite and
    clean.
  - UI drive: 257 passed, 0 failed. It covers three custom drags, each through the frame loop
    from a proven-idle baseline; every tab, visible slider, checkbox, chip, button and key;
    resize; and reset-all against a fully disturbed state.
  - Mutation sweep: 81 caught of 81 (67 physics, 14 UI). The first sweep caught 78 of 81. Its three survivors were test gaps; they are now closed, and on a re-run against the final file all three are caught (see Fixed). The other 64 physics mutants cover every PhET constant, the Courant number, every Mur coefficient and sign, the dispersion relation, the calibration, the plane wave, the slits, the screen, the probes, the clock, the aperture renderer, the FFT, the closed forms, the theory curves and the colour. The 14 UI mutants cover the dirty flags, the frame loop, the drags, the panel and the keys.
  - Audit: 0 layout problems at 1400×820, 1100×700 and 560×380. At 560×380 it reports only the
    under-readout advisory.
  - Every view's PNG was looked at.
- **Sources:** PhET's values, read from `docs/phets/wave-interference_en.html`:
  - the lattice, the event rate, and the amplitude and plane-wave factors;
  - the colour scale 2.14;
  - the media (widths, speeds, frequency ranges, scale bars, slit and source ranges and
    defaults, time scales);
  - the 90-step screen history and the barrier range;
  - the diffraction grid (256 over 4/3 mm), the aperture ranges and defaults, and the λ₀/λ
    rescaling and log display.

  Colour: the CIE 1931 2° table (DOI 10.25039/CIE.DS.xvudnb9b), from the file the
  blackbody-spectrum build fetched. PhET's model notes were fetched from GitHub.
### Fixed (during the build)
- **A damping sponge in PhET's 20-cell pad made long waves reflect more, not less.** It gave
  60 % at 73 cells per wavelength against 0.03 % for Mur alone. A damping layer thinner than a
  wavelength is an impedance step. Mur's second-order condition alone gives ≤ 3 % to 45° for
  every medium.
- **A packet measurement said Mur-2 reflects 37 % at normal incidence for long waves.** The
  6-wavelength packet overlapped the edge at t = 0. The plane-wave ansatz gives 3e-4, and the
  packet agrees with the ansatz to 2 % wherever the packet fits.
- **The clock ran on across media.** A fresh tank read t = 65 s, left over from the selfTest's
  runs, because `runClear` does not reset time (PhET's clear does not either). A new medium now
  restarts `t`, `n` and the stopwatch.
- **The path-difference map was saturated flat green** (1/r near the sources). It now shows the
  interference factor I/(1/r₁ + 1/r₂), so the fading with distance is divided out.
- **The nodal overlays re-derived the hyperbola inline, twice**, and the ellipse's minor axis
  was written in both the renderer and the drawing. The duplicate ellipse formula was found by
  `gen_mutants.py`'s pattern-uniqueness check. All of these now call one pinned function
  (`hyperY`, `farY`, `ellipseAxes`).
- **The FFT cache key held all sixteen aperture parameters**, so a hidden slider forced a
  re-render. It is now keyed on the chosen aperture's own parameters.
- **Moving the barrier restarted the plane wave.** It now uses PhET's clearRight, which wipes
  from the new barrier rightward and keeps the wave's progress (asserted).
- **Layout.** The intensity graph's and the screen plot's axis labels landed on the caption:
  their boxes ran the lattice's full height, with the labels below. The rows are now measured.
  Other layout fixes:
  - the centre-line graph is dropped with a note where it cannot fit;
  - the origin ticks of the dispersion panel collided;
  - a medium label sat under the legend (the legend is now registered first, and the label
    falls back to the bottom);
  - the stopwatch box covered the water dripper;
  - the time label dodged into the tank at 560 px.
- **A path-difference screen drag was removed before it shipped.** The map is fitted to L, so
  the dragged line would have stayed put while the map rescaled under it.
- **Test fixes:**
  - a readout pin that was not off the model (the lattice's 34-cell separation prints 1532 nm,
    not the 1530 typed);
  - a J₁ join tolerance tighter than the house J₁'s own 1e-10 class (3.2e-10 across the join);
  - UI op floors guessed at 12 and 200 where the fields batch into 10 and 78 ops. They are now
    70 % of the measured emission.
- **The mutation sweep's three survivors were test gaps.**
  - The source rows were pinned only at the sound default, 22.2 cells, where round and floor agree.
    Water's and light's 16.65 cells are now pinned too.
  - The wave-meter probe was only read at cell centres, where the bilinear neighbour has weight 0.
    It is now read between cells on a linear field.
  - The rectangle snap was pinned at 10.9 and 21.8 px, where round and ceil agree. It is now pinned
    at 19.2 px on the width and on the height.
  All three are caught on the final file.
- **One retest baseline came back silent and red under heavy CPU load.** Run directly, and again on
  the retest, the suite was green (1305/0). It was a transient osascript failure, not the suite.
  Before reading a red baseline as a failure, run the suite directly.
- **A duplicate reference label** (two speed lines printed under one label) was caught by
  `derive.py`'s own guard: every value in `p7_refs.js` must be a distinct printed line.
### Known-bad candidates
- **A thin damping sponge reflects long waves.** A 20-cell σ-layer is an impedance step for a
  73-cell wave, and the reflection grows as σ/ω. Use Mur's second-order boundary, and measure
  the reflection before choosing.
- **Measure a boundary's reflection with the plane-wave ansatz, not a packet that touches it at
  t = 0.** The packet read 0.375 where the truth is 3e-4.
- **An overlay drawn from continuum geometry will not sit exactly on a lattice's features.** The
  nodal lines here run about a cell outside the hyperbolae, which is the anisotropy. Say so on
  the view rather than fudging λ.
- **|FFT| of a real aperture cannot see the FFT's sign convention** (|F(−k)| = |F(k)|). A test
  on complex input is what pins the twiddle sign.
- **PhET's one-step-per-medium calibration makes wavelengths short by 0.7–3.2 %.** Solving Δt
  from the dispersion relation per frequency makes them exact along the axes at no cost.
- **A rounding mutant is invisible at every test value whose fraction is ½ or more.** round → floor and round → ceil both survived a sweep whose pinned sizes were 22.2, 10.9 and 21.8 cells or pixels. Pin a value with a fraction below ½. When two quantities are rounded by separate expressions, such as a rectangle's width and height, pin one for each. The first fix put the 19.2 on the height, and the width mutant survived its retest.
- **A bilinear interpolation's neighbour cannot be tested at a cell centre**, where its weight is exactly 0. A test that compares the probe with its own recorded trace compares a function with itself. Read a linear field between cells instead: bilinear interpolation is exact there.

## 2026-09-18 — circuit-construction-kit-dc-virtual-lab: PhET's DC bench built by drag, solved by modified nodal analysis with every branch current an unknown, and Kirchhoff, the power budget, Thévenin and superposition laid open
### Added
- `circuit-construction-kit-dc-virtual-lab.html` (254 KB), a remake of PhET's Circuit Construction Kit: DC -
  Virtual Lab 1.5.2 in five views: *the lab*, *nodes and branches*, *the power budget*, *the rest of the
  circuit*, *one battery at a time*. Credit line in the header and on the page; site nav absolute; no network.
- *The lab* is PhET's one screen, with PhET's toolbox read out of its build: wires (50), batteries, light bulbs,
  resistors, switches and fuses (10 each), the extreme battery, bulb and resistor (4 each), a dollar bill, a
  paper clip, a coin, an eraser, a pencil and a thin pencil (1 each), the real bulb behind "add real bulbs",
  a series ammeter (6), a two-probe voltmeter and a non-contact ammeter. Parts come out of the toolbox by drag;
  an end dropped within 30 units of another joins it under PhET's rules (not adjacent, not in the same rigid
  body, no shared neighbour); a wire's end moves freely, a rigid part's end swings it about its other end, a
  joint of rigid parts moves them together; tap to select and edit (a switch toggles), split a joint, delete,
  reverse a battery, repair a fuse, drop a part back on the toolbox. PhET's values throughout: 9-V batteries
  (0–120 V), 1000-V extreme batteries (100–100 000 V), one internal resistance 1e-4–10 Ω, 10-Ω resistors and
  bulbs (0–120 Ω), 1000-Ω extremes, coin and paper clip 0, pencil 25, thin pencil 50, eraser and dollar bill
  1e6 Ω (the 1.5.2 build's values; PhET's model.md says 1e9), fuse 0.06/rating Ω blowing above rating + 1e-6 A,
  0 Ω → 1.1e-10 Ω, wire R = ρ·(5e-4 m per unit)/5e-4 m² with ρ 1e-10–0.0168 Ω m, the real bulb
  R = 10 + 3|V|/log₂(|V| + 2), brightness ln(1 + 0.35P)/ln(1 + 0.35·2000) with the glass lit to 2b, fire at
  15 A through a battery or a resistor-like part of R ≥ 1e-8 Ω, charges 28 units apart at 25 units/s per
  ampere under PhET's speed limit (0.43 of a spacing per 1/30 s: above 14.448 A the animation slows and
  says so in PhET's words), the voltmeter's 11.2-unit solder radius and interpolation along metal, the
  ammeters' 2-decimal magnitudes saturating at 1e10 A (series 1e3 A). Lifelike or IEEE schematic parts,
  electrons or conventional current, labels, values, PhET's three zooms (chips and the wheel).
- *Nodes and branches*: the circuit as the graph the solver sees (every joint a node, every part a branch,
  wires included), its spanning tree against the chords that close the B − N + C fundamental loops, the MNA
  matrix drawn cell by cell in its four blocks (0, A, Aᵀ, −R) with the right-hand side, and both of
  Kirchhoff's laws measured on the answer at every node and round every loop against ε.
- *The power budget*: a waterfall from each EMF's E·i (a charging battery steps down) through each i²R (the
  batteries' own r included) back to exactly zero (Tellegen's theorem, asserted); the bulbs on PhET's
  brightness curve.
- *The rest of the circuit*: any part's Thévenin view — V_th with it removed, R_th with the EMFs zeroed — as
  the load line crossing the part's own law (a real bulb's curve, a battery's line) at the operating point,
  and the power it would take as its resistance is swept, largest at R = R_th (the one-bulb circuit's battery
  would put 202 kW into 100 µΩ).
- *One battery at a time*: superposition as a signed waterfall per part, each battery on its own sub-row,
  landing on the full solution.
- **Exact:** the solver keeps a voltage for every node but one reference per piece and a current for EVERY
  branch, rows = the current law and each part's own law v_a − v_b = R i − E divided by max(1, R); Gaussian
  elimination with partial pivoting and two refinement passes. `derive.py` solves every circuit by a
  different formulation (nodal analysis, batteries as Norton sources) in exact rational arithmetic: the six
  presets and five variants, eleven netlists (series, parallel, Wheatstone balanced to exactly zero and
  unbalanced, the textbook ideal-source formula, two batteries' superposition, Thévenin and the load sweep,
  16 internal-resistance cases, floating pieces, a dead short, PhET's extreme parts, a zero-ohm loop, eight
  decades of resistance) and 30 random circuits over 16 decades; the real bulb in 50-digit Decimal. The JS
  agrees to 16 ε of each piece's current and 64 ε of its voltage everywhere; both of Kirchhoff's laws close
  to 8 ε (measured ≤ 4.0e-16, also on 300 more random circuits from 1e-14 to 1e6 Ω and up to 100 kV).
- **Verification:** selfTest 1386 passed, 0 failed under osascript (with a 32-configuration × 4-size layout
  sweep and a headless pointer build); UI drive 221 passed, 0 failed — the circuit BUILT by dragging a
  battery, a bulb and two wires out of the toolbox and dropping their ends together through the canvas's own
  events and the real frame loop, every repaint asserted from a proven-idle loop; mutation sweep 94 caught of
  95 (81 physics, 14 UI), run on a copy in `build/circuit-construction-kit-dc-virtual-lab/_out/`, the one
  survivor proven equivalent: the SI-prefix boundary `a >= q` → `a > q`, because at an exact power of 1000 the
  lower prefix gives exactly "1000", which the formatter's rounding-promotion step lifts to the same string
  ("1.00 V", "1.00 mA"); display-list audit 0 problems over 31 captures at two sizes; every PNG looked at.
- **Where this differs from PhET, deliberately:** the real bulb is iterated to its fixed point (PhET's ten
  passes stop 1.7e-11 short in the series preset); charges ride each part and wrap at its ends rather than
  hopping junctions; bulbs are 100 units between terminals (PhET's have both on the base); one voltmeter and
  one non-contact ammeter (PhET's lab has two of each); logarithmic resistivity and battery-resistance sliders;
  IEEE schematics only; no stopwatch, keyboard dragging, sounds or descriptions.
### Fixed (during the build)
- **PhET's own formulation loses digits, so the solver was built another way.** Stamping resistors as
  conductances gets a wire's current as 1e8 S × a voltage difference of 1e-8 V: numpy's float solve of the
  conductance form (derive.py) is off by up to 2e-5 of the largest current on the presets and 2e-4 on random
  circuits, and a JS twin of PhET's formulation by 1e-5 and 9e-5 — so the current law it reports holds only
  to that. With every branch current an unknown the current law is a ROW of the system and closes to
  rounding. Both are asserted: the twin agrees to 1e-5, and is ≥ 1000× further from the exact currents on the
  bridge, so the choice cannot be quietly undone.
- **The Kirchhoff residuals read 100 % on a dangling node.** Normalised by a node's own through-current, a
  leaf carrying 1e-30 A is "100 % off"; normalised by the loop's own drops, a loop of 1e-10-Ω parts at 9 V
  cannot close better than 9 V's last bit. Both are now measured against the connected piece's scale (its
  largest current; its largest voltage, EMF or drop).
- **A short nudge onto a neighbouring end did not join.** A release under the 15-px tap threshold was treated
  as a pure tap. PhET's drag listeners do both — any movement tries the drop target, a short one also selects
  — and the UI drive's fuse, 11 px from its target, found it. Split into "dragged at all" and "moved past the
  threshold".
- **The coin was drawn 1.6× too large at zoom 1.6**: its radius multiplied a pixel length by the scale again.
- **Charges ran over the series ammeter's reading**; they are not drawn inside a meter's box now.
- **Bulb icons reached into the toolbox row above** at small cells; icons are scaled to their cell.
- **Schematic tags collided with value labels**, and the lab reset the label registry halfway through its own
  draw; tags now register, and only `drawView` resets.
- **Tick labels like "6.0×10^-5" ran into the rotated axis title**; every axis now speaks SI prefixes
  (µW, mA, mΩ) with literal glyphs and true minus signs, and log axes use superscript powers.
- **The power waterfall could clip** when a charging battery made the running peak exceed the net power;
  sources that deliver come first and the axis fits the true peak.
- **Captions described panels a narrow stage does not draw** (the thev view's power sweep, the graph view's
  matrix); each view now has a one-panel caption, asserted to match what was drawn.
- **Tests that could not fail, found by the sweep:** the split tested a joint by the battery's terminal name
  after "reverse" had swapped its terminals (the joint already held one part); "chips re-light" was checked
  after a reset that restores the chips' boot classes anyway; the split gap was expected as `99 − SPLIT_GAP`
  (re-deriving the constant under test); a rigid part's swing was aimed exactly 110 units from its pivot,
  where swinging and dragging free coincide; the fire line was tested at 14.8 and 18 A, never between 15 and
  16; the pencil's 25 Ω was never used; the wheel's repaint was compared against an idle, empty frame. Each
  now has a probe that only the correct code passes.
- **Two tolerances were set on the wrong scale:** V_th across the unbalanced bridge is a difference of two
  6.5-V node voltages (absolute error, on the 10-V scale), and the balanced bridge's 3.0e-11 A is the
  difference of two 0.3-A currents (known to ε × 0.4 A).
### Known-bad candidates
- **A conductance-stamped MNA (PhET's formulation) computes each wire's current as ΔV × 1e8 S.** Its branch
  currents are good to ~1e-5, and the current law it "satisfies" only to that. If a sim claims Kirchhoff to
  machine precision, keep every branch current an unknown and measure the laws on the answer.
- **Normalise a conservation residual by the scale of the connected piece, not by the node's own flow**: a
  dangling node's rounding-level current reads as a 100 % violation.
- **A tap threshold is not a drag threshold.** PhET joins on any movement and selects on a short one;
  treating a short drag as a pure tap silently fails every small nudge.
- **Element terminal names are not stable under "reverse".** A test that names a joint by a battery's `a` after
  reversing it probes the other end — and an assertion that the joint "now holds one part" passes doing nothing.
- **A chip-lit check after "reset all" is vacuous** when chips keep the classes they were built with; check that
  clicking one lights it and dims its neighbour.
- **A swing-about-the-pivot test must aim at a point not one part-length from the pivot**, or the free-drag
  mutant lands in the same place.

## 2026-09-18 — charges-and-fields: point charges on a plane, their exact field and potential, in five views

Remake of PhET's Charges and Fields 1.0.67 (`docs/phets/charges-and-fields_en.html`)
as `charges-and-fields.html` (build/charges-and-fields/), in the house form:
five views, the scaffold, palette, `h()`, 2-D layer and camera extracted from
`projects/simulations/build_buoy` and `build_lagr` (make_head.py,
make_utils.py, make_helpers.py assert every function they carry), the site
nav absolute. New code; no PhET code or assets.

### Added
- **the plane** — PhET's screen: drag +1 nC and −1 nC charges and E-field
  sensors out of the bin onto the 8 m × 5 m plane, drop them back to remove
  them; the field on PhET's 0.5-m arrow grid (fixed length, opacity |E|/5 V/m,
  or "direction only"); the voltage on PhET's 0.1-m cells saturating at ±40 V;
  the voltage sensor, whose canvas "plot" button traces the equipotential
  through its crosshair (refused within 3 cm of a charge, PhET's rule, and at
  a null, where the level set is not a curve; cleared when a charge moves, as
  PhET's are); E-field sensors reading |E| and
  its direction (arrow 15 px per V/m at 128 px/m, capped at 2 m with a double
  head); a tape measure in centimetres that also reads V(A) − V(B); PhET's
  grid (0.1 m / 0.5 m) and "1 meter" scale; value labels. **field lines** —
  lines traced along E from the majority sign, an equipotential family every
  ΔV, and the null points found by Newton and classified (saddle, in-plane
  minimum or maximum). **the landscape** — V(x, y) as a clipped height surface,
  the plotted equipotentials lifted to their level as its contour lines, one
  depth sort for surface, loops and charges. **superposition** — each charge's
  field at a probe drawn head to tail and closing on the total, and V built up
  as a signed waterfall. **the far field** — |V| along a ray on log axes
  against its leading multipole, the exact Legendre series (all orders, beyond
  d_max) checked against the tensor contraction, and r^(ℓ+1) V taken to its
  limit numerically (Richardson).
- What is exact: V = k Σ q/r and E = k Σ q r̂/r² of 3-D point charges held in
  the plane (PhET's model), in closed form; equipotentials by RK4 along ẑ × Ê
  with a Newton projection back onto V = V₀ every step (every vertex on the
  level set to ~1e-15 relative, asserted below 1e-12), closing on themselves;
  field lines by RK4 on
  E/|E| with steps from the local length scale min(r_near, |E|/|∇E|); nulls by
  Newton with the analytic Jacobian; the multipole coefficients; the tape's
  line integral. One measured number: ε₀ = 8.8541878188e-12 F/m (CODATA 2022,
  NIST), so k = 8.98755 V·m/nC; PhET's K_CONSTANT is 9, so PhET reads 0.14 %
  high (said on the page).
- Verification: `derive.py` → `refvals.txt` (scipy brentq on rays + quad for the
  equipotential loops' areas and perimeters, solve_ivp for the field lines,
  fsolve for the nulls, quad for the tape, the Legendre and tensor routes for
  the multipoles, Richardson limits), emitted into the suite as literals by
  `gen_refs.py`; selfTest 1594 assertions incl. a 29-configuration × 4-size
  layout sweep; UI drive 184 (every tab, slider, checkbox, chip, button and
  key; the charge, bin, sensor, tape, probe and camera drags and the wheel,
  each repainting through the frame loop from a proven-idle baseline);
  mutation sweep 63 of 63 caught (47 physics, 16 UI; 61 in the full sweep,
  the 2 survivors caught on re-run after their blind spots were pinned; run
  on a copy in `_out/`, log in `mutation_log.txt`); display-list audit 0
  problems over 27 captures; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **Field lines orbited the triangle's centre for 20,000 steps.** Symptom: 2 of
  48 lines neither escaped nor ended. Root cause: the centre of three like
  charges is an in-plane MINIMUM of V, a sink for in-plane lines (the field
  turns out of the plane along z); a 0.2-mm step floor made the RK4 step
  overshoot the node once it was nearer than a step, so the line circled it.
  Near a node |E|/|∇E| is the distance to it, so the steps now shrink
  geometrically and a line ends on a relative-field threshold (2 lines end
  there, asserted).
- **A neutral plane's lines "escaped".** 10 of the two rows' 112 lines passed
  the first 300-m escape radius. Every line of a neutral configuration returns,
  but a dipole-like line leaving at a small angle α reaches ~4a/α²; with steps
  proportional to distance the radius is now 10 km for ~20 steps per e-fold
  (112 of 112 end on charges, asserted).
- **Rounding residue printed and plotted as data.** The rows' V = 0 equipotential
  was labelled "3.99×10^-15 V", and the far field along the dipole's bisector
  drew a green fragment at 1e-15 V. Root cause: cos 90° = 6.1e-17, so the ray
  runs 6e-17·r off the bisector and the two cancelling terms leave residue.
  `potentialClean` zeroes a sum below 1e-12 of Σ|q|/r (a charge still reads
  ∞), sensors read 0 V/m with no direction at a null (asserted both ways).
- **The PNG pass**: opaque grid lines on the voltage-cell boundaries tiled the
  map (now translucent); white sensor labels over white "direction only"
  arrows were unreadable (now on pads, `labPad`); twelve null labels piled on
  the rows (named only when ≤ 4, counted in a status line); the landscape
  framed the bounding sphere of an 8 × 5 × 2.5 m box and sat small (the
  distance is now bisected on the 8 projected corners), its 40-V default clip
  left a dipole as two spikes (20 V), its loops and charge markers were
  painted after the surface and showed through peaks and well rims (one depth
  sort, 5-cm bias), and a foreshortened height bar piled its labels (top label
  only when short); the superposition total vanished off a corner of the plane
  (the chain may use the whole panel, and a note says when it points off).
- **A charge dropped where the bin would be vanished in views with no bin.** The
  bin's delete-on-drop ran in every view, so a charge left near (0, −2 m) in the
  field-lines or superposition view was silently removed. It now acts only on
  the plane, where the bin is drawn (asserted, and a mutant restores the old
  rule).
- Wording measured, not assumed: a line on a neutral plane that passes 10 km is
  reported as "run off past 10 km", not "to infinity" (it would return, and 1
  of 640 did not within 10 km on a 40-charge plane); the far-field INFO said the
  Richardson limit agrees "to about nine digits", but the presets give 6.5 to
  10 (triangle 3.0e-7, rows 4.9e-8, dipole 6.4e-10), so it now says so; "a
  charge confined to the plane would sit stably" at the triangle's centre
  holds only for a positive one.
- Layout sweep catches: the voltage sensor's panel ran over the caption at the
  plane's bottom edge (it flipped only at the canvas edge); a "0.1 m" x tick
  and the lowest y label collided in the far-field corner (ticks from 1 m); the
  waterfall's y ticks collided at 560 × 380 (sparse ticks).
- Test-side, each a wrong expectation rather than a wrong sim: the square
  quadrupole along x has V ≡ 0 (odd under y → −y), not a hexadecapole lead;
  8-point Gauss–Legendre misses x¹⁶ by exactly 2¹⁷(8!)⁴/(17(16!)²) = 4.65e-5
  (now pinned); a ratio of two 1e-4 differences carries JS/Python `hypot`
  rounding at 4e-9 (tolerance 1e-7); near a lone charge the length scale is
  r/√5, never the distance, which binds only where ∇E vanishes (the rows'
  centre); the UI op floors were guessed (120 for field lines) until measured
  (96), and are now 80 % of the measured emission.
- **The mutation sweep's survivors, each a blind spot, now pinned.** "The centre
  of charge's y not divided by Q" survived because every charged preset (one
  charge, the like pair, the triangle) has Σqy = 0, so the centre's y was 0
  however it was computed, and the far-field limits used only those presets.
  The replacement is an asymmetric set with Q = 2 against derive.py, plus the
  centre's defining property (the dipole moment about it vanishes). The first
  attempt had Q = 1, where dividing by Q is the identity: the same blind spot
  again, caught before it ran. "The superposition arrow scale set by the total
  alone" was invisible in both tested chains (no single term outruns the
  total in either); near the like pair's midpoint one term is 1.75× the total
  and now sets the 1.4-m scale.

### Known-bad candidates
- **A symmetric preset family blinds every assertion a symmetry zeroes.** All
  the charged presets had Σqy = 0, so a centre of charge computed wrongly in y
  still read 0, and no moment or far-field assertion built on those presets
  could see it. Pin such formulas on an asymmetric configuration, and check that the
  replacement is not degenerate in another way (Q = 1 makes "divide by Q" a
  no-op).
- **cos(90°) is 6.1e-17, not 0: a ray "along" a symmetry line samples 6e-17·r off
  it, and a cancelling sum there leaves ~1e-15 residue that a log axis draws
  as data and a label prints as a value.** Floor cancelled sums relative to the
  size of their terms (|Σ| ≤ 1e-12 Σ|terms| → 0), never absolutely, and keep an
  infinity infinite.
- **A step floor in a tracer that converges on a node makes it orbit the node
  until maxN.** If the step comes from |E|/|∇E|, which is the distance to the
  node, let it shrink and end on a relative threshold.
- **Overlays painted after a painter-sorted surface show through it.** Put
  contour segments and markers into the same depth sort, biased a few cm
  toward the eye so they do not fight the face they lie on.
- **The bounding sphere of a flat box frames it small.** Bisect the camera
  distance until the box's own projected corners fit.
- **An in-plane slice of a 3-D field is not a 2-D field**: lines per charge are
  not flux, and an in-plane minimum of V is a sink where lines end. "Every line
  ends on a charge" is only assertable for a neutral plane, and only with an
  escape radius far beyond the configuration.
- **`tools/mutate.py` writes `_mutant.js` next to the HTML it sweeps**; agents
  sharing a directory corrupt each other's counts. Sweep a copy in your own
  `_out/`.

## 2026-09-18 — coulombs-law: both of PhET's scales on the gravity lab's engine, the 14-mm closest distance reproduced from PhET's own rounding, the charge product, and electricity against gravity
### Added
- `coulombs-law.html` (128 KB), a remake of PhET's Coulomb's Law 1.0.32 in five views: *macro scale*,
  *atomic scale*, *the inverse square*, *the charge product*, *electricity and gravity*. Credit line
  in the header and on the page; site nav absolute; no network. It runs on the inverse-square engine
  built for `gravity-force-lab.html` (`build/gravity-force-lab/p2_engine.js`, `p4_lab.js`, the
  drawing and test kits), which its assembler reads from there, so the two files cannot drift.
- *Macro scale* and *atomic scale* are PhET's two screens, each with its own state as in PhET:
  charges −10..10 µC or −10..10 e in whole units, dragged along a 1-mm or 1-pm grid on a ±5 cm or
  ±50 pm track (or set by slider), arrows together for unlike charges and apart for like ones,
  "Force Values" and "Scientific Notation" (greyed out while the values are hidden, as PhET does),
  PhET's readouts (3 decimals macro, 9 atomic, a two-decimal mantissa in scientific), a draggable
  ruler per screen (10 cm, 100 pm), the "1 cm" and "10 pm" scale bars and PhET's picometre note.
  Defaults are PhET's: −4 µC at −1 cm and +8 µC at +2 cm (decimal); −2e at −20 pm and +4e at +20 pm
  (scientific). House additions: a per-screen arrow-scale ladder, the distance line, the
  acceleration the atomic pull would give a proton (6.90 × 10²⁰ m/s²).
- *The inverse square* (either scale): |F| against r on log–log axes (slope −2.0000 measured off the
  model), linear axes, and |F| r² flat at |k q₁q₂|; a zero charge draws a sentence saying there is
  no line, not a log of zero.
- *The charge product*: the (q₁, q₂) plane with attract and repel quadrants and |F| hyperbolas, the
  force on q₂ as q₂ changes sign (and q₁'s mirror), and the force against the product q₁q₂.
- *Electricity and gravity* (analysis): an electron and a proton from 1 fm to 1 m, the two
  inverse-square lines parallel and 2.269 × 10³⁹ apart at every distance, the Bohr radius
  (8.24 × 10⁻⁸ N against 3.63 × 10⁻⁴⁷ N), the ratio for e–e, e–p, p–p, and the macro screen turned
  round: two 65.6-tonne masses would pull as hard as −4 and +8 µC, at any distance, a density of
  5.1 × 10¹⁰ kg/m³ in PhET's 1.35-cm spheres.
- **Exact:** k = 1/(4πε₀) from ε₀ = 8.8541878188e-12 (CODATA 2022), k = 8987551786.170797;
  e = 1.602176634e-19 (exact); G, m_e, m_p and the Bohr radius (CODATA 2022), all through
  scipy.constants 1.18. PhET's own rounding is reproduced and pinned: 6.75 + 6.75 + 1 mm sums to
  14.4999… mm in floating point and snaps DOWN, so PhET's closest centres are 14 mm apart with a
  0.5-mm gap. Every value is pinned in selfTest to `build/coulombs-law/refvals.txt`, printed by
  `derive.py`, read in full.
- **Verification:** selfTest 798 passed, 0 failed under osascript (with a 26-configuration × 4-size
  layout sweep); UI drive 152 passed, 0 failed (charges and rulers dragged on both screens through
  the frame loop from a proven-idle baseline; the screens' states independent; the greyed-out
  checkbox inert; the analysis views ignoring the pointer where a charge sits; reset all restoring
  both screens); mutation sweep 61 caught of 62 (49 physics, 13 UI), run on a copy in
  `build/coulombs-law/_out/`, the one survivor proven equivalent below; display-list audit
  0 problems over 16 captures; every PNG looked at.
- **Where this differs from PhET, deliberately:** k and e are CODATA 2022 (PhET's k = 8.987551e9 and
  e = 1.6021766208e-19 differ by 9e-8 and 8e-9; the readout prints PhET's number too). Arrows are
  proportional at a printed scale. No pullers or pushers, sounds or screen-reader descriptions.
### Fixed (during the build)
- **A charge's sign was typeset,** so it was a text label the ruler's "0" collided with whenever the
  ruler lay across the charge. Signs are stroked symbols now (and first drawn 7 px thick, which read
  as blocks; now at most 3.2 px).
- **Symmetric plots labelled the same corner twice:** "−10" on both axes of the charge plane, 10⁻¹⁵
  against 10⁻⁷⁰ on the gravity plot, "−1" against "−10" in a lower panel. The y numbers keep 14 px
  clear of the bottom corner.
- **A zero charge would have sent log10(0) = −∞ into the inverse-square view's axis range.** The view
  says there is no force to plot, and so does the charge product's lower-left panel.
- **Readout formatting:** the proton acceleration went through `sigf` and printed "6.90×10^+20";
  the macro gap printed "0.0500 cm" and now reads "0.50 mm".
- **A prose claim from memory** ("Coulomb's data supported the exponent 2 to a few percent") could
  not be sourced here and was made qualitative.
- **The sweep's one real survivor, "the sphere hit radius shrinks to a fifth":** every pointer test
  pressed a charge dead-centre, where the radius cannot matter. The charges are now also grabbed
  0.6 of a radius off centre, and a press 2 px outside the hit radius must miss.
- **Two substance floors were copied, not derived:** a 4-px atomic charge at 560 px has no
  highlight and a tick for an arrow (4 fills), and the honest zero-charge view is one fill and a
  sentence.
### Known-bad candidates
- **With PhET's numbers the surface gap changes nothing on either Coulomb screen.** Without it,
  13.5 mm also rounds (half away from zero) to 14 mm, and 1.9 pm to 2 pm. A "drop the gap" mutant is
  therefore equivalent here; the invariance is asserted as a property, and the mutant is caught in
  `gravity-force-lab.html`, where the gap matters.
- **A symbol drawn with `fillText` is a label to every overlap check.** Stroke signs and glyph-like
  marks.
- **A zero in a quantity plotted on log axes must be refused at the view,** with a sentence, before
  `log10(0)` reaches an axis range.
- **A dead-centre press tests nothing about a hit radius.** Pin it from both sides.

## 2026-09-18 — gravity-force-lab: Newton's law between two draggable spheres with PhET's no-overlap rule exactly, the inverse square and the mass product made visible, and the twelve-hour free fall
### Added
- `gravity-force-lab.html` (133 KB), a remake of PhET's Gravity Force Lab 2.2.25 in four views:
  *the lab*, *the inverse square*, *the mass product*, *let them go*. Credit line in the header and
  on the page; site nav absolute; no network. It shares one inverse-square engine with
  `coulombs-law.html` (PhET's INVERSE_SQUARE_LAW_COMMON, rebuilt): `build/gravity-force-lab/p2_engine.js`
  and `p4_lab.js`, read by both assemblers, so the two cannot drift.
- *The lab* is PhET's screen with every control its inventory lists: two spheres dragged along a
  0.1-m grid on a ±5 m track (or set by slider), masses 10–1000 kg in 10-kg steps, force values in
  decimal notation (12 places, digits grouped in threes, as PhET prints them), scientific notation
  or hidden, constant size (0.5 m) against mass-scaled size (150 kg/m³), and a draggable 10-m ruler
  that snaps to the grid, with "ruler to m₁" and "ruler home" (PhET's jump hotkeys as buttons).
  House additions: an arrow-scale ladder printed on the canvas, a distance line, and arrows that
  run off the stage end in a chevron with a note.
- *The inverse square*: F against r on log–log axes (the slope measured off the model at the live
  distance, −2.0000), the ×2 in r / ÷4 in F triangle, the bands the spheres cannot reach (overlap,
  PhET's gap, off the track), the same force on linear axes, and F r² flat at G m₁m₂ against an
  inverse cube through the same point.
- *The mass product*: the force over every mass pair at the live distance (hyperbolas m₁m₂ = F r²/G),
  the pairs too big to sit that far apart shaded, F against one mass (straight lines), and the
  strongest pull two equal masses can reach: slope 2 for constant-size spheres, 1.398 for real
  ones (→ 4/3 for touching spheres, G m^(4/3)(4πρ/3)^(2/3)/4).
- *Let them go* (analysis): the lab's forces released. The radial two-body fall from rest in closed
  form, t(r) = √(r₀³/2GM)[√(x(1−x)) + asin √(1−x)], inverted by bisection; the centre of mass fixed,
  momenta equal and opposite, the lighter sphere doing the falling. 100 kg and 400 kg 4 m apart
  touch after 12 h 10 min at 0.18 mm/s.
- **Exact:** G = 6.6743e-11 (CODATA 2022, scipy.constants 1.18); r measured between centres (exact
  for uniform spheres by the shell theorem); the radius (3m/4πρ)^(1/3). PhET's no-overlap rule,
  snap(r₁ + r₂ + 0.1 m), is enumerated over all 10,000 reachable mass pairs in both size modes:
  the snapped gap never falls below 0.05004 m (140 and 940 kg), the nearest rounding tie is 1e-4
  away, so the order of the sum cannot matter. The push rule (who moves when a sphere grows,
  including PhET's m₂-changes-last order on the size switch) on five scenarios. The fall against
  scipy solve_ivp integrating both bodies (8e-12) and against an RK4 of the engine's own forceOn
  (Newton's third law is an output of both). Every value is pinned in selfTest to
  `build/gravity-force-lab/refvals.txt`, printed by `derive.py`, read in full.
- **Verification:** selfTest 764 passed, 0 failed under osascript (with a 24-configuration × 4-size
  layout sweep); UI drive 146 passed, 0 failed (both spheres and the ruler dragged through the
  frame loop from a proven-idle baseline, x and y of the ruler separately; every view idle while
  nothing runs; the fall released, paused, ended at contact at two frame phases; reset all against
  disturbed state); mutation sweep 68 caught of 68 (52 physics, 16 UI), run on a copy in
  `build/gravity-force-lab/_out/`; display-list audit 0 problems over 15 captures; every PNG looked at.
- **Where this differs from PhET, deliberately:** G is CODATA 2022 (PhET's 6.67408e-11 is CODATA
  2014, so its forces read 3.3e-5 lower; the readout prints PhET's number too). Arrows are
  proportional to the force at a printed scale (PhET's is a two-piece linear map with a floor).
  No pullers, sounds or screen-reader descriptions.
### Fixed (during the build)
- **A readout pin failed on correct code.** G m₁m₂/r² at the defaults is 1.6685749999999998e-7, one
  ulp under a rounding tie, and reads "0.000 000 166 857" at 12 decimals in both Python and JS. The
  test had retyped the literal 1.668575e-7, which is one ulp over the tie and reads "…858". The pin
  now comes off the model's own double, and the literal's reading is asserted as the contrast.
- **53 layout failures on the first sweep, five causes:** tick labels like "1.0 × 10⁻⁸" ran into the
  rotated axis title 40 px left of the frame (axes are now in units of 10ⁿ, named in the title);
  plot views drawn with no bottom row on a narrow stage left the main axes 16 px for their labels
  (one bottom row is kept there); labels clamped to the canvas slid past the plot frame (`labIn`);
  the ruler, slid right, ran under the floating readout (it is cut at the stage box); and the scale
  row's note was not budgeted (its lines are reserved from the longest note at the widest scale).
- **A label the registry moved out of its spot landed on a tick number it could not see:** `axes()`
  registers nothing. `axesT` registers every tick label and both axis titles (the standard_model
  trap).
- **The fall view's band overflowed at 820×520:** one plot under it left a 157-px box for 217 px of
  fixed rows. On a narrow stage the band is drawn alone.
- **The readout said "falling" after contact:** it refreshed every tenth frame, and nothing advances
  after the last step. The ending step now refreshes it, and the UI test ends the run at two frame
  phases (3 apart mod 10) so it cannot pass by luck.
- **Seen in the PNGs:** the distance label sat on the ruler's edge; the lower-left legend of the mass
  product was missing (the legend placer tests each segment's bounding box, and a two-point line's
  box is the whole panel); the live label was written across its own hyperbola; the centre-of-mass
  marker was painted under the sphere it lay inside; ticks read "2.00" and "0.50".
- **`hms` truncated minutes:** 43795.8 s printed 12 h 09 min; it rounds to the minute now.
- **Four test blind spots found while drafting mutants, before the sweep:** the arrow ladder's "2"
  rung was unpinned; the inverse-cube comparison was checked only as a ratio, where a wrong power
  cancels; the mass-rounding test used 454, where floor and round agree (now 456); the UI's "other
  views ignore the pointer" clicked empty stage (now it presses where m₁ sits in the lab).
- **The house `#hint` sat on the caption's last line** (the wave-on-a-string finding): every view lays
  out to H − 18 and the layout sweep asserts no canvas text enters the hint's corner; the 18-px
  loss then crowded 1-2-5 log ticks on short panels, which now fall back to decades below 14 px.
- **A global `axesR → axesT` sed rewrote the call inside `axesT` itself** (unbounded recursion);
  caught before the first run.
### Known-bad candidates
- **A readout string pinned off a retyped literal can sit on the other side of a rounding tie from
  the model's own double.** Pin decimal strings off the value the model computes.
- **`legendAuto` treats a two-point straight line as covering its whole panel,** because it tests
  segment bounding boxes: no corner is ever free. Sample straight lines finely.
- **A readout refreshed every Nth frame goes stale when a run ends between refreshes.** Refresh on
  the ending step, and test the end at two frame phases.
- **"This view ignores the pointer" must be tested where the object sits in the view that accepts
  it;** a press on empty stage cannot see a missing view guard.
- **`stageLayout` with no bottom row gives the main plot 16 px below for tick labels and the axis
  title,** which the caption then overlaps. Keep a bottom row or budget the labels.

## 2026-09-18 — projectile-motion: PhET's four screens in the house style, drag checked three ways, the envelope and the hodograph

### Added
- `projectile-motion.html`, a clean-room remake of PhET's Projectile Motion
  (1.0.34, CC-BY 4.0; new code, no PhET code or assets). Six views: **the
  launch** (PhET's Intro: the cannon on its pedestal, the nine projectiles,
  a target that scores 1–3 stars, the tape measure, the data probe on the
  0.1-s dots), **the vectors** (PhET's Vectors: velocity, acceleration and
  force, total or in components, plus a 0.5-s strobe along the shot),
  **the drag** (PhET's Drag: C_d with its body drawn from streamlined to
  flat-faced, diameter, mass, altitude, the same shot in vacuum beside it),
  **the lab** (PhET's Lab: every projectile or a custom one, gravity 5–20,
  altitude, air), **the envelope** (every shot at one speed, the parabola
  of safety, R(θ) with both optimum angles) and **the hodograph** (the
  velocity path, its exact closed form, the approach to (0, −v_t), speed
  and the energy ledger).
- Exact: every vacuum quantity in closed form (range, apex, time of flight,
  landing speed √(v0² + 2gh), tan θ* = v0/√(v0² + 2gh), the envelope
  y = h + v0²/2g − gx²/2v0²); the integrator reproduces them to 1e-11 over
  324 launches because RK4 is exact on a quadratic in t.
- Quadratic drag: RK4 at h = min(2 ms, 0.005/(k|v|)), steps cut onto every
  0.1-s dot, apex and ground by bisecting the partial step, the energy the
  air takes integrated as a fifth state inside the same stages. Checked
  against (1) its Python twin in `build/projectile-motion/derive.py`
  (1e-12, identical step counts), (2) scipy solve_ivp DOP853 at rtol 1e-13
  (worst 2.8e-11 over PhET's parameter box), (3) the EXACT hodograph of
  quadratic drag 1/u² = 1/u0² + (k/g)[F(θ) − F(φ)], F = sin/cos² +
  ln tan(π/4 + φ/2), integrated in the page by Gauss–Legendre (nodes by
  Newton, pinned to numpy) and in derive.py by scipy quad — the two
  routes agree with DOP853 to 6e-14 — and (4) the vertical closed forms
  (tan, tanh, ln cosh; 7.6e-12). Limits: drag → 0 approaches the vacuum
  range at exactly the first-order rate dR/dk (a perturbation integral;
  the departure falls tenfold per decade of k), and a 20-s fall sits
  1.1e-9 below v_t = √(2mg/ρC_dA).
- PhET's values read out of the original: the nine projectiles' mass,
  diameter and C_d, their Lab ranges, g = 9.81, the launch/altitude/
  gravity ranges, the target (15 m, 3 m, stars inside W/6, W/3, W/2),
  dots every 0.1 s and 1 s, three in flight, five paths, slow ×0.33, and
  NASA Glenn's air-density fit (1.2266 kg/m³ at sea level, 0.13 % above
  the ISA; 0.21 % at 5 km). PhET's per-screen defaults, except the Vectors
  view (velocity and acceleration on, strobe on) and the analysis views
  (baseball, 30 m/s, air on), so each view shows its subject at load.
- Suites: selfTest 1439 passed, 0 failed (osascript, 2.2 s; every
  reference is a line of derive.py's printed output, pulled in by
  gen_refs.py, never retyped); UI drive 275 passed, 0 failed (every tab,
  slider, checkbox and chip; the barrel, pedestal, target, tape and probe
  drags each move the drawing through the frame loop from a proven-idle
  baseline; wheel, keyboard, reset, a mid-flight air change); mutation
  sweep 67 of 67 caught (49 physics, 18 UI), 0 survived, 0 skipped, run on
  a copy in build/projectile-motion/_out/. Display lists: 27 captures,
  `tools/audit.py` 0 layout problems, every PNG looked at.

### Fixed (during the build)
- **Tick labels collided in small and degenerate plots** (the inline layout
  sweep's first run: 8 collisions, at 560×380 and on a vertical launch at
  every size). Cause: `axes()` asked
  for a fixed tick count whatever the box's pixel size, and never
  registered its tick labels, so marker labels placed later could not
  dodge them. `axes()` now caps ticks at one per 48 px (x) / 26 px (y) and
  pushes every tick label into the LABELS registry.
- **The hodograph's window collapsed to a sliver for a vertical launch**
  (vx ≡ 0): one scale on both axes makes the box a few pixels wide. The
  window now keeps a minimum aspect (x span ≥ 0.45 × y span and vice versa).
- **Vector arrows ran off the stage and across the caption** (seen only in
  the PNGs): arrows are drawn in pixels, and the strobe's launch-point
  acceleration arrow (95 px, pointing down from ground level) was never
  clipped. Arrows are now cut at the scene box and the cut is marked by a
  bar instead of a head, so a clipped arrow cannot pass for a short one
  (asserted); the strobe starts at 0.5 s, where the cannon is not.
- **The 796-m/s tank shell stretched the hodograph 30× past its flight**:
  "fly on past the ground to 3 v_t/g" ran 40 s of near free fall. The
  continuation now runs only when v_t is reachable (3 v_t/g ≤ 25 s), and
  otherwise says v_t is off the plot (asserted both ways).
- **The target painted over the ruler at zoom 2** (it was drawn after the
  labels and grew with the scale to 32 px tall): drawn first, flattened to
  at most 7 px. **The 0.1-s dots were invisible** on their own path (same
  colour): drawn 60 % toward white. **Colinear mg and a_y hid each other**:
  forces start 5 px to the side. **The C_d icon's tail ran off the canvas**
  at C_d = 0.04: smaller and anchored by its tail. **The hodograph plane
  was squeezed to ~130 px** under two plots: it now takes the full height
  with the time plots stacked beside it. **A six-line caption** took the
  narrow stage: the scene takes the short caption below 310 px of room.
- **The envelope's caption said every vacuum shot touches the parabola of
  safety.** Only shots steeper than the best angle touch it above ground;
  the flatter ones land first (which the test already asserted). Reworded.
- **The UI floors and one readout check were guesses** (op floors of 40/
  120 against measured 35/105; a landing speed the hodograph readout never
  printed): floors re-derived from the measured t = 0 emission, the row
  added.
- **Mutation survivor: dropping the "a bent path takes no new shots" guard
  changed nothing any test could see.** The code was right; the test was
  vacuous. It fired again while the air was still off, so the new shot's
  launch key already differed from the bent path's and the `!last.changed`
  guard was never consulted. The guard only matters once the conditions
  are RESTORED (air off mid-flight, the shot lands, air back on, fire the
  identical shot); the test now does exactly that and the mutant fails it.
- **Dead code that made mutants equivalent, removed before the sweep**: a
  0.2-m floor on the probe radius that no zoom can reach, and a dirty flag
  on pointer-down (a grab changes nothing on screen).

### Known-bad candidates
- **An arrow drawn in pixels escapes every data-space clip.** `polyline()`
  clips curves in data space, but vector arrows (velocity, acceleration,
  force) are drawn in screen pixels at a fixed px-per-unit scale, so near
  the ground an acceleration arrow runs through the ruler, the caption and
  off the canvas — and the text audit cannot see it. Clip arrows to the
  stage box and mark the cut (a bar, no head).
- **A fixed tick count is a collision at a small box.** Derive the count
  from the box's pixels, and register tick labels with the label registry
  so later labels dodge them; a one-scale-on-both-axes box needs a minimum
  aspect or a degenerate case (vx ≡ 0) renders as a sliver.
- **A continuation that shows an asymptote must check the asymptote is in
  reach.** "Fly on for 3 v_t/g" is 13 s for a baseball and 243 s for a
  tank shell; the latter turned the whole plot into free fall. Decide
  reachability first and say so when it is not.
- **A guard against re-joining a changed state is only tested with the
  state restored.** A dedup rule "identical shots share a path unless the
  path was bent in mid-air" survived a sweep because the test fired while
  the bending condition still held, so the keys differed anyway. Restore
  the condition first, then assert the guard.
- **Tangency to an envelope is not "every member touches it".** Members
  flatter than the optimum touch the parabola of safety below the ground,
  i.e. never. Assert the split (steep ones touch, flat ones land first),
  and word the caption the same way.

## 2026-09-18 — wave-on-a-string: PhET's bead lattice exactly, with d'Alembert's images, the resonances, and a dispersion relation that is a straight line
### Added
- `wave-on-a-string.html` (162 KB), a remake of PhET's Wave on a String 1.2.4 in five views:
  *the string*, *the space-time*, *the reflections*, *the standing waves*, *the dispersion*.
  Credit line in the header and on the page; site nav absolute; no network.
- *The string* is PhET's one screen, with every control its inventory lists:
  - the wrench (manual; dragged on the canvas or with ↑↓, stopping at ±1.3 cm, and pressing
    play as PhET's does);
  - the oscillator, drawn as a scotch yoke whose pin sits exactly at A sin 2πft;
  - the pulse generator (click it, press p, or use the button);
  - fixed end, loose end (a ring on a pole) and no end (a window);
  - amplitude, frequency, pulse width, damping and tension;
  - rulers (10 cm and 5 cm, mm ticks), the stopwatch and the reference line, all draggable;
  - normal and slow motion (×0.25), play/pause, step, restart string and reset all.
  The drawing is at true aspect, with every tenth bead marked.
- **The model is PhET's**, read out of the build (and matching its `doc/model.md`):
  - 61 beads 0.125 cm apart;
  - the leapfrog `(1+β)yᵢⁿ⁺¹ = (β−1)yᵢⁿ⁻¹ + 2(1−α²)yᵢⁿ + α²(yᵢ₊₁ⁿ + yᵢ₋₁ⁿ)` at a Courant
    number held at exactly 1, so the tension sets the clock (Δt = Δx/v) and never the stencil;
  - β = 0.1 × damping per step;
  - the end rules y₆₀ = 0, y₆₀ = y₅₉ and y₆₀ⁿ⁺¹ = y₅₉ⁿ, including PhET's re-assertion of
    the end on the current level before each update.
- *The space-time* records the last 240 levels of that string (two round trips) as a green/cyan
  picture in x and t, with the characteristics x ± vt drawn over it: d'Alembert's two sliding
  shapes as stripes, inverted in colour on their way back from the clamp.
- *The reflections* feeds one pulse into all three ends at once, undamped and in whole steps.
  The image construction (the incident pulse running on into a shaded mirror world, its image
  running out, their sum as an orange halo round the lattice) shows why the clamp inverts, why
  the ring does not, and why the loose end's mirror sits at bead 59½.
- *The standing waves* sweeps PhET's 0–3 Hz with the exact steady response of the damped lattice,
  the largest |Y| on the string over A, against the undamped curve that diverges at every fₙ.
  Drag the panel to set f. Below it, the lattice is driven from rest and grows into the exact
  envelope, with nodes marked and the transient printed.
- *The dispersion* sets the lattice's ω(k) at a chosen Courant number α beside the continuum
  (ω = vk) and a real bead chain (ω = (2v/Δx) sin(kΔx/2)). It adds phase and group speeds, and one
  pulse after 5.4 cm on each. PhET's α = 1 is exactly ω = vk: its beads carry a continuous string
  and never disperse. α → 0 is the chain.
- **Exact:**
  - at α = 1 and no damping the lattice is d'Alembert's image series sampled at the beads (below
    1e-13 for all three ends, at two parameter sets, one incommensurate);
  - a damped mode keeps √((1−β)/(1+β)) = e^(−atanh β) per step;
  - the dispersion roots against `numpy.roots` and lattice runs, and v_g against a numerical
    derivative;
  - the driven steady state three ways: closed form, a complex tridiagonal solve and brute-force
    runs of thousands of steps, all agreeing to within 3e-11;
  - the resonances nv/2L and (2n−1)v/4L′ (L′ = 7.4375 cm);
  - the peak height 1/(Nβ) as β → 0 (166.67 A at β = 1e-4);
  - the no-end leak |r| = |zλ−1|/|λ(λ−z)| (5.4 % at the defaults);
  - the chain limit, O(α²) (error ratio 100.01).

  Every reference value comes from `build/wave-on-a-string/derive.py` → `refvals.txt`, read in
  full.
- **Verification:**
  - selfTest: 1075 passed, 0 failed under osascript (1.8 s). It includes a layout sweep of
    29 configurations × 4 canvas sizes.
  - UI drive: 199 passed, 0 failed. Every drag (wrench, both rulers, reference line,
    stopwatch, the response panel) is tested through the frame loop from a proven-idle baseline,
    and every reset against a sentinel.
  - Mutation sweep: 66 caught of 66 (55 physics, 11 UI), none survived or skipped. It ran on a
    copy in `build/wave-on-a-string/_out/`.
  - Audit: 0 layout problems at 1400×820 and at 820×520. The narrow size shows only the usual
    under-readout advisory.
  - Every captured view (21 + 5 narrow) was looked at.
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - Tension: PhET's relative slider (0.2–0.8) maps √T affinely onto 10–50 steps a second, 5:1 in
    speed over 4:1 in tension. The remake keeps PhET's 1.25–6.25 cm/s and makes it the law
    v ∝ √T, so its slider runs 0.032–0.8.
  - The driver is evaluated at each lattice time, where PhET uses a 0.02-s tick.
  - The standing-wave and reflection views run their own lattices.
  - Tools are dragged with the mouse only (PhET also drags them by keyboard). The stopwatch's
    buttons are in the panel.
  - No sounds and no a11y descriptions.
### Fixed (during the build)
- **The live clock fell a step behind.** One second of 1/60-s frames gave 49 lattice steps, not
  50. `while(acc >= Δt)` met an `acc` of 0.019999… after the frame sums rounded. The loop now
  carries a relative guard (`STEP_TOL`), and the 50-step second is asserted.
- **The readout read the global state, not its model.** A no-end model rendered after the state
  moved on printed the fixed-end rows. `buildModel()` now snapshots the state, and the readout
  and tag read `M.st`.
- **The dispersion view's "exact" pulse comparison was off by 0.40 cm at α = 1.** That was the
  damping, not dispersion: the long lattice ran with the global β. The pulses now run undamped,
  so only the dispersion changes their shape.
- **The exact solution was invisible wherever it was right.** The d'Alembert sum, the continuum
  line and the exact pulse lay exactly under the green lattice, so "they agree" read as "the
  reference is missing". The sum is now an opaque orange halo under the lattice, and the
  continuum and the exact pulse are dashed on top.
- **Two layout problems in the string view:**
  - the vertical ruler's default position covered the oscillator disc, so the world's left
    margin was widened to hold it;
  - the 10-cm ruler's labels ran off an 820-px canvas, and the reference-line label met the
    stopwatch at 560 px. Off-canvas labels are skipped, and the stopwatch box is registered
    before any label is placed.
- **The space-time stripes barely tilted.** With 360 rows they sat at about 5°. The tilt is fixed
  by rows per transit, not by the tension, so the record now keeps 240 rows (about 7°). It also
  says so when it is empty rather than printing "the last 0 steps".
- **The open end's flat response lay on the panel's bottom frame,** because the log axis started
  at exactly 1. The axis now starts at 0.5, and the panel says there are no resonances.
- **The narrow dispersion caption described a speeds panel the narrow layout does not draw.** The
  narrow layout now has its own caption.
- **Seven tests could not fail where they needed to, all found by the mutation sweep or by
  checking each mutant against the suite before the sweep:**
  - the interpolation probe sat at a bead the wave front had not reached (both levels were 0);
  - the node test sat at the third harmonic, where bead 19 is at 15.6 %, just over the 15 %
    threshold. The first and second harmonics now separate the mutant;
  - the end rule's pre-update acts only on the step after a switch. `derive.py` now runs a
    mid-run fixed-to-loose switch: y₅₉ = −1.14 with the pre-update, −1.26 without;
  - `csqrt`'s branch sign was invisible through the |λ| > 1 inversion. Its own contract is now
    pinned;
  - the pulse start was only ever tested at a whole step;
  - the dispersion view's β → αβ scaling and its α ≠ 1 oscillator k were unpinned;
  - a tautological `…||true` UI assertion.
- **Three prose claims were tighter than measured.** "1e-11" is 3e-11 measured; "1e-14" is
  1.07e-14; "within 0.3 %" for the α = 0.05 chain is α²/6 = 0.04 %, now asserted.
- **A global `axesR → axesT` rename rewrote the call inside `axesT` itself** (unbounded
  recursion). It was caught before the first run.
### Known-bad candidates
- **The house `#hint` sits on the last line of every bottom-anchored canvas caption.**
  `#hint{bottom:11px}` and `capFit`'s `capY = H − 12 − 14·lines` put the two in the same pixels
  at the stage's bottom-left. This holds in buoyancy, lagrange_points, brachistochrone and every
  sim built from the same scaffold. The display-list capture cannot see it, because the hint is
  HTML. This file reserves 18 px (`HINT_H`) and asserts that no canvas text enters the hint's
  corner: 116 checks fail with `HINT_H = 0`.
- **PhET's lattice is not a bead chain, and it must not be "corrected" into one.** At Courant
  number 1 the leapfrog's time error cancels the beads' space error, so ω = vk at every k up to
  the zone edge. A real chain of the same beads is dispersive: a 0.75-cm triangle on it is 0.05 cm
  out of shape after 5.6 cm, with ripples trailing behind.
- **PhET's loose end reflects about bead 59½, not bead 60.** y₆₀ = y₅₉ is a first-order free end.
  The loose resonances are (2n−1)v/4L′ with L′ = 7.4375 cm, and an image construction mirrored
  at 7.5 cm is wrong by 0.06 cm at the default pulse.
- **PhET's tension slider is not v ∝ √T:** its 0.2–0.8 maps affinely in √T onto 10–50 steps/s.
- **PhET's damping is per lattice step.** So its rate per second scales with v (b = 2βv/Δx),
  while the decay per bead travelled, e^(−atanh β), does not. The damped lattice is a
  telegrapher: it is overdamped where sin kΔx < β, and its "no end" leaks |r| ≈ β/(2 sin ωΔt),
  5.4 % at PhET's defaults. That is PhET's own "greatly reduces but does not perfectly
  eliminate".
- **`while(acc >= dt)` in a frame clock loses a step to rounding.** Guard it with a relative
  tolerance.
- **An exact reference drawn under the curve it matches disappears.** Draw it as a halo underneath
  or dashed on top.

## 2026-09-18 — blackbody-spectrum: Planck's curve with PhET's thermometer, zoom, Graph Values and star, plus the colour two ways, Wien's peak, the Stefan–Boltzmann area and the classical limits
### Added
- `blackbody-spectrum.html` (160 KB), a remake of PhET's Blackbody Spectrum 1.0.26 in five views:
  *the spectrum*, *the star*, *the peak*, *the total*, *the limits*. Credit line in the header and
  on the page; site nav absolute; no network.
- *The spectrum* is PhET's one screen. It has every control PhET's has:
  - the thermometer (200–11000 K, snapping to 50 K), draggable on the canvas and mirrored by a
    slider, with PhET's presets as chips (Earth 250 K, Light Bulb 3000 K, Sun 5800 K,
    Sirius A 9950 K);
  - PhET's zoom ladders (wavelength ×2 from 0.75 to 48 µm, power ×5 from 1.024×10⁻⁵ to
    2500 MW/m²/µm), whose buttons disable at the ends;
  - Graph Values: a point dragged along the curve. As in PhET, it is clamped to the axis, hidden
    past it, sent back to the peak on every temperature change and whenever it is switched on,
    and it shows cue arrows until the first drag;
  - Labels: X-ray, ultraviolet, visible and infrared, cut at 10 nm, 380 nm, 780 nm and 100 µm.
    As PhET does, a band is named only where it is at least 20 px wide;
  - Intensity: the shaded area, σT⁴;
  - two saved curves;
  - the star with PhET's B/G/R photometer and halo.

  House additions: Wien's peak marker, a "fit the axes" button, the share of σT⁴ inside the
  window, and zoom warnings printed on the canvas.
- *The star* sets PhET's photometer, reproduced exactly (the curve sampled at 650, 550 and
  450 nm, divided by the largest of the three, dimmed by min(1, 0.02√(T − 798 K))), against
  CIE 1931 colorimetry over the CIE's own table. It adds strips over the whole thermometer, the
  three channels against T, and the luminous efficacy (at most 95.43 lm/W, at 6628 K).
- *The peak* shows the family on log–log axes with the locus of the peaks (slope −5). Divided by
  their own peaks, all the curves collapse onto one universal curve (half maximum from 0.613 to
  1.817 λ_max), and B_ν peaks at 1.760 λ_max.
- *The total* plots σT⁴ against T (slope 4), matched by a 1024-point Gauss–Legendre integral of
  the curve, and the band budget: the Sun puts 46.6 % into the visible, a 3000 K filament
  12.7 %, and Sirius A puts 44.0 % into the ultraviolet.
- *The limits* sets Rayleigh–Jeans and Wien against Planck, with each law's ratio to Planck:
  (eˣ − 1)/x and 1 − e⁻ˣ. At the peak, Rayleigh–Jeans is 28.66 times too high and Wien's law
  0.70 % low. Each is within 1 % of Planck on one side only: x < 0.019868 for Rayleigh–Jeans,
  x > ln 100 for Wien.
- **Exact:**
  - h, c and k are the exact SI values. c₁, c₂, σ, b and ν_max/T are derived from them and equal
    scipy.constants (CODATA 2022) to the last digit.
  - x₅ and x₃ are checked against Lambert W and against Newton's method in 50-digit arithmetic.
  - 75 values of M_λ are checked against 50-digit decimal arithmetic, to 1e-14 × max(10, hc/λkT).
  - The band fractions come from two series joined at x = 2. The Bernoulli head series takes its
    coefficients from power-series division, pinned to exact rationals. The exponential tail
    series is the other. Both are checked against scipy quad, exact rationals and 50-digit
    series.
  - σT⁴ agrees with scipy quad to 4e-16 and with Gauss–Legendre to 2e-14.
  - Chromaticities are sums over the CIE table.
  - The Illuminant A chain: a Planck body at 2855.496 K reproduces the CIE's A table to its
    printed precision (4.8e-6) and its chromaticity to 4e-8.
- **Verification:**
  - selfTest: 1035 passed, 0 failed under osascript.
  - UI drive: 160 passed, 0 failed.
  - Mutation sweep: 78 caught of 78 (65 physics, 13 UI), none survived or skipped.
  - Audit: 0 layout problems at 1400×820 and 1100×700. At 560×380 it reports only the
    under-readout advisory that every house sim shows there.
  - Every view's PNG was looked at.
- **Sources:**
  - `build/blackbody-spectrum/CIE_xyz_1931_2deg.csv` (with its metadata) and
    `CIE_std_illum_A_1nm.csv`, fetched from files.cie.co.at. Every fifth row of the first is
    embedded verbatim by `derive.py`.
  - PhET's constants, read from `docs/phets/blackbody-spectrum_en.html`. PhET's own c₁, c₂, σ and
    b differ from CODATA by +4.0e-5, −4.8e-6, −2.5e-7 and +3.6e-7. This file uses CODATA
    throughout.
### Fixed (during the build)
- **The reference for the thin band beyond 100 µm was wrong.** The JS disagreed with it by 1e-11
  to 3e-10. The cause was in `derive.py`: it converted the 50-digit F to float before computing
  1 − F, which keeps about 6 of the 15 digits of a 10⁻⁷ share. The JS, which evaluates the share
  directly from the head series, was the accurate one. The subtraction now happens in Decimal,
  and the exact-rational head series agrees to 3e-16.
- **The 50-digit tail series in `derive.py` was truncated.** Capped at 4000 terms, it was wrong
  by 1e-12 at x = 0.001, where it needs about 36/x terms. The number of terms now follows x.
- **The join of the two series is not a free choice.** I had expected any join between about
  0.02 and 6 to be an equivalent mutant. Measuring it (`join_window.py`) showed that x = 2 is
  pinned from both sides:
  - below it, the complementary route 1 − tail loses digits on thin long-wavelength shares (a
    join at 0.5 fails at 4.9e-14);
  - above it, the head series' truncation shows (a join at 4 fails at 1.4e-13).
- **Tick labels collided at the origin** ("0.0" against "0") in the spectrum and limits views:
  the bottom y tick and the left x tick overlapped by about 1 px under the audit's half-pixel
  rule. The bottom y tick is now dropped wherever an x tick sits at the left edge.
- **Labels of curves off the top of the axis landed on the frame.** They were crossed by the
  band-edge ticks and pushed the band labels down into the plot. Now the band labels claim their
  row first, a curve off the top is labelled just inside the frame, and every curve label is
  placed by `labAvoid`. That is a Liang–Barsky segment–box test against each drawn curve and
  against the Graph Values lines, which are now drawn before the labels.
- **Axis maxima printed with significant-figure padding** ("0–3.00 µm by 0–100.0").
  `axisMax()` prints the ladder value instead: 3, 0.75, 5.12×10⁻⁵.
- **The INFO prose called the Earth's peak "a hundred-thousandth" of the Sun's.**
  (250/5800)⁵ = 1.5×10⁻⁷, about a seven-millionth.
- **A reference value from mental arithmetic** (x₅/x₃ = 1.7597810788957716) was replaced by a
  printed one (x₃/x₅ = 0.5682526605497431) before its first run.
- **The first substance floors were guesses** (8, 8 and 4 fills), and they failed correct views:
  the limits view has one fill, and its substance is curves. The floors are now per
  configuration, on fills plus strokes, curve segments and texts, at 80 % of what each
  configuration emits (`set_floors.py`).
- **The CIE glow read as a target.** It was five nested translucent discs; it is now one flat
  halo in PhET's own style.
- **A tautological assertion (`…||true`) got into the UI drive.** It was caught before it ran,
  removed, and replaced by a real repaint check.
- **The first sweep left three survivors, all test gaps.** All three are caught on re-run:
  - "fit frames 4 λ_max": at every preset, 4 λ_max and 5 λ_max round up to the same ladder step.
    4500 K separates them.
  - "Graph Values shown past the axis": the test point, at 2000 nm on a 750 nm axis, was beyond
    even the mutant's doubled limit. A point at 800 nm separates them.
  - "the Graph Values checkbox does not re-centre": the point was already at the peak when the
    checkbox fired. A sentinel is now set immediately before the action.
- **`tools/mutate.py` writes its scratch `_mutant.js` next to the HTML it tests,** and several
  agents build into `docs/phets_revised/` at once. The sweep therefore ran on a copy inside
  `build/blackbody-spectrum/_out/`.
### Known-bad candidates
- **The house CMF fit has a red tail that falls 12 to 60 times too fast beyond 700 nm.** This is
  the Wyman–Sloan–Shirley fit (2013) in `diffraction.html` and `blackbody_radiation.html`. Its
  x̄/ȳ is 1.317, 0.228 and 0.048 at 700, 750 and 780 nm, where the CIE table's is a constant
  2.769. A Planck body therefore comes out greener than it is: Δx = −0.018 at 800 K, −0.011 at
  1000 K, −0.004 at 1500 K and −0.001 at 3000 K. That is why `blackbody_radiation.html` needs a
  700 K colour floor. The CIE table itself, every fifth row, is 95 rows and 5 KB.
- **Three samples of a spectrum are not a colour.** PhET's photometer paints the Sun at 5800 K
  cyan-white (223, 255, 253), where colorimetry gives warm white (255, 241, 235). It paints a
  3000 K filament (239, 144, 56), where the eye sees (255, 184, 109). Any scheme that colours by
  sampling the spectrum exaggerates saturation.
- **`255·a·v/r` with v === r is not always 255 in floating point.** PhET's star floors its
  brightest channel to 254 at 4000 K and 11000 K. Pin the value before the floor and accept 254
  or 255; pinning the floored channel pins rounding luck.
- **A reference share computed as 1 − F from a float F keeps about 6 digits of a 10⁻⁷ number.**
  Subtract at high precision, then convert.
- **`tools/mutate.py` puts its scratch file beside the HTML under test,** so concurrent sweeps in
  one directory race on it. Sweep a copy inside your own build dir.
- **PhET's Blackbody Spectrum 1.0.26 has no ruler.** Its ScreenView adds only the graph, the
  control panel, the saved-graphs panel, the thermometer and its labels, the B/G/R star display
  and reset. Its "peak marker" is the Graph Values point, which PhET sends to the peak on every
  temperature change.

## 2026-09-18 — the kit: survey of the originals, the brief, the build layout
### Added
- `build/_survey/survey.py` → `inventory.json`: title, version, screens and
  every English UI label of all 46 originals, read from the embedded
  `phet.chipper.strings` table. Older builds store it as JSON; newer ones as a
  one-line self-decoding function, which the survey evaluates alone in
  JavaScriptCore (only that statement, never the sim). Shared-repo labels
  (e.g. `BEERS_LAW_LAB` for `concentration`) are kept, framework repos
  (JOIST, SUN, SCENERY_PHET, …) and a11y/help text dropped.
- `build/BRIEF.md`: the one brief all build jobs follow (house form and
  aesthetic by extraction, absolute site-nav links, clean-room credit line,
  the four verification layers, no git writes by build agents).
