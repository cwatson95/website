# NE-11 — Attenuation, cross sections, flux density and reaction rates

Eleventh module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the first of Chapter 7. Covers **§§7.1–7.2**
(printed pp. 179–193) of Shultis & Faw, 3rd ed.: the linear interaction
coefficient, exponential attenuation of uncollided radiation, mean free path and
half-thickness, buildup, microscopic and macroscopic cross sections, mixtures and
compounds, flux density, reaction-rate density, fluence, and point sources with
and without shields.

- **Prerequisites:** `~NE-06` (the decay constant — μ is its spatial analogue,
  and every result transfers), `~NE-08` (the scattering kinematics behind the
  cross sections), `~NE-09` (Σ_f φ is reactor power).
- **Cross-links:** `~NE-12` (the photon μ/ρ decomposed into its three
  processes), `~NE-13` (neutron cross sections, 1/v and resonances), `~NE-14`
  (charged particles, which obey none of this), `~NE-15`/`~NE-16` (a detector
  counts μ_d φ V, with Poisson statistics), `~NE-17` (dose is μ_en φ E/ρ),
  `~NE-19`/`~NE-21` (Σ_f φ, with φ supplied by diffusion theory).

## Scope
The interaction coefficient μ is a constant probability per unit *path length*,
exactly as the decay constant λ is per unit *time* — so attenuation is
exponential, the distance to first interaction is exponentially distributed with
mean 1/μ (the mean free path), the half-thickness is ln2/μ, and interaction is
memoryless. The only variable that matters is the optical thickness μx in mean
free paths. The bridge to tabulated data is μ = σN: a per-atom area in barns
times an atom density, with μ/ρ intrinsic and therefore what gets tabulated.
Flux density φ = vn — read as track length per unit volume per unit time —
then gives the equation everything reduces to, **R = μφ**: reactor power,
detector count rate and tissue dose are that product with different subscripts.
Two cautions carry real weight: exponential attenuation describes *uncollided*
particles only and is a lower bound on the field (buildup can be a factor of 10),
and geometric 1/r² attenuation is a power law while material attenuation is an
exponential — which is why shielding beats standoff once space runs out.

## Operations — `code/attenuation.py`

| call | meaning | reference |
|------|---------|-----------|
| `load_photon_coefficients(material)`, `mass_coefficient(m, E, comp)` | Appendix C.3, log-log interpolated | Table C.3 |
| `linear_coefficient(m, E, comp, density)` | μ = ρ(μ/ρ) | Eq. (7.11) |
| `load_thermal_cross_sections()`, `absorption_cross_section(nuc)` | Appendix C.1; σ_a summed over removal channels | Table C.1 |
| `uncollided_intensity(I0, mu, x)` | $I^o(0)e^{-\mu x}$ | Eq. (7.4) |
| `interaction_probability`, `survival_probability` | $1-e^{-\mu x}$, $e^{-\mu x}$ | Eqs. (7.5)–(7.6) |
| `path_length_pdf(mu, x)` | $\mu e^{-\mu x}$ | Eq. (7.7) |
| `mean_free_path(mu)` | $1/\mu$ | Eq. (7.8) |
| `half_thickness`, `tenth_thickness`, `thickness_for_attenuation` | $\ln2/\mu$, $\ln10/\mu$, $\ln f/\mu$ | Eq. (7.9) |
| `mean_free_paths_traversed(mu, x)` | the optical thickness μx | §7.1.2 |
| `buildup_intensity(I0, mu, x, B)` | $I=BI^o$, with B supplied by the caller | §7.1.5 |
| `atom_density(rho, A)`, `molecular_density`, `macroscopic_cross_section(sigma_b, N)` | $N=\rho N_a/A$; $\Sigma=\sigma N$ | Eq. (7.10) |
| `mixture_mass_coefficient(components, E)`, `mixture_density(components)` | weight-fraction mixing | Eq. (7.13) |
| `compound_macroscopic(N_mol, contributions)` | $\Sigma=N\sum_in_if_i\sigma_i$ | Eq. (7.12) |
| `flux_density(n, v)`, `reaction_rate_density(mu, phi)`, `fluence(phi, t)` | $\phi=vn$; $R=\mu\phi$; $\Phi=\phi t$ | Eqs. (7.14)–(7.21) |
| `point_source_flux(S, r)` | $S_p/4\pi r^2$ | Eq. (7.23) |
| `point_source_flux_shielded(S, r, mu, t)` | + $e^{-\mu t}$ | Eq. (7.26) |
| `point_source_flux_layered(S, r, layers)` | + $\exp(-\sum\mu_it_i)$ | Eq. (7.27) |
| `MATERIALS`, `DENSITY_ERRATA` | densities; one corrected printed value | see `refs.md` |

## Use
```python
from attenuation import (linear_coefficient, mass_coefficient, half_thickness,
                         tenth_thickness, mean_free_path, mixture_mass_coefficient,
                         mixture_density, molecular_density, compound_macroscopic,
                         absorption_cross_section, load_thermal_cross_sections,
                         flux_density, reaction_rate_density, point_source_flux_shielded)

linear_coefficient("water", 1.0)          # 0.07066 /cm
tenth_thickness(linear_coefficient("water", 1.0))    # 32.59 cm   -- Example 7.1
tenth_thickness(linear_coefficient("lead", 1.0))     #  2.98 cm

mix = {"iron": 0.5, "lead": 0.5}          # Example 7.2
mixture_mass_coefficient(mix, 1.0), mixture_density(mix)     # 0.06377, 9.298

xs = load_thermal_cross_sections()        # Example 7.3
n = molecular_density(1.0, 18.0153)
compound_macroscopic(n, [(2, 0.99985, absorption_cross_section("1H", xs))])   # 0.0223 /cm

reaction_rate_density(0.0223, flux_density(1e8, 2.2e5))      # fissions etc. per cm3 per s
point_source_flux_shielded(3.7e10, 100.0, 0.7721, 10.0)      # 1 Ci behind 10 cm of lead
```

## Run
```bash
cd code
python3 attenuation.py        # demo: Examples 7.1-7.3, mfp table, point sources
python3 test_attenuation.py   # tests  ->  "All 19 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/C1_thermal_neutron_cross_sections.csv` and
`../../data_tables/C3_photon_coefficients_*.csv`.

## Files
- `notes.md` — μ and its identity with the decay constant → uncollided vs total
  and why buildup matters → microscopic to macroscopic, mixtures, and the
  abundance×cross-section rule → flux density and R = μφ → geometric vs material
  attenuation, with a "Where this goes" map.
- `code/attenuation.py`, `code/test_attenuation.py` (stdlib only). Tests
  reproduce **all three** of the chapter's worked examples from the extracted
  appendices, verify the path-length distribution numerically, and check that
  pair production switches on exactly at 1.022 MeV in the C.3 tables.
- `problems/problems.md` — 8 worked problems (S&F Ch. 7 problems 1, 2, 4, 5, 8,
  10, 11 plus one added) with numeric `*Check:*` lines.
- `figures/` — attenuation in cm vs in mean free paths, mass coefficients with
  the K edge and pair-production threshold marked, geometric vs material
  attenuation from a point source, and the path-length distribution.
- `refs.md` — page-verified citations; **an erratum in Example 7.2** (the iron
  density, printed 7.784, which the book's own next line contradicts); the
  meaning of "absorption"; and why Eq. (7.4) is a lower bound.
