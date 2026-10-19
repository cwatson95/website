## 2026-09-22 — ph-scale-basics: PhET's Macro screen as its own sim, on ph-scale's engine

### Added
- `docs/phets_revised/ph-scale-basics.html` (157 KB), a clean-room remake of PhET's
  **pH Scale: Basics** 1.7.5 (CC-BY 4.0; new code, no PhET code or assets). PhET's Basics
  sim is the Macro screen of pH Scale on its own — pick one of twelve everyday liquids,
  pour it from the dropper, dip the meter, run the tap, open the drain — and it shows a pH
  and a volume and nothing else. Four views: **the beaker** (PhET's screen), **the
  liquids** (this file's own table of the twelve), **dilution** and **the scale**.
- **The same engine as `ph-scale.html`, taken by path and pinned by SHA-256.** The
  chemistry (`build/ph-scale/p2_chem.js`), the state, the clock and the readout
  (`p3_state.js`), three of the four views (`p4_views.js`) and the reference values
  derive.py printed (`p7_refs.js`) are the same files, never copied; `assemble.py` asserts
  each one's hash, so a change in either directory cannot reach this sim unnoticed. The
  head is generated from ph-scale's by `make_head.py` (only the title, the `h1` and the
  `.sub` differ, which is what the PLAYBOOK allows), and the UI harness by `make_ui.py`,
  which carries 440 of its 465 lines across and asserts every substitution matches exactly
  once. What is genuinely this build's own: the identity (`p2b_id.js` — four tabs, and
  `SHOW_CONC = false`), the liquids table (`p5b_views.js`), the boot and the suite.
- **The trim is PhET's own.** The particle picture, the concentration graph and My Solution
  are simply absent, which is the difference between PhET's two sims; and the beaker
  readout prints a pH, a volume and acidic/neutral/basic with no concentration, no moles
  and no molecule count, as PhET's Basics does. The scale view keeps the two
  concentrations, because they are what that view exists to explain.
- **The liquids table**, the one view ph-scale does not have: the twelve sorted by pH with
  a swatch of each liquid's own colour, PhET's pH, acidic/neutral/basic, the measured range
  and its source where one could be sourced, and the same pour — 0.1 L topped up to the
  beaker's 1.2 L — worked out both ways. They agree to a hundredth of a unit down the list
  and part company at chicken soup (6.73 exact against 6.65 by PhET's rule), which sits
  near the pH where the gap is largest. Twelvefold dilution is log10(12) = 1.079 pH and no
  more, which is the table's point.
- **The chemistry, exact, and the dilution law done properly** — the same as ph-scale's and
  asserted here again, because this file has to stand on its own: Kw = 1.000e-14 at 25 °C
  (pKw = 14.000 exactly), `[H3O+] = 10^-pH`, `[OH-] = Kw/[H3O+]` (not PhET's
  `10^-(14-pH)`, which is out by up to 2.1e-15 because pH − 14 is inexact in a double
  whenever pH < 7). Dilution mixes moles of the net strong acid
  `C = [H3O+] − [OH-] = −2√Kw·sinh(ln10(pH−7))` and re-solves `[H3O+] − Kw/[H3O+] = C`;
  diluting f-fold divides C by exactly f, C is odd about pH 7, and the textbook quadratic
  root is out by 11 % at pH 15, so the rationalised branch is load-bearing. PhET's own rule
  is a chip beside it; the two never differ by more than 0.0948 pH anywhere this beaker
  can reach, and averaging the pH is wrong by up to 4.42.
- **Measured pH ranges for four of the twelve**, with their sources named in the panel and
  the other eight drawn with no range rather than an invented one; PhET's value lies inside
  all four.
- Verification: `selfTest` **1594 passed, 0 failed** (osascript and jsc); UI drive
  **184 passed, 0 failed**; display-list capture at 1400×820, 1100×700 and 560×380 audited
  clean (0 layout problems, 51 PNGs) with every view looked at. `mutants.json` carries
  **101 mutants** (90 of ph-scale's, all of which apply to this build, plus 11 of its own);
  every one of the 101 was spot-checked individually with `spot_mutants.py` and caught. The
  definitive sweep is `sweep.sh`, run against a copy inside `_out/`.

### Fixed (during the build)
- **A reference value typed from the head, wrong in its fourth digit.** The suite asserted
  orange juice diluted twelvefold at `4.5828239616268092`; it is `4.579175035770364`. Root
  cause: the constant was written out rather than read off derive.py's output — exactly the
  Known-bad "a reference value you computed in your head is not a reference value". The
  assertion now pins what the sim PRINTS (`4.58`, which is what the prose claims), the
  agreement of the two independent implementations, and that the shift is log10(12).
- **Seventeen mutants alive inside a file that called itself verified.** The Basics suite
  started as a trim of ph-scale's, so it dropped the assertions on everything the shared
  engine carries but this build never draws: PhET's particle rule, the graph's exponent
  ranges, My Solution's volume range, the unknown-solute fallback, `phFromH3O`/`phFromOH`
  and `molesOf`. All seventeen constants are still in the bundle a reader downloads, so
  they are now asserted here too. Root cause: trimming the VIEWS is not a reason to trim
  the assertions — the code ships either way.
- **The liquids table's two right-hand columns were pinned by one liquid, and it was the
  wrong one.** Orange juice reads 4.58 under both laws, so a check on it passed with the
  PhET column replaced by the exact one, and with the dilution changed under the exact
  column alone. Both survived a spot check until chicken soup — the liquid at which the two
  laws part company, 6.73 against 6.65 — was pinned instead.
- **The table's sort was asserted by membership only**, so reversing it changed nothing any
  test could see. The rows are emitted in order, so their order in the display list is the
  sort, and that is now asserted.
- **`autofill()` could have filled the beaker with water** and the suite would not have
  noticed: the trimmed version kept "autofill puts 0.5 L back" and dropped "of the liquid
  alone".
- **"Picking another liquid redraws the table" passed on a table that had not changed.**
  Two faults at once: the view's only response to the chip was a text COLOUR, which the
  display-list recorder does not capture; and the assertion compared `sigU`, which is
  length-plus-count and is identical for two different rows of the same table. The selected
  row now gets a band (a real `fillRect`) and the comparison is on the geometry.
- **Three layout defects found only by the inline sweep.** The two right-hand headers
  ("0.1 L in 1.2 L" and "by PhET's rule") are 76 px each in an 84 px column at 1100×700 and
  collided — they are now "diluted 12x" and "PhET's rule" in wider columns. The table's
  title is 649 px and ran off a 560 px stage — there is a short form. And the table was
  capped at 26 px a row, which used a third of a 1400×820 picture and left the rest empty.
- **The narrow table painted its "measured range" column green.** Root cause: the colour
  rule was "the last two columns are the computed ones", which is true of the seven-column
  layout and false of the four-column one, where the measured column IS second from last.
  The columns are now coloured by named role.

### Known-bad candidates
- **Trimming a sim's VIEWS is not a reason to trim its ASSERTIONS.** A build that shares an
  engine still ships every constant in that engine, and a suite cut down to the views it
  draws left seventeen live mutants in a file reported as verified. Assert what the bundle
  contains, not what the bundle displays.
- **A table pinned by one row is pinned by the row you happened to choose.** Pick the row
  where the two quantities being compared actually differ; a row where they agree passes on
  a table that computes one of them twice.
- **A view whose only response to a control is a text COLOUR cannot be tested through the
  display list** — the recorder captures text content and position, not fill style. Give the
  selection a geometric mark as well, or no capture-based test can see it.
- **`sigU` (JSON length plus op count) is a weak signature**: two different rows of the same
  table produce the same length and the same count, so "the picture changed" passes when it
  did not. Compare the geometry.
- **A column-colour rule stated as "the last N columns" inverts when the layout narrows.**
  Colour by named role, not by position from the end.
