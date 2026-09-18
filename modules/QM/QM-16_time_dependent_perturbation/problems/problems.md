# QM-16 — Problems

Work them by hand, then check with `code/tdpt.py`. Sources in `../refs.md`.
Natural units $\hbar=1$ throughout; $i$ = initial state, $f$ = final,
$\omega_{fi}=(E_f-E_i)/\hbar$, $\delta=\omega-\omega_{fi}$ the detuning,
$\Omega_R$ the Rabi frequency, $\rho$ the density of final states.

### P1.  The first-order amplitude, and a constant switched-on coupling  *(Griffiths 3e §11.1.2, Eq. 11.21, p.516)*
A system in $|i\rangle$ feels a *constant* perturbation with matrix element
$\langle f|H'|i\rangle=V_{fi}$ over $0\le t'\le t$. Use the first-order amplitude
$c_f^{(1)}=-\tfrac{i}{\hbar}\int_0^t V_{fi}e^{i\omega_{fi}t'}dt'$ to find
$P_{i\to f}(t)$.
*Answer:* $c_f^{(1)}=-V_{fi}\dfrac{e^{i\omega_{fi}t}-1}{\hbar\,\omega_{fi}}$, so
$P_{i\to f}=\dfrac{|V_{fi}|^2}{\hbar^2}\dfrac{4\sin^2(\omega_{fi}t/2)}{\omega_{fi}^2}$
— oscillatory, peaked at small $\omega_{fi}$, and only valid while $P\ll1$.
*Check:* `first_order_probability(0.013, 0.7, 9.0)` equals
$0.013^2\cdot4\sin^2(0.7\cdot9/2)/0.7^2$. (`test_first_order_amplitude_constant_closed_form`.)

**Solution.** The integral is elementary:
$$c_f^{(1)}=-\frac{i}{\hbar}\int_0^t V_{fi}\,e^{i\omega_{fi}t'}dt'
=-\frac{i}{\hbar}V_{fi}\,\frac{e^{i\omega_{fi}t}-1}{i\omega_{fi}}
=-\frac{V_{fi}}{\hbar}\,\frac{e^{i\omega_{fi}t}-1}{\omega_{fi}}.$$
Factor $e^{i\omega_{fi}t}-1=e^{i\omega_{fi}t/2}\,(e^{i\omega_{fi}t/2}-e^{-i\omega_{fi}t/2})=e^{i\omega_{fi}t/2}\,2i\sin(\omega_{fi}t/2)$, so $|e^{i\omega_{fi}t}-1|^2=4\sin^2(\omega_{fi}t/2)$ and
$$P_{i\to f}=\frac{|V_{fi}|^2}{\hbar^2}\,\frac{4\sin^2(\omega_{fi}t/2)}{\omega_{fi}^2}.$$
It oscillates in $t$ and is largest for small $\omega_{fi}$ (near-degenerate levels), valid only while $P\ll1$. With $\hbar=1$, `first_order_probability(0.013, 0.7, 9.0)`$=9.75\times10^{-8}$, matching $0.013^2\cdot4\sin^2(0.7\cdot9/2)/0.7^2$ to the integrator tolerance.

### P2.  Rabi oscillations and the $\pi$-pulse  *(Griffiths 3e Prob. 11.9, Eq. 11.37, p.522)*
A two-level system is driven *on resonance* ($\delta=0$) with Rabi frequency
$\Omega_R$. (a) Write $P_{i\to f}(t)$. (b) When is the population first fully in
$|f\rangle$? (c) Confirm the closed form equals the exact $2\times2$ time evolution.
*Answer:* (a) $P=\sin^2(\Omega_R t/2)$. (b) **Full inversion** at
$t=\pi/\Omega_R$ (a "$\pi$-pulse" — flip a qubit). (c) Diagonalizing
$H=\tfrac12\Omega_R\sigma_x$ and evolving $|i\rangle$ gives the same number.
*Check:* `rabi_probability(np.pi, 1.0, 0.0)` $=1.0$;
`two_level_exact_probability(np.pi, 0.0, 1.0)` $=1.0$.
(`test_rabi_resonance_full_inversion`, `test_rabi_formula_matches_exact_dynamics`.)

**Solution.** (a) Setting $\delta=0$ in the generalized Rabi formula, the cap $\Omega_R^2/(\Omega_R^2+\delta^2)\to1$ and $\sqrt{\Omega_R^2+\delta^2}\to\Omega_R$, so $P=\sin^2(\Omega_R t/2)$. (b) This first equals $1$ when $\Omega_R t/2=\pi/2$, i.e. $t=\pi/\Omega_R$ — a **$\pi$-pulse** that completely inverts the population. (c) On resonance $H=\tfrac12\Omega_R\sigma_x$, so
$$e^{-iHt}=\cos\!\tfrac{\Omega_R t}{2}\,\mathbb 1-i\sin\!\tfrac{\Omega_R t}{2}\,\sigma_x,\qquad
e^{-iHt}\binom{1}{0}=\binom{\cos(\Omega_R t/2)}{-i\sin(\Omega_R t/2)},$$
and $|\langle f|\psi(t)\rangle|^2=\sin^2(\Omega_R t/2)$ — identical to (a). Hence `rabi_probability(np.pi, 1.0, 0.0)`$=1.0$ and `two_level_exact_probability(np.pi, 0.0, 1.0)`$=1.0$, full inversion at $t=\pi$.

### P3.  Why a detuned drive can never fully invert  *(Griffiths 3e Prob. 11.9, p.522)*
Now drive *off resonance*, $\delta\neq0$. (a) What is the maximum of $P_{i\to f}$
over all $t$? (b) At what frequency does the population flop?
*Answer:* (a) The amplitude is capped at
$\dfrac{\Omega_R^2}{\Omega_R^2+\delta^2}<1$ — you cannot reach $|f\rangle$ with
certainty unless $\delta=0$. (b) The flopping frequency rises to the generalized
Rabi frequency $\sqrt{\Omega_R^2+\delta^2}$ (`generalized_rabi_frequency`).
*Check:* with $\Omega_R=1,\delta=3$ the cap is $1/10$; the max of
`rabi_probability(t,1,3)` over a fine $t$-grid attains $0.1$.
(`test_rabi_resonance_full_inversion`.)

**Solution.** (a) The flopping factor $\sin^2(\cdots)$ ranges over $[0,1]$, so the maximum of $P_{i\to f}$ over $t$ is just the prefactor,
$$P_{\max}=\frac{\Omega_R^2}{\Omega_R^2+\delta^2}<1\quad(\delta\neq0),$$
reached whenever $\sqrt{\Omega_R^2+\delta^2}\,t/2=\tfrac\pi2+n\pi$. The detuning steals amplitude — you can never deposit the system in $|f\rangle$ with certainty. (b) The sine's argument advances at the **generalized Rabi frequency** $\sqrt{\Omega_R^2+\delta^2}$, faster than the bare $\Omega_R$. For $\Omega_R=1,\delta=3$ the cap is $1/(1+9)=1/10$; a fine-grid scan of `rabi_probability(t,1,3)` peaks at $0.0999999\approx0.1$, and `generalized_rabi_frequency(1,3)`$=\sqrt{10}=3.162$.

### P4.  First-order PT is the weak/short-time shadow of Rabi  *(Griffiths 3e §11.1.2 vs Prob. 11.9)*
Show that the first-order result for a constant rotating-frame coupling,
$P^{(1)}=(\Omega_R^2/\delta^2)\sin^2(\delta t/2)$, agrees with the exact Rabi
formula (a) when $\Omega_R\ll|\delta|$ (weak coupling) and (b) at short times for
any $\delta$.
*Answer:* (a) $\Omega_R^2+\delta^2\to\delta^2$, so the exact cap
$\Omega_R^2/(\Omega_R^2+\delta^2)\to\Omega_R^2/\delta^2$ and the two coincide.
(b) Both $\to\Omega_R^2t^2/4$ as $t\to0$ — the universal quadratic onset.
*Check:* with $\Omega_R=0.01,\delta=0.6$, `first_order_probability(0.005, -0.6, t)`
$\approx$ `rabi_probability(t, 0.01, 0.6)`; at $\Omega_R=0.5,t=0.02$ both
$\approx(\,0.5\cdot0.02/2)^2$. (`test_first_order_reproduces_rabi_weak_and_short`.)

**Solution.** With constant rotating-frame coupling $V_{fi}=\Omega_R/2$ and Bohr frequency $\omega_{fi}=-\delta$, the P1 result gives $P^{(1)}=(\Omega_R/2)^2\,4\sin^2(\delta t/2)/\delta^2=(\Omega_R^2/\delta^2)\sin^2(\delta t/2)$. (a) For $\Omega_R\ll|\delta|$ the exact cap $\Omega_R^2/(\Omega_R^2+\delta^2)\to\Omega_R^2/\delta^2$ and the flopping frequency $\sqrt{\Omega_R^2+\delta^2}\to|\delta|$, so the exact Rabi probability collapses onto $P^{(1)}$. (b) For short times $\sin^2x\to x^2$, and **both** become
$$P\to\frac{\Omega_R^2}{\delta^2}\Big(\frac{\delta t}{2}\Big)^2=\frac{\Omega_R^2t^2}{4},$$
the $\delta$-independent quadratic onset. Numerically `first_order_probability(0.005, -0.6, 7.5)`$=1.68\times10^{-4}\approx$ `rabi_probability(7.5, 0.01, 0.6)`$=1.68\times10^{-4}$, and at $\Omega_R=0.5,t=0.02$ both give $(0.5\cdot0.02/2)^2=2.5\times10^{-5}$.

### P5.  The resonance line shape  *(Griffiths 3e §11.1.3, Eq. 11.35, p.520; Fig. 11.5, p.521)*
Under $H'=V\cos(\omega t)$, $P_{i\to f}=|V_{fi}|^2\sin^2[(\omega_{fi}-\omega)t/2]/
(\omega_{fi}-\omega)^2$. As a function of the drive frequency $\omega$: (a) where
is the peak and how tall is it? (b) how do the height and width scale with the
driving time $t$?
*Answer:* (a) Peak at **resonance** $\omega=\omega_{fi}$, height $|V_{fi}|^2t^2/4$.
(b) Height $\propto t^2$, width $\propto1/t$ (first zeros at
$\omega=\omega_{fi}\pm2\pi/t$): drive longer → sharper, more selective line — the
origin of spectroscopic resolution.
*Check:* `ws[np.argmax(sinusoidal_probability(40.0, ws, 1.0, 0.01))]` $\to1.0000$
for `ws=np.linspace(0.7,1.3,4001)`; doubling $t$ quadruples the peak.
(`test_sinusoidal_resonance_peak`, `test_sinusoidal_sinc_squared`.)

**Solution.** Write $d=\omega_{fi}-\omega$. (a) As $\omega\to\omega_{fi}$, $d\to0$ and $\sin^2(dt/2)/d^2\to(t/2)^2$, so the line peaks **at resonance** $\omega=\omega_{fi}$ with height
$$P_{\text{peak}}=|V_{fi}|^2\,\frac{t^2}{4}.$$
(b) The profile is $\mathrm{sinc}^2(dt/2)$: it vanishes when $dt/2=n\pi$, i.e. first zeros at $\omega=\omega_{fi}\pm2\pi/t$, so the width $\propto1/t$ while the peak $\propto t^2$ — drive longer and the line grows taller *and* sharper (spectroscopic resolution). For `ws=np.linspace(0.7,1.3,4001)`, `ws[np.argmax(sinusoidal_probability(40.0, ws, 1.0, 0.01))]`$=1.0000$ and the peak height is $(0.01\cdot40/2)^2=0.04$; going $t=20\to40$ multiplies it by $(40/20)^2=4$.

### P6.  First-order PT vs the honest driven dynamics  *(Griffiths 3e §11.1.3, p.520)*
Integrate the *full* time-dependent two-level Hamiltonian
$H(t)=H_0+V_{fi}\cos(\omega t)\,\sigma_x$ (no rotating-wave approximation) and
compare the transition probability to first-order PT. When do they agree?
*Answer:* For weak coupling ($P\ll1$) the honest dynamics matches the full
first-order amplitude (both co- and counter-rotating terms) across detunings;
near resonance the RWA formula (Eq. 11.35) also matches. Discrepancies at strong
driving / large detuning are the Bloch–Siegert shift from the dropped term.
*Check:* `evolve_tdse(make_driven_H(0.9, 1.0, 0.01), [1,0], 20.0)` then
$|\psi_1|^2\approx$ `first_order_probability(lambda t: 0.01*np.cos(0.9*t), 1.0, 20.0)`.
(`test_sinusoidal_pt_vs_tdse`.)

**Solution.** The honest lab-frame coupling is the full cosine, $\langle f|H'|i\rangle=V_{fi}\cos\omega t'=\tfrac12V_{fi}(e^{i\omega t'}+e^{-i\omega t'})$, so the first-order amplitude keeps **both** the co- and counter-rotating terms (denominators $\omega_{fi}\mp\omega$),
$$c_f^{(1)}=-\frac{i}{\hbar}\int_0^t V_{fi}\cos(\omega t')\,e^{i\omega_{fi}t'}\,dt'.$$
`evolve_tdse` integrates $i\partial_t|\psi\rangle=H(t)|\psi\rangle$ exactly — no RWA, no weak-coupling assumption — so for $V_{fi}\ll1$ the population stays $\ll1$ and the neglected $O(V^2)$ orders are tiny, leaving the honest dynamics and first order in agreement. Here `evolve_tdse(make_driven_H(0.9, 1.0, 0.01), [1,0], 20.0)` gives $|\psi_1|^2=7.14\times10^{-3}$ against `first_order_probability(...)`$=7.17\times10^{-3}$ — matching to $\sim0.4\%$, the residual being the dropped Bloch–Siegert physics.

### P7.  Stimulated emission and the laser  *(Griffiths 3e §11.2.2, p.525)*
An atom in the upper state is hit by resonant light. (a) Compared with the
upward (absorption) transition from the lower state, how likely is the downward
(emission) transition? (b) Why does laser amplification require a *population
inversion*?
*Answer:* (a) **Exactly equal** — the formula is symmetric under $a\leftrightarrow
b$ (Einstein's stimulated emission: one photon in, two out). (b) Absorption (costs
a photon) competes with stimulated emission (creates one); net gain needs more
atoms up than down. *(The quantized-field treatment — spontaneous emission,
Einstein $A/B$, cavity QED — is the bridge to `~QO-03`, not yet built.)*
*Check:* conceptual; the equal up/down probability is the $a\leftrightarrow b$
symmetry of `sinusoidal_probability` (swap which level is initial).

**Solution.** (a) The probability carries $|V_{fi}|^2=|\langle f|H'|i\rangle|^2$ with $H'=-qE_0z\cos\omega t$ Hermitian, so $|V_{ba}|=qE_0|\langle b|z|a\rangle|=qE_0|\langle a|z|b\rangle|=|V_{ab}|$. Absorption ($a\to b$) and stimulated emission ($b\to a$) thus ride the *same* resonance line of §4, with identical peak height $|V_{fi}|^2t^2/4$ — a resonant photon is exactly as likely to drive the atom down (emitting a second, coherent photon) as up. (b) The net upward rate $\propto(N_a-N_b)$: absorption consumes photons while stimulated emission creates them, so amplification (gain $>$ loss) needs $N_b>N_a$, a **population inversion**. Operationally this is just that $|V_{fi}|^2$ in `sinusoidal_probability` is invariant under $a\leftrightarrow b$, so the up and down probabilities coincide.

### P8.  Fermi's golden rule: rate and its scaling  *(Griffiths 3e §11.4, Eq. 11.81, p.539)*
A discrete state is coupled with constant matrix element $V$ to a continuum of
density $\rho(E_f)$ at the resonant energy. (a) State the transition rate.
(b) How does the survival probability behave at short vs intermediate times?
(c) How does $\Gamma$ change if you double $V$, or double $\rho$?
*Answer:* (a) $\Gamma=\dfrac{2\pi}{\hbar}|V|^2\rho(E_f)$. (b) Short times: the
total transition probability is **linear in $t$** with slope $\Gamma$;
intermediate times: $P_i(t)\approx e^{-\Gamma t}$ (exponential decay at that rate).
(c) $\Gamma\propto|V|^2$ (×4 if $V$ doubles) and $\propto\rho$ (×2 if $\rho$ doubles).
*Check:* `golden_rule_rate(0.0309, 50.0)` $=0.3000$; the slope of
`band_first_order_probability` recovers it, and the exact band dynamics decays at
$\Gamma$. (`test_golden_rule_linear_in_time`, `test_golden_rule_scaling`,
`test_golden_rule_exponential_decay`.)

**Solution.** (a) Summing the §4 sinc² over a continuum of density $\rho$, the narrow resonant slice dominates and the rate settles to **Fermi's golden rule**
$$\Gamma=\frac{2\pi}{\hbar}\,|V|^2\,\rho(E_f).$$
(b) Short times: the band-summed first-order probability $P_{\text{band}}(t)=\sum_k|c_k^{(1)}|^2$ grows **linearly** with slope $\Gamma$ (first order, no saturation); intermediate times: the exact survival $P_i(t)=|\langle i|e^{-iHt}|i\rangle|^2\approx e^{-\Gamma t}$ — the linear law is the short-time face of the exponential. (c) $\Gamma\propto|V|^2$ (doubling $V$ gives $\times4$) and $\propto\rho$ (doubling $\rho$ gives $\times2$). Here `golden_rule_rate(0.0309, 50.0)`$=2\pi\cdot0.0309^2\cdot50\approx0.3000$, and both the `band_first_order_probability` slope and the exact band decay reproduce it.

### P9.  Selection rules — forbidden transitions  *(Griffiths 3e §11.3.3, p.536 → `~QM-17`)*
Why are most atomic transitions "forbidden," and what does that mean
operationally?
*Answer:* The dipole rate carries $|\langle f|\mathbf r|i\rangle|^2$; parity and
angular-momentum algebra force it to vanish unless $\Delta\ell=\pm1$ and
$\Delta m=0,\pm1$. "Forbidden" means literally $\langle f|H'|i\rangle=0$, hence
$P_{i\to f}=0$ to this order — no amount of driving causes the jump. Worked out in
full in **`~QM-17`**.
*Check:* conceptual; in code a vanishing matrix element gives
`first_order_probability(0.0, w, t) == 0.0` and `golden_rule_rate(0.0, rho) == 0.0`.

**Solution.** To first order (and in the golden rule) the transition probability is proportional to $|\langle f|H'|i\rangle|^2$; for dipole radiation $H'\propto\mathbf r$, so the rate carries $|\langle f|\mathbf r|i\rangle|^2$. Since $\mathbf r$ is **odd** under parity, $\langle f|\mathbf r|i\rangle=0$ unless $\psi_f,\psi_i$ have opposite parity ($\Delta\ell$ odd), and the angular (Wigner–Eckart) integral sharpens this to $\Delta\ell=\pm1$, $\Delta m=0,\pm1$. "Forbidden" therefore means literally $\langle f|H'|i\rangle=0$, hence $P_{i\to f}=0$ to this order — no drive strength causes the jump. In code this is the trivial limit `first_order_probability(0.0, w, t)`$=0.0$ and `golden_rule_rate(0.0, rho)`$=0.0$.
