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
