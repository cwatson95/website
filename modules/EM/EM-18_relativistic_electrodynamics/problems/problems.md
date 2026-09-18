# EM-18 — Problems

Work by hand, then check with `code/relativistic_electrodynamics.py`. Citations in
`../refs.md`; **Gr** = Griffiths 4e (printed pages). The boost is always along
+**x̂** at v = βc, with γ = 1/√(1−β²).

### P1.  The field tensor and what is inside it  *(Gr §12.3.3, Eq. 12.118, p.562)*
For fields **E** = (E_x, E_y, E_z) and **B** = (B_x, B_y, B_z), write out F^{μν} in
the (ct, x, y, z) ordering, with $F^{0i}=E_i/c$ and $F^{ij}=-\varepsilon_{ijk}B_k$.
Show it is antisymmetric, so the diagonal vanishes and only **six** of the sixteen
entries are independent — exactly **E** and **B** — and identify which entry holds
$B_x$. *Check:* `field_tensor(E, B)` then `is_antisymmetric` returns `True`;
`fields_from_tensor` returns the original `(E, B)`; confirm $B_x$ sits at
$F^{yz}=$ `F[2][3]`.

**Solution.** Filling in $F^{0i}=E_i/c$ for the top row/column and $F^{ij}=-\varepsilon_{ijk}B_k$ for the spatial block,
$$F^{\mu\nu}=\begin{pmatrix}
0 & E_x/c & E_y/c & E_z/c\\
-E_x/c & 0 & B_z & -B_y\\
-E_y/c & -B_z & 0 & B_x\\
-E_z/c & B_y & -B_x & 0\end{pmatrix}.$$
Antisymmetry $F^{\mu\nu}=-F^{\nu\mu}$ forces each diagonal entry to satisfy $F^{\mu\mu}=-F^{\mu\mu}=0$, so the four diagonal slots vanish; the remaining $16-4=12$ entries are locked in $\pm$ pairs, leaving $6$ independent numbers — the three $E_i/c$ (top row) and the three $B_k$ (spatial block). The spatial $3\times3$ block holds $F^{xy}=B_z$, $F^{xz}=-B_y$, $F^{yz}=B_x$, so $B_x$ lives in the $(y,z)$ slot — row 2, col 3 in the $(ct,x,y,z)$ ordering, i.e. `F[2][3]`. The code confirms `is_antisymmetric` $=$ `True`, `fields_from_tensor` round-trips `(E, B)`, and `F[2][3]` $=B_x$.

### P2.  Pulling a magnetic field out of a pure electric one  *(Gr §12.3.2, Eq. 12.109, p.553)*
Take **E** = $E_0\,\hat{\mathbf y}$ and **B** = 0 in S. Boost to S′ at v = βc. Show
$$\mathbf E'=(0,\;\gamma E_0,\;0),\qquad
  \mathbf B'=\Big(0,\;0,\;-\gamma\tfrac{v}{c^2}E_0\Big)=-\tfrac{1}{c^2}\,\mathbf v\times\mathbf E',$$
so a transverse electric field acquires a magnetic field that switches off as
v → 0 (no magnetism without motion) while the field strengthens by γ. *Check:*
`boost_fields((0, E0, 0), (0, 0, 0), beta)`; compare $B'_z$ to
−`gamma(beta)`·(βc/c²)·E0 and $E'_y$ to `gamma(beta)`·E0.

**Solution.** Insert $E_x=E_z=0$, $E_y=E_0$, $\mathbf B=0$ into the boost map (Eq. 12.109). The electric components give $E'_x=E_x=0$, $E'_y=\gamma(E_y-vB_z)=\gamma E_0$, $E'_z=\gamma(E_z+vB_y)=0$, so $\mathbf E'=(0,\gamma E_0,0)$. The magnetic components give $B'_x=B_x=0$, $B'_y=\gamma(B_y+\tfrac{v}{c^2}E_z)=0$, and
$$B'_z=\gamma\Big(B_z-\tfrac{v}{c^2}E_y\Big)=-\gamma\tfrac{v}{c^2}E_0 .$$
With $\mathbf v=v\hat{\mathbf x}$ and $\mathbf E'=\gamma E_0\hat{\mathbf y}$, $\;-\tfrac1{c^2}\mathbf v\times\mathbf E'=-\tfrac{v\gamma E_0}{c^2}(\hat{\mathbf x}\times\hat{\mathbf y})=-\gamma\tfrac v{c^2}E_0\,\hat{\mathbf z}$, matching $\mathbf B'$. As $v\to0$ the magnetic field vanishes while $E'_y\to E_0$. For $E_0=1000$ V/m, $\beta=0.6$ ($\gamma=1.25$): $E'_y=1250$ V/m and $B'_z=-2.502\times10^{-6}$ T, exactly what `boost_fields((0, E0, 0), (0,0,0), beta)` returns.

### P3.  The two quantities no boost can change  *(Gr §12.3.3, Prob. 12.47, p.562)*
For arbitrary **E**, **B**, show the scalars
$$\mathbf E\cdot\mathbf B \qquad\text{and}\qquad B^2-\frac{E^2}{c^2}$$
take the same value in S and S′. (Substitute the §12.3.2 transformation and watch
the γ-dependent cross-terms cancel via $\gamma^2(1-v^2/c^2)=1$.) *Check:*
`field_invariants(E, B)` versus `field_invariants(*boost_fields(E, B, beta))` for
β = 0.2, 0.5, 0.9, 0.99 — agree to rounding.

**Solution.** Take $\mathbf E'\cdot\mathbf B'=E'_xB'_x+E'_yB'_y+E'_zB'_z$. The $x$-terms are untouched ($E'_xB'_x=E_xB_x$); the transverse pieces are
$$\gamma^2(E_y-vB_z)(B_y+\tfrac v{c^2}E_z)+\gamma^2(E_z+vB_y)(B_z-\tfrac v{c^2}E_y).$$
Expanding, the genuinely mixed terms $\tfrac v{c^2}E_yE_z$ and $-\tfrac v{c^2}E_zE_y$ cancel, as do $-vB_zB_y$ and $+vB_yB_z$, leaving $\gamma^2\big(1-\tfrac{v^2}{c^2}\big)(E_yB_y+E_zB_z)=E_yB_y+E_zB_z$ since $\gamma^2(1-v^2/c^2)=1$. Adding back $E_xB_x$ recovers $\mathbf E\cdot\mathbf B$. The identical cancellation in $B'^2-E'^2/c^2$ leaves it invariant. Numerically `field_invariants` returns $\mathbf E\cdot\mathbf B=-2.9\times10^{-3}$ and $B^2-E^2/c^2=9.19\times10^{-14}$, unchanged through $\beta=0.2,0.5,0.9,0.99$ — matching `field_invariants(*boost_fields(E, B, beta))`.

### P4.  A light wave looks like a light wave to everyone  *(Gr §12.3.3, Prob. 12.47, p.562)*
A plane electromagnetic wave has **E** ⊥ **B** with $E=cB$, so *both* invariants
vanish: E·B = 0 and B²−E²/c² = 0. Argue that, because the invariants are fixed, no
observer can boost into a frame where the wave is purely electric or purely
magnetic, and **E** ⊥ **B**, |**E**| = c|**B**| in *every* frame. *Check:* take
**E** = (0, E0, 0), **B** = (0, 0, E0/`C`); `field_invariants` returns ≈ (0, 0);
boost with `boost_fields` and confirm both invariants stay ≈ 0.

**Solution.** For the wave, $\mathbf E\perp\mathbf B$ gives $\mathbf E\cdot\mathbf B=0$, and $E=cB$ gives
$$B^2-\frac{E^2}{c^2}=B^2-\frac{(cB)^2}{c^2}=B^2-B^2=0,$$
so both invariants are zero. By P3 they are zero in *every* frame: $\mathbf E'\cdot\mathbf B'=0$ keeps $\mathbf E'\perp\mathbf B'$, and $B'^2-E'^2/c^2=0$ keeps $|\mathbf E'|=c|\mathbf B'|$. A "purely electric" frame ($\mathbf B'=0$) would force $B'^2-E'^2/c^2=-E'^2/c^2<0$, and a "purely magnetic" frame ($\mathbf E'=0$) would force $+B'^2>0$ — both contradict the vanishing invariant. So no boost can strip a light wave to one field. With $\mathbf E=(0,E_0,0)$, $\mathbf B=(0,0,E_0/c)$, `field_invariants` returns $\approx(0,0)$ and stays $\approx(0,0)$ after `boost_fields`.

### P5.  You cannot switch off a field with E·B ≠ 0  *(Gr §12.3.2–12.3.3, p.553, 562)*
Let **E** = $E_0\,\hat{\mathbf y}$ and **B** = $B_0\,\hat{\mathbf y}$ be parallel
(so E·B = $E_0B_0\neq0$). Show that no boost can make either field vanish: since
E·B is invariant and nonzero, neither **E**′ nor **B**′ can be zero in any frame.
Verify explicitly that the boosted fields **E**′ = (0, γE_0, γvB_0) and
**B**′ = (0, γB_0, −γ(v/c²)E_0) still satisfy **E**′·**B**′ = $E_0B_0$. *Check:*
`field_invariants((0, E0, 0), (0, B0, 0))` gives `(E0*B0, ...)`; scan β with
`boost_fields` and confirm E·B stays $E_0B_0$ while neither field ever drops to
zero — the reason `~RE-08` calls E·B and B²−E²/c² the *intrinsic* content of the field.

**Solution.** With $E_x=E_z=0,\ E_y=E_0$ and $B_x=B_z=0,\ B_y=B_0$, the boost map gives
$$\mathbf E'=(0,\;\gamma E_0,\;\gamma vB_0),\qquad \mathbf B'=\big(0,\;\gamma B_0,\;-\gamma\tfrac v{c^2}E_0\big),$$
since $E'_z=\gamma(E_z+vB_y)=\gamma vB_0$ and $B'_z=\gamma(B_z-\tfrac v{c^2}E_y)=-\gamma\tfrac v{c^2}E_0$. Their dot product is
$$\mathbf E'\cdot\mathbf B'=\gamma^2E_0B_0-\gamma^2\tfrac{v^2}{c^2}E_0B_0=\gamma^2\Big(1-\tfrac{v^2}{c^2}\Big)E_0B_0=E_0B_0 .$$
Because $\mathbf E'\cdot\mathbf B'=E_0B_0\neq0$ in every frame, neither field can vanish (a zero field would make the product zero). For $E_0=1000$ V/m, $B_0=2\times10^{-6}$ T, `field_invariants` gives $\mathbf E\cdot\mathbf B=2.0\times10^{-3}=E_0B_0$, and scanning $\beta=0.3,0.6,0.9$ with `boost_fields` holds $\mathbf E'\cdot\mathbf B'=E_0B_0$ while $|\mathbf E'|,|\mathbf B'|$ stay strictly positive.
