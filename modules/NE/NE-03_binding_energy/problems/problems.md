# NE-03 — Problems

Work each by hand, then check with `code/binding_energy.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6
follow the book's Chapter 4 problems 2, 3/6, 4, 7, 8 and 10 (printed 94–95);
P7–P8 are added. All masses from `../data_tables/B1_atomic_masses.csv`, with
$c^{2}=931.494043$ MeV/u, $M(^1\mathrm{H})=1.0078250321$ u and
$m_n=1.0086649156$ u.

### P1.  How many MeV in one atomic mass unit?  *(S&F Ch. 4, Prob. 2)*
Compute the rest-mass energy of 1 u directly from $E=mc^{2}$.
*Check:* `U_MEV`$=931.494043$ MeV.

**Solution.** One atomic mass unit is $1.6605389\times10^{-27}$ kg (Table A.1), so
$$E=mc^{2}=(1.6605389\times10^{-27})(2.99792458\times10^{8})^{2}
=1.49242\times10^{-10}\ \text{J},$$
and dividing by $1.60217653\times10^{-19}$ J/eV,
$$E=9.31494\times10^{8}\ \text{eV}=931.494\ \text{MeV}.$$
This single number does all the work in this module: every mass difference in u
becomes an energy in MeV by multiplying by it. Worth committing to memory as
"a nucleon is about 931.5 MeV, and a milli-u is about 0.93 MeV."

### P2.  Binding energy per nucleon  *(S&F Ch. 4, Probs. 3 and 6)*
From Appendix B masses, find $BE$ and $BE/A$ for ¹⁶O, ¹⁷O, ⁵⁶Fe and ²³⁵U. What is
the significance?
*Check:* $BE=127.619,\,131.763,\,492.254,\,1783.870$ MeV and
$BE/A=7.9762,\,7.7507,\,8.7902,\,7.5909$ MeV.

**Solution.** Apply $BE=[ZM(^1\mathrm{H})+(A-Z)m_n-M]c^{2}$. For ¹⁶O:
$$8(1.0078250)+8(1.0086649)-15.9949146=0.1370050\ \text{u},$$
$$BE=0.1370050\times931.494=127.62\ \text{MeV},\quad BE/A=7.976\ \text{MeV}.$$
The others follow identically. The significance is the **shape**: ⁵⁶Fe sits at the
top (8.79 MeV/nucleon) while ¹⁶O below it and ²³⁵U above it are both *less* bound
per nucleon. Any process that moves nucleons toward the peak releases the
difference — fusion from the light side, fission from the heavy side. Note also
that ¹⁷O is less bound per nucleon than ¹⁶O despite being heavier: adding a
neutron to a doubly magic core *lowers* the average (P3).

### P3.  Separation energy versus average  *(S&F Ch. 4, Prob. 4)*
Find $BE/A$ and $S_n$ for ¹⁶O and ¹⁷O and explain the contrast.
*Check:* $S_n(^{16}\mathrm{O})=15.664$ MeV, $S_n(^{17}\mathrm{O})=4.143$ MeV,
against averages of $7.976$ and $7.751$ MeV.

**Solution.** From Eq. (4.14), $S_n=BE(A,Z)-BE(A-1,Z)$:
$$S_n(^{16}\mathrm{O})=127.619-111.955=15.66\ \text{MeV},\qquad
S_n(^{17}\mathrm{O})=131.763-127.619=4.14\ \text{MeV}.$$
The average changes by a fraction of an MeV between the two nuclides; the
*marginal* cost changes by a factor of **3.8**. That is the whole reason to care
about separation energies. ¹⁶O is doubly magic ($Z=N=8$): its last neutron
completes a closed shell and is held by 15.7 MeV. The 17th neutron must start a
new shell and is held by only 4.1 MeV — it is nearly falling out.

Practically, this is why ¹⁷O and ¹⁸O are useful neutron sources under alpha
bombardment and why $S_n$, not $BE/A$, tells you whether neutron capture on a
given nuclide is worth much energy (`~NE-13`).

### P4.  The electron binding energy from masses alone  *(S&F Ch. 4, Prob. 7)*
The proton and hydrogen-atom masses are known to 10 significant figures. Estimate
$BE_e$ in ¹H from them, and compare with the Bohr model.
*Check:* $(m_p+m_e-M(^1\mathrm{H}))c^{2}=13.70$ eV, against Bohr's 13.606 eV.

**Solution.** The atom is lighter than its parts by the electron binding:
$$BE_e=[m_p+m_e-M(^1\mathrm{H})]c^{2}
=[1.0072764669+0.0005485799-1.0078250321]\ \text{u}\times931.494\ \text{MeV/u}.$$
The bracket is $1.47\times10^{-8}$ u, giving $BE_e=13.70$ eV against the measured
and Bohr-predicted 13.606 eV (`~NE-01` §3).

The discussion the problem asks for is about **significant figures**, not physics.
The three masses agree to their first seven digits; the entire answer lives in
digits 8–10. A one-unit change in the last tabulated digit of $M(^1\mathrm{H})$
moves the answer by 0.09 eV — which is exactly the size of the 0.1 eV discrepancy
above. So the mass-difference route reproduces the Bohr value to within its own
precision, and no better. This is why chemical energies are *never* computed from
mass tables, and why nuclear energies always are: nuclear mass defects are 6
orders of magnitude larger and sit in digits 3–5 instead.

### P5.  ³He, and a separation energy that does not exist  *(S&F Ch. 4, Prob. 8)*
Find the binding energy of ³He and its neutron separation energy.
*Check:* $BE(^3\mathrm{He})=7.718$ MeV; `has_nuclide(2, 2)` is `False`, and
`proton_separation_energy(3, 2)`$=5.493$ MeV.

**Solution.** The binding energy is routine:
$$BE=[2(1.0078250)+1(1.0086649)-3.0160293]\times931.494=7.718\ \text{MeV},$$
a mere 2.57 MeV/nucleon — ³He is very loosely bound, which is why the next step,
${}^3\mathrm{He}+n\to{}^4\mathrm{He}$, releases so much.

The neutron separation energy, however, **has no value**. Removing the single
neutron from ³He leaves ${}^2_2\mathrm{He}$ — the diproton — which is *unbound*
and therefore absent from Appendix B; `neutron_separation_energy(3, 2)` raises a
`KeyError` rather than inventing a number. The physically meaningful quantity is
the *proton* separation energy,
$$S_p(^3\mathrm{He})=BE(^3\mathrm{He})-BE(^2\mathrm{H})=7.718-2.225=5.49\ \text{MeV},$$
which removes a proton and leaves a deuteron. That the diproton does not bind
while the deuteron does is a statement about the spin dependence of the nuclear
force and the Pauli principle — two protons in the same spatial state must have
opposite spins, and the nuclear force is too weak to bind that configuration.

### P6.  Taking ⁵⁶Fe apart  *(S&F Ch. 4, Prob. 10)*
For ⁵⁶Fe, find the energy needed to (a) remove one neutron, (b) remove one
proton, (c) dismantle it completely, and (d) fission it symmetrically into two
²⁸Al.
*Check:* $S_n=11.197$, $S_p=10.184$, $BE=492.254$ MeV;
$2BE(^{28}\mathrm{Al})-BE(^{56}\mathrm{Fe})=-26.90$ MeV.

**Solution.**
(a) $S_n=BE(^{56}\mathrm{Fe})-BE(^{55}\mathrm{Fe})=11.20$ MeV.
(b) $S_p=BE(^{56}\mathrm{Fe})-BE(^{55}\mathrm{Mn})=10.18$ MeV.
(c) Complete dismantling costs the full binding energy, $492.25$ MeV — the sum of
55 successive separation energies, and about 44 times the cost of the first one.
(d) Symmetric fission into two ²⁸Al ($Z=13$ each, $2\times13=26$ ✓):
$$Q=2BE(^{28}\mathrm{Al})-BE(^{56}\mathrm{Fe})=2(232.677)-492.254=-26.90\ \text{MeV}.$$

The sign in (d) is the point. Fissioning iron **costs** 26.9 MeV — it is
endothermic, because iron already sits at the top of the $BE/A$ curve and both
fragments are less bound per nucleon than the parent. Compare ²³⁵U in P7, where
the same arithmetic gives $+194$ MeV. Fission is not a property of "big nuclei";
it is a property of nuclei on the far side of the binding-energy peak.

### P7.  Where the 200 MeV comes from
Estimate the energy released when ²³⁵U splits into two fragments near $A=117$.
*Check:* $BE/A=7.5909$ MeV for ²³⁵U and $8.4178$ MeV for ¹¹⁷Pd; the difference
times 235 is $194.3$ MeV.

**Solution.** Every one of the 235 nucleons moves from a nuclide bound at 7.591
MeV/nucleon to one bound at about 8.418 MeV/nucleon, so
$$Q\approx A\left[\frac{BE}{A}\Big|_{\text{products}}-\frac{BE}{A}\Big|_{\text{parent}}\right]
=235\,(8.418-7.591)=194\ \text{MeV}.$$
This is the famous "about 200 MeV per fission" — and the estimate needs nothing
but the $BE/A$ curve. The exact figure depends on the fragment pair (real fission
is asymmetric) and on how much goes to neutrons, gammas and neutrino-carrying
beta decays; `~NE-09` does the full budget, which comes to $\approx200$ MeV of
which about 190 MeV is recoverable as heat. For scale, a chemical reaction
releases a few eV per event: fission is $10^{8}$ times more energetic per event.

### P8.  Energetically unstable is not the same as unstable
Show that ²³⁸U is unstable to alpha emission and compute the Q-value; then
explain why ²⁰⁸Pb, with $S_\alpha=-0.52$ MeV, is nonetheless treated as stable.
*Check:* `alpha_separation_energy(238, 92)`$=-4.270$ MeV, so
$Q_\alpha=+4.270$ MeV.

**Solution.** The alpha separation energy is
$$S_\alpha=BE(^{238}\mathrm{U})-BE(^{234}\mathrm{Th})-BE(^{4}\mathrm{He})
=1801.69-1777.67-28.30=-4.27\ \text{MeV},$$
negative, so emitting an alpha *releases* $Q_\alpha=4.27$ MeV. (The measured
²³⁸U alpha energy is 4.27 MeV — the agreement is exact because this *is* the
same quantity.) The alpha is unusually favourable as an emitted fragment because
⁴He is itself tightly bound at 7.07 MeV/nucleon; emitting a single neutron from
²³⁸U would cost $+6.15$ MeV instead.

²⁰⁸Pb has $S_\alpha=-0.52$ MeV, so it too is energetically permitted to alpha
decay. It does not, observably, because the emitted alpha must tunnel through the
Coulomb barrier, and the tunnelling probability depends exponentially on
$Q_\alpha$. Dropping $Q$ from 4.27 MeV to 0.52 MeV lengthens the half-life by
something like 40 orders of magnitude — from $4.5\times10^{9}$ years to far
beyond the age of the universe. **Energetic instability sets which decays are
possible; the barrier sets which ones happen on observable timescales**, and the
gap between the two is the entire content of Gamow's theory of alpha decay
(`~NE-05`).
