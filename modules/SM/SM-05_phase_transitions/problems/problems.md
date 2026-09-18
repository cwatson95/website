# SM-05 — Problems

Work by hand, then check with `code/phase_transitions.py`. Citations in
`../refs.md`; **Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  The Weiss self-consistency  *(Pa §12.5, p.420)*
Derive m = tanh[(T_c/T)m + b] from the mean-field energy, and show T_c = qJ/k by
linearizing at small m. *Check:* `critical_temperature(4, J)` = 4J/k;
`mean_field_residual(spontaneous_magnetization(T,Tc), T, Tc)` ≈ 0.

*Answer:* Replacing each neighbor by $m$ puts a spin in field $h_{\rm eff}=qJm+\mu B$, whose Boltzmann average $\tanh(\beta h_{\rm eff})$ must equal $m$: $m=\tanh[(T_c/T)m+b]$ with $T_c=qJ/k$, $b=\mu B/kT$. Linearizing fixes the onset at $T_c$.

**Solution.** Mean-field theory replaces each of the $q$ neighbors of a spin $s_i$ by the average $\langle s\rangle=m$, so $-J\sum_{\langle ij\rangle}s_is_j$ acting on $s_i$ becomes an effective field $h_{\rm eff}=qJm+\mu B$. A single Ising spin in that field has
$$m=\langle s\rangle=\frac{\sum_{s=\pm1}s\,e^{\beta h_{\rm eff}s}}{\sum_{s=\pm1}e^{\beta h_{\rm eff}s}}=\frac{e^{\beta h_{\rm eff}}-e^{-\beta h_{\rm eff}}}{e^{\beta h_{\rm eff}}+e^{-\beta h_{\rm eff}}}=\tanh(\beta h_{\rm eff}).$$
Self-consistency gives $m=\tanh[(T_c/T)m+b]$ with $T_c\equiv qJ/k$ and $b\equiv\mu B/kT$. At $b=0$ and small $m$, $\tanh u\approx u$ gives $m\approx(T_c/T)m$; a nonzero branch can appear only when the slope reaches $1$, i.e. $T=T_c=qJ/k$. Tie to check: `critical_temperature(4, J)` $=4J/k$, and `mean_field_residual` at the solved $m$ is $\approx0$.

### P2.  Spontaneous magnetization  *(Pa §12.5, p.420)*
Show that m = tanh[(T_c/T)m] has only the trivial root for T > T_c but a nonzero root
for T < T_c, and that m → 1 as T → 0. *Check:* `spontaneous_magnetization(330,300)=0`,
`spontaneous_magnetization(150,300)≈0.957`, `spontaneous_magnetization(5,300)>0.99`.

*Answer:* $m=\tanh(am)$, $a=T_c/T$: for $a\le1$ ($T\ge T_c$) only $m=0$; for $a>1$ ($T<T_c$) the curve starts above the line $y=m$ and recrosses at $0<m_*<1$. As $T\to0$, $a\to\infty$ and $\tanh$ saturates, so $m\to1$.

**Solution.** Solve $m=\tanh(am)$, $a=T_c/T$, by intersecting the line $y=m$ with the curve $y=\tanh(am)$. Both pass through the origin, where the curve has slope $a$. For $a\le1$ ($T\ge T_c$) the curve starts no steeper than the line and, being concave for $m>0$, stays below it — so $m=0$ is the only root. For $a>1$ ($T<T_c$) the curve leaves the origin steeper than the line yet is bounded by $1$, so it must bend back and cross $y=m$ again at some
$$0<m_*<1,$$
the spontaneous magnetization. As $T\to0$, $a=T_c/T\to\infty$ and $\tanh(am)\to1$ for any fixed $m>0$, forcing saturation:
$$m=\tanh\!\Big(\frac{T_c}{T}\,m\Big)\;\xrightarrow{\,T\to0\,}\;1.$$
Tie to check: `spontaneous_magnetization(330,300)` $=0$ (paramagnet), `(150,300)` $\approx0.957$, and `(5,300)` $>0.99\to1$.

### P3.  The critical exponent β = ½  *(Pa §12.7, p.435)*
Expand tanh near T_c to show m ≈ √3 (1 − T/T_c)^{1/2}, hence β = ½. *Check:*
`critical_exponent_beta(Tc, "meanfield")` ≈ 0.5 (log–log slope).

*Answer:* With $\tanh u\approx u-u^3/3$ and $u=am$ ($a=T_c/T$), $m=\tanh(am)$ gives $m^2=3(a-1)/a^3$; as $T\to T_c^-$, $a\to1$ so $m\simeq\sqrt3\,(1-T/T_c)^{1/2}$, hence $\beta=\tfrac12$.

**Solution.** Near $T_c$ the magnetization is small, so expand $m=\tanh(am)$, $a=T_c/T$, using $\tanh u=u-\tfrac13u^3+\cdots$:
$$m=am-\tfrac13(am)^3+\cdots\ \Longrightarrow\ 1=a-\tfrac13a^3m^2\ \Longrightarrow\ m^2=\frac{3(a-1)}{a^3}.$$
Just below $T_c$, $a=T_c/T\to1^+$, so $a^3\to1$ and $a-1=\dfrac{T_c-T}{T}\approx\dfrac{T_c-T}{T_c}=1-\dfrac{T}{T_c}$. Therefore
$$m\simeq\sqrt3\,\Big(1-\frac{T}{T_c}\Big)^{1/2}\sim(T_c-T)^{1/2},$$
so the order-parameter exponent in $m\sim(T_c-T)^{\beta}$ is $\beta=\tfrac12$ (mean field). Tie to check: `critical_exponent_beta(Tc, "meanfield")` $\approx0.5$, read off as the log–log slope of $m$ vs $(T_c-T)$.

### P4.  No order in 1-D  *(Pa §13.2, p.476)*
From the transfer-matrix result m = sinh(βh)/√(sinh²(βh)+e^{−4βJ}), show m = 0 at
h = 0 for all T > 0 — the 1-D chain never spontaneously magnetizes. *Check:*
`ising_1d_magnetization(T, J, 0)` = 0 at T = 10, 100, 500 K; nonzero with a field.

*Answer:* At $h=0$, $\sinh(\beta h)=0$ kills the numerator while the denominator $\to\sqrt{e^{-4\beta J}}=e^{-2\beta J}>0$ at any finite $T$; so $m=0$ for all $T>0$. Order needs $T=0$ ($\beta\to\infty$) or $h\neq0$.

**Solution.** The exact transfer-matrix magnetization per spin is
$$m=\frac{\sinh(\beta h)}{\sqrt{\sinh^2(\beta h)+e^{-4\beta J}}},\qquad\beta=\frac{1}{kT}.$$
Switch off the field: $\sinh(\beta\cdot0)=0$, so the numerator vanishes, while the denominator becomes $\sqrt{0+e^{-4\beta J}}=e^{-2\beta J}$, strictly positive for every finite $T$ (finite $\beta$). Hence
$$m\big|_{h=0}=\frac{0}{e^{-2\beta J}}=0\qquad\text{for all }T>0,$$
no spontaneous magnetization — thermal fluctuations destroy long-range order in one dimension. Order sets in only as $T\to0$ ($\beta\to\infty$, $e^{-2\beta J}\to0$) or when a field $h\neq0$ makes $\sinh(\beta h)>0$. Tie to check: `ising_1d_magnetization(T, J, 0)` $=0$ at $T=10,100,500$ K, but nonzero once a field is applied.

### P5.  Landau double well  *(Pa §12.10, p.442)*
Minimize F = a(T−T_c)m² + bm⁴ to find m₀ = √(a(T_c−T)/2b) for T < T_c and m₀ = 0
above, and show m₀ ~ (T_c−T)^{1/2}. *Check:* below T_c `landau_free_energy(m0,…)` <
`landau_free_energy(0,…)`; doubling (T_c−T) scales m₀ by √2.

*Answer:* $\partial F/\partial m=2a(T-T_c)m+4bm^3=0$ gives $m=0$ or $m_0^2=a(T_c-T)/2b$; for $T<T_c$ the nonzero root is the minimum, $m_0=\sqrt{a(T_c-T)/2b}\sim(T_c-T)^{1/2}$ ($\beta=\tfrac12$); for $T\ge T_c$ only $m=0$.

**Solution.** Minimize $F(m)=a(T-T_c)m^2+bm^4$ ($a,b>0$):
$$\frac{\partial F}{\partial m}=2a(T-T_c)m+4bm^3=2m\big[a(T-T_c)+2bm^2\big]=0.$$
The roots are $m=0$ and $m^2=\dfrac{a(T_c-T)}{2b}$. For $T>T_c$ the bracket is positive for all $m$, so $m=0$ is the only extremum — a single well. For $T<T_c$ the factor $T_c-T>0$ makes a real pair appear,
$$m_0=\pm\sqrt{\frac{a(T_c-T)}{2b}}\sim(T_c-T)^{1/2},$$
the double-well minima; meanwhile $m=0$ becomes a maximum since $\partial^2F/\partial m^2\big|_0=2a(T-T_c)<0$. The exponent is again $\beta=\tfrac12$. Tie to check: below $T_c$, `landau_free_energy(m0,…)` $<$ `landau_free_energy(0,…)`, and since $m_0\propto\sqrt{T_c-T}$, doubling $(T_c-T)$ scales $m_0$ by $\sqrt2$.
