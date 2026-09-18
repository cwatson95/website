# 3.1 — Problems

Check with `code/temperature.py`. Citations in `../refs.md`. In any thermodynamic
relation, `T` must be **absolute** (K or °R).

### P1.  Four-scale conversion  *(Moran 8e §1.7, Eqs. 1.16–1.19, p.21–22)*
A furnace wall sits at 1200 K. Express it in °R, °C, and °F.
*Answer:* °R = 1.8·1200 = **2160**; °C = 1200 − 273.15 = **926.85**;
°F = 1.8·926.85 + 32 = **1700.33**.
*Check:* `rankine_from_kelvin(1200)` = 2160; `celsius_from_kelvin(1200)` = 926.85;
`fahrenheit_from_celsius(926.85)` = 1700.33.

### P2.  Absolute vs shifted scales in a ratio  *(Moran 8e §1.7.2, p.21)*
A Carnot engine runs between 27 °C and 327 °C. A student writes "efficiency" as
`1 − 27/327 = 0.917`. What is wrong, and what is the correct temperature ratio?
*Answer:* ratios require **absolute** `T`. `T_C = 300.15 K`, `T_H = 600.15 K`, so
`1 − 300.15/600.15 ≈ 0.500`. The °C version (0.917) is meaningless. (Carnot η is
developed in `3.3`.)
*Check:* `kelvin_from_celsius(27)` = 300.15; `kelvin_from_celsius(327)` = 600.15;
`1 - 300.15/600.15` ≈ 0.4999.

### P3.  The thermometer is the "third body"  *(Moran 8e §1.7, p.19)*
Block A reads 350 K on a thermometer; block B reads 350 K on the *same*
thermometer; the two blocks are never touched together. Are they in thermal
equilibrium?
*Answer:* **Yes** — by the zeroth law, `A~C` and `B~C` (C = thermometer) ⇒ `A~B`.
*Check:* `zeroth_law(350, 350, 350)` → `True`.

### P4.  Where Celsius equals Fahrenheit  *(Moran 8e Eq. 1.19, p.22)*
Find the temperature at which the Celsius and Fahrenheit readings are numerically
equal.
*Answer:* set `T = 1.8T + 32` ⇒ `−0.8T = 32` ⇒ `T = −40` (−40 °C = −40 °F).
*Check:* `fahrenheit_from_celsius(-40)` = −40.0.
