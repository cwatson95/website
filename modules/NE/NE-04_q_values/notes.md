# NE-04 — Nuclear reactions and Q-values (notes)

`~NE-03` computed the energy stored in a single nucleus. This module computes the
energy released or absorbed when nuclei rearrange — the Q-value, which is the
single most-used quantity in the rest of the trunk. Fission energy (`~NE-09`),
fusion energy (`~NE-10`), decay energies (`~NE-05`), reaction thresholds
(`~NE-08`) and reactor heat (`~NE-22`) are all Q-values.

The physics is one line. The bookkeeping is where people get hurt, and most of
this module is about the bookkeeping.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§4.4–4.8, cited by **printed** page (PDF = printed + 23). Masses from
`../data_tables/B1_atomic_masses.csv`.

## 1. Definition

Total energy is conserved across a reaction, rest mass included
[S&F Eq. (4.16), p. 90]:
$$\sum_i\big[E_i+m_ic^{2}\big]=\sum_i\big[E_i'+m_i'c^{2}\big],$$
with $E$ kinetic and $m$ rest mass. Define [S&F Eq. (4.17)]
$$Q\equiv(\text{KE of products})-(\text{KE of reactants}),$$
and Eq. (4.16) immediately gives the form that is actually used
[S&F Eq. (4.18), p. 91]:
$$\boxed{\;Q=\big[\textstyle\sum(\text{reactant rest masses})
-\sum(\text{product rest masses})\big]c^{2}\;}$$
— `q_value(reactants, products)`. For the binary reaction $x+X\to Y+y$
[S&F Eq. (4.19)]
$$Q=(E_y+E_Y)-(E_x+E_X)=\big[(m_x+m_X)-(m_y+m_Y)\big]c^{2}.$$

- $Q>0$ — **exothermic**: rest mass becomes kinetic energy. The reaction is
  energetically allowed at any incident energy.
- $Q<0$ — **endothermic**: kinetic energy becomes rest mass. Nothing happens
  below a threshold.

Note what $Q$ does *not* say. It is a statement about energetics only: it tells
you nothing about whether the reaction actually proceeds at a useful rate. That
depends on the Coulomb barrier (§5) and on the cross section (`~NE-11`).

## 2. The electron bookkeeping trap

Appendix B tabulates **atomic** masses — nucleus plus $Z$ electrons. Subtracting
them naively works only if the number of bound electrons balances, and it often
does not. S&F's example [printed p. 92] is ${}^{16}\mathrm{O}(n,p){}^{16}\mathrm{N}$:
$$n+{}^{16}_{\ 8}\mathrm{O}\longrightarrow{}^{16}_{\ 7}\mathrm{N}+p .$$
Writing $Q=[m_n+M({}^{16}\mathrm{O})-M({}^{16}\mathrm{N})-m_p]c^{2}$ is **wrong**:
the left side carries 8 bound electrons, the right side only 7 (plus a bare
proton). Charge is conserved, but an electron has gone missing from the
accounting. Written honestly [S&F Eq. (4.23)],
$$n+{}^{16}_{\ 8}\mathrm{O}\longrightarrow{}^{16}_{\ 7}\mathrm{N}+{}^{0}_{-1}e+p,$$
and the freed electron can be combined with the proton — its 13.6 eV binding
being negligible — into a neutral ${}^{1}_{1}\mathrm{H}$ atom [S&F Eq. (4.24)]:
$$n+{}^{16}_{\ 8}\mathrm{O}\longrightarrow{}^{16}_{\ 7}\mathrm{N}+{}^{1}_{1}\mathrm{H},
\qquad
Q=\big[m_n+M({}^{16}\mathrm{O})-M({}^{16}\mathrm{N})-M({}^{1}\mathrm{H})\big]c^{2}.$$

> **The rule** [S&F p. 92]: *in any nuclear reaction in which the numbers of
> neutrons and protons are conserved, replace every charged particle by its
> neutral-atom counterpart.* Then atomic masses may be subtracted directly.

The cost of getting it wrong is exactly one electron mass, $0.511$ MeV:
$-9.638$ MeV done right against $-9.127$ MeV done wrong
(`test_charge_conservation_trap`). Half an MeV is not a rounding error when
reaction Q-values are a few MeV.

`PARTICLES` encodes the substitution — `p`→¹H, `d`→²H, `t`→³H, `h`→³He,
`a`→⁴He, with `n` a bare neutron and `g` massless — and `check_conservation`
refuses any reaction whose $A$ and $Z$ do not balance before a Q-value is
computed at all.

**Beta decay breaks even this rule**, because there the proton number changes
without a corresponding free charged particle in the same sense. That is why
`~NE-05` treats $\beta^-$, $\beta^+$ and electron capture separately, with three
different electron-mass corrections.

## 3. Worked examples

S&F Example 4.4 [printed p. 92] does one of each sign. In neutral-atom form:

$${}^{9}_{4}\mathrm{Be}+{}^{4}_{2}\mathrm{He}\to{}^{12}_{\ 6}\mathrm{C}+{}^{1}_{0}n$$

| | atomic mass (u) |
|---|---|
| ⁹Be | 9.012182 |
| ⁴He | 4.002603 |
| **reactants** | **13.014785** |
| ¹²C | 12.000000 |
| n | 1.008664 |
| **products** | **13.008664** |

$Q=(13.014785-13.008664)\times931.494=+5.70$ MeV — exothermic, and historically
the reaction with which Chadwick discovered the neutron. The other,
${}^{16}\mathrm{O}(n,\alpha){}^{13}\mathrm{C}$, gives $-2.22$ MeV — endothermic.
`q_value_reaction("9Be(a,n)12C")` and `q_value_reaction("16O(n,a)13C")`
reproduce both.

Two more, from the book's Ch. 4 Prob. 5 — the deuterium fusion channels:
$$ {}^{2}\mathrm{H}+{}^{2}\mathrm{H}\to{}^{3}\mathrm{He}+n,\quad Q=+3.269\ \text{MeV},$$
$$ {}^{2}\mathrm{H}+{}^{3}\mathrm{H}\to{}^{4}\mathrm{He}+n,\quad Q=+17.589\ \text{MeV}.$$
The second is the D–T reaction that every fusion programme targets (`~NE-24`),
and its 17.6 MeV is the largest Q of any light-ion fusion reaction — because the
product ⁴He is exceptionally tightly bound (`~NE-03`).

## 4. Q from binding energies, and why it is the same thing

Since a mass is nucleon masses minus binding energy, and nucleons are conserved,
the nucleon terms cancel and
$$Q=\sum BE(\text{products})-\sum BE(\text{reactants}),$$
`q_from_binding_energies`. This agrees with the mass route to machine precision
(`test_q_from_masses_equals_q_from_binding_energies`) and is the form that makes
`~NE-03`'s $B/A$ curve the *driver* of nuclear energetics: a reaction releases
energy exactly when it moves nucleons to more tightly bound configurations.

Two structural consequences follow immediately, both tested:

- **$Q$ is antisymmetric.** Running a reaction backwards flips its sign, so an
  exothermic reaction and its inverse endothermic one have thresholds related by
  $|Q|$.
- **$Q$ is additive.** It depends only on the endpoints, so a two-step route sums
  to the one-step value:
  $$2\text{H}+2\text{H}\to{}^{3}\text{H}+p,\qquad
  2\text{H}+{}^{3}\text{H}\to{}^{4}\text{He}+n$$
  net to $3\times{}^{2}\text{H}\to{}^{4}\text{He}+n+p$, and
  $4.033+17.589=21.622$ MeV is exactly the one-step answer
  (`test_q_values_are_additive_along_a_chain`). This is why fusion chains can be
  bookkept by endpoints alone (`~NE-10`).

A special case worth naming: for radiative capture $(n,\gamma)$, the Q-value
*is* the neutron separation energy of the product,
$$Q\big[{}^{A-1}\mathrm{X}(n,\gamma){}^{A}\mathrm{X}\big]=S_n({}^{A}\mathrm{X}),$$
(`test_neutron_capture_q_equals_separation_energy`). Capture is therefore always
exothermic, and the released energy is what excites the compound nucleus —
the starting point of `~NE-13` and, for ²³⁵U, the reason thermal neutrons can
induce fission at all (`~NE-09`).

## 5. Excited products, thresholds, and barriers

**Excited products** [S&F §4.8, p. 93]. A nucleus left in an excited state is
heavier than its ground state by exactly the excitation energy, so
$$Q^{*}=Q_{\text{gs}}-E^{*},$$
`q_value_excited`. For ⁹Be(α,n)¹²C, leaving ¹²C in its 4.44 MeV first excited
state drops $Q$ from $+5.70$ to $+1.26$ MeV; the 7.65 MeV Hoyle state turns the
reaction endothermic at $-1.95$ MeV. Every such state opens a separate reaction
channel with its own threshold, which is why measured cross sections have
staircase structure (`~NE-13`).

**Thresholds.** For $Q<0$ the reaction needs incident kinetic energy, and
$|Q|$ is the obvious lower bound — `threshold_energy_naive`. But it is only a
bound: momentum conservation forces the products to carry off kinetic energy in
the centre of mass, so the true threshold is *larger*, by a factor of roughly
$(1+m_x/m_X)$. `~NE-08` derives it properly. The naive value is provided here
deliberately labelled as naive, because using it is a standard error.

**Barriers.** $Q>0$ does not mean "easy". A charged projectile must first get
close enough to the target for the nuclear force to act, against Coulomb
repulsion. `coulomb_barrier_mev` estimates
$$V_c=\frac{Z_1Z_2e^{2}}{4\pi\epsilon_0R},\qquad
R=r_0\big(A_1^{1/3}+A_2^{1/3}\big),\quad
\frac{e^{2}}{4\pi\epsilon_0}=1.43996\ \text{MeV\,fm},$$
with $r_0=1.2$ fm [S&F Eq. (1.7)]. Those two constants divide to 1.20 MeV, so
this is exactly the form S&F quote as Eq. (6.19); `~NE-08` reproduces the
authors' Example 6.1 table with it.

| pair | $V_c$ (MeV) |
|---|---|
| d + t | 0.44 |
| p + ¹²C | 2.19 |
| α + ⁹Be | 2.62 |
| α + ²³⁸U | 28.4 |

So ⁹Be(α,n)¹²C releases 5.7 MeV yet needs about 2.6 MeV of alpha energy before it
will go at all (`test_exothermic_does_not_mean_barrierless`), and D–T fusion
releases 17.6 MeV but needs ~0.4 MeV of approach energy — which at thermal
equilibrium means $10^{8}$ K, the whole difficulty of `~NE-24`. Neutrons feel no
barrier, which is precisely why neutron-induced reactions dominate reactor
physics (`~NE-13`, `~NE-19`).

## Where this goes

- `~NE-05` — decay energetics: $Q_\alpha$, and the three different electron-mass
  corrections that $\beta^-$, $\beta^+$ and electron capture require.
- `~NE-08` — the proper kinematic threshold, with recoil, plus the Coulomb
  threshold sketched here.
- `~NE-09` — the fission Q-value and its 200 MeV budget.
- `~NE-10` — fusion Q-values, the Gamow peak, and how stars get over the barriers
  of §5.
- `~NE-13` — $(n,\gamma)$ Q-values as compound-nucleus excitation energy.
