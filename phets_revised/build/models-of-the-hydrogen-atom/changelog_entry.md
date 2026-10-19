## 2026-09-22 — models-of-the-hydrogen-atom: six historical atoms in one box, and the spectrum that decides between them

### Added

`docs/phets_revised/models-of-the-hydrogen-atom.html` — a remake of PhET
Interactive Simulations' *Models of the Hydrogen Atom* (build 1.0.9, CC-BY 4.0).
New code; no PhET code or assets. Both PhET screens, all six of its atomic
models, its Experiment-vs-Model switch, its white/monochromatic source, its
spectrometer, its electron-energy-level diagram, its three de Broglie
representations and its (n, l, m) quantum numbers, in six views: **the box**
(PhET's Spectra screen), **the levels** (its Energy Levels screen, drawn on
PhET's compressed ladder *and* on the true one side by side), **the standing
wave**, **the orbitals**, **the series** and **the rates**.

**What is exact** — everything about the atom itself, pinned in `selfTest` to
`build/models-of-the-hydrogen-atom/derive.py` (2196 assertions, 935 printed
reference lines):

- `E_n = −R_H hc/n²` and every transition wavelength from CODATA 2022
  (`scipy.constants`) with the electron–proton reduced mass; `r_n = n²a₀`;
  `v_n = αc/n`. The reduced mass is not decoration: it moves H-α by 0.36 nm,
  350 times the residual against NIST.
- The de Broglie closure `nλ_dB = 2πr_n` is an identity and holds to
  **5.178×10⁻¹²** here — which is exactly how consistent CODATA's separately
  rounded `a₀`, `α` and `m_e` are with each other (the same number as
  `a₀ − ℏ/(m_e αc)`), and is asserted as such rather than as "zero".
- The seam mismatch when ν wavelengths are wrapped round one turn has a closed
  form: matching both height and slope costs `√(sin²2πν + (1−cos2πν)²) =
  **2|sin πν|**`, zero only at the integers. Asserted against the two-term
  expression over 400 ν.
- The hydrogen wavefunctions are the analytic ones. The radial functions are
  built from exact polynomial coefficients and agree with the Laguerre
  recurrence to 1×10⁻¹⁴ and with `scipy.special.genlaguerre` to 4×10⁻¹⁷; the
  angular parts match `scipy.special.sph_harm_y`/`lpmv` to 2×10⁻¹⁶.
  Normalisation, ⟨r⟩, ⟨r²⟩, ⟨1/r⟩, the n−l−1 radial nodes and the l−|m| angular
  nodes are each asserted twice — once against the closed form and once against
  an independent Simpson quadrature.
- The drawn cloud is `∫|ψ|²dy`, the column density along the line of sight,
  pinned against `scipy.integrate.quad` to 1×10⁻¹⁴.
- The **Einstein A coefficients** come from the dipole radial integrals
  evaluated in closed form (both radial functions are a polynomial times
  `e^{−r/n}`, so the integrand is a polynomial times `e^{−sr}` and every term
  integrates exactly). They agree with scipy quad to 2×10⁻¹³:
  A(2p→1s) = 6.26832×10⁸ s⁻¹, τ(2p) = 1.5953 ns, τ(2s) = ∞.
- The stochastic parts run on a seeded mulberry32 whose stream is reproduced
  **bit for bit** in Python, and the cascade ensembles are asserted hop by hop
  against derive.py and against the distributions they are drawn from (|z| < 3).

**The finding worth recording:** PhET's transition-strength table
`[[12.53], [3.34, 0.87], [1.36, 0.24, 0.07], …]` — the weights its Schrödinger
atom picks a lower n with — has a first column that is **twice the Einstein A
coefficient for np → 1s in units of 10⁸ s⁻¹**, to between 0.05 % and 1.2 %
(12.5366, 3.3469, 1.3645, 0.6879, 0.3948). The other columns match no average
of the real rates and are PhET's own; both tables are drawn side by side in
*the rates* view and the difference is stated on the canvas.

**Measured data.** NIST, *Handbook of Basic Atomic Spectroscopic Data*, "Strong
Lines of Hydrogen (H I)" (`physics.nist.gov/PhysRefData/Handbook/Tables/
hydrogentable2.htm`, fetched 2026-09-21): all 8 vacuum rows and all 22 air rows,
used verbatim, with Edlén 1966 (*Metrologia* **2**, 71) for the vacuum→air
conversion. Every line is reproduced to better than 3×10⁻⁵, and the eight Lyman
lines miss by 1.10–1.33×10⁻⁵ — which is **α²/4 = 1.331×10⁻⁵**, the relativistic
shift of the 1s level. The residual is the physics the model does not contain,
measured, and it is drawn as such.

**What is PhET's model, not physics** (read out of the minified build and
labelled PhET's throughout): the 475-unit box, the 300 units/s photon, one
photon every 0.0792 s, the drawn orbit radii 15/44/81/124/174/233 (not n²), the
energy-diagram heights 0.025/0.6/0.73/0.81/0.86/0.9 (not 1 − 1/n²), the
`round(1240/(13.6(1/n₁²−1/n₂²)))` integer wavelengths, the 0.75 s and 1.0 s
waits, the flat 0.5 emission chance, the 150 nm plum-pudding line, the classical
spiral (220 units/s, ×1.008 a frame, dead in 0.659 s), the 0.4 white-light bias
toward the n = 1 lines, and the metastable (2,0,0) handler. PhET's probabilities
are per animation frame; this file fixes the frame at **1/60 s**, PhET's own
rate on a 60 Hz display, so a seeded run is reproducible — and says so.

`selfTest` 2196/0, UI drive 250/0; 125 mutants, 0 survivors after the fix
round; `tools/audit.py` clean at 1400x820, 820x520 and 560x380.

### Fixed (during the build)

- **`&ouml;` is not in `ENTS`, so `plain()` returned it unchanged and the canvas
  drew `Schr&ouml;dinger` verbatim.** Symptom: the model name in the box view
  came out as a literal entity in the display-list smoke test. Root cause: the
  shared entity table has no Latin-1 letters at all, and `plain()` passes an
  unknown named entity through unchanged by design. Fixed by writing the glyph
  (`Schrödinger`) in the model list and adding `&ouml;`, `&eacute;`, `&micro;`
  and `&thinsp;` to the table.
- **`h(tag, attrs, 'text')` makes a TEXT node, so an HTML entity in a control
  label is drawn literally.** Three buttons and one checkbox read
  `Lyman &alpha; 122`, `H&alpha; 656` and `the true n&sup2; radii` in the panel.
  Root cause: only the `html:` attribute decodes; a string child does not. Found
  because the UI drive could not find the buttons by their rendered label.
- **A node that lands exactly on a grid sample is lost by a strict
  sign-change test.** `R_20` vanishes at exactly r = 2 a₀, and 2 is a grid
  point, so `sign(prev)×sign(v) < 0` was false on both sides of it and the 2s
  orbital was drawn with zero radial nodes instead of one. The same shape had
  already bitten derive.py's angular-node counter, which missed every node at
  cos θ = 0 (P₁⁰ counted 0 nodes instead of 1) because the sample grid had an
  odd number of points. Both now track the last **non-zero** sign and treat an
  exact zero as a node in its own right; the angular scan samples at midpoints.
- **A fixed panel count in the column integral is 40× too coarse at n = 1.**
  `∫|ψ|²dy` varies on the scale of n a₀, so a panel count tuned at n = 6 left
  the 1s column 1×10⁻⁵ low. The step now follows n; `selfTest` asserts the
  accurate version against scipy quad **and** asserts the coarse one is still
  visibly wrong, so the fix cannot be quietly undone.
- **The caption's last line sat in the `#hint` corner.** `fitCaption` anchored
  the caption 12 px from the bottom, where the HTML `#hint` is drawn at
  `bottom:11px` — and the canvas capture cannot see the hint, so nothing
  reported it. Every view now reserves `HINT_H = 27` px and `selfTest` asserts
  the bottom-left 340×27 corner carries no canvas text, at five stage sizes.
- **A plot box with no room under it puts its own x-axis title on the
  caption.** The first narrow-stage layout clamped the lower panel's height with
  a `Math.max` floor, which pushed the axis labels past the frame. `stackFit()`
  now shrinks the upper panel until the lower one is guaranteed
  `AXIS_BOT = 38` px of clearance, and a stage narrower than 430 px of usable
  width stacks its panels instead of putting them side by side.
- **`legendAuto` places a legend OUTSIDE a panel it does not fit in.** On a
  110 px rates panel at 560×380 the legend was 110 px wide, no candidate corner
  was inside the frame, and it landed on the neighbouring axis's tick labels. A
  legend that does not fit is now not drawn.
- **`legendAuto` dodges curves, not labels** (already on the Known-bad list, hit
  again): the ⟨r⟩ label and the branching bars' value labels landed on legends.
  The ⟨r⟩ value moved into the legend itself; the bar labels now dodge
  `LEGEND_RECTS` and sit inside the bar when it reaches the frame.
- **A rotated axis title runs DOWN the screen.** The 150 px-long
  `(model − NIST)/NIST, ×10⁻⁵` on a 46 px-tall panel stuck out 50 px past the
  frame and onto the caption. It shortens to `×10⁻⁵` below 120 px of panel.
- **Tick labels crowd on a short axis, and a decade label crowds on a narrow
  one.** Five y ticks need 60 px of frame (`nyFor()`); the series view's decade
  labels are now thinned by measured width, which is what `5.0 µm` and `7.0 µm`
  needed at 820 px.
- A general fix for the above class: every label this file draws registers its
  rectangle, and `labelIfClear()` refuses to draw one that would land on an
  existing rectangle. Mandatory text (panel titles, axis titles, the caption,
  the wavelength marker) goes down first; optional text dodges it or is dropped.
  The true energy ladder really does crowd n = 4, 5 and 6 into the top 3 % of
  the axis, so it now labels what fits and prints *"N levels too close to
  label"* — which is the point the view is making.

### Fixed (from the mutation sweep — 125 mutants, 23 survivors in the first pass)

Every survivor is listed with what closed it. Three shapes recur: a pin that
recomputed the constant it was pinning (so it moved *with* the mutant), a rule
written out more than once (so either copy's mutant was equivalent), and a
repaint asserted against a forced draw rather than through the frame loop.

1. **PhET white-light bias** (0.4 → 0.7) — nothing measured what the source
   fires. Now: 20 000 photons drawn off `firePhoton` and the fraction on an
   n = 1 line asserted at 0.4044 ± 0.04, with an explicit "and not 70 %".
2. **Legendre P_m^m sign** — **equivalent, and now stated as such.** The
   Condon–Shortley phase (−1)^m cancels in `|Y|²`, which is the only thing this
   file ever asks `legendreP` for. `selfTest` asserts the invariance
   deliberately (|Y_l^m|² = |Y_l^{−m}|² to 1e-15 at four (l, m)) so it is a
   property rather than a blind spot, and the mutant is out of the sweep.
3. **selection rule Δl** (`!== 1` → `> 1`) — unreachable through every caller,
   because `decayRate` and `rateNtoN` only ever offer l ± 1, and for s → s the
   `l_max = max(l_u, l_l)` factor is zero anyway. Now asserted directly at
   l ≥ 1: A(3p→2p) = A(4d→3d) = 0.
4. **weighted choice normalisation** (`acc += w/tot` → `acc += w`) — every
   distribution the sim passes already sums to 1, so the division cancelled in
   every call. Now tested with 3:1 weights (0.75 ± 0.02), plus the empty and
   all-zero cases.
5. **PhET lower-n floor** — two guards on one path (`Math.max(l, 1)` followed by
   `if(l === 0) lo = 2`), so either mutant was equivalent. Written as one
   decision, `const lo = (l === 0) ? 2 : l`, and both of its mutants are caught.
6. **PhET choose_m thirds** — `phetChooseL`/`phetChooseM` were declarative only;
   `setNLM` (the live atom) and `cascadeSchrodinger` (the ensemble) each
   reimplemented the rule. Three copies of one rule, so the declarative one's
   mutant was invisible. Both callers now **draw from the distribution**, so
   there is one statement of it; derive.py was changed in the same commit and
   the bit-for-bit cascade pins moved with it. That alone did *not* close it,
   and the reason is worth recording: **m is causally inert in PhET's model.**
   `phetLowerDist` reads only (n, l), `phetChooseL` does not read m, and
   `phetChooseM` can only return m, m+1 or m−1 — so |Δm| is never 2 and the
   (1,0,0) fallback is never reached through m either. Nothing about which n
   the atom lands on, or which wavelength comes out, depends on it. The
   distribution is now asserted directly (each of the three outcomes at 1/3
   over 60 000 draws), and the inertness asserted deliberately, so it is a
   stated property rather than the reason a mutant lived.
7. **PhET state validity** (`l <= n-1` → `l <= n`) — the boundary was never
   probed. Now: `validState(2,2,0)`, `validState(2,1,2)` and `validState(7,0,0)`
   are each asserted false.
8, 9, 18. **photon radius, electron radius, the quantum collision radius** — the
   absorb counts moved but every assertion on them was a bound, not a value.
   Now the collision geometry is asserted directly: a Bohr photon collides at
   19.9 units and not at 20.1 (15 + 5, PhET's), a de Broglie one at 22.9 and not
   23.1 (15 + 8), and on the far side of the ring, which a point electron would
   not.
10, 11. **the absorb wait, the emit wait** — `ATOM.absorbed > 3` survived both.
    Now: a photon arriving 0.70 s after the last transition is refused and one
    at 0.80 s is absorbed; and nothing is emitted before the state is 1 s old.
12. **the plum-pudding line** (150 → 160) — the pin read `PHET.puddingLam`, so
    it moved with the mutant. Pinned against the literal `'150'`.
13, 14, 15. **the classical collapse rate, spin-up and start radius** — all
    three pins recomputed themselves from `PHET.*`. Pinned against PhET's
    literals (150, 220, 5, 600, ×1.008) and against the measured collapse time
    (150−5)/220 = 0.6591 s, plus a linearity check on r(t) at two times.
16. **the emission direction below n = 5** (`n < 5` → `n < 4`) — the isotropy
    test was run at n = 3, which is below either threshold. Moved to n = 4, and
    paired with an n = 5 check that the direction is *not* isotropic.
17. **the tick length** (1/60 → 1/30) — nothing observable depended on it. Now:
    a 300-unit/s photon moves exactly 300 units in 60 ticks, and crosses the
    475-unit box in 95 of them.
19. **the metastable light mode** — the old pin read `ATOM.metaT`, which the
    mutant reset anyway by exciting the atom. Now: under a monochromatic lamp
    **no** `meta` photon is ever created and a 2s atom stays at n = 2.
20. **the pointer never marks the canvas dirty** — `pointermove` sets the flag
    itself, so a down–move–up sequence could not test the `pointerdown`
    handler. Firing the pointerdown alone did not close it either: the
    `pointerup` that tidied up afterwards calls `refresh()`, which draws
    unconditionally, and that draw landed in the same capture. The capture now
    happens **after the pointerdown and before any pointerup**, on a box view
    whose clock has been stopped and proved idle.
21. **a slider stops repainting** — `refresh()` draws unconditionally, so the
    immediate draw said nothing about the dirty flag. The assertion now takes a
    second capture **through the frame loop** and a third proving it goes quiet.
22. **l is no longer clamped to n − 1** — clamped in the slider handler *and* in
    `syncPanel`. One clamp now, in `syncPanel`, which runs after every change;
    the `m` clamp joins it and both mutants are caught.
23. **the seed slider does not restart the run** — masked by the lazy
    `atomKey` check inside `atomAdvance`, which resets on the next frame anyway.
    Now asserted **immediately**: `ATOM.t === 0` the moment the slider fires,
    before any frame is pumped.

### Fixed (from looking at the PNGs — the audit is blind to all of it)

Three capture sizes (1400x820, 820x520, 560x380), 46 pictures, `tools/audit.py`
clean on all three. Everything below was found by looking, not by the audit,
which inspects text only.

- **The proton was drawn 12.5 px across and swallowed its own n = 1 orbit**
  (14.7 px at the default fit), so the ground state was invisible and n = 2 was
  crowded. 7 view units now.
- **The classical spiral's trail was a path the electron never took.** It was
  reconstructed forwards from r = 150 using TODAY'S angular speed for the whole
  history, which draws an arc, not a spiral. The forward step is invertible
  (r += 220 dt, a += w dt, w /= 1.008); stepping it backwards gives the true
  path, and it now visibly tightens as it falls in.
- **The small Schrodinger cloud was drawn at a fixed screen size whatever n
  was**, so it contradicted the orbit ladder drawn behind it — the one thing
  that ladder says is that the atom grows with n. Scaled so that <r> lands on
  PhET's drawn radius for that n.
- **The de Broglie wave on the standing-wave view was invisible.** Its
  amplitude was 0.45 of the n = 1 radius, which on the true n<sup>2</sup> ladder
  is 6 px on a 55 px ring, times a sin(phase) that a still frame can catch near
  zero. It is now 0.24 of the ring being drawn, the panel is fitted to that
  ring rather than to n = 6 (the house rule: fit each axis to the structure it
  contains, and print what runs off), and the full-amplitude shape is drawn
  faintly behind the live wave so the nodes stay visible while it breathes. The
  brightness picture gained node ticks for the same reason.
- **A legend entry for something that was not drawn.** The lifetime panel's
  orange "no allowed drop" entry named the 2s state, whose marker was under the
  legend box — because `legendAuto` dodges POLY_SEGS (curves) and nothing else.
  It now also dodges the label registry, the 2s state is drawn on its own rule
  at the top of the axis with a mandatory note, and the bars of both bar charts
  are registered so the legends stop landing on them.
- **The ensemble panel's y axis ran 0 to 1 for bars of 0.2**, and its mean-hops
  note was behind the first bar. Auto-ranged; the note moved to the top.
- **A `Math.max` floor on the box's side does not make it fit.** At 560x380 the
  floor of 120 px pushed the light source onto the spectrometer's title — and
  the light source is a FILL, so neither the audit nor the inline sweep could
  see it. Below 105 px of room the spectrometer is now dropped and the box
  keeps the space, which the caption says.
- The caption promised "faint green rings" in configurations that do not draw
  them; the model's 55-character claim ran three times the width of a 130 px
  box; "1 levels too close to label"; the short fallback captions were in ASCII
  while the long ones used the glyphs.

### Known-bad candidates

- **An HTML entity in a string passed as a `h()` CHILD is drawn literally** —
  only the `html:` attribute decodes. Canvas has no entity parser and neither
  does a DOM text node, so `btn('H&alpha; 656')` puts seven characters in the
  button. Write the glyph, or use `html:`. (Found here on three buttons and one
  checkbox; the UI harness caught it only because its finders match on the
  rendered label.)
- **`plain()`'s table has no Latin-1 letters**, so `&ouml;`, `&eacute;` and
  `&micro;` reach the canvas unchanged. Extended here; check the table before
  writing a new glyph on a canvas.
- **A node that lands exactly on a sample is invisible to a strict sign-change
  test** — `sign(a)·sign(b) < 0` is false when either is zero, so the node is
  skipped *and* the sign tracker is poisoned. R₂₀ vanishes at exactly r = 2 a₀,
  and P_l^m at exactly cos θ = 0 for every odd l − |m|. Track the last
  **non-zero** sign, treat an exact zero as a node, and sample an even grid (or
  at midpoints) so the symmetric zero is never hit.
- **The HTML `#hint` sits under the last line of a bottom-anchored caption and
  the canvas capture cannot see it.** Reserve ~27 px and assert the bottom-left
  340×27 corner is clear of canvas text. (Already recorded from
  `wave-on-a-string`; hit again here, and again the audit was silent.)
- **A `Math.max` floor on a bottom panel's height does not make it fit — it
  pushes its axis labels off the frame.** When a stack cannot fit, shrink the
  panel *above* it (`stackFit`), or drop the lower panel; never clamp.
- **`legendAuto` will place a legend outside a panel too small to hold it.** Add
  the `bw > b.w − 16 || bh > b.h − 16` guard; a legend that does not fit is not
  drawn.
- **A rotated axis title's LENGTH runs down the screen**, so a long one on a
  short panel overruns the frame vertically. Shorten it below a height
  threshold.
- **A pin that reads the constant it is pinning moves with the mutant.** Six of
  the 23 survivors here were this: `rel(tDead, (PHET.classicalR0 −
  PHET.classicalRmin)/PHET.classicalDrdt, …)` cannot fail. Pin against a
  literal, or against a measurement the constant controls.
- **A rule written out three times has two invisible copies.** PhET's
  `choose_l`/`choose_m` lived as a declarative distribution and twice inline;
  mutating the declarative copy changed nothing the sim drew. One statement,
  every caller draws from it.
- **`pointermove` sets the dirty flag by itself, so a down–move–up sequence
  cannot test the `pointerdown` handler's flag.** Test a pointerdown-only action
  (here, a click that toggles the lamp) against a proven-idle loop.
- **A slider repaint asserted on the immediate draw tests `refresh()`, not the
  dirty flag** — `refresh()` draws unconditionally. Take the second capture
  through the frame loop.
- **A lazy "has the key changed?" reset masks the explicit one.** Changing the
  seed restarts the atom twice over — once in the slider callback and once in
  `atomAdvance` — so the callback's mutant survived. Assert the immediate
  behaviour (state reset *before* any frame is pumped), not the eventual one.
- **A `pointerup` handler that calls `refresh()` masks the `pointerdown`
  handler's dirty flag** — `refresh()` draws unconditionally, so the draw it
  forces lands in the same capture. Capture between the down and the up.
- **`legendAuto` dodges curves only, and a scatter or a bar chart is not a
  curve.** Register a short segment per point and per bar edge in POLY_SEGS
  before placing the legend — and teach legendAuto to dodge the label registry
  as well, or it will sit on the very marker its own entry is naming.
- **A quantity that cannot change any observable is not testable through them.**
  PhET's magnetic quantum number m is drawn and printed but changes nothing
  about which level the atom lands on or which photon comes out, so its
  distribution has to be asserted directly. Assert the inertness too, so it is
  a stated property rather than a silent excuse for a survivor.
- **The audit's half-pixel overlap rule is the real one.** An inline sweep run
  at 3 px passed pictures the audit then failed; the two now use the same 0.5 px
  threshold, and so does the label registry that decides which labels to drop.
