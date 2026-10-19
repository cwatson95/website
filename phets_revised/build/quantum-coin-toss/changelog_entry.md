## 2026-09-21 — quantum-coin-toss: PhET's Coins screen on the quantum-measurement engine, and the sideways measurement that tells a hidden face from a superposition
### Added
- `quantum-coin-toss.html` (158 KB), a remake of PhET's Quantum Coin Toss 1.0.4 (the Coins screen of Quantum
  Measurement) in four views: *the classical coin*, *the quantum coin*, *the binomial*, *the hidden difference*.
  Credit line in the header and on the page; site nav absolute; no network. It runs on the engine of
  `quantum-measurement.html`: its assembler reads `p2_engine.js`, `p4_coins.js`, `p5_binom.js` and the shared test
  library from `build/quantum-measurement/`, so the two files cannot drift. PhET's 1.0.4 build carries the same
  coin model as Quantum Measurement's 1.0.5 (checked in the minified source):
  - N ∈ {10, 100, 10⁴};
  - the 1-s flip;
  - bias steps of 0.05;
  - the draw `nextDouble() < bias ? heads : tails`;
  - the start-hidden preference.
- *The classical coin* and *the quantum coin* are PhET's two scenes, one tab each with its own state:
  - prepare (heads or tails; ↑, ↓ or a superposition with P(↑) = |α|²) and send to measure;
  - flip, hide and reveal, or reprepare and observe, for one coin or 10, 100 or 10 000;
  - the counts against Np ± √(Np(1−p)), and the single coin's last 48 outcomes;
  - click a coin on the canvas to reveal or observe it.
- *The binomial* is the quantum-measurement view: seeded sets against the exact pmf, the spread √(p(1−p)/N)
  log–log, and one long run inside its ±2σ funnel.
- *The hidden difference* answers what PhET's screen asserts but, measuring face-on only, cannot show.
  - Face-on, a hidden classical face and a superposition give identical odds, P(up) = p.
  - Sideways, along x, the hidden face (a mixture, diag(p, 1−p)) gives ½. The superposition (off-diagonal
    √(p(1−p))) gives (1 + 2√(p(1−p)))/2, which is 1 at p = ½.
  - Seeded runs go through the engine's own draws; the two states are drawn on the Bloch disc (the mixture
    inside, the superposition on the edge); P(+x) is plotted against p.
- **Exact:**
  - the Born rule;
  - the binomial (Stirling lnFact against math.lgamma, the pmf against scipy);
  - both density matrices, their P(z), P(+x), purity and coherence at seven biases against numpy;
  - pureBloch(p) = ⟨ψ|σ|ψ⟩ over 21 biases.

  Every seeded count is pinned bit for bit to the Python twins (`build/quantum-measurement/derive.py` for the
  engine, `build/quantum-coin-toss/derive.py` for this view, which imports the first's PRNG). Each count is also
  held within 4σ of its law.
- **Verification:**
  - selfTest 988 checks, 0 failed under osascript;
  - UI drive 91 checks, 0 failed. Every click and flip goes through the frame loop from a proven-idle baseline, and every reset
    is checked against a sentinel;
  - mutation sweep 35 of 35 caught (28 physics, 7 UI), no survivors, on a copy in `build/quantum-coin-toss/_out/`;
  - audit: 0 layout problems at 1400×820 (no advisories) and 820×520 (under-readout advisories only: at that
    width the house's floating readout covers the top right, as in every sibling sim);
  - every captured view (15 + 4 narrow) was looked at;
  - `_tools/verify_one.py`: OK.
- **Where this differs from PhET:**
  - the two scenes are two tabs rather than a switch;
  - the coins are not animated flying into the test boxes;
  - the sideways measurement (the fourth view) is not in PhET's screen;
  - no sounds and no screen-reader descriptions.
### Fixed (during the build)
- **A mutant of the quantum coin's collapse survived this sim's sweep.** Root cause: the assertion that observing a
  superposition leaves the coin in the observed basis state lived in `quantum-measurement`'s own suite, so the
  shared engine went into this build with that contract unguarded. It now lives in the shared `engineTests`, which
  both suites run.
- **`COINS.classical.p === 0.35` failed** after seven bias steps. Root cause: 7 × 0.05 = 0.35000000000000003.
  `snapBias` rounds to k/20, and selfTest pins the exact value in both sims.
- **The preference check passed while the control was visible.** Root cause: it read the checkbox's label rather
  than the row that is hidden, so "hidden" was never actually tested. It now reads the row.
- **A flip animation test compared a repaint against a possibly EMPTY frame** (the same weak pattern the parent
  sim's sweep exposed): `animatesU()` drains the dirty repaint and requires two consecutive drawn, different
  frames.
- **The "classical: mixed" label sat on the Bloch disc's x axis** at p = ½. Root cause: the mixture is always on
  the z axis, r = (0, 0, 2p − 1), so at p = ½ it is at the origin, where the label's own height is the axis.
  Lifted 10 px off it.
- Shared-engine fixes made in `quantum-measurement` and inherited here, each with its own regression test: the
  negative zero from `toFixed` (`fmt0`, plus a layout rule), value labels landing on the law's mark (`barValY`,
  plus a layout rule), the empty-box note landing on a mark (`freeY`), legends naming what is not drawn, a legend
  silently lost when an entry grows, and captions naming panels the layout skips (`layoutNamed`). The coins' short
  caption named the histogram's orange marks at 560 × 380, where the histogram is not drawn; the binomial's named
  its long-run panel at the same size.
### Known-bad candidates
- An engine contract exercised by only one sim's suite: the other sim's mutation sweep finds it unprotected. Put
  shared-engine assertions in the shared test library.
- k × 0.05 is not exact (7 × 0.05 = 0.35000000000000003): snap to k/20.
- A UI check that reads a control's label instead of the row that is hidden tests nothing.
- "Compare two frames and assert they differ" passes when the second frame is empty.
- A label placed at a point that can be the origin of its own axes (the mixture at p = ½).
- `toFixed` keeps the sign of a negative zero; a value label above its bar alone lands on the law's mark; a legend
  or a caption written as a constant beside a conditional drawing (all shared with `quantum-measurement`).
