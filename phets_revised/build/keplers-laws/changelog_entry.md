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
