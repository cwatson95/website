# NE-25 — Direct energy conversion: thermoelectric, thermionic, AMTEC, betavoltaic (notes)

`~NE-22`'s power plant turns heat into electricity with a turbine, and needs
thousands of tonnes of machinery to do it at 34%. This module is about the
alternatives with **no moving parts**, and about the one application where that
is worth almost any efficiency penalty: a spacecraft that must run for decades
with nobody to fix it.

**Voyager 1 has been returning data since 1977 on 470 W of thermoelectrics.** No
turbine has ever run unattended for forty-seven years.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§12.5–12.11, cited by **printed** page (PDF = printed + 23).

## 1. Everything here is still a heat engine

Thermoelectric, thermionic, AMTEC and Stirling all take heat in hot and reject it
cold, so **Carnot bounds every one** [§12.6.1]. What direct conversion replaces is
the *turbine*, not the thermodynamics.

| | efficiency | heat engine? | moving parts? |
|---|---|---|---|
| thermoelectric | 5–10% | yes | no |
| thermionic | 1–10% | yes | no |
| AMTEC | 15–25% | yes | no |
| Stirling | 25–30% | yes | **yes** |
| **betavoltaic** | 0.5–8% | **no** | no |

Only the betavoltaic escapes: beta particles create electron–hole pairs directly,
with no temperature difference to maintain. It pays in **microwatts** — a curie of
tritium at 2% conversion yields 0.7 µW, so matching a single 2.5 W SNAP-3 would
need **3.7 megacuries**.

Note the shape of the table: the most efficient converter is the only one with a
moving part, and the best of the rest (AMTEC) is the least flown.

## 2. The thermoelectric penalty is ZT

S&F quote thermoelectric efficiencies "up to 10 percent" without the relation
that produces them:
$$\eta=\eta_{\rm Carnot}\,\frac{\sqrt{1+ZT}-1}{\sqrt{1+ZT}+T_c/T_h}.$$

The second factor is the price of using a *solid* instead of a working fluid, and
it is severe. At $ZT=1$ — the plateau the best materials sat on for decades — it
is **0.23**. So a 1300 K → 500 K pair with a 61% Carnot limit yields a 14% device,
and a real RTG with worse temperatures and parasitic heat leaks lands at **5–7%**.

That factor of five is the whole reason direct conversion is a niche.

## 3. Thermionics need 1400 K because of an exponential

§12.6.1 says emitter temperatures "typically in excess of 1400 K" are needed and
does not say why. The Richardson law does:
$$J=AT^2e^{-\phi/kT}.$$

For a 2.5 eV emitter, $J$ runs $10^{-8}$ A/cm² at 800 K and **39 A/cm² at 1800 K**
— ten orders of magnitude for a factor of 2.25 in temperature. There is no
low-temperature thermionic converter and there cannot be. It is also why caesium
coatings matter: dropping φ from 2.5 to 1.8 eV buys a factor of 200.

And note the structure of the output: the voltage is a *difference* of work
functions, so the collector must be a poor emitter while the emitter is a good
one — and both must stay that way while sitting millimetres apart at 1800 K.

## 4. The isotope is chosen by half-life, not by power

Table 12.2's nine practical sources span a factor of **1500** in specific power,
and that is almost the wrong axis to read. Specific power and half-life come from
the same decay constant, so they trade against each other by construction:

| | W/g | T½ | power left after 1 y | after 47 y |
|---|---|---|---|---|
| ²¹⁰Po | 144 | 138 d | 0.16 | 10⁻³⁷ |
| ²⁴²Cm | 120 | 163 d | 0.23 | — |
| ²⁴⁴Cm | 2.78 | 18.1 y | 0.96 | 0.17 |
| **²³⁸Pu** | **0.558** | **87.7 y** | **0.992** | **0.69** |

²¹⁰Po wins a 90-day mission outright and is useless past a year. **²³⁸Pu wins
everything long**, which is why it flew on Voyager, Cassini, New Horizons and
Curiosity — and why the world ran out of it.

**A caution the mass ranking hides.** By mass, the curiums beat ²³⁸Pu even on a
30-year mission. They have never flown, and Table 12.2 says why in its shielding
row: both are marked "neut." — strong spontaneous-fission neutron emitters,
against which lead is useless. ⁶⁰Co is the opposite problem: plentiful and cheap,
but its 1.17 and 1.33 MeV gammas need **18 cm of lead**.

## 5. Table 12.2 checks itself eighteen times

The table gives half-life, recoverable energy, specific activity and specific
power for nine nuclides — and only two of those four are independent:

- every specific power reproduces from its own activity × energy row, to **0.5%**;
- every specific activity reproduces from its own half-life and mass number, to
  **1.3%** (⁹⁰Sr worst, plausibly because it is quoted in secular equilibrium
  with ⁹⁰Y);
- and the Ci/W column follows from the other two.

Eighteen internal checks passed is what makes a table usable rather than merely
printed.

## 6. The flight record

Table 12.1's SNAP series shows the same trade in hardware: the ⁹⁰Sr units are one
to two **orders of magnitude** heavier per watt than the ²³⁸Pu ones — SNAP-7B is
2100 kg for 60 W(e); SNAP-27, also 60 W(e), is 14 kg. Every space mission flew
plutonium; the strontium units sat on the sea floor and in the Arctic.

Table 12.3's space *reactors* [§12.11] tell a bleaker story. All convert at
**1–5%**, an order of magnitude below an LWR turbine. BUK flew 31 times at 3%
efficiency and 310 kg per kW(e). SP-100 — the best design on every axis, 100 kW(e)
at 5% and 54 kg/kW(e) — **never flew at all**.

And COSMOS-954, a BUK, fell on the Northwest Territories in 1978 and scattered
its fission products across a large part of it. §12.11.2's account of the
"secondary backup safety system" added afterwards — eject the fuel and let it
disperse as fine particles in the upper atmosphere — is worth reading as an
example of what counts as a fix when reentry cannot be prevented.

## Where this goes

- `~NE-22` — the turbine these devices replace, and the 34% they must be
  measured against.
- `~NE-23` — where ²³⁸Pu comes from (neutron irradiation of ²³⁷Np) and why the
  supply failed.
- `~NE-05`, `~NE-06` — decay modes and kinetics; the exponential in §4.
- `~NE-18` — the shielding requirements in Table 12.2's last rows.
- `~Thermo-12`, `~SM-11` — thermoelectric materials and the physics of ZT.

## A note on what this module adds

Nothing in §§12.5–12.11 was found to be wrong. Three things are missing and are
supplied here, because each is what turns a described device into a designed one:

1. **The thermoelectric efficiency relation.** §12.5 gives 5–10% with no formula,
   so there is no way to see that ZT is the binding parameter or what improving it
   would buy. `thermoelectric_efficiency`, `zt_for_efficiency`.
2. **The Richardson law.** §12.6.1's "in excess of 1400 K" is stated as a fact
   rather than a consequence. `richardson_current`.
3. **Mission sizing.** §12.10 lists nine isotopes and their properties without
   ever combining them into "how many grams for this mission". The ranking
   inverts with mission length, which is the whole point of the table.
   `fuel_mass_for_power`, `mission_sizing`.

`zt_for_efficiency` **refuses** a target at or above Carnot: no ZT reaches it, and
a bisection would otherwise run to its upper bound and return a plausible number.
