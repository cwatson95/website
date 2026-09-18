# 1.2 — References

Page numbers verified by **reading the actual page text** in the PDF.
**Printed** = number on the page; **PDF** = 0-based viewer index.

| Book (edition) | File | Printed → PDF offset |
|---|---|---|
| Moran, Shapiro, Boettner & Bailey, *Fundamentals of Engineering Thermodynamics*, **8th ed.** (Wiley, 2014) | `modules/Thermo/thermodynamics.pdf` | PDF = printed **+ 17** |

## Topic → location

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| closed system / control mass (def.); isolated system | §1.2.1 *Closed Systems* | — | 6 | 24 |
| kinetic energy (`delta_KE`) | §2.1.1 *Work and Kinetic Energy* | 2.5 | 41 | 59 |
| potential energy (`delta_PE`) | §2.1.2 *Potential Energy* | 2.10 | 42 | 60 |
| closed-system energy balance (`energy_balance_residual`, `heat_transfer`, `work_done`) | §2.5 *Energy Accounting: Energy Balance for Closed Systems* | **2.35a** (E₂−E₁=Q−W), **2.35b** (ΔKE+ΔPE+ΔU=Q−W) | 60 (sec) / 61 (eq) | 77 / 78 |
| time-rate form (`power_balance_residual`) | §2.5.1 *Important Aspects of the Energy Balance* | **2.37** (dE/dt=Q̇−Ẇ); 2.36, 2.38 | 62 | 80 |
| expansion/compression work `∫p dV` (`pdv_work_trapz`) | §2.2.3 *Modeling Expansion or Compression Work* | **2.17** (also 2.15, 2.16) | 47 (sec) / 48 (eq) | 64 / 65 |
| quasiequilibrium process (prereq; see module 1.5) | §2.2.5 *Expansion or Compression Work in Quasiequilibrium Processes* | — | 48–49 | 66–67 |
| polytropic work (`polytropic_work`, `polytropic_pressure`, `constant_pressure_work`) | §2.2.5; derived in **Example 2.1** *Evaluating Expansion Work* | Ex 2.1 Eq **(a)** (p₂V₂−p₁V₁)/(1−n); Eq **(b)** p₁V₁ln(V₂/V₁), n=1 | 50–51 | 68–69 |

## See also
- `1.1` open systems (`../01.1_open_systems/refs.md`) — the control-volume
  generalization of this energy balance.
- `1.5` quasiequilibrium — why `∫p dV` is well defined.
- Worked examples for `problems/problems.md`: **Example 2.1** (expansion work,
  p.50), **Example 2.2** "Cooling a Gas in a Piston–Cylinder" (closed-system
  energy balance, p.64). End-of-chapter problems: Ch.2 pp.81–90.
