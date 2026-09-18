# 3.4 — Third Law (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. What the third law adds
The first law fixed energy bookkeeping; the second law (`3.3`) gave entropy and a
direction, but only *changes* `ΔS`. The **third law** supplies the missing
**absolute zero of the entropy scale** [M §13.5, p.836].

## 2. Statement
> Based on empirical evidence, this law states that the entropy of a **pure
> crystalline substance is zero at the absolute zero of temperature, 0 K or 0 °R**.
> Substances not having a pure crystalline structure at absolute zero have a
> nonzero value of entropy at absolute zero. [M §13.5.1, p.837]

The evidence comes from low-temperature chemical-reaction studies and specific-heat
measurements as `T → 0` [M §13.5.1, p.837].

## 3. Absolute entropy
Taking `S(0)=0` as datum, the entropy definition `dS = δQ_rev/T = (c_p/T)dT` (Ch. 6,
module `4.2`) integrates to the **absolute entropy**
$$S(T)=\int_0^T \frac{c_p(T')}{T'}\,dT' .$$
This is what populates the standard-entropy tables (Moran Tables A-23, A-25) used for
reacting systems and Gibbs-function evaluations [M §13.5.1, p.837–838].

*Convergence:* near `T=0`, the Debye result `c_p ≈ aT³` gives integrand `aT²→0`, so
$$S(T)=\int_0^T aT'^2\,dT'=\tfrac{1}{3}aT^3 ,$$
finite and `→0` — exactly as the law requires. (Code: `absolute_entropy` numerically
reproduces `absolute_entropy_debye = aT³/3`.)

## 4. Unattainability corollary
A reversible refrigerator between `T_C` and `T_H` has `β = T_C/(T_H − T_C)` (`3.3`,
Eq. 5.10). As `T_C → 0`, `β → 0`: each increment of heat removed near absolute zero
costs ever more work, so **absolute zero cannot be reached in a finite number of
steps**. *Check:* with `T_H=300 K`, `β(250)=5`, `β(50)=0.2`, `β(1)≈0.0033`.

## Bridge
The datum `S(0)=0` makes `4.2`'s entropy *absolute*, enabling absolute-entropy and
Gibbs-function data for **combustion** (Topic 12) and chemical-equilibrium work.
