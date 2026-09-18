# 4.4 — Phase change & quality

Module of **Topic 4 (Properties & State Functions)**.

- **Builds on:** `4.1` (the `hf/hfg/hg` columns), property tables (Topic 5).
- **Feeds into:** `4.2` (`s = sf + x·sfg`), Rankine/refrigeration cycles (Topic 9),
  condensers (Topic 8).

## Scope
Inside the vapor dome `T` and `p` are **dependent** (saturation line), so the state
needs a second property: the **quality** `x = m_vapor/m_total` (Moran Eq. 3.1; 0 at
sat. liquid, 1 at sat. vapor). Then *every* specific property is `x`-weighted between
the saturated values — the same form for `v, u, h, s`:

| property | relation | source |
|----------|----------|--------|
| specific volume | `v = vf + x·vfg` | Eq. 3.2 |
| internal energy | `u = uf + x·ufg` | Eq. 3.6 |
| enthalpy | `h = hf + x·hfg` | Eq. 3.7 |
| entropy | `s = sf + x·sfg` | Eq. 6.4 |

`code/phase_change.py` covers all four with one `mixture_property(yf,yg,x)` and its
inverse `quality_from_property` (read quality off any measured property). `hfg = hg−hf`
is the **latent heat** of vaporization.

## Run
```bash
cd code && python3 phase_change.py    # water x=0.9, latent heat, CO2 tank (HW 3.16)
python3 test_phase_change.py          # "All 11 tests passed."
```

## Files
`notes.md`, `code/phase_change.py`, `code/test_phase_change.py`, `problems/problems.md`, `refs.md`.
