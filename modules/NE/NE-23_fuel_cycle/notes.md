# NE-23 — The nuclear fuel cycle: enrichment & SWU, burnup, spent fuel, waste (notes)

`~NE-22` ran the reactor. This module follows the **material**: 150 tonnes of
natural uranium a year in at one end, 26 tonnes of spent fuel out at the other,
and a disposal problem measured in hundreds of thousands of years.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§11.7–11.8, cited by **printed** page (PDF = printed + 23).

## 1. The trap before any arithmetic: atom-% is not weight-%

Natural uranium is **0.7204 atom-%** ²³⁵U [§11.7] and **0.7114 weight-%**. Every
enrichment calculation in the industry — feed, product, tails, separative work —
uses **weight** fractions.

Substituting the atom percent into a cascade balance changes the feed requirement
by **1.8%**: 2.7 tonnes of natural uranium a year on one reactor. And it is
invisible, because both numbers look like 0.72%.

How do we know Table 11.7 used weight fractions? Its ²³⁵U balance closes to
**0.13%** with 0.7114 wt-% and to 1.4% with 0.7204 a%. The table tells you which
convention it is in, if you ask it.

## 2. The mass balance

Table 11.7 is a complete annual flowsheet for a 1000 MW(e) PWR at 75% capacity
with 0.2% tails, and it closes:

| stage | kg/y |
|---|---|
| U in U₃O₈ (mining/milling) | 150 047 |
| U in UF₆ (conversion) | 149 297 |
| enrichment product (²³⁵U 821 + ²³⁸U 27 249) | **28 070** |
| tails at 0.2% | **121 227** |
| discharged U + Pu | 26 104 |
| fission products | 873 |

**Product + tails = 28 070 + 121 227 = 149 297 = feed, to the kilogram.**

**Four fifths of the mined uranium never enters a reactor.** It leaves the
enrichment plant as depleted tails still containing a quarter of the ²³⁵U it
arrived with — set aside because extracting the rest costs more separative work
than it is worth.

The strongest check available is a cross-check between a *mass* and an *energy*:
873 kg of fission products at 200 MeV per fission is 830 000 MWd(t) = **277
full-power days** at 3000 MW(t), against the **274 days** the table's own 75%
capacity factor implies. Two completely different routes agreeing to 1%.

## 3. Separative work — the quantity S&F never name

§11.7.2 describes five enrichment technologies — gaseous diffusion, gas
centrifuge, aerodynamic, electromagnetic, laser — and never writes down the unit
they are all measured in. It follows from one function:
$$V(x)=(2x-1)\ln\frac{x}{1-x},\qquad
\text{SWU}=P\,V(x_P)+T\,V(x_T)-F\,V(x_F).$$

$V$ vanishes at $x=1/2$ — the least-separated state — and diverges at both ends:
**purity is expensive whichever end of the mixture you want**. Table 11.7's own
numbers give **116 tSWU/y**, squarely in the industry range for a 1000 MW(e) PWR.

Two consequences worth carrying.

**The tails assay is a price, not a constant.** Leaner tails need less uranium and
more separative work. With uranium at \$50/kg the optimum is 0.30%; at \$250/kg
it is 0.14%. The 0.2% of Table 11.7 corresponds to roughly equal uranium and SWU
prices — a convention of its era.

**Enrichment work is front-loaded, which is the whole of proliferation policy.**
Making 1 kg of 90% HEU needs 4.55 kg of 20% material, and making *that* is
**90% of the total separative work**. A stock of 20%-enriched uranium is nine
tenths of the way to weapons grade — which is exactly why 20% is the regulatory
line between low- and high-enriched uranium.

## 4. Spent fuel: where the energy actually came from

Table 11.8 gives the composition before and after, in atom-%. Both columns sum to
**exactly 100.00**, and the transmutation accounting closes to two decimals with
no adjustment:

$$\begin{aligned}
^{235}\text{U consumed }2.49&=0.51\text{ captured to }^{236}\text{U}+1.98\text{ fissioned}\\
^{238}\text{U consumed }2.40&=0.88\text{ Pu remaining}+1.52\text{ Pu fissioned}\\
\text{total fissions}&=1.98+1.52=\boxed{3.50}=\text{the printed fission-product entry.}
\end{aligned}$$

**So 43% of the energy came from plutonium that was not in the fuel when it was
loaded.** That is what §11.1 means by "almost half the power" at end of life; it
is why a reactor's reactivity does not simply decay away (`~NE-20` §5); and it is
why spent fuel is simultaneously a waste and a fuel.

And the burnup implied — 3.5% of the heavy atoms fissioned is **33.3 GWd/tU** —
is `~NE-22` Table 11.2's printed discharge burnup of 33, six chapters earlier and
from a different source.

## 5. Two waste problems, 800-fold apart

Of the hundreds of fission products, only **seven** have half-lives over 25 years
[§11.7.4] — and five of those have *million*-year half-lives, which makes them
effectively stable and therefore of negligible activity. The long-term
fission-product activity is set entirely by **¹³⁷Cs (30.2 y) and ⁹⁰Sr (29.1 y)**,
and falls by $10^{-10}$ in about **1000 years**, below the activity of the ore the
uranium came from.

The **actinides** are a different problem. ²³⁹Pu's 24 000-year half-life needs the
same reduction over **800 000 years**.

That factor of 800 is the entire technical case for reprocessing: separate the
actinides back into fuel and the repository problem shortens from geological to
merely historical. Against it stands proliferation — reprocessing produces
separated plutonium, and the U.S. position since 1977 has been that leaving the
plutonium inside intensely radioactive spent fuel is itself a safeguard.

Waste is classified [§11.7.3] as **HLW** (fission products, or spent fuel itself
in the once-through cycle), **TRU** (actinides above 100 nCi/g), **mill tailings**
(low activity, large volume, the concern is radon), **LLW** (below 100 nCi/g and
handleable unshielded) and **ILW** (everything else). The 100 nCi/g line is the
only quantitative boundary in the scheme.

## 6. Uranium supply, and propulsion

A 1000 MW(e) LWR needs ~150 t of natural uranium a year, **4500 t over a 30-year
life** [§11.7.1]. Recycling roughly halves it; a fast breeder needs about **40 kg**
over its entire life — five orders of magnitude less, which is the fuel-cycle
argument behind four of the six Generation IV systems (`~NE-22` §6).

Uranium is not scarce: 700× more abundant than gold in the crust, 4 × 10⁹ tonnes
dissolved in the oceans. It is *cheaply extractable* uranium that is finite, and
the resource base at under \$130/kg is about 4 × 10⁶ tonnes.

§11.8 covers **naval propulsion**, where the fuel cycle looks completely different:
highly enriched fuel, cores designed to last the life of the vessel, and the
*Nautilus* travelling 100 000 miles on one loading. The trade is the opposite of a
power reactor's — enrichment cost is irrelevant against never refuelling.

## Where this goes

- `~NE-22` — the reactor these flows pass through; Table 11.2's burnup is
  confirmed here from Table 11.8.
- `~NE-20` — plutonium buildup as a reactivity feedback; burnup as the slowest one.
- `~NE-09`, `~NE-05` — fission yields and the decay chains behind the waste.
- `~NE-18` — the dose limits that define what a repository must achieve.
- `~NE-24` — the fusion fuel cycle, for contrast: no mining, no enrichment, and a
  tritium problem instead.

## A note on what this module adds

Nothing in §§11.7–11.8 is wrong. Two things are missing, and both are load-bearing:

1. **Separative work.** Five technologies are described without the unit that
   measures them. `value_function`, `separative_work`, `optimal_tails_assay`.
2. **The atom/weight distinction.** §11.7 prints 0.7204 a% and every calculation
   downstream needs 0.7114 wt-%. `atom_to_weight_fraction`, and a test that
   measures what the confusion costs.

The rest of the module is the book's own tables, checked against themselves —
which is how the two verifications above (the mass/energy agreement in Table 11.7,
and the exact heavy-atom closure of Table 11.8) came to light.
