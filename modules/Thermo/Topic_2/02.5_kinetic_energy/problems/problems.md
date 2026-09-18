# 2.5 — Problems

Check with `code/kinetic_energy.py`. Citations in `../refs.md`.

### P1.  Deceleration  *(Moran 8e §2.1.1, Eq. 2.5, p.41; cf. HW 2.6)*
A 1000 kg object slows from 100 m/s to 20 m/s. Find `ΔKE`.
*Answer:* `ΔKE = ½(1000)(20²−100²) = −4.8×10⁶ J = −4800 kJ`.
*Check:* `delta_KE(1000,100,20)` = −4.8e6.

### P2.  Work–energy theorem  *(Moran 8e §2.1.1, p.41)*
What speed does a 2 kg body reach from rest after 100 J of net work?
*Answer:* `½mV² = W ⇒ V = √(2W/m) = √100 = 10 m/s`.
*Check:* `speed_after_work(2,0,100)` = 10; `work_from_KE(2,0,10)` = 100.
