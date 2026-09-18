# 3.4 — Problems

Check with `code/third_law.py`. Citations in `../refs.md`. `T` absolute (K/°R).

### P1.  The entropy datum  *(Moran 8e §13.5.1, p.837)*
What is the entropy of a pure crystalline substance at 0 K? Of a substance that is
*not* perfectly crystalline at 0 K?
*Answer:* `S = 0` for the pure crystal (third law); the non-crystalline substance
has a nonzero **residual** entropy. *Check:* `standard_entropy_at_zero(True)` = 0.0;
`standard_entropy_at_zero(False)` → None.

### P2.  Absolute entropy converges  *(Moran 8e §13.5.1, p.837)*
Using the low-`T` model `c_p = aT³` with `a = 1×10⁻³`, find the absolute entropy at
10 K both analytically and from the integral `∫₀ᵀ c_p/T dT`.
*Answer:* `S = ∫₀¹⁰ aT² dT = a·10³/3 = 1/3 ≈ 0.3333`. The integrand `aT² → 0` at the
origin, so the integral is finite. *Check:* `absolute_entropy_debye(10, 1e-3)` = 1/3;
`absolute_entropy(10, lambda T: debye_cp(T,1e-3))` ≈ 0.3333.

### P3.  Why absolute zero is unattainable  *(Moran 8e §5.9.2, p.267; third-law corollary)*
A reversible refrigerator rejects heat to `T_H = 300 K`. Tabulate its COP for
`T_C = 250, 50, 1 K`. What does the trend imply about reaching 0 K?
*Answer:* `β = T_C/(T_H−T_C)`: `β(250)=5`, `β(50)=0.2`, `β(1)≈0.0033`. As `T_C→0`,
`β→0`, so the work per unit heat removed → ∞ — absolute zero is unattainable in
finite steps. *Check:* `carnot_cop_refrigerator(1, 300)` ≈ 0.00334 < `...(250,300)` = 5.

### P4.  Residual entropy  *(Moran 8e §13.5.1, p.837)*
Why does CO (carbon monoxide) retain a small entropy as `T → 0`, contrary to the
naive `S→0`?
*Answer:* CO freezes into a crystal with **orientational disorder** (C–O vs O–C),
i.e. it is not a *perfect* pure crystal; the third law's `S=0` applies only to the
ideal pure-crystalline state, so CO keeps a residual entropy. *Check (concept):*
`standard_entropy_at_zero(pure_crystalline=False)` → None.
