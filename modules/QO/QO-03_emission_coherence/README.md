# QO-03 — Emission & Coherence: Spontaneous/Stimulated Emission & Laser Physics

Third module of the **QUANTUM & NONLINEAR OPTICS** trunk (see `modules/topic_network.txt`).
The bridge from the quantum-jump *rate* of `~QM-16` to the laser physics of the
user's KrF excimer work (`~PK-04`).

- **Prerequisites:** `~QM-16` (time-dependent perturbation theory — the
  emission/absorption rate $\propto|\langle f|H'|i\rangle|^2$ that becomes the
  Einstein $B$ coefficient), `~SM-03` (Boltzmann factor / thermal populations),
  `~QO-01` (modes & photon number). Helpful: `~QO-02` (atom–field Rabi dynamics).
- **Cross-links:** `~PK-04` (excimer/laser kinetics — KrF\* 248 nm gain, the photon
  side of the repo's plasma chemistry), `~QO-02` (atom–field interaction),
  `~QO-05` (squeezing & the nonclassical $g^{(2)}<1$ frontier).

## Scope
Einstein's 1917 argument (predating quantum mechanics) demands that a gas of atoms
in a radiation bath relax to the **Planck** spectrum, and from that single
requirement extracts the rates of **spontaneous** emission ($A_{21}$),
**stimulated** emission ($B_{21}\rho$) and **absorption** ($B_{12}\rho$). Detailed
balance against the Boltzmann populations fixes the **Einstein relations**
$A_{21}/B_{21}=8\pi h\nu^3/c^3$ and $g_1B_{12}=g_2B_{21}$, and the ratio of
stimulated to spontaneous emission in equilibrium is $1/(e^{h\nu/k_BT}-1)$ — tiny
($\sim10^{-84}$) at the 248 nm KrF wavelength and room temperature, which is exactly
why a laser needs a **population inversion** and a cavity rather than heat. Feeding
the inversion into single-mode **rate equations** $\dot N=R-\gamma N-GNn$,
$\dot n=GNn-\kappa n$ gives a sharp **threshold** $R_{\text{th}}=\gamma\kappa/G$: the
photon number is zero below it and rises linearly above, while the gain **clamps**
the inversion at $\kappa/G$ — the order-parameter turn-on of a second-order phase
transition. The complementary question — how *coherent* the light is — is answered
by the correlation functions: $g^{(1)}$ (fringe visibility) and the
intensity-fluctuation $g^{(2)}(0)$, which equals **2** for thermal/chaotic light
(bunching), **1** for coherent/laser light (Poissonian), and **0** for a
single-photon Fock state (antibunching, $1-1/n$), the latter a witness of
nonclassical light with no classical analogue.

## Operations — `code/emission_coherence.py`

| call | meaning | reference |
|------|---------|-----------|
| `einstein_A_over_B(nu)` | $A_{21}/B_{21}=8\pi h\nu^3/c^3$ | S&Z Ch.1 / §6.3 |
| `planck_spectral_energy_density(nu, T)` | $\rho=(8\pi h\nu^3/c^3)/(e^{h\nu/k_BT}-1)$ | S&Z Ch.1 |
| `boltzmann_population_ratio(nu, T, g1, g2)` | $N_2/N_1=(g_2/g_1)e^{-h\nu/k_BT}$ | S&Z §5.6; `~SM-03` |
| `detailed_balance_energy_density(nu, T, g1, g2, A21)` | rate-balance $\rho$ ($=$ Planck, by the Einstein relations) | S&Z Ch.1 |
| `stimulated_to_spontaneous(nu, T)` | $B_{21}\rho/A_{21}=1/(e^{h\nu/k_BT}-1)$ | S&Z §5.6 |
| `laser_threshold(gain, kappa, gamma)` | $R_{\text{th}}=\gamma\kappa/G$ | S&Z §11.2 |
| `laser_steady_state(pump, gain, kappa, gamma)` | steady $(N,n)$: $n{=}0$ below, $n{=}(R{-}R_{\text{th}})/\kappa$ above | S&Z §5.5, Ch.11 |
| `laser_rate_rhs(state, pump, gain, kappa, gamma)` | $(\dot N,\dot n)$ rate equations | S&Z §5.5 |
| `g2_thermal()` / `g2_coherent()` / `g2_fock(n)` | $g^{(2)}(0)=2$ / $1$ / $1-1/n$ | S&Z §4.4 |
| `g2_from_distribution(p_n)` | $g^{(2)}(0)=\langle n(n-1)\rangle/\langle n\rangle^2$ | S&Z §4.5 |

Constants (SI, defined locally): `H_PLANCK`, `C_LIGHT`, `K_B`.

## Use
```python
from emission_coherence import (einstein_A_over_B, stimulated_to_spontaneous,
                                laser_threshold, laser_steady_state,
                                g2_thermal, g2_coherent, g2_fock)

nu = 2.998e8 / 248e-9                       # KrF excimer line, 248 nm (~PK-04)
einstein_A_over_B(nu)                       # 1.09e-12 J s / m^3  (= 8 pi h nu^3/c^3)
stimulated_to_spontaneous(nu, 300.0)        # ~1e-84  -> spontaneous wins; need inversion

laser_threshold(gain=1.0, kappa=1.0, gamma=1.0)   # 1.0
laser_steady_state(0.5)                     # (0.5, 0.0)   below threshold: dark
laser_steady_state(2.0)                     # (1.0, 1.0)   above: inversion clamped, photons on

g2_thermal(), g2_coherent(), g2_fock(1)     # 2.0, 1.0, 0.0  (bunched / coherent / antibunched)
```

## Run
```bash
cd code
python3 emission_coherence.py        # demo: A/B, stim/spont, laser threshold sweep, g2(0) values
python3 test_emission_coherence.py   # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — Einstein's detailed-balance argument, the laser threshold, and the
  $g^{(1)}/g^{(2)}$ coherence functions, each tied to its code function + test
- `code/emission_coherence.py`, `code/test_emission_coherence.py`
- `problems/problems.md` — worked problems (Scully & Zubairy Ch. 1, 4, 5, 11)
- `refs.md` — citation table (Scully & Zubairy, section/chapter level) + cross-links
