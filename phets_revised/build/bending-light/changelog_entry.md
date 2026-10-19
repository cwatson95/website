## 2026-09-22 — bending-light: PhET's Bending Light remade, with Snell, the Fresnel equations, PhET's dispersion model and a prism ray tracer all solved exactly

### Added
- **`docs/phets_revised/bending-light.html`** (227 KB, 4 149 lines) — a clean-room
  remake of PhET Interactive Simulations' *Bending Light* 1.2.5
  (`docs/phets/bending-light_en.html`), in the house six-view form. PhET's three
  screens map to the first three views; the last three are the analysis views.
  - **the boundary** — PhET's Intro screen. A laser you swing about the origin
    (drag its body) onto the interface between two media, with the reflected and
    transmitted rays drawn in the true CIE colour of their wavelength at their
    own share of the power, the normal, the angle arcs, PhET's protractor, PhET's
    intensity meter and the critical-angle line. White light draws the incident
    and reflected rays ONCE, in white — reflection does not disperse — and fans
    only the transmitted ray.
  - **the wave** — PhET's wave view and the two More Tools meters. Crest lines of
    the incident, reflected and transmitted waves; the time-averaged intensity
    painted behind them, which is the standing-wave pattern above the boundary
    and the (decaying) transmitted intensity below; ticks on the boundary at the
    crest positions, whose spacing IS Snell's law; a field profile on the cut
    x = 0 with its envelope; and PhET's wave sensor as two probes against time.
    The evanescent tail past the critical angle is drawn and labelled; PhET
    draws nothing there.
  - **the prism** — PhET's Prisms screen. PhET's own five prism prototypes at
    PhET's own size, traced by exact ray/polygon and ray/circle intersection with
    vector Snell at every face, total internal reflection where the geometry
    demands it, PhET's optional partial reflections and normals, and white light
    dispersed into a spectrum.
  - **the reflected fraction** — the Fresnel equations drawn: R and T for s and p
    against the angle of incidence, Brewster's angle where R_p is exactly zero,
    the critical angle where R becomes exactly one, the phase of the reflected
    amplitude (the pi jump at Brewster, the Goos–Hänchen slide past theta_c), and
    R(0) against the index ratio.
  - **the spectrum** — PhET's dispersion model made visible: n(lambda) − n(650 nm)
    for every substance (every curve the same shape, scaled), the CIE 1931 colour
    of each wavelength under the axis, the deviation of a 60-degree prism against
    wavelength, and the exit fan with its exaggeration printed.
  - **the rainbow** — Descartes' stationary deviation in a sphere of water: the
    caustic drawn from the rays themselves (both signs of the impact parameter),
    D(theta_i) for one and two internal reflections with the stationary points
    marked, the primary bow at 42.13 degrees and the secondary at 50.79,
    Alexander's dark band, and the Fresnel weights that say why a bow is faint and
    polarised.
- **What is exact**, all pinned in `selfTest` against printed lines of
  `build/bending-light/refvals.txt` (the output of `derive.py`, an independent
  Python solve with `scipy.minimize_scalar` on the prism and the rainbow):
  - Snell's law over eight medium pairs × eight angles to 1e-12 deg, in both
    directions; theta_2 = 90 deg EXACTLY at the critical angle and no solution one
    part in 1e12 past it; every refraction round-trips to 1e-14 rad; the cubic
    term of the small-angle limit measured and matched to −(r − r³)/6 (a limit
    asserted by its rate of approach, not its destination).
  - The Fresnel equations in both polarisations: R + T = 1 to 5e-15 over eight
    pairs × 601 angles; R_p = 0 at Brewster to 1e-30 and theta_B + theta_2 = 90 deg
    to 1e-12; R = 1 exactly at and past theta_c; R(0) = ((n1−n2)/(n1+n2))²; the
    beam-width factor (n2 c2)/(n1 c1) shown to be 0.32 of T at 50 deg, so it is
    not a normalisation; T(1→2) = T(2→1) to 1e-13.
  - The wave: lambda_0/n, c/n, the frequency invariant, the crest spacing along the
    boundary matched to 1e-15, 1 + r_s = t_s and the magnetic-field condition to
    1e-14, the PAINTED field continuous across y = 0 over 16 geometries × 5 places,
    and the painted intensity equal to a 720-point time average of the drawn field.
  - The prism: the traced deviation against the two-surface closed form at four
    entry angles and against n = sin((A+D_min)/2)/sin(A/2) to 1e-11 deg — two
    routes that share no arithmetic; a slab shown to displace without deviating;
    a ray through the centre of the circle undeviated; the semicircle aimed at its
    centre leaving at exactly the Snell angle of its flat face; five traced-ray
    references (segment counts, total lengths, exit directions, branch powers) with
    and without the partial reflections.
  - The rainbow: cos²theta = (n²−1)/(k²+2k) against scipy's minimiser to 3e-7 deg
    for k = 1, 2, 3, with dD/dtheta = 0 there and D larger on both sides; the bow
    angles of five wavelengths at both orders; and **two exact identities** derived
    here and asserted: at the stationary ray the internal reflectance is
    R_s = (k/(k+2))², *independent of the index*, and the whole s-polarised
    throughput of the k-th bow is (1−R)²R^k — 64/729 for the primary, 9/256 for the
    secondary.
  - The colour path: `derive.py` parses the CIE 1931 table back out of `p2_cie.js`
    and re-evaluates it in Python, so the eight monoLinear triples, the eight sRGB
    byte strings and the seven monoLevel values are pinned against an independent
    evaluation of the same published numbers rather than against themselves.
  - The world's wavenumber and the evanescent decay, both pinned absolutely and
    then MEASURED off the drawn field: `k0` per world unit at five wavelengths;
    the crest spacing along the boundary read off `waveAt` by bisected zero
    crossings; the standing-fringe period read off `meanIntensity` by
    parabola-refined maxima; kappa/k0 and 1/kappa in nanometres at three angles
    for three medium pairs at two wavelengths, with the decay rate recovered
    from the ratio of the drawn field at two depths; and, below the critical
    angle, the contract that there is no decay at all.
- `selfTest` **866 passed, 0 failed**; UI drive **432 passed, 0 failed**; layout
  audit clean over 32 captured configurations; 32 PNGs looked at.
- `mutants.json` carries **113 mutants (95 physics, 18 UI)**, every `old` checked
  unique by `check_mutants.py`. Full sweep by the orchestrator: **113 caught,
  0 survived** (the first 109-mutant sweep found two survivors, both closed
  below and each re-verified caught).

### Fixed (during the build)
- **The prism tracer's ray/segment parameter had the wrong sign, and the copy of
  the formula inside `shape_hit` was fixed a second time.** `u = (q×d)/(−den)`
  instead of `/den` made the semicircle's flat face unreachable: a ray aimed at
  its centre crossed the curved face and then missed the shape entirely,
  emerging undeviated. Symptom: two segments instead of three and an exit angle
  of −20 deg where Snell demands −30.86. Root cause: the same eight lines written
  twice (polygon edge and flat face), so fixing one left the other wrong — the
  drum's group-velocity lesson again.
- **A white beam drawn as thirty translucent strokes is not white.** Source-over
  compositing is not addition, so whichever end of the spectrum is painted last
  simply wins: the prism's white light came out crimson, and re-ordering the
  wavelengths outward-in only changed it to green. Root cause: the same defect as
  `lenses.html`'s four Fraunhofer lines reading as one red beam, thirty layers
  deep. Fixed with a geometric rule that is also a true statement —
  `mergeMask()` asks, per segment, whether the thirty wavelengths still lie within
  a line width of one another; where they do the beam is drawn ONCE in white,
  where they do not it is drawn one wavelength at a time. It is a model function,
  so `selfTest` asserts that the beam arriving at the prism merges and the beam
  leaving it does not, and that the rule tightens and loosens with the scale.
- **The prism's default beam sat on a constant-deviation path.** At tilt −7 deg the
  ray entered the left face, total-internally reflected off the right face and
  left through the bottom — an arrangement whose deviation is nearly achromatic
  (0.037 deg of spread against 1.6 deg at minimum deviation). The tracer was right
  and the picture was useless. The default is now aimed at the left face near the
  minimum-deviation angle; `selfTest` asserts both spreads, so the achromatic path
  is recorded as physics rather than forgotten as a bug.
- **The rainbow's emergent ray was drawn by turning the incoming direction through
  D, in the wrong sense.** The exit rays left up-and-right instead of back toward
  the antisolar direction. Root cause: a drawing that re-implements the model's
  arithmetic instead of using the model. `dropPath` now refracts at the exit face
  and returns that direction, and `selfTest` asserts it equals −D (mod 2 pi) over
  three orders × four impact angles — which is what ties the picture to `rainDev`.
- **The wave field painted on a cell grid aliased into a checkerboard and drowned
  the crest lines**, and cost 7 400 fillRects at 1400×820. Replaced by the
  time-averaged intensity, which depends on y alone and is therefore 140
  horizontal bands, smooth, and physically the standing-wave pattern; the crest
  lines carry the instantaneous phase on top of it.
- **Rays were not clipped to the world box**, so the prism and boundary views drew
  over the caption and off the canvas. Clipped in DATA space (Liang–Barsky), never
  `ctx.clip()`, because the recorder stubs `clip` and the audit would still lie.
- **The op-count floor of the layout sweep was copied in from a field-map sim.** A
  ray diagram is a dozen strokes and almost no fills, so a fills-only floor of 6
  failed five correct views. Floors are now counted over fills PLUS strokes and
  derived per configuration from what the sim actually emits (`opcount.js`).
- **Two dirty flags on one path made each other's mutant equivalent.** The
  `pointerdown` handler set `dirty` as well as the `pointermove` handler, so
  either could be deleted with no test failing. The down handler no longer sets it
  (a down changes nothing on screen); and the drag test now measures the repaint
  BETWEEN the move and the up, because the `pointerup` handler calls `refresh()`,
  which draws unconditionally — and re-proves idleness after its own baseline
  draw, because `forceDrawU()` is a tab click and `setView` sets `dirty` itself.
- **A drag test that only checks "the value changed" passes a mutant that pins the
  value to a constant.** The prism beam drag compared against the default, and a
  mutant that froze the beam at 1.3 differed from the default by more than the
  threshold. The test now drags twice, in opposite directions, and asserts the
  beam follows the pointer both times.
- **`fresnel()` carried an evanescent decay constant that nothing read** — the
  full sweep's first survivor. Every consumer (`waveAt`, `meanIntensity`, the
  readout, the drawing) takes kappa from `fresnelSComplex`, so mutating
  `fresnel()`'s copy from `n2 g` to `n1 g` provably could not change any output.
  Root cause: the same quantity computed in two places, one of them unreachable.
  Deleted, with `fresnelSComplex` named in a comment as the only owner — and,
  because that is the shallow half of the finding, the LIVE kappa was pinned
  properly: its old check compared `exp(-kappa|y|)` against a ratio of `waveAt`
  to itself, both sides built from the same kappa, so it was blind to a wrong
  one as well. It is now asserted absolutely against `derive.py` (kappa/k0 and
  1/kappa in nm, three angles x three pairs x two wavelengths), recovered by
  measurement from the drawn field (under total internal reflection the
  transmitted phase does not depend on depth, so the ratio at two depths IS
  exp(kappa dy)), and the readout's printed decay length is asserted to contain
  "124.8". Four new mutants cover it, including one that gives a PROPAGATING
  transmitted wave a decay — which no ratio of the field to itself could see,
  and which is caught by the flat-intensity contract.
- **Every wave assertion was taken at 650 nm, where `k0` is 2 pi whichever way
  round the ratio is written** — the sweep's second survivor. `k0 = 2 pi
  (lambda_red/lambda)` per world unit inverted to `2 pi (lambda/lambda_red)`
  and 866 assertions stayed green, because one world unit IS one red
  wavelength and the reference wavelength is the default. Root cause: exactly
  the w = -1 dark-energy exponent on this list — a parameter has a value at
  which it stops mattering, and the whole suite was sitting on it. Fixed by
  pinning `k0` at 380, 400, 500, 650 and 700 nm against `derive.py`, asserting
  that halving the wavelength doubles it, measuring the crest spacing and the
  standing-fringe period off the drawn field at 400, 500 and 650 nm, walking
  the field-continuity and mean-intensity sweeps across the band instead of
  parking them at 650, and adding violet and deep-red wave configurations to
  the layout sweep.
- Smaller ones: the caption ran under the house `#hint` (fixed with
  `stageLayoutH`, reserving HINT_H); notes under a panel landed on the axis
  labels or on a legend (`axesRB` registers the two tick strips, `legendA`
  registers the legend box, `noteIn` puts the note inside the plot); the
  intensity meter's "100.0%" ran into its polarisation tag (three lines now, and
  it picks a corner that no label occupies); the spectrum's colour strip covered
  its own tick row (drawn inside the box); the spectrum's main panel plotted n
  itself, on which every curve looks flat (it plots n(lambda) − n(650) now, with the
  absolute index in the legend); the rainbow's info block was unreadable over the
  ray fan (it has a pad, which is deliberately NOT registered — registering it
  made `lab()` dodge it and put the first line outside the panel).

### Known-bad candidates
- **Source-over compositing is not addition, so N translucent strokes on one path
  can never make white.** Ordering them does not help: with alpha a, the last
  five of thirty layers carry 1 − (1−a)⁵ of the result whatever the order, so the
  pile takes the colour of whichever end was painted last (crimson if red is last,
  green if the luminous middle is). Drawing each layer with alpha 1/k makes the
  composite the exact average but leaves the last layer at 3 % where the paths
  separate. The fix that works is geometric: decide per segment whether the
  wavelengths are still within a line width of each other, draw white where they
  are and one at a time where they are not — and make that decision a model
  function so it can be asserted rather than looked at.
- **A prism geometry can be achromatic, and the tracer will be right while the
  picture says nothing.** In-left, TIR-right, out-bottom of an equilateral prism
  is a constant-deviation arrangement: the reflection undoes most of the entry
  dispersion, leaving 0.037 deg of spread instead of 1.6. A default that lands
  there makes "white light through a prism" draw a single white line. Check the
  spread the default geometry actually produces, and assert it.
- **The same eight lines of ray/segment intersection written twice will be fixed
  once.** The polygon edge loop and the semicircle's flat face carried the same
  sign error in the parameter along the edge; correcting the first left the
  second silently returning "no hit", which reads as a ray passing through a
  surface rather than as a bug in a formula.
- **A drawing that re-derives the model's own arithmetic will disagree with it.**
  The rainbow's emergent ray was constructed by rotating the incoming direction
  through the deviation, and got the sense wrong; the fix was to refract at the
  exit face — i.e. to let the drawing ASK the model — and to assert that the two
  agree. Same family as the Mach-cone tangency: assert on the objects the view
  draws, not on the formula beside them.
- **An op-count floor must be derived from what the file emits.** A ray diagram is
  a dozen strokes and five fills; a floor tuned on a sim that paints a field map
  fails it for being efficient, and counting only fills fails it twice over.
- **Two dirty flags on one path, and a `pointerup` that calls `refresh()`, make a
  drag test blind.** Measure the repaint between the move and the up, keep one
  flag, and re-prove idleness after any forced baseline draw — a tab click is a
  forced draw.
- **A drag test must assert the control FOLLOWS the pointer, not merely that it
  differs from its default.** A mutant that freezes it at any other constant
  passes the weaker test.
- **A decay constant checked by comparing exp(-kappa y) against a ratio of the
  field to itself is not checked at all** — both sides are built from the same
  kappa, so the comparison is an identity. Pin it against an outside number, and
  recover it by MEASUREMENT from the drawn field: past the critical angle the
  transmitted phase does not depend on depth, so the ratio of the field at two
  depths is exactly exp(kappa dy) and its logarithm gives kappa back. The other
  half of the contract needs stating too: BELOW the critical angle there is no
  decay at all, which only a flat-in-depth assertion can see.
- **A world whose unit is the reference wavelength makes the reference
  wavelength the one place a wavenumber cannot be wrong.** `k0 = 2 pi
  (lambda_ref/lambda)` per unit is 2 pi at lambda = lambda_ref whichever way the
  ratio is written, so a suite that takes every wave assertion at the default
  wavelength is blind to the inversion. Same family as the w = -1 dark-energy
  exponent: spread the assertions across the band, and assert the SCALING
  (halving the wavelength doubles the wavenumber) as well as the values.
- **The quantity computed in two places will be pinned in the place nothing
  calls.** `fresnel()` and `fresnelSComplex()` both derived the evanescent
  kappa; the dead one is what the mutation sweep flagged, and the live one
  turned out to be unpinned too. Delete the copy, name the owner in a comment,
  and check that the surviving one is asserted against something outside
  itself.
