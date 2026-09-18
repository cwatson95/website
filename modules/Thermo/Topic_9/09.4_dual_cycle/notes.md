# 09.4 — Air-Standard Dual Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Why a third cycle
Real internal-combustion p–V diagrams sit *between* the Otto (constant-volume burn) and
Diesel (constant-pressure burn) idealizations. The **dual cycle** captures both by adding
heat in two steps [M §9.4, p.522]:

- **1–2** isentropic compression;
- **2–3** constant-**volume** heat addition — the Otto-like part, set by the *pressure
  ratio* $r_p=p_3/p_2$;
- **3–4** constant-**pressure** heat addition — the Diesel-like part, set by the
  *cutoff ratio* $r_c=V_4/V_3$; this is also the first part of the power stroke;
- **4–5** isentropic expansion — the rest of the power stroke;
- **5–1** constant-volume heat rejection.

## 2. Efficiency is built from the Otto and Diesel pieces
Process 2–3 (constant $V$) gives $Q_{23}/m=u_3-u_2$; process 3–4 (constant $p$) gives
$Q_{34}/m=h_4-h_3$; rejection 5–1 gives $Q_{51}/m=u_5-u_1$. So [M §9.4, p.523]
$$\eta=1-\frac{u_5-u_1}{(u_3-u_2)+(h_4-h_3)}\quad(9.14)\qquad(\text{air-table, Table A-22}).$$

## 3. Cold air-standard closed form
With constant specific heats and $V_5/V_4=r/r_c$ (since $V_5=V_1$, $V_3=V_2$),
$$\boxed{\ \eta=1-\frac{1}{r^{\,k-1}}\,\frac{r_p\,r_c^{\,k}-1}{(r_p-1)+k\,r_p\,(r_c-1)}\ }.$$
It **brackets** the two simpler cycles at the same $r$:

| limit | what drops out | result |
|---|---|---|
| $r_c\to1$ | no constant-$p$ burn | Otto, $\eta=1-1/r^{k-1}$ (9.8) |
| $r_p\to1$ | no constant-$V$ burn | Diesel, $\eta=1-\dfrac{1}{r^{k-1}}\dfrac{r_c^{k}-1}{k(r_c-1)}$ (9.13) |

## 4. Worked check — Example 9.3
$r=18$, $r_p=1.5$, $r_c=1.2$, $T_1=300$ K, $p_1=0.1$ MPa. States 1–2 are those of the
Diesel Example 9.2: $u_1=214.07$, $T_2=898.3$ K, $u_2=673.2$. Then $T_3=r_pT_2=1347.5$ K
($h_3=1452.6$, $u_3=1065.8$); $T_4=r_cT_3=1617$ K ($h_4=1778.3$, $v_{r4}=5.609$);
$v_{r5}=v_{r4}(V_5/V_4)=5.609\cdot15=84.135\Rightarrow u_5=475.96$ kJ/kg [M §9.4, p.523–524].
$$\eta=1-\frac{475.96-214.07}{(1065.8-673.2)+(1778.3-1452.6)}=1-\frac{261.89}{718.3}=0.635\,(63.5\%).$$
Net work $=456$ kJ/kg, $Q_{\text{in}}=718$ kJ/kg, and with $v_1=0.861$ m³/kg
mep $=W/[v_1(1-1/r)]=0.56$ MPa. The cold air-standard closed form for the same $r,r_p,r_c$
gives $0.680$ — again constant specific heats **overpredict**.

## Bridge
The dual cycle is the parent of `09.2` (Otto, $r_c\to1$) and `09.3` (Diesel, $r_p\to1$);
the Carnot ceiling (`09.1`) still bounds it. Next, `09.5` leaves the piston engine for the
**gas-turbine (Brayton)** cycle, and `09.6` for the **vapor-power (Rankine)** cycle.
Efficiency definitions are in `07.1`; air tables live in Topic 5.
