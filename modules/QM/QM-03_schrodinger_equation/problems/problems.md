# QM-03 — Problems

Work them by hand, then check with `code/schrodinger.py`. Sources in `../refs.md`.
Code units are $\hbar=m=1$; the well has width $L=1$ unless stated otherwise.

### P1.  Separation of variables  *(Griffiths 3e §2.1, p.43)*
Starting from the TDSE with a time-independent $V$, substitute $\Psi=\psi(x)
\varphi(t)$ and show that consistency forces both sides to a constant $E$, giving
$\varphi(t)=e^{-iEt/\hbar}$ and the TISE $\hat H\psi=E\psi$.
*Answer:* dividing by $\psi\varphi$ separates $t$ from $x$; a $t$-only function
equal to an $x$-only function must be constant. The time factor is the universal
"wiggle" $e^{-iEt/\hbar}$.
*Check:* the universality of the phase is exercised by `stationary_state`; e.g.
`stationary_state(psi[:,0], E[0], 2*np.pi/E[0])` returns $+\psi$ and at
`np.pi/E[0]` returns $-\psi$. (`test_stationary_state_phase_does_evolve`.)

**Solution.** Insert $\Psi=\psi(x)\varphi(t)$ into $i\hbar\,\partial_t\Psi=\hat H\Psi$. The
left side is $i\hbar\,\psi\dot\varphi$ and the right is $\varphi\big(-\tfrac{\hbar^2}{2m}\psi''+V\psi\big)$;
divide through by $\psi\varphi$:
$$i\hbar\,\frac{\dot\varphi}{\varphi}=\frac1\psi\Big(-\frac{\hbar^2}{2m}\psi''+V\psi\Big).$$
The left depends only on $t$, the right only on $x$, so for the equality to hold for *all*
$x,t$ both must equal one constant $E$. The time half integrates to
$\dot\varphi=-\tfrac{iE}{\hbar}\varphi\Rightarrow\varphi(t)=e^{-iEt/\hbar}$, and the space half
is the TISE $\hat H\psi=E\psi$. Every separable state shares this phase: with $\hbar=1$,
$t=\pi/E$ gives $e^{-i\pi}=-1$ (returns $-\psi$) and $t=2\pi/E$ gives $e^{-2\pi i}=1$
(returns $+\psi$) — exactly what `stationary_state(psi[:,0], E[0], ...)` produces.

### P2.  The infinite-well spectrum, numerically  *(Griffiths 3e §2.2, pp.49–50)*
Solve the TISE for $V=0$ on $[0,L]$ with $\psi(0)=\psi(L)=0$ and recover the
lowest five levels. Compare to $E_n=n^2\pi^2\hbar^2/2mL^2$.
*Answer:* $E_n=n^2\pi^2/2$ for $L=\hbar=m=1$: $4.93,\,19.74,\,44.41,\,78.96,\,
123.37$. The finite-difference grid reproduces them to $<0.02\%$.
*Check:* `E,psi = solve(make_grid(0,1,400))`; `E[0]` ≈ `infinite_well_energy(1,1)`
≈ 4.9348. (`test_infinite_well_energies`.)

**Solution.** Inside the well $V=0$, so the TISE is $-\tfrac{\hbar^2}{2m}\psi''=E\psi$, i.e.
$\psi''=-k^2\psi$ with $k=\sqrt{2mE}/\hbar$. The general solution $A\sin kx+B\cos kx$ must
vanish at $x=0$ (so $B=0$) and at $x=L$, forcing $\sin kL=0$, i.e. $k_nL=n\pi$. Hence
$$E_n=\frac{\hbar^2k_n^2}{2m}=\frac{n^2\pi^2\hbar^2}{2mL^2}\;\xrightarrow{\;L=\hbar=m=1\;}\;\frac{n^2\pi^2}{2}.$$
For $n=1\ldots5$ this is $4.9348,\,19.7392,\,44.4132,\,78.9568,\,123.3701$. The 400-point
finite-difference grid returns $4.9348,\,19.7388,\,44.4112,\,78.9504,\,123.354$ — agreeing to
$<0.02\%$, and `E[0]` $\approx$ `infinite_well_energy(1,1)` $\approx 4.9348$.

### P3.  Well eigenfunctions and orthonormality  *(Griffiths 3e §2.2, pp.50–51)*
Show the eigenstates are $\psi_n=\sqrt{2/L}\sin(n\pi x/L)$ and that
$\langle\psi_m|\psi_n\rangle=\delta_{mn}$.
*Answer:* the ground-state density is $(2/L)\sin^2(\pi x/L)$, peaking at $2/L=2$
at $x=L/2$; distinct states are orthogonal.
*Check:* `prob_density(psi[:,0])` matches `infinite_well_eigenfunction(1,x,1)**2`
to $<10^{-4}$, and `inner_product(psi[:,0], psi[:,1], dx)` ≈ 0.
(`test_infinite_well_eigenfunction_shape`, `test_eigenstates_orthonormal`.)

**Solution.** Normalizing $\psi_n=A\sin(n\pi x/L)$: $\int_0^L A^2\sin^2(n\pi x/L)\,dx=A^2\tfrac
L2=1$ gives $A=\sqrt{2/L}$, so $\psi_n=\sqrt{2/L}\sin(n\pi x/L)$. Orthogonality uses the
product-to-sum identity:
$$\int_0^L\!\sin\tfrac{m\pi x}{L}\sin\tfrac{n\pi x}{L}\,dx=\tfrac12\!\int_0^L\!\Big[\cos\tfrac{(m-n)\pi x}{L}-\cos\tfrac{(m+n)\pi x}{L}\Big]dx=\tfrac L2\,\delta_{mn},$$
since each cosine integrates to zero unless $m=n$. Thus $\langle\psi_m|\psi_n\rangle=\delta_{mn}$.
The ground density $|\psi_1|^2=(2/L)\sin^2(\pi x/L)$ peaks at $x=L/2$ where $\sin^2=1$, giving
$2/L=2$. The grid confirms `max prob_density(psi[:,0]) = 2.0` and
`inner_product(psi[:,0], psi[:,1], dx)` $\approx-1.4\times10^{-16}$.

### P4.  Why a stationary state is "stationary"  *(Griffiths 3e §2.1, p.46)*
For a single eigenstate, show $|\Psi(x,t)|^2$ is independent of $t$, even though
$\Psi$ itself is not.
*Answer:* $|\psi_n e^{-iE_nt/\hbar}|^2=|\psi_n|^2$; the phase $e^{-iE_nt/\hbar}$
has unit modulus, so every observable is frozen while the phase still rotates.
*Check:* `prob_density(stationary_state(psi[:,0],E[0],t))` is the same to
$\sim10^{-16}$ for any $t$. (`test_stationary_state_density_time_independent`.)

**Solution.** A single separable state is $\Psi_n(x,t)=\psi_n(x)\,e^{-iE_nt/\hbar}$. Its Born
density factorizes the modulus:
$$|\Psi_n(x,t)|^2=|\psi_n(x)|^2\,\big|e^{-iE_nt/\hbar}\big|^2=|\psi_n(x)|^2\cdot1,$$
because $|e^{-iE_nt/\hbar}|^2=e^{-iE_nt/\hbar}\,e^{+iE_nt/\hbar}=1$ ($E_n$ is real). So the
density — and hence every probability and every expectation of a time-independent operator —
is frozen, even though $\Psi$ itself keeps rotating in phase at rate $E_n/\hbar$. That is the
sense of "stationary." The code confirms `prob_density(stationary_state(psi[:,0],E[0],t))` is
$t$-independent to $\sim10^{-16}$.

### P5.  Two-state superposition and the Bohr beat  *(Griffiths 3e Problem 2.5, p.55)*
A particle starts as an even mixture of the first two stationary states,
$\Psi(x,0)=\tfrac1{\sqrt2}(\psi_1+\psi_2)$. Find $|\Psi(x,t)|^2$ and $\langle x
\rangle(t)$, and give the **angular frequency** of the oscillation.
*Answer:* $|\Psi|^2=\tfrac12[\psi_1^2+\psi_2^2+2\psi_1\psi_2\cos\omega t]$ with
$\omega=(E_2-E_1)/\hbar=3\pi^2\hbar/2mL^2\approx14.80$; $\langle x\rangle$
oscillates about $L/2$ with period $T=2\pi/\omega\approx0.4244$.
*Check:* `superposition_period(E[1],E[0])` ≈ 0.4244; sampling $\langle x\rangle(t)$
and calling `measure_period` returns the same to $<1\%$.
(`test_superposition_period_matches_bohr_frequency`,
`test_superposition_revival_and_time_dependence`.)

**Solution.** Each term evolves with its own phase, so
$\Psi(x,t)=\tfrac1{\sqrt2}\big(\psi_1e^{-iE_1t/\hbar}+\psi_2e^{-iE_2t/\hbar}\big)$. With real
$\psi_1,\psi_2$ the density is
$$|\Psi|^2=\tfrac12\Big[\psi_1^2+\psi_2^2+2\psi_1\psi_2\cos\tfrac{(E_2-E_1)t}{\hbar}\Big],$$
the cross-term reducing to a cosine because only the *relative* phase
$e^{-i(E_2-E_1)t/\hbar}$ survives. The beat angular frequency is
$\omega=(E_2-E_1)/\hbar=(4-1)\pi^2/2=3\pi^2/2\approx14.80$, so $\langle x\rangle$ oscillates
about $L/2$ with period $T=2\pi/\omega\approx0.4244$. This matches
`superposition_period(E[1],E[0])` $\approx0.4244$ and `measure_period` on the sampled
$\langle x\rangle(t)$.

### P6.  Fourier's trick and the meaning of the $c_n$  *(Griffiths 3e §2.1 p.47, §2.2 p.51)*
Given $\Psi(x,0)=0.6\,\psi_1+0.8\,\psi_5$, recover the coefficients $c_n$ and the
probabilities of each energy outcome.
*Answer:* $c_n=\int\psi_n^\ast\Psi_0\,dx$ gives $c_1=0.6,\,c_5=0.8$; the
probabilities are $|c_1|^2=0.36$ and $|c_5|^2=0.64$, summing to 1. A measurement
of the energy yields $E_1$ 36% of the time and $E_5$ 64% of the time, and
$\langle H\rangle=0.36E_1+0.64E_5$ is constant in time.
*Check:* `coefficients(psi, Psi0, dx)` returns those $c_n$, `psi @ c`
reconstructs $\Psi_0$, and $\sum|c_n|^2=1$. (`test_coefficients_recovered`.)

**Solution.** Fourier's trick projects onto the orthonormal eigenbasis: multiply
$\Psi_0=\sum_m c_m\psi_m$ by $\psi_n^\ast$ and integrate, using
$\langle\psi_n|\psi_m\rangle=\delta_{nm}$:
$$c_n=\int\psi_n^\ast(x)\,\Psi_0(x)\,dx=\langle\psi_n|\Psi_0\rangle.$$
For $\Psi_0=0.6\,\psi_1+0.8\,\psi_5$ only the matching terms survive, so $c_1=0.6$, $c_5=0.8$
(all others $0$); note $0.6^2+0.8^2=1$, so $\Psi_0$ is already normalized. The Born rule for
energy gives $|c_1|^2=0.36$ and $|c_5|^2=0.64$, summing to $1$, and
$\langle H\rangle=0.36\,E_1+0.64\,E_5$ — constant, since the $c_n$ never change. The code
returns exactly `c1=0.6, c5=0.8`, `sum|c_n|^2 = 1.0`, and `psi @ c` rebuilds $\Psi_0$.

### P7.  Same solver, the harmonic oscillator  *(Griffiths 3e §2.3, p.57; ~QM-09)*
Replace $V=0$ with $V=\tfrac12 m\omega^2x^2$ and recover the oscillator ladder
$E_n=(n+\tfrac12)\hbar\omega$.
*Answer:* with $\hbar=m=\omega=1$, $E_n=n+\tfrac12$: $0.5,1.5,2.5,3.5,4.5$, equally
spaced by $\hbar\omega=1$. The same finite-difference routine reproduces them to
$\sim0.1\%$ — the bridge to the analytic/ladder treatment in `~QM-09`.
*Check:* `Eh,_ = solve(make_grid(-8,8,800), V=lambda x: 0.5*x**2)`; `Eh[0]` ≈ 0.5,
`Eh[4]` ≈ 4.5. (`test_harmonic_oscillator_energies`.)

**Solution.** The Hamiltonian assembly $H=-\tfrac{\hbar^2}{2m}\,\mathrm{tridiag}(1,-2,1)/(\Delta
x)^2+\mathrm{diag}\,V_i$ is agnostic to $V$, so swapping the flat $V=0$ for the parabola
$V=\tfrac12 m\omega^2x^2$ and re-diagonalizing solves the *oscillator* TISE
$-\tfrac{\hbar^2}{2m}\psi''+\tfrac12 m\omega^2x^2\psi=E\psi$. Its exact spectrum (derived
analytically with ladder operators in `~QM-09`) is
$$E_n=\big(n+\tfrac12\big)\hbar\omega,\qquad n=0,1,2,\dots$$
With $\hbar=m=\omega=1$ this is $0.5,1.5,2.5,3.5,4.5$ — equally spaced by $\hbar\omega=1$. The
grid run on $[-8,8]$ returns $0.5,1.4999,2.4998,3.4997,4.4995$ ($\sim0.1\%$), so `Eh[0]`
$\approx0.5$ and `Eh[4]` $\approx4.5$.
