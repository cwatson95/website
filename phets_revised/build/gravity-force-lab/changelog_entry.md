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
