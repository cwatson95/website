# NE-19 — The neutron life cycle: the four- and six-factor formulas, k_eff

Nineteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), opening Chapter 10. Covers **§§10.1–10.6** (printed
pp. 322–339) of Shultis & Faw, 3rd ed.: moderation, thermal neutrons, fuel
properties, the six factors, criticality, homogeneous and heterogeneous cores,
and reflectors.

- **Prerequisites:** `~NE-13` (elastic scattering, ξ, moderation), `~NE-09`
  (fission, ν), `~NE-11` (macroscopic cross sections and reaction rates).
- **Cross-links:** `~NE-20` (what happens when k_eff ≠ 1), `~NE-21` (where the
  buckling comes from), `~NE-22`/`~NE-23` (lattices and enrichment as design).

## Scope
A reactor is a bookkeeping problem: follow a generation of neutrons round the
cycle and count. Six factors do the counting, and the physics is that **they pull
against each other** — adding moderator raises the resonance escape probability
and lowers the thermal utilization, so k_∞ has an interior maximum. For natural
uranium that maximum is **below 1 in every moderator except heavy water**, which
is why enrichment plants exist; lumping the fuel roughly doubles p and is the
other way out, which is how CP-1 worked.

## Operations — `code/neutron_cycle.py`

| call | meaning | reference |
|------|---------|-----------|
| `maxwellian_flux(E, T)` | ∝ E e^{−E/kT} — **linear in E**, mean 2kT | Eq. (10.1) |
| `westcott_averaged_cross_section(σ(E₀), T, g)` | (√π/2) g √(T₀/T) σ(E₀) | Eq. (10.5) |
| `fast_fission_factor(N238/NM, geometry)` | ε, fitted to Fig. 10.2 | Eq. (10.6) |
| `resonance_integral_homogeneous`, `resonance_escape_homogeneous` | I and p | Eqs. (10.8)–(10.9) |
| `resonance_integral_rod(r, ρ)`, `resonance_escape_lattice(...)` | A + C/√(rρ); lumped p | Eqs. (10.18)–(10.19) |
| `thermal_utilization_homogeneous(...)` | f | Eq. (10.11) |
| `thermal_fission_factor(ν, σf, σa)`, `eta_of_uranium(e)` | η | Eq. (10.12) |
| `lattice_F(x)`, `lattice_E(y, z)` | Wigner–Seitz constants, exact **or** series | Eqs. (10.22)–(10.25) |
| `thermal_utilization_lattice(...)`, `cell_radius(a)` | f for a rod lattice; b = a/√π | Eqs. (10.20)–(10.21) |
| `bessel_i0/i1/k0/k1` | modified Bessel functions (A&S), stdlib only | — |
| `diffusion_length_squared(L²_M, f)` | L² = L²_M(1−f) | Eq. (10.14) |
| `thermal_nonleakage`, `fast_nonleakage` | 1/(1+L²B²) and e^{−B²τ} | Eqs. (10.13), (10.15) |
| `geometric_buckling(geom, **dims)` | sphere / cylinder / slab / cube | Table 10.10 |
| **`k_infinity(η, p, f, ε=1)`** | **ε p f η** — the four-factor formula | Eq. (10.17) *corrected* |
| `k_effective(..., P_f, P_th, ε=1)` | the six-factor formula | Eq. (10.16) *corrected* |
| `four_factor_formula_as_printed(η, p, f)` | the printed version, for comparison | Eq. (10.17) |
| `critical_buckling`, `critical_radius_sphere` | **refuses k_∞ ≤ 1** | Ex. 10.5 |
| `FUEL_THERMAL_AVERAGED`, `FUEL_PROPERTIES`, `MODERATOR_*`, `OPTIMUM_RATIOS`, `LATTICE_TABLE` | Tables 10.1–10.8 | — |

## Use
```python
from neutron_cycle import (eta_of_uranium, thermal_utilization_homogeneous,
                           resonance_escape_homogeneous, k_infinity,
                           four_factor_formula_as_printed, critical_radius_sphere,
                           diffusion_length_squared, MODERATOR_THERMAL,
                           westcott_averaged_cross_section)

eta_of_uranium(0.007204)         # 1.339 -- natural uranium: above 1, far below 2
eta_of_uranium(0.02)             # 1.738 -- S&F Example 10.2

# S&F Table 10.5, water row -- the row that shows epsilon is missing from Eq. (10.17)
k_infinity(1.338, 0.727, 0.869, eps=1.051)      # 0.888, as the table prints
four_factor_formula_as_printed(1.338, 0.727, 0.869)   # 0.845, as Eq. (10.17) prints

f = thermal_utilization_homogeneous(592.6, 0.00386, 35000.0)   # 0.8143
kinf = k_infinity(2.080, 1.0, f)                               # 1.6939
l2 = diffusion_length_squared(MODERATOR_THERMAL["C"]["L2"], f) # 570.1 cm2
critical_radius_sphere(kinf, l2, 368.0)                        # 126.7 cm

critical_radius_sphere(0.781, 570.0, 368.0)   # raises: k_inf <= 1, no finite core
```

## Run
```bash
cd code
python3 neutron_cycle.py        # demo: Examples 10.1-10.10, Tables 10.5 and 10.8
python3 test_neutron_cycle.py   # tests  ->  "All 16 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the Maxwellian flux and the two cross-section tables → the four
  factors one at a time → leakage → the optimum-moderation trade and the missing
  ε → lumping the fuel and the Wigner–Seitz method, with a "Where this goes" map
  and a note on the module's six corrections.
- `code/neutron_cycle.py`, `code/test_neutron_cycle.py` (stdlib only, including
  its own modified Bessel functions). `critical_buckling` **refuses** a material
  with k_∞ ≤ 1: no finite core of it is critical however large, so a buckling
  would be meaningless — and that is exactly the natural-uranium-in-graphite case
  that forced Fermi to build a lattice.
- `problems/problems.md` — 8 worked problems (S&F Ch. 10 problems 5, 7, 9–10, 12,
  13, 17, 19, 21–22) with numeric `*Check:*` lines.
- `figures/` — the four factors pulling against each other in graphite and heavy
  water, Table 10.5 with and without ε, what lumping buys beside the 1/√(rρ)
  self-shielding law, and how leakage sets the critical size.
- `refs.md` — page-verified citations; **six printed results this module
  corrects**, each with the evidence; one prose claim its own fit does not
  support; and the equation whose printed layout invites a 68% misreading.
