# NE-10 — Fusion and nucleosynthesis (notes)

`~NE-09` harvested the right-hand slope of the binding-energy curve by splitting
heavy nuclei. This module harvests the left-hand slope, which is **steeper**:
D–T releases 17.6 MeV from five nucleons, against fission's 200 MeV from 236.
Per nucleon that is 3.5 MeV against 0.85 — a factor of four — and per unit mass
the gap is wider still because deuterium and tritium are light.

So why is there a fission industry and no fusion one? Entirely because of the
Coulomb barrier of `~NE-08`. It is *small* — a few hundred keV against a 17.6 MeV
payoff, a 2% overhead. But it must be paid by **every reacting pair**, and there
is no way to hand it to individual pairs selectively. The only mechanism that
scales is heat, and heating a gas to the barrier means $10^9$ K, which nothing
confines. Fission has no such gate: the neutron walks in free.

The rest of the subject is the two ways out of that trap — tunnelling, which
lowers the required temperature by two orders of magnitude, and confinement,
which is where the engineering lives.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §6.7,
cited by **printed** page (PDF = printed + 23). Masses from
`../data_tables/B1_atomic_masses.csv`.

## 1. The candidate fuels

S&F list seven [printed p. 163]. Every Q-value here is recomputed from Appendix B
(`test_book_q_values`); the last is corrected — see `refs.md`.

| reaction | $Q$ (MeV) | $E_G$ (MeV) | $E_0$ at 10 keV |
|---|---|---|---|
| D + D → T + p | 4.03 | 0.98 | 29 keV |
| D + D → ³He + n | 3.27 | 0.98 | 29 keV |
| **D + T → ⁴He + n** | **17.59** | **1.18** | **31 keV** |
| D + ³He → ⁴He + p | 18.35 | 4.70 | 49 keV |
| T + T → ⁴He + 2n | 11.33 | 1.47 | 33 keV |
| p + ⁶Li → ⁴He + ³He | 4.02 | 7.55 | 57 keV |
| p + ¹¹B → 3α | 8.68 ‡ | 22.44 | 82 keV |

‡ S&F print 8.08; their own masses give 8.68.

Two columns decide everything. $Q$ says how much you get; the **Gamow energy**
$E_G$ of §3 says how hard it is, and it scales as $(Z_1Z_2)^2$ inside a square
root inside an exponential. D–T wins not because its $Q$ is largest — D–³He's is
— but because it has nearly the largest $Q$ at the smallest $E_G$.

D–T's cost is the tritium: 12.3 y half-life, no natural occurrence, so a reactor
must **breed its own** from lithium in a blanket [S&F p. 164]:
$$n+{}^{6}\text{Li}\to{}^{4}\text{He}+\text{T},\qquad Q=+4.78\ \text{MeV},$$
$$n+{}^{7}\text{Li}\to{}^{4}\text{He}+\text{T}+n,\qquad Q=-2.47\ \text{MeV}.$$
Note the second reaction returns the neutron: it is a **neutron multiplier**, and
without it a D–T reactor could not breed more than one triton per fusion — which
it must, because neutrons leak. The 14.05 MeV D–T neutron has ample energy for
the 2.5 MeV threshold, so the blanket does both jobs with the same particle.

## 2. Where the D–T energy goes

By the inverse-mass split of `~NE-08` and `~NE-09` [S&F Eq. (6.46)]:
$$\text{D}+\text{T}\to{}^{4}\text{He}\ (3.54\ \text{MeV})+n\ (14.05\ \text{MeV}).$$

The **20/80 split is the central engineering fact of fusion**. Only the charged
alpha stays confined by the magnetic field and heats the plasma; the neutron
leaves immediately. So a self-sustaining plasma — **ignition** — requires the
alpha's 3.5 MeV *alone* to balance every loss channel, while the neutron's 14 MeV
must simultaneously carry the useful heat, breed the tritium, and not destroy the
first wall doing it. Fission has no analogue of this constraint: all 168 MeV of
fragment energy is deposited in the fuel by construction. `~NE-24` is largely the
consequences.

## 3. Tunnelling, and the Gamow peak

Set the mean thermal energy $3kT/2$ equal to the Coulomb barrier and you get
$$T\simeq3\times10^{9}\ \text{K}\quad\text{for D–T},$$
two hundred times the sun's core temperature and thirty times any tokamak. If
fusion needed that, nothing would burn anywhere.

It does not, because the reactants **tunnel**. The barrier penetration
probability is
$$P\sim\exp\left(-\sqrt{E_G/E}\right),\qquad
E_G=2\mu c^2(\pi\alpha Z_1Z_2)^2,$$
the **Gamow energy** — `gamow_energy`. (This is beyond S&F, which asserts that
"the kinetic energy needed is typically a few keV to several hundred keV" without
deriving it; `refs.md` gives the sources.)

Now the competition. Low energies are abundant but tunnel poorly; high energies
tunnel well but are exponentially rare. The reaction rate is the product of a
falling Maxwellian and a rising Gamow factor, which is sharply peaked at the
**Gamow energy**
$$\boxed{\;E_0=\left[\frac{E_G(kT)^2}{4}\right]^{1/3}\;}$$
— `gamow_peak_energy`, with width $\Delta=(4/\sqrt3)\sqrt{E_0kT}$.

For D–T at $kT=10$ keV, $E_0=31$ keV: **three times the mean thermal energy, but
a tenth of the barrier**. That factor of ten in energy — a hundred in temperature
— is the entire reason fusion is achievable. Essentially all fusion in the
universe is done by the small fraction of particles in the Maxwellian tail that
happen to sit in this window.

Two consequences worth carrying:

- **Rates are ferociously temperature-sensitive.** Doubling D–T energy from 10 to
  20 keV raises the tunnelling probability 24-fold. Fusion power is a threshold
  phenomenon, not a gradient, and ignition is a cliff.
- **Charge is punished quadratically.** $E_G(\text{p–}^{11}\text{B})=22.4$ MeV
  against D–T's 1.18. At the same energy, p–¹¹B is $10^{16}$ times less likely to
  tunnel. This is why aneutronic fusion — which would avoid the neutron problems
  of §2 entirely — remains so much harder despite a perfectly good $Q$-value.

## 4. Confinement: three ways, one of which works

**Gravitational** [S&F p. 164]. Stars. The sun's core sits at 15 MK and
$4\times10^{16}$ Pa. Perfect confinement, free, and permanent — but not
available on a bench.

**Magnetic** [S&F pp. 164–165]. A plasma is charged, so fields can hold it.
Densities are tenuous ($\sim10^{15}$ cm⁻³, a millionth of atmospheric), the
plasma is notoriously unstable, and the confining magnetic pressure needed
exceeds $10^{5}$ atm for a 10 keV plasma at atmospheric density. The chamber wall
must simultaneously survive the alpha heat load and stop 14 MeV neutrons.

**Inertial** [S&F p. 165]. Compress a pellet with laser pulses faster than it can
fly apart. Also the principle of thermonuclear weapons, where a fission primary
does the compressing. (S&F, writing before 2022, state that break-even "has yet
to be achieved"; the National Ignition Facility reached target gain > 1 in
December 2022 — see `refs.md`.)

## 5. How stars actually do it

The sun runs the **proton–proton chain** [S&F §6.7.2, p. 166]:
$$p+p\to\text{D}+\beta^++\nu,\qquad Q=0.42\ \text{MeV}$$
$$\text{D}+p\to{}^{3}\text{He}+\gamma,\qquad Q=5.49\ \text{MeV}$$
$$^{3}\text{He}+{}^{3}\text{He}\to{}^{4}\text{He}+2p,\qquad Q=12.86\ \text{MeV}$$
netting [S&F Eq. (6.47)]
$$4({}^{1}\text{H})\to{}^{4}\text{He}+2\gamma+2\beta^++2\nu,\qquad Q=26.72\ \text{MeV}.$$

**Two traps here, both worth the attention.**

The first is the $\beta^+$ correction of `~NE-05`. The p–p step computed from
bare neutral-atom masses gives 1.442 MeV; the correct value is
$1.442-2m_ec^2=0.420$ MeV. Stellar hydrogen burning is full of $\beta^+$ steps,
so this is not a corner case.

The second is subtler: **S&F use two different conventions in the same
paragraph.** Summing the three steps' (corrected) $Q$-values gives 24.69 MeV of
*nuclear* energy. But Eq. (6.47) quotes 26.72 MeV — which is the neutral-atom
difference $4M(^1\text{H})-M(^4\text{He})$, and includes the $4m_ec^2=2.044$ MeV
released when the two positrons annihilate. Both numbers are right; they answer
different questions, and they differ by 8%. For a star the larger one is the
relevant one, because the positrons annihilate instantly. (About 0.6 MeV then
leaves in the neutrinos and never thermalises — the solar neutrino flux, which is
how we know any of this is true.)

The rate-limiting step is the first, and it is **absurd**. $p+p\to$ D requires a
proton to become a neutron, so it runs on the **weak force**: about one proton in
$10^{18}$ fuses per second, a mean proton lifetime in the core of
$3\times10^{10}$ y — longer than the age of the universe. It has never been
measured in a laboratory. This bottleneck is why stars last billions of years
rather than exploding, and it is why the sun's core power density is
$$\frac{4\times10^{26}\ \text{W}}{0.001\times V_\odot}=283\ \text{W/m}^3,$$
**less than a compost heap**. The sun is bright because it is enormous. Anyone
reasoning from "if the sun can do it" to "fusion should be easy" has the argument
exactly backwards: a reactor must beat the sun's power density by five orders of
magnitude, because it cannot be the size of the sun.

In hotter stars with some carbon present, the **CNO cycle** [S&F Eq. (6.48)]
does the same job catalytically — ¹²C in the first step, ¹²C out of the last —
with the identical net $Q$ of 26.72 MeV, since both routes just turn four protons
into helium. `test_cno_cycle_is_catalytic_and_equivalent` checks that the six
steps sum correctly and that carbon is conserved.

## 6. Building the elements, and where it stops

Once the core hydrogen is spent, gravity contracts it, the temperature rises, and
helium burning starts [S&F p. 168]. The first step is famously *not* two alphas
sticking together, because **⁸Be is unbound**: $^4$He + $^4$He is endoergic by
92 keV and ⁸Be falls apart in $7\times10^{-17}$ s. The way past the $A=8$ gap is
a three-body process, catching the fleeting ⁸Be with a third alpha:
$$3({}^{4}\text{He})\to{}^{12}\text{C},\qquad Q=7.27\ \text{MeV},$$
after which alpha capture proceeds up the ladder: ¹²C→¹⁶O (7.16), ¹⁶O→²⁰Ne (4.73),
²⁰Ne→²⁴Mg (9.31). In massive stars, carbon and oxygen burn directly
[S&F p. 169]: ¹²C+¹²C→²⁰Ne+α (4.62) or ²³Na+p (2.24); ¹⁶O+¹⁶O→²⁸Si+α (9.59) or
³¹P+p (7.68). The star acquires an onion structure, and each successive stage is
dramatically faster than the last.

Then it stops at iron — but **not for the reason usually given**. It is often
said that fusion "becomes endoergic past iron". Alpha capture does not:
$^{56}$Ni + α → $^{60}$Zn still releases 2.7 MeV, because the alpha's own $B/A$
is only 7.07 and adding four nucleons at ~8.7 more than pays for it. What
actually happens is three things at once:

1. **The yield collapses.** Alpha capture releases ~8 MeV per step all the way to
   ⁵⁶Ni and then 2.7 MeV — a factor of three, exactly at the peak. The star gains
   almost nothing per gram and can no longer hold off gravity.
2. **Symmetric fusion does go endoergic.** ²⁸Si+²⁸Si→⁵⁶Ni releases 10.9 MeV;
   ⁵⁶Fe+⁵⁶Fe→¹¹²Cd *costs* 30.6 MeV.
3. **Photodisintegration reverses the ladder.** At $10^{10}$ K, $kT\simeq0.86$ MeV
   and the Planck tail reaches the 7.6 MeV alpha separation energy of ⁵⁶Fe. The
   very photons the fusion produced start knocking the nuclei back apart.

(The peak of $B/A$ is at **⁶²Ni**, 8.7945 MeV/nucleon, not ⁵⁶Fe at 8.7902 —
the same result `~NE-03` found. ⁵⁶Fe is the most *abundant* iron-peak nuclide
because it descends from ⁵⁶Ni, not the most bound.)

With no energy source, the core collapses. Below 1.44 solar masses — the
**Chandrasekhar limit** — electron degeneracy pressure catches it and a white
dwarf results. A white dwarf accreting from a binary companion past that limit
detonates as a **Type Ia supernova**, releasing $1$–$2\times10^{44}$ J, its
light curve powered by $^{56}\text{Ni}\to{}^{56}\text{Co}\to{}^{56}\text{Fe}$
(6.08 d, 77.2 d — pure `~NE-07` decay kinetics, visible across a galaxy). Above
that, a **Type II supernova**: the core collapses at 15% of light speed, electrons
are forced into protons, and $10^{46}$ J leaves in a ten-second neutrino burst
— more energy than the sun will radiate in its entire life, in ten seconds. Above
about 15 solar masses, not even neutron degeneracy holds and a black hole forms
directly.

## 7. Nucleosynthesis: everything above iron

Since fusion cannot pass the iron peak, the heavy elements are built by **neutron
capture followed by beta decay** [S&F §6.7.3, pp. 172–173]. Neutrons face no
barrier (`~NE-08`), so this route has no Gamow problem at all. Two regimes,
distinguished by which rate is faster:

- **s-process** (slow): capture rate ≪ beta-decay rate. The path hugs the
  stability valley, one neutron at a time, waiting for each beta decay. It runs
  during helium burning, on the small neutron flux from reactions like
  ¹³C(α,n)¹⁶O — and it needs pre-existing iron, so it can only happen in stars
  built from the ashes of earlier ones.
- **r-process** (rapid): capture rate ≫ beta-decay rate. Nuclei absorb many
  neutrons before decaying at all, run far out to the neutron drip line, and then
  cascade back by a long chain of $\beta^-$ decays. It needs the enormous neutron
  flux of a core-collapse supernova (and, we now know, neutron-star mergers).

The fingerprints are visible in the abundance curve: the two processes leave
peaks at *different* mass numbers near the neutron magic numbers, because the
s-process peaks at the magic $N$ of stable nuclei and the r-process peaks at the
magic $N$ of very neutron-rich ones, which decay back to *lower* $A$. Both
signatures appear in solar-system abundances, so both processes contributed. And
some proton-rich stable heavy nuclides cannot be made either way — they are
observed to be correspondingly rare.

The uranium in `~NE-09`'s reactor was made in a supernova. Fission is, at one
remove, stored fusion energy.

## 8. The scale of the fuel supply

Deuterium is 0.015% of hydrogen, and burning it fully to ⁴He gives 23.85 MeV per
pair, i.e. **11.9 MeV per deuteron** [S&F Example 6.6]. So:

| | deuterium energy |
|---|---|
| an 8 oz glass of water | $4.5\times10^{9}$ J = 5 days of a 10 kW house |
| the oceans ($1.4\times10^{43}$ D atoms) | $2.7\times10^{31}$ J ≈ 50 billion years of world use |

The fuel is not the problem and never has been. The problem is entirely §3 and
§4: a few hundred keV of Coulomb barrier, and the fact that the only confinement
scheme known to work is to be the size of a star.

## Where this goes

- `~NE-24` — fusion reactors: the Lawson criterion and the triple product are §3
  and §4 made quantitative; the 20/80 split of §2 defines ignition.
- `~NE-13` — the cross sections that turn the Gamow peak into an actual reaction
  rate $\langle\sigma v\rangle$.
- `~NE-14` — the alpha's 3.5 MeV is deposited by the stopping-power physics that
  decides whether it heats the plasma before it leaves.
- `~NE-03` — the binding-energy curve whose two slopes are fission and fusion,
  and whose peak at ⁶²Ni is where §6 stops.
- `~NE-07` — the ⁵⁶Ni→⁵⁶Co→⁵⁶Fe chain that lights a Type Ia supernova is a
  two-step Bateman problem.
- `~NE-09` — the other side of the curve, and the uranium that §7 made.
