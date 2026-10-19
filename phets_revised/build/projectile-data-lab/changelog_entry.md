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
