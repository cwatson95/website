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
