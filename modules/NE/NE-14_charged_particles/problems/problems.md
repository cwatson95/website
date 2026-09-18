# NE-14 — Problems

Work each by hand, then check with `code/charged_particles.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P5
follow the book's Chapter 7 problems 17–21 (printed 220); P6–P7 are added.
Range constants are S&F Tables 7.2–7.3, transcribed in the module.

### P1.  Bremsstrahlung in air and in lead  *(S&F Ch. 7, Prob. 17)*
For a 5 MeV electron, what is the ratio of bremsstrahlung loss to collisional
loss in air, and in lead?
*Check:* air 5.2%; lead 59%.

**Solution.** Eq. (7.43) with $m_e/M=1$:
$$\frac{(-dE/ds)_{\text{rad}}}{(-dE/ds)_{\text{coll}}}=\frac{EZ}{700}.$$

Air is 78% N ($Z=7$), 21% O ($Z=8$), 1% Ar ($Z=18$), giving an effective
$Z\simeq7.3$:
$$\frac{5\times7.3}{700}=\boxed{0.052}.$$

Lead, $Z=82$:
$$\frac{5\times82}{700}=\boxed{0.586}.$$

**In lead, more than a third of a 5 MeV electron's energy leaves as photons.**
That is the whole reason high-energy electron accelerators are surrounded by
massive photon shielding rather than the thin absorbers the electron range alone
would suggest — an electron stopping in 3 mm of lead makes x-rays that need
centimetres.

The crossover, where the two losses are equal, is $700/82=8.5$ MeV in lead. At
5 MeV we are below it but not far.

### P2.  Stopping three particles with aluminium  *(S&F Ch. 7, Prob. 18)*
About what thickness of aluminium stops (a) 2.5 MeV electrons, (b) 2.5 MeV
protons, (c) 10 MeV alphas?
*Check:* (a) 5.84 mm; (b) 58.8 μm; (c) 59.2 μm.

**Solution.** From Eq. (7.47) with Tables 7.2–7.3, and $\rho_{\text{Al}}=2.70$
g/cm³:

| | $\rho R$ (g/cm²) | $R$ |
|---|---|---|
| (a) 2.5 MeV electron | 1.5780 | **5.84 mm** |
| (b) 2.5 MeV proton | 0.01587 | **58.8 μm** |
| (c) 10 MeV alpha | 0.01597 | **59.2 μm** |

Two things are worth more than the numbers.

**The electron needs 99 times the thickness of the proton** at comparable energy,
and — from P1 — stopping it in a *high-Z* material would generate penetrating
bremsstrahlung. Hence aluminium rather than lead.

**(b) and (c) agree to 0.7%, and that is not a coincidence.** A 10 MeV
alpha and a 2.5 MeV proton have the same *speed* ($E\propto m$ at fixed $v$), and
by rule 2 their ranges scale as $m/z^2 = 4/4 = 1$. The scaling rule of §3
predicted this before either was looked up.

### P3.  A triton's range by scaling  *(S&F Ch. 7, Prob. 19)*
Estimate the range of a 10 MeV triton in air.
*Check:* 0.0594 g/cm² ≈ 49 cm.

**Solution.** Table 7.2 has no triton constants, so use rule 2 (S&F Example 7.7's
method).

*Step 1 — matched speed.* $E_p=E_T\,(m_p/m_T)=10\times(1.00728/3.01605)=3.340$ MeV.

*Step 2 — proton range in air at 3.340 MeV.* Eq. (7.47) with
$(a,b,c)=(-2.5510,1.5066,0.21732)$ and $x=\log_{10}3.340=0.5237$:
$$\rho R_p=10^{-2.5510+0.7890+0.0596}=0.01984\ \text{g/cm}^2.$$

*Step 3 — scale.* $m/z^2=3/1=3$, so
$$\rho R_T=3\times0.01984=\boxed{0.0594\ \text{g/cm}^2},$$
and at $\rho_{\text{air}}=1.205\times10^{-3}$ g/cm³ that is **49 cm** of air.

Note this is a *tritium nucleus at 10 MeV*, not the 18.6 keV beta tritium
actually emits (`~NE-05`). Real tritium betas have a range of ~6 mm in air and
cannot penetrate skin — which is why tritium is an internal hazard only, and why
the two numbers must never be confused.

### P4.  Testing the empirical formula against real data  *(S&F Ch. 7, Prob. 20)*
Janni's CSDA ranges for protons in aluminium are $2.953\times10^{-4}$,
$4.020\times10^{-3}$ and 0.1692 g/cm² at 0.1, 1 and 10 MeV. Compare with
Eq. (7.47).
*Check:* −27.5%, −3.4%, +3.9%.

**Solution.** With $(a,b,c)=(-2.4108,1.4570,0.19861)$:

| $E$ (MeV) | Eq. (7.47) | Janni | difference |
|---|---|---|---|
| 0.1 | $2.142\times10^{-4}$ | $2.953\times10^{-4}$ | **−27.5%** |
| 1.0 | $3.883\times10^{-3}$ | $4.020\times10^{-3}$ | **−3.4%** |
| 10.0 | 0.17572 | 0.1692 | **+3.9%** |

The middle of the range is good to a few percent. **The 0.1 MeV endpoint is 27%
low** — and that is the useful result, because 0.1 MeV is the *stated lower
bound* of the fit's validity. A three-parameter quadratic in $\log E$ fitted over
two decades is necessarily worst at its ends, and here the low end is bad enough
that a 100 keV proton range taken from Eq. (7.47) would be meaningfully wrong.

Two lessons. Quote the fit's accuracy, not just its answer — S&F give the
formula and the validity window but no error estimate, and this problem is
effectively the missing one. And note that the module **refuses to evaluate below
0.1 MeV at all**: if the formula is already 27% off *at* the boundary, whatever
it returns beyond it is meaningless.

### P5.  Fission fragments barely move  *(S&F Ch. 7, Prob. 21)*
Compare the range of the median heavy fission fragment (67.9 MeV) in air and in
gold, using Eq. (7.48).
*Check:* 2.33 mg/cm² in air; 8.32 mg/cm² in gold.

**Solution.** $\rho R=CE^{2/3}$ with $E^{2/3}=67.9^{2/3}=16.63$:
$$\text{air: }0.14\times16.63=\boxed{2.33\ \text{mg/cm}^2},\qquad
\text{gold: }0.50\times16.63=\boxed{8.32\ \text{mg/cm}^2}.$$

As lengths: 1.9 cm in air ($\rho=1.205\times10^{-3}$), and **4.3 μm in gold**
($\rho=19.3$).

A fission fragment carries 68 MeV — thirty times a typical alpha — and travels
one sixth as far in gold. The reason is $z^2$: a fragment leaves scission with
about 20 units of charge (`~NE-09`), so it couples $\sim400$ times more strongly
than a proton at the same speed.

The engineering consequence is the one `~NE-09` relies on: **all 168 MeV of
fission-fragment energy is deposited within a few microns of where the fission
happened.** The fuel pellet heats itself; the coolant only ever sees heat
conducted out through the cladding. Everything about reactor thermal-hydraulics
follows from that locality (`~NE-22`).

### P6.  Why an alpha emitter is safe outside and lethal inside  *(added)*
The dead outer layer of human skin is about 40 μm thick. Compare the range of a
5 MeV alpha in tissue with that, and explain the factor-20 radiation weighting
factor alphas carry.
*Check:* 38 μm in water — comparable to the dead skin layer.

**Solution.** From Eq. (7.47), a 5 MeV alpha in water has
$\rho R=3.79\times10^{-3}$ g/cm², i.e. **38 μm**. (ASTAR gives
$3.63\times10^{-3}$, so the fit is 4% high here.)

**Externally**, that is about the thickness of the stratum corneum — the dead
epidermal layer. An alpha emitter held against the skin deposits essentially all
its energy in dead cells. A sheet of paper, or a few centimetres of air (its
range in air is 3.6 cm), stops it completely.

**Internally**, the same 5 MeV is deposited in ~38 μm of *living* tissue — a
path perhaps four cell diameters long. Along it, the Bragg peak of §2 concentrates
the loss near the end. The result is dense, correlated ionization: many
double-strand DNA breaks in a small volume, which cells repair far less
successfully than the sparse damage a 1 MeV electron leaves along its 4 mm path.

That difference in *spatial density* of energy deposition — not the total energy —
is what the radiation weighting factor $w_R$ encodes (`~NE-18`): 1 for photons
and electrons, **20 for alphas**. It is a statement about stopping power, and
this module is where it comes from.

The practical corollary is the polonium-210 and radon cases: harmless in a sealed
source, extremely dangerous inhaled or ingested.

### P7.  Building a beta shield the right way round  *(added)*
A source emits 2 MeV betas. Compare shielding it with 5 mm of lead against 12 mm
of acrylic, and design the better shield.
*Check:* lead converts 23% of the energy to bremsstrahlung; acrylic 1.7%.

**Solution.** Both stop the betas. A 2 MeV electron has $\rho R=1.64$ g/cm² in
lead (1.4 mm) and 0.99 g/cm² in water-like plastic (9.9 mm), so either thickness
is ample.

The difference is what is *made* on the way. From Eq. (7.43):

| | $Z$ | radiative fraction at 2 MeV |
|---|---|---|
| lead | 82 | **23.4%** |
| aluminium | 13 | 3.7% |
| acrylic (≈ carbon) | 6 | **1.7%** |

Stopping the beta in lead converts nearly a quarter of its energy into
bremsstrahlung x-rays, which are penetrating and now require their own shield.
Stopping it in acrylic converts 1.7%.

**The correct design is layered, low-$Z$ first:**

1. enough acrylic or aluminium to exceed the beta range — this stops the betas
   while generating minimal bremsstrahlung;
2. lead *behind* that, to attenuate the small photon yield that is produced
   anyway.

Reversing the order — lead first — maximises exactly the secondary radiation you
are trying to avoid. This is a standard mistake and it is a direct consequence of
the linear $Z$ in Eq. (7.43).

(The same logic explains why ³²P sources, a common laboratory beta emitter at
1.7 MeV, are shipped in thick plastic rather than lead pots.)
