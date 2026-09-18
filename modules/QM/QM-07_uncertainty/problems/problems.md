# QM-07 — Problems

Work them by hand, then check with `code/uncertainty.py`. Sources in `../refs.md`.
Natural units $\hbar=m=1$, so the bound reads $\sigma_x\sigma_p\ge\tfrac12$.

### P1.  The minimum-uncertainty packet  *(Griffiths 3e §3.5.2 / Problem 3.17, p.141)*
Show that the Gaussian $\psi\propto e^{-(x-x_0)^2/4\sigma^2}e^{ip_0x}$ has
$\sigma_x=\sigma$, $\sigma_p=1/2\sigma$, and therefore **saturates** the bound,
$\sigma_x\sigma_p=\tfrac12$, for *any* width or boost.
*Answer:* equality holds because the Gaussian solves the minimum-uncertainty ODE
$(\hat p-\langle p\rangle)\psi=ia(\hat x-\langle x\rangle)\psi$ (Griffiths Eq. 3.69).
*Check:* `uncertainty_product(gaussian_packet(x, sigma=1.3, p0=0.7), x, dx)` ≈ `0.5`
for `x, dx = grid(40, 2048)`. (`test_gaussian_saturates`, `test_gaussian_components`.)

**Solution.** With $\hbar=1$, the density $|\psi|^2\propto e^{-(x-x_0)^2/2\sigma^2}$ is a Gaussian
of variance $\sigma^2$, so $\langle x\rangle=x_0$ and $\sigma_x=\sigma$. The boost $e^{ip_0x}$ moves
$\langle p\rangle$ to $p_0$ without changing the spread; the Fourier transform $\tilde\psi(p)$ is
again Gaussian, of width $\hbar/2\sigma=1/2\sigma$, so $\sigma_p=1/2\sigma$. Hence
$$\sigma_x\sigma_p=\sigma\cdot\frac1{2\sigma}=\frac12$$
for *every* $\sigma,p_0$. Equality is forced because $\hat p\psi=\bigl[i(x-x_0)/2\sigma^2+p_0\bigr]\psi$,
i.e. $(\hat p-\langle p\rangle)\psi=ia(\hat x-\langle x\rangle)\psi$ with $a=1/2\sigma^2$ real — exactly
the minimum-uncertainty condition (Schwarz tight, $\operatorname{Re}z$ dropped). `uncertainty_product(gaussian_packet(x, sigma=1.3, p0=0.7), x, dx)`
returns $0.49999\ldots\approx0.5$.

### P2.  Why excited states are fuzzier  *(cross-link ~QM-09; Griffiths §3.5.2, p.141)*
The oscillator eigenstate $\psi_n\propto H_n(x)e^{-x^2/2}$ has
$\sigma_x=\sigma_p=\sqrt{n+\tfrac12}$. Find $\sigma_x\sigma_p$ and identify the one
state that saturates the bound.
*Answer:* $\sigma_x\sigma_p=n+\tfrac12$; only the ground state $n=0$ gives $\tfrac12$
(it **is** the minimum-uncertainty Gaussian). Excited states strictly exceed it.
*Check:* `uncertainty_product(ho_eigenstate(x, n), x, dx)` ≈ `n+0.5` for `n=0..3`.
(`test_ho_eigenstates_product`.)

**Solution.** Multiplying the two equal spreads,
$$\sigma_x\sigma_p=\sqrt{n+\tfrac12}\,\sqrt{n+\tfrac12}=n+\tfrac12\ \ge\ \tfrac12,$$
with equality only at $n=0$. The ground state $\psi_0\propto H_0(x)e^{-x^2/2}=e^{-x^2/2}$ is exactly the
minimum-uncertainty Gaussian of P1 (width $\sigma=1/\sqrt2$, so $\sigma_x=\sigma_p=1/\sqrt2$ and the
product is $\tfrac12$). Each excitation adds one full quantum $\hbar=1$ to the product, so every
$n\ge1$ state is strictly fuzzier. `uncertainty_product(ho_eigenstate(x, n), x, dx)` returns
$0.5,\,1.5,\,2.5,\,3.5$ for $n=0,1,2,3$ — i.e. $n+\tfrac12$.

### P3.  A state that does *not* saturate  *(Griffiths 3e, Problem 1.9, p.36)*
Build a non-Gaussian state (e.g. a two-bump "cat" $\psi\propto g(x{+}3)+g(x{-}3)$)
and check that its product is *consistent with*, but strictly above, the bound.
*Answer:* any non-Gaussian has $\sigma_x\sigma_p>\tfrac12$ (the Gaussian is the
unique minimizer).
*Check:* with `cat = gaussian_packet(x,x0=-3)+gaussian_packet(x,x0=3)`,
`uncertainty_product(cat, x, dx)` $>0.5$. (`test_uncertainty_lower_bound_holds`.)

**Solution.** Being non-Gaussian, the cat must lie strictly above the bound (P1 uniqueness).
Concretely, with unit-width bumps at $x=\pm3$ and $\langle x\rangle=0$, the density has
$\langle x^2\rangle\approx\sigma^2+3^2=10$, so $\sigma_x\approx\sqrt{10}\approx3.15$; the coherent
superposition prints interference fringes in $\tilde\psi(p)$ that hold $\sigma_p\approx0.47$. Their product
$$\sigma_x\sigma_p\approx3.147\times0.475\approx1.49\;>\;\tfrac12$$
is comfortably consistent with — but far from saturating — the inequality. `uncertainty_product(cat, x, dx)`
returns $1.4935$, confirming $>0.5$.

### P4.  The generalized bound for spin  *(Griffiths 3e §3.5.1, p.138; result p.139)*
For spin-$\tfrac12$, $[\hat S_x,\hat S_y]=i\hbar\hat S_z$. Show the Robertson bound
is $\sigma_{S_x}\sigma_{S_y}\ge\tfrac\hbar2|\langle\hat S_z\rangle|$ and find a state
that saturates it.
*Answer:* $|{\uparrow_z}\rangle$ saturates it: $\sigma_{S_x}=\sigma_{S_y}=\tfrac\hbar2$,
$\langle\hat S_z\rangle=\tfrac\hbar2$, so both sides equal $\hbar^2/4$. A state off the
$x$–$z$ Bloch plane makes the inequality strict.
*Check:* `Sx,Sy,Sz = spin_ops(); std(Sx,[1,0])*std(Sy,[1,0])` = `generalized_bound(Sx,Sy,[1,0])` = `0.25`;
the complex state in `test_spin_strict_case` gives a strict gap. (`test_spin_saturation_upz`, `test_spin_bound_holds`.)

**Solution.** Feed $[\hat S_x,\hat S_y]=i\hbar\hat S_z$ into the Robertson bound:
$$\sigma_{S_x}\sigma_{S_y}\ge\tfrac12\bigl|\langle i\hbar\hat S_z\rangle\bigr|=\tfrac\hbar2\bigl|\langle\hat S_z\rangle\bigr|.$$
For $|{\uparrow_z}\rangle=(1,0)$, a $\hat S_z$ eigenstate with $\langle\hat S_z\rangle=\hbar/2$, the RHS is
$\hbar^2/4$. Since $\hat S_x=\tfrac\hbar2\sigma_x$ with $\sigma_x^2=\mathbb 1$, we get $\langle S_x\rangle=0$,
$\langle S_x^2\rangle=\hbar^2/4$, so $\sigma_{S_x}=\hbar/2$; identically $\sigma_{S_y}=\hbar/2$, making the
LHS $\hbar^2/4$ as well — saturation. In $\hbar=1$ units both sides equal $0.25$, exactly what
`std(Sx,[1,0])*std(Sy,[1,0])` and `generalized_bound(Sx,Sy,[1,0])` return.

### P5.  Compatible observables  *(Griffiths 3e, Problems 3.14 & 3.16, pp.139–140)*
Show that when $[\hat A,\hat B]=0$ the bound vanishes, so $A$ and $B$ can be sharp
simultaneously (they share a complete eigenbasis), whereas noncommuting
("incompatible") observables cannot.
*Answer:* the RHS $\tfrac12|\langle[\hat A,\hat B]\rangle|$ is identically $0$ for
commuting operators; e.g. two diagonal matrices.
*Check:* for `A=diag(1,2,3)`, `B=diag(5,7,11)`: `commutator(A,B)` is zero and
`generalized_bound(A,B,[1,1,1])` ≈ `0`, while `std(A,·)·std(B,·) ≥ 0`.
(`test_bound_zero_for_commuting`, `test_pauli_commutators`.)

**Solution.** The Robertson right-hand side is $\tfrac12\lvert\langle[\hat A,\hat B]\rangle\rvert$. If
$[\hat A,\hat B]=0$ it is identically $0$, so $\sigma_A\sigma_B\ge0$ is vacuous — nothing forbids both
spreads vanishing at once, and indeed commuting Hermitian operators are simultaneously diagonalizable
(a shared complete eigenbasis). Two diagonal matrices commute entrywise:
$$[\,\mathrm{diag}(1,2,3),\ \mathrm{diag}(5,7,11)\,]=0.$$
So `commutator(A,B)` is the zero matrix and `generalized_bound(A,B,[1,1,1])` $=0.0$, while each
$\sigma_A,\sigma_B\ge0$ separately. Incompatible (noncommuting) observables, by contrast, carry a
nonzero RHS and cannot both be sharp.

### P6.  Ehrenfest in free space  *(Griffiths 3e §1.5, Eq. 1.33, p.33; Problem 1.7, p.34)*
A free Gaussian packet is launched with mean momentum $p_0$. Verify
$d\langle x\rangle/dt=\langle p\rangle/m$ and that $\langle p\rangle$ is conserved
(no force).
*Answer:* the centroid drifts as $\langle x\rangle(t)=\langle x\rangle_0+p_0t/m$ with
$\langle p\rangle=p_0$ fixed; $d\langle p\rangle/dt=-\langle V'\rangle=0$.
*Check:* `split_step_evolve(gaussian_packet(x,p0=1.5), x, V=0.0, dt=0.02, nsteps=120)`
gives `gradient(xs,t) ≈ ps/M` and constant `ps`. (`test_ehrenfest_free`.)

**Solution.** Ehrenfest's theorem reads $\dfrac{d\langle x\rangle}{dt}=\dfrac{\langle p\rangle}{m}$ and
$\dfrac{d\langle p\rangle}{dt}=-\langle V'(\hat x)\rangle$. With $V=0$ the force $V'=0$, so $\langle p\rangle$
stays fixed at its initial value $p_0$ and
$$\langle x\rangle(t)=\langle x\rangle_0+\frac{p_0}{m}\,t,$$
a straight drift. The split-step run confirms it: at the midpoint `gradient(xs,t)` $=1.500$ equals
`ps/M` $=1.500$, and `ps` is constant to $\sim5\times10^{-15}$ across all 120 steps. So
$d\langle x\rangle/dt=\langle p\rangle/m$ with $d\langle p\rangle/dt=0$, as required.

### P7.  The classical limit: SHO  *(Griffiths 3e §1.5; Problem 3.14(d), p.140; cross-link ~CM-19)*
Evolve a packet in $V=\tfrac12 m\omega^2x^2$. Show $d\langle p\rangle/dt=-\langle V'(x)\rangle$
and that the centre obeys the **classical** oscillation $\langle x\rangle(t)=x_0\cos\omega t+(p_0/m\omega)\sin\omega t$.
*Answer:* because $V'$ is linear, $\langle V'(x)\rangle=V'(\langle x\rangle)=m\omega^2\langle x\rangle$,
so the Ehrenfest equations close into Hamilton's equations for $(\langle x\rangle,\langle p\rangle)$ —
the classical SHO, *exactly*.
*Check:* over one period, `max|xs - classical_sho(t, x0, p0, omega)|` $\sim10^{-5}$ and
`gradient(ps,t) ≈ Fs`. (`test_sho_classical_limit`, `test_ehrenfest_harmonic`.)

**Solution.** Here $V=\tfrac12 m\omega^2x^2$ has the *linear* derivative $V'(x)=m\omega^2x$, so the mean
force is exact: $\langle V'(\hat x)\rangle=m\omega^2\langle x\rangle=V'(\langle x\rangle)$. Ehrenfest then
closes into a self-contained pair for $(\langle x\rangle,\langle p\rangle)$,
$$\frac{d\langle x\rangle}{dt}=\frac{\langle p\rangle}{m},\qquad\frac{d\langle p\rangle}{dt}=-m\omega^2\langle x\rangle
\;\Rightarrow\;\frac{d^2\langle x\rangle}{dt^2}=-\omega^2\langle x\rangle,$$
whose solution is the classical SHO $\langle x\rangle(t)=x_0\cos\omega t+(p_0/m\omega)\sin\omega t$. Over one
period the code gives `max|xs - classical_sho|` $\approx6.0\times10^{-5}\sim10^{-5}$, and at $t=T/4$
`gradient(ps,t)` $\approx$ `Fs` (both $\approx-0.0024$) — the packet centre rides the classical trajectory exactly.

### P8.  Derive the Schwarz inequality  *(Griffiths 3e Eq. 3.7, p.120; Eq. A.27 & Problem A.5, p.594)*
The first inequality of the uncertainty proof is
$\langle f|f\rangle\langle g|g\rangle\ge|\langle f|g\rangle|^2$. Prove it from the
inner-product axioms alone, and state exactly when it becomes an equality.
*Answer:* subtract from $g$ its projection along $f$,
$h=g-\frac{\langle f|g\rangle}{\langle f|f\rangle}f$; expanding $\langle h|h\rangle\ge0$
gives $\langle f|f\rangle\langle g|g\rangle-|\langle f|g\rangle|^2=\langle f|f\rangle\langle h|h\rangle\ge0$.
Equality iff $h=0$, i.e. $g=cf$.
*Check:* `schwarz_residual_identity(f, g)` returns the gap, $\langle f|f\rangle\langle h|h\rangle$
(equal to round-off) and $\langle f|h\rangle$ ($=0$) for random states; `schwarz_gap(f, c*f)` $=0$.
(`test_schwarz_inequality_random`, `test_schwarz_projection_identity`, `test_schwarz_saturation`.)

**Solution.** (Griffiths's Problem A.5, hint and all — the lemma behind P4 and the whole of §2 of the notes.)
If $\langle f|f\rangle=0$ then $f=0$ and both sides vanish, so let $\langle f|f\rangle>0$ and define
$$h=g-\frac{\langle f|g\rangle}{\langle f|f\rangle}\,f,$$
$g$ minus its component along $f$. First, $h\perp f$:
$$\langle f|h\rangle=\langle f|g\rangle-\frac{\langle f|g\rangle}{\langle f|f\rangle}\langle f|f\rangle=0.$$
Next expand $\langle h|h\rangle$ with $c=\langle f|g\rangle/\langle f|f\rangle$ (antilinear first slot, linear second):
$$\langle h|h\rangle=\langle g|g\rangle-c\langle g|f\rangle-c^*\langle f|g\rangle+|c|^2\langle f|f\rangle.$$
By conjugate symmetry $\langle g|f\rangle=\langle f|g\rangle^*$, each of the last three terms equals
$|\langle f|g\rangle|^2/\langle f|f\rangle$ (two cancel), so
$$0\le\langle h|h\rangle=\langle g|g\rangle-\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle}
\;\Longrightarrow\;
\langle f|f\rangle\langle g|g\rangle-|\langle f|g\rangle|^2=\langle f|f\rangle\langle h|h\rangle\ge0. \qquad\blacksquare$$
Equality forces $\langle h|h\rangle=0$, hence $h=0$, hence $g=cf$ — one state a multiple of the other.
(In §3 of the notes, demanding this *and* $\operatorname{Re}\langle f|g\rangle=0$ makes $c$ pure imaginary
and turns the condition into the minimum-uncertainty ODE whose solution is the Gaussian.) Numerically,
for 300 random 4-component kets the gap and $\langle f|f\rangle\langle h|h\rangle$ agree to $10^{-9}$
with $\langle f|h\rangle=0$; setting $g=(2-0.7i)f$ closes the gap to $10^{-9}$, and adding an orthogonal
piece $w$ reopens it by exactly $\langle f|f\rangle\langle w|w\rangle$.
