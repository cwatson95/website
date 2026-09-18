# QM-12 — Problems

Work them by hand, then check with `code/hydrogen.py`. Sources in `../refs.md`.
Atomic units $\hbar=m=e=4\pi\varepsilon_0=1$ ($a_0=1$, energies in hartrees;
$\times$`HARTREE_EV` for eV), as in the code.

### P1.  The centrifugal barrier  *(Griffiths 3e §4.1.3, p.180)*
Write the effective radial potential for hydrogen and show that for $l>0$ it
turns *repulsive* near the origin. Why does this guarantee $R_{nl}\to0$ faster for
larger $l$?
*Answer:* $V_{\text{eff}}=-\tfrac1r+\tfrac{l(l+1)}{2r^2}$; as $r\to0$ the
$+l(l+1)/2r^2$ centrifugal term ($\propto r^{-2}$) dominates the Coulomb
$-1/r$, so $V_{\text{eff}}\to+\infty$ — a barrier that pushes the particle out and
forces $R_{nl}\sim r^l$ at small $r$.
*Check:* `effective_potential(0.01, 1)` $>0$ but `effective_potential(0.01, 0)` $<0$;
`effective_potential(0.1,2) > effective_potential(0.1,1) > effective_potential(0.1,0)`.
(`test_effective_potential_centrifugal_barrier`.)

**Solution.** The effective radial potential is $V_{\text{eff}}(r)=-\frac1r+\frac{l(l+1)}{2r^2}$.
Compare the two pieces as $r\to0$: the centrifugal term $\frac{l(l+1)}{2r^2}\sim r^{-2}$ blows
up faster than the Coulomb well $-\frac1r\sim r^{-1}$, so for any $l>0$ it dominates and
$V_{\text{eff}}\to+\infty$ — a repulsive wall. Keeping the leading terms in
$u''=[l(l+1)/r^2-\dots]u$ near the origin forces $u\sim r^{l+1}$, i.e. $R=u/r\sim r^l$, which
is suppressed more steeply the larger $l$. Numerically at $r=0.01$: $l{=}1$ gives
$V_{\text{eff}}=9900>0$ (barrier) but $l{=}0$ gives $-100<0$ (pure attraction); at $r=0.1$ the
values climb $290>90>-10$ for $l=2,1,0$ — exactly what `effective_potential` returns.

### P2.  Recover the Bohr spectrum by finite difference  *(Griffiths 3e Eq. 4.70, p.189)*
Without using the closed form, solve the radial equation
$u''=[l(l+1)/r^2-2/r-2E]u$ numerically and read off the lowest energies for
$l=0$. Confirm $E_1=-0.5$ Ha $=-13.6$ eV and the $1/n^2$ ladder.
*Answer:* $E_n=-1/(2n^2)$: $-0.5,-0.125,-0.0556,\dots$ Ha. The $k$-th state for
orbital $l$ has $n=l+1+k$.
*Check:* `radial_solve(0,3)[0]` $\approx[-0.5,-0.125,-0.0556]$;
`radial_solve(0,1)[0][0]*HARTREE_EV` $\approx-13.6$.
(`test_radial_solve_recovers_bohr_spectrum`.)

**Solution.** Setting $u=rR$ turns the radial equation into $u''=[l(l+1)/r^2-2/r-2E]u$. A
3-point stencil for $-\tfrac12 u''$ on $r_i=i\,\Delta r$ with Dirichlet walls $u(0)=u(r_{\max})=0$
makes $H$ symmetric tridiagonal, $H_{ii}=1/\Delta r^2+V_{\text{eff}}(r_i)$,
$H_{i,i\pm1}=-1/(2\Delta r^2)$. Diagonalizing for $l=0$ gives eigenvalues $E_k$ with $n=k+1$.
The Bohr prediction $E_n=-1/(2n^2)$ is $-0.5,-0.125,-0.0\overline{5}$ Ha, and the solver returns
`radial_solve(0,3)[0]`$=[-0.49999,-0.12500,-0.05556]$. The ground state in eV is
$-0.5\times27.2114=-13.61$ eV (`radial_solve(0,1)[0][0]*HARTREE_EV`$\approx-13.61$) — the
$-13.6/n^2$ ladder recovered purely numerically, no closed form used.

### P3.  Why $l<n$, and the $n^2$ degeneracy  *(Griffiths 3e p.191)*
For principal $n$, list the allowed $l$ and, for each, the number of $m$ states.
Sum them. Why is the total $n^2$, and which part of that degeneracy is generic to
any central potential?
*Answer:* $l=0,1,\dots,n-1$ (from series termination); each $l$ has $2l+1$ values
of $m$; $\sum_{l=0}^{n-1}(2l+1)=n^2$. The $2l+1$ ($m$-)degeneracy is generic
(rotational symmetry, `~QM-10`); the extra coincidence of different $l$ is the
"accidental" $1/r$ degeneracy, lifted by `~QM-17`.
*Answer (n=3):* $l\in\{0,1,2\}$ → $1+3+5=9=3^2$.
*Check:* `count_states(3)` $=9=$ `degeneracy(3)`; `allowed_l(3)` $=[0,1,2]$.
(`test_degeneracy_is_n_squared`, `test_allowed_l_and_m`.)

**Solution.** Series termination caps $l$ at $n-1$, so the allowed orbitals are
$l=0,1,\dots,n-1$ ($n$ of them), each carrying $2l+1$ magnetic substates $m=-l,\dots,+l$.
Summing the arithmetic series,
$$\sum_{l=0}^{n-1}(2l+1)=2\cdot\frac{(n-1)n}{2}+n=n^2.$$
For $n=3$: $l\in\{0,1,2\}$ gives $1+3+5=9=3^2$. The $2l+1$ factor is generic — the rotational
$L_z$ degeneracy of *any* central potential (`~QM-10`); the extra collapse of different $l$ to
one energy is the accidental $1/r$ degeneracy, lifted in `~QM-17`. Matches `allowed_l(3)`$=[0,1,2]$
and `count_states(3)`$=9=$`degeneracy(3)`.

### P4.  The ground state $R_{10}=2e^{-r}$  *(Griffiths 3e Eq. 4.80–4.82, p.190–191)*
Construct the normalized ground-state radial function and verify
$\int_0^\infty|R_{10}|^2r^2\,dr=1$.
*Answer:* with $n=1,l=0$ the Laguerre is $L_0^1=1$, so $R_{10}=2e^{-r}$;
$\int_0^\infty 4e^{-2r}r^2dr=4\cdot 2!/2^3=1$.
*Check:* `radial_wavefunction(1,0,0.0)` $=2.0$; `radial_norm(1,0)` $\approx1$.
(`test_ground_state_is_two_exp`, `test_radial_normalization`.)

**Solution.** For $n=1,l=0$ the Laguerre degree is $n-l-1=0$ and $L_0^{(\alpha)}=1$, so Eq. 4.89
collapses to $R_{10}(r)=\sqrt{(2/1)^3\,\frac{0!}{2\cdot1!}}\;e^{-r}=\sqrt{4}\,e^{-r}=2e^{-r}$,
giving $R_{10}(0)=2$. Normalize with $\int_0^\infty r^k e^{-ar}\,dr=k!/a^{k+1}$:
$$\int_0^\infty |R_{10}|^2 r^2\,dr=\int_0^\infty 4e^{-2r}r^2\,dr=4\cdot\frac{2!}{2^3}=4\cdot\frac28=1.$$
So $R_{10}=2e^{-r}$ is correctly normalized — `radial_wavefunction(1,0,0.0)`$=2.0$ and
`radial_norm(1,0)`$\approx1$.

### P5.  Count the radial nodes  *(Griffiths 3e p.195)*
How many radial nodes does each of $3s$ ($n{=}3,l{=}0$), $3p$ ($l{=}1$), $3d$
($l{=}2$) have? What distinguishes orbitals of the *same* energy?
*Answer:* $n-l-1$ nodes: $3s\!\to\!2$, $3p\!\to\!1$, $3d\!\to\!0$. Same energy
$E_3$, different node structure — that is how the degenerate states differ
spatially (the $l>0$ zero at $r=0$ is a boundary, not a node).
*Check:* `count_radial_nodes(3,0)`=2, `(3,1)`=1, `(3,2)`=0.
(`test_radial_node_count`.)

**Solution.** The radial function is $R_{nl}\propto (2r/n)^l e^{-r/n}\,L_{n-l-1}^{2l+1}(2r/n)$;
the prefactor $(2r/n)^l e^{-r/n}$ never changes sign, so every interior zero comes from the
Laguerre polynomial, which has degree $n-l-1$ and exactly that many positive real roots. Hence
the radial node count is $n-l-1$: for $n=3$, $3s\to3{-}0{-}1=2$, $3p\to1$, $3d\to0$. All three
share the energy $E_3=-1/18$ Ha but differ in node structure — the visible fingerprint that
distinguishes the degenerate orbitals (the $l>0$ vanishing at $r=0$ is a boundary, not a node).
Matches `count_radial_nodes(3,0)`=2, `(3,1)`=1, `(3,2)`=0.

### P6.  $\langle r\rangle$ vs the most probable radius  *(Griffiths 3e Problem 4.15a & 4.16, p.197)*
For the hydrogen ground state, find (a) the *most probable* radius and (b) the
*mean* radius $\langle r\rangle$. Why aren't they equal?
*Answer:* (a) $P(r)=r^2|R_{10}|^2=4r^2e^{-2r}$ peaks at $r=a_0=1$. (b)
$\langle r\rangle=\int r\,P\,dr=\tfrac32 a_0$. They differ because $P(r)$ is
skewed with a long large-$r$ tail, so the mean exceeds the mode. General:
$\langle r\rangle_{nl}=\tfrac12[3n^2-l(l+1)]$.
*Check:* `expectation_r(1,0)` $\approx1.5$; the peak of `radial_probability(1,0,r)`
is at $r\approx1$; `expectation_r_closed(2,1)` $=5$.
(`test_expectation_r_ground_state`, `test_radial_probability_peaks_at_bohr_radius`,
`test_expectation_r_matches_closed_form`.)

**Solution.** The ground-state radial density is $P(r)=r^2|R_{10}|^2=4r^2e^{-2r}$. Its mode
solves $P'(r)=0$: $\frac{d}{dr}(r^2e^{-2r})=2r\,e^{-2r}(1-r)=0\Rightarrow r=1=a_0$, the *most
probable* radius. The mean weights by $r$:
$$\langle r\rangle=\int_0^\infty r\,P(r)\,dr=4\int_0^\infty r^3 e^{-2r}\,dr=4\cdot\frac{3!}{2^4}=\frac{24}{16}=\frac32\,a_0.$$
The mean exceeds the mode because $P$ is right-skewed with a long large-$r$ tail. In general
$\langle r\rangle_{nl}=\tfrac12[3n^2-l(l+1)]$, e.g. $(2,1)\to\tfrac12[12-2]=5$. Confirmed:
`expectation_r(1,0)`$\approx1.5$, the peak of `radial_probability(1,0,r)` at $r\approx1.0$, and
`expectation_r_closed(2,1)`$=5$.

### P7.  The associated Laguerre polynomial  *(Griffiths 3e Eq. 4.87–4.88, p.192)*
The radial polynomial is $L_{n-l-1}^{2l+1}(2r/n)$. Show it reduces, at the lowest
order, to a constant, and that the $\alpha=0$ family is exactly the Laguerre
polynomial of `~MA-12`.
*Answer:* $L_0^{(\alpha)}(x)=1$ for any $\alpha$ — so every $n=l+1$ state ($1s$,
$2p$, $3d$, …) has the nodeless form $R\propto r^l e^{-r/n}$. And
$L_k^{(0)}=L_k$, the ordinary Laguerre `~MA-12` builds from its recurrence.
*Check:* `generalized_laguerre(0,3,2.34)` $=1$;
`generalized_laguerre(k,0,x)` $=$ MA-12 `laguerre(k,x)`.
(`test_generalized_laguerre_reduces_to_MA12`.)

**Solution.** The generalized Laguerre polynomial is
$L_k^{(\alpha)}(x)=\sum_{j=0}^{k}(-1)^j\binom{k+\alpha}{k-j}\frac{x^j}{j!}$. At $k=0$ only the
$j=0$ term survives, $\binom{\alpha}{0}=1$, so $L_0^{(\alpha)}(x)=1$ for *every* $\alpha$ —
therefore each $n=l+1$ state ($1s,2p,3d,\dots$) has the nodeless form $R\propto r^l e^{-r/n}$.
Setting $\alpha=0$ reproduces the ordinary Laguerre $L_k=L_k^{(0)}$ that `~MA-12` builds from its
recurrence. Hence `generalized_laguerre(0,3,2.34)`$=1$, and `generalized_laguerre(k,0,x)` equals
MA-12's `laguerre(k,x)`.

### P8.  The radial functions are orthogonal  *(Griffiths 3e Eq. 4.90, p.193)*
For fixed $l$, show $\int_0^\infty R_{nl}R_{n'l}\,r^2dr=\delta_{nn'}$, and explain
*why* without doing the integral.
*Answer:* the integral is $1$ on the diagonal, $0$ off it; orthogonality follows
because the $R_{nl}$ (for fixed $l$) are eigenfunctions of the Hermitian radial
operator with distinct eigenvalues $E_n$ — the same argument that makes `~QM-10`'s
$Y_l^m$ orthogonal.
*Check:* `_trapz(radial_wavefunction(2,0,r)*radial_wavefunction(3,0,r)*r*r, r)`
$\approx0$, while $n=n'$ gives $\approx1$. (`test_radial_functions_orthogonal`.)

**Solution.** The radial operator $H_l=-\tfrac12\frac{d^2}{dr^2}+V_{\text{eff}}(r)$ (acting on
$u=rR$ on $L^2(0,\infty)$, equivalently $H$ acting on $R$ under the weight $r^2\,dr$) is
Hermitian. For fixed $l$ the $R_{nl}$ are its eigenfunctions with *distinct* eigenvalues
$E_n=-1/2n^2$, and eigenfunctions of a Hermitian operator belonging to different eigenvalues are
automatically orthogonal — no integral required, the same argument that orthogonalizes `~QM-10`'s
$Y_l^m$. With the P4 normalization this gives $\int_0^\infty R_{nl}R_{n'l}\,r^2dr=\delta_{nn'}$.
Numerically the $(2,0)$–$(3,0)$ overlap is $\approx-2\times10^{-11}\approx0$ while $n=n'$ returns
$\approx1$, matching the `_trapz(...)` check.
