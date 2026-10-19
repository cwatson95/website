# The wave-interference engine: `p2_engine.js`

The 2-D lattice wave engine behind the first three views of `wave-interference.html`: PhET's
lattice, its sources, a screen, probes, and the calibration to physical units. **No DOM.**
It needs only `clamp`, `PI` and `TAU` from `p1_utils.js` (the house utilities). Copy the file
verbatim into a new build; if you change it, re-run `derive.py` (its numpy twin repeats every
operation below in the same order) and the selfTest sections A–E.

## What it computes

The scalar wave equation u_tt = c² ∇²u, as PhET's 5-point leapfrog at Courant number C = cΔt/Δx = ½:

    u^{n+1} = 2u^n − u^{n−1} + C² (u_E + u_W + u_N + u_S − 4u^n)

The lattice is PhET's: 151 × 151 cells, with a 20-cell pad on every side, so 111 × 111 are
visible. The outer ring is Mur's absorbing boundary: second order on the edges, first order at
the corners. Its exact plane-wave reflection is ≤ 3 % up to 45° and 11 % at 60°
(`murReflection`).

Dispersion (exact for this scheme):

    sin²(Ω/2) = C² [sin²(kx/2) + sin²(ky/2)]      Ω rad/step, k rad/cell

The physical time per step is **solved from it at every frequency**, so a wave along a lattice
axis has exactly the wavelength v/f and the period 1/f. PhET instead fixes one step per medium,
which makes its wavelengths 0.7 %–3.2 % short. Along the diagonal the wavelength runs up to
1.2 % long at 8.4 cells per wavelength.

## Constants

| name | value | meaning |
|---|---|---|
| `LAT.N`, `LAT.PAD`, `LAT.VIS` | 151, 20, 111 | lattice, pad, visible cells (PhET's) |
| `LAT.C`, `LAT.C2` | 0.5, 0.25 | Courant number (PhET's WAVE_SPEED) |
| `LAT.SRC_I`, `LAT.MID` | 25, 75 | source column, middle row on the 151 lattice |
| `LAT.AMP_CAL` | 1.2 | source cell = 1.2 × amplitude (PhET's) |
| `LAT.PLANE_MAG` | 0.21 | plane wave = 0.21 × amplitude (PhET's) |
| `LAT.EVENT_RATE` | 20·111/61 ≈ 36.39 | lattice steps per wall second at normal speed (PhET's) |
| `LAT.VISIT` | 1e-3 | a cell counts as visited once \|u\| exceeds this (PhET's light mask) |
| `MUR1, MUR2A, MUR2B` | −1/3, 4/3, 1/12 | Mur coefficients at C = ½ |
| `SCENES.water/sound/light` | see file | PhET's media: `W` visible width, `unit`, `tunit`, `v`, `fmin`, `fmax`, `scaleLen`, slit/source ranges and defaults, `phetTimeScale`, `what`, `fUnit`, `fMul` |
| `SCREEN_HIST` | 180 | the screen's ring buffer, in steps |

Units, in PhET's style:
- water: cm and s, v = 1.65 cm/s, 0.25–1 Hz;
- sound: cm and ms, v = 34.3 cm/ms, 0.22–0.44 per ms;
- light: nm and fs, v = 299.792458 nm/fs, c/780–c/380 per fs.

Frequencies are in the scene's per-time unit. `fMul` converts to the display unit (Hz, THz).

## The lattice

    const L = makeLattice(nx, ny, pad)   // Float64Array u (current), up (previous), un (scratch); Uint8Array vis
    latStep(L)                           // one step: interior, then edges (Mur 2nd order), then corners; rotates u/up/un
    latClear(L)
    latIndex(L, i, j)                    // = j*nx + i  (row-major; i = column = x, j = row = y, y DOWN)

After `latStep`, `L.u` is the new level and `L.up` the one before. A hard source is written
into `L.u` after the step.

## Dispersion helpers

    latOmega(kx, ky)          // Ω for a wavevector (rad/cell)
    latK(Om, th)              // the wavenumber along direction th carrying Ω (bisection; NaN if none)
    latPhaseSpeed(k, th)      // cells per step (continuum: C)
    latGroupSpeed(k, th)      // |∇_k Ω|, cells per step; NOT parallel to k off the axes and diagonals
    murReflection(kx, ky, 1|2)  // exact |R| off the Mur edge, from the plane-wave ansatz

## Media and calibration

    sceneF0(S)            // PhET's default frequency, mid-range
    sceneDx(S)            // W/111
    waveLen(S, f)         // v/f
    cellsPerWave(S, f)    // v/(f dx)
    omegaStep(Nl)         // Ω = 2 asin(C sin(π/Nl)), radians per step for Nl cells per wavelength
    stepDt(S, f)          // Ω/(2πf): physical time per step (s, ms or fs)
    phetLambda(S, f)      // what PhET's fixed step makes of f (for comparison only)

## Runs (a lattice plus what drives and measures it)

    const R = makeRun(sceneId, mode, nSrc, n)   // mode 'point' (nSrc 1 or 2) or 'plane'; n = lattice size (151)
    runStep(R)                                   // one step, the order below
    runSetScene(R, id)       // new medium: default f, separations, slit sizes; clears; restarts R.t, R.n and the stopwatch
    runSetFrequency(R, f)    // keeps the phase continuous; clears only for light or plane waves (PhET)
    runClear(R)              // empties the lattice, the screen history and the probe trace; phase to 0
    runClearRight(R, col)    // PhET's clearRight: wipes columns ≥ col (the barrier moved), keeps the plane wave
    runSetSource(R, s, on)   // switching on restarts the phase only if no other source runs (sources stay in phase)
    firePulse(R)             // one period of the drive, then the source lets go (only when !R.cont)

The fields of `R` you set: `A` (amplitude 0–10), `cont` (continuous if true, else pulse), `src[0..1]`,
`sep` (source separation, scene units), `plane.{on, barrier:'none'|'one'|'two', bcol, slitW, slitD}`,
`watch.on`, and `probes`, an array of model [x, y] points (set it to record `trace`).

The fields you read: `f`, `Nl`, `Om`, `dt`, `phi`, `t` (physical time), `n` (steps), `pulse.on`,
`watch.t`, `trace` ([t, v1, v2…] per step, at most 900) and `screen`.

**`runStep` order:**
1. `latStep`;
2. `phi += Om`;
3. the sources;
4. `t += dt` and `n++`;
5. the stopwatch;
6. the screen column;
7. the probes.

The sources in step 3 depend on the mode:
- **point:** each source cell is set to `A·1.2·sin(phi)`.
- **pulse:** its own phase runs from 0 to 2π, then the source lets go.
- **plane:** every column from the pad to `iR` is set, in both `u` and `up`, to
  `0.21·A·sin(Ω m − k x)` behind the front, which moves at the phase speed. `x` is cells from
  the pad and `m` is steps since switch-on. `iR` is the barrier column, or `nx − pad` with no
  barrier. The barrier column is zero where `slitOpen` is false.

This plane wave is an **exact** lattice solution (5e-15 over 20 steps).

Geometry helpers:
- `srcCol(L)` gives the source column: pad + 5, which is 25.
- `runSourceRows(R)` gives the source rows, MID ± round(sep/2dx).
- `slitOpen(R, j)` tests whether a cell centre lies inside a slit.
- `slitCells(R)` gives the geometry the lattice really has (`a`, `d` in cells).
- `cellOfX(R, x)` / `xOfCell(R, i)` convert between model units and cells. Cell centres are at
  (i − pad + ½)·dx, and the model spans 0..W over the visible cells.
- `probeValue(R, x, y)` is a bilinear read of `u`.

Screen:
- `screenIntensity(R)` is the mean of u² over the last `screenWindow(R)` steps, on column
  nx − pad − 1. It has `rows` = 111 entries.
- The window is the whole number of periods nearest 90 steps (PhET's 90), so it carries no phase
  ripple.

## Pinned

`derive.py` (read `refvals.txt` in full):
- the numpy twin agrees with this file to 1e-11 on five scenarios, 150–400 steps (tank,
  two sources, two slits, pulse, one slit);
- the calibration of all three media;
- the dispersion relation, `latK` (brentq), phase and group speeds;
- Mur's |R| (the ansatz, checked against a packet simulation to 2 %).

Findings to keep in mind:
- At steady state the lattice's screen follows the 2-D Rayleigh–Sommerfeld sum to 6 % (3 % rms),
  and its nodal lines sit 0.85 cells outside the continuum hyperbolae, 1.4 at worst. Both come
  from the lattice's anisotropy.
- The display pieces (colour scale `U_FULL = 2.14`, PhET's MAX_AMPLITUDE_TO_PLOT_ON_RIGHT, and
  `drawField`, `drawSide`, `parcelPositions`, `drawScreenStrip`, `drawIntensity`,
  `drawCentreGraph`, `drawMeter`, `latGeo`) live in `p3_state.js` / `p4_views.js`. So does the
  clock (`clockFrame`: a fixed 1/60 s per frame, `EVENT_RATE` steps per second, half on slow).
  They are reusable but not part of the engine.

## For waves-intro

PhET's Waves Intro is the Waves screen split into Water, Sound and Light. That is one
`makeRun(scene, 'point', 1)` per view, with the ripple-tank drawing from `p4_views.js`.

Drop the two-source, plane-wave and screen-theory branches from the views if they are unused.
Keep this file whole: the twin pins cover all of it.
