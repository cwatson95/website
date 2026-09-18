# NE-09 — Problems

Work each by hand, then check with `code/fission.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6 follow the book's
Chapter 6 problems 16–21 (printed 176–177); P7–P8 are added. Masses from
`../data_tables/B1_atomic_masses.csv`.

### P1.  A milligram of californium  *(S&F Ch. 6, Prob. 16)*
How many neutrons per second are emitted spontaneously by 1 mg of $^{252}$Cf?
*Check:* $2.30\times10^{9}$ n/s, from $6.17\times10^{8}$ fissions/s.

**Solution.** Straight from Table 6.2's last column:
$$2.3\times10^{12}\ \frac{\text{n}}{\text{g·s}}\times10^{-3}\ \text{g}
=\boxed{2.30\times10^{9}\ \text{n/s}}.$$

It is worth rebuilding that column rather than quoting it, because doing so
checks the row. With $T_{1/2}=2.638$ y,
$$\lambda=\frac{\ln2}{2.638\times3.156\times10^{7}}=8.33\times10^{-9}\ \text{s}^{-1},$$
so 1 mg ($2.39\times10^{18}$ atoms) undergoes $1.99\times10^{10}$ decays/s. Only
3.09% of those are fissions — the rest are alphas — giving
$6.15\times10^{8}$ fissions/s, and at $\nu=3.73$ neutrons each,
$2.29\times10^{9}$ n/s. The tabulated value is recovered to 0.4%.

Two things make ²⁵²Cf the standard portable neutron source: a large $\nu$ (3.73,
the highest in common use) and a half-life short enough for a high specific
activity but long enough to be a usable product. A 10 μg source — a speck —
emits over $2\times10^{7}$ n/s, enough for well logging, moisture gauges and
neutron radiography, with no accelerator and no reactor.

### P2.  Finding the partner fragment  *(S&F Ch. 6, Prob. 17)*
A $^{235}$U fission gives 4 prompt neutrons and one fragment of $^{121}$Ag.
(a) What is the other fragment? (b) How much energy is liberated promptly?
(c) If the fragments share 150 MeV, how much does each get? (d) What is left for
the four neutrons?
*Check:* (a) $^{111}$Rh; (b) 173.7 MeV; (c) 78.2 and 71.8 MeV; (d) 23.7 MeV.

**Solution.** (a) Eq. (6.34):
$$A_H=236-121-4=111,\qquad Z_H=92-47=45,$$
so the partner is $^{111}_{45}$Rh.

(b) The mass deficit, with `prompt_energy_release`:
$$E_p=\left[M(^{235}\text{U})+m_n-M(^{121}\text{Ag})-M(^{111}\text{Rh})-4m_n\right]c^2
=173.7\ \text{MeV}.$$
Note this is below the 200 MeV average, and the reason is visible in the mass
numbers: 121 and 111 is a nearly **symmetric** split, and symmetric splits are
both rare (0.01% versus 6.5%, §2 of the notes) and less energetic, because
neither fragment lands on the doubly-magic-adjacent shell structure near $A=132$
that makes the asymmetric split favourable.

(c) By Eq. (6.41) the energies go inversely as the masses:
$$E(^{111}\text{Rh})=150\times\frac{120.92}{231.83}=78.2\ \text{MeV},\qquad
E(^{121}\text{Ag})=150\times\frac{110.91}{231.83}=71.8\ \text{MeV}.$$
The lighter fragment takes more, as always.

(d) $173.7-150=23.7$ MeV shared by four neutrons, about 5.9 MeV each — well
above the 2 MeV average of §4, which is consistent: a fission that emits four
neutrons rather than the usual two or three left its fragments unusually
excited.

### P3.  A fission taken all the way to stability  *(S&F Ch. 6, Prob. 18)*
For $^{235}\text{U}(n,f)\to{}^{90}\text{Kr}+{}^{142}\text{Ba}+4n+6\gamma$:
(a) give the two fission-product chains, (b) the equivalent reaction to stable
end products, (c) the prompt energy, (d) the total eventually emitted.
*Check:* (c) 169.5 MeV; (d) 190.0 MeV.

**Solution.** (a) Both fragments are neutron-rich and beta-decay at constant $A$:
$$^{90}\text{Kr}\to{}^{90}\text{Rb}\to{}^{90}\text{Sr}\to{}^{90}\text{Y}
\to{}^{90}\text{Zr (stable)},$$
$$^{142}\text{Ba}\to{}^{142}\text{La}\to{}^{142}\text{Ce (stable)}.$$
Four decays and two decays, six in all — one per unit of $Z$ gained.

(b) $$^{235}\text{U}+n\longrightarrow{}^{90}\text{Zr}+{}^{142}\text{Ce}
+4n+6\beta^-+6\bar\nu+\gamma\text{'s}.$$

(c) `prompt_energy_release` gives $E_p=169.5$ MeV.

(d) `delayed_energy_release` on the two chains gives
$$E_d=\left[M(^{90}\text{Kr})+M(^{142}\text{Ba})-M(^{90}\text{Zr})-M(^{142}\text{Ce})\right]c^2
=20.5\ \text{MeV},$$
for a total of **190.0 MeV**. The six emitted electrons need no correction: six
ambient electrons are absorbed to keep the atoms neutral, and neutral-atom masses
already account for both.

The 190 MeV includes roughly 10 MeV that leaves in the six antineutrinos and is
never recoverable, so this fission is worth about 180 MeV of heat — a little
under Table 6.5's 201 MeV average, which is what you would expect from a split
that emits four neutrons instead of 2.4 and therefore locks up more energy in
neutron kinetic energy and neutron rest mass.

Note also that this chain passes through **⁹⁰Sr** (28.79 y) — one of the two
fission products, with ¹³⁷Cs, that dominate spent-fuel activity from a year to a
century out (`~NE-07`, `~NE-23`).

### P4.  Technetium from a 10-gram sample  *(S&F Ch. 6, Prob. 19)*
A 10 g sample of $^{235}$U in a reactor generates 100 W of thermal fission power.
(a) What is the fission rate? (b) After a year, estimate the number of $^{99}$Tc
atoms produced through the chain of Eq. (6.37), assuming everything above $^{99}$Tc
decays immediately.
*Check:* (a) $3.12\times10^{12}$ fissions/s; (b) $\sim6\times10^{18}$ atoms.

**Solution.** (a) At 200 MeV recoverable per fission,
$$\dot{N}_f=\frac{100\ \text{J/s}}{200\times1.602\times10^{-13}\ \text{J}}
=3.12\times10^{12}\ \text{fissions/s},$$
which is `fissions_per_second(100.0)`. The 10 g is a red herring for part (a) —
the fission rate is fixed by the power, not by how much fuel is present. (It
matters for whether 100 W is *sustainable*: 10 g of ²³⁵U holds
$2.56\times10^{22}$ atoms, so a year at this rate consumes 0.4% of it.)

(b) In a year, $3.12\times10^{12}\times3.156\times10^{7}=9.85\times10^{19}$
fissions. The $A=99$ chain yield is about 6.1%, so
$$N(^{99}\text{Tc})\simeq0.061\times9.85\times10^{19}
=\boxed{6.0\times10^{18}\ \text{atoms}}.$$
Everything above ⁹⁹Tc in Eq. (6.37) has a half-life of days or less against a
one-year irradiation, so it has all funnelled down; ⁹⁹Tc itself has $T_{1/2}=0.21$
My, so essentially none of it has decayed. That combination — a fast feed into a
long-lived sink — is exactly the "decay with production reaching saturation"
problem of `~NE-07`, in the limit where the product's half-life vastly exceeds
the irradiation.

⁹⁹Tc is one of the more troublesome long-lived fission products for waste
disposal: soluble and mobile as pertechnetate in oxidising groundwater
(`~NE-23`).

### P5.  A light bulb, in uranium and in coal  *(S&F Ch. 6, Prob. 20)*
(a) How much $^{235}$U is consumed per year to run a 100 W bulb continuously?
(b) How much coal (12 GJ/tonne)? Assume 33% thermal-to-electric efficiency.
*Check:* (a) 0.137 g/y; (b) 0.80 tonnes/y.

**Solution.** At 33% efficiency, 100 W of electricity needs 303 W of thermal
power, i.e. $303\times3.156\times10^{7}=9.56\times10^{9}$ J = 9.56 GJ per year,
which is $1.107\times10^{-4}$ MWd/s... more usefully, 0.1107 MWd.

(a) At 1.24 g of ²³⁵U consumed per MWd,
$$m=0.1107\ \text{MWd}\times1.24\ \frac{\text{g}}{\text{MWd}}
=\boxed{0.137\ \text{g/y}}.$$
Of that, 0.117 g actually fissions and 0.021 g is lost to $(n,\gamma)$ capture
into ²³⁶U — a 15% tax that is invisible in the energy balance but shows up
directly in fuel-cycle costs (`~NE-23`).

(b) $$m_{\text{coal}}=\frac{9.56\ \text{GJ}}{12\ \text{GJ/tonne}}
=\boxed{0.80\ \text{tonnes/y}}.$$

The ratio is about **5.8 million**. One way to feel it: the uranium for a
lifetime of one light bulb fits on a fingertip; the coal fills a small truck, and
turns into about 2 tonnes of CO₂. The comparison is the reason the field exists,
and it is also incomplete — it says nothing about mining, enrichment, capital
cost, or what to do with the ⁹⁹Tc of P4.

### P6.  A criticality accident, three months later  *(S&F Ch. 6, Prob. 21)*
An accidental criticality releases energy equivalent to 7 kg of TNT
(4.6 kJ/g); 80% of the fission products stay in the building. (a) How many
fissions occurred? (b) Three months later, at what rate do the retained fission
products release energy?
*Check:* (a) $1.0\times10^{18}$ fissions; (b) ~2 mW by extrapolation — **but see
the caution**.

**Solution.** (a) $7000\ \text{g}\times4.6\ \text{kJ/g}=32.2$ MJ, so
$$N_f=\frac{3.22\times10^{7}\ \text{J}}{200\times1.602\times10^{-13}\ \text{J}}
=\boxed{1.0\times10^{18}\ \text{fissions}}.$$
For scale, that is about 0.4 mg of uranium fissioned — the accident's hazard is
overwhelmingly the prompt radiation dose and the fission-product inventory, not
the 32 MJ of blast.

(b) Three months is $7.78\times10^{6}$ s. Eqs. (6.44)–(6.45) give
$$F(t)=2.66\,t^{-1.2}\ \frac{\text{MeV}}{\text{s·fission}}
\;\Rightarrow\;
P=0.8\times1.0\times10^{18}\times2.66\times(7.78\times10^{6})^{-1.2}
\simeq2\ \text{mW}.$$

**The caution:** S&F state Eqs. (6.44)–(6.45) as valid for
$10\ \text{s}<t<10^{5}$ s. Three months is $7.8\times10^{6}$ s — nearly **two
decades beyond** the stated range, and the answer should be quoted as an
extrapolation, not a result. The real curve flattens relative to $t^{-1.2}$ at
long times as the short-lived chains exhaust and the surviving inventory becomes
dominated by a handful of specific nuclides (⁹⁰Sr, ¹³⁷Cs and their daughters),
so the true power is *higher* than the extrapolation. `decay_heat_total` does
not police the range — the formula is the book's, and silently clamping it would
hide exactly this issue — so the caller must.

For comparison, the same formula inside its valid range:

| $t$ | power (retained) |
|---|---|
| 1 h | 18.5 W |
| 1 d | 0.41 W |
| 3 months | 2 mW (extrapolated) |

### P7.  Why the pairing term decides everything  *(added)*
Show that the fissile/fissionable split is a parity effect, and estimate the size
of the gap from the SEMF pairing term alone.
*Check:* the SEMF gives $\sim2\delta/\sqrt{A}\simeq1.4$ MeV; the measured gap
between the two groups is 1.07 MeV.

**Solution.** For a target with $N$ neutrons, absorbing one makes a compound
nucleus with $N+1$. The pairing term of `~NE-02` contributes $-a_p/\sqrt{A}$ to
the binding energy with $a_p=+11.2$ MeV for odd–odd, $0$ for odd–even and
$-11.2$ MeV for even–even.

Take ²³⁵U ($Z=92$ even, $N=143$ odd — an odd-$A$, odd-$N$ target). Absorbing a
neutron gives ²³⁶U with $N=144$: **even–even**, the most tightly bound parity
class. Take ²³⁸U ($N=146$ even) instead: absorbing a neutron gives ²³⁹U with
$N=147$, **even–odd**. The compound nucleus in the first case gains the pairing
bonus and in the second does not, so
$$\Delta S_n\simeq\frac{2a_p}{\sqrt{A}}\simeq\frac{2\times11.2}{\sqrt{236}}
=1.46\ \text{MeV}.$$

Measured, from `excitation_energy`:
$$S_n(^{236}\text{U})-S_n(^{239}\text{U})=6.545-4.806=1.74\ \text{MeV},$$
and across the whole set the *lowest* fissile value (²⁴¹Pu, 6.31) exceeds the
*highest* fissionable one (²⁴⁰Pu, 5.24) by 1.07 MeV — a clean gap with no
overlap, which `test_fissile_and_fissionable_split_on_the_pairing_term` asserts.

So the reason a reactor runs on the 0.72% of natural uranium that is ²³⁵U rather
than the 99.27% that is ²³⁸U is one term in a 1935 semi-empirical mass formula.
It is also why the fertile chains of §1 work: two beta decays convert an even-$N$
nucleus into an odd-$N$ one, moving it across the same divide.

### P8.  Why a reactor is controllable  *(added)*
A reactor is critical with $k=1$. Compare the response time when the chain is
sustained by prompt neutrons alone against one sustained with the delayed
contribution, using $\beta=0.0065$ for $^{235}$U.
*Check:* prompt lifetime $\sim10^{-4}$ s; effective lifetime with delayed
neutrons $\sim0.08$ s — a factor of ~800.

**Solution.** In a thermal reactor a prompt neutron lives about
$\ell\simeq10^{-4}$ s between birth and its next absorption. A delayed neutron
appears only when its precursor decays, with a mean life of order $\tau_d\simeq12$ s
averaged over the precursor groups. The mean generation time is the weighted
average
$$\bar\ell=(1-\beta)\ell+\beta\,\tau_d
=0.9935\times10^{-4}+0.0065\times12\simeq0.078\ \text{s}.$$

Two-thirds of a percent of the neutrons stretch the generation time by a factor
of nearly a thousand. A reactivity insertion that would double the population in
milliseconds on prompt neutrons alone instead does so over many seconds —
comfortably within the reach of control rods, feedback and operators.

The corollary is the definition of the danger line. If reactivity exceeds
$\rho=\beta$, the chain is critical **on prompt neutrons alone**: the delayed
neutrons stop mattering and the period collapses to $\ell$. That state is called
prompt criticality, it is what SL-1 and Chernobyl reached, and it is why
reactivity is universally quoted in units of dollars, $\$=\rho/\beta$, with
$\$1$ the prompt-critical threshold. Because ²³⁹Pu's $\beta$ is 0.0021, a
plutonium-fuelled core has less than a third of the margin — the same physical
reactivity buys three times as many dollars. The full treatment is `~NE-20`.
