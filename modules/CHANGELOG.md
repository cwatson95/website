# Changelog — modules

Per-project changelog (policy: Agent repo `CLAUDE.md` → "Per-project changelogs").
Dated entries, newest first. The Known-bad list is permanent — check it before
editing or resurrecting files.

## Known-bad — do not reintroduce
- **NE trunk: do not "restore" values to what Shultis & Faw print where a
  module has corrected them.** **Thirty-one** printed values are wrong and are
  corrected in code, each with the printed value preserved (in a `*_ERRATA`
  constant or a named constant) and a test pinning the correction to the evidence
  that forces it. Reverting any of them silently breaks a test. Twenty-four are
  listed in the *NE trunk complete* entry below; the other seven in the *NE trunk
  opened* entry, whose heading says "six" but lists seven — the miscount is in the
  heading, not the list.
- **NE trunk: Table 7.2's proton/lead row is unusable and is withheld
  deliberately.** `csda_mass_range` RAISES for proton + lead rather than
  returning a number. The printed constants (0.065607, 0.98751, 0.0047353) do not
  belong to the same family as any other proton row, give 4.59 g/cm² at 4 MeV
  against ~0.065 accepted, and their $b$ matches the lead ALPHA row's to 1e-4.
  The correct constants cannot be recovered from what is printed, so no
  replacement may be invented. See `NE-14_charged_particles/refs.md`.
- **NE trunk: the four-factor formula in code is `eps*p*f*eta`, not `p*f*eta`.**
  S&F Eqs. (10.16)–(10.17) omit ε; Table 10.5's water row and all 11 rows of
  Table 10.8 require it. `four_factor_formula_as_printed` exists only for
  comparison — do not make it the default. See `NE-19_neutron_cycle/refs.md`.
- **NE trunk: `dosimetry.quality_factor` and `effective_dose` refuse unknown
  input by design.** Defaulting QF to 1 understates fast neutrons 20×, and
  weighting an unlisted organ at zero silently drops it from the effective dose.
  Do not add a "sensible default" to either.
- **NE trunk: `R0_FM` (nuclear radius coefficient) is 1.2 fm, not 1.4.** S&F
  Eq. (6.19)'s printed 1.20 MeV numerator is $e^2/4\pi\epsilon_0 r_0$ with
  $r_0=1.2$ fm, confirmed against three of the authors' own worked barrier values.
  An earlier draft of NE-04 used 1.4 fm, which makes every Coulomb barrier 17%
  low and breaks S&F Example 6.1. Fixed 2026-08-01; do not reintroduce.
- **Never let `ALT` and `STEEL` be the only difference between two series in a
  figure.** The palette every trunk shares —
  `INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"` — is safe
  in every pair except this one: OKLab ΔE 2.6 under simulated deuteranopia and
  12.5 under normal vision (floor 15), i.e. indistinguishable to a red-green
  colourblind reader and marginal for everyone else. Use at most three
  colour-coded series per axes, or separate them by linestyle/marker as well.
  Measured with the data-viz validator's six checks, 2026-08-01.

## 2026-09-15 — arrival by deep link: the sidebar scrolls itself, the page stays put
### Changed
- `generate_webpage.py`: Cooper reported that opening a module from the
  Teaching Network sometimes clipped the header off. The arrival used
  `scrollIntoView` on the sidebar item, which scrolls every scrollable
  ancestor as well — any nudge of the page under the fixed site bar cuts the
  top off both columns. Now `revealItem` sets the list's own `scrollTop`
  from bounding rects and touches nothing else: by deep link the trunk (or
  Thermo topic) starts from its heading when the item fits below it, else
  the item sits a third of the way down; a click only nudges an item that
  is out of view. `pinTop` puts the reading column and the page at the top
  on arrival, again on the next frame and at `load`; a stale sidebar filter
  is cleared so the target is visible; `html{scroll-padding-top:36px}`
  keeps any future scroll-to-target below the bar. `teaching_modules.html`
  regenerated: identical apart from the inline script and that CSS line.
### Verified
- `website/dev/check_links.py` all green; its `modules` harness now lays the
  sidebar out and checks the arrival geometry (29/29). No element on the
  page carries an id equal to a fragment, so the browser's own anchor jump
  is ruled out. No browser here: if a header still clips, the browser and
  the module id are what to report.

## 2026-09-15 — every module links back to its orb in the Teaching Network; hash routing
### Changed
- `generate_webpage.py`: the page answers deep links — `#MA-02` (or
  `#m-MA-02`) opens that module, `#MA` a trunk's first module (likewise
  `#TD-1.1`, `#MACRO_EM`); picking a module in the sidebar keeps the URL in
  step (`history.replaceState`, so Back still leaves the page) and scrolls
  the sidebar to it; only the routed module is KaTeX-rendered at load.
  Every module that is a node of `topic_network.txt` (143 of 268: the ten
  network trunks) gets **open in the Teaching Network**
  (`../website/teaching.html#<id>`) in its subtitle line. NE, MACRO_EM and
  Thermo have no orb yet, so no link: list them in topic_network.txt, rerun
  `website/dev/build_network.py` and this generator, and they join.
  `teaching_modules.html` regenerated.
- The network side (the panel's "open module" link, glide-to-hash) is in
  the website changelog, 2026-09-15 a; `website/dev/check_links.py` audits
  the round trip both ways.
### Verified
- The regenerated page is byte-identical to the previous one apart from the
  143 netlink anchors, two CSS rules and the inline script; 268 modules /
  1616 equations / 455 figures unchanged. `website/dev/check_links.py` all
  green, including the deno harness that drives this page's inline script
  against a stub DOM built from the page itself (20/20).

## 2026-08-12 — teaching_modules is the site's Modules tab
### Changed
- `generate_webpage.py`: the site header template now includes the Modules
  tab (self-link, aria-current) between Teaching and Simulations; Teaching
  no longer claims current. `teaching_modules.html` regenerated.
### Verified
- Nav audit on the regenerated page: seven tabs in site order, Modules
  uniquely current, remaining tabs still point at `../website/*.html`;
  regeneration deterministic (268 modules / 1616 equations / 455 figures
  unchanged).

## 2026-08-12 — browser renamed to generate_webpage.py / teaching_modules.html; full width
### Changed
- `ma_browser_web.py` → `generate_webpage.py`; its output `ma_browser.html` →
  `teaching_modules.html`; the two old files are removed (the Tkinter
  `ma_browser.py` keeps its name and remains untouched). The usage pointer in
  `topic_network.txt` now names the new command — that line is commentary, and
  the teaching-network bake is byte-identical after the edit (155 nodes /
  261 edges unchanged), so `website/teaching_network.js` did not move.
- Full browser width: the 860-px caps are gone (`.module`'s `max-width` and
  the bare `.doc{max-width:860px}` rule) — the paper reading panel now spans
  the whole content pane beside the sidebar.
### Verified
- `teaching_modules.html` differs from the just-themed `ma_browser.html` by
  exactly the two max-width lines (3-line diff); zero `max-width:860` left;
  site-nav and `#070b18` intact; regeneration from the renamed script
  reproduces the file deterministically (268 modules / 1616 equations / 455
  figures unchanged).

## 2026-08-12 — ma_browser wears the personal site's frame
### Changed
- `ma_browser_web.py` (and regenerated `ma_browser.html`): the page now
  carries the personal site's chrome (projects/website/) — backdrop `--bg`
  `#f6f6fb` → `#070b18`, plus the fixed 36-px six-tab site nav that every
  sim in projects/simulations/ also carries (simulations changelog
  2026-08-12 (d)); Teaching is marked current, since the modules are the
  teaching network's source material. The reading surface stays light:
  `.module` is now a white paper panel (var(--panel), 12-px radius) floating
  on the dark backdrop, so no ink-on-light text ends up on a dark background;
  the sidebar is unchanged. `#side` height `100vh` → `100%` so the nav bar's
  `body{padding-top:36px}` (border-box) doesn't overflow the viewport.
### Verified
- Unpatched regeneration FIRST came out byte-identical to the committed
  ma_browser.html (deterministic generator, content in sync), so the new
  page differs from its predecessor by exactly the theme. Patched-vs-baseline
  diff = 31 lines (three CSS edits + the injected style block + the header);
  tag deltas exactly +1 header / +1 nav / +6 a / +1 style, all closed;
  `var(--bg)` referenced only by the body background; no `:first-child`
  selectors for the new first child to break; 268 modules / 1616 equations /
  455 figures reported unchanged. No headless browser on this Mac — the
  bar's rendering rests on the same block already carried (and rasterised)
  across the 49 sims and six site copies.

## 2026-08-01 — NE trunk complete (NE-12..NE-27)

Supersedes the "Still to do" note in the entry below. The trunk is now **27 of 27
modules**, covering Shultis & Faw Chapters 3–14 end to end.

### Added
- **Modules NE-12..NE-27**, each with the house layout (`README.md`, `notes.md`,
  `refs.md`, `code/` + tests, `problems/`, `figures/` + `captions.json`):
  NE-12 photon interactions (§7.3), NE-13 neutron interactions (§7.4), NE-14
  charged-particle stopping (§7.5), NE-15 radiation detectors (§§8.1–8.5), NE-16
  counting statistics (§§8.6–8.7), NE-17 dosimetry (§§9.1–9.4), NE-18 health
  effects (§§9.5–9.10), NE-19 the neutron life cycle (§§10.1–10.6), NE-20 reactor
  kinetics (§§10.7–10.9, 10.11–10.12), NE-21 diffusion theory (§10.10), NE-22
  power reactors (§§11.1–11.6), NE-23 the fuel cycle (§§11.7–11.8), NE-24 fusion
  reactors (§§12.1–12.4), NE-25 direct energy conversion (§§12.5–12.11), NE-26
  industrial and research applications (Ch. 13), NE-27 medical applications
  (Ch. 14).
- **Relations the book needs and omits**, supplied and flagged as additions
  rather than folded in silently: the **Fano factor** (NE-15 — S&F never mention
  it, and using √N instead of √(FN) overestimates a germanium photopeak width
  2.8×); gas W-values (NE-15); error propagation for a *difference*, optimal
  counting-time allocation, and the two-source dead-time method (NE-16); the
  roentgen-to-gray conversion, 1 R = 8.73 mGy (NE-17); **separative work** and the
  value function (NE-23 — Chapter 11 describes enrichment without them); usable
  ⟨σv⟩ fits for D-T and D-D (NE-24); the thermoelectric ZT relation, Richardson
  emission and RTG mission sizing (NE-25); the transmission-gauge optimum
  **µt = 2** and the ⁹⁹Mo generator's 48.5 h ingrowth peak (NE-26); the
  **Hounsfield unit** (NE-27 — §14.1.5 develops the Radon transform and filtered
  backprojection in full, names Hounsfield, and never defines the CT number).

### Fixed — 24 further errata in Shultis & Faw, each caught by cross-checking
Same method as the NE-01..NE-11 pass: printed values are checked against *other
printed values*, and where two book statements disagree the disagreement is
resolved by evidence and both are recorded. None was found by reading.

- **Table 7.2 / NE-14** — the proton/lead row is corrupt and is withheld; see the
  Known-bad list above. *Verified: `csda_mass_range` raises for that pair.*
- **Example 7.7 / NE-14** — evaluates the water proton range with b = 1.4501,
  which is the **LiF** row two lines below; Table 7.2's H₂O row gives 1.4975.
  NIST PSTAR picks the table (+0.3% vs −2.9%), so the printed 0.021 cm is ~3%
  low. *Verified against PSTAR, an independent source.*
- **Example 9.3 / NE-17** — reports 10.5 µSv from factors that give 0.105 µSv,
  a factor of 100. **Example 9.5 / NE-17** — reports "7.1 mrem" where its own
  Table 9.4 gives 7.1 **rem** (71 mSv), a factor of 1000. Plus **Problem 9.1**
  (tritium's β energy is in keV, not MeV) and one solution-manual answer
  (Problem 9.4(a)) that Problem 9.5(a) disproves.
- **Table 9.11 / NE-18** — a total that does not match its own column.
  **Example 9.7 / NE-18** — prints 3116 where its factors give 3416, proved by
  the example's own following line (47/y); and quotes respiratory mortality
  "from Table 9.12" as 71.9/25.2 where the table says 76.2/42.2. Plus two
  solution-manual errors (a ²²⁰Rn alpha inside a ²²²Rn chain; the banana problem,
  where two errors partly cancel).
- **Eqs. (10.16)–(10.17) / NE-19** — the four-factor formula is printed without ε.
  Table 10.5's water row (ε = 1.051, k∞ = 0.888) is the only row with ε ≠ 1 and
  discriminates: ηpf = 0.845. Confirmed across all 11 rows of Table 10.8 and
  independently by §10.10. See the Known-bad list. **Table 10.3 / NE-19** —
  D₂O's σ_sM is printed as 0.509 b, which duplicates its own ξ; Table 10.7's
  ξΣ_sM = 0.178 cm⁻¹ requires 10.6 b, and the identical cross-check reproduces
  graphite to four figures. Plus four arithmetic slips (Example 10.1's stray
  6.206; Example 10.3 writing ν where η belongs; Example 10.4's 3500 against
  Table 10.4's 3070; Example 10.9's inserted 8).
- **NE-20** — Example 10.12 cites the wrong example; §10.7.4 inverts the lifetime
  formula; §10.9.2 attributes stability to the wrong nuclide.
- **Table 11.3 / NE-22** — specific power × loading gives 4351 MW against the
  printed 3830, a 14% gap. The identical check passes for Table 11.2 to 0.15%,
  so the method is sound and the row is not.
- **§12.1.1 / NE-24** — hydrogen's ionisation energy is given as 13.06 eV; it is
  13.598. The book's own worked example reproduces *only* with 13.06, so the
  error is upstream of the example, not in it.
- **§14.1.5 / NE-27** — "shared the Nobel prize in **1972**". The prize was
  **1979**; 1972 is the year of the first published CT images. Checked against
  nobelprize.org — a fact check, not a recomputation, and recorded as such.
- **Fig. 14.16 caption / NE-27** — the pinhole point-spread is printed as
  "R_ph = (d/b)/(f+b)", which has units of 1/length. The caption's own first
  equality gives the product d(f+b)/b — the *image*-plane blur — while the body
  text's (d/f)(f+b) is object-referred, and only that form closes Eq. (14.19).

### Changed — recorded rather than silently resolved
- **NE-19** — §10.4.1 says heterogeneous ε runs "5–10% higher", but Eq. (10.6)'s
  own constants give ≤1.2%. Documented as a discrepancy; neither side asserted.
  Also: ε falls below 1 at infinite dilution, and Eq. (10.25)'s two-dimensional
  printed layout invites a 68% error — the *correct* reading is pinned by a test
  that asserts the misreading **as** a misreading.
- **NE-22** — §11.1.2's "about 40%" thermal efficiency contradicts §11.1.4's own
  numbers; both recorded.
- **NE-26 — one of my own claims retracted.** A draft asserted that Table 13.2's
  radiography sources sit at the µt = 2 gauge optimum. They run 1.8–9.2.
  Radiography optimises contrast through a *fixed* workpiece, not thickness
  variance, so the two optima are unrelated. *Verified:
  `test_radiography_is_not_run_at_the_gauge_optimum`, so no later reader "fixes"
  it back.*
- **NE-19 — a second self-correction.** `maxwellian_flux` was first implemented
  as √E·e^(−E/kT); S&F Eq. (10.1) is linear in E, because a flux is density ×
  speed. Corrected, with the reason recorded in the source.

### Verification
- **462 tests across all 27 NE modules, all passing** (234 of them new in this
  pass; `python3 code/test_*.py` in each). **27 figure scripts run clean,
  producing 107 SVGs** + `captions.json` (64 new).
- Reproduced from the book: Tables 7.2, 8.1, 8.3, 8.4, 9.4, 9.9, 9.11, 10.3–10.8,
  11.2, 11.3, 11.7, 11.8, 13.1–13.3, 14.2, 14.3, 14.6, 14.7, and Examples 7.7,
  9.3, 9.5, 9.7, 10.1–10.12. Several checks were **independent of the book**:
  NE-14's ranges against NIST PSTAR/ASTAR/ESTAR, NE-12's Klein–Nishina
  computation against Appendix C.3's tabulated Compton column (<1% above
  0.5 MeV in all five materials), and NE-27's Table 14.3 against the trunk's own
  `data_tables/D1_decay_radiation.csv` (<0.5%, with the 511 keV yield exactly
  twice the positron branch).
- Standout internal consistency checks that **passed**: Table 11.7's 873 kg of
  fission products = 277 full-power days against the 274 its capacity factor
  implies (1%); Table 11.8's heavy-atom balance closes exactly, implies 43% of
  fissions are plutonium, and gives 33.3 GWd/tU against Table 11.2's printed 33;
  NE-21 independently recovers NE-19's P_NL = 0.7192; NE-24's ⟨σv⟩ fits reproduce
  Fig. 12.2's ignition temperatures to 4% (D-T) and 12% (D-D); NE-27's Table 14.6
  sums exactly to its printed totals in all four columns.
- Eight of the sixteen modules found **nothing wrong** — NE-12, NE-13, NE-15,
  NE-16, NE-21, NE-23, NE-25, NE-26 — each after multiple independent
  cross-checks. That is recorded because "no errata" is only meaningful if the
  search was real.
- **Two test defects caught and fixed while writing** (both would have made an
  assertion vacuous rather than wrong): NE-14's NIST comparison used a helper
  that degrades to an *absolute* tolerance below 1, so assertions on ~4e-3 g/cm²
  passed for any value — now strictly relative, and it asserts the worst
  deviation *exceeds* 2% so it cannot go vacuous again. NE-16's
  variance-equals-mean check simulated a binomial with p = 0.2, whose variance is
  20% below its mean — it would have failed against *correct* code; it now
  generates exponential inter-arrival times and keeps the binomial as an explicit
  contrast.

## 2026-08-01 — NE trunk opened (NE-01..NE-11)

### Added
- **`NE/` — a new trunk: Nuclear Science & Engineering**, following Shultis &
  Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd ed. Chapters 1–2
  are deliberately skipped (that ground is held by MA-01, RE-02..RE-06 and
  QM-01..QM-08); the trunk opens at Chapter 3. Planned as 27 modules covering
  Chapters 3–14; **11 are complete** (NE-01..NE-11, Chapters 3–6 and §§7.1–7.2).
  Index and chapter map in `NE/list_NE.txt`.
- **`NE/data_tables/` — Appendices A–D extracted to 13 CSVs** by
  `NE/data_tables/_extract.py` (poppler `pdftotext -bbox-layout`; no PyMuPDF
  dependency). 20 physical constants, 92 element properties, 916 isotopic
  abundances and half-lives, 2931 atomic masses, 75 thermal cross sections,
  31 activation radionuclides, 5 photon-coefficient tables, 1276 decay-radiation
  lines and 338 decay group totals. Documented in `NE/data_tables/README.md`.
- Modules NE-01 (atomic models), NE-02 (nuclear models & SEMF), NE-03 (binding
  energy), NE-04 (Q-values), NE-05 (decay modes), NE-06 (decay kinetics),
  NE-07 (decay chains & radiodating), NE-08 (binary kinematics & the Coulomb
  barrier), NE-09 (fission), NE-10 (fusion & nucleosynthesis), NE-11
  (attenuation, cross sections & reaction rates). Each with the house layout:
  `README.md`, `notes.md`, `refs.md`, `code/` + tests, `problems/`, `figures/`.
- **`Thermo/` gained a `figures/` layer for all 53 concept modules (106 SVGs)** —
  the last trunk that had none. It was 92 of the library's 241 modules and 0 of
  its 242 figures; adding them took the browser to 348, and with the NE trunk
  landing the same day `ma_browser_web.py` now reports **253 modules and 395
  figures**. Detail, the topic map, and an inventory of the numerical mathematics
  the Thermo Python actually performs are in `Thermo/CHANGELOG.md`.

### Fixed — Thermo dual-cycle Otto limit
- `Thermo/Topic_9/09.4_dual_cycle`: `dual_efficiency` raised `ZeroDivisionError`
  at exactly `rp = rc = 1`, so the reduction to Otto its own docstring promises
  was reachable only as a limit. Numerator and denominator vanish together there;
  the removable singularity is the Otto value and the guard now returns it.
  Verified: `test_dual_cycle.py` 14 → 16 assertions, all passing. Full argument
  in `Thermo/CHANGELOG.md`.

### Fixed — six errata in Shultis & Faw, each caught by cross-checking
The extractor and the module tests check printed values against *other printed
values* rather than accepting them. Where two book statements disagree, the
disagreement is resolved by evidence and both are recorded. All six are corrected
in code with the printed value kept in a `*_ERRATA` constant and a dedicated test.

- **Eq. (6.19) / NE-04, NE-08** — the barrier constant implies $r_0=1.2$ fm, not
  the 1.4 fm this trunk first used. Verified against S&F's own worked values
  (1.994, 2.111, 1.236 MeV) and Example 6.1. *Verified: NE-08
  `test_barrier_matches_the_books_1_20_mev_form`, plus NE-04's 15 tests re-run.*
- **§6.4.2 / NE-08** — the ⁷Li(p,n)⁷Be kinematic threshold is printed as
  1.875 MeV; the book's own Appendix B masses give 1.8803, which is also the
  accepted neutron-metrology calibration value. *Verified:
  `test_known_thresholds`, which asserts 1.8803 and asserts 1.875 is not
  reproduced.*
- **Table 6.2 / NE-09** — ²³⁷Np's fission probability, printed 2.1×10⁻¹² %,
  must be 2.1×10⁻¹⁰ %; both the alphas-per-fission column and the neutron
  emission rate demand the factor of 100. *Verified:
  `test_the_two_table_6_2_typos`.*
- **Table 6.2 / NE-09** — ²⁴⁸Cm's emission rate, printed 4.1×10¹² n/(g·s), must
  be 4.1×10⁷; its own half-life and fission probability give 10⁷, and 10¹² would
  make a 339 000-year nuclide outshine ²⁵²Cf. *Verified: same test.*
- **§6.7 / NE-10** — p + ¹¹B → 3α is printed at 8.08 MeV; the book's masses give
  8.68, the accepted aneutronic-fusion value. *Verified:
  `test_the_p11B_erratum`.*
- **§6.7.2 / NE-10** — the solar core is described as "about 7,000 km in radius
  or about 0.1% of the sun's total volume"; those differ by 1000× in volume.
  The volume fraction is the consistent half (it gives the accepted 283 W/m³
  core power density). *Verified: `test_the_solar_core_radius_erratum`.*
- **Example 7.2 / NE-11** — ρ(Fe) is printed as 7.784 g/cm³, but the next line's
  arithmetic (0.2151 cm³, 9.298 g/cm³) requires 7.874, which is also the accepted
  density of iron. *Verified: `test_the_iron_density_typo`.*

Root cause in every case is the same: a printed value that the book's own
adjacent numbers contradict. None was found by reading; all were found by
recomputing.

### Changed
- **NE-09, NE-10 — two ambiguities documented rather than silently resolved.**
  S&F's decay-heat correlations Eqs. (6.44)–(6.45) carry a stated validity range
  (10 s < t < 10⁵ s) that the book's own Problem 21 exceeds by two decades;
  `decay_heat_*` deliberately does not clamp, and the problem set flags the
  extrapolation and its direction. S&F §6.7.2 also switches accounting
  conventions mid-section — the pp-chain steps are β⁺-corrected nuclear Q-values
  summing to 24.69 MeV while Eq. (6.47) quotes 26.72 MeV including positron
  annihilation; `pp_chain_energy` takes an `include_annihilation` flag and a test
  pins both.
- **NE-10 — one of my own claims corrected.** A first draft asserted that fusion
  becomes endoergic past iron. It does not: ⁵⁶Ni + α still releases 2.7 MeV.
  Stellar burning stops because the yield collapses threefold at the peak,
  symmetric fusion goes endoergic (⁵⁶Fe + ⁵⁶Fe costs 30.6 MeV), and
  photodisintegration reverses the ladder at 10¹⁰ K. *Verified:
  `test_fusion_stops_at_iron_but_not_the_way_one_might_guess`.*

### Verification
- **228 tests across the 11 modules, all passing** (`python3 code/test_*.py` in
  each). They reproduce every published table and worked example in scope:
  S&F Table 6.1 (moderators), Table 6.2 (26 spontaneous fissioners, checked
  against themselves through two relations the book never prints), Tables 6.3–6.5,
  Examples 6.1–6.6, and Examples 7.1–7.3. All 20 Q-values printed in §6.7 were
  recomputed from Appendix B; 19 agree to better than 3 keV.
- **11 figure scripts run clean, producing 43 SVGs** + `captions.json`.
- **The appendix extractor re-runs and still passes all its validators**,
  including the cross-check that rebuilds 81 standard atomic weights from
  A.4 + B.1 to within 2.9×10⁻⁴.

### Still to do
- Modules **NE-12..NE-27** (Chapters 7 §§7.3–7.5, and Chapters 8–14) are indexed
  in `NE/list_NE.txt` with directories created, but not yet written.
  *(Superseded later the same day — see the "NE trunk complete" entry above.)*

## 2026-07-14

### Added
- This changelog. Open items tracked in `edits_todo.txt`. Backfill notable
  prior history as it resurfaces.
