# NE-25 — Problems

Work each by hand, then check with `code/direct_conversion.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. Chapter 12's
problems on conversion devices are largely descriptive; these are added and are
quantitative.

### P1.  A table that checks itself  *(added)*
Verify Table 12.2's ²³⁸Pu row: derive its specific power from its activity and
energy, and its activity from its half-life and mass number.
*Check:* 0.557 W/g (printed 0.558); 17.13 Ci/g (printed 17.1).

**Solution.**
$$P=(17.1\ \text{Ci/g})(3.7\times10^{10})(5.495\ \text{MeV})(1.602\times10^{-13})
=\boxed{0.557\ \text{W/g}},$$
$$A=\frac{\ln2}{T_{1/2}}\frac{N_A}{238}
=\frac{\ln2}{2.77\times10^9\ \text{s}}\times2.53\times10^{21}
=6.34\times10^{11}\ \text{Bq/g}=\boxed{17.13\ \text{Ci/g}}.$$

**Only two of the table's four numeric rows are independent**, and all nine
nuclides pass both checks (0.5% on power, 1.3% on activity, ⁹⁰Sr worst). Eighteen
internal checks is what makes a table usable rather than merely printed — and it
takes about five minutes to do for all nine.

Note also the Ci/W column: 30.7 for ²³⁸Pu. That is the number that sets the
transport licence and the handling regime, and it is *not* proportional to the
power. ¹³⁷Cs needs 901 Ci per thermal watt — thirty times as much activity for the
same heat.

### P2.  Sizing an RTG  *(added)*
A mission needs 100 W(e) from a 6%-efficient thermoelectric converter. How much
²³⁸Pu, at launch and after 30 years? Which isotope would be lightest for a 90-day
mission?
*Check:* 2987 g and 3786 g; ²¹⁰Po at 18 g.

**Solution.** 100 W(e) at 6% needs 1667 W thermal, so at 0.558 W/g,
$\boxed{2987\ \text{g}}$. Sized to still deliver 100 W(e) *after* 30 years the
power has fallen by $e^{-30\ln2/87.7}=0.789$, so $\boxed{3786\ \text{g}}$ — 27%
more.

For 90 days the ranking is completely different: ²¹⁰Po **18 g**, ²⁴²Cm 20 g,
¹⁴⁴Ce 85 g. ²³⁸Pu would need nearly three kilograms.

**A mission is sized at end of life, not at launch** — and the isotope ranking
inverts with mission length, because specific power and half-life both come from
the same decay constant and therefore trade against each other by construction.

### P3.  What ZT would you need?  *(added)*
A converter runs between 1300 K and 500 K. Find the Carnot limit, the efficiency
at ZT = 1, and the ZT needed for 20%.
*Check:* 61.5%; 14.2%; ZT = 1.78.

**Solution.** $\eta_C=(1300-500)/1300=\boxed{0.615}$. Then
$$\eta=\eta_C\frac{\sqrt{1+ZT}-1}{\sqrt{1+ZT}+T_c/T_h}
=0.615\times\frac{\sqrt2-1}{\sqrt2+0.385}=\boxed{0.142},$$
i.e. **23% of Carnot**, and inverting for 20% gives $\boxed{ZT=1.78}$.

**The factor of five between 61% and 14% is the whole story of the technology.**
It is not a manufacturing problem: it is what a solid-state converter costs
relative to a working fluid, and it is why S&F's quoted 5–10% is what real RTGs
achieve once parasitic heat leaks and worse temperatures are included.

Note the shape of the curve. Going from ZT = 1 to ZT = 2 buys 50%; going from 2
to 4 buys 36%; reaching Carnot requires ZT → ∞. Materials research chases a
target that recedes.

### P4.  Why 1400 K  *(added)*
S&F say thermionic emitters need "temperatures in excess of 1400 K". Show why,
using the Richardson law with φ = 2.5 eV.
*Check:* 1.4 × 10⁻⁸, 0.24 and 39 A/cm² at 800, 1400 and 1800 K.

**Solution.** $J=AT^2e^{-\phi/kT}$ with A = 120 A cm⁻² K⁻²:

| T | J |
|---|---|
| 800 K | 1.4 × 10⁻⁸ A/cm² |
| 1000 K | 3.0 × 10⁻⁵ |
| 1400 K | 0.24 |
| 1800 K | 39 |

**Nine orders of magnitude for a factor of 2.25 in temperature.** Below ~1400 K
the current density is not small, it is negligible; there is no low-temperature
thermionic converter and there cannot be one.

The same exponential explains caesium: lowering φ from 2.5 to 1.8 eV at 1400 K
buys a factor of **200**, which is why thermionic emitters are caesiated and why
keeping them that way — at 1800 K, millimetres from a collector that must *not* be
a good emitter — is the central engineering difficulty.

### P5.  The one device with no Carnot bound  *(added)*
A betavoltaic converts tritium betas (5.67 keV mean) at 2%. What does a curie
give, and what would it take to match a 2.5 W SNAP-3?
*Check:* 0.67 µW per curie; 3.7 million curies.

**Solution.**
$$P=(3.7\times10^{10}\ \text{s}^{-1})(5670\ \text{eV})(1.602\times10^{-19})(0.02)
=\boxed{6.7\times10^{-7}\ \text{W}}.$$
To reach 2.5 W would take $\boxed{3.7\times10^6\ \text{Ci}}$ — about **385 grams
of tritium**, and 140 petabecquerels.

**Escaping Carnot does not make you competitive.** The betavoltaic has no
temperature difference to maintain and no thermodynamic ceiling, and it is still
six orders of magnitude short of the smallest RTG in Table 12.1. Its niche is
where microwatts for decades is exactly the requirement: pacemakers, memory
backup, remote sensors.

Note also what fixes the scale — the *activity*, not the energy. A curie is a
curie; the only levers are the beta energy (⁶³Ni's 17.4 keV is worth 3×) and the
conversion efficiency, and neither buys orders of magnitude.

### P6.  Voyager, and the strontium units  *(added)*
Voyager 1 launched in 1977 with 470 W(e) of ²³⁸Pu thermoelectrics. What thermal
fraction remains? And compare SNAP-7B with SNAP-27, both 60 W(e).
*Check:* 69% after 47 years; 150× difference in mass per watt.

**Solution.** $e^{-47\ln2/87.7}=\boxed{0.690}$, so the *thermal* source is at
69% — the electrical output is lower still, because thermocouples degrade too.

From Table 12.1:

| | fuel | W(e) | mass | kg per W(e) |
|---|---|---|---|---|
| SNAP-7B | ⁹⁰Sr | 60 | 2100 kg | 35.0 |
| SNAP-27 | ²³⁸Pu | 60 | 14 kg | 0.23 |

**A factor of 150 for the same electrical output.** Two causes compound: ⁹⁰Sr's
specific power is 0.916 W/g against ²³⁸Pu's 0.558 — actually *higher* — but its
half-life is a third, and its beta emissions (with ⁹⁰Y's 2.28 MeV endpoint) make
bremsstrahlung that needs real shielding, while ²³⁸Pu's alphas stop in the fuel
cladding.

That is why every SNAP that left the atmosphere burned plutonium and every ⁹⁰Sr
unit sat on the sea floor, on an Arctic shoreline or on an offshore rig, where
2100 kg is free and cost is not.

**And it is why the ²³⁸Pu supply mattered.** It is made by irradiating ²³⁷Np, a
reprocessing product (`~NE-23`), so the decision not to reprocess ended U.S.
production in 1988. Every outer-planet mission since has flown from stockpile.
