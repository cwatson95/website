# MA-15 — Problems

Work by hand, then check with `code/dirac_delta.py`. Citations in `../refs.md`.

### P1.  Nascent sequences and sifting  *(Boas 3e §11, p.449)*
Show each of (1/(a√π))e^{−(x/a)²}, (a/π)/(x²+a²), and the box (1/a)·1_{|x|<a/2}
integrates to 1, and that ∫δ_a(x−x₀)φ(x)dx→φ(x₀) as a→0. Which converges fastest,
and why does the Lorentzian lag? (Heavy tails — no finite second moment.)
*Check:* `sift(phi, 1.2, "gaussian", a)` for shrinking a.

**Solution.** Each integrates to $1$: with $u=x/a$,
$\int\frac{1}{a\sqrt\pi}e^{-(x/a)^2}dx=\frac1{\sqrt\pi}\int e^{-u^2}du=1$;
$\int\frac{a/\pi}{x^2+a^2}dx=\frac1\pi\big[\arctan(x/a)\big]_{-\infty}^{\infty}=1$;
and $\int\frac1a\mathbf 1_{|x|<a/2}\,dx=\frac1a\cdot a=1$. As $a\to0$ each spike concentrates at
$x_0$, so $\int\delta_a(x-x_0)\phi(x)\,dx\to\phi(x_0)$. The Gaussian converges fastest (its
$e^{-u^2}$ tail is negligible), while the Lorentzian lags — its $1/x^2$ tail has no finite second
moment, so distant regions still contribute. For $\phi(1.2)=0.564997$, at $a=0.01$ the gaussian
gives $0.564967$ and the box $0.564992$, but the lorentzian only $0.557379$.

### P2.  The derivative δ′  *(Boas 3e §11, p.449)*
By parts, ⟨δ′,φ⟩=−⟨δ,φ′⟩=−φ′(0). Verify with φ=e^{−x} (answer +1) and φ=sin 2x
(answer −2). *Check:* `delta_prime_sift(lambda x: math.exp(-x), 0.03)` ≈ 1.

**Solution.** Integrate by parts, the boundary term vanishing because $\delta$ has compact
support:
$$\langle\delta',\phi\rangle=\int\delta'(x)\phi(x)\,dx=-\int\delta(x)\phi'(x)\,dx=-\phi'(0).$$
For $\phi=e^{-x}$, $\phi'(0)=-1$, so the answer is $-\phi'(0)=+1$; for $\phi=\sin2x$,
$\phi'(0)=2\cos0=2$, so $-\phi'(0)=-2$. Numerically
`delta_prime_sift(lambda x: math.exp(-x), 0.03)` $=1.0002\approx1$, and the $\sin2x$ case gives
$-1.998\approx-2$.

### P3.  Scaling and composition  *(Boas 3e §11 eq.11.19, p.456)*
Prove δ(ax)=δ(x)/|a| by substitution (Boas (11.19c)), then the general rule
δ(f(x))=Σ δ(x−x_i)/|f′(x_i)| (Boas (11.19e)). Apply to δ(x²−c²) to get
[δ(x−c)+δ(x+c)]/(2c). *Check:* `delta_compose_rhs`, `delta_compose_integral` agree
as a→0.

**Solution.** Substitute $u=ax$: $\int\delta(ax)\phi(x)\,dx=\frac1{|a|}\int\delta(u)\phi(u/a)\,du
=\frac1{|a|}\phi(0)$ (the $|a|$ comes from flipping limits when $a<0$), so $\delta(ax)=\delta(x)/|a|$.
Near each simple root $x_i$, $f(x)\approx f'(x_i)(x-x_i)$, hence
$$\delta\big(f(x)\big)=\sum_i\frac{\delta(x-x_i)}{|f'(x_i)|}.$$
For $f=x^2-c^2=(x-c)(x+c)$ the roots are $\pm c$ with $|f'|=2c$, giving
$[\delta(x-c)+\delta(x+c)]/(2c)$, i.e. $[\phi(c)+\phi(-c)]/(2c)$. With $c=1.5$ the closed form is
$0.047158$, matched by the nascent integral → $0.047159$ as $a\to0$ — so `delta_compose_rhs`,
`delta_compose_integral` agree.

### P4.  Heaviside and the jump  *(Boas 3e §11, p.449)*
Show H′(x)=δ(x) via ⟨H′,φ⟩=−∫₀^∞φ′=φ(0). This is why a point charge has density
ρ=qδ(r−r₀) (Boas (11.20)–(11.21), p.456) — `~EM-01`. *Check:* the integration-by-parts
identity −∫₀^L φ′dx ≈ φ(0) for decaying φ.

**Solution.** With $H(x)=0$ for $x<0$ and $1$ for $x>0$, and a decaying test function $\phi$,
$$\langle H',\phi\rangle=-\langle H,\phi'\rangle=-\int_{-\infty}^{\infty}\!H(x)\phi'(x)\,dx
=-\int_0^{\infty}\!\phi'(x)\,dx=-[\phi(\infty)-\phi(0)]=\phi(0)=\langle\delta,\phi\rangle.$$
Hence $H'(x)=\delta(x)$: the delta is the density of a unit jump, which is exactly why a point
charge carries density $\rho=q\,\delta(\mathbf r-\mathbf r_0)$ (`~EM-01`). Numerically
$-\int_0^L\phi'\,dx=\phi(0)-\phi(L)\approx\phi(0)$ for decaying $\phi$.

### P5.  The Fourier representation  *(Boas 3e §11, p.454; Ch.7 §12, p.378)*
Show (1/2π)∫_{−K}^{K}e^{ikx}dk = sin(Kx)/(πx), and that it → δ(x) as K→∞. Confirm
it sifts a **decaying** φ (it is not integrable against a growing one). *Check:*
`fourier_delta_kernel(x, K)` integrated against e^{−x²}cos x → φ(0).

**Solution.** Integrate the exponential directly:
$$\frac1{2\pi}\int_{-K}^{K}e^{ikx}\,dk=\frac1{2\pi}\frac{e^{iKx}-e^{-iKx}}{ix}
=\frac1{2\pi}\frac{2i\sin Kx}{ix}=\frac{\sin(Kx)}{\pi x}.$$
This Dirichlet kernel has $\int=1$ and oscillates ever faster as $K\to\infty$, so it behaves as a
nascent $\delta$, sifting any decaying $\phi$: $\int\frac{\sin Kx}{\pi x}\phi(x)\,dx\to\phi(0)$.
Against $\phi=e^{-x^2}\cos x$ (so $\phi(0)=1$), `fourier_delta_kernel(x, K)` integrated already
gives $1.000000$ by $K=20$.

### P6.  The impulse response (bridge to MA-14)  *(Boas 3e §11 Example 1, eq.11.2, p.450)*
Boas's first delta example is y″+ω²y=δ(t−t₀), y(0)=y′(0)=0 — solve it to get the
response sin ω(t−t₀)/ω for t>t₀. This is exactly the causal Green's function of
`~MA-14`. (Pen-and-paper; compare with `MA-14`'s `causal_green_oscillator`.)

**Solution.** For $t<t_0$ causality forces $y=0$. Integrating $y''+\omega^2y=\delta(t-t_0)$ across
$t_0$ imparts a unit velocity jump: $y(t_0^+)=0,\ y'(t_0^+)=1$. For $t>t_0$ the homogeneous
solution $y=C\cos\omega(t-t_0)+D\sin\omega(t-t_0)$ with these data has $C=0,\ D=1/\omega$, so
$$y(t)=\frac{\sin\omega(t-t_0)}{\omega},\qquad t>t_0.$$
This impulse response is precisely the retarded Green's function of `~MA-14` — namely
`causal_green_oscillator(t, t0, omega)`.
