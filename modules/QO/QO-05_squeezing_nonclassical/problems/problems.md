# QO-05 — Problems

Work each by hand, then check with `code/squeezing.py`. Citations in `../refs.md`;
**SZ** = Scully & Zubairy, *Quantum Optics* (Ch. 2–3, 16, 18), cited at
section/chapter level. Units $\hbar=1$; $X_1=(a+a^\dagger)/2$,
$X_2=(a-a^\dagger)/2i$; squeeze parameter $\xi=r e^{i\phi}$.

### P1.  Quadratures and the standard quantum limit  *(SZ §2.7.1)*
From $[a,a^\dagger]=1$, show the two quadratures obey $[X_1,X_2]=\tfrac{i}{2}$,
so the Robertson uncertainty relation gives
$\operatorname{Var}X_1\,\operatorname{Var}X_2\ge\tfrac1{16}$. Show the vacuum
$|0\rangle$ saturates it with $\operatorname{Var}X_1=\operatorname{Var}X_2=\tfrac14$
(use $a|0\rangle=0$ and $\langle0|aa^\dagger|0\rangle=1$). Why does every coherent
state have the *same* variances? *Check:*
`quadrature_variances(vacuum_state())` → `(0.25, 0.25)` and
`quadrature_variances(coherent_state(1.5))` → `(0.25, 0.25)`, product
$=\tfrac1{16}=0.0625$; the interior of $[X_1,X_2]$ is $\tfrac{i}{2}$
(`test_quadrature_commutator_is_i_over_two`).

**Solution.** With $X_1=\tfrac12(a+a^\dagger)$ and $X_2=\tfrac1{2i}(a-a^\dagger)$,
$$[X_1,X_2]=\tfrac1{4i}\,[\,a+a^\dagger,\ a-a^\dagger\,]=\tfrac1{4i}\big(-[a,a^\dagger]+[a^\dagger,a]\big)=\tfrac1{4i}(-2)=\tfrac{i}{2}.$$
Robertson then gives $\operatorname{Var}X_1\operatorname{Var}X_2\ge\tfrac14\big|\langle[X_1,X_2]\rangle\big|^2=\tfrac14\cdot\tfrac14=\tfrac1{16}$. On the vacuum $a|0\rangle=0$, so $\langle X_1\rangle=\langle X_2\rangle=0$ and only the $aa^\dagger$ term survives, $\langle0|X_1^2|0\rangle=\tfrac14\langle0|aa^\dagger|0\rangle=\tfrac14$, and likewise $\langle X_2^2\rangle=\tfrac14$ — the bound is saturated. A coherent state is $|\alpha\rangle=D(\alpha)|0\rangle$ with $D^\dagger aD=a+\alpha$, a c-number shift that leaves the fluctuation operator $a-\langle a\rangle$ untouched, so every coherent state inherits the vacuum's $\operatorname{Var}X_1=\operatorname{Var}X_2=\tfrac14$. Matches `quadrature_variances(vacuum_state())`→`(0.25, 0.25)` and `coherent_state(1.5)`→`(0.25, 0.25)`, product $\tfrac1{16}=0.0625$, with the $[X_1,X_2]$ interior $\tfrac{i}{2}$.

### P2.  The squeeze operator and the Bogoliubov transformation  *(SZ §2.7)*
For $S(\xi)=\exp[\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})]$, use the Hadamard lemma
$S^\dagger a S=a+[a,M]+\tfrac1{2!}[[a,M],M]+\dots$ with
$M=\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})$ to prove
$$S^\dagger(\xi)\,a\,S(\xi)=a\cosh r-a^\dagger e^{i\phi}\sinh r .$$
(The series resums to $\cosh$/$\sinh$ because $[a,M]\propto a^\dagger$ and
$[a^\dagger,M]\propto a$ close on each other.) Confirm $S$ is unitary because its
generator $M$ is anti-Hermitian. *Check:* `squeeze_operator(0.9, 40, phi=0.7)`
satisfies $S^\dagger S=\mathbb{1}$ to $10^{-9}$, and `squeeze_operator(0.0, N)` is
the identity (`test_squeeze_operator_zero_is_identity_and_unitary`).

**Solution.** With $M=\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})$ the first nested commutator is
$$[a,M]=-\tfrac{\xi}{2}\,[a,a^{\dagger2}]=-\tfrac{\xi}{2}\,(2a^\dagger)=-\xi\,a^\dagger,$$
and feeding it back, $[\,[a,M],M\,]=-\xi\,[a^\dagger,M]=-\xi\big(-\xi^{*}a\big)=|\xi|^2a=r^2a$. The two commutators map $a\!\to\!a^\dagger\!\to\!a$, so the Hadamard series closes: even orders rebuild $a$, odd orders $a^\dagger$,
$$S^\dagger aS=a\Big(1+\tfrac{r^2}{2!}+\cdots\Big)-\xi a^\dagger\Big(1+\tfrac{r^2}{3!}+\cdots\Big)=a\cosh r-a^\dagger\,\frac{\xi}{r}\sinh r,$$
and $\xi/r=e^{i\phi}$ gives $S^\dagger aS=a\cosh r-a^\dagger e^{i\phi}\sinh r$. Finally $M^\dagger=\tfrac12(\xi a^{\dagger2}-\xi^{*}a^2)=-M$, so $M$ is anti-Hermitian and $S=e^{M}$ is unitary. This is what `squeeze_operator(0.9, 40, phi=0.7)` confirms, $S^\dagger S=\mathbb1$ to $10^{-9}$, with `squeeze_operator(0.0, N)`$=\mathbb1$.

### P3.  Squeezed-vacuum variances, the minimum-uncertainty product, and dB  *(SZ §2.7.1)*
Using P2 with $\phi=0$, show $S^\dagger X_1 S=X_1 e^{-r}$ and
$S^\dagger X_2 S=X_2 e^{+r}$, hence for $|\xi\rangle=S|0\rangle$
$$\operatorname{Var}X_1=\tfrac14 e^{-2r},\quad
\operatorname{Var}X_2=\tfrac14 e^{+2r},\quad
\operatorname{Var}X_1\operatorname{Var}X_2=\tfrac1{16}.$$
Which quadrature is squeezed, and what does $\phi$ do? Express the squeezing of
$X_1$ in decibels, $10\log_{10}(\operatorname{Var}X_1/\tfrac14)=-8.686\,r$ dB.
*Check:* `quadrature_variances(squeezed_vacuum(0.6))` ≈ `(0.0753, 0.830)`, product
`0.0625`; at $r=0.6$ that is $-5.2$ dB. `squeezed_vacuum(0.7, phi=pi)` swaps the
two (`test_phi_rotates_the_squeezed_quadrature`).

**Solution.** Take $\phi=0$, so P2 gives $S^\dagger aS=a\cosh r-a^\dagger\sinh r$ and (adjoint) $S^\dagger a^\dagger S=a^\dagger\cosh r-a\sinh r$. Adding and subtracting,
$$S^\dagger X_1S=\tfrac12\big(S^\dagger aS+S^\dagger a^\dagger S\big)=X_1(\cosh r-\sinh r)=X_1e^{-r},\qquad S^\dagger X_2S=X_2e^{+r}.$$
Since $|\xi\rangle=S|0\rangle$, $\operatorname{Var}_{|\xi\rangle}X_1=\langle0|(S^\dagger X_1S)^2|0\rangle-\langle0|S^\dagger X_1S|0\rangle^2=e^{-2r}\operatorname{Var}_0X_1=\tfrac14e^{-2r}$, and likewise $\operatorname{Var}X_2=\tfrac14e^{+2r}$, product $\tfrac1{16}$. So $X_1$ (for $\phi=0$) is the squeezed quadrature, dropping below $\tfrac14$; a general $\phi$ rotates the squeezed direction by $\phi/2$ in phase space, and $\phi=\pi$ swaps $X_1\leftrightarrow X_2$. In decibels $10\log_{10}(\operatorname{Var}X_1/\tfrac14)=10\log_{10}e^{-2r}=-8.686\,r$. At $r=0.6$ this is `quadrature_variances(squeezed_vacuum(0.6))`$\approx(0.0753,0.830)$, product $0.0625$, i.e. $-5.2$ dB; `squeezed_vacuum(0.7, phi=pi)` swaps the two.

### P4.  Photon pairs: even-only statistics and $\langle n\rangle=\sinh^2 r$  *(SZ §2.7)*
Argue from the structure of $S$ (it only changes the photon number by $\pm2$) that
$|\xi\rangle$ contains **only even** Fock states, and derive
$$P(2m)=\frac{1}{\cosh r}\,\frac{(2m)!}{(2^{m}m!)^{2}}(\tanh r)^{2m},\qquad
\langle n\rangle=\langle\xi|a^\dagger a|\xi\rangle=\sinh^2 r .$$
(Hint for $\langle n\rangle$: conjugate $a^\dagger a$ with $S$ using P2.) *Check:*
`photon_distribution(squeezed_vacuum(0.8))` has odd-$n$ sum $\sim10^{-17}$ and
$P(0)=1/\cosh 0.8=0.748$; `mean_photon_number(squeezed_vacuum(r))` $=$
`mean_photon(r)` $=\sinh^2 r$ for every $r$ (e.g. $0.789$ at $r=0.8$)
(`test_only_even_photon_numbers_populated`, `test_mean_photon_is_sinh_squared_r`).

**Solution.** The generator $M=\tfrac12(\xi^{*}a^2-\xi a^{\dagger2})$ moves population only in steps of $\pm2$ (the $a^2$ and $a^{\dagger2}$ pieces), so acting on the even state $|0\rangle$ it never reaches an odd $|n\rangle$: $P(2m+1)=0$. The disentangled form $|\xi\rangle=\tfrac1{\sqrt{\cosh r}}\sum_m\tfrac{\sqrt{(2m)!}}{2^mm!}(-e^{i\phi}\tanh r)^m|2m\rangle$ squares to
$$P(2m)=\frac{1}{\cosh r}\,\frac{(2m)!}{(2^mm!)^2}(\tanh r)^{2m}.$$
For the mean, conjugate with $S$ ($\phi=0$): $\langle n\rangle=\langle0|(S^\dagger a^\dagger S)(S^\dagger aS)|0\rangle$, and with $S^\dagger aS=a\cosh r-a^\dagger\sinh r$ only the $\sinh^2 r$ term survives the vacuum sandwich,
$$\langle n\rangle=\sinh^2 r\,\langle0|aa^\dagger|0\rangle=\sinh^2 r.$$
Hence `photon_distribution(squeezed_vacuum(0.8))` has odd-$n$ sum $\sim10^{-17}$ and $P(0)=1/\cosh0.8=0.748$, while `mean_photon_number`$=$`mean_photon(r)`$=\sinh^2 r$ (e.g. $0.789$ at $r=0.8$).

### P5.  Nonclassicality is not one thing: $g^{(2)}(0)$ vs. squeezing  *(SZ §4.4.4)*
Compute $g^{(2)}(0)=\langle a^\dagger a^\dagger a a\rangle/\langle a^\dagger a\rangle^2$
for (a) a Fock state $|1\rangle$, (b) a coherent state, (c) the squeezed vacuum.
Show $|1\rangle$ gives $g^{(2)}(0)=0$ (antibunched, $Q=-1$), coherent gives $1$
($Q=0$), and squeezed vacuum gives $g^{(2)}(0)=3+1/\sinh^2 r>1$ (super-Poissonian,
$Q>0$). Conclude that the squeezed vacuum is nonclassical (sub-SQL quadrature) yet
**not** antibunched — squeezing and sub-Poissonian statistics are independent.
*Check:* `g2_zero(fock_state(1))` → `0.0`, `g2_zero(coherent_state(2.0))` → `1.0`,
`g2_zero(squeezed_vacuum(0.8))` → `4.268` $=3+1/\sinh^2 0.8$; `mandel_q` returns
$-1$, $0$, $+2.58$ respectively (`test_g2_and_mandel_classify_states`).

**Solution.** Use $g^{(2)}(0)=\langle a^\dagger a^\dagger aa\rangle/\langle a^\dagger a\rangle^2=\langle n(n-1)\rangle/\langle n\rangle^2$. For $|1\rangle$, $n=1$ so $n(n-1)=0$ and $g^{(2)}(0)=0$ (perfectly antibunched), with $Q=\langle n\rangle(g^{(2)}(0)-1)=-1$. For a coherent state $a|\alpha\rangle=\alpha|\alpha\rangle$ gives $\langle a^\dagger a^\dagger aa\rangle=|\alpha|^4=\langle n\rangle^2$, so $g^{(2)}(0)=1$ and $Q=0$. For the squeezed vacuum the even-pair statistics give $\operatorname{Var}n=2\sinh^2 r\cosh^2 r$ on top of $\langle n\rangle=\sinh^2 r$, so
$$g^{(2)}(0)=1+\frac{\operatorname{Var}n-\langle n\rangle}{\langle n\rangle^2}=1+\frac{2\cosh^2 r-1}{\sinh^2 r}=3+\frac{1}{\sinh^2 r}>1,$$
with $Q=2\cosh^2 r-1=\cosh 2r>0$ — super-Poissonian. So a state can be quadrature-squeezed (sub-SQL) yet bunched: the two nonclassicalities are independent. Matches `g2_zero`→`0.0`, `1.0`, `4.268`$=3+1/\sinh^2 0.8$ and `mandel_q`→$-1,\,0,\,+2.58$.

### P6.  Two-mode squeezing and the EPR correlation  *(SZ Ch. 16, 18)*
For $S_2(\xi)=\exp(\xi^{*}ab-\xi a^\dagger b^\dagger)$, show
$S_2|0,0\rangle=\operatorname{sech}r\sum_n(-e^{i\phi}\tanh r)^n|n,n\rangle$, so the
two modes are perfectly **photon-number correlated** with per-mode
$\langle n\rangle=\sinh^2 r$. Then prove the joint quadratures beat the
vacuum/separable bound,
$$\operatorname{Var}(X_a+X_b)=\operatorname{Var}(Y_a-Y_b)=\tfrac12 e^{-2r}<\tfrac12,$$
and explain how the $r\to\infty$ limit realizes the EPR "elements of reality" for
the non-commuting $X$ and $Y$ (`~QM-21`); this is the entangled-photon state made
by parametric down-conversion (`~QO-06`). *Check:*
`two_mode_photon_distribution(two_mode_squeezed_vacuum(0.6))` is diagonal with
$P(n,n)=(\tanh^2 0.6)^n/\cosh^2 0.6$; `epr_variances(0.6)` → `(0.151, 0.151)`,
both $<0.5=\tfrac12 e^{-2\cdot0.6}$ (`test_two_mode_is_photon_number_correlated`,
`test_epr_joint_quadratures_beat_the_sql`).

**Solution.** $S_2=\exp(\xi^{*}ab-\xi a^\dagger b^\dagger)$ has a generator that adds or removes one photon in *each* mode at once ($ab$ and $a^\dagger b^\dagger$), so from $|0,0\rangle$ it stays on the diagonal $|n,n\rangle$; the disentangling theorem resums this to
$$S_2|0,0\rangle=\operatorname{sech} r\sum_{n}(-e^{i\phi}\tanh r)^n|n,n\rangle,\qquad P(n,n)=\frac{(\tanh^2 r)^n}{\cosh^2 r}.$$
The geometric marginal gives $\langle n_a\rangle=\langle n_b\rangle=\sinh^2 r$, with $n_a=n_b$ always (perfect number correlation). With $\phi=0$ the two-mode Bogoliubov rule $S_2^\dagger aS_2=a\cosh r-b^\dagger\sinh r$ (and $a\!\leftrightarrow\! b$) yields $S_2^\dagger(X_a+X_b)S_2=(X_a+X_b)e^{-r}$, so
$$\operatorname{Var}(X_a+X_b)=e^{-2r}\operatorname{Var}_{0,0}(X_a+X_b)=\tfrac12e^{-2r}<\tfrac12,$$
and identically for $Y_a-Y_b$. As $r\to\infty$ both $\to0$: $X_a+X_b$ and $Y_a-Y_b$ become simultaneously sharp even though $[X,Y]\neq0$ per mode — the EPR "elements of reality." Confirmed by `two_mode_photon_distribution(...)` being diagonal with $P(n,n)=(\tanh^2 0.6)^n/\cosh^2 0.6$, and `epr_variances(0.6)`→`(0.151, 0.151)`, both $<0.5=\tfrac12 e^{-2\cdot0.6}$.
