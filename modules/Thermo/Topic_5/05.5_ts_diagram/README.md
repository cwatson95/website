# 5.5 — The T–s Diagram (area under the path = heat)

Topic 5 (Property Data: Tables & Diagrams), the **temperature–entropy projection** and the
Mollier (enthalpy–entropy) chart.

- **Builds on:** entropy data from the steam tables (`5.1` supplies `sf, sg`); the dual
  statement on the p–v diagram (`5.4`, area = work).
- **Feeds into:** cycle analysis (Carnot, Rankine) in later topics; `5.EP` (the heat term
  of Example 6.1), `5.EQ`.

## Scope
For an **internally reversible** process `dS = (δQ/T)`, so heat is the **area under the
path** on a T–s diagram, with `T` in **kelvin** [Moran Eq. 6.23, §6.6.1, p.302]:
$$Q_{\text{int,rev}}=\int_1^2 T\,dS .$$

| use | relation | `code/ts_diagram.py` |
|-----|----------|----------------------|
| area under a T–s path | trapezoid rule on `(T,S)` | `heat_TdS` |
| isothermal heat | `Q = T(S₂ − S₁)` | `heat_isothermal` |
| linear `T`-in-`S` | `Q = ½(T₁ + T₂)(S₂ − S₁)` | `heat_linear_TS` |
| Carnot net work (enclosed area) | `W = (T_H − T_C)ΔS` | `carnot_net_work` |
| Carnot efficiency | `η = 1 − T_C/T_H` | `carnot_efficiency` |

**Key idea:** the T–s area is the reversible heat, just as the p–v area is the reversible
work. A Carnot cycle is a **rectangle** on T–s; its enclosed area is the net heat = net
work, and the efficiency reduces to a ratio of temperatures (Moran §6.6.2).

## Run
```bash
cd code && python3 ts_diagram.py          # Ex 6.1 isothermal heat + Carnot rectangle
python3 test_ts_diagram.py                # "All 15 tests passed."
```

## Files
`notes.md`, `code/ts_diagram.py`, `code/test_ts_diagram.py`, `problems/problems.md`, `refs.md`.
