# NE-22 — Problems

Work each by hand, then check with `code/power_reactors.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. Chapter 11's
own problems are almost all fuel-cycle and belong to `~NE-23`; these are added
and work the reactor side.

### P1.  What 34% costs a site  *(added)*
A 1000 MW(e) LWR runs at 34%. How much heat must the site reject, and how much
cooling water does that take at a 10 °C rise? What would 44% change?
*Check:* 2941 MW(t), 1941 MW rejected, 46 m³/s; at 44%, 1273 MW.

**Solution.** $Q_{\rm in}=1000/0.34=\boxed{2941\ \text{MW(t)}}$, so the rejected
heat is
$$Q_{\rm out}=Q_{\rm in}-W=1000\left(\frac{1}{0.34}-1\right)=\boxed{1941\ \text{MW}}.$$
With $c_p=4186$ J kg⁻¹K⁻¹ and a 10 °C rise,
$$\dot m=\frac{1.941\times10^9}{4186\times10}=4.6\times10^4\ \text{kg/s}
=\boxed{46\ \text{m}^3\text{/s}}.$$

**That is a small river**, and it is the reason power reactors sit on coastlines,
large rivers and lakes, or carry 150 m cooling towers. A Generation IV plant at
44% rejects 1273 MW — a third less, and 30 m³/s.

Note the asymmetry the number exposes: the plant is sold as "1000 megawatts", and
the largest single thing it does is heat water by ten degrees at two thousand
megawatts. Waste heat is not a side effect of the design; at 34% it *is* the
design.

### P2.  How good is a reactor turbine?  *(added)*
A PWR delivers 284 °C steam to a condenser at 33 °C and achieves 34%. What
fraction of Carnot is that, and what would a 540 °C gas-cooled core allow?
*Check:* 45.1% Carnot, so 75% of it; 62.4% at 540 °C.

**Solution.** With absolute temperatures 557 K and 306 K,
$$\eta_{\rm Carnot}=\frac{557-306}{557}=\boxed{0.451},\qquad
\frac{0.34}{0.451}=\boxed{75\%\ \text{of Carnot}}.$$
At 540 °C (813 K), $\eta_{\rm Carnot}=\boxed{0.624}$ — **38% higher**.

**The 34% is not a turbine failure.** 75% of Carnot is a good machine; the
limitation is entirely the source temperature, and the source temperature is set
by water. That reframes the whole Generation IV programme: it is not an attempt
to build better turbines but to feed the existing ones hotter gas.

A caution on Eq. (11.1) as the book states it: the Carnot efficiency applies to a
reversible engine between two *reservoirs*. A real Rankine cycle takes heat over
a range of temperatures, so the appropriate comparison is a little subtler than a
single $T_{\rm in}$ — which is one reason "75% of Carnot" is a good turbine and
not an indictment.

### P3.  Why a BWR core is bigger  *(added)*
Compare the two 1970s cores of Tables 11.2 and 11.3 by volume and power density,
and explain the ratio.
*Check:* 37.2 m³ at 102 kW/L against 68.0 m³ at 56 kW/L — a factor of 1.8.

**Solution.**
$$V_{\rm PWR}=\pi\left(\frac{3.37}{2}\right)^2(4.17)=\boxed{37.2\ \text{m}^3},
\qquad V_{\rm BWR}=\pi\left(\frac{4.8}{2}\right)^2(3.76)=\boxed{68.0\ \text{m}^3},$$
and dividing the thermal outputs gives 102.2 and 56.3 kW/L — matching the printed
102 and 56 to better than 1%.

**The factor of 1.8 is the price of boiling.** A BWR's core contains, on average,
37% steam by volume (75% at the top), and steam neither moderates nor cools
usefully. So the same fission power needs nearly twice the core volume, and the
larger vessel — 6.4 m against 4.4 m inside diameter — is the visible consequence.

What the BWR gets back: half the operating pressure (7.17 against 15.5 MPa),
hence a **thinner** vessel wall (15 against 22 cm) despite the larger diameter,
and no steam generators at all. The trade is core size against primary-system
pressure, and both designs remain in service because neither side of it is
decisively better.

### P4.  A table that does not add up  *(added)*
Check Table 11.3's specific power against its own thermal output and fuel
loading. Do the same for Table 11.2.
*Check:* BWR 22.8 kW/kg derived against 25.9 printed — 14% apart; the PWR agrees
to 0.15%.

**Solution.** Specific power is thermal output per kilogram of uranium:
$$\text{BWR: }\frac{3830\times10^3\ \text{kW}}{168\times10^3\ \text{kg}}
=\boxed{22.8\ \text{kW/kg}}\quad\text{(printed 25.9)},$$
$$\text{PWR: }\frac{3800\times10^3}{115\times10^3}
=\boxed{33.0\ \text{kW/kg}}\quad\text{(printed 33)}.$$

Three numbers fix each other and the BWR's three do not. Either the loading
should be 148 t, or the output 4351 MW, or the specific power 22.8 kW/kg — the
book gives no way to choose.

**The method is the point.** A table of thirty numbers is not thirty independent
facts; most of them are derivable from the rest, and checking those relations is
how you find out whether you can trust it. Table 11.2 passes five such checks and
is therefore usable; Table 11.3 fails one and its specific power should be treated
as suspect. Neither conclusion is available by reading.

### P5.  What flattening the core is worth  *(added)*
`~NE-21` gives 3.639 for a bare uniform cylinder. Tables 11.2 and 11.3 give 2.50
and 2.20. What is the difference worth, and how is it bought?
*Check:* 46% more power for the PWR at the same peak limit.

**Solution.** The peak heat flux limits the reactor: exceed it anywhere and that
pin fails. For a given peak, the output is proportional to the *average*, so
$$\frac{P_{\rm flattened}}{P_{\rm bare}}=\frac{3.639}{2.50}=\boxed{1.46}.$$

**46% more saleable power from the same core.** It is bought three ways:

- a **reflector** returns leaked neutrons preferentially at the edges, lifting the
  edge flux (`~NE-19` §10.6);
- **fuel zoning** puts fresh, high-reactivity fuel at the periphery and depleted
  fuel at the centre — deliberately the opposite of what a naive design would do;
- **burnable poisons** (gadolinium in BWR fuel, boron in PWR coolant) suppress the
  centre early in life, when it would otherwise peak hardest.

The BWR flattens slightly better (2.20 against 2.50) because its steam voids give
it a *distributed* negative feedback in-core: wherever the flux runs high, more
steam forms, less moderation is available, and the flux is pushed back down. A
PWR has no equivalent mechanism inside the core.

### P6.  How much uranium does a reactor eat?  *(added)*
From Tables 11.2 and 11.3, find the refuelling interval and the annual uranium
throughput of the PWR.
*Check:* 999 full-power days (2.7 y); 42 t U per year.

**Solution.** Discharge burnup times loading, divided by power:
$$t=\frac{33\ \text{GWd/t}\times115\ \text{t}}{3.8\ \text{GW}}
=\boxed{999\ \text{full-power days}}=2.73\ \text{y}.$$
For the BWR, $27.5\times168/3.83=1206$ d = 3.30 y. Annual throughput is then
$115/2.73=\boxed{42\ \text{t U/y}}$.

**Two things to notice.** Real plants do not run a whole core to discharge and
then replace it; they replace roughly a third every 18 months, which gives the
same average residence time while keeping the reactivity swing manageable
(`~NE-20` §5).

And 42 t of uranium per year is small — a few railway wagons — against roughly
**2.5 million tonnes of coal** for the same electricity. That density is the whole
economic case for fission, and it is also why the back end (`~NE-23`) is a
different kind of problem from fly ash: the waste is small enough to be kept, so
it must be.
