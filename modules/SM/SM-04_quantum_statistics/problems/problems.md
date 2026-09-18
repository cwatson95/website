# SM-04 — Problems

Work by hand, then check with `code/quantum_statistics.py`. Citations in
`../refs.md`; **Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  The three occupations and their classical limit  *(Pa §6.3, p.149)*
Write ⟨n⟩ for Bose–Einstein, Fermi–Dirac, and Maxwell–Boltzmann. Show all three
coincide when (ε − µ) ≫ kT, and that BE > MB > FD otherwise. *Check:*
`bose_einstein`, `fermi_dirac`, `maxwell_boltzmann` agree at (ε−µ)/kT = 10.

*Answer:* $\langle n\rangle=\dfrac{1}{e^x\mp1}$ for BE/FD and $e^{-x}$ for MB, with $x\equiv(\varepsilon-\mu)/kT$; at $x=10$ all three equal $e^{-10}=4.540\times10^{-5}$ to one part in $10^4$.

**Solution.** Let $x\equiv(\varepsilon-\mu)/kT$. The three mean occupations are
$$\langle n\rangle_{\rm BE}=\frac{1}{e^x-1},\qquad \langle n\rangle_{\rm FD}=\frac{1}{e^x+1},\qquad \langle n\rangle_{\rm MB}=e^{-x}.$$
For $x\gg1$, $e^x\gg1$ so the $\mp1$ is negligible beside $e^x$ and both quantum forms collapse to $1/e^x=e^{-x}$, the classical Maxwell–Boltzmann factor. For finite $x$ the denominators order as $e^x-1<e^x<e^x+1$, so the reciprocals give
$$\langle n\rangle_{\rm BE}>\langle n\rangle_{\rm MB}>\langle n\rangle_{\rm FD}:$$
bosons bunch (no exclusion), fermions are suppressed (Pauli). Tie to check: at $(\varepsilon-\mu)/kT=10$ the three functions agree to $\sim10^{-4}$, all $\approx e^{-10}=4.540\times10^{-5}$.

### P2.  Pauli bound and half-filling  *(Pa §6.3, p.149; §8.1, p.231)*
Show the Fermi–Dirac occupation is always in [0,1] and equals exactly ½ at ε = µ.
*Check:* `fermi_dirac(mu,mu,T) == 0.5`; the value stays in [0,1] for all ε.

*Answer:* $\langle n\rangle_{\rm FD}=1/(e^x+1)$, $x=(\varepsilon-\mu)/kT$; since $e^x>0$ the value lies in $(0,1)$, and at $\varepsilon=\mu$ ($x=0$) it is exactly $\tfrac12$.

**Solution.** Write $\langle n\rangle_{\rm FD}=1/(e^x+1)$ with $x=(\varepsilon-\mu)/kT$. For every real $x$, $e^x>0$, so the denominator obeys $e^x+1>1$ and is finite, giving
$$0<\langle n\rangle_{\rm FD}=\frac{1}{e^x+1}<1.$$
The ceiling $\langle n\rangle\le1$ is the Pauli principle — at most one fermion per state. The extremes are $\langle n\rangle\to1$ for $\varepsilon\ll\mu$ ($x\to-\infty$, filled) and $\langle n\rangle\to0$ for $\varepsilon\gg\mu$ ($x\to+\infty$, empty). At the Fermi level $\varepsilon=\mu$, $x=0$ and $e^0=1$, so
$$\langle n\rangle_{\rm FD}\big|_{\varepsilon=\mu}=\frac{1}{1+1}=\frac12.$$
Tie to check: `fermi_dirac(mu,mu,T)` $=0.5$, and the occupation stays in $[0,1]$ for all $\varepsilon$.

### P3.  The zero-temperature Fermi sea  *(Pa §8.1, p.231)*
Argue that as T → 0 the FD distribution becomes a step at the Fermi energy. *Check:*
`fermi_dirac_T0(0.9*eF, eF) == 1` and `fermi_dirac_T0(1.1*eF, eF) == 0`.

*Answer:* As $T\to0$ the exponent $(\varepsilon-\varepsilon_F)/kT\to\mp\infty$, so $\langle n\rangle\to1$ below $\varepsilon_F$ and $\to0$ above — the Fermi function becomes the step $\Theta(\varepsilon_F-\varepsilon)$.

**Solution.** At $T=0$ the chemical potential is the Fermi energy, $\mu(0)=\varepsilon_F$, so $\langle n\rangle_{\rm FD}=1/\!\left(e^{(\varepsilon-\varepsilon_F)/kT}+1\right)$. Fix $\varepsilon\neq\varepsilon_F$ and let $T\to0^+$, so $1/kT\to+\infty$. If $\varepsilon<\varepsilon_F$ the exponent $\to-\infty$, $e^{(\varepsilon-\varepsilon_F)/kT}\to0$ and $\langle n\rangle\to1$; if $\varepsilon>\varepsilon_F$ the exponent $\to+\infty$ and $\langle n\rangle\to0$:
$$\lim_{T\to0}\frac{1}{e^{(\varepsilon-\varepsilon_F)/kT}+1}=\begin{cases}1,&\varepsilon<\varepsilon_F,\\ 0,&\varepsilon>\varepsilon_F,\end{cases}\;=\;\Theta(\varepsilon_F-\varepsilon).$$
The smooth Fermi function sharpens into a step whose width $\sim kT$ shrinks to zero — every state below $\varepsilon_F$ filled, every one above empty (the Fermi sea). Tie to check: `fermi_dirac_T0(0.9*eF, eF)` $=1$ and `fermi_dirac_T0(1.1*eF, eF)` $=0$.

### P4.  Planck, Rayleigh–Jeans, and the UV catastrophe  *(Pa §7.3, p.200)*
Show the Planck spectrum reduces to Rayleigh–Jeans (ω²/π²c³)kT at low ω, and that
the classical law would diverge if extrapolated. *Check:* `planck_energy_density`
≈ `rayleigh_jeans` for ω = 10¹⁰–10¹² rad/s at T = 5778 K.

*Answer:* For $\hbar\omega\ll kT$, $e^{\hbar\omega/kT}-1\approx\hbar\omega/kT$, so $u(\omega)\to(\omega^2/\pi^2c^3)kT$ (Rayleigh–Jeans); lacking the exponential cutoff, $\int\omega^2\,d\omega$ would diverge — the ultraviolet catastrophe.

**Solution.** The Planck density is $u(\omega)=\dfrac{\hbar\omega^3}{\pi^2c^3}\dfrac{1}{e^{\hbar\omega/kT}-1}$. Put $x=\hbar\omega/kT$; at low frequency $x\ll1$, so $e^x-1=x+\tfrac{x^2}{2}+\cdots\approx x$ and $1/(e^x-1)\approx1/x=kT/\hbar\omega$. Then
$$u(\omega)\;\to\;\frac{\hbar\omega^3}{\pi^2c^3}\cdot\frac{kT}{\hbar\omega}=\frac{\omega^2}{\pi^2c^3}\,kT,$$
the Rayleigh–Jeans law — note that $\hbar$ has cancelled. It rises as $\omega^2$ without bound, so $\int_0^\infty u\,d\omega\propto\int\omega^2\,d\omega$ diverges (the ultraviolet catastrophe). Planck's denominator $e^{\hbar\omega/kT}$ rescues it: modes with $\hbar\omega\gg kT$ are exponentially frozen out. Tie to check: `planck_energy_density` $\approx$ `rayleigh_jeans` for $\omega=10^{10}$–$10^{12}$ rad/s at $T=5778$ K (ratio $0.99993$ at $10^{11}$).

### P5.  Wien and Stefan–Boltzmann  *(Pa §7.3, p.200)*
Find the peak of u(ω) by solving 3(1 − e⁻ˣ) = x, and integrate u(ω) over ω to get
U/V = aT⁴. *Check:* `wien_peak_x()` ≈ 2.8214; the numerical integral of
`planck_energy_density` equals `radiation_energy_density(T)`; `stefan_boltzmann_constant()`
≈ 5.670×10⁻⁸.

*Answer:* $u\propto x^3/(e^x-1)$ peaks where $3(1-e^{-x})=x$, i.e. $x=\hbar\omega_{\max}/kT\approx2.8214$ (Wien); $\int_0^\infty u\,d\omega=aT^4$ with $a=\pi^2k^4/15\hbar^3c^3$, so $\sigma=ac/4=\pi^2k^4/60\hbar^3c^2\approx5.670\times10^{-8}$.

**Solution.** Write $u\propto x^3/(e^x-1)$ with $x=\hbar\omega/kT$. The peak is where $du/d\omega=0$:
$$\frac{d}{dx}\frac{x^3}{e^x-1}=0\ \Rightarrow\ 3(e^x-1)=xe^x\ \Rightarrow\ 3\left(1-e^{-x}\right)=x,$$
whose nonzero root is $x=2.821439$ — Wien's displacement law, $\omega_{\max}\propto T$. For the total density substitute $x=\hbar\omega/kT$ ($d\omega=(kT/\hbar)\,dx$) and use $\int_0^\infty x^3/(e^x-1)\,dx=\pi^4/15$:
$$\frac{U}{V}=\int_0^\infty u(\omega)\,d\omega=\frac{(kT)^4}{\pi^2c^3\hbar^3}\int_0^\infty\frac{x^3\,dx}{e^x-1}=\frac{\pi^2k^4}{15\hbar^3c^3}\,T^4=aT^4.$$
The radiated flux is $\sigma T^4$ with $\sigma=ac/4=\pi^2k^4/60\hbar^3c^2$. Tie to check: `wien_peak_x()` $\approx2.8214$, the numerical $\int u\,d\omega$ equals `radiation_energy_density(T)`, and `stefan_boltzmann_constant()` $\approx5.670\times10^{-8}$.
