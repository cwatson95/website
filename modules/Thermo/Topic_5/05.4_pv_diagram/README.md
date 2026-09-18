# 5.4 — The p–v Diagram (area under the path = work)

Topic 5 (Property Data: Tables & Diagrams), the **pressure–volume projection** of the
p–v–T surface.

- **Builds on:** the p–v–T surface, vapor dome, and saturation lines (Moran §3.2–3.3);
  the boundary-work integral `W = ∫p dV` from Topic 2/3.
- **Feeds into:** `5.5` (the dual statement on the T–s diagram, area = heat), `5.EP`
  (the work term of Examples 3.4 and 6.1), `5.EQ`.

## Scope
Projecting the p–v–T surface onto the `p–v` plane shows the two-phase dome bounded by the
saturated-liquid and saturated-vapor lines, meeting at the critical point [Moran §3.2.2,
p.99]. For an **internally reversible** process of a simple compressible substance the
pressure is uniform, so the boundary work is the **area under the path**:
$$W=\int_1^2 p\,dV\quad(\text{Moran Eq. 2.17}).$$

| use | relation | `code/pv_diagram.py` |
|-----|----------|----------------------|
| area under an arbitrary path | trapezoid rule on `(p,V)` | `work_pdV` |
| isobaric work | `W = p(V₂ − V₁)` | `work_isobaric` |
| polytropic `pV ⁿ = const` (n≠1) | `W = (p₂V₂ − p₁V₁)/(1 − n)` | `work_polytropic` |
| isothermal ideal gas (n=1) | `W = p₁V₁ ln(V₂/V₁)` | `work_isothermal_ideal_gas` |
| pressure on a polytrope | `p₂ = p₁(V₁/V₂)ⁿ` | `p_polytropic` |

**Key idea:** the area — hence the work — depends on the **path**, so `W` is not a
property. Two paths between the same end states enclose different areas.

## Run
```bash
cd code && python3 pv_diagram.py          # Ex 2.1 polytropic work + Ex 3.4 / 6.1 isobaric
python3 test_pv_diagram.py                # "All 14 tests passed."
```

## Files
`notes.md`, `code/pv_diagram.py`, `code/test_pv_diagram.py`, `problems/problems.md`, `refs.md`.
