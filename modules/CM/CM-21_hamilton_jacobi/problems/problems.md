# CM-21 — Problems

Work by hand, then check with `code/hamilton_jacobi.py`. Citations in `../refs.md`.

### P1.  Separating the HJ equation  *(Goldstein 3e §10.3, p.440)*
For a time-independent H show S = W(q) − Et reduces the Hamilton–Jacobi equation
to H(q, ∂W/∂q) = E, and for 1-DOF gives ∂W/∂q = √(2m(E−V)). *Check:*
`characteristic_function`.
*Answer:* $H(q,\partial W/\partial q)=E$ with $\partial W/\partial q=\sqrt{2m(E-V)}$.

**Solution.** The Hamilton–Jacobi equation is $H\!\left(q,\dfrac{\partial S}{\partial q}\right)+\dfrac{\partial S}{\partial t}=0$.
Insert the separated ansatz $S(q,t)=W(q)-Et$, for which
$$\frac{\partial S}{\partial q}=\frac{dW}{dq},\qquad \frac{\partial S}{\partial t}=-E,$$
so the time term supplies the $-E$ and the equation collapses to the time-independent $H(q,\partial W/\partial q)=E$.
For one degree of freedom $H=\dfrac{p^2}{2m}+V(q)$ with $p=\partial W/\partial q$, setting $H=E$ gives
$\dfrac{(\partial W/\partial q)^2}{2m}+V=E$, hence
$$\frac{\partial W}{\partial q}=\sqrt{2m\,(E-V(q))},\qquad W(q)=\int\sqrt{2m(E-V)}\,dq.$$
This is precisely the integrand `characteristic_function` accumulates from the turning point outward.

### P2.  Action of the harmonic oscillator  *(Goldstein 3e §10.6, p.452)*
Show J = ∮p dq = 2πE/ω for V = ½mω²q². *Check:* `action_variable` vs 2πE/ω.
*Answer:* $J=2\pi E/\omega$.

**Solution.** In phase space the energy-$E$ orbit is $\dfrac{p^2}{2m}+\dfrac12 m\omega^2 q^2=E$, an ellipse,
and $J=\oint p\,dq$ is the area it encloses. Its semi-axes are
$$q_{\max}=\sqrt{\frac{2E}{m\omega^2}},\qquad p_{\max}=\sqrt{2mE},$$
so the enclosed area is
$$J=\pi\,q_{\max}\,p_{\max}=\pi\sqrt{\frac{2E}{m\omega^2}}\,\sqrt{2mE}=\frac{2\pi E}{\omega}.$$
(The direct integral $J=2\int_{-a}^{a}\sqrt{2m(E-\tfrac12 m\omega^2 q^2)}\,dq$ gives the same result.)
For $\omega=2$ this is $J=\pi E$; at $E=1$, `action_variable` $\to 3.14160$ versus $2\pi E/\omega=3.14159$.

### P3.  The oscillator is isochronous  *(Goldstein 3e §10.6, p.452)*
Show T = dJ/dE = 2π/ω, independent of energy/amplitude. *Check:* `period` for
several E.
*Answer:* $T=dJ/dE=2\pi/\omega$, independent of $E$ (isochronous).

**Solution.** From P2 the action is $J=2\pi E/\omega$ with $\omega$ constant. The period of any bound
1-DOF motion is $T=dJ/dE$, so
$$T=\frac{dJ}{dE}=\frac{d}{dE}\!\left(\frac{2\pi E}{\omega}\right)=\frac{2\pi}{\omega}.$$
There is no $E$ on the right: the period is independent of energy, hence of amplitude — the oscillator is
**isochronous** (the basis of the pendulum clock at small swing). The recovered frequency is
$\omega_{\rm osc}=2\pi/T=\omega$. For $\omega=2$, `period` returns $3.14159=2\pi/\omega$ at every tested $E$
(e.g. $E=1,2,4$), exactly as claimed.

### P4.  The pendulum is anharmonic
Show the pendulum period grows with amplitude and reduces to 2π√(l/g) for small
swings. *Check:* `period(lambda q: 1-cos(q), 1, E, …)` increasing in E.
*Answer:* $T\to 2\pi\sqrt{l/g}$ as the amplitude $\to 0$, and $T$ grows with amplitude.

**Solution.** Expand the potential for small angle, $V=1-\cos\theta=\tfrac12\theta^2-\tfrac{1}{24}\theta^4+\cdots$.
Keeping the leading term gives a harmonic well $V\approx\tfrac12\theta^2$ with $\omega_0=1$, so as $E\to0$
the period approaches the isochronous value
$$T_0=\frac{2\pi}{\omega_0}=2\pi\sqrt{\frac{l}{g}}=2\pi\qquad(l=g=1).$$
The quartic correction is negative, so the true restoring torque $-\sin\theta$ is softer than the linear
$-\theta$: the bob lingers near the turning points and $T$ grows with amplitude (exactly,
$T=4\sqrt{l/g}\,K(\sin\tfrac{\theta_{\max}}{2})$, increasing in $\theta_{\max}$). The code bears this out —
`period` rises from $6.2911\approx2\pi$ at $E=0.01$ to $6.7430$ at $E=0.5$ and $8.6261$ at $E=1.5$.

### P5.  Bohr–Sommerfeld quantization  *(→ `~QM-01`/`~QM-15`)*
Impose the old-quantum-theory condition ∮p dq = nh on the oscillator and recover
E_n = nℏω. *(A historical bridge from the classical action to quantization.)*
*Answer:* $\oint p\,dq=nh$ with $J=2\pi E/\omega$ gives $E_n=n\hbar\omega$.

**Solution.** From P2 the oscillator's action is $J=\oint p\,dq=\dfrac{2\pi E}{\omega}$ (the value
`action_variable` returns numerically). The Bohr–Sommerfeld rule quantizes this action in units of
Planck's constant,
$$\oint p\,dq=nh\quad\Longrightarrow\quad \frac{2\pi E_n}{\omega}=nh,$$
so $E_n=\dfrac{nh\,\omega}{2\pi}=n\hbar\omega$ using $\hbar=h/2\pi$. The old quantum theory thus gives evenly
spaced levels $E_n=n\hbar\omega$. The full WKB treatment (`~QM-15`) adds the Maslov $\tfrac12$,
$\oint p\,dq=(n+\tfrac12)h$, sharpening this to $E_n=(n+\tfrac12)\hbar\omega$ and restoring the zero-point
energy the old theory missed — but the level spacing $\hbar\omega$ already drops straight out of the
classical action $J=2\pi E/\omega$.
