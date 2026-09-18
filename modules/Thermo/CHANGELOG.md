### Thermodynamics Modules - change log

Tracks how `modules/Thermo/` is built: what exists, what each topic covers, and
what mathematics the Python actually does. Dated entries newest first
(Added / Changed / Fixed / Removed). The Known-bad list is permanent — check it
before editing or resurrecting files. Repo policy: Agent `CLAUDE.md` →
"Per-project changelogs".

Source text throughout: Moran, Shapiro, Boettner & Bailey, *Fundamentals of
Engineering Thermodynamics*, 8th ed. (`thermodynamics.pdf` in this directory).

---

## Known-bad — do not reintroduce

- **Do not pass `rp = rc = 1` to `dual_efficiency` expecting the pre-2026-08-01
  behaviour.** It used to raise `ZeroDivisionError` there; it now returns the
  Otto limit. Code that caught the exception to detect "this is really an Otto
  cycle" will silently stop firing. Test for the ratios, not the exception.
- **Do not use `ALT` and `STEEL` as the only difference between two series in a
  figure.** The shared house palette
  `INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"` is safe
  in every pair except this one: OKLab ΔE is 2.6 under simulated deuteranopia
  and 12.5 under normal vision (floor 15), i.e. effectively the same colour for
  a red-green colourblind reader. Use at most three colour-coded series per
  axes, or add a linestyle/marker. See `Topic_9/09.4_dual_cycle/figures/`.
- **Do not place a matplotlib artist outside the axes limits.** Artists are not
  clipped, and `bbox_inches="tight"` then inflates the canvas — one annotation
  at `y≈11` with `ylim=(0, 1.05)` produced a 3564 px-tall SVG. The figure
  checker below catches this.
- **Re-running a `make_figures.py` always dirties its SVGs in git, even when
  nothing has changed.** matplotlib stamps a `<dc:date>` into the SVG metadata
  and generates fresh random `clip-path` ids on every run, so `git status` shows
  the files modified while the rendered image is byte-for-byte equivalent. This
  is true of every trunk's figures, not just Thermo. After re-running generators
  for a check, `git checkout -- <path>` rather than committing 106 no-op diffs.

---

## Layout — how the directory is put together

```
Thermo/
  Topic_<n>/                       13 topic groups, numbered per list.txt
    <nn>.<m>_<slug>/               53 concept modules (the leaves)
      README.md                    scope, operations table, how to run
      notes.md                     derivation with inline page citations;
                                   display maths in $$...$$ (the browser
                                   extracts equations from these)
      refs.md                      citation table: section, equation,
                                   printed + PDF page
      code/<slug>.py               the callable API
      code/test_<slug>.py          self-running checks, "All N tests passed."
      problems/problems.md         worked problems
      figures/make_figures.py      generates the SVGs + captions.json
      figures/*.svg, captions.json
    <n>.EP_example_problems/       worked book examples   ) 39 document folders
    <n>.EQ_list_of_equations/      equation register      ) (13 topics x 3),
    <n>.HP_homework_problems/      end-of-chapter problems) each with code/ + tests
  constants/                       physical constants + gas-constant table
  steam_tables/                    A-2..A-6 as machine-readable CSV + _extract.py
  list.txt                         the 53-module breakdown (authoritative index)
  plan.txt                         the original structuring plan
  Thermodynamics_Conversion_Factors_and_Constants.md
```

92 module directories in total (53 concept + 39 document), which is what
`../ma_browser_web.py` reports. Tests are plain scripts, not pytest: run
`python3 test_<slug>.py` from inside a `code/` directory.

---

## Topic map

| # | Topic | Concept modules |
|---|-------|-----------------|
| 1 | Foundations & system concepts | open systems, closed systems, extensive properties, intensive properties, quasiequilibrium |
| 2 | Energy & work | work, expansion work, compression work, power, kinetic energy, potential energy, buoyancy |
| 3 | The laws of thermodynamics | zeroth, first, second, third |
| 4 | Properties & state functions | enthalpy, entropy, exergy, phase change, Gibbs phase rule |
| 5 | Property data: tables & diagrams | saturation tables, vapour tables, liquid tables, p-V diagram, T-S diagram |
| 6 | Processes & idealizations | reversible, irreversible, adiabatic, steady state, mass conservation |
| 7 | Performance metrics | efficiency (η, COP, isentropic efficiencies) |
| 8 | Components & devices | compressor, condenser, heat exchanger, heat pump |
| 9 | Power & refrigeration cycles | Carnot, Otto, Diesel, dual, Brayton, Rankine |
| 10 | Engines | Carnot engine, Stirling engine |
| 11 | Psychrometrics | dry-bulb, wet-bulb |
| 12 | Combustion & reacting mixtures | fuels, ionization (Saha) |
| 13 | Compressible flow & gas dynamics | subsonic, supersonic, shock, laminar flow, turbulent flow |

Cross-trunk leaves kept here for completeness but really belonging elsewhere:
buoyancy and laminar/turbulent flow (→ CM, fluids), ionization (→ PK, plasma).

---

## Numerical mathematics used in the Python

What the code actually *computes*, as opposed to what it states. Everything is
plain `math`/`csv` in the module code — no SciPy — so each method is visible and
checkable. `numpy`/`matplotlib` appear only in `figures/`.

**Quadrature — trapezoid rule.** Used wherever a thermodynamic quantity is an
area: `W = ∫p dV` and `Q = ∫T dS`. Second-order accurate; the convergence is
demonstrated against a closed form in `01.5_quasiequilibrium/figures/fig2`
(error ∝ N⁻²), which is also the check that the default `n_steps=20000` is far
inside tolerance.
- `01.2_closed_systems` (`pdv_work_trapz`), `01.5_quasiequilibrium` (`pdv_work`),
  `05.4_pv_diagram` (`work_pdV`), `05.5_ts_diagram` (`heat_TdS`),
  `06.1_reversible_processes` (`heat_int_rev_area`), `5.EQ`
- `03.4_third_law` (`absolute_entropy`) integrates `c_p/T` from 0 K, which
  converges only because the Debye `c_p ∝ T³` kills the integrand at the origin.

**Root-finding — bisection.** Used where a relation cannot be inverted in closed
form.
- `13.2_supersonic` (`mach_from_area_ratio`): the area-Mach relation is
  double-valued, so the bracket is chosen by the `supersonic` flag — one root
  below M=1 and one above.
- `12.2_ionization` (`dissociation_extent_CO2`): degree of dissociation from the
  equilibrium constant.

**Fixed-point / successive substitution.** `itmax`-bounded loops.
- `13.5_turbulent_flow` (`friction_factor_colebrook`): the Colebrook equation is
  implicit in `f`. `friction_factor_haaland` is the explicit approximation, and
  the two are compared inside the module's own figure (agreement ~1%).
- `12.2_ionization`: iteration on the dissociation balance.

**Interpolation — linear and bilinear.** The steam tables are discrete, so every
property lookup is an interpolation.
- `05.1_saturation_tables` (`sat_T`, `sat_p`): linear in one index.
- `05.2_vapor_tables` (`superheated`): **double** interpolation, in temperature
  along each bracketing isobar and then in pressure between the results — drawn
  node by node in that module's `fig2`.
- `05.3_liquid_tables` (`compressed`), `01.1_open_systems/steam_lookup.py`,
  `4.HP`, `5.EP`, `5.EQ`, `5.HP`.

**Closed-form algebra with removable singularities.** The cycle-efficiency
expressions are exact, but several have 0/0 points at physically meaningful
limits. `dual_efficiency` at `rp = rc = 1` is the one that bites; see the
2026-08-01 entry.

**Data loading.** `csv` against `steam_tables/*.csv` (A-2 … A-6), which
`_extract.py` produced from the book's appendix.
- `05.1`, `05.2`, `05.3`, `01.1_open_systems`, `constants`, `9.HP`, and the
  figure generators for `09.6_rankine_cycle`, `11.1_dry_bulb_temperature`,
  `11.2_wet_bulb_temperature`, `12.1_fuels`.

**Lever rule (linear mixing).** `y = y_f + x·y_fg` for every two-phase property,
and its inverse for quality. Exact, not numerical, but it is the single most
reused relation in the trunk — Topics 4, 5, 8, 9 all lean on it.

---

## 2026-08-01 (second pass) — depth of the written derivations

### Why
Measured against the other trunks, Thermo was thin on *explanation*, not on
files. Medians before this pass:

| | `notes.md` | `problems.md` | `README.md` | `$$` equations per module |
|---|---|---|---|---|
| **Thermo** | **42** | **34** | **33** | **3** |
| NE | 187 | 173 | 100 | 11 |
| ST | 186 | 138 | 95 | 18 |
| QM | 157 | 156 | 96 | 12 |
| MACRO_EM | 175 | — | — | — |
| RE | 103 | 100 | — | — |
| SM | 54 | 74 | 56 | — |
| CM | 26 | — | — | — |

Thermo was second-lowest on derivation depth and carried about a quarter of the
displayed mathematics per module. The gap was one of *kind*: Thermo stated
results in backticked prose where the mature trunks derive them step by step in
LaTeX, cite the book's own equation numbers at each step, and tie every formula
to the function that implements it and the test that pins it.

### The house standard, for whoever continues this
`NE/NE-06_decay_kinetics/notes.md` is the reference instance. The shape is:

1. A framing paragraph: what this module answers, relative to its neighbours.
2. A **citation key** naming the source and the printed→PDF page offset.
3. **Numbered sections**, each one idea, with the derivation shown — assumption
   → algebra → `\boxed{}` result — and `[M Eq. 2.17, §2.2.3, p.48]` at each step.
4. Every formula tied to the call that implements it, in backticks.
5. A table of **computed** values, never hand-arithmetic.
6. The physical reading, and the mistake the reader is about to make.
7. A closing **"Where this goes"** listing downstream modules.

Two rules were applied throughout and are worth keeping:
- **Every number written down was computed from the module's own code first.**
  This caught a wrong claim in 2.4 (forgetting rpm→rad/s overstates power by
  60/2π ≈ 9.55, not by 2π/60 ≈ 0.105) before it shipped.
- **Anything the notes claim the tests pin, the tests must actually pin.** Where
  a note said "the test suite checks X", X was added to the test file.

### Added — 8 of 53 concept modules brought to that standard
`2.1`–`2.7` (all of Topic 2) and `3.2`. Their `notes.md` went from 16–42 lines
to 108–142; the trunk total rose from 2412 to 3211 lines. Test assertions in
those modules went from 54 to 122 — measured, not estimated:

| module | before | after | | module | before | after |
|---|---|---|---|---|---|---|
| 2.1 work | 7 | 11 | | 2.5 kinetic energy | 5 | 12 |
| 2.2 expansion work | 5 | 12 | | 2.6 potential energy | 5 | 14 |
| 2.3 compression work | 6 | 18 | | 2.7 buoyancy | 7 | 20 |
| 2.4 power | 7 | 11 | | 3.2 first law | 12 | 24 |

The trunk now runs **2175 assertions across 92 test files**, all passing.

New material pinned by tests rather than asserted in prose: Moran's Example 2.1
in all three polytropic exponents plus its Quick Quiz two-step path (22.16 kJ);
his p.43 units example for both ΔKE (0.34 kJ) and ΔPE (−0.10 kJ) on the same
1 kg system; datum-independence of ΔPE; the polytropic compression cost table
(69.3 / 74.3 / 77.0 / 79.9 kJ at n = 1.0 / 1.2 / 1.3 / 1.4); the spring's
quadratic work increments; and Example 2.2's −4.4 kJ heat rejection.

### Fixed — the printed→PDF page offset in Topics 1 and 2
Every `refs.md` states the offset between the book's printed page numbers and
the PDF's physical pages. **16 files claimed +17 and 80 of their table rows gave
a PDF page one too low**; the remaining 473 rows across the trunk already used
+18. Verified with `pdftotext`, which is unambiguous: PDF 58→printed 40,
59→41 (carrying Eq. 2.5), 65→47, 66→48 (carrying Eq. 2.17 `W = ∫p dV`). Two rows
that were already +18 were spot-checked and left alone: PDF 283→printed 265
(Eq. 5.9 η_max) and PDF 533→printed 515 (Example 9.1). The **printed** numbers
were right throughout, so only the PDF column and the header sentence changed;
all 553 citation rows now agree at +18.

### Fixed — a mis-described equation in 2.7
`refs.md` listed Eq. 1.11 as the differential `dp = −ρg dz` in §1.6.2 on printed
p.16. Reading the page: Eq. 1.11 is the *integrated*, constant-ρ form
`p = p_atm + ρgL`, stated in **§1.6.1 on printed p.15** and merely *applied* in
§1.6.2. Corrected, with the distinction recorded in the table.

### Still to do
45 concept modules remain at the old depth — Topic 1, Topic 3 (`3.1`, `3.3`,
`3.4`), and Topics 4–13. `3.3` is already the best of the untouched set (57
lines, with the Clausius and Kelvin–Planck statements quoted verbatim and
checked against printed pp.245–246 during this pass) and needs the least work.
The thinnest remaining are `13.3` (35), `4.4` (35), `1.3` (36), `13.2` (36),
`13.4` (36). The 39 EP/EQ/HP document folders were not in scope.

---

## 2026-08-01

### Added
- **A `figures/` layer for all 53 concept modules — 106 SVGs.** Thermo was the
  only trunk in `modules/` with no figures at all: it is 92 of the library's 241
  modules and was contributing 0 of its 242 figures, while every other trunk
  averaged 2 per module (SM 6, QO 6, PK 4, QF 5, CM 20, EM 18, QM 22, MA 22,
  ST 18, RE 16 figure directories). `ma_browser_web.py` already discovered
  `<module>/figures/*.svg` + `captions.json` and counted them, so the slot was
  wired up and simply empty. Adding them took the browser from **242 figures to
  348**; the NE trunk landed the same day, so `ma_browser_web.py` now reports
  253 modules and 395 figures overall.

  Each `make_figures.py` follows the convention shared by the other 137
  generators in `modules/`: matplotlib → SVG with `svg.fonttype="path"` (text as
  vector outlines, no font dependency), `font.size=11`, the house palette, a
  `_save()` helper, and a `captions.json` mapping each filename to the one-line
  caption the browser renders beneath it. Every generator imports its own
  module's code from `../code`, so the figures exercise the API they document
  and a broken module breaks its figure — several captions additionally assert
  a closed form against the module's numerical routine.

  Figures were chosen to carry content the prose cannot: path-dependence of work
  drawn as three areas between the same end states (1.5); the saturation dome
  plotted from every row of A-2 (5.1); the double interpolation drawn node by
  node (5.2); p-v and T-s diagrams for all six cycles (Topic 9); the
  area-velocity sign flip at M=1 (13.1); a Moody chart generated from the
  Colebrook solver rather than scanned (13.5).

- **`figures/make_figures.py` for Topics 1–13**, plus this changelog's layout,
  topic map, and numerical-methods inventory above.

### Changed
- **Figure palette discipline, recorded in Known-bad.** The house palette was
  run through the data-viz validator's six checks (ported to Python; the bundled
  `validate_palette.js` needs a JS runtime, which this Mac has not). Result:
  every pair separates safely **except ALT/STEEL**, which is deuteranopia-ΔE 2.6
  and normal-vision ΔE 12.5 — below the floor of 15. New figures therefore use
  at most three colour-coded series per axes and never let ALT/STEEL be the sole
  distinction; `09.4_dual_cycle` groups its two combustion legs under one hue
  with different linestyles for exactly this reason. No existing figure was
  repainted — this is a rule for new work, not a migration.
- Dual-axis plots avoided throughout. Where two measures of different scale had
  to be shown together (η vs COP in 7.1, η vs net work in 9.5, efficiency vs
  exit quality in 9.6, p_sat vs h_fg in 5.1, M_y vs pressure ratio in 13.3) they
  are drawn as side-by-side panels instead.

### Fixed
- **`dual_efficiency(r, rp, rc)` raised `ZeroDivisionError` at exactly
  `rp = rc = 1`.** Symptom: plotting the dual-cycle family across `rc ∈ [1, 3]`
  died on the first point. Root cause: the closed form
  `η = 1 − r^(1−k)·(rp·rc^k − 1)/((rp−1) + k·rp·(rc−1))` sends numerator and
  denominator to zero together at that point, so the reduction to Otto that the
  function's own docstring promises was reachable only as a limit, never at the
  point — the module's tests had been quietly working around it with
  `1.0 + 1e-9`. Writing `rp = 1+a`, `rc = 1+b` gives `num ≈ a + kb ≈ den`, so
  the ratio → 1 and `η → 1 − r^(1−k)`, exactly Otto; the guard now returns that.
  Verified: `test_dual_cycle.py` 14 → 16 assertions, all passing, with the two
  new ones pinning both the point and the approach to it.

### Verification
- All 92 module test scripts pass (`python3 test_*.py` in each `code/`),
  unchanged from before this work apart from dual_cycle's 14 → 16.
- All 53 figure generators run clean; 106 SVGs emitted, each with a matching
  caption entry.
- A throwaway checker (not committed) additionally asserted, across the whole
  trunk: no generator failures, no runaway `bbox_inches="tight"` canvases, no
  SVG without a caption and no caption without an SVG, and no caption with an
  odd number of unescaped `$` (which would leave a KaTeX math span open and
  swallow the prose). Worth re-creating before any future figure sweep.
- Figures were also rasterised to PNG and inspected by eye, which is the only
  thing that caught a degenerate p-V "cycle" in 5.4 whose two isotherms shared
  the same pV product and so enclosed zero area, and several legend/annotation
  collisions.

---

## Earlier history (backfilled from git)

Reconstructed from `git log -- projects/modules/Thermo`; the pre-August work
predates this changelog, so the granularity is coarse.

- **2026-07-06** — `merged all modules` (97b5e8f4): Thermo brought together with
  the other trunks under `modules/`.
- **2026-06-30** — `Untrack pyc bytecode caches and .DS_Store` (f6189050).
- **2026-06-28** — `major overhaul (chunk 6/6)` (959cec8e) and the chunks before
  it: the topic/module skeleton, `code/` + tests, `notes.md`/`refs.md`/
  `problems/`, the EP/EQ/HP document folders, `steam_tables/` extraction, and
  `constants/`.
