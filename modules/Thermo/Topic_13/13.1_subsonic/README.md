# 13.1 — Subsonic Compressible Flow (M < 1)

Opening module of **Topic 13 (Compressible Flow & Gas Dynamics)**.

- **Builds on:** ideal-gas property model and isentropic processes (Topics 4–7);
  enthalpy `h` and the specific-heat ratio `k = cp/cv`.
- **Feeds into:** `13.2` (supersonic / choking), `13.3` (normal shock). The
  stagnation ratios and the area–velocity relation defined here are reused throughout.

## Scope
A flow is **subsonic** when `M = V/c < 1` (Moran Eq. 9.38). The toolkit:

| use | relation | `code/subsonic.py` |
|-----|----------|--------------------|
| speed of sound (ideal gas) | `c = √(kRT)` | `speed_of_sound_ideal_gas` |
| Mach number | `M = V/c` | `mach_number` |
| stagnation enthalpy | `ho = h + V²/2` | `stagnation_enthalpy` |
| stagnation T ratio | `To/T = 1 + (k−1)/2·M²` | `stagnation_temperature_ratio` |
| stagnation p ratio | `po/p = (1 + (k−1)/2·M²)^(k/(k−1))` | `stagnation_pressure_ratio` |
| stagnation ρ ratio | `ρo/ρ = (1 + (k−1)/2·M²)^(1/(k−1))` | `stagnation_density_ratio` |
| area–velocity | `dA/A = −(dV/V)(1−M²)` | `area_change_ratio`, `duct_shape` |

**Key idea:** for `M < 1` the factor `(1 − M²) > 0`, so area and velocity change in
*opposite* directions — a subsonic flow **accelerates in a converging** duct (nozzle)
and **decelerates in a diverging** duct (diffuser) [Moran Sec. 9.13.1, cases 1, 4].

## Run
```bash
cd code && python3 subsonic.py          # speed of sound + Ex 9.14(b) subsonic exit
python3 test_subsonic.py                # "All 18 tests passed."
```

## Files
`notes.md`, `code/subsonic.py`, `code/test_subsonic.py`, `problems/problems.md`, `refs.md`.
