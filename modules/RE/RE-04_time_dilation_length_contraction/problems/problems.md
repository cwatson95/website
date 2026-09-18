# RE-04 — Problems

Work them by hand, then check with `code/sr_effects.py`. Sources in `../refs.md`.

### P1. The cosmic-ray muon  *(Griffiths 4e, Ex. 12.1, p.511)*
Muons are created ~10 km up (`d ≈ 33` light-μs) with rest-frame mean life
`τ₀ = 2.2 μs` and travel down at `β = 0.98`. What fraction reaches the ground —
(a) ignoring relativity, (b) with time dilation? Why is the *muon's*-frame story
(a contracted atmosphere) the same answer?
*Answer:* naive `e^{−33/(0.98·2.2)} ≈ 2×10⁻⁷` (≈ none); relativistic
`e^{−33/(γ·0.98·2.2)}` with `γ = 5.03`, ≈ `0.048` (~5%, as observed).
*Check:* `muon_fraction(2.2, 0.98, 33.0) → (0.0476, 2.25e-07)`; the ratio is ~10⁵.

**Solution.** The muon covers $d=33$ light-μs in lab time $d/\beta$ (with $c=1$),
surviving a fraction $\exp(-t_\text{life}/\tau)$ where $t_\text{life}$ is read on its
own clock. (a) Ignoring dilation its mean life stays $\tau_0$, so
$$\frac{N}{N_0}=e^{-d/(\beta\tau_0)}=e^{-33/(0.98\cdot2.2)}=e^{-15.31}\approx2.25\times10^{-7}\ (\approx\text{none}).$$
(b) Time dilation stretches the lab mean life to $\gamma\tau_0$ with $\gamma=1/\sqrt{1-0.98^2}=5.025$, so
$$\frac{N}{N_0}=e^{-d/(\gamma\beta\tau_0)}=e^{-3.046}\approx0.048\ (\sim5\%).$$
In the muon's frame nothing is dilated — the atmosphere is instead contracted to
$d/\gamma$, giving the *same* exponent. This reproduces `muon_fraction(2.2, 0.98, 33.0) → (0.0476, 2.25e-07)`, a ratio $\sim10^5$.

### P2. Measuring a moving rod  *(Griffiths 4e, §12.1.2, p.508)*
A rod has rest length `L₀ = 1 m`. It flies past at `β = 0.6`. (a) What length do you
measure, and *what must you do simultaneously* to measure it? (b) Recover `L₀` from
your measurement. (c) Show the same γ governs the time dilation of a clock on the
rod.
*Answer:* `L = L₀/γ = 0.8 m` (mark both ends at one instant of *your* frame);
`L₀ = γL = 1 m`; `γ = 1.25` dilates a 1 s tick to 1.25 s.
*Check:* `length_contraction(1.0, 0.6) → 0.8`; `rest_length(0.8, 0.6) → 1.0`;
`time_dilation(1.0, 0.6) → 1.25`.

**Solution.** With $\beta=0.6$, $\gamma=1/\sqrt{1-\beta^2}=1/\sqrt{1-0.36}=1/0.8=1.25$.
(a) The measured length is $L=L_0/\gamma=1/1.25=0.8$ m; to measure a *moving* rod you
must mark **both ends at the same instant of your frame** ($\Delta t=0$), else it
shifts between the markings. (b) Inverting, $L_0=\gamma L=1.25\cdot0.8=1.0$ m.
(c) The *same* $\gamma$ dilates a clock riding the rod: a 1 s proper tick stretches to
$\Delta t=\gamma\,\Delta\tau=1.25$ s — contraction and dilation are one boost read two
ways ($\Delta x'=0$ vs $\Delta t=0$). This gives `length_contraction(1.0, 0.6) → 0.8`,
`rest_length(0.8, 0.6) → 1.0`, and `time_dilation(1.0, 0.6) → 1.25`.

### P3. Leading clocks lag  *(Griffiths 4e, §12.1.2, p.508; relativity of simultaneity)*
Two clocks `L₀ = 10` (light-units) apart are synchronised in their own frame, which
moves past you at `β = 0.5`. At one instant of *your* frame, which reads ahead and
by how much?
*Answer:* the **trailing** clock reads ahead; the leading one lags by
`βL₀ = 0.5·10 = 5`.
*Check:* `leading_clocks_lag(10.0, 0.5) → 5.0`; `leading_clocks_lag(10.0, 0.0) → 0`
(no motion ⇒ synchronised in every frame).

**Solution.** Synchronised in their own frame, both clocks read $t'=0$. Reading
$t'=\gamma(t-\beta x)$ at one instant of *your* frame (fixed $t$) gives
$\Delta t'=-\gamma\beta\,\Delta x$; with the contracted separation $\Delta x=L_0/\gamma$,
$$\Delta t'=-\gamma\beta\,(L_0/\gamma)=-\beta L_0=-0.5\cdot10=-5.$$
The **leading** clock (in front, along the motion) reads $\beta L_0=5$ *behind*, so the
**trailing** clock reads ahead by $5$. At $\beta=0$ the offset vanishes — clocks synced
in one frame stay synced in every frame. This matches `leading_clocks_lag(10.0, 0.5) → 5.0`
and `leading_clocks_lag(10.0, 0.0) → 0`.

### P4. The twin paradox  *(Griffiths 4e, Ex. 12.2 / Prob. 12.16, pp.513, 524)*
A twin travels at `β = 0.8` while the home clock logs `T = 30 yr` for the round
trip. (a) How much does the traveller age? (b) Why is this *not* symmetric (each
"sees the other slow"), and where does the missing time go? (c) What happens to the
gap as `β → 0`?
*Answer:* traveller ages `T/γ = 30/1.667 = 18 yr` (younger by 12). Only the
traveller changes frames at the turnaround; her simultaneity slice sweeps across
the home worldline, ageing the home twin by exactly the deficit. As `β → 0` the gap
→ 0.
*Check:* `twin_ages(0.8, 30.0) → (30.0, 18.0)`; `twin_ages(1e-4, 30.0) ≈ (30, 30)`.

**Solution.** With $\beta=0.8$, $\gamma=1/\sqrt{1-0.8^2}=1/\sqrt{0.36}=1/0.6=1.667$.
(a) The home twin ages by the coordinate time $T=30$ yr; the traveller's clock runs
slow the whole trip, logging proper time $T/\gamma=30/1.667=18$ yr — younger by $12$.
(b) It is **not** symmetric because only the traveller **changes inertial frame** at the
turnaround; there her line of simultaneity sweeps across the home worldline, ageing the
home twin suddenly by exactly the missing $12$ yr (a $\beta L_0$-type jump). (c) As
$\beta\to0$, $\gamma\to1$ and $T/\gamma\to T$, so the gap closes. Hence
`twin_ages(0.8, 30.0) → (30.0, 18.0)` and `twin_ages(1e-4, 30.0) ≈ (30, 30)`.

### P5. The barn and the ladder  *(Griffiths 4e, Ex. 12.3, p.516)*
A pole of rest length `L₀ = 10` runs at `β = 0.6` through a barn of length
`L_barn = 10` with a door at each end. (a) Does it fit, with both doors shut at
once? (b) The pole's frame says it can't possibly fit — reconcile.
*Answer:* in the barn frame the pole contracts to `L₀/γ = 8 ≤ 10`, so yes — both
doors shut *simultaneously*. In the pole frame the barn is only `8` long and the
two door-shuts are **not** simultaneous (separated by `γβL_barn = 7.5`): the far
door opens before the near one shuts. Same events, different "now."
*Check:* `pole_in_barn(10, 10, 0.6)` → `contracted_pole = 8.0`,
`fits_in_barn_frame = True`, `door_gap_barn = 0.0`, `door_gap_pole = 7.5`.

**Solution.** With $\beta=0.6$, $\gamma=1.25$. (a) In the **barn** frame the pole
contracts to $L_0/\gamma=10/1.25=8\le10=L_\text{barn}$, so it momentarily fits and both
doors can shut **simultaneously** ($\Delta t_\text{barn}=0$) with the pole inside.
(b) In the **pole** frame the *barn* is contracted to $L_\text{barn}/\gamma=8<10$, so the
pole cannot fit. Those same two door-shut events — simultaneous for the barn — are
separated in the pole frame by
$$\Delta t_\text{pole}=\gamma\beta L_\text{barn}=1.25\cdot0.6\cdot10=7.5,$$
the far door shutting (and reopening) before the near one, so the pole is never enclosed.
Same events, different "now": `pole_in_barn(10, 10, 0.6)` → `contracted_pole = 8.0`,
`fits_in_barn_frame = True`, `door_gap_barn = 0.0`, `door_gap_pole = 7.5`.

### P6. Scissoring the axes  *(Zee III.4; Minkowski diagram)*
On a Minkowski diagram (`ct` up, `x` across) draw the `ct′`- and `x′`-axes for a
frame moving at `β = 0.6`. (a) What are their slopes? (b) Show they tilt toward the
light line `ct = x` by equal angles. (c) What is that angle?
*Answer:* `ct′`-axis is `x = βct` (slope `1/β = 1.667`); `x′`-axis is `ct = βx`
(slope `β = 0.6`). The slopes are reciprocals ⇒ mirror images about `ct = x`; each
tilts by `arctan β = 30.96°`.
*Check:* `boosted_axes(0.6) → ([1.0, 0.6], [0.6, 1.0])`; slopes `ct/x` are
`1/0.6` and `0.6`, product `1.0`.

**Solution.** The $ct'$-axis is the worldline of the moving origin $x'=0$, i.e.
$x=\beta ct$, with direction $(ct,x)=(1,\beta)$ and slope $ct/x=1/\beta=1/0.6=1.667$.
The $x'$-axis is the simultaneity locus $ct'=0$, i.e. $ct=\beta x$, direction
$(\beta,1)$, slope $ct/x=\beta=0.6$. (b) The slopes $1/\beta$ and $\beta$ are reciprocals
(product $1$), so the axes are mirror images about the light line $ct=x$ — they
**scissor** toward it through equal angles. (c) That common tilt is
$\arctan\beta=\arctan0.6=30.96^\circ$. So `boosted_axes(0.6) → ([1.0, 0.6], [0.6, 1.0])`,
whose slopes $ct/x$ are $1/0.6$ and $0.6$ with product $1.0$.
