# The gas engine — `p2_engine.js`

This is the hard-disk gas behind `gas-properties.html`, kept in one part file.
It has no DOM and no view state, so `gases-intro` and `diffusion` can be built
on it unchanged: concatenate it after `p1_utils.js`, as `assemble.py` does. The
tests that pin it are in `p7_test.js`, and the Python twin is `derive.py`. Read
the Known-bad list in `projects/simulations/CHANGELOG.md` before extending it.

## Units and frame (PhET's)

The units are pm, ps and AMU. Speed is in pm/ps, which is exactly m/s. Kinetic
energy is in AMU pm²/ps²; `zJ(e)` in `p3_state.js` converts it with PhET's
1.66e-27 kg per AMU.

The origin is the container's **bottom-right** corner:

- x runs from `g.left = −W` to 0;
- y runs from 0 to `H` = 8750;
- the depth `D` is 4000 and only enters the volume `V = W·H·D`.

A particle enters at `(−r, H/5)`. Every constant in `GAS` was read from the
minified original (`docs/phets/gas-properties_en.html`, 1.1.10). Change
none of them without changing the pins.

## API

**Build a gas**

`gasMake(o)` accepts these options:

| option | effect |
|---|---|
| `width` | the container width |
| `wRange` | the width range |
| `height` | the container height |
| `depth` | the container depth |
| `species:[{m,r},{m,r}]` | species 0 and 1; heavy and light by default |
| `seed` | the random stream (mulberry32) |
| `collisions` | default `true` |
| `doesWork` | the Explore wall |
| `wallSpeed` | the wall's speed limit |
| `noLid` | Diffusion has no lid |
| `virial` | keep the virial ledger |
| `noise` | the gauge noise |

**Add and remove particles**

| function | what it does |
|---|---|
| `gasInject(g,k,n,T?)` | PhET's pump and spinners. `n` particles at `(−r, H/5)`, speed `√(3kT_i/m)`, directions in a π/2 fan pointing left. With collisions on and `n > 1` the `T_i` are Gaussian about `T` (σ = 0.2T) with the mean restored exactly. Stops at 1000 per species. `T` defaults to `gasInjectT(g)`: `g.injectT`, else the current T, else 300 K. |
| `gasFill(g,k,n,T,delta?,region?)` | A house addition, not PhET's. Uniform non-overlapping positions (rejection, 200 tries) with 2-D Maxwell–Boltzmann velocities rescaled so the batch is exactly at `T`. With `delta`, every particle has the same speed. |
| `gasScatter(g,k,n,T,x0,x1)` | PhET's Diffusion placement: uniform in `[x0, x1]` with no overlap rejection, every particle at `√(3kT/m)` in a random direction. |
| `gasRemove(g,k,n)` | Removes the most recently added particles of species `k` (PhET's removeLastParticles). |
| `gasRemoveAll(g)` | Removes every particle. |
| `gasSetCount(g,k,n)` | Injects or removes to reach `n`. |
| `gasSetTemp(g,T)` | PhET's setTemperature: every KE is scaled by the same factor. |
| `gasPush(g,k,x,y,vx,vy)` | Places one disk explicitly (used by the tests). |

**Time**

- `gasStep(g, dt)` is one frame of PhET's step. It runs the substeps, then the
  counter, the stopwatch and `gasUpdate`: the hold-constant compensation, T, the
  gauge, the lid, the maximum temperature and the Oops cases. Last come the
  sampler and the flow counter.
- One frame is `GAS.DT_FRAME = 1/24` ps: PhET's 1 ps = 0.4 s at 60 fps. Slow
  is `GAS.DT_SLOW`, and the step button is `GAS.STEP = 0.2` ps.
- `gasRefresh(g)` re-derives T, P and the gauge without time passing. Use it
  after any change made while paused.

**The container**

| function | what it does |
|---|---|
| `gasResize(g,w,redistribute)` | The Ideal wall. No work is done; the x positions are scaled about the right wall. |
| `g.wantW` (with `doesWork`) | The Explore wall: it moves at up to `g.wallSpeed` and does work. |
| `gasSetLid` | Sets the lid width. |
| `gasBlowLid` | PhET's rule: the lid blows off unless the gap is already ≥ 1500 pm. |
| `gasReturnLid` | Puts the lid back. |
| `gasOpenLeft` / `gasOpenRight` / `gasOpening` / `gasLidOpen` | The gap in the lid. |
| `gasSetDivided` | Puts the Diffusion divider in or takes it out. |

**Hold constant**

- `gasSetHold(g,mode)` sets the mode and refuses what PhET disables: T needs
  particles and a closed lid; the P modes need P > 0.
- `gasHoldAllowed(g,mode)` answers the same question without setting anything.
- The modes are `'nothing'`, `'volume'`, `'temperature'`, `'pressureV'` and
  `'pressureT'`.
- An impossible request sets `g.oops` to a key of `GAS_OOPS` (PhET's text) and
  drops the hold to `'nothing'`. `g.oops` is the model's flag; the view clears
  it when the next action begins.

**PhET's displayed quantities**

| name | meaning |
|---|---|
| `g.T`, `gasTemp(g,k?)` | T = (2/3)⟨KE⟩/k; `null` when the box is empty |
| `g.P` | NkT/V in kPa, 0 until the first wall hit |
| `g.gaugeP` | the gauge's value: refreshed every 0.75 ps, with PhET's noise law |
| `gasPressureOf(N,T,V)` | NkT/V in kPa for any state |

**Statistics**

- `gasBinCounts(g,k,w,nb,energy)` uses PhET's `floor(v/w)` binning.
- `gasSamplerOn(g)` with `g.sampler.out` and `.mean` gives the 1-ps averages of
  the Energy screen.
- `gasMeanSpeedOf(g,k)` is the species' mean speed.
- `gasCOM(g,k)` is the centre of mass, measured from the box's middle.
- `gasSideData(g)` gives the Diffusion Data panel.
- `gasFlowOn(g)` with `g.flow.rateL/rateR` gives the flow counts, crossings of
  the divider line averaged over 300 frames.
- `gasWallForce(g)` gives the momentum per unit time delivered to each wall.

**Diffusion's settings** (PhET's DiffusionParticleSystem)

| function | what it does |
|---|---|
| `gasDiffCount(g,k,n,T)` | Adds in the species' own half. Removing re-speeds the rest, as PhET does. |
| `gasDiffMassTemp(g,k,m,T)` | Every particle of the species goes to `√(3kT/m)`. |
| `gasDiffRadius(g,k,r,playing)` | Sets the radius. |
| `gasDiffRestart(...)` | The divider back in: everything is regenerated. |

**Exact laws**, for views and tests

- 2-D Maxwell–Boltzmann, with `kT2 = gasKT2(T) = (3/2)kT`: `mbSpeedPdf`,
  `mbSpeedCdf`, `mbEnergyPdf`, `mbEnergyCdf`, `mbMeanSpeed`, `mbModeSpeed`,
  `mbRmsSpeed`.
- The finite-N closed-box law: `mcEnergyCdf`.
- Hard disks: `hdB2`, `HD_B3_RATIO`, `hdContact` (the contact measure of a
  rectangle), `hdZ1`, `hdZ` and `hdAdiabatRatio` (the quasi-static adiabat).
- `gasSound(kT2, m̄)`.

**Ledgers**

- `gasLedgerReset(g)` and `gasLedger(g)` give the energy ledger, with the
  residual.
- `gasVirialReset(g)` and `gasVirial(g)` give the virial ledger (`virial:true`).
- `gasImpulseReset(g)` restarts the wall impulses and `g.imp.E`, the energy
  carried by wall hits.

## How a step works, and why it is exact

Each substep is event-driven:

1. The grid is built with cells `C = σ_max + 2·v_b·h`, where
   `v_b = √(4·KE_max/m_min)` bounds every speed after one binary collision.
   Any pair that can touch within the substep then starts in adjacent cells.
2. Every wall event and pair event is predicted and pushed on a heap. One
   routine, `gasPredict(g,i,t0,h,L0,u,G,half)`, does both the opening
   prediction (`half`: each pair once, from its lower index) and every
   re-prediction, so each wall, lid and pair rule lives in one place.
3. Events are processed in time order. Each particle is advanced lazily to the
   event time, the event is resolved, and the particle's own events are
   re-predicted.
4. Each disk carries a stamp `g.st[i]` that counts its events. An event records
   the stamps of its disk(s) when predicted and is skipped when either stamp
   has moved on (`g.stats.stale` counts the skips). Run R5 pins both checks:
   a pair event stale in its partner, one stale in its owner, and a wall event
   whose disk was struck first; processing any of them kicks a disk that is
   touching nothing.

The contact time is the earlier root of `|dp + t·dv|² = σ²`, in the
cancellation-free form `c/(−b + √(b² − ac))` (`derive.py` section 2 checks it
in exact rationals). The number of substeps is a speed knob, not an accuracy
one: halving it is an equivalent mutant, and the sweep reports it as one.

## Invariants (each pinned in `selfTest`)

- **Elastic.** Pair impulses conserve momentum and energy to rounding: over
  5000 random collisions with masses from 1 to 40, the worst errors are
  3.4e-16 and 1.5e-15. Stationary walls flip one velocity component exactly.
- **Moving wall.** It returns `v′ = 2u − v` (elastic). PhET's `u − v` does half
  the work. It is **not** implemented; the difference is documented.
- **Overlap rule.** Disks that overlap get no pair event, so they pass through
  each other until they separate, as in PhET. This is what lets the pump inject
  every particle at one point.
- **No overlaps from dynamics.** Disks that start apart never come closer than
  σ: 400 disks at area fraction 0.22, all pairs every frame for 4 ps. The same
  overlap rule hides a missed collision from the energy and the statistics, so
  run this check after any change to the event search.
- **Energy ledger.**
  `KE == E0 + work + heatQ + inj − rem − esc + setT`
  closes to 1e-15 relative.
- **Virial ledger.**
  `Δ(Σ m r·v) == ∫2KE dt + Σ_walls r·J + Σ_pairs σ|J| + heat + escapes`
  closes to about 1e-15 of its terms, event by event.
- **Brute-force parity.** Runs R1–R5 agree with the O(N²) event-driven MD in
  `derive.py` to better than 1e-6 pm, with identical event counts.
- **Statistics.** Energy fractions follow Dirichlet(1,…,1); disks of different
  masses share the energy equally; the collisional Z resolves B₃; wall hits
  carry (3/2)kT₂ (effusion); a slow push follows the hard-disk adiabat.
  Every tolerance comes from the exact sampling law, not a guess.
- **Determinism.** Each `gasMake` owns its stream, `g.rng`. The gauge noise
  has its own stream, `g.noise`, so turning the noise off never changes the
  particle trajectories.

## Traps for a reuser

- **A dense pump start is O(N²).** Injecting hundreds of particles at once puts
  them all in one grid cell until they spread. 1000 + 1000 in the 10 nm box is
  about 70 ms per frame under osascript: correct, but slow.
- **Keep `gasRefresh` after paused edits.** PhET only shows a pressure after a
  wall hit, and `g.pOn` records whether one has happened. A pre-filled box
  needs `g.pOn = true` followed by `gasRefresh(g)`.
- **Guard auto-ranged axes.** `ticksFor` in the shared layer spins for ever
  when an axis span is below the rounding of its endpoints. `niceRange()` in
  `p4_views.js` is the guard. Use it on any auto-ranged axis.
- **Species indices, not names.** Species are 0 and 1 everywhere.
  `g.species[k]` holds `{m, r}`, and changing it changes every particle of that
  species at once.
- **Escaped particles stay in the arrays** (`g.out[i] = 1`) until they are 30 nm
  away. `gasCount` excludes them.
