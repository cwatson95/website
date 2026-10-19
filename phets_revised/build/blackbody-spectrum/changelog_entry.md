## 2026-09-18 — blackbody-spectrum: Planck's curve with PhET's thermometer, zoom, Graph Values and star, plus the colour two ways, Wien's peak, the Stefan–Boltzmann area and the classical limits
### Added
- `blackbody-spectrum.html` (160 KB), a remake of PhET's Blackbody Spectrum 1.0.26 in five views:
  *the spectrum*, *the star*, *the peak*, *the total*, *the limits*. Credit line in the header and
  on the page; site nav absolute; no network.
- *The spectrum* is PhET's one screen. It has every control PhET's has:
  - the thermometer (200–11000 K, snapping to 50 K), draggable on the canvas and mirrored by a
    slider, with PhET's presets as chips (Earth 250 K, Light Bulb 3000 K, Sun 5800 K,
    Sirius A 9950 K);
  - PhET's zoom ladders (wavelength ×2 from 0.75 to 48 µm, power ×5 from 1.024×10⁻⁵ to
    2500 MW/m²/µm), whose buttons disable at the ends;
  - Graph Values: a point dragged along the curve. As in PhET, it is clamped to the axis, hidden
    past it, sent back to the peak on every temperature change and whenever it is switched on,
    and it shows cue arrows until the first drag;
  - Labels: X-ray, ultraviolet, visible and infrared, cut at 10 nm, 380 nm, 780 nm and 100 µm.
    As PhET does, a band is named only where it is at least 20 px wide;
  - Intensity: the shaded area, σT⁴;
  - two saved curves;
  - the star with PhET's B/G/R photometer and halo.

  House additions: Wien's peak marker, a "fit the axes" button, the share of σT⁴ inside the
  window, and zoom warnings printed on the canvas.
- *The star* sets PhET's photometer, reproduced exactly (the curve sampled at 650, 550 and
  450 nm, divided by the largest of the three, dimmed by min(1, 0.02√(T − 798 K))), against
  CIE 1931 colorimetry over the CIE's own table. It adds strips over the whole thermometer, the
  three channels against T, and the luminous efficacy (at most 95.43 lm/W, at 6628 K).
- *The peak* shows the family on log–log axes with the locus of the peaks (slope −5). Divided by
  their own peaks, all the curves collapse onto one universal curve (half maximum from 0.613 to
  1.817 λ_max), and B_ν peaks at 1.760 λ_max.
- *The total* plots σT⁴ against T (slope 4), matched by a 1024-point Gauss–Legendre integral of
  the curve, and the band budget: the Sun puts 46.6 % into the visible, a 3000 K filament
  12.7 %, and Sirius A puts 44.0 % into the ultraviolet.
- *The limits* sets Rayleigh–Jeans and Wien against Planck, with each law's ratio to Planck:
  (eˣ − 1)/x and 1 − e⁻ˣ. At the peak, Rayleigh–Jeans is 28.66 times too high and Wien's law
  0.70 % low. Each is within 1 % of Planck on one side only: x < 0.019868 for Rayleigh–Jeans,
  x > ln 100 for Wien.
- **Exact:**
  - h, c and k are the exact SI values. c₁, c₂, σ, b and ν_max/T are derived from them and equal
    scipy.constants (CODATA 2022) to the last digit.
  - x₅ and x₃ are checked against Lambert W and against Newton's method in 50-digit arithmetic.
  - 75 values of M_λ are checked against 50-digit decimal arithmetic, to 1e-14 × max(10, hc/λkT).
  - The band fractions come from two series joined at x = 2. The Bernoulli head series takes its
    coefficients from power-series division, pinned to exact rationals. The exponential tail
    series is the other. Both are checked against scipy quad, exact rationals and 50-digit
    series.
  - σT⁴ agrees with scipy quad to 4e-16 and with Gauss–Legendre to 2e-14.
  - Chromaticities are sums over the CIE table.
  - The Illuminant A chain: a Planck body at 2855.496 K reproduces the CIE's A table to its
    printed precision (4.8e-6) and its chromaticity to 4e-8.
- **Verification:**
  - selfTest: 1035 passed, 0 failed under osascript.
  - UI drive: 160 passed, 0 failed.
  - Mutation sweep: 78 caught of 78 (65 physics, 13 UI), none survived or skipped.
  - Audit: 0 layout problems at 1400×820 and 1100×700. At 560×380 it reports only the
    under-readout advisory that every house sim shows there.
  - Every view's PNG was looked at.
- **Sources:**
  - `build/blackbody-spectrum/CIE_xyz_1931_2deg.csv` (with its metadata) and
    `CIE_std_illum_A_1nm.csv`, fetched from files.cie.co.at. Every fifth row of the first is
    embedded verbatim by `derive.py`.
  - PhET's constants, read from `docs/phets/blackbody-spectrum_en.html`. PhET's own c₁, c₂, σ and
    b differ from CODATA by +4.0e-5, −4.8e-6, −2.5e-7 and +3.6e-7. This file uses CODATA
    throughout.
### Fixed (during the build)
- **The reference for the thin band beyond 100 µm was wrong.** The JS disagreed with it by 1e-11
  to 3e-10. The cause was in `derive.py`: it converted the 50-digit F to float before computing
  1 − F, which keeps about 6 of the 15 digits of a 10⁻⁷ share. The JS, which evaluates the share
  directly from the head series, was the accurate one. The subtraction now happens in Decimal,
  and the exact-rational head series agrees to 3e-16.
- **The 50-digit tail series in `derive.py` was truncated.** Capped at 4000 terms, it was wrong
  by 1e-12 at x = 0.001, where it needs about 36/x terms. The number of terms now follows x.
- **The join of the two series is not a free choice.** I had expected any join between about
  0.02 and 6 to be an equivalent mutant. Measuring it (`join_window.py`) showed that x = 2 is
  pinned from both sides:
  - below it, the complementary route 1 − tail loses digits on thin long-wavelength shares (a
    join at 0.5 fails at 4.9e-14);
  - above it, the head series' truncation shows (a join at 4 fails at 1.4e-13).
- **Tick labels collided at the origin** ("0.0" against "0") in the spectrum and limits views:
  the bottom y tick and the left x tick overlapped by about 1 px under the audit's half-pixel
  rule. The bottom y tick is now dropped wherever an x tick sits at the left edge.
- **Labels of curves off the top of the axis landed on the frame.** They were crossed by the
  band-edge ticks and pushed the band labels down into the plot. Now the band labels claim their
  row first, a curve off the top is labelled just inside the frame, and every curve label is
  placed by `labAvoid`. That is a Liang–Barsky segment–box test against each drawn curve and
  against the Graph Values lines, which are now drawn before the labels.
- **Axis maxima printed with significant-figure padding** ("0–3.00 µm by 0–100.0").
  `axisMax()` prints the ladder value instead: 3, 0.75, 5.12×10⁻⁵.
- **The INFO prose called the Earth's peak "a hundred-thousandth" of the Sun's.**
  (250/5800)⁵ = 1.5×10⁻⁷, about a seven-millionth.
- **A reference value from mental arithmetic** (x₅/x₃ = 1.7597810788957716) was replaced by a
  printed one (x₃/x₅ = 0.5682526605497431) before its first run.
- **The first substance floors were guesses** (8, 8 and 4 fills), and they failed correct views:
  the limits view has one fill, and its substance is curves. The floors are now per
  configuration, on fills plus strokes, curve segments and texts, at 80 % of what each
  configuration emits (`set_floors.py`).
- **The CIE glow read as a target.** It was five nested translucent discs; it is now one flat
  halo in PhET's own style.
- **A tautological assertion (`…||true`) got into the UI drive.** It was caught before it ran,
  removed, and replaced by a real repaint check.
- **The first sweep left three survivors, all test gaps.** All three are caught on re-run:
  - "fit frames 4 λ_max": at every preset, 4 λ_max and 5 λ_max round up to the same ladder step.
    4500 K separates them.
  - "Graph Values shown past the axis": the test point, at 2000 nm on a 750 nm axis, was beyond
    even the mutant's doubled limit. A point at 800 nm separates them.
  - "the Graph Values checkbox does not re-centre": the point was already at the peak when the
    checkbox fired. A sentinel is now set immediately before the action.
- **`tools/mutate.py` writes its scratch `_mutant.js` next to the HTML it tests,** and several
  agents build into `docs/phets_revised/` at once. The sweep therefore ran on a copy inside
  `build/blackbody-spectrum/_out/`.
### Known-bad candidates
- **The house CMF fit has a red tail that falls 12 to 60 times too fast beyond 700 nm.** This is
  the Wyman–Sloan–Shirley fit (2013) in `diffraction.html` and `blackbody_radiation.html`. Its
  x̄/ȳ is 1.317, 0.228 and 0.048 at 700, 750 and 780 nm, where the CIE table's is a constant
  2.769. A Planck body therefore comes out greener than it is: Δx = −0.018 at 800 K, −0.011 at
  1000 K, −0.004 at 1500 K and −0.001 at 3000 K. That is why `blackbody_radiation.html` needs a
  700 K colour floor. The CIE table itself, every fifth row, is 95 rows and 5 KB.
- **Three samples of a spectrum are not a colour.** PhET's photometer paints the Sun at 5800 K
  cyan-white (223, 255, 253), where colorimetry gives warm white (255, 241, 235). It paints a
  3000 K filament (239, 144, 56), where the eye sees (255, 184, 109). Any scheme that colours by
  sampling the spectrum exaggerates saturation.
- **`255·a·v/r` with v === r is not always 255 in floating point.** PhET's star floors its
  brightest channel to 254 at 4000 K and 11000 K. Pin the value before the floor and accept 254
  or 255; pinning the floored channel pins rounding luck.
- **A reference share computed as 1 − F from a float F keeps about 6 digits of a 10⁻⁷ number.**
  Subtract at high precision, then convert.
- **`tools/mutate.py` puts its scratch file beside the HTML under test,** so concurrent sweeps in
  one directory race on it. Sweep a copy inside your own build dir.
- **PhET's Blackbody Spectrum 1.0.26 has no ruler.** Its ScreenView adds only the graph, the
  control panel, the saved-graphs panel, the thermometer and its labels, the B/G/R star display
  and reset. Its "peak marker" is the Graph Values point, which PhET sends to the peak on every
  temperature change.
