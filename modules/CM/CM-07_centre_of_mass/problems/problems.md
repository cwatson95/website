# CM-07 — Problems

Work by hand, then check with `code/centre_of_mass.py`. Citations in `../refs.md`.

### P1.  Centre of mass of two bodies  *(Fowles 7e §7.1, p.275)*
Find the CM of m₁ at the origin and m₂ at distance d. *Answer:* a distance
m₂d/(m₁+m₂) from m₁. *Check:* `centre_of_mass([3,1], [[0,0,0],[4,0,0]])` → (1,0,0).

**Solution.** Put $m_1$ at the origin and $m_2$ at $\mathbf d$. The mass-weighted average position is
$$\mathbf R=\frac{m_1\cdot\mathbf 0+m_2\mathbf d}{m_1+m_2}=\frac{m_2}{m_1+m_2}\,\mathbf d,$$
a distance $m_2 d/(m_1+m_2)$ from $m_1$ along the line to $m_2$ — always pulled toward the heavier body. For $m_1=3,\ m_2=1,\ \mathbf d=(4,0,0)$: $\mathbf R=\tfrac14(4,0,0)=(1,0,0)$, exactly `centre_of_mass([3,1], [[0,0,0],[4,0,0]])`.

### P2.  The CM moves uniformly  *(Goldstein 3e §1.2, p.5)*
Argue from **P** = M**V** that, with no external force, the CM velocity is constant
— internal forces cannot accelerate it. *Check:* `cm_velocity` is invariant under
internal interactions.

**Solution.** The total momentum is $\mathbf P=\sum_i m_i\mathbf v_i=M\mathbf V$ with $M=\sum_i m_i$, so $\mathbf V=\mathbf P/M$. Differentiating,
$$M\dot{\mathbf V}=\frac{d\mathbf P}{dt}=\mathbf F^{\rm(ext)},$$
because internal forces cancel pairwise (Newton's third law). With $\mathbf F^{\rm(ext)}=\mathbf 0$ we get $\dot{\mathbf V}=\mathbf 0$: the CM glides at constant velocity, and internal interactions only shuffle momentum among the parts. Hence `cm_velocity` is invariant under internal interactions.

### P3.  Reduced mass limits  *(Fowles 7e §7.3, p.283)*
Show μ = m/2 for equal masses and μ → m₁ when m₂ ≫ m₁ (e.g. Earth–Sun). *Check:*
`reduced_mass(2,2)=1`, `reduced_mass(1,1e12)≈1`.

**Solution.** From $\mu=\dfrac{m_1 m_2}{m_1+m_2}$: equal masses $m_1=m_2=m$ give $\mu=\dfrac{m^2}{2m}=\dfrac m2$. For $m_2\gg m_1$, divide numerator and denominator by $m_2$:
$$\mu=\frac{m_1}{\,m_1/m_2+1\,}\ \xrightarrow{\,m_1/m_2\to0\,}\ m_1.$$
The reduced mass collapses onto the lighter body (e.g. essentially Earth's mass in Earth–Sun). So `reduced_mass(2,2)=1` and `reduced_mass(1,1e12)≈1`.

### P4.  Two-body → one-body  *(Fowles 7e §7.3, p.283)*
Show the relative coordinate **r** = **r₁** − **r₂** obeys μ**r̈** = **F**₁₂ — a
single particle of mass μ in the interaction force. *Check:* `two_body_decompose`.

**Solution.** Write Newton's law for each particle, $m_1\ddot{\mathbf r}_1=\mathbf F_{12}$ and $m_2\ddot{\mathbf r}_2=\mathbf F_{21}=-\mathbf F_{12}$, then subtract after dividing by the masses:
$$\ddot{\mathbf r}_1-\ddot{\mathbf r}_2=\frac{\mathbf F_{12}}{m_1}-\frac{-\mathbf F_{12}}{m_2}=\Big(\frac1{m_1}+\frac1{m_2}\Big)\mathbf F_{12}=\frac{\mathbf F_{12}}{\mu}.$$
Since $\mathbf r=\mathbf r_1-\mathbf r_2$, this is $\mu\ddot{\mathbf r}=\mathbf F_{12}$ — a single fictitious particle of mass $\mu$ driven by the interaction force. Together with the free CM motion (P2), `two_body_decompose` returns the pair $(\mathbf R,\mathbf r)$ in which the problem separates (→ `~CM-11`).

### P5.  Centre of mass of a non-symmetric triangle
Three equal masses at (0,0,0), (3,0,0), (0,3,0): find the CM. *Check:*
`centre_of_mass([1,1,1], [[0,0,0],[3,0,0],[0,3,0]])` → (1,1,0).

**Solution.** With three equal masses the CM is the plain average (centroid) of the positions:
$$\mathbf R=\frac13\big[(0,0,0)+(3,0,0)+(0,3,0)\big]=\Big(\tfrac33,\tfrac33,0\Big)=(1,1,0).$$
The equal weights make the mass-weighted average reduce to the geometric centroid of the triangle. This matches `centre_of_mass([1,1,1], [[0,0,0],[3,0,0],[0,3,0]])` → (1,1,0).
