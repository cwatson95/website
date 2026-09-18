# 2.5 — Kinetic Energy (notes)

Kinetic energy is the first of the three terms that make up the total energy
$E=U+\mathrm{KE}+\mathrm{PE}$ [M Eq. 2.27, §2.3, p.55]. It is also the term
whose derivation is pure mechanics: nothing thermodynamic enters, which is
exactly why M reviews it before the first law. `2.6` does the same for potential
energy; `1.2` and `1.1` then carry both into the energy balances.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18). This module works in **joules**
($m$ in kg, $V$ in m/s); the balances in `1.1`/`1.2` want kJ, hence their
factor of $10^{3}$.

## 1. It falls out of Newton's second law

Take a body of mass $m$ under a resultant force $F_s$ along its path $s$.
Newton's second law says $F_s = m\,dV/dt$. Multiply both sides by $ds$ and use
$ds = V\,dt$ to change the variable of integration from time to velocity:
$$F_s\,ds = m\frac{dV}{dt}\,ds = m\frac{dV}{dt}V\,dt = mV\,dV .$$
Integrating from state 1 to state 2, the left side is the work of the resultant
force and the right side evaluates in closed form [M Eq. 2.4, p.41]:
$$\int_{V_1}^{V_2} mV\,dV = \tfrac12 m\bigl(V_2^{2}-V_1^{2}\bigr).$$
The quantity $\tfrac12mV^{2}$ is named the **kinetic energy**, and its change is
[M Eq. 2.5, §2.1.1, p.41]
$$\boxed{\;\Delta \mathrm{KE}=\mathrm{KE}_2-\mathrm{KE}_1=\tfrac12 m\bigl(V_2^{2}-V_1^{2}\bigr)\;}$$
so the two sides together give the **work–energy theorem** [M Eq. 2.6, p.41]:
$$\tfrac12 m\bigl(V_2^{2}-V_1^{2}\bigr)=\int_{s_1}^{s_2}\mathbf{F}\cdot d\mathbf{s}
\qquad\Longleftrightarrow\qquad \Delta\mathrm{KE}=W_{\text{net}} .$$
`kinetic_energy`, `delta_KE`, and `work_from_KE` — the last is literally
`delta_KE` under the name the theorem gives it, which is the point: *net work on
a body and its change in kinetic energy are the same number*.

M's phrasing is worth keeping: when a body is accelerated by the resultant
force, the work done on it "can be considered a transfer of energy to the body,
where it is stored as kinetic energy". Work is the transfer; kinetic energy is
the store.

## 2. Why it is a property, and an extensive one

Kinetic energy can be assigned a value "knowing only the mass of the body and
the magnitude of its instantaneous velocity … without regard for how this
velocity was attained" [M p.41]. That is precisely the test for a **property**:
it depends on the state, not on the path taken to reach it. Contrast the $W$ of
module `2.2`, which is not a property and for which $\int_1^2\delta W$ genuinely
depends on the route.

Because KE is attached to the body as a whole and scales with its mass, it is an
**extensive** property (module `1.3`), and it is a **scalar** — velocity's
direction has been squared away.

One consequence that trips people: KE is frame-dependent, since $V$ is measured
"relative to a specified coordinate frame". A cup of coffee on an aircraft tray
has enormous kinetic energy in the ground frame and none in the cabin frame.
Only *changes*, evaluated consistently in one frame, enter the energy balance.

## 3. The quadratic, and what it costs

$\mathrm{KE}\propto V^{2}$ is the whole practical content of the module.
Doubling a speed quadruples the energy that must be supplied to reach it, and
quadruples the energy the brakes must dissipate to remove it:

| 1500 kg vehicle | $\mathrm{KE}$ |
|---|---|
| 10 m/s | 75 kJ |
| 20 m/s | 300 kJ |
| 40 m/s | 1200 kJ |

Braking from 40 to 20 m/s therefore sheds 900 kJ — three times what braking
from 20 m/s to rest sheds — which is why stopping distances grow faster than
speed and why regenerative braking is worth engineering [M's *Energy &
Environment* box, p.41, makes exactly this argument for hybrids].

Run the theorem backwards and the same quadratic becomes a square root:
$$\tfrac12mV_2^{2}=\tfrac12mV_1^{2}+W_{\text{net}}
\quad\Longrightarrow\quad
V_2=\sqrt{V_1^{2}+\frac{2W_{\text{net}}}{m}}$$
— `speed_after_work`. The returns diminish sharply: on a 1500 kg body the first
300 kJ buys 20.0 m/s from rest, the second 300 kJ adds only 8.3 m/s more.

## 4. Units, and the book's own worked check

Energy units are force times distance: the newton-metre, called the **joule**
[M §2.1.3, p.43]. Kinetic and potential energy share them with work, which is
the arithmetic statement that the three can be added at all.

M works a units example on p.43 that this module reproduces exactly. A 1 kg
system speeds up from 15 to 30 m/s:
$$\Delta\mathrm{KE}=\tfrac12(1)\bigl(30^{2}-15^{2}\bigr)=337.5\ \mathrm{J}=0.3375\ \mathrm{kJ},$$
which the book quotes as 0.34 kJ. `delta_KE(1.0, 15.0, 30.0)` returns 337.5 J;
`test_kinetic_energy.py` pins it against the book's rounded value.

The unit trap the example exists to teach: $\mathrm{kg\,m^{2}/s^{2}}$ is a
joule, so an answer in $\mathrm{m^{2}/s^{2}}$ has lost its mass, and one in J
must be divided by $10^{3}$ before it can be added to an enthalpy in kJ/kg. The
open-system module `1.1` does that division explicitly inside `flow_energy`, and
its `fig1` shows how small the term usually is — velocity must exceed about
250 m/s before $V^{2}/2$ reaches 1% of a typical steam enthalpy.

## 5. Consistency checks in the code

`test_kinetic_energy.py` pins: $\mathrm{KE}=\tfrac12mV^{2}$; $\Delta\mathrm{KE}$
for a deceleration (negative); the work–energy theorem; the `speed_after_work`
inverse; the identity $\mathrm{KE}_2-\mathrm{KE}_1=\Delta\mathrm{KE}$ evaluated
two ways; M's 0.34 kJ units example; and the round trip
`speed_after_work(m, V1, delta_KE(m, V1, V2)) == V2`, which is the theorem
asserted as an invertible pair rather than as two separate formulas.

## Where this goes

- `2.6` — potential energy, derived from the same Eq. 2.6 starting point.
- `1.2` — $\Delta\mathrm{KE}$ as a term in the closed-system energy balance
  $Q-W=\Delta U+\Delta\mathrm{KE}+\Delta\mathrm{PE}$.
- `1.1` / `6.4` — the flow-energy term $V^{2}/2$ in $\psi=h+V^{2}/2+gz$, and the
  criterion for when it may be dropped.
- `13.1`–`13.3` — compressible flow, where $V^{2}/2$ stops being a correction
  and becomes the dominant term: stagnation enthalpy is $h_o=h+V^{2}/2$.
