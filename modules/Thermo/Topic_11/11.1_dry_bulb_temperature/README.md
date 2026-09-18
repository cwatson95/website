# 11.1 — Dry-Bulb Temperature & the Moist-Air Model

Opening module of **Topic 11 (Psychrometrics — Moist Air)**.

- **Builds on:** the ideal-gas mixture / Dalton model (Topic 12 trunk, Moran §12.1–12.4)
  and saturation pressure $p_g(T)$ / enthalpy data for water (Topic 4, Table A-2).
- **Feeds into:** `11.2` (wet-bulb & adiabatic saturation), `11.EP` (worked Examples),
  and every air-conditioning analysis (Moran §12.8).

## Scope
The **dry-bulb temperature** $T$ is the ordinary thermometer reading; it is the abscissa
of the psychrometric chart and the temperature at which $p_g$, $h_g$ are read. With one
more property it fixes the moist-air state. The toolkit (`code/dry_bulb.py`):

| use | relation | function |
|-----|----------|----------|
| humidity ratio (definition) | $\omega = m_v/m_a$ (12.42) | `humidity_ratio` |
| humidity ratio from pressures | $\omega = 0.622\,p_v/(p-p_v)$ (12.43) | `humidity_ratio_from_pressures` |
| relative humidity | $\phi = p_v/p_g(T)$ (12.44) | `relative_humidity` |
| invert for $p_v$ | $p_v=\phi\,p_g$ ; $p_v=\omega p/(0.622+\omega)$ | `vapor_pressure_from_phi`, `vapor_pressure_from_ratio` |
| mixture enthalpy (total / per dry air) | $H=m_a h_a+m_v h_v$ ; $h=h_a+\omega h_v$ (12.45/12.46) | `mixture_enthalpy_total`, `mixture_enthalpy_per_dry_air` |
| low-pressure vapor enthalpy | $h_v\approx h_g(T)$ (12.47) | `vapor_enthalpy_approx` |
| mass split of a sample | $m_a=m/(1+\omega)$, $m_v=\omega m/(1+\omega)$ | `dry_air_mass`, `vapor_mass` |

**Key idea:** at fixed mixture pressure there is a one-to-one map $p_v \leftrightarrow \omega$
(12.43), so the chart can carry either on its ordinate. The **dew point** is
$T_{sat}(p_v)$: cool at constant $p$ (constant $\omega$) until $\phi=100\%$.

## Run
```bash
cd code && python3 dry_bulb.py          # humidity ratio, dew point, Ex 12.7 anchor
python3 test_dry_bulb.py                # "All 14 tests passed."
```

## Files
`notes.md`, `code/dry_bulb.py`, `code/test_dry_bulb.py`, `problems/problems.md`, `refs.md`.
