## 2026-09-22 — beers-law-lab: PhET's two screens, with the mole ledger closed to the last bit and the transmitted colour worked out over the CIE observer

### Added
- **`docs/phets_revised/beers-law-lab.html`** — a remake of PhET Interactive Simulations'
  Beer's Law Lab (beers-law-lab 1.8.7, CC-BY 4.0), six views: **the beaker** (PhET's
  Concentration screen: nine solutes, a shaker and a dropper, a water faucet, a drain, an
  evaporator, the concentration meter on a draggable probe, and the saturation point where
  solid appears), **the cuvette** (its Beer's Law screen, drawn to scale in centimetres,
  with a draggable cuvette wall that snaps to PhET's 0.1 cm on release and a draggable
  detector probe), **the spectrum**, **the law**, **the ledger** and **true colour** (this
  file's own analysis).
- **Exact, and asserted as exact.** `A = eps l c` and `T = 10^-A` against 50-digit
  `decimal` over 8 solutions x 4 path lengths x 4 concentrations: worst relative error
  2.7e-16 on the product, 4.7e-16 on the power, 1.4e-16 on the round trip
  `-log10(10^-A) = A`. The end-to-end error in T is deliberately **larger** (1.2e-15) and
  the suite asserts the `ln10 * A` amplification that explains it rather than pretending it
  is not there. Both extremes are pinned: `A = 0` gives `T = 1` exactly, `A = 1` and `A = 2`
  give exactly 10 % and 1 %, `10^-A` underflows a double to exactly zero at **A = 324** (found
  by search, not assumed) and the value one below it is a denormal, and a detector reading
  0 % T inverts to `+Infinity` — no finite absorbance produces it.
- **The beaker is a mole ledger and it closes.** PhET's five mechanisms in PhET's order
  (faucet, drain, dropper, evaporator, shaker), each returning what ACTUALLY moved.
  `derive.py` runs a 900-frame script through all five twice — once in doubles, once in
  exact `fractions.Fraction` — and both ledgers close, the rational one identically and the
  double one to **0.0 mol and 0.0 L**, with the two runs agreeing to 4.4e-15. The JS runs
  the same script and reaches the twin's 1.14375 mol once the last grain lands. The ledger
  closes **through** the clamps too (a beaker filled past the brim, a drain asked for more
  than is there, the 7 mol ceiling).
- **Saturation, exactly**: `C = min(Csat, n/V)`, `solid = max(0, n - V Csat)`, and
  evaporating a fixed n climbs the exact hyperbola `n/V` to `V = n/Csat` and is flat after
  it. The drain is the subtle one and is asserted: it removes SOLUTION, so it carries
  solute at the DISSOLVED concentration and leaves the precipitate behind (0.138 mol out of
  a saturated CuSO4 beaker against a naive 0.200).
- **PhET's data, read out of the original and never typed.** `extract_phet.py` parses the
  minified build for the nine solutes (molar mass, stock, saturation, all three colour
  stops), the eight Beer's Law solutions, the **eight molar-absorptivity spectra at one
  value per nanometre from 380 to 780 nm**, the beaker's 1 L, the 0–7 mol and 0–1 L ranges,
  the 0.5–2 cm cuvette and its 0.1 cm snap, the flow rates and every decimal-place count;
  `make_data.py` writes them into the file.
- **Literature beside PhET's** (Wikipedia chemical infoboxes, fetched 2026-09-22, quoted to
  their own printed precision, converted on the stated assumption that a litre of water
  makes a litre of solution): PhET's molar masses match to **5.6e-5** relative, and its
  saturation points to 0.0–0.6 % for the four whose sources quote a room-temperature figure
  (K2CrO4, KMnO4, NiCl2, K2Cr2O7). The worst gap is cobalt(II) nitrate at 23 %, whose only
  usable infobox figure is at 0 °C, and the view says so. PhET's "drink mix" carries
  **sucrose's** molar mass to a milligram per mole.
- **No molar-absorptivity literature value could be sourced offline.** Three sources were
  tried and all three carry only qualitative colour: Wikipedia's "Molar attenuation
  coefficient" (no numerical example for any substance), "Metal aquo complex" (a colour
  column, no wavelengths and no coefficients) and "Permanganate" (a spectrum figure, no
  printed lambda_max and no epsilon). The spectra therefore stand as PhET's own digitised
  data, are labelled that way on the canvas and in the panel, and no comparison is invented
  for them. "Still unverified" is the honest answer for those eight curves, and the file
  says so.
- **The true transmitted colour**: `T(lambda) = 10^-eps(lambda) l c` at every nanometre,
  integrated against the CIE 1931 2° observer **on the same 1 nm grid the spectra live on**
  (CIE_xyz_1931_2deg.csv, DOI 10.25039/CIE.DS.xvudnb9b) — nothing interpolated, nothing
  resampled — then adapted so the illuminant itself renders exactly white, which needs no
  white-point constant and makes an empty cuvette rgb(255,255,255) under either illuminant.
  Two illuminants, because no D65 spectrum could be sourced offline: equal energy (flat by
  definition) and CIE standard illuminant A from the CIE's own formula. PhET's ramp is
  nowhere within **68 of 255** on its worst channel, and the sharpest difference is not
  brightness: PhET's ramp has no path length in it at all.
- Findings worth keeping, each derived rather than recalled: PhET's `Color.interpolateRGBA`
  **floors** each channel, so halfway from (224,255,255) to (255,225,225) is (239,240,240);
  the Beer's Law ramp has a genuine **step at c = 0**; `eps(lambda)` is a LOOKUP indexed by
  `floor(lambda - 380)`, so 500.0 nm and 500.9 nm read the same cell; copper sulfate's
  lambda_max is the LAST sample (780 nm) because its band is in the infrared and PhET's
  table stops where the eye does; **every one of PhET's nine stock solutions is below its
  own saturation point**, so the dropper can never saturate a beaker and a drop of stock
  into a saturated one dissolves solid; and PhET's own `doc/model.md` disagrees with PhET's
  own code twice (it clamps the concentration against the STOCK concentration where the code
  clamps against the SATURATED one, and writes the precipitate as a difference of
  concentrations where the code takes a difference of moles) — the code is what is
  implemented here.
- **Verification**: `selfTest` 552 assertions, 0 failed; UI drive 323, 0 failed (every tab,
  every visible slider at its ends, every checkbox, every chip, every button, the keys,
  resize, three custom drags each proven-idle-first and one axis at a time, and reset-all
  against a fully disturbed state including the beaker, which is not a slider value);
  display-list capture at 1400x820, 1100x700 and 560x380, `audit.py` clean at all three, and
  every view's PNG looked at. `mutants.json` carries **71 mutants (57 physics, 14 UI)**, and the sweep run here
  caught **71 of 71** with no survivors.

### Fixed (during the build)
- **The shaker's over-delivery was blamed on the wrong half of PhET's expression.** PhET
  makes `round(max(1, rate * particlesPerMole * dt))` grains a frame. The first draft said
  the `max(1, ...)` FLOOR is what makes it deliver 0.30 mol/s against its nominal 0.20 at
  60 fps. It is not: the bracket is 0.6667 there and `Math.round` takes that to 1 with or
  without the floor — the ROUNDING does it. The floor bites only above about 80 frames a
  second, where the same shaker delivers **0.60 mol/s**. Both are now derived and pinned at
  60 fps, 120 fps and a whole-second step, which is also what makes the mutant that deletes
  the floor catchable: while the only frame rates asserted were ones at which the floor does
  nothing, that mutant survived.
- **Six survivors of the first 58-mutant physics sweep, one at a time.** (1)+(2) Nothing
  drained or evaporated a beaker PAST empty, so the floor clamp in `bkRemoveSolvent` and the
  use of the actually-moved volume in the drain were both untested — they differ from their
  mutants only when the clamp bites. (3) EQUIVALENT: every one of PhET's nine solutes has
  `cMin = 0` and a minColor equal to the water colour, so two of `SoluteColorScheme`'s four
  branches cannot fire; the data property is asserted instead and the two mutants are left
  out with that as the stated reason. (4) `srgbGamma`'s LINEAR segment was reached by no
  assertion — every colour the suite checked was either black or far above the knee. (5)
  **Two guards on one path** (Known-bad, buoyancy.html): `trueRGB` clamped its linear
  channels at zero and `srgbGamma` clamps again, so each made the other's mutant equivalent;
  one guard now, in the function that owns the transfer curve. (6) The ledger view's drawn
  curve is capped at Csat and only its finiteness was asserted, not the cap.
- **`bezierCurveTo` is not in the display-list recorder**, so the meter's wire, the
  detector's wire and the evaporation squiggles recorded as nothing at all and threw under
  the selfTest stub. Drawn as explicit polylines — the same rule as the `ellipse()` entry on
  the Known-bad list.
- **The beam was painted UNDER the cuvette's own fill**, so the one thing the Beer's Law
  view exists to show — the beam dying as it crosses the solution — was hidden. And when
  that was fixed the beam's slabs were still drawn at bench positions 0–2 cm rather than
  inside the cuvette, because the bench's `X(cm)` had been re-based on the bench origin and
  the slab loop had not followed. Fill, then beam, then glass; slabs at `CUV0 + d`.
- **There was nothing to compare the outgoing beam WITH.** The source sat 14 px from the
  cuvette, so the undimmed run was invisible. The bench is now 8.4 cm at up to 120 px/cm
  with the source at one end and a real two-centimetre run before the glass.
- **Ninety text collisions, in four causes.** The caption is drawn LAST but owns the bottom
  of the stage from the moment it is measured, and nothing registered it, so every label
  that dodges collisions was dodging everything except the largest block of text on the
  screen. `legendAuto` dodges CURVES and not LABELS (Known-bad, pupil_plane), so every
  legend was free to land on one. The shared `axes()` takes a tick COUNT, and the count that
  suits a 1400 px stage puts eleven y labels in a 90 px panel at 560. And several labels
  were placed with `lab(rc, 1e5, 1e5, ...)`, which switches off the helper's own clamp to
  the canvas. Fixed by `noteCaption`, `legendFit` (both registries, and it records its own
  box), `axesFit` (counts from the panel's own size, and it drops the x tick sitting exactly
  on the left edge because the y label at that corner is a pixel away from it), and real
  W/H everywhere.
- **The solutes view was laid out for one stage size.** Nine rows of two lines need 30 px a
  row and at 1100x700 it has 22; its row labels were painted ON the bars, so green text sat
  on a green bar; and its rows ran bottom to top, putting PhET's first solute at the foot of
  a list the narrow-stage note called "top to bottom in PhET's order". Now: text above the
  bars, PhET's order downwards, one line a row below 30 px, bars only below 15 px, the
  molar-mass table's column count from the panel's height and its numbers measured against
  the column before they are drawn.
- **Saturated! was dark orange on a bright blue solution**, over the grains. It has a pad of
  its own above the liquid now. The precipitate was drawn in the solute's own saturated
  colour on top of a solution of very nearly that colour — at 1.38 M of copper sulfate the
  grains were invisible; drawn dark with a light speckle.
- **The beaker sat in the bottom third of an 820 px stage** with four hundred pixels of
  nothing above it, because its height was capped at 250 and it was pinned to the floor.
- **The errbox showed a stack and no message.** JavaScriptCore's `Error.stack` carries only
  the frames, so the harness was told where and not what; `fail()` now prints both, which is
  how the two `bezierCurveTo` faults were found in one run each instead of by bisection.

### Known-bad candidates
- **The rasteriser has no letter super/subscripts, and `10^-A` written with U+1D2C is
  tofu.** The BRIEF already says letter subscripts are unsafe; superscript capital A
  (U+1D2C), superscript small c (U+1D9C) and U+141F are not in DejaVu Sans either, so
  `10⁻ᴬ` and `10⁻ᴱᐟᴸᶜ` render as boxes. Digit superscripts are fine. Write exponents on the
  canvas as `10^-A`.
- **`bezierCurveTo`, `quadraticCurveTo` and `ellipse()` are all invisible to
  `tools/recorder.js` and absent from the selfTest stub.** A curve drawn with one records as
  nothing and throws headlessly. Draw them as explicit polylines (the same lesson the
  mosquito's body taught in `pupil_plane_interferometry.html`, one primitive wider).
- **The caption is drawn last and occupies the stage the whole time.** Register its measured
  rectangle in `LABELS` at layout time or every dodging label will dodge everything except
  it. Ninety collisions in this file came from that one omission.
- **`legendAuto()` checks `POLY_SEGS` and not `LABELS`, and records nothing of its own.**
  Use a wrapper that tests both registries and pushes its own text box, or legends and
  labels will keep landing on each other in both directions.
- **One tick COUNT cannot serve a 1400 px stage and a 560 px one.** Derive `nx`/`ny` from
  the panel's own width and height. And the x tick that sits exactly on the left edge
  collides with the y tick label at the same corner by about a pixel — drop it.
- **A frame-rate-dependent particle rule is a rate you did not choose.**
  `round(max(1, rate * n * dt))` delivers `rate` only when `rate * n * dt` is a whole number:
  at 60 fps PhET's shaker is 50 % fast and at 120 fps it is 200 % fast. Before blaming a
  floor or a rounding for an over-delivery, evaluate the expression at more than one frame
  rate — the half that does it changes.
- **Two guards on one path make each other's mutant equivalent** (already on the list from
  `buoyancy.html`, and it happened again here between `trueRGB`'s `Math.max(0, ...)` and
  `srgbGamma`'s own clamp). One guard, in the function that owns the quantity.
- **A branch that cannot be reached with the shipped data is not covered by anything, and
  the honest fix is to assert the data property rather than to delete PhET's branch.** Two
  of `SoluteColorScheme`'s four are unreachable because every solute has `cMin = 0` and a
  minColor equal to water.
- **PhET's `doc/model.md` is not PhET's code.** For beers-law-lab it writes the concentration
  clamp against the stock concentration (the code uses the saturated one) and the precipitate
  as a difference of concentrations (the code takes a difference of moles). Read the
  minified build, not the prose.
