# PK-04 — References

| Book (editor/author) | File | Notes |
|---|---|---|
| Rhodes (ed.), *Excimer Lasers* (Topics in Applied Physics, vol. 30) | `PK_Plasma_Kinetic_Theory/Excimer_Lasers_Topics_Rhodes.pdf` | **the KrF reference**: rare-gas-halide formation channels, the 248 nm B→X bound–free band, quenching & laser kinetics |
| Michel, *Introduction to Laser–Plasma Interactions* | `PK_Plasma_Kinetic_Theory/Laser_plasma_pierre_michel.pdf` | atomic processes in plasmas: collisional rate coefficients, the EEDF, ionization / Saha equilibrium |

> **Citation granularity.** These are cited at **chapter / section level only** — the
> printed↔PDF page offsets were not verified here, so no exact page numbers are given
> (cf. `~SM-06/refs.md`, which verifies Pathria page-by-page). Open the PDFs above to
> tighten to page level if needed. The Maxwellian $\langle\sigma v\rangle$ derivation
> is developed in `~SM-06` (Pathria Ch. 6) and the EEDF / kinetic equation in `~PK-01`.

## Living reference — the user's KrF/LoKI code
The module is a teaching distillation of the in-repo simulator; these are the
authoritative, *runnable* sources for the real reaction set and rate constants:

| Topic | Location |
|---|---|
| factored architecture, 26-element log-packed state vector, `run_sim → build_rhs_u → rhs_u` | `projects/Kinetic_Modeling/KrF_and_LoKI/docs/architecture.md` |
| physics overview (formation pathways, LoKI coupling, validation targets), rendered math | `projects/Kinetic_Modeling/KrF_and_LoKI/docs/about/index.html` |
| the real reactions r25 (harpoon), r26 (ion channel), r30 (stimulated), r31 (radiative), r32 (quench) | `…/KrF Code/factored-pyfiles/phantom11/reactions.py` |
| embedded LoKI swarm/EEDF tables; `CHOW_EN_TD_DEFAULT = 51 Td` | `…/phantom11/loki_tables.py` |
| the full 23-species $\dot n_i$ = production − loss body | `…/phantom11/_rhs_u_body.py` |
| audit history of rate-constant fixes (τ_eff, σ_stim, K32, …) | `…/KrF_and_LoKI/docs/CHANGELOG.md` |

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| rate coefficient k = ⟨σv⟩, the EEDF (`rate_coefficient_maxwellian`, `maxwell_energy_pdf`) | Mi | atomic-processes / electron-collision-rates ch. |
| threshold cross-sections → Arrhenius (`rate_coefficient_step_closed_form`, `arrhenius`) | Mi; `~SM-06` | collisional rates; Maxwellian averaging (Pathria §6.4) |
| ionization equilibrium, Saha (`saha_ratio`, `saha_ionization_fraction`) | Mi | ionization / Saha equilibrium ch. |
| KrF* formation, harpooning, ion channel (`excimer_rhs`, `default_krf_params`) | Rh | rare-gas-halide formation kinetics ch. |
| 248 nm B→X bound–free emission, quenching, gain (`simulate_krf`, `photon_energy_eV`) | Rh; `~QO-03` | KrF laser physics ch.; emission & gain |

## See also
- `~QO-03` (spontaneous/stimulated emission, Einstein coefficients, laser gain) — the
  photon side of KrF* kinetics, where `photon_energy_eV` and the inversion feed in.
- `~SM-06` (kinetic theory; the Maxwellian $\langle\sigma v\rangle$ that §2–3 specialize)
  and `~PK-01` (the electron kinetic equation → the non-Maxwellian EEDF LoKI supplies).
- Rhodes *Excimer Lasers* (the KrF kinetics & 248 nm band); Michel (rates, EEDF, Saha);
  and the in-repo `KrF_and_LoKI` code as the living, runnable reference.
