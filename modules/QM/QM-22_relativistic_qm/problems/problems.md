# QM-22 — Problems

Work each by hand, then check with `code/relativistic.py` (natural units
$\hbar=c=1$, metric $\mathrm{diag}(+,-,-,-)$). Sources in `../refs.md`. Griffiths
is non-relativistic, so most checks are against the **code** (the verification),
as flagged per problem.

### P1.  Klein–Gordon dispersion and the negative-energy disease  *(code-verified; Sakurai Ch. 8, unpinned)*
Show that the plane wave $\phi=e^{-ip\cdot x}$ satisfies $(\Box+m^2)\phi=0$ iff
$E^2=\vec p^{\,2}+m^2$, and that therefore $E=-\sqrt{\vec p^{\,2}+m^2}$ is *also* a
solution. Why is this fatal for a single-particle probability interpretation?
*(Each $\partial_\mu$ pulls down $-ip_\mu$, so $\Box\phi=-(p\cdot p)\phi$ and
$(\Box+m^2)\phi=-(p\cdot p-m^2)\phi$, which vanishes for **both** roots of
$E^2=\vec p^{\,2}+m^2$. The conserved density $\rho\propto\mathrm{Im}(\phi^*\partial_t\phi)$
goes negative for the negative-energy root — not a probability.)*
*Answer:* both $\pm\sqrt{\vec p^{\,2}+m^2}$ solve KG; no ground state; indefinite $\rho$.
*Check:* `kg_operator_fd(four_momentum([.6,0,.8],1.0,+1),1.0,[.3,.2,.1,.4])` ≈ 0 **and**
`...,-1),...` ≈ 0. (`test_kg_planewave_on_shell`, `test_kg_negative_energy_exists`.)

**Solution.** Acting on $\phi=e^{-ip\cdot x}$, each $\partial_\mu$ pulls down $-ip_\mu$, so
$\Box\phi=\partial_\mu\partial^\mu\phi=(-ip_\mu)(-ip^\mu)\phi=-(p\cdot p)\,\phi$ and
$$(\Box+m^2)\phi=-(p\cdot p-m^2)\,\phi=-(E^2-\vec p^{\,2}-m^2)\,\phi,$$
which vanishes iff $E^2=\vec p^{\,2}+m^2$. This is **quadratic** in $E$, so
$E=\pm\sqrt{\vec p^{\,2}+m^2}$ — both roots solve KG and the spectrum is unbounded
below. The conserved density $\rho=\frac{i}{2m}(\phi^*\partial_t\phi-\phi\,\partial_t\phi^*)=\frac{E}{m}|\phi|^2$
flips sign with $E$, so the negative-energy root gives $\rho<0$ — not a probability.
With $\vec p=(0.6,0,0.8)$, $m=1$, $E=\sqrt2$; `kg_operator_fd` returns $\approx2.9\times10^{-7}$
(the finite-difference floor) for **both** the $+1$ and $-1$ signs — i.e. $\approx0$,
confirming each root sits on shell.

### P2.  The Clifford algebra forces matrices  *(code-verified; MA-18; Bjorken–Drell Ch. 1, unpinned)*
From $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}\mathbb1$ deduce $(\gamma^0)^2=+\mathbb1$,
$(\gamma^i)^2=-\mathbb1$, and that distinct gammas anticommute. Argue these cannot
be satisfied by numbers, so the $\gamma^\mu$ must be (at least $4\times4$) matrices.
Then verify the relation holds for **all 16** pairs in the Dirac representation.
*Answer:* $\mu=\nu=0\Rightarrow2(\gamma^0)^2=2\Rightarrow(\gamma^0)^2=\mathbb1$;
$\mu=\nu=i\Rightarrow(\gamma^i)^2=-\mathbb1$; $\mu\ne\nu\Rightarrow\gamma^\mu\gamma^\nu=-\gamma^\nu\gamma^\mu$.
Anticommuting square-roots of $\pm1$ need a non-abelian (matrix) realization.
*Check:* `clifford(mu,nu)` $=2\,$`metric()[mu,nu]`$\,I_4$ for every $\mu,\nu$.
(`test_clifford_algebra_all_pairs`; Pauli blocks cross-checked in `test_pauli_cross_check_MA18`.)

**Solution.** Set $\mu=\nu=0$: $\{\gamma^0,\gamma^0\}=2(\gamma^0)^2=2g^{00}\mathbb1=+2\mathbb1\Rightarrow(\gamma^0)^2=+\mathbb1$.
Set $\mu=\nu=i$: $2(\gamma^i)^2=2g^{ii}\mathbb1=-2\mathbb1\Rightarrow(\gamma^i)^2=-\mathbb1$. For $\mu\ne\nu$, $g^{\mu\nu}=0$ forces
$$\gamma^\mu\gamma^\nu=-\gamma^\nu\gamma^\mu\qquad(\mu\ne\nu).$$
Ordinary numbers always commute ($ab=ba$), so objects that anticommute yet square to the **nonzero** values $\pm\mathbb1$
cannot be scalars — they must be matrices, and the smallest faithful realization of this Clifford algebra is $4\times4$. The
Dirac representation satisfies it for every pair: `clifford(0,0)`$=+2\mathbb1_4$ (entry $2.0$), `clifford(1,1)`$=-2\mathbb1_4$
(entry $-2.0$), `clifford(0,1)`$=0$ — all 16 pairs equal $2g^{\mu\nu}\mathbb1_4$.

### P3.  $\det(\not{\!p}-m)$ and "Dirac² = Klein–Gordon"  *(code-verified; Sakurai Ch. 8, unpinned)*
Using only $\not{\!p}^{\,2}=(p\cdot p)\mathbb1$ (itself a one-line consequence of
the Clifford algebra), show $(\not{\!p}-m)(\not{\!p}+m)=(p\cdot p-m^2)\mathbb1_4$,
hence $\det(\not{\!p}-m)=(p\cdot p-m^2)^2$. Conclude that nontrivial spinor
solutions exist **iff** $E^2=\vec p^{\,2}+m^2$ — the Dirac equation still enforces
the relativistic relation, and every Dirac solution solves Klein–Gordon.
*Answer:* $\not{\!p}^2-m^2=(p\cdot p-m^2)\mathbb1$; det of a multiple of $\mathbb1_4$
gives the 4th power, but the operator factorizes as a perfect square → $(p\cdot p-m^2)^2$.
*Check:* `dirac_squared(four_momentum([.3,.4,0],1.0),1.0)` ≈ 0;
`dirac_determinant(p4,m)` $=(p\cdot p-m^2)^2$. (`test_dirac_squares_to_klein_gordon`,
`test_dirac_determinant_closed_form`.)

**Solution.** Because $p_\mu p_\nu$ is symmetric, only the symmetric (anticommutator) part of $\gamma^\mu\gamma^\nu$ survives:
$$\not{\!p}^{\,2}=p_\mu p_\nu\gamma^\mu\gamma^\nu=\tfrac12 p_\mu p_\nu\{\gamma^\mu,\gamma^\nu\}=p_\mu p_\nu\,g^{\mu\nu}\mathbb1=(p\cdot p)\,\mathbb1.$$
Hence $(\not{\!p}-m)(\not{\!p}+m)=\not{\!p}^{\,2}-m^2\mathbb1=(p\cdot p-m^2)\mathbb1_4$ — the Klein–Gordon operator. The eigenvalues
of $\not{\!p}$ are $\pm\sqrt{p\cdot p}$ (each doubly degenerate), so $\det(\not{\!p}-m)=(\sqrt{p\cdot p}-m)^2(\sqrt{p\cdot p}+m)^2=(p\cdot p-m^2)^2$,
vanishing **iff** $p\cdot p=m^2$, i.e. $E^2=\vec p^{\,2}+m^2$. For $\vec p=(0.3,0.4,0)$, $m=1$, on shell $p\cdot p=1.0=m^2$, so
`dirac_squared`$\approx8\times10^{-17}$ and `dirac_determinant`$\approx1\times10^{-32}$ (both $\approx0$); off shell the determinant
reproduces $(p\cdot p-m^2)^2$ exactly (e.g. $1.1881$).

### P4.  The four plane-wave spinors  *(code-verified; Bjorken–Drell Ch. 3, unpinned)*
For $\vec p=(0.3,0.4,0)$, $m=1$, build the two positive-energy spinors $u^{s}$ and
two negative-energy spinors $v^{s}$ ($N=\sqrt{E+m}$), and verify
$(\not{\!p}-m)u=0$, $(\not{\!p}+m)v=0$. Check the normalizations $\bar u u=+2m$,
$\bar v v=-2m$ ($\bar w=w^\dagger\gamma^0$). What does the **minus sign** signal?
*Answer:* all four solve their equation; $\bar u u=2m=2.0$, $\bar v v=-2m=-2.0$.
The negative norm marks the antiparticle (positron) sector — the Dirac echo of
KG's indefinite density, resolved by `~QF-01`.
*Check:* `dirac_solutions([.3,.4,0],1.0)`; `dirac_matrix(p4,1.0)@u0` ≈ 0.
(`test_dirac_spinors_solve_equation`, `test_dirac_spinor_normalization`.)

**Solution.** In the Dirac rep $\not{\!p}=\begin{pmatrix}E\,\mathbb1&-\vec\sigma\cdot\vec p\\\vec\sigma\cdot\vec p&-E\,\mathbb1\end{pmatrix}$.
The lower block of $(\not{\!p}-m)u=0$ gives $\chi=\frac{\vec\sigma\cdot\vec p}{E+m}\varphi$, so with $\varphi=\xi^s$ and $N=\sqrt{E+m}$,
$$u^s=N\begin{pmatrix}\xi^s\\\frac{\vec\sigma\cdot\vec p}{E+m}\xi^s\end{pmatrix},\qquad
v^s=N\begin{pmatrix}\frac{\vec\sigma\cdot\vec p}{E+m}\xi^s\\\xi^s\end{pmatrix}\ \ [(\not{\!p}+m)v=0].$$
With $\bar w=w^\dagger\gamma^0$ and $(\vec\sigma\cdot\vec p)^2=\vec p^{\,2}$, $\bar uu=N^2\big[1-\frac{p^2}{(E+m)^2}\big]=\frac{(E+m)^2-p^2}{E+m}=2m$
(using $(E+m)^2-p^2=2m(E+m)$); swapping upper/lower blocks flips the bracket, so $\bar vv=-2m$. The minus sign marks the
negative-energy/antiparticle (positron) sector. Numerically `dirac_solutions([.3,.4,0],1.0)` gives $\bar uu_0=2.0$, $\bar vv_0=-2.0$,
$u_0^\dagger u_0=2.236=2E$, $\bar u_0v_0=0$, and `dirac_matrix(p4,1.0)@u0`$\approx0$.

### P5.  The magnetic moment $g=2$, for free  *(code-verified; Sakurai Ch. 8, unpinned)*
In the non-relativistic limit the upper 2-spinor obeys the Pauli equation with
kinetic operator $(\vec\sigma\cdot\vec\pi)^2/2m$. Using
$(\vec\sigma\cdot\vec\pi)^2=\vec\pi^{\,2}-q\,\vec\sigma\cdot\vec B$ (from the
identity $(\vec\sigma\cdot\vec a)(\vec\sigma\cdot\vec b)=\vec a\cdot\vec b+i\vec\sigma\cdot(\vec a\times\vec b)$
with $[\pi_x,\pi_y]=iqB$), read off the spin Zeeman term and show the gyromagnetic
ratio is $g=2$ — i.e. spin couples to $\vec B$ **twice** as strongly as orbital motion.
*Answer:* $H_{\text{spin}}=-\frac{q}{2m}\vec\sigma\cdot\vec B=-\frac{q}{2m}g\,\vec S\cdot\vec B$
with $\vec S=\tfrac12\vec\sigma\Rightarrow g=2$.
*Check:* `dirac_g_factor()` → `(2.0, ~1e-15)`. Also verify the underlying identity:
`test_pauli_vector_identity`, `test_magnetic_commutator`, `test_dirac_g_factor_is_two`.

**Solution.** Apply $(\vec\sigma\cdot\vec a)(\vec\sigma\cdot\vec b)=\vec a\cdot\vec b+i\vec\sigma\cdot(\vec a\times\vec b)$ with $\vec a=\vec b=\vec\pi$.
The kinetic momenta no longer commute: $(\vec\pi\times\vec\pi)_z=[\pi_x,\pi_y]=iqB$ (and cyclic), so
$$(\vec\sigma\cdot\vec\pi)^2=\vec\pi^{\,2}+i\,\vec\sigma\cdot(\vec\pi\times\vec\pi)=\vec\pi^{\,2}-q\,\vec\sigma\cdot\vec B.$$
Dividing by $2m$, the Pauli Hamiltonian splits into an orbital piece $\vec\pi^{\,2}/2m$ and a spin piece
$H_{\text{spin}}=-\frac{q}{2m}\vec\sigma\cdot\vec B$. Writing $\vec\sigma=2\vec S$ recasts this as $-\frac{q}{2m}g\,\vec S\cdot\vec B$ with
$\boxed{g=2}$ — twice the orbital $g=1$, and spin was never inserted by hand. `dirac_g_factor()` returns $(2.0,\,1.55\times10^{-15})$,
the tiny residual confirming the operator identity $(\vec\sigma\cdot\vec\pi)^2-\vec\pi^{\,2}=-q\,\vec\sigma\cdot\vec B$ holds exactly.

### P6.  Leading relativistic energy correction → fine structure  *(Griffiths §7.3, p.378; "exact" via Dirac, Prob. 7.22, p.388)*
Expand $E=\sqrt{\vec p^{\,2}+m^2}$ to two terms past the rest mass and identify each
piece physically. Which term, treated as a perturbation, is one of the two
contributions to hydrogen's **fine structure** (`~QM-17`)?
*Answer:* $E=m+\dfrac{p^2}{2m}-\dfrac{p^4}{8m^3}+\cdots$ — the rest energy, the
Schrödinger kinetic energy, and the **relativistic correction** $-p^4/8m^3$ (the
other fine-structure piece is spin–orbit, also from the Dirac reduction).
Griffiths derives this perturbatively (§7.3) and notes the *exact* result follows
"from the (relativistic) Dirac equation" (Prob. 7.22, p.388; footnote p.415).
*Check:* `energy_expansion([.2,.1,0],1.0,order=2)` is closer to `nonrel_energy([.2,.1,0],1.0)`
than the `order=1` (Schrödinger) value. (`test_nonrelativistic_energy_limit`.)

**Solution.** Factor out the rest mass and expand the square root for $|\vec p|\ll m$:
$$E=\sqrt{\vec p^{\,2}+m^2}=m\sqrt{1+\tfrac{p^2}{m^2}}=m+\frac{p^2}{2m}-\frac{p^4}{8m^3}+\cdots.$$
The three terms are the rest energy $m$, the Schrödinger kinetic energy $p^2/2m$, and the **leading relativistic correction**
$-p^4/8m^3$. Treated as a perturbation in hydrogen, this last term is one of the two contributions to the fine structure
(`~QM-17`); the other, spin–orbit coupling, likewise drops out of the Dirac reduction. For $\vec p=(0.2,0.1,0)$, $m=1$,
`energy_expansion(...,order=2)`$=1.0246875$ lies within $7.6\times10^{-6}$ of the exact $m+$`nonrel_energy`$=1.0246951$ — far
closer than the `order=1` (Schrödinger) value $1.025$, whose error is $3.0\times10^{-4}$.
