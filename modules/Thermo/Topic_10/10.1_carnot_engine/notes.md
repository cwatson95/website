# 10.1 — Carnot Engine (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The Carnot cycle
The **Carnot cycle** is the concrete realization of a *reversible* power cycle
operating between two thermal reservoirs at $T_H$ and $T_C$. The system (a gas in a
piston–cylinder, or steam circulating through boiler/turbine/condenser/pump)
executes **four internally reversible processes**: two adiabatic processes
alternated with two isothermal processes [M §5.10, p.270].

For the gas Carnot **power** cycle (Figs. 5.13–5.14) [M §5.10.1, p.270–271]:

| Process | type | what happens |
|---|---|---|
| 1–2 | adiabatic (isentropic) compression | $T_C \to T_H$ on the insulating stand |
| 2–3 | isothermal expansion at $T_H$ | gas receives $Q_H$ from the hot reservoir |
| 3–4 | adiabatic (isentropic) expansion | $T_H \to T_C$ on the insulating stand |
| 4–1 | isothermal compression at $T_C$ | gas discharges $Q_C$ to the cold reservoir |

On a **p–v diagram** the enclosed (shaded) area is the net work per unit mass; on a
**T–s diagram** the cycle is a *rectangle* — two horizontal isotherms ($T_H$, $T_C$)
and two vertical isentropes — so $Q_H=T_H\Delta s$ in and $Q_C=T_C\Delta s$ out, with
$W=(T_H-T_C)\Delta s$. The same efficiency (Eq. 5.9) holds for the steam (vapor)
Carnot cycle of Fig. 5.15, where the isothermals are constant-pressure phase
changes [M §5.10.1, p.271–272].

## 2. Carnot efficiency
Combining the reversible heat ratio $(Q_C/Q_H)_{rev}=T_C/T_H$ (Eq. 5.7) with the
efficiency definition $\eta=1-Q_C/Q_H$ (Eq. 5.4) gives the **Carnot efficiency**
$$\eta_{max}=1-\frac{T_C}{T_H}\quad(5.9),$$
with $T$ on the **Kelvin or Rankine** scale [M §5.9.1, p.265]. It rises as $T_H$
increases and/or $T_C$ decreases. *Check:* $T_H=2000$ K, $T_C=400$ K gives
$\eta_{max}=1-400/2000=0.80$ (book 80%); $T_H=745$ K, $T_C=298$ K gives 0.60.

This is the **ceiling**: by the Carnot corollaries (module `3.3`), no power cycle
between the same two reservoirs can exceed it, and *all* reversible ones equal it.
Conventional power cycles reach ~40% — to be judged against this limit, not 100%
[M §5.9.1, p.266].

## 3. Worked example — Example 5.1 (p.266)
A power cycle runs between $T_H=2000$ K and $T_C=400$ K with $Q_H=1000$ kJ, so
$\eta_{max}=0.80$. Classify each claim against the ceiling:

- **(a)** $\eta=60\%<80\%$ → operates **irreversibly**.
- **(b)** $W_{cycle}=850$ kJ ⇒ $\eta=850/1000=0.85>0.80$ → **impossible**.
- **(c)** $Q_C=200$ kJ ⇒ $W=800$ kJ ⇒ $\eta=0.80=\eta_{max}$ → operates **reversibly**
  (this is exactly the Carnot cycle: $Q_C=Q_H\,T_C/T_H=200$ kJ, $W=800$ kJ).

## 4. Reversed Carnot cycle — refrigerator & heat pump
Run the Carnot cycle **backwards** and the energy transfers reverse: it becomes a
reversible refrigeration or heat-pump cycle [M §5.10.2, p.272]. Their coefficients
of performance are the Carnot ceilings
$$\beta_{max}=\frac{T_C}{T_H-T_C}\ (5.10),\qquad
\gamma_{max}=\frac{T_H}{T_H-T_C}\ (5.11),\qquad \gamma_{max}=\beta_{max}+1,$$
with $T$ absolute [M §5.9.2, p.267]. (Worked in Examples 5.2 and 5.3; see `10.EP`.)

## Bridge
The Carnot ceiling caps every real engine in **Topic 9** (Otto, Diesel, Brayton,
Rankine) and rates the devices in Topic 8. The **Stirling** and **Ericsson** cycles
(`10.2`) are *other* reversible cycles that reach this very same ceiling through
ideal regeneration. The corollaries behind Eq. 5.9 are derived in module `3.3`.
