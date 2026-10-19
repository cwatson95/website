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
