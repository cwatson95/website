## 2026-09-22 — gravity-and-orbits: four systems and one inverse-square law, drawn big enough to see and then drawn true

### Added
- `docs/phets_revised/gravity-and-orbits.html` — a clean-room remake of PhET
  Interactive Simulations' **Gravity and Orbits** (1.6.28; CC-BY 4.0,
  University of Colorado Boulder). New code; no PhET code or assets. Five
  views: *the model*, *to scale*, *the circular orbit*, *the exact orbit*,
  *what is conserved*. Build dir `build/gravity-and-orbits/`; Python twin
  `derive.py`; the engine, the utilities and the 2-D layer are read from
  `build/keplers-laws/` by `assemble.py`, so the three sims of this family
  (keplers-laws, my-solar-system, gravity-and-orbits) share one solver.
- **PhET's two screens are the first two views.** The Model screen with its
  four systems (Sun and Planet, Sun Planet and Moon, Planet and Moon, Planet
  and Space Station), the gravity switch, the half-to-double mass sliders,
  the velocity and gravity-force arrows, the path, the grid, the measuring
  tape, the mass readout and the clock in Earth days (Earth minutes on the
  station scene). To Scale is the same four with every radius true.
- **What is exact**, all asserted against `derive.py`:
  - v = √(GM/r) and T = 2π√(r³/GM) at all three real radii to 1e-14, each
    also re-derived from `m v²/r = GMm/r²` and from `2πr/v`.
  - Kepler's third law, with the masses in it: T²/a³ = 4π²/G(M+m) to 1e-13
    for both Earth satellites, so the space station's constant is 1.23 %
    larger than the Moon's — a bigger total mass gives a smaller constant —
    and that 1.23 % is exactly the Moon's own mass as a fraction of the
    Earth's. (That (T_m/T_s)² = (r_m/r_s)³ for two circular
    orbits about the same mass is an *identity* of T = 2π√(r³/GM), not a
    measurement; it is asserted, and labelled as the identity it is.)
  - Each period is separately measured by integrating the orbit until it
    closes, and agrees with the Kepler period to 2e-9.
  - Every two-body run tracks the closed-form Kepler solution — elements from
    the state vector, then E − e sin E = M by safeguarded Newton to 1e-15 in
    the step. After 400 frames the integration is 2.5e-12 of r from Kepler on
    the Sun–Earth scene and 1.6e-8 of r on the station scene; `derive.py`
    checks both against scipy's `brentq` and `solve_ivp` (DOP853, rtol 1e-13).
  - **Gravity off is exactly a drift:** one frame is bit-for-bit
    `r + v dt`, 600 frames change no speed **at all** (asserted `=== 0`, not
    "small"), and the path leaves the straight line by ≤ 1.2e-14 of its own
    length. The gravity-on control leaves it by 0.3 of the distance travelled.
  - Momentum and angular momentum are conserved to rounding on the To Scale
    screen (|Δp|/p ≤ 8.7e-15, |ΔL/L| ≤ 1.3e-14 over 4,000 frames); the energy
    to |ΔE/E| ≤ 2.1e-10.
- **PhET's two deliberate distortions of the Model screen are kept and
  measured**, because they are its model: the star is nailed down, and in
  Sun-Planet-Moon the moon's pull from the planet is multiplied by 10,200
  **one-sidedly** (PhET's `adjustMoonOrbit`), so Newton's third law does not
  hold there. Measured: the drawn moon sits 23.85× its real distance at 21×
  its real speed; a circular orbit there needs 214.5 m/s unboosted and
  21,662 m/s with the boost, and the boost that would make it exactly
  circular is 11,223, not 10,200. The one-sidedness costs 89 % of the
  momentum in 600 frames. The conservation view draws all of it.
- **PhET's data against the measurement**, both columns on the page, each
  measured value at the precision its source prints (NASA planetary fact
  sheets; NASA's ISS Facts and Figures):
  - PhET's Moon radius is **1,727.4 km against the measured 1,737.4 km** —
    0.58 % low, and the shape of a transposed digit. Every other radius it
    ships is the fact-sheet value exactly.
  - Sun 1.989e30 vs 1.9884e30 kg (+0.030 %), Earth 5.9724e24 vs 5.9722e24
    (+0.0033 %), Moon mass and the 419,725-kg station exact, Sun and Earth
    radii exact, perihelion +0.0021 %, max speeds +0.033 % / exact.
  - PhET's own numbers give a year of 365.558 d (measured sidereal 365.256),
    a month of 27.249 d (27.3217) and a 91.45-min station orbit at 347.0 km,
    against NASA's "about 90 minutes" for a station nearer 420 km.
- **The integrator.** PEFRL (Omelyan, Mryglod & Folk 2002) — PhET's own
  choice, and its three coefficients are read out of PhET's build — four
  force evaluations a step, substepped so no step exceeds 0.02 of the
  shortest pairwise crossing or free-fall time. Its order is measured by
  halving the step: **4.00** against **1.00** for PhET's step as shipped,
  which carries the same coefficients but evaluates the acceleration once and
  reuses it for all four kicks (that composition is exactly
  r + vh + ½ah², v + ah). Over PhET's own 600 frames its energy drifts
  8.7e-3 against our 1.3e-13, and the two runs end 9.3e8 m apart.
- **PhET's own interface details, kept and asserted:** its mass readouts
  ("1 Earth mass", "333 thousand Earth masses", "14 billion billion Space
  Station masses") with its own thresholds; its rule that a body whose drawn
  diameter falls to 12 px or less gets a leader line and its name; its clock
  in Earth days and, on the station scene, Earth minutes; its 0.5–1.3 zoom;
  its 1/4/7 substeps a frame; its grid steps; and its Sun-Planet-Moon moon
  built with `massSettable` false, so that slider is dead there.
- Verification: `selfTest` **1,150 passed, 0 failed**; UI drive
  **194 passed, 0 failed**; 25 captured configurations through
  `tools/audit.py` (0 layout problems) and `tools/raster.py`, every PNG read.
  Mutation sweep, 99 mutants (84 physics, 15 UI): **88 caught, 11 survived**
  on the first full pass; every survivor was a missing assertion, all eleven
  are closed, and each was re-verified as caught on the final file.

### Fixed (during the build)
- **The order sweep measured saturation, not order, on the Model screen.**
  Symptom: the conservation view's title read "order: 3.99 vs 0.58" on
  Sun-Planet-Moon. Root cause: the sweep ran over a fixed 40 days, which is
  more than a whole *boosted* lunar orbit, so PhET's first-order step at 20
  steps was already wrong by the size of the system and its error stopped
  falling. Fix: the window is now a ninth of the closest pair's reference
  period (39.6 d for Sun-and-Planet, 3.2 d for the Model moon), which reads
  3.98 vs 1.00. `derive.py` pins both windows and both orders.
- **The `(derive)` reference errors for PEFRL flattened at N = 1600.**
  Symptom: measured order 1.573 on correct code, with ratios 16.0, 1.36,
  1.22. Root cause: positions are ~1.5e11 m, so one ulp is 3e-5 m and a
  25,600-step reference run random-walks to ~3e-3 m — which *is* PEFRL's own
  truncation error at N = 1600. The step counts are now 20–160, where every
  error is above 1 m, and the reason is written where the constants are.
- **A bar-chart label written across its own bar.** The "lengths on a log
  axis" panels put each label after the bar's end; a bar reaching 90 % of the
  axis leaves no room, `labIn` clamped it back inside the box, and it landed
  on the bar it names. Labels now go *above* their own bar, left-aligned at
  the frame.
- **The centre-of-mass label was written inside the Sun.** For a star and its
  planet the centre of mass is inside the star — and the Model screen's star
  is drawn 50× too big — so magenta text landed on a yellow disc. Pushed
  clear of the nearest body along the line between them (the same fix
  `my-solar-system.html` needed, for the same reason).
- **Notes drawn after `legendR` get dropped, not the legend.** `legendR`
  rejects a corner that covers a *registered label*, so a note drawn
  afterwards has no claim: on the Model conservation view both notes vanished
  entirely. The notes now go on first and the legend dodges them. They also
  pick the half of the box the curves are not in (measured from the current
  drift level), because on the Model screen the curves run along the top.
- **A UI-harness finder matching on a word drove the wrong control.**
  `findLabelledU('PhET')` matched the *gravity* checkbox ("gravity acts
  (PhET's on/off switch)") before the comparison one, so the test switched
  gravity off and then failed an assertion about the shadow integrator. Both
  finders now match the whole decoded label, never a substring.
- Three labels overflowed a 560-px canvas (the Model screen's
  bends-the-physics note, the three-body "no closed form" sentence, the
  central-body note in the circular-orbit view). Each now has a measured
  short form, or is split into two lines.
- The circular-orbit view drew its central body at 2.5 % of the *orbit*,
  which is one pixel once a near-escape conic widens the view six-fold. The
  floor is now 2.8 % of the *view*, and the factor it amounts to is printed.
- **Cutting gravity rewound the clock, which threw away the one thing the
  switch is for.** The toggle called `sysSaveStart`, which restores the start
  state — so a planet halfway round its orbit jumped back to the beginning
  instead of flying off along the tangent from where it was. Root cause: the
  straight-line residual needs an anchor, and the anchor was being taken by
  re-saving the whole start. Split apart: `coastAnchor` records position,
  velocity and speed at the instant gravity was cut, and nothing else moves.
  The UI drive now runs 200 frames, cuts gravity mid-orbit, and asserts the
  clock is unchanged, the planet has not moved, and it then leaves along the
  tangent *at the cut*.
- **The third-law statement was the wrong way round, and the suite caught
  it.** T²/a³ = 4π²/G(M+m), so a *bigger* total mass gives a *smaller*
  constant: it is the space station's constant that exceeds the Moon's by
  1.23 %, not the other way about. Written as the inverse, the assertion
  failed at 2.4e-2 — which is what an assertion against an absolute value is
  for.
- **Two analysis views opened on a degenerate axis.** Before the clock has
  run, the error, separation and drift panels have a time range of zero, and
  the tick formatter then prints six identical "0" labels along the bottom —
  the first thing a reader sees on those tabs. They now draw the frame and
  say what will appear there, and the order panel (which needs no run) is
  still drawn. `selfTest`'s layout sweep and the capture both gained a
  zero-frame configuration for each, so it cannot come back unseen.
- **A mutant that is caught can still stall the whole sweep.** `r³ → r²` in
  the step-limit's free-fall time asks for 74,000 substeps a frame; the suite
  caught it in its third section but does not abort on a failed assertion, so
  it ground on through 4,000-frame conservation runs for the best part of an
  hour. Four mutants were re-aimed so that every one of them makes the sim
  *faster*, not slower (the exponent up not down, the distance out not in,
  the step short not long).

- **The mutation sweep found eleven missing assertions and no wrong physics.**
  Each is now closed, and each was re-run individually against the final file
  to confirm it is caught:
  1. *the step limit's free-fall branch.* It takes the shorter of the crossing
     time `r/|dv|` and the free-fall time, and in **every** scene PhET ships
     the crossing time is the shorter one — so no shipped scene reaches the
     free-fall branch at all. It is reachable (drag a velocity arrow to zero)
     and is now pinned there, together with its r^(3/2) scaling.
  2. *the Planet-and-Moon hand split.* PhET computes it by hand **and** then
     calls `center()` on it, so a mutant on the hand split is undone by the
     centring. Pinned by its own contract instead: it already leaves zero
     momentum before the centring runs.
  3–4. *the two Earth-mass readout thresholds.* Nothing was ever evaluated
     between 1.01 and 1000 Earth masses, so both branch points could move
     freely. Pinned at 500, 1500 and 1.05 Earth masses.
  5. *the length units.* Only the unit **string** was checked, so the
     megametre's divisor could become 1e5. Each divisor now has its own value.
  6–7. *the two arrow scales.* The drawn length was compared against the
     constant that drew it — a tautology (the Prandtl-2/π trap again). Now
     against the literal 90 px and 60 px.
  8. *the reference speed.* Taking each body's own speed instead of its speed
     relative to the primary differs by the primary's recoil, 3e-6 here — far
     inside any pixel tolerance. Pinned against PhET's own typed speeds.
  9. *the dragging class.* Every pointer-move the harness fired carried
     `buttons: 1`, so the class that lets a drag survive a no-button move was
     never exercised. The harness now fires one.
  10. *the tab-selects-its-screen link.* Tested from the chips, never from the
     tabs.
  11. *the too-small-to-see pointer.* The check matched one canvas op reading
     `Earth` — which the **legend** also draws. It now requires two.
  One survivor was not an assertion at all: `dirty = true` in the
  pointer-down handler, redundant beside the `refresh()` on the same path.
  Removed, and the mutant retargeted at the `dragging` class, which is not.

### Known-bad candidates
- **A fixed window for an order sweep measures saturation on any system whose
  own timescale is shorter than the window.** A first-order method run at a
  step comparable to the orbit does not have an order at all — its error is
  bounded by the size of the system — and the measured slope then reports the
  bound. Scale the window to the system's own shortest reference period, and
  say in the code why the step counts are coarse.
- **A roundoff floor looks exactly like a wrong order.** At 1e11-metre
  coordinates one ulp is 3e-5 m, so any reference run of N steps carries
  ~√N ulps of noise; when the method's truncation error reaches that, the
  halving ratio collapses toward 1 on perfectly correct code. Check the error
  against the ulp scale before believing a measured order.
- **`legendR` dodges registered labels, so draw every label BEFORE the
  legend.** The existing Known-bad entry ("legendAuto avoids curves, not
  labels — draw the legend first and let labels dodge it") is the rule for
  `legendAuto`; `legendR` is the other way round, and following the older
  rule silently deletes the notes instead of moving the legend.
- **An identity of the formula is not a measurement, however many digits it
  agrees to.** `(T₁/T₂)² = (r₁/r₂)³` for two circular orbits about the same
  mass follows from `T = 2π√(r³/GM)` by algebra, so quoting twelve figures of
  agreement as "two orbits nothing else connects" is a rubber stamp. The
  measurable third law has the masses in it (`T²/a³ = 4π²/G(M+m)`), and the
  independent check is a period *measured by integrating the orbit*. Both are
  in the file now, and the identity is labelled as one.
- **A mutant that terminates can still stall a sweep, because the suite does
  not abort on a failed assertion.** `mutate.py` has no per-mutant timeout,
  and a mutant that makes the integrator take 10⁴ times as many substeps runs
  for an hour before reporting a mutant the suite caught in its first minute.
  Aim every mutant so that it makes the model *cheaper*: exponents up,
  distances out, steps shorter.
- **A branch that every shipped configuration misses is covered by nothing,
  and the `min()` of two timescales is exactly that shape.** The adaptive step
  takes `min(crossing time, free-fall time)`, and in all eight scenes here the
  crossing time is the smaller — so the free-fall exponent could be anything.
  Whenever a limit is a `min` or a `max`, find the state that selects the
  *other* argument and pin it there.
- **Comparing a drawing against the constant that drew it is a tautology.**
  `velScale(sys) * vRef(sys)` IS `VEL_PX` by construction, and so is the
  drawn arrow's length; both survived a halving of the constant. Measure the
  emitted geometry against a LITERAL.
- **A canvas-text check that matches one op matches whichever op comes
  first — and the legend draws body names too.** "the canvas names the Earth"
  passed with the too-small-to-see pointer deleted, because the legend entry
  also reads exactly `Earth`. Count the ops, or match on something only the
  feature under test emits.
- **Angular momentum about the origin loses four digits when the system sits
  1 AU away from it.** The Planet-and-Moon scene is built at the Earth's
  heliocentric position, so `x v_y − y v_x` is a large number minus a large
  number and |ΔL/L| reads 4.4e-12 where the same scene at the origin reads
  1e-14. That is the coordinate, not the physics — assert it at the tolerance
  the coordinate allows and say which is which.
