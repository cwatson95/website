## 2026-09-22 — build-an-atom: PhET's Build an Atom remade, with its stability table checked against an independent one

### Added

`docs/phets_revised/build-an-atom.html` — a clean-room remake of PhET
Interactive Simulations' **Build an Atom** 1.9.3 (University of Colorado
Boulder, CC-BY 4.0; new code, no PhET code or assets). Six views: *the atom*
(PhET's first screen — the three buckets, the nucleus, orbits or cloud, and
the four things the counts determine), *the symbol* (its second screen),
*the game* (its third: four levels of five challenges scored 2 and 1),
*the counting* (all 1694 bucket configurations, with the census that makes
the rules checkable), *chart of nuclides* (PhET's whole stability table on
the (N, Z) plane beside an independent one), and *mass and binding*
(measured isotope masses and abundances, their mean, and the binding energy
they imply).

**What is exact.** The three rules are arithmetic on three integers and are
checked *everywhere*: `selfTest` walks all 11 × 14 × 11 = 1694 configurations
the buckets allow and compares the element, the mass number, the charge and
the stability of each against an independently written expression (counting
loops rather than arithmetic, a Set of keys rather than `indexOf`). The
census that follows is pinned to `derive.py`: 153 neutral, 1540 ions, 220
with a stable nucleus — which is 20 distinct stable nuclides × 11 electron
counts, exactly, because stability does not depend on electrons. Those 20
are every stable nuclide with Z ≤ 10 that exists, and PhET's 13-neutron
bucket is exactly one more than neon-22 needs.

**PhET's own values, read out of the minified original** by
`build/build-an-atom/extract_phet.py`: the 10/13/10 buckets, MAX_ELECTRONS,
the 85 and 130 shell radii, the ten electron slots (two at ±85, eight at
130 starting at π/8 × 1.2 and stepping 2π/8), the cloud law
r(e) = 42.5 + 8.75 e (which puts ten electrons exactly on the outer shell),
the 100 and 1.1 × 130 capture radii, both charge-sign conventions,
`stableElementTable`, `numNeutronsInMostCommonIsotope`, `standardMassTable`,
the isotope table, the symbol and element-name strings, the atomic radii, the
four `AtomValuePool` challenge pools, the four level type lists and the
5-challenges / 2 / 1 scoring.

**Stability is measured data, and it is cross-checked.** PhET's table holds
**244** nuclides, Z = 1 to 82. It is compared here against an independent
one built from NUBASE half-lives and NIST isotopic compositions (by way of
this repo's own `projects/simulations/periodic_table.html`) under the
criterion "occurs in nature and has never been observed to decay": **253**
nuclides, also stopping at lead. **They agree on 243.** PhET alone counts
germanium-76, whose double-beta half-life of 1.9 × 10²¹ yr has actually been
measured; the independent table alone counts ten (Cr-50, Zn-70, Te-123,
Xe-124, Xe-134, Ba-132, Ce-138, Ce-142, W-183, Pb-204), every one a nuclide
whose predicted decay has never been seen. **Below Z = 24 the two sets are
identical**, so nothing this sim can build is in dispute. Neither counts
bismuth-209 (α, 2.0 × 10¹⁹ yr, measured 2003). Both give technetium and
promethium no stable isotope at all. Asserted: the 244, the 253, the 243
agreement, the two exception lists nuclide by nuclide, the heaviest (Pb-208),
the two empty rows, and the Z below which the two are identical.

**Other measured results, all pinned to `derive.py`.** PhET's isotope masses
agree with the independent mass excesses to 1.6 × 10⁻⁶ u and its abundances
with NIST to 3.2 × 10⁻³ percentage points. Σ(abundance × mass) reproduces
PhET's published standard atomic weight to 1.4 × 10⁻⁴ relative, worst at
lithium — which is not an error in either, because lithium's isotopic
composition varies enough between natural sources that IUPAC gives it an
interval. Binding energies come from the masses by
B = [Z m(¹H) + N mₙ − m(A, Z)]c², with no mass formula and no fit; the curve
peaks at **nickel-62** (8.7945 MeV/nucleon) just above iron-56 (8.7903), and
the two data sources give the same B/A to 1.6 × 10⁻⁴ MeV. Hydrogen-1's
binding energy is zero to the keV the table is rounded to. The even/odd
census of the stable set is 140 / 52 / 48 / 4, and the four odd-odd nuclides
(H-2, Li-6, B-10, N-14) are all inside what the buckets can build. Four of
the five commonest neutron numbers are magic, and N = 82 carries six stable
isotones against one on each side.

**The game** reproduces PhET's rules exactly — its four type lists, its four
atom pools, no type twice in a row, schematic challenges restricted to Z < 3
and every other type to Z ≥ 4, a charged atom asked for about half the time
on charge questions — with a seeded mulberry32 that is reproduced bit for bit
in Python. `selfTest` generates 16 000 levels and checks that every one of
the 80 000 challenges is answerable, that no type repeats and that the Z
rules hold. PhET's fallback (reuse a used atom when the filtered pool is
empty) is reachable exactly once in those 16 000 — level 2 at seed 2691,
whose five all-schematic challenges exhaust the four charged atoms with
Z < 3 — and that rate is asserted rather than forbidden.

Verification: `selfTest` **2330 passed, 0 failed**; UI drive
**437 passed, 0 failed**; mutation sweep **86 of 86 caught, 0 survivors,
0 skipped** (68 physics + 18 UI mutants — every leading constant, every
unit conversion, every sign, PhET's bucket sizes and shell radii, the PRNG,
the challenge-selection rules, the scoring, and the dirty flag on every
interaction); `tools/audit.py` clean on all three captures (1400 × 820,
820 × 520, 560 × 380); 32 captured configurations rasterised and looked at.
The first sweep had four survivors, all real gaps, all now pinned (below).

### Fixed (during the build)

- **A finder that matches a word drives the wrong control.** The game's
  answer sliders were first labelled `protons` / `neutrons` / `electrons`,
  the same as the atom group's. Renamed `answer: protons` and so on before
  the harness could silently drive the wrong one.
- **A pointer handler that refreshes the whole view masks the dirty flag.**
  `pointerup` called `refresh()`, which draws unconditionally, so the
  frame-loop drag test would have passed with the flag deleted. Split
  `refresh()` into `panels()` (the HTML) and the draw; the handlers update
  the panels and set `dirty`, and only the frame loop draws.
- **A click and the picture disagreeing.** The atom view's periodic table and
  the game's level cards were positioned inside the draw and the pointer
  recomputed them, so the two could drift. Both are now produced by
  `atomGeo` / `gameGeo`, which draw nothing.
- **`axes()` draws its tick labels outside the label registry**, so a
  `labelIfClear` label lands on a tick. Added `axesR`, which registers every
  piece of text `axes()` draws — including the y title's *rotated* box.
- **A panel title wider than its panel.** "N/Z along the valley" ran out of
  the right-hand chart panel and under the floating readout at 820 px.
  `panelTitleFit` measures and falls back to a short title.
- **A long key beside a right-aligned value.** The counting view's census
  rows collided ("odd-odd" through "4: H-2, Li-6, B-10, N-14") at 820 px.
  `kvRow` now puts the value on its own line when the pair does not fit;
  squeezing the key into whatever the value left was the first, worse, fix.
- **`legendAuto` dodges polylines and labels, and the nuclides are
  fillRects**, so the chart's legend was placed over the top of the stable
  band. It is now placed by a function that tests each corner against the
  *drawn* squares, and `selfTest` re-measures that over the whole Z-range
  slider (37 settings).
- **An annotation over the data it describes.** The isotope panel's
  "Σ ab × m" block sat on the tallest abundance bar. `annotate()` is given
  the bars' rectangles and picks a clear corner.
- **A fixed question height pushes the answer onto the caption.** At
  560 × 380 the game's "set them in the panel" line landed on the stage
  caption. The question box now gives up exactly the height the answer needs,
  and the inline sweep was extended to draw every challenge of every level at
  three sizes — the first sweep sat in the game's *idle* phase and could not
  see it.
- **The corner captions of the symbol box overlapped its numbers**, because
  their offset was a fixed fraction of the box rather than the number's own
  measured height.
- **The element name landed on a bucket caption.** The atom view now reserves
  a band for the three labels PhET puts under the atom and shrinks the
  picture into what is left.
- **A drawing test that reads ambient state.** The display capture runs after
  `selfTest` (the entry block calls it when there is no document), and
  `gameReset` deliberately does not clear the best scores — so every level
  card read "best 10/10" in the first capture. The capture tail resets them.
- **Four mutation survivors, all real gaps.** `signed()` (the charge
  formatter) and PhET's `ELECTRON_RADIUS` only ever reached a drawing, so
  swapping the signs and shrinking the radius changed nothing any assertion
  could see; both now have absolute pins, and the one test that *mentioned*
  the radius ("no two electron slots overlap") still passed at 7 px, which is
  the lesson. The level-seed mixing was an argument to `makeChallengeSet`,
  and dropping it was invisible because the challenge sets differ between
  levels anyway (the type lists differ) — it is now a named function whose
  result is stored in `GAME.seed` and pinned against `derive.py`. And the
  reset-all test ran from the default view, so "it leaves the view where you
  were" was vacuous; it now resets from the chart view.
- **A capture that names a state it is not in.** `gameCheck()` returns
  without doing anything while the phase is `wrong`, so the `game_shown`
  capture (wrong twice) sat in the one-more-try state under a name that said
  the answer had been shown. The capture tail retries between the two checks.
- **An empty type name in the finished-level caption.** `gameCaption` read
  `gameCurrent()`, which is null once the level is over, and printed
  `type ""`. The done phase has its own caption.
- **A longer caption breaks a two-panel layout whose panels have minimum
  heights.** Adding one sentence to the mass caption pushed the binding
  panel's axis title onto it at 820 × 520, because `layout()` only reserves
  120 px of stage before keeping the long caption and the `Math.max` floors
  then overflow. `layoutMin()` takes the view's own floor, so a long caption
  is traded for the short one instead of for a collision.

### Known-bad candidates

- **Never reconcile PhET's atomic radii against `periodic_table.html`'s
  radius column.** They are different quantities: PhET ships the *Clementi
  calculated* radii (hydrogen 53 pm, which is the Bohr radius) and
  `periodic_table.html` column 15 is mendeleev's `atomic_radius` (hydrogen
  154 pm). A first version of `derive.py` reported 94 "mismatches" and they
  were all definitional. What IS checkable is the definition — hydrogen's
  Clementi radius is a₀ to the printed precision — and that is what the
  suite asserts.
- **"Half-life is null" is not "stable".** The NUBASE table carries no
  half-life for 569 nuclides, most of them drip-line nuclides whose
  half-life is unmeasured because it is ~10⁻²¹ s (Li-12, B-16). Abundance
  alone is no better: it admits K-40 and U-238. The criterion that works is
  *both* — occurs in nature AND no decay ever observed — which gives 253,
  all with Z ≤ 82.
- **A generator's documented fallback must be asserted as a rate, not
  forbidden.** PhET reuses an already-posed atom when the filtered pool is
  empty, and that path is reachable: 1 level in 16 000. A test that demanded
  "no atom is ever repeated" failed on correct code.
- **A canvas quantity used only in drawing is invisible to every
  assertion, and a test that *mentions* it is not a test of it.** Two of the
  sweep's four survivors were `signed()` (the charge formatter, used only in
  captions and the charge strip) and PhET's `ELECTRON_RADIUS` — whose only
  assertion, "no two electron slots overlap", still passed at 7 px because
  the slots are 99 px apart. Absolute pins, always.
- **A value that only ever appears as a function ARGUMENT cannot be
  asserted.** The level seed was `makeChallengeSet(level - 1, (gseed +
  level * 7919) | 0)`, and deleting the mixing changed no challenge set that
  any test compared, because different levels have different type lists and
  so produce different sets either way. Lift such a value into named state
  (`GAME.seed`) and pin it — which also made it honest on the canvas, where
  the finished-level card prints the seed the level actually ran on.
- **`layout()`'s 120 px stage floor is not enough for a view whose panels
  have minimum heights.** One extra sentence in a caption pushed the lower
  panel's axis title onto it. Use a per-view floor (`layoutMin`).
