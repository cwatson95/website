# QM-10 — Problems

Work them by hand, then check with `code/angular_momentum.py`. Sources in
`../refs.md`. Natural units $\hbar=1$ (as in the code).

### P1.  The algebra is the whole story  *(Griffiths 3e §4.3.1, p.202)*
From $[L_x,L_y]=i\hbar L_z$ and its cyclic partners, show (a) no two components
share eigenstates, but (b) $L^2$ does commute with each, so $L^2$ and one
component can be diagonalized together.
*Answer:* (a) $[L_x,L_y]\neq0$ ⇒ incompatible (generalized uncertainty). (b)
$[L^2,L_i]=0$. This is *why* the labels are $(l,m)$ — one for $L^2$, one for $L_z$.
*Check:* `commutator(Lx(1),Ly(1))` $=i\,$`Lz(1)`; `commutator(L_squared(1),Lz(1))`
$=0$. (`test_commutators_cyclic`, `test_L2_commutes_with_each_component`.)

**Solution.** Two operators share a complete eigenbasis only if they commute, so test a *single* common eigenstate: if $|\psi\rangle$ obeyed $L_x|\psi\rangle=a|\psi\rangle$ and $L_y|\psi\rangle=b|\psi\rangle$, then
$$[L_x,L_y]\,|\psi\rangle=(ab-ba)|\psi\rangle=0,\qquad\text{yet}\qquad [L_x,L_y]|\psi\rangle=i\hbar L_z|\psi\rangle,$$
forcing $L_z|\psi\rangle=0$; cyclically $L_x|\psi\rangle=L_y|\psi\rangle=0$, so $L^2|\psi\rangle=0$ — only the trivial $l=0$ state. Hence (a) no two components share eigenstates. (b) But $[L^2,L_i]=0$, so $L^2$ and one component ($L_z$) *do* share a basis, labelled $(l,m)$. The code confirms `commutator(Lx(1),Ly(1))` $=i\,$`Lz(1)` and `commutator(L_squared(1),Lz(1))` $=0$.

### P2.  Build the $l=1$ representation  *(Griffiths 3e Eq. 4.118–4.119, p.205)*
Write the $3\times3$ matrices for $l=1$ and read off the spectrum of $L_z$ and the
single eigenvalue of $L^2$.
*Answer:* $L_z=\mathrm{diag}(1,0,-1)$; spectrum $\{-1,0,1\}$; $L^2=2\,\mathbb 1$
since $\hbar^2 l(l+1)=2$. The components are *not* diagonal, but their squares
sum to a multiple of the identity.
*Check:* `numpy.linalg.eigvalsh(Lz(1))` → `[-1,0,1]`;
`L_squared(1)` $=2\,I$ ; `casimir_eigenvalue(1)` $=2$.
(`test_Lz_is_diagonal_spectrum`, `test_casimir_is_l_l_plus_one`.)

**Solution.** Order the rungs $m=1,0,-1$. Then $L_z=\hbar\,\mathrm{diag}(1,0,-1)$, with spectrum $\{-1,0,1\}$. The ladder element $\hbar\sqrt{l(l+1)-m(m+1)}=\hbar\sqrt{2-m(m+1)}$ equals $\hbar\sqrt2$ for both $m=0$ and $m=-1$, so
$$L_+=\hbar\sqrt2\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix},\qquad L_x=\tfrac{1}{2}(L_++L_-)=\frac{\hbar}{\sqrt2}\begin{pmatrix}0&1&0\\1&0&1\\0&1&0\end{pmatrix}.$$
$L_x,L_y$ are *not* diagonal, but their squares conspire: $L^2=L_x^2+L_y^2+L_z^2=\hbar^2l(l+1)\,\mathbb1=2\hbar^2\mathbb1$. So `eigvalsh(Lz(1))`$=[-1,0,1]$, `L_squared(1)`$=2I$, and `casimir_eigenvalue(1)`$=2$.

### P3.  Why the ladder stops  *(Griffiths 3e Problem 4.21, p.206)*
The raising operator acts as $L_+|l,m\rangle=\hbar\sqrt{l(l+1)-m(m+1)}\,|l,m+1\rangle$.
Show the coefficient vanishes at the top rung $m=l$ (and $L_-$ at $m=-l$), so the
ladder is finite — this is what quantizes $m$ to $2l+1$ integer-spaced values.
*Answer:* at $m=l$, $l(l+1)-l(l+1)=0$; at $m=-l$ (with $L_-$), $l(l+1)-(-l)(-l-1)=0$.
*Check:* `ladder_coeff(2,2,+1)` $=0$, `ladder_coeff(2,-2,-1)` $=0$;
`L_plus(2)[:,0]` and `L_minus(2)[:,-1]` are all-zero columns.
(`test_ladder_matrix_elements`.)

**Solution.** The raising coefficient is $c_+(m)=\hbar\sqrt{l(l+1)-m(m+1)}$. At the top rung $m=l$,
$$l(l+1)-l(l+1)=0\ \Rightarrow\ L_+|l,l\rangle=0.$$
The lowering coefficient $c_-(m)=\hbar\sqrt{l(l+1)-m(m-1)}$ at $m=-l$ gives $l(l+1)-(-l)(-l-1)=l(l+1)-l(l+1)=0$, so $L_-|l,-l\rangle=0$. Both ends are sealed, leaving exactly $2l+1$ integer-spaced rungs $m=-l,\dots,l$. For $l=2$ this is `ladder_coeff(2,2,+1)`$=0$ and `ladder_coeff(2,-2,-1)`$=0$; correspondingly `L_plus(2)[:,0]` (the $|2,2\rangle$ column) and `L_minus(2)[:,-1]` (the $|2,-2\rangle$ column) are all-zero.

### P4.  Spin-½ is just the smallest ladder  *(Griffiths 3e §4.4; Bethe p.14)*
Take $l=\tfrac12$ (allowed by the algebra). What are $2L_x,2L_y,2L_z$?
*Answer:* exactly the Pauli matrices $\sigma_x,\sigma_y,\sigma_z$; i.e.
$L_i=\tfrac{\hbar}{2}\sigma_i$. The $2\times2$ rep is `~QM-11` (spin) in full.
*Check:* `2*Lx(0.5)`, `2*Ly(0.5)`, `2*Lz(0.5)` are the Pauli matrices.
(`test_spin_half_is_pauli`.)

**Solution.** For $l=\tfrac12$ the rungs are $m=\pm\tfrac12$ (dim 2), so $L_z=\tfrac\hbar2\,\mathrm{diag}(1,-1)$. The single ladder element is $\hbar\sqrt{\tfrac12\cdot\tfrac32-(-\tfrac12)(\tfrac12)}=\hbar\sqrt{\tfrac34+\tfrac14}=\hbar$, giving
$$L_+=\hbar\begin{pmatrix}0&1\\0&0\end{pmatrix},\quad L_-=\hbar\begin{pmatrix}0&0\\1&0\end{pmatrix},\quad L_x=\tfrac\hbar2\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad L_y=\tfrac\hbar2\begin{pmatrix}0&-i\\i&0\end{pmatrix}.$$
Hence $\tfrac2\hbar L_x,\tfrac2\hbar L_y,\tfrac2\hbar L_z=\sigma_x,\sigma_y,\sigma_z$, i.e. $L_i=\tfrac\hbar2\sigma_i$. With $\hbar=1$ the code returns `2*Lx(0.5)`$=\sigma_x$, `2*Ly(0.5)`$=\sigma_y$, `2*Lz(0.5)`$=\sigma_z$ — the entire spin-$\tfrac12$ content of `~QM-11`.

### P5.  Spherical harmonics are orthonormal  *(Griffiths 3e Eq. 4.33 / Prob. 4.4, p.178–179)*
Verify $\displaystyle\int {Y_l^m}^{*}\,Y_{l'}^{m'}\,d\Omega=\delta_{ll'}\delta_{mm'}$
for a few modes, and explain *why* they're orthogonal without doing the integral.
*Answer:* the integral is $1$ on the diagonal, $0$ off it; orthogonality follows
because the $Y_l^m$ are eigenfunctions of the Hermitian operators $L^2,L_z$ for
distinct eigenvalues (Griffiths p.206).
*Check:* `sphere_inner_product(2,1,2,1)` $\approx1$;
`sphere_inner_product(1,0,2,0)` $\approx0$. (`test_spherical_harmonics_orthonormal`.)

**Solution.** Numerically `sphere_inner_product(2,1,2,1)`$=1.0000$ and `sphere_inner_product(1,0,2,0)`$=-8.7\times10^{-17}\approx0$. No integral is needed to *know* this: $L^2$ and $L_z$ are Hermitian, and eigenfunctions of a Hermitian operator belonging to **distinct** eigenvalues are orthogonal. $Y_1^0$ and $Y_2^0$ have different $L^2$ eigenvalues ($2\hbar^2$ vs $6\hbar^2$), and any two $Y_l^m$ with $m\neq m'$ have different $L_z$ eigenvalues $\hbar m$. Either mismatch forces the overlap to vanish, which is exactly the $\delta_{ll'}\delta_{mm'}$ the checks return.

### P6.  $Y_l^m$ is an $L_z$ eigenfunction  *(Griffiths 3e Eq. 4.129, p.208)*
In position space $L_z=-i\hbar\,\partial/\partial\phi$. Show $Y_l^m$ has eigenvalue
$\hbar m$.
*Answer:* $Y_l^m\propto e^{im\phi}$, so $-i\hbar\,\partial_\phi Y_l^m=\hbar m\,Y_l^m$.
The "matrix" $L_z$ of P2 and the differential $L_z$ here are the *same operator*
in two representations.
*Check:* `Lz_on_Y(3,-2,0.6,0.9)` $\approx -2\cdot$`spherical_harmonic(3,-2,0.6,0.9)`.
(`test_spherical_harmonics_are_Lz_eigenfunctions`.)

**Solution.** Write $Y_l^m=N\,P_l^m(\cos\theta)\,e^{im\phi}$; only the $e^{im\phi}$ factor depends on $\phi$. Then
$$L_zY_l^m=-i\hbar\,\partial_\phi\!\left(N\,P_l^m(\cos\theta)\,e^{im\phi}\right)=-i\hbar\,(im)\,Y_l^m=\hbar m\,Y_l^m.$$
So $Y_l^m$ is an $L_z$ eigenfunction with eigenvalue $\hbar m$ — the very number sitting on the diagonal of the *matrix* $L_z$ in P2; the two are one operator in two representations. For $(l,m)=(3,-2)$ the eigenvalue is $-2\hbar$, and the finite-difference `Lz_on_Y(3,-2,0.6,0.9)`$=0.1222+0.5238i$ matches $-2\cdot$`spherical_harmonic(3,-2,0.6,0.9)`$=0.1222+0.5238i$.

### P7.  Integer vs half-integer  *(Griffiths 3e p.176 vs p.205; Bethe p.14)*
The algebra (P1–P3) allows $l=0,\tfrac12,1,\tfrac32,\dots$, yet the spherical
harmonics exist only for *integer* $l$. Reconcile this.
*Answer:* the $\phi$-equation gives $\Phi=e^{im\phi}$; single-valuedness under
$\phi\to\phi+2\pi$ forces $m$ (hence $l$) integer for any *spatial* wavefunction
(Griffiths Eq. 4.22, p.176). The half-integer rungs the algebra permits have no
$Y_l^m$ — they are **spin** (`~QM-11`), an intrinsic angular momentum with no
$\mathbf r\times\mathbf p$ realization.
*Check:* `spherical_harmonic(0.5, 0.5, θ, φ)` raises `ValueError`; but
`Lz(0.5)`, `L_squared(0.5)` exist and satisfy the algebra.
(`test_spherical_harmonics_require_integer_l`, `test_commutators_cyclic`.)

**Solution.** The algebra of P1–P3 only needs the ladder to terminate, which it does for every $l=0,\tfrac12,1,\tfrac32,\dots$. But a *spatial* wavefunction must be single-valued: the azimuthal factor $\Phi(\phi)=e^{im\phi}$ has to satisfy $\Phi(\phi+2\pi)=\Phi(\phi)$, i.e. $e^{2\pi i m}=1$, which forces $m\in\mathbb Z$ and hence $l\in\mathbb Z$. The half-integer rungs the algebra permits therefore carry **no** $Y_l^m$ — they are intrinsic spin (`~QM-11`), matrices with no $\mathbf r\times\mathbf p$ realization. Accordingly `spherical_harmonic(0.5,0.5,…)` raises `ValueError`, while `Lz(0.5)`$=\tfrac12\mathrm{diag}(1,-1)$ and `L_squared(0.5)`$=\tfrac34\,\mathbb1$ exist and satisfy $[L_x,L_y]=i\hbar L_z$.

### P8.  Angular momentum can't align with an axis  *(Griffiths 3e p.205, Fig. 4.12)*
For $l=2$, compare the length $|\mathbf L|=\hbar\sqrt{l(l+1)}$ with the largest
$L_z$ eigenvalue $\hbar l$. Why can't they be equal?
*Answer:* $\sqrt{l(l+1)}=\sqrt6\approx2.449>2=l$, so the vector is always longer
than its biggest projection. Equality would mean $L_x=L_y=0$ with $L_z$ definite —
forbidden by $[L_x,L_y]=i\hbar L_z\neq0$ (P1). The classical limit is $l\to\infty$,
where $\sqrt{l(l+1)}/l\to1$.
*Check:* `math.sqrt(casimir_eigenvalue(2))` $\approx2.449$ vs `max(m_values(2))` $=2$.

**Solution.** The length of $\mathbf L$ is fixed by $L^2=\hbar^2l(l+1)$, so $|\mathbf L|=\hbar\sqrt{l(l+1)}$; for $l=2$, $|\mathbf L|=\hbar\sqrt6\approx2.449\hbar$, whereas the largest projection is $L_z^{\max}=\hbar l=2\hbar$. Since $l(l+1)>l^2$ for any $l>0$, always $\sqrt{l(l+1)}>l$. Equality would demand $L_x=L_y=0$ with $L_z$ sharp — impossible, because $[L_x,L_y]=i\hbar L_z\neq0$ (P1) forbids that simultaneous eigenstate. Only as $l\to\infty$ does $\sqrt{l(l+1)}/l\to1$, recovering the classical vector. Hence `math.sqrt(casimir_eigenvalue(2))`$=2.449$ strictly exceeds `max(m_values(2))`$=2$.
