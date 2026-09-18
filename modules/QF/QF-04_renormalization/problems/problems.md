# QF-04 — Problems

Work by hand, then check with `code/renormalization.py`. Citations in `../refs.md`;
**PS** = Peskin & Schroeder, cited at chapter/section level.

### P1.  A divergent loop and its counterterm  *(PS Ch. 10, §10.1–10.2)*
For $\phi^4$ theory, power-count the one-loop four-point integral
$\int d^4k\,(k^2-m^2)^{-2}$ and show it is **logarithmically** UV-divergent, giving
$\Gamma^{(4)}\sim-\lambda+\tfrac{3\lambda^2}{32\pi^2}\ln(\Lambda^2/\mu^2)$. Which
counterterm $\delta_\lambda$ absorbs it, and why is the theory renormalizable (only
finitely many counterterms)? *Check:* the finite coefficient is the beta-function
slope — `beta_phi4(0.1)` = 3(0.1)²/16π² ≈ 1.90e-4.

*Answer:* The integral is **logarithmically** UV-divergent ($D=0$); the counterterm $\delta_\lambda=-\tfrac{3\lambda^2}{32\pi^2}\ln(\Lambda^2/\mu^2)$ absorbs it, and $\phi^4$ is renormalizable because $\lambda$ is dimensionless (only finitely many divergent amplitudes).

**Solution.** Power-count the integrand at large loop momentum $k$: the measure $d^4k\sim k^3\,dk$ scales as $k^4$ and the two propagators as $(k^2-m^2)^{-2}\sim k^{-4}$, so
$$\int^\Lambda\!\frac{d^4k}{(k^2-m^2)^2}\sim\int^\Lambda\frac{k^3\,dk}{k^4}=\int^\Lambda\frac{dk}{k}\sim\ln\Lambda,$$
a **logarithmic** divergence (superficial degree $D=4-4=0$). Carrying out the integral,
$$\Gamma^{(4)}=-\lambda+\frac{3\lambda^2}{2}\!\int\!\frac{d^4k}{(2\pi)^4}\frac{1}{(k^2-m^2)^2}+\cdots\sim-\lambda+\frac{3\lambda^2}{32\pi^2}\ln\frac{\Lambda^2}{\mu^2}.$$
A coupling counterterm $\delta_\lambda=-\tfrac{3\lambda^2}{32\pi^2}\ln(\Lambda^2/\mu^2)$ cancels the cutoff dependence, leaving a finite renormalized vertex. The theory is renormalizable because $\lambda$ is dimensionless in $d=4$: only the 2- and 4-point functions have $D\ge0$, so finitely many counterterms suffice at every order. The cutoff-independent coefficient of $\ln(\Lambda/\mu)$ is exactly the beta-function slope $\beta(\lambda)=3\lambda^2/16\pi^2$, matching `beta_phi4(0.1)` $=3(0.1)^2/16\pi^2\approx1.90\times10^{-4}$.

### P2.  The QED beta function and the running coupling  *(PS Ch. 7; Ch. 12)*
From $\mu$-independence of physics, derive $\beta(\alpha)=\mu\,d\alpha/d\mu=2\alpha^2/3\pi$
and integrate it to the closed form $\alpha(Q)=\alpha(\mu)/[1-(\alpha(\mu)/3\pi)\ln(Q^2/\mu^2)]$.
Why does the **positive** sign mean charge is *screened* (weaker at long distance)?
*Check:* `beta_qed(1/137.036)` ≈ 1.13e-5 > 0; `qed_running_alpha(Q)` increases
monotonically (α(m_e)=1/137.0, α(1 GeV)=1/135.4, α(M_Z)=1/134.5, electron-only).

*Answer:* $\beta(\alpha)=2\alpha^2/3\pi>0$ integrates to $\alpha(Q)=\alpha(\mu)/[1-(\alpha(\mu)/3\pi)\ln(Q^2/\mu^2)]$; the $+$ sign makes $\alpha$ grow toward the UV, i.e. the charge is screened at long distance.

**Solution.** Holding the bare coupling fixed, $\mu$-independence of physics forces the renormalized $\alpha(\mu)$ to run; the one-loop vacuum-polarization log gives
$$\beta(\alpha)=\mu\frac{d\alpha}{d\mu}=\frac{2\alpha^2}{3\pi}>0.$$
Separate variables, $d\alpha/\alpha^2=(2/3\pi)\,d\ln\mu$, and integrate from $\mu$ to $Q$:
$$\frac{1}{\alpha(\mu)}-\frac{1}{\alpha(Q)}=\frac{1}{3\pi}\ln\frac{Q^2}{\mu^2}\quad\Longrightarrow\quad\alpha(Q)=\frac{\alpha(\mu)}{1-\dfrac{\alpha(\mu)}{3\pi}\ln(Q^2/\mu^2)}.$$
The positive $\beta$ makes $1/\alpha$ decrease with energy, so $\alpha$ is largest in the UV and smallest in the IR: the $e^+e^-$ vacuum polarizes around a bare charge and **screens** it, weakening the effective charge seen from afar. The check confirms both: `beta_qed(1/137.036)` $\approx1.13\times10^{-5}>0$, and $\alpha$ runs up monotonically — $\alpha(m_e)=1/137.0\to\alpha(1\,\text{GeV})=1/135.4\to\alpha(M_Z)=1/134.5$ (electron-only).

### P3.  α(M_Z) from α(0)  *(PS Ch. 7)*
Run $\alpha$ from the Thomson limit $\alpha(0)=1/137$ up to $Q=M_Z=91.19$ GeV. Show
the electron loop alone gives only $1/134.5$, and that summing $Q_f^2 N_c^f$ over all
charged Standard-Model fermions (each turning on above its threshold) steepens the
slope to the measured $\alpha(M_Z)\approx1/128$. Why is the hadronic part not a clean
free-quark calculation? *Check:* `1/qed_running_alpha(M_Z)` ≈ 134.5 (electron only);
`1/qed_alpha_sm(M_Z)` ≈ 128.4 (all charged fermions).

*Answer:* Electron-only $1/\alpha(M_Z)\approx134.5$; summing $Q_f^2N_c^f$ over all charged SM fermions steepens it to $\approx128.4$ (measured $\sim1/128$). The light-quark part is non-perturbative, fixed from $e^+e^-\to$ hadrons data (the $R$-ratio).

**Solution.** With only the electron in the loop ($S=1$) the closed form gives
$$\frac{1}{\alpha(M_Z)}=\frac{1}{\alpha(0)}-\frac{1}{3\pi}\ln\frac{M_Z^2}{m_e^2}=137.0-\frac{1}{3\pi}\ln\frac{(91.19)^2}{(0.000511)^2}\approx134.5.$$
Each charged fermion $f$ contributes the same way once $Q>m_f$, weighted by $Q_f^2N_c^f$ (squared charge $\times$ colour), steepening the slope:
$$\frac{1}{\alpha(Q)}=\frac{1}{\alpha(0)}-\frac{1}{3\pi}\sum_{m_f<Q}Q_f^2N_c^f\,\ln\frac{Q^2}{m_f^2}.$$
Summing $e,\mu,\tau$ and the five quarks ($u,d,s,c,b$ with $N_c=3$) brings $1/\alpha(M_Z)$ down to $\approx128$, the measured value. The hadronic part is **not** a clean free-quark calculation because near $m_u,m_d$ the strong coupling is large and the quarks are confined; the genuine low-energy hadronic vacuum polarization is extracted from $e^+e^-\to$ hadrons data (the $R$-ratio), the $\sim0.3$ GeV light-quark "mass" being only a stand-in. The check matches: `1/qed_running_alpha(M_Z)` $\approx134.5$ (electron only) and `1/qed_alpha_sm(M_Z)` $\approx128.4$ (all charged fermions).

### P4.  The Landau pole  *(PS Ch. 12)*
Set the denominator of the QED running coupling to zero and solve for
$Q_\text{Landau}=Q_0\exp(3\pi/2\alpha_0)$. Evaluate it and compare to the Planck
scale ($\sim10^{19}$ GeV). What does it (not) mean physically that QED has a Landau
pole? *Check:* `qed_landau_pole()` ≈ 1.45e277 GeV (≈ 10²⁷⁷, far above the Planck
scale); at that scale the closed-form denominator vanishes.

*Answer:* $Q_{\text{Landau}}=Q_0\exp(3\pi/2\alpha_0)\approx1.45\times10^{277}$ GeV, far above the Planck scale $\sim10^{19}$ GeV. It signals only that perturbative QED is incomplete, not a genuine divergence.

**Solution.** The running coupling $\alpha(Q)=\alpha_0/[1-(\alpha_0/3\pi)\ln(Q^2/Q_0^2)]$ blows up when its denominator vanishes. Setting it to zero,
$$1-\frac{\alpha_0}{3\pi}\ln\frac{Q^2}{Q_0^2}=0\quad\Longrightarrow\quad\ln\frac{Q^2}{Q_0^2}=\frac{3\pi}{\alpha_0},$$
and $\ln(Q^2/Q_0^2)=2\ln(Q/Q_0)$ gives the **Landau pole**
$$Q_{\text{Landau}}=Q_0\exp\!\Big(\frac{3\pi}{2\alpha_0}\Big).$$
With $\alpha_0\approx1/137$ and $Q_0=m_e$ this is $\approx1.45\times10^{277}$ GeV — vastly above the Planck scale $\sim10^{19}$ GeV. Physically it does **not** mean the charge truly becomes infinite: long before such energies gravity and new physics intervene and the one-loop formula has broken down. The pole only signals that perturbative QED cannot be complete up to arbitrarily high scales. The check gives `qed_landau_pole()` $\approx1.45\times10^{277}$ GeV, the scale at which the closed-form denominator vanishes.

### P5.  φ⁴ running and triviality  *(PS Ch. 12)*
Integrate $d\lambda/d\ln\mu=3\lambda^2/16\pi^2$ and obtain
$1/\lambda(\mu)=1/\lambda_0-(3/16\pi^2)\ln(\mu/\mu_0)$. Show the coupling grows in the
UV and hits a Landau pole; argue that a finite continuum limit forces $\lambda\to0$
("triviality"). *Check:* `phi4_running(1.0, 1.0, 1e10)` ≈ 1.7776 (matches the closed
form), and `phi4_landau_pole(1.0, 1.0)` ≈ 7.25e22 GeV.

*Answer:* $1/\lambda(\mu)=1/\lambda_0-(3/16\pi^2)\ln(\mu/\mu_0)$; $\lambda$ grows in the UV to a Landau pole at $\mu_0\exp(16\pi^2/3\lambda_0)$, and a finite continuum limit forces $\lambda_0\to0$ (triviality).

**Solution.** Separate variables in $d\lambda/d\ln\mu=3\lambda^2/16\pi^2$:
$$\int\frac{d\lambda}{\lambda^2}=\frac{3}{16\pi^2}\int d\ln\mu\quad\Longrightarrow\quad\frac{1}{\lambda(\mu)}=\frac{1}{\lambda_0}-\frac{3}{16\pi^2}\ln\frac{\mu}{\mu_0}.$$
Since $1/\lambda$ falls as $\mu$ grows, $\lambda(\mu)$ rises in the UV and diverges when $1/\lambda\to0$, at the Landau pole
$$\mu_{\text{pole}}=\mu_0\exp\!\Big(\frac{16\pi^2}{3\lambda_0}\Big).$$
A genuine continuum theory needs the cutoff $\Lambda\to\infty$ with the pole pushed to infinity, which from the formula requires $1/\lambda_0\to\infty$, i.e. $\lambda_0\to0$: the renormalized coupling is driven to zero and the interacting theory collapses to a free one — the **triviality** of $\phi^4$ in four dimensions. The check confirms the integration: `phi4_running(1.0, 1.0, 1e10)` $\approx1.7776$, matching the closed form, and `phi4_landau_pole(1.0, 1.0)` $\approx7.25\times10^{22}$ GeV.

### P6.  Asymptotic freedom: the opposite sign  *(PS Ch. 16–17)*
Quote the non-abelian one-loop beta function
$\beta(g)=-(g^3/16\pi^2)(\tfrac{11}{3}C_A-\tfrac{4}{3}T_F n_f)$ and explain why $C_A>0$
(gluon self-interaction) makes it **negative** for QCD ($n_f<33/2$), so $\alpha_s$
*decreases* at high energy. Contrast this with QED (P2). *Check:* `beta_qcd(0.1181)`
≈ −0.017 < 0; `qcd_running_alpha` gives α_s(2 GeV)=0.263 > α_s(M_Z)=0.118 > α_s(1 TeV)=0.088.

*Answer:* $\beta(g)=-(g^3/16\pi^2)(\tfrac{11}{3}C_A-\tfrac43 T_Fn_f)<0$ for QCD ($C_A=3$, $n_f<33/2$): the gluon self-coupling term dominates, so $\alpha_s$ shrinks toward the UV — asymptotic freedom, opposite to QED's screening.

**Solution.** The non-abelian one-loop beta function is
$$\beta(g)=-\frac{g^3}{16\pi^2}\Big(\frac{11}{3}C_A-\frac{4}{3}T_Fn_f\Big),\qquad C_A=N=3,\ \ T_F=\tfrac12.$$
The first term $+\tfrac{11}{3}C_A$ comes from the **gluon self-interaction** (gluons carry colour charge, with no abelian analogue) and *antiscreens*; the second $-\tfrac43 T_Fn_f$ is the QED-like fermion screening. For QCD the gluon term wins whenever $n_f<33/2=16.5$, so the bracket is positive and $\beta<0$. Equivalently $b_0=11-\tfrac23 n_f>0$, and the closed form
$$\frac{1}{\alpha_s(Q)}=\frac{1}{\alpha_s(Q_0)}+\frac{b_0}{4\pi}\ln\frac{Q^2}{Q_0^2}$$
shows $1/\alpha_s$ growing with $Q$, so $\alpha_s$ **shrinks** in the UV — **asymptotic freedom**, why quarks are nearly free at short distance. This is the exact opposite of QED (P2), where $\beta>0$ makes $\alpha$ grow with energy. The check confirms the sign and the running: `beta_qcd(0.1181)` $\approx-0.017<0$, and $\alpha_s(2\,\text{GeV})=0.263>\alpha_s(M_Z)=0.118>\alpha_s(1\,\text{TeV})=0.088$.

### P7.  Fixed points and the bridge to critical phenomena  *(PS Ch. 12–13; `~SM-05`)*
For the toy $\beta(g)=a\,g^2-b\,g^3$ find both zeros and classify their stability from
the sign of $\beta'$. Show $g_*=a/b$ has $\beta'(g_*)=-a^2/b<0$ (UV-attractive) while
the origin is UV-repulsive. Explain how $\beta'(g_*)$ — the linearized RG eigenvalue —
becomes a **critical exponent** at the Wilson–Fisher fixed point of `~SM-05`. *Check:*
`fixed_point(2.0, 4.0)` returns `g_star` = 0.5 and `beta_prime` = −1.0 with
`stability` = "UV-attractive"; `beta_toy(0.5, 2.0, 4.0)` ≈ 0.

*Answer:* Zeros $g=0$ (UV-repulsive) and $g_*=a/b$ (UV-attractive, $\beta'(g_*)=-a^2/b<0$); the linearized slope $\beta'(g_*)$ is the RG eigenvalue that becomes a critical exponent at the Wilson–Fisher fixed point.

**Solution.** Factor the beta function, $\beta(g)=ag^2-bg^3=g^2(a-bg)$, so the zeros are $g=0$ and
$$g_*=\frac{a}{b}.$$
Stability follows from the slope $\beta'(g)=2ag-3bg^2$. Near the origin $\beta\approx ag^2>0$ for small $g>0$, so the coupling flows *away* from $0$ as $\mu$ rises — UV-repulsive. At $g_*$,
$$\beta'(g_*)=2a\Big(\frac ab\Big)-3b\Big(\frac ab\Big)^2=\frac{2a^2}{b}-\frac{3a^2}{b}=-\frac{a^2}{b}<0,$$
a negative slope, so nearby couplings flow *into* $g_*$ as $\mu\to\infty$ — UV-attractive. This linearized slope $\beta'(g_*)$ is the RG eigenvalue at the fixed point; at the Wilson–Fisher fixed point of $\phi^4$ in $d=4-\epsilon$ it fixes the **critical exponents** (e.g. the correlation-length exponent $\nu$) of the Ising universality class — the bridge to `~SM-05`. The check matches: `fixed_point(2.0, 4.0)` returns `g_star` $=0.5$ and `beta_prime` $=-1.0$ with `stability` $=$ `"UV-attractive"`, and `beta_toy(0.5, 2.0, 4.0)` $\approx0$.
