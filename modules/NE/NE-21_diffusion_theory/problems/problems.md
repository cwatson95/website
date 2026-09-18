# NE-21 — Problems

Work each by hand, then check with `code/diffusion.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. §10.10 is an addendum and
carries no problems of its own; these are added, and P1–P3 close the loop on
`~NE-19`'s Chapter 10 problems by deriving what that module assumed.

Throughout, the reference core is `~NE-19` Example 10.3's: ²³⁵U in graphite at
1:35 000, with $k_\infty=1.6939$, $L^2=570.1$ cm², $\tau=368$ cm².

### P1.  The same material in five shapes  *(added)*
Find the critical dimension and volume of the reference core as a sphere, a cube,
a cylinder, an infinite cylinder and a slab.
*Check:* $B^2_{\rm mat}=1.217\times10^{-3}$ cm⁻²; sphere R = 90.0 cm; cube
a = 156.0 cm; cylinder R = 84.4, H = 156.0 cm.

**Solution.** The material buckling is the same for all of them:
$$B^2_{\rm mat}=\frac{k_\infty-1}{L^2}=\frac{0.6939}{570.1}
=\boxed{1.217\times10^{-3}\ \text{cm}^{-2}},$$
and each geometry's $B_g^2$ is then set equal to it [Eq. (10.80)]:

| geometry | $B_g^2$ | critical size | volume |
|---|---|---|---|
| sphere | $(\pi/R)^2$ | R = 90.0 cm | 3.06 m³ |
| cylinder (optimal) | $(2.405/R)^2+(\pi/H)^2$ | R = 84.4, H = 156.0 cm | 3.49 m³ |
| cube | $3(\pi/a)^2$ | a = 156.0 cm | 3.79 m³ |
| infinite cylinder | $(2.405/R)^2$ | R = 68.9 cm | — |
| slab | $(\pi/a)^2$ | a = 90.0 cm | — |

**The sphere wins, and it must.** Leakage is a surface effect, so the shape with
the least surface per unit volume needs the least material; the cube costs 24%
more. The optimum cylinder sits at $H/R=\pi\sqrt2/2.405=1.847$, which is worth
knowing because it is very nearly the aspect ratio of real power cores — those
are set by other constraints, but the neutronics does not fight them.

Note the last two rows have no volume: an infinite cylinder and an infinite slab
are critical at finite *thickness* and infinite *volume*, which is the sense in
which the buckling, not the size, is the physical quantity.

### P2.  A solution is not a pile  *(added)*
Take `~NE-19` P7's fully enriched ²³⁵U in water ($k_\infty=1.159$, $L^2=3.60$ cm²).
What is the one-speed critical sphere?
*Check:* R = 14.9 cm.

**Solution.** $B^2_{\rm mat}=0.159/3.60=0.0442$ cm⁻², so
$R=\pi/\sqrt{B^2}=\boxed{14.9\ \text{cm}}$.

**Compare P1: 90 cm of graphite pile against 15 cm of solution**, for materials
whose $k_\infty$ differ by less than a factor of 1.5. The difference is entirely
$L^2$ — 570 cm² against 3.6, because water absorbs 70 times more strongly per
centimetre and a thermal neutron therefore travels a tenth as far before being
absorbed.

That is criticality safety in one line: **a moderated solution is critical in a
volume you can carry.** (The one-speed answer is optimistic here for the reason
P6 gives; with the Fermi age the two-group radius is larger. But not by enough to
change the conclusion, because water's $\tau=27$ cm² is small too.)

### P3.  Recovering `~NE-19`'s non-leakage probability  *(added)*
Show that $P^{th}_{NL}=1/(1+L^2B^2)$, asserted in `~NE-19` Eq. (10.13), is the
one-speed diffusion result, and check it against Example 10.4.
*Check:* 0.7192 at R = 120 cm.

**Solution.** In the one-speed model the balance is
$$\underbrace{DB^2\phi}_{\text{leakage}}+\underbrace{\Sigma_a\phi}_{\text{absorption}}
=\underbrace{\nu\Sigma_f\phi}_{\text{production}},$$
so the fraction *not* leaking is
$$P_{NL}=\frac{\Sigma_a}{\Sigma_a+DB^2}=\frac{1}{1+L^2B^2}.$$
At R = 120 cm, $B^2=(\pi/120)^2=6.854\times10^{-4}$, so
$L^2B^2=0.3907$ and $P_{NL}=\boxed{0.7192}$ — Example 10.4's number exactly.

**The leakage term is $DB^2$**, and that is the sentence worth keeping. Buckling
is not a metaphor: $B^2$ has units of cm⁻², it multiplies $D$ to give a
macroscopic removal cross section, and it enters the balance on exactly the same
footing as $\Sigma_a$. Leakage is an absorber whose strength is set by geometry.

### P4.  Two exponentials that are not the same  *(added)*
A point source of 10⁸ n/s sits in an infinite graphite medium ($D=0.84$ cm,
$L=55.4$ cm, $\Sigma_t\approx0.4$ cm⁻¹). Compare the diffusion flux at 50 cm
with the uncollided flux of `~NE-11`.
*Check:* 7.7×10⁴ against 6.6×10⁻⁶ cm⁻²s⁻¹ — a factor of 10¹⁰.

**Solution.**
$$\phi_{\rm diff}=\frac{Se^{-r/L}}{4\pi Dr}
=\frac{10^8e^{-0.903}}{4\pi(0.84)(50)}=\boxed{7.7\times10^4},$$
$$\phi_{\rm unc}=\frac{Se^{-\Sigma_t r}}{4\pi r^2}
=\frac{10^8e^{-20}}{4\pi(2500)}=\boxed{6.6\times10^{-6}}.$$

**Ten orders of magnitude, and both are right** — they answer different
questions. The uncollided flux counts neutrons that have never scattered, and at
20 mean free paths there are essentially none. The diffusion flux counts the
whole population, almost all of which has scattered dozens of times and random-
walked its way out.

Which you want depends on the question: for a *beam* experiment or a
thin-collimator dose calculation, the uncollided flux; for activation, heating or
criticality, the total. Using the uncollided form for a shielding calculation in
a scattering medium — the classic blunder — underestimates the answer here by a
factor of 10¹⁰.

### P5.  What a bare core wastes  *(added)*
A bare cylindrical reactor is limited by the peak fuel temperature. What fraction
of its potential output is it giving up, and what do designers do about it?
*Check:* peak/average = 3.64; it runs at 27% of a flat core's power.

**Solution.** The flux profile is $J_0(2.405r/R)\cos(\pi z/H)$, and integrating,
$$\frac{\phi_{\max}}{\bar\phi}=\frac{2.405}{2J_1(2.405)}\times\frac{\pi}{2}
=2.316\times1.571=\boxed{3.639}.$$

If the hottest pin sets the limit, the core delivers $1/3.639=\boxed{27\%}$ of
what a perfectly flat core of the same size and peak limit would.

| geometry | peak/average | fraction of flat |
|---|---|---|
| slab | 1.571 | 64% |
| infinite cylinder | 2.316 | 43% |
| sphere | 3.290 | 30% |
| **cylinder** | **3.639** | **27%** |
| cube | 3.876 | 26% |

**Note the sphere is the worst of the compact shapes**, which cuts against P1: the
shape that minimises *critical mass* is nearly the worst for *power density*.
Research reactors care about the first and power reactors about the second, and
they look different for exactly that reason.

The fixes are all about flattening: a **reflector** raises the edge flux
(`~NE-19` §10.6), **fuel zoning** puts fresh fuel at the periphery and depleted
fuel at the centre, and **burnable poisons** and part-length control rods trim
what is left. A modern PWR runs a peaking factor near 2.5 rather than 3.6, and
every point of that is directly saleable power.

### P6.  Two approximations, quantified  *(added)*
(a) S&F set the extrapolation distance to zero. How wrong is that for a 20 cm
graphite slab? (b) The one-speed model gives 90 cm for P1's critical sphere while
`~NE-19` gives 126.7 cm. Why, and which is right?
*Check:* (a) 28% in $B^2$; (b) the one-speed answer is 30% small.

**Solution.**
(a) The flux vanishes not at the surface but at $d=0.7104\lambda_{tr}$ beyond it.
In graphite $\lambda_{tr}=2.5$ cm, so $d=1.78$ cm and a 20 cm slab behaves as
23.55 cm. Since $B^2=(\pi/a)^2$,
$$\text{error}=1-\left(\frac{20}{23.55}\right)^2=\boxed{28\%}.$$
For a 400 cm core it is 1.8%, and in water (where $\lambda_{tr}=0.43$ cm) it is
negligible almost everywhere. **S&F's approximation is safe in the regime they
have in mind and not in general** — and §10.10 is exactly the machinery one would
reach for to analyse a small critical assembly.

(b) The one-speed model never lets a neutron slow down, so it has **no fast
leakage term at all**. `~NE-19` includes $e^{-B^2\tau}$ with the Fermi age
$\tau=368$ cm² — a fission neutron in graphite wanders ~50 cm before it is
thermal, and a good fraction of them leave during that journey.

Solving $k_\infty e^{-B^2\tau}/(1+L^2B^2)=1$ instead gives R = 126.7 cm.
**The two-group answer is right**, and the one-speed result is 30% small — an
error in the *unsafe* direction, since it says a smaller assembly is critical
than really is. The lesson is not that diffusion theory is wrong but that
one energy group is not enough; real analysis uses multigroup diffusion, and
where even that fails, transport (§10.10.3).
