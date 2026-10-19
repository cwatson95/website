## 2026-09-21 — magnets-and-electromagnets: a bar magnet and an electromagnet, their exact fields, in six views

Remake of PhET's Magnets and Electromagnets 1.0.7
(`docs/phets/magnets-and-electromagnets_en.html`, screens from the shared
FARADAYS_ELECTROMAGNETIC_LAB repo) as `magnets-and-electromagnets.html`, in
the house form: the scaffold, palette, `h()`, 2-D layer and view helpers
extracted from `projects/simulations/build_buoy` by `family.py`, which asserts
every function it carries and rewrites only the title, header comment,
accents, `<h1>`, tagline and site-nav hrefs. New code; no PhET code or assets.

This is the FAMILY's home build dir: one engine (`e1_core.js` … `e5_gen.js`),
one set of drawing primitives (`v_common.js`, `v_screens.js`, `v_analysis.js`),
one Python twin (`derive.py`) and one mutant list, from which `family.py` also
cuts `magnet-and-compass.html` and `generator.html`. Each page carries only
what it uses: five feature markers (`#bar`, `#coil`, `#emag`, `#far`, `#gen`)
are stripped at build time, and the build then asserts that no symbol of a
stripped feature is left anywhere in the page.

### Added
- **the bar magnet** — PhET's screen: drag and flip the magnet, set its
  strength (0–300 G, 75 % at start); the field as PhET's 40-mm needle grid with
  its 2(|B|/300 G)^(1/2.7) brightness rule; a compass (a damped rotor, so it
  swings and settles); the field meter reading B, Bx, By and θ in gauss or
  tesla with PhET's own formats ("~ 0 G" below 0.01 G, scientific tesla); see
  inside; the Earth. **the electromagnet** — a coil of 1–4 loops driven by a DC
  battery (±10 V) or an AC supply (0–110 V, 0–1.25 Hz), electrons whose speed
  shows the current, the same field display, compass and meter. **field lines**
  — exact lines of B in the page, seeded at equal flux, with the magnet's bound
  surface current. **on the axis** — B and μ₀H along the axis in closed form
  against the point dipole; for the coil, the loop sum against the continuous
  sheet of the same ampere-turns. **the far field** — |B| on the axis and the
  bisector on log axes against the dipole, and the approach to it as the
  octupole C/r². **the needle** — the compass as a damped rotor, its period
  against |B| (Gauss's method), with an energy ledger.
- What is exact: the magnet is a uniformly magnetised cylinder (PhET's
  250 × 50 bar), so its B field is exactly that of an ideal finite solenoid
  carrying the bound current K = M × n̂ — Derby & Olbert's closed form (Am. J.
  Phys. 78, 229 (2010)) through Bulirsch's generalized complete elliptic
  integral, in 3-D, everywhere. The coil is N thin loops by Biot–Savart, exact
  on and off the axis. Field lines are RK4 along B/|B| with the magnet's side
  wall crossed exactly (secant landing) and, for the coil, a Newton projection
  onto its closed-form flux function; they close to ~2e-5 mm (magnet) and
  1.5e-4 mm (coil). The far-field limits are taken NUMERICALLY (Richardson at
  2, 4, 8 m) and come out 1 to ~4e-9; the approach matches the octupole
  coefficients 2(b² − 3R²/4) and 6⟨x²⟩ − 3a²/2 in closed form. One measured
  number: μ₀ = 1.25663706127e-6 N/A² (CODATA 2022, NIST).
- **PhET's precomputed grid is a sampling of this same field.** `derive.py`
  reads all 15,971 grid points out of the 1.0.7 build and compares: median
  2.2e-7 G per G of strength, 97.9 % within 1e-4, worst 4.6e-3 beside the
  pole-face rim where the exact field has its logarithmic edge singularity.
  Said on the page, and asserted point by point in selfTest.
- Verification: `derive.py` → `refvals.txt` (scipy dblquad over the current
  sheet, quad, ellipkm1, brentq, solve_ivp; 198 reference lines), emitted into
  the page as literals by `family.py` — never retyped; selfTest 1150
  assertions including a 17-configuration × 5-size layout sweep; UI drive 228;
  mutation sweep 89 of 89 caught (70 physics, 19 UI); display-list audit 0
  problems over 19 captures at 1400 x 820 and again at 820 x 560; every PNG looked at; `_tools/verify_one.py` OK.

### Fixed (during the build)
- **Field lines stalled on the axis at z = −125.10 mm.** Symptom: one line of
  ten never closed. Root cause: the side-wall correction (B_u jumps by μ₀M
  across the bound-current sheet) was applied on the END faces too, where there
  is no sheet, because the test only looked at ρ; the line then followed a
  field that does not exist. Fixed by applying it only when both ends of the
  step lie within |z| < b on opposite sides of ρ = a, with a secant landing on
  the wall and a nudge across it.
- **Coil lines closed to 1.2e-2 mm, not to rounding.** Root cause: RK4 alone
  accumulates. The coil has a closed-form flux function, so every vertex is now
  pulled back onto its own level set by Newton along ∇Ψ; closure fell to
  1.5e-4 mm. (The magnet's Ψ needs a quadrature, so its lines still rely on
  RK4 — stated in the page's comment.)
- **The loop field was 11 % wrong at ρ = 1e-6 a.** Root cause: the textbook
  K, E form of the off-axis loop field subtracts two nearly equal terms. Both
  B_ρ and Ψ are now the cancellation-free `cel` forms.
- **The electromagnet read as a copper blob with the electrons in a lattice.**
  Fixed by drawing all the turns' dark rims in one pass and their copper in a
  second, reducing the perspective tilt 0.36 → 0.28, and staggering the
  electron phases turn by turn.
- **The magnet painted over its own field lines** in the lines view: the body
  now goes down first, translucent.
- **Mixed tick decimals, two x labels in the far view, and raw logarithms when
  the field was zero.** Root causes: `fmt(t,2)` regardless of the tick spacing;
  `ticksFor` given the full width on a log axis; and the zero case returning
  before the second frame was drawn. Fixed with `tickFmt` (decimals from the
  spacing), `logTicksFine` and an empty-case path that keeps both frames.
- **Two captions described what their own checkboxes had switched off** (found
  by looking at `view_lines_no_bound.png`): the field-lines caption named the
  bound current's dots and crosses when they were hidden, and the axis caption
  — and its plot title — explained μ₀H when it was not drawn. Both follow their
  boxes now, in the full caption and the short one, and a shared test reads the
  text that actually reaches the canvas. Root cause for the axis one: the
  caption was a top-level `const`, built once at load, so it could not follow
  anything; it is a function now.
- **Four mutants survived the first sweep** — the AC full scale, the AC
  frequency, the pendulum period and the "~ 0 G" threshold — because the tests
  recomputed the same constants they were checking. All four are now pinned to
  `derive.py`'s printed values. **Four more survived the second**: a
  centre-grab that hid both a lost drag offset and a shrunken hit box (the
  magnet is now grabbed by its north END), a repaint masked by the compass's
  own motion (the compass is switched off for that test), a provably dead
  `rest=false` (removed, and its mutant replaced by one on the rest criterion),
  and a readout that did not change when the magnet moved with the tools hidden
  (the readout now carries the magnet's position — a page fix, not a test fix).

### Known-bad candidates
- **A feature marker that spans more than its feature.** Marking `projectPsi`
  as coil-only wrapped the block from its comment to the next function, which
  swallowed a nested `#endcoil` and left an orphaned `return` in the stripped
  page (`SyntaxError: Return statements are only valid inside functions`).
  Same-feature markers must not nest, and a block must end at its own
  function's closing brace.
- **A registry entry is safer than a ternary** when code is cut at build time:
  `A.kind==='magnet'?x:y` cannot be stripped in half, so per-source values
  (the axis curve, the view's title) live on `ANA_SRC` instead.
- **A mutant on a quantity that is provably zero is equivalent.** The Fourier
  sine terms and the k = 0 normalisation in the generator, and any drag-offset
  test that grabs an object by its centre: pin the consequence, or replace the
  mutant.
- The `og-pyfiles` rule of this repo applies here too: `derive.py` is the
  authority, and every JS constant that matters is emitted from it rather than
  typed into the page.
