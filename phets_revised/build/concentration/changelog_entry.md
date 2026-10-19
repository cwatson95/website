## 2026-09-22 — concentration: PhET's Concentration screen on beers-law-lab's engine, with the mole ledger drawn as a ledger and the nine solutes against their sources

### Added
- **`docs/phets_revised/concentration.html`** — a remake of PhET Interactive Simulations'
  Concentration (concentration 1.8.6, CC-BY 4.0), which is the Concentration screen of
  Beer's Law Lab shipped on its own. Four views: **the beaker** (nine solutes, a shaker and
  a dropper, a water faucet, a drain, an evaporator, the concentration meter on a draggable
  probe reading mol/L or mass percent, and the saturation point where solid appears),
  **the ledger**, **the solutes** and **true colour**.
- **The same engine as `beers-law-lab.html`, not a copy of it.** `build/concentration/`
  holds exactly two files of its own — `p1_head.html` (its header and tagline) and
  `p2b_id.js` (its identity and its four tabs, and the `SHOW_BEERS = false` that switches
  the cuvette off). Everything else is read from `build/beers-law-lab/` **by path** at
  assemble time: the data, the chemistry, the state, the beaker, the ledger and colour
  views, boot, the reference table and the whole selfTest. The UI drive is the same harness
  too, copied rather than shared only because `_tools/verify_one.py` insists on the name
  `ui_drive_<stem>.js`, and the copy is rewritten on every assemble so the two cannot drift.
- **The solutes view** is this sim's own, and is where the literature comparison the family
  owes its data lives: PhET's nine saturation points against the Wikipedia chemical
  infoboxes (fetched 2026-09-22, quoted to their own printed precision), with the
  temperature each source states printed beside every row, and the molar masses below. PhET
  matches the literature to **5.6e-5** relative on molar mass and to 0.0–0.6 % on saturation
  for the four sources that quote a room-temperature figure; the worst gap is cobalt(II)
  nitrate at 23 %, whose only usable figure is at 0 °C, and the row says so rather than
  hiding it.
- Everything the shared engine asserts is asserted here too — the exact mole and volume
  ledgers, saturation, the evaporation hyperbola, PhET's colour interpolation and its
  `Math.floor`, the transmitted colour over the CIE 1931 observer — and the pieces that
  belong to the Beer's Law bench are skipped by `SHOW_BEERS`. See
  `build/beers-law-lab/changelog_entry.md` for the derivation and the sources.
- **Verification**: `selfTest` 510 assertions, 0 failed; UI drive 205, 0 failed; display-list
  capture at 1400x820, 1100x700 and 560x380, `audit.py` clean at all three, every view's PNG
  looked at. `mutants.json` carries **61 mutants (52 physics, 9 UI)**, and the sweep run here
  caught **61 of 61** with no survivors.

### Fixed (during the build)
- **The solutes view was laid out for a 1400 x 820 stage and nowhere else.** Nine rows of
  two lines need about 30 px a row; at 1100 x 700 the panel gives 22 and every row landed on
  its neighbour (95 collisions). It now measures what it has: two lines a row above 30 px,
  one line with the numbers pushed right below that, and bars only below 15 px, with the
  molar-mass table dropped entirely at narrow widths so the rows get the whole stage.
- **Its row labels were painted ON the bars**, so a green name sat on a green bar and the
  numbers on an orange one. The text has the top of each row to itself now.
- **Its rows ran bottom to top**, putting PhET's first solute at the foot of a list whose
  own narrow-stage note said "top to bottom in PhET's order".
- **A legend had nowhere to go.** At one line a row the text fills the panel edge to edge,
  so any legend sits on top of it; the two colour roles moved into the axis title, which is
  always there and needs no space of its own.
- **With no bottom row, the main panel ran to the caption** and its x tick labels (which
  hang 21 px below the box) landed in it. `layoutPanels` now shaves 30 px when it builds no
  bottom row.
- **Five mutants survive this sim's sweep for a reason that is not a gap**: the beam's
  width, the sensor's, the cuvette's snap interval, the preset wavelength and the
  per-solution default concentration belong to the Beer's Law bench, which this sim does not
  build. They are swept in `beers-law-lab`, where they are live, and are excluded here with
  that written into `gen_mutants.py` rather than reported as survivors.

### Known-bad candidates
- **A trimmed variant built on a shared engine will carry code it cannot reach, and a
  mutation sweep will call every constant in it a survivor.** Either split the part files so
  the variant does not ship the code (which is what was done for the cuvette, the spectrum,
  the law and the solutes views here), or exclude those mutants by name with the reason
  written down. A survivor that is "this sim has no cuvette" looks exactly like a survivor
  that is a missing assertion.
- The rest of this family's traps are on `build/beers-law-lab/changelog_entry.md` and apply
  to both files, because both files are the same code.
