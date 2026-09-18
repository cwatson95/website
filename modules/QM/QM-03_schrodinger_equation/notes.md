# QM-03 — The Schrödinger Equation (notes)

`~QM-01` gave us the de Broglie wave; `~QM-02` made $|\Psi|^2$ a probability
density (Born). What is missing is the **law of motion** for $\Psi$ — the quantum
analogue of $F=ma$. That law is the Schrödinger equation, and this module is
about its structure: how a *single* dynamical equation in time splits, by
separation of variables, into a *spectrum* of stationary states, and how those
recombine into the general solution. Everything here is checked on a grid in
`code/schrodinger.py`.

Citation key: **Gr** = Griffiths & Schroeter, *Introduction to QM*, **3rd ed.**;
pages are the *printed* book page (verified — see `refs.md`).

## 1. The time-dependent Schrödinger equation (the dynamical law)

Classically, give Newton the force and the initial $x,\dot x$ and he returns
$x(t)$ for all time. Quantum mechanics replaces $x(t)$ by the wavefunction
$\Psi(x,t)$, and Newton's law by the **time-dependent Schrödinger equation**
(TDSE) [Gr §1.1, p.16]:
$$\boxed{\;i\hbar\,\frac{\partial \Psi}{\partial t}=\hat H\,\Psi\;},\qquad
\hat H=-\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2}+V(x).$$
$\hat H$ is the **Hamiltonian** (kinetic + potential, with $\hat p\to-i\hbar\,
\partial_x$). Given $\Psi(x,0)$, the TDSE determines $\Psi(x,t)$ for all later
$t$ — it is first order in time, so the *single* function $\Psi(x,0)$ is the
complete initial data (contrast Newton, who needs both position and velocity).
The $i$ makes $\Psi$ intrinsically complex; the $\hbar$ sets the scale.

## 2. Separation of variables → the time-independent equation

When $V$ is independent of $t$ (the case treated here and through most of QM),
the PDE yields to **separation of variables** — "the physicist's first line of
attack on any partial differential equation" [Gr §2.1, p.43; cf. `~MA-08`]. Look
for product solutions
$$\Psi(x,t)=\psi(x)\,\varphi(t).$$
Then $i\hbar\,\psi\dot\varphi = \big(-\tfrac{\hbar^2}{2m}\psi''+V\psi\big)\varphi$;
divide by $\psi\varphi$:
$$\underbrace{i\hbar\,\frac{\dot\varphi}{\varphi}}_{\text{function of }t}
=\underbrace{\frac1\psi\Big(-\frac{\hbar^2}{2m}\psi''+V\psi\Big)}_{\text{function of }x}=E.$$
A function of $t$ alone equals a function of $x$ alone only if **both equal a
constant**, $E$ (the *separation constant*, with units of energy). The two
halves are:

- **Time:** $\dot\varphi=-\tfrac{iE}{\hbar}\varphi\;\Rightarrow\;
  \varphi(t)=e^{-iEt/\hbar}$ — universal, the same "wiggle factor" for every
  separable solution [Gr §2.1, p.46].
- **Space:** the **time-independent Schrödinger equation** (TISE), an
  *eigenvalue problem* for $\hat H$:
$$\boxed{\;\hat H\,\psi=E\,\psi\;}\qquad
-\frac{\hbar^2}{2m}\psi''+V(x)\,\psi=E\,\psi.$$
So each separable solution is
$$\Psi_n(x,t)=\psi_n(x)\,e^{-iE_nt/\hbar},$$
with $(\psi_n,E_n)$ an eigenpair of $\hat H$. The allowed energies $E_n$ are the
spectrum; this is where quantization *comes from* (`~QM-08`, `~QM-09`).

## 3. Stationary states — why $|\Psi|^2$ stops moving

For a single separable solution the time dependence is a pure phase, so
$$|\Psi_n(x,t)|^2=|\psi_n(x)|^2\,\big|e^{-iE_nt/\hbar}\big|^2=|\psi_n(x)|^2,$$
**independent of $t$.** Every probability and every expectation value of a
time-independent operator is therefore frozen — hence **stationary state** [Gr
§2.1, p.46]. In particular the energy is *sharp*: $\langle H\rangle=E$ and
$\sigma_H^2=\langle H^2\rangle-\langle H\rangle^2=0$, so a measurement of the
energy of a stationary state is certain to return $E$ [Gr §2.1, p.45]. (The state
is not "doing nothing" — its phase rotates at rate $E/\hbar$; what is frozen is
everything *observable*. The code checks both: $|\Psi|^2$ constant to machine
precision, yet $\Psi(t=\pi\hbar/E)=-\psi$.)

## 4. The general solution: superposition and the rôle of the $c_n$

The TISE delivers a whole (generally infinite, discrete) family $\{\psi_n,E_n\}$
that is **orthonormal** and **complete** [Gr §2.2, p.51]:
$$\langle\psi_m|\psi_n\rangle=\int\psi_m^\ast\psi_n\,dx=\delta_{mn}.$$
Because the TDSE is *linear*, any sum of separable solutions is again a solution,
and completeness guarantees this is the **general** solution [Gr §2.1, p.45–46]:
$$\boxed{\;\Psi(x,t)=\sum_n c_n\,\psi_n(x)\,e^{-iE_nt/\hbar}\;}$$
The constants $c_n$ are fixed *once and for all* by the initial state
$\Psi(x,0)=\sum_n c_n\psi_n(x)$, extracted by **Fourier's trick** (project onto
$\psi_n$ and use orthonormality) [Gr §2.2, p.51]:
$$c_n=\langle\psi_n|\Psi(\cdot,0)\rangle=\int\psi_n^\ast(x)\,\Psi(x,0)\,dx.$$
Their meaning [Gr §2.1, p.47]: $|c_n|^2$ is the **probability that a measurement
of the energy yields $E_n$**, so
$$\sum_n|c_n|^2=1,\qquad \langle H\rangle=\sum_n|c_n|^2E_n,$$
and since the $c_n$ are constants in time, *both are conserved* — this is energy
conservation in quantum mechanics. (`code`: `coefficients`, then $\sum|c_n|^2=1$
and reconstruction of $\Psi_0$ to machine precision.)

**Why a superposition is not stationary.** Take two real eigenstates,
$\Psi=\tfrac1{\sqrt2}(\psi_1e^{-iE_1t/\hbar}+\psi_2e^{-iE_2t/\hbar})$. Then
$$|\Psi(x,t)|^2=\tfrac12\Big[\psi_1^2+\psi_2^2+2\psi_1\psi_2
\cos\!\big(\tfrac{(E_2-E_1)t}{\hbar}\big)\Big].$$
The interference cross-term **beats** at the **Bohr angular frequency**
$$\omega=\frac{E_2-E_1}{\hbar},\qquad T=\frac{2\pi\hbar}{E_2-E_1}.$$
So $\langle x\rangle(t)$ oscillates sinusoidally at $\omega$ — only *energy
differences* are observable, which is exactly the spectroscopic content of the
Bohr frequencies from `~QM-01`. (`code`: `measure_period` on $\langle x\rangle(t)$
recovers $T$ to $\sim10^{-9}$; this is Gr Problem 2.5.)

## 5. Solving it on a grid (this module's code)

We never need a closed form to *see* all of the above. Put $\psi$ on a uniform
grid $x_i$ and replace the second derivative by the 3-point finite difference
$$\psi''(x_i)\approx\frac{\psi_{i+1}-2\psi_i+\psi_{i-1}}{(\Delta x)^2}
\quad\Rightarrow\quad
\hat H\to H=-\frac{\hbar^2}{2m}\,\frac{\mathrm{tridiag}(1,-2,1)}{(\Delta x)^2}+\mathrm{diag}\,V_i.$$
$H$ is real-symmetric, so `numpy.linalg.eigh` returns real $E_n$ and orthonormal
$\psi_n$ — the TISE solved as a matrix eigenproblem (`~MA-04`). With Dirichlet
walls (the grid endpoints) this *is* the infinite square well [Gr §2.2], and the
code recovers $E_n=n^2\pi^2\hbar^2/2mL^2$ to $<0.02\%$ for the lowest five $n$.
Feed it $V=\tfrac12m\omega^2x^2$ and the *same* routine returns
$E_n=(n+\tfrac12)\hbar\omega$ (`~QM-09`). Time evolution is then just attaching
the phases $e^{-iE_nt/\hbar}$ and summing — `evolve`.

**Units.** The code uses $\hbar=m=1$ (kept as default arguments so the general
$E_n=n^2\pi^2\hbar^2/2mL^2$ can still be exercised — see the tests). Lengths are
in the grid unit, energies in the matching $\hbar^2/(m\cdot\text{length}^2)$.

---
### Where this goes
- The norm $\int|\Psi|^2dx$ is conserved under this (unitary) evolution — the
  *why* is the **probability current / continuity equation**, `~QM-04`
  (`~CM-22`/`~EM-14` are the same equation for mass/charge).
- The eigenproblem $\hat H\psi=E\psi$ and the bra–ket projection $c_n=\langle
  \psi_n|\Psi\rangle$ are the concrete face of the **formalism**, `~QM-05`
  (Hilbert space, operators), and of the **measurement postulates**, `~QM-06`
  ($|c_n|^2$ as a probability).
- The two worked spectra here are developed properly in `~QM-08` (wells, steps,
  barriers) and `~QM-09` (oscillator, analytically and with ladder operators).
