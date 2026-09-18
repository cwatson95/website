"""test_ts_diagram.py — checks for Module 5.5.  Run: python3 test_ts_diagram.py"""
import math
from ts_diagram import (heat_TdS, heat_isothermal, heat_linear_TS,
                        carnot_net_work, carnot_efficiency)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# trapezoid: rectangle area = T*(S2-S1)
chk("trapezoid rectangle", heat_TdS([400.0, 400.0], [1.0, 2.0]), 400.0)
# trapezoid: linear T in S = average T times dS
chk("trapezoid linear", heat_TdS([300.0, 500.0], [0.0, 2.0]), 800.0)   # 1/2(300+500)(2)
# sign: dS<0 (heat rejected) gives negative area
chk("trapezoid reject sign", heat_TdS([400.0, 400.0], [2.0, 1.0]), -400.0)

# isothermal closed form matches trapezoid
chk("isothermal == trapezoid", heat_isothermal(423.15, 1.8418, 6.8379),
    heat_TdS([423.15, 423.15], [1.8418, 6.8379]), 1e-9)
# linear-in-S closed form matches trapezoid
chk("linear closed form", heat_linear_TS(300.0, 500.0, 0.0, 2.0),
    heat_TdS([300.0, 500.0], [0.0, 2.0]))

# Moran Example 6.1 -- water vaporized at 150 C (423.15 K), reversible isothermal
# Q/m = T(s2-s1) = 423.15*(6.8379-1.8418) = 2114.1 kJ/kg
chk("Ex6.1 Q/m", heat_isothermal(423.15, 1.8418, 6.8379), 2114.1, 0.1)

# Carnot cycle: T_H=600 K, T_C=300 K, dS=1 kJ/K
TH, TC, dS = 600.0, 300.0, 1.0
chk("Carnot Q_in", heat_isothermal(TH, 0.0, dS), 600.0)
chk("Carnot Q_out", heat_isothermal(TC, dS, 0.0), -300.0)
chk("Carnot W_net", carnot_net_work(TH, TC, dS), 300.0)
chk("Carnot eta", carnot_efficiency(TH, TC), 0.5)
# enclosed rectangle (closed loop) area = net work
loop = heat_TdS([TH, TH, TC, TC, TH], [0.0, dS, dS, 0.0, 0.0])
chk("Carnot closed-loop area = W_net", loop, carnot_net_work(TH, TC, dS), 1e-9)
# eta from areas equals Wnet/Qin
chk("eta = Wnet/Qin", carnot_efficiency(TH, TC),
    carnot_net_work(TH, TC, dS) / heat_isothermal(TH, 0.0, dS), 1e-12)

# isentropic leg (S const) carries no heat
chk("isentropic Q=0", heat_TdS([600.0, 300.0], [2.0, 2.0]), 0.0)
# heat to a system raises entropy (dS>0 <=> Q>0 at fixed T)
assert heat_isothermal(400.0, 1.0, 2.0) > 0; _n += 1
# Carnot efficiency rises with T_H at fixed T_C
assert carnot_efficiency(800.0, 300.0) > carnot_efficiency(600.0, 300.0); _n += 1

print(f"All {_n} tests passed.")
