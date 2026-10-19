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
