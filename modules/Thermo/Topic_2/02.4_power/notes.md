# 2.4 — Power (notes)

Modules `2.1`–`2.3` evaluated work as an *amount* — a quantity of energy that
crossed a boundary during a process. Almost every engineering question is
instead asked about a *rate*: not "how much work did the turbine do" but "what
is its output". This module is that change of variable, and it is what makes the
steady-state control-volume analyses of `6.4` and Topic 8 possible.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18).

## 1. Why work needs a rate at all: the inexact differential

Just before defining power, M settles a notational point that explains the whole
shape of the subject [M §2.2.1, p.46]. For a property such as volume,
$$\int_{V_1}^{V_2} dV = V_2-V_1,$$
and the integral can be evaluated knowing only the end states — the differential
is **exact**. For work it cannot:
$$\int_1^2 \delta W = W \quad(\text{not } W_2-W_1),$$
because there is no function $W$ of the state to difference. The differential is
**inexact**, and that is why it is written $\delta W$ rather than $dW$. "$W_2$"
is meaningless; a system does not *contain* work.

The consequence for this module: $\dot W$ is not the derivative of any stored
quantity. It is a *flux* — energy crossing a boundary per unit time — and it can
be non-zero indefinitely without anything running out, which is precisely what a
machine at steady state does.

## 2. Power from a moving force

When a work interaction involves a macroscopically observable force, the rate of
energy transfer is the force times the velocity of its point of application
[M Eq. 2.13, §2.2.2, p.46]:
$$\boxed{\;\dot W=\mathbf F\cdot\mathbf V\;}$$
— `power_force_velocity`. It is the differential statement of $\delta W=F\,ds$
divided by $dt$, with $V=ds/dt$. The dot product matters: a force perpendicular
to the motion transmits no power, which is why a satellite in a circular orbit
neither gains nor loses energy from gravity.

Integrating recovers the amount [M Eq. 2.14, p.46]:
$$W=\int_{t_1}^{t_2}\dot W\,dt=\int_{t_1}^{t_2}\mathbf F\cdot\mathbf V\,dt .$$
At **constant** power this collapses to $W=\dot W\,\Delta t$
(`energy_from_power`) and its inverse $\dot W=W/\Delta t$ (`power_from_work`),
which is an *average* power whenever the rate is not actually constant.

The sign convention is inherited unchanged: $\dot W>0$ means power **out of**
the system.

## 3. The rotating shaft, where the radius cancels

A shaft transmitting torque $\tau$ at radius $R$ exerts a tangential force
$F_t=\tau/R$ at its surface, and that surface moves at $V=R\omega$. Feeding both
into Eq. 2.13 [M Eq. 2.20, §2.2.6, p.53]:
$$\dot W=F_tV=\Bigl(\frac{\tau}{R}\Bigr)\bigl(R\omega\bigr)=\boxed{\;\tau\omega\;}$$
— `shaft_power`. **The radius cancels**, which is the entire reason a gearbox
works: torque and speed may be traded against each other at will, and only their
product — the power — is conserved by an ideal transmission.

$\omega$ must be in **radians** per unit time, because $V=R\omega$ presumes it;
`rpm_to_rad_s` applies $\omega=2\pi\,\mathrm{rpm}/60$, a factor of 0.1047.
Feeding rpm straight into $\tau\omega$ is the commonest error here, and it
overstates the power by the reciprocal, $60/2\pi\approx9.55$.

A shaft at $\tau=9.7\ \mathrm{N\,m}$ and 1000 rpm delivers
$\dot W=9.7\times104.72=1016$ W.

## 4. The electrical case, and its sign

For a system with current $i$ crossing its boundary at electrical potential
$\varepsilon$, the power is [M Eq. 2.21, §2.2.6, p.53]
$$\dot W=-\varepsilon i .$$
The minus sign is not decoration. With the current drawn *in* the direction
shown by M's electrolytic cell, energy flows **into** the system, and the
work-out-positive convention then requires $\dot W<0$. `electric_power` returns
the **magnitude** $\varepsilon i$; its docstring records that the signed
contribution to the energy balance is $-\varepsilon i$, and the caller applies
the sign. That split is deliberate — magnitudes are what nameplates quote, signs
are what balances need.

## 5. Units

Power is energy per time, so in SI it is J/s, named the **watt**; kW is the
working unit for thermal systems [M §2.2.2, p.46]. M also uses ft·lbf/s, Btu/h
and horsepower. Two conversions worth having: $1\ \mathrm{hp}=745.7$ W and
$1\ \mathrm{kW}=3412\ \mathrm{Btu/h}$.

Because power is a rate, a bare figure says nothing about energy delivered until
it is multiplied by a duration:

| source | $\dot W$ | over 60 s |
|---|---|---|
| shaft, 18 N·m at 100 rad/s | 1.8 kW | 108 kJ |
| resistor, 120 V at 10 A | 1.2 kW | 72 kJ |
| shaft, 9.7 N·m at 1000 rpm | 1.016 kW | 61 kJ |

## 6. Where the module's numbers come from

`test_power.py` pins: $\dot W=\tau\omega$ with the rpm conversion; the
`rpm_to_rad_s` factor itself; $\dot W=\mathbf F\cdot\mathbf V$; the electrical
magnitude; and the round trip
`power_from_work(energy_from_power(P, t), t) == P`, which asserts that the two
helpers are genuine inverses rather than two spellings of a multiplication.

The gearbox of M's Example 2.4 and the motor of Example 2.6 [both in
`Topic_1/1.EP`] are the worked applications: each is a steady-state device where
the electrical power in and the shaft power out differ by exactly the heat
transfer rate, which is `3.2`'s rate-form first law with the terms named.

## Where this goes

- `2.1` — the work modes whose rates these are.
- `3.2` — the rate form of the energy balance, $dE/dt=\dot Q-\dot W$.
- `6.4` — steady state, where $dE/dt=0$ and the balance becomes an algebraic
  relation between $\dot W$, $\dot Q$ and $\dot m\,\Delta h$.
- `7.1` — efficiency, which is a ratio of two powers.
- `8.1` — compressor shaft power, the same $\tau\omega$ read as a duty.
