# 1.3 — Extensive Properties (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 17; `refs.md`).

A **property** is a macroscopic characteristic of a system (mass, volume,
pressure, temperature, energy) to which a definite value can be assigned at an
instant without knowing the history — its value fixes part of the **state**
[M §1.3.2, p.9].

Properties split into two classes [M §1.3.3 *Extensive and Intensive Properties*,
p.9]:

> A property is **extensive** if its value for the whole system is the **sum** of
> the values for its parts. Extensive properties depend on the **size or extent**
> of a system and may change with time.

So mass `m`, volume `V`, total energy `E` (and its parts `U`, `KE`, `PE`),
enthalpy `H`, and entropy `S` are extensive. Two operational signatures:

$$X_\text{total}=\sum_i X_i \qquad\text{(additive over subsystems)},$$
$$X(k\cdot\text{system})=k\,X(\text{system})\qquad\text{(scales with extent)}.$$

Code: `total(values)` sums an extensive property over subsystems;
`is_additive(parts, whole)` tests it; `scales_with_extent(X_unit, k)` shows `k`
copies carry `k·X`; the helpers `volume = m·v`, `internal_energy = m·u`,
`kinetic_energy = ½mV²` are written as *extent × per-mass value* to make the
size dependence explicit.

*Check:* a 3 kg system split into 2 kg + 1 kg at the **same** specific volume
`v` has `V(2) + V(1) = V(3)` — but its specific volume does **not** add; it
stays `v` (that is the intensive side, module `1.4`). Extensive properties live
inside every balance equation: the closed-system `ΔU` (`1.2`) and the
control-volume `dE_cv/dt` (`1.1`) are changes in extensive energy.

Equilibrium — when no further change occurs once the system is isolated — is the
state at which properties are uniform and well defined [M §1.3.4, p.10].
