# QM-10 — Angular Momentum (notes)

Angular momentum is where quantum mechanics shows its hand most clearly. For the
energy levels of the harmonic oscillator (`~QM-05`) or the hydrogen atom
(`~QM-12`) you can, if you insist, grind through a differential equation. For
angular momentum you don't have to: **the eigenvalues are forced by a single
commutation algebra**, and the differential equation only reappears at the very
end to name the eigenfunctions. This note follows that algebraic route
(Griffiths 3e §4.3), then connects it to the spherical harmonics (§4.1.2, §4.3.2).

Throughout, $\hbar$ is kept explicit in the formulae; the code uses natural units
$\hbar=1$ (documented in `angular_momentum.py`).

## 1. The observable: $\mathbf L=\mathbf r\times\mathbf p$

Classically the angular momentum of a particle about the origin is
$\mathbf L=\mathbf r\times\mathbf p$, i.e. $L_x=yp_z-zp_y$, and cyclically
(Griffiths 3e §4.3, p.201). Promote it to an operator by the canonical
prescription $\mathbf p\to-i\hbar\nabla$:
$$L_x=-i\hbar\Big(y\partial_z-z\partial_y\Big),\quad\text{etc.}$$
In the classical theory of central forces, energy *and* angular momentum are the
conserved quantities; the same is true here (Griffiths §4.3, p.201), and `~CM-09`
is the classical statement this module quantizes (**bridge B3**).

## 2. The algebra: $[L_i,L_j]=i\hbar\,\varepsilon_{ijk}L_k$

From the canonical relations $[x,p_x]=i\hbar$ (and $[x,p_y]=0$, …) a short
computation gives (Griffiths 3e Eq. 4.99, p.202)
$$\boxed{\,[L_x,L_y]=i\hbar L_z,\qquad [L_y,L_z]=i\hbar L_x,\qquad [L_z,L_x]=i\hbar L_y\,}$$
— the **fundamental commutation relations for angular momentum; everything
follows from them.** They say the three components are *incompatible
observables*: by the generalized uncertainty principle you cannot have a
simultaneous eigenstate of any two (Griffiths Eq. 4.100, p.202). So angular
momentum can never point exactly along an axis.

But the **total** $L^2=L_x^2+L_y^2+L_z^2$ commutes with each component
(Griffiths Eq. 4.101–4.103, p.202):
$$[L^2,L_x]=[L^2,L_y]=[L^2,L_z]=0.$$
Hence $L^2$ is *compatible* with (say) $L_z$, and we may look for simultaneous
eigenstates $f$ of $L^2$ and $L_z$ — labelled, in the end, by the two numbers
$l$ and $m$. *(The code verifies all of §2 to machine precision in
`test_commutators_cyclic`, `test_L2_commutes_with_each_component`,
`test_casimir_is_l_l_plus_one`.)*

## 3. The ladder: $L_\pm=L_x\pm iL_y$

Define the **ladder operators** (Griffiths 3e Eq. 4.105, p.203)
$$\boxed{\,L_\pm=L_x\pm iL_y\,}$$
Their commutators with $L_z$ and $L^2$ are
$$[L_z,L_\pm]=\pm\hbar L_\pm,\qquad [L^2,L_\pm]=0.$$
The first relation is the engine. If $f$ is a simultaneous eigenstate with
$L_zf=\hbar m\,f$ and $L^2f=\lambda f$, then $L_\pm f$ is *also* an eigenstate:
$L^2$ is unchanged ($[L^2,L_\pm]=0$), while
$$L_z(L_\pm f)=(L_\pm L_z\pm\hbar L_\pm)f=\hbar(m\pm1)\,(L_\pm f).$$
So $L_+$ **raises** $m$ by one and $L_-$ **lowers** it — a ladder of states all
sharing the same $L^2$ (Griffiths p.203, Fig. 4.11).

## 4. The spectrum — quantization from termination

The ladder cannot run forever: $L_z^2\le L^2$, so $m$ is bounded. There must be a
**top rung** $f_{\text{top}}$ with $L_+f_{\text{top}}=0$ and a **bottom rung**
with $L_-f_{\text{bot}}=0$ (Griffiths 3e p.203–204). Using
$L_\mp L_\pm = L^2-L_z^2\mp\hbar L_z$ at each end and calling the top value of
$m$ by the name $l$, both ends give the *same* $\lambda$, which forces the
bottom value to be $-l$ and the number of steps to be an integer. The results
(Griffiths Eq. 4.118–4.119, p.205):
$$\boxed{\,L^2f_l^m=\hbar^2\,l(l+1)\,f_l^m,\qquad L_zf_l^m=\hbar m\,f_l^m\,}$$
with
$$m=-l,\,-l+1,\,\dots,\,l-1,\,l\qquad(\,2l+1\ \text{values}\,),$$
and $l=0,\tfrac12,1,\tfrac32,2,\dots$ — **integer or half-integer**, the only
constraint the algebra imposes. Note $\sqrt{l(l+1)}>l$ (except $l=0$): the
magnitude always exceeds the largest projection, the geometric face of the
uncertainty principle (Griffiths p.205, Fig. 4.12, drawn for $l=2$).

The normalization of a ladder step (Griffiths 3e Problem 4.21, p.206) is
$$L_\pm\,f_l^m=\hbar\sqrt{l(l+1)-m(m\pm1)}\;f_l^{\,m\pm1},$$
and $\sqrt{l(l+1)-m(m\pm1)}$ vanishes exactly at $m=\pm l$ — that is *why* the
ladder terminates. **This $\hbar\sqrt{l(l+1)-m(m\pm1)}$ is the matrix element the
code uses to build $L_\pm$.**

## 5. Matrix representation (what the code constructs)

For a fixed $l$ the $2l+1$ kets $|l,m\rangle$ form a basis, and the operators
become $(2l+1)\times(2l+1)$ matrices. Ordering $m=l,l-1,\dots,-l$:
$$L_z=\hbar\,\mathrm{diag}(l,\dots,-l),\qquad
(L_+)_{m+1,\,m}=(L_-)^\dagger_{\,m+1,m}=\hbar\sqrt{l(l+1)-m(m+1)},$$
then $L_x=\tfrac12(L_++L_-)$, $L_y=\tfrac1{2i}(L_+-L_-)$, and
$L^2=L_x^2+L_y^2+L_z^2$. Unlike the position/momentum matrices of `~QM-05`, this
representation is **finite and closes exactly**: the code checks
$[L_x,L_y]=i\hbar L_z$ (and cyclic) and $L^2=\hbar^2l(l+1)\,\mathbb 1$ to
$\sim10^{-12}$, for $l=\tfrac12,1,\tfrac32,2$.

The smallest nontrivial case $l=\tfrac12$ gives
$L_i=\tfrac{\hbar}{2}\sigma_i$ with $\sigma_i$ the **Pauli matrices** — the
entire content of `~QM-11` (spin-$\tfrac12$). The half-integer rungs are exactly
the representations that have *no* position-space wavefunction (next section), so
"spin" is what is left of angular momentum when you discard $\mathbf r\times\mathbf p$.

## 6. Position space: the spherical harmonics $Y_l^m(\theta,\phi)$

Where do the eigenfunctions live? Separating the time-independent Schrödinger
equation for any central potential gives the **angular equation** (Griffiths 3e
§4.1.2, p.176). Its $\phi$-part is trivial,
$$\Phi(\phi)=e^{im\phi},$$
and single-valuedness under $\phi\to\phi+2\pi$ forces $m$ — and hence $l$ — to be
an **integer** (Griffiths Eq. 4.22, p.176). The $\theta$-part is the associated
Legendre equation, solved by $P_l^m(\cos\theta)$ (Griffiths Eq. 4.27, p.177; this
is exactly `~MA-12`'s `assoc_legendre`). The normalized product is the
**spherical harmonic** (Griffiths Eq. 4.32, p.178):
$$\boxed{\,Y_l^m(\theta,\phi)=\sqrt{\frac{2l+1}{4\pi}\frac{(l-m)!}{(l+m)!}}\;
P_l^m(\cos\theta)\,e^{im\phi}\,}\qquad(Y_l^{-m}=(-1)^m\,{Y_l^{m}}^{\!*}),$$
orthonormal over the sphere (Griffiths Eq. 4.33, p.178):
$$\int_0^{2\pi}\!\!\int_0^{\pi} {Y_l^m}^{*}\,Y_{l'}^{m'}\,\sin\theta\,d\theta\,d\phi=\delta_{ll'}\delta_{mm'}.$$

Rewriting the operators in spherical coordinates (Griffiths 3e §4.3.2, p.208)
gives the punchline $L_z=-i\hbar\,\partial_\phi$, so on $Y_l^m\propto e^{im\phi}$
$$L_z\,Y_l^m=-i\hbar\,\partial_\phi\,Y_l^m=\hbar m\,Y_l^m,$$
and likewise $L^2Y_l^m=\hbar^2l(l+1)Y_l^m$. **The $Y_l^m$ are nothing but the
algebraic eigenstates of §4, realised as functions on the sphere** (Griffiths
p.206) — which is *why* they are orthogonal: eigenfunctions of the Hermitian
operators $L^2,L_z$ for distinct eigenvalues. The code builds $Y_l^m$ from
`~MA-12`, then verifies orthonormality by integrating over the sphere, matches
Griffiths' Table 4.3 closed forms (e.g. $Y_0^0=1/\sqrt{4\pi}$,
$Y_1^0=\sqrt{3/4\pi}\cos\theta$), and confirms $-i\hbar\,\partial_\phi Y_l^m=\hbar m\,Y_l^m$ numerically.

---
### Why this is the hinge of the QM trunk
Angular momentum is the template for every later quantization-by-algebra:
- **Spin** (`~QM-11`) is the same algebra with the half-integer $l$ that §4 allows
  but §6 forbids a wavefunction — the Pauli matrices of §5.
- **Hydrogen** (`~QM-12`): the $Y_l^m$ are the exact angular factor of every
  orbital; only the radial equation remains.
- **Addition of angular momenta** (`~QM-13`): two such ladders combine via
  Clebsch–Gordan coefficients.
- Classically the same object is `~CM-09` (conserved $\mathbf L$ under central
  forces) feeding `~CM-13` (the inertia tensor) — bridge **B3** of the network.
The lesson: *find the commutators, and the spectrum builds itself.*
