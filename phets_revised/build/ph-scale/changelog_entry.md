## 2026-09-21 — ph-scale: the beaker, the particles, the graph, and dilution done by mixing moles

### Added
- `docs/phets_revised/ph-scale.html` (171 KB), a clean-room remake of PhET's **pH Scale**
  1.7.6 (CC-BY 4.0; new code, no PhET code or assets). Six views: **the beaker** (PhET's
  Macro screen — twelve liquids, the dropper, the water faucet, the drain, and the pH
  meter whose probe you drag in and out), **the particles** and **the graph** (its Micro
  screen), **my solution** (its third screen), and two of this file's own: **dilution**
  and **the scale**.
- **Exact chemistry.** K<sub>w</sub> = 1.000e-14 at 25 °C (pK<sub>w</sub> = 14.000 — the
  conventional value, and the one PhET's hard-coded `14` encodes), so neutral is pH 7.000
  exactly. `[H3O+] = 10^-pH` and `[OH-] = Kw/[H3O+]`, both asserted against 50-digit
  `decimal` evaluation over the whole scale *including its ends*. `[OH-]` is written as a
  division on purpose: PhET's spelling `10^-(14-pH)` is out by up to 2.1e-15 because
  `pH - 14` is inexact in a double whenever pH < 7, while the division is out by 2.1e-16
  and keeps `[H3O+][OH-] = Kw` to a rounding. Molecule counts use the exact SI 2019
  N<sub>A</sub>; PhET's 6.023e23 is 1.43e-4 high and both are printed.
- **The dilution law, done properly — the point of the build.** What dilutes is not the pH
  and not either ion but the net strong acid
  `C = [H3O+] − [OH-] = −2√Kw·sinh(ln10(pH−7))`, a difference of *analytical*
  concentrations whose moles are conserved on mixing; water carries exactly none of it.
  So `C = (C1V1 + C2V2)/(V1+V2)`, then re-solve `[H3O+] − Kw/[H3O+] = C`, which is the
  water autoionisation PhET's rule leaves out. Implemented twice (the asinh closed form
  and the stable branch of the quadratic root) and asserted against a Decimal mole ledger
  plus a scipy `brentq` root of the charge balance. Two structural facts fall out and are
  pinned: diluting f-fold divides C by **exactly** f (0.0 relative error), and C is an
  **odd** function about pH 7 — so pH 2 and pH 12 are exactly as strong as each other and
  equal volumes of them are exactly neutral (the instinct that the acid wins is wrong).
- **PhET's own rule beside it, and the size of the gap.** A chip switches the model to
  PhET's `computePH` (mix the majority ion linearly, take a log, never re-solve). Over
  everything this beaker can reach — pH −1..15 × 0.015..1.2 L in 1.2 L — the two laws
  never differ by more than **0.0948 pH**, at pH 4.91 with 0.015 L in the beaker; at
  PhET's own liquids the worst is 0.0815 (chicken soup, 0.1 L in 1.2 L). Volume-averaging
  the pH, the mistake the view exists to rule out, is wrong by up to **4.42 pH**. The
  dilution view draws all three laws and the envelope of the exact-minus-PhET gap.
- **PhET's constants and rules, read from the minified original** and cited as PhET's: the
  twelve liquids' pH values and colours, the beaker's 1.2 L and 0.015 L minimum, the
  pH range −1..15 at two decimals, the dropper's 0.05 L/s and the faucets' 0.25 L/s, the
  0.5 L autofill at 0.45 L/s, water at 55 mol/L, the graph's 18 decades, the solute colour
  law (water → colour-stop over the first quarter, then → stock) and the particle rule
  (50 dots per 1e-7 mol/L inside pH 6–8, floor 5, the minority ramping to 3000 outside).
  At pH 13 the drawn ratio is 457:1 against a true 1e12:1, and the canvas prints both.
- **Measured pH ranges for four of the twelve**, quoted to their sources' own precision:
  blood 7.37–7.43 (Merck Manual Professional, "Acid-Base Regulation", J. L. Lewis III);
  orange juice 3.30–4.19, milk 6.40–6.80 and chicken broth 5.80 (FDA, "Approximate pH of
  Foods and Food Products"). **PhET's value lies inside every one of the four.** No range
  could be sourced for the other eight; they are drawn with no bar at all and the canvas
  says so rather than inventing one.
- Verification: `selfTest` **1957 passed, 0 failed**; UI drive **208 passed, 0 failed**;
  mutation sweep **90 caught, 0 survived**; display-list capture at 1400×820, 1100×700 and
  560×380 audited clean (0 layout problems) with every PNG looked at.

### Fixed (during the build)
- **The naive `[H3O+] − [OH-]` and the textbook quadratic root both lose their digits
  inside PhET's own range, and derive.py asserts that they still do.** The difference
  cancels near neutral (1.9e-11 relative at pH 6.999999, 1.7e-13 at 6.9999) and the
  textbook root `(C+√(C²+4Kw))/2` cancels for *every base*: 3.6e-5 at pH 13, 8.0e-4 at
  pH 14, **11 % at pH 15**. Root cause: both are differences of nearly equal quantities.
  The sinh and the rationalised branch `2Kw/(√(C²+4Kw)−C)` are exact, and the twin asserts
  the naive forms are *still* that bad so the branches cannot be quietly deleted.
- **Two of my own assumptions were wrong and the twin caught them.** (i) "Equal volumes of
  pH 2 and pH 12 come out acidic" — false: C is odd about 7, so they neutralise exactly.
  (ii) "PhET's N_A is 1.3e-4 high" — it is 1.43e-4. Both were written as checks, failed,
  and were corrected rather than loosened.
- **A pH round trip costs eight digits at high dilution, so the model keeps volumes.** A
  double holds `7 − ε` to an absolute 8.9e-16, so ε itself keeps only what is left:
  recovering C from a stored pH after a millionfold dilution is out by 4.0e-9 against
  2.2e-12 at a thousandfold. `beakerIons()` therefore builds *both* ion concentrations
  from C and never from the printed pH — pinned bit for bit at all 4104 reachable states.
- **The pH strip was never drawn at any stage size.** Symptom: the acidic/neutral/basic
  scale was simply absent from the beaker view. Root cause: it was sized from the height
  *left over* after the beaker, and there never was any; the guard `sy > bk.y1+10` was
  false at every size. The strip is now part of the layout, reserved before the beaker is
  sized.
- **The pH meter sat on top of the glass at 560×380.** Root cause: the meter was placed at
  `right − 140` while the beaker had already been sized from the whole span. Its width now
  comes out of the span *before* the beaker is sized.
- **The beaker was 600 × 420 and read as a tank.** Root cause: it filled whatever box was
  left instead of keeping PhET's 450 × 300 aspect. Same fault in `my solution`, where the
  beaker came out taller than it was wide and the strip above it was asked for at a y
  above the stage top.
- **The water pipe did not reach the spout it feeds** — drawn from the beaker's right wall
  outwards, it was a floating bar with nothing under it.
- **The particle view printed `drawn 0.00 : 1` for every base.** Root cause: both ratios
  were written hydronium-per-hydroxide. They are now majority-per-minority, with the names
  printed, which is also the number derive.py pins (457.20 : 1 at pH 13).
- **The "dots are capped" note was drawn in the liquid's dark ink above the liquid**, where
  the background is the page: invisible. Also, the dots were scattered across the volume
  label at the foot of the glass, which is drawn before them.
- **The difference panel was flat at zero at the default state.** Root cause: it plotted
  the gap at the beaker's *current* dilution, which is 1.0× when nothing has been diluted.
  It now plots the worst gap over every dilution the beaker can hold — whose peak is
  derive.py's headline 0.0948 pH — with the beaker's own value marked on top of it.
- **Five layout defects found only by the inline sweep and three only by looking at the
  PNGs**: the strip's words and numbers on one line ("0" under "acidic" at every size);
  labels pushed down onto the strip because its rectangle was not in the registry (`spit
  7.4` inside `neutral`); the x-axis label running into the caption in three views because
  `axesR` registers the *title* only; the linear graph's `4.0e-14` tick reaching the
  rotated y-axis title (fixed by drawing that axis in units of 10^exponent, PhET's own
  0–8 mantissa, with the factor printed in the title); and the meter's reading and its
  "probe is out" note on top of each other in every body under 82 px.
- **Five mutation survivors, each a real blind spot.** (i) The no-stop colour law was
  tested only at r = 0.5, the one ratio where `lerp(a,b,r)` and `lerp(b,a,r)` agree.
  (ii) The probe's wall margin was probed only far outside it. (iii) The dilution
  envelope's reach was never read off the model. (iv) The grab's repaint flag survived
  because the *previous* `pointerup` had called `refresh()` and re-armed `dirty` — the
  Known-bad "anything that forces a draw between an idle proof and the action" one layer
  out. (v) `[OH-] = Kw/h` versus a pH round trip agrees exactly at 1579 of the 4104
  reachable states, so a single-point equality pin lands on one of them; the sweep across
  the grid (2525 states differ, by up to 2.2e-15) is what kills it.

### Known-bad candidates
- **`lerp(a, b, 0.5)` is symmetric, so a two-colour ramp tested only at its midpoint is
  tested by nothing.** The no-stop solute colour survived a 90-mutant sweep with its two
  endpoints swapped. Probe any interpolation off its midpoint.
- **A panel sized from "whatever is left over" can be allocated zero and vanish without a
  single test noticing.** The pH strip was absent from every stage size of a shipped view
  because its guard was `if there is room`, and there never was. Reserve a fixture's space
  *before* sizing the thing next to it, and assert that the fixture is drawn.
- **A quantity written majority-per-minority one way round prints `0.00 : 1` for half its
  domain.** Ratios that can invert need the names of both ends printed with them.
- **`axesR` registers the plot TITLE and nothing else**, so a label placed under a panel
  lands on the *x-axis* label, and the rotated *y-axis* title (drawn at `b.x − 40`, about
  13 px wide) is invisible to every registry — a y-tick label wider than 34 px will reach
  it. Wrap `axesR` to register the x label, and keep linear tick labels short by drawing
  the axis in units of a stated power of ten.
- **An equality pin on a floating-point code path must be swept, not sampled.** Two
  spellings of `[OH-]` agree bit for bit at 38 % of the reachable states; a single-state
  `===` lands on one of those with 38 % probability and proves nothing.
- **A difference panel drawn "at the current setting" is empty whenever the current
  setting is the default.** Plot the envelope over the parameter instead, and mark the
  current setting on it.
