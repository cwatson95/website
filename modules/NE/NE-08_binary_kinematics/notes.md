# NE-08 — Binary reaction kinematics, thresholds and the Coulomb barrier (notes)

`~NE-04` computed $Q$-values and stopped there: $Q>0$ means a reaction releases
energy, $Q<0$ means it costs energy. That is a statement about *bookkeeping*, and
it is not the same as a statement about what actually happens when you fire a
beam at a target. Two things stand between an allowed reaction and an observed
one, and neither is visible in $Q$ alone.

The first is **momentum**. Energy conservation alone would let an endoergic
reaction proceed the instant the projectile carries $|Q|$. But the incident
particle brings momentum as well as energy, and that momentum must be conserved:
the products cannot be born at rest in the laboratory. The kinetic energy locked
into the motion of the centre of mass is unavailable, so the beam must supply
$|Q|$ *plus* that share.

The second is **charge**. The strong force has a range of a few femtometres, so
the projectile must physically reach the target's surface. A charged projectile
must climb the Coulomb hill to get there — regardless of the sign of $Q$. This is
why ⁹Be(α,n)¹²C releases 5.7 MeV and still needs a 2.6 MeV alpha source, and why
neutron-induced reactions run at room temperature while everything else needs an
accelerator or a star.

The last third of the chapter specialises the same kinematics to a neutron
bouncing elastically off a nucleus, and out falls the energy-loss law that
governs moderation — the reason reactors are built around light elements.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§6.1–6.5, cited by **printed** page (PDF = printed + 23). Masses from
`../data_tables/B1_atomic_masses.csv`.

## 1. The binary reaction and the compound nucleus

Everything here concerns the two-body reaction [S&F Eq. (6.1), p. 136]
$$x+X\longrightarrow y+Y,\qquad\text{written compactly as } X(x,y)Y.$$
Most such reactions proceed through a short-lived **compound nucleus**
[S&F Eq. (6.2), §6.1.1]
$$x+X\longrightarrow (x+X)^{*}\longrightarrow y+Y,$$
which lives long enough ($\sim10^{-14}$ s, against $\sim10^{-22}$ s for the
crossing time) to forget how it was made. That amnesia is why the same excited
nucleus can be reached by several entry channels and decay through several exit
channels — the structure of S&F Example 6.1 and of Chapter 6's problems 1–4.

## 2. Where the threshold comes from

Energy conservation gives [S&F Eqs. (6.4)–(6.7), p. 139]
$$Q=(m_x+m_X-m_y-m_Y)c^2 = E_y+E_Y-E_x,$$
and momentum conservation adds a second constraint. Eliminating the unobserved
product $Y$ between them gives the master equation of the chapter, a quadratic in
$\sqrt{E_y}$ [S&F Eqs. (6.10)–(6.11), p. 140]. For $Q<0$ its square root turns
real only above [S&F Eq. (6.14), p. 142]
$$\boxed{\;E_x^{th}=-Q\,\frac{m_y+m_Y}{m_y+m_Y-m_x}\;}$$
— `threshold_energy`. Since the rest masses dwarf $Q/c^2$, $m_y+m_Y\simeq m_x+m_X$
and this collapses to the form everyone actually uses [S&F Eq. (6.15)]
$$E_x^{th}\simeq -Q\left(1+\frac{m_x}{m_X}\right)$$
— `threshold_energy_approx`. The two agree to about a part in $10^4$
(`test_exact_and_approximate_thresholds_agree`).

The physical content is clearest through the **centre-of-mass split**. Of the
laboratory energy $E_x$, only
$$E_{cm}=E_x\frac{m_X}{m_x+m_X}$$
is available to rearrange nucleons; the rest rides along with the centre of mass
and is untouchable (`cm_kinetic_energy`). Setting $E_{cm}=|Q|$ reproduces
Eq. (6.15) exactly — `test_threshold_delivers_exactly_the_q_value_in_the_cm_frame`
— and at that beam energy the products are born at rest in the CM frame.

The penalty is therefore governed by the **mass ratio alone**:

| projectile / target | $E_x^{th}/|Q|$ | comment |
|---|---|---|
| n on ²³⁸U | 1.004 | 0.4% wasted; the naive answer is nearly right |
| p on ⁷Li | 1.144 | 14% |
| α on ⁹Be | 1.444 | 44% |
| d on d | 2.000 | half the beam energy is wasted |

`~NE-04`'s `threshold_energy_naive` returns $|Q|$ and is deliberately named: it is
a **lower bound only**, and quoting it is a standard student error.

## 3. The Coulomb barrier

A neutron or photon reaches the nucleus unimpeded. A charged projectile does not.
The work done pushing charge $Z_xe$ against charge $Z_Xe$ from infinity to
separation $b$ is [S&F Eq. (6.17), p. 143]
$$W_C=\frac{Z_xZ_Xe^2}{4\pi\epsilon_0 b},$$
and the reaction needs the surfaces to touch, $b=R_x+R_X=R_o(A_x^{1/3}+A_X^{1/3})$
[S&F Eq. (6.18)]. With $R_o=1.2$ fm and
$e^2/4\pi\epsilon_0=1.43996$ MeV·fm — which divide to 1.20 MeV — this is
[S&F Eq. (6.19), p. 144]
$$\boxed{\;E_x^{C}\simeq 1.20\,\frac{Z_xZ_X}{A_x^{1/3}+A_X^{1/3}}\ \text{MeV}\;}$$
— `coulomb_barrier`. Note this is derived treating the target as fixed, so it is
a **laboratory** requirement and enters Eq. (6.20) directly.

| projectile + target | $E_x^C$ (MeV) |
|---|---|
| n + ²³⁵U | 0 |
| d + t | 0.44 |
| p + ⁷Li | 1.24 |
| α + ⁹Be | 2.62 |
| α + ²³⁸U | 28.4 |

Two consequences do most of the work in the rest of the trunk. **Neutrons feel no
barrier at all**, at any energy, against any target — so a fission chain can be
sustained by particles with millivolts of kinetic energy (`~NE-13`, `~NE-19`).
And a charged-particle reaction can be violently exoergic and still need an
accelerator, because $Q$ and $E_x^C$ are independent quantities.

The barrier energy is not *lost*: the target recoils, the compound nucleus takes
$E_x^C(m_x/M_{cn})$ and the remainder excites it, and on decay the whole of
$E_x^C$ reappears in the products (S&F, p. 144). That is why
`minimum_product_energy` returns $Q+(E_x^{th})_{\min}$ and is never negative.

Two thresholds, and the reaction needs whichever is higher [S&F Eq. (6.20)]:
$$(E_x^{th})_{\min}=\max\!\left(E_x^{C},\,E_x^{th}\right)$$
— `overall_threshold`. S&F Example 6.1 tabulates all of this for three routes to
¹⁵N\*, and `test_reproduces_example_6_1` reproduces every column:

| reaction | $Q$ | $E_x^C$ | $E_x^{th}$ | governed by | $\min(E_y+E_Y)$ |
|---|---|---|---|---|---|
| ¹³C(d,t)¹²C | +1.311 | 1.994 | 0 | Coulomb | 3.305 |
| ¹⁴C(p,n)¹⁴N | −0.626 | 2.111 | 0.671 | Coulomb | 1.485 |
| ¹⁴N(n,α)¹¹B | −0.158 | 0 | 0.170 | kinematic | 0.011 |

Note the pattern: for the two charged projectiles the Coulomb hurdle wins even
when the reaction is endoergic, and for the neutron there is no contest.

## 4. A digression that pays off later: hitting an electron

Put an electron in the target slot — $m_X=m_y=m_e$, $m_x=m_Y=M$, $Q=0$ — and the
master equation gives the recoil electron energy [S&F Eq. (6.21), p. 146]
$$E_e=4\frac{m_e}{M}E_M\cos^2\theta_e,\qquad
(E_e)_{\max}=4\frac{m_e}{M}E_M .$$
A 4 MeV alpha can lose at most **2.2 keV** to one electron: 0.05% of its energy.
So a heavy charged particle needs tens of thousands of collisions to stop, and
travels in almost a straight line while doing it — the origin of the sharp,
well-defined range and the Bragg peak of `~NE-14`, and the reason alpha particles
are stopped by a sheet of paper yet deposit everything within it.

## 5. Elastic neutron scattering, and why moderators are light

Specialise to a neutron ($m_x=m_y=m_n$) elastically scattering ($Q=0$) off a
nucleus of mass number $A\equiv M/m_n$. The master equation becomes
[S&F Eq. (6.25), p. 148]
$$\frac{E'}{E}=\frac{\left[\cos\theta_s+\sqrt{A^2-1+\cos^2\theta_s}\right]^2}{(A+1)^2}$$
— `elastic_scattering_energy_ratio`. Its two extremes [S&F Eq. (6.27)] are
$$E'_{\max}=E \quad(\theta_s=0),\qquad
E'_{\min}=\alpha E \quad(\theta_s=\pi),\qquad
\boxed{\;\alpha\equiv\left(\frac{A-1}{A+1}\right)^{2}}$$
— `alpha_collision`. Everything about moderation follows from $\alpha$.

- $\alpha(^{1}\mathrm{H})=0$: a head-on hit on a proton stops a neutron **dead**.
  Hydrogen is unique in this.
- $\alpha(^{238}\mathrm{U})=0.983$: a neutron never loses more than 1.7% to a
  uranium nucleus.

Hydrogen also has a peculiarity worth knowing (S&F Example 6.3): for $A=1$ the
kinematics reduce to $E'/E=\cos^2\theta_s$ with $0\le\theta_s\le\pi/2$ — **a
neutron cannot backscatter from a proton at all**, exactly as a billiard ball
cannot bounce back off an identical ball. `test_hydrogen_forbids_backscatter`
pins it.

For low-energy neutrons the scattering is isotropic in the CM frame, which makes
$E'$ uniform on $[\alpha E, E]$, so the mean is the midpoint
[S&F Eq. (6.28)]
$$\bar{E}'=\tfrac{1}{2}(1+\alpha)E,\qquad
(\Delta E)_{av}=\tfrac{1}{2}(1-\alpha)E .$$
Note the consequence: **as the neutron slows, its absolute energy loss shrinks in
proportion**. Slowing down is geometric, not arithmetic, which is why the natural
variable is $\ln E$. The mean logarithmic loss per collision is
[S&F Eq. (6.29), p. 149]
$$\boxed{\;\xi\equiv\left\langle \ln\frac{E}{E'}\right\rangle=1+\frac{\alpha\ln\alpha}{1-\alpha}\;}$$
— `average_log_energy_decrement`, with $\xi=1$ exactly for $A=1$. Its decisive
property is that **$\xi$ does not depend on energy**, so the collisions needed to
cross a given energy range is simply [S&F Eq. (6.30)]
$$n=\frac{1}{\xi}\ln\frac{E_1}{E_2}$$
— `collisions_to_thermalize`. S&F Table 6.1 (p. 150), reproduced exactly by
`test_reproduces_table_6_1`:

| material | $A$ | $\alpha$ | $\xi$ | $n$ (2 MeV → 0.025 eV) |
|---|---|---|---|---|
| H | 1 | 0 | 1.000 | 18.2 |
| D | 2 | 0.111 | 0.725 | 25.1 |
| He | 4 | 0.360 | 0.425 | 42.8 |
| Be | 9 | 0.640 | 0.207 | 88.1 |
| C | 12 | 0.716 | 0.158 | 115 |
| ²³⁸U | 238 | 0.983 | 0.0084 | 2172 |

Hydrogen thermalises a fission neutron in 18 collisions; graphite needs 115;
uranium would need 2172. That ordering is why every thermal reactor moderates
with hydrogen, deuterium, beryllium or carbon and nothing heavier, and why a
**fast** reactor works by *omitting* the moderator and building the core out of
heavy nuclei that cannot slow neutrons down (`~NE-19`, `~NE-22`).

The counting above is not the whole moderator story: a good moderator must also
scatter often and absorb rarely, which needs the cross sections of `~NE-11` and
`~NE-13`. Ordinary water has the best $\xi$ but absorbs neutrons in its
hydrogen — the reason a light-water reactor cannot run on natural uranium while
a heavy-water one can (`~NE-22`, `~NE-23`).

Slowing down stops at **thermal equilibrium**: below ~1 eV the target nuclei's own
thermal motion means a neutron is as likely to gain energy as lose it, and the
population settles into a Maxwellian around 0.025 eV (2200 m/s at 293 K) — the
energy at which the capture and fission cross sections of `~NE-13` are quoted.

## Where this goes

- `~NE-09` — fission: §6.5.3 and §6.6 take the neutron-induced reaction whose
  compound nucleus splits, and the same $Q$-value bookkeeping gives the ~200 MeV
  budget.
- `~NE-10` — fusion: the barrier of §3 is what stars must beat, by *tunnelling*
  through it rather than climbing it (the Gamow peak).
- `~NE-13` — the cross sections that turn "this reaction is allowed" into "this
  reaction happens at this rate", plus lethargy, the natural variable that §5
  makes inevitable.
- `~NE-14` — charged-particle stopping: §4's 2.2 keV maximum electron transfer is
  the microscopic input to the Bethe stopping-power formula.
- `~NE-19` — the neutron life cycle: $\xi$, the collision count and the
  moderating ratio decide the resonance-escape probability and the thermal
  utilisation.
- `~NE-24` — fusion reactors: the Lawson criterion is the barrier of §3 recast as
  a plasma-confinement requirement.
