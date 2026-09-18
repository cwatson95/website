# SM-02 — Laws of Thermodynamics (notes)

Thermodynamics is the macroscopic face of `~SM-01`'s counting: once entropy is
S = k ln Ω, the laws and all the thermodynamic relations follow by calculus.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria 3e;
**Sch** = Schroeder, *Thermal Physics* (image-only, cited by chapter). Printed pages.

## 1. The four laws
- **Zeroth:** thermal equilibrium is transitive — a consistent **temperature** exists.
- **First:** energy is conserved, $dU = T\,dS - P\,dV + \mu\,dN$ (heat + work + matter).
- **Second:** the entropy of an isolated system never decreases, $dS_\text{total}\ge 0$.
- **Third:** $S\to 0$ as $T\to 0$ (a unique, perfectly ordered ground state).

## 2. Temperature from entropy
Temperature is *defined* by how entropy responds to energy [Pa §1.2, p.3; §1.3, p.6]:
$$\frac1T=\left(\frac{\partial S}{\partial U}\right)_{V,N},\qquad
  \frac{P}{T}=\left(\frac{\partial S}{\partial V}\right)_{U,N},\qquad
  -\frac{\mu}{T}=\left(\frac{\partial S}{\partial N}\right)_{U,V}.$$
For the ideal gas $S=\tfrac32 Nk\ln U+\cdots$, so $1/T=\tfrac32 Nk/U$, i.e.
$U=\tfrac32 NkT$ — equipartition. Code: `temperature_from_entropy(S_of_U, U)`
(finite difference with a step **relative** to U, so it works for U ~ 10⁻²¹ J).

## 3. Thermodynamic potentials and Legendre transforms
Different experiments hold different variables fixed, so it is convenient to trade
$U(S,V)$ for potentials whose natural variables match [Sch Ch.5; Pa §3.3, p.50]:
$$H=U+PV,\qquad F=U-TS,\qquad G=U-TS+PV=H-TS.$$
Each is a **Legendre transform** swapping a variable for its conjugate
($S\leftrightarrow T$, $V\leftrightarrow P$). At fixed $(T,V)$ equilibrium minimizes
$F$; at fixed $(T,P)$ it minimizes $G$. Statistical mechanics delivers $F$ directly
from the partition function, $F=-kT\ln Z$ (`~SM-03`, Pa §3.3). Code: `enthalpy`,
`helmholtz_free_energy`, `gibbs_free_energy`; `pressure_from_helmholtz` gives
$P=-(\partial F/\partial V)_T$.

## 4. Maxwell relations
Because mixed second derivatives commute, each potential yields an identity. From
$dF=-S\,dT-P\,dV$ [Sch Ch.5]:
$$\left(\frac{\partial S}{\partial V}\right)_T=\left(\frac{\partial P}{\partial T}\right)_V.$$
For the ideal gas both sides equal $Nk/V$. Code: `maxwell_relation_residual` checks
this numerically (residual ≈ 0).

## 5. The Carnot cycle and the second law
No engine between reservoirs $T_h>T_c$ beats the reversible **Carnot** efficiency
[Sch Ch.4]:
$$\eta_\text{Carnot}=1-\frac{T_c}{T_h},$$
with refrigerator/heat-pump COPs $T_c/(T_h-T_c)$ and $T_h/(T_h-T_c)$. The second law
shows up directly when heat $Q$ flows spontaneously hot → cold: the total entropy
rises, $dS=Q(1/T_c-1/T_h)>0$. Code: `carnot_efficiency`, `carnot_cop_*`,
`total_entropy_change_heat_flow`.

## Where this goes
- `~SM-03` computes $F=-kT\ln Z$ from a microscopic partition function, closing the loop with `~SM-01`.
- The potentials and Maxwell relations are the everyday tools of chemical thermodynamics and phase equilibria (`~SM-05`).
- Engineering thermodynamics (Carnot, cycles) is developed in the standalone `modules/Thermo` set.
