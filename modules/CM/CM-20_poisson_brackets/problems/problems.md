# CM-20 — Problems

Work by hand, then check with `code/poisson_brackets.py`. Citations in `../refs.md`.

### P1.  Fundamental brackets  *(Goldstein 3e §9.5, p.388)*
Show {q, p} = 1, {q, q} = 0, {p, p} = 0. *Check:* `poisson_bracket` of the
coordinate functions.
*Answer:* $\{q,p\}=1$ and $\{q,q\}=\{p,p\}=0$.

**Solution.** Treat $q$ and $p$ as independent phase-space coordinates, so
$\partial q/\partial q=1,\ \partial q/\partial p=0$ and $\partial p/\partial p=1,\ \partial p/\partial q=0$. The bracket is
$$\{f,g\}=\frac{\partial f}{\partial q}\frac{\partial g}{\partial p}-\frac{\partial f}{\partial p}\frac{\partial g}{\partial q}.$$
With $f=q,\ g=p$: $\{q,p\}=(1)(1)-(0)(0)=1$. With $f=g=q$: $\{q,q\}=(1)(0)-(0)(1)=0$,
and likewise $\{p,p\}=(0)(1)-(1)(0)=0$ — also forced by antisymmetry, since $\{f,f\}=-\{f,f\}=0$.
These are the fundamental brackets, matching `poisson_bracket` $\to 1.000000$ for $\{q,p\}$
and $0.000000$ for $\{q,q\}$.

### P2.  Antisymmetry  *(Goldstein 3e §9.5, p.388)*
Show {f, g} = −{g, f} for arbitrary f, g. *Check:* compare `poisson_bracket(f,g,…)`
to `−poisson_bracket(g,f,…)`.
*Answer:* swapping $f\leftrightarrow g$ flips the sign of every term, so $\{f,g\}=-\{g,f\}$ (hence $\{f,f\}=0$).

**Solution.** Write both brackets out, using that ordinary partial derivatives are numbers that commute:
$$\{f,g\}=\frac{\partial f}{\partial q}\frac{\partial g}{\partial p}-\frac{\partial f}{\partial p}\frac{\partial g}{\partial q},\qquad
\{g,f\}=\frac{\partial g}{\partial q}\frac{\partial f}{\partial p}-\frac{\partial g}{\partial p}\frac{\partial f}{\partial q}.$$
Reading the two right-hand sides term by term, $\{g,f\}$ is $\{f,g\}$ with the two products interchanged,
i.e. with every sign reversed, so $\{f,g\}=-\{g,f\}$. Setting $g=f$ gives $\{f,f\}=-\{f,f\}=0$ — the
reason $\{q,q\}=\{p,p\}=0$ in P1. The check bears this out at every sampled point, where
`poisson_bracket(f,g,…)` and `poisson_bracket(g,f,…)` come out equal and opposite for $f=q^2+p,\ g=qp-p^2$.

### P3.  Equations of motion  *(Goldstein 3e §9.6, p.396)*
Show q̇ = {q, H} = ∂H/∂p and ṗ = {p, H} = −∂H/∂q. *Check:* `time_derivative` of q
and p with the oscillator Hamiltonian.
*Answer:* $\dot q=\{q,H\}=\partial H/\partial p$ and $\dot p=\{p,H\}=-\partial H/\partial q$ — Hamilton's equations.

**Solution.** Put $g=H$ in the bracket and use $\partial q/\partial q=1,\ \partial q/\partial p=0$ (and the reverse for $p$):
$$\{q,H\}=\frac{\partial q}{\partial q}\frac{\partial H}{\partial p}-\frac{\partial q}{\partial p}\frac{\partial H}{\partial q}=\frac{\partial H}{\partial p},\qquad
\{p,H\}=\frac{\partial p}{\partial q}\frac{\partial H}{\partial p}-\frac{\partial p}{\partial p}\frac{\partial H}{\partial q}=-\frac{\partial H}{\partial q}.$$
These are Hamilton's equations, now compressed into the single statement $\dot f=\{f,H\}$. For
$H=\tfrac12 p^2+\tfrac12\omega^2 q^2$ with $\omega=2$ they read $\dot q=p,\ \dot p=-\omega^2 q$; at
$(q,p)=(1,\tfrac12)$ that is $\dot q=0.5$ and $\dot p=-4$, matching `time_derivative` $\to 0.5000$ and $-4.0000$.

### P4.  Conserved quantities  *(Goldstein 3e §9.6, p.396)*
Show a quantity f with ∂f/∂t = 0 is conserved iff {f, H} = 0 (e.g. momentum for a
free particle, energy via {H, H} = 0). *Check:* `time_derivative(p, free_H, …)` ≈ 0.
*Answer:* with $\partial f/\partial t=0$, $df/dt=\{f,H\}$, so $f$ is conserved iff $\{f,H\}=0$; energy via $\{H,H\}=0$, free-particle momentum via $\{p,H\}=0$.

**Solution.** The general rate of change is $\dfrac{df}{dt}=\{f,H\}+\dfrac{\partial f}{\partial t}$. For a quantity
with no explicit time dependence the last term drops, leaving
$$\frac{df}{dt}=\{f,H\},$$
so $f$ is conserved ($df/dt=0$) **iff** $\{f,H\}=0$. Energy is automatic: $\{H,H\}=0$ by antisymmetry (P2),
hence $dH/dt=0$. A free particle has $H=p^2/2m$ depending only on $p$, so $\{p,H\}=-\partial H/\partial q=0$
and momentum is conserved. This is exactly what `time_derivative(p, free_H, …)` $\approx 0$ and
`poisson_bracket(H,H,…)` $=0$ report.

### P5.  Canonical transformations  *(Goldstein 3e §9.5, p.388)*
Show the scaling (Q = λq, P = p/λ) and the swap (Q = p, P = −q) are canonical, but
(Q = q, P = 2p) is not. *Check:* `is_canonical`. *(Preserving {q,p} = preserving
phase-space volume — Liouville's theorem.)*
*Answer:* $\{Q,P\}=1$ for the scaling and the swap (canonical); $\{q,2p\}=2\neq1$ (not canonical).

**Solution.** A map $(q,p)\to(Q,P)$ is canonical iff it preserves the fundamental bracket, $\{Q,P\}=1$. Evaluate each:
$$\{\lambda q,\ p/\lambda\}=\lambda\cdot\tfrac1\lambda-0=1,\qquad
\{p,\ -q\}=(0)(0)-(1)(-1)=1,\qquad
\{q,\ 2p\}=(1)(2)-(0)(0)=2.$$
The scaling and the swap give $1$ and are canonical; $Q=q,\ P=2p$ gives $2$ and is not. Geometrically
$\{Q,P\}$ is the Jacobian $\partial(Q,P)/\partial(q,p)$, so a canonical map preserves phase-space area
(Liouville's theorem) while $Q=q,\,P=2p$ doubles it. Hence `is_canonical` returns `True`, `True`, `False` respectively.
