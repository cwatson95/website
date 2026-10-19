## 2026-09-21 — magnet-and-compass: PhET's Bar Magnet screen as its own sim, on the family engine, in five views

Remake of PhET's Magnet and Compass 1.0.7
(`docs/phets/magnet-and-compass_en.html`; its single screen is PhET's Bar
Magnet screen from the shared FARADAYS_ELECTROMAGNETIC_LAB repo) as
`magnet-and-compass.html`. Built from the same engine as
`magnets-and-electromagnets.html` and `generator.html`: the shared parts, the
Python twin and the mutant list live in `build/magnets-and-electromagnets/`,
and `family.py` cuts this page from them. New code; no PhET code or assets.

The electromagnet is **stripped**, not hidden: the `#coil`, `#emag` and `#gen`
blocks are removed at build time and the build asserts that no symbol of them
(`coilField`, `loopB`, `I_MAX`, `drawBattery`, `projectPsi`, `fluxSeries`, …)
is left anywhere in the file. 2390 lines against the full sim's 2858.

### Added
- **the bar magnet** — PhET's screen, entire: drag and flip the magnet, set its
  strength (0–300 G, 75 % at start), the field as PhET's 40-mm needle grid with
  its 2(|B|/300 G)^(1/2.7) brightness rule, a compass that swings and settles,
  the field meter (B, Bx, By, θ; gauss or tesla, PhET's formats), see inside,
  the Earth. **field lines** — exact lines of B in the page, seeded at equal
  flux, and the magnet's bound surface current. **on the axis** — B and μ₀H in
  closed form against the point dipole, μ₀H drawn in three pieces so nothing
  joins its branches across a pole face. **the far field** — |B| on the axis
  and the bisector against the dipole on log axes, and the octupole approach.
  **the needle** — the compass as a damped rotor, its period against |B|.
- What is exact: as the family's — the uniformly magnetised cylinder's field in
  closed form (Derby & Olbert through Bulirsch's `cel`), exact field lines,
  numerically taken dipole limits, the octupole coefficient 2(b² − 3R²/4).
  What is modelled: the compass rotor, with PhET's constants converted from
  per-frame to per-second (κ = 6.25 /(G s²), γ = 2 /s, flip kick 0.75 rad/s at
  25 frames/s) — said on the page. The Earth adds no field, as in PhET.
- Verification: selfTest 775 assertions (the shared engine suites plus this
  page's model, panels and a 17-configuration × 5-size layout sweep); UI drive
  147; mutation sweep 67 of 67 caught (49 physics, 18 UI) — the family's list,
  filtered to the patterns that are actually in this page (26 dropped with the
  electromagnet, each named by `gen_mutants.py` rather than skipped in
  silence), plus four of its own; display-list audit 0 problems over 16
  captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **The page would not parse after the electromagnet was stripped**
  (`SyntaxError: Return statements are only valid inside functions`, line 499).
  Root cause: the `#coil` block that was meant to hold `projectPsi` alone ran
  from its comment to the next function definition, swallowing a nested
  `#endcoil` inside `psiMid`; the strip then cut at that inner marker and left
  the rest of `psiMid`'s body — including its `return` — outside any function.
  Fixed by ending the block at `projectPsi`'s own closing brace and marking its
  two call sites separately.
- **Four mutants survived this page's first sweep**, each a real finding:
  (i) the Newton projection onto Ψ was unreachable here (coil-only) yet still
  in the file — it is now inside `#emag`; (ii) nothing proved the frame loop
  drove the model rather than the tests — both UI drives now pump frames and
  watch the needle turn; (iii) nothing pinned that μ₀H is drawn in three
  pieces — asserted on the drawn strokes (no segment straddles a pole face);
  (iv) an equivalent slider mutant, replaced by a family-level one that bites.
- **My first version of (iii) was wrong in premise**: it asserted that the μ₀H
  curve is drawn only inside the magnet. Outside the magnet μ₀H = B and the
  page draws it deliberately. Replaced by the straddle test.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **Two dimmed boxes and a readout in gauss under the tesla chip** — both the
  ordinary kind of UI slip; the sweep found them through the "a dead control is
  dimmed" and "the unit chips reach the readout" mutants.

### Known-bad candidates
- **Trimming a family page is not finished until a mechanical check says so.**
  A stripped page that still names a stripped symbol is code the tests cannot
  reach; `family.py`'s `FEATURE_SYMBOLS` assertion is what catches it, and it
  has caught three separate leaks (an unmarked branch in `sourceField`, a REF
  key, and the axis view's coil branch).
- **Never assert a page's behaviour against a formula retyped in the test.**
  Two survivors here were tests that recomputed the constant they were
  checking; the fix is always a `REF` value or a drawn measurement.
- Branch-scoped group lookups: `groupU('tools')` matched the hidden screen's
  identically-named group in the full sim. A control lookup must prefer the
  visible group, or the test drives a control the user cannot see.
