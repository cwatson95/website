## 2026-09-22 — geometric-optics: PhET's lens and mirror benches, with the thin-optic equation solved exactly and every ray traced to agree with it

### Added

`docs/phets_revised/geometric-optics.html` (188 KB, six views), a clean-room
remake of PhET Interactive Simulations' **Geometric Optics** (build 1.3.16;
University of Colorado Boulder, CC-BY 4.0). New code; no PhET code or assets.

- **the lens bench** — PhET's Lens screen. Drag the object (pencil, penguin,
  star, arrow or a point light source) in front of a convex or concave lens;
  PhET's four ray modes (marginal, principal, many, none), F and 2F on both
  sides, a second point of interest, a virtual-image toggle, PhET's guides, the
  260 cm ruler, and — with the light source — the projection screen with its two
  light spots.
- **the mirror bench** — PhET's Mirror screen: concave, convex or flat, with F
  and 2F on the side the mirror actually has them (left for concave, right for
  convex, neither for flat — PhET's own `doc/model.md`).
- **the conjugate curve** — d_i against d_o as the rectangular hyperbola it is,
  with the asymptotes d_o = f and d_i = f, the magnification below it, and the
  pole at d_o = f where the equation has no answer.
- **the lens maker** — the (n, R) plane with the contours of f = R/2(n−1), which
  are straight lines through n = 1; PhET's two focal-length models and the
  hand-off between them; and the shape PhET's artwork draws against the sphere
  its numbers name.
- **the guides** — PhET's own construction, reproduced exactly and then measured.
- **the real lens** — the same index, radius and diameter built as two real
  spherical surfaces and traced with exact vector Snell.

**What is exact.** The thin-optic equation and everything that follows from it:
d_i = f d_o/(d_o − f) and m = −d_i/d_o are solved, and `selfTest` asserts the
residual 1/d_o + 1/d_i − 1/f against zero over 100 (f, d_o) pairs and against a
scipy `brentq` root of the same equation (3.4e-15 over 15 pairs); Newton's form
(d_o − f)(d_i − f) = f² holds to 4.5e-16 over 35 pairs. Ray tracing is not a
separate drawing: every outgoing ray is built from the one-line paraxial law
u′ = u − h/f, and the suite asserts that a ray leaving the object at **any**
height h on the optic lands on the image point the equation gives — worst
residual **1.79e-13 over 1200 configurations**, and that number is the lever arm
(at f = 80, d_o = 79.5 the image is 12 720 cm away), not the algebra. The three
principal rays meet at the image pairwise to **1.04e-15 over 360
configurations**. The lens maker's equation reduces to PhET's f = R/2(n−1) to
1.42e-16 over twenty (n, R) pairs. The light spot on the screen is the exact
cone from the lens rim through the image, D|x_s − d_i|/d_i, agreeing with the
two-ray construction to 0. The real lens's trace uses a closed-form sphere root
cross-checked against Newton on the sag (1.42e-14 cm over five heights), and its
longitudinal spherical aberration is shown to be O(h²) by **measured** ratios
(4.0091, 4.0023, 4.0006, 4.0001 per halving) rather than asserted to be. Every
reference value in `selfTest` is a printed line of
`build/geometric-optics/refvals.txt`, the output of `derive.py`.

**What is PhET's, and where it came from.** Read out of the minified build: the
40–120 cm focal-length and radius ranges and the 60–120 cm diameter for the lens,
75–150 and 150–300 cm for the mirror, the 1.2–1.8 index, the n = 1.5 the direct
lens model pins and the n = 2 that turns the lens maker's equation into the
paraxial mirror formula, the flat mirror's f = 100 000 cm stand-in, the object
positions, the −56.5 cm second point, the screen at 200 cm, the 120° fan and its
20·(⌊d_o/300⌋+1) ray count, the guides' own arithmetic, and the softened lens sag
(D/2)²/2(|R|+100) the artwork uses. PhET's `doc/model.md` prints the lens maker's
equation as f = R/2(1−n); its code computes the magnitude as |R|/2(n−1) and puts
the sign on from the surface type, which is what is implemented here.

**Three things this file measured about PhET that are worth recording.**

1. **Its guides are the thin-optic construction to second order and no
   further.** A guide rotates the ray through a fixed angle 2 arctan(D/4f) where
   a thin optic changes its *slope* by −h/f. At PhET's defaults the two
   transmitted arms cross **6.73 cm short of a 151.11 cm image — 4.40 %** — and
   shrinking the lens alone takes that to **4.548 %, not to zero**, because the
   surviving error is the u² of the ray's own inclination. Shrink the lens and
   the object's inclination together and the miss falls as e² (measured ratio
   3.996 per halving). Its two branches, 2 arctan r and arctan 3r − arctan r,
   differ by exactly 3 arctan r − arctan 3r = 8r³ + O(r⁵).
2. **Its flat mirror is not a plane.** f = 100 000 cm puts the image of an object
   at 150 cm at −150.2253 cm rather than −150, and m = 1.0015 rather than 1.
   Both numbers are printed rather than rounded away.
3. **Its artwork is not its model.** The drawn lens uses a softened sag, so at
   R = 80, D = 80 it draws 4.444 cm of half-thickness where the sphere it names
   has a 10.718 cm sag — and at R = 40, D = 120 it draws a lens whose surfaces
   could not meet. Taking PhET's default lens at face value as a real biconvex
   glass element (n = 1.5, R = ±80 cm, 80 cm across, 2 cm edge) makes it an f/1
   lens whose rim ray crosses **43.47 cm inside the paraxial focus, 51.7 % of the
   focal length**.

### Fixed (during the build)

- **The rays ran across the caption.** Symptom: in every bench capture the
  outgoing rays crossed the prose at the bottom of the stage and left the canvas
  sideways. Root cause: the drawn segments were emitted at a `reach` of 1.6 world
  widths with no clip — the house rule that everything drawn inside a frame is
  clipped to it had been read as covering axis-derived lines only, and a ray is
  data. Fixed with a Liang–Barsky clip in **world** space (`clipSeg`/`segW`); a
  canvas `ctx.clip()` would have fixed the browser and not the display-list
  audit, which records `clip()` as a no-op. `selfTest` now asserts that no
  emitted segment reaches the caption band or leaves the canvas, over ten
  configurations at two sizes, and the assertion was checked against the
  reintroduced defect (24 failures).
- **The concave mirror was drawn as a convex one.** Symptom: the arc's vertex sat
  nearer the light than its rim. Root cause: a sign — a concave mirror is the
  *inside* of a sphere whose centre of curvature is in front of it, so its rim
  reaches back toward the source (x < 0) and its vertex is the deepest point;
  the outline wrote `s*(-sag)` with s = −1 for concave. The physics was right
  throughout and only the picture was wrong, so nothing but a PNG could see it.
  The backing was wrong for the same reason (it is behind the mirror, +x, for
  both kinds). Pinned by asserting the rim's sign for both surfaces.
- **A flat mirror stretched the frame to 1640 cm for a 170 cm scene.** Root
  cause: the world extent reserved room for ±f and ±2f whether or not those
  marks were drawn, and PhET's flat mirror has f = 100 000 cm. The extent now
  takes only the focal points that are actually drawn, and the *side* they are
  drawn on is computed once in the model and used by both the extent and the
  drawing (it had been written in two places, and a number written twice is two
  numbers of which only one gets mutated).
- **`legendAuto` avoids curves, not labels.** It put the colour key on top of
  "Virtual Image" at 620 × 420 and on "r = D/4f" at 900 × 600. `legendSafe`
  checks both registries and then registers its own rectangle; where every
  corner is taken it draws nothing and the caption names the colours.
- **A caption that said "equal aspect" twice**, and three labels that landed on
  the thing they describe (the axis label on the object standing on the axis,
  the glass's own label across the lens, the dashed-reference note on the curve
  it names). The floating notes above the caption also collided with the bottom
  panel's axis label at every size that has one — every note is now folded into
  the caption itself, which is where a scale factor belongs.
- **Two UI-harness lookups found the wrong control.** Both the lens group and the
  mirror group carry a slider labelled "focal length", "radius R" and
  "diameter D", and a whole-panel walk returns the *mirror's* every time; four
  assertions failed for reasons that had nothing to do with the sim. Every
  lookup in `ui_drive_geometric-optics.js` is now group-scoped.
- **Three survivors of the physics pre-sweep, each fixed at its cause.** (i) The
  aperture test `|h| ≤ D/2` survived because the ray-count check re-typed the
  condition instead of reading `traceRay`'s own `missed` flag, and no probe sat
  between D/2 and D. (ii) `slopeCross`'s heights survived because *any* two
  distinct rays from one object point meet at the image, so the crossing cannot
  see which heights were used — the function now returns them and the suite pins
  that they are the guides' own fulcrum heights. (iii) The rim's x-coordinate in
  `spotEdge` survived because it is identically zero: the optic is at (0, 0) by
  construction. That is dead generality, so it was deleted rather than excused.
- **Two reference values had been read off the wrong row of `derive.py`.** The
  h² ratio labelled "1 to 0.5" is derive's 2→1 ratio, and the real-lens readout
  prints `84.106`, not `84.11` (four significant figures, not two decimals).
  Both are the same mistake: quoting a printed table without checking which line
  the number is on.
- **PhET signs a mirror's radius and its focal length by different rules**, which
  showed up as a failing assertion rather than as a bug here: a concave mirror
  gets R = −180 cm (convex-is-positive) and f = +90 cm (converging-is-positive),
  so for a mirror f and R/2 disagree in sign while their magnitudes agree. The
  suite asserts both halves of that.

- **Two silhouettes that did not survive being drawn.** The penguin was an
  octagonal blob at 80 cm tall, which defeats the point of an object whose top
  and bottom differ — an inverted image has to be recognisably upside down. The
  ruler's own name was drawn inside its band, on top of the zero tick, which is
  exactly where the eye goes first. Both found only by looking.

**Verification.** `selfTest` 901 passed / 0 failed (0.1 s under `jsc`, 0.4 s
under `osascript`); the UI drive 400 / 0; `tools/audit.py` reports 0 layout
problems at 1400 x 820 over 35 captured configurations and 0 at 820 x 520 over
six; every view's PNG was looked at. `mutants.json` carries **77 mutants (64
physics, 13 UI)**, every `old` pattern checked to occur exactly once by
`gen_mutants.py`; a pre-sweep in this build's own scratch directory
(`_out/presweep.py`, `jsc` for the physics suite and `osascript` for the UI one)
reports **77 caught, 0 survived**, and three separate hand-reintroduced defects
were each confirmed to fail their own assertion. The authoritative sweep is the
orchestrator's.

### Known-bad candidates

- **A ray is data, and data inside a frame gets clipped to it.** The rule on this
  list about clipping reference curves was read as covering lines drawn from
  *axis limits*; an optical bench draws rays from the model and they sprawl
  across the caption just the same. Clip in world space, not with `ctx.clip()` —
  the display-list recorder treats `clip()` as a no-op, so the captured geometry
  would still lie. The assertion that closes it is on the emitted geometry: no
  segment may reach the caption band.
- **A concave mirror's rim is NEARER the light than its vertex.** It is the
  inside of a sphere whose centre of curvature is in front of it. Getting this
  backwards draws a convex mirror under a concave label, with every number on
  the page correct, and no physics assertion can see it. Pin the sign of the
  drawn rim, for both surfaces, whenever a curved optic is drawn.
- **A frame sized from marks that are not drawn.** PhET's flat mirror carries
  f = 100 000 cm as a stand-in for infinity; reserving room for it squeezed a
  170 cm scene into 1640 cm of frame. Size the extent from what the view will
  actually paint, and compute "which side is F on" ONCE — it was written in the
  extent and again in the drawing, and only one of them would have been mutated.
- **Two panel groups that share a slider label defeat a whole-panel lookup.** The
  harness's `sliderU('radius R')` walked the whole panel and took the last
  match — the mirror's — so four assertions about the lens failed for unrelated
  reasons. When two groups can carry the same label, address the control by
  group and index, never by label alone (this is the `sliderU('offset')` entry
  from `lagrange_points`, one step worse: here the labels are *identical*).
- **Any two distinct rays from one object point meet at the image, so a
  crossing-point assertion cannot pin WHICH rays were used.** `slopeCross`'s
  ±D/2 survived a sweep for exactly that reason. When a construction's identity
  matters (here: it must be the guides' own fulcrum heights), return the inputs
  and assert them; the output is invariant to them by construction.
- **`legendAuto()` avoids curves and not labels** (already on this list from
  `pupil_plane`) — and the fix has to *register* the legend's own rectangle too,
  or the next label drawn lands on it instead.
- **PhET's guides are exact to second order in the ANGLE, not in D/f.** Shrinking
  the lens alone leaves a 4.5 % miss. A "small parameter" argument has to name
  which parameter: here rotating by a fixed angle where a thin optic changes a
  slope leaves an error of order u², the ray's own inclination, which no amount
  of shrinking the aperture touches.
