# QM-19 — Propagators & path integrals (notes)

`~QM-03` evolved a state by diagonalising $\hat H$ on a grid and rotating each
eigen-phase. Here we package *all* of time evolution into a single object — the
**propagator** (kernel) — and then ask Feynman's question: can we build it
straight from classical paths, with no mention of operators or eigenstates?

Units in the code are natural, $\hbar=m=1$; the formulae below keep $\hbar,m$
explicit.

## 1. The propagator (kernel)

The formal solution of the time-dependent Schrödinger equation
$i\hbar\,\partial_t\Psi=\hat H\Psi$ is $\Psi(t)=e^{-i\hat Ht/\hbar}\Psi(0)$. In
position space this reads
$$\Psi(x,t)=\int K(x,t;x',0)\,\Psi(x',0)\,dx',\qquad
K(x,t;x',0)=\langle x|\,e^{-i\hat Ht/\hbar}\,|x'\rangle.$$
$K$ is everything: hand it *any* initial wavefunction and it returns the state at
time $t$. It is the integral kernel of the evolution operator (Griffiths 3e,
Prob. 6.30, p.342).

Insert a complete set of energy eigenstates, $\hat H\psi_n=E_n\psi_n$:
$$K(x,t;x',0)=\sum_n \psi_n(x)\,\psi_n^*(x')\,e^{-iE_nt/\hbar}.$$
This **eigenfunction-sum (spectral) form** is Griffiths Eq. 6.79 (p.342). It
makes three structural facts immediate:

- **initial condition:** at $t=0$, $K=\sum_n\psi_n(x)\psi_n^*(x')=\delta(x-x')$
  (completeness), so $\Psi(x,0)$ is returned unchanged;
- **composition (semigroup):** $e^{-i\hat Ht_2/\hbar}e^{-i\hat Ht_1/\hbar}=
  e^{-i\hat H(t_1+t_2)/\hbar}$ becomes
  $\int K(x,t_2;y)\,K(y,t_1;x')\,dy=K(x,t_1+t_2;x')$;
- $|K(x,t;x',0)|^2$ is the probability for the particle to travel from $x'$ to
  $x$ in time $t$ (Griffiths p.342).

## 2. The propagator IS a Green's function (`~MA-14`)

Define the **retarded propagator** $G^R(x,t;x',0)=\theta(t)\,K(x,t;x',0)$. Because
$\partial_t\theta(t)=\delta(t)$ and $K(\cdot,0;x')=\delta(x-x')$,
$$\big(i\hbar\,\partial_t-\hat H\big)\,G^R(x,t;x',0)=i\hbar\,\delta(x-x')\,\delta(t).$$
So the propagator is the **time-domain Green's function of the Schrödinger
operator** $L=i\hbar\partial_t-\hat H$: for $t>0$ the kernel solves the
*homogeneous* equation, and the $\theta$-step supplies the $\delta(t)$ source —
exactly the causal construction of `~MA-14` (whose `causal_green_oscillator` is
$\theta(t-\tau)\times$ a homogeneous solution, the jump in $y'$ supplying its
$\delta$). (Griffiths p.503: in scattering "the Green's function is sometimes
called the propagator… the inspiration for Feynman's formulation.")

The spectral forms line up too. `~MA-14`'s Green's function of a differential
operator is $G=\sum_n\varphi_n(x)\varphi_n(\xi)/\lambda_n$; the propagator is the
*same* construction with $1/\lambda_n$ replaced by $e^{-iE_nt/\hbar}$. The static
$E\to0$ limit — the resolvent at zero energy — is the Green's function of $\hat H$
itself:
$$\langle x|\hat H^{-1}|x'\rangle=\sum_n\frac{\psi_n(x)\,\psi_n^*(x')}{E_n}.$$
For the particle in a box on $[0,1]$ ($\hbar=m=1$, $\hat H=-\tfrac12\partial_x^2=
\tfrac12 L_{\rm MA14}$) this equals **twice** MA-14's tent Green's function
`green_dirichlet`; the code imports MA-14 and verifies it term by term.

## 3. The free particle

For $\hat H=\hat p^2/2m$ the sum over (continuum) plane waves is a Gaussian
(Fresnel) integral, giving
$$\boxed{\,K_0(x,t;x',0)=\sqrt{\frac{m}{2\pi i\hbar t}}\;
\exp\!\left[\frac{im(x-x')^2}{2\hbar t}\right].}$$
(Griffiths Prob. 6.30(d).) Note what the pieces are:

- $|K_0|=\sqrt{m/2\pi\hbar t}$, **independent of $x$** — the amplitude to reach
  any point is the same, the physics is all in the phase;
- the phase is $m(x-x')^2/2\hbar t=S_{\rm cl}/\hbar$, the **classical action** of
  the straight-line path $x'\to x$; the $\sqrt{i}$ prefactor contributes a
  fixed **Maslov phase $-\pi/4$**;
- $K_0\to\delta(x-x')$ as $t\to0$ (a complex Gaussian collapsing to a spike);
- it obeys the semigroup law (a Gaussian convolution) and solves the free TDSE
  $i\hbar\,\partial_t K_0=-\tfrac{\hbar^2}{2m}\partial_x^2 K_0$ — i.e. it *is* the
  free retarded Green's function.

A Gaussian wavepacket $\Psi(x,0)=(2\pi\sigma^2)^{-1/4}e^{-(x-x_0)^2/4\sigma^2+ip_0x}$
propagated by $\int K_0\,\Psi_0$ keeps its Gaussian shape, its centre drifting at
the group velocity $p_0/m$ while its width spreads:
$$\sigma(t)=\sigma\sqrt{1+\left(\frac{\hbar t}{2m\sigma^2}\right)^2}.$$
The code cross-checks this against an **independent split-step FFT** integration
of the TDSE (Griffiths §2.4 *The Free Particle*, p.74; spreading is Prob. 2.21,
p.76) — propagator and direct evolution agree to machine precision.

## 4. The Feynman path integral

Slice $[0,t]$ into $N$ steps of width $\varepsilon=t/N$ and insert completeness
$\int dx_k\,|x_k\rangle\langle x_k|$ between every factor of
$e^{-i\hat Ht/\hbar}=\big(e^{-i\hat H\varepsilon/\hbar}\big)^N$:
$$K=\lim_{N\to\infty}\int\!\prod_{k=1}^{N-1}dx_k
\prod_{k=0}^{N-1}\langle x_{k+1}|e^{-i\hat H\varepsilon/\hbar}|x_k\rangle ,
\qquad x_0=x',\ x_N=x.$$
For small $\varepsilon$ each short-time amplitude is itself a free kernel times a
potential phase,
$$\langle x_{k+1}|e^{-i\hat H\varepsilon/\hbar}|x_k\rangle\simeq
\sqrt{\frac{m}{2\pi i\hbar\varepsilon}}\,
\exp\!\left\{\frac{i\varepsilon}{\hbar}\Big[\tfrac12 m\Big(\tfrac{x_{k+1}-x_k}{\varepsilon}\Big)^2-V(x_k)\Big]\right\},$$
so the total phase is $\frac{i}{\hbar}\sum_k L_k\,\varepsilon\to\frac{i}{\hbar}\int_0^t L\,dt$.
The product of integrals becomes a sum over all *paths* $x(\tau)$ from $x'$ to $x$:
$$\boxed{\,K=\int\mathcal{D}[x(\tau)]\;\exp\!\left(\frac{i}{\hbar}S[x]\right),
\qquad S[x]=\int_0^t L\,d\tau,\quad L=\tfrac12 m\dot x^2-V(x).}$$
Every path contributes with **unit modulus** and a phase equal to its classical
action in units of $\hbar$. Griffiths does not develop this (no path-integral
section exists in the book); the standard reference is Sakurai Ch. 2, and **the
verification here is the code**.

**Classical limit = stationary phase.** As $\hbar\to0$ the phase $S/\hbar$ sweeps
through many cycles for neighbouring paths, so their contributions cancel —
*except* near a path where $S$ is **stationary**, $\delta S=0$. That is the
Euler–Lagrange / Hamilton's-principle condition: the **classical path** dominates
(`~CM-13` calculus of variations; bridge **B1** to `~CM-17` Lagrangian mechanics,
which lands later). The free-particle phase being exactly $S_{\rm cl}/\hbar$ is
the simplest instance.

**Why we Wick-rotate to compute it.** In real time the integrand has *constant
modulus* and never decays, so a grid sum over the bare kernel converges only by
fragile stationary-phase cancellation (the "sign problem" — see the real-time
3-slice case in the code). The standard cure is the rotation $t\to-i\tau$: the
**heat kernel** $e^{-\tau\hat H}$ has positive, exponentially decaying matrix
elements, and the Trotter product $(D_{V/2}\,F\,D_{V/2})^N\to e^{-\tau\hat H}$
converges as $O(1/N^2)$. The code shows the time-sliced sum converging to the
closed form for the free particle and the oscillator. (Wick rotation is also the
bridge to the statistical-mechanics partition function $Z=\operatorname{Tr}e^{-\beta\hat H}$.)

## 5. The harmonic oscillator

Carrying out the path integral (the action is quadratic, so stationary phase is
*exact*) — or summing the Hermite eigenfunctions — gives **Mehler's kernel**
$$K=\sqrt{\frac{m\omega}{2\pi i\hbar\sin\omega t}}\,
\exp\!\left\{\frac{im\omega}{2\hbar\sin\omega t}\big[(x^2+x'^2)\cos\omega t-2xx'\big]\right\},
\qquad 0<\omega t<\pi.$$
(Griffiths Prob. 6.30(b).) It reduces to $K_0$ as $\omega\to0$ (since
$\sin\omega t\to\omega t$, $\cos\omega t\to1$) and solves the oscillator TDSE
$i\hbar\,\partial_t K=\big(-\tfrac{\hbar^2}{2m}\partial_x^2+\tfrac12 m\omega^2x^2\big)K$;
both are checked in `test_propagator.py`.

### Where this sits in the network
The propagator unifies `~QM-03` (time evolution), `~MA-14` (Green's functions),
and classical mechanics (`~CM-17`, recovered as the stationary-phase $\hbar\to0$
limit). The path-integral form is the launch point for `~QF-01` (quantum field
theory) and, after Wick rotation, for statistical mechanics.
