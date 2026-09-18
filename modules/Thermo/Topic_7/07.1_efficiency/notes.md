# 07.1 — Efficiency (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. One idea, many names
Every performance metric in this module is the same ratio —
$$\text{performance}=\frac{\text{desired energy effect}}{\text{required energy input}}.$$
What changes is *what you want* and *what it costs* [M §2.6, p.73]. For a **cycle** the
inputs/outputs are heat and net work; for a single **device** they are enthalpies.
Throughout §2.6 the symbols $Q_{in},Q_{out},Q_C,Q_H,W_{cycle}$ are taken as **positive
magnitudes**, with directions fixed by the arrows on Fig. 2.17 [M §2.6.1, p.73].

## 2. Thermal efficiency (power cycle)
A power cycle takes in $Q_{in}$ from the hot body and rejects $Q_{out}$ to the cold body;
the energy balance is $W_{cycle}=Q_{in}-Q_{out}$ (Eq. 2.41). The fraction converted to
work is the **thermal efficiency**
$$\eta=\frac{W_{cycle}}{Q_{in}}\quad(2.42),\qquad
\eta=\frac{Q_{in}-Q_{out}}{Q_{in}}=1-\frac{Q_{out}}{Q_{in}}\quad(2.43),$$
and since energy is conserved $\eta<1$ always — not all heat in becomes work
[M §2.6.2, p.74].

## 3. Coefficients of performance (refrigerator, heat pump)
Reverse the arrows (Fig. 2.17b): a work input $W_{cycle}=Q_{out}-Q_{in}$ (Eq. 2.44) drives
heat from cold to hot. The two devices share hardware but differ in *objective*, so their
ratios — **coefficients of performance** — differ [M §2.6.3, p.75]:
$$\beta=\frac{Q_C}{W_{cycle}}\ (2.45)\quad(\text{refrigerator: want }Q_C),\qquad
\gamma=\frac{Q_H}{W_{cycle}}\ (2.47)\quad(\text{heat pump: want }Q_H).$$
Because $Q_H-Q_C=W_{cycle}$, the two satisfy $\boxed{\gamma=\beta+1}$, so $\gamma\ge1$
always. (Alternative heat-only forms: $\beta=Q_C/(Q_H-Q_C)$ (2.46),
$\gamma=Q_H/(Q_H-Q_C)$ (2.48).)

## 4. The Carnot ceilings (what bounds §2,§3)
The second law (`3.3`) caps all of the above. For *reversible* cycles between two
reservoirs, $(Q_C/Q_H)_{rev}=T_C/T_H$ (Eq. 5.7), and substituting into the definitions
gives the **best any cycle can do** [M §5.9, p.265–267]:
$$\eta_{max}=1-\frac{T_C}{T_H}\ (5.9),\quad
\beta_{max}=\frac{T_C}{T_H-T_C}\ (5.10),\quad
\gamma_{max}=\frac{T_H}{T_H-T_C}\ (5.11),$$
with $\gamma_{max}=\beta_{max}+1$. **`T` in K or °R only.** A real $\eta,\beta,\gamma$
*equal* the ceiling only if reversible; exceeding it is **impossible**.
*Check:* between 2000 K and 400 K, $\eta_{max}=1-400/2000=0.80$, so a claimed 85% is
impossible while 60% is merely irreversible (Ex 5.1). A freezer at 268 K in 295 K air has
$\beta_{max}=268/27=9.9$ (Ex 5.2); a house at 530 °R from 492 °R air has
$\gamma_{max}=530/38=13.95$ (Ex 5.3).

## 5. Isentropic (device) efficiencies
A single adiabatic device is rated not against Carnot but against its own
**reversible-adiabatic (isentropic)** ideal at the *same inlet state and same exit
pressure*; that ideal exit is state "2s" with $s_{2s}=s_1$ (Topic 6) [M §6.12, p.332].

- **Turbine** (work *out*, so actual $\le$ ideal):
  $\eta_t=\dfrac{h_1-h_2}{h_1-h_{2s}}$ (6.46), typically 0.7–0.9 [M §6.12.1, p.333].
- **Nozzle** (kinetic energy *out*): $\eta_n=\dfrac{V_2^2/2}{(V_2^2/2)_s}$ (6.47), often
  $\ge0.95$; the exit KE follows from $V_2^2/2=(h_1-h_2)+V_1^2/2$ [M §6.12.2, p.335].
- **Compressor / pump** (work *in*, so actual $\ge$ ideal — the ratio inverts):
  $\eta_c=\dfrac{h_{2s}-h_1}{h_2-h_1}$ (6.48), typically 0.75–0.85 [M §6.12.3, p.338].

*Check:* a steam turbine with $\eta_t=0.75$, $h_1=3105.6$, $h_{2s}=2743.0$ kJ/kg delivers
$w=0.75(3105.6-2743.0)=271.95$ kJ/kg (Ex 6.11); an R-22 compressor with
$h_1=249.75$, $h_2=294.17$, $h_{2s}=285.58$ has $\eta_c=35.83/44.42=0.81$ (Ex 6.14).

## Bridge
These ratios *rate* the cycles of Topic 9 (Otto, Diesel, Brayton, Rankine) and the devices
of Topic 8 (turbines, compressors, pumps, heat pumps). The gap between a real efficiency
and its Carnot/isentropic ceiling is exactly the work *lost* to irreversibility — the
exergy story (`4.3`), with $E_d=T_0\sigma$.
