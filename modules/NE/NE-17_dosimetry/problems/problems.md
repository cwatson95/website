# NE-17 — Problems

Work each by hand, then check with `code/dosimetry.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6 are the book's
Chapter 9 problems 1–6 (printed 318–319); P7–P8 are added. Chapter 9's remaining
problems are health effects and radon and belong to `~NE-18`.

Photon coefficients are interpolated **linearly** from Appendix C.3 throughout,
because that is the method S&F's own solutions name (`../refs.md`, last section).

### P1.  Tritium in air  *(S&F Ch. 9, Prob. 1)*
Infinite air, density 0.0012 g/cm³, containing tritium at 2.3 pCi/L. Tritium has
$T_{1/2}=12.33$ y and an average beta energy of 5.37 **keV** per decay. What is
the air-kerma rate?
*Check:* 0.219 nGy/h as stated; 0.232 nGy/h using Appendix D's 5.67 keV.

**Solution.** In an infinite homogeneous medium with a uniformly distributed
source, energy is absorbed at exactly the rate it is emitted — there is nowhere
else for it to go — so the kerma rate is just emitted power per unit mass, with
no transport calculation at all. Decays per hour per litre:
$$(2.3\times10^{-12}\ \text{Ci/L})(3.7\times10^{10}\ \text{s}^{-1}\text{Ci}^{-1})(3600\ \text{s/h})
=306.4\ \text{h}^{-1}\text{L}^{-1},$$
and each carries $5.37\times10^{-3}$ MeV $\times\,1.602\times10^{-13}$ J/MeV:
$$\dot K=\frac{306.4\times8.60\times10^{-16}\ \text{J h}^{-1}\text{L}^{-1}}{0.0012\ \text{kg/L}}
=\boxed{2.20\times10^{-10}\ \text{Gy/h}}=0.219\ \text{nGy/h}.$$

**The printed problem says 5.37 MeV, and that is impossible.** Tritium's entire
decay energy is 18.6 keV, so the beta cannot carry 5.37 MeV; the book's own
Appendix D gives 5.67 keV/decay, which yields 0.232 nGy/h. The authors' solution
manual restates the problem in keV, substitutes MeV anyway, and then reports its
own $2.196\times10^{-7}$ Gy/h as "22.0 µGy/h" — it is 0.2196 µGy/h. Three errors
in one short problem, all of which a units check catches.

Sanity: continuous exposure at 0.23 nGy/h is 2 µGy per year, roughly a thousandth
of the terrestrial gamma background. That is the right order for a trace tritium
concentration, and it is the check that tells you 22 µGy/h could not be right.

### P2.  A ¹³⁷Cs source in air  *(S&F Ch. 9, Prob. 2)*
700 µCi of ¹³⁷Cs; the 0.662 MeV gamma is emitted 0.849 times per decay. At 2 m,
find the exposure rate, the air kerma rate, and the dose-equivalent rate.
*Check:* 56.1 µR/h; 0.490 µGy/h; 0.544 µSv/h.

**Solution.** The photon emission rate is
$$S=(700\times10^{-6}\ \text{Ci})(3.7\times10^{10})(0.849)=2.199\times10^7\ \text{s}^{-1},$$
and air attenuation over 2 m is negligible, so
$$\phi=\frac{S}{4\pi r^2}=\frac{2.199\times10^7}{4\pi(200)^2}=43.75\ \text{cm}^{-2}\text{s}^{-1}.$$

Interpolating Appendix C.3 at 0.662 MeV gives $(\mu_{en}/\rho)_{\rm air}=0.02931$,
$(\mu_{tr}/\rho)_{\rm air}=0.02937$ and $(\mu_{en}/\rho)_{\rm water}=0.03260$ cm²/g.

$$\dot X=1.835\times10^{-8}(0.662)(0.02931)(43.75)=1.558\times10^{-8}\ \text{R/s}
=\boxed{56.1\ \mu\text{R/h}}$$
$$\dot K_{\rm air}=1.602\times10^{-10}(0.662)(0.02937)(43.75)=\boxed{0.490\ \mu\text{Gy/h}}$$
$$\dot H=QF\,\dot D_{\rm tissue}\simeq(1)(1.602\times10^{-10})(0.662)(0.03260)(43.75)
=\boxed{0.544\ \mu\text{Sv/h}}$$

using water for tissue and $QF=1$ for photons.

**Three consistency checks worth making.** Converting the exposure with
1 R = 8.73 mGy gives 0.490 µGy/h in air, matching (b) to 0.2% — the residual is
the $\mu_{en}$/$\mu_{tr}$ difference, which is exactly what it should be at
0.662 MeV. Tissue reads 11% higher than air, the ratio of the two $\mu_{en}$;
that 11% is nearly energy-independent, which is why exposure survives as a proxy
at all. And 0.544 µSv/h continuous is 4.8 mSv/y — twice natural background — so
this is not a source to keep on a desk.

### P3.  The same source under water  *(S&F Ch. 9, Prob. 3)*
Now in a large water tank; uncollided photons only, at 0.5 m.
*Check:* 12.1 µR/h; 0.106 µGy/h; 0.118 µSv/h.

**Solution.** Water's total coefficient at 0.662 MeV is $\mu=0.08604$ cm⁻¹, so
$$\phi=\frac{S\,e^{-\mu r}}{4\pi r^2}=\frac{2.199\times10^7 e^{-4.302}}{4\pi(50)^2}
=9.48\ \text{cm}^{-2}\text{s}^{-1},$$
and the three answers scale with $\phi$: $\boxed{12.1\ \mu\text{R/h}}$,
$\boxed{0.106\ \mu\text{Gy/h}}$, $\boxed{0.118\ \mu\text{Sv/h}}$.

**Read the competition between the two factors.** Moving from 200 cm to 50 cm
multiplies the geometric term by 16; the attenuation term $e^{-4.302}=0.0135$
divides by 74. Net, four times closer is **4.6 times less dose**. Half a metre of
water is 4.3 mean free paths, and that beats an inverse-square gain of sixteen
comfortably — which is the whole argument for water as a spent-fuel shield.

Note "uncollided only" is doing real work: at 4.3 mfp the *scattered* photons
dominate the true field, typically by a buildup factor of 5–10 (`~NE-11`). This
answer is a lower bound on the dose, not an estimate of it.

### P4.  A ¹⁶N and a ⁴³K source in air  *(S&F Ch. 9, Prob. 4)*
1 mCi point sources, dose rate in air at 10 cm, using Appendix D's gamma lines.
*Check:* ¹⁶N 1.27 mGy/h; ⁴³K 0.479 mGy/h.

**Solution.** Sum Eq. (9.6) over the discrete lines:
$$\dot D=\frac{1.602\times10^{-10}S}{4\pi r^2}\times3600\sum_i f_iE_i\left(\frac{\mu_{en}}{\rho}\right)_i.$$

For ¹⁶N (two lines, 6.129 MeV at 69% and 7.115 MeV at 5%) the sum is
$0.06931+0.00562=0.07493$, giving $\boxed{1.27\ \text{mGy/h}}$. For ⁴³K (six
lines) the sum is 0.02823, giving $\boxed{0.479\ \text{mGy/h}}$.

**The solution manual prints 1.611 mGy/h for ¹⁶N, and its own next problem proves
that wrong.** Its table lists $0.690\times6.129\times0.01639=0.08931$; the product
is 0.06931. Problem 5 uses the *same* line and prints
$0.006269=0.06931\times e^{-2.403}$. A 6 was transcribed as an 8.

The physics worth keeping: ¹⁶N delivers 2.7 times the dose of ⁴³K per becquerel,
almost entirely because its photons are ten times more energetic. It is also why
¹⁶N — made continuously by ¹⁶O(n,p)¹⁶N in reactor coolant — dominates the
radiation field around a running BWR's steam lines (`~NE-22`), and why its 7.13 s
half-life makes that field vanish minutes after shutdown.

### P5.  The same sources inside iron  *(S&F Ch. 9, Prob. 5)*
*Check:* ¹⁶N 0.115 mGy/h; ⁴³K 0.954 µGy/h (book 1.654 µGy/h — see below).

**Solution.** Insert $e^{-\mu^{\rm Fe}_ir}$ per line. For ¹⁶N the weighted sum
falls from 0.07493 to 0.006790, so $\dot D=\boxed{0.115\ \text{mGy/h}}$ — the book's
number exactly.

**Attenuation sorts the two sources violently.** 10 cm of iron cuts ¹⁶N's
6–7 MeV photons by a factor of 11, and ⁴³K's few-hundred-keV photons by a factor
of 503. A shield does not merely reduce a field; it changes which nuclide you are
looking at — outside the iron, ¹⁶N outshines ⁴³K by 121:1 where in the open air
the ratio was 2.7:1.

For ⁴³K the book gets 1.654 µGy/h and this module gets 0.954 µGy/h. The whole
difference is one coefficient: for the 617.5 keV line the solution manual uses the
table's 0.8 MeV row ($\mu_{en}/\rho=0.02880$, $\mu^{\rm Fe}=0.5174$ cm⁻¹) instead
of interpolating to 0.6175 MeV (0.02947 and 0.5905). In air that costs 1.2%; here
it sits inside an exponential over 10 cm and the answer comes out 1.73× too high.
Every other coefficient in both tables is reproduced exactly, which is what
identifies this one.

### P6.  A rule of thumb  *(S&F Ch. 9, Prob. 6)*
$\dot X=6CEN/r^2$ with $C$ in Ci, $E$ in MeV, $r$ in **feet**, $\dot X$ in R/h.
(a) Restate it in Bq and metres. (b) Over what energies is it good to 20%?
*Check:* $1.507\times10^{-11}$; roughly 0.12–1.9 MeV.

**Solution.** (a) Substituting $C(\text{Ci})=C(\text{Bq})/3.7\times10^{10}$ and
$r(\text{ft})=r(\text{m})/0.3048$,
$$\dot X\ (\text{R/h})=\frac{6\times(0.3048)^2}{3.7\times10^{10}}\frac{C(\text{Bq})EN}{[r(\text{m})]^2}
=\boxed{\frac{1.507\times10^{-11}\,C(\text{Bq})EN}{[r(\text{m})]^2}}.$$

(b) Comparing with the exact Eq. (9.9) shows what the rule *is*: the exact
expression carries a factor $(\mu_{en}/\rho)_{\rm air}$ where the rule carries a
constant, so the rule is exactly right where
$$\left(\frac{\mu_{en}}{\rho}\right)_{\rm air}=0.02866\ \text{cm}^2/\text{g},$$
and its error is just the fractional departure of air's coefficient from that.
Air's $\mu_{en}/\rho$ is remarkably flat — 0.0233 to 0.0297 over two decades —
so the rule holds within 20% from about **0.12 MeV to 1.9 MeV**.

It fails in both directions, for different reasons: below 0.1 MeV the
photoelectric effect lifts $\mu_{en}$, above 2 MeV Compton scattering drops it.
Note the direction at high energy — at 5 MeV the rule is **65% high**, i.e.
conservative for a dose estimate and wasteful for a shield.

A curiosity the closed form hides: air's coefficient has a shallow local minimum
near 0.1 MeV, so the 20% band is not quite one interval — the rule dips to 23%
error right at 0.1 MeV and recovers on both sides. `rule_of_thumb_valid_range`
returns the band containing 1 MeV and its docstring says so.

### P7.  Reading a survey meter  *(added)*
An ion chamber reads 12 mR/h in a ¹³⁷Cs field. What is the dose rate to tissue,
and how long can someone stand there?
*Check:* 105 µGy/h in air, 117 µGy/h in tissue; 8.6 h to 1 mSv.

**Solution.** The instrument reports **exposure**, which is charge per unit mass
of air. Convert with the relation S&F never write down:
$$\dot D_{\rm air}=(0.012\ \text{R/h})(8.73\times10^{-3}\ \text{Gy/R})
=\boxed{105\ \mu\text{Gy/h}}.$$

Tissue absorbs more per gram than air does, by the ratio of the two $\mu_{en}$ —
the "f-factor":
$$f=\frac{(\mu_{en}/\rho)_{\rm water}}{(\mu_{en}/\rho)_{\rm air}}
=\frac{0.03260}{0.02931}=1.112,$$
so $\dot D_{\rm tissue}=\boxed{117\ \mu\text{Gy/h}}$, and with $QF=1$ that is
117 µSv/h.

$$t=\frac{1\ \text{mSv}}{0.117\ \text{mSv/h}}=\boxed{8.6\ \text{hours}}$$
to reach the annual public limit, or 172 hours to reach 20 mSv.

**Two things make this problem worth doing.** First, $f=1.11$ is nearly
energy-independent from 0.1 to 3 MeV (1.095 to 1.113) — that accident is the
entire justification for a unit defined in air being used to protect people.
Second, the answer reframes the reading: 12 mR/h sounds small, and continuous
occupancy would be **1.0 Sv/y**. Survey readings only mean something once
multiplied by an occupancy time.

### P8.  A mixed neutron and gamma field  *(added)*
A field delivers 0.20 mGy/h of gammas and 0.050 mGy/h from 1-MeV neutrons. What
is the equivalent dose rate, and how long to 20 mSv?
*Check:* 1.20 mSv/h; 16.7 h. Ignoring QF understates it 4.8-fold.

**Solution.** Absorbed doses add; equivalent doses add *after* weighting:
$$\dot H=QF_\gamma\dot D_\gamma+QF_n\dot D_n=(1)(0.20)+(20)(0.050)
=\boxed{1.20\ \text{mSv/h}},$$
using $QF=20$ for 1-MeV neutrons [Table 9.1]. The 20 mSv limit is reached in
$\boxed{16.7\ \text{hours}}$.

**The neutrons are 20% of the energy and 83% of the hazard.** An instrument that
measures only absorbed dose — or a calculation that quietly takes $QF=1$ — would
report 0.25 mSv/h and permit 80 hours, a 4.8-fold error in the unsafe direction.

This is precisely why `quality_factor` raises on an unrecognised radiation rather
than returning 1. It is also why mixed-field dosimetry needs a neutron-sensitive
detector alongside the gamma one (`~NE-15`): the neutron component is invisible to
the instrument that dominates the reading, and it dominates the risk.

Note too where 1 MeV sits — dead in the middle of the QF = 20 band, which is
where the fission spectrum lives. The worst quality factor and the most common
reactor neutron are the same neutron.
