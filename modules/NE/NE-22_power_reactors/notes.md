# NE-22 — Nuclear power reactors: PWR/BWR steam cycles, Gen III & IV (notes)

`~NE-19`–`~NE-21` built a critical core. This module is about the machine around
it, and the machine is mostly a **steam plant**. Everything distinctive follows
from one constraint:

> Water's critical temperature is **374 °C**, so a water-cooled core runs below
> ~340 °C, so the steam is barely superheated, so the Carnot ceiling is ~45% and
> the plant achieves **~34%**.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§11.1–11.6, cited by **printed** page (PDF = printed + 23).

## 1. The 374 °C ceiling

Above its critical temperature no pressure makes water a liquid [§11.1.4] — and a
water-moderated core needs *liquid* water, both to moderate and because steam is
a far worse coolant. So the core outlet is capped near 340 °C and the steam
reaches the turbine at 284 °C.

$$\eta_{\rm Carnot}=\frac{T_{\rm in}-T_{\rm out}}{T_{\rm in}}
=\frac{557-306}{557}=0.451\qquad\text{[Eq. (11.1)]}$$

against an achieved 0.34 — **75% of Carnot**, which is a good turbine, not a bad
reactor.

Three consequences run through the rest of the chapter:

- **The turbines are wet-steam machines.** Saturated or barely superheated steam
  means moisture separators, reheaters, and larger, more expensive turbines than
  a fossil plant's.
- **Two thirds of the heat is thrown away.** A 1000 MW(e) plant makes 2940 MW(t)
  and rejects **1940 MW** — nearly twice what it sells — into a river, the sea or
  a cooling tower. That number, not the reactor, picks the site.
- **Generation IV is an escape attempt.** All six systems run above 374 °C, using
  gas, sodium, lead or salt, and all six therefore beat 34%.

A note on a tension in the text: §11.1.2 says "in modern nuclear power plants,
conversion efficiencies of about 40% can be achieved", while §11.1.4 says water
plants are limited "to about 34%" and that only non-water coolants "permit
thermal efficiencies up to 40%". Since essentially every operating plant is
water-cooled, the 40% belongs to the second sentence. The book's own tables agree
with §11.1.4: 0.34 for both 1970s designs, 0.329–0.370 for the Gen III PWRs.

## 2. PWR against BWR: one decision, a factor of two everywhere

Both 1970s designs deliver ~285 °C steam at 34%. Nearly everything else differs
by about a factor of two, and every difference traces to one choice — **a BWR
boils in the core and a PWR does not**:

| | PWR | BWR | |
|---|---|---|---|
| operating pressure | 15.5 MPa | 7.17 MPa | boiling is allowed, so less pressure is needed |
| vessel wall | 22 cm | 15 cm | ...and a thinner wall suffices |
| power density | 102 kW/L | 56 kW/L | but the steam voids need room |
| core volume | 37 m³ | 68 m³ | so the core is nearly twice as big |
| equilibrium enrichment | 3.2% | 1.9% | the direct cycle is neutronically cheaper |
| discharge burnup | 33 GWd/tU | 27.5 GWd/tU | ...and pays for it here |
| assemblies × rods | 193 × 264 | 760 × 62 | |

The PWR's extra loop — a steam generator between primary and secondary — costs
pressure, capital and a heat-transfer step; it buys a secondary circuit that
never sees the core, which is why PWR turbine halls are not radiologically
controlled and BWR ones are.

## 3. The tables check themselves — and one does not

Chapter 11's content *is* its tables, so the useful discipline is to make each
reproduce its own derived quantities from its own primary ones. **Table 11.2
(PWR) passes on five independent relations:**

| relation | derived | printed |
|---|---|---|
| core geometry → power density | 102.2 kW/L | 102 |
| fuel loading → specific power | 33.0 kW/kg | 33 |
| rod count → linear heat rate | 17.9 kW/m | 17.5 |
| linear rate → surface heat flux | 0.586 MW/m² | 0.584 |
| lattice × pitch → assembly width | 21.42 cm | 21.4 |

**Table 11.3 (BWR) fails one**: 25.9 kW/kg × 168 t = 4351 MW against a printed
3830 MW — 14% apart. Its own thermal output and loading imply 22.8 kW/kg. Since
the identical three-way check passes for the PWR to 0.15%, the defect is in the
table and not in the method.

## 4. Peaking, and what flattening is worth

`~NE-21` derives 3.639 for a bare uniform cylinder. Table 11.2's PWR runs
**2.50** and Table 11.3's BWR **2.20**.

Since the hottest fuel pin limits the whole reactor, that gap is directly
saleable power: flattening from 3.64 to 2.50 is **46% more output** from the same
core at the same peak limit. It is bought with the reflector (`~NE-19` §10.6),
fuel zoning — fresh fuel at the periphery, depleted at the centre — and burnable
poisons. The BWR does slightly better because its voids give it a distributed
in-core negative feedback a PWR does not have.

## 5. Generation III: subtraction

The BWR/6 → ABWR → ESBWR sequence [Table 11.4] is not about efficiency, which
does not move (34.9%, 34.4%, 34.4%). It is about **removing components**:

| | BWR/6 | ABWR | ESBWR |
|---|---|---|---|
| recirculation pumps | 2 external | 10 internal | **0** |
| safety-system pumps | 9 | 18 | **0** |
| safety diesel generators | 3 | 3 | **0** |

**Passive safety is not a better pump; it is no pump.** The ESBWR buys it by
growing the vessel 27% taller so that natural circulation drives the core flow —
and gets 14% more output while doing it.

The PWR line does the same thing differently [Table 11.5]. The AP1000 halves the
loops (2 against the EPR's 4); the EPR instead buys margin with size, running a
*lower* linear heat rate (156 W/cm against 187) in a bigger vessel. The EPR is
also the more efficient plant, at 37% against 32.9% — the only Gen III entry that
approaches §11.1.2's "about 40%".

## 6. Generation IV, and small reactors

All six GIF systems [§11.5] run outlet temperatures above 374 °C:

| | coolant | outlet | η | spectrum |
|---|---|---|---|---|
| SCWR | supercritical water | 550 °C | 0.44 | thermal or fast |
| LFR | lead / lead-bismuth | 550 °C | 0.42 | **fast** |
| SFR | sodium | 550 °C | 0.40 | **fast** |
| MSR | fluoride salt | 700 °C | 0.44 | thermal or fast |
| GFR | helium | 850 °C | 0.48 | **fast** |
| VHTR | helium | 1000 °C | 0.50 | thermal |

Note that **four of the six are fast**. That is a *fuel-cycle* argument
(`~NE-23`) rather than a thermodynamic one — the two goals are being pursued
together, and the book is explicit that as of 2015 none had reached full plant
design, with deployment "sometime after 2030".

The small-reactor landscape [Table 11.6] is the opposite bet: **most SMR designs
are PWRs**, i.e. established technology shrunk rather than a new technology, and
as of 2014 almost none were under construction.

## Where this goes

- `~NE-19`, `~NE-21` — the core physics; peaking and power density are where
  those modules' results become engineering.
- `~NE-20` — control rods, boron and burnable poisons appear here as hardware.
- `~NE-23` — enrichment, burnup and the back end; the fuel-cycle case for fast
  reactors.
- `~Thermo-08`, `~Thermo-09` — the Rankine cycle this chapter runs on.
- `~NE-18` — the dose limits that shape containment and the turbine hall.

## A note on this module's finding

One printed inconsistency, and one tension between two sections.

1. **Table 11.3**'s specific power (25.9 kW/kg), thermal output (3830 MW) and
   fuel loading (168 t) cannot all be right — the product is 14% too large. The
   same check on Table 11.2 passes to 0.15%.
2. **§11.1.2 vs §11.1.4** on "about 40%": the first attributes it to "modern
   nuclear power plants", the second to non-water coolants only. Both of the
   book's own 1970s tables and both of its Gen III PWRs are at or below 37%.
