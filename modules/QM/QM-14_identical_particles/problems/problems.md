# QM-14 — Problems

Work them by hand, then check with `code/identical.py`. Sources in `../refs.md`.
All `Check:` snippets assume `from identical import *` and `import numpy as np`.

### P1.  Bosons are $+1$, fermions are $-1$ eigenstates of exchange  *(Griffiths 3e §5.1.1 p.256; §5.1.4 p.264)*
For orthonormal one-particle states $|a\rangle,|b\rangle$, build the symmetric and
antisymmetric combinations and show each is an eigenstate of the exchange operator
$P_{12}$ with eigenvalue $+1$ (boson) and $-1$ (fermion), respectively.
*Answer:* $\Psi_\pm=\tfrac{1}{\sqrt2}(|a\rangle|b\rangle\pm|b\rangle|a\rangle)$;
since $P_{12}|a\rangle|b\rangle=|b\rangle|a\rangle$, $P_{12}\Psi_\pm=\pm\Psi_\pm$.
*Check:* `a,b = np.eye(3)[0], np.eye(3)[1]`, `P = swap_operator(3)`:
`np.allclose(P@symmetrize(a,b), symmetrize(a,b))` and
`np.allclose(P@antisymmetrize(a,b), -antisymmetrize(a,b))`.
(`test_boson_state_is_symmetric_and_normalized`,
`test_fermion_state_is_antisymmetric_and_normalized`.)

**Solution.** With orthonormal $|a\rangle,|b\rangle$ form
$\Psi_\pm=\tfrac1{\sqrt2}(|a\rangle|b\rangle\pm|b\rangle|a\rangle)$. The exchange operator swaps
the two slots, $P_{12}|a\rangle|b\rangle=|b\rangle|a\rangle$ and
$P_{12}|b\rangle|a\rangle=|a\rangle|b\rangle$, so
$$P_{12}\Psi_\pm=\tfrac1{\sqrt2}\big(|b\rangle|a\rangle\pm|a\rangle|b\rangle\big)
=\pm\tfrac1{\sqrt2}\big(|a\rangle|b\rangle\pm|b\rangle|a\rangle\big)=\pm\,\Psi_\pm.$$
Orthonormality also fixes the norm, $\langle\Psi_\pm|\Psi_\pm\rangle=\tfrac12(1+1)=1$. Thus the
symmetric state is a $+1$ eigenstate (boson) and the antisymmetric a $-1$ eigenstate (fermion):
`P@symmetrize(a,b)` $=$ `symmetrize(a,b)` and `P@antisymmetrize(a,b)` $=$ `-antisymmetrize(a,b)`.

### P2.  The Pauli exclusion principle  *(Griffiths 3e §5.1.1, p.256)*
Show that two identical fermions cannot occupy the same one-particle state, while
two bosons can.
*Answer:* setting $\psi_b=\psi_a$ in $\Psi_-=A[\psi_a(1)\psi_a(2)-\psi_a(1)\psi_a(2)]=0$
— "no wave function at all." For bosons $\Psi_+=2A\,\psi_a(1)\psi_a(2)\neq0$.
*Check:* `a = np.array([.3,.4,-.5,.7]); a/=norm(a)`;
`norm(antisymmetrize(a,a))` $=0$, while `norm(symmetrize(a,a))` $=1$.
(`test_pauli_exclusion_two_identical_orbitals`, `test_bosons_may_share_a_state`.)

**Solution.** Set $\psi_b=\psi_a$ in the two combinations. The antisymmetric one has two
identical tensor terms that cancel exactly,
$$\Psi_-=A\big(|a\rangle|a\rangle-|a\rangle|a\rangle\big)=0,$$
"no wave function at all" — two identical fermions cannot share a state, the Pauli exclusion
principle. The symmetric one does **not** cancel: $\Psi_+=A\cdot2\,|a\rangle|a\rangle$, which
normalizes to the plain product $|a\rangle\otimes|a\rangle$, so any number of bosons may pile
into one state. Hence `norm(antisymmetrize(a,a))` $=0$ while `norm(symmetrize(a,a))` $=1$.

### P3.  The normalization constant $A$  *(Griffiths 3e, Problem 5.4, p.257)*
For $\Psi_\pm=A[\psi_a(1)\psi_b(2)\pm\psi_b(1)\psi_a(2)]$ find $A$ (a) when
$\psi_a,\psi_b$ are orthonormal, and (b) for bosons with $\psi_a=\psi_b$
normalized.
*Answer:* (a) $\|\psi_a(1)\psi_b(2)\pm\psi_b(1)\psi_a(2)\|=\sqrt2$, so
$A=1/\sqrt2$. (b) the symmetric state is $2A\,\psi_a(1)\psi_a(2)$ with
$\|\,\|=2|A|=1$, so $A=\tfrac12$. (For non-orthogonal normalized orbitals with
overlap $s$, $A=1/\sqrt{2(1\pm|s|^2)}$.)
*Check:* orthonormal `a,b = np.eye(2)`: `norm(tensor(a,b)+tensor(b,a))`$=\sqrt2$;
non-orthogonal `b=np.array([1,1])/np.sqrt(2)` ($|s|^2=\tfrac12$):
`norm(tensor(a,b)+tensor(b,a))`$=\sqrt3$, `...-...`$=1$.
(`test_general_normalization_nonorthogonal`.)

**Solution.** Expand the squared norm of the raw combination using $\langle a|a\rangle=\langle b|b\rangle=1$:
$$\big\|\,|a\rangle|b\rangle\pm|b\rangle|a\rangle\,\big\|^2=\langle a|a\rangle\langle b|b\rangle+\langle b|b\rangle\langle a|a\rangle\pm2|\langle a|b\rangle|^2=2(1\pm|s|^2),\qquad s=\langle a|b\rangle.$$
(a) Orthonormal ($s=0$): the norm is $\sqrt2$, so $A=1/\sqrt2$. (b) Bosons with $\psi_a=\psi_b$:
the symmetric state is $2A\,|a\rangle|a\rangle$ of norm $2|A|=1$, so $A=\tfrac12$. In general
$A=1/\sqrt{2(1\pm|s|^2)}$. Numerically the orthonormal raw norm is $\sqrt2=1.4142$, while for
$b=(1,1)/\sqrt2$ (so $|s|^2=\tfrac12$) the sum has norm $\sqrt3=1.7321$ and the difference norm $1$.

### P4.  The Slater determinant for three fermions  *(Griffiths 3e, Problem 5.8, p.262)*
Construct the completely antisymmetric state of three fermions in orthonormal
orbitals $\phi_1,\phi_2,\phi_3$ and verify it changes sign under the interchange
of *any* pair.
*Answer:* the $3\times3$ Slater determinant, equivalently
$\Psi=\tfrac{1}{\sqrt6}\sum_{\sigma}\mathrm{sgn}(\sigma)\,\phi_{\sigma(1)}\phi_{\sigma(2)}\phi_{\sigma(3)}$;
any pair swap permutes two columns, so $\Psi\to-\Psi$.
*Check:* `e = np.eye(3); Psi = slater_determinant([e[0],e[1],e[2]])`; for each
pair `(p,q)`: `np.allclose(apply_pair_swap(Psi,3,3,p,q), -Psi)`.
(`test_slater_antisymmetric_under_any_pair_swap`.)

**Solution.** The completely antisymmetric three-fermion state is the antisymmetrizer applied
to the product,
$$\Psi=\frac{1}{\sqrt{3!}}\sum_{\sigma\in S_3}\mathrm{sgn}(\sigma)\,|\phi_{\sigma(1)}\rangle|\phi_{\sigma(2)}\rangle|\phi_{\sigma(3)}\rangle,$$
the tensor-space form of the $3\times3$ Slater determinant $\det[\phi_i(\mathbf r_j)]$.
Interchanging particles $p$ and $q$ permutes two *columns* of that determinant, which flips its
sign, so $P_{pq}\Psi=-\Psi$ for every pair. With $\phi_i=e_i$ the code confirms
`apply_pair_swap(Psi,3,3,p,q)` $=-\Psi$ for all three pairs $(0,1),(0,2),(1,2)$.

### P5.  Two equal rows, and the $1/\sqrt{N!}$ factor  *(Griffiths 3e, Problem 5.8, p.262)*
Show that the Slater determinant vanishes if two orbitals coincide (Pauli for $N$
fermions), and that for orthonormal orbitals the prefactor is $1/\sqrt{N!}$.
*Answer:* two equal orbitals are two equal rows $\Rightarrow\det=0$. The raw
antisymmetric sum has $\langle\Psi|\Psi\rangle=\sum_\sigma1=N!$, so dividing by
$\sqrt{N!}$ normalizes it.
*Check:* `norm(slater_determinant([e[0],e[1],e[0]]))` $=0$;
`norm(slater_determinant([e[0],e[1],e[2]], normalize_state=False))` $=\sqrt{3!}=\sqrt6$.
(`test_slater_vanishes_if_two_orbitals_coincide`,
`test_slater_normalization_is_sqrt_N_factorial`.)

**Solution.** If two orbitals coincide the determinant has two equal *rows*, and a determinant
with two equal rows is zero — Pauli exclusion for $N$ fermions. For the prefactor, expand the
raw antisymmetric sum's norm with orthonormal orbitals: cross terms between distinct
permutations vanish (each carries a factor $\langle\phi_i|\phi_j\rangle=0$), leaving one
surviving term per permutation,
$$\langle\Psi|\Psi\rangle=\sum_{\sigma\in S_N}1=N!,$$
so the raw norm is $\sqrt{N!}$ and dividing by it normalizes the state. Hence
`norm(slater_determinant([e[0],e[1],e[0]]))` $=0$ and the raw norm
`norm(...,normalize_state=False)` $=\sqrt{3!}=\sqrt6=2.449$.

### P6.  Exchange force in the infinite well  *(Griffiths 3e, Problem 5.6, p.261)*
Two noninteracting particles in the infinite well, one in $\psi_1$, one in
$\psi_2$. Compute $\langle(x_1-x_2)^2\rangle$ for distinguishable, boson and
fermion cases (width $L=1$).
*Answer:* $\langle x\rangle_n=\tfrac L2$, $\langle x^2\rangle_n=L^2(\tfrac13-\tfrac1{2n^2\pi^2})$,
and $\langle x\rangle_{12}=-\tfrac{16L}{9\pi^2}$, giving distinguishable
$=L^2(\tfrac16-\tfrac{5}{8\pi^2})\approx0.1033\,L^2$ and an exchange term
$2|\langle x\rangle_{12}|^2=\tfrac{512L^2}{81\pi^4}\approx0.0649\,L^2$, so
boson $\approx0.0384\,L^2$ and fermion $\approx0.1682\,L^2$.
*Check:* `x=np.linspace(0,1,8001); r=exchange_dx2(well_state(1,x),well_state(2,x),x)`;
`r["distinguishable"]`$\approx0.1033$, `r["exchange_term"]`$\approx0.0649$,
`r["boson"] < r["distinguishable"] < r["fermion"]`.
(`test_exchange_force_infinite_well_closed_form`,
`test_exchange_force_ordering_infinite_well`.)

**Solution.** For the well $\langle x\rangle_n=\tfrac L2$ and $\langle x^2\rangle_n=L^2(\tfrac13-\tfrac1{2n^2\pi^2})$,
while the off-diagonal element is
$$\langle x\rangle_{12}=\int_0^L x\,\tfrac2L\sin\tfrac{\pi x}L\,\sin\tfrac{2\pi x}L\,dx=-\frac{16L}{9\pi^2}.$$
The distinguishable value is $\langle x^2\rangle_1+\langle x^2\rangle_2-2\langle x\rangle_1\langle x\rangle_2=L^2(\tfrac16-\tfrac5{8\pi^2})\approx0.1033$,
and the exchange term is $2|\langle x\rangle_{12}|^2=\tfrac{512L^2}{81\pi^4}\approx0.0649$. Bosons
subtract it (closer, $\approx0.0384$), fermions add it (farther, $\approx0.1682$). This matches
`r["distinguishable"]` $\approx0.1033$, `r["exchange_term"]` $\approx0.0649$, with
`r["boson"] < r["distinguishable"] < r["fermion"]`.

### P7.  Exchange force in the harmonic oscillator  *(Griffiths 3e, Problem 5.7, p.261)*
Two particles share a harmonic-oscillator potential, one in the ground state, one
in the first excited state. Find $\langle(x_1-x_2)^2\rangle$ for the three cases
(natural units $\hbar=m=\omega=1$).
*Answer:* $\langle x\rangle_0=\langle x\rangle_1=0$, $\langle x^2\rangle_0=\tfrac12$,
$\langle x^2\rangle_1=\tfrac32$, and $\langle x\rangle_{01}=\tfrac1{\sqrt2}$, so
distinguishable $=2$, exchange term $2|\langle x\rangle_{01}|^2=1$, hence
boson $=1$, fermion $=3$ (units $\hbar/m\omega$).
*Check:* `x=np.linspace(-9,9,8001); r=exchange_dx2(ho_state(0,x),ho_state(1,x),x)`;
`r["distinguishable"]`$\approx2$, `r["boson"]`$\approx1$, `r["fermion"]`$\approx3$.
(`test_exchange_force_harmonic_oscillator_closed_form`.)

**Solution.** In natural units $\langle x\rangle_n=0$ and $\langle x^2\rangle_n=n+\tfrac12$, so
$\langle x^2\rangle_0=\tfrac12$ and $\langle x^2\rangle_1=\tfrac32$. Writing
$x=\tfrac1{\sqrt2}(a+a^\dagger)$ gives the one nonzero off-diagonal element
$$\langle x\rangle_{01}=\tfrac1{\sqrt2}\langle0|(a+a^\dagger)|1\rangle=\tfrac1{\sqrt2}.$$
Then distinguishable $=\langle x^2\rangle_0+\langle x^2\rangle_1-0=2$ and the exchange term
$2|\langle x\rangle_{01}|^2=1$, so boson $=2-1=1$ and fermion $=2+1=3$. Confirmed by
`r["distinguishable"]` $\approx2$, `r["boson"]` $\approx1$, `r["fermion"]` $\approx3$.

### P8.  Chicago and Seattle — no overlap, no exchange  *(Griffiths 3e §5.1.2, p.260)*
Show that the exchange term vanishes if the two orbitals do not overlap, so
spatially separated identical particles behave as distinguishable.
*Answer:* the exchange term is $\mp2|\langle x\rangle_{ab}|^2$ with
$\langle x\rangle_{ab}=\int x\,\psi_a^*\psi_b\,dx$; if $\psi_a\psi_b=0$ everywhere
the integral is $0$, so boson $=$ fermion $=$ distinguishable.
*Check:* place $\psi_a$ on $[0,1]$ and $\psi_b$ on $[2,3]$:
`x=np.linspace(0,3,9001)`,
`a=np.where(x<=1, well_state(1,x), 0.)`,
`b=np.where((x>=2)&(x<=3), well_state(1,x-2), 0.)`,
`r=exchange_dx2(a,b,x)`: `abs(r["exchange_term"]) < 1e-10`.
(`test_no_exchange_force_without_overlap`.)

**Solution.** The entire identical-particle effect rides on the off-diagonal element
$\langle x\rangle_{ab}=\int x\,\psi_a^*(x)\psi_b(x)\,dx$. If the orbitals have disjoint support —
$\psi_a$ on $[0,1]$, $\psi_b$ on $[2,3]$ — then the product $\psi_a^*(x)\psi_b(x)=0$ at every
$x$, so the integrand vanishes identically and $\langle x\rangle_{ab}=0$. The exchange term
$2|\langle x\rangle_{ab}|^2$ is then $0$ and boson $=$ distinguishable $=$ fermion: spatially
separated identical particles behave as distinguishable. The code gives
`abs(r["exchange_term"]) < 1e-10` (here exactly $0$), with the three $\langle(\Delta x)^2\rangle$ values equal.

### P9.  Helium's ground state forces the spin singlet  *(Griffiths 3e §5.1.3, p.263)*
The two electrons of helium in the $1s^2$ ground state share the same spatial
orbital. What spin state must they be in, and why can't they both be spin up?
*Answer:* the spatial part $1s(1)\,1s(2)$ is symmetric ($P_{12}=+1$); the total
two-electron state must be antisymmetric, so the spin part must be the
antisymmetric **singlet** ($P_{12}=-1$). "Both spin up" is the symmetric
$|\!\uparrow\uparrow\rangle$ paired with the symmetric spatial state — overall
symmetric, forbidden; equivalently the antisymmetrizer of two identical
$|\!\uparrow\rangle$ spins is zero (Pauli).
*Check:* `P=swap_operator(2)`; `s=singlet()`: `np.allclose(P@s, -s)` (antisym.);
`norm(antisymmetrize(spin_up(), spin_up()))` $=0$ (both-up forbidden);
each `triplet()` state has `np.allclose(P@t, +t)`.
(`test_spin_singlet_antisymmetric_triplet_symmetric`,
`test_helium_ground_state_requires_singlet`.)

**Solution.** The full two-electron state must be antisymmetric. In $1s^2$ both electrons share
the *same* spatial orbital, so the spatial part $1s(1)\,1s(2)$ is symmetric, $P_{12}=+1$. To make
the product antisymmetric the spin part must carry $P_{12}=-1$, i.e. the antisymmetric
**singlet** $\tfrac1{\sqrt2}(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)$; the
product of exchange eigenvalues is $(+1)(-1)=-1$. "Both spin up" is the symmetric
$|\!\uparrow\uparrow\rangle$, which paired with the symmetric spatial state is overall symmetric —
forbidden; equivalently antisymmetrizing two identical $|\!\uparrow\rangle$ spins gives the zero
vector. Hence `P@s` $=-s$, `norm(antisymmetrize(spin_up(), spin_up()))` $=0$, and each
`triplet()` state satisfies `P@t` $=+t$.
