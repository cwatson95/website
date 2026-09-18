# MA-18 — Problems

Work by hand, then check with `code/groups.py`. Citations in `../refs.md`.

### P1.  Cayley table & the axioms  *(standard — see refs)*
Write the Cayley table of Z₄ and of the Klein four-group. Verify closure,
identity, inverses, associativity, and that each row/column is a permutation (a
Latin square). *Check:* `cyclic_group(4).is_group()`.

**Solution.** The Cayley table of $\mathbb{Z}_4$ under addition mod 4 is
$$\begin{array}{c|cccc} + & 0&1&2&3\\ \hline 0&0&1&2&3\\ 1&1&2&3&0\\ 2&2&3&0&1\\ 3&3&0&1&2\end{array}$$
Identity is $0$; inverses are $0\leftrightarrow0,\ 1\leftrightarrow3,\ 2\leftrightarrow2$; associativity is
inherited from integer addition; every row and column lists $0,1,2,3$ once (Latin square).
The Klein four-group $V=\{e,a,b,c\}$ satisfies the same axioms but with every non-identity
element self-inverse ($a^2=b^2=c^2=e,\ ab=c$), so it is *not* cyclic (no element of order 4)
whereas $\mathbb{Z}_4$ is. Both pass all four axioms, so `cyclic_group(4).is_group()` returns `True`.

### P2.  The smallest non-abelian group  *(standard — see refs)*
Show S₃ has order 6 and is non-abelian by exhibiting two permutations that don't
commute. List the element orders (1, 2, 3). *Check:* `symmetric_group(3).is_abelian()`
→ False.

**Solution.** $S_3$ permutes $\{0,1,2\}$, so $|S_3|=3!=6$. Take the transpositions
$a=(0\,1)\to(1,0,2)$ and $b=(1\,2)\to(0,2,1)$. With the code's convention $(p\circ q)[i]=p[q[i]]$,
$$ab=(1,2,0),\qquad ba=(2,0,1),$$
so $ab\ne ba$ — $S_3$ is the smallest non-abelian group. Its elements split by order: the
identity (order 1), the three transpositions (order 2), and the two 3-cycles
$(0\,1\,2),(0\,2\,1)$ (order 3), giving the order list $\{1,2,3\}$. Hence
`symmetric_group(3).is_abelian()` returns `False`.

### P3.  Lagrange's theorem  *(standard — see refs)*
Prove the order of a subgroup divides |G| (partition G into cosets). Deduce that a
group of prime order is cyclic. *Check:* `symmetric_group(4).subgroup_orders()` —
all divide 24.

**Solution.** Let $H\le G$. The left cosets $gH=\{gh:h\in H\}$ partition $G$: two cosets are
identical or disjoint, and every $g\in gH$ so they cover $G$. Each coset has exactly $|H|$
elements since $h\mapsto gh$ is a bijection. Therefore
$$|G|=[G:H]\,|H|\ \Longrightarrow\ |H|\ \big|\ |G|.$$
In particular the order of any element $a$, being $|\langle a\rangle|$, divides $|G|$. If
$|G|=p$ is prime, pick $a\ne e$: its order divides $p$ and exceeds $1$, hence equals $p$, so
$\langle a\rangle=G$ and $G\cong\mathbb{Z}_p$ is cyclic. The cyclic-subgroup orders of $S_4$ are
$\{1,2,3,4\}$, each dividing $24=|S_4|$, as `symmetric_group(4).subgroup_orders()` reports.

### P4.  D₃ = S₃, but D₄ ≠ S₄  *(standard — see refs)*
Realize the dihedral group as permutations of the n vertices. Show D₃ gives all 6
permutations (=S₃) but D₄ gives only 8 of the 24 in S₄. *Check:*
`set(dihedral_group(3).elements) == set(symmetric_group(3).elements)`.

**Solution.** Realize $D_n$ on the $n$ vertices as $n$ rotations $r_k:i\mapsto i+k$ and $n$
reflections $s_k:i\mapsto k-i$ (mod $n$), so $|D_n|=2n$ and $D_n\le S_n$ always. For $n=3$,
$|D_3|=2\cdot3=6=3!=|S_3|$; a subgroup of the same finite order *is* the whole group, so
$D_3=S_3$ — all six permutations of three points are triangle symmetries. For $n=4$,
$|D_4|=8$ while $|S_4|=24$, so $D_4$ is a *proper* subgroup: only the 8 permutations preserving
the square's edge-adjacency qualify. Thus
`set(dihedral_group(3).elements) == set(symmetric_group(3).elements)` is `True`, while $D_4$
supplies just 8 of 24.

### P5.  A representation is a homomorphism  *(Warner §3, p.82)*
Show ρ(k)=rotation by 2πk/n is a representation of Zₙ: ρ(a)ρ(b)=ρ(a+b). Why does
this make Zₙ a subgroup of SO(2)? *Check:* `cyclic_rep(6)`; `matmul(rep[a],rep[b])`
== `rep[(a+b)%6]`.

**Solution.** The planar rotation matrix
$R(\theta)=\begin{pmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{pmatrix}$ obeys the
addition law
$$R(\alpha)R(\beta)=\begin{pmatrix}\cos(\alpha+\beta)&-\sin(\alpha+\beta)\\ \sin(\alpha+\beta)&\cos(\alpha+\beta)\end{pmatrix}=R(\alpha+\beta),$$
using $\cos\alpha\cos\beta-\sin\alpha\sin\beta=\cos(\alpha+\beta)$. Setting $\rho(k)=R(2\pi k/n)$ and
using $2\pi$-periodicity, $\rho(a)\rho(b)=R\!\big(2\pi(a+b)/n\big)=\rho\big((a+b)\bmod n\big)$ — a
homomorphism $\mathbb{Z}_n\to SO(2)$ with $\rho(0)=I,\ \rho(k)^{-1}=\rho(n-k)$. Its image is the
$n$ equally spaced rotations, a cyclic subgroup of $SO(2)$. For $n=6$, $\rho(1)$ is the
$60^\circ$ rotation $\begin{pmatrix}0.5&-0.866\\ 0.866&0.5\end{pmatrix}$, and
`matmul(rep[a],rep[b]) == rep[(a+b)%6]` holds for all $a,b$.

### P6.  The rotation Lie algebra  *(Warner §3 p.85; §3.29 p.102)*
For the 3×3 rotation generators verify [Lₓ,L_y]=L_z (and cyclic). Then check the
Pauli matrices give [σₓ,σ_y]=2iσ_z — su(2), the double cover of so(3) (spin-½).
*Check:* `commutator(*so3_generators()[:2])`; `commutator(*pauli()[:2])`.

**Solution.** With the antisymmetric generators $L_x,L_y,L_z$ of `so3_generators()` (rotations
about the three axes), direct multiplication gives
$$[L_x,L_y]=L_xL_y-L_yL_x=\begin{pmatrix}0&-1&0\\ 1&0&0\\ 0&0&0\end{pmatrix}=L_z,$$
and cyclically $[L_y,L_z]=L_x,\ [L_z,L_x]=L_y$ — the algebra $[L_i,L_j]=\varepsilon_{ijk}L_k$ of
$so(3)$. For the Pauli matrices $\sigma_x\sigma_y=i\sigma_z$ and $\sigma_y\sigma_x=-i\sigma_z$, so
$$[\sigma_x,\sigma_y]=\sigma_x\sigma_y-\sigma_y\sigma_x=2i\,\sigma_z=\begin{pmatrix}2i&0\\ 0&-2i\end{pmatrix},$$
the $su(2)$ relation $[\sigma_i,\sigma_j]=2i\,\varepsilon_{ijk}\sigma_k$ — the double cover of $so(3)$
(spin-½). These match `commutator(*so3_generators()[:2])` $=L_z$ and
`commutator(*pauli()[:2])` $=2i\sigma_z$.
