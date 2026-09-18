# NE-02 — Problems

Work each by hand, then check with `code/nuclear_models.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P4
follow the book's Chapter 3 problems 6, 7, 9 and 10 (printed 77–78); P5–P8 are
added. Liquid-drop constants throughout: $a_v=15.835$, $a_s=18.33$,
$a_c=0.714$, $a_a=23.20$, $a_p=\pm11.2$ MeV.

### P1.  The nuclear surface  *(S&F Ch. 3, Prob. 6)*
Using the nucleon distribution $\rho(r)=\rho_o/\{1+\exp[(r-R)/a]\}$
[Eq. (3.11)], by what fraction does the density fall between $r=R-2a$ and
$r=R+2a$?
*Check:* $\rho(R-2a)/\rho_o=0.8808$ and $\rho(R+2a)/\rho_o=0.1192$, a ratio of
$0.135$ — an 86.5% drop.

**Solution.** At $r=R\pm2a$ the exponent is $\pm2$, so
$$\frac{\rho(R-2a)}{\rho_o}=\frac{1}{1+e^{-2}}=\frac{1}{1.1353}=0.8808,\qquad
\frac{\rho(R+2a)}{\rho_o}=\frac{1}{1+e^{2}}=\frac{1}{8.389}=0.1192 .$$
The density falls by a factor $0.1192/0.8808=0.135$, i.e. **86.5%**, over a span
of $4a\approx2$ fm. Two readings matter. First, the nucleus has no sharp edge:
the surface region is about 2 fm thick regardless of $A$, which is why "radius"
must be defined (half central density). Second, since surface thickness is fixed
while $R\propto A^{1/3}$, the *fraction* of nucleons in the surface falls as $A$
grows — precisely why the surface term $-a_sA^{2/3}$ costs less per nucleon for
heavy nuclei, and why $B/A$ rises at small $A$.

### P2.  Liquid-drop bookkeeping for ⁴⁰Ca and ²⁰⁸Pb  *(S&F Ch. 3, Prob. 7)*
Tabulate every contribution to the binding energy for ⁴⁰Ca and ²⁰⁸Pb, and the
total. Compare with the measured values.
*Check:* `semf_terms(40,20)` and `semf_terms(208,82)`; totals $337.27$ and
$1624.75$ MeV against measured $342.05$ and $1636.45$ MeV.

**Solution.** For **⁴⁰Ca** ($A=40$, $Z=20$, $N=20$, even-even):

| term | value (MeV) |
|---|---|
| volume $+a_vA$ | $+633.40$ |
| surface $-a_sA^{2/3}$ | $-214.39$ |
| Coulomb $-a_cZ^2/A^{1/3}$ | $-83.51$ |
| asymmetry $-a_a(A-2Z)^2/A$ | $0$ |
| pairing $+a_p/\sqrt A$ | $+1.77$ |
| **total** | **$+337.27$** |

The asymmetry term vanishes exactly because $N=Z$. For **²⁰⁸Pb** ($Z=82$,
$N=126$, even-even): volume $+3293.68$, surface $-643.48$, Coulomb $-810.29$,
asymmetry $-215.94$, pairing $+0.78$, total $+1624.75$ MeV.

The comparison is the lesson. In ⁴⁰Ca the Coulomb term is 13% of the volume term;
in ²⁰⁸Pb it is 25% and nearly equals the surface term. Coulomb repulsion is what
eventually stops the chart of the nuclides, and it is the term that makes heavy
nuclei fissionable (`~NE-09`). Against experiment the model is 4.8 MeV low for
⁴⁰Ca and 11.7 MeV low for ²⁰⁸Pb — both are *doubly magic*, so the shortfall is
the shell effect the drop model structurally cannot capture (P7).

### P3.  Where does the $B/A$ curve come from?  *(S&F Ch. 3, Prob. 9)*
Plot, per nucleon and against $A$: the volume term, and the negatives of the
surface, asymmetry and Coulomb terms, plus the total $B/A$ ignoring pairing,
taking $Z=Z(A)$ from Eq. (3.18). Explain the peak.
*Check:* `figures/make_figures.py` draws this; the maximum of $B/A$ falls at
$A\approx56$ with $B/A\approx8.7$ MeV.

**Solution.** Divide each term by $A$:
$$\frac{BE}{A}=a_v-a_sA^{-1/3}-a_c\frac{Z^{2}}{A^{4/3}}-a_a\frac{(A-2Z)^{2}}{A^{2}} .$$
The volume term is a **constant** $15.835$ MeV — the ceiling. The surface term
$-a_sA^{-1/3}$ is large and negative at small $A$ and dies away as $A^{-1/3}$:
this is the *rising* part of the curve. The Coulomb term, with $Z\propto A$,
behaves as $-a_cA^{2/3}$ per nucleon: negligible when light, dominant when heavy —
this is the *falling* part. The asymmetry term grows too, because $Z(A)$ pulls
away from $A/2$.

So $B/A$ is the difference of a decaying surface penalty and a growing Coulomb
penalty, and it peaks where their derivatives balance, near $A\approx56$
(`test_binding_energy_per_nucleon_peaks_in_the_iron_region`). Everything downstream
follows: nuclei below the peak release energy by **fusing** (`~NE-10`), nuclei
above it by **fissioning** (`~NE-09`), and iron/nickel is where stellar burning
stops (`~NE-10` §nucleosynthesis).

### P4.  The $A=70$ isobar  *(S&F Ch. 3, Prob. 10)*
Using the Appendix B masses, tabulate $70-M({}^{70}_{Z}\mathrm{X})$ against $Z$
for the $A=70$ chain and identify the stable members.
*Check:* `load_atomic_masses()` gives, for $Z=28\ldots36$,
$70-M = 0.063860,\,0.067591,\,0.074675,\,0.073972,\,0.075750,\,0.069070,\,0.066500,\,0.055380,\,0.043990$ u;
`most_stable_Z(70)`$=31.39$.

**Solution.** Larger $70-M$ means smaller mass, hence more stable. Reading the
column, the two maxima are at $Z=30$ ($0.074675$) and $Z=32$ ($0.075750$) — both
**even-even** — while $Z=31$ ($0.073972$, odd-odd) sits *below both of them*.
The stable nuclides at $A=70$ are indeed ⁷⁰Zn ($Z=30$) and ⁷⁰Ge ($Z=32$), and
Eq. (3.18) predicts the minimum at $Z=31.39$, **between** them.

This is the two-parabola picture of §5 of the notes, and it explains the whole
pattern: ⁷⁰Ga ($Z=31$) is odd-odd and lies on the upper curve, so it is heavier
than both of its even-even neighbours and can decay *either* way — $\beta^-$ to
⁷⁰Ge or $\beta^+$/EC to ⁷⁰Zn. (It does both, 99.6% $\beta^-$.) An odd-odd nuclide
wedged between two even-even ones is the standard configuration for a
branching decay, and the same structure at $A=110$ gives the book's Fig. 3.13.

### P5.  How dense is nuclear matter?
From $R=1.1A^{1/3}$ fm, compute the nucleon number density and convert it to a
mass density in kg/m³. Compare with water.
*Check:* `nucleon_number_density(238)`$=0.1794$ fm⁻³; the mass density is
$2.97\times10^{17}$ kg/m³.

**Solution.** For any $A$,
$$n=\frac{A}{\frac43\pi(1.1A^{1/3})^{3}}=\frac{3}{4\pi(1.1)^{3}}
=0.179\ \text{fm}^{-3},$$
independent of $A$ — the $A$ cancels identically, which is the whole point.
Multiplying by the nucleon mass $1.66\times10^{-27}$ kg and converting
$1\ \text{fm}^{-3}=10^{45}\ \text{m}^{-3}$,
$$\rho = 0.179\times1.66\times10^{-27}\times10^{45}=2.97\times10^{17}\ \text{kg/m}^{3},$$
about $3\times10^{14}$ times the density of water. A teaspoon (5 mL) of nuclear
matter would weigh $1.5\times10^{12}$ kg — a billion tonnes. This is the density
of a neutron star, which is essentially one enormous nucleus held together by
gravity instead of the strong force (`~RE-14`).

### P6.  Why is there no stable nuclide beyond bismuth?
Using the SEMF, show that the Coulomb term eventually defeats the volume term,
and estimate where $B/A$ would fall to zero.
*Check:* $B/A$ at $A=238$ is $7.589$ MeV; the Coulomb term for ²⁰⁸Pb is
$-810.29$ MeV, a quarter of its $+3293.68$ MeV volume term.

**Solution.** Per nucleon, with $Z\approx0.4A$ for heavy nuclei,
$$\frac{BE}{A}\approx a_v-a_sA^{-1/3}-a_c(0.4)^{2}A^{2/3}-a_a(0.2)^{2}.$$
The Coulomb term grows without bound as $A^{2/3}$ while everything else is
bounded, so $B/A$ must eventually go negative. Setting the expression to zero:
$$15.835-0.928-0.114A^{2/3}-0.928=0\ \Longrightarrow\ A^{2/3}\approx122
\ \Longrightarrow\ A\approx1350 .$$
That is far beyond any observed nuclide, and correctly so — *binding* does not
have to vanish for a nucleus to be unstable, it only has to become unfavourable
relative to a decay channel. Alpha emission becomes exothermic well before $B/A$
reaches zero (around $A\approx150$), and spontaneous fission takes over near
$Z^{2}/A\approx47$ (for ²³⁸U, $Z^{2}/A=35.6$). The practical limit — bismuth-209
as the heaviest quasi-stable nuclide — is set by those channels, computed in
`~NE-04` and `~NE-09`, not by the sign of $BE$.

### P7.  The shell surplus
For the doubly magic nuclides ¹⁶O, ⁴⁰Ca, ⁴⁸Ca and ²⁰⁸Pb, compute
(measured $BE$) − (SEMF $BE$). What does the sign tell you?
*Check:* $+5.98$, $+4.78$, $+5.91$ and $+11.70$ MeV respectively.

**Solution.** All four residuals are **positive**: every doubly magic nucleus is
more tightly bound than the smooth formula predicts. Since the SEMF is a smooth
function of $A$ and $Z$ (polynomials, $A^{2/3}$, $\sqrt A$), it *cannot* produce a
local enhancement at isolated values of $Z$ and $N$ — it can only be fitted to
average through them. So the residual is not a fitting deficiency to be tuned
away; it is evidence for structure the model does not contain.

That structure is shell closure: at $Z$ or $N=2,8,20,28,50,82,126$ a nucleon
energy level fills, the next nucleon must go into a substantially higher level,
and the nucleus gains stability exactly as a noble gas does. The largest surplus,
$+11.7$ MeV at ²⁰⁸Pb, is the doubly magic closure at $Z=82$, $N=126$ — which is
why ²⁰⁸Pb is the heaviest stable nuclide and why so many decay chains terminate
there (`~NE-07`).

### P8.  Reading the pairing sign off the data
Show from the SEMF that even-even and odd-odd members of the same isobar lie on
curves separated by $2a_p/\sqrt A$, and confirm the direction of the split
against the $A=70$ data of P4.
*Check:* `pairing_term(110,46) - pairing_term(110,45)` $=2\times11.2/\sqrt{110}$;
in P4, $Z=31$ (odd-odd) is heavier than both $Z=30$ and $Z=32$ (even-even).

**Solution.** The pairing contribution to $BE$ is $-a_p/\sqrt A$ with
$a_p=-11.2$ MeV for even-even and $+11.2$ MeV for odd-odd. So
$$BE_{\text{ee}}-BE_{\text{oo}}=\frac{11.2}{\sqrt A}-\left(-\frac{11.2}{\sqrt A}\right)
=\frac{2a_p}{\sqrt A}=\frac{22.4}{\sqrt A}\ \text{MeV},$$
which for $A=70$ is $2.68$ MeV. More binding means less mass, so the even-even
curve lies **below** the odd-odd curve by $2.68$ MeV $=0.00288$ u.

The P4 table confirms both the direction and roughly the size: $Z=31$ (odd-odd)
has $70-M=0.073972$ u while its even-even neighbours $Z=30$ and $Z=32$ have
$0.074675$ and $0.075750$ u — the odd-odd nuclide is heavier than both, by
$0.0007$ and $0.0018$ u. (The measured gaps are smaller than the crude $0.00288$
u because the parabola's own curvature works against the split on one side.) Had
the sign convention been reversed, ⁷⁰Ga would be predicted *lighter* than both
neighbours and therefore stable — the opposite of reality, and a good reason to
check this sign whenever borrowing SEMF constants from another textbook.
