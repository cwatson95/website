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
