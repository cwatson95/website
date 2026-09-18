# QM-12 — Central Potentials & the Hydrogen Atom (notes)

The hydrogen atom is the showpiece of quantum mechanics: a realistic,
three-dimensional system solved **exactly** in closed form, whose spectrum is the
$-13.6/n^2$ eV ladder that the old Bohr model (`~QM-01`) only guessed. This note
takes the standard route (Griffiths 3e §4.1.3–§4.2): separate the Schrödinger
equation in spherical coordinates, reduce the angular part to the spherical
harmonics of `~QM-10`, and solve the radial part — first for a general central
potential, then for the Coulomb well.

Energies and lengths are quoted in SI in the formulae but the code uses **atomic
units** $\hbar=m=e=4\pi\varepsilon_0=1$, where $a_0=1$ and $E_n=-1/2n^2$ Ha.

## 1. Separation in spherical coordinates

For any potential that depends only on the distance from the origin, $V=V(r)$
(a **central potential**), the time-independent Schrödinger equation
$-\tfrac{\hbar^2}{2m}\nabla^2\psi+V\psi=E\psi$ separates in spherical coordinates
(Griffiths 3e §4.1, p.171). Writing
$$\psi(r,\theta,\phi)=R(r)\,Y_l^m(\theta,\phi),$$
the angular factor is the **same for every central potential** — it is the
spherical harmonic of `~QM-10`, the simultaneous eigenfunction of $L^2$ and $L_z$
(Griffiths 3e §4.1.3, p.180: *"the angular part… is the same for all spherically
symmetric potentials; the actual shape of the potential affects only the radial
part"*). The angular equation contributes the separation constant
$$L^2\,Y_l^m=\hbar^2 l(l+1)\,Y_l^m,$$
so all of the potential's physics lives in $R(r)$, labelled by $l$.

## 2. The radial equation and the centrifugal barrier

Substituting the product form and using $L^2Y_l^m=\hbar^2l(l+1)Y_l^m$ gives the
**radial equation** (Griffiths 3e §4.1.3, Eq. 4.37, p.180). It simplifies under
the substitution $u(r)\equiv rR(r)$ to a one-dimensional Schrödinger equation:
$$\boxed{\,-\frac{\hbar^2}{2m}\frac{d^2u}{dr^2}+\underbrace{\left[V(r)+\frac{\hbar^2}{2m}\frac{l(l+1)}{r^2}\right]}_{V_{\text{eff}}(r)}u=E\,u\,}$$
This is *identical in form to the 1-D problems of `~QM-08`*, except that the
effective potential carries an extra repulsive piece — the **centrifugal term**
$\tfrac{\hbar^2 l(l+1)}{2mr^2}$ — which "tends to throw the particle outward, just
like the centrifugal pseudo-force" of classical mechanics (Griffiths 3e p.180).
The boundary condition is $u(0)=0$ (so that $R=u/r$ does not blow up at the
origin, Griffiths 3e p.181).

In **atomic units** with the Coulomb potential $V=-1/r$, the boxed equation is
$$-\tfrac12 u''+\Big[-\tfrac1r+\tfrac{l(l+1)}{2r^2}\Big]u=Eu
\quad\Longleftrightarrow\quad
u''=\Big[\frac{l(l+1)}{r^2}-\frac{2}{r}-2E\Big]u,$$
which is exactly what `radial_solve(l)` discretizes (3-point stencil, Dirichlet
walls at $r=0$ and $r=r_{\max}$, the symmetric-tridiagonal eigenproblem of
`~QM-08`/`~MA-20`). It recovers $E_n$ below to $<0.5\%$ for $n=1,2,3$ and its
eigenvector matches $rR_{nl}(r)$.

## 3. The Coulomb problem and the Bohr spectrum

For hydrogen the electron sits in the Coulomb well of the proton (Griffiths 3e
§4.2, Eq. 4.52, p.185):
$$V(r)=-\frac{e^2}{4\pi\varepsilon_0}\frac1r.$$
Following the oscillator method (`~QM-09`): peel off the asymptotic behaviour
$u\sim e^{-\kappa r}$ at large $r$ (with $\kappa=\sqrt{-2mE}/\hbar$, real for
bound $E<0$) and $u\sim r^{l+1}$ at small $r$ (Griffiths 3e §4.2.1, p.187), then
expand the remainder as a power series. The series **must terminate** or the
wavefunction blows up — and termination at order $N$ forces $\kappa$ to take
discrete values (Griffiths 3e p.189). The result is the **allowed energies**
(Griffiths 3e Eq. 4.70, p.189 — *"the famous Bohr formula… the most important
result in all of quantum mechanics,"* p.190):
$$\boxed{\,E_n=-\left[\frac{m}{2\hbar^2}\!\left(\frac{e^2}{4\pi\varepsilon_0}\right)^{\!2}\right]\frac{1}{n^2}=-\frac{13.606\ \text{eV}}{n^2},\qquad n=1,2,3,\dots\,}$$
In atomic units this is simply $E_n=-\tfrac1{2n^2}$ Ha. The principal quantum
number is $n=N+l+1$, so the lowest state for a given $l$ has $n=l+1$. The ground
state $E_1=-13.6$ eV is the **binding (ionization) energy** of hydrogen
(Griffiths 3e p.190). This is the *same* spectrum the Bohr model produced
(`~QM-01`), now for the right reason — and `~QM-01`'s Rydberg formula
$1/\lambda=R(1/n_1^2-1/n_2^2)$ is just $hc/\lambda=E_{n_2}-E_{n_1}$ (Griffiths 3e
§4.2.2, Eq. 4.93, p.198).

## 4. Quantum numbers $(n,l,m)$ and the $n^2$ degeneracy

The wavefunctions are labelled by **three** quantum numbers (Griffiths 3e
Eq. 4.75, p.190):
$$\psi_{nlm}(r,\theta,\phi)=R_{nl}(r)\,Y_l^m(\theta,\phi).$$
Termination of the radial series caps $l$ at $n-1$, and `~QM-10`'s angular theory
caps $|m|$ at $l$ (Griffiths 3e p.191):
$$n=1,2,3,\dots;\qquad l=0,1,\dots,n-1;\qquad m=-l,-l+1,\dots,+l.$$
Because $E_n$ depends on $n$ **alone**, every $(l,m)$ with the same $n$ shares the
energy. Summing the $2l+1$ values of $m$ over the $n$ allowed $l$ gives the
**degeneracy**
$$\boxed{\,\sum_{l=0}^{n-1}(2l+1)=n^2\,}$$
(Griffiths 3e p.191; `count_states(n)` does the sum, `degeneracy(n)` the closed
form). The $m$-degeneracy ($2l+1$) holds for *any* central potential — it is the
rotational symmetry of `~QM-10`. The extra **"accidental" $l$-degeneracy** (that
$2s$ and $2p$ coincide) is special to the $1/r$ potential (Griffiths 3e p.192,
Fig. 4.6); it is the quantum face of the closed Kepler orbit of `~CM-11`, and it
is **lifted** by the fine-structure corrections of `~QM-17`. (Spin doubles every
count to $2n^2$ — that is `~QM-11`.)

## 5. The radial wavefunctions $R_{nl}$ and their nodes

The terminating series is, up to normalization, an **associated Laguerre
polynomial** (Griffiths 3e Eq. 4.87–4.88, p.192): $L_{n-l-1}^{\,2l+1}(2r/na)$,
the $\alpha=2l+1$ generalization of the ordinary Laguerre $L_k$ of `~MA-12`
(`generalized_laguerre`; the code verifies $L_k^{(0)}$ equals MA-12's `laguerre`).
The normalized radial functions are (Griffiths 3e Eq. 4.89, p.192; here in atomic
units, $a_0=1$):
$$\boxed{\,R_{nl}(r)=\sqrt{\left(\frac{2}{n}\right)^{\!3}\frac{(n-l-1)!}{2n\,(n+l)!}}\;
e^{-r/n}\left(\frac{2r}{n}\right)^{\!l}L_{n-l-1}^{\,2l+1}\!\left(\frac{2r}{n}\right)}$$
For example $R_{10}=2e^{-r}$ and $R_{20}=\tfrac{1}{2\sqrt2}(2-r)e^{-r/2}$
(Griffiths 3e Eq. 4.80–4.82, Table 4.7). They are normalized,
$\int_0^\infty|R_{nl}|^2r^2\,dr=1$, and orthogonal in $n$ for fixed $l$
(Griffiths 3e Eq. 4.90, p.193 — *because* they are eigenfunctions of a Hermitian
radial operator). The polynomial has degree $n-l-1$, so $R_{nl}$ has exactly
$$\#\text{radial nodes}=n-l-1$$
(Griffiths 3e p.195). The node count is what visually distinguishes orbitals of
the same energy: $3s$ ($n{-}l{-}1=2$), $3p$ ($1$), $3d$ ($0$). `count_radial_nodes`
confirms this for all of them.

## 6. $\langle r\rangle$ and the Bohr radius

The natural length scale that drops out is the **Bohr radius** (Griffiths 3e
Eq. 4.72, p.190)
$$a_0=\frac{4\pi\varepsilon_0\hbar^2}{me^2}=0.529\ \text{Å}\quad(=1\ \text{in atomic units}).$$
A common trap: $a_0$ is the *most probable* radius (the peak of the radial
density $P(r)=r^2|R_{10}|^2$, at $r=a_0$ — Griffiths 3e Problem 4.16), but the
**mean** radius is larger because $P(r)$ has a long tail:
$$\boxed{\,\langle r\rangle_{nl}=\int_0^\infty r\,|R_{nl}|^2r^2\,dr=\tfrac12\big[3n^2-l(l+1)\big]a_0\,}$$
For the ground state $\langle r\rangle_{10}=\tfrac32 a_0$ (Griffiths 3e
Problem 4.15a), **not** $a_0$. The growth $\langle r\rangle\sim n^2$ is the
quantum echo of the classical Kepler relation between orbit size and energy
(`~CM-11`, bridge B4). `expectation_r` integrates the density and matches
`expectation_r_closed`.

---
### Why this is a keystone of the QM trunk
The hydrogen atom ties the trunk together:
- it **realizes** `~QM-10`: every orbital is $R_{nl}Y_l^m$, the $Y_l^m$ the exact
  angular factor and the source of the $2l+1$ $m$-degeneracy;
- it **vindicates** `~QM-01`: the Bohr $-13.6/n^2$ eV spectrum, now derived;
- it **uses** `~MA-12`: the associated Laguerre polynomials *are* the radial
  functions, just as Hermite are the oscillator's (`~QM-09`);
- it is the **starting point** for `~QM-17` (fine structure lifts the accidental
  degeneracy), `~QM-21` (perturbation theory), and `~QM-13` (the periodic table,
  by filling hydrogenic shells);
- and it is the quantum image of the classical central-force problem `~CM-11`.
The lesson: *separate the symmetry off into the angles, and a 3-D atom becomes a
1-D radial problem you can solve exactly.*
