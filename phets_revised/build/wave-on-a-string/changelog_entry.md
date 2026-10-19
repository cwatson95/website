## 2026-09-18 — wave-on-a-string: PhET's bead lattice exactly, with d'Alembert's images, the resonances, and a dispersion relation that is a straight line
### Added
- `wave-on-a-string.html` (162 KB), a remake of PhET's Wave on a String 1.2.4 in five views:
  *the string*, *the space-time*, *the reflections*, *the standing waves*, *the dispersion*.
  Credit line in the header and on the page; site nav absolute; no network.
- *The string* is PhET's one screen, with every control its inventory lists:
  - the wrench (manual; dragged on the canvas or with ↑↓, stopping at ±1.3 cm, and pressing
    play as PhET's does);
  - the oscillator, drawn as a scotch yoke whose pin sits exactly at A sin 2πft;
  - the pulse generator (click it, press p, or use the button);
  - fixed end, loose end (a ring on a pole) and no end (a window);
  - amplitude, frequency, pulse width, damping and tension;
  - rulers (10 cm and 5 cm, mm ticks), the stopwatch and the reference line, all draggable;
  - normal and slow motion (×0.25), play/pause, step, restart string and reset all.
  The drawing is at true aspect, with every tenth bead marked.
- **The model is PhET's**, read out of the build (and matching its `doc/model.md`):
  - 61 beads 0.125 cm apart;
  - the leapfrog `(1+β)yᵢⁿ⁺¹ = (β−1)yᵢⁿ⁻¹ + 2(1−α²)yᵢⁿ + α²(yᵢ₊₁ⁿ + yᵢ₋₁ⁿ)` at a Courant
    number held at exactly 1, so the tension sets the clock (Δt = Δx/v) and never the stencil;
  - β = 0.1 × damping per step;
  - the end rules y₆₀ = 0, y₆₀ = y₅₉ and y₆₀ⁿ⁺¹ = y₅₉ⁿ, including PhET's re-assertion of
    the end on the current level before each update.
- *The space-time* records the last 240 levels of that string (two round trips) as a green/cyan
  picture in x and t, with the characteristics x ± vt drawn over it: d'Alembert's two sliding
  shapes as stripes, inverted in colour on their way back from the clamp.
- *The reflections* feeds one pulse into all three ends at once, undamped and in whole steps.
  The image construction (the incident pulse running on into a shaded mirror world, its image
  running out, their sum as an orange halo round the lattice) shows why the clamp inverts, why
  the ring does not, and why the loose end's mirror sits at bead 59½.
- *The standing waves* sweeps PhET's 0–3 Hz with the exact steady response of the damped lattice,
  the largest |Y| on the string over A, against the undamped curve that diverges at every fₙ.
  Drag the panel to set f. Below it, the lattice is driven from rest and grows into the exact
  envelope, with nodes marked and the transient printed.
- *The dispersion* sets the lattice's ω(k) at a chosen Courant number α beside the continuum
  (ω = vk) and a real bead chain (ω = (2v/Δx) sin(kΔx/2)). It adds phase and group speeds, and one
  pulse after 5.4 cm on each. PhET's α = 1 is exactly ω = vk: its beads carry a continuous string
  and never disperse. α → 0 is the chain.
- **Exact:**
  - at α = 1 and no damping the lattice is d'Alembert's image series sampled at the beads (below
    1e-13 for all three ends, at two parameter sets, one incommensurate);
  - a damped mode keeps √((1−β)/(1+β)) = e^(−atanh β) per step;
  - the dispersion roots against `numpy.roots` and lattice runs, and v_g against a numerical
    derivative;
  - the driven steady state three ways: closed form, a complex tridiagonal solve and brute-force
    runs of thousands of steps, all agreeing to within 3e-11;
  - the resonances nv/2L and (2n−1)v/4L′ (L′ = 7.4375 cm);
  - the peak height 1/(Nβ) as β → 0 (166.67 A at β = 1e-4);
  - the no-end leak |r| = |zλ−1|/|λ(λ−z)| (5.4 % at the defaults);
  - the chain limit, O(α²) (error ratio 100.01).

  Every reference value comes from `build/wave-on-a-string/derive.py` → `refvals.txt`, read in
  full.
- **Verification:**
  - selfTest: 1075 passed, 0 failed under osascript (1.8 s). It includes a layout sweep of
    29 configurations × 4 canvas sizes.
  - UI drive: 199 passed, 0 failed. Every drag (wrench, both rulers, reference line,
    stopwatch, the response panel) is tested through the frame loop from a proven-idle baseline,
    and every reset against a sentinel.
  - Mutation sweep: 66 caught of 66 (55 physics, 11 UI), none survived or skipped. It ran on a
    copy in `build/wave-on-a-string/_out/`.
  - Audit: 0 layout problems at 1400×820 and at 820×520. The narrow size shows only the usual
    under-readout advisory.
  - Every captured view (21 + 5 narrow) was looked at.
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - Tension: PhET's relative slider (0.2–0.8) maps √T affinely onto 10–50 steps a second, 5:1 in
    speed over 4:1 in tension. The remake keeps PhET's 1.25–6.25 cm/s and makes it the law
    v ∝ √T, so its slider runs 0.032–0.8.
  - The driver is evaluated at each lattice time, where PhET uses a 0.02-s tick.
  - The standing-wave and reflection views run their own lattices.
  - Tools are dragged with the mouse only (PhET also drags them by keyboard). The stopwatch's
    buttons are in the panel.
  - No sounds and no a11y descriptions.
### Fixed (during the build)
- **The live clock fell a step behind.** One second of 1/60-s frames gave 49 lattice steps, not
  50. `while(acc >= Δt)` met an `acc` of 0.019999… after the frame sums rounded. The loop now
  carries a relative guard (`STEP_TOL`), and the 50-step second is asserted.
- **The readout read the global state, not its model.** A no-end model rendered after the state
  moved on printed the fixed-end rows. `buildModel()` now snapshots the state, and the readout
  and tag read `M.st`.
- **The dispersion view's "exact" pulse comparison was off by 0.40 cm at α = 1.** That was the
  damping, not dispersion: the long lattice ran with the global β. The pulses now run undamped,
  so only the dispersion changes their shape.
- **The exact solution was invisible wherever it was right.** The d'Alembert sum, the continuum
  line and the exact pulse lay exactly under the green lattice, so "they agree" read as "the
  reference is missing". The sum is now an opaque orange halo under the lattice, and the
  continuum and the exact pulse are dashed on top.
- **Two layout problems in the string view:**
  - the vertical ruler's default position covered the oscillator disc, so the world's left
    margin was widened to hold it;
  - the 10-cm ruler's labels ran off an 820-px canvas, and the reference-line label met the
    stopwatch at 560 px. Off-canvas labels are skipped, and the stopwatch box is registered
    before any label is placed.
- **The space-time stripes barely tilted.** With 360 rows they sat at about 5°. The tilt is fixed
  by rows per transit, not by the tension, so the record now keeps 240 rows (about 7°). It also
  says so when it is empty rather than printing "the last 0 steps".
- **The open end's flat response lay on the panel's bottom frame,** because the log axis started
  at exactly 1. The axis now starts at 0.5, and the panel says there are no resonances.
- **The narrow dispersion caption described a speeds panel the narrow layout does not draw.** The
  narrow layout now has its own caption.
- **Seven tests could not fail where they needed to, all found by the mutation sweep or by
  checking each mutant against the suite before the sweep:**
  - the interpolation probe sat at a bead the wave front had not reached (both levels were 0);
  - the node test sat at the third harmonic, where bead 19 is at 15.6 %, just over the 15 %
    threshold. The first and second harmonics now separate the mutant;
  - the end rule's pre-update acts only on the step after a switch. `derive.py` now runs a
    mid-run fixed-to-loose switch: y₅₉ = −1.14 with the pre-update, −1.26 without;
  - `csqrt`'s branch sign was invisible through the |λ| > 1 inversion. Its own contract is now
    pinned;
  - the pulse start was only ever tested at a whole step;
  - the dispersion view's β → αβ scaling and its α ≠ 1 oscillator k were unpinned;
  - a tautological `…||true` UI assertion.
- **Three prose claims were tighter than measured.** "1e-11" is 3e-11 measured; "1e-14" is
  1.07e-14; "within 0.3 %" for the α = 0.05 chain is α²/6 = 0.04 %, now asserted.
- **A global `axesR → axesT` rename rewrote the call inside `axesT` itself** (unbounded
  recursion). It was caught before the first run.
### Known-bad candidates
- **The house `#hint` sits on the last line of every bottom-anchored canvas caption.**
  `#hint{bottom:11px}` and `capFit`'s `capY = H − 12 − 14·lines` put the two in the same pixels
  at the stage's bottom-left. This holds in buoyancy, lagrange_points, brachistochrone and every
  sim built from the same scaffold. The display-list capture cannot see it, because the hint is
  HTML. This file reserves 18 px (`HINT_H`) and asserts that no canvas text enters the hint's
  corner: 116 checks fail with `HINT_H = 0`.
- **PhET's lattice is not a bead chain, and it must not be "corrected" into one.** At Courant
  number 1 the leapfrog's time error cancels the beads' space error, so ω = vk at every k up to
  the zone edge. A real chain of the same beads is dispersive: a 0.75-cm triangle on it is 0.05 cm
  out of shape after 5.6 cm, with ripples trailing behind.
- **PhET's loose end reflects about bead 59½, not bead 60.** y₆₀ = y₅₉ is a first-order free end.
  The loose resonances are (2n−1)v/4L′ with L′ = 7.4375 cm, and an image construction mirrored
  at 7.5 cm is wrong by 0.06 cm at the default pulse.
- **PhET's tension slider is not v ∝ √T:** its 0.2–0.8 maps affinely in √T onto 10–50 steps/s.
- **PhET's damping is per lattice step.** So its rate per second scales with v (b = 2βv/Δx),
  while the decay per bead travelled, e^(−atanh β), does not. The damped lattice is a
  telegrapher: it is overdamped where sin kΔx < β, and its "no end" leaks |r| ≈ β/(2 sin ωΔt),
  5.4 % at PhET's defaults. That is PhET's own "greatly reduces but does not perfectly
  eliminate".
- **`while(acc >= dt)` in a frame clock loses a step to rounding.** Guard it with a relative
  tolerance.
- **An exact reference drawn under the curve it matches disappears.** Draw it as a halo underneath
  or dashed on top.
