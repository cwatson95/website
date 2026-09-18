# 3.2 — First Law / Energy Balance (notes)

`2.1`–`2.7` built the pieces: work, its modes, and the two mechanical energy
stores. This module assembles them into the accounting identity that the rest of
the subject is written in. It says nothing about *direction* — that is `3.3`'s
job — and everything about *quantity*.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18).

## 1. The statement

Energy is conserved: it is neither created nor destroyed, only **transferred**
across a boundary (as heat or work) or **stored** inside one (as internal,
kinetic or potential energy). In words, the change in the energy contained
within a system equals the net energy transferred in. In symbols, for a closed
system over a process 1→2 [M Eq. 2.35a, §2.5, p.61]:
$$\boxed{\;E_2-E_1=Q-W\;}$$
Resolving $E$ into its parts with Eq. 2.27 gives the working form
[M Eq. 2.35b, p.61]:
$$\Delta\mathrm{KE}+\Delta\mathrm{PE}+\Delta U=Q-W .$$
`delta_E` evaluates the first; `closed_system_dU`, `heat_transfer` and
`work_transfer` solve the second for whichever term is unknown.

M's own gloss is worth keeping: the equation "shows that an energy transfer
across the system boundary results in a change in one or more of the macroscopic
energy forms" [p.61]. Energy that crosses does not vanish into the system — it
lands in an identifiable store.

The word **net** is load-bearing. There may be heat and work transfers at many
places on the boundary, some in and some out; $Q$ and $W$ are the algebraic sums
over all of them [M p.61].

## 2. Why the signs differ, and the one error everyone makes

The minus before $W$ and the plus before $Q$ are not arbitrary. They follow from
the two conventions adopted separately [M p.61]:

| | positive when | set in |
|---|---|---|
| $Q$ | heat flows **into** the system | M §2.4.1, p.56 |
| $W$ | work is done **by** the system | M §2.2.1, p.45 (module `2.1`) |

Both are "energy the engineer cares about is positive" — fuel in, work out —
inherited from engine practice. Carry it as **"Q in +, W out +"**. Mixing the two
flips a sign in the middle of a problem and is the classic first-law error; it
typically shows up as a heat transfer of the right magnitude and the wrong
direction.

Note also that $\Delta$ always means *final minus initial* [M TAKE NOTE, p.41],
so $\Delta U<0$ for a cooling system.

## 3. What is a property here, and what is not

$E$ — and hence $U$ — is a **property**: $\Delta E$ depends only on the end
states. $Q$ and $W$ are **path functions** (`1.5`, `2.1`): each depends on the
route. The first law therefore says something sharp and slightly surprising:

> The *difference* $Q-W$ of two path functions is a state function.

Infinitely many $(Q,W)$ pairs produce the same $\Delta U$. A gas can be brought
from state 1 to state 2 adiabatically by doing work on it, or without any work
by heating it, or by any mixture — and the internal energy change is identical.
That is what makes $U$ tabulable (Topic 5) while $Q$ and $W$ never can be.

`first_law_holds(Q, W, dE)` is the residual test $Q-W-\Delta E\approx0$, which is
the right tool when a problem is over-specified: six measured quantities that
ought to satisfy one identity are a far better check on the data than
recomputing a seventh.

## 4. Differential and rate forms

For an infinitesimal change [M Eq. 2.36, §2.5.1, p.62]:
$$dE=\delta Q-\delta W ,$$
where the mixed notation is deliberate — $dE$ exact, $\delta Q$ and $\delta W$
inexact (`2.1` §3). Dividing by $dt$ gives the form that control-volume analysis
actually uses [M Eq. 2.37, §2.5.1, p.62]:
$$\boxed{\;\frac{dE}{dt}=\dot Q-\dot W\;}$$
— `rate_energy_balance`. At **steady state** nothing accumulates, $dE/dt=0$, and
the balance collapses to $\dot Q=\dot W$ for a closed system; adding flow terms
gives the steady-flow energy equation of `6.4` and every device in Topic 8.

## 5. The cycle, and what the first law does *not* forbid

A cycle returns the system to its initial state, so $\Delta E_{\text{cycle}}=0$
identically and [M Eq. 2.40, §2.6, p.73]
$$W_{\text{cycle}}=Q_{\text{cycle}} .$$
For a power cycle drawing $Q_{\text{in}}$ and rejecting $Q_{\text{out}}$
[M Eq. 2.41, p.73]:
$$W_{\text{cycle}}=Q_{\text{in}}-Q_{\text{out}}$$
— `cycle_net_work` and `power_cycle_work`. The thermal efficiency
$\eta=W_{\text{cycle}}/Q_{\text{in}}$ (M Eq. 2.42) and the COPs (Eqs. 2.44–2.46)
follow, and are developed in `7.1` and Topic 9.

Now the crucial negative result. Nothing in Eq. 2.41 forbids
$Q_{\text{out}}=0$ — a cycle converting heat *entirely* into work, at
$\eta=1$. Energy would still balance perfectly. Such a machine has never been
built, and the reason is not conservation: it is the **second law** (`3.3`),
whose Kelvin–Planck statement exists precisely to rule this out. The first law
is silent on direction, which is why a second law is needed at all.

`fig1_first_law_plane` draws $\Delta E=Q-W$ over the whole $(Q,W)$ plane; its
$\Delta E=0$ contour is exactly the cycle condition, and `fig2_power_cycle`
marks the forbidden $Q_{\text{out}}=0$ line.

## 6. The worked case

M's Example 2.2 cools a gas in a piston–cylinder: the boundary work is the
$+17.6$ kJ computed in `2.2` from Example 2.1(a), and the internal energy falls
by 22 kJ. Solving Eq. 2.35b for the heat, with $\Delta\mathrm{KE}=\Delta\mathrm{PE}=0$:
$$Q=\Delta U+W=(-22)+(+17.6)=-4.4\ \text{kJ},$$
negative, i.e. **out of** the system — `heat_transfer(-22.0, 17.6)` returns
$-4.4$. Note that the gas does positive work *while* being cooled: the work came
partly from the heat rejected and partly from the internal energy store, which
is precisely the flexibility §3 described.

## 7. What the code checks

`test_first_law.py` pins: $\Delta E=Q-W$; the balance solved for each of $Q$,
$W$ and $\Delta U$ in turn, and their mutual consistency; the rate form; the
cycle identity $W_{\text{cycle}}=Q_{\text{cycle}}$; the power-cycle difference;
M's Example 2.2 result of $-4.4$ kJ; and `first_law_holds` accepting a
consistent triple and rejecting an inconsistent one.

## Where this goes

- `3.3` — the second law, which supplies the direction the first law lacks.
- `1.2` / `1.1` — the closed-system and control-volume balances in full.
- `6.4` — steady state, where $dE/dt=0$ does the work.
- `4.1` — enthalpy, the combination $u+pv$ that makes the flow form tidy.
- `7.1` / Topic 9 — efficiencies and the cycles they score.
