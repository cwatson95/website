# MA-22 — Problems

Work by hand, then check with `code/topo_dynamics.py`. Citations in `../refs.md`.

### P1.  Classify the equilibria  *(Chicone §1.6, pp.20–23)*
For each Jacobian find the eigenvalues and classify the rest point:
[[1,0],[0,−1]] (saddle), [[−2,0],[0,−1]] (stable node), [[−1,−2],[2,−1]] (stable
spiral), [[0,−1],[1,0]] (center). *Check:* `classify_equilibrium(J)`.

**Solution.** Eigenvalues come from $\det(J-\lambda I)=\lambda^2-(\operatorname{tr}J)\lambda+\det J=0$;
stability is set by the sign of $\operatorname{Re}\lambda$.
$$\begin{pmatrix}1&0\\0&-1\end{pmatrix}\!:\ \lambda=1,-1\ \text{(opposite sign, }\det=-1<0)\Rightarrow\textbf{saddle};$$
$$\begin{pmatrix}-2&0\\0&-1\end{pmatrix}\!:\ \lambda=-2,-1<0\Rightarrow\textbf{stable node};$$
$\begin{pmatrix}-1&-2\\2&-1\end{pmatrix}$ has $\operatorname{tr}=-2,\det=5$, disc $=4-20<0$,
so $\lambda=-1\pm2i$ ($\operatorname{Re}<0$) $\Rightarrow$ **stable spiral**; and
$\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ has $\operatorname{tr}=0,\det=1$, $\lambda=\pm i$
(purely imaginary) $\Rightarrow$ **center**. These are exactly the strings
`classify_equilibrium(J)` returns for the four matrices.

### P2.  Why no chaos in the plane  *(Chicone p.91)*
State the Poincaré–Bendixson theorem and explain why a bounded 2-D flow can only
end at an equilibrium or a limit cycle — so chaos in a continuous system needs ≥3
dimensions (or a discrete map). (Pen-and-paper.)

**Solution.** *Poincaré–Bendixson.* For a $C^1$ planar flow $\dot{\mathbf x}=f(\mathbf x)$,
if a forward orbit stays in a closed bounded region $K$ that contains **no equilibrium**,
then its $\omega$-limit set is a **periodic orbit** (a limit cycle). Equivalently, a
bounded planar trajectory can only end at an equilibrium or approach a closed orbit.
The reason is topological: by the Jordan curve theorem a closed orbit in the plane
separates inside from outside, and continuity ($C^1$ flows can't cross trajectories)
traps the motion — there is no room for the exponential stretch-and-fold that defines
chaos. Hence sustained aperiodic (chaotic) motion needs $\ge 3$ continuous dimensions
(e.g. the Lorenz system) **or** a discrete map such as the logistic map below.

### P3.  Logistic fixed point & its stability  *(Chicone pp.13–14)*
Find the fixed point x*=1−1/r of x→rx(1−x) and show it is stable iff |f′(x*)|<1,
i.e. r<3. *Check:* `logistic_orbit(2.5, 0.1, 20, skip=5000)` → 1−1/2.5 = 0.6.

**Solution.** A fixed point satisfies $x^\*=rx^\*(1-x^\*)$, so either $x^\*=0$ or
$1=r(1-x^\*)\Rightarrow x^\*=1-\tfrac1r$. The multiplier is $f'(x)=r(1-2x)$, and at the
nontrivial fixed point
$$f'(x^\*)=r\Big(1-2\big(1-\tfrac1r\big)\Big)=2-r.$$
Stability requires $|f'(x^\*)|<1$, i.e. $|2-r|<1\Rightarrow 1<r<3$. At $r=2.5$,
$x^\*=1-1/2.5=0.6$ and $f'(x^\*)=-0.5$ (so $|{\cdot}|<1$, stable). Accordingly
`logistic_orbit(2.5, 0.1, 20, skip=5000)` settles to $0.6$.

### P4.  Period-doubling  *(Chicone Ch.8, p.545)*
Track the attracting period as r increases through 3.2, 3.5, 3.55: observe 2 → 4 →
8 (the Feigenbaum cascade). *Check:* `period_of_orbit(3.2)`, `(3.5)`, `(3.55)`.

**Solution.** When $r$ crosses $3$, $|f'(x^\*)|=|2-r|>1$ and the fixed point loses
stability through a **period-doubling** (flip) bifurcation: the multiplier passes through
$-1$, spawning a stable 2-cycle of $f$ (a fixed point of $f^{2}$). The same instability
recurs for $f^{2},f^{4},\dots$, so the attracting period doubles $1\to2\to4\to8\to\cdots$
at bifurcation values $r\approx3,\,3.449,\,3.544,\dots$ accumulating at the Feigenbaum
point $r_\infty\approx3.5699$. The detector confirms the cascade:
$$\texttt{period\_of\_orbit(3.2)}=2,\quad \texttt{(3.5)}=4,\quad \texttt{(3.55)}=8.$$

### P5.  Lyapunov exponent of chaos  *(Chicone p.28)*
Compute λ=⟨ln|r(1−2x)|⟩ along the orbit. Show λ<0 on stable cycles and λ>0 at r=4
(= ln 2). *Check:* `lyapunov_logistic(4.0)` ≈ 0.693.

**Solution.** Nearby orbits separate as $|\delta x_n|\approx|\delta x_0|\prod_{k}|f'(x_k)|$,
so the per-step growth rate is the orbit average
$$\lambda=\lim_{n\to\infty}\frac1n\sum_{k=0}^{n-1}\ln\big|f'(x_k)\big|,\qquad f'(x)=r(1-2x).$$
On a stable cycle the $\ln|f'|$ average is negative — `lyapunov_logistic(2.5)`$=-0.693$,
`(3.2)`$=-0.916$ (orbits converge). At $r=4$ the map is conjugate to the tent map (via
$x=\sin^2(\pi\theta/2)$), whose slope is $\pm2$ everywhere, so $\ln|f'|=\ln2$ at every
point and $\lambda=\ln2$ exactly. Indeed `lyapunov_logistic(4.0)`$=0.69315\approx\ln2=0.69315$
— a positive exponent, the signature of chaos.

### P6.  Euler characteristic  *(Hatcher p.6 / p.146)*
Verify V−E+F = 2 for all five Platonic solids and explain why (each is a sphere).
Build a torus mesh and confirm χ=0=2−2g with g=1. *Check:* `euler_characteristic(V,E,F)`
on `PLATONIC`.

**Solution.** With $\chi=V-E+F$, the five Platonic solids give
$$\text{tetra }(4,6,4),\ \text{cube }(8,12,6),\ \text{octa }(6,12,8),\ \text{dodeca }(20,30,12),\ \text{icosa }(12,30,20)$$
$$\Rightarrow\ \chi=4{-}6{+}4=8{-}12{+}6=6{-}12{+}8=20{-}30{+}12=12{-}30{+}20=2.$$
Every convex polyhedron is homeomorphic to the sphere (radial projection onto $S^2$), and
$\chi(S^2)=2$ is a topological invariant — independent of how the surface is meshed. A
**torus** ($g=1$ handle) instead has $\chi=2-2g=0$; a triangulation $(V,E,F)=(9,27,18)$ gives
$9-27+18=0$. So `euler_characteristic(V,E,F)` returns $2$ for every entry of `PLATONIC`.
