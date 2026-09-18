# 6.3 — Adiabatic & Isentropic Processes

The `Q = 0` idealization of **Topic 6** and its reversible limit, the **isentropic**
process — the backbone of every turbine/compressor/nozzle/pump analysis.

- **Builds on:** `6.1` (adiabatic int. rev. ⇒ isentropic), `6.2` (σ ≥ 0 ⇒ real devices
  miss the isentropic ideal), the ideal-gas entropy relations.
- **Feeds into:** isentropic efficiencies and every cycle in Topics 7–9.

## Scope
Adiabatic means `Q = 0`; adiabatic **+ internally reversible** ⇒ **isentropic**. Ideal-gas
isentropic relations and the isentropic-efficiency bridge:

| use | relation | `code/adiabatic.py` |
|-----|----------|---------------------|
| adiabatic test | `Q = 0` | `is_adiabatic` |
| ideal-gas Δs (tables / const cp) | Eq. 6.20a / 6.22 | `delta_s_ideal_gas_so`, `delta_s_ideal_gas_cp` |
| **T–p isentropic** | `T₂/T₁=(p₂/p₁)^((k−1)/k)` | `temp_ratio_from_pressure`, `final_temp_isentropic` |
| **T–v / p–v isentropic** | `(v₁/v₂)^(k−1)`, `pv^k=const` | `temp_ratio_from_volume`, `pressure_ratio_from_volume` |
| **air `p_r`/`v_r` tables** | `p₂/p₁=p_r2/p_r1` | `p2_from_pr`, `v2_from_vr`, `pr2_isentropic` |
| `c_p, c_v` from `k` | Eq. 3.47 | `cp_from_k`, `cv_from_k` |
| **isentropic efficiency** | `η_t=(h₁−h₂)/(h₁−h₂s)` | `isentropic_turbine_eff`, `isentropic_nozzle_eff` |

**Key idea:** an adiabatic, internally reversible process is **isentropic**. For an ideal
gas with constant `k`, that is `pv^k = const`; for air, the tabulated `p_r`/`v_r` functions
do the same job with variable specific heats. Real adiabatic devices have σ > 0 and so fall
short of the isentropic ideal — quantified by the **isentropic efficiency**.

## Run
```bash
cd code && python3 adiabatic.py    # Ex 6.9 p2=15.28 atm; Ex 6.10 m2=1.58 kg; Ex 6.12 η_t=0.70
python3 test_adiabatic.py          # "All N tests passed."
```

## Files
`notes.md`, `code/adiabatic.py`, `code/test_adiabatic.py`, `problems/problems.md`, `refs.md`.
