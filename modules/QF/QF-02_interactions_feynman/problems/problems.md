# QF-02 — Problems

Work them by hand, then check with `code/feynman.py`. Citations in `../refs.md`;
**Pe** = Peskin & Schroeder Ch. 4, **Zee** = Zee Part I. Natural units
$\hbar=c=1$, metric $(+,-,-,-)$ (so on-shell $p^2=m^2$), all four legs of mass $m$.

### P1.  The Dyson series and the S-matrix  *(Pe §4.2)*
From the interaction-picture Schrödinger equation $i\,\partial_t|\psi\rangle=H_I(t)|\psi\rangle$,
derive the time-ordered exponential $U(t,t_0)=T\exp(-i\int_{t_0}^t H_I\,dt')$ and hence
$S=T\exp(i\int\mathcal{L}_{\mathrm{int}}\,d^4x)$. Why must the exponential be
*time-ordered*, and why is the $n$-th term of order $\lambda^n$ (i.e. $n$ vertices)?
*Answer:* iterate $U=1-i\int H_I U$; the $T$ keeps later times to the left because
$[H_I(t_1),H_I(t_2)]\ne0$. Each $H_I\propto\lambda$, so $n$ factors $=$ order $\lambda^n=n$
vertices. *Check:* the lowest order that scatters $\phi\phi\to\phi\phi$ is one vertex
(order $\lambda^1$), giving `phi4_amplitude_squared(0.3)` $=0.09=\lambda^2$.

**Solution.** Integrate $i\,\partial_t|\psi\rangle=H_I|\psi\rangle$ from $t_0$ to $t$ and iterate:
$$U=1-i\!\int_{t_0}^t\!H_I(t_1)\,dt_1+(-i)^2\!\int_{t_0}^t\!\!dt_1\!\int_{t_0}^{t_1}\!\!dt_2\,H_I(t_1)H_I(t_2)+\cdots$$
In the $n$-th term the times are already ordered $t_1>t_2>\cdots$; symmetrizing the nested limits
over all $n!$ orderings and dividing by $n!$ replaces the ordering constraint by the time-ordering
symbol $T$, resumming to $U=T\exp(-i\int H_I\,dt')$. The $T$ is essential because
$[H_I(t_1),H_I(t_2)]\ne0$, so the factors must be stacked later-to-the-left. Writing
$H_I=-\int d^3x\,\mathcal{L}_{\mathrm{int}}$ makes it covariant,
$S=U(\infty,-\infty)=T\exp(i\int d^4x\,\mathcal{L}_{\mathrm{int}})$, and each $\mathcal{L}_{\mathrm{int}}\propto\lambda$
is one vertex, so the $n$-th term is order $\lambda^n$. The lowest order scattering $\phi\phi\to\phi\phi$
is a single vertex ($\lambda^1$), hence $|\mathcal{M}|^2=\lambda^2$: `phi4_amplitude_squared(0.3)`$=0.09$.

### P2.  Wick's theorem and the Feynman propagator  *(Pe §4.3, §2.4)*
Use Wick's theorem to reduce $\langle 0|T\,\phi(x)\phi(y)|0\rangle$ to a single
contraction, identify it as $D_F(x-y)$, and Fourier-transform to
$\widetilde D_F(p)=i/(p^2-m^2+i\epsilon)$. What does the $+i\epsilon$ do at $p^2=m^2$?
*Answer:* only the fully-contracted term survives the vacuum (normal-ordered pieces
annihilate $|0\rangle$); the contraction is $D_F$, and the $+i\epsilon$ (Feynman
prescription) shifts the on-shell pole off the real axis, regulating it while fixing
the causal/antiparticle boundary condition. *Check:* on shell, `propagator(np.array([np.sqrt(5),2,0,0]), 1.0, 1e-6)`
has $|D_F|\approx10^{6}=1/\epsilon$; off shell, `propagator([3,0,0,0],1.0)` $\approx 0.125\,i=i/(p^2-m^2)$.

**Solution.** Wick's theorem gives $T\,\phi(x)\phi(y)={:}\phi(x)\phi(y){:}+\langle0|T\,\phi(x)\phi(y)|0\rangle$.
The normal-ordered piece has all annihilators on the right, so $\langle0|{:}\phi\phi{:}|0\rangle=0$ and
only the single contraction survives — and that contraction *is* the Feynman propagator $D_F(x-y)$.
Fourier-transforming,
$$\widetilde D_F(p)=\frac{i}{p^2-m^2+i\epsilon}.$$
On shell $p^2=m^2$ the denominator would vanish; the $+i\epsilon$ holds it at $i\epsilon$, so
$|\widetilde D_F|\to1/\epsilon$ stays finite, and the infinitesimally displaced pole fixes the causal
boundary condition (positive energy forward, antiparticles backward). The code shows both limits:
on shell `propagator(np.array([np.sqrt(5),2,0,0]), 1.0, 1e-6)` has $|D_F|\approx10^6=1/\epsilon$ (the
regulated pole), while off shell at $p^2=9$, `propagator([3,0,0,0],1.0)`$=i/(9-1)=0.125\,i$.

### P3.  Mandelstam variables and the sum rule  *(Pe §4.5)*
Define $s=(p_1+p_2)^2$, $t=(p_1-p_3)^2$, $u=(p_1-p_4)^2$ for $p_1+p_2\to p_3+p_4$.
Expanding each and using momentum conservation and $p_i^2=m_i^2$, prove
$s+t+u=\sum_i m_i^2=4m^2$ — so only two invariants are independent.
*Answer:* $s+t+u=3p_1^2+\dots$ collects $2(p_1^2+p_2^2+p_3^2+p_4^2)$ from the squares
and cross terms that cancel by $p_1+p_2=p_3+p_4$, leaving $\sum_i m_i^2$.
*Check:* `mandelstam(5.0, np.pi/3, 1.0)` $=(25,-5.25,-15.75)$ and their sum equals
`mandelstam_sum(1.0)` $=4.0$.

**Solution.** Expand each invariant, e.g. $s=p_1^2+2\,p_1\!\cdot\!p_2+p_2^2$, $t=p_1^2-2\,p_1\!\cdot\!p_3+p_3^2$,
$u=p_1^2-2\,p_1\!\cdot\!p_4+p_4^2$, and add:
$$s+t+u=3p_1^2+p_2^2+p_3^2+p_4^2+2\,p_1\!\cdot\!(p_2-p_3-p_4).$$
Momentum conservation $p_1+p_2=p_3+p_4$ gives $p_2-p_3-p_4=-p_1$, so the cross term is $-2p_1^2$ and
the $3p_1^2$ collapses to $p_1^2$, leaving
$$s+t+u=p_1^2+p_2^2+p_3^2+p_4^2=\sum_i m_i^2=4m^2,$$
where $p_i^2=m_i^2$ is the on-shell condition. Only two of $s,t,u$ are independent. For $m=1$,
`mandelstam(5.0, np.pi/3, 1.0)`$=(25,-5.25,-15.75)$ sums to $4.0=$`mandelstam_sum(1.0)`$=4m^2$.

### P4.  CM kinematics and the threshold  *(Pe §4.5)*
Show that $\sqrt{s}=E_{\mathrm{cm}}$ is the total energy in the CM frame, that each
particle carries 3-momentum $|\mathbf p|=\tfrac12\sqrt{s-4m^2}$, and that physical
scattering requires $\sqrt{s}\ge 2m$. What happens to $t$ and $u$ as functions of
$\cos\theta$ in the physical region?
*Answer:* in the CM frame $\mathbf p_1+\mathbf p_2=0$, so $s=(E_1+E_2)^2=E_{\mathrm{cm}}^2$;
on-shell $|\mathbf p|=\tfrac12\sqrt{s-4m^2}$ is real only for $\sqrt{s}\ge2m$. Both
$t=-2|\mathbf p|^2(1-\cos\theta)\le0$ and $u=-2|\mathbf p|^2(1+\cos\theta)\le0$.
*Check:* `cm_energy` of two back-to-back on-shell 4-momenta $=2E$; `cm_momentum(5.0,1.0)` $=2.2913$,
while `cm_momentum(2.0,1.0)` $=0.0$ (at threshold) and `cm_momentum(1.5,1.0)` $=0.0$ (below).

**Solution.** In the CM frame the 3-momenta cancel, $\mathbf p_1+\mathbf p_2=0$, so
$s=(p_1+p_2)^2=(E_1+E_2)^2=E_{\mathrm{cm}}^2$ — $\sqrt s$ is the total energy. With both legs on-shell
and equal mass, $E_1=E_2=\sqrt{|\mathbf p|^2+m^2}=\tfrac12\sqrt s$, which inverts to
$$|\mathbf p|=\tfrac12\sqrt{s-4m^2}.$$
This is real only for $s\ge4m^2$, i.e. $\sqrt s\ge2m$ — the threshold to make two real particles;
below it `cm_momentum(1.5,1.0)`$=0$ and at it `cm_momentum(2.0,1.0)`$=0$ (no phase space), while above
it `cm_momentum(5.0,1.0)`$=\tfrac12\sqrt{21}=2.2913$ and `cm_energy` of two back-to-back on-shell
momenta returns $2E$. Then $t=-2|\mathbf p|^2(1-\cos\theta)$ and $u=-2|\mathbf p|^2(1+\cos\theta)$ are
both $\le0$, sweeping from $t=0$ (forward, $\cos\theta=1$) to $u=0$ (backward, $\cos\theta=-1$).

### P5.  The $\phi^4$ vertex and the tree amplitude  *(Pe §4.4–4.5)*
For $\mathcal{L}_{\mathrm{int}}=-\tfrac{\lambda}{4!}\phi^4$, explain why the four-point
**vertex** Feynman rule is $-i\lambda$ (where did the $4!$ go?), and deduce the
tree-level $2\to2$ amplitude $i\mathcal{M}=-i\lambda$, hence $|\mathcal{M}|^2=\lambda^2$.
Is it forward-peaked?
*Answer:* the $4!$ field-ordering choices at the vertex cancel the $1/4!$, leaving
$-i\lambda$; the single tree diagram gives $\mathcal{M}=-\lambda$, **isotropic** (no
$\theta$ dependence at this order). *Check:* `phi4_amplitude_squared(lam)` $=\lambda^2$
(e.g. $0.09$ at $\lambda=0.3$), independent of angle.

**Solution.** The first-order S-matrix term is $i\int d^4x\,\mathcal{L}_{\mathrm{int}}=-\tfrac{i\lambda}{4!}\int d^4x\,\phi^4$.
Attaching the four external legs $\phi\phi\to\phi\phi$ to the four fields at the vertex can be done in
$4!$ ways — the four fields pair with the four distinct legs in any order — and these $4!$ identical
contractions cancel the $1/4!$:
$$i\mathcal{M}=4!\times\Big(\!-\frac{i\lambda}{4!}\Big)=-i\lambda\ \Longrightarrow\ \mathcal{M}=-\lambda.$$
There is a single tree diagram — a point vertex, no internal propagator, no momentum transfer — so
$|\mathcal{M}|^2=\lambda^2$ is **isotropic**, *not* forward-peaked: no $\theta$ dependence at this order.
Hence `phi4_amplitude_squared(0.3)`$=0.09=\lambda^2$ for every scattering angle.

### P6.  The 2→2 cross section and identical particles  *(Pe §4.5, Eq. 4.84)*
Starting from $d\sigma/d\Omega=\frac{1}{64\pi^2 s}\frac{|\mathbf p_f|}{|\mathbf p_i|}|\mathcal{M}|^2$,
specialize to elastic equal-mass scattering and integrate to the total $\phi^4$ cross
section. Explain the factor $\tfrac12$.
*Answer:* elastic $\Rightarrow|\mathbf p_f|=|\mathbf p_i|$, so $d\sigma/d\Omega=\lambda^2/(64\pi^2 s)$;
the two final-state $\phi$'s are **identical**, so integrating over the full $4\pi$ counts
each configuration twice — divide by $2$: $\sigma=\tfrac12(4\pi)\lambda^2/(64\pi^2 s)=\lambda^2/(32\pi s)$.
*Check:* `phi4_cross_section(5.0,0.3,1.0)` $=3.581\times10^{-5}$, and equals
$\tfrac12\cdot4\pi\cdot$`phi4_differential_cross_section(5.0,0.3,1.0)`.

**Solution.** Elastic scattering keeps the same CM momentum in and out, $|\mathbf p_f|=|\mathbf p_i|$,
so the kinematic ratio is $1$ and with $|\mathcal{M}|^2=\lambda^2$ the rate is angle-independent,
$d\sigma/d\Omega=\lambda^2/(64\pi^2 s)$. Integrating an isotropic $d\sigma/d\Omega$ over the sphere
gives $4\pi$, but the two final-state $\phi$'s are **identical**, so the full-solid-angle integral
counts each distinct configuration twice; dividing by $2$,
$$\sigma=\frac12\!\int\!\frac{\lambda^2}{64\pi^2 s}\,d\Omega=\frac12(4\pi)\frac{\lambda^2}{64\pi^2 s}=\frac{\lambda^2}{32\pi s}.$$
At $\sqrt s=5,\ \lambda=0.3$: $\sigma=0.09/(32\pi\cdot25)=3.581\times10^{-5}$, exactly
`phi4_cross_section(5.0,0.3,1.0)` and equal to $\tfrac12\cdot4\pi\cdot$`phi4_differential_cross_section(5.0,0.3,1.0)`.

### P7.  Positivity, energy-falloff, and threshold  *(Pe §4.5; cf. `~QM-18`)*
From $\sigma=\lambda^2/(32\pi s)$ argue $\sigma>0$, $\sigma\propto\lambda^2$,
$\sigma\propto1/s$ (falls with energy), and $\sigma=0$ for $\sqrt{s}<2m$. How does this
compare to the non-relativistic $d\sigma/d\Omega=|f(\theta)|^2$ of `~QM-18`, where $f$
came from the Born approximation?
*Answer:* $\lambda^2>0$ and $s>0$ give $\sigma>0$; doubling $\lambda$ quadruples $\sigma$;
larger $s$ suppresses it; below threshold there is no phase space ($|\mathbf p_i|$ imaginary).
The structure mirrors `~QM-18`: tree level $\leftrightarrow$ Born, both first order in the
coupling, both giving $d\sigma/d\Omega\propto|\text{amplitude}|^2$. *Check:*
`phi4_cross_section(5.0,0.4,1.0)/phi4_cross_section(5.0,0.2,1.0)` $=4.0$ (i.e. $\propto\lambda^2$);
`phi4_cross_section(3.0,0.3,1.0)` $>$ `phi4_cross_section(6.0,0.3,1.0)`; and
`phi4_cross_section(1.99,0.3,1.0)` $=0.0$.

**Solution.** Read the closed form $\sigma=\lambda^2/(32\pi s)$ directly. The numerator $\lambda^2>0$
and denominator $s=E_{\mathrm{cm}}^2>0$ force $\sigma>0$; it is exactly $\propto\lambda^2$, so doubling
the coupling quadruples it — `phi4_cross_section(5.0,0.4,1.0)/phi4_cross_section(5.0,0.2,1.0)`$=(0.4/0.2)^2=4.0$.
The explicit $1/s$ makes $\sigma$ fall with energy,
$$\frac{\sigma(\sqrt s=3)}{\sigma(\sqrt s=6)}=\frac{6^2}{3^2}=4,$$
so `phi4_cross_section(3.0,0.3,1.0)`$>$`phi4_cross_section(6.0,0.3,1.0)`. Below threshold the incoming
pair cannot be on-shell ($|\mathbf p_i|=\tfrac12\sqrt{s-4m^2}$ imaginary), there is no phase space, and
$\sigma=0$ — `phi4_cross_section(1.99,0.3,1.0)`$=0.0$. The shape mirrors the non-relativistic `~QM-18`:
tree level $\leftrightarrow$ Born approximation, each first order in the coupling, each giving
$d\sigma/d\Omega\propto|\text{amplitude}|^2$ — here $|\mathcal{M}|^2$, there $|f(\theta)|^2$.
