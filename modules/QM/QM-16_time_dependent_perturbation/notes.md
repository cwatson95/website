# QM-16 — Time-dependent perturbation theory, Rabi & Fermi's golden rule (notes)

Everything in `~QM-03`–`~QM-15` has been *quantum statics*: the potential is
independent of time, so the Schrödinger equation separates, the wiggle factor
$e^{-iE_nt/\hbar}$ cancels in $|\Psi|^2$, and **the occupation probabilities never
change** — no transitions (Griffiths 3e Ch. 11 opener, p.510). To get a *quantum
jump* between levels we must turn on a **time-dependent** piece of the
Hamiltonian, $H'(t)$. When $H'$ is small we can treat it perturbatively; the
machinery and its headline application (emission/absorption of radiation) are the
subject of Griffiths 3e Ch. 11 *Quantum Dynamics* (p.510).

Natural units throughout: $\hbar=1$ (energies are angular frequencies, rates are
inverse times). $i$ = initial state, $f$ = final state, and
$\omega_{fi}\equiv(E_f-E_i)/\hbar$ is the **Bohr (transition) frequency**.

## 1. The two-level system, exactly (Griffiths §11.1, p.512)

Take two unperturbed eigenstates, $H_0|a\rangle=E_a|a\rangle$,
$H_0|b\rangle=E_b|b\rangle$, orthonormal. Any state is
$|\Psi(t)\rangle=c_a(t)e^{-iE_at}|a\rangle+c_b(t)e^{-iE_bt}|b\rangle$ — the explicit
exponentials are the "free" wiggle that would be there even without $H'$, so
$c_a,c_b$ carry only the *transition* dynamics (Griffiths §11.1.1, Eq. 11.10,
p.513). Plugging into $i\,\partial_t|\Psi\rangle=(H_0+H')|\Psi\rangle$ and taking
inner products with $\langle a|,\langle b|$ gives the **exact** coupled equations
(Griffiths Eqs. 11.14–11.15, p.513). With the diagonal matrix elements vanishing
(the generic case, $H'_{aa}=H'_{bb}=0$; Griffiths Eq. 11.16, p.514):
$$\dot c_a=-\tfrac{i}{\hbar}H'_{ab}\,e^{-i\omega_0 t}\,c_b,\qquad
\dot c_b=-\tfrac{i}{\hbar}H'_{ba}\,e^{+i\omega_0 t}\,c_a,$$
where $\omega_0=\omega_{ba}=(E_b-E_a)/\hbar$ (Griffiths Eqs. 11.17–11.18, p.514).
This pair *is* the Schrödinger equation for a two-level system — no approximation
yet. For a **constant** coupling it is exactly solvable (Griffiths Prob. 11.3,
p.514): the result is **Rabi flopping**, derived in §3.

In code, exact two-level (and many-level) evolution is `evolve(H, psi0, t)` =
$e^{-iHt}|\psi_0\rangle$ via eigendecomposition; the honest time-dependent driven
case is `evolve_tdse` (`test_evolve_unitary_and_consistent`).

## 2. First-order perturbation theory: the master amplitude (Griffiths §11.1.2, p.516)

If $H'$ is small, solve the coupled equations by iteration. Start in the lower
state, $c_a(0)=1,\,c_b(0)=0$. **Zeroth order** ignores $H'$ entirely:
$c_a^{(0)}=1$, $c_b^{(0)}=0$ (Griffiths Eq. 11.20, p.516). **First order** inserts
the zeroth-order values on the right of $\dot c_b$ and integrates (Griffiths
Eq. 11.21, p.516):
$$\boxed{\;c_f^{(1)}(t)=-\frac{i}{\hbar}\int_0^t\langle f|H'(t')|i\rangle\,
e^{i\omega_{fi}t'}\,dt'\;}$$
and the first-order **transition probability** is
$$P_{i\to f}(t)=\bigl|c_f^{(1)}(t)\bigr|^2.$$
This is the central formula of the whole chapter. (Higher orders insert the
$n$-th approximation back into the right-hand side, picking up one more factor of
$H'$ each time — Griffiths Eqs. 11.22–11.25, p.516–517, with the nice "transition
at intermediate time" picture, Fig. 11.1.)

A useful closed form for a **constant** coupling $V_{fi}$ switched on over
$[0,t]$: the integral is elementary,
$$P_{i\to f}^{(1)}(t)=|V_{fi}|^2\,\frac{4\sin^2(\omega_{fi}t/2)}{\omega_{fi}^2}.$$
`first_order_amplitude(matrix_element, omega_fi, t)` evaluates the boxed integral
numerically for *any* time profile (constant, kick, or sinusoid) and
`first_order_probability` squares it; both are checked against the closed form
(`test_first_order_amplitude_constant_closed_form`,
`test_first_order_amplitude_callable_matches_constant`).

## 3. Rabi oscillations: the exact two-level solution (Griffiths Prob. 11.9, p.522)

First-order PT breaks down once $P$ approaches 1. For the two-level system we can
do better. In the rotating frame (rotating-wave approximation for a sinusoidal
drive, or simply a constant coupling) the $2\times2$ Hamiltonian is
*time-independent*,
$$H=\frac{1}{2}\begin{pmatrix}\delta & \Omega_R\\[2pt]\Omega_R & -\delta\end{pmatrix}
=\frac{\Omega_R}{2}\sigma_x+\frac{\delta}{2}\sigma_z,$$
with $\Omega_R$ the **Rabi frequency** (drive amplitude $\times$ dipole matrix
element) and $\delta=\omega-\omega_{fi}$ the **detuning**. Evolving $|i\rangle=(1,0)$
with $e^{-iHt}$ and reading $|\langle f|\psi(t)\rangle|^2$ gives the **generalized
Rabi formula** (Griffiths Eq. 11.37, p.522):
$$\boxed{\;P_{i\to f}(t)=\frac{\Omega_R^2}{\Omega_R^2+\delta^2}\,
\sin^2\!\left(\frac{\sqrt{\Omega_R^2+\delta^2}}{2}\,t\right)\;}$$
Read off three facts, all verified against the dynamics
(`test_rabi_formula_matches_exact_dynamics`,
`test_rabi_resonance_full_inversion`):

- **On resonance** ($\delta=0$): $P=\sin^2(\Omega_R t/2)$ reaches **1** — a
  *complete population inversion* — at $t=\pi/\Omega_R$. This is how a $\pi$-pulse
  flips a qubit.
- **Off resonance**: the amplitude is capped at $\Omega_R^2/(\Omega_R^2+\delta^2)<1$
  — you can *never* fully invert a detuned two-level system, and the flopping
  speeds up to the **generalized Rabi frequency** $\sqrt{\Omega_R^2+\delta^2}$.
- It **never exceeds 1** — unlike the first-order estimate, which is only the
  small-$P$ shadow of this exact result.

**First-order PT is the weak/short-time limit.** With constant rotating-frame
coupling $V_{fi}=\Omega_R/2$ and Bohr frequency $-\delta$, the boxed amplitude of
§2 gives $P^{(1)}=(\Omega_R^2/\delta^2)\sin^2(\delta t/2)$. When $\Omega_R\ll|\delta|$
the exact denominator $\Omega_R^2+\delta^2\to\delta^2$ and the two agree; and for
short times *any* detuning gives $P\to\Omega_R^2t^2/4$. Both limits are checked in
`test_first_order_reproduces_rabi_weak_and_short`.

## 4. Sinusoidal perturbations and resonance (Griffiths §11.1.3, p.520)

The physically important $H'$ oscillates: $H'(t)=V\cos(\omega t)$ (e.g. an atom in
a light wave, §5). The matrix element is $\langle f|H'|i\rangle=V_{fi}\cos\omega t
=\tfrac12V_{fi}(e^{i\omega t}+e^{-i\omega t})$. Feeding this into the first-order
amplitude gives two terms with denominators $\omega_{fi}\pm\omega$ (Griffiths
Eq. 11.32, p.520). Near resonance, $\omega\approx\omega_{fi}$, only the
$\omega_{fi}-\omega$ term is large (the **rotating-wave approximation**; dropping
the other), and the transition probability is (Griffiths Eq. 11.35, p.520):
$$\boxed{\;P_{i\to f}(t)=|V_{fi}|^2\,
\frac{\sin^2\!\big[(\omega_{fi}-\omega)t/2\big]}{(\omega_{fi}-\omega)^2}\;}$$
As a function of the **drive frequency** $\omega$ this is a $\mathrm{sinc}^2$ line
centred on resonance (Griffiths Fig. 11.5, p.521):

- the **peak is at $\omega=\omega_{fi}$**, with central height $|V_{fi}|^2t^2/4$
  (the $\delta\to0$ limit; `sinusoidal_probability` handles it without dividing by
  zero) — `test_sinusoidal_resonance_peak`;
- the **peak grows like $t^2$** and the line **narrows like $1/t$**, with first
  zeros at $\omega=\omega_{fi}\pm2\pi/t$ — `test_sinusoidal_sinc_squared`. (The
  longer you drive, the sharper and more frequency-selective the resonance —
  exactly the energy–time complementarity behind spectroscopic linewidths.)

This RWA result is not just a perturbative artifact: integrating the **honest,
full** lab-frame $H(t)=H_0+V\cos(\omega t)\,\sigma_x$ with `evolve_tdse` (no RWA,
no weak-coupling assumption) reproduces the full first-order amplitude across
detunings, and the RWA formula on top of that near resonance
(`test_sinusoidal_pt_vs_tdse`). Off resonance and at strong driving the dropped
counter-rotating term is the Bloch–Siegert correction.

## 5. Emission and absorption of radiation (Griffiths §11.2, p.523)

An atom in a long-wavelength light wave sees a spatially uniform, oscillating
electric field; the perturbation is the dipole coupling $H'=-qE_0z\cos(\omega t)$
(Griffiths §11.2.1, Eq. 11.38, p.524) — precisely the sinusoidal perturbation of
§4 with $V_{ba}=-qE_0\langle b|z|a\rangle$ (Griffiths Eq. 11.41, p.524). So §4's
resonance formula governs light–matter interaction (Griffiths §11.2.2, p.525):

- **Absorption.** Starting in the lower state, the atom is driven up, absorbing
  energy $\hbar\omega_0$ — "absorbing a photon."
- **Stimulated emission.** Starting in the *upper* state, the *same* formula
  drives it *down*, with **equal** probability — one photon in, two out. This is
  Einstein's prediction and the principle of the **laser** (Light Amplification by
  Stimulated Emission of Radiation); it requires a **population inversion**
  (Griffiths p.525). *(The full laser/quantized-field story is the bridge to
  `~QO-03`, not yet built.)*
- **Spontaneous emission.** Even with no field present an excited atom decays —
  this needs the quantized field (or Einstein's $A/B$ relations); Griffiths
  develops it in §11.3.

**Selection rules.** The transition rate carries the matrix element
$\langle f|z|i\rangle$ (or $\mathbf r$); by parity and angular-momentum algebra
*most* of these vanish, leaving the dipole **selection rules**
$\Delta\ell=\pm1$, $\Delta m=0,\pm1$ (Griffiths §11.3.3 *Selection Rules*, p.536).
"A transition is forbidden" means exactly "$\langle f|H'|i\rangle=0$, so
$P_{i\to f}=0$." This is taken up in full in **`~QM-17`**.

## 6. Fermi's golden rule (Griffiths §11.4, p.538)

Sections 1–5 treated two *discrete* states. Often the final state lies in a
**continuum** — e.g. photoionization kicks the electron into scattering states
(Griffiths §11.4, p.538). We cannot ask for the probability of one precise final
state; we sum §4's result over a band of finals with **density of states**
$\rho(E)$ (the number of states per unit energy), $dn=\rho\,dE$ (Griffiths
Eq. 11.79, p.538). Two regimes:

- **Short times:** the $\mathrm{sinc}^2$ is broad, the sum is dominated by its
  $t^2$ peak times the width $1/t$, giving a probability **linear in $t$**
  (Griffiths p.538) — a *constant rate*.
- The oscillation "washes out" and the transition rate becomes time-independent:
$$\boxed{\;\Gamma=\frac{2\pi}{\hbar}\,\bigl|\langle f|H'|i\rangle\bigr|^2\,
\rho(E_f)\;}$$
**Fermi's golden rule** (Griffiths Eq. 11.81, p.539): the rate is the *matrix
element squared* (all the dynamics) times the *density of states* (how many roads
are open — "the more roads, the faster the traffic," Griffiths p.539).

**Numerical demonstration.** Model the continuum as a dense, evenly spaced band:
one discrete $|i\rangle$ coupled with constant $V$ to $N$ final states spaced by
$\Delta E$ (so $\rho=1/\Delta E$), the Wigner–Weisskopf "star" Hamiltonian
(`band_hamiltonian`). Two independent checks:

1. **Linear in $t$ (the literal derivation).** The first-order probability summed
   over the band, $\sum_k|c_k^{(1)}|^2$ (`band_first_order_probability`), grows
   *linearly*; its slope matches $\Gamma=2\pi|V|^2\rho$ to $\sim0.1\%$, and scales
   correctly as $|V|^2$ and as $\rho$ — `test_golden_rule_linear_in_time`,
   `test_golden_rule_scaling`.
2. **Exponential decay (the exact dynamics).** In the wide, dense regime
   $W\gg\Gamma\gg\Delta E$ (bandwidth $W=N\Delta E$, before the recurrence time
   $2\pi/\Delta E$), the *exact* survival probability $P_i(t)=|\langle
   i|e^{-iHt}|i\rangle|^2$ decays as $e^{-\Gamma t}$ with the same $\Gamma$ (to a
   few percent; the residual is the finite-bandwidth correction) —
   `test_golden_rule_exponential_decay`. The linear-in-$t$ law is the short-time
   face of this exponential.

Griffiths' Example 11.2 (p.539) uses the *same* rule with plane-wave finals and
box-normalized $\rho$ to rederive the Born scattering cross-section — the golden
rule and the first Born approximation (`~QM-15` neighbourhood) are the same
matrix element seen two ways.

---
### Where this sits
`~QM-15` perturbs the *spectrum* of a static $H$; this module perturbs *in time*
and gets **transitions** between those levels. The amplitude $c_f^{(1)}$ becomes a
*probability* via the Born rule of `~QM-06`; the two-level/Rabi language is that
of `~QM-11`. Which transitions survive the matrix element is `~QM-17` (selection
rules); the emission/absorption physics, done properly with a quantized field, is
the bridge to `~QO-03` (lasers, cavity QED) when it is built.
