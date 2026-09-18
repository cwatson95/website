# QM-15 — Problems

Work them by hand, then check with `code/approximations.py`. Sources in
`../refs.md` (Griffiths & Schroeter 3e, Ch.7–9). Units $\hbar=m=\omega=1$.

### P1.  First-order energy is an expectation value  *(Griffiths 3e §7.1.2, Eq. 7.9, p.359)*
For $H=H^0+\lambda H'$, show the first-order energy shift is
$E_n^{(1)}=\langle\psi_n^0|H'|\psi_n^0\rangle$. Apply it to the oscillator with
$H'=x^2$ and with $H'=x$.
*Answer:* $\langle n|x^2|n\rangle=n+\tfrac12$ (stiffening raises every level);
$\langle n|x|n\rangle=0$ by parity (a uniform field gives no first-order shift).
*Check:* `first_order_energy(ho_energies(40), ho_matrix_power(40,2), 2)` → `2.5`;
`first_order_energy(ho_energies(40), ho_position(40), 2)` → `0.0`.
(`test_first_order_energy_is_expectation_value`.)

**Solution.** Insert the series into $H|\psi_n\rangle=E_n|\psi_n\rangle$ and collect $O(\lambda)$:
$H^0|\psi_n^{(1)}\rangle+H'|\psi_n^0\rangle=E_n^0|\psi_n^{(1)}\rangle+E_n^{(1)}|\psi_n^0\rangle$.
Project onto $\langle\psi_n^0|$; since $H^0$ is Hermitian,
$\langle\psi_n^0|H^0|\psi_n^{(1)}\rangle=E_n^0\langle\psi_n^0|\psi_n^{(1)}\rangle$ cancels the
matching term on the right, leaving $E_n^{(1)}=\langle\psi_n^0|H'|\psi_n^0\rangle$. With
$x=\tfrac1{\sqrt2}(a+a^\dagger)$ the number-conserving terms give
$\langle n|x^2|n\rangle=\tfrac12\langle n|(aa^\dagger+a^\dagger a)|n\rangle=\tfrac12(2n+1)=n+\tfrac12$,
while $\langle n|x|n\rangle=0$ because $x$ sends $|n\rangle\to|n\pm1\rangle$. At $n=2$ these are
$2.5$ and $0$ — matching `first_order_energy(...,ho_matrix_power(40,2),2)`→`2.5` and
`(...,ho_position(40),2)`→`0.0`.

### P2.  Second-order energy and level repulsion  *(Griffiths 3e §7.1.3, Eq. 7.15, p.363)*
Derive $E_n^{(2)}=\sum_{m\neq n}|\langle m|H'|n\rangle|^2/(E_n^0-E_m^0)$ and
evaluate it for the oscillator with $H'=x^2$. Why is $E_0^{(2)}\le0$ for *any*
$H'$?
*Answer:* $E_n^{(2)}=-\tfrac12(n+\tfrac12)$. For the ground state every
denominator $E_0^0-E_m^0<0$, so $E_0^{(2)}\le0$ — second order always pushes the
ground state down (states "repel").
*Check:* `second_order_energy(ho_energies(60), ho_matrix_power(60,2), 2)` →
`-1.25`. (`test_second_order_energy_formula`,
`test_second_order_energy_pushes_ground_state_down`.)

**Solution.** Projecting the $O(\lambda^2)$ equation onto $\langle\psi_n^0|$ and substituting
$|\psi_n^{(1)}\rangle=\sum_{m\neq n}\frac{\langle m|H'|n\rangle}{E_n^0-E_m^0}|m\rangle$ gives
$E_n^{(2)}=\sum_{m\neq n}|\langle m|H'|n\rangle|^2/(E_n^0-E_m^0)$. For $H'=x^2=\tfrac12(a+a^\dagger)^2$
the only off-diagonal links are $\langle n{+}2|x^2|n\rangle=\tfrac12\sqrt{(n{+}1)(n{+}2)}$ and
$\langle n{-}2|x^2|n\rangle=\tfrac12\sqrt{n(n{-}1)}$, with denominators $\mp2$:
$$E_n^{(2)}=\frac{\tfrac14(n{+}1)(n{+}2)}{-2}+\frac{\tfrac14 n(n{-}1)}{+2}=-\tfrac18(4n+2)=-\tfrac12\Big(n+\tfrac12\Big).$$
For $n=2$ this is $-1.25$. For the ground state every $E_m^0>E_0^0$ makes each denominator
negative while $|\langle m|H'|n\rangle|^2\ge0$, so $E_0^{(2)}\le0$ — the levels repel. Matches
`second_order_energy(...,ho_matrix_power(60,2),2)`→`-1.25`.

### P3.  The accuracy of perturbation theory — error scaling
Truncating after first order should be accurate to $O(\lambda^2)$, and through
second order to $O(\lambda^3)$. Verify the scaling against exact diagonalization
of $\operatorname{diag}(E^0)+\lambda H'$ (with $H'=x^2$) by halving $\lambda$.
*Answer:* the first-order error drops by $\approx4$ per halving (slope $\lambda^2$),
the through-second-order error by $\approx8$ (slope $\lambda^3$).
*Check:* compare `perturbed_energy(...,order=1)` and `order=2` to `exact_energy`
at $\lambda=0.04,0.02,0.01$. (`test_first_order_error_is_order_lambda_squared`,
`test_through_second_order_error_is_order_lambda_cubed`.)

**Solution.** The exact eigenvalue expands as
$E_n=E_n^0+\lambda E_n^{(1)}+\lambda^2 E_n^{(2)}+\lambda^3 E_n^{(3)}+\cdots$. Truncating after first
order leaves the remainder $\lambda^2 E_n^{(2)}+O(\lambda^3)=O(\lambda^2)$; through second order
leaves $\lambda^3 E_n^{(3)}+O(\lambda^4)=O(\lambda^3)$. So halving $\lambda$ should divide the
first-order error by $2^2=4$ and the through-second-order error by $2^3=8$. Diagonalizing
$\operatorname{diag}(E^0)+\lambda x^2$ exactly at $\lambda=0.04,0.02,0.01$ gives first-order errors
$\{3.85,0.98,0.25\}\times10^{-4}$ (ratios $\times3.9,\times4.0$) and through-second errors
$\{1.52,0.20,0.025\}\times10^{-5}$ (ratios $\times7.8,\times7.9$) — exactly the $O(\lambda^2)$ and
$O(\lambda^3)$ scalings the `test_*_error_is_order_lambda_*` checks assert.

### P4.  Charged oscillator in a field — PT is exact here  *(Griffiths 3e Problem 7.6, p.364)*
For $H=\tfrac{p^2}{2}+\tfrac12x^2+\lambda x$, find the exact spectrum and compare
to perturbation theory.
*Answer:* complete the square: $H=\tfrac{p^2}{2}+\tfrac12(x+\lambda)^2-\tfrac12
\lambda^2$, so $E_n=(n+\tfrac12)-\tfrac12\lambda^2$ exactly. PT gives
$E_n^{(1)}=0$, $E_n^{(2)}=-\tfrac12$, and all higher corrections vanish — so
through second order PT is *exact*.
*Check:* `perturbed_energy(ho_energies(60), ho_position(60), n, 0.3, order=2)`
$=(n+\tfrac12)-\tfrac12(0.3)^2$ to machine precision.
(`test_stark_perturbation_exact_through_second_order`.)

**Solution.** Complete the square: $H=\tfrac{p^2}{2}+\tfrac12(x+\lambda)^2-\tfrac12\lambda^2$ is a
harmonic oscillator recentred at $x=-\lambda$, so the *exact* spectrum is
$E_n=(n+\tfrac12)-\tfrac12\lambda^2$. Perturbatively, $H'=x$ gives $E_n^{(1)}=\langle n|x|n\rangle=0$
by parity, and only $m=n\pm1$ contribute to second order, with $|\langle n{\pm}1|x|n\rangle|^2=
\tfrac12(n{+}1),\tfrac12 n$ and denominators $\mp1$:
$$E_n^{(2)}=\frac{\tfrac12(n{+}1)}{-1}+\frac{\tfrac12 n}{+1}=-\tfrac12.$$
The shift $-\tfrac12\lambda^2$ is reproduced already at second order and every higher correction
vanishes (the square completes exactly), so PT is *exact* here. At $\lambda=0.3$,
$\tfrac12\lambda^2=0.045$, so `perturbed_energy(...,n,0.3,order=2)`$=(n+\tfrac12)-0.045$, i.e.
$0.455,1.455,2.455$ for $n=0,1,2$.

### P5.  Degenerate perturbation theory — diagonalize the block  *(Griffiths 3e §7.2.1, Eq. 7.30/7.33, p.370)*
Two states are degenerate at $E^0$. Why does ordinary PT fail, and what replaces
the first-order energy? Show the naive answer (diagonal matrix elements) is wrong
when the perturbation couples the two states.
*Answer:* ordinary PT divides by $E_n^0-E_m^0=0$. The first-order splittings are
the **eigenvalues of $H'$ in the degenerate subspace** ($W_{ij}=\langle i|H'|j
\rangle$); its eigenvectors are the "good" states. With an off-diagonal $W_{01}
\neq0$, the eigenvalues lie *outside* $\{W_{00},W_{11}\}$ (interlacing), so the
diagonal entries are not the splittings.
*Check:* for the $W=\begin{psmallmatrix}0.3&0.4\\0.4&-0.2\end{psmallmatrix}$ block,
`degenerate_first_order_split(Hp,[0,1])` → `[-0.422, 0.522]`, matching
$(E^{\text{exact}}-E^0)/\lambda$ as $\lambda\to0$, while the diagonal gives
$[-0.2,0.3]$. (`test_degenerate_split_equals_subspace_eigenvalues`,
`test_naive_nondegenerate_answer_is_wrong`.)

**Solution.** Ordinary PT puts $E_n^0-E_m^0=0$ in the denominator for the two degenerate states,
so it diverges; the cure is that $H'$ itself selects the "good" zeroth-order states. Projecting
the $O(\lambda)$ equation into the degenerate subspace turns the first-order problem into the
eigenvalue equation $\det(W-E^{(1)}\mathbb 1)=0$ with $W_{ij}=\langle i|H'|j\rangle$. For
$W=\begin{pmatrix}0.3&0.4\\0.4&-0.2\end{pmatrix}$,
$$E^{(1)}=\frac{0.3-0.2}{2}\pm\sqrt{\Big(\frac{0.3+0.2}{2}\Big)^2+0.4^2}=0.05\pm0.4717=\{-0.4217,\,0.5217\}.$$
The off-diagonal $0.4$ pushes the eigenvalues *outside* the diagonal pair $\{W_{00},W_{11}\}=
\{0.3,-0.2\}$ (eigenvalue interlacing), so the naive answer $[-0.2,0.3]$ is wrong.
`degenerate_first_order_split(Hp,[0,1])`→`[-0.422, 0.522]` matches $(E^{\text{exact}}-E^0)/\lambda$
as $\lambda\to0$.

### P6.  The variational principle as an upper bound  *(Griffiths 3e §8.1, Eq. 8.1, p.418; Example 8.1, p.419)*
Prove $\langle H\rangle_\psi\ge E_{gs}$ for any normalized $\psi$. Then minimize a
Gaussian trial $\psi_b=(2b/\pi)^{1/4}e^{-bx^2}$ on the oscillator and explain why
the bound is hit exactly.
*Answer:* expand $\psi=\sum c_n\psi_n$; $\langle H\rangle=\sum|c_n|^2E_n\ge
E_{gs}$. For the oscillator $\langle H\rangle(b)=b/2+1/(8b)$, minimized at
$b=\tfrac12$ giving $\langle H\rangle=\tfrac12=E_0$ — exact, because the Gaussian
family contains the true ground state.
*Check:* `gaussian_variational_min(lambda t: 0.5*t**2, x)` → `(0.5, 0.5)`.
(`test_variational_gaussian_recovers_oscillator_exactly`.)

**Solution.** Expand any normalized trial state in the (unknown) energy eigenbasis,
$\psi=\sum_n c_n\psi_n$ with $\sum_n|c_n|^2=1$; then
$\langle H\rangle=\sum_n|c_n|^2E_n\ge E_{gs}\sum_n|c_n|^2=E_{gs}$ since every $E_n\ge E_{gs}$,
with equality only for $\psi=\psi_{gs}$. For the Gaussian on $V=\tfrac12 x^2$,
$$\langle H\rangle(b)=\frac{b}{2}+\frac{1}{8b},\qquad
\frac{d\langle H\rangle}{db}=\frac12-\frac{1}{8b^2}=0\ \Rightarrow\ b=\tfrac12,\quad
\langle H\rangle_{\min}=\tfrac14+\tfrac14=\tfrac12.$$
The bound is saturated because at $b=\tfrac12$ the trial $\psi_b\propto e^{-x^2/2}$ *is* the exact
ground state $\psi_0$. Hence `gaussian_variational_min(lambda t: 0.5*t**2, x)`→`(0.5, 0.5)`:
minimum energy $0.5=E_0$ at width $b=0.5$.

### P7.  Gaussian bound on the quartic well  *(Griffiths 3e Problem 8.1(b), p.422)*
Use a Gaussian trial to bound the ground-state energy of $V=\tfrac14x^4$. Is the
bound exact? By how much does it exceed the truth?
*Answer:* minimizing gives $\langle H\rangle_{\min}\approx0.4293$, which lies
$\approx2\%$ **above** the exact $E_{gs}\approx0.4208$ (finite-difference) — a
genuine, non-saturated upper bound (the Gaussian is not the true quartic ground
state). The inequality holds at *every* width $b$, not just the optimum.
*Check:* `gaussian_variational_min(lambda t: 0.25*t**4, x)[0]` $\ge$
`fd_ground_energy(lambda t: 0.25*t**4, ...)`.
(`test_variational_quartic_bound_is_tight_but_above`, `test_variational_is_an_upper_bound`.)

**Solution.** For the Gaussian, $\langle T\rangle=\tfrac{\hbar^2 b}{2m}=\tfrac{b}{2}$ and
$\langle x^4\rangle=3\langle x^2\rangle^2=3/(16b^2)$, so on $V=\tfrac14 x^4$
$$\langle H\rangle(b)=\frac{b}{2}+\frac{3}{64b^2},\qquad
\frac{d\langle H\rangle}{db}=\frac12-\frac{3}{32b^3}=0\ \Rightarrow\ b=\Big(\tfrac{3}{16}\Big)^{1/3}\approx0.572,$$
giving $\langle H\rangle_{\min}\approx0.4293$. Unlike the oscillator the Gaussian is *not* the true
quartic ground state, so this is a strict over-estimate: the finite-difference truth is
$E_{gs}\approx0.4208$, about $2\%$ below ($0.4293\ge0.4208$). The inequality in fact holds at every
width $b$. So `gaussian_variational_min(lambda t: 0.25*t**4, x)[0]`$=0.4293\ge$
`fd_ground_energy(...)`$=0.4208$.

### P8.  WKB: Bohr–Sommerfeld and the harmonic oscillator  *(Griffiths 3e §9.3, Eq. 9.50, p.465)*
Apply $\int_{x_1}^{x_2}p\,dx=(n+\tfrac12)\pi\hbar$ to $V=\tfrac12\omega^2x^2$.
Why is WKB *exact* here but only approximate for $V=\tfrac14x^4$?
*Answer:* the oscillator action is $\int_{-x_0}^{x_0}\sqrt{2(E-\tfrac12x^2)}\,dx
=\pi E/\omega$, so $\pi E/\omega=(n+\tfrac12)\pi\Rightarrow E_n=n+\tfrac12$ —
exact. WKB drops the $A''/A$ term, which vanishes identically for the oscillator
but not for the quartic; there the error is $O(1/n)$ (18% at $n=0$, $<1\%$ by
$n=2$) — WKB is a semiclassical (large-$n$) method.
*Check:* `bohr_sommerfeld_energy(lambda t:0.5*t**2, n, -80, 80)` → `n+0.5`
exactly; the quartic errors shrink with $n$.
(`test_wkb_recovers_oscillator_exactly`, `test_wkb_quartic_improves_with_quantum_number`.)

**Solution.** With $p=\sqrt{2(E-\tfrac12 x^2)}$ the turning points are $x_0=\pm\sqrt{2E}$ and the
action is the area of a momentum ellipse,
$$\int_{-x_0}^{x_0}\sqrt{2E-x^2}\,dx=\pi E=\Big(n+\tfrac12\Big)\pi\hbar\ \Rightarrow\ E_n=n+\tfrac12,$$
exactly the oscillator spectrum. WKB drops the $A''/A$ term; for the quadratic potential this does
not disturb the quantization condition (the result is exact), but for $V=\tfrac14 x^4$ it does,
leaving an $O(1/n)$ semiclassical error. Numerically
`bohr_sommerfeld_energy(lambda t:0.5*t**2, n, -80, 80)` returns $0.5,1.5,2.5,3.5$ (exact), while the
quartic error falls from $18\%$ at $n=0$ to $1.3\%$ ($n=1$) and $0.6\%$ ($n=2$) — WKB is a
large-$n$ method.

### P9.  WKB tunnelling vs the exact barrier  *(Griffiths 3e §9.2, Eq. 9.22–9.23, p.455; cf. ~QM-08)*
For a rectangular barrier ($V_0>E$, width $a$) compute the WKB transmission and
compare to QM-08's exact result. What do they share, and where do they differ?
*Answer:* $T_{\text{WKB}}=e^{-2\kappa a}$, $\kappa=\sqrt{2m(V_0-E)}/\hbar$. The
exact $T=[1+\tfrac{V_0^2\sinh^2\kappa a}{4E(V_0-E)}]^{-1}\to\tfrac{16E(V_0-E)}{V_0^2}
e^{-2\kappa a}$ for a thick barrier: **same exponent**, the ratio
$T_{\text{exact}}/T_{\text{WKB}}\to16E(V_0-E)/V_0^2$ is constant in $a$. WKB
captures the dominant exponential and misses only the $O(1)$ prefactor (this is
the engine of Gamow's alpha-decay law, Example 9.2).
*Check:* `tunneling_rectangular(2,10,a)` vs `transmission_barrier(2,10,a)` (from
`~QM-08`): the ratio is $2.56=16\cdot2\cdot8/100$ for all thick $a$.
(`test_wkb_tunneling_shares_exact_exponent`.)

**Solution.** In the forbidden region the momentum magnitude is constant,
$|p|=\sqrt{2m(V_0-E)}\equiv\hbar\kappa$ with $\kappa=\sqrt{2(V_0-E)}=4$ here, so $\gamma=\kappa a$ and
$T_{\text{WKB}}=e^{-2\kappa a}$. QM-08's exact $T=[1+\tfrac{V_0^2\sinh^2\kappa a}{4E(V_0-E)}]^{-1}$
uses $\sinh\kappa a\to\tfrac12 e^{\kappa a}$ for a thick barrier, giving
$$T_{\text{exact}}\to\frac{16E(V_0-E)}{V_0^2}\,e^{-2\kappa a},\qquad
\frac{T_{\text{exact}}}{T_{\text{WKB}}}\to\frac{16E(V_0-E)}{V_0^2}=\frac{16\cdot2\cdot8}{100}=2.56.$$
Both decay with the *same* exponent $e^{-2\kappa a}$; WKB misses only the constant $O(1)$ prefactor.
`tunneling_rectangular(2,10,a)` and `transmission_barrier(2,10,a)` give ratio $2.56000$ for all
thick $a$ ($a=3,5,8$) — the exponent that powers Gamow's alpha-decay law.
