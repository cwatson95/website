# EM-12 — AC Circuits & Driven RLC (notes)

AC circuit theory is the **steady-state** response of the elements $R$, $L$, $C$ to a
sinusoidal drive of angular frequency $\omega$. The method (the `~MA-05`
complex-exponential trick) is to write the drive as $\mathrm{Re}\,(V_0e^{i\omega t})$ and
look for a current $I(t)=\mathrm{Re}\,(I_0e^{i\omega t})$: each time-derivative becomes a
factor $i\omega$, so the integro-differential loop equation collapses to **algebra**,
$V=IZ$, with a complex **impedance** $Z$.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e; page numbers
are the *printed* pages. The induction physics of the elements is Gr §7.1–7.2; the
impedance/resonance synthesis is the standard complex method (`~MA-05`/`~MA-06`, Boas
Ch. 2) — Griffiths develops it in the **Ch. 7 problems**, not a numbered section, so the
formulas below are referenced at that level, never to an invented page.

## 1. Element impedances
With $V=\mathrm{Re}\,(V_0e^{i\omega t})$ and $I=\mathrm{Re}\,(I_0e^{i\omega t})$, each
element's voltage–current law becomes a complex Ohm's law $V_0=I_0Z$:
$$Z_R=R,\qquad Z_L=i\omega L,\qquad Z_C=\frac{1}{i\omega C}=-\frac{i}{\omega C}.$$
- **Resistor** ($V=IR$): $Z_R$ is real — current and voltage are in phase.
- **Inductor** ($V=L\,dI/dt$): the derivative pulls down $i\omega L$ — the voltage **leads**
  the current by $90^\circ$.
- **Capacitor** ($I=C\,dV/dt$): inverting gives $1/i\omega C$ — the current **leads** the
  voltage by $90^\circ$.

The imaginary part of $Z$ is the **reactance** $X$: $X_L=\omega L$ grows with frequency,
$X_C=-1/\omega C$ shrinks. Code: `impedance_resistor`, `impedance_inductor`,
`impedance_capacitor`. Impedances combine exactly like resistances — **add in series,
reciprocals add in parallel** (`impedance_series`, `impedance_parallel`).

## 2. The series RLC
For $R$, $L$, $C$ in series the same current flows through all three, so the impedances
add:
$$Z=Z_R+Z_L+Z_C=R+i\!\left(\omega L-\frac{1}{\omega C}\right).$$
The real part $R$ dissipates; the net reactance $X=\omega L-1/\omega C$ stores and returns
energy. Its magnitude and phase are
$$\lvert Z\rvert=\sqrt{R^2+\Big(\omega L-\tfrac{1}{\omega C}\Big)^2},\qquad
  \arg Z=\arctan\frac{\omega L-1/\omega C}{R}.$$
Code: `series_rlc_impedance` returns this as a Python `complex`.

## 3. Resonance and the quality factor
The reactance vanishes when $\omega L=1/\omega C$, i.e. at the **resonant frequency**
$$\omega_0=\frac{1}{\sqrt{LC}},$$
the natural frequency of the undriven $LC$ loop. There $Z=R$ is purely real and
**minimal** ($\lvert Z\rvert=R$). The **quality factor** sets how sharply tuned the peak
is:
$$Q=\frac{\omega_0 L}{R}=\frac{1}{R}\sqrt{\frac{L}{C}},$$
the second form because $\omega_0 L=L/\sqrt{LC}=\sqrt{L/C}$. The full width at half-power
is
$$\Delta\omega=\frac{\omega_0}{Q}=\frac{R}{L},$$
so a high-$Q$ circuit (small $R$) is narrowly selective. Code: `resonant_frequency`,
`quality_factor`, `bandwidth`.

## 4. Amplitude, phase and average power
Phasor Ohm's law gives the steady-state current amplitude and its phase relative to the
drive:
$$\lvert I\rvert=\frac{V_0}{\lvert Z\rvert}
   =\frac{V_0}{\sqrt{R^2+(\omega L-1/\omega C)^2}},\qquad
  \phi=-\arg Z=-\arctan\frac{\omega L-1/\omega C}{R}.$$
The current is **largest at resonance** ($\lvert Z\rvert=R$, so $\lvert I\rvert=V_0/R$),
and $\phi$ passes through zero there. Below $\omega_0$ the circuit is **capacitive**
($X<0$, $\phi>0$: current leads); above $\omega_0$ it is **inductive** ($X>0$, $\phi<0$:
current lags). Code: `current_amplitude`, `current_phase`.

Only the resistor dissipates, so the time-averaged power is
$$\langle P\rangle=\tfrac12\lvert I\rvert^2R
   =\tfrac12\frac{V_0^2R}{\lvert Z\rvert^2}
   =\tfrac12V_0^2\,\frac{\mathrm{Re}\,Z}{\lvert Z\rvert^2}
   =\tfrac12V_0\lvert I\rvert\cos\phi,$$
with $\cos\phi=R/\lvert Z\rvert$ the **power factor**. It peaks at
$\langle P\rangle=V_0^2/2R$ on resonance; the **half-power points**
$\lvert Z\rvert^2=2R^2$ (i.e. $\lvert X\rvert=R$) sit at $\omega_0\pm\Delta\omega/2$ and
define $Q$. Code: `average_power`.

## 5. The `~CM-15` analogy (the same ODE)
Kirchhoff's voltage law around the loop, written for the capacitor charge $q$ (with
$I=\dot q$), is
$$L\ddot q+R\dot q+\frac{q}{C}=V_0\cos\omega t.$$
This is **identical** to the driven, damped mechanical oscillator of `~CM-15`,
$m\ddot x+b\dot x+kx=F_0\cos\omega t$, under the dictionary

| mechanical (`~CM-15`) | electrical (EM-12) |
|---|---|
| mass m | inductance L |
| damping b | resistance R |
| stiffness k | inverse capacitance 1/C |
| displacement x | charge q |
| drive F₀ | EMF V₀ |
| velocity dx/dt | current I = dq/dt |

Every result above is therefore a `~CM-15` result re-labelled: $\omega_0=1/\sqrt{LC}
\leftrightarrow\sqrt{k/m}$, $Q=\omega_0L/R\leftrightarrow\omega_0 m/b=\sqrt{mk}/b$, the
Lorentzian resonance peak, the phase that swings through $90^\circ$, and the half-power
bandwidth. This is the electrical end of **KEY BRIDGE B6** — the oscillator that runs
`~CM-15` → `~CM-16` → `~QM-09` → `~QF-01`. The single method that solves both the
mechanical and electrical versions is the `~MA-05`/`~MA-06` complex exponential.

## Where this goes
- `~EM-16` reuses impedance for **transmission lines** (characteristic impedance $Z_0$)
  and resonance/$Q$ for **microwave cavities**.
- `~EM-15`: the phasor $E_0e^{i(kz-\omega t)}$ that solves the wave equation is the same
  complex ansatz, and the ratio $E/H$ of a wave is its **impedance**
  ($\eta=\sqrt{\mu/\varepsilon}\approx 377\,\Omega$ in vacuum).
- `~EM-13`: the AC current a capacitor "passes" is completed across its gap by the
  **displacement current** $\varepsilon_0\,\partial\mathbf E/\partial t$.
- The driven-oscillator resonance recurs all along bridge **B6** — `~CM-16` (normal
  modes), `~QM-09` (the quantum SHO), and the driven nonlinear response of `~QO-06`
  (Brillouin/Raman).
