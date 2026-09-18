# QO-01 — Problems

Work each by hand, then check with `code/quantized_light.py`. Citations in
`../refs.md`; **SZ** = Scully & Zubairy, *Quantum Optics* (Ch.1–2), cited at
section level. Units $\hbar=\omega=1$, so $E_n=n+\tfrac12$.

### P1.  The mode is an oscillator: spectrum & zero-point  *(SZ §1.1)*
Starting from $H=\hbar\omega(a^\dagger a+\tfrac12)$, $[a,a^\dagger]=1$, and the
existence of a lowest rung $a|0\rangle=0$, deduce the allowed energies and the
ground-state (vacuum) energy — without solving any differential equation, exactly
as in `~QM-09`. Why is $E_0\neq0$, and what does $\tfrac12\hbar\omega$ mean for a
mode containing *no photons*?
*Answer:* $E_n=\hbar\omega(n+\tfrac12)$; $E_0=\tfrac12\hbar\omega$ is the
zero-point energy — the field still fluctuates in vacuum (forced by
$[a,a^\dagger]=1$).
*Check:* `number(8)` is $\mathrm{diag}(0,\dots,7)$; `energy(n)` $=n+0.5$;
`zero_point_energy()` $=0.5$.

**Solution.** Let $\hat n|n\rangle=n|n\rangle$. From $[\hat n,\hat a^\dagger]=\hat a^\dagger$
and $[\hat n,\hat a]=-\hat a$, the kets $\hat a^\dagger|n\rangle$ and $\hat a|n\rangle$ are
again $\hat n$-eigenstates with eigenvalues $n\pm1$ — the photon ladder. Eigenvalues cannot
go negative, since
$$\langle n|\hat n|n\rangle=\langle n|\hat a^\dagger\hat a|n\rangle=\lVert \hat a|n\rangle\rVert^2\ge0\ \Rightarrow\ n\ge0.$$
So lowering must terminate at a floor with $\hat a|0\rangle=0$, giving $\hat n|0\rangle=0$ and
$E_0=\hbar\omega(0+\tfrac12)=\tfrac12\hbar\omega$. Raising with $\hat a^\dagger$ adds one
photon at a time, so $n=0,1,2,\dots$ and $E_n=\hbar\omega(n+\tfrac12)$. The floor is nonzero
because $[\hat a,\hat a^\dagger]=1$ forbids $\hat a|0\rangle$ and the energy from vanishing
together: even with **no photons** the mode carries the vacuum energy $\tfrac12\hbar\omega$,
the measurable zero-point fluctuation of the field. Matches `number(8)`$=\mathrm{diag}(0,\dots,7)$,
`energy(n)`$=n+0.5$, and `zero_point_energy()`$=0.5$.

### P2.  Ladder relations and the vacuum  *(SZ §1.2)*
Show $a|n\rangle=\sqrt n\,|n-1\rangle$, $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$,
and that lowering terminates at $a|0\rangle=0$. Hence build $|n\rangle=
(a^\dagger)^n/\sqrt{n!}\,|0\rangle$ and confirm orthonormality $\langle m|n\rangle
=\delta_{mn}$. *Answer:* the $\sqrt n,\sqrt{n+1}$ factors come from normalising
$a|n\rangle$, $a^\dagger|n\rangle$ (use $aa^\dagger=N+1$).
*Check:* `creation(12) @ fock_state(2,12)` $=\sqrt3\,|3\rangle$ (entry
$1.7321$ in slot 3); `annihilation(12) @ fock_state(0,12)` $=0$; and
$\langle m|n\rangle=\delta_{mn}$ via `fock_state` dot products.

**Solution.** Since $\hat a^\dagger|n\rangle$ has number eigenvalue $n+1$, write
$\hat a^\dagger|n\rangle=c_n|n+1\rangle$ and fix $|c_n|$ from the norm, using
$\hat a\hat a^\dagger=\hat a^\dagger\hat a+[\hat a,\hat a^\dagger]=\hat n+1$:
$$\lVert \hat a^\dagger|n\rangle\rVert^2=\langle n|\hat a\hat a^\dagger|n\rangle=\langle n|(\hat n+1)|n\rangle=n+1,$$
so with the standard real-positive phase $\hat a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$.
Likewise $\lVert \hat a|n\rangle\rVert^2=\langle n|\hat a^\dagger\hat a|n\rangle=n$ gives
$\hat a|n\rangle=\sqrt n\,|n-1\rangle$, and at $n=0$ the factor $\sqrt0$ kills the state:
$\hat a|0\rangle=0$. Iterating the raising relation builds
$|n\rangle=(\hat a^\dagger)^n/\sqrt{n!}\,|0\rangle$, and because the $|n\rangle$ are eigenstates
of the Hermitian $\hat n$ with distinct eigenvalues they are orthogonal,
$\langle m|n\rangle=\delta_{mn}$. Hence `creation(12) @ fock_state(2,12)`$=\sqrt3\,|3\rangle$
(the entry $\sqrt3=1.7321$ in slot $3$) and `annihilation(12) @ fock_state(0,12)`$=0$.

### P3.  The coherent state is an eigenstate of $a$  *(SZ §2.2)*
For $|\alpha\rangle=e^{-|\alpha|^2/2}\sum_n \alpha^n/\sqrt{n!}\,|n\rangle$, apply
$a$ term by term (using $a|n\rangle=\sqrt n|n-1\rangle$) and show
$a|\alpha\rangle=\alpha|\alpha\rangle$. Where does the $e^{-|\alpha|^2/2}$ prefactor
come from? *Answer:* it normalises the state, $\langle\alpha|\alpha\rangle=1$;
shifting the summation index reproduces the same series times $\alpha$.
*Check:* `annihilation(60) @ coherent_state(2.0,60)` equals `2.0 *
coherent_state(2.0,60)` to $\sim10^{-16}$ (the residual norm
`test_coherent_is_eigenstate_of_annihilation` checks is $<10^{-9}$).

**Solution.** Apply $\hat a$ term by term with $\hat a|n\rangle=\sqrt n\,|n-1\rangle$; the
$n=0$ term drops out:
$$\hat a|\alpha\rangle=e^{-|\alpha|^2/2}\sum_{n=1}^{\infty}\frac{\alpha^n}{\sqrt{n!}}\sqrt n\,|n-1\rangle=e^{-|\alpha|^2/2}\sum_{n=1}^{\infty}\frac{\alpha^n}{\sqrt{(n-1)!}}\,|n-1\rangle,$$
using $\sqrt n/\sqrt{n!}=1/\sqrt{(n-1)!}$. Relabel $m=n-1$ and pull out one factor of $\alpha$:
$$\hat a|\alpha\rangle=\alpha\,e^{-|\alpha|^2/2}\sum_{m=0}^{\infty}\frac{\alpha^m}{\sqrt{m!}}\,|m\rangle=\alpha\,|\alpha\rangle.$$
The prefactor is exactly the normalization,
$\langle\alpha|\alpha\rangle=e^{-|\alpha|^2}\sum_n|\alpha|^{2n}/n!=e^{-|\alpha|^2}e^{|\alpha|^2}=1$.
So $|\alpha\rangle$ is the eigenstate of $\hat a$ with eigenvalue $\alpha$, confirmed by
`annihilation(60) @ coherent_state(2.0,60)`$=2.0\times$`coherent_state(2.0,60)` to a residual
$\sim10^{-16}$ — well under the $10^{-9}$ the test allows.

### P4.  Poisson statistics and the Mandel $Q$  *(SZ §2.3–2.4)*
From $P(n)=|\langle n|\alpha\rangle|^2$, derive the Poisson distribution
$P(n)=e^{-|\alpha|^2}|\alpha|^{2n}/n!$ and show $\langle n\rangle=|\alpha|^2$,
$(\Delta n)^2=|\alpha|^2$, hence $\Delta n=\sqrt{\langle n\rangle}$ and the Mandel
parameter $Q=((\Delta n)^2-\langle n\rangle)/\langle n\rangle=0$. *Answer:* the
variance equals the mean — the defining property of Poisson and of "classical-like"
light. *Check:* for $\alpha=2$, `mean_n` $\approx4$, `var_n` $\approx4$,
`mandel_q` $\approx0$; `photon_distribution(coherent_state(2,60))[:7]` matches
$e^{-4}4^n/n!$.

**Solution.** From the coherent expansion $\langle n|\alpha\rangle=e^{-|\alpha|^2/2}\alpha^n/\sqrt{n!}$,
$$P(n)=|\langle n|\alpha\rangle|^2=e^{-|\alpha|^2}\frac{|\alpha|^{2n}}{n!},$$
the **Poisson** distribution with parameter $\lambda=|\alpha|^2$. Its mean and variance are both
$\lambda$:
$$\langle n\rangle=\sum_n nP(n)=|\alpha|^2,\qquad (\Delta n)^2=\langle n^2\rangle-\langle n\rangle^2=|\alpha|^2,$$
the Poisson identity $\text{variance}=\text{mean}$. Hence $\Delta n=\sqrt{\langle n\rangle}=|\alpha|$
and the Mandel parameter $Q=((\Delta n)^2-\langle n\rangle)/\langle n\rangle=0$ — the boundary
between classical-like and nonclassical light. For $\alpha=2$ ($\lambda=4$): `mean_n`$\approx4$,
`var_n`$\approx4$, `mandel_q`$\approx0$, and `photon_distribution(coherent_state(2,60))[:7]`$=[0.0183,0.0733,0.1465,0.1954,0.1954,0.1563,0.1042]$
matches $e^{-4}4^n/n!$ term by term.

### P5.  Vacuum fluctuations and the uncertainty floor  *(SZ §2.3)*
With $X=(a+a^\dagger)/2$ and $P=(a-a^\dagger)/2i$, compute $[X,P]$ and hence the
bound $\Delta X\,\Delta P\ge\tfrac14$. Evaluate $\langle X^2\rangle,\langle
P^2\rangle$ in the vacuum $|0\rangle$ (use $a|0\rangle=0$) and show the bound is
*saturated* with equal noise. *Answer:* $[X,P]=i/2$; $\langle0|X^2|0\rangle=
\langle0|P^2|0\rangle=\tfrac14$, so $\Delta X\,\Delta P=\tfrac14$.
*Check:* `quadrature_variance(fock_state(0,40))` $=(0.25,0.25)$; the commutator
`commutator(quadrature_x(N),quadrature_p(N))` is $\tfrac{i}{2}\mathbb 1$ on the
interior.

**Solution.** With $\hat X=(\hat a+\hat a^\dagger)/2$ and $\hat P=(\hat a-\hat a^\dagger)/2i$,
expand the commutator using $[\hat a,\hat a^\dagger]=1$:
$$[\hat X,\hat P]=\frac{1}{4i}\big[\hat a+\hat a^\dagger,\ \hat a-\hat a^\dagger\big]=\frac{1}{4i}\big(-[\hat a,\hat a^\dagger]+[\hat a^\dagger,\hat a]\big)=\frac{-2}{4i}=\frac{i}{2},$$
so the Heisenberg bound is $\Delta X\,\Delta P\ge\tfrac12|\langle[\hat X,\hat P]\rangle|=\tfrac14$.
In the vacuum $\hat a|0\rangle=0$, so $\langle X\rangle=\langle P\rangle=0$ and only the
$\hat a\hat a^\dagger$ term survives the squares:
$$\langle0|\hat X^2|0\rangle=\tfrac14\langle0|\hat a\hat a^\dagger|0\rangle=\tfrac14\langle0|(\hat a^\dagger\hat a+1)|0\rangle=\tfrac14,$$
and identically $\langle0|\hat P^2|0\rangle=\tfrac14$. Thus $\Delta X\,\Delta P=\tfrac14$ — the
bound is **saturated** with equal noise. This matches `quadrature_variance(fock_state(0,40))`$=(0.25,0.25)$,
with `commutator(quadrature_x(N),quadrature_p(N))`$=\tfrac{i}{2}\mathbb 1$ on the interior.

### P6.  What makes coherent light "the most classical"  *(SZ §2.3–2.4)*
Show that a coherent state $|\alpha\rangle$ has the *same* quadrature noise as the
vacuum, $\Delta X=\Delta P=\tfrac12$ (it is a displaced vacuum), whereas a Fock
state $|n\rangle$ has the larger isotropic noise $(2n+1)/4$ and is sub-Poissonian
($Q=-1$). Argue why $|\alpha\rangle$ — minimum-uncertainty *and* Poissonian — is the
closest quantum state to a classical wave. *Answer:* $|\alpha\rangle$ saturates
$\Delta X\Delta P=\tfrac14$ with equal, intensity-independent noise; $|n\rangle$
does not. *Check:* `quadrature_variance(coherent_state(2,60))` $\approx(0.25,0.25)$;
`quadrature_variance(fock_state(3,60))` $=(1.75,1.75)$;
`mandel_q(fock_state(4,60))` $=-1$.

**Solution.** A coherent state has $\langle\hat a\rangle=\alpha$, $\langle\hat a^2\rangle=\alpha^2$,
$\langle\hat a^\dagger\hat a\rangle=|\alpha|^2$, $\langle\hat a\hat a^\dagger\rangle=|\alpha|^2+1$.
The displacement-dependent pieces cancel between $\langle\hat X^2\rangle$ and $\langle\hat X\rangle^2$:
$$\text{Var}\,\hat X=\tfrac14\langle(\hat a+\hat a^\dagger)^2\rangle-\langle\hat X\rangle^2=\tfrac14\big(\alpha^2+\alpha^{*2}+2|\alpha|^2+1\big)-\tfrac14\big(\alpha+\alpha^*\big)^2=\tfrac14,$$
and identically $\text{Var}\,\hat P=\tfrac14$, so $\Delta X=\Delta P=\tfrac12$ at the vacuum floor
for **any** $\alpha$ — a displaced vacuum. A Fock state instead has
$\langle n|\hat X^2|n\rangle=\tfrac14\langle n|(\hat a\hat a^\dagger+\hat a^\dagger\hat a)|n\rangle=\tfrac14(2n+1)$
with $\langle\hat X\rangle=0$, i.e. the larger isotropic noise $(2n+1)/4$, and being number-sharp
it is sub-Poissonian with $Q=-1$. So $|\alpha\rangle$ is uniquely minimum-uncertainty **and**
Poissonian — definite amplitude and phase at the lowest allowed noise — which is what "most
classical" means. Confirmed by `quadrature_variance(coherent_state(2,60))`$\approx(0.25,0.25)$,
`quadrature_variance(fock_state(3,60))`$=(1.75,1.75)$ (that is $(2\cdot3+1)/4$), and
`mandel_q(fock_state(4,60))`$=-1$.
