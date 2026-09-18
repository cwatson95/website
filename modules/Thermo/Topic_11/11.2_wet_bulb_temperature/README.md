# 11.2 — Wet-Bulb Temperature & Adiabatic Saturation

Second concept module of **Topic 11 (Psychrometrics — Moist Air)**.

- **Builds on:** `11.1` (humidity ratio $\omega$, relative humidity $\phi$, mixture
  enthalpy, dew point) and steam-table $p_g$, $h_f$, $h_g$ data (Table A-2).
- **Feeds into:** `11.EP` (Example 12.12 reads $\omega$ at a dry/wet-bulb point),
  `11.HP` (wet-bulb problem 12.77), and the chart-based air-conditioning analyses.

## Scope
The **wet-bulb temperature** $T_{wb}$ is an evaporative-cooling reading below the
dry-bulb temperature; with the dry-bulb temperature it fixes the moist-air state. Its
theory is the **adiabatic-saturation temperature** $T_{as}$ ($\approx T_{wb}$), which
yields the humidity ratio from $p$, $T$, $T_{as}$. Toolkit (`code/wet_bulb.py`):

| use | relation | function |
|-----|----------|----------|
| saturated exit humidity ratio | $\omega' = 0.622\,p_g(T_{as})/(p-p_g(T_{as}))$ (12.49) | `humidity_ratio_at_saturation` |
| humidity ratio from $T_{as}\!\approx\!T_{wb}$ | $\omega = [h_a(T_{as})-h_a(T)+\omega'(h_g(T_{as})-h_f(T_{as}))]/(h_g(T)-h_f(T_{as}))$ (12.48) | `humidity_ratio_from_wet_bulb` |
| adiabatic-saturator energy balance | residual of Eq. 12.50 (zero at solution) | `adiabatic_saturator_residual` |
| chart dry-air enthalpy datum | $h_a = c_{pa}\,T(^\circ\text{C})$ (12.51) | `dry_air_enthalpy` |
| mixture enthalpy at a chart point | $h_a + \omega h_g$ ($\approx$ const along $T_{wb}$) | `state_enthalpy` |
| dew-point vapor pressure | $p_v = \omega p/(0.622+\omega)$ | `dew_point_pressure` |
| add moisture to a stream | $\omega_{out}=\omega_{in}+\dot m_w/\dot m_a$ (12.52) | `exit_humidity_ratio` |

**Key idea:** the wet-bulb depression $T-T_{wb}$ measures dryness; substituting $T_{wb}$
for $T_{as}$ in Eqs. 12.48–12.49 turns two thermometer readings into $\omega$.

## Run
```bash
cd code && python3 wet_bulb.py          # omega' (12.49), Eq 12.48 consistency, dew point
python3 test_wet_bulb.py                # "All 11 tests passed."
```

## Files
`notes.md`, `code/wet_bulb.py`, `code/test_wet_bulb.py`, `problems/problems.md`, `refs.md`.
