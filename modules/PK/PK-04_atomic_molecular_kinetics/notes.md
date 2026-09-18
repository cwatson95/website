# PK-04 — Atomic & Molecular Kinetics — Rate Equations, Excimer Chemistry & EEDF (notes)

A laser-pumped plasma is a bookkeeping problem: dozens of species, each created
and destroyed by electron-impact collisions, heavy-particle chemistry and
radiation. The ledger is a set of **rate equations**; the exchange rate of each
reaction is a **rate coefficient** $k=\langle\sigma v\rangle$, an average of the
cross-section over the **electron energy distribution function (EEDF)**. This is
exactly the machinery of the KrF excimer-laser kinetics simulator in this repo
(`projects/Kinetic_Modeling/KrF_and_LoKI`): a 0-D state vector
$u\in\mathbb{R}^{26}$ of log-transformed densities, integrated by
`run_sim → build_rhs_u → rhs_u` as $\dot n_i=\text{production}-\text{loss}$.

Citation key (full details in `refs.md`): **Rh** = Rhodes (ed.), *Excimer Lasers*;
**Mi** = Michel, *Introduction to Laser–Plasma Interactions*. Cited at
chapter/section level; the Maxwellian $\langle\sigma v\rangle$ machinery is `~SM-06`.

## 1. Coupled rate equations
For a set of species with densities $n_i$, each reaction contributes a term
$+$(production) or $-$(loss). A two-body reaction $a+b\to\dots$ proceeds at rate
$R=k\,n_a n_b$; a three-body reaction $a+b+M\to\dots$ at $R=k_3\,n_a n_b n_M$
[Mi, atomic-processes ch.]:
$$\frac{dn_i}{dt}=\sum_{\text{production}} k\,n_a n_b\;-\;\sum_{\text{loss}} k\,n_i n_c .$$
For numerical stiffness the phantom11 solver evolves the **log** densities
$u_i=\ln n_i$, so $\dot u_i=\dot n_i/n_i$ (BDF/LSODA-stable, positivity-preserving).
Code: `excimer_rhs`, `simulate_krf`.

## 2. The rate coefficient as an EEDF average
A rate coefficient is the flux-weighted average of the cross-section over the
velocity distribution $f(\mathbf v)$ — for electron-impact processes, the **EEDF**
[Mi; cf. `~SM-06` $\langle\sigma v\rangle$]:
$$k=\langle\sigma v\rangle=\int \sigma(v)\,v\,f(\mathbf v)\,d^3v
=\sqrt{\frac{8}{\pi m}}\;(kT)^{-3/2}\!\int_0^\infty \sigma(\varepsilon)\,\varepsilon\,e^{-\varepsilon/kT}\,d\varepsilon ,$$
the right form using a Maxwellian and $\varepsilon=\tfrac12 m v^2$. The Maxwellian
EEDF in energy is
$$F(\varepsilon)=\frac{2}{\sqrt\pi}\,(kT)^{-3/2}\sqrt{\varepsilon}\;e^{-\varepsilon/kT},
\qquad \int_0^\infty F\,d\varepsilon=1,\quad \langle\varepsilon\rangle=\tfrac32 kT .$$
Code: `rate_coefficient_maxwellian`, `maxwell_energy_pdf`. **Real swarm solvers
do not assume a Maxwellian:** LoKI (LisbOn KInetics Monte Carlo) computes a
*non-Maxwellian* $F(\varepsilon)$ from the electron kinetic equation (`~PK-01`)
and tabulates $k(E/N)$ vs the reduced field; phantom11 reads those tables at
$E/N=\texttt{CHOW\_EN\_TD\_DEFAULT}=51\ \text{Td}$ (`phantom11/loki_tables.py`).

## 3. Threshold cross-section → Arrhenius
Most inelastic processes have a **threshold** $E_{\rm th}$ (the excitation or
ionization energy). For a step cross-section $\sigma(\varepsilon)=\sigma_0$ for
$\varepsilon\ge E_{\rm th}$, the Maxwellian average of §2 integrates in closed form:
$$k(T)=\sigma_0\,\langle v\rangle\Big(1+\frac{E_{\rm th}}{kT}\Big)e^{-E_{\rm th}/kT}
\;\approx\;\sigma_0\,\langle v\rangle\,\frac{E_{\rm th}}{kT}\,e^{-E_{\rm th}/kT}
\quad (E_{\rm th}\gg kT),$$
with $\langle v\rangle=\sqrt{8kT/\pi m}$. The dominant factor $e^{-E_{\rm th}/kT}$
is the **Arrhenius** law,
$$k(T)=A\,e^{-E_a/kT},$$
the threshold $E_{\rm th}$ playing the role of the activation energy $E_a$. Code:
`rate_coefficient_step_closed_form`, `arrhenius`.

## 4. Detailed balance and the Saha equation
In thermodynamic equilibrium every forward reaction is balanced by its reverse
(**detailed balance**): ionization $A\to A^++e$ is balanced by recombination
$A^++e\to A$. Equating the two rates fixes the equilibrium ionization ratio — the
**Saha equation** [Mi, ionization ch.]:
$$\frac{n_e\,n_i}{n_0}=\frac{2g_i}{g_0}\Big(\frac{2\pi m_e kT}{h^2}\Big)^{3/2}e^{-E_{\rm ion}/kT}.$$
The factor $2$ is the electron-spin degeneracy and $(2\pi m_e kT/h^2)^{3/2}$ is the
quantum concentration. Writing $n_e=n_i$ and $n_0=n_{\rm tot}-n_i$ gives a
quadratic for the ionization fraction $x=n_i/n_{\rm tot}$, which rises from $0$
(cold) to $1$ (hot). Code: `saha_ratio`, `saha_ionization_fraction`.

## 5. The KrF excimer scheme
KrF* is an **excimer** — bound only in the excited state. The dominant channels in
phantom11 (`reactions.py`; labels $r_{25}$ etc. are the code's reaction ids) are
$$\begin{aligned}
\text{pump:}\quad & e+\mathrm{Kr}\to\mathrm{Kr}^*+e \\
r_{25}\ \text{harpoon:}\quad & \mathrm{Kr}^*+\mathrm{F_2}\to\mathrm{KrF}^*+\mathrm{F} \\
r_{26}\ \text{ion channel:}\quad & \mathrm{Kr}^++\mathrm{F}^-+M\to\mathrm{KrF}^*+M \\
r_{31}\ \text{radiative:}\quad & \mathrm{KrF}^*\to\mathrm{Kr}+\mathrm{F}+h\nu\;(248\,\text{nm}) \\
r_{32}\ \text{quench:}\quad & \mathrm{KrF}^*+\mathrm{F_2}\to\mathrm{Kr_2F}^*+\mathrm{F}
\end{aligned}$$
Because the **lower state $(\mathrm{Kr}+\mathrm{F})$ is repulsive**, it dissociates
in $\sim$ps and is never populated — so emission is **bound–free** and there is no
ground-state reabsorption. That is what makes a population inversion (and laser
gain at 248 nm) automatic (`~QO-03`).

## 6. The 0-D KrF* rate equations
The teaching cartoon keeps the harpoon, radiative and quench channels plus a
Gaussian discharge pump $g(t)$; with rates $r_1=k_{\rm pump}\,g(t)\,n_{\rm Kr}$,
$r_2=k_h n_{\mathrm{Kr}^*}n_{\mathrm F_2}$, $r_3=A\,n_{\mathrm{KrF}^*}$,
$r_4=k_q n_{\mathrm{KrF}^*}n_{\mathrm F_2}$:
$$\begin{aligned}
\dot n_{\mathrm{Kr}^*}&=r_1-r_2, &
\dot n_{\mathrm{KrF}^*}&=r_2-r_3-r_4, \\
\dot n_{\mathrm F_2}&=-r_2, &
\dot n_{\mathrm F}&=r_2+r_3+r_4 .
\end{aligned}$$
KrF* **rises to a peak then decays** (formation outruns the few-ns decay during the
pump, then the precursor $\mathrm{Kr}^*$ drains away). The closed reactions conserve
the heavy-particle (atom) inventories exactly:
$$n_{\mathrm{Kr}}+n_{\mathrm{Kr}^*}+n_{\mathrm{KrF}^*}=\text{const},
\qquad 2\,n_{\mathrm F_2}+n_{\mathrm F}+n_{\mathrm{KrF}^*}=\text{const}.$$
Code: `excimer_rhs`, `simulate_krf` (with `scipy.integrate.solve_ivp`, stiff LSODA).

## 7. Gain and the laser link
Each radiative event emits a 248 nm photon of energy
$$E_\gamma=\frac{hc}{\lambda}=\frac{hc}{248\,\text{nm}}\approx 5.0\ \text{eV}$$
(phantom11 uses $E_{h\nu}=4.999$ eV). The spontaneously emitted photons seed
**stimulated emission**, the code's reaction $r_{30}:\ \mathrm{KrF}^*+\phi\to\dots$
with cross-section $\sigma_{\rm stim}$; the small-signal gain is
$g_0=\sigma_{\rm stim}\,\Delta N$ with the inversion $\Delta N\simeq n_{\mathrm{KrF}^*}$
(no lower-state population). The Einstein-coefficient machinery behind spontaneous
$A$, stimulated $B$ and gain is `~QO-03`. Code: `photon_energy_eV`.

## Where this goes
- `~QO-03` — spontaneous/stimulated emission, Einstein coefficients, laser gain: the
  photon side of the same KrF* kinetics.
- `~SM-06` — kinetic theory and the Maxwellian $\langle\sigma v\rangle$ that §2–3 specialize.
- `~PK-01` — the electron kinetic equation that produces the (non-Maxwellian) EEDF
  LoKI feeds to these rate coefficients.
- The live code: `projects/Kinetic_Modeling/KrF_and_LoKI` — `phantom11/reactions.py`
  (the real $r_{25},r_{26},r_{31},r_{32}$), `loki_tables.py` (the EEDF tables),
  `_rhs_u_body.py` (the full 23-species $\dot n_i=$ production $-$ loss).
