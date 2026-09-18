# 09.1 — Carnot Cycle (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Why start with Carnot
Topic 9 is a tour of real power and refrigeration cycles — Otto, Diesel, dual,
Brayton, Rankine. Every one of them is judged against a single yardstick: the
**Carnot cycle**, the reversible cycle that delivers the *most* work (or the *best*
COP) between two thermal reservoirs [M §5.10, p.270]. It is the practical face of the
second law (`3.3`) and of the efficiency definitions (`07.1`).

## 2. The four internally reversible processes
A Carnot cycle always has the same four internally reversible processes — **two
adiabatic alternated with two isothermal** [M §5.10, §5.10.3, p.270, 273]. For the
**power** cycle of a gas in a piston–cylinder (Figs. 5.13–5.14):

- **1–2** adiabatic compression, $T_C\to T_H$;
- **2–3** isothermal expansion at $T_H$, receiving $Q_H$;
- **3–4** adiabatic expansion, $T_H\to T_C$;
- **4–1** isothermal compression at $T_C$, rejecting $Q_C$.

The enclosed area on the $p$–$v$ diagram is the net work. The same four steps run a
Carnot **vapor** cycle (boiler/turbine/condenser/pump, Fig. 5.15) [M §5.10.1, p.271].

## 3. Carnot efficiency — Eq. 5.9
For the reversible cycle, $(Q_C/Q_H)_{rev}=T_C/T_H$ (Eq. 5.7), so the thermal
efficiency reduces to a ratio of **absolute** temperatures only:
$$\eta_{max}=1-\frac{T_C}{T_H}\quad(5.9).$$
By the Carnot corollaries this is the efficiency of *all* reversible cycles between
$T_H,T_C$ and the **maximum any cycle can reach** [M §5.10.1/§5.10.3, p.271, 273].
*Check:* $T_H=2000$ K, $T_C=400$ K $\Rightarrow\eta_{max}=1-400/2000=0.80$ (Ex 5.1).

## 4. Reverse it: refrigerator and heat pump
Run the cycle backward (Fig. 5.16) and it pumps heat from cold to hot with the best
possible coefficients of performance [M §5.10.2, p.272]:
$$\beta_{max}=\frac{T_C}{T_H-T_C}\ (5.10),\qquad
\gamma_{max}=\frac{T_H}{T_H-T_C}\ (5.11),\qquad \gamma_{max}=\beta_{max}+1.$$
*Check:* a freezer at $T_C=268$ K in $T_H=295$ K air has $\beta_{max}=268/27=9.9$
(Ex 5.2); a house at $530\,^\circ$R from $492\,^\circ$R air has
$\gamma_{max}=530/38=13.95$ (Ex 5.3). **`T` in K or °R only.**

## 5. The ceiling in action
No Otto, Diesel, Brayton, or Rankine cycle (09.2–09.6) can beat $\eta_{max}$ for its
hot/cold extremes — they fall short because of finite-temperature heat addition and
internal irreversibility. The cold air-standard Otto at $r=8$ reaches $0.565$, the
ideal Brayton at $r_p=10$ reaches $0.482$, the ideal Rankine at 8 MPa/0.008 MPa
reaches $0.371$ — all under the Carnot value for their reservoir temperatures.

## Bridge
Carnot ties together `3.3` (second-law corollaries, same `carnot_*` functions),
`07.1` (the efficiency/COP definitions it bounds), and the rest of **Topic 9**: it is
the reversible limit each engine and refrigerator is compared against. The work the
real cycle loses relative to Carnot is exactly the destroyed exergy (`4.3`),
$E_d=T_0\sigma$.
