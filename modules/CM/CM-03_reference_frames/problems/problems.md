# CM-03 — Problems

Work by hand, then check with `code/reference_frames.py`. Citations in `../refs.md`.

### P1.  Galilean velocity addition  *(Fowles 7e §5.1, p.184)*
A boat moves at **u** in the water; the water moves at **V** relative to the bank.
Find the boat's velocity relative to the bank and relative to the water.
*Check:* `galilean_velocity`.

**Solution.** Velocities add under a Galilean boost. The water moves at $\mathbf V$ relative to the bank and the boat moves at $\mathbf u$ relative to the water, so the boat's velocity in the bank frame is the sum
$$\mathbf v_\text{boat/bank}=\mathbf u+\mathbf V.$$
To get the boat's velocity relative to the water, boost into the water frame (which moves at $\mathbf V$): $\mathbf v'=\mathbf v_\text{boat/bank}-\mathbf V=\mathbf u$, recovering the original $\mathbf u$. This is exactly `galilean_velocity(v, V) = v − V`; e.g. `galilean_velocity(u+V, V)` returns $\mathbf u$.

### P2.  Relative velocity is frame-independent  *(Fowles 7e §2.1, p.54)*
Show **v**ₐ − **v**_b is unchanged by a Galilean boost (both velocities shift by
the same **V**). *Check:* compare `relative_velocity(va, vb)` before and after
`galilean_velocity(·, V)`.

**Solution.** Under a Galilean boost by $\mathbf V$, every velocity shifts the same way: $\mathbf v_a'=\mathbf v_a-\mathbf V$ and $\mathbf v_b'=\mathbf v_b-\mathbf V$. Their difference is therefore
$$\mathbf v_a'-\mathbf v_b'=(\mathbf v_a-\mathbf V)-(\mathbf v_b-\mathbf V)=\mathbf v_a-\mathbf v_b,$$
so the relative velocity is independent of the (inertial) frame — the common boost $\mathbf V$ cancels. Numerically, `relative_velocity(va, vb)` returns $(2,0,0)$ both before and after boosting each velocity by `galilean_velocity(·, V)`.

### P3.  Velocity of the centre of mass  *(Fowles 7e §7.1, p.275)*
For two bodies m=[2,1] with v=[(1,0,0),(−2,0,0)], find **V**_cm. *Check:*
`cm_velocity([2,1], [[1,0,0],[-2,0,0]])` → (0,0,0): the CM is at rest here.

**Solution.** The centre-of-mass velocity is the momentum-weighted average $\mathbf V_\text{cm}=\frac{\sum_i m_i\mathbf v_i}{\sum_i m_i}$. With $m=[2,1]$ and $\mathbf v=[(1,0,0),(-2,0,0)]$ the total momentum is
$$\sum_i m_i\mathbf v_i=2(1,0,0)+1(-2,0,0)=(0,0,0),$$
and $\sum_i m_i=3$, so $\mathbf V_\text{cm}=(0,0,0)/3=(0,0,0)$ — the heavier body's rightward momentum exactly cancels the lighter body's leftward momentum, leaving the CM at rest. `cm_velocity([2,1], [[1,0,0],[-2,0,0]])` returns $(0,0,0)$.

### P4.  Zero momentum in the C-frame  *(Fowles 7e §7.6, p.306)*
Show that subtracting **V**_cm from every velocity makes the total momentum zero.
*Check:* `total_momentum(masses, to_cm_frame(masses, vels))` ≈ 0 for random systems.

**Solution.** Boosting into the C-frame subtracts $\mathbf V_\text{cm}$ from every velocity: $\mathbf v_i'=\mathbf v_i-\mathbf V_\text{cm}$. The total momentum measured there is
$$\mathbf P'=\sum_i m_i\mathbf v_i'=\sum_i m_i\mathbf v_i-\Big(\sum_i m_i\Big)\mathbf V_\text{cm}=\mathbf P-M\cdot\frac{\mathbf P}{M}=\mathbf 0,$$
using $\mathbf V_\text{cm}=\mathbf P/M$. So the centre-of-mass frame is precisely the zero-momentum frame, which is why collisions are simplest there (`~CM-08`). Hence `total_momentum(masses, to_cm_frame(masses, vels))` returns $\approx\mathbf 0$ for any system.

### P5.  Where Galilean fails  *(→ `~RE-01`)*
Galilean addition gives u + V with no upper bound. State qualitatively why this
cannot hold for light and what replaces it (the Lorentz transformation, `~RE-03`).

**Solution.** Galilean addition $\mathbf u+\mathbf V$ has no ceiling, so it predicts that a light pulse measured at speed $c$ in one frame would travel at $c-V$ in a frame moving alongside it. Experiment (Michelson–Morley) instead finds the speed of light $c$ to be identical in every inertial frame, contradicting the unbounded rule. The fix is to replace the Galilean boost with the **Lorentz transformation** (`~RE-03`), whose velocity-addition law
$$u\oplus V=\frac{u+V}{1+uV/c^2}$$
never exceeds $c$ yet reduces to $u+V$ when $u,V\ll c$ — recovering Galilean relativity as the low-speed limit.
