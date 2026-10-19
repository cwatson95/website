## 2026-09-22 — fourier-making-waves: PhET's three screens, with every coefficient re-derived from the waveform it belongs to and the Gibbs constant measured

### Added

`docs/phets_revised/fourier-making-waves.html` — a remake of PhET Interactive
Simulations' **Fourier: Making Waves** (build 1.1.5), in six views. THE
HARMONICS is PhET's Discrete screen: eleven harmonics whose amplitudes you drag
on the canvas, drawn one per colour on the house NEON ramp, their sum below,
PhET's five presets (sinusoid, triangle, square, sawtooth, wave packet) plus
custom, sines or cosines, the domain switched between space, time and space &
time, the waveform the infinite series converges to, and PhET's
wavelength/period caliper. THE WAVE GAME is PhET's Wave Game screen: five
levels, a hidden waveform in magenta, the amplitudes to find, and PhET's own
rule that a guess counts only when every one of the eleven matches exactly.
THE WAVE PACKET is PhET's Wave Packet screen: a Gaussian in k with PhET's
centre, width and four component spacings, its components, its sum and its
envelope, with the 2σ_k and 2σ_x width markers. THE CONVERGENCE, THE SPECTRUM
and THE TRANSFORM PAIR are this file's own analysis views.

**What is exact.** Almost all of it; this sim is arithmetic, not a solver.

- **The preset coefficients are checked against the waveforms they belong to,
  not quoted.** `build/fourier-making-waves/derive.py` integrates `sgn(sin u)`,
  `(2/π)asin(sin u)` and `u/π` against `sin nu` and `cos nu` with
  `scipy.integrate.quad` broken at every corner, and the closed forms 4/(πn),
  8/(π²n²) and 2/(πn) come back to **2.2e-16**. The coefficients of the *wrong*
  parity come back zero to 2.5e-16, which is what says the sine forms are odd
  and the cosine forms even — and is why PhET refuses to build a sawtooth out
  of cosines.
- **PhET's wave-packet preset is a Gaussian, and its table has one typo.** That
  preset is 66 hard-coded numbers in PhET's build. derive.py fits σ from PhET's
  own numbers at every N and gets N/5 to 2e-5, and 65 of the 66 entries are
  `exp(-(n-c)²/2σ²)` with c = (N+1)/2, σ = N/5 to **4.9e-7**, PhET's own printed
  precision. The exception is N = 10, n = 2 and its mirror n = 9, where PhET
  reads 0.216255 and the Gaussian gives 0.216265 — a transposed digit. This
  file uses the closed form; selfTest pins both numbers so the difference
  cannot be lost.
- **Parseval both ways.** `⟨F²⟩ = ½ΣA_n²` is asserted against the trapezium
  rule on the square of the actual sum for every preset and eight random
  amplitude sets in both parities, worst residual **1e-13** — and the quadrature
  is *exact* rather than converged, which selfTest states by checking that 32
  and 4096 samples agree to 1e-14 while 16 (below 2N) do not. The complete
  series reproduce the exact mean squares 1, 1/3 and 1/3.
- **The Gibbs overshoot is the Wilbraham–Gibbs constant.** The peak of the
  M-odd-term square partial sum sits at u = π/2M exactly and equals
  `(2/π)Si(π) = 1.1789797444721672` in the limit, so the overshoot is
  **8.948987223608 %** of the jump. derive.py finds the peak by a dense scan
  plus Brent refinement and confirms the closed form to 1e-13 at M = 1, 2, 3, 6,
  12, 50, 400; the approach to the limit is O(1/M²) (measured ratio 4.0094
  between M = 6 and 12). The triangle, being continuous, never exceeds 1 — the
  falsifier for "series always overshoot" — and the sawtooth's jump is also 2,
  so it tends to the same fraction (0.08899 at 1000 terms).
- **The wave packet's transform pair is done, not approximated.** The Fourier
  transform of `A(k) = exp(-(k-k0)²/2σ_k²)/(σ_k√(2π))` is
  `exp(-σ_k²x²/2)cos(k0x)`, so σ_x σ_k = 1 **exactly** and the envelope is
  1/√e at x = σ_x, which is why the width markers sit at that height. Checked
  against quadrature over the whole line in Python (3.8e-16) and in JS (1e-12).
- **The discrete packet IS the continuous one, repeated.** By Poisson summation
  the two-sided sum over k_n = n k1 equals `Σ_m F(x − mλ1)`, λ1 = 2π/k1 —
  verified to 6.8e-16 in Python and 1e-12 in JS — and the truncated one-sided
  sum PhET draws is exactly periodic with period λ1 (residual 5.5e-15). What
  separates it from the continuous packet inside one period is only the
  Gaussian tail below k = 0 and above 24π, bounded by erfc at 6.3e-5 and
  measured at 5.3e-5. At PhET's own default (k1 = π, window ±2 m) the copies
  sit exactly at the window edges and stand at full height, which the readout
  reports as a separate number rather than hiding in the "error".
- **Analysis closes on synthesis.** Projecting a sum back onto sin nu and cos nu
  returns the amplitudes to 1e-15, by a radix-2 FFT written here, checked
  against a direct O(N²) DFT on an arbitrary (non-series) signal to 1e-12 and
  against `numpy.fft` in derive.py to 5e-16.

**What is modelled rather than exact.** The drawn curves are sampled at PhET's
own 1000 points; every number in the readout comes from a closed form, with two
stated exceptions (the measured peak of a partial sum and its position, found
on a refined grid, whose grid error selfTest bounds against the closed form).
The game's challenges are random, following PhET's generator exactly.

**What is not modelled.** Sound (PhET's Discrete screen can play the series);
PhET's per-screen zoom buttons and its equation-form dropdown; its keyboard-only
amplitude editing, info dialogs and PhET-iO instrumentation.

**Verification.** `selfTest` 6212 passed / 0 failed; UI drive 465 / 0; the
layout audit clean on 30 captured configurations at 1400×820 (and 6 at
860×560, where the panels run under the floating readout as the siblings
do); every view's PNG looked at; mutation sweep **95 / 95 caught, 0 survivors**
(85 physics, 10 UI; two survivors of the first full pass were fixed and
re-swept, see below).

### Fixed (during the build)

- **Two mutants survived the first full sweep, and both were missing
  assertions rather than bugs.** (1) `stepOnce(){ ST.t += 0.05 }` — PhET's
  step button — was exercised only by the UI drive, so the physics suite let
  0.05 become 0.1. `selfTest` now drives the clock directly: the step button's
  0.05 ms, the play rate of 1 ms of model time per second, a paused clock that
  does not move, and the fact that neither runs outside the space & time domain.
  (2) `setView` writes `className = 'active'` on the chosen tab, and nothing in
  the harness ever read the tab classes; the UI drive now asserts that exactly
  one tab is marked active after every switch. Both were re-swept and are
  caught.

- **The time domain drew a flat line in every view that used it.** *Symptom:*
  THE HARMONICS with "function of: time" showed three empty panels — the sum, the
  eleven harmonics and the caliper all at zero. `selfTest` (6188 assertions) and
  the layout audit were both green; the PNG was what showed it. *Root cause:*
  the phase is `phaseOf(domain, x, t)`, and the three curve builders passed the
  DRAWN abscissa as `x` for all three domains. In the time domain the abscissa
  *is* t, and `phaseOf('time', s, t)` ignores `s` entirely, so every sample got
  the same phase. Fixed by a separate `phaseAt(domain, s, t)` that routes the
  abscissa to the right argument, with every curve builder going through it and
  selfTest asserting, for each domain, that the drawn sum and its fundamental
  actually vary (range > 1.5 and > 2) and that the window holds a whole number
  of periods. The lesson is the general one: a model function with a correct
  signature can still be called with the arguments in the wrong roles, and only
  a test of the DRAWN curve sees it.
- **One amplitude array for the Discrete screens and the Wave Game wiped the
  preset at boot.** *Symptom:* the sim started with every amplitude zero instead
  of PhET's A₁ = 1; caught by the UI drive, not by selfTest. *Root cause:*
  `boot()` calls `applyPreset()` and then `GAME.reset()`, and the game's reset
  zeroed the same shared array. Fixed by two arrays, `AMPS` and `GUESS`, with
  `ampArray()` choosing by view — which is PhET's own arrangement (a
  fourierSeries per screen, and answerSeries/guessSeries in the game). selfTest
  now asserts both directions of the separation.
- **The convergence view's "terms kept M" meant two different things.** The
  slider keeps harmonics 1..M, but `squarePeakClosed(M)` is written in the count
  of ODD harmonics, so at M = 6 the view compared a three-odd-harmonic sum with
  a six-term closed form and was out by 0.6 %. Fixed with an explicit
  `oddCount(N) = ceil(N/2)`, shown in the readout, and the overshoot panel's
  x axis relabelled "odd harmonics kept".
- **A whole-half-period scan for the Gibbs peak lands on its MIRROR.** A square
  wave's partial sum is symmetric about u = π/2 (only odd harmonics survive
  u → π − u), so a scan of (0, π) finds the mirror of the first ear as often as
  the ear — same height, wrong position, and the readout then printed a peak
  position that disagreed with its own π/2M. Fixed with a per-waveform
  `peakWindow()` that looks next to the jump: (0, π/2) for a square, (π/2, π)
  for a sawtooth, the whole half period for a continuous waveform. selfTest
  asserts the symmetry AND that the wide scan still lands on the mirror, so the
  reason the window exists is itself a test.
- **The wave-packet components panel was an aliased hairball.** Across PhET's
  ±2 m window the highest component runs 48 cycles; drawn at 240 samples that is
  5 points per cycle, so the curves shown were not the components. The panel now
  draws over ±3σ_x with the sample count set from the phase excursion
  (16 points per cycle of k_max), prints the zoom factor, and the sum panel
  below carries a cyan bracket showing which slice it is.
- **Two panel-stack gaps were too small for the labels they had to clear.** A
  36 px gap put an upper panel's x tick labels (bottom + 5) under the next
  panel's title (top − 9), and 14 px of clearance above the caption put the
  bottom panel's axis label on the caption's first line. Both were found by
  selfTest's collision check across 26 configurations × 3 sizes; the gaps are
  now 46 px (50–62 where an axis label is involved) and 48 px above the caption,
  with the arithmetic written down beside them.
- **`logTicks` leaves a single label on an axis spanning under two decades.**
  The rms-error panel showed one "0.1". Added `logTicksFine`, which subdivides
  1-2-5 per decade below 2.2 decades, and `logLab`, which writes plain decimals
  because a superscript minus is not safe on the canvas.
- **A limit line drawn UNDER the curve converging onto it is invisible.** The
  Wilbraham–Gibbs line was drawn first and the green peak curve sat exactly on
  it. It is now drawn last, dashed, so both show.
- **The peak label ran under the floating readout for a sawtooth.** Its ear is
  at u = πN/(N+1), hard against the right edge of the panel; the label now goes
  on the side away from the edge.
- **The amplitude bars drew their harmonic numbers twice.** The x ticks are the
  harmonic numbers already, and a second row on the same baseline read as 11
  text collisions in the audit.

### Known-bad candidates

- **A model function with a correct signature can still be called with its
  arguments in the wrong roles, and no assertion on the function catches it.**
  `phaseOf(domain, x, t)` is right; passing the time axis's abscissa as `x` is
  wrong, and produced a flat line in three views while 6188 assertions stayed
  green. Assert something about the DRAWN curve — that it varies, that it is
  periodic over the window — not only about the function it came from.
- **Two screens sharing one state array is a reset bug waiting to happen.**
  PhET keeps a separate Fourier series per screen for a reason. Here one shared
  amplitude array meant the game's reset wiped the Discrete screen's preset at
  boot; the UI drive caught it only because it asserted PhET's start state
  explicitly.
- **A partial sum's symmetry can hand a peak-finder the wrong extremum.** Only
  odd harmonics survive u → π − u, so a square wave's Gibbs ear has an exact
  mirror at the same height. Search next to the jump, not over the half period,
  and assert the symmetry so the reason is testable.
- **Sampling a drawn curve coarser than its own structure is an alias, not a
  simplification.** 5 samples per cycle draws a curve that is not the one asked
  for. Set the sample count from the phase excursion, or narrow the window and
  print the zoom.
- **PhET's hard-coded tables can carry typos.** The wave-packet preset's N = 10,
  n = 2 entry is 1.0e-5 off the Gaussian every other entry follows. Pin both
  numbers rather than matching the table.
