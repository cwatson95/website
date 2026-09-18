# QO-04 — Open Quantum Systems: Master Equations & Decoherence

Fourth module of the **QUANTUM & NONLINEAR OPTICS** trunk (see
`modules/topic_network.txt`). It is the open-system, irreversible sequel to
`~QM-20`'s closed-system density matrix.

- **Prerequisites:** `~QM-20` (the density operator $\rho$ — Tr $\rho=1$,
  Hermitian, positive; the von Neumann equation $i\hbar\dot\rho=[H,\rho]$),
  `~QO-02` (the two-level atom, Rabi frequency $\Omega$), `~QO-03` (the
  spontaneous-emission rate $\gamma$).
- **Cross-links:** `~QM-20` (closed-system limit & decoherence of coherences),
  `~QO-02` (driven atom / Rabi oscillations), `~QO-03` (emission rate, why a
  two-level atom cannot be inverted), `~QO-05` (squeezed reservoirs).

## Scope
A real atom is coupled to the electromagnetic vacuum — a reservoir it cannot
follow. Tracing the reservoir out turns the unitary von Neumann evolution of
`~QM-20` into the **Lindblad (GKSL) master equation**
$\dot\rho=-\tfrac{i}{\hbar}[H,\rho]+\sum_k(L_k\rho L_k^\dagger-\tfrac12\{L_k^\dagger L_k,\rho\})$,
whose **collapse operators** $L_k$ inject irreversible relaxation while keeping
$\rho$ a legitimate state — **completely positive and trace-preserving (CPTP)**:
$\mathrm{Tr}\,\rho=1$, $\rho=\rho^\dagger$, $\rho\succeq0$ for all time.
**Spontaneous emission** is the single jump operator $L=\sqrt\gamma\,\sigma^-$: the
excited population decays as $e^{-\gamma t}$ (the **$T_1$** time $1/\gamma$) while
the **coherence** decays at half that rate, $e^{-\gamma t/2}$ — coherences
collapsing to zero **is decoherence**. Adding population-conserving
**pure dephasing** $L_\phi=\sqrt{\gamma_\phi/2}\,\sigma_z$ gives the textbook
transverse-relaxation relation $1/T_2=1/(2T_1)+1/T_\phi$. Driving the atom and
letting it relax yields the **optical Bloch equations**, whose steady state
saturates at $\rho_{ee}^{\,\mathrm{ss}}\to\tfrac12$ as $\Omega\to\infty$ — a
classical field can equalize but never invert a two-level atom. Everything here is
*verified numerically*: trace, Hermiticity, positivity, the two decay rates, the
$T_2$ law, and both the undriven (ground) and driven (Bloch) steady states.

## Operations — `code/open_systems.py`

| call | meaning | reference |
|------|---------|-----------|
| `density_matrix(psi)` | pure-state $\rho=\|\psi\rangle\langle\psi\|$ | SZ §5.3 |
| `populations(rho)` / `excited_population(rho)` | diagonal $\rho_{ii}$; $\rho_{ee}$ | SZ §5.3 |
| `coherence(rho)` | off-diagonal $\rho_{eg}$ (the $T_2$ observable) | SZ §5.3 |
| `is_hermitian` / `is_positive_semidefinite` / `is_density_matrix` | the CPTP-preserved validity tests | SZ Ch. 8 |
| `commutator(A,B)` / `anticommutator(A,B)` | $[A,B]$, $\{A,B\}$ | — |
| `lindblad_rhs(rho, H, collapse_ops)` | $\dot\rho=-\tfrac{i}{\hbar}[H,\rho]+\sum_k\mathcal D[L_k]\rho$ | SZ Ch. 8 |
| `evolve_lindblad(rho0, H, collapse_ops, times)` | integrate (ravel $\rho$, `solve_ivp`) | SZ Ch. 8 |
| `two_level_hamiltonian(omega_rabi, detuning)` | $H=\hbar\Delta\|e\rangle\langle e\|+\tfrac{\hbar\Omega}{2}\sigma_x$ | SZ Ch. 10 |
| `spontaneous_emission_op(gamma)` | $L=\sqrt\gamma\,\sigma^-$ ($T_1$) | SZ §6.3 |
| `dephasing_op(gamma_phi)` | $L_\phi=\sqrt{\gamma_\phi/2}\,\sigma_z$ ($T_\phi$) | SZ §5.3.3 |
| `steady_state_excited_population(omega_rabi, gamma, detuning)` | $\rho_{ee}^{\,\mathrm{ss}}$ (optical Bloch) | SZ Ch. 10 |

Also exported: `HBAR`, the two-level operators `I2, sigma_x, sigma_y, sigma_z,
sigma_minus, sigma_plus`, and kets/projector `ket_e, ket_g, proj_e`. Basis order
is $(|e\rangle,|g\rangle)$, so `rho[0,0]` is the population that decays. Units
$\hbar=1$ (pass `hbar=...` to override).

## Use
```python
import numpy as np
from open_systems import (density_matrix, ket_e, ket_g, evolve_lindblad,
    spontaneous_emission_op, excited_population, coherence,
    two_level_hamiltonian, steady_state_excited_population)

gamma = 1.0
plus = (ket_e + ket_g) / np.sqrt(2)            # equal-coherence superposition
t = np.linspace(0, 6, 400)
rhos = evolve_lindblad(density_matrix(plus), np.zeros((2, 2)),
                       [spontaneous_emission_op(gamma)], t)
pe  = np.array([excited_population(r) for r in rhos])   # ~ e^{-gamma t}   (T1)
coh = np.array([abs(coherence(r))     for r in rhos])   # ~ e^{-gamma t/2} (T2 = 2 T1)

H = two_level_hamiltonian(omega_rabi=2.0, detuning=0.0) # drive on resonance
traj = evolve_lindblad(density_matrix(ket_g), H,
                       [spontaneous_emission_op(gamma)], np.linspace(0, 60, 600))
excited_population(traj[-1])                    # 0.4444 = Omega^2/(gamma^2+2 Omega^2)
steady_state_excited_population(2.0, gamma)     # 0.4444 (analytic Bloch steady state)
```

## Run
```bash
cd code
python3 open_systems.py          # demo: T1/T2 decay rates fitted from the sim, trace conservation, Bloch steady state
python3 test_open_systems.py     # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — density matrix → Lindblad master equation → spontaneous emission ($T_1$), decoherence ($T_2$), optical Bloch steady state
- `code/open_systems.py`, `code/test_open_systems.py`
- `problems/problems.md` — worked problems (Scully & Zubairy §5.3, §6.3, Ch. 8, Ch. 10)
- `refs.md` — citation table (verified printed↔PDF pages, offset +20)
