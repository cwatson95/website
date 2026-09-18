# QM-08 — Problems

Work them by hand, then check with `code/one_dim.py`. Sources in `../refs.md`.
Natural units $\hbar=m=1$ throughout.

### P1.  The infinite-well ladder, from finite differences
Show that confining a free particle to $0<x<L$ quantizes its energy as
$E_n=n^2\pi^2\hbar^2/2mL^2$, and that a numerical eigensolver on a grid recovers
this from the bare Schrödinger operator. *(The walls enter only as boundary
conditions $\psi=0$.)*
*Answer:* $E_1:E_2:E_3=1:4:9$; for $L=1$, $E_1=\pi^2/2\approx4.93$.
*Check:* `bound_states(np.zeros(2001), np.linspace(0,1,2001), n_states=3)[0]`
$\approx$ `[infinite_well_energy(n,1.0) for n in (1,2,3)]`.
(`test_infinite_well_eigenvalues`, `test_infinite_well_orthonormal`.)
*(Griffiths 3e §2.2, p.49–50.)*

**Solution.** Inside the well $V=0$, so the TISE is $\psi''=-k^2\psi$ with
$k=\sqrt{2mE}/\hbar$, giving $\psi=A\sin kx+B\cos kx$. The wall condition
$\psi(0)=0$ kills the cosine ($B=0$); $\psi(L)=0$ then forces $\sin kL=0$, i.e.
$kL=n\pi$. Therefore
$$E_n=\frac{\hbar^2k_n^2}{2m}=\frac{n^2\pi^2\hbar^2}{2mL^2},\qquad n=1,2,3,\dots,$$
so $E_1:E_2:E_3=1:4:9$, and for $L=1,\ \hbar=m=1$, $E_1=\pi^2/2\approx4.9348$.
The finite-difference eigensolver, which only knows $V=0$ and the Dirichlet walls,
returns $[4.9348,\,19.7392,\,44.4131]$ — matching `infinite_well_energy(n,1.0)` and
confirming quantization comes purely from confinement.

### P2.  How many bound states does a finite well hold?
For the well $V=-V_0$ on $|x|<a$, show the number of bound states is finite and
equals $\lceil 2z_0/\pi\rceil$ with $z_0=\frac a\hbar\sqrt{2mV_0}$, and that every
level sits in $-V_0<E<0$. Take $V_0=15$, $a=1$.
*Answer:* $z_0=\sqrt{30}\approx5.48$, so $\lceil 2z_0/\pi\rceil=4$ bound states.
*Check:* `finite_square_well_bound_count(15.0, 1.0)` $=4$; a finite-difference
solve on a wide box finds exactly 4 levels with $E<0$, all $>-15$.
(`test_finite_well_count_matches_formula_and_solver`,
`test_finite_well_energies_below_depth`.) *(Griffiths 3e §2.6, p.93.)*

**Solution.** A bound state has $-V_0<E<0$: inside it oscillates with
$l=\sqrt{2m(E+V_0)}/\hbar$, outside it decays with $\kappa=\sqrt{-2mE}/\hbar$.
Matching $\psi$ and $\psi'$ at $x=a$ (using parity) gives the transcendental pair
$\tan z=\sqrt{z_0^2-z^2}/z$ (even) and $-\cot z=\sqrt{z_0^2-z^2}/z$ (odd), where
$z=la$ and $z_0=\frac a\hbar\sqrt{2mV_0}$. The right-hand side is a quarter-circle
of radius $z_0$, so there are **finitely** many intersections — one even per
$(n\pi,n\pi+\tfrac\pi2)$ and one odd per $(n\pi+\tfrac\pi2,(n{+}1)\pi)$ — totalling
$\lceil 2z_0/\pi\rceil$. With $V_0=15,a=1$: $z_0=\sqrt{30}\approx5.477$, so
$2z_0/\pi\approx3.49$ and $\lceil\cdot\rceil=4$. `finite_square_well_bound_count(15,1)`
returns $4$, and the FD solver finds exactly four levels, all with $-15<E<0$.

### P3.  The delta well — exactly one bound state  *(Griffiths 3e Prob. 2.31, p.97)*
Show $V=-\alpha\,\delta(x)$ binds exactly one state at $E=-m\alpha^2/2\hbar^2$, and
that it is the zero-width limit of a finite well of fixed area $2aV_0=\alpha$.
*Answer:* $E=-\alpha^2/2$ (natural units); independent of the value of $\alpha$.
*Check:* `delta_well_energy(2.0)` $=-2.0$; modelling the delta as a narrow finite
well and shrinking its width, `bound_states` ground energy $\to-2.0$ monotonically.
(`test_delta_well_one_bound_state`, `test_delta_well_as_finite_square_well_limit`.)

**Solution.** Away from the origin $V=0$, so a bound state ($E<0$) is the decaying
$\psi=Be^{-\kappa|x|}$ with $\kappa=\sqrt{-2mE}/\hbar$. Integrating the TISE across
$x=0$ over $[-\varepsilon,\varepsilon]$, the $V$ term gives $-\alpha\psi(0)$ and the
kinetic term gives the slope jump, so
$$\Delta\psi'=\psi'(0^+)-\psi'(0^-)=-\frac{2m\alpha}{\hbar^2}\psi(0).$$
Here $\psi'(0^\pm)=\mp\kappa B$, so $-2\kappa B=-\frac{2m\alpha}{\hbar^2}B$, fixing
$\kappa=m\alpha/\hbar^2$ — one value, hence **one** bound state. Then
$E=-\hbar^2\kappa^2/2m=-m\alpha^2/2\hbar^2$, i.e. $E=-\alpha^2/2$ in natural units,
independent of $\alpha$. For $\alpha=2$, $E=-2$: `delta_well_energy(2.0)` returns
$-2.0$, and the narrow-well limit recovers it.

### P4.  Tunnelling through a rectangular barrier  *(Griffiths 3e Prob. 2.33, p.97)*
A particle with $E<V_0$ meets a barrier of height $V_0$, width $a$. Show the
transmission is nonzero, $T=[1+\frac{V_0^2\sinh^2\kappa a}{4E(V_0-E)}]^{-1}$ with
$\kappa=\sqrt{2m(V_0-E)}/\hbar$, and that for a thick barrier $T\sim e^{-2\kappa a}$.
*Answer:* for $V_0=10,E=5$: $T(a{=}1)\approx7.1\times10^{-3}$, falling ~30$\times$
per unit width — classically zero, quantum-mechanically finite (the STM, $\alpha$-decay).
*Check:* `transmission_barrier(5.0, 10.0, 1.0)` $\approx0.00714$; compare
`transmission_barrier(5.0, 10.0, a)` for $a=1,2,3$. (`test_barrier_tunnelling_is_positive`,
`test_barrier_analytic_formula`, `test_barrier_limits`.)

**Solution.** With $E<V_0$ the wave is **evanescent** inside the barrier,
$\psi\sim e^{\pm\kappa x}$, $\kappa=\sqrt{2m(V_0-E)}/\hbar$. Matching $\psi,\psi'$ at
$x=0$ and $x=a$ gives the standard result
$$T=\Big[\,1+\frac{V_0^2\sinh^2(\kappa a)}{4E(V_0-E)}\,\Big]^{-1}>0,$$
nonzero because $\sinh$ never vanishes — the particle tunnels. For $V_0=10,E=5$:
$\kappa=\sqrt{2\cdot5}=\sqrt{10}\approx3.162$, and $T(a{=}1)\approx7.14\times10^{-3}$.
For a thick barrier $\sinh\kappa a\to\tfrac12 e^{\kappa a}$, so
$T\to\frac{16E(V_0-E)}{V_0^2}e^{-2\kappa a}\propto e^{-2\kappa a}$: each unit of width
multiplies $T$ by $e^{-2\kappa}=e^{-2\sqrt{10}}\approx1/560$. Indeed
`transmission_barrier(5,10,a)` gives $7.14\times10^{-3},\,1.28\times10^{-5},\,
2.30\times10^{-8}$ for $a=1,2,3$ — a $\sim$560-fold drop per unit width.

### P5.  Over-barrier resonances — when a barrier turns transparent
For $E>V_0$ show the transmission oscillates and hits $T=1$ exactly when the
barrier width is an integer number of internal half-wavelengths, $k_2a=n\pi$, i.e.
$E_n=V_0+n^2\pi^2\hbar^2/2ma^2$.
*Answer:* for $V_0=10,a=1$ the first perfect-transmission energy is
$E_1=10+\pi^2/2\approx14.93$.
*Check:* `transmission_barrier(10+np.pi**2/2, 10.0, 1.0)` $\approx1.0$; between
resonances $T<1$. (`test_barrier_over_barrier_resonances`.) *(Cf. the finite-well
transparency, Griffiths 3e Eq. 2.172, p.96 — the Ramsauer–Townsend effect.)*

**Solution.** For $E>V_0$ the inside wave is **oscillatory**,
$k_2=\sqrt{2m(E-V_0)}/\hbar$, and matching at both faces replaces $\sinh$ by $\sin$:
$$T=\Big[\,1+\frac{V_0^2\sin^2(k_2 a)}{4E(E-V_0)}\,\Big]^{-1}.$$
This dips below $1$ in general but equals $1$ exactly when $\sin(k_2a)=0$, i.e.
$k_2a=n\pi$ — the barrier holds an integer number of internal half-wavelengths and
becomes transparent. Squaring, $\frac{2m(E-V_0)}{\hbar^2}a^2=n^2\pi^2$, so
$$E_n=V_0+\frac{n^2\pi^2\hbar^2}{2ma^2}.$$
For $V_0=10,a=1,n=1$: $E_1=10+\pi^2/2\approx14.9348$, and
`transmission_barrier(10+np.pi**2/2,10,1)` returns $T=1.0$, while off-resonance
$T<1$ — the Ramsauer–Townsend resonance.

### P6.  The step: reflection, transmission, and a partial bounce  *(Griffiths 3e Prob. 2.34, p.97–98)*
For the step $V=0\,(x<0),V_0\,(x>0)$ compute $R$ and $T$. (a) For $E>V_0$ show
$R=(\frac{k_1-k_2}{k_1+k_2})^2$ and, using the **current-weighted** $T=\frac{k_2}{k_1}|F/A|^2$,
that $R+T=1$. (b) For $E<V_0$ show $R=1$ (total reflection, evanescent tail).
*Answer:* a quantum particle partially reflects even when $E>V_0$ (e.g. $E=1.5,V_0=1$:
$R\approx0.072$); only $E\gg V_0$ gives $T\to1$.
*Check:* `step_RT(1.5, 1.0)` $\approx(0.072,0.928)$, sum 1; `step_RT(0.5,1.0)`
$=(1.0,0.0)$. The transfer matrix `scatter_piecewise(E,[0,V0],[0])` agrees.
(`test_step_R_plus_T_and_transfer_matrix`, `test_step_total_reflection_below_barrier`.)

**Solution.** Write $\psi=Ae^{ik_1x}+Be^{-ik_1x}$ for $x<0$ and $\psi=Fe^{ik_2x}$ for
$x>0$, with $k_1=\sqrt{2mE}/\hbar$, $k_2=\sqrt{2m(E-V_0)}/\hbar$. Continuity of
$\psi$ and $\psi'$ at $x=0$ gives $A+B=F$ and $k_1(A-B)=k_2F$, whence
$$\frac BA=\frac{k_1-k_2}{k_1+k_2},\qquad \frac FA=\frac{2k_1}{k_1+k_2}.$$
(a) Then $R=|B/A|^2=\big(\tfrac{k_1-k_2}{k_1+k_2}\big)^2$ and, current-weighted,
$T=\tfrac{k_2}{k_1}|F/A|^2=\tfrac{4k_1k_2}{(k_1+k_2)^2}$; adding,
$R+T=\tfrac{(k_1-k_2)^2+4k_1k_2}{(k_1+k_2)^2}=1$. For $E=1.5,V_0=1$:
$k_1=\sqrt3,k_2=1$, giving $R\approx0.072$, $T\approx0.928$ — partial reflection
despite $E>V_0$. (b) For $E<V_0$, $k_2$ is imaginary, the right side is evanescent
(no current), so $R=1,T=0$. This matches `step_RT(1.5,1.0)`$\approx(0.072,0.928)$
and `step_RT(0.5,1.0)`$=(1,0)$.

### P7.  Free particle: group velocity and a spreading packet  *(Griffiths 3e §2.4, Prob. 2.22, p.74)*
For $\omega(k)=\hbar k^2/2m$, show the group velocity $v_g=d\omega/dk=\hbar k/m=p/m$
is the classical speed and is twice the phase velocity. Show a minimum-uncertainty
Gaussian of initial width $\sigma_0$ spreads as
$\sigma_x(t)=\sigma_0\sqrt{1+(\hbar t/2m\sigma_0^2)^2}$.
*Answer:* $v_g=2v_p$; the packet is narrowest at $t=0$ and broadens symmetrically.
*Check:* `group_velocity(3.0) == 2*phase_velocity(3.0)`; `gaussian_packet_sigma(0,1)`
$=1<$ `gaussian_packet_sigma(2,1)`. (`test_free_particle_dispersion_and_velocities`,
`test_gaussian_packet_spreads`.) Links to `~MA-09` (Fourier) and `~EM-15` (optical dispersion).

**Solution.** From $\omega(k)=\hbar k^2/2m$ the two velocities are
$$v_g=\frac{d\omega}{dk}=\frac{\hbar k}{m}=\frac pm,\qquad
v_p=\frac{\omega}{k}=\frac{\hbar k}{2m},$$
so $v_g=2v_p$, and $v_g=p/m$ is exactly the classical particle speed
(`group_velocity(3)`$=3=2\times$`phase_velocity(3)`). Because $\omega\propto k^2$ is
nonlinear, the component waves dephase and a minimum-uncertainty Gaussian broadens
as $\sigma_x(t)=\sigma_0\sqrt{1+(\hbar t/2m\sigma_0^2)^2}$. This is smallest at $t=0$
(where $\sigma_x=\sigma_0$) and grows symmetrically in $|t|$: with $\sigma_0=1$,
`gaussian_packet_sigma(0,1)`$=1<$`gaussian_packet_sigma(2,1)`$=\sqrt2\approx1.414$,
confirming the packet spreads.
