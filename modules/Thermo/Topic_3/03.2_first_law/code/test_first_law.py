"""test_first_law.py — checks for Module 3.2.  Run: python3 test_first_law.py"""
import math
from first_law import (delta_E, closed_system_dU, heat_transfer, work_transfer,
                       rate_energy_balance, cycle_net_work, power_cycle_work,
                       first_law_holds)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# closed-system balance
chk("delta_E", delta_E(100.0, 30.0), 70.0)
chk("Ex2.2 Q", heat_transfer(dU=-22.0, W=17.6), -4.4)            # Moran Ex 2.2 -> -4.4 kJ
chk("Ex2.2 dU", closed_system_dU(Q=-4.4, W=17.6), -22.0)         # invert the same example
chk("Ex2.2 W", work_transfer(dU=-22.0, Q=-4.4), 17.6)
chk("balance w/ KE,PE dU", closed_system_dU(Q=10.0, W=2.0, dKE=1.0, dPE=0.5), 6.5)
chk("balance w/ KE,PE Q", heat_transfer(dU=6.5, W=2.0, dKE=1.0, dPE=0.5), 10.0)
# rate form / steady state
chk("rate dE/dt", rate_energy_balance(-1.2, -1.2), 0.0)          # Ex 2.4 steady state
chk("rate dE/dt 2", rate_energy_balance(5.0, 2.0), 3.0)
# cycle
chk("cycle Wnet=Qnet", cycle_net_work(400.0), 400.0)
chk("power cycle W", power_cycle_work(1000.0, 600.0), 400.0)
# predicate
assert first_law_holds(100.0, 30.0, 70.0) is True;  _n += 1
assert first_law_holds(100.0, 30.0, 71.0) is False; _n += 1

# ---- Moran Example 2.2 (p.64): gas cooled in a piston-cylinder ----
# boundary work is Example 2.1(a)'s +17.6 kJ; internal energy falls 22 kJ
chk("Ex 2.2 heat transfer", heat_transfer(-22.0, 17.6), -4.4)
assert heat_transfer(-22.0, 17.6) < 0;  _n += 1          # heat OUT of the system
chk("Ex 2.2 closes", delta_E(-4.4, 17.6), -22.0)
assert first_law_holds(-4.4, 17.6, -22.0);  _n += 1

# the same dU can be reached by many (Q, W) splits -- only the difference is fixed
for _Q, _W in ((-22.0, 0.0), (-4.4, 17.6), (10.0, 32.0), (-50.0, -28.0)):
    chk("dU is path-independent (Q=%g, W=%g)" % (_Q, _W), delta_E(_Q, _W), -22.0)

# a cycle stores nothing, so net work IS net heat
chk("cycle: W = Q", cycle_net_work(600.0), 600.0)
chk("power cycle difference", power_cycle_work(1000.0, 400.0), 600.0)
chk("power cycle agrees with cycle_net_work",
    power_cycle_work(1000.0, 400.0), cycle_net_work(1000.0 - 400.0))
# the first law alone does NOT forbid Q_out = 0 (that takes the second law, 3.3)
chk("first law permits eta = 1", power_cycle_work(1000.0, 0.0), 1000.0)

print(f"All {_n} tests passed.")
