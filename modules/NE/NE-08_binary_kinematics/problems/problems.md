# NE-08 — Problems

Work each by hand, then check with `code/binary_kinematics.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P8
follow the book's Chapter 6 problems 5, 6, 8, 9, 10, 11, 12 and 15 (printed
174–176). Masses from `../data_tables/B1_atomic_masses.csv`.

### P1.  Derive the working threshold formula  *(S&F Ch. 6, Prob. 5)*
Obtain the approximate threshold $E_x^{th}\simeq-Q(1+m_x/m_X)$ of Eq. (6.15) from
the exact result of Eq. (6.14).
*Check:* the two agree to better than $2\times10^{-4}$ for every reaction in this
module (`test_exact_and_approximate_thresholds_agree`).

**Solution.** Eq. (6.14) is
$$E_x^{th}=-Q\,\frac{m_y+m_Y}{m_y+m_Y-m_x}.$$
The whole approximation is one substitution. Mass–energy conservation gives
$m_x+m_X=m_y+m_Y+Q/c^2$, and $|Q|$ is at most a few MeV against rest energies of
thousands of MeV, so to a part in $10^{3}$
$$m_y+m_Y\simeq m_x+m_X .$$
Substituting into both numerator and denominator,
$$E_x^{th}\simeq-Q\,\frac{m_x+m_X}{m_x+m_X-m_x}=-Q\,\frac{m_x+m_X}{m_X}
=\boxed{-Q\left(1+\frac{m_x}{m_X}\right)}.$$

The algebra is trivial; the *reading* is not. The factor $(1+m_x/m_X)$ is exactly
the inverse of $m_X/(m_x+m_X)$, the fraction of laboratory energy that survives
into the centre-of-mass frame. So Eq. (6.15) says nothing more than: **supply
$|Q|$ in the CM frame, and pay the laboratory surcharge for the CM motion you
cannot avoid creating.** Checking that reading directly,
$$E_{cm}\big(E_x^{th}\big)=E_x^{th}\frac{m_X}{m_x+m_X}
=-Q\left(1+\frac{m_x}{m_X}\right)\frac{m_X}{m_x+m_X}=-Q=|Q|,$$
which is `test_threshold_delivers_exactly_the_q_value_in_the_cm_frame`, and holds
to machine precision because it is an identity, not an approximation.

*(The book's problem statement says "start with Eq. (6.17)". Eq. (6.17) is the
Coulomb work integral and has nothing to do with the kinematic threshold; the
intended starting point is Eq. (6.14), as above. Noted in `../refs.md`.)*

### P2.  Verify Example 6.1  *(S&F Ch. 6, Prob. 6)*
Reproduce the authors' table for the three routes to the compound nucleus
$^{15}$N\*: $^{13}$C(d,t)$^{12}$C, $^{14}$C(p,n)$^{14}$N and
$^{14}$N(n,α)$^{11}$B.
*Check:* every entry below, reproduced by `test_reproduces_example_6_1`.

**Solution.**

| reaction | $Q$ (MeV) | $E_x^{C}$ (MeV) | $E_x^{th}$ (MeV) | condition | $\min(E_y+E_Y)$ |
|---|---|---|---|---|---|
| $^{13}$C(d,t)$^{12}$C | +1.311 | 1.994 | 0 | $E_x>E_x^{C}$ | 3.305 |
| $^{14}$C(p,n)$^{14}$N | −0.626 | 2.111 | 0.671 | $E_x>E_x^{C}$ | 1.485 |
| $^{14}$N(n,α)$^{11}$B | −0.158 | 0 | 0.170 | $E_x>E_x^{th}$ | 0.011 |

Each column is a different physical statement.

$Q$ from Eq. (6.6) with neutral-atom masses. $E_x^C$ from Eq. (6.19); for
$^{14}$C(p,n) that is $1.20(1)(6)/(1^{1/3}+14^{1/3})=7.2/3.410=2.111$ MeV. $E_x^{th}$
from Eq. (6.15); for the same reaction $0.6259(1+1.0073/14.003)=0.671$ MeV. The
governing condition is Eq. (6.20), $\max$ of the two.

Two lessons sit in this table. **Row 1** is exoergic and still has a threshold —
1.99 MeV of it — purely because the deuteron is charged. **Row 3** has no
Coulomb term at all, so its threshold is the kinematic 0.170 MeV, and a fast
neutron above ~0.2 MeV will do it; that is why $^{14}$N(n,α) contributes to tissue
dose from fast neutrons (`~NE-17`) while a charged projectile would need an
accelerator.

The last column is $Q+(E_x^{th})_{\min}$ and is never negative. It is easy to
misread the Coulomb energy as "lost". It is not: the target recoils, the compound
nucleus carries $E_x^C(m_x/M_{cn})$ and the rest excites it, and on decay the
whole of $E_x^C$ reappears in the products' masses and kinetic energies
(S&F p. 144). Row 1's products come out with 3.305 MeV, more than $Q$ itself.

### P3.  A 2-MeV neutron scattering off carbon  *(S&F Ch. 6, Prob. 8)*
A 2 MeV neutron scatters elastically from $^{12}$C through 45°. What is its
energy afterwards?
*Check:* $E'/E=0.9523$, so $E'=1.905$ MeV.

**Solution.** Eq. (6.25) with $Q=0$, $A=12$, $\cos45°=0.7071$:
$$\frac{E'}{E}=\frac{\left[0.7071+\sqrt{144-1+0.5}\right]^2}{13^2}
=\frac{\left[0.7071+11.9791\right]^2}{169}=\frac{160.94}{169}=0.9523,$$
so $E'=1.905$ MeV and the carbon nucleus recoils with 95 keV.

That is the whole difficulty of graphite moderation in one number: a
*perpendicular* hit — a fairly violent one — costs the neutron under 5% of its
energy. Even a head-on collision leaves it $\alpha=0.716$ of what it had. Compare
hydrogen, where the same 45° scattering gives $E'/E=\cos^2 45°=0.500$: half the
energy gone in one glancing blow.

### P4.  Inelastic scattering and the double-energy region  *(S&F Ch. 6, Prob. 9)*
The first excited state of $^{12}$C lies 4.439 MeV above the ground state. Find
(a) the $Q$-value for inelastic neutron scattering to that level, (b) the
threshold, and (c) the energy of an 8 MeV neutron scattered from it at 45°.
*Check:* (a) $-4.439$ MeV, (b) $4.812$ MeV, (c) $3.224$ MeV.

**Solution.** (a) Inelastic scattering leaves the nucleus excited, so the products
are heavier than the reactants by exactly the excitation energy:
$Q=-E^{*}=-4.439$ MeV. Nothing else changes — same nucleons, same charges.

(b) Eq. (6.15) with $m_x=m_n$, $m_X=12.000$ u:
$$E_n^{th}=4.439\left(1+\frac{1.00866}{12.000}\right)=4.812\ \text{MeV}.$$
A neutron carrying 4.5 MeV — well above the 4.439 MeV level — *cannot* excite it.
Below 4.812 MeV the $^{12}$C 4.439 MeV level is invisible to neutrons, and the
scattering is purely elastic.

(c) The full Eq. (6.25), now with $Q\neq0$:
$$E'=\frac{\left[\sqrt{8}\cos45°+\sqrt{8(143.5)+12(13)(-4.439)}\right]^2}{169}
=\frac{\left[2.000+\sqrt{455.6}\right]^2}{169}=3.224\ \text{MeV},$$
so 4.776 MeV vanished: 4.439 MeV into the excited nucleus (re-emitted promptly as
a 4.44 MeV gamma — a line seen in every fast-neutron spectrum from carbon-bearing
material) and 0.337 MeV into recoil.

**The double-energy region.** For $Q<0$ the $\pm$ in Eq. (6.25) matters. The
"−" root is real and positive only when $E\cos^2\theta_s$ exceeds the
discriminant, which at 45° confines it to
$$4.826\ \text{MeV}\;<\;E\;<\;4.842\ \text{MeV},$$
a 16 keV window in which **one scattering angle corresponds to two possible
outgoing energies**. Physically the CM-frame velocity of the scattered neutron is
smaller than the CM velocity itself, so both the forward and backward CM
directions project onto the same forward laboratory angle. `scattering_energy`
takes a `branch` argument for this, and
`test_inelastic_scattering_and_the_double_energy_region` pins the window. Far
above threshold, as at 8 MeV, only the "+" root survives.

### P5.  Why reactor coolant water becomes radioactive  *(S&F Ch. 6, Prob. 10)*
$^{16}$N ($T_{1/2}=7.13$ s) emits 6.1 and 7.1 MeV gammas and is made by
$^{16}$O(n,p)$^{16}$N. What is the minimum neutron energy?
*Check:* $Q=-9.638$ MeV, $E_n^{th}=10.25$ MeV.

**Solution.** From Appendix B,
$$Q=\left[m_n+M(^{16}\text{O})-M(^{1}\text{H})-M(^{16}\text{N})\right]c^2=-9.638\ \text{MeV},$$
and since the projectile is a neutron there is no Coulomb term, so Eq. (6.15)
alone governs:
$$E_n^{th}=9.638\left(1+\frac{1.00866}{15.9949}\right)=10.25\ \text{MeV}.$$

Ten MeV is a *very* fast neutron: the fission spectrum peaks near 0.7 MeV and
only about 0.1% of fission neutrons exceed 10 MeV. So $^{16}$N is made only by
the extreme tail of the spectrum, and only in the water actually inside the core
before it has been moderated — which is exactly what makes it useful as a signal
and dangerous as a hazard. Its 7 s half-life means the primary coolant loop of a
BWR is intensely gamma-active while running and quiet within a minute of
shutdown, which drives the shielding design of the turbine hall (`~NE-22`).

### P6.  Making $^{18}$F with neutrons  *(S&F Ch. 6, Prob. 11)*
$^{18}$F for PET can be made by irradiating Li₂CO₃ with neutrons: the neutrons
make tritons in $^{6}$Li, and the tritons react with the oxygen. (a) Write the two
reactions. (b) Find each $Q$. (c) Find each threshold. (d) Can thermal neutrons
(0.0253 eV) do it?
*Check:* $Q_1=+4.783$ MeV, $Q_2=+1.268$ MeV; $E^{C}(\text{t}+^{16}$O$)=2.423$ MeV;
the triton is born with 2.728 MeV.

**Solution.** (a) $^{6}$Li(n,t)$^{4}$He, then $^{16}$O(t,n)$^{18}$F.

(b) $Q_1=+4.783$ MeV and $Q_2=+1.268$ MeV — both exoergic, so neither has a
kinematic threshold.

(c) The first has a neutral projectile and $Q>0$: **no threshold whatsoever**, and
in fact its cross section rises as $1/v$, so thermal neutrons are the *best* ones
(`~NE-13`). The second has a charged projectile, so Eq. (6.20) leaves the Coulomb
term:
$$E_t^{C}=1.20\frac{(1)(8)}{3^{1/3}+16^{1/3}}=\frac{9.6}{3.9621}=2.423\ \text{MeV}.$$

(d) Yes — and the reason is the neatest part of the problem. A thermal neutron
brings negligible energy, so the 4.783 MeV of $Q_1$ is shared by inverse mass:
$$E_t=Q_1\frac{m_\alpha}{m_t+m_\alpha}=4.783\times\frac{4.0026}{7.0187}=2.728\ \text{MeV},$$
with 2.055 MeV to the alpha. The triton is born with **2.728 MeV, just above the
2.423 MeV barrier it needs** — a margin of 300 keV. The thermal neutron does not
supply the energy for the second reaction; it unlocks nuclear binding energy that
supplies it. Two-step production schemes like this are how a reactor, which makes
only neutrons, can drive charged-particle reactions it could never drive directly.

### P7.  The PET production reaction  *(S&F Ch. 6, Prob. 12)*
For $^{18}$O(p,n)$^{18}$F — the cyclotron route actually used for PET — find
(a) $Q$, (b) the kinematic threshold, (c) the reaction threshold, (d) the minimum
product energy.
*Check:* $-2.438$, $2.574$, $2.651$, $0.213$ MeV.

**Solution.** (a) $Q=-2.438$ MeV from Appendix B.

(b) Eq. (6.15): $E_p^{th}=2.438(1+1.0073/17.9992)=2.574$ MeV.

(c) The proton is charged, so Eq. (6.19) also applies:
$$E_p^{C}=1.20\frac{(1)(8)}{1+18^{1/3}}=\frac{9.6}{3.6207}=2.651\ \text{MeV},$$
and Eq. (6.20) gives $(E_p^{th})_{\min}=\max(2.651,\,2.574)=\boxed{2.651\ \text{MeV}}$.
This is a close-run thing: the two hurdles differ by 77 keV, and had the target
been lighter the kinematic term would have won instead. Both must always be
computed.

(d) $\min(E_y+E_Y)=Q+(E_p^{th})_{\min}=-2.438+2.651=0.213$ MeV.

Real $^{18}$F production runs at 11–18 MeV, far above 2.65 MeV, because a
threshold tells you where the cross section becomes non-zero and nothing about
where it becomes *large* — near threshold it is negligible. Yield needs cross
sections (`~NE-11`), and the practical energy is set by where $\sigma$ peaks
against target heating and unwanted side channels (`~NE-27`).

### P8.  Slowing neutrons in oxygen and iron  *(S&F Ch. 6, Prob. 15)*
How many elastic scatters, on average, slow a 2 MeV neutron below 1 eV in
(a) $^{16}$O and (b) $^{56}$Fe?
*Check:* $\xi=0.1199$ and $0.0353$; $n=121$ and $411$.

**Solution.** With $\alpha=((A-1)/(A+1))^2$ and $\xi=1+\alpha\ln\alpha/(1-\alpha)$:

| | $A$ | $\alpha$ | $\xi$ | $n=\xi^{-1}\ln(2\times10^{6}/1)$ |
|---|---|---|---|---|
| $^{16}$O | 16 | 0.7785 | 0.1199 | **121** |
| $^{56}$Fe | 56 | 0.9311 | 0.0353 | **411** |

using $\ln(2\times10^{6})=14.509$.

Neither is a moderator, and that is the point. Oxygen is *carried along* in water
and in UO₂ fuel, and iron is structure and cladding: both scatter neutrons
constantly without slowing them usefully. In water essentially all the moderation
is done by the two hydrogens (18 collisions each) rather than the oxygen (121) —
which is why $\text{H}_2\text{O}$ appears in Table 6.1 with an effective
$\xi=0.920$, close to hydrogen's 1.000 and nowhere near oxygen's 0.120.

The comparison also shows why $\xi$, not $\alpha$, is the right figure of merit.
Iron's $\alpha=0.931$ looks only modestly worse than oxygen's $0.779$, but the
collision counts differ by a factor of 3.4: $\xi$ turns the per-collision ratio
into an additive currency, and only additive currencies can be counted.

A full moderator ranking needs one more ingredient still — the *moderating ratio*
$\xi\Sigma_s/\Sigma_a$, which penalises materials that absorb what they slow.
That is why ordinary water, with the best $\xi$ of any practical moderator, still
cannot sustain a chain reaction in natural uranium while graphite and heavy water
can (`~NE-19`, `~NE-22`).
