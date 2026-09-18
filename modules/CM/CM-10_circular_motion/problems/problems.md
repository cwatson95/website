# CM-10 — Problems

Work by hand, then check with `code/circular_motion.py`. Citations in `../refs.md`.

### P1.  Centripetal acceleration  *(Fowles 7e §1.11, p.38)*
For uniform circular motion show a_c = v²/R = ω²R, directed toward the centre.
*Check:* `centripetal_acceleration(R*omega, R)` = ω²R; `acceleration(uniform_circular(R,omega))(t)` ≈ −ω²**r**.

**Solution.** Write the trajectory $\mathbf r(t)=R(\cos\omega t,\sin\omega t,0)$ and differentiate twice:
$$\dot{\mathbf r}=R\omega(-\sin\omega t,\cos\omega t,0),\qquad \ddot{\mathbf r}=-\omega^2 R(\cos\omega t,\sin\omega t,0)=-\omega^2\mathbf r.$$
The speed $v=|\dot{\mathbf r}|=R\omega$ is constant, and the acceleration points opposite $\mathbf r$ (inward) with magnitude
$$a_c=\omega^2 R=\frac{(R\omega)^2}{R}=\frac{v^2}{R}.$$
For $R=2,\omega=3$ this is $\omega^2R=18$, exactly `centripetal_acceleration(6, 2)`, while `acceleration(uniform_circular(R,omega))(t)`$=-\omega^2\mathbf r$.

### P2.  Period and frequency
Relate T, f, and ω: T = 2π/ω, f = 1/T. *Check:* `period`, `frequency`,
`angular_velocity` round-trip.

**Solution.** The position $\mathbf r(t)=R(\cos\omega t,\sin\omega t,0)$ repeats when the phase $\omega t$ advances by $2\pi$, i.e. after one **period** $T=2\pi/\omega$. The **frequency** is $f=1/T=\omega/2\pi$, and inverting, $\omega=2\pi/T=2\pi f$. The three converters are mutual inverses, so for $\omega=3$: $T=2\pi/3\approx2.0944$, $f\approx0.4775$, and `angular_velocity(period(3))` round-trips back to $3.0$.

### P3.  Curvature of a circle  *(Fowles 7e §1.11, p.36; → `~CM-01`)*
Show a circle of radius R has curvature κ = 1/R, so a_N = v²/R = κv². *Check:*
`curvature(uniform_circular(2,3))(t)` → 0.5.

**Solution.** Parameterize by arc length $s=R\theta$; the unit tangent $\hat{\mathbf T}$ turns through $d\theta=ds/R$, so the **curvature** is $\kappa=|d\hat{\mathbf T}/ds|=1/R$. The normal (centripetal) acceleration is then $a_N=v^2\kappa=v^2/R$. For $R=2$ this gives $\kappa=\tfrac12$, which is why `curvature(uniform_circular(2,3))(t)`$\to0.5$ (the code returns $0.49999\ldots$ from finite differencing).

### P4.  The conical pendulum
A mass on a string sweeps a horizontal circle. Use F_c = m v²/R supplied by the
horizontal component of the tension to find the angle vs. speed. *Check:*
`centripetal_force(m, v, R)` against the tension component.

**Solution.** Let the string make angle $\theta$ with the vertical and carry tension $\mathbf T$. Vertically the bob is in equilibrium, $T\cos\theta=mg$; horizontally the inward component supplies the centripetal force, $T\sin\theta=\dfrac{mv^2}{R}=F_c$. Dividing the two,
$$\tan\theta=\frac{v^2}{gR}.$$
The horizontal tension component equals `centripetal_force(m, v, R)`$=mv^2/R$ (e.g. $m=1,v=2,R=2\Rightarrow2.0$).

### P5.  Banked curve
A car rounds a curve of radius R at speed v; find the banking angle for which no
friction is needed (tan θ = v²/gR = a_c/g). *Check:* `centripetal_acceleration(v,R)/g`.

**Solution.** On a frictionless bank only gravity $mg$ (down) and the normal force $\mathbf N$ (perpendicular to the road) act. Vertical balance $N\cos\theta=mg$ and the horizontal (centripetal) equation $N\sin\theta=mv^2/R$ divide to give
$$\tan\theta=\frac{v^2}{gR}=\frac{a_c}{g}.$$
The required bank depends only on $a_c/g$, i.e. `centripetal_acceleration(v,R)/g`.
