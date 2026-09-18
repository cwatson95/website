# 12.2 — Dissociation, Equilibrium Constant & Ionization (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).
**~PK** = cross-trunk plasma / statistical mechanics (**NOT in Moran 8e**) — see §4 and
`refs.md`. This module has **two trunks**, kept strictly separate.

## 1. Why dissociation matters (Moran §13.3.3 → §14)
The adiabatic-flame-temperature module (`12.EP`, Ex 13.8) warns that the measured flame
temperature falls *below* the ideal value partly because, at high `T`, **products
dissociate** (e.g. `CO₂ → CO + ½O₂`, `H₂O → H₂ + ½O₂`, `N₂ → 2N`); these endothermic
reactions absorb energy [M §13.3.3, p.832]. How far a reaction proceeds is an
**equilibrium** question, governed by the equilibrium constant `K`.

## 2. Equation of reaction equilibrium → K (§14.2–14.3)
For a single reaction `νA A + νB B ⇌ νC C + νD D` in an ideal-gas mixture, the equilibrium
criterion `dG]_{T,p} = 0` gives `νA μA + νB μB = νC μC + νD μD` [M Eq. 14.26, p.889]. Using
`μ_i = g°_i + R̄T ln(y_i p/p_ref)` [M Eq. 14.17, p.886], this collapses to
$$-\frac{\Delta G^\circ}{\bar R T}=\ln K(T),\qquad
K(T)=\frac{y_C^{\nu_C}\,y_D^{\nu_D}}{y_A^{\nu_A}\,y_B^{\nu_B}}\Big(\frac{p}{p_{ref}}\Big)^{\Delta\nu},$$
with `Δν = νC + νD − νA − νB` [M Eqs. 14.31–14.32, p.890]. The standard Gibbs change is
$$\Delta G^\circ=\sum_P\nu\,(\bar h-T\bar s^\circ)-\sum_R\nu\,(\bar h-T\bar s^\circ),$$
`h̄` and `s°` from Tables A-23/A-25 [M Eq. 14.29b, p.890]. **Table A-27** tabulates
`log₁₀K(T)`; for the inverse reaction `log₁₀K* = −log₁₀K` [M Eq. 14.34, p.890].

*Check (M Ex 14.1):* for `CO + ½O₂ ⇌ CO₂`, at 298 K `ΔG° = −257,253 kJ/kmol`,
`ln K = 103.83`, `log₁₀K = 45.093`; at 2000 K `ΔG° = −110,453`, `log₁₀K = 2.885`
(`code/ionization.py`). Both match Table A-27 via `log₁₀K = −log₁₀K*`.

## 3. Equilibrium composition (§14.3.2)
Writing `y_i = n_i/n` turns `K` into one equation in one unknown extent. For
`CO + ½O₂ (+aN₂) → zCO + (z/2)O₂ + (1−z)CO₂ (+aN₂)`, with `n = (2 + 2a + z)/2`,
$$K=\frac{z}{1-z}\Big(\frac{z}{2+2a+z}\Big)^{1/2}\Big(\frac{p}{p_{ref}}\Big)^{1/2}.$$
*Check (M Ex 14.2, 14.4):* at 2500 K (`K = 0.0363`), `z = 0.129` at 1 atm but `0.062` at
10 atm — **higher pressure suppresses dissociation** (`Δν > 0`); adding 1.88 mol inert N₂
raises it to `z = 0.175`. Mole fractions `yCO = 0.121, yO₂ = 0.061, yCO₂ = 0.818` (1 atm).

## 4. Ionization — the Saha equation  *(~PK, beyond Moran)*
> **Cross-trunk note.** Moran Ch.14 stops at **molecular dissociation**. Thermal
> **ionization** `A ⇌ A⁺ + e⁻` in a hot gas/plasma is governed by the **Saha equation**
> (M. N. Saha, 1920), a standard statistical-mechanics / plasma-physics result **not in
> Moran 8e**. It is flagged `~PK` here and cited to Chen, Rybicki & Lightman, Carroll &
> Ostlie, and Reif (`refs.md`).

Ionization is *the same* `ΔG° = −R̄T ln K` idea, except the freed electron contributes a
**translational** partition function. In number-density form,
$$\frac{n_{i+1}\,n_e}{n_i}=2\,\frac{g_{i+1}}{g_i}\Big(\frac{2\pi m_e k_B T}{h^2}\Big)^{3/2}
\exp\!\Big(-\frac{\chi_i}{k_B T}\Big),$$
where `χ_i` is the ionization energy and `g` the degeneracies. The factor
`n_Q = (2π m_e k_B T/h²)^{3/2} = 1/λ³` is the **quantum concentration** (λ = electron
thermal de Broglie wavelength; `λ ≈ 4.30 nm` at 300 K). For a single-ionization pure gas,
`x = n_e/n` solves `x²/(1−x) = S/n` with `S` the RHS above.

*Behavior (illustrative, hydrogen):* although `χ/k_B = 158,000 K ≫ T`, the huge `n_Q`
phase-space factor makes ionization set in much earlier — at `n = 10²³ m⁻³`, `x ≈ 0.02%`
at 6000 K, `≈ 5.6%` at 10,000 K, `≈ 96%` at 20,000 K. `x` rises with `T`, falls with
density `n` (recombination), `→1` as `T→∞`, `→0` as `T→0`. No official key exists for the
Saha values; they are checked for **physical consistency** plus the literature de Broglie
wavelength.

## Bridge
`12.1` provides the combustion enthalpies; this module's `K(T)` (and dissociation extents)
explains why the real flame temperature sits below the adiabatic ideal. The Saha leaf
connects to plasma kinetics (e.g. the KrF excimer / arc-discharge regimes).
