# NE-04 — Problems

Work each by hand, then check with `code/q_values.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P2 follow the book's
Chapter 4 problems 1 and 5 (printed 94–95); P3–P8 are added. Masses from
`../data_tables/B1_atomic_masses.csv`, $c^{2}=931.494043$ MeV/u.

### P1.  Completing reactions by conservation  *(S&F Ch. 4, Prob. 1)*
Fill in the missing species, using conservation of nucleon number and charge:
(a) $^{238}_{92}\mathrm{U}+{}^{1}_{0}n\to(?)$;
(b) $^{14}_{7}\mathrm{N}+{}^{1}_{0}n\to(?)+{}^{1}_{1}\mathrm{H}$;
(c) $^{226}_{88}\mathrm{Ra}\to(?)+{}^{4}_{2}\mathrm{He}$;
(d) $(?)\to{}^{230}_{90}\mathrm{Th}+{}^{4}_{2}\mathrm{He}$.
*Check:* `check_conservation` returns `(0, 0)` for each completed reaction;
the Q-values are (b) $+0.626$, (c) $+4.871$, (d) $+4.858$ MeV.

**Solution.** Balance $A$ and $Z$ separately.
(a) $A: 238+1=239$, $Z: 92+0=92$ → $^{239}_{92}\mathrm{U}$. This is radiative
capture, and its Q-value is $S_n(^{239}\mathrm{U})=4.806$ MeV (P4).
(b) $A: 14+1=15$, minus the proton's 1 → 14; $Z: 7+0=7$, minus 1 → 6. So
$^{14}_{6}\mathrm{C}$, and the reaction is $^{14}\mathrm{N}(n,p)^{14}\mathrm{C}$
with $Q=+0.626$ MeV. This is the reaction that manufactures atmospheric $^{14}$C
from cosmic-ray neutrons — the basis of radiocarbon dating (`~NE-07`).
(c) $A: 226-4=222$, $Z: 88-2=86$ → $^{222}_{86}\mathrm{Rn}$, $Q=+4.871$ MeV. Radium
decaying to radon, the step that puts a gas into the uranium chain and makes
radon a health problem (`~NE-18`).
(d) $A: 230+4=234$, $Z: 90+2=92$ → $^{234}_{92}\mathrm{U}$, $Q=+4.858$ MeV.

All four Q-values are positive, as they must be for decays that are observed to
happen spontaneously.

### P2.  The deuterium fusion channels  *(S&F Ch. 4, Prob. 5)*
Find the net energy released by (a) $^2\mathrm{H}+{}^2\mathrm{H}\to{}^3\mathrm{He}+n$
and (b) $^2\mathrm{H}+{}^3\mathrm{H}\to{}^4\mathrm{He}+n$.
*Check:* $+3.2689$ MeV and $+17.5893$ MeV.

**Solution.** (a) In atomic masses,
$$Q=[2(2.0141018)-3.0160293-1.0086649]\times931.494=+3.269\ \text{MeV}.$$
(b) $Q=[2.0141018+3.0160493-4.0026032-1.0086649]\times931.494=+17.589$ MeV.

The ratio is the point. D–T releases **5.4 times** more energy than D–D per
reaction, and it also has the largest cross section at accessible temperatures,
which is why every fusion reactor design burns D–T rather than pure deuterium
(`~NE-24`) — despite tritium being radioactive, scarce, and requiring breeding
from lithium (P3). The energy comes overwhelmingly from the tight binding of the
$^4$He product: $B/A=7.07$ MeV against 1.11 MeV for the deuteron (`~NE-03`).

### P3.  Breeding tritium
Compute $Q$ for $^{6}\mathrm{Li}(n,\alpha)^{3}\mathrm{H}$ and explain its role in
a fusion reactor.
*Check:* $Q=+4.7829$ MeV.

**Solution.**
$$Q=[6.0151223+1.0086649-4.0026032-3.0160493]\times931.494=+4.783\ \text{MeV}.$$
Exothermic, and driven by a *neutron*, so there is no Coulomb barrier — the
reaction proceeds readily at thermal energies (its cross section is 941 b, the
largest entry in `../data_tables/C1_thermal_neutron_cross_sections.csv`).

This closes the D–T fuel cycle. Each D–T fusion (P2) emits one 14.1 MeV neutron;
if that neutron is caught in a lithium blanket, it regenerates the tritium that
was burned, and releases a further 4.8 MeV as a bonus. Tritium has a 12.3 year
half-life and essentially no natural abundance, so a D–T reactor that did not
breed its own would have no fuel. The blanket is not an accessory to a fusion
reactor; it is part of the fuel cycle (`~NE-24`).

### P4.  Why $^{235}$U is fissile and $^{238}$U is not
Compute the $(n,\gamma)$ Q-values for $^{235}$U, $^{238}$U and $^{1}$H, and
compare the first two with the $\approx6.2$ MeV fission barrier of the compound
nucleus.
*Check:* $Q=6.5448$, $4.8062$ and $2.2246$ MeV.

**Solution.** For radiative capture the Q-value is the neutron separation energy
of the product,
$$Q=\big[M(^{A}\mathrm{X})+m_n-M(^{A+1}\mathrm{X})\big]c^{2}=S_n(^{A+1}\mathrm{X}).$$
Capturing a neutron on $^{235}$U forms $^{236}$U$^{*}$ with $6.545$ MeV of
excitation; on $^{238}$U it forms $^{239}$U$^{*}$ with only $4.806$ MeV.

The fission barrier of these compound nuclei is about 6.2 MeV. So a **zero-energy
thermal neutron** already excites $^{236}$U$^{*}$ above its barrier — $^{235}$U is
*fissile*. The same neutron leaves $^{239}$U$^{*}$ 1.4 MeV **short**, so $^{238}$U
requires a neutron with over an MeV of kinetic energy — it is merely
*fissionable*, and only by fast neutrons. That 1.7 MeV difference in $S_n$ is the
entire reason natural uranium must be enriched, and it traces back to pairing:
$^{236}$U has an even neutron number and gains the pairing energy, $^{239}$U has
an odd one and does not (`~NE-02`, `~NE-03`).

The third value is a useful landmark: $^{1}\mathrm{H}(n,\gamma)^{2}\mathrm{H}$
releases $2.2246$ MeV, the deuteron binding energy. That 2.22 MeV gamma is emitted
whenever a neutron is captured in water or any hydrogenous shield, and it is one
of the standard signatures in radiation detection (`~NE-15`).

### P5.  Getting the electrons right
Compute $Q$ for $^{16}\mathrm{O}(n,p)^{16}\mathrm{N}$ correctly, then again using
a bare proton mass, and account for the difference.
*Check:* $-9.6381$ MeV against $-9.1271$ MeV; the gap is $0.5110$ MeV.

**Solution.** With the neutral-atom substitution [S&F Eq. (4.25)],
$$Q=\big[m_n+M(^{16}\mathrm{O})-M(^{16}\mathrm{N})-M(^{1}\mathrm{H})\big]c^{2}=-9.638\ \text{MeV}.$$
Using $m_p$ in place of $M(^1\mathrm{H})$ removes one electron mass from the
product side, so $Q$ comes out **larger** by
$$m_ec^{2}=5.48580\times10^{-4}\times931.494=0.5110\ \text{MeV}.$$

The error is systematic, not random, and it is 5% of this Q-value. The reason is
that the left side has 8 bound electrons ($^{16}$O) and the right side only 7
($^{16}$N) plus a bare proton — one electron has vanished from the books. Writing
the freed electron explicitly and pairing it with the proton into a $^1$H atom
restores the balance, at the cost of an ignorable 13.6 eV of atomic binding.
The general rule: **replace every charged particle by its neutral atom**, then
subtract atomic masses.

### P6.  Excited products close reaction channels
For $^{9}\mathrm{Be}(\alpha,n)^{12}\mathrm{C}$, find $Q$ when $^{12}$C is left in
its 4.44 MeV first excited state and in the 7.65 MeV Hoyle state.
*Check:* $+1.2611$ MeV and $-1.9489$ MeV, against $+5.7011$ MeV to the ground state.

**Solution.** An excited nucleus is heavier by exactly its excitation energy, so
$Q^{*}=Q_{\text{gs}}-E^{*}$:
$$Q(4.44)=5.7011-4.44=+1.261\ \text{MeV},\qquad
Q(7.65)=5.7011-7.65=-1.949\ \text{MeV}.$$
The ground-state channel is exothermic and open at any alpha energy (above the
Coulomb barrier). The 4.44 MeV channel is still exothermic but yields a much
slower neutron. The 7.65 MeV channel is **endothermic** and simply closed unless
the incident alpha brings at least 1.95 MeV of extra energy.

Each excited state therefore opens at its own threshold, and a plot of neutron
yield against alpha energy shows a staircase, with a new step wherever another
level becomes accessible. That structure in measured cross sections is a direct
map of the product's level scheme (`~NE-13`). The 7.65 MeV Hoyle state, incidentally,
is the resonance that lets three alphas fuse into $^{12}$C in red giants and so
makes carbon-based chemistry possible (`~NE-10`).

### P7.  Exothermic is not the same as easy
Compute Coulomb barriers for d+d, p+p and α+α, and reconcile them with the
positive Q-values of P2.
*Check:* $0.476$, $0.600$ and $1.512$ MeV.

**Solution.** With $V_c=1.43996\,Z_1Z_2/R$ MeV and $R=1.2(A_1^{1/3}+A_2^{1/3})$ fm
(the nuclear-radius coefficient of S&F Eq. (1.7), which makes this the 1.20 MeV
form of S&F Eq. (6.19) — `~NE-08`):
$$V_c(dd)=\frac{1.43996(1)(1)}{1.2(1.26+1.26)}=0.476\ \text{MeV},$$
and similarly $0.600$ MeV for p+p and $1.512$ MeV for α+α.

So D–D fusion releases 3.27 MeV but the two deuterons must first be pushed to
within 3.0 fm of each other against 0.48 MeV of repulsion. In a thermal plasma
$kT=0.48$ MeV corresponds to $6\times10^{9}$ K — far above what any reactor
achieves. Fusion works at all only because (i) the Maxwellian has a high-energy
tail and (ii) the barrier is *tunnelled*, not climbed, giving the Gamow peak
(`~NE-10`). The lesson generalises: $Q>0$ tells you a reaction is energetically
allowed, and nothing about its rate. Rates need cross sections (`~NE-11`).

Neutron-induced reactions have $Z_1=0$ and therefore **no barrier at all**, which
is why P3 and P4 proceed at thermal energies while P2 needs $10^{8}$ K. That
asymmetry is the reason reactors are built around neutrons.

### P8.  Endothermic thresholds are larger than $|Q|$
For $^{16}\mathrm{O}(n,\alpha)^{13}\mathrm{C}$, state the naive threshold and
explain why the true one is higher.
*Check:* `threshold_energy_naive` returns $2.2156$ MeV $=|Q|$.

**Solution.** $Q=-2.216$ MeV, so at least $2.216$ MeV must be supplied — that is
what `threshold_energy_naive` returns, and it is a **lower bound only**.

The reason it is not the answer: momentum must also be conserved. In the
laboratory the incident neutron carries momentum, so the products cannot be
created at rest — they must retain the centre-of-mass motion, and that kinetic
energy is unavailable for the reaction. Only the energy in the centre-of-mass
frame counts, and for a projectile $x$ on a stationary target $X$,
$$E_{\text{th}}\simeq|Q|\left(1+\frac{m_x}{m_X}\right),$$
so here $E_{\text{th}}\approx2.216(1+1/16)=2.355$ MeV — about 6% higher.
The correction grows as the projectile approaches the target in mass, and it is
derived properly in `~NE-08`. Quoting $|Q|$ as a threshold is one of the standard
errors in this subject, which is why the function that returns it says `naive` in
its name.
