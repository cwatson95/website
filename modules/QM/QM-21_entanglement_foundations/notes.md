# QM-21 — Entanglement & foundations (notes)

By `~QM-11` we have two spin-½ qubits and the Pauli algebra; by `~QM-20` the
density matrix and the reduced state $\rho_A=\mathrm{Tr}_B\rho$. This module asks
the question Einstein refused to let go of: when two particles are *entangled*,
does measuring one **really** affect the other, or did the outcomes exist all
along? Bell turned that philosophical dispute into an **inequality you can test**,
and quantum mechanics violates it. The whole story is Griffiths 3e Ch. 12, the
"Afterword" (Griffiths 3e §12, p.566).

The thread: **entangled state** → it cannot be factored (the reduced state goes
mixed) → a **local hidden variable** theory must obey a **Bell/CHSH inequality**
→ the singlet **violates** it, up to the **Tsirelson bound $2\sqrt2$** → therefore
**no local hidden variables**, but also **no faster-than-light signaling**.

## 1. The EPR paradox and the singlet

A neutral pion at rest decays, $\pi^0\to e^-+e^+$; since the pion has spin 0,
conservation of angular momentum forces the pair into the **singlet** spin state
(Griffiths 3e §12.1, p.567, Eq. 12.1):
$$|\Psi^-\rangle=\frac{1}{\sqrt2}\big(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle\big)
=\frac{1}{\sqrt2}\big(|01\rangle-|10\rangle\big).$$
If you measure the electron and get spin up, the positron is *instantly* spin
down, "10 light-years away." To the **realist** (EPR) the spins were fixed at
creation and QM merely doesn't know them; to the **orthodox** view neither spin
existed until measurement collapsed the pair. EPR's one assumption is the
**principle of locality** — no influence travels faster than light (Griffiths 3e
§12.1, p.567) — and from it they argued QM is *incomplete*: a hidden variable
$\lambda$ is missing. (`singlet()`; the anti-correlation $E(\hat z,\hat z)=-1$ is
`test_singlet_correlation_is_minus_a_dot_b`.)

The singlet is also the total-spin **$J=0$** state of `~QM-13`: it is the unique
two-qubit state invariant under a *simultaneous* rotation of both spins,
$$(U\otimes U)\,|\Psi^-\rangle=|\Psi^-\rangle\qquad\forall\,U\in SU(2),$$
the rotational scalar. The code builds $U=\cos\tfrac\theta2\,\mathbb
I-i\sin\tfrac\theta2\,(\hat{\mathbf n}\!\cdot\!\boldsymbol\sigma)$ (`su2`) and
checks this for random rotations, contrasting with the triplet/$|\Phi^+\rangle$
which is *not* invariant (`test_singlet_rotational_invariance_J0`).

## 2. Entangled = non-separable: the reduced state goes mixed

A two-qubit pure state is **separable** (a *product*) if it factors,
$|\psi\rangle=|a\rangle\otimes|b\rangle$; otherwise it is **entangled**. Griffiths
makes this precise (Griffiths 3e §12.1, Problem 12.1, p.568): the state
$\alpha|01\rangle+\beta|10\rangle$ **cannot** be written as a product for any
one-particle states unless $\alpha=0$ or $\beta=0$ — "one cannot really speak of
the state of either particle separately."

The operational diagnostic comes from `~QM-20`. Take $\rho=|\psi\rangle\langle\psi|$
and trace out qubit B:
$$\rho_A=\mathrm{Tr}_B|\psi\rangle\langle\psi|.$$
- **Product state** $|a\rangle\otimes|b\rangle$: $\rho_A=|a\rangle\langle a|$ is
  **pure**, $\mathrm{Tr}(\rho_A^2)=1$.
- **Entangled state**: $\rho_A$ is **mixed**, $\mathrm{Tr}(\rho_A^2)<1$. For any
  Bell state it is *maximally* mixed:
  $$\rho_A=\tfrac12\,\mathbb I,\qquad \mathrm{Tr}(\rho_A^2)=\tfrac12.$$
  Knowing the global pure state, you know *nothing* about the local one — that is
  entanglement. (`partial_trace`, `purity`; `test_product_state_reduced_is_pure`,
  `test_bell_state_reduced_is_maximally_mixed`.)

Three equivalent measures, all checked:

**Schmidt rank.** Reshape $|\psi\rangle$ into a $2\times2$ matrix and take its
singular values $\lambda_i\ge0$ (the **Schmidt coefficients**, $\sum\lambda_i^2=1$):
$$|\psi\rangle=\sum_i\lambda_i\,|u_i\rangle_A\otimes|v_i\rangle_B.$$
The number of nonzero $\lambda_i$ is the **Schmidt rank**: rank $1$ ⇔ product,
rank $2$ ⇔ entangled. The reduced purity is $\mathrm{Tr}(\rho_A^2)=\sum_i\lambda_i^4$
(`schmidt_coeffs`, `schmidt_rank`; `test_schmidt_coefficients`).

**Concurrence.** For a two-qubit pure state
$|\psi\rangle=a|00\rangle+b|01\rangle+c|10\rangle+d|11\rangle$,
$$\boxed{\,C=2\,|ad-bc|\in[0,1]\,},$$
$C=0$ for a product state, $C=1$ for any maximally entangled (Bell) state, and
$C=2\lambda_1\lambda_2$ in terms of the Schmidt coefficients. The equivalent
Wootters spin-flip form $C=|\langle\psi|\sigma_y\otimes\sigma_y|\psi^*\rangle|$ is
checked to agree (`concurrence`, `concurrence_spinflip`;
`test_concurrence_two_forms_agree`). Applied to $\alpha|01\rangle+\beta|10\rangle$
it gives $C=2|\alpha\beta|$, which is zero *exactly* on Griffiths' two degenerate
cases — a numerical proof of his Problem 12.1 (`test_no_factorization_theorem`).

The **four Bell states** form a maximally entangled orthonormal basis:
$$|\Phi^\pm\rangle=\tfrac1{\sqrt2}(|00\rangle\pm|11\rangle),\qquad
|\Psi^\pm\rangle=\tfrac1{\sqrt2}(|01\rangle\pm|10\rangle),$$
with $|\Psi^-\rangle$ the singlet (`bell_basis`; `test_bell_states_orthonormal_basis`).

## 3. The singlet correlation $E(\mathbf a,\mathbf b)=-\mathbf a\cdot\mathbf b$

Bell's generalization of EPRB (Griffiths 3e §12.2, p.569): orient Alice's
detector along unit vector $\mathbf a$ and Bob's along $\mathbf b$, each reading
$\pm1$. The observable along $\hat{\mathbf n}$ is $\hat{\mathbf
n}\!\cdot\!\boldsymbol\sigma$ (eigenvalues $\pm1$; `measure_op`). The average of
the product of the two readings, in the singlet, is
$$\boxed{\,E(\mathbf a,\mathbf b)=\langle\Psi^-|(\mathbf a\!\cdot\!\boldsymbol\sigma)\otimes(\mathbf b\!\cdot\!\boldsymbol\sigma)|\Psi^-\rangle=-\,\mathbf a\!\cdot\!\mathbf b=-\cos\theta_{ab}\,}$$
(Griffiths 3e §12.2, Eq. 12.4, p.570). Parallel detectors ($\mathbf b=\mathbf a$)
give $E=-1$ (perfect anti-correlation, Eq. 12.2); anti-parallel give $E=+1$
(Eq. 12.3). The code computes $E$ *from the state* and checks it against the
closed form $-\mathbf a\!\cdot\!\mathbf b$ for random directions
(`correlation`, `E_singlet`; `test_singlet_correlation_is_minus_a_dot_b`).

## 4. Bell's theorem: the local-hidden-variable bound

Suppose a hidden variable $\lambda$ (distributed as $\rho(\lambda)\ge0$,
$\int\rho\,d\lambda=1$) fixes the outcomes. **Locality** demands Alice's result
depend only on *her* setting, not Bob's: there are functions
$A(\mathbf a,\lambda)=\pm1$ and $B(\mathbf b,\lambda)=\pm1$ (Griffiths 3e §12.2,
p.570, Eqs. 12.5–12.6), with perfect anti-correlation when aligned,
$B(\mathbf a,\lambda)=-A(\mathbf a,\lambda)$. The correlation is
$$P(\mathbf a,\mathbf b)=\int\rho(\lambda)\,A(\mathbf a,\lambda)\,B(\mathbf b,\lambda)\,d\lambda
=-\int\rho(\lambda)\,A(\mathbf a,\lambda)\,A(\mathbf b,\lambda)\,d\lambda.$$

**Griffiths' inequality (3 settings).** Using $A(\mathbf b,\lambda)^2=1$,
$$P(\mathbf a,\mathbf b)-P(\mathbf a,\mathbf c)
=-\!\int\!\rho\,A(\mathbf a)A(\mathbf b)\big[1-A(\mathbf b)A(\mathbf c)\big]d\lambda,$$
and since $\rho[1-A(\mathbf b)A(\mathbf c)]\ge0$,
$$\boxed{\,|P(\mathbf a,\mathbf b)-P(\mathbf a,\mathbf c)|\le 1+P(\mathbf b,\mathbf c)\,}$$
(Griffiths 3e Eq. 12.12, p.571). QM violates it: take $\mathbf a\perp\mathbf b$
with $\mathbf c$ at $45°$ to both, so $P(\mathbf a,\mathbf b)=0$,
$P(\mathbf a,\mathbf c)=P(\mathbf b,\mathbf c)=-\tfrac1{\sqrt2}$, giving
$$\tfrac1{\sqrt2}\approx0.707\;\not\le\;1-\tfrac1{\sqrt2}\approx0.293.$$
(Griffiths 3e p.571, Fig. 12.3.) (`bell_3setting`;
`test_griffiths_3setting_bell_violation`.)

**CHSH inequality (4 settings).** The modern, experiment-standard form
(Clauser–Horne–Shimony–Holt 1969) uses two settings per side,
$$\boxed{\,S=E(\mathbf a,\mathbf b)-E(\mathbf a,\mathbf b')+E(\mathbf a',\mathbf b)+E(\mathbf a',\mathbf b')\,}.$$
For any **local deterministic** strategy the four readings $A,A',B,B'\in\{\pm1\}$
give
$$S=A(B-B')+A'(B+B'),$$
and since $B,B'=\pm1$, one of $(B-B')$, $(B+B')$ is $0$ and the other is $\pm2$,
so $|S|=2$ for *every* $\lambda$. Any local hidden-variable theory is a convex
mixture of these strategies, hence
$$\boxed{\,|S|\le 2\quad\text{(classical / LHV bound)}\,}.$$
The code enumerates all 16 deterministic strategies and confirms $|S|\le2$ with
the maximum exactly $2$, then checks random mixtures stay $\le2$, and that a
*physical* shared-randomness model (shared $\boldsymbol\lambda$,
$A=\mathrm{sgn}(\mathbf a\!\cdot\!\boldsymbol\lambda)$) sits at/under $2$ and far
below the quantum value (`lhv_deterministic_strategies`,
`test_chsh_classical_bound_exhaustive`, `test_chsh_physical_lhv_model_below_2`).

## 5. The quantum violation and the Tsirelson bound

For the singlet, $E=-\cos\theta$, and choosing the four directions in a plane at
the **optimal angles** $(\mathbf a,\mathbf a',\mathbf b,\mathbf b')=(0°,90°,45°,135°)$
makes three terms reinforce:
$$S=-\cos45°-\cos135°... \;\Rightarrow\;|S|=2\sqrt2\approx2.828>2.$$
Concretely $E(a,b)=E(a',b)=E(a',b')=-\tfrac1{\sqrt2}$ and $E(a,b')=+\tfrac1{\sqrt2}$,
so $S=-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}=-2\sqrt2$.
Quantum mechanics **beats the classical bound** (`chsh_from_angles`;
`test_chsh_quantum_violation_at_optimal_angles`).

But it cannot beat $2\sqrt2$. **Tsirelson's bound** (Cirel'son 1980) says
$$\boxed{\,|S|\le 2\sqrt2\quad\text{(quantum bound)}\,}$$
for *any* state and *any* observables with eigenvalues $\pm1$. Sketch: the CHSH
operator $\hat B$ squares to $\hat B^2=4\,\mathbb I-[\hat A,\hat A']\otimes[\hat
B,\hat B']$, and each commutator has norm $\le2$, so $\lVert\hat
B^2\rVert\le4+4=8$, i.e. $\lVert\hat B\rVert\le2\sqrt2$. The code verifies this
two ways: $|S|\le2\sqrt2$ for the singlet over thousands of random angle sets,
and $\lVert\hat B\rVert\le2\sqrt2$ at the operator level for arbitrary settings
and arbitrary states (`chsh_operator`, `tsirelson_bound`;
`test_chsh_never_exceeds_tsirelson`).

So entanglement is a *bounded* resource: it sits strictly between the classical
$2$ and the algebraic maximum $4$. The Aspect–Grangier–Roger experiments
(Griffiths 3e p.571) measured $S$ near $2\sqrt2$ — local hidden variables are
ruled out by experiment, not just by argument.

> **Bridge to `~QO-05` (not built).** Aspect used entangled *photon polarization*.
> Because polarization correlation goes as $\cos2\theta$, the optimal analyzer
> angles are halved to $0°,22.5°,45°,67.5°$ — the same $2\sqrt2$ violation in a
> different physical realization. `~QO-05` will build the optical version.

## 6. What it means — and what it doesn't

**It means:** there is **no local hidden variable theory** behind quantum
mechanics. Either locality fails or realism fails; the experiments say nature is
**nonlocal** (Griffiths 3e p.571). The realist program EPR launched is dead in
its *local* form.

**It does not mean** you can signal faster than light. The entangled
correlations are only visible when Alice and Bob *compare notes* (a classical,
subluminal channel). Alice's own data — her marginal statistics — are completely
independent of what Bob does. Formally, for **any** unitary $U$ (Bob's choice of
measurement basis),
$$\rho_A=\mathrm{Tr}_B\big[(\,\mathbb I\otimes U)\,\rho\,(\mathbb I\otimes U^\dagger)\big]=\mathrm{Tr}_B\,\rho,$$
and even if Bob *measures* (non-selectively) in any basis, averaging over his
outcomes leaves
$$\rho_A=\sum_k\mathrm{Tr}_B\big[(\mathbb I\otimes P_k)\rho(\mathbb I\otimes P_k)\big]=\mathrm{Tr}_B\,\rho.$$
Bob cannot change $\rho_A$, so Alice cannot tell what Bob did — **no signaling**
(Griffiths 3e p.571–572, the moving-shadow argument: the shadow can move faster
than light but carries no energy or information). For a Bell state $\rho_A=\mathbb
I/2$ no matter what Bob does. (`no_signaling_unitary`, `no_signaling_measurement`;
`test_no_signaling_under_bob_unitary`, `test_no_signaling_under_bob_measurement`.)

---
### Where this sits
`~QM-11` gave two qubits and the spin algebra; `~QM-20` gave the reduced density
matrix. This module uses them to define entanglement (§2), correlate it (§3), and
bound it both classically (§4, $|S|\le2$) and quantum-mechanically (§5,
$|S|\le2\sqrt2$). The singlet's rotational invariance ties to the $J=0$
addition-of-angular-momentum result of `~QM-13`; the no-signaling theorem (§6)
is the bridge to relativity (`~RE-06`); and the optical Bell test / squeezing is
`~QO-05`.
