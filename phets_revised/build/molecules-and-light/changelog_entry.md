## 2026-09-22 — molecules-and-light: PhET's photon-and-molecule chamber, its response table beside the real spectroscopy, and the normal modes derived from symmetry and mass

### Added

- `docs/phets_revised/molecules-and-light.html` (241 KB, six views:
  *the chamber*, *the spectrum*, *what responds*, *the normal modes*,
  *the statistics*, *the atmosphere*), a clean-room
  remake of PhET Interactive Simulations' **Molecules and Light** (build 1.5.33,
  CC-BY 4.0). No PhET code or assets; PhET's own PNG photon sprites are replaced
  by four house accents, and every number marked "PhET's value" is read out of
  the minified build in `docs/phets/molecules-and-light_en.html` or out of its
  `doc/model.md`.
- **the chamber** — PhET's single screen, rule for rule. The light source at
  x = −1350 firing photons at 3000 model units/s; the 100-unit absorption
  radius; **exactly one** absorption trial per photon at p = ½ (PhET's
  pass-through list makes the first failed trial final, so four frames inside
  the radius still buy one coin flip); a hold time uniform on 1.1–1.3 s; a
  re-emission in a direction uniform on the circle; a 0.2 s refusal window
  afterwards; 5 Hz vibration, 1.1 Hz rotation, the 0.8 s emission period, the
  half-rate slow motion, the 0.2 s frame ceiling and the break-apart speeds 990
  and 0.67 × 3000. The strip under the chamber is the molecule's state against
  time, recorded by the simulation rather than by the drawing.
- **the spectrum** — PhET's Light Spectrum Diagram with the seven band edges its
  own accessibility text states, its four source wavelengths marked with their
  exact energies, and two zooms carrying every measured transition of these nine
  molecules on the same logarithmic axis.
- **what responds** — PhET's 8 × 4 response table, read straight out of its
  `setPhotonAbsorptionStrategy` calls, beside the real answer computed here.
- **the normal modes** — the vibrations, diagonalised from a valence force field
  fitted to the measured wavenumbers, animated at their true displacement ratios,
  with the exact symmetry statements checked against the eigenvectors beside them.
- **the statistics** — PhET's three random rules measured over a seeded
  generator against the standard error each is entitled to, with a deliberately
  biased generator shown being rejected by the same test.
- **the atmosphere** — Earth at 288 K per unit wavenumber, the measured
  IR-active fundamentals drawn on it, the 8–13 µm window, and the composition
  bar that shows 99.966 % of dry air absorbing nothing.
- `build/molecules-and-light/derive.py`, the Python twin: 199 reference values,
  every one of them asserted in `selfTest`. `gen_ref.py` turns its `refvals.json`
  into `p7a_ref.js` and `p2b_fields.js`, so no reference number is hand-typed.
- Verification: `selfTest` 749/0 and the UI drive 310/0 under `osascript`
  (0.5 s and 1 s); `tools/audit.py` clean on 19 captured configurations;
  99 mutants in `mutants.json`, every pattern checked to match exactly once
  by `gen_mutants.py`.

### What is exact

- **Photon energies.** The 2019 SI fixes h, c and e by definition, so
  hc = 1.986445857148929e-25 J m and hc/e = 1239.841984332002 eV nm are exact
  rational numbers. Every energy, frequency and wavenumber the file prints is
  that identity, computed two ways and asserted to agree at 1e-14.
- **The mode shapes symmetry alone fixes.** For a linear symmetric XY₂ the
  symmetric stretch is (1, 0, −1) with the central atom *exactly* at rest
  (3.8e-16 here) and the antisymmetric stretch and the bend are both
  (1, −2m_Y/m_X, 1); for a bent XY₂ the B₂ antisymmetric stretch has
  v/u = cot(θ/2) from zero linear and zero angular momentum. None of the four
  depends on a force constant or on a bond length. The JS re-diagonalises the
  Hessian with its own Jacobi solver and reproduces all of them to 7e-15.
- **The infrared selection rule, two independent ways.** Rigid point charges
  give |∂μ/∂Q| = 0 to 4e-15 for all six inactive modes — and the zero survives
  rescaling every charge by 2.7, so it is the mode shape and not the charge.
  The inversion character decides the same six centrosymmetric modes with no
  numbers at all, and the two agree on every one.
- **PhET's two columns ARE the two selection rules.** Its microwave column is
  exactly the four molecules with a permanent dipole (CO, H₂O, NO₂, O₃) and its
  infrared column is exactly the six with an IR-active fundamental (all but N₂
  and O₂). Both are asserted as properties, not spot-checked.
- **The CO J = 1 ← 0 line, derived rather than quoted.** B_e from the measured
  r_e and the reduced mass reproduces the tabulated constant to 3.5e-7, and
  2B₀ lands at 115.2719 GHz against the 115.2712018 GHz radio astronomers use —
  6e-6 out, in the direction and of the size centrifugal distortion demands.
- **The stochastic layer.** The generator is a 32-bit mulberry32 and the Python
  twin reproduces every draw bit for bit, so the 60-second and 600-second
  chamber runs are pinned photon for photon (76/28/47/28 and 751/256/494/255)
  rather than statistically.

### What is modelled, and what is not

- The A₁ pair of a bent triatomic mixes, and the mixing angle needs a force
  field. Three measured wavenumbers do not determine the four symmetry constants
  of a bent XY₂, so the fit returns the solution of **smallest stretch–bend
  interaction** that still reproduces all three exactly — a stated choice, and
  the reason those two shapes are labelled MODEL on the canvas. Ozone needs
  f_rθ = 0.087 aJ/Å²; water and NO₂ come out at zero.
- Line strengths, line shapes, rotational fine structure, overtones, Fermi
  resonance (CO₂'s ν₁ is quoted as its deperturbed 1333 cm⁻¹), excited-state
  photolysis products, collisions and quenching are not modelled. The atmosphere
  view marks band POSITIONS and never strengths, and says so.
- Bond dissociation energies are QUOTED (Active Thermochemical Tables) and were
  not re-derived; the canvas and the credit line both say so.

### Fixed (during the build)

- **The NIST WebBook prints O₂'s rotational constant in square brackets, and in
  Huber & Herzberg that means B₀, not B_e.** Taking the fetched `Be = 1.4376766`
  at face value disagreed with the same row's `re = 1.20752` by 0.55 %, which is
  what caught it; B_e computed from r_e minus α_e/2 reproduces the bracketed
  number to 1.1e-5, a factor of 504 better, which is what settled it. CO and N₂
  are unbracketed and agree as B_e to 3.5e-7 and 5.0e-7. The file now asserts
  the RATIO both ways, so the bracket convention is pinned rather than assumed.
- **A finite-difference Hessian is only translationally and rotationally
  invariant to O(h²), and the residual leaks into the eigenvectors.** Water's
  modes carried 2.2e-8 of spurious centre-of-mass drift and 1.3e-8 of spin. An
  acoustic-sum-rule patch on the diagonal blocks fixed the translations and
  broke the symmetry (the two row sums S_i^{αβ} and S_i^{βα} differ, so
  re-symmetrising undoes it); the Eckart projection P H P with P = I − ΣBBᵀ
  fixes both at once and takes every residual to 1e-14.
- **A linear molecule's bend cannot be written as (π − θ)².** `arccos` has
  infinite gradient at θ = π, so a Cartesian finite difference of it is
  garbage. Writing the bend energy as f_θ r² (1 + cos θ) — identically the same
  harmonic form to leading order — is smooth in the Cartesians and gives CO₂'s
  667 cm⁻¹ to 5e-15.
- **`&micro;` is not in the shared entity table**, so three captions drew
  `&micro;m` verbatim on the canvas. `&ldquo;`/`&rdquo;` were missing too. Both
  added in `make_head.py`, so a regeneration keeps them.
- **`stageLayout` floors its main box at 80 px, and on a short stage that floor
  pushes the main panel straight over the bottom row.** At 560 × 380 the
  atmosphere view's axis title and the composition panel's summary overlapped,
  and the normal-modes view drew its molecule below its own box and over the
  footnote. A `stage()` wrapper now re-lays the stage with NO bottom row when
  the floor bites: one honest panel beats two overlapping ones.
- **The house `#hint` sits on the last line of a bottom-anchored caption.**
  Every view passes `H − HINT_H` (18 px) to `stageLayout`, as
  `build/wave-on-a-string` and `build/molecule-polarity` do.
- **The O₃ fragments' atom labels flew off the canvas.** After dissociation the
  pieces leave the observation window and were still being drawn at −1023 px.
  A fragment outside the window is now dropped, and the view *says* the pieces
  have left rather than going quietly blank.
- **`legendAuto` avoids curves, and the zoom panels draw their transitions with
  raw strokes**, so `POLY_SEGS` was empty and it thought every corner was clear:
  both legends landed on the data. Replaced by one shared legend in the main
  panel's empty middle, drawn only when it fits clear of everything above it.
- **`const DRAG` collides with `p4a_helpers.js`.** The extracted house helper
  block already declares it; a second `const DRAG` is a hard SyntaxError, not a
  subtle bug. Extended the existing object instead.
- **A renewal estimate of the duty cycle is 6 % low, and it is not noise.**
  T/2 + (1/p − 1)T + busy predicts the molecule excited 46.2 % of the time; five
  1200-second runs measure 49.1 % with a spread of 0.021, and the estimate is
  below *every* seed. The source is exactly periodic and the busy time nearly
  deterministic (σ = 0.058 s on 1.4 s), so the phase never decorrelates. The
  file prints both and names the assumption that fails.
- **The eigenvector arrows were buried inside the atoms.** At some phases every
  arrow points inward, and a CPK-radius sphere swallowed it. The spheres are
  drawn at 0.78 of the CPK radius, the arrow starts at the sphere's edge, and
  every arrow is drawn after every sphere.
- **Eight defects the mutation sweep found, every one a masked assertion.**
  (1) `pointerdown` sets the dirty flag too, so a drag fired in one go could
  not test whether the MOVE handler sets it -- the pumped frame repainted
  either way, and the mutant that deletes it survived. The drag now presses,
  drains to idle, proves it, and only then moves. (2) `reset all` restored the
  camera twice -- `Object.assign(st, DEFAULTS)` already carries `camTheta`,
  `camPhi` and `zoom` -- so a mutant on either path was equivalent; the
  redundant `S.resetCam()` is gone and `resetCam` is pinned where it is the
  only path. (3) "the molecule chip rewinds the mode index" was vacuous
  because the index was already 0; a sentinel of 5 is set first. (4) The
  re-emitted photon was created with `pass: true` AND the molecule set a 0.2 s
  hysteresis -- two guards on one path, so deleting the hysteresis changed
  nothing. PhET emits an ordinary photon and relies on the hysteresis alone;
  this file now does the same, and the mutant is caught. (5) `nubarToUm` was
  printed by the readout and the canvas and asserted by nothing; it is now
  round-tripped through `photonOf`, which reaches a wavenumber by a different
  route. (6) Only the `'asym'` branch of `linearExact` was ever evaluated, so
  the symmetric-stretch and bend branches could be mutated freely; all three
  are now checked against the eigenvectors. (7) The emission direction was
  measured through `ensembleDirection`, a different code path from the
  chamber's own emission, so the chamber's `rng() * 2 * Math.PI` was untested;
  400 seeded re-emissions are now measured directly. (8) The Jacobi rotation
  ANGLE is an equivalent mutant -- halving it fails to annihilate A[p][q] in
  one rotation but the cyclic sweep still converges to the same
  eigen-decomposition -- so it was replaced by the sweep cap and the
  convergence test, which are the load-bearing parts. (9) CO2's measured bond
  length survived, correctly: with the force field fitted in the coordinates
  r*dtheta and |r| - r_e, the bond LENGTH cancels out of every wavenumber and
  every mode shape, so no amount of spectroscopy can see it. Every measured
  geometry now has an absolute pin, and the invariance is asserted
  deliberately (to 5e-8, the residual being the fixed finite-difference step
  against a rescaled geometry) rather than left as a blind spot.
- **The house z-up camera cannot look down z** (`right = cross(fwd, [0,0,1])` is
  degenerate at φ = π/2), so a planar molecule built in the x–y plane was always
  seen edge-on-ish. The molecules are mapped onto the world x–z plane instead,
  where φ ≈ 0 looks straight at them and a drag still orbits normally.

### Known-bad candidates

- **A rotational constant in SQUARE BRACKETS in Huber & Herzberg (and in the
  NIST WebBook that reproduces them) is the value for the stated vibrational
  level, not the equilibrium one.** Reading O₂'s `[1.4376766]` as B_e is wrong
  by 0.55 %; it is B₀. The tell is that the same row's r_e disagrees with it,
  and the test that settles it is the RATIO of the two readings' residuals
  (504× here), not an absolute tolerance — r_e is printed to six figures, which
  alone accounts for 4e-6 of the 1.1e-5 that remains.
- **A finite-difference Hessian needs an Eckart projection, and the obvious
  acoustic-sum-rule fix breaks the symmetry it is applied to.** Setting
  H[3i+α,3i+β] = −Σ_j H[3i+α,3j+β] satisfies the row sums but makes the
  diagonal block non-symmetric, and re-symmetrising undoes the sum rule.
  Project instead: P = I − Σ B Bᵀ over the mass-weighted rigid motions, then
  P H P. Both residuals go to machine precision in one step.
- **`(π − θ)²` is not a usable bend coordinate for a linear molecule.** Use
  2(1 + cos θ), which equals it to leading order and is smooth in the
  Cartesians where `arccos` is not.
- **`&micro;` is NOT in the shared `ENTS` table** (`&mu;` is). A micrometre
  written as an entity reaches the canvas verbatim. So do `&ldquo;`/`&rdquo;`.
- **`stageLayout`'s 80-px floor on the main box silently overlaps the bottom
  row on a short stage.** When `L.main.h <= 82` and there are bottom boxes, lay
  the stage out again with none.
- **A renewal estimate assuming a decorrelated phase is systematically wrong
  against an exactly periodic source with a nearly deterministic busy time.**
  Measure it, sweep the seed to separate sampling spread from the systematic
  gap, and print both.
- **Two guards on one path make each other's mutant equivalent, and a
  re-emitted photon is where it happens here.** PhET's molecule emits an
  ordinary photon AT its own position, inside the absorption radius, and the
  only thing that stops it swallowing it again on the next frame is the 0.2 s
  hysteresis. Marking that photon `pass: true` as well is a second owner of
  the same behaviour and makes the hysteresis untestable.
- **A number that only the readout and the canvas print is covered by
  nothing.** `nubarToUm`'s 1e4 survived a sweep for exactly that reason. Pin
  such a conversion by ROUND-TRIPPING it through an independent route rather
  than restating it.
- **A closed form with a `which` argument needs every branch evaluated.**
  `linearExact(mol, 'sym'|'asym'|'bend')` had two branches no assertion ever
  reached.
- **A bond length CANCELS out of a valence force field fitted in r*dtheta and
  |r| - r_e.** Every wavenumber and every mode shape is invariant to it, so a
  spectroscopy suite cannot see a wrong bond length however many assertions it
  carries. Pin the geometry absolutely and assert the invariance deliberately.
- **A Jacobi rotation angle is not a physical constant.** Any angle that
  reduces the off-diagonal norm converges to the same eigen-decomposition, so
  mutating it is equivalent; mutate the sweep cap and the convergence test
  instead.
- **`p4a_helpers.js` (the extracted house block) already declares `const DRAG`
  as well as `const LABELS`, `CAP_FONT` and the camera.** A sim that declares
  `DRAG` again fails to parse.
