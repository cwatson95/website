# QF-02 — Interactions & Feynman Diagrams — Perturbation Theory & the S-matrix (notes)

Free fields (`~QF-01`) never scatter: their quanta sail past one another. All of
particle physics lives in the *interaction* term added to the Lagrangian, and —
because that term is almost never solvable exactly — in the **perturbative**
expansion of its effects. This note follows Peskin & Schroeder Chapter 4: the
**interaction picture** isolates the interaction, the **Dyson series** sums it into
the **S-matrix**, **Wick's theorem** turns time-ordered products into
**Feynman propagators**, and the bookkeeping of contractions becomes **Feynman
diagrams**. We read it all off the simplest interacting theory, $\phi^4$, and end
at the observable: the 2→2 **cross section**.

Citation key (full details + granularity in `refs.md`): **Pe** = Peskin &
Schroeder, *An Introduction to Quantum Field Theory*; **Zee** = Zee, *QFT in a
Nutshell*. Cited at section/chapter level. Natural units $\hbar=c=1$, metric
$(+,-,-,-)$ so an on-shell momentum has $p^2=m^2$.

## 1. The interaction picture
Split the Hamiltonian $H=H_0+H_{\mathrm{int}}$. In the **interaction (Dirac)
picture**, operators carry the *free* evolution while states carry only the
interaction. A field is therefore the free field of `~QF-01`, and the interaction
Hamiltonian itself is evolved with $H_0$, $H_I(t)=e^{iH_0 t}\,H_{\mathrm{int}}\,e^{-iH_0 t}$
[Pe §4.2]. States obey $i\,\partial_t|\psi\rangle=H_I(t)|\psi\rangle$, solved by a
time-evolution operator $U(t,t_0)$. Because $H_I$ at different times need not
commute, the solution is **time-ordered**:
$$U(t,t_0)=T\exp\!\left(-i\int_{t_0}^{t}H_I(t')\,dt'\right).$$
This is exactly the structure of time-dependent perturbation theory in `~QM-16`,
promoted to fields.

## 2. The Dyson series and the S-matrix
Expanding the time-ordered exponential gives the **Dyson series** [Pe §4.2]:
$$U(t,t_0)=\sum_{n=0}^{\infty}\frac{(-i)^n}{n!}\int_{t_0}^{t}\!dt_1\cdots dt_n\;
T\{H_I(t_1)\cdots H_I(t_n)\}.$$
The **S-matrix** is the evolution from the far past to the far future,
$S=U(\infty,-\infty)$, whose elements $\langle f|S|i\rangle$ are the scattering
amplitudes. Writing $H_I=-\int d^3x\,\mathcal{L}_{\mathrm{int}}$ makes the whole
construction manifestly Lorentz-covariant:
$$\boxed{\;S=T\exp\!\left(i\int d^4x\,\mathcal{L}_{\mathrm{int}}\right)\;}$$
Each power of $\mathcal{L}_{\mathrm{int}}$ is one **vertex**; order $n$ in the
coupling is $n$ vertices.

## 3. Wick's theorem and the Feynman propagator
To evaluate $\langle f|S|i\rangle$ we must reduce time-ordered products of fields to
something we can integrate. **Wick's theorem** [Pe §4.3] does this: a time-ordered
product equals its normal-ordered form plus the sum over **all contractions**,
$$T\{\phi(x_1)\cdots\phi(x_n)\}={:}\phi(x_1)\cdots\phi(x_n){:}+(\text{all contractions}).$$
Sandwiched between vacua, every normal-ordered term dies ($a|0\rangle=0$), so only
**fully contracted** terms survive. A single contraction *is* the **Feynman
propagator** [Pe §2.4, §4.3]:
$$\boxed{\;D_F(x-y)=\langle 0|T\,\phi(x)\phi(y)|0\rangle
=\int\frac{d^4p}{(2\pi)^4}\,\frac{i\,e^{-ip\cdot(x-y)}}{p^2-m^2+i\epsilon},
\qquad \widetilde D_F(p)=\frac{i}{p^2-m^2+i\epsilon}\;}$$
The $+i\epsilon$ (Feynman boundary condition) fixes which poles the $p^0$ contour
encircles — the causal prescription that propagates positive-energy modes forward
and antiparticles backward. Each surviving contraction draws a line; the lines and
vertices are a **Feynman diagram**, and Wick's theorem is precisely the statement
"sum over all diagrams" [Pe §4.4]. Code: `propagator` (and its on-shell pole at
$p^2=m^2$, $|\widetilde D_F|\sim1/\epsilon$).

## 4. $\phi^4$ theory: the vertex and the tree amplitude
The simplest interacting scalar theory adds a quartic self-coupling
$\mathcal{L}_{\mathrm{int}}=-\frac{\lambda}{4!}\phi^4$, whose four-point **vertex**
is $-i\lambda$ — the $4!$ cancelled by the $4!$ ways of attaching four external
lines to it [Pe §4.4]. At lowest order the 2→2 process $\phi\phi\to\phi\phi$ is a single
vertex with four legs — one **tree** diagram, no loops — giving
$$\boxed{\;i\mathcal{M}=-i\lambda\;\Longrightarrow\;\mathcal{M}=-\lambda,\qquad
|\mathcal{M}|^2=\lambda^2\;}$$
an **isotropic** amplitude (no angular dependence). Code: `phi4_amplitude_squared`.
At the next order, $O(\lambda^2)$, the diagrams close into a **loop** with an
internal integral $\int d^4k\,\widetilde D_F(k)\widetilde D_F(k{-}q)$ that **diverges**
logarithmically — the problem cured by **renormalization** in `~QF-04`.

## 5. Mandelstam variables and CM kinematics
A 2→2 reaction $p_1+p_2\to p_3+p_4$ has three Lorentz-invariant combinations, the
**Mandelstam variables** [Pe §4.5, Ch. 5]:
$$s=(p_1+p_2)^2,\qquad t=(p_1-p_3)^2,\qquad u=(p_1-p_4)^2.$$
Only two are independent: summing them and using $p_i^2=m_i^2$ gives the identity
$$\boxed{\;s+t+u=\sum_{i=1}^{4}m_i^2=4m^2\;}\quad(\text{equal masses}).$$
Here $s$ is the squared **CM energy**, $\sqrt{s}=E_{\mathrm{cm}}$; physical
scattering needs $\sqrt{s}\ge 2m$ so each particle is on-shell with real CM momentum
$|\mathbf p|=\tfrac12\sqrt{s-4m^2}$. In the CM frame, with scattering angle $\theta$,
$$s=E_{\mathrm{cm}}^2,\qquad
t=-\tfrac12(s-4m^2)(1-\cos\theta),\qquad
u=-\tfrac12(s-4m^2)(1+\cos\theta),$$
both $t,u\le0$ (spacelike momentum transfer). Code: `mandelstam`, `cm_energy`,
`cm_momentum` (and the sum check $s+t+u=4m^2$).

## 6. Two-body phase space and the 2→2 cross section
The S-matrix element becomes an observable through the **cross section**: amplitude
squared, times the incident flux, times the **two-body phase space**. For 2→2
scattering in the CM frame the whole package collapses to [Pe §4.5, Eq. 4.84]
$$\boxed{\;\left(\frac{d\sigma}{d\Omega}\right)_{\!\mathrm{CM}}
=\frac{1}{64\pi^2 s}\,\frac{|\mathbf p_f|}{|\mathbf p_i|}\,|\mathcal{M}|^2
\;=\;\frac{|\mathcal{M}|^2}{64\pi^2 s}\quad(\text{elastic})\;}$$
since elastic scattering has $|\mathbf p_f|=|\mathbf p_i|$. Code:
`phi4_differential_cross_section`. For $\phi^4$, $|\mathcal{M}|^2=\lambda^2$ is
isotropic, so the **total** cross section is the solid-angle integral with a factor
$\tfrac12$ for the two **identical** final-state particles (each configuration would
otherwise be counted twice) [Pe §4.5]:
$$\boxed{\;\sigma=\frac12\!\int\frac{|\mathcal{M}|^2}{64\pi^2 s}\,d\Omega
=\frac{1}{2}\,(4\pi)\,\frac{\lambda^2}{64\pi^2 s}=\frac{\lambda^2}{32\pi s}\;}$$
positive, $\propto\lambda^2$, falling as $1/s$, and vanishing below threshold
$\sqrt{s}<2m$. Code: `phi4_cross_section`. This is the field-theory cousin of the
non-relativistic $d\sigma/d\Omega=|f(\theta)|^2$ of `~QM-18`: there $f$ came from the
Born approximation (first-order perturbation theory in $V$); here $\mathcal{M}$ comes
from the Dyson series (perturbation theory in $\lambda$) — the same idea, made
relativistic and many-body.

## Where this goes
- `~QF-01` — the free fields and propagators contracted here; a field is the
  infinitely-many-oscillator object of bridge **B6**.
- `~QM-16` — time-dependent perturbation theory: the Dyson series is its
  field-theory form ($S=T\exp(-i\int H_I)$ is the Schrödinger-picture $U$ promoted).
- `~QM-18` — the non-relativistic limit: $\mathcal{M}\to$ the scattering amplitude
  $f(\theta)$, $d\sigma/d\Omega=|f|^2$, Born $\leftrightarrow$ tree level.
- `~QF-04` — the loop diagrams that $\phi^4$ generates at $O(\lambda^2)$ diverge;
  renormalization and the renormalization group make sense of them.
- `~QF-03` — gauge theories (QED): the same Feynman-rule machinery with spin,
  polarization sums, and the photon propagator.
