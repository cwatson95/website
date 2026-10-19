## 2026-09-21 — generator: water turns a magnet beside a pickup coil, and the flux integral that makes the EMF, in six views

Remake of PhET's Generator 1.0.7 (`docs/phets/generator_en.html`; its single
screen comes from the shared FARADAYS_ELECTROMAGNETIC_LAB repo) as
`generator.html`. Third sim cut by `family.py` from the engine in
`build/magnets-and-electromagnets/`: the electromagnet (`#emag`), the bar-magnet
screen (`#bar`) and the far-field view (`#far`) are stripped, the coil DRAWING
(`#coil`) and the generator (`#gen`) are kept, and the build asserts that no
symbol of a stripped feature is left in the file. New code; no PhET code or
assets.

### Added
- **the generator** — PhET's screen: a faucet whose flow turns a water wheel
  carrying the bar magnet; a pickup coil of 1–4 loops whose area runs over
  PhET's 20–100 % of 70685 mm²; a light bulb or a voltmeter; electrons whose
  speed shows the induced current (with PhET's electron/conventional Current
  Flow preference); the wheel's speed written in its hub, as PhET's RPMDisplay
  does; the field as PhET's 40-mm needle grid; a compass, which here rides a
  TURNING field and lags it; the field meter.
  **flux and EMF** — Φ(θ) over one turn of the wheel against the single cosine
  a distant magnet would give, and below it the EMF, −Nω dΦ/dθ, with its peak
  marked (it is not at 90°). **the coil face** — the two ways of adding the
  field over the coil's disc, drawn as integrands whose AREAS are the two flux
  estimates: the exact strip (B integrated along the chord, off the page as
  well as in it) against PhET's (the in-page value carried across the chord,
  with its own 5-mm samples), and below, their ratio across the area slider.
  **field lines**, **on the axis**, **the needle** — the family's views of the
  magnet the wheel carries.
- What is exact: the magnet is the family's uniformly magnetised cylinder in
  closed form. **The flux is the AREA integral of B over the coil's disc** —
  16-point Gauss–Legendre in radius by 32-point trapezoid in angle, the field
  taken in 3-D off the page, asserted against scipy's `dblquad` to 1e-10 G·mm²
  at every angle and unchanged when both rules are doubled. One turn is sampled
  at 128 angles and kept as a Fourier series, so Φ(θ) and dΦ/dθ are exact
  between the samples; only odd cosines survive (Φ is even in θ and reverses
  every half turn) — asserted, not assumed, to 1e-11. **The EMF is Faraday's
  law**, −N dΦ/dt = −Nω dΦ/dθ: linear in N and in ω, reversed by reversing
  either, zero where the flux is stationary, checked against a finite
  difference of Φ itself AND against −dΦ/dt taken by stepping the page's own
  clock (whose midpoint error is checked for ORDER — halving the step quarters
  it — rather than pretended away).
- **Two findings about the original, both drawn on the page.** (i) Because the
  flux is not a cosine, the EMF does not peak with the magnet across the coil:
  it peaks at 24.79° for the smallest coil and 37.95° for the largest (python,
  bounded maximiser), the value at 90° being 0.29–0.60 of the peak. (ii) PhET's
  own flux is a line sample — B_x every 5 mm along the coil's vertical diameter
  in the page, each weighted by its chord, with the field off the page taken to
  be the field in it — which overestimates the flux by 13 % for the smallest
  coil and 57 % for the largest. That is not an error in PhET: its EMF is
  deliberately a relative number against its own full scale (maxEMF = 1.2e5 in
  its units), and a fast line sample is the sensible choice for it. This page's
  volts are volts only because the integral is done.
- PhET's values carried: the turbine and coil positions, 60 RPM at full flow,
  the drag rule (rpm = flow/100 × (1 − drag) × 60, drag a linear ramp in
  N × area from 0.01 to 0.2 scaled by the magnet's strength — phenomenological,
  and labelled so: a real back-torque needs the circuit's resistance, which
  neither PhET nor this page models), maxEMF, the 5-mm sample spacing, the
  1–4 loops and 20–100 % area, and the layout. The water falls on the LEFT of
  the wheel here so the magnet's angle increases; PhET steps its own the other
  way, which only reverses the sign of the EMF (said in the header).
- Verification: `derive.py` (the family's) grew section 7 — the flux against
  `dblquad`, its harmonics by numpy's FFT over 256 angles, the peak by a
  bounded maximiser, PhET's line sample, and the drag rule — plus
  `gen.drag`/`gen.drag.default`; selfTest 1162 assertions including a
  24-configuration × 5-size layout sweep; UI drive 198; mutation sweep 112 of
  112 caught (78 physics, 34 UI; 106 of 106 on the previous build, after the
  survivors below were pinned); display-list audit 0 problems over 23
  captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **The EMF peak came out at 155° instead of 24.8°.** Root cause: with only odd
  harmonics, |dΦ/dθ| is symmetric about 90°, so there are always TWO peaks and
  the coarse scan took whichever floating-point noise made larger. The search
  runs over the first quarter turn, as `derive.py`'s does.
- **The coil-face view drew two curves that lay exactly on top of each other.**
  Root cause: with the magnet in line with the coil — the view's own default —
  the field over the face depends only on the distance from the axis, so the
  ring average and the in-page value are equal BY SYMMETRY, and PhET's error at
  that angle is not a difference between them at all but a difference of
  weights. The panel now draws the two flux integrands strip by strip, whose
  areas are the two estimates; the exact one is asserted to integrate to
  `flux1` and PhET's, summed at its own 5-mm spacing, to `fluxPhet1`.
- **The pickup coil read as a copper barrel and the bulb sat behind it.** The
  turns are 44 mm apart now with a thinner wire, the leads are drawn before the
  front turns and the indicator after them, 92 mm above the coil's top.
- **The bulb looked dark when it was working.** PhET's brightness rule is
  |EMF|/full scale and this generator's peak is only 0.57 of full scale, so the
  glass is painted through a NAMED display mapping, `bulbShade` = sqrt — the
  same kind of thing PhET does to the needles' alpha. The model number is
  untouched and the readout prints it.
- **Every flux tick label read "0.0000".** Root cause: the flux is ~1e-6 Wb and
  `tickFmt` caps at four decimals. The flux axis is in microwebers.
- **Two stacked panels cannot both carry an x label**: the house layout leaves
  46 px between them and the lower panel's title starts 24 px above its own
  box, so the upper x label and the lower title collided at 560 × 380. The
  upper panel's x quantity went into its title.
- **14 mutants survived the first sweep.** The real ones: nothing pinned the
  clamp on the normalised current (and it turns out nothing can REACH it here —
  the largest EMF the sliders allow is 0.57 of full scale, now asserted, where
  PhET's larger flux estimate is what its clamp is for); nothing pinned the
  bar's dipole moment or m = M V on a page with no far-field view (the axis
  view's dipole curve is now asserted against the exact field at 4 m); nothing
  measured the flux view's live marker, the drawn turns' centring, the
  indicator's clearance from the coil, or the water landing on the wheel's rim;
  the compass was grabbed at its exact centre (so a lost drag offset made no
  difference) and its own motion masked the repaint after a move (the meter,
  grabbed off-centre with the compass away, tests both now); and the "tools are
  not in this view" check looked for a slider in a group that has none, so it
  passed everywhere. Two were equivalent and were replaced rather than excused:
  the Fourier normalisation differs only for k = 0 and the Nyquist term, and
  the series' sine terms are zero — both facts are asserted, so no mutation of
  them can change a number.
- **The wheel's speed was written under the magnet that is bolted across it**,
  so the capture showed a hub with nothing in it — which is the whole reason to
  look at the PNGs. It is drawn after the magnet now, on its own disc, and a
  test measures which fill is last at the hub.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **A test that compared the drawn water with the function that drew it.** The
  water's landing point is now a property: the bottom of the column lies ON the
  wheel's rim, at WHEEL_R from its hub, on the upper LEFT, which is why the
  wheel turns the way it does.

### Known-bad candidates
- **A view whose default setting hides its own point.** The coil-face panel was
  correct and useless at θ = 0. When a comparison collapses by symmetry at the
  default, either the default or the comparison is wrong.
- **Sampling a field along one line and calling it an area integral.** PhET's
  own rule, and the reason this page's flux had to be integrated properly; the
  error grows with the coil (13 → 57 %).
- **A display mapping must be named and kept out of the model.** `bulbShade` is
  a drawing constant with its own test; the brightness the readout prints is
  PhET's |EMF|/full scale.
- **`|dΦ/dθ| has two peaks`** — any extremum search over a symmetric function
  must state which half it is searching.
