# QM-06 — Problems

Work them by hand, then check with `code/measurement.py`. Sources in `../refs.md`.
Spin states/operators use natural units $\hbar=1$, so $\sigma$ eigenvalues are
$\pm1$ and $S=\tfrac\hbar2\sigma$ eigenvalues are $\pm\tfrac12$.

### P1.  Why observables are Hermitian  *(Griffiths 3e, Prob. 3.8, p.129)*
Show that a Hermitian operator has (a) real eigenvalues and (b) an orthonormal,
complete set of eigenvectors — the two properties that make it a legitimate
observable (real meter readings; a full set of distinguishable outcomes).
*Answer:* $\hat A=\hat A^\dagger\Rightarrow a_n\in\mathbb R$ and $\langle
a_m|a_n\rangle=\delta_{mn}$ with $\sum_n|a_n\rangle\langle a_n|=\mathbb 1$
(Griffiths §3.3, p.127).
*Check:* `eigensystem(A)` returns real eigenvalues; for a random Hermitian `A`,
`V.conj().T @ V` and `V @ V.conj().T` are both the identity.
(`test_hermitian_real_eigenvalues`, `test_eigenbasis_orthonormal_and_complete`.)

**Solution.** Let $\hat A=\hat A^\dagger$ with $\hat A|a_n\rangle=a_n|a_n\rangle$ and
$\langle a_n|a_n\rangle=1$. Sandwiching the operator and moving it onto the bra
(Hermiticity) gives
$$a_n=\langle a_n|\hat A|a_n\rangle=\langle\hat A a_n|a_n\rangle=a_n^*,$$
so $a_n\in\mathbb R$ — real meter readings. For two eigenvectors,
$\langle a_m|\hat A|a_n\rangle$ read rightward is $a_n\langle a_m|a_n\rangle$ and read
leftward (Hermiticity, $a_m$ real) is $a_m\langle a_m|a_n\rangle$, so
$(a_n-a_m)\langle a_m|a_n\rangle=0$ forces $\langle a_m|a_n\rangle=0$ when $a_n\neq a_m$
(degenerate blocks are orthogonalized by Gram–Schmidt). The spectral theorem then makes
the normalized set complete, $\sum_n|a_n\rangle\langle a_n|=\mathbb 1$. This is exactly why
`eigensystem(A)` returns real eigenvalues and `V.conj().T @ V = V @ V.conj().T = I`.

### P2.  The generalized statistical interpretation  *(Griffiths 3e §3.4, p.133)*
A particle is in state $|\psi\rangle=\sum_n c_n|a_n\rangle$. What values can a
measurement of $A$ return, with what probabilities, and why do they form a
probability distribution?
*Answer:* one of the eigenvalues $a_n$, with $P(a_n)=|c_n|^2=|\langle
a_n|\psi\rangle|^2$; completeness + normalization give $\sum_n P(a_n)=1$.
*Check:* for any state and Hermitian `A`, `outcome_probabilities(psi, A)[1].sum()`
$=1$. (`test_probabilities_sum_to_one`, `test_born_rule_nondegenerate`.)

**Solution.** A measurement can only return one of the eigenvalues $a_n$ of $\hat A$.
Projecting the expansion $|\psi\rangle=\sum_n c_n|a_n\rangle$ onto $\langle a_m|$ isolates the
amplitude $c_m=\langle a_m|\psi\rangle$, and the generalized Born rule assigns
$$P(a_n)=|\langle a_n|\psi\rangle|^2=|c_n|^2.$$
These form a probability distribution because completeness
$\sum_n|a_n\rangle\langle a_n|=\mathbb 1$ and normalization give
$$\sum_n P(a_n)=\sum_n|c_n|^2=\langle\psi|\Big(\sum_n|a_n\rangle\langle a_n|\Big)|\psi\rangle
=\langle\psi|\psi\rangle=1.$$
Hence `outcome_probabilities(psi, A)[1].sum()` $=1$ for any state and any Hermitian `A`.

### P3.  Expectation value two ways  *(Griffiths 3e §3.4, Eqs. 3.48–3.51, p.134)*
Show $\langle A\rangle=\sum_n a_nP(a_n)$ equals $\langle\psi|\hat A|\psi\rangle$,
and that it is real for a Hermitian $\hat A$.
*Answer:* substitute $|\psi\rangle=\sum_n c_n|a_n\rangle$ into the sandwich and
use $\hat A|a_n\rangle=a_n|a_n\rangle$, $\langle a_m|a_n\rangle=\delta_{mn}$:
$\langle\psi|\hat A|\psi\rangle=\sum_n a_n|c_n|^2$.
*Check:* `expectation(psi, A)` computes both forms and asserts they agree; it
returns a real number. (`test_expectation_two_ways`.)

**Solution.** Insert $|\psi\rangle=\sum_n c_n|a_n\rangle$ into the sandwich and use
$\hat A|a_n\rangle=a_n|a_n\rangle$ with $\langle a_m|a_n\rangle=\delta_{mn}$:
$$\langle\psi|\hat A|\psi\rangle=\sum_{m,n}c_m^*c_n\,a_n\langle a_m|a_n\rangle
=\sum_n a_n|c_n|^2=\sum_n a_n\,P(a_n).$$
So the "average of outcomes" and the "sandwich" are the same number. It is real because
every $a_n\in\mathbb R$ and every $|c_n|^2\ge0$ — equivalently
$\langle\psi|\hat A|\psi\rangle^*=\langle\psi|\hat A^\dagger|\psi\rangle=\langle\psi|\hat A|\psi\rangle$.
`expectation(psi, A)` evaluates both the spectral and sandwich forms and asserts they agree,
returning that real value.

### P4.  Determinate states  *(Griffiths 3e §3.2.2, p.125)*
For which states is a measurement of $A$ certain (zero spread)? Compute the
variance of $\sigma_z$ in $|0\rangle$ (spin-up-$z$) and in $|{+x}\rangle$.
*Answer:* the determinate states are exactly the eigenstates of $\hat A$
($\sigma_A=0\Leftrightarrow\hat A\psi=q\psi$). $\mathrm{Var}_{|0\rangle}
(\sigma_z)=0$ (eigenstate); $\mathrm{Var}_{|+x\rangle}(\sigma_z)=1$
($\langle\sigma_z\rangle=0$, $\langle\sigma_z^2\rangle=1$).
*Check:* `variance(spin_state(0), sigma_z)` $\approx0$;
`variance(spin_state(np.pi/2,0), sigma_z)` $\approx1$.
(`test_variance_nonneg_and_determinacy`, `test_eigenstate_is_determinate`.)

**Solution.** Write the spread as
$\sigma_A^2=\langle(\hat A-\langle A\rangle)^2\rangle=\lVert(\hat A-\langle A\rangle)|\psi\rangle\rVert^2\ge0$,
which vanishes iff $(\hat A-\langle A\rangle)|\psi\rangle=0$, i.e. $|\psi\rangle$ is an eigenstate
($\hat A\psi=q\psi$ with $q=\langle A\rangle$). For $|0\rangle$: $\sigma_z|0\rangle=+|0\rangle$ is an
eigenstate, so $\mathrm{Var}=0$. For $|{+x}\rangle=\tfrac1{\sqrt2}(1,1)$ the diagonal
$\sigma_z=\mathrm{diag}(1,-1)$ gives $\langle\sigma_z\rangle=\tfrac12(1-1)=0$, while
$\sigma_z^2=\mathbb 1\Rightarrow\langle\sigma_z^2\rangle=1$, so
$$\mathrm{Var}_{|+x\rangle}(\sigma_z)=\langle\sigma_z^2\rangle-\langle\sigma_z\rangle^2=1-0=1.$$
This matches `variance(spin_state(0), sigma_z)` $\approx0$ and
`variance(spin_state(np.pi/2,0), sigma_z)` $\approx1$.

### P5.  Collapse is idempotent  *(Griffiths 3e §3.4, p.133; Prob. 3.23, p.154)*
After a measurement of $A$ returns $a_n$, the state is $\hat
P_n|\psi\rangle/\lVert\hat P_n|\psi\rangle\rVert$. Show that an immediate
re-measurement returns $a_n$ with probability 1, and connect this to the fact
that projectors satisfy $\hat P_n^2=\hat P_n$.
*Answer:* the collapsed state is an eigenstate of $\hat A$ (eigenvalue $a_n$), so
$P'(a_n)=\lVert\hat P_n\psi'\rVert^2=1$; idempotence $\hat P_n^2=\hat P_n$ is
exactly why the second projection changes nothing.
*Check:* `s = collapse(psi, A, n); outcome_probabilities(s, A)[1][n]` $=1$.
(`test_collapse_idempotent`.)

**Solution.** Collapse sends $|\psi\rangle\to|\psi'\rangle=\hat P_n|\psi\rangle/\lVert\hat P_n|\psi\rangle\rVert$.
The weight of the same outcome on re-measurement is $P'(a_n)=\lVert\hat P_n|\psi'\rangle\rVert^2$.
Using idempotence $\hat P_n^2=\hat P_n$,
$$\hat P_n|\psi'\rangle=\frac{\hat P_n^2|\psi\rangle}{\lVert\hat P_n\psi\rVert}
=\frac{\hat P_n|\psi\rangle}{\lVert\hat P_n\psi\rVert}=|\psi'\rangle,$$
so $\hat P_n$ leaves $|\psi'\rangle$ untouched and $P'(a_n)=\lVert\psi'\rVert^2=1$. The collapsed
state is already an $a_n$-eigenstate, so the second projection changes nothing — this is the
reproducibility checked by `s = collapse(psi, A, n)` then `outcome_probabilities(s, A)[1][n]` $=1$.

### P6.  Stern–Gerlach: the spin projection law
A spin-½ is prepared pointing at polar angle $\theta$ from $\hat z$.
(a) What is $\langle\sigma_z\rangle$? (b) If it is prepared along $\hat x$
($\theta=90^\circ$) and you measure $\sigma_z$, what are the probabilities?
*Answer:* (a) $\langle\sigma_z\rangle=\cos\theta$ (so $\langle S_z\rangle=
\tfrac\hbar2\cos\theta$ — the spin-½ Malus law). (b) $P(\pm1)=\tfrac12$ each:
$\hat z$ and $\hat x$ are mutually unbiased because $[\sigma_x,\sigma_z]\neq0$.
*Check:* `expectation(spin_state(np.pi/3), sigma_z)` $=0.5$ ($\cos60^\circ$);
`outcome_probabilities(spin_state(np.pi/2,0), sigma_z)` $\to(\,[-1,1],[0.5,0.5]\,)$.
(`test_spin_expectation_law`, `test_spin_born_probabilities`.)

**Solution.** The prepared state is $|{+n}\rangle=(\cos\tfrac\theta2,\,e^{i\phi}\sin\tfrac\theta2)$.
(a) With $\sigma_z=\mathrm{diag}(1,-1)$,
$$\langle\sigma_z\rangle=\cos^2\tfrac\theta2-\sin^2\tfrac\theta2=\cos\theta,$$
the spin-½ Malus law (so $\langle S_z\rangle=\tfrac\hbar2\cos\theta$); at $\theta=60^\circ$ this is
$\cos60^\circ=\tfrac12$. (b) For $\theta=90^\circ$, $|{+x}\rangle=\tfrac1{\sqrt2}(1,1)$, and the
$\sigma_z$-eigenstates are $|0\rangle,|1\rangle$, so
$$P(\pm1)=|\langle0|{+x}\rangle|^2=|\langle1|{+x}\rangle|^2=\cos^2\tfrac\pi4=\tfrac12.$$
Confirmed by `expectation(spin_state(np.pi/3), sigma_z)` $=0.5$ and
`outcome_probabilities(spin_state(np.pi/2,0), sigma_z)` $\to([-1,1],[0.5,0.5])$.

### P7.  Sequential measurements & disturbance  *(Griffiths 3e, Prob. 3.33, p.160; Prob. 3.16, p.140)*
Prepare $|{+x}\rangle$, so $\sigma_x$ is certain to read $+1$. (a) **Compatible**
case: re-measuring $\sigma_x$ (or any commuting observable then $\sigma_x$) still
gives $+1$ for sure. (b) **Incompatible** case: measure $\sigma_z$ *in between*,
then $\sigma_x$ again — what is $P(\sigma_x=+1)$ now?
*Answer:* (a) $+1$ with probability 1 — commuting observables share an eigenbasis
and do not disturb (Griffiths §3.5.1, p.139). (b) $P(+1)=\tfrac12$: the
intervening $\sigma_z$ collapses the state to a $\sigma_z$-eigenstate, which is an
equal superposition of $\sigma_x$ eigenstates, so the once-certain outcome is now
random. Noncommuting operators share no complete common eigenbasis (Prob. 3.16).
*Check:* `outcome_probabilities(spin_state(np.pi/2,0), sigma_x)[1]` $=[0,1]$
($+1$ sure); after `collapse(..., sigma_z, index_of(sigma_z,+1))` the
$\sigma_x$ probabilities become $[0.5, 0.5]$.
(`test_incompatible_randomized`, `test_compatible_no_disturbance`.)

**Solution.** (a) If $[\hat B,\sigma_x]=0$ the two share an eigenbasis, so measuring
$\sigma_x=+1$ leaves the state a simultaneous eigenstate and a later $\sigma_x$ still reads $+1$
— no disturbance. (b) Write $|{+x}\rangle=\tfrac1{\sqrt2}(|0\rangle+|1\rangle)$. The intervening
$\sigma_z$ measurement collapses it to $|0\rangle$ (or $|1\rangle$). Re-expanding that result in the
$\sigma_x$-basis, $|0\rangle=\tfrac1{\sqrt2}(|{+x}\rangle+|{-x}\rangle)$, gives
$$P(\sigma_x=+1)=|\langle{+x}|0\rangle|^2=\tfrac12.$$
Because $\sigma_z$ fails to commute, $[\sigma_x,\sigma_z]=-2i\sigma_y\neq0$, it shares no common
eigenbasis with $\sigma_x$ and randomizes the once-certain outcome. So
`outcome_probabilities(spin_state(np.pi/2,0), sigma_x)[1]` $=[0,1]$, but after
`collapse(..., sigma_z, index_of(sigma_z,+1))` the $\sigma_x$ probabilities become $[0.5,0.5]$.
