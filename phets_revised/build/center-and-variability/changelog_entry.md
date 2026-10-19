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
