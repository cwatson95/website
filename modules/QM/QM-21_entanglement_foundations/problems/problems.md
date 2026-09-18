# QM-21 — Problems

Work them by hand, then check with `code/entanglement.py`. Sources in `../refs.md`.
Spin observables use natural units $\hbar=1$: the measurement along $\hat{\mathbf
n}$ is $\hat{\mathbf n}\!\cdot\!\boldsymbol\sigma$ with eigenvalues $\pm1$.
Two-qubit basis order is $|00\rangle,|01\rangle,|10\rangle,|11\rangle$
(A = "Alice", B = "Bob").

### P1.  Entangled states — the no-factorization theorem  *(Griffiths 3e, Prob. 12.1, p.568)*
Show that $|\psi\rangle=\alpha|01\rangle+\beta|10\rangle$ cannot be written as a
product $|a\rangle\otimes|b\rangle$ unless $\alpha=0$ or $\beta=0$.
*Answer:* a product $(a_0|0\rangle+a_1|1\rangle)\otimes(b_0|0\rangle+b_1|1\rangle)$
has amplitudes $(a_0b_0,a_0b_1,a_1b_0,a_1b_1)$, which must satisfy
$a_0b_0=a_1b_1=0$ (the $|00\rangle,|11\rangle$ coefficients) yet
$a_0b_1=\alpha\neq0$ and $a_1b_0=\beta\neq0$ — impossible. Equivalently the
concurrence $C=2|ad-bc|=2|\alpha\beta|$ is nonzero, so the state is entangled.
*Check:* `concurrence(np.array([0,a,b,0]))` $=2|\alpha\beta|>0$ for $a,b\neq0$;
`is_product_state(...)` is `False`. (`test_no_factorization_theorem`.)

**Solution.** A product state expands as
$(a_0|0\rangle+a_1|1\rangle)\otimes(b_0|0\rangle+b_1|1\rangle)=a_0b_0|00\rangle+a_0b_1|01\rangle+a_1b_0|10\rangle+a_1b_1|11\rangle$.
Matching $\alpha|01\rangle+\beta|10\rangle$ needs $a_0b_0=0$ and $a_1b_1=0$, yet $a_0b_1=\alpha\neq0$
forces $a_0,b_1\neq0$ and $a_1b_0=\beta\neq0$ forces $a_1,b_0\neq0$ — then $a_0b_0\neq0$, a
contradiction. So no factorization exists. Equivalently the concurrence
$C=2|ad-bc|=2|0\cdot0-\alpha\beta|=2|\alpha\beta|$ is nonzero. With $(\alpha,\beta)=(0.6,0.8)$,
`concurrence(np.array([0,a,b,0]))`$=0.96>0$ and `is_product_state(...)` is `False`.

### P2.  The reduced state is the entanglement diagnostic  *(Griffiths 3e §12.1, p.567–568; ~QM-20)*
Trace out Bob. For the product state $|0\rangle\otimes|1\rangle$ and for the
singlet, what is Alice's reduced state $\rho_A$, and what does its purity say?
*Answer:* product → $\rho_A=|0\rangle\langle0|$, **pure**, $\mathrm{Tr}(\rho_A^2)=1$
(Alice has a definite state). Singlet → $\rho_A=\tfrac12\mathbb I$, **maximally
mixed**, $\mathrm{Tr}(\rho_A^2)=\tfrac12$ (knowing the pair tells you nothing
about Alice alone). That gap is entanglement.
*Check:* `purity(partial_trace(density_matrix(product_state(ket0,ket1)),0))` $=1$;
`purity(partial_trace(density_matrix(singlet()),0))` $=0.5$, and the matrix is
$I/2$. (`test_product_state_reduced_is_pure`, `test_bell_state_reduced_is_maximally_mixed`.)

**Solution.** With $\rho=|\psi\rangle\langle\psi|$, trace out Bob. The product $|0\rangle\otimes|1\rangle$
keeps its factorization, $\rho_A=|0\rangle\langle0|\,\langle1|1\rangle=|0\rangle\langle0|$, so
$\mathrm{Tr}(\rho_A^2)=1$ — pure. For the singlet $|\Psi^-\rangle=\tfrac1{\sqrt2}(|01\rangle-|10\rangle)$,
$$\rho_A=\mathrm{Tr}_B\,\rho=\tfrac12\big(|0\rangle\langle0|+|1\rangle\langle1|\big)=\tfrac12\mathbb I,
\qquad \mathrm{Tr}(\rho_A^2)=\tfrac12.$$
The maximally mixed $\rho_A$ means Alice's qubit alone reads 50/50 in every basis — the global
pure state pins down *nothing* local; that gap is the entanglement. Matches `purity(...)`$=1.0$
for the product vs $=0.5$ for the singlet, whose $\rho_A=I/2$.

### P3.  The singlet correlation $E(\mathbf a,\mathbf b)=-\mathbf a\cdot\mathbf b$  *(Griffiths 3e §12.2, Eq. 12.4, p.570)*
Compute $E(\mathbf a,\mathbf b)=\langle\Psi^-|(\mathbf a\!\cdot\!\boldsymbol\sigma)
\otimes(\mathbf b\!\cdot\!\boldsymbol\sigma)|\Psi^-\rangle$. What is it for
parallel, anti-parallel, and perpendicular detectors?
*Answer:* $E=-\mathbf a\!\cdot\!\mathbf b=-\cos\theta_{ab}$. Parallel: $-1$
(perfect anti-correlation, Eq. 12.2); anti-parallel: $+1$ (Eq. 12.3);
perpendicular: $0$ (uncorrelated).
*Check:* `E_singlet(ndir(0), ndir(0))` $=-1$; `E_singlet(ndir(0), ndir(np.pi))`
$=+1$; `E_singlet(ndir(0), ndir(np.pi/2))` $=0$. (`test_singlet_correlation_is_minus_a_dot_b`.)

**Solution.** On the singlet the two-spin operator is isotropic,
$\langle\Psi^-|\sigma_i\otimes\sigma_j|\Psi^-\rangle=-\delta_{ij}$, so
$$E(\mathbf a,\mathbf b)=\sum_{i,j}a_ib_j\,\langle\Psi^-|\sigma_i\otimes\sigma_j|\Psi^-\rangle
=-\sum_i a_ib_i=-\mathbf a\!\cdot\!\mathbf b=-\cos\theta_{ab}.$$
Parallel detectors ($\theta=0$) give $E=-1$ — whenever Alice reads $+1$, Bob reads $-1$ (perfect
anti-correlation); anti-parallel ($\theta=\pi$) give $E=+1$; perpendicular ($\theta=\pi/2$) give
$E=0$. Confirmed by `E_singlet(ndir(0),ndir(0))`$=-1$, `E_singlet(ndir(0),ndir(np.pi))`$=+1$, and
`E_singlet(ndir(0),ndir(np.pi/2))`$\approx0$.

### P4.  Griffiths' Bell inequality and its 45° violation  *(Griffiths 3e §12.2, Eq. 12.12, p.571)*
A local hidden-variable theory obeys $|P(\mathbf a,\mathbf b)-P(\mathbf a,\mathbf
c)|\le1+P(\mathbf b,\mathbf c)$. Take $\mathbf a\perp\mathbf b$ with $\mathbf c$
at $45°$ to both. Does quantum mechanics satisfy it?
*Answer:* QM gives $P(a,b)=-\cos90°=0$, $P(a,c)=P(b,c)=-\cos45°=-\tfrac1{\sqrt2}$.
LHS $=|0-(-\tfrac1{\sqrt2})|=0.707$; RHS $=1-\tfrac1{\sqrt2}=0.293$. So
$0.707\le0.293$ is **false** — QM **violates** Bell.
*Check:* `bell_3setting(ndir(0), ndir(np.pi/2), ndir(np.pi/4))` returns
$(0.707, 0.293)$ with LHS > RHS. (`test_griffiths_3setting_bell_violation`.)

**Solution.** Using $E(\mathbf a,\mathbf b)=-\cos\theta_{ab}$ with $\mathbf a\perp\mathbf b$ and
$\mathbf c$ at $45°$ to each,
$$P(\mathbf a,\mathbf b)=-\cos90°=0,\qquad P(\mathbf a,\mathbf c)=P(\mathbf b,\mathbf c)=-\cos45°=-\tfrac1{\sqrt2}.$$
The inequality $|P(\mathbf a,\mathbf b)-P(\mathbf a,\mathbf c)|\le1+P(\mathbf b,\mathbf c)$ then reads
$$\Big|0-\big(-\tfrac1{\sqrt2}\big)\Big|=\tfrac1{\sqrt2}\approx0.707\ \overset{?}{\le}\ 1-\tfrac1{\sqrt2}\approx0.293,$$
which is **false**: quantum mechanics violates Griffiths' Bell inequality.
`bell_3setting(ndir(0),ndir(np.pi/2),ndir(np.pi/4))` returns $(0.707,0.293)$ with LHS $>$ RHS.

### P5.  CHSH and the Tsirelson bound
The CHSH quantity is $S=E(a,b)-E(a,b')+E(a',b)+E(a',b')$. (a) Show $|S|\le2$ for
any local deterministic theory. (b) Find the singlet's $S$ at the optimal spin
angles $(a,a',b,b')=(0°,90°,45°,135°)$.
*Answer:* (a) $S=A(B-B')+A'(B+B')$ with $A,A',B,B'=\pm1$; one of $B\mp B'$ is $0$,
the other $\pm2$, so $|S|=2$ exactly — and any mixture stays $\le2$. (b) Three
correlations equal $-\tfrac1{\sqrt2}$ and one $+\tfrac1{\sqrt2}$, giving
$S=-2\sqrt2\approx-2.828$ — above the classical $2$, and equal to the
**Tsirelson** bound $2\sqrt2$, which $|S|$ never exceeds.
*Check:* `lhv_deterministic_strategies()` → all $|S|\le2$, max $=2$;
`chsh_from_angles(singlet(),0,90,45,135)` $=-2\sqrt2$; `tsirelson_bound()`
$=2.828$. (`test_chsh_classical_bound_exhaustive`,
`test_chsh_quantum_violation_at_optimal_angles`, `test_chsh_never_exceeds_tsirelson`.)

**Solution.** (a) For a local deterministic assignment $A,A',B,B'\in\{\pm1\}$,
$$S=AB-AB'+A'B+A'B'=A(B-B')+A'(B+B').$$
Since $B,B'=\pm1$, exactly one of $B-B'$, $B+B'$ vanishes and the other is $\pm2$, so $|S|=2$ for
*every* strategy; a general LHV theory is a convex mixture of these vertices and stays $|S|\le2$.
(b) At $(0°,90°,45°,135°)$ the singlet gives $E(a,b)=E(a',b)=E(a',b')=-\tfrac1{\sqrt2}$ and
$E(a,b')=+\tfrac1{\sqrt2}$, so $S=-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}-\tfrac1{\sqrt2}=-2\sqrt2$.
Thus `lhv_deterministic_strategies()` has max $|S|=2$, while
`chsh_from_angles(singlet(),0,90,45,135)`$=-2.828=-2\sqrt2$, exactly `tsirelson_bound()`$=2.828$.

### P6.  A classical hidden-variable model can't reach the quantum value  *(Griffiths 3e, Prob. 12.3, p.573)*
"Baseballs": a shared random vector $\boldsymbol\lambda$ is set at launch; each
detector records $\mathrm{sgn}$ of the spin component along its axis (Alice
$A=\mathrm{sgn}(\mathbf a\!\cdot\!\boldsymbol\lambda)$, Bob the negative). With
isotropic $\boldsymbol\lambda$, what is $P(\mathbf a,\mathbf b)$, and what CHSH
$S$ does it give?
*Answer:* $P(\mathbf a,\mathbf b)=-1+2\eta/\pi$ (linear in the angle $\eta$, vs
the quantum $-\cos\eta$). It is a *local* model, so $|S|\le2$ — at the optimal
angles it sits right at $2$, never reaching the quantum $2\sqrt2$. This is
Griffiths' explicit demonstration (Prob. 12.3d) that a local theory satisfies
Bell.
*Check:* the Monte-Carlo estimate in `test_chsh_physical_lhv_model_below_2`
returns $|S|\lesssim2$ and well under $2.4$.

**Solution.** For isotropic $\boldsymbol\lambda$ the readings $\mathrm{sgn}(\mathbf a\!\cdot\!\boldsymbol\lambda)$
and $\mathrm{sgn}(\mathbf b\!\cdot\!\boldsymbol\lambda)$ disagree with probability $\eta/\pi$ (the
fraction of the sphere between the two flip-planes), $\eta$ being the angle between $\mathbf a,\mathbf b$.
With Bob's extra minus sign,
$$P(\mathbf a,\mathbf b)=\big\langle\mathrm{sgn}(\mathbf a\!\cdot\!\boldsymbol\lambda)\,[-\mathrm{sgn}(\mathbf b\!\cdot\!\boldsymbol\lambda)]\big\rangle
=-\Big(1-\tfrac{2\eta}{\pi}\Big)=-1+\tfrac{2\eta}{\pi},$$
*linear* in $\eta$ rather than the quantum $-\cos\eta$. Being local it must obey $|S|\le2$; at the
optimal angles $\eta=45°,135°$ it gives $S=-2$, sitting right at the classical bound and never
reaching $2\sqrt2$. Accordingly the Monte-Carlo `test_chsh_physical_lhv_model_below_2` returns
$|S|\lesssim2$, well under $2.4$.

### P7.  No faster-than-light signaling
Alice and Bob share a Bell state. Can Bob's choice of *what to measure* (or
whether to measure) change Alice's local statistics?
*Answer:* No. For any Bob unitary $U$, $\rho_A=\mathrm{Tr}_B[(\mathbb I\otimes
U)\rho(\mathbb I\otimes U^\dagger)]=\mathrm{Tr}_B\rho$; and a non-selective Bob
measurement, averaged over outcomes, also leaves $\rho_A$ unchanged ($=\mathbb
I/2$ for a Bell state). Alice's data alone are "completely random" regardless of
Bob (Griffiths 3e p.572) — the correlations appear only when the two lists are
compared, so no information travels.
*Check:* `no_signaling_unitary(singlet(), U)` and
`no_signaling_measurement(singlet(), U)` return $(\rho_A^{before},\rho_A^{after})$
that are equal to machine precision. (`test_no_signaling_under_bob_unitary`,
`test_no_signaling_under_bob_measurement`.)

**Solution.** Partial trace is cyclic *within* Bob's factor, so for any unitary $U$
$$\rho_A=\mathrm{Tr}_B\big[(\mathbb I\otimes U)\rho(\mathbb I\otimes U^\dagger)\big]
=\mathrm{Tr}_B\big[\rho\,(\mathbb I\otimes U^\dagger U)\big]=\mathrm{Tr}_B\,\rho.$$
A non-selective measurement inserts $\sum_kP_k=\mathbb I$, so
$\rho'=\sum_k(\mathbb I\otimes P_k)\rho(\mathbb I\otimes P_k)$ likewise gives
$\mathrm{Tr}_B\rho'=\mathrm{Tr}_B[\rho\sum_kP_k]=\rho_A$. Bob cannot touch Alice's marginal — for a
Bell state it stays $\mathbb I/2$ whatever he does, so her data alone are completely random and carry
no signal. Hence `no_signaling_unitary(singlet(),U)` and `no_signaling_measurement(singlet(),U)`
return $\rho_A^{\text{before}}=\rho_A^{\text{after}}$ to machine precision.

### P8.  The singlet is the $J=0$ state  *(~QM-13; Griffiths 3e §12.1, p.567)*
Show the singlet is unchanged by a simultaneous rotation of both spins,
$(U\otimes U)|\Psi^-\rangle=|\Psi^-\rangle$ for $U\in SU(2)$, and that the
triplet/$|\Phi^+\rangle$ is not. What does invariance mean physically?
*Answer:* the singlet is the rotational **scalar** — total angular momentum
$J=0$ — so it looks the same from every orientation (which is why "spin up" along
*any* axis on one side forces "spin down" along that same axis on the other). The
$J=1$ states transform nontrivially.
*Check:* with `U = su2(theta, axis)`, `kron(U,U) @ singlet()` equals `singlet()`;
for `bell_state("Phi+")` under a $z$-rotation it does not.
(`test_singlet_rotational_invariance_J0`.)

**Solution.** Write the singlet antisymmetrically, $|\Psi^-\rangle=\tfrac1{\sqrt2}\sum_{ij}\varepsilon_{ij}|i\rangle|j\rangle$
with $\varepsilon_{01}=-\varepsilon_{10}=1$. Under $U\otimes U$ the coefficient of $|k\rangle|l\rangle$
becomes $\sum_{ij}\varepsilon_{ij}U_{ki}U_{lj}=\varepsilon_{kl}\det U$, so
$$(U\otimes U)|\Psi^-\rangle=(\det U)\,|\Psi^-\rangle=|\Psi^-\rangle\qquad(\det U=1\ \text{for }U\in SU(2)).$$
The singlet is the rotational scalar $J=0$ — the same from every orientation, which is exactly why
"up along $\hat{\mathbf n}$" for Alice forces "down along $\hat{\mathbf n}$" for Bob on *any* axis.
The symmetric triplet $|\Phi^+\rangle$ ($J=1$) instead picks up relative phases $e^{\mp i\theta}$ on
$|00\rangle,|11\rangle$ under a $z$-rotation. Hence `kron(U,U) @ singlet()` equals `singlet()`, while
for `bell_state("Phi+")` it does not.
