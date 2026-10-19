## 2026-09-18 — coulombs-law: both of PhET's scales on the gravity lab's engine, the 14-mm closest distance reproduced from PhET's own rounding, the charge product, and electricity against gravity
### Added
- `coulombs-law.html` (128 KB), a remake of PhET's Coulomb's Law 1.0.32 in five views: *macro scale*,
  *atomic scale*, *the inverse square*, *the charge product*, *electricity and gravity*. Credit line
  in the header and on the page; site nav absolute; no network. It runs on the inverse-square engine
  built for `gravity-force-lab.html` (`build/gravity-force-lab/p2_engine.js`, `p4_lab.js`, the
  drawing and test kits), which its assembler reads from there, so the two files cannot drift.
- *Macro scale* and *atomic scale* are PhET's two screens, each with its own state as in PhET:
  charges −10..10 µC or −10..10 e in whole units, dragged along a 1-mm or 1-pm grid on a ±5 cm or
  ±50 pm track (or set by slider), arrows together for unlike charges and apart for like ones,
  "Force Values" and "Scientific Notation" (greyed out while the values are hidden, as PhET does),
  PhET's readouts (3 decimals macro, 9 atomic, a two-decimal mantissa in scientific), a draggable
  ruler per screen (10 cm, 100 pm), the "1 cm" and "10 pm" scale bars and PhET's picometre note.
  Defaults are PhET's: −4 µC at −1 cm and +8 µC at +2 cm (decimal); −2e at −20 pm and +4e at +20 pm
  (scientific). House additions: a per-screen arrow-scale ladder, the distance line, the
  acceleration the atomic pull would give a proton (6.90 × 10²⁰ m/s²).
- *The inverse square* (either scale): |F| against r on log–log axes (slope −2.0000 measured off the
  model), linear axes, and |F| r² flat at |k q₁q₂|; a zero charge draws a sentence saying there is
  no line, not a log of zero.
- *The charge product*: the (q₁, q₂) plane with attract and repel quadrants and |F| hyperbolas, the
  force on q₂ as q₂ changes sign (and q₁'s mirror), and the force against the product q₁q₂.
- *Electricity and gravity* (analysis): an electron and a proton from 1 fm to 1 m, the two
  inverse-square lines parallel and 2.269 × 10³⁹ apart at every distance, the Bohr radius
  (8.24 × 10⁻⁸ N against 3.63 × 10⁻⁴⁷ N), the ratio for e–e, e–p, p–p, and the macro screen turned
  round: two 65.6-tonne masses would pull as hard as −4 and +8 µC, at any distance, a density of
  5.1 × 10¹⁰ kg/m³ in PhET's 1.35-cm spheres.
- **Exact:** k = 1/(4πε₀) from ε₀ = 8.8541878188e-12 (CODATA 2022), k = 8987551786.170797;
  e = 1.602176634e-19 (exact); G, m_e, m_p and the Bohr radius (CODATA 2022), all through
  scipy.constants 1.18. PhET's own rounding is reproduced and pinned: 6.75 + 6.75 + 1 mm sums to
  14.4999… mm in floating point and snaps DOWN, so PhET's closest centres are 14 mm apart with a
  0.5-mm gap. Every value is pinned in selfTest to `build/coulombs-law/refvals.txt`, printed by
  `derive.py`, read in full.
- **Verification:** selfTest 798 passed, 0 failed under osascript (with a 26-configuration × 4-size
  layout sweep); UI drive 152 passed, 0 failed (charges and rulers dragged on both screens through
  the frame loop from a proven-idle baseline; the screens' states independent; the greyed-out
  checkbox inert; the analysis views ignoring the pointer where a charge sits; reset all restoring
  both screens); mutation sweep 61 caught of 62 (49 physics, 13 UI), run on a copy in
  `build/coulombs-law/_out/`, the one survivor proven equivalent below; display-list audit
  0 problems over 16 captures; every PNG looked at.
- **Where this differs from PhET, deliberately:** k and e are CODATA 2022 (PhET's k = 8.987551e9 and
  e = 1.6021766208e-19 differ by 9e-8 and 8e-9; the readout prints PhET's number too). Arrows are
  proportional at a printed scale. No pullers or pushers, sounds or screen-reader descriptions.
### Fixed (during the build)
- **A charge's sign was typeset,** so it was a text label the ruler's "0" collided with whenever the
  ruler lay across the charge. Signs are stroked symbols now (and first drawn 7 px thick, which read
  as blocks; now at most 3.2 px).
- **Symmetric plots labelled the same corner twice:** "−10" on both axes of the charge plane, 10⁻¹⁵
  against 10⁻⁷⁰ on the gravity plot, "−1" against "−10" in a lower panel. The y numbers keep 14 px
  clear of the bottom corner.
- **A zero charge would have sent log10(0) = −∞ into the inverse-square view's axis range.** The view
  says there is no force to plot, and so does the charge product's lower-left panel.
- **Readout formatting:** the proton acceleration went through `sigf` and printed "6.90×10^+20";
  the macro gap printed "0.0500 cm" and now reads "0.50 mm".
- **A prose claim from memory** ("Coulomb's data supported the exponent 2 to a few percent") could
  not be sourced here and was made qualitative.
- **The sweep's one real survivor, "the sphere hit radius shrinks to a fifth":** every pointer test
  pressed a charge dead-centre, where the radius cannot matter. The charges are now also grabbed
  0.6 of a radius off centre, and a press 2 px outside the hit radius must miss.
- **Two substance floors were copied, not derived:** a 4-px atomic charge at 560 px has no
  highlight and a tick for an arrow (4 fills), and the honest zero-charge view is one fill and a
  sentence.
### Known-bad candidates
- **With PhET's numbers the surface gap changes nothing on either Coulomb screen.** Without it,
  13.5 mm also rounds (half away from zero) to 14 mm, and 1.9 pm to 2 pm. A "drop the gap" mutant is
  therefore equivalent here; the invariance is asserted as a property, and the mutant is caught in
  `gravity-force-lab.html`, where the gap matters.
- **A symbol drawn with `fillText` is a label to every overlap check.** Stroke signs and glyph-like
  marks.
- **A zero in a quantity plotted on log axes must be refused at the view,** with a sentence, before
  `log10(0)` reaches an axis range.
- **A dead-centre press tests nothing about a hit radius.** Pin it from both sides.
