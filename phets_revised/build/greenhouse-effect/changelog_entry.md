## 2026-09-21 — greenhouse-effect: PhET's three screens on one exactly solvable layer model, and the line between its fit and its physics

### Added
- **`docs/phets_revised/greenhouse-effect.html`** (181 KB, 3179 lines) — a remake of PhET
  Interactive Simulations' *Greenhouse Effect* 1.3.13 in the house style. Five views:
  **the waves** and **the photons** (PhET's Waves and Photons screens: twelve sheets,
  concentration by slider or by date, the cloud, the glaciated ice-age ground, the
  thermometer in K / °C / °F, the energy-balance meter and the flux meter), **the layers**
  (PhET's Layer Model screen: 0–3 explicit sheets, their absorbance, ½–2 suns, the surface
  albedo, each sheet's temperature), and two analysis views of this file's own, **the
  ladder** and **the record**.
- **The whole model is exact, and derived rather than asserted.** For N sheets of infrared
  absorbance a_i over a ground of albedo α under an absorbed solar flux F, each sheet
  conserving energy makes the net upward flux the same at every level, so
  `U_i = U_{i−1} − F a_i/(2 − a_i)`, and with `U_N = F` at the top

      sigma T_s^4 = F [ 1 + Σ_i a_i/(2 − a_i) ].

  It is implemented **twice** — that recursion, and a dense Gaussian solve of the full
  13-unknown flux system that never uses the net-flux invariant — and the two agree to
  4e-15 over 131 stacks. Energy balance holds at every sheet, at the ground and at the top
  to 9e-13 W/m², and the net flux is constant with altitude to the same. For a_i = 1 it
  collapses to the textbook `T_s = (N+1)^(1/4) T_eff`, asserted at every N from 0 to 12,
  and the general law at 24 (N, a) pairs.
- **σ two ways and the Earth's 255 K.** `scipy.constants.Stefan_Boltzmann` and
  `2π⁵k⁴/15h³c²` built from CODATA h, c, k agree to 1e-15; PhET's ten-digit rounding
  (5.670374419e-8, the constant the sim carries throughout) is 3.25e-11 away, worth 2e-9 K
  on a 300 K planet. `T_eff = 254.578 K` from the 2015 IAU nominal irradiance 1361 W/m²
  and a Bond albedo of 0.30 (254.03 K at NASA's 0.306), against the conventional 288 K
  surface — 33.4 K of greenhouse warming, which one perfectly absorbing sheet would
  overshoot (302.7 K). The real atmosphere is worth Σ = 0.638, i.e. **two thirds of one
  perfect sheet, or a single pane at a = 0.779**.
- **The photon picture tied to the flux solution exactly.** The chance an infrared photon
  leaving the ground escapes to space — absorbed with probability a_i on crossing sheet i,
  then re-emitted up or down at even odds — is `F / σT_s^4`, proved three ways: as a
  Markov chain (a linear solve over the 2N up/down states), as the closed form
  `1/(1 + Σ a_i/(2−a_i))`, and by a 200 000-walk Monte Carlo. The sim and `derive.py`
  share one 32-bit linear congruential generator (`s = (1664525 s + 1013904223) mod 2^32`,
  every product below 2^53 so both languages carry it exactly), and the suite pins the
  generator's stream, the walk's crossing/absorption/up counts and the escape fraction
  **bit for bit** against the Python twin, not merely within the sampling error.
- **PhET's own convention, and what it costs.** PhET's sheet absorbs a fraction a but
  radiates a full σT⁴ in *each* direction, which is not Kirchhoff's law. It makes no
  difference whatever to the fluxes or to the surface temperature — the emitted flux per
  direction is `a(U+D)/2` either way — and changes every sheet's reported temperature by
  exactly `a^(−1/4)` (19 % at a = ½, 50 % at a = 0.2). Both are asserted, and a tick box
  shows both.
- **PhET's fit named as a fit.** The concentration screens' `a_i = 0.85 c e^(−z/8400 m)` on
  twelve sheets at `i·50000/13 m`, the four dates' c = 0.625 / 0.7147 / 0.7182 / 0.7446,
  the sun's 343.6 W/m², the albedos 0.2 / 0.225 / 0.3, the cloud's 12.5 %
  (`0.125 × 85000/18000 × 18000/85000`, exactly), the 245 K and 125 K floors, the heat
  capacities 1250/1250 and 2500/840 with the 3e-7 volume coefficient, the photon rules and
  rates, and the CO₂/CH₄/N₂O printed beside each date were all read out of the minified
  original and are quoted as PhET's. Solving them exactly shows what PhET tuned: its 1750
  surface is **296.48 K (23.3 °C), 8.48 K above the real Earth**, while the *differences*
  are good — ice age −6.29 K against about −6 K observed, 2020 +1.32 K against about
  +1.2 K. The page says so in the caption, the readout and the header.
- **An independent check that this really is PhET's model, not a look-alike:** the hottest
  state its concentration screens can reach is **309.13 K** by this solve, and PhET
  hard-codes **309** as its thermometer's `EXPECTED_MAX_TEMPERATURE`.
- The temperature is integrated with PhET's own heat capacities (the ground's response is
  exactly 32/15 K per J/m², a glass sheet's 1.5873) from PhET's own cold start (ground at
  its floor, every sheet at 0 K) in four forward-Euler sub-steps of a 1/60 s frame, inside
  the ODE's own stability bound `h < 2/(8 K σ T³)` = 0.0198 s at 520 K, which the stepper
  **clamps against**. The march is pinned frame by frame against the numpy twin at frames
  1, 6, 60, 300 and 1800.
- Verification: `selfTest` **1333 passed, 0 failed**; UI drive **174 passed, 0 failed**;
  mutation sweep **91 caught, 0 survived, 0 skipped** (85 physics + 6 UI); display-list
  capture at 1400×820, 1100×700 and 560×380, **0 layout problems** at all three, every
  view's PNG looked at. `derive.py` runs 82 of its own checks. Reference values are printed
  at `%.17g` so the JavaScript is pinned to the twin at full double precision.

### Fixed (during the build)
- **The flux meter read the steady state while the picture showed the live model.** With
  the sun switched off the exact solve is identically zero, yet the ground sits at its
  245 K floor radiating 204 W/m² and the infrared waves are still drawn — and the sensor
  read `up 0.0`. Root cause: the meter and the probe were wired to `solveClosed`'s profile
  rather than to `fluxesNow`'s. Both now read the LIVE model, as PhET's do, and the panel
  draws the exact steady profile beside them; `selfTest` asserts they coincide to
  1e-8 W/m² once settled and that they part company with the sun off.
- **Altitude zero was the bottom of the window, not the top of the ground.** Every photon
  below about 2 km was drawn inside the soil. The map now takes the ground band's height.
- **`new Array(1.5)` is a RangeError, not a rounding error.** The sheet-count slider has
  step 1, but the UI harness drives every slider to its midpoint, and 1.5 sheets took the
  ladder view down with a bare `viewLadder@` stack and no message. The count goes through
  `nSheets()`, which rounds and clamps.
- **The ladder's "stack you have loaded" read the wrong atmosphere.** `atmosphere()`
  special-cases only `view === 'layers'`, so on the ladder view it returned the twelve-sheet
  concentration stack and the absorbance slider did nothing to the readout. The ladder now
  builds the layer model's stack explicitly. A second, subtler half of the same bug: the
  marker must sit on the family the panel *draws* (PhET's F, albedo 0.2, one sun) while the
  readout carries the same sheets at the albedo and intensity actually set — two different
  questions, and the suite now asserts both and asserts they differ by 3 K at albedo 0.3.
- **`makeThermal` always started at the 245 K night floor**, so "reset all" left the layer
  model's ground 120 K above its own 125 K floor and the reset test failed. It takes the
  floor as an argument.
- **Three mutation survivors, each a real blind spot.** (1) The solar-intensity slider could
  be disconnected from the model and every layer-model assertion still passed, because they
  all recomputed F beside the model instead of reading `M.S.F` off it — the `drum_head`
  rule, again. (2) The ladder's equivalent-uniform-absorbance was never asserted off the
  built model. (3) The flux sensor's 14-px hit test could be narrowed to zero and the drag
  test still passed, because the harness clicked the sensor's *exact* pixel; it now clicks
  6 px off and asserts that 40 px away does not grab.
- **`&thinsp;` is not in the shared `ENTS` table**, so "F a/(2−a)" reached the canvas as
  `F&thinsp;a/(2−a)` in every caption. The table is extended from this sim's own part file
  (the shared helper is sha-pinned and must not change under the other builds), and the
  extension is asserted.
- **A stripped `<sup>` turns 10¹³ into 1013.** `plain()` removes tags, so `10<sup>13</sup>`
  in a canvas caption reads as one thousand and thirteen — a wrong number, not a cosmetic
  loss. Every superscript in canvas text is now a literal glyph (⁴, ¹³).
- **The energy-balance box's labels escaped it.** The "net" figure was positioned from the
  bars rather than from the box, so on a narrow window it landed in the thermometer column;
  and the box is drawn with `ctx.fillText`, which the label registry cannot see, so
  "redirected down" sat under "top of atmosphere" at every size until the box's rectangle
  was pushed into `LABELS` before anything else was labelled. The box now refuses to draw
  at all below 128 × 76 px, where it cannot hold its own labels.
- **The floating readout is invisible to the canvas.** The ladder's "Earth ≈ one sheet at
  a = 0.779" sat underneath it. `drawView` now registers the readout's rectangle
  (336 × 548, top right) in `LABELS` whenever the stage is wide enough that the layout
  keeps clear of it.
- **Two legend swatches of the same colour meaning different things.** The ice-age ring was
  drawn in the structure cyan to mark that it sits off the curve, and the legend then had
  cyan for both "with PhET's cloud" and "ice age (glaciated ground)" — the `sbs_sims`
  Known-bad in a new place. The ring is now the dates' own magenta and the gap is drawn as
  a dashed connector up to where that concentration would sit over a green meadow, with the
  connector's length asserted to be exactly what albedo 0.2 → 0.225 is worth.
- Layout: the analysis panels keep a measured 76 px below their frames for the axis title
  and the per-panel caption (the x-axis label sat inside the main caption at every size);
  per-panel captions are drawn only if they clear it; the thermometer's reading and scale
  note were overlapping its bulb; the record view's two closest dates (1750 and 1950, 0.0035
  apart in c) alternate above and below.
- **`SIZES=(${@:-a b c})` expands as ONE word in zsh when `$@` is empty**, so
  `capture_all.sh` with no arguments made a directory called `c1400x820 1100x700 560` and
  audited a file that was not there. (The same line is in `build/waves-intro/capture_all.sh`.)

### Known-bad candidates
- **Subscript LETTERS are not safe on the canvas: there is no subscript f in Unicode at
  all, and the ones that exist are not all in the rasteriser's font.** `T&#8337;&#8335;&#8335;`
  for T_eff came out as `T₆⃞⃞` — two tofu boxes — in `tools/raster.py`'s output, and
  nothing in the text audit can see it (the string is well formed and the entity decoded).
  Digit subscripts (a₁, CO₂, CH₄) and superscripts (⁴, ¹³) are fine. Write letter
  subscripts as ASCII (`T_s`, `T_eff`, `a_i`) on the canvas, and keep `<sub>` for the
  readout and the equation bar, which are HTML.
- **A quantity that has both a "now" value and a "steady" value must say which one every
  instrument reads, and the awkward case is the one where they differ.** Here the flux
  meter reads the live model and the panel draws the exact profile beside it; the test
  that matters is not the settled one (where they agree trivially) but the sun-off one,
  where the steady solve is identically zero and the model is still radiating 204 W/m².
- **PhET's grey layer is a grey absorber and a BLACK emitter**, which is not Kirchhoff's
  law. Do not "fix" it: the fluxes and the surface temperature are identical either way
  (the emitted flux per direction is a(U+D)/2 in both), and only the sheet temperatures
  differ, by exactly a^(−1/4). Both conventions are implemented and asserted; the file
  says which is which.
- **PhET's absolute temperatures are about 8.5 K high and its differences are right.**
  Anyone comparing this remake's 296.48 K at 1750 with the real 288 K should reach for the
  caption before reaching for the solver: it is PhET's concentration fit, faithfully
  solved, and the page says so in four places.
