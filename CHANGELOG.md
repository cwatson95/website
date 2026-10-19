# Changelog — website

Per-project changelog (policy: Agent repo `CLAUDE.md` → "Per-project
changelogs"). Static hand-written site: no build step, no frameworks, opens
over `file://`. **Don't commit unasked** — delivery is uncommitted files in
the main checkout.

## Known-bad — do not reintroduce
- **A full-viewport overlay above an interactive canvas must set
  `pointer-events: none`** (re-enabling `auto` only on its interactive
  children). The teaching page shipped with the `.page` overlay (z-index 1,
  100vh) silently swallowing every pointer/wheel event — pan, zoom, and
  click-travel were dead while the canvas rendered fine. Fixed 2026-08-12 c.

## 2026-10-14 e — Apollo DSKY: the ascent and the rendezvous now run the real lunar-module computer, Luminary 099; every view runs the flight programs

`simulations/apollo_dsky.html` is updated. Cooper's ask: "Use the virtual AGC to simulate the Apollo flight". The
last view, the rendezvous, now runs the flight program itself, as the others already do: Luminary 099, the lunar
module's program as flown on Apollo 11, on the Virtual AGC project's emulator of the guidance computer, built into
the page. It starts on the surface at 124:10 with what the computer had there, and the crew keys what the
transcripts and the Mission Report give: P12 with the ascent PAD, the go for the engine, the trim of the residuals,
the radar, P32, P33 and P34 with their passes, each burn on P41 with the hand controller, two midcourses in P35, the
braking in P47. The program does the rest: the ascent's steering and cutoff, pointing the radar and weighing its
marks, the targeting of every burn.
- THE PICTURE: P12's climb against the distance flown, with the flight's insertion; the LM seen from the CSM, from
  behind and below to the docking, with the burns where this run flew them.
- AGAINST THE FLIGHT: insertion at 60,703 ft (the best estimate 60,300); P32's CSI 51.6 ft/s (the flight's 51.5);
  CDH within six seconds of the flight's time; TPI half a minute after the time CSI aimed for (the flight's came
  six and a half minutes late); two midcourses of 1.4 and 1.0 ft/s (1.0 and 1.5); station-keeping 50 minutes after
  TPI (48.6); no program alarm.
- Jumps to 40 s before liftoff, the radar, CSI, CDH, TPI and the braking.

One line of the emulator now differs from the published one: its divide lost a count when the lower word of the
dividend was −0, which on the rendezvous threw the computer's estimate of the CSM's velocity off by 29 m/s at a mark
(the Virtual AGC's current source has the same code). The fix moved the other flights a little; the landing now
touches down at 102:45:41 (the flight: 102:45:39.9). The emulator and NASSP are GPL software; the page carries
their source with their licenses. Its card's text says every view runs the flight programs; the count stays 91.

## 2026-10-14 d — Apollo DSKY: lunar orbit insertion now runs the real command-module computer, Comanche 055

`simulations/apollo_dsky.html` is updated. Cooper's ask: "Use the virtual AGC to simulate the Apollo flight". The
way out now runs the flight program itself, as the landing and the entry home already do: Comanche 055, the command
module's program as flown on Apollo 11, on the Virtual AGC project's emulator of the guidance computer, built into
the page. It starts half an hour before the burn behind the Moon, from the memory of Project Apollo - NASSP's
Apollo 11 scenario with the flight's state vector, and the crew keys what the onboard recorder heard: the DAP load,
P30 with the PAD, P40, the go for the engine at V99, the residuals, V82's orbit. The program does the rest: the
attitude it asks for, the test swing of the engine's gimbals, the countdown, the ignition, steering the engine
through its gimbals for six minutes, and the cutoff.
- THE PICTURE: the arrival, the burn and the orbit behind the Moon to scale, where the radio is lost and found; the
  engine's gimbals, where the computer commands them and where they go, against the flight's gauge readings; the
  velocity still to gain on the DSKY, and the thrust.
- AGAINST THE FLIGHT: N42 reads the PAD's 431.3 by −128.2; the burn lasts 356.9 s (the flight: 357.5); V82 then
  shows 170.8 by 60.5 nmi, where the crew read "169.6 by 60.9"; the radio goes behind the Moon and comes back within
  4 s of the PAD's times.
- Jumps to P30, P40, the gimbal test, 40 s before ignition, the cutoff, V82 and the acquisition of signal.

The emulator is free software under the GNU GPL (version 2 or later); NASSP, whose scenario memory the burn starts
from, is GPL v2. The page carries the source of both pieces with their licenses, and a button under "the real
computers" saves them as a file. The rendezvous still runs the page's re-implementation, and the page says so. Its
card's text says what runs where; the count stays 91.

## 2026-10-14 c — Apollo DSKY: the way home now runs the real command-module computer, Comanche 055

`simulations/apollo_dsky.html` is updated. Cooper's ask: "Use the virtual AGC to simulate the Apollo flight". The
entry home now runs the flight program itself, as the landing did since this morning: Comanche 055, the command
module's program as flown on Apollo 11, on the Virtual AGC project's emulator of the guidance computer, built into
the page. It starts 25 minutes before the command module meets the air, from the memory of Project Apollo - NASSP's
Apollo 11 scenario with the day's uplink, and the crew keys what Apollo 11's crew keyed. Then the program does the
rest: P61's target and predictions, the separation from the service module, the turn to the entry attitude, P63,
P64 at 0.05 g, P65's up-control to reach the far target, P67, and its jets.
- THE PICTURE: altitude against the ground flown, coloured by program; the roll the computer commands against the
  roll the command module flies; the load on the crew against the entry monitor's two peaks.
- AGAINST THE FLIGHT: the displays come out as the crew read them (N60 36,185 against 36,184 ft/s; N74 36,276
  against 36,275; N69's 22,048 ft/s against the flight computer's own 22,091), the first peak 6.71 g against the
  entry monitor's 6.73, and the splashdown 1.9 nmi from the target (the flight: 1.69).
- A switch turns on the command module's second jet system, which Apollo 11 left off: the roll logic is written for
  one.

The emulator is free software under the GNU GPL (version 2 or later); NASSP, whose scenario memory the entry starts
from, is GPL v2. The page carries the source of both pieces with their licenses, and a button under "the real
computers" saves them as a file. The way out and the rendezvous still run the page's re-implementation, and the page
says so. Its card's text says what runs where; the count stays 91.

## 2026-10-14 b — Apollo DSKY: the keyboard, the landing and the 1202 alarms now run the real Apollo 11 computer

`simulations/apollo_dsky.html` is updated. Cooper's ask: "Use the virtual AGC to simulate the Apollo flight". Three of
its six views now run the flight program itself instead of the page's re-implementation of it: Luminary 099, the
lunar module's program as flown on Apollo 11, on the Virtual AGC project's emulator of the guidance computer (yaAGC),
compiled to WebAssembly and built into the page. Everything the DSKY shows in those views is the program's.
- THE KEYBOARD: the LM's DSKY in lunar orbit 23 minutes before the descent; what PINBALL is doing, read from its own
  memory; new examples that compute (the orbit with V82, the range to the CSM with V83, the bank sums with V91).
- THE LANDING: the program flies P63 to touchdown, with the LM simulated around it and the crew keying what Apollo
  11's crew keyed; the four-mile navigation error is drawn as where the computer thought the LM was. The arrows take
  the controls.
- THE ALARMS: the 1202s and the 1201 raised by the program itself, with its core sets and VAC areas read from its
  memory as they were at each alarm.

The way out, the rendezvous and the way home still run the re-implementation, and the page says so. The emulator is
free software under the GNU GPL (version 2 or later); the page carries its complete source and license, and a button
under "the real computers" saves them as a file. The page starts its guidance computer asynchronously before it
draws. Its card's text says what runs where; the count stays 91.

## 2026-10-14 a — Special Relativity joins the catalog, 91 sims: muons that outlive their lifetime, and a jet that fits in a shorter hangar

`simulations/special_relativity.html` is new. Cooper's ask: "Under ~/coding/website/simulations/ let us create a
simulation showing special relativity of muons being able to pass through the atmosphere by an "increased" lifetime
due to time dilation. Similarly let us have another tab showing length contraction with the classic idea of a jet
larger than the length of a barn/hanger is able to "fit" near the speed of light." Like its siblings it has a
readout, the calculation beside the views, a self-test that runs headless under jsc (1460 checks), and no network;
it is built from parts in the Agent repo's `projects/simulations/build_sr/` (the assembled page is not the one to
edit).

The quotation marks in the ask are the design: the lifetime is "increased" only in the Earth's account, and the jet
"fits" only in the hangar's. Each effect is told twice, once in each frame, and the relativity of simultaneity is
what makes the two accounts agree. Six views:
- THE DESCENT: a row of muons from one shower, made at PDG's typical 15 km with PDG's example energy, 2.4 GeV, each
  decaying when its own clock reaches a lifetime drawn for it. The Earth's frame (their clocks 22.7 times slow) beside
  the muons' frame (the air 0.660 km thick, rushing up; the Earth's clocks out of step, the ground's already at
  49.99 µs when they are made), on one scale and on the muons' own time; twins without time dilation; the survivors
  against the distance fallen, with the slowing in real air (the US Standard Atmosphere 1976 and PDG's range table)
  dashed: 8.96 km of effective decay length against the review's 8.7.
- MUON SPACETIME: the descent as worldlines, boosted continuously from the Earth's frame to the muon's; the hyperbola
  of 2.197 µs stays where it is and the events slide along it.
- MOUNT WASHINGTON: Frisch and Smith's count (563 ± 10 an hour on the summit, 408 ± 9 at sea level; the film's own
  hour, 568 and 412), the muons' own time read from it (0.71 µs against the laboratory's 6.41), and the descent
  recomputed through this page's air: 393 expected at sea level.
- THE HANGAR: a jet longer than the hangar (six real aircraft, lengths from Wikipedia's specifications), the entrance
  shut behind its tail and the exit opened at its nose: shut together in the hangar's frame, never in the jet's, with
  the doors' and the jet's clocks in both.
- HANGAR SPACETIME: the doors and the jet as worldlines, boosted from frame to frame: the same events on the same
  worldlines, sliced into "now" differently, and the two door events trade places at 0.0541 c for the defaults.
- THE CRASH: the exit stays shut; the stop runs back through the jet at c, and the jet ends crushed to
  L√((1 − β)/(1 + β)), inside, the same jet in the same place in every frame.

Its card sits in Astrophysics & Relativity, before Doppler & Causality. The lede says ninety-one and the meta says
91, and `dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the catalog, and its "COMPLETED
SIMULATIONS" header counts that list again: 85 (the six WIP pages are not in it). The ask was on no list, so
TODO.txt also gains it as a dated DONE line in PHYSICS, after "Time cone, null cone". `simulations/LIST.txt` is
Cooper's file and is not touched.

The readout lies over the picture at phone widths, as it does in every sibling.

## 2026-10-13 a — Apollo DSKY joins the catalog, 90 sims: the guidance computer's keyboard, working, and Apollo 11 flown on it

`simulations/apollo_dsky.html` is new. Cooper's ask: "Look at ~/coding/Agent/Apollo-11/ I want to make a simulation
under ~/coding/website/simulations/ with the LM DSKY interface to educate about how it was used to get to the moon
and back". Like its siblings it has a readout, the calculation beside the views, a self-test that runs headless under
jsc (249 checks), and no network; it is built from parts in the Agent repo's `projects/simulations/build_dsky/`
(the assembled page is not the one to edit).

The DSKY is the Apollo guidance computer's display and keyboard. Its program, PINBALL, is re-implemented routine by
routine with its own tables read from the Apollo 11 listings (Luminary 099 for the lunar module, Comanche 055 for the
command module): the verb and noun names, the register formats and scales, the alarm and checklist codes. Six views
follow the mission, each with a computer running the flight's programs, their displays in the listing's order, and
a crew keying what Apollo 11's crew keyed (or you):
- THE KEYBOARD: the LM's DSKY on the surface; what PINBALL is doing with each key, and every display read back in the
  listing's own words.
- THE WAY OUT: the CM's computer through lunar orbit insertion behind the Moon (P30, P40, V82), with the coast from
  injection and the free return.
- THE LANDING: P63 to touchdown on Luminary's descent guidance law with Apollo 11's own targets, the radar, P64's
  landing point designator and P66, against Aldrin's call-outs.
- THE ALARMS: the 1202 and 1201 inside the Executive: core sets, VAC areas, SERVICER every two seconds, the time the
  rendezvous radar stole.
- THE RENDEZVOUS: the ascent (P12) and the coelliptic sequence as the LM's computer targeted it (P32 to P35, P41), to
  docking.
- THE WAY HOME: the CM's entry from P61 to the drogue chutes (P62 to P67), with its load against the flight's.

Its card sits in Mathematics & Machines, after Logic Gates. The lede says ninety and the meta says 90, and
`dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the catalog, and its "COMPLETED
SIMULATIONS" header counts that list again: 84 (it said 88, the catalog's count before Granulation; the six WIP
pages, not counted as finished, are not in the list). The ask was on no list, so TODO.txt also gains it as a dated
DONE line. `simulations/LIST.txt` is Cooper's file and is not touched.

The readout lies over the DSKY at phone widths, as it lies over the picture in every sibling.

## 2026-10-11 g — Granulation: switching to the walls crashed the draw

Cooper: `TypeError: Cannot read properties of undefined (reading 'I') at drawWalls`. The frame's model was memoised
when the surface view built it (overhead image only); a click on the walls or the cut then drew from that cached
model without the inclined image or the slice, and while the clock was paused the cache never cleared at all.
`completeModel` now fills in whatever the current view needs on every call (the inclined image keyed on μ, the
slice keyed on the row, the mean profiles for the model view), so a view can change between the build and the draw.
Self-test: 259 checks (the completion exercised with a stub model: the surface asks for nothing, the walls fetch
once and keep it, a new inclination or row refreshes, both views draw). Verified in the browser through every
view switch, paused and running.

## 2026-10-11 f — Granulation joins the catalog, 89 sims: the Sun's surface convection computed live on the GPU

`simulations/granulation.html` is new. Cooper's ask: "simulate the thermoforming process that causes the bubbles and
striations on the surface of the sun", after the NSO release on the Inouye telescope's ultra-fine striations
(Kuridze et al. 2025, ApJL, arXiv:2505.03965). Like its siblings it has a readout, the calculation beside the views,
a self-test that runs headless under jsc (252 checks), and no network; built from scratchpad parts (the sprite
page's stylesheet and utilities verbatim; its own physics, solver, shaders, drawing and prose); the assembled page
is the one to edit.

What it computes, as you watch: a 3-Mm patch of the surface layers, 1.5 Mm deep (−1.2 to +0.3 Mm), as a
radiation-magnetohydrodynamic model on a 96²–256² × 80–112 grid, in WebGL2 fragment shaders over 2-D atlases of
the 3-D state (one tile per layer). The gas: H and He ionising by Saha with the metals as electron donors, on a
128 × 224 table in (log ρ, log e). The opacity from the cross-sections: H⁻ bound-free (Wishart, Gray's polynomial)
and free-free (Bell & Berrington), hydrogen bound-free and free-free, Rayleigh and Thomson; the Rosseland mean by
quadrature over 96 frequencies for the transfer, the 430-nm value for the image. Grey transfer on eight rays
(μ = ±1/√3 at four azimuths), each ray shifted sideways per layer with the intensity resampled, by short
characteristics with a linear source; the heating is what each ray loses in the cell (conservative), so the
granules warm the lanes sideways. The flow: finite volume, van Leer / MC reconstruction of the primitives scaled by
a discretely hydrostatic reference (the stratified rest state is an exact solution), HLLC fluxes for the gas and
HLL with Dedner's GLM for the field, the Lorentz force as a Boris-limited source with its work, gravity's work from
the same mass fluxes that move the mass, the magnetic dissipation returned as heat, SSP-RK2 at 0.45 of the Courant
limit. Images at 430 nm along vertical and inclined rays with the τ = 1 crossings (height, B_z, v_z, T).

Four views on one clock in solar time: THE SURFACE (the continuum from above, or B_z, v_z, the height of τ = 1, T
at τ = 1); THE WALLS (the same window from above and from μ = 0.85, magnified 1–4×, with cross-cuts of I, B_z and
the τ = 1 height across the stripes: the paper's figure 7); THE CUT (a vertical slice: T, density contrast, |B| or
v_z, the τ = 1 surfaces for vertical and inclined rays, |B| contours, the flow, a fan of inclined sightlines each
ending where its τ reaches 1 and coloured by what it sees); THE MODEL (⟨T⟩(z) against the start, the enthalpy and
kinetic fluxes against σT⊙⁴, the histories, the checks).

The hard part was the energy budget, and it is worth recording:
- An internal-energy formulation leaked ~40 % of the flux through the mismatch between upwinded advection and the
  centred −p∇·v. Replaced by the conservative hydrodynamic total energy E = e + ρv²/2 (the kinetic dissipation then
  heats automatically), with gravity's work taken from the face mass fluxes so it telescopes against the potential
  energy; a closed box now keeps its energy to 2 × 10⁻⁴ of the kinetic.
- Vertical-only two-stream transfer left the lanes unheated; the eight-ray transfer fixed the contrast (27 → 20 %).
  The horizontal flux divergence must be the ray-deposition form, not the vertical divergence plus a cell-centred
  horizontal flux (that gave dipole artefacts at sharp edges).
- The deep adiabat pinned to the grey model's own τ = 1 point carried too little entropy (that point sits at twice
  the Sun's photospheric density for want of line opacity), and the box radiated 5000 K whatever the resolution or
  limiter. It is now pinned to Model S (Christensen-Dalsgaard et al. 1996, the model sun.html uses) 1203 km down:
  15,289 K at 3.954 × 10⁶ dyn/cm²; the start follows a steep boundary layer into Model S's T(p) and the adiabat
  below 700 km. With it the box settles in 15–20 solar minutes to T_eff ≈ 6050 (96²) / 6090 K (128²), ⟨T⟩(τ=1) ≈
  6350 K, rms contrast 24 %, kilogauss sheets in the lanes (≤ 2.7 kG), the surface depressed 100–200 km in them.
  The slider shifts the adiabat ±30 %.
- The Boris limit is height dependent (20 km/s at the surface, +20 km/s per 100 km below) so the sheets below the
  surface feel the full Lorentz force; a uniform limit let the field exceed equipartition.
- The browser pane throttles timers when hidden; the page steps the model from a setInterval with a wall budget and
  draws on requestAnimationFrame.

Known limits (on the page): grey transfer, LTE continuum only (no G-band CH lines), closed sponged top at 300 km
and closed bottom at 1.2 Mm with the adiabat enforced in the lowest 100 km, 12–31 km cells against MURaM's 7 (the
striations here are 2–4 cells wide), T_eff a few per cent above the Sun's.

Catalog: card in the Astrophysics group after Lightning; lede and meta say eighty-nine; `dev/check_sims.py` WORDS
gains 89; TODO.txt lists it under the astrophysics entries.

## 2026-10-11 e — Lightning: the dissipating storm earns its place; the leader grows every tip at once

Cooper: "The dissipating storm seems unnecessary as nothing occurs visually." Two causes, and a bug under them.

- **The storm chips pick the flash.** Choosing a storm now sets the flash it makes (mature and sheared → −CG;
  dissipating → +CG with 150 ms of continuing current; winter → upward from the tower, 100 ms), so a storm never
  sits on a flash type it cannot produce.
- **The channel keeps growing after the strike.** The attached channel is grounded (every element at 0 V), every
  branch end wakes, and the cloud ends go on growing for max(continuing current, 60 ms): the J and K processes
  between strokes, and under the stratiform deck the negative end crawling along the positive layer — NSSL's
  spider lightning, 10–11 km of it at the default from a strike under the middle of the deck, lit as it grows and
  classified when it passes 8 km (the post-strike growth runs fewer, longer channels: 6 tips, branching 0.04). The
  stratiform layer is nine 4-C spheres along 4.8 km (36 C in all) with the cloud base at 4.3 km, so the crawl shows
  under the deck as the photographs have it; the +CG origin is the lowest positive charge nearest the middle.
- **The bug.** The origin element was identified as "element 0", but the tower's own elements come first whenever
  the tower is 125 m or taller — the default — so the bidirectional leader never grew its second end in any flash.
  Fixed by reference. With both ends growing, one-cell-per-step growth starved the ground end (the in-cloud end
  sits in the stronger field), so the growth loop is now synchronous: every live tip steps when its time comes at
  its own speed, picks among its own neighbours by (ΔU − U_c)³, dies when none will do, and leaves a branch with
  probability 0.1 per step, at most 8 tips alive, 600 elements in all. The mature −CG now strikes at 51 ms with
  20 branch points and 10 km of channel; the self-test checks that both ends grow, that after the strike every
  element is at the ground's potential, and that the stratiform flash's negative end crawls past 8 km.
- Self-test: 801 checks.

## 2026-10-11 d — Lightning joins the catalog, 88 sims

`simulations/lightning.html` is new. Cooper's ask: "let us now make simulations for the other types of lightning
under a new sim lightning.html. Information from https://www.nssl.noaa.gov/education/svrwx101/lightning/types/".
The page follows NSSL's taxonomy and quotes its figures (5–10 cloud flashes per ground flash, 50-yard steps,
60,000 miles/s, 1–20 strokes, +CG's single stroke and continuing current, the 6-mile bolt from the blue, elves of
300 miles, jets to 25–35 miles). Like its siblings it has a readout, the calculation beside the views, a self-test
that runs headless under jsc (795 checks), and no network; built from scratchpad parts (the sprite page's
stylesheet, utilities, atmosphere, bands and optics verbatim; its own engine, drawing and prose); the assembled page
is the one to edit.

Four views on one clock in milliseconds, switched by the tabs (no journey):
- **The storm.** Four storms as uniformly charged spheres with their images in a conducting ground: the mature
  tripole (+40 C at 10 km, −40 at 6.5, +3 at 4.3), a sheared storm with the anvil's positive 5.5 km downwind, a
  dissipating storm's stratiform region (a +60 C layer at 5.5 km under −30 C), a low winter storm over the tower.
  The map is |E| against the relativistic-runaway threshold 284 kV/m × n/n₀ (magenta rings the region past it); the
  strongest field (298 kV/m in the mature storm, 2.4 E_th and 0.21 E_k: what balloons measure, and the initiation
  puzzle) and the avalanche's e-foldings ∫dz/λ with λ = 7.3 MV/(E − E_th); the field mill's potential gradient along
  the ground (−6.9 kV/m under the mature storm, +14 under the stratiform deck, −34 under the winter storm).
- **The flash.** A leader grown in that field. Each cell is a 125-m channel element with a 1-m sheath; the coupling
  matrix (Coulomb with images, a line's self term) gets a Cholesky row per element; all floating elements sit at
  one potential fixed by zero net charge (Kasemir's bidirectional leader), grounded ones at 0; a tip grows into the
  neighbouring cell with probability (ΔU − U_c)^4 where ΔU is the potential drop over the step, U_c = 6 MV for
  negative and 3 MV for positive tips at 4 km (positive leaders run in weaker fields). Upward leaders start from
  the tower (height a slider), a 20-m tree and an 8-m house when the potential at their tips passes Rizk's
  1556 kV/(1 + 3.89 m/h). Attachment, then return strokes at c/3 lighting the tree after d/v, dart leaders at
  10⁴ km/s relighting only the main channel, 60-ms log-normal intervals, Heidler currents (30 kA first, 12 kA
  after; 5 and 1.5 C), continuing current 200 A; a strip shows the channel-base current (√ scale) and the light.
  The outcome is classified as NSSL does from what the leader did: −CG (the mature storm, striking the ground in
  ~38 ms with ~14 branch points), +CG (the stratiform region, one stroke), upward (the winter storm's tower; a
  300-m tower under the mature storm fails Rizk's test and the page says so), intracloud (the mature storm's IC
  leader, 200 elements, never leaves), cloud-to-air, bolt from the blue (≥ 2 km outside the cloud), spider (> 8 km
  along the deck). Channels inside the cloud are diffused into the sheet.
- **Far away.** The storm at D on the round Earth (R = 7/6 R⊕ for refraction): what lies under D²/2R is hidden,
  so beyond ~120 km only the cloud lights up. Sound rays from the channel as circles of radius c/|dc/dz| in the
  lapse rate, the grazing ray's reach √(2Rh) (26 km from 4 km, 33 from 6 at −6.5 K/km) and the shadow zone: NSSL's
  heat lightning; an inversion removes it. The flash-to-bang delay at c(T); the flash's colour after the path
  (Rayleigh + haze over the 8-km scale height at the 1-km density): white at 5 km, reddish at 50.
- **Above the storm.** A blue jet (100 km/s to 42 km) and a gigantic jet (120 km/s to 50 km, then 10⁴ km/s to
  88 km) as cones coloured by height with the sprite page's band quenching, so blue below 50 km and red above; the
  sprite and the elve for scale, pointing to Red Sprites; a gamma-ray beam where the avalanche gives ≥ 5
  e-foldings in the flash's first 8 ms (indicative).

Known limits, stated on the page: the floating leader carries ~0.05 mC/m (a cloud-connected one ~1); no field
change from the flash itself; the cone angles are drawn; the TGF threshold is indicative. Its card sits in
Astrophysics & Relativity after Red Sprites. The lede says eighty-eight and the meta 88; `dev/check_sims.py` gains
the word; `simulations/TODO.txt` gets the ask under PHYSICS as DONE and the page under COMPLETED, now 88.
`simulations/LIST.txt` is Cooper's file and is not touched.

## 2026-10-11 c — Red Sprites: the frame is a slider and short by default, a tone curve, a light curve

Cooper, on the 33-ms default of 2026-10-11 b: "It shouldn't be static, I wanted more than just the intensity of 1
unit." With the whole event inside the frame the camera views stood still while the clock ran, and the hard clamp
flattened the bright columns to one level.

- **Frame length** is a slider in "the cameras", 50 µs to 33 ms, default 0.5 ms (a high-speed camera): the heads
  run, the channels fade behind them, the columns linger; slide it to 33 ms and the photograph comes back. The chip
  pair is gone.
- **Auto-gain and a soft shoulder.** The collected light is normalised by the frame length between 60 µs and 1 ms,
  so short frames are not dark, and the response is 1 − e^(−x) (film's shoulder) with twenty alpha levels, so the
  columns keep their gradation instead of clipping at one.
- **A light curve** at the bottom left of both camera views: the whole sprite's instantaneous light against time
  (every third segment, weighted by band yield and column width, relative to its peak) with the halo's curve dotted,
  the frame's window shaded and "now" marked. The readout gives the sprite's light and the halo's as a percentage
  of their peaks. The halo peaks before the streamers, as photometers see.
- Self-test: 897 checks (the light curve: dark before the streamers, peaking within 3 ms of them, the halo first,
  faded four ms after the last streamer).

## 2026-10-11 b — Red Sprites: the journey removed, the sprite rebuilt as a cluster after Cooper's photograph

Cooper: "Remove the 'journey' mechanism. I don't like it jumping over the place. I also included sprite.avif that I
was hoping to recreate." `simulations/sprite.avif` is his reference (a jellyfish sprite from the ground: bright
upward columns under a diffuse red glow, a wide skirt of fine tendrils drooping outward); it is not referenced by
the page and is not a catalog file.

- **No journey.** The follow checkbox, the chapter clock and the view switching are gone; "the clock" group has
  play/pause, from the start, the time slider and the playback rate, and the tabs (or 1–4) are the only way the view
  changes.
- **A cluster.** "the sprite" group gains "elements in the cluster" (1–40, default 20). The elements are seeded
  uniformly over the breakdown region at the onset (the radius where E/E_k falls under 1 on the streamers' grid,
  ×0.9; 25 km at the default), each born within 0.6 ms of the first, each with a positive streamer down and a
  negative one up, 80 tips per element and 60,000 segments in all. The downward tendrils splay away from the
  cluster's centre with depth (SPLAY = 0.35), standing in for the channels' mutual repulsion, which the model does
  not have; the page says so. The upward columns are drawn 2.2× wider and 1.6× brighter (assumed), and the heads
  bloom. The default ground camera narrows to 12° so the cluster fills the frame as in the photograph.
- **Rendering.** The tens of thousands of segments are bucketed by quantised colour, alpha and width and drawn as
  one path per bucket (two passes: channels normally, heads additively), and the camera views get a cheap bloom —
  the canvas added to itself through 1/6 and 1/18 copies — drawn before the labels. The halo is drawn broader, over
  the cluster and a little above it.
- **Exposure.** A photograph integrates its whole exposure, which is why the tendrils and the columns appear
  together in Cooper's picture while the instantaneous model has the tendrils fading before the columns peak. The
  cameras gain a chip: a 33-ms video frame (default) or an instant. With the frame, each segment gives its head's 60 µs
  plus the channel's ∫e^(−t/τ_g)dt over the window (the upper channels, τ_g up to 3 ms, outweigh the tendrils at a
  tenth of that), and the halo, the flash and the elve are taken over the window too. The cross-section stays
  instantaneous. The default ground camera is 10°.
- **Fixed on the way.** The tree's memo key lacked the element count, so changing it returned the old tree; the
  segment cap could be overshot by one step. Self-test: 892 checks pass (eight new cluster and exposure checks).

## 2026-10-11 a — Red Sprites joins the catalog, 87 sims

`simulations/red_sprites.html` is new. Cooper's ask: "Let us make a simulation of the red sprite lightning. It would be
nice to see it simulated like through dielectric/ground media as well as from space." Like the other astrophysics pages
it has a readout, the calculation beside the views, a self-test that runs headless under jsc (788 checks), and no
network. It is built from scratchpad parts (the head, solar_winds.html's stylesheet and number utilities verbatim, its
own physics and drawing); the assembled page is self-contained and is the one to edit from now on.

Four views on one clock in milliseconds; the journey plays them in turn and pressing a tab stops it following:
- **The stroke.** The storm in cross-section, a positive cloud-to-ground stroke removing Q from height h as
  Q(1 − e^(−t/τ_s)), and the field in the air above as the quasi-electrostatic solution of
  ∂_t(ε₀∇·E) + ∇·(σE) = source in a horizontally stratified conductor over the ground: a Hankel transform in r (64
  wavenumbers to 0.3 km⁻¹) and a backward-Euler tridiagonal solve in z (1-km nodes to 110 km, a conductor) for each,
  on a quadratic clock of 320 steps. Everything is linear in Q, so the solution is for one coulomb and scaled. With
  σ → 0 it reproduces the charge and its image series between the two conductors to 0.3% (checked). The map is
  |E|/E_k on a log scale with the breakdown contour and the two streamer stability contours (0.14 and 0.39 E_k),
  arrows along E, the image charge ghosted in the ground, the relaxation-time ladder ε₀/σ on the right, the halo,
  the elve passing at 90 km, and the streamers.
- **The medium.** σ(z), τ = ε₀/σ and E_k = 3.2 MV/m × n/n₀ (US Standard Atmosphere 1976) against height, the
  live |E| profile with the breakdown band shaded, the avalanche-to-streamer time t_form = 20 ns × n₀/n (assumed), and
  E/E_k against time at 55–85 km on a square-root time axis with the streamers' onset marked. Chips: night/day (the D
  region 20× more conducting above 55 km by day), a conducting ground (φ = 0) or an insulating one (φ̂′ = kφ̂, the
  bare charge, about 3× the field aloft).
- **From the ground.** A pinhole camera at distance D on a round Earth looking up at the sprite: the horizon from
  the camera's height, the cloud tops below it beyond 390 km, the stroke's light spilling over, the elve, the halo
  and the streamer tree in 3-D, each segment coloured by the quenching of N₂ first positive (half quenched at 53 km),
  N₂ second positive (30 km) and N₂⁺ first negative (48 km) — red body, violet-to-blue tendrils — then dimmed per
  channel by the air on the slant path: Kasten & Young's airmass, Hansen & Travis's Rayleigh depth and an Ångström
  haze term. At 450 km the red keeps 28% and the blue 4%, which is the page's answer to why they are *red* sprites.
  A checkbox takes the air away.
- **From space.** The same scene from an orbit at 420 km: the limb (its depression acos(R/(R+H)) = 20.3°), the
  airglow layer at 85–100 km as the limb of a shell 2° above the hard limb, the lit cloud, the elve as the ring
  r = √(c²t² − (z_e − h)²) that starts out faster than light, and the sprite — against the dark Earth from 800 km,
  climbing above the limb into the airglow band from beyond about 1100 km (the readout gives its depression). No
  extinction from orbit, and the page says so.

The streamers: initiation where E > E_k has held for t_form (73 km, 0.78 ms after the stroke begins at the default),
positive streamers along E at 10⁷ m/s × (E/E_k)/0.5 (clamped), negative ones against it, a seeded random walk with
branching, dying where E falls under the stability field — so the tendrils stop near 51 km and the top near 85. The
sprite develops in about 2 ms; the channel afterglow is 1 ms × n(70 km)/n (assumed). "another sprite" reseeds it.

Defaults: Q = 250 C from 8 km in 0.5 ms (2000 C·km), a 120-kA return stroke, night, conducting ground, cameras at
450 km (18° field) and 800 km (30°). The readout gives the least charge moment that makes streamers with this stroke
(1100 C·km) and the diffuse onset (980 C·km); the prose says the observed threshold is lower and why (Qin, Celestin &
Pasko 2012: the streamers' own charge, not modelled here). Everything assumed is listed in the file's header comment.

Its card sits in Astrophysics & Relativity, after Solar Winds. The lede says eighty-seven and the meta says 87, and
`dev/check_sims.py` gains the word. `simulations/TODO.txt` gets the ask under PHYSICS as DONE and the page under
COMPLETED, now 87. `simulations/LIST.txt` is Cooper's file and is not touched.

## 2026-10-08 b — Solar Winds joins the catalog, 86 sims

`simulations/solar_winds.html` is new. Cooper's ask: "make a new simulation titled solar_winds in which we start
with a closed magnetic field extending from the sun that pinches off like generating a propagating wave that then
travels to earth and get converted into the auroras". It answers the to-do's "Aurora Borealis and solar wind,
magnetic fields", which is marked done in place. Like the other astrophysics pages it has a readout, the
calculation beside the views, a self-test that runs headless under jsc (591 checks), and no network.

Four views on one clock. The journey plays them in turn, and pressing a tab stops it following:
- **The pinch-off.** An arcade (a line dipole under a flattened surface) and a flux rope (a line current with its
  image). The rope's flux is raised over three hours until its equilibrium curve has no more room (the nose), and
  then it erupts. The contours of the flux function show the X-point where the loops pinch off: magenta loops
  leave with the rope, and orange flare loops stay below. The eruption is RK4 with gravity and, beyond 20 R,
  Vršnak's drag. Energy is conserved to 1e-5 out to 20 R.
- **The crossing.** The rope as a magnetic cloud (Lundquist's force-free field) seen end on, with its shock
  (Rankine–Hugoniot) and sheath. Below it, |B|, B_z and the speed a spacecraft at the Earth measures. The field
  over the rope on the Sun sets whether B_z turns south then north, or the reverse.
- **The magnetosphere.** Shue et al.'s magnetopause and the bow shock. The dipole's closed lines, and its open
  lines swept into the lobes. The Dungey cycle opens flux at Milan et al.'s dayside rate and closes it again with
  a one-hour nightside relaxation (assumed). Dst follows O'Brien & McPherron.
- **The aurora.** The oval round the open flux, seen from above the magnetic pole, with night shading and eight
  cities turning under it. The curtain is drawn where it truly stands as a chosen city sees it. The green, red and
  blue lines come from a Maxwellian's energy deposit (Rees's range) times each metastable's survival against
  quenching, using JPL rates on an approximate US Standard Atmosphere.

The defaults give a 1470 km/s CME, the shock at the Earth after 34 h, Dst −136 nT, and the oval down to about 50°
magnetic around local midnight over Chicago. Everything assumed is listed in the file's header comment and named on
the page.

Its card sits in Astrophysics & Relativity, after The Sun. The lede says eighty-six and the meta says 86, and
`dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page, and its "COMPLETED SIMULATIONS" header
now gives the actual count, 86 (it had said 79). `simulations/LIST.txt` is Cooper's file and is not touched.

The page's hint sits bottom right. In `sun.html` the hint lies over the canvas caption at some sizes, and that is
still so there.

## 2026-10-08 a — The Sun: the CME out of the Sun view, and scroll to zoom

Cooper's asks: "remove the CME from sun.html it detracts from the simulation" (the Sun view only, when asked), then
"Make it so that we can zoom in with the scroll wheel". The Sun view loses its CME shell, the CME checkboxes, its
time slider, and its readout, caption, legend and hint lines. The corona and wind views keep their CME. The 3-D
Sun now zooms toward the cursor from 1× to 12× with the wheel or a pinch, and "turn it back" resets it. The
self-test gains a check that the point under the cursor stays put, and two zoomed views.

## 2026-10-07 a — The Sun joins the catalog, 85 sims

`simulations/sun.html` is new. Cooper's ask: "Under ~/coding/website/simulations/ and copying the format of
earth_interior.html make one for the Sun. Include Coronal Mass Ejections as a feature". It answers the to-do's
"Solar cycle/ Nucleosynthesis of Solar cycle" (the cycle, and the burning in the core), which is marked done in
place. "Aurora Borealis and solar wind, magnetic fields" stays open: the page has the wind but no aurora. It is
built like The Earth's Interior: six views, a readout, the calculation beside them, data from the measuring
institutions, and no network, so it opens over `file://`.

Six views:
- **The Sun.** Model S cut open to scale: the core where 99 % of the light is made, the radiative zone and the
  convection zone, or a quantity, or HMI's rotation on the cut. The surface in white light with a rotation's
  spots, or as its field. The corona's field is a potential field from that surface, and a CME rises as
  Thernisien's shell.
- **The core.** The burning computed stage by stage from Solar Fusion II's rates against Model S's own, with the
  Gamow peaks, the hydrogen burnt and the ³He built. Also the transport (where convection takes over), and the
  neutrinos against B16, Borexino and SNO.
- **The waves.** A sound wave's ray through Model S and HMI's 2114 modes on the l–ν diagram. The ridges are
  computed from Duvall's law. The f mode is a surface wave and has its own curve.
- **The cycle.** SILSO's sunspot number since 1749 and the butterfly diagram 1874–2016. WSO's polar fields are set
  against a flux transport model fed only by the spots: it reverses within 0.7 years of WSO's four reversals.
- **The corona.** A synthetic LASCO C2 or C3 image of the CME, from the Earth or from the side (a halo when it
  heads for the Earth). Its height against time shows the projection effect. The torus instability starts the
  eruption, and LASCO's 43,294 CMEs are shown by speed and by year.
- **The wind.** Parker's wind and its spiral in the ecliptic. The CME's front travels by a drag model fitted to the
  171 CMEs Richardson & Cane tie to LASCO; one fit for all makes the fastest far too slow, and the page says so.

Its card sits in Astrophysics & Relativity, after The Earth's Interior. The lede says eighty-five and the meta says
85; `dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the catalog and marks the solar
cycle item done, and its "COMPLETED SIMULATIONS" header counts the list. `simulations/LIST.txt` is Cooper's file
and is not touched.

## 2026-10-06 b — Logic Gates joins the catalog, 84 sims

`simulations/logic_gates.html` is new. Cooper's ask: "Make a simulation for basic boolean logic gates. Make the gates
and introduce a swtich-gate/memory-circuit, then introduce a simple adder then subtractor". It was on no list, so
`simulations/TODO.txt` gains it as a dated DONE line in CIRCUITS. Every circuit on the page runs gate by gate, each
gate one unit of delay, so a change can be watched travelling through it. No network: it opens over `file://`.

Six views:
- **The gates.** NOT, AND, OR, NAND, NOR, XOR and XNOR, with their truth tables, each built again from NANDs alone.
- **Switches.** Switches in series and in parallel light a lamp as AND and OR (Shannon 1938). CMOS NOT, NAND and
  NOR are shown as their pull-up and pull-down transistor networks. The transmission gate is a switch that keeps
  its value when opened.
- **Memory.** The SR latch, two gates holding each other (and oscillating when S and R are released together),
  the gated D latch, and the edge-triggered D flip-flop, with timing diagrams.
- **The adder.** Half and full adders and an n-bit ripple-carry adder. The carry ripples two gate delays a bit, and
  the sum read too early is wrong.
- **The subtractor.** Half and full subtractors, a borrow chain, and subtraction on the adder as A + ¬B + 1, with
  the signed overflow flag.
- **The accumulator.** A register and an adder that add X at every clock edge (a counter when X = 1). It has a
  fastest safe clock: 2n + 4 gate delays for n ≥ 3. Faster than that, adds go wrong, and a latch can be caught
  ringing between 0 and 1.

Its card sits in Mathematics & Machines, after Green's Functions & the Wronskian. The lede says eighty-four and the
meta says 84; `dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the catalog and adds the
request as done, and its "COMPLETED SIMULATIONS" header counts the list. `simulations/LIST.txt` is Cooper's file
and is not touched.

The build is in the Agent repo at `projects/simulations/build_logic/`, uncommitted, beside the other builds. It was
built on the Agent worktree branch `worktree-logic-gates`, which is not pushed.

Verified:
- selfTest 1181 passed, 0 failed; the UI drive 221 passed, 0 failed; 17 scenes, 0 layout problems; 70 mutants, all
  caught. An independent Python gate simulator agrees with every truth table, sum, difference and timing the page
  prints.
- At the destination `verify_dest_20261006b.py` (in the Agent build) checks the page byte for byte, runs its
  selfTest and UI drive from this copy, and runs `dev/check_sims.py` on a staged tree.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-10-06 a — The Kardashev & Barrow Scales joins the catalog, 83 sims

`simulations/kardashev_barrow.html` is new. Cooper's ask: "Under ~/coding/website/simulations/ let us make a
simulation for the kardashev scale and the barrow scale". It was on no list, so `simulations/TODO.txt` gains it as a
dated DONE line at the end of PHYSICS. The page ranks civilizations outward by the power they command (Kardashev
1964, Sagan 1973) and inward by the smallest thing they can control (Barrow 1998), and works out the physics on the
way. No network: it opens over `file://`. Every number on it is computed on the page, apart from the sources'
printed values and the words it quotes.

Six views:
- **The ladder.** Power on one log axis from a person's food to 10¹¹ Suns, with Kardashev's three types as he
  printed them, Sagan's continuous K = (log₁₀ P − 6)/10, and what is physically there. Kardashev's Type I was Earth
  in 1963 (4 TW). Humanity in 2025 (20.3 TW, Our World in Data) is five times that and K = 0.73.
- **The climb.** World primary energy 1800-2025 on a log axis, a fitted growth rate (1.94 % a year over
  1965-2025), and steady growth from 2025 to each type. Kardashev's own 1 % sums come out at 3224 and 5756 years;
  he printed 3200 and 5800.
- **The heat.** The warming from waste heat alone: +0.012 K today, +5.7 K at Sagan's Type 1.0, and the oceans boil
  at 2.2 × 10¹⁷ W, 470 years away at 2 % a year.
- **The sphere.** A Dyson shell or swarm: its temperature (394 K at 1 au around the Sun), the spectrum an astronomer
  sees with its infrared excess, and Jupiter spread over it (1.2 m thick).
- **The galaxy.** A colonization front, d/(d/v + tₛ), across the Milky Way's disc. At 1 % of c, with 10-ly hops and
  1000 years to settle, half the stars are reached in 5.9 million years.
- **Inward.** Barrow's types I-minus to Ω-minus on an axis of length, his verdicts on us quoted from his book, and
  what it takes to see a length with protons: a ring, its synchrotron loss, a straight machine and the power to
  keep one proton circulating, against the Kardashev ladder. The Planck length needs a ring 3250 light years
  across at the LHC's 8.33 T, whose protons would radiate 10²⁰ times their energy every turn, or a straight
  machine 81 000 light years long.

Its card sits in Astrophysics & Relativity, after The Intrinsic Hamilton–Jacobi Equation. The lede says
eighty-three and the meta says 83; `dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the
catalog and adds the request as done, and its "COMPLETED SIMULATIONS" header counts the list.
`simulations/LIST.txt` is Cooper's file and is not touched.

The build is in the Agent repo at `projects/simulations/build_kardashev/`, uncommitted, beside the other builds.
It was built on the Agent worktree branch `worktree-kardashev-barrow`, which is not pushed.

Verified:
- selfTest 1119 passed, 0 failed; the UI drive 212 passed, 0 failed; 13 scenes at three sizes, 0 layout problems;
  88 mutants, 88 caught; all 12 quotations found in their sources.
- At the destination `verify_dest_20261006a.py` (in the Agent build) checks the page byte for byte, runs its
  selfTest and UI drive from this copy, and runs `dev/check_sims.py` on a staged tree.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-28 c — The Miraculous Staircase joins the catalog, 82 sims

`simulations/miraculous_staircase.html` is new. Cooper's ask: "let us simulate the stability of the Miraculous
Staircase in Sante Fe through Free body diagrams showing its amazing engineering". It was on no list, so
`simulations/TODO.txt` gains it as a dated DONE line at the end of PHYSICS. The Loretto Chapel's staircase (built
1877–1881) climbs two full turns with no post up its middle. The page solves it as a 3-D frame of two helical
stringers and 32 treads and shows it as free bodies. No network: it opens over `file://`, and every number on it is
computed on the page, apart from the dimensions, the wood's properties and the words it quotes from its sources.

Six views:
- **The staircase.** The whole stair as one free body: its weight, the person or the people, the railing, and every
  support's force and moment, with a signed bar chart of the supports' vertical pushes. The weight lies inside the
  inner feet, yet every end that holds it up is on one side of the axis. So the inner ends push up more than the
  load and the outer ends pull down. The tipping is answered by the vertical pushes, the sideways pushes and the
  ends' moments, in computed shares.
- **One tread.** A tread cut free: the stringers' pushes and moments against a plank on two knife edges, and the
  shear and bending moment along it. Hinged at the stringers it is that plank exactly; with the inner stringer
  taken away it is a cantilever.
- **A cut.** The stair cut through both stringers between any two treads, either part as the free body, and each
  stringer's axial force, shears, twist and bending moments along its whole length. The inner stringer stands on
  the floor and hangs from the loft; the outer one pulls the other way.
- **What holds it up.** One change at a time: the loft let go, the ends pinned, the treads hinged, the inner
  stringer taken away, the bracket added.
- **The helix.** One stringer as an open-coiled spring, its four ways to give against the radius, and two stringers
  tied, against Tománek and Every's double-helix formula.
- **Buckling and bounce.** The six lowest natural frequencies against the pace of feet on stairs, and the first
  buckling load factor, with their shapes.

Checks:
- **Sources.** Two findings files of byte-checked quotes (178 on the staircase, 188 on the theory), from the
  chapel's pages, Nickell (1998), the Santa Fe Daily New Mexican of 5 January 1895, Tománek and Every (2017), Sumali
  (2021), the Wood Handbook, the 2012 IBC and Andrade et al. (2020). Every quotation the page prints is found in them
  or in the saved sources (`check_page_quotes.py`).
- **Twins.** `build_stair/fe_twin.py` (numpy and scipy, dense, no shared code) solves sixteen configurations. The
  page agrees with it to 1e-9 in the largest displacement, the frequencies and the buckling factor, to 5e-9 of the
  weight in every reaction, and in every displacement of the default. `derive_checks.py` pins the closed forms to
  sympy and mpmath. The chords differ from exact helical arcs by 0.27 % of the largest displacement.
- **Found by them:**
  - With a person on step 16, the inner feet push up 1.38 times the whole load.
  - Tománek and Every's lock is real only if the feet are held: rigid treads and held feet come within 3.2 % of
    their formula, while the frame as built, hung from the loft, is 42 times softer.
  - The strengths Sumali set beside her stresses (2.0 and 4.0 MPa) are the Wood Handbook's across the grain. Along
    it they are 30.9 and 38.7 MPa, and the bare frame under her load and on her dimensions reaches 15.7 MPa, 51 % of
    Engelmann spruce's.
  - The lowest frequency is 4.53 Hz, which twice a climber's pace reaches. The railing's weight (Sumali's rough 200
    N/m) brings it to 2.78 Hz, inside the pace itself; the bracket alone lifts it to 8.30 Hz, and railing and bracket
    together, as the stair stands today, give 5.14 Hz.

Its card sits in Mechanics & Control, after Brachistochrone. The lede says eighty-two and the meta says 82;
`dev/check_sims.py` gains the word. `simulations/TODO.txt` lists the page in the catalog and adds the request as
done, and its "COMPLETED SIMULATIONS" header counts the list. `simulations/LIST.txt` is Cooper's file and is not
touched.

The build is in the Agent repo at `projects/simulations/build_stair/`, uncommitted, beside the other builds. It was
built on the Agent worktree branch `worktree-miraculous-staircase`, which is not pushed.

Verified:
- selfTest 1153 passed, 0 failed (jsc and osascript); the UI drive 219 passed, 0 failed; 17 scenes at five sizes, 0
  layout problems; 125 mutants, 124 caught and one declared equivalent.
- At the destination `verify_dest_20260928c.py` (in the Agent build) checks the page byte for byte, runs its
  selfTest and UI drive from this copy, and runs `dev/check_sims.py` on a staged tree.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-28 b — Newtonian & Non-Newtonian Fluids joins the catalog, 81 sims

`simulations/non_newtonian_fluids.html` is new (Cooper's ask: "Let us make a
simulation over Newtonian and Non-newtonian fluids"; it was on no list, so
`simulations/TODO.txt` gains it as a dated DONE line at the end of PHYSICS).
A Newtonian fluid has one viscosity; every other fluid on the page departs
from that in one way: by the rate of shearing, by time, by crowding or by
history. No network: it opens over `file://`, and every number on it is
computed on the page, apart from the measurements and fits it quotes
from its sources.

Six views:
- **The rheometer.** A sample sheared between plates, and the viscosity,
  stress and local flow index against the rate on log axes: blood
  (Carreau–Yasuda and Casson), a ketchup base (Herschel–Bulkley), xanthan
  and cornstarch (Carreau), water, glycerol, two glycerol–water mixtures
  and honey, from their sources, and seven model families to set by hand.
- **The pipe.** Laminar flow of any of them: the stress a straight line for
  every fluid, the profile it makes, the yield-stress plug, the flow rate
  against the pressure gradient with its threshold, the Rabinowitsch–Mooney
  correction and the Metzner–Reed Reynolds number.
- **The cavity.** A lid-driven cavity solved live by a two-relaxation-time
  lattice-Boltzmann solver in which every node takes the viscosity its own
  shear rate asks for: Newtonian against Ghia et al.'s centrelines, power
  law thinning and thickening, and Bingham with its unyielded zones.
- **Springs and dashpots.** The Maxwell, Kelvin–Voigt, standard linear
  solid and Burgers networks drawn moving through relaxation, creep and
  oscillation, their moduli over frequency, a bouncing putty's measured
  relaxation time and the Deborah number on a time axis from 10⁻¹³ s to
  10⁶ s, about twelve days.
- **The jam.** Wyart and Cates' model with the fit made to cornstarch in
  water: grains whose contacts turn frictional, S-shaped flow curves, the
  phase diagram, and the jump and hysteresis of a rate ramp.
- **The gel.** A thixotropic kerosene gel's structural kinetics (Houska):
  start-up, the hysteresis loop, steps of rate, rest and recovery, its
  network drawn intact in the fraction λ.

Checks:
- **Sources.** 46 Wikipedia articles, the Wyart–Cates paper, Ghia et al.'s
  tables from five repositories (agreeing digit for digit) and 14
  open-access papers from Europe PMC, fetched on 2026-09-27;
  `check_sources.py` pins each of 69 quoted numbers and claims to
  a phrase of its source.
- **Twins.** `build_fluids/derive_*.py` share no code with the page: sympy
  for the pipe's closed forms and the networks' Laplace inverses, scipy's
  quadrature and Radau, and `lbm_core.py`, a numpy lattice-Boltzmann solver
  written operation for operation like the page's (short runs agree to
  1e-13): 222 checks.
- **Found by them:**
  - Wyart and Cates state that the lower turning rate vanishes toward
    φ_m as (φ_m − φ)³ when f′(0) > 0; with their own f = 1 − e⁻ᵖ their
    equations give exactly p₂ε²(2p₂/(2p₂ − 1))², ε² ln(1/ε): the square with
    a logarithm, not the cube.
  - The cornstarch fit reproduces its paper's printed φ_DST ≈ 0.37
    (0.3722, from φ₀ − 2D/√e) and τ_c(0.405) ≈ 4.0 Pa (3.951).
  - At Re 400 the solver converges away from Ghia's printed v = −0.23827
    at x = 0.9063 (−0.362 on 64 × 64, −0.377 on 128 × 128), while the other
    33 points agree within 0.0089 on the finer grid; the point is drawn
    hollow.
  - A strongly shear-thinning fluid locked the solver into a period-2 mode
    under the lid; the viscosity is under-relaxed, which leaves every steady
    state unchanged.
  - A Bingham plastic at Bn 10 leaves 47 % of the box unyielded: a dead zone
    at rest on the floor, and under the vortex's centre a crescent that
    turns as one rigid piece.
  - Two of the four spring-and-dashpot networks, Kelvin–Voigt and the
    standard linear solid, are solids: the Deborah strip calls only Maxwell
    and Burgers liquid-like when relaxed.

Its card sits in Fluids & Flight, after Buoyancy. The lede says eighty-one
and the meta says 81; `dev/check_sims.py` gains the word. `simulations/TODO.txt`
lists the page in the catalog and adds the request as done, and its
"COMPLETED SIMULATIONS" header counts the list. `simulations/LIST.txt` is
Cooper's file and is not touched.

The build is in the Agent repo at `projects/simulations/build_fluids/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-non-newtonian-fluids`, which is not pushed.

Verified:
- selfTest 1797 passed, 0 failed (jsc and osascript); the UI drive 293 passed,
  0 failed; 22 scenes at three sizes, 0 layout problems; 127 mutants, all
  caught.
- At the destination `verify_dest_20260928b.py` (in the Agent build)
  checks the page byte for byte, runs its selfTest and UI drive from this
  copy, and runs `dev/check_sims.py` on a staged tree.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-28 a — The Meissner Effect & Superfluids joins the catalog, 80 sims

`simulations/meissner_superfluids.html` is new (Cooper's ask: "Let us make a
simulation of the Meissner Effect and Superfluids"; it closes the OTHER item
"Meissner Effect and Superfluids" of the to-do list). It follows a
superconductor from the Meissner effect through its two lengths to flux
quanta, then helium II through its two fluids and Landau's criterion to the
quantized vortices of a rotating bucket. No network: it opens over
`file://`, and every number on it is computed on the page, apart from the
dates and figures it quotes from its sources.

Six views:
- **The Meissner effect.** A sphere in a field, superconducting (London's
  equation: the field lines bend round it, screened by a shell λ deep) or
  perfectly conducting (the field it cooled in stays frozen), cooled before
  or in the field, or switched off after. Or a magnetized NdFeB ball over a
  flat plate: cooled with the ball on it, the plate lifts it, turns it flat
  and floats it; lowered onto the plate cold, it bounces and settles.
- **Two lengths.** The Ginzburg–Landau wall at Hc, solved for any
  κ = λ/ξ, its energy shaded as cost and gain and changing sign exactly
  at κ = 1/√2 (type I and type II), and the fields a material stands.
- **Flux quanta.** Abrikosov's lattice near Hc2 (|ψ|², one h/2e per cell),
  London's at low field, one vortex solved in Ginzburg–Landau theory, why a
  type I metal takes none (Hc1 above Hc), and a ring's Little–Parks dips.
- **Two fluids.** The fountain effect behind a superleak; the normal fluid
  as Landau's gas of excitations, from the measured spectrum, against the
  measured one; second sound against the two-fluid formula.
- **Landau's criterion.** Helium II's measured spectrum with the line pv,
  Landau's velocity (the tangent from the origin), E/p, and the angles at
  which a moving body could emit.
- **The rotating bucket.** Quantized vortex lines entering a turning bucket,
  moved by their own flow and mutual friction; the staircase against
  Feynman's count, and the free energy of each count. A thin annulus's
  Hess–Fairbank staircase beside a superconducting ring's fluxoid.

Checks:
- **Sources.** 26 Wikipedia articles, Delin and Orlando's material tables
  (after Donnelly's Physics Vade Mecum), two APS abstracts and NIST's
  CODATA pages, fetched on 2026-09-27: each of the 100 quoted rows was
  checked verbatim in its source. Ten of Donnelly and Barenghi's helium II
  tables, from their online edition.
- **A twin.** `build_msf/derive.py` shares no code with the page. It uses
  sympy for the London sphere, scipy's solve_bvp for the Ginzburg–Landau
  wall and vortex, quad over a spline of the measured spectrum, and BFGS
  over free arrangements of vortex lines: 307 checks.
- **Found by it:**
  - The Superfluid helium-4 article gives the fountain pressure at Tλ as
    0.692 bar and 56 m. Donnelly and Barenghi's entropy gives 0.751 bar, a
    column of 52.4 m. The article's 56 m is its 0.692 bar over helium I's
    125 kg/m³, and its own formula gives 0.746 bar.
  - Landau's normal fluid, from the measured spectrum, is within 6.2 % of
    the measured one up to 1.6 K and falls short above (0.453 against
    0.553 at 2.0 K).
  - The two-fluid formula runs up to 5.3 % above the measured second sound
    between 1.05 and 1.3 K, and within 1.1 % above 1.55 K.
  - The Macroscopic quantum phenomena article prints an old measured
    flux quantum, 2.067833758(46) × 10⁻¹⁵ Wb, and calls it exact by
    definition; the exact h/2e is 2.0678338485 × 10⁻¹⁵ Wb.

Its card sits in Atoms, Matter & Light, after p–n Junctions & Transistors.
The lede says eighty and the meta says 80 (`dev/check_sims.py` already knew
the word). `simulations/TODO.txt` lists the page in the catalog and
marks "Meissner Effect and Superfluids" done, and its "COMPLETED
SIMULATIONS" header counts the list. `simulations/LIST.txt` is Cooper's
file and is not touched; it still lists the item as open.

The build is in the Agent repo at `projects/simulations/build_msf/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-meissner-superfluids`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 2290 passed and 0 failed, under jsc and osascript;
  - the UI drive, 188 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 30 scenes at
    1100 × 712 and in spot scenes at 1400 × 820, 560 × 380 and 480 × 860;
  - a mutation sweep: the first 166 mutants caught 158. The eight
    survivors were closed with new tests; they and 13 new mutants were then
    all caught on the final page. One survivor was a harmless variant and
    was replaced by the real error it stood for.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-27 j — Green’s Functions & the Wronskian joins the catalog, 79 sims

`simulations/greens_functions.html` is new (Cooper's ask: "Let us make a
simulation for Wronskian solutions of green's functions with different
examples"). No network: it opens over `file://`.

One construction, and six places it shows up. For L u = −(p u′)′ + q u = f
with a condition at each end, take y₁ solving L y = 0 with the left
condition and y₂ with the right one. Then G(x, ξ) = −y₁(x<)y₂(x>)/(pW),
with W = y₁y₂′ − y₁′y₂. Abel's identity makes pW a constant, and G exists
exactly when it is not zero.
- **The construction.** Eight examples: a string with fixed, free or
  spring ends, a string on an elastic bed, a driven string, the whole line,
  a disk's angular mode, a ball's multipole, a drum, and a drifting string
  whose G is not symmetric. Both solutions are integrated from their own
  ends and checked against the closed forms where they exist. The kink at ξ
  has the slope jump −1/p(ξ). With both ends free, W = 0 and there is no G.
- **The load.** A load built up from point loads, u = ∫ G f dξ, swept in
  from the left. It is checked against a finite-difference solve that never
  forms G, and it shows Maxwell–Betti reciprocity and how drift breaks it.
- **Abel's identity.** Two solutions as two vectors in the phase plane,
  whose parallelogram has area W: the damped oscillator, Bessel, Legendre,
  Airy and Euler–Cauchy, each against the DLMF's Wronskian. Mixing one
  solution into the other flattens the parallelogram.
- **Resonance.** A driven string and a drum. p W(k) vanishes at the
  eigenvalues, which the page finds as its zeros (nπ, and the zeros of Jₘ
  without evaluating a Bessel function). The eigenfunction series with up
  to 40 terms is set against G, and the response has a pole at each
  eigenvalue.
- **The impulse.** A damped oscillator's causal Green's function from two
  free solutions and their Wronskian (variation of parameters). A kick, a
  step, a pulse, a sine and a train of kicks. The response is computed
  three ways, and a panel shows what it remembers of the force at each
  moment.
- **Bound states.** The Schrödinger equation in a square well, the
  harmonic oscillator, Pöschl–Teller, a double well and a δ well. G is
  glued from the solution that decays to the left and the one that decays
  to the right, and W(E) is zero exactly at the bound states. The page
  finds the levels as those zeros and checks them against 2n + 1,
  −(λ − n)² and −α²/4.

Sources and checks:
- **Sources:** the NIST Digital Library of Mathematical Functions, Version
  1.2.8 (fetched 2026-09-27). It supplies the Wronskian, Abel's identity,
  variation of parameters and the Wronskians of the Airy, Bessel,
  parabolic-cylinder and Legendre functions, quoted verbatim in
  `build_green/data/lit_dlmf.md`.
- **Twin.** `build_green/derive.py` shares no code with the page. It
  re-derives every closed form in sympy and computes every reference value
  in mpmath (448 checks).
- **Tests.** `selfTest()` runs 3851 checks and a UI drive runs 379. 41 scenes
  are audited at three window sizes, and a mutation sweep catches all 116
  of its mutants.

## 2026-09-27 i — Div, Grad, Curl joins the catalog, 78 sims

`simulations/div_grad_curl.html` is new (Cooper's ask: "Let us do vector
fields of Divergence Gradient and Curl"). No network: it opens over
`file://`, and every sourced number is embedded.

Six views:
- **The field near a point.** Eleven plane fields as arrows, streamlines and
  maps of div or curl. At a probe the Jacobian splits into expansion,
  rotation and shear. A parcel is carried by the linear part of the flow,
  and a paddle wheel turns at half the curl. The flux and circulation of a
  shrinking circle, over its area, become the divergence and the curl.
- **The gradient.** Six landscapes as maps or turnable surfaces. The slope
  in every direction, the path of steepest descent onto a minimum, and two
  paths whose integrals agree for a gradient and differ, for a field with
  curl, by the curl between them (Green).
- **The divergence.** Draggable line charges and Gauss's law; dye blobs
  that grow where the divergence is positive and keep their area where it
  is zero; the divergence theorem on three regions.
- **The curl.** Paddle wheels in a vortex zoo: in a point vortex they orbit
  without turning. Also two wires and Ampère's law in SI, and a spinning
  cylinder with its lift and no drag.
- **In three dimensions.** Five fields with the curl at a probe, Gauss on a
  sphere, and Stokes on a loop, where a disk and a cap carry the same flux
  of curl.
- **The decomposition.** Any field on the torus split by FFT into a
  gradient, a curl and a mean, with sources and vortices to place.

Sources and checks:
- **Sources.** NIST's μ₀ (CODATA 2022), and the English Wikipedia articles
  for the history and the named flows. 30 quoted values are each verified
  by a verbatim needle.
- **Twin.** `build_dgc/derive.py` shares no code with the page. It uses
  sympy, mpmath at 25–40 digits, scipy and numpy (361 checks).

Its card sits in Mathematics & Machines after Special Functions. The lede
says seventy-eight and the meta says 78. `simulations/TODO.txt` lists the
page in the catalog, marks its two MATHEMATICS items, "Div, Grad, Curl" and
"Vector fields", done, and its "COMPLETED SIMULATIONS" header counts the
list. `simulations/LIST.txt` carries the same two items and was left alone,
for Cooper.

The build (part files, the twin, the sources, the harnesses and the landing
scripts) is in the Agent repo at `projects/simulations/build_dgc/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-vector-calculus`, which is not pushed.

Verified from this repo's path:
- selfTest, 5857 passed and 0 failed, under jsc and osascript;
- the UI drive, 553 passed and 0 failed;
- the display-list audit, 30 scenes with 0 layout problems at 1100×712,
  1400×820 and 560×380;
- a 184-mutant sweep, every mutant caught, none by timeout;
- `dev/check_sims.py` on a staged tree.

Left uncommitted. Not pushed.

## 2026-09-27 h — The Earth's Interior joins the catalog, 77 sims

`simulations/earth_interior.html` is new (Cooper's ask: "Let us do a simulation of the Earth's inner core,
and show the tetonic plates, magma currents, iron core, magnetic fields"; it closes the PHYSICS item
"Tetonic Plates and magma currents, iron core" of the to-do list). Everything on it is measured from
outside the Earth or computed from physics: PREM's layers from seismic waves and free oscillations, Bird's
plates and Euler poles, IGRF-14's field from observatories and satellites. The one thing nobody can
measure, the mantle's flow, is a live 2-D model, labelled as one. "Magma currents" is read honestly: the
mantle is solid rock that creeps, and the liquid that flows is the outer core's iron. No network: it opens
over `file://`.

Six views:
- **The Earth.** The globe to scale with the octant facing you cut away: PREM's layers, the convection
  model running on the level face, the field at the core's surface, the plates outside, and IGRF's field
  lines from the surface into space and down to the core.
- **The plates.** Bird's 52 plates and seven boundary classes, velocities in the frame without net
  rotation (computed here) or with any plate held fixed, a plate's Euler pole and its boundary walked
  step by step.
- **The mantle.** Convection in the mantle's own ring, heated from the core, from within or both, and the
  same solver in Blankenbach et al.'s benchmark box beside their Table 9.
- **The core.** PREM's density and seismic speeds with depth, gravity and pressure integrated on the page,
  and the self-compression test that shows the liquid outer core is well mixed.
- **The field.** IGRF-14 from 1900 to 2030 at the surface and continued down to the core, the wandering dip
  poles (NOAA's track back to 1590), the South Atlantic Anomaly, the weakening dipole.
- **The waves.** Rays and wavefronts through PREM, the shadow that revealed the core (Oldham 1906,
  Gutenberg 1913) and PKIKP inside it (Lehmann 1936), the travel times against ObsPy's TauP.

Checks:
- **Sources.** 68 files fetched on 2026-09-27, among them SPECFEM's PREM, Bird's PB2002 files and paper,
  the IGRF-14 coefficients, NOAA's pole tracks and 49 Wikipedia articles. The BGS IGRF web service's 76
  answers are kept beside them.
- **Twins.** Five Python programs (scipy and numpy, with ObsPy's TauP run beside them) share no code with the
  page and run 97 checks:
  PREM's mass and I/MR² 0.3308, all 710 TauP arrivals within 0.0014 s, the BGS values within their
  rounding, Bird's printed step velocities to their last digit, Blankenbach's benchmark to its printed digits.
- **Found by them, among others:** the fastest plate without net rotation is Tonga (197 mm a year), not
  the Pacific (72); the dipole fell 7.6 % between 1900 and 2025.

Its card sits in Astrophysics & Relativity, after Earth Observation, Live. The lede says seventy-seven and the
meta says 77. `simulations/TODO.txt` lists the page in the catalog and marks "Tetonic Plates and magma
currents, iron core" done, and its "COMPLETED SIMULATIONS" header counts the list. `simulations/LIST.txt`
is Cooper's renamed file and is not touched; it still lists that item as open.

The build is in the Agent repo at `projects/simulations/build_earth/`, uncommitted, beside the other
builds. It was built on the Agent worktree branch `worktree-earth-interior`, which is not pushed.

Verified:
- **From this repo's copy:** selfTest, 1413 passed and 0 failed, under jsc.
- **On the build's byte-identical copy:** the selfTest under jsc and osascript; the UI drive, 266 passed
  and 0 failed; the display-list audit, with 0 layout problems in 25 scenes at 1100 × 712 and 1400 × 820;
  a 69-mutant sweep, 68 caught and 1 declared (a tuning constant, measured).

At a 560-px stage the floating readout covers the stage's right half, as on every page here.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-27 g — Bremsstrahlung & Inverse Bremsstrahlung joins the catalog, 76 sims

`simulations/bremsstrahlung.html` is new (Cooper's ask: "Let us do a
simulation of bremsstrahlung and inverse bremsstrahlung of x-rays"). No
network: it opens over `file://`, and every sourced number is embedded.

One collision, run in both directions of time. Six views:
- **The encounter.** One electron past one nucleus on its Coulomb
  hyperbola, the wavefronts leaving at c. Beside it are the pulse of
  acceleration and the pass's exact classical spectrum (Bessel functions of
  imaginary order), whose integral over photon energy returns the Larmor
  energy (Parseval). Sommerfeld's η says how far the classical picture
  holds, and the quantum wall stops the spectrum at ħω = T.
- **The cross section.** The photon spectrum of one electron energy on one
  atom in six approximations: Kramers, Born, Born × Elwert, Sommerfeld's
  exact non-relativistic result, Bethe–Heitler 3BN and Seltzer & Berger's
  table. The Gaunt factor runs across the regimes, and the table's
  radiative stopping power is set against NIST ESTAR's.
- **The x-ray tube.** A thick target: the electron slows in the anode, and
  its photons leave through the anode itself and a filter, K-edges
  included. Shown against Kramers' straight line and SpekPy's spectrum, with
  Duane–Hunt's wall, the characteristic lines marked (not modelled), the
  efficiency against ESTAR's radiation yield, and the half-value layer.
- **The hot plasma.** Thermal bremsstrahlung with the thermally averaged
  Gaunt factor (computed here, and within 2 × 10⁻⁵ of van Hoof et al.'s
  table). The temperature is read back from the slope, and the ignition
  balance gives D–T's ideal ignition temperature and what Z_eff does to it.
  Six presets: ITER, NIF, a solar flare, the Coma cluster, the Sun's core
  and a laser corona.
- **The absorption.** Inverse bremsstrahlung from Kirchhoff, κ = j/B, from
  the plasma frequency to hard x-rays, with laser lines and x-ray lines
  marked. It gives the absorption into a laser's density ramp and Langdon's
  reduction at 10¹⁵ W/cm². Twelve electrons quivering in a slow wave cross
  an ion, integrated exactly, against the slow-wave limit
  ⟨ΔE⟩ = −m v₀² cos χ(1 − cos χ).
- **The balance.** A slab that is thin bremsstrahlung above its turnover
  and a blackbody below. Beside it, a dark box of plasma fills with light
  up to Planck's spectrum, and its electrons pay for it.

Sources and checks:
- **Sources** (fetched 2026-09-27): CODATA 2022; Seltzer & Berger's
  bremsstrahlung table (as EGSnrc distributes it); NIST ESTAR, the x-ray
  mass attenuation tables and the x-ray transition energies; van Hoof et
  al.'s Gaunt-factor tables; Bosch & Hale 1992; the NRL formulary; SpekPy
  2.5.4; and each preset's own paper.
- **Twin.** `build_brems/derive.py` shares no code with the page. It
  recomputes every exact result with mpmath, numpy and scipy (140
  checks).

Found in the sources:
- **Bosch & Hale's Table VIII** prints its 1.25 and 1.75 keV rows as "1.3"
  and "1.8" keV in three of its four columns. Evaluated at the printed 1.3
  keV, the fit is 22–25 % above the printed value.
- **The NRL formulary's** 1.69 × 10⁻³² is this page's coefficient with the
  Born Gaunt factor, and its 3.1 × 10⁻⁷ for inverse bremsstrahlung is the
  classical low-frequency Kirchhoff κ (3.085 × 10⁻⁷). The exact quantum
  Coulomb logarithm exceeds its ln(kT/ħω) by ln(4/e^γ) = 0.809.
- **Kramers' own 1923 efficiency** (his eq. 78) is 34 % below ESTAR's
  radiation yield for tungsten at 100 kV. The page's thick-target yield
  matches ESTAR's to within 0.6 % (W, Mo, Rh and Cu, 20 to 150 kV).
- **SpekPy's HVL1** is for its unfiltered beam, lines included (0.028 mm Al
  at W 100 kV). Through the same 2.5 mm Al, its bremsstrahlung's half-value
  layer is 3.31 mm against the page's 4.45 mm. The page's electrons go
  straight in and over-filter their own beam.
- **The ideal ignition temperature** comes out 4.39 keV with van Hoof's
  Gaunt factor, within 3 % of the literature's 4.3 keV. With carbon as the
  impurity, no Z_eff above 4.14 ignites anywhere from 1 to 100 keV.
- **ITER's volume-averaged core** radiates 23.9 MW, 14 % above the 21 MW
  its design basis gives from the real, peaked profiles.

Its card sits in Scattering & Brillouin Physics after Differential
Scattering. The lede says seventy-six and the meta says 76.
`simulations/TODO.txt` lists the page in the catalog and marks the X-rays
item partly done: the characteristic lines themselves, Moseley's law, Bragg
diffraction and radiography/CT contrast stay open. Its "COMPLETED
SIMULATIONS" header counts the list.

The build (part files, the twin, the data, the harnesses and the landing
scripts) is in the Agent repo at `projects/simulations/build_brems/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-bremsstrahlung`, which is not pushed.

Verified from this repo's path:
- selfTest, 2550 passed and 0 failed, under jsc and osascript;
- the UI drive, 273 passed and 0 failed;
- the display-list audit, 31 scenes with 0 layout problems at 1100×712,
  1400×820 and 560×380;
- a 176-mutant sweep with 175 caught. The one survivor is
  measured equivalent: K_iν's contour back-off changes K by at most
  1.6 × 10⁻¹²;
- `dev/check_sims.py` on a staged tree.

Left uncommitted. Not pushed.

## 2026-09-27 f — Special Functions joins the catalog, 75 sims

`simulations/special_functions.html` is new (Cooper's ask: "Let us a do a
simulation of the legendre functions, Airy functions, Rodriguez formula,
Sonine polynomials, etc."). No network: it opens over `file://`, and every
sourced number is embedded.

Six views:
- **The Rodrigues ladder.** w Fⁿ differentiated n times, one rung per
  derivative, for the seven classical families. Each rung gains one zero
  between the zeros above it (Rolle), and the last, divided by κ_n w, is
  the polynomial, which the three-term recurrence draws again.
- **Legendre functions.** P and Q of any real degree, with the logarithm at
  x = −1. Also the degree a conducting cone chooses (the lightning rod),
  the multipole expansion of a point charge and where it converges, and the
  spherical harmonics on a turnable sphere.
- **The turning point.** Ai and Bi on the line, with their asymptotic forms
  and the best place to cut the divergent series, and over the complex
  plane with their zeros. Also a neutron's quantum levels above a mirror,
  against the qBounce and GRANIT measurements.
- **Sonine and the gas.** The Sonine polynomials in exact fractions, and
  the hard-sphere gas's conductivity and viscosity in 1 to 12 Sonine terms,
  converging on Pekeris & Alterman's values. Also the second approximation
  for any repulsion, and the distorted Maxwellian that carries heat or
  shear. That distribution turns negative in the far tail at every
  strength, and the page says where.
- **The zeros.** Unit charges in the weight's field slide onto the zeros
  (Stieltjes). Gauss quadrature races the trapezoid and Simpson, and many
  zeros are set against their limiting densities.
- **The family.** Eight limits between the families, each with its
  measured rate, and a map whose arrows can be followed.

Sources and checks:
- **Sources.** DLMF, Chapman & Cowling, Sonine (1880), Pekeris & Alterman
  (1957), Tipton (2008), Stieltjes (1885), Airy (1838), CODATA, Cronenberg
  et al. (2018) and Nesvizhevsky et al. (2005). 28 quoted values are each
  verified by a verbatim needle.
- **Twin.** `build_sf/derive.py` shares no code with the page. It uses
  mpmath at 40 digits and sympy, and integrates the hard-sphere collision
  brackets exactly (1742 checks).

Found in the sources:
- **Chapman & Cowling's fourth viscosity approximation,** printed 1.01600,
  is the sum of their rounded increments. The approximation itself is
  1.016006.
- **Nesvizhevsky et al.'s z₄ = 39.9 µm** is the product of rounded inputs.
  The Airy zero gives 39.83 µm.
- **Chapman & Cowling's footnote** writes Sonine's own polynomial with
  Γ(m+n+1) and (−1)ⁿ multiplying where Sonine's p. 41 divides.

Its card sits in Mathematics & Machines after Cycloids. The lede says
seventy-five and the meta says 75. `simulations/TODO.txt` lists the page in
the catalog and records the ask as done under MATHEMATICS, and its
"COMPLETED SIMULATIONS" header counts the list.

The build (part files, the twin, the sources, the harnesses and the landing
scripts) is in the Agent repo at `projects/simulations/build_sf/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-special-functions`, which is not pushed.

Verified from this repo's path:
- selfTest, 8755 passed and 0 failed, under jsc and osascript;
- the UI drive, 524 passed and 0 failed;
- the display-list audit, 41 scenes with 0 layout problems at 1100×712,
  1400×820 and 560×380;
- a 176-mutant sweep with 174 caught. The two survivors are
  declared equivalent;
- `dev/check_sims.py` on a staged tree.

Left uncommitted. Not pushed.

## 2026-09-27 e — The Intrinsic Hamilton–Jacobi Equation joins the catalog, 74 sims

`simulations/intrinsic_hamilton_jacobi.html` is new. Cooper's ask: "let us
make a simulation under ~/coding/website/simulations/ of the intrinsic
Hamilton Jacobi under ~/coding/Agent/Thesis/revise_thesis.* , similar to
that of riemann_sphere.html's mapping . This way I can show how the
diffeomorphisms of maps and semi-classical maps different under
diffeomorphism invariance and why we need boundaries to fully understand the
dynamical evolution". It follows Chs. 1, 4 and 5 of Cooper's revised
dissertation (Spacetime Invariants and Invariant Spacetimes, Baylor 2024)
and cites its equations by number. Everything on it is mathematics,
computed on the page. No network: it opens over `file://`.

Six views:
- **The two readings.** A diffeomorphism of a disc, read actively (the
  fields move) and passively (the points are relabelled). The maps are the
  hole argument's, a twist fixed on the boundary, a rigid rotation that
  moves the boundary, and a fold. A distance between dragged points never
  changes. The distance to a mark held fixed from outside changes only when
  the map moves the boundary. The fold has no passive reading: its dust
  density is the sum of 1/|det| over every preimage, infinite on the
  caustic.
- **The chart's pole.** A spin turning about an axis, in the thesis's
  stereographic chart ζ = (x + iy)/(1 − z) (Eq. 1.8). The linear flow
  becomes a Riccati equation that blows up when the state crosses N. RK4 in
  one chart loses digits and then overflows. Switched between two charts it
  stays within 5 × 10⁻⁷.
- **The fold.** The rays of a phase grating's Hamilton–Jacobi function
  fold into a caustic and a cusp. The exact wave (its Bessel series) is
  drawn against the WKB sum of one or three rays with the Maslov phase. A
  point map, linear in p, carries the caustic along but can neither make
  nor remove one. The free evolution, quadratic in p, makes it. This is
  the thesis's split of a diffeomorphism into the parts the momentum and
  the scalar constraint generate (Eq. 5.2).
- **The clock.** Two oscillators under one constraint (Rovelli's model).
  The gauge orbits are the points of a Riemann sphere, ζ = z₁/z₂. The
  intrinsic Hamilton–Jacobi equation (Eq. 4.21) is solved for three clocks:
  q₂, a rotated quadrature and the phase. A position clock turns back where
  its physical Hamiltonian has a square-root branch point. The timeless
  quantum state of the n-quantum level gives conditional states, and the
  clock's density goes over to the classical arcsine as n grows.
- **The tube.** Cartan's integral invariant (Eqs. 4.3 and 4.9). A loop of
  starts carried by the pendulum or the oscillator keeps ∮(p dq − H dt),
  cut at one time or obliquely. An open arc changes by exactly S at one end
  minus S at the other. A gauge term reaches an arc only through its ends,
  and a closed orbit carries its action J.
- **The slicing.** Schwarzschild in slices T = t + λh(r), from the static
  (λ = 0) to the Gullstrand–Painlevé (λ = 1, Eq. 5.75), in the Penrose
  diagram. The Gauss relation (Eq. 5.93) gives the same tidal field on
  every slice, and the constraints vanish on every slice. The mass read on
  a boundary sphere is m for every λ, split between the slice's curvature
  and its bending. The ADM formula, which reads the metric alone, sees
  m(1 − λ²).

Checks:
- **A twin.** `build_ihj/derive.py` shares no code with the page. It
  proves the closed forms in sympy and pins the numbers the selfTest holds
  the page to (mpmath at 30 digits, numpy, scipy): 151 checks.
- **The thesis.** Every equation number the page cites (1.7, 1.8, 4.3,
  4.5, 4.6, 4.9, 4.12, 4.21, 5.2, 5.70, 5.71, 5.75, 5.93) was checked
  against the compiled `revised_thesis.pdf`.

Its card sits in Astrophysics & Relativity, after Loop Quantum Gravity.
The lede says seventy-four and the meta says 74. `dev/check_sims.py`
already had the count word. `simulations/TODO.txt` lists the page in the
catalog, and its "COMPLETED SIMULATIONS" header counts the list. Neither
TODO.txt nor LIST.txt had an item for this sim, so none is marked, and
LIST.txt is not touched.

The build is in the Agent repo at `projects/simulations/build_ihj/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-intrinsic-hj-sim`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 299 passed and 0 failed, under jsc and osascript;
  - the UI drive, 250 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 26 scenes at each
    of 1100 × 712, 1400 × 820 and 560 × 380;
  - an 82-mutant sweep with every mutant caught.

Below 900 px the side plots are not drawn, and each caption then describes
the main picture only, however tall the canvas. The selfTest renders 20
scenes at four narrow sizes to hold it.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-27 d — Rabi Oscillations & Superoscillations joins the catalog, 73 sims

`simulations/rabi_superoscillations.html` is new (Cooper's ask: "Add a
simulation that explains rabi oscillations then super oscillations"; it also
closes the PHYSICS item "Rabi Flapping" of the to-do list). It follows a
driven two-level atom from Rabi's flop to the weak value of a post-selected
turn, and from there to Berry's superoscillations. No network: it opens over
`file://`, and every number on it is computed on the page, apart from the
dates and figures it quotes from its sources.

Six views:
- **The flop.** The atom's Bloch vector in the lab and in the frame turning
  with the drive, for a linear drive and for Rabi's rotating field. Pₑ(t)
  integrated in the lab is drawn against Rabi's formula. The flop's own
  frequency is drawn against the detuning, slowest at the Bloch–Siegert
  resonance ω₀(1 + Ω²/4ω₀²).
- **Pulses & fringes.** π, π/2 and 2π pulses, where a 2π pulse returns
  |g⟩ times −1. A pulse's line against the detuning, the flop against the
  pulse's area, and Ramsey's two π/2 pulses with their fringes.
- **A real atom.**
  - Decay: the optical Bloch equations, the steady state, power broadening
    and the Mollow triplet of the scattered light.
  - Photons: the Jaynes–Cummings model for a vacuum, Fock, coherent or
    thermal field, with the collapse, the revival, and the atom's Bloch
    vector shortening while it is entangled with the field.
- **The weak turn.** The Weak value article's example: pre-select, turn by
  θ, post-select. The amplitude's phase runs at A_w/2 where a turn alone
  allows 1/2, and the price is a post-selection that succeeds 1 time in
  10,001 for A_w = 100.
- **Superoscillation.** Berry's f(x) = (cos(x/N) + i a sin(x/N))ᴺ, a sum of
  waves with |k| ≤ 1, oscillates like cos ax in a window. The view shows
  the spectrum, the local wavenumber and the price, |f| growing to aᴺ.
- **The pointer.** N spins push a Gaussian pointer by ±1/N each. Post-
  selected, the pointer lands at the weak value once it is wider than
  √((a² − 1)/2N). As a focal field, Re f makes a fringe narrower than the
  diffraction limit, beside sidebands far brighter.

Checks:
- **Sources.** 29 Wikipedia articles were fetched on 2026-09-27. Each of
  the 58 quoted rows was checked verbatim in its source.
- **A twin.** `build_rso/derive.py` shares no code with the page. It uses
  40- to 100-digit matrix exponentials, DOP853, a Lindblad Liouvillian's
  eigen-decomposition and a diagonalised Jaynes–Cummings Hamiltonian, and
  pins the numbers the selfTest holds the page to: 203 checks in all.
- **Found by it:**
  - The Bloch–Siegert shift shows in the flop's frequency, not in its depth
    or time average.
  - Ramsey's central fringe is π/(T + 4τ/π) wide, since the pulses count as
    4τ/π of free flight.
  - The atom's Bloch vector is nearly pure again halfway to the revival
    (0.957 at gt = 13.9, n̄ = 16).

Its card sits in Quantum Mechanics, after Bloch Sphere. The lede says
seventy-three and the meta says 73. `dev/check_sims.py` gains the count
words for 73 to 75. `simulations/TODO.txt` lists the page in the catalog
and marks "Rabi Flapping" done, and its "COMPLETED SIMULATIONS" header
counts the list. `simulations/LIST.txt` is Cooper's renamed file and is not
touched; it still lists "Rabi Flapping" as open.

The build is in the Agent repo at `projects/simulations/build_rso/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-rabi-superoscillations`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 2340 passed and 0 failed, under jsc and osascript;
  - the UI drive, 166 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 22 scenes at each
    of 1100 × 712, 1400 × 820 and 560 × 380;
  - a 132-mutant sweep with every mutant caught.

Below 900 px the house layout draws one plot under the picture or none.
This page's captions then describe the picture only, instead of naming
plots that are not there, and the selfTest holds every narrow stage to it.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-27 c — The Riemann Sphere joins the catalog, 72 sims

`simulations/riemann_sphere.html` is new (Cooper's ask: "Let us make a
simulation under ~/coding/website/simulations/ of the Rieamannian Sphere",
the first MATHEMATICS item of the to-do list). It is the complex plane
closed up by its point at infinity. No network: it opens over `file://`,
and nothing on it is measured; it is all mathematics.

Six views:
- **The projection.** The sphere on the plane through its equator, the
  line from N through ζ meeting the sphere at P, N the point at infinity;
  the grids and their images; a right angle at ζ kept at P, stretched by
  2/(1 + |ζ|²).
- **Circles.** A circle in the plane is a plane's cut through the sphere,
  a line is a circle through N, and two circles cross at the same angle on
  both.
- **Möbius maps.** Elliptic, hyperbolic, loxodromic and parabolic, from
  their fixed points and multiplier, as flows on the plane and the sphere.
- **Functions.** Six rational maps as phase portraits on the plane and the
  sphere, their zeros, poles and critical points counted with ∞, and
  Newton's basins for z³ − 1.
- **Spin states.** A spin-j state as Majorana's 2j stars: coherent states,
  |j, m⟩, the cat state, the tetrahedron and the octahedron, turned by a
  rotation.
- **The sky.** A moving observer's sky: aberration as the one Möbius map
  ζ′ = e^η ζ, the Doppler factor, and a round object that stays round.

Checks:
- **A twin.** `build_riemann/derive.py` shares no code with the page. It
  proves the closed forms in sympy and checks the numbers with mpmath,
  numpy and scipy, 185 checks in all, and pins the values the selfTest
  holds the page to.
- **Found by it:** the Cayley map (z − i)/(z + i) is a turn of the sphere
  by 120° about (−1, 1, −1)/√3, and rotations act on ζ as the complex
  conjugates of exp(−iθ n·σ/2), because projecting from N puts a spinor
  (α, β) at ζ = ᾱ/β̄.

Its card sits in Mathematics & Machines, after Platonic & Catalan Solids.
The lede says seventy-two and the meta says 72. `simulations/TODO.txt`
lists the page in the catalog, marks the MATHEMATICS item done, and its
"COMPLETED SIMULATIONS" header counts the list; the same item is marked in
`simulations/LIST.txt`. `dev/check_sims.py` already had the count word for
72.

The build is in the Agent repo at `projects/simulations/build_riemann/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-riemann-sphere`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 202 passed and 0 failed, under jsc and osascript;
  - the UI drive, 215 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 31 scenes at each
    of 1100 × 712, 1400 × 820 and 560 × 380;
  - a 72-mutant sweep with every mutant caught.

Below 900 px the views use the whole width, and the floating readout
covers their right side, as in every sibling sim.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-27 b — Voltage & Current Dividers joins the catalog, 71 sims

`simulations/dividers.html` is new (Cooper's ask: "Let us make a Voltage and
Current divider simulation under ~/coding/website/simulations/"). No network:
it opens over `file://`, and every sourced number is embedded.

Six views:
- **The two dividers.** The same two to five resistors in series from a
  battery and in parallel from a current source. The wires are coloured by
  their potential and the charge moves at a speed set by the current. The
  voltage falls on one straight line against the resistance passed, and the
  current builds on one straight line against the conductance passed. The
  branches share the current in the one way that heats the least (Maxwell).
  Resistors can come from an E series, with the tolerance's worst corners.
- **The landscape.** Six circuits laid on a board with every wire raised to
  its potential. Resistors are ramps and the battery is a lift, and a bridge
  balances when its two middles stand at the same height.
- **The load.** A divider feeding a load, with its Thévenin equivalent and
  the 10x rule. The most power goes in at R_L = R_th (Jacobi), with half of
  it lost. Also a loaded potentiometer, whose error is largest near
  two-thirds of the travel, and the divider's Johnson noise, which is that
  of R_th alone.
- **The meter.** An analog multimeter built from one movement. The
  multiplier chain is a voltage divider and the Ayrton shunt a current
  divider. It shows the needle, the reading on a high-resistance divider,
  the best range once 3 % of full scale is counted, and the same divider
  read by the meters of a century.
- **The bridge.** Two dividers compared: Wheatstone's balance, strain gauges
  in quarter, half and full bridges, and a thermistor divider on the
  datasheet's own law. Its fixed resistor is chosen for slope, for linearity
  or for the widest swing, and its self-heating is shown.
- **The ladder.** The R-2R ladder as a string of current dividers, each
  halving, with its staircase and what resistor mismatch does to it (DNL,
  INL, the major carry). Also the Kelvin-Varley divider.

Sources and checks:
- **Sources** (fetched 2026-09-27 and verified by needle): thirty Wikipedia
  articles and the Vishay NTCLE100E3 datasheet (document 29049, 07-May-2025),
  144 rows in all, and the datasheet's resistance table.
- **Twin.** `build_div/derive.py` shares no code with the page. It solves
  every circuit by exact nodal analysis over the rationals and checks every
  closed form the page uses against those solves (598 checks).

Found in the sources:
- **Resistor ladder** asks the MSB resistors to be well inside 1/2^N of R
  (1/32 for 5 bits, 1/256 for 8). The major carry first steps backwards at
  1/(2^(N−1) − 1), which is 1/15 and 1/127, so the rule has about a factor
  of 2 in hand.
- **The datasheet's printed table** sits up to 0.011 °C from its own law,
  about four times the table's rounding. The law and its inverse agree as
  the datasheet claims (0.0048 °C above 25 °C, 0.0116 °C below). The
  one-parameter B model is off the law by +2.99 °C at −40 °C and +1.39 °C
  at 125 °C.
- **Multimeter's** 1 mA, 500 Ω movement needs 9,500 Ω for 10 V and a shunt
  "just over 0.5 Ω" for 1 A. Both are reproduced (0.5005 Ω). Built as an
  Ayrton chain, the same 1 A tap is 0.5556 Ω.
- **E series of preferred numbers:** the rounding formula misses eight E24
  values and gives 9.19 for E192's 9.20. The page uses the published lists.

Its card sits in Signals & Sound after RLC Band-Pass Filters. The lede says
seventy-one and the meta says 71. `simulations/TODO.txt` lists the page in
the catalog and marks "Voltage divider" and "Current divider" done under
CIRCUITS, and its "COMPLETED SIMULATIONS" header counts the list.

The build (part files, the twin, the sources, the harnesses and the landing
scripts) is in the Agent repo at `projects/simulations/build_div/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-dividers`, which is not pushed.

Verified from this repo's path:
- selfTest, 3458 passed and 0 failed, under jsc and osascript;
- the UI drive, 254 passed and 0 failed;
- the display-list audit, 38 scenes with 0 layout problems at 1100×712,
  1400×820 and 560×380;
- a 174-mutant sweep with 170 caught. Of the four survivors, three are
  measured equivalent and one is a look constant (the dots' spacing);
- `dev/check_sims.py` on a staged tree.

Left uncommitted. Not pushed.

## 2026-09-27 a — LXCat Cross Sections joins the catalog, 70 sims

`simulations/lxcat.html` is new (Cooper's ask: "Look at
~/coding/Agent/projects/Kinetic_Modeling/LoKI-MC/Code/Input and make a
simulation titled "lxcat.html" under ~/coding/website/simulations/ of the
different energy states, cross-sections, and average cross-sections
\langle \sigma v \rangle"). It draws the electron-collision data LoKI-MC
reads: the 18 LXCat files of the fifteen cross-section sets its swarm
setups combine, argon to water, 445 blocks carried verbatim with each
file's sha256. No network: it opens over `file://`.

Six views:
- **The states.** Every state a collision reaches, at its threshold above
  the ground state, in columns by kind (an atom's Rydberg series by
  orbital, singlets and triplets, rotation, vibration, electronic states,
  dissociation, attachment, ions), each lit by its rate over the chosen
  distribution.
- **The cross sections.** Every σ(ε) exactly as LoKI-MC interpolates it,
  with the elastic cross section LoKI-MC derives from an Effective one.
- **The average.** The distribution, σv and their product, the integrand
  of ⟨σv⟩, for one collision, with the Maxwellian and Druyvesteyn rates of
  the same mean energy side by side.
- **The rates.** Every collision's ⟨σv⟩ against kT_e or E/N, with the
  Arrhenius energy.
- **The distribution.** The two-term Boltzmann solution beside the
  Maxwellian, the Druyvesteyn and LoKI-MC's own Monte Carlo, with the swarm
  parameters and where the field's power goes.
- **The gases.** All fifteen sets' momentum transfer and ionization on one
  plot.

The distribution is a Maxwellian, a Druyvesteyn, or the two-term Boltzmann
equation (Hagelaar & Pitchford 2005) solved in the page at 0.1 to 1000 Td,
for a pure gas or the KrF and ArF laser mixtures of LoKI-MC's krf0d
setups.

Checks:
- **LoKI-MC itself.** Fed LoKI-MC's own EEDF, the page's sum gives back
  every rate LoKI-MC printed, in all 27 runs under its Code/Output to
  1e-13 and in 22 runs made for this page to 1e-12.
- **Its Monte Carlo.** The two-term solution is within 1.0 % in the mean
  energy and 1.3 % in the drift for neon from 10 to 300 Td. Argon's D/μ
  comes out 10 to 26 % high and krypton's and xenon's up to 72 %, the
  known two-term failure in the Ramsauer gases.
- **A twin.** `build_lxcat/derive.py` and `derive_boltz.py` share no code
  with the page. They parse the files with their own code, integrate every
  Maxwellian rate at 40 digits with mpmath, and solve the same Boltzmann
  discretization densely with numpy. The page matches the Maxwellian rates
  to 1e-12, and the solver's swarm parameters to 1e-10 and its
  distribution and rates to 1e-9.
- **MultiBolt.** Reid's ramp gas against the multi-term column of
  LoKI-MC's benchmark document: the drift +0.25 % at 1 Td and +3.3 % at
  24 Td.

Found and stated on the page:
- **Xenon's file repeats its Elastic collision.** LoKI-MC keeps the first,
  and so does the page.
- **F2's elastic from its Effective cross section goes negative** at two
  energies and is clipped, as LoKI-MC clips it.
- **Pure F2 below about 58 Td has no positive two-term solution.** The
  page says so instead of drawing one.

Found in LoKI-MC's Input and reported in the Agent repo's changelog:
- **`Mixture/KrF_swarm.in` points at `F2/F2_LXCat.txt`,** but the file is
  in `Fluorine2/`.
- **The atomic-fluorine file has no block LoKI-MC can parse.**
- **Helium's LoKI-MC run cannot reach 300 Td.** Its electrons pass the end
  of the 1000 eV elastic table.

Its card sits in Scattering & Brillouin Physics, after Differential
Scattering. The lede says seventy and the meta says 70.
`simulations/TODO.txt` lists the page in the catalog and as a done PHYSICS
item, and its "COMPLETED SIMULATIONS" header counts the list.
`dev/check_sims.py` already had the count word for 70.

The build is in the Agent repo at `projects/simulations/build_lxcat/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-lxcat`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 113 passed and 0 failed, under jsc and osascript;
  - the UI drive, 590 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 48 scenes at each
    of 1100 × 712, 1400 × 820 and 560 × 380;
  - a 70-mutant sweep with every mutant caught.

Below 900 px the views use the whole width, and the floating readout
covers their right side, as in every sibling sim.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-25 c — Hyperfine Structure: krypton and KrF

`simulations/hyperfine_structure.html` now draws krypton and the KrF excimer (Cooper's ask: "Add Kr and KrF").
There is still no network: it opens over `file://`, and every sourced number is embedded.

What is new:
- **Krypton.** ⁸³Kr, its one stable isotope with a nuclear spin, is drawn on three lines:
  - the 811.3 nm line, on which atom-trap trace analysis cools the radioactive ⁸¹Kr and ⁸⁵Kr;
  - the resonance lines at 123.6 and 116.5 nm.

  ⁸⁵Kr and ⁸¹Kr are drawn where they have been measured.
- **KrF**, the 248-nm excimer laser molecule. Both of its states are drawn dashed, because no hyperfine
  constant of KrF is published in an open source; each state's note says what is known. The line is given to
  the three figures its source prints.
- **KrF's spectrum view is a ladder of widths** on one logarithmic scale, from its sources:
  - the B → X band, about 2 nm or 10 THz wide;
  - a free-running KrF laser (1.5 THz);
  - Nike at 1 and 3 THz;
  - the hyperfine structure of the atoms it is made of (a few GHz);
  - the Doppler width and the 17 MHz natural width.
- **The overview has a third page**, krypton beside KrF, with rubidium. Its tab is now "the overview".

Fixed (in 2026-09-25 b's page):
- **GHz values printed as whole numbers.** Values quoted without an uncertainty that reach 1 GHz were printed
  as whole GHz (vanadium's 3.778 234 GHz as "4 GHz"). This hit all of vanadium's levels, titanium's and
  chlorine-35's spans, and neon-21's s₂. They now keep their decimals.
- **The wrong isotope named.** The note on a line drawn with another isotope's energies named the wrong
  isotope for ³⁷Cl and ⁴⁷Ti.
- **Too many digits.** The diagram's "the optical gap is … times the widest manifold" printed five figures
  where two were meant.

Sources and checks:
- **Sources:** 313 quoted numbers, up from 277, each found word for word in one of 66 downloaded sources. Their
  download URLs are in `build_hfs/data/lit_manifest.tsv`, and all 55 still answer.
- **Found in them** (stated on the page):
  - Faust & Chow Chiu's krypton-83 constants give back their own measured intervals only to 16 kHz, so that
    level is printed to 100 kHz;
  - no open source says KrF's lower state binds: it repels where the laser leaves it.
- **Not found in an open source,** and drawn as missing with a note: KrF's hyperfine structure, krypton-83's
  1s₂, krypton-81's 2p₉, and the radioactive isotopes' 1s₄ and 1s₂. Krypton, like neon, has no measured g_J
  in NIST, so it gets no field or vector picture.
- **Twin:** `build_hfs/derive.py` now checks 811 numbers, up from 794. New are Faust's intervals and every
  width of KrF's ladder, recomputed by a second route.

The card now says "hydrogen through chromium, krypton and the KrF excimer". `simulations/TODO.txt` records the
update on the page's done line. The count is unchanged at 69.

The build is in the Agent repo at `projects/simulations/build_hfs/`, uncommitted, updated from 2026-09-25 b.
It was built on the Agent worktree branch `worktree-hyperfine-structure`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 664 passed and 0 failed, under jsc and osascript;
  - the UI drive, 498 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 224 scenes at each of 1100 × 712, 1400 × 820 and
    560 × 380;
  - a 148-mutant sweep with every mutant caught.

Known-bad for this page (the full list is in its header comment):
- A number formatter must be tested in every unit it switches to (the GHz bug above).
- The isotope NIST's energies belong to is the line's own, not "the second isotope".
- A molecule has no Z and no NIST levels. KrF is built from its atoms, and its line is given to its source's
  figures.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-25 b — Hyperfine Structure: the next dozen, aluminium to chromium

`simulations/hyperfine_structure.html` now draws the next dozen elements (Cooper's ask: "Please proceeed with
the next dozen elements"). Hydrogen to chromium, and rubidium-85, are all there. Still no network: it opens
over `file://`, and every sourced number is embedded.

What is new:
- **Twelve more atoms**, each with the isotope that has a nuclear spin and its resonance lines: ²⁷Al, ²⁹Si,
  ³¹P, ³³S, ³⁵Cl and ³⁷Cl, ³⁹Ar, ³⁹K, ⁴⁰K and ⁴¹K, ⁴³Ca, ⁴⁵Sc, ⁴⁷Ti and ⁴⁹Ti, ⁵¹V, and ⁵³Cr.
  - **Argon** has no stable isotope with a spin. Its drawn isotope is the radioactive ³⁹Ar, on the 811.5 nm
    line atom-trap trace analysis counts it on to date groundwater and ice.
  - **Potassium-40's** structure is inverted (its highest F lowest), with each potassium isotope's own D-line
    frequency.
- **The overview** shows a dozen atoms at a time, with rubidium on each page; choosing an atom turns to its
  page.
- **Scandium's ground levels** carry the measured octupole constant C (Steck's Eq. 16 in full), which moves
  their F levels by up to 1.46 kHz.
- **The vectors' state** is chosen by F, then m_F, since a level can now have 80 states.
- **Precision:** each constant in the readout keeps its source's uncertainty digits, and a level with a
  constant quoted without an uncertainty prints its F levels without one.

Sources and checks:
- **Sources:** 277 quoted numbers, up from 138, each found word for word in one of 54 downloaded sources. They
  were collected by four research agents and each reading was re-checked against the saved text. The second
  dozen's download URLs are recorded in `build_hfs/data/lit_manifest.tsv`.
- **Found in them** (stated on the page):
  - a swapped isotope column in a chlorine table;
  - a misprinted titanium-49 value in a 2026 preprint;
  - an abstract that disagrees with its own table (silicon);
  - a fit without B that biases A (scandium's upper level);
  - an aluminium B quoted two ways;
  - a compilation file without a unit (vanadium);
  - a sign that only a figure gives (chromium's z⁷P°₄).
- **Not measured, or not found in an open source,** and drawn as missing with a note: the upper levels of
  silicon's 251.6 nm line, phosphorus, sulfur and chlorine, argon-39's 4s[3/2]₁, and chromium's z⁷P°₂ and
  z⁷P°₃. Sulfur-33's ground term is a calculation: it has never been measured.
- **Twin:** `build_hfs/derive.py` now checks 794 numbers, up from 694. New are the octupole term built a
  second way, potassium against NIST, chromium's sign, vanadium's unit, and the numbers in the level notes.

The card now says "hydrogen through chromium". `simulations/TODO.txt` records the update on the page's done
line. The count is unchanged at 69.

The build is in the Agent repo at `projects/simulations/build_hfs/`, uncommitted, updated from 2026-09-25 a. It
was built on the Agent worktree branch `worktree-hyperfine-structure`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 550 passed and 0 failed, under jsc and osascript;
  - the UI drive, 440 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 193 scenes at each of 1100 × 712, 1400 × 820 and
    560 × 380;
  - a 111-mutant sweep with every mutant caught.

Known-bad for this page (the full list is in its header comment):
- A measured octupole C must reach every place the F levels are placed: Eq. (16), the Zeeman blocks, and
  their names.
- Eight F levels overflow a layout built for four. Labels need fallbacks that stay inside the diagram (the
  caption, drawn later, cannot refuse an overlap).
- Level crossing gives |A|, not A. A magnitude is drawn only with a sourced sign.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-25 a — Hyperfine Structure joins the catalog, 69 sims

`simulations/hyperfine_structure.html` is new (Cooper's ask: "Take a look at
the file ~/coding/website/ARTICLES/Rb_85_data.pdf I want to make a simulation
under ~/coding/website/simulations/ titled "hyperfine_structure" as done in
the .pdf's Figures 2 and 3 for Rubidium. Can you do it for the first 12
elements as well?"). The PDF is D. A. Steck, "Rubidium 85 D Line Data",
rev. 2.3.4 (2025). No network: it opens over `file://`, and every sourced
number is embedded.

Six views:
- **The diagram.** A line's two fine-structure levels, each fanned into its
  F levels to scale within its own manifold. It shows every F's shift from
  the centre of gravity with its uncertainty, the splittings between
  neighbours, the approximate g_F and its MHz/G, and the line's wavelength,
  frequency, wave number and photon energy. That is Steck's Figure 2 (D2)
  and Figure 3 (D1) for rubidium-85, and the same drawing for every
  resonance line of H, He, Li, Be, B, C, N, O, F, Ne, Na and Mg.
- **Hydrogen to magnesium.** The thirteen atoms side by side, each with its
  default line. Five of the twelve are mostly an isotope with no nuclear
  spin (⁴He, ¹²C, ¹⁶O, ²⁰Ne, ²⁴Mg), so their odd isotopes are drawn.
- **The spectrum.** Every F → F′ component with its share of the
  absorption, each a Voigt profile (the natural Lorentzian and the Doppler
  Gaussian), from 1 µK to 3000 K or the atoms at rest.
- **In a magnetic field.** Every state of a level from zero field to
  Paschen–Back, as in Steck's Figures 4 to 6, with the Breit–Rabi formula
  and the clock shift.
- **The sublevels.** The m_F ladders and the transitions that σ⁺, π or σ⁻
  light drives from one lower F, each with its squared matrix element
  (Steck's Tables 9 to 20), and the cycling transition.
- **The vectors.** J and I locked into F at weak field and each turning
  about B at strong field, with the exact ⟨J_z⟩ and ⟨I_z⟩ between.

Sources and checks:
- **Sources** (fetched 2026-09-24 and verified by needle): 138 rows from 28
  sources.
  - Steck's rubidium-85 and sodium D-line documents.
  - The NIST Atomic Spectra Database (level energies, Einstein A
    coefficients) and NIST's atomic weights and isotopic compositions.
  - Stone's IAEA table of nuclear moments.
  - The papers that measured or computed each light atom's hyperfine
    constants.
- **Twin.** `build_hfs/derive.py` shares no code with the page. It uses
  exact rational angular momentum (Racah's formulas in fractions.Fraction),
  numpy's eigh for the field and scipy's wofz for the Voigt profile. It
  reproduces:
  - every number of Steck's Figures 2 and 3 for both his atoms;
  - his Table 8 and all 248 matrix elements of his Tables 9 to 20;
  - the Breit–Rabi formula and both clock shifts;
  - every level and line of the thirteen atoms, by a second route.

Found in the sources (stated on the page):
- **Steck's photon energies** use h/e cut at 4.135 667 696 × 10⁻¹⁵ eV s,
  2.2 × 10⁻¹⁰ short. For rubidium's D2 line that is 6.3 of his standard
  deviations. The page prints hν/e from the exact SI constants.
- **Steck's P₃/₂ interval uncertainties** combine the two levels in
  quadrature, as if the levels were independent when both come from one A
  and one B. The page propagates A and B directly. It gives 120.860(78) MHz
  where he prints 120.860(61).
- **Five last digits of his figures** come from his arithmetic, not his
  data:
  - Rubidium's 5²P₁/₂ values of 210.923(99) and 150.659(71) MHz need an A
    carried past the 120.527(56) MHz he prints. The page gives 210.922(98)
    and 150.659(70).
  - Sodium's 3²P₃/₂ F′ = 3 and 0 are exact ties, 42.3825 and −66.0975 MHz.
    His figure rounds them down and the page rounds them up.
- **g_I from the bare nuclear moment** is 3.81 per mille from Steck's
  atomic value for rubidium-85, because the electrons shield the nucleus.
  The light atoms use the bare moments, and the page says so.

Its card sits in Atoms, Matter & Light, after the Periodic Table. The lede
says sixty-nine and the meta says 69. `simulations/TODO.txt` lists the page
in the catalog and as a done PHYSICS item, and its "COMPLETED SIMULATIONS"
header counts the list. `dev/check_sims.py` has count words to 72.

The build is in the Agent repo at `projects/simulations/build_hfs/`,
uncommitted, beside the other builds. It holds the part files, the twin,
the sources, the harnesses and the landing scripts. It was built on the
Agent worktree branch `worktree-hyperfine-structure`, which is not pushed.

Verified:
- **From this repo's copy:**
  - selfTest, 294 passed and 0 failed, under jsc and osascript;
  - the UI drive, 345 passed and 0 failed;
  - `dev/check_sims.py` on a staged tree.
- **On the build's byte-identical copy:**
  - the display-list audit, with 0 layout problems in 108 scenes at
    1100 × 712 and 43 each at 1400 × 820 and 560 × 380;
  - a 90-mutant sweep with every mutant caught.

Below 900 px the views use the whole width, and the floating readout
covers their right side, as in every sibling sim (none has a narrow
layout).

Known-bad for this page (the full list is in its header comment):
- Steck's quadrature and the direct propagation are both pinned. Neither
  is to be "fixed" to the other.
- Don't retype the figure's five digits to match. The page prints what
  Table 5 gives and says why his differ.
- A 6-MHz line on a 3-GHz axis falls between uniform samples. The spectrum
  samples densely around every component.
- The stretched state is an eigenstate at every field. The vectors default
  to the top F's smallest positive m_F.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-24 c — p–n Junctions & Transistors: building the bands of a blue LED

`simulations/transistors.html` has a seventh view (Cooper's ask: "Can you visualize the depletion
zone and the band like that of in the video https://www.youtube.com/watch?v=AF8d72mA41M I want to
show how to "build" a band such as for the blue diode which requires many more bands than just two or
three"; the video is Veritasium's "Why It Was Almost Impossible to Make the Blue LED"). Still no
network, and every sourced number embedded.

- **Building the bands** (key 7). A band diagram built one layer at a time, drawn the video's way:
  - each band a filled strip; electrons as dots in the conduction band and holes as rings in the
    valence band; the depletion zone empty;
  - every layer first alone, its bands hung under the vacuum level by its electron affinity, its own
    Fermi level set by its doping;
  - "build it" joins the layers one at a time: the Fermi levels meet, the ions left bare in the
    depletion zone (shown in a strip above) bend the bands, and the wells appear.
- **Four stacks:** silicon p–n (the junction view's), GaN p–n, one InGaN well, and the blue LED
  (n-GaN, five In₀.₁₅Ga₀.₈₅N wells between GaN barriers, a p-Al₀.₁₅Ga₀.₈₅N electron-blocking layer,
  p-GaN).
- **A layer editor** sets any layer's material, alloy fraction, thickness and doping, and adds or
  removes layers, up to 16.
- **Polarization:** the Ga-face sheets tilt the wells against the junction's field.
- **Forward bias** splits the Fermi level in two, and the wells glow in the colour of their gap, 450
  nm.

Computed and pinned:
- **The LED's built-in step:** 3.303 eV.
- **n-GaN** is degenerate, E_F 0.039 eV above E_c.
- **p-GaN:** only 2.53 % of its magnesium is ionized, giving 5.06×10¹⁷ holes from 2×10¹⁹ atoms.
  Kazazis et al. call 5×10¹⁷ typical of commercial p-GaN.
- **Wells:** 2.756 eV, 0.437 eV deep for electrons and 0.187 eV for holes.
- **Polarization:** 1.47×10¹³ electron charges per cm² at each well interface. The middle well is
  at −1.94 MV/cm at rest, against the junction's +0.39.
- **Silicon's step:** 0.775 V, the junction view's to 0.05 mV.

Found in the sources:
- **Ioffe's InN/GaN band offsets** (Martin et al. 1996) belong to the InN gap of the time, 1.970 eV,
  which Ioffe still prints. With today's 0.64 eV they cannot be combined. The page uses Kazazis et
  al.'s consistent set (70 % of a gap step in the conduction band) and says this split is the least
  certain number.
- **Wikipedia's "Indium gallium nitride"** puts blue 440 nm at 30 % indium ("citation needed").
  The measured bowing gives 562 nm there, so it is not used.

Its card text now names the band builder. The count is unchanged (68), and the PHYSICS line of
`simulations/TODO.txt` is extended.

The build is in the Agent repo at `projects/simulations/build_pn/`, uncommitted: `p2_bands.js`,
`p5b_bands.js`, the twin `derive_bands.py` and 49 new sourced constants. It was built on the Agent
worktree branch `worktree-pn-junctions`, which is not pushed.

Verified from this repo's path:
- selfTest, 1631 passed and 0 failed, under jsc and osascript;
- the UI drive, 339 passed and 0 failed;
- the display-list audit, 34 scenes with 0 layout problems;
- a 146-mutant sweep, every mutant caught once an equivalent one was replaced;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in the Agent changelog):
- **The isolated hydrogenic donor is wrong past the Mott density.** n-GaN read 20 % ionized.
- **A part-built Ga-face stack needs the free end's partner sheet.** Without it, a lone well bent
  the bands 3.2 V.
- **Ioffe's InN numbers are pre-2002.**

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-24 b — RLC Band-Pass Filters: press a station, or step through the band

The radio dial in `simulations/rlc_bandpass.html` (key 7) can be tuned by the
stations themselves and by buttons (Cooper's ask: "Can you make it so I can
click onto the different stations or use buttons to move through the
frequency band").

- **Press a station** to tune to it: its mark on the dial, or beside its bar
  on the band. A drag along the band still tunes smoothly through everything
  in between. With the switch, a press goes to the circuit nearest that
  station.
- **Four buttons** under the rotor. « station and station » go to the next
  station down or up the band. ‹ 10 kHz and 10 kHz › move one channel of the
  10-kHz grid; from between two channels they go to the next one that way.
  A button greys out where the dial can go no further. With the switch, the
  station buttons click it a position and the channel buttons hide.
- **The arrow keys** do the same on the radio tab: ← and → move a channel,
  and with shift a station. A slider with the focus keeps its own arrows.

At small window sizes the marks of 650 and 660 kHz lie a pixel or two apart
on the dial. The nearer mark wins a press, and the buttons step between the
two.

Verified from this repo's path:
- selfTest, 3734 passed and 0 failed, under jsc and osascript;
- the UI drive, 275 passed and 0 failed. It presses every station on the
  dial and the band, runs the buttons from one end of the dial to the other,
  and checks the keys and the switch;
- the display-list audit, 41 scenes with 0 layout problems;
- a mutation sweep of the 34 new mutants and the band press's, rewritten
  for the new code: all 35 caught. The other 178 were swept at 2026-09-24 a,
  all caught;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in its header comment):
- The arrow keys belong to a focused slider, and only to it. Skip a range
  input, not every input, or the arrows go dead once listen is ticked.
- A snap added to a plot moves old press tests onto its targets. Re-derive
  each press's distance to them.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-24 a — RLC Band-Pass Filters: the radio dial

`simulations/rlc_bandpass.html` has a seventh tab, key 7 (Cooper's ask: "Add
another tab that shows that a mechanical knob on a radio could switch from one
radio frequency to another, e.g. one circuit at a certain radio frequency and
another with different RLC. Could also show the old radio where you could hear
static between radio frequencies").

- **The knob** turns a variable capacitor through a 5:1 drive. The tab offers
  three plate shapes, each outline computed from its law: semicircular (C in
  proportion to the angle), straight-line frequency, and equal ratios. The
  knob can also be a switch that connects one of five fixed tuned circuits,
  each its own coil and capacitor.
- **The band:** ten made-up stations on the AM grid of the Americas. One to
  three tuned stages are ganged on the one shaft, each a coil of fixed Q, so
  the band widens toward 1700 kHz. There is a tuning eye on the AGC line.
- **The sound**, computed in the page and streamed when you tick listen: the
  station you are on, two stations and their whistle through one stage, or,
  between stations, the static the automatic gain control turns up to fill
  the loudspeaker. With the AGC off the set is nearly silent there, as a
  crystal set is. Lightning adds crackle.

Sources: eight more Wikipedia articles (Variable capacitor, Tuned radio
frequency receiver, Automatic gain control, Magic eye tube, Atmospheric noise,
Crystal radio, Envelope detector, Rayleigh distribution), 27 rows, each
verified by needle. `build_rlc/derive.py` checks the plate laws, the tank and
the noise bandwidths at 40 digits.

Found:
- Semicircular plates crowd the top of the dial: 1600 to 1700 kHz takes
  2.3° of the half turn and 530 to 630 kHz 53.3°. Straight-line-frequency
  plates give each 14.7°.
- The static between stations is the envelope of Gaussian noise, so it is
  Rayleigh-distributed. With the AGC holding its mean, its r.m.s. is
  √(4/π − 1) = 0.523 of the level held. The rendered sound, in half-second
  stretches, gives 0.522 to 0.526.

The card's paragraph now names the radio dial, and the TODO's CIRCUITS line
notes it. The build is in the Agent repo at `projects/simulations/build_rlc/`,
uncommitted; the branch `worktree-rlc-bandpass` is not pushed.

Verified from this repo's path:
- selfTest, 3705 passed and 0 failed, under jsc and osascript;
- the UI drive, 236 passed and 0 failed, with a fake sound card: the
  chunks butted end to end on the audio clock, an edit heard in the next
  chunks, the stream stopped on leaving the tab, and the branch with no
  Web Audio;
- the display-list audit, 41 scenes with 0 layout problems;
- a 179-mutant sweep with every mutant caught;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in its header comment):
- An AGC starts from nothing. Measure the level after several time constants,
  not 0.4 s after switch-on.
- The static's own peaks reach 6 r.m.s. in a second. A crackle detector
  sits at 10.
- Keep a stream's state on the absolute sample count, or the chunking
  changes the sound.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-23 c — RLC Band-Pass Filters joins the catalog, 68 sims

`simulations/rlc_bandpass.html` is new (Cooper's ask: "Make a simulation for
the different types/permuations of RLC bandpass filters under
~/coding/website/simulations/"). No network: it opens over `file://`, and
every sourced number is embedded.

Six views:
- **The permutations.** The twelve ways to put one R, one L and one C in the
  two arms of an L-section, each drawn as a circuit over its response. The
  census is computed: 2 pass a band, 2 stop one, 4 pass low frequencies and 4
  high ones. Only the resistor alone passes a band (across R in the loop,
  through R into the tank), and with the same parts the two Q's are
  reciprocal.
- **The series resonator.** The loop's phasors turning at the drive. The
  voltages across L and C are each Q times the source's at resonance and
  peak either side of f₀. The half-power points sit geometrically about f₀,
  and a source's own resistance lowers Q.
- **The parallel resonator.** The tank's circulating current, and a real
  coil's resistance pulling apart four "centre" frequencies: 1/2π√(LC), zero
  phase, the largest |Z| and the largest output, in a zoomed panel.
- **The ladder.** Butterworth, Chebyshev (five ripples) and Bessel
  prototypes of order 1 to 7 turned band-pass, a tank or a series arm first.
  It shows the element values, |S21|², |S11|², the group delay and the 1/FBW²
  spread of values, with the 455-kHz AM and 10.7-MHz FM IFs as presets.
- **Coupled tanks.** Two tanks joined by a top capacitor or a mutual
  inductance: under-, critically and over-coupled, their even and odd modes,
  the lopsided skirts, and the transmission at f₀ against kQ.
- **The s-plane.** |H(s)| as a surface for any of the circuits, the poles and
  zeros, and the exact response to a tone burst at f₀.

Sources and checks:
- **Sources** (fetched 2026-09-23 and verified by needle): nine Wikipedia
  articles (RLC circuit, the Butterworth, Chebyshev and Bessel filters,
  Prototype filter, Coupling coefficient of resonators, Intermediate
  frequency, Medium wave, FM broadcasting), 43 rows in all.
- **Twin.** Every computed number is pinned to `build_rlc/derive.py`, which
  shares no code with the page:
  - sympy for the twelve transfer functions, and a nodal solve;
  - mpmath at 40 digits, with every maximum found by root finding on the
    circuit itself;
  - 40-digit chain matrices for the ladders, their poles as zeros of 1/S21;
  - scipy DOP853 on each circuit's own state equations for the bursts.

Found in the sources:
- **The Chebyshev-filter article** prints 17.37 for 40/ln 10. The rounded
  constant moves the response by 10⁻⁴, so the page uses the exact one.
- **RLC circuit's** largest |Z| of a lossy tank (after Cartwright et al.) is
  right, but in double precision it subtracts two numbers near 2Q² and
  loses 4×10⁻¹² by Q = 1000. The page computes a rationalised form.
- **The coupled-resonator design rule** (Qₑ = g₀g₁/FBW, k = FBW/√(g₁g₂)) is
  in none of the fetched sources. The page checks it instead: the
  Chebyshev pair built by it dips 0.503 dB for the 0.5 dB asked.

Its card sits in Signals & Sound after the Synthesizer. The lede says
sixty-eight and the meta says 68. `simulations/TODO.txt` lists the page in
the catalog and as a done CIRCUITS item, and its "COMPLETED SIMULATIONS"
header counts the list.

The build (part files, the twin, the sources, the harnesses and the
landing scripts) is in the Agent repo at `projects/simulations/build_rlc/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-rlc-bandpass`, which is not pushed.

Verified from this repo's path:
- selfTest, 3385 passed and 0 failed, under jsc and osascript;
- the UI drive, 180 passed and 0 failed;
- the display-list audit, 35 scenes with 0 layout problems;
- a 125-mutant sweep with every mutant caught;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in its header comment):
- A window f₀(1 ± span) reaches negative frequencies once span > 1. There a
  mirrored second top appears and a log axis goes NaN. Windows about f₀ are
  geometric.
- A closed form that is right can still lose digits in doubles, like the
  printed |Z|max and the half-power point at small Q. Rationalise it, or take
  the reciprocal.
- Draw marker lines before plated labels. Two lines closer than a label is
  wide take their labels on their outer sides.
- A legend inside a plot can find nowhere clear and vanish. Keys go on the
  title line, and the tests count anything dropped.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-23 b — p–n Junctions & Transistors joins the catalog, 67 sims

`simulations/transistors.html` is new (Cooper's ask: "Under
~/coding/website/simulations/ please make a simulation for the basics of p-n
junctions and transistors"). No network: it opens over `file://`, and every
sourced number is embedded.

Six views:
- **The doped crystal.** Silicon as its bonds, doped with phosphorus, arsenic,
  antimony, boron, aluminium, gallium or indium from 10¹³ to 10¹⁸ cm⁻³, from
  30 to 700 K. Each bound carrier circles its atom at the radius the hydrogen
  model gives for that dopant's measured binding. Below, the same crystal in
  energy, with the Fermi level from charge neutrality and incomplete
  ionization. Beside, the carriers against temperature through freeze-out,
  the extrinsic plateau and the intrinsic rise.
- **The junction.** The p–n junction in equilibrium, solved exactly
  (Poisson's equation with Boltzmann carriers) against the depletion
  approximation: each ion with the carrier that neutralizes it, the
  densities, the field, the bands under a flat Fermi level, and drift and
  diffusion equal and opposite everywhere.
- **The diode.** A whole diode by drift-diffusion from −5 to +0.8 V against
  the Shockley equation and the depletion region's recombination current,
  with the quasi-Fermi levels, the carriers and the two currents. Under
  light it is a solar cell, with J_sc, V_oc, the maximum power point and the
  fill factor.
- **The bipolar transistor.** Electrons random-walking across the base with
  its diffusion constant, their sinh profile, the Early effect as base-width
  modulation, the output characteristics and the Gummel plot.
- **The MOSFET.** The exact surface potential under an n⁺ poly gate, the
  channel thinning to pinch-off, the bands in depth, and the charge-sheet
  current against the square law on linear and log axes.
- **The amplifier and the switch.** A common-source or common-emitter stage
  on its load line with its output and distortion, and a CMOS inverter's
  transfer curve, noise margins and switching delays.

Sources and checks:
- **Sources** (fetched 2026-09-23 and verified by needle): 67 values from 12
  sources: CODATA 2022; the Ioffe NSM archive for silicon; Wikipedia's
  mobility fits; the measured n_i of Misiakos & Tsamakis; the dopant
  degeneracies of Schenk, Altermatt & Schmithüsen (2006).
- **Twins.** Every computed number is pinned to three Python twins, which
  work independently of the page:
  - the junction's first integral at 40 digits and by scipy's solve_bvp;
  - the drift-diffusion equations solved with scipy's sparse LU (the page
    matches to 5×10⁻¹⁵);
  - the MOSFET by the exact Pao–Sah double integral, and the transistor's
    base by solve_bvp.

Found in the sources:
- **Ioffe's n_i formula** gives 8.7×10⁹ cm⁻³ at 300 K, 11 % below the
  measured 9.7×10⁹. The page uses the measured value.
- **The textbook square law** gives 1.81 times the charge-sheet current at
  V_GS = 1.5 V on this substrate. The body factor is 1.40; the rest is the
  surface potential running about 5 kT/q past 2φ_F.
- **Tsividis' closed-form charge sheet** reads 0.67 of the exact current in
  weak inversion; Brews' form, used here, reads 0.98–0.99.

Its card sits in Atoms, Matter & Light after Crystal Lattices. The lede says
sixty-seven and the meta says 67. `simulations/TODO.txt` lists the page in
the catalog and as a done PHYSICS item, and its "COMPLETED SIMULATIONS"
header counts the list.

The build (part files, the twins, the sources, the harnesses and the
landing scripts) is in the Agent repo at `projects/simulations/build_pn/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-pn-junctions`, which is not pushed.

Verified from this repo's path:
- selfTest, 1146 passed and 0 failed, under jsc and osascript;
- the UI drive, 268 passed and 0 failed;
- the display-list audit, 21 scenes with 0 layout problems;
- a 100-mutant sweep, every mutant caught once the survivors were pinned;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in the Agent changelog):
- A drift-diffusion solver must carry the quasi-Fermi potential relative to
  the contact. Absolute, its ulp at −2 V made the current jitter 5–57 %.
- Random walkers for minority carriers reflect at the injecting edge. Absorbed
  there, 98 % went straight back and the base looked empty.
- Carriers drawn at one global scale over ions at per-side scales make a
  neutral region look charged.
- An optimum read off a coarse sweep is only as good as its grid. The
  maximum power point is found on the solve itself.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-23 a — The Hohmann Transfer joins the catalog, 66 sims

`simulations/hohmann_transfer.html` is new (Cooper's ask: "Under
~/coding/website/simulations/ please make a simulation of the Hohmann
transfer as well as the periapsis and apoapsis"). No network: it opens over
`file://`, and every sourced number is embedded.

Six views:
- **The apsides.** Real orbits round the Earth, the Moon, Mars, Jupiter and
  the Sun (the ISS, GTO, Molniya, GEO, the Moon, a low lunar orbit, Phobos,
  MAVEN, Juno, the Earth, Mercury, Mars, Halley), or any two apsides. The
  nearest and farthest points carry each body's own names, from perigee and
  apogee to perihelion and aphelion. The craft moves by Kepler's equation,
  with twelve wedges of equal time, r(t), v(t) and the hodograph. A circle is
  shown as having no apsides at all.
- **The transfer.** Half an ellipse between two circles, with a burn at each
  apsis. It covers LEO to GEO and to the Moon, GEO down to LEO, Phobos to
  Deimos, and the Earth to Mercury, Venus, Mars, Jupiter and Saturn. The
  speed through the mission rises at each forward burn and still ends lower.
  The energy changes only at the burns.
- **One burn.** Any Δv, anywhere on the orbit, in any direction in the
  plane: the new apsides, the apse line turned, escape, or a periapsis in the
  ground. The same burn is scanned round the orbit to show the Oberth effect.
- **The budget.** The Hohmann cost peaks at R = 15.58. The bi-elliptic route
  breaks even at 11.94 and has a least far apoapsis for each R. Beside them
  are the bi-parabolic limit and the slow spiral.
- **The window.** The Earth and a planet on Hohmann's circles at the mean
  longitudes of JPL's Table 1, beside the real orbits. It shows the phase
  angle, the dates of the windows and the wait for the way home, with 48
  Mars launches since 1960 against the model's windows.
- **The precession.** The Earth's J₂ turning the apse line and the node, from
  an RK4 run against the first-order rates. It shows the critical inclination
  and Molniya, and Mercury's perihelion from the Schwarzschild orbit
  equation.

Sources and checks:
- **Sources** (fetched 2026-09-23 and verified by needle):
  - JPL Solar System Dynamics: the GMs (DE440), radii, the sidereal day,
    Standish's Table 1, and Halley from the SBDB at full precision;
  - 27 Wikipedia articles, for the apsis names, the worked examples, the
    orbits, J₂, Mercury's 42.9799″ and the list of Mars missions.
- **Twin.** Every computed number is pinned to `build_hohmann/derive.py`,
  which works independently of the page:
  - mpmath at 40 digits;
  - scipy DOP853 propagation of every preset, with no Kepler equation
    anywhere;
  - brentq windows;
  - operation-for-operation twins of the page's RK4 runs.

Found in the sources:
- **Wikipedia's LEO-to-GEO example** prints 2.42 + 1.46 = 3.88 km/s. That
  subtracts speeds already rounded; the burns are 2.4258 + 1.4668 =
  3.8926.
- **The Hohmann article** prints the peak cost as 53.0 %. It is 53.6 %.
- **Escobal's least-apoapsis table** (via Wikipedia) has a first root so flat
  that 5×10⁻⁹ v₁ moves it by 0.01.
- **The Molniya article's figure caption** keeps the satellite north of
  55.5° N for four hours either side of apogee. The orbit gives 2.96 hours,
  and the figure's own orbit 3.00.
- **The Mars launches** have a median 5.2 days after the circular model's
  window, with half between −20 and +26 days.

Its card sits in Astrophysics & Relativity after Lagrange Points. The lede
says sixty-six and the meta says 66. `simulations/TODO.txt` lists the page in
the catalog and as a done PHYSICS item, and its "COMPLETED SIMULATIONS"
header counts the list.

The build (part files, the twin, the sources, the harnesses and the
landing scripts) is in the Agent repo at `projects/simulations/build_hohmann/`,
uncommitted, beside the other builds. It was built on the Agent worktree
branch `worktree-hohmann-transfer`, which is not pushed.

Verified from this repo's path:
- selfTest, 1503 passed and 0 failed, under jsc and osascript;
- the UI drive, 210 passed and 0 failed;
- the display-list audit, 33 scenes with 0 layout problems;
- a 114-mutant sweep with every mutant caught;
- `dev/check_sims.py` on a staged tree.

Known-bad for this page (the full list is in its header comment):
- A curve sampled evenly in time steps over a deep periapsis. Sample an
  orbit in the eccentric anomaly, and draw each burn as a step at its
  instant.
- A label crossed by a dashed circle needs a plate. Where the dash runs on
  under the decimal point it still reads "2,945", so move the label.
- A caption that states a direction must be read in every state. It once
  said the speed "rises at each backward burn".
- HTML5 has no `&frac32;` or `&sup4;`, and a browser prints them as typed.
  The build now checks every entity against the HTML5 table.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-21 e — Loop Quantum Gravity: the mesoscale

`simulations/loop_quantum_gravity.html` has a fifth view at Cooper's ask, the
mesoscale between the quanta and the continuum. The weave's crossings are
counted in cells of side ℓ: below one quantum a cell they are single quanta;
with many quanta a cell the count is a smooth field plus Gaussian noise, drawn
beside the count as the mesoscopic approximation; in cells as large as the
curvature radius the bump is averaged away. The graininess, falling as 1/ℓ,
and the curvature across a cell, growing as ℓ², balance at ℓ* (46 Planck
lengths on the default sheet, 7 % error there), and the same balance for any
curvature radius puts ℓ* near 0.3 mm at Earth's surface and 2 nm on a
solar-mass black hole's horizon. The card's blurb mentions the mesoscale.

Built and verified in the Agent repo (changelog 2026-09-21 (e)); still in its
in-site form. Verified from this repo's path: selfTest (1120 passed, 0 failed)
under jsc and osascript, the UI drive (172 passed, 0 failed), and
`dev/check_sims.py` (65 sims, 65 copies, 65 cards, 0 problems).

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-21 d — Earth Observation, Live: the Copernicus point can be typed

Cooper's ask: "Under copernicus, there should be an option to manually change
the GPS coordinates, as clicking on the global map to a point is not precise
enough". The Copernicus view's "the place" group now has a coordinate box. It
reads decimal degrees (signed, or with N/S/E/W before or after, as in
"30.0444° N, 31.2357° E"), degrees and decimal minutes ("N 30 02.667 E 031
14.142"), and degrees, minutes and seconds ("30°02'40.0"N 31°14'08.5"E", as
Google Maps copies it). Enter or "go" applies it, and a line under the box
says what was read, in degrees-minutes-seconds, or why it was refused (a
latitude past 90°, 60 minutes, a minus sign with S or W, and so on). The box
follows a place chip or a map click, but never overwrites a half-typed entry.

The point is used as typed: the catalogue and scene searches are now keyed at
5 decimals (about 1 m) instead of 3 (about 110 m). A diamond marks the point
in the scene, placed from the scene's own projection metadata (its EPSG code
and the red band's affine transform, pinned against PROJ). Until a pixel is
clicked, the spectrum is the one at the point. The readout gives the point to
5 decimals, its UTM metres and its pixel in the 160 m overview.

Verified from this repo's path: the sim's selfTest (1667 passed, 0 failed)
under jsc and osascript and its UI drive (273 passed, 0 failed), a 95-mutant
sweep with every mutant caught, 0 layout problems at two sizes, and a live run
that puts the Nile point in the newest real scene at the pixel PROJ gives
(548, 84), with the same point pasted in degrees-minutes-seconds landing on
the same pixel. The count stays sixty-five.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-21 c — Loop Quantum Gravity: bigger weaves, and the uncertainty principle

`simulations/loop_quantum_gravity.html` updated at Cooper's asks: the weave can
grow to 1152 Planck lengths (from 709 to 183 908 rings), so the counted area
visibly settles on the classical one (the 1024-wide square: 1.0022 of its
classical area, shot noise ±0.29 %) and the plane, once the rings are too small
to draw, is shaded by its crossings; and the uncertainty principle is drawn
under the weave: area and the angle conjugate to it cannot both be sharp
(ΔA·Δξ ≥ a½/2), a squeeze trades one for the other, and as the square grows
both relative uncertainties fall as 1/√n̄ while ΔA itself grows as √n̄. The
default sheet is now 288 wide.

Built and verified in the Agent repo (changelog 2026-09-21 (c)); still in its
in-site form. Verified from this repo's path: selfTest (853 passed, 0 failed)
under jsc and osascript, the UI drive (136 passed, 0 failed), and
`dev/check_sims.py` (65 sims, 65 copies, 65 cards, 0 problems).

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-21 b — Earth Observation, Live joins the catalog, 65 sims

`simulations/earth_observation.html` is new (Cooper's ask: "a simulation under
~/coding/website/simulations/ in which we pull and use the free real-time data
from NASA Worldview/Earthdata and Lance, MODIS, VIIRS, NOAAA GOES, ESA
copernicus Data, Sentinel etc. and visualize it"). It is the first page in the
catalog that needs the network, which the ask requires: every source is free,
keyless and CORS-open, fetched only when a view needs it, with timeouts and
every failure shown in the readout, and offline it still draws its models on
CelesTrak elements embedded at build time.

Six views. Today's Earth: the LANCE MODIS or VIIRS mosaic of a UTC day, with
a science overlay whose colours are read back into values, under the page's
own SGP4 swath edges, equator times, sun glint and daytime coverage by
latitude against the picture, and NASA's published ground track measured
against the orbit. Geostationary: GOES-East and -West, Himawari, Meteosat 0°
and IODC resampled onto each satellite's fixed grid, three hours of frames,
cloud-top temperature, height and parallax, and the whole ring. Fires: a day
of FIRMS detections, their power-law tail, Dozier's two-channel fire
temperature, and pixel size against the scan geometry. Copernicus: the Data
Space catalogue over a point against predicted overpasses, and a Sentinel-2
L2A scene read from its COGs (composites, indices, a pixel's spectrum). The
fleet: 27 satellites on a globe from live elements. Space weather: GOES
X-rays and flare classes, SUVI, Kp, and the OVATION aurora with its horizon
line.

Built in this repo's worktree branch `worktree-earth-observation` (not
pushed) and landed as the page alone. The build (`build_eo/`: the part files,
the Python twins, the validation scripts and the source extracts) now sits in
the Agent repo at `projects/simulations/build_eo/`, uncommitted, beside the
other builds. This repo is served as it stands, `dev/` included, so the build
must not be merged here; the branch's last commit removes it.

Pinned to independent twins: SGP4 against python-sgp4 (1e-9 km), the
Earth-fixed rotation against skyfield, geodesy, UTM and the GOES-R fixed grid
against PROJ, the Sun against DE421, Planck and Dozier against scipy, the
coverage against a point-by-point brute force, and the MVT, colour-map, TIFF
and inflate decoders against Python's. Checked against the data (recorded in
`build_eo/validation/README.md`): the model's daytime coverage against the
day's pictures (Aqua to 2.5 points per latitude); VIIRS's aggregation zones
and MODIS's pixel growth read off 1200 FIRMS detections placed on the orbit;
the geostationary disk on NOAA's own GOES-19 image to the pixel; and every
Sentinel product over the Nile delta in 30 days against the predicted passes
(S1 5/5, S2 18/18, S3 30/31, S5P 60/60). Found on the way: TROPOMI's swath is
its 108° field of view, not "2600 km" (seven products were missed, and at
2600 km SentiWiki's own 95 % coverage statement fails); NASA's published orbit
tracks sit 12–17 km west of SGP4 on the same elements, whichever way the
satellite travels; Terra's and Aqua's elements put their equator crossings at
8:40 and 15:41 local time.

Its card sits in Astrophysics & Relativity after Lagrange Points. The lede
says sixty-five and no longer says "no network" of every page (it excepts this
one), and the meta says 65. `simulations/TODO.txt` lists it in the catalog and
as a done PHYSICS item, and its "COMPLETED SIMULATIONS" header counts the list
(59). `dev/check_sims.py` learned the count words for 65 to 68.

Verified from this repo's path: the sim's selfTest (1601 passed, 0 failed)
under jsc and osascript and its UI drive (247 passed, 0 failed), the
display-list audit (16 scenes, 0 layout problems), a 75-mutant sweep with
every mutant caught, a live run of the page's own loaders under deno (49 of 49
services answering, every image decoded), and `dev/check_sims.py` (65 sims,
65 copies, 65 cards, 0 problems) run on a staged tree whose sources are the
site copies with the two nav rewrites undone.

Known-bad for this page (the full list is in its header comment):
- GIBS WMS answers sub-daily geostationary requests with HTTP 200 and an empty
  picture: build frames from WMTS tiles, and decode every image a smoke test
  fetches.
- GIBS lists a frame before all its tiles exist, and a tile can answer 200 and
  then 404: a frame is all its tiles or nothing.
- Earth Search's `earthsearch:boa_offset_applied`: never apply the -0.1 offset
  again.
- Natural Earth closes Antarctica along the pole: never break a fill at that
  longitude jump.
- A world map drawn full-bleed under the floating readout hides north-east Asia
  at the whole-world zoom.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-21 a — Loop Quantum Gravity joins the catalog, 64 sims

`simulations/loop_quantum_gravity.html` is new (Cooper's ask: "a simple
visualization of how quantum gravity knits together loops for Loop Quantum
Gravity … how it creates a mesh or chain-mail-like lattice to create an
emergent classical continuous field"). Four views: an arrow carried round a
loop on a curved surface comes back turned by the curvature inside, and the
gauge orbit (every starting frame) leaves that angle alone; plaquettes knit
into one loop because their inner edges cancel, and holonomy per area becomes
the curvature as they shrink; a weave of spin-½ rings, the chain mail, gives a
surface one quantum of area per crossing, the classical area on large scales,
and a smooth area density when the crossings are coarse-grained; and the area
spectrum 8πγ l_P² Σ√(j(j+1)), with γ from three countings of black-hole
horizon states.

Built and verified in the Agent repo (build: `projects/simulations/build_lqg/`,
changelog 2026-09-21 (a); built 2026-09-18) and written straight into this repo's form, like
clebsch_gordan: `href="../index.html"` and
`href="../../modules/teaching_modules.html"`, no `../website/` href, so no
`sync_sims.py` rewrite.

Sourced: CODATA 2022 (Planck length and time), Meissner 2004 (γ =
0.23753295796592), Ghosh and Mitra (γ ≈ 0.274), Domagała and Lewandowski
2004 (the area eigenvalues), ABCK's ln 2/(π√3) and the weave and
coarse-graining abstracts. The page is pinned to an independent twin (mpmath,
scipy, numpy). One finding on the way: Meissner's aside value 0.273985635 for
the 2j + 1 weighting is that equation's root with the sum stopped at j = 5;
the full sum gives 0.2740669.

Its card sits in Astrophysics & Relativity after Doppler & Causality; the lede
and meta say sixty-four. `simulations/TODO.txt` lists it in the catalog and as
a done PHYSICS item, and its "COMPLETED SIMULATIONS" header counts the list
(58). `dev/check_sims.py` already knew the count word for 64.

Verified from this repo's path: the sim's selfTest (662 passed, 0 failed)
under jsc and osascript and its UI drive (123 passed, 0 failed), and
`dev/check_sims.py` (64 sims, 64 copies, 64 cards, 0 problems) run on a staged tree whose sources are the site
copies with the two nav rewrites undone.

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-18 c — Clebsch–Gordan Coefficients joins the catalog, 63 sims

`simulations/clebsch_gordan.html` is new (Cooper's ask: "an interactive
Clebsh-Gordan coefficients and how they correspond to the Bra-Ket notation"):
two angular momenta, the product kets |j₁ m₁⟩|j₂ m₂⟩ and the coupled kets
|J M⟩, and the coefficients ⟨j₁ m₁; j₂ m₂|J M⟩ that are the brackets between
them. Six views: a ket written out with the exact coefficient and its bracket
under every term, and the Born rule sampled from it; the whole change-of-basis
matrix, or the PDG's own layout of it; the ladder-operator construction step by
step; the vector model against its classical limit; the Breit–Rabi levels of
hydrogen (21 cm), rubidium-87, caesium-133 and sodium 3p in a field, where the
field turns one basis into the other; and why a rotation never changes J.

Built and verified in the Agent repo (build: `projects/simulations/build_cg/`,
changelog 2026-09-18 (c)) and written straight into this repo's form: it
carries `href="../index.html"` and `href="../../modules/teaching_modules.html"`
and no `../website/` href, so it needs no `sync_sims.py` rewrite.

Every coefficient is exact (the Racah formula in integer arithmetic), and the
page is pinned to an independent twin (sympy, numpy, mpmath) that agrees with
141 entries read from the PDG 2026 table. The atoms use CODATA 2022 and
D. A. Steck's alkali data (2025); the Landé factors of sodium's 3p computed
from |CG|² weights land 0.43σ and 0.55σ from the measured ones, and the clock
shifts match Steck's printed 427.45 and 575.15 Hz/G².

Its card sits in Quantum Mechanics after Bloch Sphere; the lede and meta say
sixty-three. `simulations/TODO.txt` lists it in the catalog and as a done
PHYSICS item, and its "COMPLETED SIMULATIONS" header now counts the list (57);
it had stayed at 55 when organic_mechanisms landed. `dev/check_sims.py`
already knew the count word for 63.

Verified from this repo's path: the sim's selfTest (2085 passed, 0 failed)
under jsc and osascript and its UI drive (177 passed, 0 failed), and
`dev/check_sims.py` (63 sims, 63 copies, 63 cards, 0 problems) run on a staged
tree whose sources are the site copies with the two nav rewrites undone (the
check still looks for `../simulations`, the old Agent layout).

Left uncommitted, per this changelog's header. Not pushed.

## 2026-09-18 b — Organic Mechanisms joins the catalog, 62 sims

`simulations/organic_mechanisms.html` is new: why HBr adds to propene one way
round and not the other, and what has to change for it to add the other way.
Six views — the ionic addition stepped through in 3-D with its curly arrows,
the carbocation ladder that Markovnikov's rule is really about, the peroxide
radical chain that reverses it, hydroboration that never makes an intermediate
at all, the 1,2-shifts that give a cation away, and a ledger with the
ratio-against-barrier-gap master curve and a Curtin–Hammett demonstration.

Built and verified in the Agent repo (`projects/simulations/` changelog
2026-09-18 (b)) and written straight into this repo's form, so it needs no
`sync_sims.py` rewrite: it already carries `href="../index.html"` and
`href="../../modules/teaching_modules.html"` and no `../website/` href.

Every bond energy and reaction enthalpy in it is computed at run time from
gas-phase enthalpies of formation fetched from the NIST Chemistry WebBook
(CODATA review values for the atoms and hydrogen halides, Tsang 1996 for the
alkyl radicals, Furuyama 1969 for the halopropanes), so nothing is a table
lookup. Three independent checks agree: the cation ladder by two routes to
0.10 kJ/mol, those cation enthalpies against Hunter & Lias proton affinities to
2.14 kJ/mol, and Furuyama's over-determined set closing to 0.26 kJ/mol.

Its card sits in Atoms, Matter & Light after Amino Acids in 3-D, the lede and
meta count say sixty-two, and `simulations/TODO.txt` lists it both in the
catalog and as a completed chemistry item. `dev/check_sims.py` already knew the
count word for 62.

Verified from this repo's paths: the sim's selfTest (582 passed, 0 failed) and
UI drive (221 passed, 0 failed) under osascript, the display-list audit (30
scenes, 0 layout problems), and a 59-mutant mutation sweep with every mutant
caught.

Note, unchanged from 2026-09-18 a: `dev/sync_sims.py` and `dev/check_sims.py`
still look for their sources in `../simulations`, the old Agent layout. That
folder does not exist beside this repo, so both need a staged source tree (or
`--source` for `sync_sims.py`) to run.

## 2026-09-18 a — Amino Acids in 3-D joins the catalog, 61 sims

`simulations/amino_acids.html` is new: the twenty amino acids as turning 3-D
molecules, their handedness (L, its mirror and the D form), the chain and its
helices, the hard-sphere Ramachandran map and the genetic code. It was built
and verified in the Agent repo (`projects/simulations/` changelog
2026-09-17 (a)) and arrives here as that source with exactly the two
`dev/sync_sims.py` nav rewrites. Its card sits in Atoms, Matter & Light after
The Standard Model from Symmetry, the lede and meta count say sixty-one,
`simulations/TODO.txt` lists it as completed (55), and `dev/check_sims.py`
knows the count words for 61–64. Each of these files now matches its
Agent-side counterpart byte for byte (the same landing, made there on
2026-09-17).

Verified from this repo's paths: the sim's selfTest (3100 passed, 0 failed)
and UI drive (173 passed, 0 failed) under osascript, and `dev/check_sims.py`
(61 sims, 61 copies, 61 cards, 0 problems) run against the original sources
out of the Agent repo's git history.

Note: `dev/sync_sims.py` and `dev/check_sims.py` still look for their sources
in `../simulations`, the old Agent layout. That folder does not exist beside
this repo, so both need a staged source tree (or `--source` for
`sync_sims.py`) to run.

## 2026-09-17 e — the preview draws to canvas, so a "save PDFs" browser cannot blank it

Cooper reported View still downloading the file and the viewer showing black.
Both come from one cause, and it is not the server: `curl -I` on
`https://cooper-watson.net/CV.pdf` returns `content-type: application/pdf`
with **no `Content-Disposition`, no CSP and no `X-Frame-Options`**, and the
deployed page was confirmed current. The browser is configured to save PDFs
rather than display them (Firefox: Applications -> PDF -> Save File; Chrome:
"Download PDFs instead of automatically opening them"). Under that setting an
`<iframe>` pointed at a PDF fires the download and renders nothing, so the
frame showed `--bg-1` through — the "black" box.

The `<iframe>` was therefore the wrong mechanism: correct for a default
browser, silently broken for anyone who has changed that preference. The
viewer now renders with **PDF.js onto `<canvas>`**, which never touches the
browser's PDF handler, so the preview behaves the same whatever the setting.
Pages render lazily via `IntersectionObserver` (600px margin) and closing the
viewer calls `pdf.destroy()`, so a 28-page article does not rasterise pages
nobody scrolled to. Page slots carry the first page's `aspect-ratio`, so the
scroll height is right before anything is drawn.

PDF.js 3.11.174 (UMD) loads from jsdelivr — the same CDN the modules browser
already uses for KaTeX — and is fetched only on the first View click. Verified
both URLs live (`pdf.min.js` 320 KB, `pdf.worker.min.js` 1.09 MB, HTTP 200) and
that the bundle assigns `window.pdfjsLib`, which is the entry point the script
uses. If the CDN is unreachable the viewer shows "Preview unavailable" plus a
working new-tab link rather than failing silently; with JavaScript off the
control is still a plain link to the PDF.

The dead `.doc-frame` / `.doc-fallback` rules are removed. Verified: both pages
tag-balanced (0 errors), `dev/check_links.py` green, no stale class references
left in either page or the stylesheet. **Could not check:** the rendering path
was not executed — no node/deno/browser here — so this is verified structurally
and against the live CDN, not visually.

Trade-off worth knowing: the preview now needs network access. Self-hosting
pdfjs-dist (~1.4 MB in the repo) would remove that if the CDN dependency is
unwanted.

Left uncommitted, per this changelog's header.

## 2026-09-17 d — "View PDF" opens the document in the page, not another copy of it

Two related complaints from Cooper: View and Download "appear to do the same
thing", and the CV page loaded its PDF viewer before anyone asked for it.

They were not literally identical — `download` saves the file, `target="_blank"`
opens a tab — but both just handed you the PDF, so the difference was invisible,
and a browser configured to save PDFs rather than display them makes them truly
identical. View now does something Download cannot: it builds an `<iframe>` into
an empty slot in the page and toggles to "Hide preview"; Download still saves.

New `pdf_view.js` (1.6 KB, no dependencies) delegates one click listener on the
document. The viewer is created on first click and **torn down on the second**,
so a nine-PDF page never fetches a document nobody opened — which is also the CV
fix: `cv.html`'s eager `<object>` is gone, replaced by the same empty
`<div class="doc-box" hidden>`.

Progressive enhancement: the control is still a plain link to the PDF with
`target="_blank"`, so with JavaScript off, or if the script 404s, it opens in a
new tab as before. Modified clicks (ctrl/cmd/shift/alt, middle button) are let
through untouched.

Verified: 8 viewer slots and 8 `js-view` links on research.html, 1 and 1 on
cv.html, every `data-target` resolves to a slot, all 9 PDF paths exist, **zero
eager `<object>`/`<iframe>` left in either page**, both tag-balanced (0 errors),
`dev/check_links.py` green. **Could not check:** the JS was not executed — no
node/deno on this machine — so the toggle is verified structurally, not at
runtime.

Left uncommitted, per this changelog's header.

## 2026-09-17 c — Research and CV pages are real: abstracts, view, download

Both pages were still the scaffolded placeholders ("Coming soon", and a TODO to
turn the CV badge into a real link). Cooper uploaded eight PDFs to
`my_articles/` and `CV.pdf` to the site root, so both are now filled in.

**Research.** One card per publication, newest first: title, author list with
Cooper's name marked, venue/volume/year, a DOI link, the abstract behind a
native `<details>` disclosure (no script), and *View PDF* / *Download* buttons.
Eight entries — PRA 113 063523 (2026), Fluct. Noise Lett. 25 2640002 (2026) and
its erratum, Symmetry 18 182 (2026), Universe 11 389 (2025), Symmetry 13 1469
(2021), Particles 3 642–659 (2020), Universe 6 11 (2020).

**CV.** An inline `<object>` preview of `CV.pdf` with a fallback paragraph for
browsers that will not render a PDF inline (most mobile ones), plus the same
View/Download pair and a link across to Research.

`style.css` gains one block at the end — `.pub-list`/`.pub`, the `details.abs`
disclosure, `.btn`/`.btn-row`, `.doc-frame` — in the existing azure palette, no
new colors and no webfonts.

Titles, authors, venues, DOIs and abstracts were **transcribed from the PDFs,
not recalled**: every DOI is the one printed in its own file. Two text repairs
were needed — the World Scientific files use a legacy encoding where `®`, `¯`
and `°` stand for *ff*, *fi* and *fl* (so "Kadano®–Baym" is Kadanoff–Baym), and
the Particles abstract lost an em dash in extraction ("four independent
curvature invariants—the Ricci scalar"). Verified: all 37 local links resolve,
both pages tag-balanced (0 errors), `dev/check_links.py` green.

The PDFs are ~15 MB total (largest `universe-06-00011-v2.pdf` at 8.45 MB, well
under the 100 MB file limit). Left uncommitted, per this changelog's header.

## 2026-09-17 b — the module browser is 14 pages, 3.8 MB (was one 29.7 MB page)

Regenerated with the generator's new split (modules changelog 2026-09-17 b):
`teaching_modules.html` is a ~30 KB index and each trunk is its own
`modules_<TRUNK>.html`, with figures referenced as lazily-loaded `<img>`
instead of inlined — they were 89% of the old page. Largest page is now
0.60 MB; NE went 7.44 MB -> 0.48 MB.

Old deep links are unaffected: the index forwards `#<id>` to the trunk page
that holds it, so the Teaching Network's "open module" links and any bookmark
keep working. `dev/check_links.py` passes here (270 sections over 13 trunk
pages, 143 netlinks); all 455 figure refs resolve.

**The 13 `modules_*.html` files are new and must be committed** or the index
will forward to pages that are not on the site. Left uncommitted, per this
changelog's header.

## 2026-09-17 a — the module browser's links now work on the deployed site

Every link out of `modules/teaching_modules.html` pointed at `../website/...`
— the six nav tabs and all 143 Teaching-Network back-links — which resolves to
`/website/...` here and 404s, because Pages serves the repo root and `modules/`
sits under it rather than beside it. The *inbound* links were never broken:
`../modules/teaching_modules.html` from a root page is clamped to
`/modules/...` per RFC 3986, so it lands correctly.

Regenerated with the generator's new `--deploy` flag (modules changelog
2026-09-17 a), so the links are now `../index.html`, `../teaching.html#CM-01`,
and so on. All six targets confirmed present at the repo root;
`dev/check_links.py` passes here (270 sections, 143 netlinks, all checks
passed). Added `.nojekyll`: nothing uses Jekyll and the site is 2,590 files,
so the build step is pure overhead.

Left uncommitted, per this changelog's header.

## 2026-09-16 c — The Standard Model from Symmetry joins the catalog, 60 sims

`standard_model.html` landed in `projects/simulations/` (simulations
changelog 2026-09-16 (h)): the gauge groups and their generators, one
generation with its anomalies, the Higgs potential and the masses, the
eightfold way with PDG 2026 masses, colour singlets and SU(6), and the
running couplings. A card in Atoms, Matter &amp; Light after Nuclear Clocks,
the lede and meta count moved to sixty, and the sim added to the completed
list at the bottom of `simulations/TODO.txt`; `dev/sync_sims.py` +
`dev/check_sims.py` green (60 sims, 60 copies, 60 cards).

## 2026-09-16 b — a WIP section at the bottom of the catalog

At Cooper's ask, `simulations.html` gets a last section titled WIP, and the
six sims he counts as work in progress move into it: Quaternions (from
Mathematics &amp; Machines) and the five SBS pages (from Scattering &amp;
Brillouin Physics) — `sbs_sims`, `sbs_axes_phase`, `sbs_gaslaw_manifold`,
`sbs_parent_law`, `sbs_state_surface`. The cards are moved byte-for-byte,
nothing else changes, and the count stays fifty-nine; `dev/check_sims.py`
green (59 sims, 59 copies, 59 cards). The same split is listed at the
bottom of `simulations/TODO.txt`. When one of these is finished, move its
card back to its subject section.

## 2026-09-16 a — Lagrange Points joins the catalog, 59 sims

`lagrange_points.html` landed in `projects/simulations/` (simulations
changelog 2026-09-16 (g)): the five points in the rotating frame, the
effective potential as a landscape, stability and Routh's limit, the SOHO
and JWST halos, the Queqiao halo and the Gateway NRHO, Jupiter's trojans and
the horseshoes. A card in Astrophysics &amp; Relativity after the
Ephemerides, the lede and meta count moved to fifty-nine, `dev/sync_sims.py`
+ `dev/check_sims.py` green (59 sims, 59 copies, 59 cards).

## 2026-09-15 e — Buoyancy joins the catalog, 58 sims

`buoyancy.html` landed in `projects/simulations/` (simulations changelog
2026-09-15 (d)): Archimedes' principle from the spring scale to the
metacentre, the golden crown, the Cartesian diver and the balloon. A card in
Fluids &amp; Flight, the lede and meta count moved to fifty-eight,
`dev/sync_sims.py` + `dev/check_sims.py` green (58 sims, 58 copies, 58 cards).

## 2026-09-15 d — Light Scattering: the sky from six worlds

`simulations/scattering.html` re-synced from `projects/simulations/` after its
BLUE SKY view was rebuilt (see the simulations changelog, 2026-09-15 (c)):
the sun's elevation runs from +90° to −18° through sunset and the three
twilights, and world chips switch the atmosphere between Earth, Earth without
ozone, Mars, Venus, Titan and the Moon. The Light Scattering card on
`simulations.html` now says so. `dev/sync_sims.py` + `dev/check_sims.py`
green; the copy differs from the source only by the two nav-href rewrites.

## 2026-09-15 b — the catalog catches up: eight new cards, 57 sims
### Changed
- simulations.html: eight sims that existed in projects/simulations/ but had
  no card — wave_fronts (uncarded since 2026-08-14), doppler_causality,
  pupil_plane_interferometry, sbs_state_surface, pascals_triangle, primes,
  and today's brachistochrone and cycloids — each get a card in their
  subject section, copy distilled from the sim's own header; the lede and
  meta description say fifty-seven. `dev/sync_sims.py` re-run: 57 copies in
  website/simulations/, the seven that were missing on the site now
  present, no dead cards, no uncarded sims.
- dev/check_sims.py (new): an INDEPENDENT check of the sync, sharing no
  code with sync_sims.py — copied set = source set, every copy byte-equal to
  its source apart from exactly the two documented nav-href rewrites, no
  un-rewritten href, nav targets intact, cards ↔ copies a bijection with no
  duplicates, the page tag-balanced, and the lede/meta count equal to the
  card count. Exit 1 on any problem; run it after every sync.
- projects/simulations/build_cycloid/land_site_cards.py: the idempotent
  card inserter used for this batch (anchor card + section, count words
  recomputed), so the same cards can be applied to any copy of the page.
### Verified
- check_sims.py: 57 sims, 57 copies, 57 cards, 0 problems — in the
  worktree and again against the main checkout after landing.

## 2026-09-15 c — arrival by deep link no longer clips the modules page header
### Changed
- dev/render_check/links_harness.js: the `modules` run now lays the sidebar
  out (trunk 30 px, topic 24 px, item 34 px, list 600 px tall) and checks
  that arriving by hash scrolls ONLY the list (never the page or the reading
  column), keeps the trunk heading in view when the item fits below it,
  clears a stale filter, pins the top again at `load`, and that a click
  nudges only an item that is out of view: 29 checks (was 20). The fix
  itself is in generate_webpage.py — modules changelog, same date.
### Verified
- check_links.py all green: 17 static checks, harness 28/28 (network),
  29/29 (modules).

## 2026-09-15 a — Teaching ↔ Modules: every orb opens its module, every module travels back
### Changed
- teaching.html + teaching_network.js: the panel gains an **open module**
  link (`../modules/teaching_modules.html#<id>`; a trunk hub says "browse
  the MA modules"; the CMx/QC stubs, which have no folders, show nothing).
  The page now answers deep links: `teaching.html#CM-22` glides from the
  whole sky to that orb on load, the URL follows your travel
  (`history.replaceState`, so Back still leaves the page), double-click fit
  clears it, and a hashchange travels. Two DOM-free helpers join the core,
  `nodeFromHash` / `moduleHref`. Drawing untouched: the four
  record_teaching.js display lists are byte-identical before and after.
- dev/build_network.py: bakes an 8th node field, has-module-page (folder
  `projects/modules/<TRUNK>/<ID>_*/` exists; a hub: any module in its
  trunk), so the link is offered only where a page exists, and warns when
  the network lists a module with no folder. **Rerun it when a module
  lands, not only when topic_network.txt changes.** Positions and edges
  unchanged.
- style.css: `.net-module`, plus a `[hidden]` guard inside the panel (an
  `inline-block` rule would otherwise defeat the `hidden` attribute).
- dev/check_links.py + dev/render_check/links_harness.js: the round-trip
  audit — flags ↔ folders ↔ module sections ↔ back-links (a bijection over
  the 143 module nodes; 10 hubs), teaching.html tag balance, and both
  pages' scripts driven headlessly under deno against stub DOMs (hash →
  orb, chip travel, hub/stub/garbage/empty hashes, double-click; hash →
  module for bare, `m-`-prefixed, trunk, Thermo and underscore ids, junk,
  sidebar click, lazy render). From projects/website/:
  `python3 dev/check_links.py`.
- The modules side (generate_webpage.py: hash routing + the per-module
  back-link) is in the modules changelog, same date.
### Verified
- check_links.py all green: 17 static checks, harness 28/28 (network) and
  20/20 (modules). Baked DATA: the first seven fields of all 155 nodes, all
  261 edges and the trunk names identical to before; flags 143/143 modules,
  10/12 hubs. Old-vs-new record_teaching.js frames: 4/4 `cmp` clean.
- Not verifiable here (no headless browser on this Mac): a real-browser
  pass. The glide-on-load and `replaceState` over `file://` are the two
  things worth a look.

## 2026-08-14 b — edits.txt: name, email, ORCID, CV link
### Changed
- Per Cooper's `edits.txt`: the homepage now says **Cooper K. Watson**
  (h1, title, meta description, footer); About's contact card switches the
  email to cooper_watson@tamu.edu and gains an ORCID link
  (0000-0001-8245-541X) and a link to the CV page. The CV file itself
  (cv.pdf) still doesn't exist — the link points at cv.html until it does.
### Verified
- Both pages tag-balanced (html.parser); mailto/ORCID/CV hrefs grepped at
  their destinations; other pages' name/footer deliberately unchanged
  (edits.txt says homepage).

## 2026-08-14 a — the whole catalog: all 49 simulations
### Changed
- simulations.html: the six launch cards become the full catalog — every
  sim in projects/simulations/ (49 today), grouped into eleven subject
  sections from Mechanics & Control to Mathematics & Machines, each
  description distilled from the sim's own header comment. The original
  six cards keep their copy.
- dev/sync_sims.py: the hand-kept SIMS list is gone. The script now
  discovers every top-level `*.html` in the source directory (finished
  sims land there by house rule, so discovery IS the catalog), copies all
  of them with the two nav-href rewrites, deletes stale copies whose
  source is gone, and audits simulations.html against the copied set —
  a card linking a missing sim is an ERROR, a copied sim with no card a
  WARNING. Adding a sim to the site is now: land the sim, add its card,
  rerun `python3 dev/sync_sims.py` from projects/website/.
- style.css: `.sim-catalog` section spacing for the grouped gallery.
### Verified
- Independent checker (not the sync script itself): all 49 copies are
  byte-equal to source-plus-exactly-the-two-documented-rewrites; no
  un-rewritten `../website/` or `../modules/` hrefs remain; every copy
  keeps its `../index.html` and `../../modules/` nav targets; card hrefs
  ↔ copied files is a bijection with no duplicate cards; simulations.html
  tag-balanced. Re-verified from the main checkout after landing.

## 2026-08-12 f — Modules tab in the site nav
### Changed
- All six pages' header nav gains **Modules** between Teaching and
  Simulations, pointing at `../modules/teaching_modules.html` (the generated
  modules browser; it marks itself current). The homepage hero pills are
  deliberately unchanged — Modules is a header tab only.
- `dev/sync_sims.py`: second rewrite for the in-site sim copies,
  `href="../modules/` → `href="../../modules/`; copies re-synced.
- Note: the Modules tab points one level OUTSIDE the site folder, so it is
  the one nav target that would need copying in (or dropping) if the folder
  is ever deployed alone; everything else stays self-contained.
### Verified
- Nav audit: 6/6 pages + 6/6 sim copies — full seven-tab order, correct
  Modules href per location, correct aria-current; target file exists.

## 2026-08-12 e — sims wear the site theme; sync rewrites nav hrefs
### Changed
- Every sim in projects/simulations/ now carries this site's background
  (`#070b18`) and the six-tab site nav — see the simulations changelog,
  2026-08-12 (d). In the source tree the tabs point at `../website/*.html`;
  `dev/sync_sims.py` now rewrites `href="../website/` → `href="../` while
  copying, so the six in-site copies navigate inside the self-contained site
  folder. Copies re-synced (their sha256s now differ from the source by
  exactly that rewrite).
### Verified
- All six copies: site-nav present, zero `../website/` hrefs left, every
  rewritten target (`../index.html` … `../cv.html`) exists; sims' selfTests
  green from the copied path.

## 2026-08-12 d — first six simulations on the site
### Added
- `simulations/` — the site's own copies of six sims from
  projects/simulations/ (orbitals, steam_carnot_cycle, lattice, ephemerides,
  synth, cart_pendulum), placed by `dev/sync_sims.py` so the site stays one
  self-contained folder (file:// now, static hosting later).
  **projects/simulations/ remains the source of truth** — after a sim changes
  there, rerun from projects/website/: `python3 dev/sync_sims.py`. To put
  another sim on the site: add it to SIMS in that script + a card in
  simulations.html.
- simulations.html: placeholder cards replaced by six whole-card launch links,
  descriptions distilled from each sim's own header comment; `a.card` hover
  styling in style.css.
- Note: the request said "lattics.html"; the actual file is `lattice.html`.
### Verified
- Tag balance on simulations.html; all six card hrefs resolve to the copied
  files; sync_sims.py prints size + sha256 per copy; main-checkout landing
  re-synced from the default source path and byte-compared clean.

## 2026-08-12 c — network interaction fix; blue void; homepage stars
### Fixed
- teaching.html ignored all mouse input (no pan, no zoom, no click-travel)
  while rendering fine. Root cause: the full-viewport `.page` overlay holding
  the nav and panel sits at z-index 1 above the canvas, so it received every
  pointer/wheel event and the canvas listeners never fired. Fix in style.css:
  `pointer-events: none` on the overlay, restored to `auto` on the nav links
  and the panel; plus `touch-action: none` on the canvas so touch drags pan
  the sky instead of scrolling the page. (See Known-bad.)
### Changed
- The void is now the site's dark blue (vertical gradient `#070b18 →
  `#04060c`, the other pages' background) instead of pure black; the black
  orbs now read as true black discs against it.
- Stars glimmer like the homepage: same size/alpha/twinkle parameters, same
  ice-blue `#9fd8ff`, occasional cross flares; parallax layers kept.
- Verified headlessly: overview frame pair differs (op counts 1101/1099,
  mean|diff| 0.02/255 — smooth twinkle), arrival frame diff 1.76/255; frames
  inspected for the blue gradient, star flares, and orb contrast.

## 2026-08-12 b — teaching network page
### Added
- `teaching.html` is now the network: an empty near-black void, sparse specks
  of light glimmering, every topic a small black orb outlined by a thin white
  halo. Data = `projects/modules/topic_network.txt` — 155 nodes (143 modules +
  12 trunk hubs), 261 edges (129 prerequisite-chain, 84 `~`cross-links, 38 KEY
  BRIDGES segments, 10 hub spokes) — baked into `teaching_network.js` by
  `dev/build_network.py`, so the page stays `file://` (nothing fetched).
  Constellation layout: hubs pinned on an affinity-ordered ring (big trunks
  interleaved with small), each trunk's chain wound as an arc-length spiral;
  cross-links/bridges render as long faint threads (bridges brighter). Click
  an orb to glide there; drag pans; wheel zooms about the cursor; double-click
  empty void fits the whole sky. Side panel lists the current topic and its
  links as travel buttons (bridge links first). `prefers-reduced-motion` gets
  static frames + instant travel; hidden tabs pause.
- `dev/build_network.py` — parser (trunk sections, module lines, `~` tags,
  KEY BRIDGES incl. wrapped lines; consecutive ids in a bridge become edges,
  `..` ranges contribute endpoints) + seeded constellation layout + DATA
  baking between AUTO-GENERATED markers; `--preview` renders the layout to a
  PNG. Rerun from `projects/website/` after editing topic_network.txt:
  `python3 dev/build_network.py`
- `dev/render_check/record_teaching.js`; `rasterise.py` gained arc + fillText.
### Verified
- Parse: 0 unresolved cross-links. Layout previewed: 12 separated clusters.
- Headless frames: overview pair differs in 115/161 speck alphas (glimmer),
  glide-mid and CM-22 arrival differ 2.3–3.2/255 (travel), orbs render as
  black discs + thin white rings; a synthwave frame re-rasterised unchanged
  as a regression check after the rasteriser upgrade.

## 2026-08-12 a — initial skeleton
### Added
- Six linked pages: `index.html` (homepage), `about.html`, `teaching.html`,
  `simulations.html`, `research.html`, `cv.html`, sharing `style.css` and a
  common top nav (`aria-current` marks the active page). Placeholder copy is
  tagged with `<!-- TODO -->` comments.
- `synthwave.js` — homepage background canvas. Layout after
  `watermarked_preview.mp4` (flat perspective floor grid scrolling slowly
  toward the viewer, wireframe mountains at the horizon, starfield sky);
  palette sampled from `example_wave.mp4` frames (sky `#123453→#173f65`, mesh
  ramp `#123a63→#0b5a94→#1089c4→#1bbeeb→#7deeff`), background pulled darker
  than the video per `README.md` ("soft dark violet/blue") — deliberately NOT
  the preview's magenta/orange. The ridge is a triangulated mesh whose heights
  drift through 2-octave value noise (~20 s features + slow swell), per
  `example_wave.mp4`. Deterministic (seeded PRNG / integer-hash noise), honors
  `prefers-reduced-motion` (static frame), pauses when the tab is hidden,
  devicePixelRatio-aware. Drawing core is DOM-free for headless verification.
- `dev/render_check/` — no headless browser on this Mac, so: `record_frames.js`
  (deno) loads `synthwave.js` with a stub 2D context and records display
  lists; `rasterise.py` (matplotlib) turns them into PNGs and prints
  frame-to-frame mean|diff| as the motion check. Regenerate with:
  `cd dev/render_check && deno run --allow-read --allow-write record_frames.js`
  `&& python3 rasterise.py out/frame_*.json`. PNG/JSON outputs are generated
  artifacts — don't commit them.
### Verified
- Frames rasterised at t = 0 / 2.5 / 5 / 7.5 s and inspected against the two
  reference videos; nonzero frame-to-frame diffs confirm the ridge undulates
  and the floor scrolls. Cross-links between all six pages checked by hand.
