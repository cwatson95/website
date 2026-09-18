# QM-19 — Problems

Work them by hand, then check with `code/propagator.py`. Sources in `../refs.md`.
Natural units $\hbar=m=1$ throughout.

### P1.  The free propagator: amplitude and classical-action phase  *(Griffiths 3e, Prob. 6.30(d), p.342)*
Write down $K_0(x,t;x',0)$. Show its modulus is independent of position, and that
its phase (stripped of the constant prefactor) equals the classical action
$S_{\rm cl}=m(x-x')^2/2t$ of the straight-line path. What constant phase does the
$\sqrt{i}$ prefactor contribute?
*Answer:* $|K_0|=\sqrt{m/2\pi\hbar t}$; phase $=S_{\rm cl}/\hbar$; the prefactor
$=e^{-i\pi/4}/\sqrt{2\pi\hbar t/m}$ adds the Maslov phase $-\pi/4$.
*Check:* `free_propagator(np.array([1.0]),-0.5,0.8)`; compare $|K_0|$ to
`1/np.sqrt(2*np.pi*0.8)` and `np.angle(K)+np.pi/4` to
`classical_action_free(1.0,-0.5,0.8)`. (`test_free_propagator_closed_form`.)

**Solution.** The kernel is $K_0=\sqrt{\tfrac{m}{2\pi i\hbar t}}\,\exp\!\big[\tfrac{im(x-x')^2}{2\hbar t}\big]$.
The exponent is purely imaginary, so $|e^{iS/\hbar}|=1$ and the modulus lives entirely in
the prefactor; since $|1/\sqrt{i}|=1$,
$$|K_0|=\sqrt{\tfrac{m}{2\pi\hbar t}},$$
**independent of $x,x'$** — every endpoint is reached with equal amplitude, all the physics
is in the phase. That phase is $\tfrac{m(x-x')^2}{2\hbar t}=S_{\rm cl}/\hbar$, the action of the
straight-line path. Finally $1/\sqrt{i}=e^{-i\pi/4}$, so the prefactor adds the Maslov phase
$-\pi/4$. Numerically `free_propagator(np.array([1.0]),-0.5,0.8)` $=0.36279+0.25947i$ with
$|K_0|=0.44603=1/\sqrt{2\pi\cdot0.8}$ and $\arg K_0+\pi/4=1.40625=$ `classical_action_free(1.0,-0.5,0.8)`.

### P2.  $K_0$ is a nascent delta function  *(Griffiths 3e, §2.4, p.74)*
Show that as $t\to0$ the free propagator collapses to $\delta(x-x')$, in the sense
that $\int K_0(x,t;x')\,g(x')\,dx'\to g(x)$ for smooth $g$. Why must the
verification use a *decreasing* sequence of $t$?
*Answer:* $K_0$ is a complex Gaussian of width $\sim\sqrt{\hbar t/m}$ and unit
integral; as $t\to0$ it concentrates at $x'=x$. The convolution error is
$O(t\,g'')$, so it shrinks as $t\to0$.
*Check:* with $g$ a unit Gaussian, the convolution error at $t=0.2,0.1,0.05,0.02$
decreases monotonically to $<10^{-2}$. (`test_free_propagator_delta_limit`.)

**Solution.** $K_0(x,t;x')$ is a complex Gaussian in $x-x'$ of width $\sim\sqrt{\hbar t/m}$ with
unit integral, $\int K_0\,dx'=1$. Expanding a smooth $g$ about $x$ inside the convolution,
$$\int K_0(x,t;x')\,g(x')\,dx'=g(x)+\tfrac{i\hbar t}{2m}\,g''(x)+O(t^2),$$
because the Gaussian's second moment is $\propto t$. As $t\to0$ the kernel concentrates at
$x'=x$ and the integral returns $g(x)$ — a nascent $\delta(x-x')$. The leading error is
$O(t\,g'')$, **linear in $t$**, so it only shrinks for *decreasing* $t$; a fixed or growing $t$
would not converge. The check confirms this: at $t=0.2,0.1,0.05,0.02$ the errors are
$\{3.07,\,1.54,\,0.77,\,0.31\}\times10^{-2}$ — halving as $t$ halves, monotone down to $<10^{-2}$.

### P3.  The composition (semigroup) law  *(Griffiths 3e, Prob. 6.30(a), p.342)*
Prove $\int K_0(x,t_2;y)\,K_0(y,t_1;x')\,dy=K_0(x,t_1+t_2;x')$ — propagating in two
hops equals propagating in one. (It is the Gaussian-convolution statement of
$e^{-i\hat Ht_2}e^{-i\hat Ht_1}=e^{-i\hat H(t_1+t_2)}$.)
*Answer:* the $y$-integral is Gaussian; completing the square reproduces $K_0$ at
time $t_1+t_2$.
*Check:* the convolution at $t_1=0.5,\ t_2=0.3$ reproduces
`free_propagator(...,0.8)` to $<10^{-2}$ (the residual is real-time Fresnel
truncation, not a physics error). (`test_free_propagator_composition`.)

**Solution.** The $y$-integral is Gaussian. Combining the two exponents,
$\tfrac{im}{2\hbar}\big[\tfrac{(x-y)^2}{t_2}+\tfrac{(y-x')^2}{t_1}\big]$, and completing the
square in $y$ gives a $y$-independent remainder $\tfrac{im(x-x')^2}{2\hbar(t_1+t_2)}$ plus a
Gaussian in $y$. Doing the Fresnel integral, its $\sqrt{2\pi i\hbar\,t_1t_2/m(t_1+t_2)}$ exactly
cancels one factor in the product of prefactors:
$$\sqrt{\tfrac{m}{2\pi i\hbar t_2}}\sqrt{\tfrac{m}{2\pi i\hbar t_1}}\sqrt{\tfrac{2\pi i\hbar\,t_1t_2}{m(t_1+t_2)}}=\sqrt{\tfrac{m}{2\pi i\hbar(t_1+t_2)}},$$
reproducing $K_0(x,t_1+t_2;x')$ — the Gaussian-convolution form of
$e^{-i\hat Ht_2}e^{-i\hat Ht_1}=e^{-i\hat H(t_1+t_2)}$. Numerically with $t_1=0.5,t_2=0.3$ the
convolution gives $0.36117+0.26176i$ vs the closed form $K_0(\dots,0.8)=0.36279+0.25947i$, a
$2.8\times10^{-3}$ residual that is real-time Fresnel-truncation, not physics.

### P4.  A Gaussian packet spreads — propagator vs direct evolution  *(Griffiths 3e, Prob. 2.21, p.76)*
Propagate $\Psi(x,0)=(2\pi\sigma^2)^{-1/4}e^{-(x-x_0)^2/4\sigma^2+ip_0x}$ with
$K_0$. Find the centre and width of $|\Psi(x,t)|^2$, and confirm they match an
independent (split-step FFT) evolution of the Schrödinger equation.
*Answer:* centre $=x_0+p_0t/m$ (group velocity), width
$\sigma(t)=\sigma\sqrt{1+(\hbar t/2m\sigma^2)^2}$.
*Check:* `propagate(gaussian_packet(xs,x0,p0,sigma),xs,t)` vs
`evolve_free_spectral(...)` agree to $\sim10^{-14}$; `packet_center_width`
reproduces the formulas. (`test_gaussian_packet_vs_spectral`,
`test_gaussian_packet_spreading`.)

**Solution.** Propagating a Gaussian by $\Psi(x,t)=\int K_0(x,t;x')\Psi(x',0)\,dx'$ is again a
Gaussian integral, so $|\Psi(x,t)|^2$ stays Gaussian. The mean momentum $p_0$ rides through
unchanged, so the centroid moves ballistically at the group velocity,
$$\langle x\rangle_t=x_0+\tfrac{p_0}{m}t,\qquad
\sigma(t)=\sigma\sqrt{1+\Big(\tfrac{\hbar t}{2m\sigma^2}\Big)^2},$$
the width growing because the packet's momentum spread $\hbar/2\sigma$ disperses it. In natural
units $\hbar=m=1$: at $t=1,3$ with $x_0=-3,p_0=1.5,\sigma=1$, `packet_center_width` returns
centres $-1.5,\,+1.5$ ($=x_0+p_0t$) and widths $1.118,\,1.803$, matching
$\sigma\sqrt{1+(t/2)^2}$. And `propagate(...)` agrees with the independent split-step FFT
`evolve_free_spectral(...)` to $\sim10^{-14}$ — two algorithms, one $\Psi(x,t)$.

### P5.  The harmonic-oscillator propagator (Mehler)  *(Griffiths 3e, Prob. 6.30(b), p.342)*
Quote the Mehler kernel for the oscillator. Show it (a) reduces to $K_0$ as
$\omega\to0$ and (b) satisfies the oscillator Schrödinger equation
$i\partial_tK=(-\tfrac12\partial_x^2+\tfrac12\omega^2x^2)K$.
*Answer:* with $\sin\omega t\to\omega t$, $\cos\omega t\to1$ the prefactor and
exponent become those of $K_0$; the TDSE residual is zero.
*Check:* `harmonic_propagator(...,omega=1e-5)` ≈ `free_propagator(...)`; finite
differences give a TDSE residual $\sim10^{-9}$. (`test_harmonic_free_limit`,
`test_harmonic_satisfies_schrodinger`.)

**Solution.** Mehler's kernel is
$K=\sqrt{\tfrac{m\omega}{2\pi i\hbar\sin\omega t}}\,\exp\!\big\{\tfrac{im\omega}{2\hbar\sin\omega t}[(x^2+x'^2)\cos\omega t-2xx']\big\}$.
**(a)** As $\omega\to0$, $\sin\omega t\to\omega t$ and $\cos\omega t\to1$, so the prefactor
$\to\sqrt{\tfrac{m}{2\pi i\hbar t}}$ and the bracket $\to(x^2+x'^2)-2xx'=(x-x')^2$, giving the
free phase $\tfrac{im(x-x')^2}{2\hbar t}$ — exactly $K_0$. **(b)** Since $K$ is built from the
oscillator's stationary states it solves
$i\hbar\partial_tK=(-\tfrac{\hbar^2}{2m}\partial_x^2+\tfrac12 m\omega^2x^2)K$. The checks bear
both out: `harmonic_propagator(...,omega=1e-5)` differs from `free_propagator(...)` by
$4.6\times10^{-12}$, and the finite-difference TDSE residual is $7.0\times10^{-9}$ — zero up to
stencil error.

### P6.  The path integral converges to the propagator  *(Sakurai Ch. 2, unpinned; verification = code)*
Build the time-sliced path integral. For the free particle, show the $N=1,2$
sums-over-paths already reproduce $K_0$. Then explain why a *real-time* grid sum
is numerically fragile, and show that the **Wick-rotated** Trotter product
converges to the closed-form kernel as $N\to\infty$ for $V=\tfrac12\omega^2x^2$.
*Answer:* each free slice is an exact Gaussian, so the free sum is exact for every
$N$; the real-time kernel has constant modulus (no damping → sign problem); in
imaginary time $t\to-i\tau$ the heat kernel damps and the Strang–Trotter error is
$O(1/N^2)$.
*Check:* `path_integral_realtime_free(1.0,-0.5,0.8,N)` for $N=1,2$ matches $K_0$;
`path_integral_euclidean(...,N,lambda z:0.5*z**2,...)` error falls monotonically
with $N=1,4,16,64$ to $<10^{-3}$. (`test_path_integral_free_realtime`,
`test_path_integral_euclidean_harmonic_converges`.)

**Solution.** Slicing $[0,t]$ into $N$ steps and inserting completeness at each gives
$K=\int\!\prod dx_k\prod_k k_\varepsilon(x_{k+1};x_k)$ with the free short-step kernel
$k_\varepsilon$. Each intermediate integral is Gaussian and, by the semigroup law of P3,
collapses exactly back to $K_0$ — so for the **free** particle the sum is exact for *every* $N$
(`path_integral_realtime_free` matches $K_0$ to $0$ at $N=1$, to $3\times10^{-3}$ at $N=2$, the
residual being finite-$R$ truncation). The trouble is that the real-time integrand has
**constant modulus** $|e^{iS/\hbar}|=1$ and never damps — convergence rests on fragile
stationary-phase cancellation (the sign problem). Wick-rotating $t\to-i\tau$ turns
$e^{iS/\hbar}$ into the positive, decaying heat kernel $e^{-S_E/\hbar}$, and the Strang–Trotter
product $(D_{V/2}FD_{V/2})^N\to e^{-\tau\hat H}$ with error $O(1/N^2)$. For $V=\tfrac12\omega^2x^2$
the errors at $N=1,4,16,64$ are $\{9.5\times10^{-3},6.7\times10^{-4},4.3\times10^{-5},2.7\times10^{-6}\}$,
falling $\sim16\times$ per $4\times$ refinement — the advertised $O(1/N^2)$ — to $<10^{-3}$.

### P7.  The eigenfunction-sum propagator for a box  *(Griffiths 3e, Prob. 6.30 / Eq. 6.79, p.342; §2.2, p.49)*
For the infinite well on $[0,L]$, write $K=\sum_n\psi_n(x)\psi_n^*(x')e^{-iE_nt}$.
Verify that at $t=0$ it is the completeness relation ($\to\delta$) and that it
carries an eigenstate $\psi_m$ forward by a pure phase $e^{-iE_mt}$.
*Answer:* orthonormality gives $\int K\,\psi_m\,dx'=e^{-iE_mt}\psi_m(x)$;
truncating at $n_{\max}$ is exact for $m\le n_{\max}$.
*Check:* `box_propagator(0.4,Lx,t,60)` integrated against `box_eigenfunction(m,Lx)`
equals `exp(-1j*box_energy(m)*t)*box_eigenfunction(m,0.4)` to $\sim10^{-15}$, and
the $t=0$ sum reconstructs a smooth test function (improving with $n_{\max}$).
(`test_box_eigensum_propagates`.)

**Solution.** With $\psi_n(x)=\sqrt{2/L}\sin(n\pi x/L)$ and $E_n=n^2\pi^2\hbar^2/2mL^2$, write
$K=\sum_n\psi_n(x)\psi_n^*(x')e^{-iE_nt/\hbar}$. **At $t=0$** every phase is $1$ and the sum is
the completeness relation $\sum_n\psi_n(x)\psi_n^*(x')=\delta(x-x')$, so $\int K\,g\,dx'\to g(x)$
(sharper as $n_{\max}$ grows). **For an eigenstate** $\psi_m$, orthonormality
$\int\psi_n^*\psi_m\,dx'=\delta_{nm}$ collapses the sum to its single $n=m$ term:
$$\int K(x,t;x')\,\psi_m(x')\,dx'=\sum_n\psi_n(x)e^{-iE_nt/\hbar}\delta_{nm}=e^{-iE_mt/\hbar}\psi_m(x),$$
a pure phase, and truncation is exact once $m\le n_{\max}$. The check confirms it: for
$m=1,2,3$, `box_propagator(0.4,Lx,0.5,60)` integrated against `box_eigenfunction(m,Lx)` equals
$e^{-iE_m\cdot0.5}\psi_m(0.4)$ to $\sim10^{-15}$ (e.g. $m=1$: $-1.05073-0.83964i$ either way).

### P8.  The propagator IS a Green's function — the `~MA-14` link  *(Griffiths 3e, p.503; import MA-14)*
Argue that $G^R=\theta(t)K$ solves $(i\partial_t-\hat H)G^R=i\delta(x-x')\delta(t)$.
Then show the static ($E\to0$) resolvent $\sum_n\psi_n(x)\psi_n^*(x')/E_n$ is the
Green's function of $\hat H$, and that for the box it equals **twice** MA-14's
`green_dirichlet` (because $\hat H=-\tfrac12\partial_x^2=\tfrac12 L_{\rm MA14}$).
*Answer:* the $\theta$-step's derivative supplies $\delta(t)$; replacing
$e^{-iE_nt}\to1/E_n$ in the eigen-sum gives $\hat H^{-1}$; $\hat H^{-1}=2L^{-1}$
so the kernel is $2\,x_<(1-x_>)$.
*Check:* `box_resolvent_static(x,xp,N)` $= 2\cdot$`green_series(x,xp,N)` to
$10^{-10}$ for all $N$, and $\to 2\cdot$`green_dirichlet(x,xp)` as $N\to\infty$.
(`test_ma14_resolvent_link`.)

**Solution.** With $G^R=\theta(t)K$, the product rule gives
$i\hbar\partial_tG^R=i\hbar\,\delta(t)\,K(x,0;x')+\theta(t)\,i\hbar\partial_tK$. For $t>0$ the
kernel solves the homogeneous TDSE, $\theta(i\hbar\partial_t-\hat H)K=0$; and
$K(x,0;x')=\delta(x-x')$, so
$$(i\hbar\partial_t-\hat H)G^R=i\hbar\,\delta(t)\,\delta(x-x'),$$
the retarded Green's function (the $\theta$-step's derivative supplies $\delta(t)$, exactly as
MA-14's causal Green's function does). Replacing $e^{-iE_nt/\hbar}\to1/E_n$ in the eigen-sum
gives $\sum_n\psi_n(x)\psi_n^*(x')/E_n=\langle x|\hat H^{-1}|x'\rangle$. For the box
$\hat H=-\tfrac12\partial_x^2=\tfrac12 L_{\rm MA14}$, so $\hat H^{-1}=2L^{-1}$ and the kernel is
$2\,x_<(1-x_>)$. The check matches term-by-term: at $(0.3,0.7)$, `box_resolvent_static`
$=2\cdot$`green_series` to $\lesssim10^{-16}$ and both $\to0.180000=2\cdot(0.3)(1-0.7)=2\,$`green_dirichlet`.
