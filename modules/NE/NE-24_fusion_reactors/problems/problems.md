# NE-24 — Problems

Work each by hand, then check with `code/fusion.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. Chapter 12's problems are
mostly on the conversion devices of `~NE-25`; these are added and work the fusion
side.

### P1.  A plasma has no on-ramp  *(added)*
Using the Saha equation at n = 2 × 10²¹ m⁻³, find the ionised fraction at 293 K,
5000 K and 20 000 K, and the temperature at which hydrogen is 95% ionised.
*Check:* 10⁻¹¹⁶, 10⁻⁴, 0.999; 95% at 13 630 K.

**Solution.** Eq. (12.1) with I = 13.598 eV gives

| T | f |
|---|---|
| 293 K | 8.8 × 10⁻¹¹⁶ |
| 5 000 K | 9.2 × 10⁻⁵ |
| 10 000 K | 0.336 |
| 20 000 K | 0.9992 |

and 95% at $\boxed{13\,630\ \text{K}}$.

**Four orders of magnitude in $f$ for a factor of two in $T$**, because $I/kT$
sits in an exponential. There is no regime of "slightly ionised gas" to
experiment in: everything about fusion — confinement, heating, diagnostics — has
to work in a state you can only arrive at abruptly.

*Note the book's own example.* §12.1.1 states I = 13.06 eV and gets 95% at
13 150 K. Hydrogen's ionisation energy is 13.598 eV; 13.06 is a transposed 13.60.
The example is internally consistent with the wrong value (it reproduces 0.9498),
which is why the constant and the example must be corrected together.

Note also the direction of the density term: a *denser* gas is *harder* to
ionise, because the $1/n$ prefactor favours recombination. Compressing a plasma
does not help you make one.

### P2.  Why everyone burns tritium  *(added)*
Find the critical ignition temperatures for D-T and D-D by setting Eq. (12.5)
equal to Eq. (12.6).
*Check:* 3.1 × 10⁷ K and 5.3 × 10⁸ K — a factor of 17.

**Solution.** Both power densities go as $n^2$, so **the density cancels** and
the crossing is a property of the fuel alone:
$$\tfrac14\langle\sigma v\rangle Q_{\rm fus}=1.42\times10^{-34}\sqrt{T}\ \ (\text{per }n^2).$$
Solving gives $\boxed{3.1\times10^7}$ K (2.7 keV) for D-T and
$\boxed{5.3\times10^8}$ K (46 keV) for D-D, against S&F Fig. 12.2's 3 × 10⁷ and
6 × 10⁸.

**A factor of seventeen in temperature** — and, because $\langle\sigma v\rangle$
is so steep there, a factor of ~100 in reactivity at any temperature you can
actually reach. That is why every serious experiment burns tritium, despite
tritium having a 12.3-year half-life, being essentially absent from nature, and
having to be bred in the blanket from the lithium that also cools it.

**And watch the $Z^2$.** The bremsstrahlung coefficient scales as $Z^2$, so a
1% tungsten impurity radiates like 5000 extra hydrogens and shifts the ignition
temperature up by ~70%. Plasma-facing materials are not an engineering
afterthought; they are in the ignition condition.

### P3.  A tokamak-like operating point  *(added)*
A D-T plasma runs at n = 10¹⁴ cm⁻³ and 15 keV. Compare fusion and radiated power,
and find the confinement time Lawson demands.
*Check:* 1.80 vs 0.019 W/cm³; τ = 2.0 s.

**Solution.** $P_{\rm fus}=\tfrac14n^2\langle\sigma v\rangle Q=\boxed{1.80\
\text{W/cm}^3}$ and $P_{\rm rad}=\boxed{0.019\ \text{W/cm}^3}$ — fusion beats
bremsstrahlung by 96×, so at 15 keV radiation is no longer the binding
constraint.

Lawson [Eq. (12.10)] gives $n\tau_E\ge2.0\times10^{14}$ s/cm³, so
$$\tau_E\ge\boxed{2.0\ \text{s}}.$$

**Two seconds is the whole difficulty of magnetic confinement.** It sounds
undemanding until you notice what is being held: a 150-million-degree gas, at a
pressure of several atmospheres, touching nothing, in a geometry that is
unstable in several independent ways. JET's best is under a second.

Note also that ignition is *far* behind us at 15 keV — the plasma passed it at
2.7 keV. The binding constraint has changed from "does it radiate away" to "does
it stay put", which is exactly why the subject's figure of merit changed from a
temperature to a triple product.

### P4.  The best place to build a reactor  *(added)*
At what temperature is the triple product minimised, and what does it demand?
*Check:* 14 keV, 3.0 × 10¹⁵ keV s cm⁻³.

**Solution.** Minimising $n\tau_ET=12kT^2/(E_c\langle\sigma v\rangle)$ gives
$\boxed{13.6\ \text{keV}}$ and $\boxed{3.0\times10^{15}}$ keV s cm⁻³ — consistent
with S&F's stated bound of $>2\times10^{15}$ [Eq. (12.14)]. At n = 10¹⁴ cm⁻³ that
is τ = 2.2 s.

**Why this replaced the Lawson product.** The triple product varies by under 35%
over a factor of three in temperature, while $n\tau_E$ itself varies by a factor
of two. Eq. (12.13) explains it: $n\tau_ET\propto T^{-1/3}$, essentially flat.

So the triple product characterises the **confinement scheme** rather than the
operating point — which is what you want when comparing a tokamak with a
stellarator, or JET with ITER. Its minimum also sits at a *lower* temperature
than the Lawson product's, which is why modern designs target ~15 keV rather than
the ~30 keV the older criterion suggests.

### P5.  Break-even is not the goal  *(added)*
What Q does a fusion *power plant* need, and why is Q = 1 not it?
*Check:* about 20; Q = 1 means the alphas supply 20% of the heating.

**Solution.** Eq. (12.7) with S&F's assumptions ($\eta_{\rm heat}=0.7$,
$f_{\rm recirc}=0.25$, $\eta_{\rm elect}=0.35$, $f_c=0.2$):
$$Q=\frac{1}{(0.7)(0.25)(0.35)(0.8)}=\boxed{20.4}.$$

At $Q=1$ the plasma produces as much fusion energy as was put into heating it —
but only $E_\alpha/Q_{\rm fus}=3.5/17.6=\boxed{20\%}$ of that energy stays in the
plasma as charged particles. The other 80% leaves as a neutron and has to be
caught, turned into heat, turned into electricity at 35%, and fed back at 70%.

**Ignition ($Q=\infty$) is a fivefold further step**, not a marginal one: the
alphas must supply *all* the heating rather than a fifth of it.

Better engineering helps but does not rescue it: at 45% electrical efficiency and
40% recirculation, Q ≈ 10. The requirement stays firmly in double figures, which
is why "we achieved break-even" and "we have a power plant" are separated by
about an order of magnitude.

### P6.  Why ICF compresses a thousandfold  *(added)*
A 1 mm D-T pellet is heated to 10 keV. How long is it confined, what density does
Lawson then demand, and what areal density burns a third of the fuel?
*Check:* 0.8 ns; 4 × 10²³ cm⁻³; ρR = 3 g/cm².

**Solution.** From Eq. (12.15) with $R=0.5$ mm and the D-T sound speed,
$$\tau_E=R\sqrt{m/kT}=\boxed{8.0\times10^{-10}\ \text{s}},$$
**eight orders of magnitude shorter than a tokamak's**. Since $n\tau_E$ must still
reach 3.2 × 10¹⁴ s/cm³,
$$n\ge\boxed{4\times10^{23}\ \text{cm}^{-3}}$$
— about **eight times solid density**, and that is only to satisfy Lawson at the
pellet's full radius.

To actually *burn* the fuel, $\phi=\rho R/(\rho R+H_B)$ with $H_B\approx6$ g/cm²
demands $\rho R=\boxed{3.0\ \text{g/cm}^2}$ for a third — against ~0.02 g/cm² for
an uncompressed millimetre pellet. That is 150× in areal density, i.e. **a
thousandfold in volume density**: denser than lead, from a target the size of a
peppercorn, in a nanosecond, and symmetrically enough that the compression does
not tear itself apart.

**MCF and ICF are the same inequality solved from opposite ends.** One buys
$n\tau$ with seconds at 10¹⁴ cm⁻³; the other with 10²⁵ cm⁻³ for a nanosecond.
Neither has yet delivered net electricity, and the reasons are different in every
particular except the inequality itself.
