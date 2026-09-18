# NE-19 — Problems

Work each by hand, then check with `code/neutron_cycle.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. These are
the book's Chapter 10 problems 5, 7, 9–10, 12, 13, 17, 19 and 21–22 (printed
366–368). Problems 24 onward are kinetics and belong to `~NE-20`.

Thermal cross sections are the **thermal-averaged** ones of Table 10.1 unless
stated; see `../notes.md` §1 for why that matters.

### P1.  The Westcott factor  *(S&F Ch. 10, Prob. 5)*
From Tables 10.1 and 10.2, find $g_a(T_0)$ for ²³⁵U at room temperature.
*Check:* 0.978.

**Solution.** Table 10.1 is thermal-*averaged*, Table 10.2 is at 0.0253 eV, and
Eq. (10.5) connects them at $T=T_0$:
$$\bar\sigma_a=\frac{\sqrt\pi}{2}g_a(T_0)\,\sigma_a(E_0)
\;\Rightarrow\;
g_a=\frac{592.6}{0.8862\times683.68}=\boxed{0.978}.$$

**What the number means.** $g_a=1$ would say ²³⁵U is a perfect $1/v$ absorber.
It is not quite — it has resonances just above thermal — and the 2.2% shortfall
is exactly the correction the Westcott factor exists to carry. Repeat the
exercise for ²³⁸U and you get $g_a=2.382/(0.8862\times2.6835)=1.002$: a clean
$1/v$ absorber to two parts in a thousand, which is the check that the method —
and the two tables — are sound.

The practical warning: the two tables differ by 13% for ²³⁵U, so taking $\nu$ from
one and $\sigma_f$ from the other — which S&F's own Example 10.3 does — is a
systematic few-percent error.

### P2.  Natural uranium  *(S&F Ch. 10, Probs. 7–8)*
Find $\eta$ and the thermal-averaged macroscopic absorption cross section per
uranium atom for natural uranium.
*Check:* η = 1.339; Σ_a/N = 6.639 b.

**Solution.** With abundances 0.0055% ²³⁴U, 0.7204% ²³⁵U, 99.2745% ²³⁸U,
$$\frac{\Sigma_a^U}{N^U}=0.000055(89.49)+0.007204(592.6)+0.992745(2.382)
=\boxed{6.639\ \text{b}},$$
and only ²³⁵U fissions, so
$$\eta=\frac{\nu_{235}\,\sigma_f^{235}f_{235}}{\Sigma_a^U/N^U}
=\frac{2.437\times505.9\times0.007204}{6.639}=\boxed{1.339}.$$

**Two things to notice.** ²³⁵U is 0.72% of the atoms and supplies **64%** of the
absorption — the whole of the numerator and two thirds of the denominator.
And η = 1.34 is the number the rest of the chapter fights: comfortably above 1,
so a chain reaction is possible, but so far below 2 that after leakage, resonance
capture and parasitic absorption there is very little margin left. Table 10.5 is
the accounting of what remains.

### P3.  Enrichment  *(S&F Ch. 10, Probs. 9–10)*
Find η for 5 atom-% enriched uranium, and the enrichment giving η = 1.85 (ignore
²³⁴U).
*Check:* 1.933; 3.13 atom-%.

**Solution.** With $e$ the ²³⁵U atom fraction,
$$\eta(e)=\frac{\nu\sigma_f^{235}e}{\sigma_a^{235}e+\sigma_a^{238}(1-e)}
=\frac{1232.9\,e}{592.6e+2.382(1-e)}.$$
At $e=0.05$ this is $\boxed{1.933}$. Setting $\eta=1.85$ and solving,
$e=\boxed{3.13\%}$.

**The shape is the point.** η rises steeply at low enrichment and then flattens:
0.72% → 1.34, 3% → 1.84, 5% → 1.93, and the ceiling at pure ²³⁵U is only 2.08.
Nearly all the benefit of enrichment is bought in the first few percent — which is
why power reactors sit at 3–5% and why going higher buys little reactivity for a
great deal of separative work (`~NE-23`).

### P4.  A fissile solution  *(S&F Ch. 10, Prob. 12)*
A salt of fully enriched ²³⁵U in water, $1.5\times10^{-3}$ atoms of ²³⁵U per water
molecule. (a) Why is p ≈ 1? (b) k_∞? (c) Critical radius of a bare sphere?
*Check:* k_∞ = 1.251; R = 36.5 cm.

**Solution.**
(a) The resonance escape probability describes capture in ²³⁸U's resonances.
**There is no ²³⁸U**, so there is essentially nothing to escape from and p ≈ 1.

(b) With $\bar\sigma_a(\mathrm{H_2O})=(\sqrt\pi/2)(0.6644)=0.5888$ b and
$N^{NF}/N^F=667$,
$$f=\frac{592.6}{592.6+0.5888\times667}=0.6015,\qquad
k_\infty=\eta f=2.080\times0.6015=\boxed{1.251}.$$

(c) $L^2=L^2_{\rm H_2O}(1-f)=8.12(0.3985)=3.24$ cm², $\tau=27$ cm². Solving
$$\frac{k_\infty e^{-B^2\tau}}{1+L^2B^2}=1
\;\Rightarrow\;B_c^2=7.43\times10^{-3},\ \boxed{R=36.5\ \text{cm}}.$$

**This problem is criticality safety in miniature.** A 36 cm sphere is a bucket.
Fissile material in *solution* is far more dangerous than the same mass dry,
because the water is a near-ideal moderator at exactly the right ratio — and most
historical criticality accidents were solutions. Note also that the fast leakage
does the work here: $\tau=27$ cm² against graphite's 368, so the water core is
small precisely because water thermalises in a few centimetres.

### P5.  Graphite and 1% uranium  *(S&F Ch. 10, Prob. 17)*
Homogeneous graphite + 1%-enriched uranium at $N_M/N_U=500$, ignoring ²³⁴U and
taking ε = 1. Find k_∞.
*Check:* 0.900.

**Solution.** Per uranium atom, $\Sigma_a^U/N^U=592.6(0.01)+2.382(0.99)=8.284$ b, so
$$\eta=\frac{2.437\times505.9\times0.01}{8.284}=1.488,\qquad
f=\frac{8.284}{8.284+0.003421(500)}=0.829.$$
For p, $N_{238}/N_C=0.99/500=1.98\times10^{-3}$ and Eq. (10.9) with graphite's
ξ = 0.158, σ_sM = 4.8 b gives $p=0.730$. Hence
$$k_\infty=\eta pf=1.488\times0.730\times0.829=\boxed{0.900}.$$

**Subcritical — and the reason is p, not the enrichment.** 27% of the neutrons
are lost to ²³⁸U resonances even at 1% enrichment and 500:1 moderation. Compare
P4, where p = 1 because there is no ²³⁸U at all. This is the calculation that
tells you a graphite reactor on lightly enriched uranium must either be
heterogeneous (P6, and Table 10.8) or use more moderator.

### P6.  A critical cube  *(S&F Ch. 10, Prob. 19)*
Graphite + 3%-enriched uranium at the optimum $N_M/N_U=828$ has
$k_\infty=(1.0)(0.78642)(1.84117)(0.87640)=1.26897$. What cube is critical?
*Check:* 300 cm on a side.

**Solution.** $L^2=L_C^2(1-f)=3070(1-0.8764)=379$ cm², $\tau=368$ cm². Solve
$$\frac{1.26897\,e^{-368B^2}}{1+379B^2}=1\;\Rightarrow\;B_c^2=3.283\times10^{-4}\ \text{cm}^{-2},$$
and for a cube $B_g^2=3(\pi/a)^2$, so
$$a=\pi\sqrt{3/B_c^2}=\boxed{300\ \text{cm}}.$$

**Three metres on a side for 3% fuel.** Compare P4's 36 cm bucket of solution.
The difference is almost entirely the Fermi age: graphite's 368 cm² against
water's 27 means a fission neutron wanders ~50 cm before thermalising, and a core
must be several times that in every direction or it simply leaks. Moderator choice
sets reactor *size* far more strongly than it sets reactivity.

### P7.  A uranium–water sphere  *(S&F Ch. 10, Probs. 21–22)*
Fully enriched ²³⁵U in water at $N_{\rm H_2O}/N_{235}=800$, in a 40 cm sphere.
(a) k_∞? (b) k_eff? (c) The critical radius and mass?
*Check:* 1.159; 0.960; R = 45.2 cm, 6.3 kg of ²³⁵U.

**Solution.**
(a) $f=592.6/[592.6+0.5888(800)]=0.5571$, so $k_\infty=2.080(0.5571)=\boxed{1.159}$.

(b) $L^2=8.12(0.4429)=3.60$ cm², $B^2=(\pi/40)^2=6.17\times10^{-3}$ cm⁻²:
$$P^f_{NL}=e^{-0.1666}=0.847,\quad P^{th}_{NL}=\frac{1}{1.0222}=0.978,\quad
k_{\rm eff}=\boxed{0.960}.$$

(c) Solving for criticality gives $\boxed{R=45.2\ \text{cm}}$, a volume of
$3.87\times10^5$ cm³ containing $N_{235}=4.18\times10^{-5}$ atoms/b·cm, i.e.
$\boxed{6.3\ \text{kg}}$ of ²³⁵U.

**Note which leakage term dominates.** At R = 40 cm the thermal non-leakage is
0.978 — almost nothing escapes once thermalised, because $L=1.9$ cm in this
mixture — while the fast non-leakage is 0.847. **15% of the neutrons leak out
while still fast.** That asymmetry is general in water-moderated systems and is
why a reflector helps a small water core so much: it returns fast neutrons that
would otherwise be gone before they could be used.

### P8.  Nine perturbations  *(S&F Ch. 10, Prob. 13)*
A bare, homogeneous, source-free, critical uranium reactor runs at power $P_0$.
What happens to the power, and why, for each separate change?

**Solution.** The discipline is to name *which factor* moves.

| change | factor | effect |
|---|---|---|
| (a) deformed into an ellipsoid | $B_g^2$ ↑ | The sphere minimises buckling for a given volume, so any deformation increases leakage. **Power falls**, and the reactor goes subcritical. |
| (b) a person stands next to it | $P_{NL}$ ↑ | A human is mostly water: a partial reflector. Some leaked neutrons come back. **Power rises** — slightly, and this is a real and documented criticality hazard. |
| (c) core temperature raised | $f$, $p$, density | Density falls (less moderator per cm³) and Doppler broadening widens the ²³⁸U resonances, lowering $p$. **Power falls** — see `~NE-20` §2, where this negative feedback is the thing that makes a reactor controllable. |
| (d) a neutron source brought near | none | Adds neutrons without changing any factor. At exactly critical the population rises to a new steady level set by the source; **power rises to a new steady value**, it does not run away. |
| (e) an energetic electron beam | none | Electrons do not induce fission and their photonuclear yield is negligible here. **Unchanged.** |
| (f) run at high power a long time | $f$, $\eta$ | Fuel burns out and fission products (notably ¹³⁵Xe) build in, both lowering $f$; ²³⁹Pu builds in, raising it. Net **power falls** without control action — this is the burnup reactivity loss of `~NE-23`. |
| (g) launched into space | none | Nothing in the six factors refers to gravity or to the surroundings of a *bare* core. **Unchanged.** |
| (h) wrapped in cadmium | $P^{th}_{NL}$ ↓ | Cadmium is a huge thermal absorber, so it is an anti-reflector: thermal neutrons that leak are absorbed instead of returning. **Power falls.** |
| (i) enrichment increased | $\eta$ ↑, $f$ ↑ | Both rise (more ²³⁵U per absorption and per atom). **Power rises.** |

**The lesson of (d) and (g).** A critical reactor is not a bomb waiting for a
trigger: adding a source or moving it does not change $k$, and a system at
$k=1$ with a source settles at a *finite* power. What changes power is what
changes a factor — and (a), (c), (f) and (h) all change one in the safe
direction, which is not an accident of the question but a design principle.
