# 3.3 — Second Law (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Why a second law
The first law (`3.2`) is satisfied by many processes that never happen — a cup of
coffee spontaneously reheating, a weight rising as a gas cools. Energy balance
alone does not forbid them; the **second law** supplies the missing *direction*
and the limit on heat→work conversion [M §5.1, p.240].

## 2. Clausius statement
> It is impossible for any system to operate in such a way that the **sole result**
> would be an energy transfer by heat from a cooler to a hotter body. [M §5.2.1, p.245]

(Refrigerators *do* move heat "uphill" — but not as the *sole* result; they require
a work input. That is exactly the COP story, §7.)

## 3. Kelvin–Planck statement
> It is impossible for any system to operate in a thermodynamic cycle and deliver a
> net amount of energy by work to its surroundings while receiving energy by heat
> transfer from a **single thermal reservoir**. [M §5.2.2, p.246]

Analytically, for a cycle communicating with a single reservoir,
$$W_{cycle}\le 0 \quad(5.1),\qquad W_{cycle}\begin{cases}=0 & \text{no internal irreversibilities}\\ <0 & \text{irreversibilities present}\end{cases}\ \text{(single reservoir)}\quad(5.3).$$
The two statements are **equivalent**: violating one violates the other [M §5.2.3, p.247].

## 4. Reversible vs irreversible; the Carnot corollaries
A process is **reversible** if both system and surroundings can be returned to
their initial states; real processes (friction, finite-ΔT heat transfer, mixing,
unrestrained expansion) are **irreversible** [M §5.3, p.248]. From Kelvin–Planck:

1. *No* power cycle between two reservoirs is more efficient than a **reversible**
   one between the same reservoirs.
2. *All* reversible power cycles between the same two reservoirs have the **same**
   efficiency. [M §5.5, p.257]

## 5. The Kelvin temperature scale
For a reversible cycle between reservoirs at $T_H,T_C$,
$$\left(\frac{Q_C}{Q_H}\right)_{rev}=\frac{T_C}{T_H}\quad(5.7),$$
which (with the triple point fixed at 273.16 K, `3.1`) *defines* the Kelvin scale
independent of any thermometric substance [M §5.7, p.262].

## 6. Carnot efficiency and the best COPs
Combining Eqs. 5.4 and 5.7 gives the ceilings for two-reservoir cycles:
$$\eta_{max}=1-\frac{T_C}{T_H}\ (5.9),\quad
\beta_{max}=\frac{T_C}{T_H-T_C}\ (5.10),\quad
\gamma_{max}=\frac{T_H}{T_H-T_C}\ (5.11),$$
with $\gamma_{max}=\beta_{max}+1$. **`T` in K or °R only** [M §5.9, p.265–267].

*Check:* between $T_H=745$ K and $T_C=298$ K, $\eta_{max}=1-298/745=0.60$ (book's
60%); between 2000 K and 400 K, $\eta_{max}=0.80$. A claimed power-cycle efficiency
of 0.65 between 745/298 K is **impossible** (exceeds 0.60).

## Bridge
The inequality in Eq. 5.3 becomes the **entropy production** $\sigma\ge0$ (module
`4.2`); the Carnot ceilings cap every cycle in Topic 9 and rate the devices in
Topic 8. Exergy (`4.3`) measures the work *lost* to irreversibility.
