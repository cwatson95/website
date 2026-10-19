## 2026-09-21 — molecule-shapes: PhET's two screens on an explicit repulsion energy, the AXE table as its global minima, and the one measured angle it gets backwards
### Added
- `molecule-shapes.html` (213 KB), a remake of PhET's Molecule Shapes 1.6.19 in five views: *the
  model*, *real molecules*, *the AXE table*, *the squeeze* and *the relaxation*. The credit line is
  in the header and on the page, the site nav is absolute, nothing touches the network.
- *The model* is PhET's Model screen: add single, double and triple bonds and lone pairs round the
  central atom (six pairs at most, PhET's `maxConnections`), remove the last of a kind or all of
  them, drag any pair round the atom and let it slide back, turn the molecule, wheel to zoom;
  Show Lone Pairs, Show Bond Angles, and the molecule-geometry and electron-geometry names, in
  PhET's wording. It opens on PhET's own two single bonds along (8, 0, 3) and (2, 8, −5).
- *Real molecules* is PhET's second screen: its thirteen molecules with their measured geometry,
  the Real / Model switch (animated between the two), Show Outer Lone Pairs, the same options and
  names. Every angle and length shown is computed from PhET's stored numbers.
- THE MODEL. Every electron pair is a point on a sphere — a bond on the unit sphere, a lone pair on
  one of radius ρ (PhET's value 0.7: its lone pairs sit at 7 against 10 for its bonds) — and every
  pair repels every other with energy 1/d², d the 3-D separation. The shape drawn is the
  arrangement of least total energy. Single, double and triple bonds act alike, as PhET's notes say
  its own do. The ρ slider runs from PhET's 0.7 to 1, where a lone pair is a bond and every angle
  is exactly ideal.
- **No attractor.** PhET's model notes describe a Coulomb-like repulsion *steered* toward ideal
  slots, because plain Coulomb repulsion has locally-stable arrangements that are not the VSEPR
  one. `derive.py` audits this file's law instead: for every lone-pair class and every ρ from 0.60
  to 1.00 it relaxes every assignment of the pairs to the slots plus sixteen random starts, checks
  the shape and takes the Hessian. The VSEPR arrangement (lone pairs equatorial in the bipyramid,
  trans in the octahedron) is the global minimum, keeps its shape and is a true local minimum for
  **ρ ≥ 0.64** — the slider starts at 0.70, with room to spare. The same audit rejects the
  alternatives: with Coulomb's 1/d at ρ = 0.7, ClF₃ comes out trigonal planar (7.36173 against the
  T-shape's 7.36450), and charge-weighted lone pairs on one sphere make XeF₄ *cis* at every
  exponent tried (1, 2 and 6).
- WHAT IS EXACT. The ideal geometries (linear 180°, trigonal planar 120°, tetrahedral
  arccos(−1/3) = 109.4712206…°, bipyramidal 90/120/180, octahedral 90/180) and the equal-pair
  energies 1/4, 1, 9/4, 17/4, 27/4; plain descent from seeded random starts reaches each of them to
  1e-9° and the closed-form energy to 1e-12. Every class at ρ = 0.70, 0.85 and 1.00 is pinned to
  the Python twin (angles to 1e-8°, energies to 1e-11), which is itself checked against scipy's
  BFGS. Horn's quaternion fit is checked against scipy's `Rotation.align_vectors` (1e-12 on a
  known rotation, 1e-10 on a noisy one). The lone-pair directions asserted: AX₂E below 120°, AX₂E₂
  and AX₃E below 109.47°, the seesaw's axial pair below 180°, the T-shape's and the square
  pyramid's arms below 90°, while AX₂E₃, AX₄E₂ and AX₂E₄ stay exactly 180°, 90°, 180° by symmetry.
  The departure from ideal is linear in 1 − ρ (ratios 1.96–2.00 between ρ = 0.98 and 0.99).
- WHERE IT FAILS, ON THE CANVAS. Of the seven measured lone-pair angles in PhET's table the model
  bends six the right way and **SF₄'s equatorial F–S–F the wrong way**: point pairs open it to
  121.2° where the molecule closes it to 101.6°. *The squeeze* view plots all seven against ρ and
  says so in words; three (H₂O 104.5°, ClF₃ 87.5°, BrF₅ 84.8°) need more squeeze than ρ = 0.70
  gives, and three are matched at a fitted ρ (SO₂ 0.954, NH₃ 0.833, SF₄'s axial pair 0.792, each
  found by bisection on the relaxation itself and pinned against `brentq`).
- *The AXE table* draws all fifteen classes of steric number 2 to 6 relaxed at the current ρ, each
  turned lone-pairs-up; clicking one builds it in the model view. *The relaxation* runs plain
  gradient descent from a seeded random start with no steering, and plots how far the energy stands
  above the VSEPR minimum against the other arrangements' energies: it is where PhET's warning about
  locally-stable configurations becomes visible, and `derive.py` counts how often it bites — 65 of
  100 random AX₄E₂ starts stall with the lone pairs cis, 66 of 100 AX₂E₄ starts end bent, while
  every one of 100 starts of five or six equal pairs reaches the ideal shape.
- PhET's data, verbatim: the thirteen molecules' bond angles as the numbers its constructor is
  given (104.5° for H₂O, 119° for SO₂, 87.5° for ClF₃, 84.8° for BrF₅, 173.1° and 101.6° for SF₄,
  NH₃'s polar angle 1.202623030417028 rad = 107.8°, the tetrahedron's elevation −19.471220333°,
  which leaves CH₄ at 109.47122033° and 109.47122094°, not quite ideal), the bond lengths in
  ångström, the lone-pair counts, the bond orders, the 7-to-10 lone-pair radius, six pairs at most,
  the lone-pair slot order, the arc-brightness thresholds and all 22 AXE names.
- Verification: `selfTest` 1937 assertions green under osascript; the UI drive 170; 61 mutants, all
  killed; 23 captured configurations audited (0 layout problems) and every PNG looked at.

### Fixed (during the build)
- **A bond pointing straight at the camera hides behind the central atom, and every class loaded
  from the table did it.** Water's second bond and the seesaw's equatorial bond were invisible at
  the default camera: `liveLoad` dropped a class in the raw slot frame, whose axes happen to line
  up with the default line of sight. Root cause: the same one the Known-bad list records for
  `bloch_sphere` — a default camera pointed along the thing the view exists to show. `displayFrame`
  now puts the lone pairs up and then picks, from 72 turns about the vertical, the one that keeps
  *every* pair furthest from the default line of sight; the reference is the default camera, not
  the current one, so the shapes do not re-orient while being turned. `selfTest` asserts no pair of
  any class comes within 72° of that line.
- **`acos` is ill-conditioned at 0° and 180°: one ulp of the dot product is 1.2e-6°.** Two pins
  failed at exactly that value (a two-pair random start and BrF₅'s lone pair, both 180° angles).
  Both the JS and the Python twin now take angles as `atan2(|a×b|, a·b)`, which is accurate
  everywhere; the pins hold at 1e-8°.
- **A display merge tolerance swallowed CH₄'s two distinct angles.** PhET's rounded tetrahedral
  elevation leaves CH₄ with 109.47122033° and 109.47122094°, 6e-7° apart; `distinctAngles` merged
  anything within 1e-6° and the test compared 1 value against the twin's 2. The tolerance is now a
  parameter: 1e-6° for the readout, 1e-10° for the pins.
- **Two panels do not fit a 560×380 stage, and the lower axis ran into the caption.** The squeeze
  view now reserves 44 px below the lower panel and falls back to its one primary panel (the
  curves) with its own caption when the stage is short — the Known-bad remedy for collapsing
  two-column layouts. Its curve labels moved into a column clear of the tick labels, and the
  rotated y-axis title came off that panel.
- **`dirty = true` before `refresh()` was dead code in eight handlers.** Mutation testing killed a
  mutant that removed it from the tab click and nothing else changed: `refresh()` draws
  unconditionally. The flag now survives only where it is load-bearing — the pointer and the wheel,
  which do not refresh — and the UI drive pumps the pointer-down and the pointer-move through
  separate frames, because pointer-up calls `refresh()` and masked the move's flag.
- **A button whose action starts no motion must repaint on its own, and only one does.** The
  sweep's last survivor dropped `refresh()` from every panel button and lived: the adding buttons
  set the flow going, so the loop redrew anyway. `reset view` does not, and its click was
  therefore invisible until the next interaction. The drive now clicks it from a proven-idle
  baseline after turning the camera and asserts ops came out of the click itself.
- **The ideal angle each class is compared against was data no test pinned.** Mutating AX₂E₂'s
  ideal from the tetrahedral angle to 120° survived the Basics sweep outright (only the full sim's
  squeeze view draws it, and there it showed up as a layout failure rather than a wrong number).
  Both suites now assert that each named angle's ideal IS the angle its two slots make.
- **Five more test gaps the sweep found, each closed:** a display-frame assertion that took a minimum
  where it meant a maximum (vacuous); the isomer ladder's *length* unpinned, which matters only at
  ρ = 0.99 where the gaps fall to 1e-4 (AX₃E₂ and AX₂E₃ have three distinct minima there and two at
  0.70 — pinned per ρ now); PhET's bond orders and outer-lone-pair counts unpinned as data, and a
  double bond's two sticks unpinned in the drawing; the ρ a drag sets probed only at values that
  are already on the slider's 0.01 step; and the display flow's repulsion term, now pinned by the
  property it actually has (it changes the path the pairs take by more than a degree, and not where
  they end).
- The camera fitter used the near-point approximation `fR/(D − R)`, which frames a ball at 0.82 of
  the size it claims (Known-bad, `polyhedra`); it is the exact tangent cone `fR/√(D² − R²)`, and
  the claimed fraction is asserted.

### Known-bad candidates
- **A points-on-a-sphere model of VSEPR gets SF₄'s equatorial angle backwards, whatever the law.**
  Charge weights (exponents 1, 3 and 6) and lone-pair radii (exponents 0.5 to 4, ρ 0.6 to 0.9) were
  all tried in the build: every one of them opens the seesaw's equatorial F–S–F past 120° where the
  molecule closes it to 101.6°. The equatorial lone pair pushes the two axial bonds (90° away) much
  harder than the two equatorial ones (120° away); the axial bonds bend toward the equatorial pair
  and lever it open. Do not "fix" it by tuning ρ — say it on the canvas, which this file does.
- **Coulomb's 1/d is the wrong exponent for a two-sphere VSEPR model, and the failure is a shape,
  not an error term.** At PhET's ρ = 0.7 a 1/d law makes ClF₃ trigonal planar (the lone pairs go
  axial); 1/d² ranks every class correctly for ρ ≥ 0.64. Any change to the exponent or to the ρ
  range must re-run `derive.py`'s audit, which is what pins the claim.
- **Product charge weights cannot separate cis from trans.** With w_L = q on one sphere, the
  unrelaxed cis–trans gap of AX₄E₂ is (f(90°) − f(180°))(q − 1)² — second order in q − 1, and the
  cis arrangement's relaxation gain beats it at every exponent tried. If lone pairs are ever
  modelled as stronger charges rather than closer ones, XeF₄ will come out cis.
- **A relaxation from a random start is not a model of VSEPR.** Plain descent stalls in a higher
  local minimum for most AX₄E₂ and AX₂E₄ starts. The model view avoids it by starting from the
  VSEPR slots and steering; the relaxation view exists to show the trap rather than hide it.
