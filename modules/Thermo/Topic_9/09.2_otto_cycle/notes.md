# 09.2 — Air-Standard Otto Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The spark-ignition idealization
The Otto cycle is the air-standard model of the **spark-ignition** (gasoline) engine.
The messy intake–compress–combust–expand–exhaust of a real four-stroke engine is
replaced by four internally reversible processes of a fixed mass of air [M §9.2, p.513]:

- **1–2** isentropic compression;
- **2–3** constant-**volume** heat addition (the spark-ignited burn, assumed instant at
  top dead center);
- **3–4** isentropic expansion — the power stroke;
- **4–1** constant-volume heat rejection.

## 2. Energy transfers and efficiency
Treating each stroke as a closed system with $\Delta\text{ke}=\Delta\text{pe}=0$, the
work and heat reduce to internal-energy differences (Eq. 9.2). The thermal efficiency
is net work over heat added [M §9.2, p.514]:
$$\eta=\frac{(u_3-u_2)-(u_4-u_1)}{u_3-u_2}=1-\frac{u_4-u_1}{u_3-u_2}\quad(9.3).$$
Moran's primary route evaluates $u$ from the **air table** (Table A-22), which keeps the
temperature variation of the specific heats.

## 3. Cold air-standard closed form — Eq. 9.8
On a **cold air-standard** basis the specific heats are constant, and the isentropic
legs give [M §9.2, p.514–515]
$$\frac{T_2}{T_1}=r^{k-1}\ (9.6),\qquad \frac{T_4}{T_3}=\frac{1}{r^{k-1}}\ (9.7),$$
with $r=V_1/V_2$ the **compression ratio**. Since $T_4/T_1=T_3/T_2$, Eq. 9.3 collapses to
$$\boxed{\ \eta=1-\frac{1}{r^{\,k-1}}\ }\quad(9.8)\quad(\text{cold air-standard, }k=1.4).$$
Efficiency depends only on $r$ and $k$ — it **rises with compression ratio** (Fig. 9.4).
Autoignition ("knock") caps spark-ignition $r$ near 9.5–11.5 [M §9.2, p.515].

## 4. Worked check — Example 9.1
$r=8$, $T_1=540\,^\circ$R, $p_1=1$ atm, $T_3=3600\,^\circ$R (max). Two analyses:

| parameter | air-table (Table A-22E) | cold air-standard, $k=1.4$ |
|---|---|---|
| $T_2$ | 1212 °R | $540\cdot8^{0.4}=1241$ °R |
| $T_4$ | 1878 °R | $3600/8^{0.4}=1567$ °R |
| $\eta$ | **0.51** (Eq. 9.3) | **0.565** (Eq. 9.8) |
| mep | 8.03 atm | 7.05 atm |

The constant-$c_v$ assumption **overpredicts** $\eta$ (0.565 vs 0.51) because real
specific heats grow with temperature [M §9.2, p.516–517]. Both numbers are read from
the book's own comparison table.

## Bridge
The Carnot ceiling (`09.1`) for these reservoir temperatures (~2000 K / 400 K) is
$0.80$, well above 0.565 — the Otto cycle loses ground to finite-temperature heat
addition. The Diesel cycle (`09.3`) keeps the isentropic compression but burns at
constant **pressure**; the dual cycle (`09.4`) does both. Efficiency definitions are
in `07.1`; the air tables live in Topic 5.
