# EM-12 — Problems

Work each by hand, then check with `code/ac_circuits.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages). Because AC steady-state theory is not a numbered
Griffiths section, problems are cited at the section level (Gr §7.1–7.2) and to the
`~CM-15` driven-oscillator analogy — the same ODE $L\ddot q+R\dot q+q/C=V_0\cos\omega t$.
Use the complex method throughout: drive $\propto e^{i\omega t}$, then solve $V=IZ$.

### P1.  Impedance and resonance of a series RLC  *(Gr §7.1–7.2; complex method)*
For $R$, $L$, $C$ in series driven at $\omega$, show the impedance is
$$Z=R+i\!\left(\omega L-\frac{1}{\omega C}\right),$$
and that the reactance cancels — so $Z$ is **purely resistive and minimal**,
$\lvert Z\rvert=R$ — exactly at $\omega_0=1/\sqrt{LC}$. *Check:*
`series_rlc_impedance(R, L, C, resonant_frequency(L, C))` returns a `complex` with zero
imaginary part and real part $R$; off resonance the imaginary part is nonzero.

**Solution.** In series the same current flows through every element, so the impedances
add: $Z=Z_R+Z_L+Z_C=R+i\omega L+\frac{1}{i\omega C}$. Using $\frac{1}{i\omega C}=-\frac{i}{\omega C}$,
$$Z=R+i\!\left(\omega L-\frac{1}{\omega C}\right),\qquad X\equiv\omega L-\frac{1}{\omega C}.$$
The reactance $X$ vanishes when $\omega L=1/\omega C$, i.e. $\omega^2=1/LC$, giving
$\omega_0=1/\sqrt{LC}$. There $Z=R$ is purely real, and since $\lvert Z\rvert=\sqrt{R^2+X^2}\ge R$
with equality only at $X=0$, the magnitude is **minimal**, $\lvert Z\rvert=R$. So
`series_rlc_impedance(R, L, C, resonant_frequency(L, C))` returns $R+0i$ (here $10+0i\,\Omega$),
while off resonance the imaginary part is nonzero.

### P2.  The current resonance curve  *(~CM-15 analogy)*
With drive amplitude $V_0$, show the steady-state current amplitude
$\lvert I\rvert=V_0/\lvert Z\rvert$ peaks at resonance with $\lvert I\rvert=V_0/R$, and is
smaller at every other frequency. Sketch $\lvert I\rvert(\omega)$ — the Lorentzian
resonance peak shared with the `~CM-15` oscillator. *Check:*
`current_amplitude(V0, series_rlc_impedance(...))` evaluated at `resonant_frequency(L, C)`
equals `V0/R`, and exceeds its values at $0.7\,\omega_0$ and $1.3\,\omega_0$.

**Solution.** Phasor Ohm's law gives $\lvert I\rvert=V_0/\lvert Z\rvert$ with
$\lvert Z\rvert=\sqrt{R^2+X^2}$, $X=\omega L-1/\omega C$. The denominator is smallest when the
reactance vanishes ($X=0$ at $\omega_0$), so the current is largest there:
$$\lvert I\rvert(\omega)=\frac{V_0}{\sqrt{R^2+\left(\omega L-\frac{1}{\omega C}\right)^2}},\qquad
  \lvert I\rvert(\omega_0)=\frac{V_0}{R}.$$
Any nonzero $X$ only adds to the denominator, so $\lvert I\rvert$ falls off on both sides — the
Lorentzian resonance peak shared with the `~CM-15` oscillator, of height $V_0/R$ and width set by
$R$. With $R=10,\,V_0=5$ the peak is $\lvert I\rvert=V_0/R=0.5$ A; at $0.7\,\omega_0$ and
$1.3\,\omega_0$ the current has dropped to $0.199$ A and $0.256$ A — both below the peak, so
`current_amplitude` is maximal exactly at `resonant_frequency(L, C)`.

### P3.  Phase across resonance  *(Gr §7.1–7.2; complex method)*
Show the current phase relative to the drive is $\phi=-\arg Z$: the current **leads**
($\phi>0$, capacitive) below $\omega_0$, **lags** ($\phi<0$, inductive) above, and is zero
at resonance. Explain the signs from the reactance $X=\omega L-1/\omega C$. *Check:*
`current_phase(series_rlc_impedance(...))` is $>0$ at $0.5\,\omega_0$, $\approx 0$ at
$\omega_0$, and $<0$ at $2\,\omega_0$.

**Solution.** The phasor current $I_0=V_0/Z$ carries the phase $\phi=-\arg Z=-\arctan(X/R)$ with
reactance $X=\omega L-1/\omega C$:
$$\phi(\omega)=-\arctan\frac{\omega L-\frac{1}{\omega C}}{R}.$$
Below $\omega_0$ the capacitor dominates ($1/\omega C>\omega L$, so $X<0$): $\phi>0$, the current
**leads** the drive — capacitive. Above $\omega_0$ the inductor dominates ($X>0$): $\phi<0$, the
current **lags** — inductive. At $\omega_0$ the reactances cancel ($X=0$) and $\phi=0$, current in
phase. So `current_phase` returns $+78.1^\circ$ at $0.5\,\omega_0$ (leading), $\approx0$ at
$\omega_0$, and $-78.1^\circ$ at $2\,\omega_0$ (lagging) — equal magnitudes because $X(r\omega_0)
=-X(\omega_0/r)$ is antisymmetric about $\omega_0$ on a log-frequency axis.

### P4.  Quality factor and bandwidth  *(~CM-15: Q ↔ ω₀m/b)*
Derive the two equal forms of the quality factor,
$$Q=\frac{\omega_0 L}{R}=\frac{1}{R}\sqrt{\frac{L}{C}}\qquad(\text{use }\omega_0 L=\sqrt{L/C}),$$
and the half-power bandwidth $\Delta\omega=\omega_0/Q=R/L$. Confirm the mechanical
correspondence $Q\leftrightarrow\omega_0 m/b$. *Check:* `quality_factor(R, L, C)` equals
both `w0*L/R` and `(1/R)*sqrt(L/C)`, and `bandwidth(R, L)` equals
`w0/quality_factor(R, L, C)`.

**Solution.** At resonance the inductive reactance is $\omega_0 L=L/\sqrt{LC}=\sqrt{L/C}$, so the
quality factor — the reactance-to-resistance ratio at $\omega_0$ — has two equal forms:
$$Q=\frac{\omega_0 L}{R}=\frac{1}{R}\sqrt{\frac{L}{C}}.$$
The half-power width is $\Delta\omega=R/L$; dividing by $\omega_0=1/\sqrt{LC}$,
$$\frac{\Delta\omega}{\omega_0}=\frac{R/L}{1/\sqrt{LC}}=\frac{R\sqrt{LC}}{L}=\frac{R}{\sqrt{L/C}}=\frac{1}{Q},$$
so $\Delta\omega=\omega_0/Q$ — small $R$ gives large $Q$ and a narrow, sharply selective peak.
Under the `~CM-15` dictionary $L\to m,\;R\to b$ this is $Q=\omega_0 m/b$, the mechanical quality
factor. With $R=10,\,L=10^{-3},\,C=10^{-6}$: $Q=3.162$ and $\Delta\omega=R/L=10^4$ rad/s, equal to
$\omega_0/Q$ — exactly what `quality_factor(R, L, C)` and `bandwidth(R, L)` return.

### P5.  Average power and the half-power points  *(~CM-15; Gr §7.2.4 energy, p328)*
Show that only the resistor dissipates, so
$$\langle P\rangle=\tfrac12\lvert I\rvert^2R=\tfrac12V_0^2\,\frac{\mathrm{Re}\,Z}{\lvert Z\rvert^2},$$
peaking at $V_0^2/2R$ on resonance. Show the power falls to **half** its peak where
$\lvert X\rvert=R$, i.e. at $\omega_0\pm\Delta\omega/2$ — the width that defines $Q$.
*Check:* `average_power(V0, series_rlc_impedance(...))` equals `V0**2/(2*R)` at $\omega_0$,
is smaller off resonance, and is $\approx$ half-peak at
$\omega_0+\,$`bandwidth(R, L)`$/2$.

**Solution.** Inductor and capacitor are lossless (their current runs $90^\circ$ out of phase with
their voltage), so only $R$ dissipates: with $\lvert I\rvert=V_0/\lvert Z\rvert$,
$$\langle P\rangle=\tfrac12\lvert I\rvert^2R=\frac{V_0^2R}{2\lvert Z\rvert^2}
  =\tfrac12V_0^2\,\frac{\mathrm{Re}\,Z}{\lvert Z\rvert^2},\qquad
  \langle P\rangle_{\max}=\frac{V_0^2}{2R}\ \text{at}\ \omega_0,$$
since $\lvert Z\rvert^2=R^2+X^2$ is minimal ($=R^2$) at resonance. The power halves when
$\lvert Z\rvert^2=2R^2$, i.e. $X^2=R^2$, i.e. $\lvert X\rvert=\lvert\omega L-1/\omega C\rvert=R$.
The two roots of $\omega L-1/\omega C=\pm R$ are separated by exactly $\Delta\omega=R/L$, the
bandwidth that defines $Q$, and lie at $\omega_0\pm\Delta\omega/2$ to leading order in $1/Q$. With
$R=10,\,V_0=5$ the peak is $V_0^2/2R=1.25$ W, and at $\omega_0+\Delta\omega/2$ `average_power`
returns $\approx0.67$ W against the half-peak $0.625$ W — the small excess being the finite-$Q$
asymmetry of the exact half-power roots about $\omega_0$.
