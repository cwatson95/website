# 1.5 — Problems

Check with `code/quasiequilibrium.py`. Citations in `../refs.md`.

### P1.  Area under a polytropic path  *(Moran 8e Example 2.1, p.50)*
A gas expands along `pV = const` (isothermal, `n=1`) from `100 kPa, 2 m³` to
`1 m³`. Find the work as the area `∫p dV`.
*Answer:* `W = p₁V₁ ln(V₂/V₁) = 100(2)ln(½) = −138.63 kJ`.
*Check:* `polytropic_work(100,2,1,1)` ≈ −138.63; numerically
`pdv_work(lambda V:200/V, 2, 1)` agrees (here `pV=200`).

### P2.  Work depends on the path  *(Moran 8e §2.2.3, p.48)*
Connect the **same** end states `A=(100 kPa, 2 m³)` and `B=(200 kPa, 1 m³)` by
(i) const-`p` then const-`V`, and (ii) const-`V` then const-`p`. Find each work
and compare to P1.
*Answer:* (i) `W = 100(1−2) + 0 = −100 kJ`; (ii) `W = 0 + 200(1−2) = −200 kJ`.
Three paths → three works (`−138.63 / −100 / −200`): `W` is a **path function**.
*Check:* `path_work([("p",100,2,1),("V",1)])` = −100;
`path_work([("V",2),("p",200,2,1)])` = −200.

### P3.  Constant-volume and constant-pressure legs  *(Moran 8e §2.2.3, Eq. 2.17)*
What is the boundary work of (a) a rigid tank being heated, and (b) a gas pushed
out at constant 200 kPa from 1 m³ to 3 m³?
*Answer:* (a) `W = 0` (no volume change); (b) `W = 200(3−1) = 400 kJ`.
*Check:* `constant_volume_work(1)` = 0; `constant_pressure_work(200,1,3)` = 400.
