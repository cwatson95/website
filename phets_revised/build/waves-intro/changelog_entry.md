## 2026-09-21 — waves-intro: PhET's three screens on the landed wave-interference engine, PhET's own light screen and tone, and v = fλ measured on the lattice by least squares
### Added
- `waves-intro.html` (183 KB, 2775 lines), a remake of PhET's Waves Intro 1.1.24 in four views:
  *water*, *sound*, *light* — PhET's three screens, one view each — and *the three media*,
  an analysis view of the law that ties them together. Credit line in the header and on the
  page; site nav absolute; no network.
- **PhET's three screens.** One hard source five cells in from the left edge of PhET's
  151 × 151 lattice, with frequency, amplitude and PhET's green wave-generator button
  (continuous: it switches the source on and off and restarts its phase at zero; pulse: it
  fires one period and pops back up, and is dead while that pulse runs — PhET's
  `handleButton1Toggled`, and its `disturbanceTypeProperty` link, which stops everything when
  the mode changes). Each screen keeps its own lattice, as each PhET screen keeps its own
  model. Water adds PhET's top and side views, sound its air parcels (waves / particles /
  both) and PhET's tone, light the screen at the right-hand edge. Graph of the centre line,
  tape measure, stopwatch, two-probe wave meter, normal and slow speed, pause, one step,
  clear, reset all; the button, the tape's ends and the probes are dragged on the canvas.
- **Built on the landed engine, which is not re-derived.**
  `build/wave-interference/p2_engine.js` ships unchanged (its SHA-256 is pinned in
  `assemble.py`, with the four other house parts taken from that build), and the lines this
  sim needs from its proof — the dispersion relation, the calibration of the three media,
  Mur's coefficients — are read from `build/wave-interference/refvals.txt` rather than derived
  again. This build's own numpy twin reproduces that file's tank and pulse scenarios to
  **1e-13** before adding its own: sound at 0.2937 per ms, light, a source switched off at
  step 150 and on again at 190, and the light screen.
- **Exact:**
  - the lattice's dispersion relation and the time step solved from it at every frequency, so
    λ = v/f and T = 1/f hold along the lattice axes at all nine settings (three media × fmin,
    default, fmax) — PhET's one fixed step per medium leaves its wavelengths 0.7 % to 3.2 %
    short, which the readout prints for the current setting;
  - the engine's point-source path against the numpy twin at 1e-11 over five scenarios;
  - PhET's light screen as Waves Intro draws it, read from the minified original: the mean
    square of the last column over whole periods, a 3-row smoothing, a ±39-row box average
    (`lightScreenAveragingWindowSize` 40, against Wave Interference's 3) and PhET's
    piecewise-linear brightness table, pinned knot by knot;
  - PhET's tone: 1000 f Hz at output level 0.3 A/10, as a looped buffer of whole cycles whose
    samples are computed here rather than taken from an OscillatorNode, so the suite can check
    the pitch, the level and the seam.
- **New here — the wavelength measured on the lattice.** At every cell of the tank's axis a
  least-squares fit against the drive's own phase (sin, cos, a constant and a drift, the last
  two to absorb the 2-D wake of the switch-on, which dies only as 1/ωt); the wavelength is the
  slope of the unwrapped phase over cells 30 to 100, the envelope's power the slope of log
  amplitude against log r. The JS and the numpy twin agree to **4e-16**. What it finds:
  - λ within **0.03 %** (light), **0.08 %** (water) and **0.15 %** (sound) of v/f at PhET's
    default frequencies, and an envelope power of **−0.47 to −0.54** against the −½ that 2-D
    spreading demands;
  - at water's 0.25 Hz, where the tank is 1.4 wavelengths long, **1.6 % short** — of which the
    2-D near field (the phase of H₀(kr), scipy, fitted over the same cells) is 0.46 % and the
    rest is the tank: on a 401-cell lattice the same fit returns 0.49 %;
  - the light screen departs from the 1/r of a point source by up to **9 %**: a ripple of about
    one wavelength's period that the edges reflect back (rms 2.0 % on PhET's 151 cells, 1.5 %
    on 401, 0.75 % on 601) on a smooth **6 %** tilt that is the square lattice's own
    anisotropy. PhET's ±39-row average smooths the ripple away, which is why it is there.
- **Verification:** selfTest 968 passed, 0 failed under osascript (a layout sweep of 15
  configurations × 4 sizes, every slider end in every medium at both amplitude ends and both
  modes, and the #hint corner asserted clear). UI drive 164 passed, 0 failed: three custom
  pointer actions (PhET's button, a tape end, a probe), each through the frame loop from a
  proven-idle baseline, every tab, slider, checkbox, chip, button and key, resize, the tone
  against a stub AudioContext, and reset-all against a fully disturbed state. Mutation sweep:
  98 mutants (79 physics, 19 UI), every one on a copy inside `_out/`. All 79 physics mutants
  were swept under jsc against the shipped file — **79 caught, 0 survived** — after proving the
  runner can see a failure; `tools/mutate.py` itself, under osascript, swept all 19 UI mutants
  and a 29-mutant physics cross-section covering every layer of the file and all three
  first-round survivors — **48 caught, 0 survived** — and the two runners agree on every mutant
  they share. Audit: 0 layout problems at 1400×820, 1100×700 and 560×380 (at 560 the
  under-readout advisory only). All fifteen captured views were looked at.
- **Sources:** PhET's values, read from `docs/phets/waves-intro_en.html` (1.1.24): the lattice
  (151, pad 20, C = ½, source column 25, row 75), 20 × 111/61 steps per second, the amplitude
  calibration 1.2 and range 0–10 with 8 initial, the colour scale 2.14, the three media
  (widths, speeds, frequency ranges starting mid-range, scale bars, time scales), the 90-step
  intensity history and its 3-row smoothing, the screen's ±39-row window and brightness table,
  and the tone's 1000 f Hz and 0.3 A/10. PhET's model note for waves-intro ("a subset of the
  Wave Interference simulation, which shows one scene per screen") was fetched from GitHub.
  Colour: the CIE 1931 2° table (DOI 10.25039/CIE.DS.xvudnb9b), via the file the
  blackbody-spectrum build fetched.
### Fixed (during the build)
- **A claim about a drawing's scaling was true only where the field is inside the colour
  scale.** The parcel displacement is scaled so that a wave at PhET's full colour (2.14) moves
  a parcel 0.3 of its spacing — but beside a point source the field is four times that, and
  the largest push is really 0.39 of the spacing. The caption, the derivation and the header
  all said 0.3. They now say what derive.py measures, and the parcels are pinned against the
  twin position by position.
- **Three sliders are labelled "amplitude", one per medium, and the UI harness found the wrong
  one** — the hidden light slider rather than the visible water one, so two assertions failed
  for a reason that had nothing to do with the sim. The finder now takes the visible row.
- **A silent tone cannot be shown to be stopped.** The tone tests ran with the clock paused
  from an earlier block, so "switching the source off stops the tone" passed vacuously on the
  stop count and failed on the assertion that could see it. The clock now runs through the
  whole tone sequence — the dual of a proven-idle baseline.
- **An HTML entity in a checkbox label.** `intensity graph (not in PhET&rsquo;s Waves Intro)`
  is built from a text node, where a browser draws the entity verbatim. The UI harness now
  walks every label, button and heading for `&…;` (and deliberately not the `.tag` and `.src`
  blocks, which are set through innerHTML, where entities are right).
- **Op-count floors, three times over.** One floor for every configuration failed the side
  view (10 fills, honestly) and the analysis view (curves, not fields), and would have passed a
  blank field view. Each configuration now carries its own floor at 70 % of what it emits at
  its leanest size, and the tab floors come from the first draw, which is a tank with no waves
  in it yet.
- **A caption long enough to squeeze out the panel it explains.** At 1100 × 700 the full
  caption left 30 px under the plane, so the three measurement strips — the point of the view —
  were dropped. The layout now falls back to the short caption when that is what keeps them.
- **Three significant figures hid the difference a row exists to show.** The analysis readout
  printed "104 cm" for v/f and "104 cm" for the measured wavelength. Both are now at four
  figures (103.9 against 103.8).
- **`sigf` renders 2.998e8 as "2.998×10^+8".** The speed of light appears in the readout, the
  caption and a canvas label, so there are now `sciTxt` (superscript glyphs) and `sciHTML`
  (`<sup>`), asserted against both forms.
- **A label hung to the left of a marker lies along the line it names.** The light line's
  label cannot go above-right (it would run under the floating readout), and below the marker
  it collided with the axis ticks at 560 px — caught by the layout sweep. It now clears the
  line's own rise, falls back to the medium's name alone, and is dropped if even that will not
  fit; the caption and readout still carry all three speeds.
- **The side view's source spike ran to the floor of the picture.** The source cell swings 1.2
  × the amplitude — 9.6 lattice units at the default, four and a half times the colour scale of
  2.14. The surface is clipped at ±1.8 of that scale and the caption says so.
- **The marked air parcel was magenta**, which in this sim already means the source, its
  button, the tape's ends and the probes. It is cyan, and the caption names it.
- **The wave meter's window was 2.5 periods of the medium's SLOWEST frequency** (inherited from
  wave-interference), so at the default the chart was 60 % empty. It is 2.5 periods of the
  frequency on show.
- **The tone's rounding was pinned only where rounding cannot be caught.** At 0.33 and 0.44 per
  ms the cycle count and the buffer length come out exact, and at 0.2937 both fractions are
  above ½ — so round → floor and round → ceil would both have survived, exactly as
  wave-interference's Known-bad predicts. A fourth case at 0.301 per ms (150.5 cycles,
  22123.25 samples) pins both.
- **The sweep's three survivors were all test gaps, and one was dead code.**
  - *a new medium restarts the clock* (`R.t = 0` in `runSetScene`): only the UI suite could see
    it, because the physics suite never reset a run that had been **stepped**. It now asserts
    that `resetRuns` puts t, n, the lattice, the amplitude, the mode and the stopwatch back.
  - *the unwrap's second branch*: this wave travels outward, so its phase only ever falls and
    the `d < −π` branch is reached by no measurement in the file. The unwrap is now a function
    of its own (`unwrapPhase`), asserted in both directions — including a rising ramp of
    0.41 rad a step through every wrap, which nothing in the sim produces.
  - *solve4's pivot search* (largest → smallest pivot): a well-conditioned 4 × 4 is solved to
    1e-12 whichever pivot is taken, so no measurement could see it. It is now given a system
    whose first pivot is zero, which only a row swap can solve.
- **A mutant that turns a correction loop into an infinite loop hangs the sweep, and the
  runner's timeout takes the whole run down with it.** The first draft mutated
  `while (d > π) d −= 2π` into `d += 2π`, which never terminates — `tools/mutate.py` has no
  per-mutant timeout handler, so the sweep stalled there and would have aborted 30 minutes
  later. The pattern now changes the correction from 2π to π, which still changes the answer
  and still ends, and the other branch is mutated the same way.
- **`capture_all.sh` would have audited one size while looking as though it audited three.**
  `SIZES=(${@:-1400x820 1100x700 560x380})` puts the whole default into ONE word in zsh when the
  script is run with no arguments, so it makes a single directory called
  `c1400x820 1100x700 560` and captures once. Every run here passed the three sizes explicitly,
  so the captures were right, but the trap was live (another build in this batch hit it). The
  default is now its own array, and the script was re-run with no arguments to prove it: three
  directories, three audits, 0 problems.
- **A second estimator was added for the wavelength, not a second assertion.** The phase-slope
  fit is now checked against the spacing of the snapshot's own zero crossings, which shares no
  code with it: they agree to 0.008–0.024 % at four settings. At water's 0.25 Hz the fit window
  holds only **two** crossings, so that estimator is a single spacing there — which is pinned
  too, because it is the reason the hard case is hard.
### Known-bad candidates
- **A scaling described "at full colour" is not a bound near a source.** A displacement scaled
  so that a full-colour wave moves a marker 0.3 of a spacing will move it further wherever the
  field exceeds full colour — beside a hard source it always does. State what the sweep
  measures, not what the scale factor was chosen for.
- **A caption can squeeze out the panel it is explaining.** Where a layout puts a measured
  caption and the panels in the same column, the caption must be allowed to shorten, or the
  first thing lost at a middling window size is the content.
- **Three significant figures hide the difference a comparison row exists to show.** When a row
  prints a measurement beside the theory it is being compared with, give both enough figures
  for the difference to survive the rounding.
- **A label beside a marker on a sloped line must clear the line's own rise, not just the
  marker.** Hung to the left of a marker on a line of slope −1 in screen pixels, a horizontal
  label lies along the line unless it is lifted by (its own length) × (the line's slope).
- **A harness finder must pick the VISIBLE control when several share a label.** Three sliders
  labelled "amplitude", one per medium, and only one on show: matching the last one found is
  matching the wrong one (the same family as wave-interference's "achromat" chip).
- **A tone that is already silent cannot be shown to be stopped.** Any test that an action
  stops something needs that thing demonstrably running first, the way a repaint test needs a
  proven-idle baseline.
- **`SIZES=(${@:-a b c})` is one word in zsh, not three.** A capture script whose default sizes
  are written that way silently captures a single size named after all of them, and its audit
  then covers one picture while reading as though it covered every size. Give the default its
  own array, and run the script once with no arguments to see what it really does.
- **`wave-interference.html` fits its captions to H, not H − 18**, so the last line of its
  bottom-anchored captions shares pixels with the house `#hint` — the trap `BRIEF.md` records
  from wave-on-a-string, which the display-list capture cannot see because the hint is HTML.
  This build reserves the 18 px (`HINT_H`) and asserts that no canvas text enters the hint's
  corner, at four sizes and fifteen configurations. That build was not touched.
- **PhET's Waves Intro can never show its intensity graph**: the screen is built with
  `showIntensityCheckbox: false`, so `showIntensityGraphProperty` stays false forever. Reading
  Wave Interference's controls as Waves Intro's would put a control on the page that PhET's
  own build cannot reach.
