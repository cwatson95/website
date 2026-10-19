## 2026-09-18 — circuit-construction-kit-dc-virtual-lab: PhET's DC bench built by drag, solved by modified nodal analysis with every branch current an unknown, and Kirchhoff, the power budget, Thévenin and superposition laid open
### Added
- `circuit-construction-kit-dc-virtual-lab.html` (254 KB), a remake of PhET's Circuit Construction Kit: DC -
  Virtual Lab 1.5.2 in five views: *the lab*, *nodes and branches*, *the power budget*, *the rest of the
  circuit*, *one battery at a time*. Credit line in the header and on the page; site nav absolute; no network.
- *The lab* is PhET's one screen, with PhET's toolbox read out of its build: wires (50), batteries, light bulbs,
  resistors, switches and fuses (10 each), the extreme battery, bulb and resistor (4 each), a dollar bill, a
  paper clip, a coin, an eraser, a pencil and a thin pencil (1 each), the real bulb behind "add real bulbs",
  a series ammeter (6), a two-probe voltmeter and a non-contact ammeter. Parts come out of the toolbox by drag;
  an end dropped within 30 units of another joins it under PhET's rules (not adjacent, not in the same rigid
  body, no shared neighbour); a wire's end moves freely, a rigid part's end swings it about its other end, a
  joint of rigid parts moves them together; tap to select and edit (a switch toggles), split a joint, delete,
  reverse a battery, repair a fuse, drop a part back on the toolbox. PhET's values throughout: 9-V batteries
  (0–120 V), 1000-V extreme batteries (100–100 000 V), one internal resistance 1e-4–10 Ω, 10-Ω resistors and
  bulbs (0–120 Ω), 1000-Ω extremes, coin and paper clip 0, pencil 25, thin pencil 50, eraser and dollar bill
  1e6 Ω (the 1.5.2 build's values; PhET's model.md says 1e9), fuse 0.06/rating Ω blowing above rating + 1e-6 A,
  0 Ω → 1.1e-10 Ω, wire R = ρ·(5e-4 m per unit)/5e-4 m² with ρ 1e-10–0.0168 Ω m, the real bulb
  R = 10 + 3|V|/log₂(|V| + 2), brightness ln(1 + 0.35P)/ln(1 + 0.35·2000) with the glass lit to 2b, fire at
  15 A through a battery or a resistor-like part of R ≥ 1e-8 Ω, charges 28 units apart at 25 units/s per
  ampere under PhET's speed limit (0.43 of a spacing per 1/30 s: above 14.448 A the animation slows and
  says so in PhET's words), the voltmeter's 11.2-unit solder radius and interpolation along metal, the
  ammeters' 2-decimal magnitudes saturating at 1e10 A (series 1e3 A). Lifelike or IEEE schematic parts,
  electrons or conventional current, labels, values, PhET's three zooms (chips and the wheel).
- *Nodes and branches*: the circuit as the graph the solver sees (every joint a node, every part a branch,
  wires included), its spanning tree against the chords that close the B − N + C fundamental loops, the MNA
  matrix drawn cell by cell in its four blocks (0, A, Aᵀ, −R) with the right-hand side, and both of
  Kirchhoff's laws measured on the answer at every node and round every loop against ε.
- *The power budget*: a waterfall from each EMF's E·i (a charging battery steps down) through each i²R (the
  batteries' own r included) back to exactly zero (Tellegen's theorem, asserted); the bulbs on PhET's
  brightness curve.
- *The rest of the circuit*: any part's Thévenin view — V_th with it removed, R_th with the EMFs zeroed — as
  the load line crossing the part's own law (a real bulb's curve, a battery's line) at the operating point,
  and the power it would take as its resistance is swept, largest at R = R_th (the one-bulb circuit's battery
  would put 202 kW into 100 µΩ).
- *One battery at a time*: superposition as a signed waterfall per part, each battery on its own sub-row,
  landing on the full solution.
- **Exact:** the solver keeps a voltage for every node but one reference per piece and a current for EVERY
  branch, rows = the current law and each part's own law v_a − v_b = R i − E divided by max(1, R); Gaussian
  elimination with partial pivoting and two refinement passes. `derive.py` solves every circuit by a
  different formulation (nodal analysis, batteries as Norton sources) in exact rational arithmetic: the six
  presets and five variants, eleven netlists (series, parallel, Wheatstone balanced to exactly zero and
  unbalanced, the textbook ideal-source formula, two batteries' superposition, Thévenin and the load sweep,
  16 internal-resistance cases, floating pieces, a dead short, PhET's extreme parts, a zero-ohm loop, eight
  decades of resistance) and 30 random circuits over 16 decades; the real bulb in 50-digit Decimal. The JS
  agrees to 16 ε of each piece's current and 64 ε of its voltage everywhere; both of Kirchhoff's laws close
  to 8 ε (measured ≤ 4.0e-16, also on 300 more random circuits from 1e-14 to 1e6 Ω and up to 100 kV).
- **Verification:** selfTest 1386 passed, 0 failed under osascript (with a 32-configuration × 4-size layout
  sweep and a headless pointer build); UI drive 221 passed, 0 failed — the circuit BUILT by dragging a
  battery, a bulb and two wires out of the toolbox and dropping their ends together through the canvas's own
  events and the real frame loop, every repaint asserted from a proven-idle loop; mutation sweep 94 caught of
  95 (81 physics, 14 UI), run on a copy in `build/circuit-construction-kit-dc-virtual-lab/_out/`, the one
  survivor proven equivalent: the SI-prefix boundary `a >= q` → `a > q`, because at an exact power of 1000 the
  lower prefix gives exactly "1000", which the formatter's rounding-promotion step lifts to the same string
  ("1.00 V", "1.00 mA"); display-list audit 0 problems over 31 captures at two sizes; every PNG looked at.
- **Where this differs from PhET, deliberately:** the real bulb is iterated to its fixed point (PhET's ten
  passes stop 1.7e-11 short in the series preset); charges ride each part and wrap at its ends rather than
  hopping junctions; bulbs are 100 units between terminals (PhET's have both on the base); one voltmeter and
  one non-contact ammeter (PhET's lab has two of each); logarithmic resistivity and battery-resistance sliders;
  IEEE schematics only; no stopwatch, keyboard dragging, sounds or descriptions.
### Fixed (during the build)
- **PhET's own formulation loses digits, so the solver was built another way.** Stamping resistors as
  conductances gets a wire's current as 1e8 S × a voltage difference of 1e-8 V: numpy's float solve of the
  conductance form (derive.py) is off by up to 2e-5 of the largest current on the presets and 2e-4 on random
  circuits, and a JS twin of PhET's formulation by 1e-5 and 9e-5 — so the current law it reports holds only
  to that. With every branch current an unknown the current law is a ROW of the system and closes to
  rounding. Both are asserted: the twin agrees to 1e-5, and is ≥ 1000× further from the exact currents on the
  bridge, so the choice cannot be quietly undone.
- **The Kirchhoff residuals read 100 % on a dangling node.** Normalised by a node's own through-current, a
  leaf carrying 1e-30 A is "100 % off"; normalised by the loop's own drops, a loop of 1e-10-Ω parts at 9 V
  cannot close better than 9 V's last bit. Both are now measured against the connected piece's scale (its
  largest current; its largest voltage, EMF or drop).
- **A short nudge onto a neighbouring end did not join.** A release under the 15-px tap threshold was treated
  as a pure tap. PhET's drag listeners do both — any movement tries the drop target, a short one also selects
  — and the UI drive's fuse, 11 px from its target, found it. Split into "dragged at all" and "moved past the
  threshold".
- **The coin was drawn 1.6× too large at zoom 1.6**: its radius multiplied a pixel length by the scale again.
- **Charges ran over the series ammeter's reading**; they are not drawn inside a meter's box now.
- **Bulb icons reached into the toolbox row above** at small cells; icons are scaled to their cell.
- **Schematic tags collided with value labels**, and the lab reset the label registry halfway through its own
  draw; tags now register, and only `drawView` resets.
- **Tick labels like "6.0×10^-5" ran into the rotated axis title**; every axis now speaks SI prefixes
  (µW, mA, mΩ) with literal glyphs and true minus signs, and log axes use superscript powers.
- **The power waterfall could clip** when a charging battery made the running peak exceed the net power;
  sources that deliver come first and the axis fits the true peak.
- **Captions described panels a narrow stage does not draw** (the thev view's power sweep, the graph view's
  matrix); each view now has a one-panel caption, asserted to match what was drawn.
- **Tests that could not fail, found by the sweep:** the split tested a joint by the battery's terminal name
  after "reverse" had swapped its terminals (the joint already held one part); "chips re-light" was checked
  after a reset that restores the chips' boot classes anyway; the split gap was expected as `99 − SPLIT_GAP`
  (re-deriving the constant under test); a rigid part's swing was aimed exactly 110 units from its pivot,
  where swinging and dragging free coincide; the fire line was tested at 14.8 and 18 A, never between 15 and
  16; the pencil's 25 Ω was never used; the wheel's repaint was compared against an idle, empty frame. Each
  now has a probe that only the correct code passes.
- **Two tolerances were set on the wrong scale:** V_th across the unbalanced bridge is a difference of two
  6.5-V node voltages (absolute error, on the 10-V scale), and the balanced bridge's 3.0e-11 A is the
  difference of two 0.3-A currents (known to ε × 0.4 A).
### Known-bad candidates
- **A conductance-stamped MNA (PhET's formulation) computes each wire's current as ΔV × 1e8 S.** Its branch
  currents are good to ~1e-5, and the current law it "satisfies" only to that. If a sim claims Kirchhoff to
  machine precision, keep every branch current an unknown and measure the laws on the answer.
- **Normalise a conservation residual by the scale of the connected piece, not by the node's own flow**: a
  dangling node's rounding-level current reads as a 100 % violation.
- **A tap threshold is not a drag threshold.** PhET joins on any movement and selects on a short one;
  treating a short drag as a pure tap silently fails every small nudge.
- **Element terminal names are not stable under "reverse".** A test that names a joint by a battery's `a` after
  reversing it probes the other end — and an assertion that the joint "now holds one part" passes doing nothing.
- **A chip-lit check after "reset all" is vacuous** when chips keep the classes they were built with; check that
  clicking one lights it and dims its neighbour.
- **A swing-about-the-pivot test must aim at a point not one part-length from the pivot**, or the free-drag
  mutant lands in the same place.
