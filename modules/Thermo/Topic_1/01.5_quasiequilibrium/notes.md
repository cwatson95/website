# 1.5 — Quasiequilibrium Processes (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 17; `refs.md`).

## 1. The idealization
A **quasiequilibrium** (quasistatic) process is one in which [M §2.2.5, p.48–49]:

> …the departure from thermodynamic equilibrium is **at most infinitesimal**.

Every state the system passes through is therefore (to within an infinitesimal) an
equilibrium state, so a single uniform pressure `p` is defined at each step. Two
consequences:
- the process traces a **continuous path** of equilibrium states that can be
  drawn on a `p–V` diagram;
- the boundary work is the **area under that path** [M §2.2.3, Eq. 2.17, p.48]:
$$W=\int_{V_1}^{V_2} p\,dV .$$
Without quasiequilibrium, `p` is not single-valued during the process and this
integral is undefined — real rapid processes are bounded *between* quasiequilibrium
limits. Code: `pdv_work(p_of_V, V1, V2)` integrates any path.

## 2. Work is a path function
The central lesson: `W` depends on the **path**, not just the end states. Take the
same end states `A=(100\,\mathrm{kPa},\,2\,\mathrm{m^3})` and
`B=(200\,\mathrm{kPa},\,1\,\mathrm{m^3})` and connect them three ways:

| path | construction | `W` (kJ) |
|------|--------------|----------|
| isothermal `n=1` (`pV=200`) | `polytropic_work(100,2,1,1)` | `−138.63` |
| const-`p` (100) then const-`V` (1) | `path_work([("p",100,2,1),("V",1)])` | `−100.00` |
| const-`V` (2) then const-`p` (200) | `path_work([("V",2),("p",200,2,1)])` | `−200.00` |

Same endpoints, three different areas, three different works. Hence `W` (and
likewise `Q`) is **not a property** — it is a path function, written `δW` not
`dW`. By contrast `ΔU` between `A` and `B` is the same for all three paths
(module `1.2`). Code: `path_work(segments)` sums constant-`p`, constant-`V`, and
polytropic legs; `constant_pressure_work` and `constant_volume_work`(`=0`) are
the straight-line legs.

## 3. Why it underpins the rest
Every `∫p dV` in module `1.2` (polytropic work), in expansion/compression work
(group `2`), and every closed cycle drawn on a `p–V` diagram (group `9`) tacitly
assumes quasiequilibrium so that the area is meaningful. The polytropic family
`pVⁿ=const` is the standard worked path [M Example 2.1, p.50].
