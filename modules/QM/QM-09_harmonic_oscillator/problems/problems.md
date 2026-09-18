# QM-09 — Problems

Work them by hand, then check with `code/oscillator.py`. Sources in `../refs.md`
(Griffiths & Schroeter 3e, §2.3). Units $\hbar=m=\omega=1$ unless stated.

### P1.  The spectrum and the zero-point energy, from the algebra alone
From $H=\hbar\omega(a^\dagger a+\tfrac12)$, $[a,a^\dagger]=1$, and the existence
of a lowest rung $a|0\rangle=0$, deduce the allowed energies and the ground-state
energy — *without ever solving a differential equation*.
*Answer:* $E_n=\hbar\omega(n+\tfrac12)$; $E_0=\tfrac12\hbar\omega\neq0$ (forced by
$[x,p]=i\hbar$ — the particle can't have $x=p=0$). *(Griffiths Eq. 2.62, p.62.)*
*Check:* `algebraic_spectrum(6)` → `[0.5 1.5 2.5 3.5 4.5 5.5]`;
`zero_point_energy()` → `0.5`. (`test_hamiltonian_spectrum_is_n_plus_half`.)

**Solution.** Let $N|n\rangle=n|n\rangle$. From $[N,a^\dagger]=a^\dagger$ and $[N,a]=-a$, the
kets $a^\dagger|n\rangle$ and $a|n\rangle$ are again $N$-eigenstates, with eigenvalues
$n+1$ and $n-1$ — the ladder. Eigenvalues cannot go negative, since
$$\langle n|N|n\rangle=\langle n|a^\dagger a|n\rangle=\lVert a|n\rangle\rVert^2\ge0\ \Rightarrow\ n\ge0.$$
So lowering must terminate at a floor with $a|0\rangle=0$, giving $N|0\rangle=0$ and
$E_0=\hbar\omega(0+\tfrac12)=\tfrac12\hbar\omega$. Climbing with $a^\dagger$ adds one
quantum at a time, so $n=0,1,2,\dots$ and $E_n=\hbar\omega(n+\tfrac12)$. The floor
$\tfrac12\hbar\omega\neq0$ because $a|0\rangle=0$ is a minimum-uncertainty state, not
$x=p=0$. Matches `algebraic_spectrum(6)`→`[0.5 1.5 2.5 3.5 4.5 5.5]` and
`zero_point_energy()`→`0.5`.

### P2.  The ladder relations
Show $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$ and $a|n\rangle=\sqrt{n}\,
|n-1\rangle$, and confirm the bottom of the ladder $a|0\rangle=0$.
*Answer:* the $\sqrt{n+1},\sqrt{n}$ factors come from normalising
$a^\dagger|n\rangle$ and $a|n\rangle$ (Griffiths Eq. 2.66, p.64).
*Check:* `creation(6) @ basis_vector(2,6)` $=\sqrt3\,|3\rangle$;
`annihilation(6) @ basis_vector(0,6)` $=0$.
(`test_raising_lowering_relations`.)

**Solution.** Since $a^\dagger|n\rangle$ has $N$-eigenvalue $n+1$, write
$a^\dagger|n\rangle=c_n|n+1\rangle$. Fix $|c_n|$ from the norm, using
$aa^\dagger=a^\dagger a+[a,a^\dagger]=N+1$:
$$\lVert a^\dagger|n\rangle\rVert^2=\langle n|aa^\dagger|n\rangle=\langle n|(N+1)|n\rangle=n+1,$$
so with the standard real-positive phase $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$.
Likewise $\lVert a|n\rangle\rVert^2=\langle n|a^\dagger a|n\rangle=n$ gives
$a|n\rangle=\sqrt{n}\,|n-1\rangle$, and at $n=0$ the factor $\sqrt0$ kills the state,
$a|0\rangle=0$. Hence `creation(6) @ basis_vector(2,6)` $=\sqrt3\,|3\rangle$ (the $\sqrt3=1.7321$
entry in slot $3$) and `annihilation(6) @ basis_vector(0,6)` $=0$.

### P3.  Why $[a,a^\dagger]=1$ is impossible for finite matrices
Prove that no finite-dimensional matrices $A,B$ can satisfy $[A,B]=\mathbb 1$.
Then explain what the truncated $D\times D$ ladder operators actually give.
*Answer:* $\operatorname{tr}[A,B]=\operatorname{tr}(AB)-\operatorname{tr}(BA)=0$,
but $\operatorname{tr}\mathbb 1=D\neq0$ — contradiction. Truncation forces the
defect into one corner: $[a,a^\dagger]=\operatorname{diag}(1,\dots,1,-(D-1))$,
identity on the interior, with the bottom-right entry $-(D-1)$ making the trace
zero. *(The infinite-dimensional relation $[a,a^\dagger]=1$ holds only in the
limit $D\to\infty$.)*
*Check:* `np.diag(commutator(annihilation(6),creation(6))).real` →
`[1 1 1 1 1 -5]`; `np.trace(...)` $=0$.
(`test_ladder_commutator_interior_is_identity`, `test_truncation_artifact_is_honest`.)

**Solution.** The trace is cyclic for any finite square matrices,
$\operatorname{tr}(AB)=\operatorname{tr}(BA)$, so
$$\operatorname{tr}[A,B]=\operatorname{tr}(AB)-\operatorname{tr}(BA)=0.$$
But $\operatorname{tr}\mathbb 1_D=D\neq0$, so $[A,B]=\mathbb 1$ cannot hold in finite
dimensions — it needs the infinite ladder. Truncating $a,a^\dagger$ to $D$ levels keeps
$[a,a^\dagger]=1$ on every interior rung, but $a^\dagger|D-1\rangle=\sqrt{D}\,|D\rangle$
is dropped, so the bottom-right entry must equal $-(D-1)$ to force the trace to zero.
For $D=6$ this is $\operatorname{diag}(1,1,1,1,1,-5)$, exactly what
`np.diag(commutator(annihilation(6),creation(6))).real`→`[1 1 1 1 1 -5]` returns, with
`np.trace(...)`$=0$.

### P4.  Orthonormality of the Hermite–Gaussians  *(Griffiths Prob. 2.10c, p.65)*
Show by explicit integration that $\psi_0,\psi_1,\psi_2$ are orthonormal:
$\int\psi_m\psi_n\,dx=\delta_{mn}$. *(Hint: exploit the parity of the integrands —
even$\times$odd integrates to zero.)*
*Answer:* the diagonal integrals are $1$ (normalisation), the off-diagonal ones
$0$ (Griffiths Eq. 2.67, p.64).
*Check:* `overlap(2,2)` ≈ 1.0, `overlap(1,2)` ≈ 0.0.
(`test_eigenfunctions_orthonormal`.)

**Solution.** The eigenfunction $\psi_k$ has parity $(-1)^k$, so the product
$\psi_m\psi_n$ has parity $(-1)^{m+n}$. When $m+n$ is odd the integrand is an odd
function and $\int_{-\infty}^\infty\psi_m\psi_n\,dx=0$ with no calculation — this kills
$(0,1),(1,2),\dots$. The diagonal terms are the normalization integrals, set to $1$ by
the prefactor $(m\omega/\pi\hbar)^{1/4}/\sqrt{2^n n!}$ together with
$\int H_n(\xi)^2e^{-\xi^2}\,d\xi=\sqrt\pi\,2^n n!$. Hence
$\int\psi_m\psi_n\,dx=\delta_{mn}$, confirmed by `overlap(2,2)`≈$1.0$ and
`overlap(1,2)`≈$0.0$.

### P5.  Build a Hermite–Gaussian and check its parity  *(Griffiths Prob. 2.10a / 2.15, pp.65, 73)*
Construct $\psi_2(x)\propto(2\xi^2-1)e^{-\xi^2/2}$ using $H_2(\xi)=4\xi^2-2$, and
state its parity. More generally, $\psi_n$ has parity $(-1)^n$, so $\psi_n(0)=0$
for odd $n$.
*Answer:* $\psi_2$ is even ($\psi_2(-x)=\psi_2(x)$); $\psi_1,\psi_3,\dots$ are odd.
*Check:* `psi(2,-x) == psi(2,x)` and `psi(1,-x) == -psi(1,x)`.
(`test_parity_of_eigenfunctions`; `psi` imports $H_n$ from `~MA-12`.)

**Solution.** With $H_2(\xi)=4\xi^2-2=2(2\xi^2-1)$, Eq. 2.85 gives
$$\psi_2(x)=\Big(\tfrac{m\omega}{\pi\hbar}\Big)^{1/4}\frac{1}{\sqrt{2^2\,2!}}\,(4\xi^2-2)\,e^{-\xi^2/2}\ \propto\ (2\xi^2-1)\,e^{-\xi^2/2},\qquad \xi=\sqrt{\tfrac{m\omega}{\hbar}}\,x.$$
Under $x\to-x$ we have $\xi\to-\xi$, but $\xi^2$ and $e^{-\xi^2/2}$ are unchanged, so
$\psi_2(-x)=\psi_2(x)$ — **even**. Generally $H_n(-\xi)=(-1)^nH_n(\xi)$, so $\psi_n$ has
parity $(-1)^n$; for odd $n$ the function is odd and $\psi_n(0)=0$. Hence
`psi(2,-x) == psi(2,x)` while `psi(1,-x) == -psi(1,x)`.

### P6.  The two methods agree
The algebraic method (diagonalise $H=\hbar\omega(N+\tfrac12)$) and the analytic
method (diagonalise the finite-difference Hamiltonian $-\tfrac12 d^2/dx^2+
\tfrac12 x^2$) are built from completely different machinery. Show they give the
same spectrum.
*Answer:* both yield $E_n=\hbar\omega(n+\tfrac12)$; the FD spectrum converges to
it as the grid refines (Griffiths: the analytic states are "identical, of course,
to the ones we obtained algebraically", p.71).
*Check:* `algebraic_spectrum(20)[:6]` vs `fd_spectrum(k=6)` — both
$\approx[0.5,1.5,2.5,3.5,4.5,5.5]$. (`test_two_methods_same_spectrum`.)

**Solution.** The algebraic route diagonalizes $H=\hbar\omega(N+\tfrac12)$ with
$N=\operatorname{diag}(0,1,2,\dots)$, returning $E_n=\hbar\omega(n+\tfrac12)$ exactly. The
analytic route discretizes $-\tfrac12 d^2/dx^2+\tfrac12 x^2$ with a 3-point Laplacian and
diagonalizes that matrix — no ladder operators anywhere. Both give the same numbers:
`algebraic_spectrum(20)[:6]`$=[0.5,1.5,2.5,3.5,4.5,5.5]$ and
`fd_spectrum(k=6)`$=[0.5,1.500,2.500,3.500,4.499,5.499]$, the tiny deficits being
$O(\Delta x^2)$ grid error that vanishes as the box refines. One spectrum, two
independent derivations.

### P7.  Each eigenfunction solves the Schrödinger equation
Verify directly that the analytic $\psi_n$ satisfies the TISE
$-\tfrac{\hbar^2}{2m}\psi_n''+\tfrac12 m\omega^2x^2\psi_n=E_n\psi_n$ with
$E_n=\hbar\omega(n+\tfrac12)$ (use a finite-difference second derivative).
*Answer:* the relative residual $\lVert H\psi_n-E_n\psi_n\rVert/\lVert\psi_n\rVert$
is $\sim10^{-4}$ and shrinks $\propto(\Delta x)^2$ — zero in the continuum limit.
*Check:* `fd_residual(0)`…`fd_residual(4)` all $<2\times10^{-3}$.
(`test_eigenfunctions_solve_fd_tise`.)

**Solution.** Sample the analytic $\psi_n$ on the grid and apply the finite-difference
Hamiltonian $H_{\rm fd}=-\tfrac12 D^2+\tfrac12 x^2$ (3-point stencil). Each $\psi_n$
solves the continuum TISE $H\psi_n=E_n\psi_n$ with $E_n=n+\tfrac12$ exactly, so the only
error is the stencil's $D^2\psi_n=\psi_n''+O(\Delta x^2)$. The relative residual is then
$$\frac{\lVert H_{\rm fd}\psi_n-E_n\psi_n\rVert}{\lVert\psi_n\rVert}=O(\Delta x^2)\ \xrightarrow{\ \Delta x\to0\ }\ 0.$$
Numerically `fd_residual(0..4)`$=\{3.0,\,8.9,\,19,\,34,\,53\}\times10^{-5}$, all
$<2\times10^{-3}$ and shrinking as the grid refines — every Hermite–Gaussian solves the
discretized Schrödinger equation.

### P8.  Expectation values and the uncertainty product  *(Griffiths Prob. 2.12, p.66)*
For the $n$th stationary state, use $x=\sqrt{\tfrac{\hbar}{2m\omega}}(a+a^\dagger)$
and $p=i\sqrt{\tfrac{\hbar m\omega}{2}}(a^\dagger-a)$ to find $\langle x\rangle,
\langle p\rangle,\langle x^2\rangle,\langle p^2\rangle$ and the product
$\sigma_x\sigma_p$.
*Answer:* $\langle x\rangle=\langle p\rangle=0$; $\langle x^2\rangle=
\tfrac{\hbar}{m\omega}(n+\tfrac12)$, $\langle p^2\rangle=\hbar m\omega(n+\tfrac12)$,
so $\sigma_x\sigma_p=\hbar(n+\tfrac12)\ge\tfrac{\hbar}{2}$ — saturated by the
ground state. *(The $\langle x^2\rangle,\langle p^2\rangle$ split $E_n$ equally
between kinetic and potential energy.)*
*Check (natural units):* the $x,p$ matrices give
$\langle n|x^2|n\rangle=\langle n|p^2|n\rangle=n+\tfrac12$ on the interior, e.g.
`v=basis_vector(2,12); x=position_operator(12); (v.conj()@(x@x)@v).real` → `2.5`.
(Built from `position_operator`/`momentum_operator`; cf.
`test_hamiltonian_from_xp_matches_ladder_form`.)

**Solution.** Write $x=\sqrt{\tfrac{\hbar}{2m\omega}}(a+a^\dagger)$ and
$p=i\sqrt{\tfrac{\hbar m\omega}{2}}(a^\dagger-a)$. Each shifts $|n\rangle$ to
$|n\pm1\rangle$, orthogonal to $|n\rangle$, so $\langle x\rangle=\langle p\rangle=0$. For
the squares only the number-conserving terms survive:
$$\langle n|(a+a^\dagger)^2|n\rangle=\langle n|(aa^\dagger+a^\dagger a)|n\rangle=(n+1)+n=2n+1,$$
giving $\langle x^2\rangle=\tfrac{\hbar}{2m\omega}(2n+1)=\tfrac{\hbar}{m\omega}(n+\tfrac12)$
and likewise $\langle p^2\rangle=\tfrac{\hbar m\omega}{2}(2n+1)=\hbar m\omega(n+\tfrac12)$.
With $\langle x\rangle=\langle p\rangle=0$, $\sigma_x\sigma_p=\sqrt{\langle x^2\rangle\langle p^2\rangle}=\hbar(n+\tfrac12)\ge\tfrac\hbar2$,
saturated at $n=0$. In natural units $n=2$ gives $\langle x^2\rangle=\langle p^2\rangle=2.5$,
matching `(v.conj()@(x@x)@v).real`→`2.5`.
