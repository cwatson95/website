# CM-25 — Problems

Work by hand, then check with `code/waves_in_media.py`. Citations in `../refs.md`.

### P1.  Wave speed on a string  *(Boas 3e §13.4, p.633)*
Show transverse waves travel at c = √(T/μ). *Check:* `wave_speed(T, mu)`.

*Answer:* $c=\sqrt{T/\mu}$ — greater tension speeds waves up, more mass per unit length slows them.

**Solution.** Apply Newton's law to a string element of length $dx$ and mass $\mu\,dx$. For small slopes the transverse component of the tension at each end is $T\sin\theta\approx T\,y_x$, so the net transverse force is the difference $T\big(y_x|_{x+dx}-y_x|_x\big)=T\,y_{xx}\,dx$. Newton's law $\mu\,dx\,y_{tt}=T\,y_{xx}\,dx$ then gives
$$\frac{\partial^2 y}{\partial t^2}=\frac{T}{\mu}\frac{\partial^2 y}{\partial x^2}\equiv c^2\frac{\partial^2 y}{\partial x^2},\qquad c=\sqrt{\frac{T}{\mu}}.$$
The disturbance propagates at $c=\sqrt{T/\mu}$. For $T=100,\ \mu=0.01$, `wave_speed(100,0.01)` $=\sqrt{10^4}=100$.

### P2.  Harmonics of a string  *(Boas 3e §13.4, p.633)*
From the fixed–fixed boundary conditions derive f_n = nc/2L and λ_n = 2L/n, and
show the overtones are integer multiples of the fundamental. *Check:*
`string_mode_frequency`, `string_wavelength`.

*Answer:* $k_n=n\pi/L\Rightarrow\lambda_n=2L/n$ and $f_n=nc/2L=n f_1$ — the overtones are exact integer multiples of the fundamental.

**Solution.** A standing mode $y=\sin(kx)\cos(\omega t)$ with $\omega=ck$ already satisfies $y(0)=0$; the far boundary then forces
$$\sin(kL)=0\ \Rightarrow\ k_n=\frac{n\pi}{L},\qquad \lambda_n=\frac{2\pi}{k_n}=\frac{2L}{n}.$$
The temporal frequency is $f_n=\omega_n/2\pi=ck_n/2\pi=nc/2L$, so $f_n=n\,f_1$ with fundamental $f_1=c/2L$: every overtone is an exact integer multiple of $f_1$ — the reason a plucked string sounds one definite musical pitch. For $c=100,\ L=1$ this gives $f_1=50$ and $f_2=100=2f_1$, matching `string_mode_frequency` and `string_wavelength`.

### P3.  A plucked mode evolves as a standing wave  *(→ `~MA-08`)*
Start `wave_1d` from y(x,0) = sin(πx/L), ẏ = 0 and show it equals
sin(πx/L)cos(cπt/L). *Check:* `wave_1d` vs `wave_mode` from MA-08.

*Answer:* $y(x,t)=\sin(\pi x/L)\cos(c\pi t/L)$ — a pure standing wave oscillating at $f_1=c/2L$ with fixed nodes at the ends.

**Solution.** The initial data $y(x,0)=\sin(\pi x/L)$ with $\dot y(x,0)=0$ is exactly the $n=1$ normal mode, so the string keeps that spatial profile and only oscillates in time:
$$y(x,t)=\sin\!\frac{\pi x}{L}\,\cos\!\frac{c\pi t}{L},\qquad \omega_1=ck_1=\frac{c\pi}{L}.$$
This solves the wave equation because $y_{tt}=-\omega_1^2\,y$ and $c^2 y_{xx}=-c^2(\pi/L)^2 y=-\omega_1^2 y$ are equal; it meets the fixed ends ($\sin0=\sin\pi=0$) and the zero-velocity start ($\dot y\propto-\sin0=0$). The profile never travels — only its amplitude breathes at $f_1=\omega_1/2\pi=c/2L$. Evolving the same data with `wave_1d` reproduces the closed-form `wave_mode` from MA-08 to within $10^{-2}$ at every interior node.

### P4.  Non-dispersive vs dispersive  *(standard)*
Show ω = ck gives v_p = v_g = c, while ω = √(c²k²+ω₀²) gives v_p > c > v_g with
v_p·v_g = c². *Check:* `phase_velocity`/`group_velocity` for `nondispersive` and
`klein_gordon`.

*Answer:* non-dispersive $\Rightarrow v_p=v_g=c$; Klein–Gordon $\Rightarrow v_p=\sqrt{c^2+\omega_0^2/k^2}>c>v_g=c^2/v_p$, with $v_p v_g=c^2$.

**Solution.** For $\omega=ck$ both velocities equal the same constant, $v_p=\omega/k=c$ and $v_g=d\omega/dk=c$, so a pulse keeps its shape — no dispersion. For $\omega=\sqrt{c^2k^2+\omega_0^2}$,
$$v_p=\frac{\omega}{k}=\sqrt{c^2+\frac{\omega_0^2}{k^2}}>c,\qquad v_g=\frac{d\omega}{dk}=\frac{c^2k}{\sqrt{c^2k^2+\omega_0^2}}=\frac{c^2}{v_p}<c,$$
so $v_p\,v_g=c^2$ — the signature of the medium: the phase races ahead of $c$ while the group lags behind. At $c=2,\ \omega_0=1,\ k=1$ this gives $\omega=\sqrt5$, $v_p=2.2361$, $v_g=4/\sqrt5=1.7889$, and $v_p v_g=4.0000=c^2$, exactly the `phase_velocity`/`group_velocity` outputs for `nondispersive` (both $2$) and `klein_gordon`.

### P5.  Why the phase velocity can exceed c  *(→ `~EM-15`, `~RE`)*
Explain why v_p > c does not violate relativity (no information travels at the
phase velocity; the signal moves at v_g ≤ c). Connect to EM waves in a waveguide
or plasma (`~EM-15`).

*Answer:* a pure phase carries no information (it is unmodulated and infinite); signals ride the modulation at $v_g=c^2/v_p\le c$, so $v_p>c$ never transmits anything faster than light.

**Solution.** A single plane wave $e^{i(kx-\omega t)}$ extends over all space and time with constant amplitude, so its travelling phase carries no information — there is no feature whose arrival could be timed. To send a signal you must modulate the wave (switch it on, build a packet), superposing a band of wavenumbers that moves at the group velocity. For the Klein–Gordon / plasma relation
$$v_g=\frac{c^2}{v_p}<c\qquad(\text{because } v_p>c),$$
so although the phase outruns light, the envelope — and with it any signal or energy — travels slower than $c$, and causality is safe. The same dispersion $\omega=\sqrt{c^2k^2+\omega_p^2}$ governs EM waves in a waveguide or plasma (`~EM-15`), where $v_p>c$ yet $v_g<c$, consistent with `group_velocity(klein_gordon(...))` $<c$.
