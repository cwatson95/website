# 09.3 — Air-Standard Diesel Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Compression ignition
The Diesel cycle models the **compression-ignition** engine. It keeps the Otto cycle's
isentropic compression but, instead of a spark at constant volume, injects fuel into the
hot compressed air so that combustion proceeds at constant **pressure** [M §9.3, p.518]:

- **1–2** isentropic compression;
- **2–3** constant-**pressure** heat addition (the burn) — also the first part of the
  power stroke;
- **3–4** isentropic expansion;
- **4–1** constant-volume heat rejection.

## 2. Heat added is an enthalpy difference
Process 2–3 does $p\,dV$ work, so $Q_{23}/m=u_3-u_2+p(v_3-v_2)=h_3-h_2$ (Eq. 9.10). With
the constant-volume rejection $Q_{41}/m=u_4-u_1$, the efficiency is [M §9.3, p.519]:
$$\eta=1-\frac{u_4-u_1}{h_3-h_2}\quad(9.11)\qquad(\text{air-table, Table A-22}).$$

## 3. Cold air-standard closed form — Eq. 9.13
Introduce the **cutoff ratio** $r_c=V_3/V_2=T_3/T_2$ (how far the constant-pressure burn
stretches the volume). With constant specific heats and $V_4/V_3=r/r_c$ (Eq. 9.12),
$$\boxed{\ \eta=1-\frac{1}{r^{\,k-1}}\left[\frac{r_c^{\,k}-1}{k\,(r_c-1)}\right]\ }\quad(9.13).$$
The bracket exceeds 1 for $r_c>1$, so Eq. 9.13 differs from the Otto Eq. 9.8 only by that
factor: **at the same $r$ the Diesel cycle is less efficient than the Otto** cycle
[M §9.3, p.519–520]. As $r_c\to1$ the bracket $\to1$ and Eq. 9.13 reduces to Eq. 9.8.
Diesels recover by running much higher compression ratios (12–20).

## 4. Worked check — Example 9.2
$r=18$, $r_c=2$, $T_1=300$ K, $p_1=0.1$ MPa. Air-table states: $u_1=214.07$,
$h_2=930.98$, $h_3=1999.1$, $u_4=664.3$ kJ/kg, with $T_2=898.3$ K, $T_3=1796.6$ K,
$T_4=887.7$ K, $p_2=5.39$ MPa.
$$\eta=1-\frac{664.3-214.07}{1999.1-930.98}=1-\frac{450.23}{1068.12}=0.578\ (57.8\%).$$
The cold air-standard closed form for the same $r,r_c$ gives $0.632$ — again the
constant-$c_p$ assumption overpredicts [M §9.3, p.521]. mep $=0.76$ MPa.

## Bridge
Same isentropic compression as Otto (`09.2`); the dual cycle (`09.4`) blends Diesel's
constant-$p$ burn with Otto's constant-$v$ burn, and Eq. 9.13 is the $r_p\to1$ limit of
the dual efficiency. Carnot (`09.1`) still bounds it; efficiency definitions in `07.1`.
