# QM-17 — Fine Structure, Zeeman & Hyperfine

Corrections to the hydrogen spectrum (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-12` (the hydrogen atom — the Bohr levels `E_n` that
  everything here perturbs, and the wavefunctions whose expectation values give
  the shifts), `~QM-15` (time-independent perturbation theory — **this module is
  its showcase application**: every correction is a first-order shift `E¹ =
  ⟨ψ⁰|H′|ψ⁰⟩`), `~QM-13` (addition of angular momenta — `J = L + S` and `F = I + S`
  supply the "good" quantum numbers), `~QM-11` (spin — the electron's `S` and its
  anomalous moment `g_e ≈ 2`), `~QM-10` (the `L·S` operator from
  `j(j+1)−l(l+1)−s(s+1)`).
- **Feeds into:** `~QM-22` (the Dirac equation reproduces the exact
  fine-structure formula and *explains* the Darwin term and `g_e = 2`), `~QM-16`
  (radiative transitions between these split levels), and astrophysics via the
  21 cm line. The Zeeman effect is the bridge to atomic magnetometry / NMR.

## Scope
The Bohr/Schrödinger spectrum `E_n = −13.6 eV/n²` is only the leading term. Three
small corrections, each a textbook use of perturbation theory (`~QM-15`), refine
it — and each is checked here against a **measured number**:

1. **Fine structure** `O(α²)` — two mechanisms that happen to be the same size:
   the **relativistic** kinetic correction `−p⁴/8m³c²` (depends on `n,l`) and
   **spin-orbit** coupling `∝ L·S` (depends on `n,l,j`), plus the **Darwin** term
   for `l=0`. Their sum is the famous `(n,j)`-only formula
   `E_fs = −(13.6 eV/n²)(α²/n²)[n/(j+½)−¾]`, which splits the `l`-degeneracy but
   preserves the `j`-degeneracy.
2. **The Zeeman effect** — a level in an external field `B`. **Weak field**
   (`B ≪ B_internal`): the Landé `g_J` and `E = μ_B g_J B m_j` (anomalous Zeeman).
   **Strong field** (Paschen–Back): `B` decouples `L` and `S`, giving
   `E = μ_B B(m_l + 2m_s)`.
3. **Hyperfine splitting** `O(α²·m_e/m_p)` — the proton is itself a magnetic
   dipole; spin-spin coupling `∝ S_p·S_e` splits the ground state into a
   triplet/singlet pair. The gap is the **21 cm / 1420 MHz line** of neutral
   hydrogen.

**House rule (inherited from `~QM-01`):** nothing is quoted. The fine-structure
constant `α`, the Rydberg `Ry = ½α²mc²`, the Bohr magneton `μ_B`, and the 21 cm
wavelength are all **rederived from CODATA constants** (`e, ℏ, c, m_e, m_p, ε₀`)
and checked against reference values in the tests. The central identity
`E_rel + E_so + E_Darwin = E_fs(n,j)` is verified **to machine precision** for
every state — making the constant set self-consistent (`Ry` derived from `α`) so
the two ways of writing the fine structure agree exactly.

## Operations — `code/fine_structure.py`

| call | meaning | formula |
|------|---------|---------|
| `fine_structure_constant()` | the scale `α` | `e²/(4πε₀ℏc) ≈ 1/137.036` |
| `electron_rest_energy_eV()` | `mc²` | `≈ 511 keV` |
| `rydberg_energy_eV()` | `Ry`, rederived | `½α²mc² ≈ 13.6057 eV` |
| `bohr_energy_eV(n,Z)` | unperturbed level | `−Ry Z²/n²` |
| `relativistic_correction_eV(n,l,Z)` | kinetic `O(α²)` | `−(E_n²/2mc²)[4n/(l+½)−3]` |
| `LS_coupling(j,l,s)` | `⟨L·S⟩` (units ℏ²) | `½[j(j+1)−l(l+1)−s(s+1)]` |
| `spin_orbit_correction_eV(n,l,j,Z)` | spin-orbit `O(α²)` | Griffiths Eq. 7.67 (0 at `l=0`) |
| `darwin_correction_eV(n,l,Z)` | `l=0` contact term | `2n E_n²/mc²` (else 0) |
| `fine_structure_correction_eV(n,j,Z)` | total fine structure | `−(Ry Z²/n²)(Zα)²/n²[n/(j+½)−¾]` |
| `hydrogen_energy_eV(n,j,Z)` | gross + fine | `E_n + E_fs` (Eq. 7.69) |
| `lande_g_factor(j,l,s)` | weak-field `g_J` | `1 + [j(j+1)+s(s+1)−l(l+1)]/2j(j+1)` |
| `bohr_magneton()` / `_eV_per_T()` | moment unit | `eℏ/2m_e` |
| `zeeman_weak_field_eV(j,l,m_j,B,s)` | anomalous Zeeman | `μ_B g_J B m_j` |
| `zeeman_strong_field_eV(m_l,m_s,B)` | Paschen–Back | `μ_B B(m_l+2m_s)` |
| `spin_spin_coupling(F,s1,s2)` | `⟨S₁·S₂⟩` (units ℏ²) | `½[F(F+1)−s₁(s₁+1)−s₂(s₂+1)]` |
| `hyperfine_splitting_eV()` | ground-state gap | `4g_p ℏ⁴/(3m_p m_e²c²a₀⁴)` |
| `hyperfine_frequency()` / `_wavelength()` | the 21 cm line | `ΔE/h`, `c/f` |

Constants `h, ℏ, c, k_B, e, m_e, m_p, ε₀, μ₀, a₀, Ry_eV, g_e, g_p` and the
reference values `alpha_ref, mu_B_ref, f_21cm_ref, lambda_21cm_ref` (used only to
*check* the rederivations) are exported too. Energies in eV, frequencies in Hz,
lengths in m; the angular-momentum brackets `⟨L·S⟩`, `⟨S₁·S₂⟩` are in units of ℏ².

## Use
```python
from fine_structure import (fine_structure_constant, fine_structure_correction_eV,
    LS_coupling, lande_g_factor, hyperfine_frequency, hyperfine_wavelength, e, h)

1/fine_structure_constant()                       # 137.036  -- the famous "1/137"
LS_coupling(1.5, 1) - LS_coupling(0.5, 1)         # 1.5 ħ²  -- p3/2 above p1/2
dE = fine_structure_correction_eV(2,1.5) - fine_structure_correction_eV(2,0.5)
dE * e / h / 1e9                                   # 10.95 GHz -- n=2 fine splitting
lande_g_factor(0.5, 0), lande_g_factor(0.5, 1)    # (2.0, 0.667) -- ²S₁/₂, ²P₁/₂
hyperfine_frequency() / 1e6                        # 1421 MHz  (measured 1420.4)
hyperfine_wavelength() * 100                        # 21.1 cm   -- the 21 cm line
```

## Run
```bash
cd code
python3 fine_structure.py          # demo: the three layers of corrections
python3 test_fine_structure.py     # tests  ->  "All 21 tests passed."
```

## Files
- `notes.md` — the derivations: α as the scale; relativistic + spin-orbit +
  Darwin → the `(n,j)` formula; weak/strong Zeeman; hyperfine → 21 cm
- `code/fine_structure.py` — the library (pure `math`; α, Ry, μ_B, 21 cm rederived)
- `code/test_fine_structure.py` — 21 checks: the exact decomposition, the Landé
  values, the n=2 splitting, the 21 cm line, the Bohr→fine→hyperfine hierarchy
- `problems/problems.md` — worked problems (Griffiths 3e, Ch. 7)
- `refs.md` — verified textbook locations
