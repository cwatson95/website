# 11.EP — Topic 11 Example Problems (Moran Ch.12, psychrometrics)

Four Moran 8e Chapter-12 worked **Examples** reproduced from their *given* data with the
Topic-11 moist-air relations and verified in `code/examples.py` (`test_examples.py`, 21
checks). Each regenerates the book's published answer. Citations in `refs.md`.

| Moran Ex. | concept (module) | given → find | function |
|-----------|------------------|--------------|----------|
| **12.7** Cooling moist air at constant pressure | $\omega$, dew point, condensate (`11.1`) | 1 lb at $70\,^\circ$F, $14.7\;\text{lbf/in.}^2$, $\phi=70\%$ → $40\,^\circ$F | `ex_12_7` |
| **12.8** Cooling moist air at constant volume | dew point, onset $T'$, condensate (`11.1`) | $35\,\text{m}^3$ rigid, $1.5$ bar, $120\,^\circ$C, $\phi=10\%$ → $22\,^\circ$C | `ex_12_8` |
| **12.11** Assessing dehumidifier performance | $\dot m_a$, condensate, tons (`11.1`,`11.2`) | $30\,^\circ$C, $50\%$, $280\,\text{m}^3$/min; sat. exit $10\,^\circ$C, $1.013$ bar | `ex_12_11` |
| **12.12** Steam-spray humidifier | $\omega_2$, $T_2$ (chart) (`11.2`) | $22\,^\circ$C, $T_{wb}=9\,^\circ$C, $\dot m_a=90$ kg/min; sat. vapor $110\,^\circ$C @ 52 kg/h | `ex_12_12` |

### Book answers (all reproduced)
| Ex. | published results |
|-----|-------------------|
| **12.7** | $p_{v1}=0.2542\;\text{lbf/in.}^2$, $\omega_1=0.011$, dew point $=60\,^\circ$F, $\omega_2=0.0052$, $m_a=0.9891$, $m_{v1}=0.0109$, condensate $m_w=0.0058$ lb |
| **12.8** | $p_{v1}=0.1985$ bar, dew point $=60\,^\circ$C, $v_{v1}=9.145\;\text{m}^3$/kg, $m_{v1}=3.827$ kg, onset $T'=56\,^\circ$C, $x_2=0.178$, $m_{v2}=0.681$, condensate $m_{w2}=3.146$ kg, $m_a=40.389$ kg |
| **12.11** | $\dot m_a=319.35$ kg/min, $\omega_1=0.0133$, $\omega_2=0.0076$, $\dot m_w/\dot m_a=0.0057$, $\dot Q_{cv}\approx-11{,}084$ kJ/min $\Rightarrow$ 52.5 tons |
| **12.12** | $\omega_1=0.002$ (chart), $\omega_2=0.0116$, $(h_a+\omega h_g)_1=27.2$, $(\omega_2-\omega_1)h_{g3}=25.8$, $(h_a+\omega h_g)_2=53$ kJ/kg(a), $T_2=23.5\,^\circ$C |

**Key lessons.** *12.7 vs 12.8* — cooling at **constant pressure** condenses at the dew
point ($60\,^\circ$F / $60\,^\circ$C), but at **constant volume** condensation begins
*lower* (here $56\,^\circ$C) because $p_v$ falls as $T$ drops along the rigid-vessel
process. *12.11* — a dehumidifier cools below the dew point so $\omega$ drops
($0.0133\!\to\!0.0076$); the refrigeration load converts via $1\,\text{ton}=211$ kJ/min.
*12.12* — steam injection raises both $\omega$ and $T$; the exit state is fixed on the
chart by $\omega_2$ and the mixture enthalpy $(h_a+\omega h_g)_2=53$ kJ/kg(a).

> **Stepwise-rounding note.** Saturation pressures, $h_f$, $h_g$ are the values Moran
> reads from Tables A-2 / A-2E (and $h_a$ from A-22), so the published answers reproduce
> to book significant figures. $\omega_1=0.002$ in Ex. 12.12 is the chart read at the
> $(22\,^\circ$C, $T_{wb}=9\,^\circ$C) point, as the book uses.

## Run
```bash
cd code
python3 examples.py          # all four examples vs the book answers
python3 test_examples.py     # -> "All 21 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
