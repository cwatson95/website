## 2026-09-18 — wave-interference: PhET's lattice with its time step solved from its own dispersion relation, two sources against their hyperbolae, slits against Rayleigh–Sommerfeld, and the far field as an FFT checked against Airy, sinc² and the Gaussian
### Added
- `wave-interference.html` (209 KB), a remake of PhET's Wave Interference 2.0.22 in six
  views: *the ripple tank*, *two sources*, *the slits*, *the far field*, *path difference*,
  *the lattice*. Credit line in the header and on the page; site nav absolute; no network.
- **PhET's four screens, one view each:**
  - *The ripple tank* is the Waves screen. It has water, sound and light, frequency and
    amplitude, and continuous or pulse. Water has top and side views; sound has waves,
    particles or both; light has the screen and its intensity graph. It also has the
    centre-line graph, the tape measure, the stopwatch and the two-probe wave meter (both
    probes and the tape end drag), normal and slow speed, pause, one step, and clear.
  - *Two sources* is the Interference screen. Each source switches separately, the separation
    is set per medium, and the nodal hyperbolae are drawn over the lattice.
  - *The slits* is the Slits screen: a plane wave with no barrier, one slit or two; slit width
    and separation; a barrier you drag by its handle. Moving the barrier clears only its right,
    as PhET's does. The light screen is compared with the Rayleigh–Sommerfeld sum and with the
    Fraunhofer formula.
  - *The far field* is the Diffraction screen. It has PhET's five apertures (ellipse,
    rectangle, circle & square, disorder, and a waving figure), plus a Gaussian and N slits for
    the closed-form checks. It has PhET's λ₀/λ rescaling, PhET's log(0.01|F| + 1) display or
    linear |F|², and the horizontal cut against the closed form.
- **The engine is its own part file** (`build/wave-interference/p2_engine.js`, API in
  `ENGINE.md`) for the waves-intro follow-up. It has:
  - PhET's lattice: 151 × 151 cells, a 20-cell pad and C = ½;
  - Mur's second-order absorbing edge;
  - point and plane sources, the screen and the probes.
- **Exact:**
  - The lattice's dispersion relation sin²(ωΔt/2) = C²[sin²(kₓΔx/2) + sin²(k_yΔx/2)]: Ω(k),
    k(Ω, θ) by bisection against scipy brentq, and phase and group speeds.
  - The time step is solved from that relation at every frequency. So λ = v/f and T = 1/f hold
    exactly along the lattice axes in all three media. PhET fixes one step per medium, which
    makes its wavelengths 0.7 % to 3.2 % short (derive.py; plotted on *the lattice*).
  - The driven plane wave is an exact lattice solution (5e-15 over 20 steps, axis and
    diagonal).
  - The engine agrees with a numpy twin that repeats every operation to 1e-11, over five
    scenarios of 150–400 steps.
  - Mur's reflection, from the plane-wave ansatz, is checked against a packet simulation to
    2 %: ≤ 3 % to 45° against 17 % for first order.
  - Two sources: the hyperbolae, their count 2⌈d/λ − ½⌉, and exact against far-field screen
    positions.
  - The far field:
    - |FFT| of the drawn aperture against numpy.fft.fft2 (eight apertures, six bins each) and
      against a direct DFT;
    - the pixel-snapped rectangle against the Dirichlet kernel (1e-15);
    - the sampled Gaussian against its continuous transform (5e-16);
    - the disc against [2J₁(v)/v]² (1.2e-3 of the peak for k ≤ 10, first ring on bin 16 of
      16.26);
    - J₀, J₁, sinc² and the N-slit factor against scipy.
  - Colour is the CIE 1931 table, every 5 nm, read from the CIE's file.
- **Findings (derive.py, stated on the page):**
  - At steady state the lattice's light screen follows the 2-D Rayleigh–Sommerfeld sum to 6 %
    (3 % rms) but misses the Fraunhofer formula by 26 %. PhET's screen sits 2.5 µm behind slits
    1.5 µm apart, where d²/λ is 4.4 µm. The first minimum falls 10 rows out on the lattice and
    in the Rayleigh–Sommerfeld sum, but 9 in the Fraunhofer formula.
  - The lattice's nodal lines sit 0.85 cells outside the continuum hyperbolae on average, 1.4
    at worst, always outward. The continuum 1/√r formula puts them within 0.08. The cause is
    the lattice's anisotropy: k(θ) differs by about 1 % between axis and diagonal at 11 cells
    per wavelength.
- **Verification:**
  - selfTest: 1453 passed, 0 failed under osascript. It includes a layout sweep of 37
    configurations × 4 sizes (each checked for overflow, collisions, entities, substance and
    a clear bottom-left corner), and every slider end across all media and apertures, finite
    and clean.
  - UI drive: 257 passed, 0 failed. It covers three custom drags, each through the frame loop
    from a proven-idle baseline; every tab, visible slider, checkbox, chip, button and key;
    resize; and reset-all against a fully disturbed state.
  - Mutation sweep: 81 caught of 81 (67 physics, 14 UI), 0 survived and 0 skipped in one pass
    against the landed file. The first sweep, before the caption fix, caught 78 of 81. Its three survivors were test gaps; they are now closed, and on a re-run against the final file all three are caught (see Fixed). The other 64 physics mutants cover every PhET constant, the Courant number, every Mur coefficient and sign, the dispersion relation, the calibration, the plane wave, the slits, the screen, the probes, the clock, the aperture renderer, the FFT, the closed forms, the theory curves and the colour. The 14 UI mutants cover the dirty flags, the frame loop, the drags, the panel and the keys.
  - Audit: 0 layout problems at 1400×820, 1100×700 and 560×380. At 560×380 it reports only the
    under-readout advisory.
  - Every view's PNG was looked at.
- **Sources:** PhET's values, read from `docs/phets/wave-interference_en.html`:
  - the lattice, the event rate, and the amplitude and plane-wave factors;
  - the colour scale 2.14;
  - the media (widths, speeds, frequency ranges, scale bars, slit and source ranges and
    defaults, time scales);
  - the 90-step screen history and the barrier range;
  - the diffraction grid (256 over 4/3 mm), the aperture ranges and defaults, and the λ₀/λ
    rescaling and log display.

  Colour: the CIE 1931 2° table (DOI 10.25039/CIE.DS.xvudnb9b), from the file the
  blackbody-spectrum build fetched. PhET's model notes were fetched from GitHub.
### Fixed (during the build)
- **The captions were fitted to the full canvas height, so their last line shared pixels with
  the house #hint box** (HTML, `bottom:11px`), which the display-list capture and `audit.py`
  cannot see because the hint is not canvas. Every caption is now fitted to H − HINT_H
  (18 px), as `build/wave-on-a-string/` and `build/waves-intro/` do, and the layout sweep
  asserts that nothing is drawn in the bottom-left corner. The assertion was checked against
  the defect first: all 148 configuration × size cases failed before the fix.
  The 18 px cost two narrow-stage adjustments:
  - at 560 × 380 the far field's cut plot no longer fits, so it is dropped with a note and
    its two squares take the height instead (190 px rather than 90); at 820 × 520 and above
    the cut is unchanged;
  - the tank's two "needs a taller window" notes take short forms below 300 px of tank, so
    they cannot run out past its right edge into the intensity graph's ticks.
- **A damping sponge in PhET's 20-cell pad made long waves reflect more, not less.** It gave
  60 % at 73 cells per wavelength against 0.03 % for Mur alone. A damping layer thinner than a
  wavelength is an impedance step. Mur's second-order condition alone gives ≤ 3 % to 45° for
  every medium.
- **A packet measurement said Mur-2 reflects 37 % at normal incidence for long waves.** The
  6-wavelength packet overlapped the edge at t = 0. The plane-wave ansatz gives 3e-4, and the
  packet agrees with the ansatz to 2 % wherever the packet fits.
- **The clock ran on across media.** A fresh tank read t = 65 s, left over from the selfTest's
  runs, because `runClear` does not reset time (PhET's clear does not either). A new medium now
  restarts `t`, `n` and the stopwatch.
- **The path-difference map was saturated flat green** (1/r near the sources). It now shows the
  interference factor I/(1/r₁ + 1/r₂), so the fading with distance is divided out.
- **The nodal overlays re-derived the hyperbola inline, twice**, and the ellipse's minor axis
  was written in both the renderer and the drawing. The duplicate ellipse formula was found by
  `gen_mutants.py`'s pattern-uniqueness check. All of these now call one pinned function
  (`hyperY`, `farY`, `ellipseAxes`).
- **The FFT cache key held all sixteen aperture parameters**, so a hidden slider forced a
  re-render. It is now keyed on the chosen aperture's own parameters.
- **Moving the barrier restarted the plane wave.** It now uses PhET's clearRight, which wipes
  from the new barrier rightward and keeps the wave's progress (asserted).
- **Layout.** The intensity graph's and the screen plot's axis labels landed on the caption:
  their boxes ran the lattice's full height, with the labels below. The rows are now measured.
  Other layout fixes:
  - the centre-line graph is dropped with a note where it cannot fit;
  - the origin ticks of the dispersion panel collided;
  - a medium label sat under the legend (the legend is now registered first, and the label
    falls back to the bottom);
  - the stopwatch box covered the water dripper;
  - the time label dodged into the tank at 560 px.
- **A path-difference screen drag was removed before it shipped.** The map is fitted to L, so
  the dragged line would have stayed put while the map rescaled under it.
- **Test fixes:**
  - a readout pin that was not off the model (the lattice's 34-cell separation prints 1532 nm,
    not the 1530 typed);
  - a J₁ join tolerance tighter than the house J₁'s own 1e-10 class (3.2e-10 across the join);
  - UI op floors guessed at 12 and 200 where the fields batch into 10 and 78 ops. They are now
    70 % of the measured emission.
- **The mutation sweep's three survivors were test gaps.**
  - The source rows were pinned only at the sound default, 22.2 cells, where round and floor agree.
    Water's and light's 16.65 cells are now pinned too.
  - The wave-meter probe was only read at cell centres, where the bilinear neighbour has weight 0.
    It is now read between cells on a linear field.
  - The rectangle snap was pinned at 10.9 and 21.8 px, where round and ceil agree. It is now pinned
    at 19.2 px on the width and on the height.
  All three are caught on the final file.
- **One retest baseline came back silent and red under heavy CPU load.** Run directly, and again on
  the retest, the suite was green (1305/0). It was a transient osascript failure, not the suite.
  Before reading a red baseline as a failure, run the suite directly.
- **A duplicate reference label** (two speed lines printed under one label) was caught by
  `derive.py`'s own guard: every value in `p7_refs.js` must be a distinct printed line.
### Known-bad candidates
- **The house #hint is HTML at `bottom:11px`, and it owns the bottom-left corner of the
  stage.** A caption fitted to the full canvas height sits on top of it, and neither the
  display-list capture nor `tools/audit.py` can see the overlap, because the hint is not
  canvas. Fit captions to H − 18 and assert the corner is clear.
- **A thin damping sponge reflects long waves.** A 20-cell σ-layer is an impedance step for a
  73-cell wave, and the reflection grows as σ/ω. Use Mur's second-order boundary, and measure
  the reflection before choosing.
- **Measure a boundary's reflection with the plane-wave ansatz, not a packet that touches it at
  t = 0.** The packet read 0.375 where the truth is 3e-4.
- **An overlay drawn from continuum geometry will not sit exactly on a lattice's features.** The
  nodal lines here run about a cell outside the hyperbolae, which is the anisotropy. Say so on
  the view rather than fudging λ.
- **|FFT| of a real aperture cannot see the FFT's sign convention** (|F(−k)| = |F(k)|). A test
  on complex input is what pins the twiddle sign.
- **PhET's one-step-per-medium calibration makes wavelengths short by 0.7–3.2 %.** Solving Δt
  from the dispersion relation per frequency makes them exact along the axes at no cost.
- **A rounding mutant is invisible at every test value whose fraction is ½ or more.** round → floor and round → ceil both survived a sweep whose pinned sizes were 22.2, 10.9 and 21.8 cells or pixels. Pin a value with a fraction below ½. When two quantities are rounded by separate expressions, such as a rectangle's width and height, pin one for each. The first fix put the 19.2 on the height, and the width mutant survived its retest.
- **A bilinear interpolation's neighbour cannot be tested at a cell centre**, where its weight is exactly 0. A test that compares the probe with its own recorded trace compares a function with itself. Read a linear field between cells instead: bilinear interpolation is exact there.
