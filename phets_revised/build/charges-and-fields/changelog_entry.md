## 2026-09-18 — charges-and-fields: point charges on a plane, their exact field and potential, in five views

Remake of PhET's Charges and Fields 1.0.67 (`docs/phets/charges-and-fields_en.html`)
as `charges-and-fields.html` (build/charges-and-fields/), in the house form:
five views, the scaffold, palette, `h()`, 2-D layer and camera extracted from
`projects/simulations/build_buoy` and `build_lagr` (make_head.py,
make_utils.py, make_helpers.py assert every function they carry), the site
nav absolute. New code; no PhET code or assets.

### Added
- **the plane** — PhET's screen: drag +1 nC and −1 nC charges and E-field
  sensors out of the bin onto the 8 m × 5 m plane, drop them back to remove
  them; the field on PhET's 0.5-m arrow grid (fixed length, opacity |E|/5 V/m,
  or "direction only"); the voltage on PhET's 0.1-m cells saturating at ±40 V;
  the voltage sensor, whose canvas "plot" button traces the equipotential
  through its crosshair (refused within 3 cm of a charge, PhET's rule, and at
  a null, where the level set is not a curve; cleared when a charge moves, as
  PhET's are); E-field sensors reading |E| and
  its direction (arrow 15 px per V/m at 128 px/m, capped at 2 m with a double
  head); a tape measure in centimetres that also reads V(A) − V(B); PhET's
  grid (0.1 m / 0.5 m) and "1 meter" scale; value labels. **field lines** —
  lines traced along E from the majority sign, an equipotential family every
  ΔV, and the null points found by Newton and classified (saddle, in-plane
  minimum or maximum). **the landscape** — V(x, y) as a clipped height surface,
  the plotted equipotentials lifted to their level as its contour lines, one
  depth sort for surface, loops and charges. **superposition** — each charge's
  field at a probe drawn head to tail and closing on the total, and V built up
  as a signed waterfall. **the far field** — |V| along a ray on log axes
  against its leading multipole, the exact Legendre series (all orders, beyond
  d_max) checked against the tensor contraction, and r^(ℓ+1) V taken to its
  limit numerically (Richardson).
- What is exact: V = k Σ q/r and E = k Σ q r̂/r² of 3-D point charges held in
  the plane (PhET's model), in closed form; equipotentials by RK4 along ẑ × Ê
  with a Newton projection back onto V = V₀ every step (every vertex on the
  level set to ~1e-15 relative, asserted below 1e-12), closing on themselves;
  field lines by RK4 on
  E/|E| with steps from the local length scale min(r_near, |E|/|∇E|); nulls by
  Newton with the analytic Jacobian; the multipole coefficients; the tape's
  line integral. One measured number: ε₀ = 8.8541878188e-12 F/m (CODATA 2022,
  NIST), so k = 8.98755 V·m/nC; PhET's K_CONSTANT is 9, so PhET reads 0.14 %
  high (said on the page).
- Verification: `derive.py` → `refvals.txt` (scipy brentq on rays + quad for the
  equipotential loops' areas and perimeters, solve_ivp for the field lines,
  fsolve for the nulls, quad for the tape, the Legendre and tensor routes for
  the multipoles, Richardson limits), emitted into the suite as literals by
  `gen_refs.py`; selfTest 1594 assertions incl. a 29-configuration × 4-size
  layout sweep; UI drive 184 (every tab, slider, checkbox, chip, button and
  key; the charge, bin, sensor, tape, probe and camera drags and the wheel,
  each repainting through the frame loop from a proven-idle baseline);
  mutation sweep 63 of 63 caught (47 physics, 16 UI; 61 in the full sweep,
  the 2 survivors caught on re-run after their blind spots were pinned; run
  on a copy in `_out/`, log in `mutation_log.txt`); display-list audit 0
  problems over 27 captures; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **Field lines orbited the triangle's centre for 20,000 steps.** Symptom: 2 of
  48 lines neither escaped nor ended. Root cause: the centre of three like
  charges is an in-plane MINIMUM of V, a sink for in-plane lines (the field
  turns out of the plane along z); a 0.2-mm step floor made the RK4 step
  overshoot the node once it was nearer than a step, so the line circled it.
  Near a node |E|/|∇E| is the distance to it, so the steps now shrink
  geometrically and a line ends on a relative-field threshold (2 lines end
  there, asserted).
- **A neutral plane's lines "escaped".** 10 of the two rows' 112 lines passed
  the first 300-m escape radius. Every line of a neutral configuration returns,
  but a dipole-like line leaving at a small angle α reaches ~4a/α²; with steps
  proportional to distance the radius is now 10 km for ~20 steps per e-fold
  (112 of 112 end on charges, asserted).
- **Rounding residue printed and plotted as data.** The rows' V = 0 equipotential
  was labelled "3.99×10^-15 V", and the far field along the dipole's bisector
  drew a green fragment at 1e-15 V. Root cause: cos 90° = 6.1e-17, so the ray
  runs 6e-17·r off the bisector and the two cancelling terms leave residue.
  `potentialClean` zeroes a sum below 1e-12 of Σ|q|/r (a charge still reads
  ∞), sensors read 0 V/m with no direction at a null (asserted both ways).
- **The PNG pass**: opaque grid lines on the voltage-cell boundaries tiled the
  map (now translucent); white sensor labels over white "direction only"
  arrows were unreadable (now on pads, `labPad`); twelve null labels piled on
  the rows (named only when ≤ 4, counted in a status line); the landscape
  framed the bounding sphere of an 8 × 5 × 2.5 m box and sat small (the
  distance is now bisected on the 8 projected corners), its 40-V default clip
  left a dipole as two spikes (20 V), its loops and charge markers were
  painted after the surface and showed through peaks and well rims (one depth
  sort, 5-cm bias), and a foreshortened height bar piled its labels (top label
  only when short); the superposition total vanished off a corner of the plane
  (the chain may use the whole panel, and a note says when it points off).
- **A charge dropped where the bin would be vanished in views with no bin.** The
  bin's delete-on-drop ran in every view, so a charge left near (0, −2 m) in the
  field-lines or superposition view was silently removed. It now acts only on
  the plane, where the bin is drawn (asserted, and a mutant restores the old
  rule).
- Wording measured, not assumed: a line on a neutral plane that passes 10 km is
  reported as "run off past 10 km", not "to infinity" (it would return, and 1
  of 640 did not within 10 km on a 40-charge plane); the far-field INFO said the
  Richardson limit agrees "to about nine digits", but the presets give 6.5 to
  10 (triangle 3.0e-7, rows 4.9e-8, dipole 6.4e-10), so it now says so; "a
  charge confined to the plane would sit stably" at the triangle's centre
  holds only for a positive one.
- Layout sweep catches: the voltage sensor's panel ran over the caption at the
  plane's bottom edge (it flipped only at the canvas edge); a "0.1 m" x tick
  and the lowest y label collided in the far-field corner (ticks from 1 m); the
  waterfall's y ticks collided at 560 × 380 (sparse ticks).
- Test-side, each a wrong expectation rather than a wrong sim: the square
  quadrupole along x has V ≡ 0 (odd under y → −y), not a hexadecapole lead;
  8-point Gauss–Legendre misses x¹⁶ by exactly 2¹⁷(8!)⁴/(17(16!)²) = 4.65e-5
  (now pinned); a ratio of two 1e-4 differences carries JS/Python `hypot`
  rounding at 4e-9 (tolerance 1e-7); near a lone charge the length scale is
  r/√5, never the distance, which binds only where ∇E vanishes (the rows'
  centre); the UI op floors were guessed (120 for field lines) until measured
  (96), and are now 80 % of the measured emission.
- **The mutation sweep's survivors, each a blind spot, now pinned.** "The centre
  of charge's y not divided by Q" survived because every charged preset (one
  charge, the like pair, the triangle) has Σqy = 0, so the centre's y was 0
  however it was computed, and the far-field limits used only those presets.
  The replacement is an asymmetric set with Q = 2 against derive.py, plus the
  centre's defining property (the dipole moment about it vanishes). The first
  attempt had Q = 1, where dividing by Q is the identity: the same blind spot
  again, caught before it ran. "The superposition arrow scale set by the total
  alone" was invisible in both tested chains (no single term outruns the
  total in either); near the like pair's midpoint one term is 1.75× the total
  and now sets the 1.4-m scale.

### Known-bad candidates
- **A symmetric preset family blinds every assertion a symmetry zeroes.** All
  the charged presets had Σqy = 0, so a centre of charge computed wrongly in y
  still read 0, and no moment or far-field assertion built on those presets
  could see it. Pin such formulas on an asymmetric configuration, and check that the
  replacement is not degenerate in another way (Q = 1 makes "divide by Q" a
  no-op).
- **cos(90°) is 6.1e-17, not 0: a ray "along" a symmetry line samples 6e-17·r off
  it, and a cancelling sum there leaves ~1e-15 residue that a log axis draws
  as data and a label prints as a value.** Floor cancelled sums relative to the
  size of their terms (|Σ| ≤ 1e-12 Σ|terms| → 0), never absolutely, and keep an
  infinity infinite.
- **A step floor in a tracer that converges on a node makes it orbit the node
  until maxN.** If the step comes from |E|/|∇E|, which is the distance to the
  node, let it shrink and end on a relative threshold.
- **Overlays painted after a painter-sorted surface show through it.** Put
  contour segments and markers into the same depth sort, biased a few cm
  toward the eye so they do not fight the face they lie on.
- **The bounding sphere of a flat box frames it small.** Bisect the camera
  distance until the box's own projected corners fit.
- **An in-plane slice of a 3-D field is not a 2-D field**: lines per charge are
  not flux, and an in-plane minimum of V is a sink where lines end. "Every line
  ends on a charge" is only assertable for a neutral plane, and only with an
  escape radius far beyond the configuration.
- **`tools/mutate.py` writes `_mutant.js` next to the HTML it sweeps**; agents
  sharing a directory corrupt each other's counts. Sweep a copy in your own
  `_out/`.
