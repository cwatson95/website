# NE-23 — Problems

Work each by hand, then check with `code/fuel_cycle.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. §§11.7–11.8
carry no worked problems of their own; these are added, and P1–P3 use the
separative-work machinery the chapter needs and omits.

Weight fractions throughout: natural uranium is **0.7114 wt-%** ²³⁵U, not the
0.7204 **atom**-% of §11.7.

### P1.  Feeding a reload  *(added)*
A PWR reload is 20 t of uranium enriched to 4.5%, with 0.2% tails. How much
natural uranium and how much separative work?
*Check:* 168 t of natural U; 154 tSWU.

**Solution.** From the two balance equations,
$$\frac{F}{P}=\frac{x_P-x_T}{x_F-x_T}=\frac{0.045-0.002}{0.007114-0.002}=8.409,$$
so $F=\boxed{168\ \text{t}}$ and $T=148$ t. The separative work is
$$\text{SWU}=P\,V(x_P)+T\,V(x_T)-F\,V(x_F)=\boxed{154\ \text{tSWU}}.$$

**Note what leaves and what stays.** 168 tonnes in, 20 tonnes out: **88% of the
uranium is set aside as tails**, and it still holds 0.2% ²³⁵U. Enrichment is not
a purification so much as a triage.

Had you used the *atom* percent 0.7204% instead of the weight percent 0.7114%,
$F/P$ would come out 8.26 and the feed 165 t — 1.8% low, three tonnes of uranium
a reload, and nothing in the arithmetic would look wrong.

### P2.  What tails assay should the plant run?  *(added)*
Uranium costs \$100/kg and enrichment \$100/SWU. Is 0.2% tails the right choice
for 4.5% fuel?
*Check:* the optimum is 0.227%; 0.2% costs 0.4% more.

**Solution.** The unit cost of product is
$$C=\frac{F}{P}c_U+\frac{\text{SWU}}{P}c_S,$$
and at $x_T=0.002$ that is $8.409(100)+7.687(100)=\boxed{\$1610\text{/kg}}$.
Scanning $x_T$ gives a minimum at $\boxed{x_T=0.227\%}$, costing \$1604/kg.

**Two lessons.** The optimum is *flat* — 0.2% is within 0.4% of the best — which
is why "0.2%" survived as an industry convention for decades. But the optimum
*moves*: at \$250/kg uranium it falls to 0.14%, and at \$50/kg it rises to 0.30%.

So a stock of depleted tails is not waste in any permanent sense; it is uranium
that was not worth extracting *at the prices of the day*. When uranium prices
rose in the 2000s, enrichers re-ran old tails. The tails assay is a market
signal that happens to be written in isotopes.

### P3.  Why 20% is the line  *(added)*
Compare the separative work to make 1 kg of 90% HEU directly, against making it
from 20%-enriched material. Tails 0.3%.
*Check:* 193 SWU direct; the 20% stage is 90% of it.

**Solution.** Directly from natural uranium, $\boxed{193\ \text{SWU/kg}}$ and 218
kg of feed. Via an intermediate: 1 kg of 90% needs
$$\frac{0.90-0.003}{0.20-0.003}=4.553\ \text{kg of 20\% material},$$
and each of those took 38.3 SWU, so the first stage is
$4.553\times38.3=174$ SWU — $\boxed{90.4\%}$ of the total.

**A stock of 20% uranium is nine tenths of the way to weapons grade**, measured
in the only currency that matters. That is why the IAEA's line between low- and
high-enriched uranium sits at 20% and not somewhere that sounds more dangerous,
and it is why research reactors were converted from HEU to LEU fuel rather than
merely guarded better.

S&F's §11.7.2 has every ingredient of this argument and does not assemble it,
because it never introduces the SWU.

### P4.  What is in the tails pile  *(added)*
Table 11.7's reactor sends 121 227 kg of uranium to tails each year at 0.2%. How
much ²³⁵U is in it, and what fraction of the mined ²³⁵U is that?
*Check:* 242 kg, which is 23% of the ²³⁵U fed in.

**Solution.** The tails carry $121\,227\times0.002=\boxed{242\ \text{kg}}$ of
²³⁵U. The feed carried $149\,297\times0.007114=1062$ kg, so
$\boxed{23\%}$ of the mined ²³⁵U is left behind at enrichment.

**Put that beside the reactor.** The reactor discharges 220 kg of unburned ²³⁵U
plus 178 kg of fissile plutonium — 398 kg of fissile material — while the tails
pile holds 242 kg. **More fissile material is set aside at the enrichment plant
and in the spent-fuel pool than is actually fissioned** (about 600 kg of ²³⁵U
plus the bred plutonium).

That is the once-through cycle in one line, and it is what "recycling reduces
lifetime U₃O₈ requirements by about 45%" (§11.7) is measuring. The depleted
uranium is also the feedstock a fast breeder runs on, which is why a breeder's
lifetime natural-uranium requirement is 40 kg rather than 4500 tonnes.

### P5.  Where the energy came from  *(added)*
From Table 11.8, how much of the fission energy in a discharged LWR assembly came
from plutonium, and what burnup does the table imply?
*Check:* 43%; 33.3 GWd/tU.

**Solution.** Account for the heavy atoms per 100 loaded:

| | |
|---|---|
| ²³⁵U: 3.30 → 0.81, so 2.49 consumed | of which 0.51 captured to ²³⁶U, **1.98 fissioned** |
| ²³⁸U: 96.7 → 94.3, so 2.40 consumed | of which 0.88 remains as Pu, **1.52 fissioned** |
| total | 1.98 + 1.52 = **3.50** = the printed fission-product entry |

So $\boxed{1.52/3.50=43\%}$ of the fissions were plutonium. And 3.5% of the heavy
atoms fissioned, at 200 MeV each, is
$$\frac{0.035\times10^6\ \text{g}}{235}\times6.022\times10^{23}\times200\ \text{MeV}
=\boxed{33.3\ \text{GWd/tU}},$$
which is `~NE-22` Table 11.2's printed discharge burnup of 33 GWd/tU.

**Two tables six chapters apart, from different sources, agreeing to 1%** — and
neither the balance nor the burnup check appears in the book. The 43% is the
quantitative version of §11.1's "almost half the power" at end of life, and it is
also why the fuel does not simply lose reactivity as it burns (`~NE-20` §5).

For a modern 50 GWd/tU fuel the same arithmetic gives 5.3% of heavy atoms
fissioned — half again as much, which is why cladding and fission-gas pressure,
not reactivity, set today's burnup limit.

### P6.  Two clocks  *(added)*
How long must fission-product waste be isolated, and how long must the actinides?
*Check:* ~1000 years against ~800 000 — a factor of 800.

**Solution.** Only seven fission products have half-lives over 25 years, and
**five of those are million-year nuclides** — effectively stable, and therefore of
negligible specific activity. The long-term activity is ¹³⁷Cs (30.2 y) and ⁹⁰Sr
(29.1 y), so
$$t=\frac{-\ln(10^{-10})\times30}{\ln2}=\boxed{997\ \text{years}}$$
to fall below the activity of the original ore. For ²³⁹Pu at 24 000 y the same
reduction takes $\boxed{800\,000}$ years.

**That factor of 800 is the entire technical case for reprocessing.** Separate the
actinides and put them back in a reactor and the repository problem shortens from
geological to merely historical — from "will the rock still be there" to "will
anyone still be reading the sign".

Against it: reprocessing produces separated plutonium, and the U.S. has held
since 1977 that leaving plutonium embedded in intensely radioactive spent fuel is
itself a safeguard. **This is not a technical disagreement.** Both sides accept
the 800-fold number; they weigh a proliferation risk now against a stewardship
burden later, and reasonable people have reached opposite conclusions —
France and the UK reprocess, the U.S. does not.
