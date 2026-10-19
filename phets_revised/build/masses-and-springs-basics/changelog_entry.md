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
