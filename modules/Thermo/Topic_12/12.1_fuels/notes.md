# 12.1 — Fuels & Combustion of Reacting Mixtures (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Combustion and the air model
In **combustion** the combustible elements of a fuel (C, H, S) are rapidly oxidized,
releasing energy [M §13.1, p.806]. Combustion is **complete** when all C → CO₂, all
H → H₂O, all S → SO₂. Mass is conserved, so every chemical element must balance on
both sides — though the *number of moles* need not (e.g. `H₂ + ½O₂ → H₂O`).

For **combustion air** Moran uses a fixed model [M §13.1.2, p.807]: dry air is 21% O₂ /
79% N₂ on a molar basis, so each mole of O₂ is accompanied by `0.79/0.21 = 3.76` mol N₂,
i.e. **4.76 mol air per mol O₂**. N₂ is treated as **inert** (`M_air = 28.97`).

## 2. Theoretical air & balancing
The **theoretical (stoichiometric) amount of air** is the minimum that completely burns
the fuel, leaving *no* free O₂ in the products [M §13.1.2, p.808]. For `CₐHᵦ` (general
`CₐHᵦOᵧSₛ`) the theoretical O₂ per mole of fuel is
$$a_{O_2}=C+\tfrac{H}{4}+S-\tfrac{O}{2},\qquad \overline{AF}_{\text{theo}}=4.76\,a_{O_2}.$$
*Check (M Ex 13.1, octane):* `C₈H₁₈ + 12.5(O₂ + 3.76N₂) → 8CO₂ + 9H₂O + 47N₂`, so
`a_O₂ = 8 + 18/4 = 12.5` and `AF̄ = 12.5·4.76 = 59.5` (`code/fuels.py`).

## 3. Air–fuel ratio (Eq. 13.2)
The **air–fuel ratio** is air ÷ fuel, molar (`AF̄`) or mass (`AF`); convert with the
molecular weights [M Eq. 13.2, p.808]:
$$AF=\overline{AF}\,\frac{M_{air}}{M_{fuel}}.$$
*Check:* octane `AF = 59.5·(28.97/114.22) = 15.1` kg air/kg fuel. The reciprocal is the
**fuel–air ratio**.

Air is usually supplied **above or below** theoretical [M §13.1.2, p.808]:
**% theoretical air** `= AF/AF_theo` (150% theoretical = 50% **excess** air = the same
fuel burnt with 1.5× the air); 80% theoretical = 20% **deficiency**. The
**equivalence ratio** [M §13.1.2, p.809]
$$\phi=\frac{(F/A)_{\text{actual}}}{(F/A)_{\text{theo}}}=\frac{AF_{\text{theo}}}{AF_{\text{actual}}}$$
is `<1` **lean**, `>1` **rich**. For octane with 50% excess air, `φ = 59.5/89.25 = 0.67`.

## 4. Products & dew point (§13.1.3)
With complete combustion the only products are CO₂, H₂O, N₂ (and O₂ if excess air). A
measured **dry product analysis** (mole fractions of everything except water) plus a mass
balance fixes the reaction [M Ex 13.2, p.811]. Cooling the products at constant `p`, the
**dew point** is reached when water vapor begins to condense: `p_v = y_v p`, and the dew
point is `T_sat(p_v)` [M §13.1.3, p.812]. Below it, the vapor still present satisfies
`p_sat = (n/(n + n_dry))p`, so `n = p_sat·n_dry/(p - p_sat)`.

## 5. Enthalpy of formation & combustion (§13.2)
For reacting systems the enthalpy datum is the **standard reference state** `Tref =
298.15 K`, `pref = 1 atm`, with stable elements assigned `h = 0` [M §13.2.1, p.816]. The
**enthalpy of formation** `h°_f` is the energy to form a compound from its elements at
that state (Table A-25); e.g. `h°_f,CO₂ = −393,520 kJ/kmol` (exothermic ⇒ negative). At
any other state [M Eq. 13.9, p.817]
$$h(T,p)=h^{\circ}_f+\big[h(T)-h(T_{ref})\big]=h^{\circ}_f+\Delta h.$$
The **enthalpy of combustion** is the product–reactant enthalpy difference at fixed `T,p`
for complete combustion [M Eq. 13.18, p.825]:
$$h_{RP}=\sum_P n_e h_e-\sum_R n_i h_i.$$
The **heating value** is `|h_RP|`: **HHV** (liquid water in products) > **LHV** (vapor),
the gap being the latent heat of the product water [M §13.2.3, p.825].
*Check (M Ex 13.7, methane):* HHV `= −393,520 + 2(−285,830) − (−74,850) = −890,330
kJ/kmol = −55,507 kJ/kg`; LHV (vapor) `= −802,310 kJ/kmol = −50,019 kJ/kg` — both match
Table A-25.

## 6. Energy balance for steady combustion (§13.2.2)
For a steady reactor, mass + energy balances give, per mole of fuel [M Eqs. 13.12b/13.15b,
p.818–819],
$$\frac{\dot Q_{cv}}{\dot n_F}-\frac{\dot W_{cv}}{\dot n_F}
=\overline h_P-\overline h_R=\sum_P n_e(h^{\circ}_f+\Delta h)_e-\sum_R n_i(h^{\circ}_f+\Delta h)_i.$$
Reactant `Δh = 0` when fuel and air enter at `Tref`. For a **closed** rigid system use
`u = h − R̄T`: `Q − W = ΣP n(h°_f+Δh−R̄T_P) − ΣR n(h°_f+Δh−R̄T_R)` [M Eq. 13.17b, p.823].

## Bridge
Push the reactor toward **adiabatic** (`Q_cv → 0`) and `h_P = h_R` fixes the **adiabatic
flame temperature** (module `12.EP`, Ex 13.8). Raise `T` further and products begin to
**dissociate** — an equilibrium-constant problem (module `12.2`), whose plasma limit is
thermal **ionization** (the Saha equation).
