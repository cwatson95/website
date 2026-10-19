# BRIEF — remaking the PhET sims of `docs/phets/` in Cooper's house style

You are one of several agents working in parallel. Each remakes one PhET
simulation (or one family of them) as a **new single-file HTML sim that looks
and works like Cooper's own simulations** in `projects/simulations/`. Read this
whole brief before starting.

## Paths

`W` = `/Users/cooper/coding/Agent/.claude/worktrees/phets-revised` (a sparse git
worktree on branch `worktree-phets-revised`). Use absolute paths.

| what | where |
|---|---|
| the PhET originals (official minified builds, read-only) | `W/docs/phets/<stem>_en.html` |
| every English UI label each original ships, decoded, plus its screens | `W/docs/phets_revised/build/_survey/inventory.json` (keys: `title`, `version`, `screens_by_repo`, `ui_by_repo`) |
| the house process — read ALL of it | `W/projects/simulations/PLAYBOOK.md`, `W/projects/simulations/CLAUDE.md` |
| the accumulated traps — read them | the Known-bad list at the top of `W/projects/simulations/CHANGELOG.md` (everything above the first `## 20` heading) |
| house sims to learn from and extract from | `W/projects/simulations/*.html` (59). Scaffold source: `diffraction.html` or `steam_carnot_cycle.html` (the PLAYBOOK recipe yields 252 lines incl. the site nav and `h()`). 3-D molecules: `/Users/cooper/coding/website/simulations/amino_acids.html` and `standard_model.html` (not in the worktree; their nav hrefs are in the site form) |
| harnesses | `W/projects/simulations/tools/` (`ui_drive.js`, `recorder.js`, `audit.py`, `raster.py`, `mutate.py`) |
| **your output** | `W/docs/phets_revised/<stem>.html` — `stem` = the PhET file name minus `_en.html`, e.g. `projectile-motion.html` |
| your build dir | `W/docs/phets_revised/build/<stem>/` — part files, `derive.py` (the Python twin), reference values, `ui_drive_<stem>.js`, `capture_tail_<stem>.js`, `mutants.json`, `changelog_entry.md` |
| generated artifacts | `W/docs/phets_revised/build/<stem>/_out/` (gitignored): `run.js`, `ui_run.js`, `display.json`, PNGs, logs, mutant scratch |

## What to build

- **A clean-room remake of the PhET sim's content**: the same screens, the
  same model (physics / chemistry / maths), the same key interactions
  (dragging charges, launching, placing objects, the sliders and toggles).
  Sources: `inventory.json`, your knowledge of the PhET sim, PhET's model
  notes (try WebFetch on
  `https://raw.githubusercontent.com/phetsims/<repo>/main/doc/model.md`;
  a failed fetch is not a blocker), and constants read out of the minified
  original where parity matters (cite them as "PhET's value").
- **Never copy PhET code, images or sounds.** New code, drawn on canvas in
  the house style.
- **House form** (PLAYBOOK §4): tabbed views with lower-case noun-phrase tab
  names, a left canvas stage, the floating readout top right, the right
  control panel with an `INFO[view]` paragraph of prose, and the equation bar
  along the bottom carrying the one equation that view is about. Map each
  PhET screen to one or two views. House form is six views; use the spare
  slots for analysis views only where they add real insight (the governing
  law made visible, a sweep, a limiting case). 4–6 views.
- **The aesthetic is extracted, not restyled.** Take the scaffold (CSS,
  palette, `h()`, camera) and the 2-D plotting layer from the house sims with
  the PLAYBOOK recipe, and edit only the `<h1>`, the `.sub` tagline and the
  `:root` accents. Colour semantics: green = the computed thing, orange =
  reference/analytic or a warning, magenta = the live marker, cyan =
  structure. Georgia italic for tabs, chips, plot titles and the equation
  bar. Significant-figure formatting. Print every scale distortion on the
  canvas.
- **Site nav**: keep the house `site-nav-css` block and header, but point
  every link at the live site with absolute URLs, because the house sims'
  relative `../website/` links are dead from `docs/phets_revised/`:
  `https://cooper-watson.net/index.html`, `/about.html`, `/teaching.html`,
  `/modules/teaching_modules.html`, `/simulations.html` (keep
  `aria-current="page"` on it), `/research.html`, `/cv.html`.
- **Credit** in the header comment and in a visible `.src` line: "Remake of
  PhET Interactive Simulations' <Title> (University of Colorado Boulder,
  phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets." The
  header also says plainly what is exact, what is modelled, what is not
  modelled, and where every measured number came from.
- Flat single file: no network, no external libraries, works from `file://`.

## Verification (PLAYBOOK §5, all four layers; "verify" means falsify)

1. `derive.py` first: re-derive the model and print reference values to 10+
   digits. The `selfTest()` asserts them, labelled `(python)` / `(scipy)`.
   Cross-check anything clever against a brute-force version.
2. `selfTest()` green under `osascript -l JavaScript` (`N passed, 0 failed`),
   including panels-build-clean for every view × preset and no non-finite
   values.
3. UI drive: adapt `tools/ui_drive.js` (its three sim-specific thresholds),
   covering every tab, slider, checkbox and chip. Assert that your custom
   drags MOVE the drawing, through the frame loop, idle first.
4. Mutation sweep with `tools/mutate.py`: ≥ 20 physics mutants (every leading
   coefficient, exponent, unit conversion and sign) plus the UI mutants.
   Every survivor is fixed or explained as equivalent. **Sweep a COPY of your
   html inside your own `_out/`, never `docs/phets_revised/<stem>.html` in
   place**: `mutate.py` writes its scratch `_mutant.js` next to the html it
   tests, so in-place sweeps by parallel agents share one
   `docs/phets_revised/_mutant.js` and corrupt each other's kill counts.
5. Display-list capture → `audit.py` → `raster.py` → **look at every view's
   PNG** (Read them). Fix overlaps, unclipped curves and blank views.

Run osascript jobs one at a time: other agents share the CPU.

`tools/mutate.py` has no per-mutant timeout, so a mutant that turns a
correction loop into an infinite one stalls the whole sweep (and aborts it
half an hour later). Keep every mutant terminating — break constants, signs
and exponents, not loop conditions that must converge. Worse, such a mutant
OUTLIVES the sweep: two `jsc` runs of one waves-intro mutant were still
burning half a core each 28 hours later. After a sweep, check for stragglers
(`ps -Ao pid,etime,command | grep jsc`) and kill them by PID once you have
read the command line — never by pattern.

**Never kill processes by a shared pattern** (`pkill -f _mutant.js`, `killall
osascript`, and the like). Other agents' sweeps and suites are running at the
same time, and `mutate.py` records a killed run as a CAUGHT mutant — so a
stray kill silently turns someone else's real survivor into a false pass.
Kill only PIDs you started yourself, and only when you must.

Letter subscripts are not safe on the canvas (found by the greenhouse-effect
build): there is no Unicode subscript f at all, and the ones that do exist are
not all in the rasteriser's font, so `T_eff` renders as tofu. Digit subscripts
and superscripts are fine; write letter subscripts as ASCII.

Known scaffold trap (found by the wave-on-a-string build): the HTML hint
(`#hint{bottom:11px}`) sits on the last line of a bottom-anchored canvas
caption, and the canvas capture cannot see it because the hint is HTML.
Reserve ≥ 18 px at the canvas bottom for the caption and assert that the
corner is clear (`build/wave-on-a-string/` has the fix and its assertion).

## Rules

- **No git writes** (no add, commit, stash, checkout, reset, worktree). Read-only git is fine.
- Name the UI drive exactly `build/<stem>/ui_drive_<stem>.js` (full stem, no
  abbreviation): the orchestrator's `_tools/verify_one.py` runs it by that name.
- Create or modify files only in your build dir(s) and your output html(s).
  Never touch the main checkout (`/Users/cooper/coding/Agent/docs/...`); the
  orchestrator lands your work. Never edit shared files (`BRIEF.md`,
  `inventory.json`, `docs/phets_revised/CHANGELOG.md`).
- **Family jobs**: build the full sim first, then each basics/intro variant
  as its own complete single file (the same engine code, trimmed to that
  sim's screens and controls), with its own build dir, selfTest, UI drive and
  captures.
- Don't gold-plate. PhET's screens and core interactions first, analysis
  views second. If one PhET feature is disproportionately expensive (a game
  screen, say), build a faithful subset and name the gap in your report.
- Write `build/<stem>/changelog_entry.md` in the house format: heading
  `## <the date you finish, YYYY-MM-DD> — <stem>: <one line>`, then `### Added` (what is exact),
  `### Fixed (during the build)` (symptom **and** root cause) and
  `### Known-bad candidates`.

## Report back (your final message, ≤ 40 lines)

Per sim: output path, file size, the views (tab names), what is exact vs
modelled, `selfTest` N/0, UI drive M/0, mutants killed/total with every
survivor explained, data sources, known gaps against the PhET original, and
anything the orchestrator must know.
