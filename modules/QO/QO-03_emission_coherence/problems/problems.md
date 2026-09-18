# QO-03 — Problems

Work by hand, then check with `code/emission_coherence.py`. Citations in
`../refs.md`; **S&Z** = Scully & Zubairy, *Quantum Optics* (cited by chapter/section).

### P1.  Einstein's relations from detailed balance  *(S&Z Ch. 1)*
Write the up-rate $N_1B_{12}\rho$ and down-rate $N_2(A_{21}+B_{21}\rho)$, set them
equal, and solve for $\rho(\nu)$. Insert the Boltzmann ratio $N_2/N_1=(g_2/g_1)e^{-h\nu/k_BT}$
and demand the answer be Planck's law *for all $T$*; deduce $A_{21}/B_{21}=8\pi h\nu^3/c^3$
and $g_1B_{12}=g_2B_{21}$. *Check:* `detailed_balance_energy_density(nu, T, g1, g2, A21)`
$/$ `planck_spectral_energy_density(nu, T)` $= 1.000000$ for *any* $g_1,g_2,A_{21}$;
and `einstein_A_over_B(c/248e-9)` $\approx 1.09\times10^{-12}$ J·s/m³.

*Answer:* $A_{21}/B_{21}=8\pi h\nu^3/c^3$ and $g_1B_{12}=g_2B_{21}$.

**Solution.** Detailed balance $N_1B_{12}\rho=N_2(A_{21}+B_{21}\rho)$, solved for the field, gives
$$\rho=\frac{N_2A_{21}}{N_1B_{12}-N_2B_{21}}=\frac{A_{21}/B_{21}}{\dfrac{B_{12}}{B_{21}}\dfrac{N_1}{N_2}-1}.$$
Insert the inverse Boltzmann ratio $N_1/N_2=(g_1/g_2)\,e^{h\nu/k_BT}$:
$$\rho=\frac{A_{21}/B_{21}}{\dfrac{g_1B_{12}}{g_2B_{21}}\,e^{h\nu/k_BT}-1}.$$
This can equal Planck's $\rho=\dfrac{8\pi h\nu^3/c^3}{e^{h\nu/k_BT}-1}$ *for every* $T$ only if the coefficient of $e^{h\nu/k_BT}$ is $1$, i.e. $g_1B_{12}=g_2B_{21}$, and the prefactor matches, $A_{21}/B_{21}=8\pi h\nu^3/c^3$. With those two relations the rate-balance density is Planck identically — independent of $A_{21},g_1,g_2$ — so `detailed_balance_energy_density`/`planck_spectral_energy_density`$=1.000000$, and the prefactor is `einstein_A_over_B(c/248e-9)`$\approx1.09\times10^{-12}$ J·s/m³.

### P2.  Why a hot lamp won't lase  *(S&Z §5.6)*
Show the equilibrium ratio of stimulated to spontaneous emission is
$B_{21}\rho/A_{21}=1/(e^{h\nu/k_BT}-1)$, and find the crossover frequency where the
two are equal ($h\nu=k_BT\ln2$). Evaluate the ratio for the 248 nm KrF line at 300 K
and argue why amplification requires a population inversion, not temperature.
*Check:* `stimulated_to_spontaneous(c/248e-9, 300.0)` $\approx 1.0\times10^{-84}$;
at $\nu=k_BT\ln2/h$ the ratio is exactly $1.0$.

*Answer:* $B_{21}\rho/A_{21}=1/(e^{h\nu/k_BT}-1)$; equal rates at $h\nu=k_BT\ln2$; $\sim10^{-84}$ for 248 nm at 300 K.

**Solution.** Divide the stimulated rate by the spontaneous rate and use the first Einstein relation $A_{21}/B_{21}=8\pi h\nu^3/c^3$ together with the Planck $\rho$:
$$\frac{B_{21}\rho}{A_{21}}=\frac{\rho}{A_{21}/B_{21}}=\frac{8\pi h\nu^3/c^3}{(8\pi h\nu^3/c^3)\,(e^{h\nu/k_BT}-1)}=\frac{1}{e^{h\nu/k_BT}-1}.$$
The two are equal when $e^{h\nu/k_BT}-1=1$, i.e. $e^{h\nu/k_BT}=2$, giving the crossover $h\nu=k_BT\ln2$. For the 248 nm KrF line at 300 K, $h\nu/k_BT\approx193\gg1$, so
$$\frac{B_{21}\rho}{A_{21}}\approx e^{-h\nu/k_BT}\approx e^{-193}\approx10^{-84}.$$
Spontaneous emission wins by $\sim10^{84}$: heat cannot build coherent gain, only a non-thermal population inversion can. This is `stimulated_to_spontaneous(c/248e-9, 300.0)`$\approx1.0\times10^{-84}$, while at $\nu=k_BT\ln2/h$ the ratio is exactly $1.0$.

### P3.  The two limits of Planck  *(S&Z Ch. 1)*
From $\rho=(8\pi h\nu^3/c^3)/(e^{h\nu/k_BT}-1)$ recover the **Rayleigh–Jeans**
($h\nu\ll k_BT$) law $\rho\to8\pi\nu^2k_BT/c^3$ and the **Wien** ($h\nu\gg k_BT$)
exponential cutoff. Explain why the classical (Rayleigh–Jeans) result is the
$h\to0$ limit and where it diverges. *Check:* `planck_spectral_energy_density(1e9, 300.0)`
$\approx 3.86\times10^{-27}$ J·s/m³, matching $8\pi\nu^2k_BT/c^3$ to $<0.1\%$
(`test_planck_closed_form_and_rayleigh_jeans_limit`).

*Answer:* Rayleigh–Jeans $\rho\to8\pi\nu^2k_BT/c^3$ (the $h\to0$ limit, UV-divergent); Wien $\rho\to(8\pi h\nu^3/c^3)e^{-h\nu/k_BT}$.

**Solution.** Let $x=h\nu/k_BT$. For $x\ll1$ ($h\nu\ll k_BT$) expand $e^{x}-1=x+O(x^2)$:
$$\rho=\frac{8\pi h\nu^3/c^3}{e^{x}-1}\;\xrightarrow{\,x\to0\,}\;\frac{8\pi h\nu^3/c^3}{h\nu/k_BT}=\frac{8\pi\nu^2k_BT}{c^3}.$$
The $h$ cancels, so the **Rayleigh–Jeans** law is precisely the classical $h\to0$ limit; its $\nu^2$ growth makes $\int\rho\,d\nu$ diverge — the ultraviolet catastrophe. For $x\gg1$ ($h\nu\gg k_BT$), $e^{x}-1\to e^{x}$ and
$$\rho\to\frac{8\pi h\nu^3}{c^3}\,e^{-h\nu/k_BT},$$
the **Wien** exponential cutoff that quantization supplies to tame the divergence. At $\nu=10^9$ Hz, $T=300$ K we sit deep in Rayleigh–Jeans: `planck_spectral_energy_density(1e9, 300.0)`$\approx3.86\times10^{-27}$ J·s/m³, matching $8\pi\nu^2k_BT/c^3$ to $<0.1\%$.

### P4.  Laser threshold and gain clamping  *(S&Z §5.5, §11.2)*
For $\dot N=R-\gamma N-GNn$, $\dot n=GNn-\kappa n$, set both to zero. Show the photon
equation forces either $n=0$ or $N=\kappa/G$, giving threshold $R_{\text{th}}=\gamma\kappa/G$;
then derive $n=(R-R_{\text{th}})/\kappa$ above threshold and explain why the inversion
**clamps** (every extra pump quantum becomes a photon, not more inversion). *Check:*
`laser_threshold(1,1,1)` $=1.0$; `laser_steady_state(0.5)` $=(0.5,\,0.0)$,
`laser_steady_state(2.0)` $=(1.0,\,1.0)$, `laser_steady_state(5.0)` $=(1.0,\,4.0)$ —
$N$ frozen at $1$, $n$ rising linearly.

*Answer:* $R_{\text{th}}=\gamma\kappa/G$; below it $n=0,\ N=R/\gamma$; above it $N=\kappa/G$ (clamped), $n=(R-R_{\text{th}})/\kappa$.

**Solution.** The photon equation factors,
$$\dot n=GNn-\kappa n=n\,(GN-\kappa)=0\quad\Rightarrow\quad n=0\ \text{ or }\ N=\frac{\kappa}{G}.$$
On the dark branch $n=0$, the inversion balance $\dot N=R-\gamma N=0$ gives $N=R/\gamma$, valid while $N\le\kappa/G$, i.e. up to $R_{\text{th}}=\gamma\kappa/G$. Past threshold the photon term pins $N=\kappa/G$; substituting into $\dot N=0$,
$$R-\gamma\frac{\kappa}{G}-G\frac{\kappa}{G}\,n=0\quad\Rightarrow\quad n=\frac{R-\gamma\kappa/G}{\kappa}=\frac{R-R_{\text{th}}}{\kappa}.$$
The inversion **clamps** at $\kappa/G$: every additional pump quantum is converted to a photon, never to more inversion. With $G=\kappa=\gamma=1$, `laser_threshold(1,1,1)`$=1.0$, and `laser_steady_state` returns $(0.5,0)$ at $R=0.5$, $(1,1)$ at $R=2$, $(1,4)$ at $R=5$ — $N$ frozen at $1$, $n$ rising linearly.

### P5.  Bunching, randomness, antibunching  *(S&Z §4.4–4.5)*
Compute $g^{(2)}(0)=\langle n(n-1)\rangle/\langle n\rangle^2$ for (i) a thermal
(Bose–Einstein) distribution $p_n=\bar n^{\,n}/(1+\bar n)^{n+1}$, (ii) a Poisson
(coherent) distribution, and (iii) a Fock state $|n_0\rangle$. Obtain $2$, $1$, and
$1-1/n_0$; explain why $g^{(2)}(0)<1$ has no classical (positive-$P$) description.
*Check:* `g2_from_distribution` gives $2$ (thermal), $1$ (Poisson), and `g2_fock(5)`
$=0.8$; `g2_fock(1)` $=0.0$ (a single photon, perfect antibunching).

*Answer:* $g^{(2)}(0)=2$ (thermal), $1$ (Poisson), $1-1/n_0$ (Fock).

**Solution.** Use $g^{(2)}(0)=\langle n(n-1)\rangle/\langle n\rangle^2$ with $\langle n(n-1)\rangle=\langle n^2\rangle-\langle n\rangle$. (i) Bose–Einstein $p_n=\bar n^{\,n}/(1+\bar n)^{n+1}$ has $\langle n\rangle=\bar n$ and variance $\bar n+\bar n^2$, so $\langle n(n-1)\rangle=(\bar n+2\bar n^2)-\bar n=2\bar n^2$ and
$$g^{(2)}_{\text{th}}=\frac{2\bar n^2}{\bar n^2}=2.$$
(ii) Poisson has variance $=\bar n$, hence $\langle n(n-1)\rangle=\bar n^2$ and $g^{(2)}=\bar n^2/\bar n^2=1$. (iii) A Fock state $|n_0\rangle$ is sharp, $\langle n(n-1)\rangle=n_0(n_0-1)$, so $g^{(2)}=n_0(n_0-1)/n_0^2=1-1/n_0$. This falls **below** $1$, yet for any classical (positive-$P$) field $g^{(2)}(0)=1+\langle(\Delta I)^2\rangle/\langle I\rangle^2\ge1$, so $g^{(2)}<1$ has no positive-probability description. Confirmed by `g2_from_distribution` $=2$ (thermal) and $1$ (Poisson), with `g2_fock(5)`$=0.8$ and `g2_fock(1)`$=0.0$ (perfect antibunching).

### P6.  First- vs. second-order coherence  *(S&Z §4.2–4.4)*
A narrowband-filtered thermal source and an ideal laser can both show fringe
visibility $|g^{(1)}(\tau)|\to1$. Explain why $g^{(1)}$ therefore **cannot**
distinguish them, and how the Hanbury-Brown–Twiss measurement of $g^{(2)}(0)$ does:
$2$ versus $1$. Sketch the physical ordering of $g^{(2)}(0)$ from most-bunched to
most-antibunched. *Check:* `g2_thermal()` $>$ `g2_coherent()` $>$ `g2_fock(1)`, i.e.
$2 > 1 > 0$ (`test_g2_ordering_antibunched_coherent_bunched`).

*Answer:* both reach $|g^{(1)}|\to1$, so only $g^{(2)}(0)$ — thermal $2$ vs coherent $1$ — separates them.

**Solution.** $g^{(1)}(\tau)$ is the normalized *field* (amplitude) correlation, and the fringe visibility is $\mathcal V=|g^{(1)}(\tau)|$. A narrowband-filtered thermal source has a long coherence time $\tau_c\sim1/\Delta\nu$, so for $\tau\ll\tau_c$ it reaches $|g^{(1)}|\to1$ — the *same* value an ideal laser gives. Identical visibility means
$$|g^{(1)}|\to1\ \text{(both)}\quad\Longrightarrow\quad g^{(1)}\ \text{cannot tell thermal from coherent.}$$
Hanbury-Brown–Twiss instead correlates *intensities*, $g^{(2)}(0)=\langle n(n-1)\rangle/\langle n\rangle^2$: thermal photons arrive in **bunches** ($g^{(2)}=2$), coherent light is Poissonian ($g^{(2)}=1$). The ordering from most-bunched to most-antibunched is
$$\underbrace{2}_{\text{thermal}}\;>\;\underbrace{1}_{\text{coherent}}\;>\;\underbrace{1-\tfrac1n\ (\to0)}_{\text{Fock}}.$$
Hence `g2_thermal()` $>$ `g2_coherent()` $>$ `g2_fock(1)`, i.e. $2 > 1 > 0$.
