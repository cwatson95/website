## 2026-09-21 — quantum-measurement: coins, photons, spins and the Bloch sphere on one bit-exact engine, the Born rule both ways, and the binomial
### Added
- `quantum-measurement.html` (254 KB), a remake of PhET's Quantum Measurement 1.0.5 in six views:
  *the coins*, *the photons*, *the spins*, *the Bloch sphere*, *the Born rule*, *the binomial*. Credit line in the
  header and on the page; site nav absolute; no network. Its engine is shared with `quantum-coin-toss.html`
  (`build/quantum-coin-toss/assemble.py` reads `p2_engine.js`, `p4_coins.js`, `p5_binom.js` and the test library
  from `build/quantum-measurement/`), so the two files cannot drift.
- **PhET's four screens, with PhET's values read from the build** (every one marked "PhET's value" in the code):
  - *The coins*: a classical coin and a quantum "coin" in separate scenes. Prepare heads or tails, or up, down or a
    superposition, with the bias in steps of 0.05, then send the coin to be measured. The classical coin flips
    (1 s), hides and reveals; the quantum coin is reprepared and observed. This works for one coin at a time or
    for 10, 100 or 10 000 identical coins, and PhET's "classical coins start hidden" preference is included. The
    seeded draw is PhET's rule, u < p for heads or up, one coin at a time. The set's counts are drawn against
    Np ± √(Np(1−p)), and the single coin's last 48 outcomes are shown with their running fraction.
  - *The photons*: PhET's bench at true aspect in its own model units. The laser sits at −0.15 and sends a
    0.04-wide beam at 0.3 units a second into the 0.07 splitter cube, whose diagonal is y = x. The mirror is
    x + y = 0.11, and the detector lines are y = 0.2 and −0.09.
    - Photons arrive one at a time (click the laser) or as a beam of up to 200 a second.
    - Presets are V, H, 45° and unpolarized, plus a custom angle (0–90° in 5° steps) that can be dragged on
      the polarization dial.
    - Behaviour is classical (the path is chosen at the splitter) or quantum (the photon rides both paths
      until the detectors).
    - Counts are capped at 999; the rates use PhET's 1-s average in 0.5-s samples; slow motion is ×0.4 and
      the step is 2/60 s.
    - The display shows the average polarization (N_V − N_H)/N against −cos 2θ, and Malus's law with the
      measured fraction ±1σ.
  - *The spins*: PhET's six Stern–Gerlach experiments and its custom one. Single particles (click the source; a
    dial shows the spin at each stage) or a continuous beam (5 × amount per 60-Hz frame), with blockers on
    magnet 1's exits and each magnet's up percentage against its projection. In the custom experiment either
    magnet can be clicked to turn it, and the prepared spin can be dragged. A products-of-projections table
    sits beside it.
  - *The Bloch sphere*: prepare θ and φ in 15° steps or from six presets, and measure one atom or ten (PhET's
    3-2-3-2) along X, Y or Z.
    - Optionally a field along z turns the state during a 0–1 ns delay (default 0.75). The field is PhET's
      unit made real: an electron in B₀ = 35.68 mT turns once a nanosecond.
    - The state can be written in the Z, X or Y basis, with or without the global phase. Drag to orbit.
    - Beside PhET's screen, a fringe panel plots P(up) against the delay for this field, with the measured
      fraction at the current delay.
- **Two analysis views:**
  - *The Born rule* sets the spin's cos²(Θ/2) against the photon's cos²θ at 13 angles. Each point is 2000 seeded
    shots through the same measurement code the other views run, χ² 8.39 on 16. The view also shows the middle
    measurement (¼sin²α for spins, ¼sin²2α for photons) and a chain of N magnets passing [cos²(π/2N)]^N → 1 as
    1 − π²/4N.
  - *The binomial* repeats N-coin sets against the exact pmf (binned when N = 10 000). It also shows the spread
    of k/N against √(p(1−p)/N) on log–log axes, and one long run of 10 000 flips inside its ±2σ funnel.
- **Exact:**
  - the Born rule four ways (projector trace, (1 + r·n)/2, |⟨n|ψ⟩|², cos²(Θ/2));
  - the sequential Stern–Gerlach probabilities as products of projections, against 2×2 complex projectors in
    numpy for all seven experiments × four sources, plus a [z, x, z] layout PhET cannot build (it links its
    second-stage magnets), so the beam routing is pinned too;
  - Larmor precession as an exact rotation of the prepared vector, against scipy `expm` on the ket (vector, U
    and P(up) on three axes, three cases) and against a 4000-step RK4 integration of the Schrödinger equation.
    The sign is pinned: +X after 0.75 ns is −Y, so a y measurement is always down;
  - the ket ↔ Bloch vector ↔ angles round trip over 169 states, and every printed equation rebuilt into its ket;
  - ln n! (Stirling above 30) against math.lgamma to 2e-15, and the pmf against scipy to 1e-10.
- **Every random draw is one mulberry32 stream**, mirrored bit for bit in `derive.py`. Every seeded count in
  selfTest is an integer pinned exactly AND tested against its law with a tolerance from its own variance:
  - 4σ on counts;
  - 4σ/√M on sample means;
  - the fourth moment for the sample variance;
  - χ² below scipy's 99.9 % quantile;
  - 4/√(2(M−1)) on a measured spread.
- **Verification:**
  - selfTest 1775 checks, 0 failed under osascript;
  - UI drive 219 checks, 0 failed. Every canvas interaction goes through the frame loop from a proven-idle baseline: the coin
    clicks, the laser click, the dial drag, the source click, the magnet click, the spin-disc drag, the camera
    one axis at a time, and the Born cursor. Every reset is checked against a sentinel;
  - mutation sweep 79 of 79 caught (63 physics, 16 UI), no survivors, on a copy in `build/quantum-measurement/_out/`;
  - audit: 0 layout problems at 1400×820 (no advisories) and 820×520 (under-readout advisories only);
  - every captured view (26 + 6 narrow) was looked at;
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - PhET's custom spin state uses θ = π(1 − |α|²), so its own equation disagrees with its |α|² slider except at 0,
    ½ and 1 (0.854 at 0.75). Here θ = 2 arccos|α| and the slider IS P(↑z).
  - PhET's Y-basis equation prints 1.5π for +X, which rebuilds −X with PhET's own +Y. Here it prints 0.5π.
  - PhET turns its spheres a frame at a time and measures after the frame that reaches the delay, up to 1.5°
    late at 60 Hz and full field. Here the rotation lands exactly on the delay.
  - The beam starts at 60/s (PhET: 0), and an unpolarized beam shows its expectation value 0.
  - The two photon scenes share one set of controls, and the blocker is one setting (PhET keeps them per scene
    and per experiment).
  - There is no flying-coin animation, PhET's display toggles are always on, and its 10 000-coin easter egg is
    absent.
  - No sounds and no screen-reader descriptions.
### Fixed (during the build)
- **The Python twin disagreed with the engine on one seeded count** (the middle measurement's spins: 955 vs 951).
  Root cause: `derive.py` drew the complementary event (`u < ½(1 − cos α)`, a down) where the engine counts "not
  up" — the same probability, a different draw off the same stream. A bit-exact twin must mirror the EVENT, not an
  equivalent probability.
- **Panels were drawn under the caption and the HTML #hint at 560 × 380.** Root cause: the lower rows had floors on
  their heights, so they kept their size instead of vanishing when the space ran out. The floors are gone: a row
  that does not fit is not drawn, and selfTest asserts the hint band (18 px) is clear of canvas text.
- **Titles sat on their own frames, the Bloch titles collided with the axis labels, B collided with Z, the mirror
  label ran into the histogram's ticks, and corner ticks collided.** Root cause: labels were positioned from the
  box rather than measured against their neighbours. Titles moved above their boxes, the field label went left of
  its tip, the mirror label left of the ticks, and a tick at zero is written as a bare "0".
- **selfTest took 18.4 s under osascript.** Root cause: the test helper `fresh()` cleared the memo, so every
  binomial drawing in the layout sweep recomputed 2.5 M seeded draws. The memo keys carry all their inputs (the
  functions are pure), so it is never cleared; `binSpread` also caps a point at 1e6 draws. 5 s now.
- **Four test bugs that hid or faked a result**: an emission counter hooked onto an array `photonAdvance` replaces;
  a particle-rate expectation written per second for a 9-s run; a dial probe 3 px off the axis it meant to hit; and
  a classical-timing test that assumed every photon's splitter distance is 0.15 (it is 0.13–0.17 across the beam's
  width, so the test now reads the photon's own `d1`).
- **The UI drive passed 8 checks it should have failed.** Root cause: its button finder matched hidden buttons, so
  clicks on a panel group that was not shown "worked". It now walks the ancestors for `hidden`. Idle proofs were
  added before every interaction, and one pump was too short to reach the state it asserted.
- **The atoms chip reset the counts**, which PhET does not do: it reprepares without clearing the histogram.
- **Mutation survivors, each fixed rather than excused**: a Stirling series re-typed inside a test (now the
  engine's own `lnFactStirling`); the `quantumInit` threshold and the Stern–Gerlach beam routing (now pinned off
  PhET's domain); the collapse assertion, which only the parent sim's suite ran (moved into the shared
  `engineTests`); and "the precession does not repaint", which survived because the animation test compared a
  repaint against a possibly EMPTY second frame — `animatesU()` now drains the dirty repaint and requires two
  consecutive animation frames, both drawn and different.
- **`COINS.classical.p === 0.35` failed** after seven bias steps. Root cause: 7 × 0.05 = 0.35000000000000003.
  `snapBias` rounds to k/20 and selfTest pins the exact value.
- **The photon view printed a negative zero**: "(expected -0.000)" on the canvas and "−cos 2θ  -0.0000" in the
  readout at 45°. Root cause: ⟨P⟩ = −cos 2θ is −6.1e-17 in floating point and `toFixed` keeps the sign.
  `p1_utils.js` is a verbatim house extract, so the fix is `fmt0()` at the call sites; `layoutCheck` and both
  panel sweeps now reject any negative zero on the canvas or in the readout, equation bar and tag.
- **Value labels sat on the law's orange mark** ("28.1/s" on the 0.5 mark, "45%", "97.5/s", the coins' "46").
  Root cause: `barVal` placed the label 9 px above the BAR and knew nothing of the mark, so a bar stopping just
  short of its mark put the label on it. `barValY` now takes the mark's pixel y and picks the first place that
  clears it by 8 px (above the bar, above a higher mark, inside the bar's top, inside under the mark), checked
  over 6363 bar × mark pairs in three box heights; `layoutCheck` rejects any text crossing a short horizontal
  orange stroke, which is how the last three were found.
- **The empty-box note ("nothing yet") sat on a high mark** in the custom spin state. Root cause: it was pinned to
  the box top. `freeY` takes the top, then the middle, then the first line clearing every mark.
- **Legends named things that were not drawn.** The Malus legend listed "measured V fraction ± 1σ" in the beam and
  unpolarized views, where no point is drawn; the Bloch fringe legend listed the measured point before any
  observation with the field on, and never listed it with the field off although it draws one. Root cause: the
  legend was a constant while the drawing was conditional. Both are now built from what is drawn, and the beam's
  measured point (the rates' fraction, where the counts' σ does not apply) is drawn.
- **A legend vanished with no error** when the beam's entry grew longer. Root cause: the house `legendAuto` draws
  NO legend rather than a lying one when every candidate spot is crossed by a curve. The entry is short again, and
  selfTest wraps `legendAuto` during the layout sweep and fails if any legend is lost at 1100 px or wider — which
  immediately caught a second one, the Born view's middle-measurement legend at 1100 × 700: its y-axis ran to 0.3
  against curves peaking at 0.25, leaving a sixth of the box. The axis now runs to 0.4.
- **Captions named panels that were not drawn**: the Bloch caption's "the panel below draws it against the delay"
  at 820 × 520 and 700 × 450, and at 560 × 380 the coins' "Orange: Np ± √(Np(1−p))", the Born view's "the chain
  → 1" and the binomial's "one long run". Root cause: the caption is fixed text, but the panel it names survives
  only in the height the caption itself leaves. `layoutNamed()` lays out with the naming caption; if the panel
  does not fit it lays out again with the caption that does not name it and keeps the panel off.
- **The "after magnet 2" dial sat on the upper magnet's up beam** (28 px of overlap at 1400 × 820). Root cause: all
  three stage dials were placed at the same height, which is inside the second stage's beams. It now sits on the
  midline between the second magnets' inner beams with its label to the right; selfTest measures every dial
  against every beam band (7 experiments × 4 sizes, worst clearance 6.9 px).
- **The magnets' exit labels (↑z, +x) were covered by particles.** Root cause: they were drawn on the beams, and
  the particles are drawn over the beams. They now sit inside the magnet at its exit face, where the particles
  pass underneath.
- **Found by looking at the PNGs**: the coin strip ran under the floating readout; "10000" instead of "10 000";
  photon dots large enough to cover the detectors' letters; a full bar hid its own green-on-green count;
  particles covered the magnet labels; blocked beams were drawn past the blocker; "none yet" sat on the 0.5 marks;
  the equation rows lost their alignment; and the Bloch view's lower half was empty (it is now the fringe panel).
### Known-bad candidates
- **PhET's custom spin state θ = π(1 − |α|²)** disagrees with PhET's own printed equation except at 0, ½ and 1
  (0.854 against 0.750 at |α|² = 0.75), and **PhET's Y-basis phase** prints 1.5π for +X, which rebuilds −X. Do not
  copy either into a remake; both are pinned here as PhET's values with the correct ones beside them.
- A bit-exact twin that draws the complementary event is not bit-exact: mirror the event, not the probability.
- A button finder that ignores hidden ancestors turns "not shown" into "clicked".
- Floors on derived panel heights: a floor keeps a panel alive under the caption and the hint instead of dropping it.
- Clearing a pure memo inside a test helper (18 s of recomputation for nothing).
- "Compare two frames and assert they differ" passes when the second frame is empty: drain the dirty repaint and
  require two consecutive drawn frames.
- An engine contract that only one sim's suite exercises belongs in the shared `engineTests`, or the other sim's
  sweep finds it unprotected.
- k × 0.05 is not exact (7 × 0.05 = 0.35000000000000003): snap to k/20.
- `toFixed` keeps the sign of a negative zero, so an exact zero built from a cosine prints "-0.000".
- A value label placed above its bar alone lands on the law's mark whenever the bar stops just short of it.
- A legend written as a constant beside a conditional drawing, and `legendAuto`'s silent "no legend at all" when
  every spot is crossed — a longer entry can remove a legend with no error.
- A caption that names a panel the layout is allowed to skip.
- Labels and dials placed where the beams and particles are drawn (the particles are drawn last).
- One splitter cannot distinguish classical which-path from quantum collapse: with one photon at a time both give
  identical seeded counts, so the difference must be asserted on the timing, not on the counts.
