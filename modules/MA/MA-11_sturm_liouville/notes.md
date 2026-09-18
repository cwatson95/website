# MA-11 — Sturm–Liouville Theory (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. Boas develops Sturm–Liouville theory through the
orthogonal-function sections of Ch.12 (the SL equation itself is stated in the
Ch.12 miscellaneous problems, p.617); Ch.7 (Fourier series) is the prototype.

## 1. The self-adjoint (Sturm–Liouville) form
Almost every linear 2nd-order ODE of physics can be written
$$\frac{d}{dx}\!\Big(p(x)\frac{dy}{dx}\Big)-q(x)\,y+\lambda\,w(x)\,y=0,\qquad x\in[a,b],$$
with p, w > 0 — the **Sturm–Liouville form** [B Ch.12, misc. prob., p.617]. Write
the operator as $\mathcal L y=-(p y')'+q y$, so the problem is the eigenvalue
equation $\mathcal L y=\lambda\,w\,y$ with homogeneous boundary conditions. Code:
`sl_tridiagonal` builds the finite-difference matrix of $\mathcal L$.

## 2. Self-adjointness ⇒ a real, orthogonal, complete spectrum
Because $\mathcal L$ is self-adjoint under the **weighted inner product**
$\langle f,g\rangle_w=\int_a^b f g\,w\,dx$ (integrate $\int(f\mathcal Lg-g\mathcal Lf)=[p(fg'-gf')]_a^b=0$
by the boundary conditions), three theorems follow — the continuous analogue of a
real symmetric matrix (`~MA-04`):
1. **Eigenvalues are real** and form a discrete, increasing sequence
   $\lambda_1<\lambda_2<\cdots\to\infty$.
2. **Eigenfunctions are w-orthogonal:** $\langle y_m,y_n\rangle_w=0$ for $m\ne n$
   [B §7 *Orthogonality of the Legendre Polynomials* p.577 — the model case].
3. **They are complete:** any sufficiently nice f expands as
   $f(x)=\sum_n c_n y_n(x)$, $c_n=\langle f,y_n\rangle_w/\langle y_n,y_n\rangle_w$
   [B §6 *Complete Sets of Orthogonal Functions* p.575; §9 *Legendre Series* p.580].
Code: `inner_w`, `expand`/`reconstruct`; the test verifies orthonormality and
**Parseval** $\langle f,f\rangle_w=\sum_n c_n^2\langle y_n,y_n\rangle_w$.

## 3. The canonical example
$-y''=\lambda y$ on $[0,\pi]$ with $y(0)=y(\pi)=0$ (i.e. $p=w=1,\,q=0$) has
$$\lambda_n=n^2,\qquad y_n(x)=\sin(nx),\qquad n=1,2,\dots$$
This **is** the Fourier sine series (`~MA-09`): Fourier analysis is just the
simplest Sturm–Liouville problem. The code recovers $\lambda_n\to n^2$ and
$y_n\propto\sin nx$ numerically.

## 4. How the eigenvalues are found — the Sturm sequence
Discretizing $\mathcal L$ gives a **symmetric tridiagonal** matrix. For such a
matrix the leading principal minors $p_k(\mu)=\det(T_k-\mu I)$ obey
$$p_k=(d_k-\mu)\,p_{k-1}-e_{k-1}^2\,p_{k-2},$$
and the number of **sign changes** in $\{p_0,\dots,p_N\}$ equals the number of
eigenvalues below $\mu$ — **Sturm's theorem** for the characteristic polynomial.
Counting (in the stable ratio form $q_k=p_k/p_{k-1}$, counting negatives) plus
bisection isolates every eigenvalue. Code: `sturm_count`, `tridiag_eigenvalues`;
the eigenvectors then come from inverse iteration (`tridiag_eigenvector`). A
nonconstant weight is folded in by the symmetric scaling
$M=D^{-1}AD^{-1},\,D=\mathrm{diag}(\sqrt w)$, which keeps $M$ tridiagonal.

## 5. The Rayleigh quotient (the variational handle)
For any admissible trial function,
$$R[y]=\frac{\int_a^b\!\big(p\,y'^2+q\,y^2\big)\,dx}{\int_a^b w\,y^2\,dx}\ \ge\ \lambda_1,$$
with equality only at the ground eigenfunction [B §6 p.575, completeness/energy].
Trying the parabola $y=x(\pi-x)$ on $[0,\pi]$ gives $R=10/\pi^2\approx1.0132$ — a
1.3 % upper bound on the true $\lambda_1=1$ from a one-line guess. This is the
seed of the **variational method** in `~QM-15`. Code: `rayleigh_quotient`.

## Where this goes
- `~MA-12`: Legendre, Bessel, Hermite, Laguerre are the eigenfunctions of specific
  SL operators — their orthogonality is theorem 2 above, one weight each.
- `~MA-14`: the Green's function is $G(x,\xi)=\sum_n y_n(x)y_n(\xi)/\lambda_n$, the
  spectral inverse of $\mathcal L$ — completeness made operational.
- `~QM-05`: a quantum observable is a self-adjoint operator; its real eigenvalues
  are measured values and its eigenfunctions a complete basis — §2, verbatim.
