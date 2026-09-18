# 1.1 — Open Systems (Control Volumes)

First module of the **THERMODYNAMICS** breakdown (group 1, *Foundations & system
concepts*; see `modules/Thermo/list.txt`). Standalone for now — cross-links below
use the `list.txt` numbering, not network trunk IDs.

- **Prerequisites:** `1.2` closed systems (the control-mass balance this generalizes);
  `2` energy & work and `3.2` the First Law (energy accounting); `4.1` enthalpy
  (`h = u + pv`, which packages internal energy with flow work).
- **Feeds into:** `6.4` steady-state and `6.5` conservation of mass flow (special
  cases handled here); the steady-flow **devices** `8.1`–`8.3` (compressor,
  condenser, heat exchanger) and nozzles/turbines/throttles; the **cycles** `9.6`
  Rankine and `9.5` Brayton, which are just networks of these control volumes.
- **Uses the data in** `../../steam_tables/` (A-3, A-4) for its worked examples.

## Scope
An **open system** (control volume, CV) is a region with a fixed boundary that
**mass can cross**. Two book-keeping laws govern it:

1. **Mass rate balance** — `dm_cv/dt = Σ ṁ_in − Σ ṁ_out`, with one-dimensional
   flow rate `ṁ = A V / v`.
2. **Energy rate balance** — `dE_cv/dt = Q̇ − Ẇ + Σ ṁ(h + V²/2 + gz)_in
   − Σ ṁ(h + V²/2 + gz)_out`. The flowing matter carries **enthalpy** (internal
   energy + flow work `pv`) plus kinetic and potential energy.

At **steady state** both time-derivatives vanish, giving the steady-flow energy
equation that every component model in later modules specializes: nozzles &
diffusers, turbines, compressors & pumps, throttles, heat exchangers, mixing
chambers. Derivations with page citations are in `notes.md`/`refs.md`.

## Operations — `code/open_systems.py`

| call | meaning | reference (Moran 8e, Ch.4) |
|------|---------|----------------------------|
| `flow_energy(h, V, z)` | ψ = h + V²/2 + gz  (kJ/kg) | "Conservation of Energy for a Control Volume" |
| `mass_flow_rate(A, V, v)` | ṁ = A V / v | "Conservation of Mass for a Control Volume" |
| `mass_rate_residual(ins, outs)` | dm_cv/dt; 0 at steady state | " |
| `energy_rate_residual(Q̇, Ẇ, ins, outs)` | dE_cv/dt; 0 at steady state | "Conservation of Energy for a Control Volume" |
| `shaft_power(in, out, Q̇)` / `turbine_power` / `compressor_power` | steady 1-in/1-out work rate | "Turbines"; "Compressors and Pumps" |
| `nozzle_exit_velocity(h_in, h_out, V_in)` | V_out = √(V_in² + 2·10³·Δh) | "Nozzles and Diffusers" |
| `diffuser_exit_enthalpy(h_in, V_in, V_out)` | h_out from velocity drop | "Nozzles and Diffusers" |
| `throttle_exit_enthalpy(h_in)` | h_out = h_in (isenthalpic) | "Throttling Devices" |
| `mixing_exit_enthalpy(ins)` | adiabatic mixing h_out | "Heat Exchangers" |
| `heat_exchanger_flow_ratio(...)` | ṁ_cold/ṁ_hot from energy balance | "Heat Exchangers" |

`Stream(mdot, h, V=0, z=0)` is the carrier object; `V` and `z` default to 0 (the
"kinetic and potential energy changes negligible" assumption).

## Use
```python
from open_systems import Stream, turbine_power, energy_rate_residual
import steam_lookup as st

h1 = st.h_superheated(60.0, 400.0)     # 3177.2 kJ/kg  (steam_tables A-4)
h2 = st.h_two_phase(0.10, 0.90)        # 2345.35 kJ/kg (A-3: hf + x·hfg)
sin, sout = Stream(1.0, h1), Stream(1.0, h2)

turbine_power(sin, sout)                       # 831.85 kW per kg/s
energy_rate_residual(0.0, 831.85, [sin], [sout])  # ~0 — the balance closes
```

## Run
```bash
cd code
python3 open_systems.py          # demo: turbine, nozzle, throttle, mass flow
python3 test_open_systems.py     # tests  ->  "All 16 tests passed."
```

## Files
- `notes.md` — derivations (mass & energy rate balances, the steady-flow device set) with inline page citations
- `code/open_systems.py` — the control-volume toolkit
- `code/steam_lookup.py` — minimal reader over `../../steam_tables/*.csv` for the examples
- `code/test_open_systems.py` — checks (`"All 16 tests passed."`)
- `problems/problems.md` — worked problems (Moran Ch.4)
- `refs.md` — citation table (section, equation, **printed + PDF page**)
