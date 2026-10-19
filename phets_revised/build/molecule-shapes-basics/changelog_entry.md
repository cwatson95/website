## 2026-09-21 — molecule-shapes-basics: the same repulsion engine with the lone pairs taken out, and the five shapes equal pairs make
### Added
- `molecule-shapes-basics.html` (205 KB), a remake of PhET's Molecule Shapes: Basics 1.6.19 in four
  views: *the model*, *real molecules*, *the shapes* and *the relaxation*. The credit line is in the
  header and on the page, the site nav is absolute, nothing touches the network.
- It is `molecule-shapes.html`'s engine, trimmed the way PhET trims its own Basics: no lone pairs
  anywhere — no lone-pair button, no Show Lone Pairs, no outer lone pairs, no electron-geometry
  name, no ρ slider — and PhET's five Basics molecules, the ones whose central atom has none
  (BeCl₂, BF₃, CH₄, PCl₅, SF₆). Its `assemble.py` copies the nine shared part files from
  `build/molecule-shapes/` and checks them byte for byte, so the two sims cannot drift; what differs
  is the header, a ten-line variant file (four views, PhET's Basics molecule list, no lone pairs)
  and the squeeze view, which Basics does not carry and which is simply left out of the parts list.
- *The model* is PhET's Basics Model screen: single, double and triple bonds round the central atom,
  six at most; remove the last of a kind or all of them; drag an atom round the atom and let it
  slide back; Show Bond Angles and the molecule-geometry name. *Real molecules* is its second
  screen, with the measured geometry of the five. *The shapes* lays the five ideal geometries side
  by side with their angles, and clicking one builds it. *The relaxation* runs plain gradient
  descent from a random start, which for equal pairs always ends in the ideal shape.
- What is exact is the whole content of this sim: linear 180°, trigonal planar 120°, tetrahedral
  arccos(−1/3) = 109.4712206…°, bipyramidal 90/120/180, octahedral 90/180, and the energies 1/4, 1,
  9/4, 17/4, 27/4 of two to six equal pairs. `derive.py` (the twin the two sims share) lands 100 of
  100 seeded random starts of five and of six pairs on the ideal shape; the JS reproduces each to
  1e-9° from the same seeds.
- PhET's data, verbatim: the five molecules' geometry and bond lengths, the tetrahedron's elevation
  −19.471220333° (so its CH₄ is 109.47122033°, not quite ideal), the bond orders, six pairs at most
  and the arc-brightness thresholds; the AXE names are PhET's rules.
- Verification: `selfTest` 1798 assertions green under osascript (the same suite as the full sim,
  its lone-pair sections skipped where Basics cannot reach them and replaced by the Basics
  behaviour: a lone pair is refused outright, six bonds go octahedral); the UI drive 117; 59
  mutants, all killed; 17 captured configurations audited (0 layout problems) and every PNG looked
  at.

### Fixed (during the build)
- **A shared suite that assumes the richer variant fails the trimmed one.** The first Basics run
  had ten failures, all from the model-view block adding a lone pair and then asserting on it. The
  suite now branches once on the variant: in Basics a lone pair is *refused* (which is itself the
  assertion PhET's Basics deserves) and the six-pair molecule is an octahedron rather than a square
  pyramid, with the expected angles read off the shared engine's equilibrium either way.
- **An assertion that hard-codes a count from the other variant.** "The last single bond added
  went" also checked that two singles remained — true for the full sim's mixture, wrong for Basics'
  four. It now counts the singles before the removal and expects one fewer.
- **One row of cells inherits five rows' height.** The AXE table's cell height came from
  `(box height)/rows`, so the Basics table drew five glyphs in cells twice as tall as they were
  wide. The height is capped at 1.45 × the cell width and the row is centred.
- **A trimmed sim is where an untested constant shows up.** Mutating the ideal angle AX₂E₂ is
  compared against (the tetrahedral angle → 120°) survived Basics' sweep and was caught in the full
  sim only through a layout failure in the squeeze view, which Basics does not carry. Both suites
  now pin each named angle's ideal to the angle its two slots actually make — the shared engine got
  a better test because the trimmed variant could not hide behind a drawing.
- **The same sweep found the button-repaint gap in both sims:** dropping `refresh()` from the panel
  buttons survived, because the adding buttons start the relaxation and the loop repaints anyway.
  `reset view` starts nothing; both drives now click it from a proven-idle baseline.

### Known-bad candidates
- **A variant is not a copy.** Basics shares nine part files with `molecule-shapes` and copies them
  at build time with a byte-for-byte check; editing them in the Basics directory is silently undone
  by the next build. Edit them in `build/molecule-shapes/` and rebuild both.
- **A trimmed sim still ships the engine's untrimmed tests, and that is deliberate.** The Basics
  suite still exercises lone-pair classes through the shared engine (they are reachable in code,
  not through its UI), which is what keeps the two sims' physics identical. A mutant in lone-pair
  code is therefore caught by both sweeps; a mutant in a control Basics does not build (its ρ
  slider) can only survive, and is excluded from its mutant list rather than left to look like a
  finding.
