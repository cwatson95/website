# CM-21 — Hamilton–Jacobi Theory & Action-Angle Variables (notes)

Citation key (details + PDF pages in `refs.md`): **G** = Goldstein 3e *(image scan)*.

## The Hamilton–Jacobi equation
Seek a canonical transformation (`~CM-20`) to coordinates in which the new
Hamiltonian vanishes; the generating function is **Hamilton's principal function**
S(q, t), satisfying [G §10.1 p.430]
$$H\!\left(q,\frac{\partial S}{\partial q}\right)+\frac{\partial S}{\partial t}=0.$$
For a time-independent H, separate S = W(q) − E t; **Hamilton's characteristic
function** W satisfies H(q, ∂W/∂q) = E [G §10.3 p.440]. For 1-DOF,
∂W/∂q = p = √(2m(E − V)), so W = ∫p dq (`characteristic_function`).

## Action-angle variables
For bound (periodic) motion the natural variable is the **action** [G §10.6 p.452]
$$J=\oint p\,dq,$$
an adiabatic invariant. The conjugate **angle** advances linearly in time at the
frequency ω = 2π ∂E/∂J. Equivalently the **period** is
$$T=\frac{dJ}{dE}=\oint\frac{dq}{v},$$
which the code evaluates with an angle substitution that cancels the
turning-point √ singularity (`action_variable`, `period`, `frequency`).

## Isochronous vs anharmonic
- **Harmonic oscillator:** J = 2πE/ω and T = 2π/ω — *independent of energy*
  (isochronous), the special case behind clocks (a test, exact to machine precision).
- **Pendulum** V = 1 − cos θ: T grows with amplitude (anharmonic); the small-energy
  limit recovers 2π√(l/g) (a test).

The action is the bridge to the old quantum theory (Bohr–Sommerfeld ∮p dq = nh)
and to WKB (`~QM-15`), where S/ℏ is the quantum phase.
