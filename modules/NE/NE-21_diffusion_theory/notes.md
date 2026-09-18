# NE-21 — Neutron diffusion theory: Fick's law, the diffusion equation (notes)

`~NE-19` used the buckling $B_c^2$ as a given, and asserted
$P^{th}_{NL}=1/(1+L_T^2B^2)$ with a citation. This module is where both come
from, and the whole derivation is a balance sheet written on a differential
volume [Eq. (10.57)]:

$$\text{leakage}+\text{absorption}=\text{production}.$$

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§10.10 (Addendum 1), cited by **printed** page (PDF = printed + 23).

## 1. Fick's law

Neutrons random-walk between scatters, so on average more move from where there
are many to where there are few. Assume the net current is proportional to the
flux gradient [Eq. (10.58)]:
$$\boxed{\;J_x=-D\frac{d\phi}{dx}\;}$$

The minus sign is the entire physical content. Fick wrote this for molecules in
1855; Fourier had written $q=-k\,dT/dx$ for heat in 1823, and for the same
reason — both describe a random walk seen from far enough away that individual
steps stop mattering.

S&F treat $D$ as an empirical constant. It is not free: the standard P₁ result is
$D=\lambda_{tr}/3$, so **$D$ is a length**, of order a centimetre.

## 2. The equation

Balancing over a slab of thickness $dx$ [Eqs. (10.59)–(10.63)] and substituting
Fick's law:
$$-D\nabla^2\phi+\Sigma_a\phi=\nu\Sigma_f\phi+Q,$$
which with $L^2\equiv D/\Sigma_a$ and $k_\infty=\nu\Sigma_f/\Sigma_a$ becomes
[Eq. (10.66)]
$$\nabla^2\phi+\frac{k_\infty-1}{L^2}\phi=-\frac{Q}{D}.$$

**A useful aside.** S&F justify $k_\infty=\eta f$ here by saying "for the
one-speed model, $\varepsilon=1$ and $p=1$ since there are no fast neutron
effects". That is only meaningful if $\varepsilon$ and $p$ belong in $k_\infty$
in general — which is exactly the point `~NE-19` had to argue from Tables 10.5
and 10.8, because Eq. (10.17) omits $\varepsilon$. §10.10 supports the
correction independently.

The equation splits the subject in two.

## 3. Fixed-source problems: what $L$ means

Take a plane source in a non-multiplying medium [Eq. (10.68)]. The solution is
[Eq. (10.72)]
$$\phi(x)=\frac{S_0L}{2D}e^{-|x|/L}.$$

**Pure exponential decay with scale $L$** — that is what the diffusion length
*means*, before any random-walk interpretation. The module checks two things the
book does not: that the solution satisfies its own ODE, and that it conserves
neutrons ($\Sigma_a\int\phi\,dx=S_0$, since in an infinite non-multiplying medium
every source neutron is eventually absorbed).

The point-source version — not in S&F, and worth having because it is the one
that appears in shielding —
$$\phi(r)=\frac{S e^{-r/L}}{4\pi D r}$$
is **not** `~NE-11`'s uncollided $Se^{-\mu r}/4\pi r^2$. Diffusion counts the
scattered population too, so the geometric falloff is $1/r$ and the exponent
carries $L$. At 50 cm in graphite the two differ by **eight decades**. Confusing
them is the classic shielding blunder.

## 4. Criticality: an eigenvalue problem

With $Q=0$ [Eq. (10.73)],
$$\nabla^2\phi+B^2_{\rm mat}\phi=0,\qquad B^2_{\rm mat}\equiv\frac{k_\infty-1}{L^2},$$
subject to $\phi\to0$ at the boundary. For a slab this admits
$\phi=A\cos(B_{\rm mat}x)$ only if $B_{\rm mat}=n\pi/a$ — a **discrete
spectrum**. Generically the only solution is $\phi\equiv0$, which is the
mathematics saying that an arbitrary slab is not critical.

**Only $n=1$ is physical.** Every higher harmonic goes negative somewhere inside
the core, and a negative neutron density is meaningless. So [Eq. (10.80)]
$$\boxed{\;B^2_{\rm mat}=B_g^2\;}$$

with $B_{\rm mat}$ depending only on the **material** and $B_g$ only on the
**geometry**. Criticality is where the two meet, and that factorisation is what
lets a designer choose fuel and shape almost independently.

Two consequences follow immediately:

- **$k_\infty\le1$ makes $B_{\rm mat}^2\le0$**, and every $B_g^2$ is strictly
  positive, so no bare assembly of a subcritical material is critical at any
  size. `critical_dimension` refuses rather than returning a number.
- **The sphere is the smallest critical assembly.** Leakage is a surface effect,
  so least surface per volume wins; the module confirms
  sphere < cylinder < cube, with the optimum cylinder at $H/R=1.847$.

## 5. The flux shape is pure geometry

Table 10.10's profiles contain **no material properties at all**:

| geometry | profile | $B_g^2$ | peak/average |
|---|---|---|---|
| slab | $\cos(\pi x/a)$ | $(\pi/a)^2$ | $\pi/2=1.571$ |
| infinite cylinder | $J_0(2.405r/R)$ | $(2.405/R)^2$ | $2.316$ |
| sphere | $(1/r)\sin(\pi r/R)$ | $(\pi/R)^2$ | $\pi^2/3=3.290$ |
| cylinder | $J_0\cos$ | sum | $3.639$ |
| cube | $\cos^3$ | $3(\pi/a)^2$ | $(\pi/2)^3=3.876$ |

So once the shape is chosen, so is the power distribution, and the peaking factor
is a pure number. **A bare cylindrical core runs its centre 3.6× hotter than its
average.** Since the hottest fuel pin limits the whole reactor, that factor is
thrown-away capacity — and it is precisely why real cores are neither bare nor
uniform: a reflector raises the edges (`~NE-19` §10.6), and fuel zoning puts
fresh fuel at the periphery and depleted fuel at the centre.

## 6. Where this stops working

Three limits, and the module makes each explicit rather than leaving it as prose.

**Fick's law is an approximation.** It needs a nearly isotropic angular flux and
a nearly linear gradient over a mean free path, and gets neither within ~3
transport mean free paths of a source, a vacuum boundary, or a control rod. In
graphite that is 7.5 cm — a real fraction of a small assembly, and, awkwardly,
exactly where the plane-source problem imposes its boundary condition.

**The extrapolation distance is not always negligible.** The flux does not vanish
at the surface but at $d=0.7104\lambda_{tr}$ beyond it. S&F set $d=0$ as
"generally very small compared to the size of the reactor". For a metre-scale
power core, true. For a 20 cm graphite assembly, $d=1.8$ cm makes it effectively
18% larger — a **28% error in the buckling**.

**One speed is not enough.** The model never lets a neutron slow down, so it has
no fast-leakage term. For `~NE-19`'s ²³⁵U/graphite core it puts the critical
sphere at **90 cm** where the two-group answer with the Fermi age is **127 cm** —
a 30% underestimate, in the unsafe direction. Real analysis uses multigroup
diffusion, and where even that fails (near a control rod) the transport equation,
solved by discrete ordinates or Monte Carlo [§10.10.3].

## Where this goes

- `~NE-19` — supplies $k_\infty$, $L^2$ and $\tau$; this module supplies the
  $B^2$ and the non-leakage probabilities it used.
- `~NE-20` — point kinetics integrates the space away entirely; xenon spatial
  oscillations are exactly what it therefore cannot see.
- `~NE-22` — power peaking as a design constraint.
- `~MA-14` — the Helmholtz eigenvalue problem this is, and `~EM-03` for the same
  equation with a different name.

## A note on this module's correction

**Eq. (10.79)** prints the criticality condition as $B_{\rm mat}=n\pi/a$ —
*after* Eq. (10.78) has already selected $n=1$ and the preceding paragraph has
explained at length why every $n>1$ is unphysical. Table 10.10's slab entry is
$(\pi/a)^2$. The $n$ should not be there; keeping it reintroduces exactly the
solutions the text has just discarded.
