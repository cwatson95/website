# QM-08 — One-dimensional problems (notes)

Every problem here is the **time-independent Schrödinger equation** (TISE, `~QM-03`)
$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}+V(x)\,\psi=E\,\psi$$
for a different choice of $V(x)$. Two kinds of solution appear (Griffiths 3e §2.5.1,
p.82): **bound states** (normalizable, discrete $E$, when $E$ lies below $V$ at
both infinities) and **scattering states** (non-normalizable plane waves, continuous
$E$). The 1-D potentials below are the ones solvable in closed form, and between
them they introduce the entire vocabulary — quantization, parity, tunnelling,
resonance. *Natural units throughout:* $\hbar=m=1$ (restore SI by dimensional
analysis; energies carry $\hbar^2/m$).

## 1. The infinite square well — quantization from confinement

$V=0$ for $0<x<L$ and $V=\infty$ outside, so $\psi=0$ at the walls (Griffiths 3e
§2.2, p.49). Inside, $\psi''=-k^2\psi$ with $k=\sqrt{2mE}/\hbar$; the solution
vanishing at $x=0$ is $\psi=A\sin kx$, and $\psi(L)=0$ forces $kL=n\pi$. Hence
$$\boxed{\,E_n=\frac{n^2\pi^2\hbar^2}{2mL^2}\,},\qquad
\psi_n(x)=\sqrt{\tfrac2L}\,\sin\!\frac{n\pi x}{L},\quad n=1,2,3,\dots$$
The energies are **quantized** purely because the particle is *confined* — the
boundary conditions select a discrete set of standing waves, exactly like a string
fixed at both ends (`~MA-08`, `~CM-25`). There is a nonzero ground-state energy
$E_1>0$ (the uncertainty principle, `~QM-07`: you cannot have a confined particle
at rest). The $\psi_n$ are orthonormal and alternate parity about the centre.

**Numerically (`bound_states`).** Discretize the TISE with the 3-point stencil
$\psi''(x_i)\approx(\psi_{i-1}-2\psi_i+\psi_{i+1})/\Delta x^2$. The Hamiltonian
becomes a symmetric **tridiagonal matrix**
$$H_{ii}=\frac{\hbar^2}{m\,\Delta x^2}+V_i,\qquad
H_{i,i\pm1}=-\frac{\hbar^2}{2m\,\Delta x^2},$$
whose eigenpairs (via `scipy.linalg.eigh_tridiagonal`, `~MA-04`) are $(E_n,\psi_n)$.
With Dirichlet walls this reproduces the well ladder to $<0.1\%$ for the lowest $n$
(`test_infinite_well_eigenvalues`), and the eigenvectors come out orthonormal
(`test_infinite_well_orthonormal`). The same routine handles *any* $V(x)$ — it is
the workhorse for the finite well and delta well below, and a stand-in for `~QM-09`
when no closed form exists.

## 2. The finite square well — a finite tower of bound states

$V=-V_0$ for $|x|<a$ and $V=0$ outside, $V_0>0$ (Griffiths 3e §2.6, p.93). For a
bound state $-V_0<E<0$: inside, $\psi$ oscillates with $l=\sqrt{2m(E+V_0)}/\hbar$;
outside it decays as $e^{-\kappa|x|}$ with $\kappa=\sqrt{-2mE}/\hbar$. Because $V$
is symmetric, solutions split into **even** and **odd** parity. Matching $\psi$ and
$\psi'$ at $x=a$ gives the transcendental conditions (solved graphically)
$$\text{even: }\ \tan z=\frac{\sqrt{z_0^2-z^2}}{z},\qquad
\text{odd: }\ -\cot z=\frac{\sqrt{z_0^2-z^2}}{z},\qquad
z=la,\ \ z_0=\frac{a}{\hbar}\sqrt{2mV_0}.$$
The right-hand side is a quarter-circle of radius $z_0$, so the number of
intersections — the number of bound states — is **finite**, growing with the well's
"strength" $z_0$:
$$\boxed{\,N_\text{bound}=\Big\lceil \tfrac{2z_0}{\pi}\Big\rceil\,}$$
(one even state per interval $(n\pi,n\pi+\tfrac\pi2)$, one odd per
$(n\pi+\tfrac\pi2,(n+1)\pi)$). There is **always at least one** (even) bound state,
no matter how shallow. `finite_square_well_bound_count` returns this, and
`bound_states` finds exactly that many levels with $-V_0<E<0$
(`test_finite_well_count_matches_formula_and_solver`,
`test_finite_well_energies_below_depth`). As $V_0\to\infty$ ($z_0\to\infty$) the
levels become the infinite-well ladder of §1.

## 3. The delta-function well — exactly one bound state

$V(x)=-\alpha\,\delta(x)$, $\alpha>0$ (Griffiths 3e §2.5, p.85). Away from the
origin $V=0$, so a bound state ($E<0$) is $\psi=Be^{-\kappa|x|}$,
$\kappa=\sqrt{-2mE}/\hbar$. The delta forces a **kink**: integrating the TISE across
$x=0$ gives the jump condition $\Delta\psi'=-\tfrac{2m\alpha}{\hbar^2}\psi(0)$
(Griffiths 3e §2.5, p.86–87), which fixes $\kappa=m\alpha/\hbar^2$ and so
$$\boxed{\,E=-\frac{m\alpha^2}{2\hbar^2}\,}$$
— a **single** bound state, regardless of $\alpha$ (Griffiths Eq. 2.132, p.87).
This is the $z_0\to0$ corner of §2: a delta well is the limit of a deep, narrow
finite well of fixed area $V_0\!\cdot\!(2a)=\alpha$ (Griffiths Problem 2.31, p.97),
and `test_delta_well_as_finite_square_well_limit` recovers $-m\alpha^2/2\hbar^2$ from
`bound_states` as the width shrinks. *Switch the sign* ($V=+\alpha\delta$) and the
bound state vanishes — but the scattering coefficients, depending only on
$\alpha^2$, are unchanged: a particle tunnels through a delta *barrier* just as
readily as it crosses a delta *well* (Griffiths p.90).

## 4. The free particle — wave packets and dispersion

$V=0$ everywhere (Griffiths 3e §2.4, p.74). The stationary states
$\psi_k=e^{i(kx-\omega t)}$ carry any $E=\hbar^2k^2/2m\ge0$ but are **not
normalizable** — they are not physical states on their own. A real particle is a
**wave packet**, a superposition $\Psi(x,t)=\frac1{\sqrt{2\pi}}\int\phi(k)\,
e^{i(kx-\omega t)}\,dk$ (a Fourier transform, `~MA-09`). Its dispersion is
$$\omega(k)=\frac{\hbar k^2}{2m},\qquad
v_\text{phase}=\frac{\omega}{k}=\frac{\hbar k}{2m},\qquad
v_\text{group}=\frac{d\omega}{dk}=\frac{\hbar k}{m}=\frac{p}{m}.$$
The **group velocity** is the classical particle speed and is **twice** the phase
velocity (`test_free_particle_dispersion_and_velocities`) — a quirk of the quadratic
dispersion. Because $\omega\propto k^2$ is nonlinear, the packet **spreads**: a
minimum-uncertainty Gaussian of initial width $\sigma_0$ broadens as
$$\sigma_x(t)=\sigma_0\sqrt{1+\Big(\frac{\hbar t}{2m\sigma_0^2}\Big)^2}$$
(Griffiths Problem 2.22), narrowest at $t=0$ and symmetric in $|t|$
(`test_gaussian_packet_spreads`). This is the matter-wave analogue of optical
dispersion (`~EM-15`).

## 5. Scattering — the step, the barrier, and tunnelling

For $E$ above $V(\pm\infty)$ the states are travelling waves and the question is:
what fraction of an incident beam is reflected vs transmitted? With incident,
reflected and transmitted amplitudes $A,B,F$ the **reflection** and **transmission**
coefficients are the probability-current ratios (Griffiths 3e §2.5, p.89)
$$R=\frac{|B|^2}{|A|^2},\qquad T=\frac{k_\text{out}}{k_\text{in}}\frac{|F|^2}{|A|^2},
\qquad R+T=1 .$$
The current weight $k_\text{out}/k_\text{in}$ matters whenever the wave exits at a
different speed (Griffiths Problem 2.34(c), p.98): $T\ne|F/A|^2$ at a step.

**The step** $V=0\,(x<0),\ V_0\,(x>0)$ (Griffiths Problem 2.34, p.97). With
$k_1=\sqrt{2mE}/\hbar$, $k_2=\sqrt{2m(E-V_0)}/\hbar$:
$$E>V_0:\quad R=\Big(\frac{k_1-k_2}{k_1+k_2}\Big)^2,\quad
T=\frac{4k_1k_2}{(k_1+k_2)^2};\qquad E\le V_0:\quad R=1,\ T=0.$$
A classical particle with $E>V_0$ always passes; quantum-mechanically there is
partial reflection at *any* abrupt change in potential (`test_step_*`). The same is
true of a potential *drop* (Griffiths Problem 2.35, the "cliff", p.98) — a fast
neutron can reflect off the edge of a nucleus.

**The rectangular barrier** $V=V_0>0$ for $0<x<a$, else $0$ (Griffiths Problem
2.33, p.97). Inside, when $E<V_0$, $\psi$ is **evanescent** ($\kappa=
\sqrt{2m(V_0-E)}/\hbar$, $\psi\sim e^{\pm\kappa x}$); matching at both faces gives
$$\boxed{\,T=\Big[\,1+\frac{V_0^2\,\sinh^2(\kappa a)}{4E(V_0-E)}\,\Big]^{-1}\,}\qquad(E<V_0).$$
Crucially $T>0$: the particle can pass through a barrier higher than its energy.
This is **quantum tunnelling** (Griffiths p.90) — the mechanism of $\alpha$-decay,
the scanning tunnelling microscope, and the tunnel diode. For a thick/high barrier
$\sinh\kappa a\to\tfrac12 e^{\kappa a}$ and $T\propto e^{-2\kappa a}$, the
exponential sensitivity that lets an STM resolve single atoms; `~QM-15` generalizes
this to $T\sim e^{-2\int\kappa\,dx}$ (WKB). For $E>V_0$ the inside wave is
oscillatory ($k_2=\sqrt{2m(E-V_0)}/\hbar$) and
$$T=\Big[\,1+\frac{V_0^2\,\sin^2(k_2 a)}{4E(E-V_0)}\,\Big]^{-1}\qquad(E>V_0),$$
which **oscillates** and reaches **perfect transmission $T=1$** at the resonances
$k_2 a=n\pi$, i.e. $E=V_0+n^2\pi^2\hbar^2/2ma^2$ — the barrier becomes
"transparent" when its width is an integer number of internal half-wavelengths
(the Ramsauer–Townsend effect; the finite-well analogue is Griffiths Eq. 2.172,
p.96). Between $E=V_0$ the two formulae meet continuously
($T=[1+mV_0a^2/2\hbar^2]^{-1}$).

**Verification two ways.** `transmission_barrier`/`step_RT` give the analytic
coefficients; `scatter_piecewise` solves the *same* potential by the **transfer
matrix** — writing $\psi=A_je^{ik_jx}+B_je^{-ik_jx}$ in each constant region,
continuity of $\psi,\psi'$ at every interface gives
$[A_j,B_j]^T=W_j^{-1}W_{j+1}[A_{j+1},B_{j+1}]^T$, and the product maps the outgoing
($B=0$) to the incident amplitudes. The two agree to $10^{-9}$ for $E\lessgtr V_0$
(`test_barrier_matches_transfer_matrix`, `test_step_R_plus_T_and_transfer_matrix`),
and the transfer matrix extends unchanged to double barriers, wells and arbitrary
step-stacks.

---
### Why these five
The infinite well gives **quantization**; the finite well, a **finite** tower and
parity; the delta well, the **bound/scattering** dichotomy in miniature; the free
particle, **wave packets and dispersion**; the step and barrier, **reflection,
resonance and tunnelling**. Together they are the exactly-solvable backbone on which
`~QM-09` (the harmonic well), `~QM-12` (hydrogen) and `~QM-15` (WKB, perturbation)
build.
