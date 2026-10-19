## 2026-09-18 — energy-forms-and-changes: PhET's bench and energy systems, with every joule on a ledger that closes
### Added
- `energy-forms-and-changes.html` (236.7 KB), a remake of PhET's Energy Forms and Changes 1.4.24 in five views:
  *the bench*, *the systems*, *the heat ledger*, *the energy flow*, *equilibrium*.
  Credit line in the header and on the page; site nav absolute; no network.
- *The bench* is PhET's Intro screen. It has the iron and brick blocks, the water and olive-oil
  beakers, PhET's six spots and stacking rules (no beaker on or in a beaker), and two heat/cool
  burners with draggable levers and "link heaters". It also has four thermometers in a tray (they
  stick to what they are dropped on, and read PhET's steam and flame temperatures), energy symbols,
  play, step and ×4, and five presets (PhET's start, heat the iron, hot iron into water, brick on
  iron cooling, boil the water).
- *The systems* is PhET's Systems screen, with every source, converter and user in PhET's carousels:
  - sources: the cyclist (21 chunks of food, "feed me"), the faucet, the sun with clouds, and the
    teapot on a burner;
  - converters: the water-wheel generator (belted to the cyclist) and the solar panel;
  - users: the beaker heater, the incandescent bulb, the fluorescent bulb and the fan.
  Energy chunks are drawn by form (mechanical, electrical, thermal, light, chemical) under PhET's
  "forms of energy" key.
- *The heat ledger* records the bench. It draws each body's temperature, and the first law as three
  accounts: the burners did = the bodies gained + the room took. The halo and the sum coincide to
  the last digit. A panel beside them sets each body's chunks against PhET's map g(E).
- *The energy flow* is the chain as a Sankey diagram to scale in watts, with its stores (the falling
  water, the kettle, the wheel, the heater's water) and every loss. Below it runs the cumulative
  ledger, IN = OUT + LOST + STORED.
- *Equilibrium* takes one of five pairs. It lays PhET's stepped model over the exact solution of the
  linear pair-and-room system: a closed-form 2×2 matrix exponential, checked against
  `scipy.linalg.expm` and against its own ODE. It draws T_eq = (C₁T₁ + C₂T₂)/(C₁ + C₂), the gap in
  mK, and PhET's heat capacities against the real ones.
- **The model is PhET's**, read out of the build:
  - EFACConstants: the specific heats and densities 450/7800, 840/3300, 3000/1000 and 1411/916;
    4.5-cm blocks; 8.5-cm beakers, 1.1× tall and half full; the 120-per-m² displacement.
  - HeatTransferConstants: k = 1000 W/(m·K) between bodies and 30 W/(m·K) with the air.
  - ThermalContactArea's contact length, with PhET's operator precedence kept.
  - The burners' 5000 and 1500 W, the 620-K and boiling-point caps, and the 1e-6-K threshold.
  - The air as an infinite 296-K bath.
  - The chunk map (brick at 0 °C = 1.25 chunks, at 296 K = 2.4), so ENERGY_PER_CHUNK = 5019.022 J.
  - The Systems rates: 10 kW; the crank's 3π rad/s and π/2 rad/s²; the 0.4-s fall; the sun at
    0.1 + 0.9(1 − clouds); the 10-s teapot and the 5/3-s wheel; the 68 % panel; the heater's
    5000 W and 0.5/s ramp; the bulbs' 65/35 and 80/20; the fan's 0.0051 rad/s per W.
  - PhET's own pre-distributed chunk tables (6, 2, 34, 8, 20 chunks) are reproduced exactly: an
    independent check of the masses and the map.
- **Real materials** (in *equilibrium*), each from its source:
  - water: NIST Chemistry WebBook (IAPWS-95) at 296 K, 4182.32 J/(kg·K) and 997.577 kg/m³;
  - iron: NIST-JANAF Cp 25.094 J/(mol·K) over 55.845 g/mol, and 7874 kg/m³ (Arblaster 2018);
  - brick: 840 J/(kg·K) (Wikipedia's table) and 1900 kg/m³ (Engineering ToolBox's 1400–2400);
  - olive oil: 1970 J/(kg·K) (Engineering ToolBox) and 911 kg/m³ (USDA).
- **Exact:**
  - the bench's first law every step to rounding (≤ 8ε of the energies; 1e-8 J summed over 1800
    steps);
  - the chunk identity E + Σ(energy in transit on a body's links) − EPC·chunks = constant,
    ≤ 1e-12 at every step of every scenario, with |chunks − g(E)| < 1 always;
  - every Systems element's in = out + losses + Δstore every step (≤ 4ε), and the global ledger
    across chain swaps and feeding;
  - every channel's chunks = floor(E/EPC);
  - equilibria against expm to 1e-11;
  - eleven bench scenarios, eleven chains and every equilibrium pair (both materials) pinned to
    `derive.py`, an independent Python twin, through `refvals.txt` → `p7a_refs.js` (679
    references, none typed by hand).
- **PhET's own numbers that do not close, each pinned in derive.py and corrected here:**
  - the teapot makes steam at 20 kW × heat, twice its burner's power below its cap;
  - the cyclist puts out 10 kW × crank/max while his chunks send one in six to heat;
  - the generator's efficiency depends on the frame rate: 69 % at 60 frames/s, while at
    30 frames/s it puts out 1.38× what it takes in;
  - the heater puts half its power into the water and says nothing of the rest.
- **Verification:**
  - selfTest: 2037 passed, 0 failed under osascript. It includes a layout sweep of 31
    configurations × 4 sizes with the #hint-corner check.
  - UI drive: 250 passed, 0 failed. The lever, body and thermometer drags are all tested through
    the frame loop from proven-idle baselines, and every reset against a sentinel.
  - Mutation sweep: 110 of 111 mutants caught (97 physics, 14 UI). It ran on the copy in
    `build/energy-forms-and-changes/_out/`. The last mutant, the right slider’s link, was added
    after the full sweep and ran in its own pass on the same html. The one survivor,
    `no displacement cap`, is equivalent. PhET’s min(0.5 + 120·area, 1) cannot bind, because
    only the two 4.5-cm blocks displace, and together they lift the water to 0.986 at most
    (asserted in scenario I).
  - Audit: 0 layout problems at 1400×820, 1100×700 and 820×520. The narrow size shows only the
    under-readout advisory.
  - Every captured PNG (28 + 5 + 6) was looked at.
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET, deliberately:**
  - One fixed 1/60-s step.
  - Drops snap to PhET's spots at once; PhET lets bodies fall.
  - The levers stay where they are left; PhET's spring back unless `stickyBurners` is set.
  - ×4 is shown; PhET hides it behind `showSpeedControls`.
  - One play/pause for both screens.
  - The Systems screen opens on the faucet running; PhET opens on the cyclist, not pedalling.
  - Energy symbols start shown.
  - Thermometers print °C.
  - Blocks are drawn with their front face on the model's rectangle; PhET centres the cube on it.
  - Chunks are the ledger quantised, not PhET's random paths.
  - The fan's heat is PhET's full-power 1/14 at every power.
  - No sounds, no keyboard dragging, no screen-reader descriptions.
### Fixed (during the build)
- **The cyclist's 21 food chunks lay on one diagonal.** Their jitter was (k·0.618 mod 1,
  k·0.382 mod 1), and the two sequences sum to 1, so every point sat on a line. They now sit on a
  grid along the torso.
- **The iron vanished when it was dropped into the water.** Two causes:
  - the water's chunks were painted over it;
  - PhET's oblique cube, centred on the model rectangle, hung 5.6 mm through the floor of a beaker
    that is drawn flat.
  The bench now paints by depth: the liquid, its chunks, the block and its chunks, then a
  translucent liquid front and the glass. Every box draws its front face on the model rectangle,
  and the pick and sensing shapes follow what is drawn.
- **Hot blocks were given a glow, which is unphysical.** Iron does not visibly glow below about
  800 K, and PhET caps blocks at 620 K. The glow was removed.
- **The ice and flames poked above the burner into the block,** and at full heat the lever's knob sat
  on the flame. Both now stay in the burner's mouth, and the lever's track runs below them. The
  drawing and the pointer share one pair of constants, so the two cannot drift apart.
- **At 820×520 and 560×380 tick labels ran into the caption.** The two-row layout squeezed its main
  panel below 80 px, and its no-row fallback ran the panel to 16 px above the caption, where its
  ticks hang. The fallback (`layoutFit`) drops the row only when the main panel would be under
  100 px, and then leaves the 34 px its ticks and axis title need.
- **Captions described panels the narrow layout does not draw.** Each view now carries full, two,
  solo and short captions, and draws the one that matches its panels.
- **Labels were shifted into the caption and onto legends.** `lab()` avoids only registered boxes.
  The captions and every legend are now registered before any label is placed.
- **The per-element ledger check failed on correct code (6e-12).** It judged each step's residual
  against that step's flows alone. A 1.6e5-J store of water rounds at 3e-11 J, which is 1e-9 of a
  0.02-J step. The check now includes the store it touches, and holds at ≤ 4ε.
- **Six tests could not fail, found by pre-screening the mutants:**
  - the chunk-speed check compared CHUNK_V with CHUNK_V;
  - the corrective pass's shedding branch never ran (a hot iron under the brick, losing heat on
    two links, now runs both branches);
  - the heater's 0.5/s ramp never bound (switching the heater into a running chain makes it bind);
  - a converter swap with a full wheel was never tried;
  - PhET's substeps, a block straddling the glass and the 1e-6-K threshold were unreachable at the
    fixed 1/60-s step, and each now has a direct pin;
  - the room's box only showed its size with a beaker held at the bench's end.
- **Two prose claims were wrong against the measurements:**
  - "a few tenths of a kelvin at most" for PhET's step against the exact solution: the gap is
    1.33 K at the extreme settings, always under 0.4 % of the starting difference, and that is now
    asserted;
  - "100 % at ×4" for PhET's generator: the Systems screen has no ×4. At 30 frames/s the
    generator puts out 1.38× what it takes in. Now pinned in derive.py.
- **"link heaters" worked through two mechanisms, so cutting either changed nothing.** The first
  mutation sweep’s "linking the heaters does nothing" survived. The sliders copied the left level
  into the right while linked, and the level reader also used the left level for both. The reader
  now returns the two levels as stored, every writer (both sliders, the lever drag, the link box)
  keeps them equal, and one UI mutant cuts each writer.
- **What the converter cannot use was drawn twice.** The source's own chunks carry on past it, and
  the `x.miss` channel spawned a second set. The channel is now counted but not drawn.
- **The thermometer drop test aimed at the wrong pixels,** and the grab-offset and linked-lever
  tests assumed levels that the previous steps had changed. Each test now computes its target from
  the current state.
### Known-bad candidates
- **PhET's Systems screen does not close its own ledger.** A remake that copies its rates verbatim
  inherits three faults: a teapot that makes steam at 2× its burner's power below its cap, a
  generator whose output depends on the frame rate (1.38× its input at 30 frames/s), and a cyclist
  whose numeric output disagrees with his chunks by one in six. Choose rates that close, and pin
  each PhET discrepancy in the Python twin.
- **(k·φ mod 1, k·(1 − φ) mod 1) is a line, not a scatter.** A golden-ratio jitter in x paired with
  its complement in y puts every point on one diagonal.
- **An oblique box centred on its model rectangle, drawn next to flat containers, hangs through the
  containers' floors.** Draw its front face on the rectangle.
- **`stageLayout` with no bottom row leaves 16 px under the main panel,** so its ticks and axis
  title land on the caption. A fallback that drops the row must shrink the panel about 34 px.
- **`lab()` avoids only what is registered.** Register captions and legends before placing labels.
- **A per-element ledger residual must be judged against the store it touches, not just the
  step's flows.** Otherwise a correct element holding a large store reads 1e-9.
- **A heuristic transfer rule gains an exact, testable invariant if every transfer moves its
  link's balance by exactly one quantum.** Energy plus the balances still in transit, less
  EPC × chunks, is then conserved to rounding.
- **PhET's own spots are asymmetric:** spot 0 is −0.241 and spot 5 is +0.242, because
  −241.4999… rounds down. Copy the arithmetic, not the intent.
- **PhET's burner clamps its displayed temperature at 273.15 K for any level below −0.23,**
  although the cooling it applies still scales with the level.
