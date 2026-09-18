# NE-21 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Power from flux, P = E_r Σ_f φ | Eq. (10.56), §10.10 | 356 | 379 |
| The neutron balance | Eq. (10.57) | 356 | 379 |
| **Fick's law** (`fick_current`); Fourier's 1823 analogue | Eq. (10.58), Fig. 10.18 | 357 | 380 |
| Leakage from a differential slab | Eq. (10.59), Fig. 10.19 | 357 | 380 |
| Absorption and production terms | Eqs. (10.60)–(10.61) | 358 | 381 |
| **The diffusion equation** | Eqs. (10.62)–(10.64) | 358 | 381 |
| **L² = D/Σ_a; the k_∞ form** (`diffusion_length`) | Eqs. (10.65)–(10.66) | 358 | 381 |
| Fixed-source vs criticality problems | §10.10 | 358–359 | 381–382 |
| **The infinite plane source** (`plane_source_flux`) | Eqs. (10.67)–(10.72), §10.10.1 | 359–360 | 382–383 |
| **The criticality problem**; material buckling | Eqs. (10.73)–(10.75), §10.10.2 | 360 | 383 |
| Extrapolation distance (set to zero) | §10.10.2 | 360 | 383 |
| The discrete spectrum; why only n = 1 | Eqs. (10.76)–(10.78) | 360–361 | 383–384 |
| **The criticality condition** (`critical_dimension`) | Eqs. (10.79)–(10.80) | 361 | 384 |
| **Table 10.10** — profiles and bucklings (`geometric_buckling`) | Table 10.10 | 362 | 385 |
| Multigroup diffusion; transport; discrete ordinates; Monte Carlo | §10.10.3 | 361–362 | 384–385 |

## The printed **n** in Eq. (10.79)

§10.10.2 works through the slab carefully. Eq. (10.76) gives the discrete
spectrum $B_{\rm mat}=n\pi/a$ for $n=1,3,5,\dots$; the following paragraph then
rejects every $n>1$ — "all the non-trivial solutions for $n>1$ become negative in
some regions between $-a/2$ and $a/2$, a physical impossibility" — and
Eq. (10.78) fixes the critical profile as $\phi_c=A\cos(\pi x/a)$.

Eq. (10.79), one line later, prints

$$B_{\rm mat}=\frac{n\pi}{a}$$

as "the following criticality condition", reintroducing exactly the solutions the
text has just discarded. It should read $\pi/a$, which is what **Table 10.10**
gives for the slab, $(\pi/a)^2$, and what Eq. (10.78) has already assumed.

*Recorded in `test_only_the_lowest_eigenvalue_is_physical`, which checks
numerically that every $n>1$ harmonic goes negative inside the slab and that
Table 10.10's entry is the $n=1$ value.*

## Three approximations this module quantifies rather than inherits

### The extrapolation distance
S&F impose $\phi(\pm a/2)=0$ at the physical surface, remarking that the
extrapolation distance "is generally very small compared to the size of the
reactor". The standard transport result is $d=0.7104\lambda_{tr}=2.1312D$, so
the flux vanishes at $a+2d$ rather than $a$.

For a 400 cm graphite slab that is a 1.8% error in $B^2$; for a **20 cm**
assembly it is **28%**. In water, where $\lambda_{tr}\approx0.43$ cm, it is
negligible almost everywhere. The approximation is safe in the regime S&F have in
mind and not in general, which is worth stating because the same §10.10 machinery
is exactly what one would reach for to analyse a small critical assembly.
`extrapolation_distance`, `extrapolated_dimension`.

### Where Fick's law fails
§10.10.3 says the diffusion equation "is quite inaccurate" for "certain
specialized calculations" such as the flux near a control rod, and gives no
criterion. The usual one is ~3 transport mean free paths from any source,
boundary or strong absorber — 7.5 cm in graphite, 1.3 cm in water.

That matters here specifically: the plane-source problem's boundary condition
$J(0^+)=S_0/2$ is imposed at $x=0$, which is precisely where the assumption is
worst. The solution is still right far from the source; it is not right near it.
`diffusion_valid`.

### One speed is not enough
The one-speed model never lets a neutron slow down, so it has no fast-leakage
term. Applied to `~NE-19`'s ²³⁵U/graphite core ($k_\infty=1.6939$,
$L^2=570.1$ cm²) it gives a critical sphere of **90.0 cm**; including the Fermi
age $\tau=368$ cm² gives **126.7 cm**, `~NE-19` Example 10.5's answer. The
one-speed result is 30% small, in the unsafe direction.

`test_this_is_where_NE_19s_non_leakage_probability_came_from` pins both, and also
confirms that $1/(1+L^2B^2)$ reproduces Example 10.4's $P^{th}_{NL}=0.7192$ at
$R=120$ cm — so the probability `~NE-19` cited is derived here.

## A note supporting the `~NE-19` four-factor correction
§10.10 justifies writing $k_\infty=\eta f$ for the one-speed model with the
explicit reason "$\varepsilon=1$ and $p=1$ since there are no fast neutron
effects". That statement is only meaningful if $\varepsilon$ and $p$ belong in
$k_\infty$ in the general case — which is what `~NE-19`'s `refs.md` argues from
Tables 10.5 and 10.8 against the printed Eq. (10.17). §10.10 supports the
correction independently, from a different part of the chapter.

## Two results added beyond S&F

**The point-source solution.** $\phi=Se^{-r/L}/(4\pi Dr)$, which S&F omit. Worth
having because it is the form that appears in shielding and because contrasting
it with `~NE-11`'s uncollided $Se^{-\mu r}/4\pi r^2$ is instructive: the
geometric falloff is $1/r$ rather than $1/r^2$ and the exponent carries $L$ rather
than the total mean free path, because diffusion counts the scattered population.
At 50 cm in graphite the two differ by eight decades.

**Peak-to-average flux.** Table 10.10 gives the profiles but never integrates
them. The peaking factors — $\pi/2$, 2.316, $\pi^2/3$, 3.639, $(\pi/2)^3$ — are
pure numbers with no material in them, and they are the quantitative reason real
cores are reflected and zoned. The module derives them and the test verifies each
by direct numerical integration of the profile rather than by the formula.

## Cross-module dependencies
- **`~NE-19`** — supplies $k_\infty$, $L^2$, $\tau$; consumes the $B_g^2$ of
  Table 10.10 and the non-leakage probabilities derived here.
- **`~NE-11`** — macroscopic cross sections, and the uncollided flux the
  point-source result must not be confused with.
- **`~NE-20`** — point kinetics is this equation with the space integrated out;
  xenon spatial oscillations are what that costs.
- **`~NE-22`** — power peaking as a design constraint.
- **`~MA-14`**, **`~EM-03`** — the Helmholtz eigenvalue problem under other names.

## Further reading
- Lamarsh, J.R., *Introduction to Nuclear Reactor Theory* (1966), Ch. 5–6 — the
  full derivation of Fick's law from P₁, and where the 0.7104 comes from.
- Duderstadt & Hamilton, *Nuclear Reactor Analysis*, Ch. 4–5 — multigroup
  diffusion and the numerical methods §10.10.3 gestures at.
- Bell & Glasstone, *Nuclear Reactor Theory* — the transport equation, and the
  Milne problem that gives the extrapolation distance exactly.
- Case, K.M. & Zweifel, P.F., *Linear Transport Theory* — where diffusion theory
  comes from and precisely when it fails.
