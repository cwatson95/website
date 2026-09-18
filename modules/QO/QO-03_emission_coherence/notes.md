# QO-03 — Emission & Coherence: Spontaneous/Stimulated Emission & Laser Physics (notes)

In 1917, eight years before quantum mechanics existed, Einstein extracted the
**spontaneous** and **stimulated** emission rates of an atom from a single
demand: a gas of atoms in a radiation bath must settle into the **Planck**
spectrum. That argument fixes the ratio of the two emission coefficients, names
the process that makes a **laser** possible, and — read backwards — explains why
you cannot build one with heat alone. This module walks the chain from Einstein's
$A$/$B$ relations to the laser **threshold**, then asks the complementary
question: not *how much* light, but *how coherent* — the correlation functions
$g^{(1)}$ and $g^{(2)}$ that tell thermal, laser, and single-photon light apart.

Citation key (full details in `refs.md`): **S&Z** = Scully & Zubairy,
*Quantum Optics* (Cambridge, 1997), cited at chapter/section level. Companion:
`~QM-16` (the emission/absorption *rate* from time-dependent perturbation theory),
`~PK-04` (excimer/laser kinetics — the photon side of KrF\* chemistry).

## 1. Three ways light and atoms exchange energy
Take two atomic levels, lower $1$ and upper $2$, energy gap $h\nu=E_2-E_1$, bathed
in radiation of **spectral energy density** $\rho(\nu)$. Einstein posited three
processes, each a transition rate per atom [S&Z Ch. 1; Sect. 5.6]:
$$W_{\text{spont}}=A_{21},\qquad
  W_{\text{stim}}=B_{21}\,\rho(\nu),\qquad
  W_{\text{abs}}=B_{12}\,\rho(\nu).$$
**Spontaneous** emission ($A_{21}$) needs no field; **stimulated** emission
($B_{21}\rho$) and **absorption** ($B_{12}\rho$) are field-driven and, crucially,
*proportional to the same $\rho$*. The stimulated photon is emitted into the very
mode that triggered it — same frequency, direction, phase — which is what makes
amplification **coherent**. Code: `einstein_A_over_B`.

## 2. Detailed balance against thermal populations
In equilibrium at temperature $T$ the level populations are Boltzmann-distributed
(`~SM-03`),
$$\frac{N_2}{N_1}=\frac{g_2}{g_1}\,e^{-h\nu/k_BT}\ (<1),$$
with degeneracies $g_1,g_2$ — note there is **no thermal inversion**: a hot gas
never puts more atoms up than down. **Detailed balance** sets the up-rate equal to
the down-rate, $N_1B_{12}\rho=N_2\!\left(A_{21}+B_{21}\rho\right)$, and solving for
the field [S&Z Ch. 1]:
$$\rho(\nu)=\frac{A_{21}}{B_{12}\,(N_1/N_2)-B_{21}}
          =\frac{A_{21}/B_{21}}{\dfrac{g_1B_{12}}{g_2B_{21}}\,e^{h\nu/k_BT}-1}.$$
Code: `boltzmann_population_ratio`, `detailed_balance_energy_density`.

## 3. The Einstein relations and the Planck spectrum
This $\rho$ can equal **Planck's law at every $T$** only if two relations hold —
Einstein read them straight off the comparison, and with them §2 collapses to the
Planck spectrum [S&Z Ch. 1]:
$$\boxed{\ \frac{A_{21}}{B_{21}}=\frac{8\pi h\nu^3}{c^3},\qquad g_1B_{12}=g_2B_{21}\ }
\;\Longrightarrow\;
\rho_{\text{Planck}}(\nu,T)=\frac{8\pi h\nu^3}{c^3}\,\frac{1}{e^{h\nu/k_BT}-1}.$$
The first relation fixes the *absolute* spontaneous rate from the stimulated one; the
second makes absorption and stimulated emission equal-strength (per state). Code:
`einstein_A_over_B`, `planck_spectral_energy_density`; the closure
$\rho_{\text{db}}=\rho_{\text{Planck}}$ (independent of $A_{21},g_1,g_2$) is checked
in `test_detailed_balance_reproduces_planck`.

## 4. Stimulated vs. spontaneous — why heat won't lase
Dividing the two emission rates in equilibrium uses only the first Einstein relation:
$$\boxed{\ \frac{W_{\text{stim}}}{W_{\text{spont}}}
  =\frac{B_{21}\rho}{A_{21}}=\frac{1}{e^{h\nu/k_BT}-1}\ }$$
The crossover is at $h\nu=k_BT\ln 2$. At **optical/UV** frequencies and room
temperature $h\nu\gg k_BT$ (for the 248 nm KrF line, $h\nu/k_BT\approx190$), so the
ratio is $\sim10^{-84}$: spontaneous emission dominates by astronomical factors. To
make stimulated emission win you must abandon equilibrium — create a **population
inversion** and recycle photons in a **cavity**. (At radio frequencies the ratio is
$\gg1$, the maser/Rayleigh–Jeans regime.) Code: `stimulated_to_spontaneous`.

## 5. Inversion, gain, and the laser rate equations
Net stimulated power along a beam $\propto (N_2-\tfrac{g_2}{g_1}N_1)\,B_{21}$: the
medium **amplifies** only with an **inversion** $N_2>\tfrac{g_2}{g_1}N_1$. Couple
the inversion $N$ to the cavity photon number $n$ via single-mode rate equations
[S&Z Sect. 5.5]:
$$\frac{dN}{dt}=R-\gamma N-G\,N n,\qquad
  \frac{dn}{dt}=G\,N n-\kappa\,n,$$
with pump rate $R$, inversion relaxation $\gamma$, stimulated coefficient $G$, and
cavity loss $\kappa$. Code: `laser_rate_rhs`.

## 6. The laser threshold and gain clamping
Set $\dot N=\dot n=0$. The photon equation factors as $n\,(GN-\kappa)=0$: either
$n=0$, or the inversion is pinned at $N_{\text{th}}=\kappa/G$. The result is a sharp
**threshold** at pump $R_{\text{th}}=\gamma\kappa/G$ [S&Z Sect. 11.2]:
$$\boxed{\ n=\begin{cases}0, & R\le R_{\text{th}}\\[4pt]
  \dfrac{R-R_{\text{th}}}{\kappa}, & R> R_{\text{th}}\end{cases}\qquad
  N=\begin{cases}R/\gamma, & R\le R_{\text{th}}\\[4pt]
  \kappa/G\ (\text{clamped}), & R> R_{\text{th}}\end{cases}}$$
Below threshold the pump just builds inversion (no coherent light); above it the
inversion **clamps** and every extra pump quantum becomes a laser photon — the
turn-on is the order parameter of a **second-order phase transition** [S&Z Sect.
11.6]. Code: `laser_threshold`, `laser_steady_state`.

## 7. First-order coherence — fringe visibility
Emission rates say nothing about *coherence*. The normalized **first-order**
correlation of the field [S&Z Sect. 4.3] is
$$g^{(1)}(\tau)=\frac{\langle E^{*}(t)E(t+\tau)\rangle}{\langle|E(t)|^2\rangle},
  \qquad
  \mathcal{V}=\frac{I_{\max}-I_{\min}}{I_{\max}+I_{\min}}=\bigl|g^{(1)}(\tau)\bigr|.$$
$|g^{(1)}|$ *is* the fringe **visibility** in a Michelson/Young interferometer:
$1$ for monochromatic light, decaying over the coherence time $\tau_c\sim1/\Delta\nu$.
But $g^{(1)}$ alone **cannot** separate filtered thermal light from laser light —
both can show $|g^{(1)}|=1$. For that we need intensity correlations.

## 8. Second-order coherence — bunching vs. antibunching
The **second-order** correlation at zero delay measures intensity (photon-pair)
fluctuations [S&Z Sect. 4.4]:
$$\boxed{\ g^{(2)}(0)=\frac{\langle :\!\hat I^2\!:\rangle}{\langle\hat I\rangle^2}
  =\frac{\langle\hat a^\dagger\hat a^\dagger\hat a\hat a\rangle}{\langle\hat a^\dagger\hat a\rangle^2}
  =\frac{\langle n(n-1)\rangle}{\langle n\rangle^2}\ }$$
Three statistics, three signatures (Hanbury-Brown–Twiss, antibunching):
$$
\begin{array}{lcl}
\text{thermal / chaotic (Bose–Einstein)} & g^{(2)}(0)=2 & \text{(bunching)}\\
\text{coherent / laser (Poisson)} & g^{(2)}(0)=1 & \text{(random)}\\
\text{Fock }|n\rangle & g^{(2)}(0)=1-\tfrac1n & \text{(}=0\text{ for }n{=}1\text{, antibunching)}
\end{array}
$$
$g^{(2)}(0)<1$ is **impossible classically** — a witness of nonclassical, single-photon
light (`~QO-05`). Code: `g2_thermal`, `g2_coherent`, `g2_fock`, `g2_from_distribution`
(the last computes $g^{(2)}(0)$ from any photon-number distribution and reproduces
$2$, $1$, $1-1/n$ — `test_g2_from_distribution_matches_closed_forms`).

## Where this goes
- `~QM-16` — the emission/absorption *rate* $\propto|\langle f|H'|i\rangle|^2$ from
  time-dependent perturbation theory; here it becomes Einstein's $B$ coefficient, and
  spontaneous emission is its quantized-field completion (Weisskopf–Wigner, S&Z 6.3).
- `~PK-04` — the laser/excimer kinetics in this repo: KrF\* emits at 248 nm, the
  inversion is *automatic* (bound–free lower state), and the gain feeds the rate
  equations of §5–6. This module is the photon physics behind that chemistry.
- `~QO-02` — atom–field Rabi/Jaynes–Cummings dynamics that underlie $A$, $B$, and the
  coherence of the emitted light; `~QO-05` — squeezing and the $g^{(2)}<1$ frontier.
