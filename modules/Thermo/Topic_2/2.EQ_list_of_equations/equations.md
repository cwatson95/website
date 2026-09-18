# 2.EQ — Topic 2: List of Equations

The key equations of **Topic 2 (Energy & Work)** in canonical Moran 8e form. Each
is a function in `code/equations.py`; `code/test_equations.py` checks every value
**and** cross-checks that the concept modules (2.1–2.6) reproduce these forms.
Complements `Topic_1/1.EQ` (foundations); citations are Moran 8e (printed pages;
PDF = +17; `refs.md`).

## Work (Ch. 2 §2.2)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 1 | 2.12 | `W = ∫F·ds` | `general_work` | §2.2, p.44 |
| 2 | 2.17 | `W = ∫p dV` (boundary) | `boundary_work` | §2.2.3, p.48 |
| 3 | 2.20 | `Ẇ = τω` ⟹ `W = τω·Δt` (shaft) | `shaft_work` | §2.2.6, p.53 |
| 4 | 2.21 | `Ẇ = −εi`; `|W| = VI·Δt` (electric) | `electric_work` | §2.2.6, p.53 |
| 5 | (2.18) | `W = ½k(x₂²−x₁²)` (spring) | `spring_work` | §2.2.6, p.52 |

## Power (§2.2.2)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 6 | 2.13 | `Ẇ = F·V` | `power_force_velocity` | §2.2.2, p.46 |
| — | 2.20/2.21 | shaft `τω`, electric `VI` | `shaft_power`, `electric_power` | §2.2.6, p.53 |

## Energy (§2.1, §2.3)
| # | Eq. | form | function | source |
|---|-----|------|----------|--------|
| 7 | 2.5 | `ΔKE = ½m(V₂²−V₁²)` | `delta_KE`, `kinetic_energy` | §2.1.1, p.41 |
| 8 | 2.10 | `ΔPE = mg(z₂−z₁)` | `delta_PE`, `potential_energy` | §2.1.2, p.42 |
| 9 | 2.27 | `E = U + KE + PE` | `total_energy` | §2.3, p.55 |

The generalized work form `δW = p dV + σ d(Ax) + τ dA − ε dZ + …` (Eq. 2.26,
§2.2.8, p.54) unifies modes 1–5.

> `python3 code/test_equations.py` → 13 value checks + 14 cross-module checks =
> `"All 27 tests passed."`
