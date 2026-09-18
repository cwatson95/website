# QM-15 — Approximation Methods I (notes)

Almost no Schrödinger equation can be solved exactly. The exactly solvable
systems (free particle, square well, oscillator, hydrogen) are a measure-zero
island; everything else needs **approximation**. This module is the
time-*independent* toolkit — three methods, each answering a different question:

| method | when to use | what it gives |
|---|---|---|
| **Perturbation theory** | $H$ is close to a solved $H^0$ | a power series in the small parameter $\lambda$ |
| **Variational principle** | you only need the ground state, no nearby solved problem | a rigorous **upper bound** on $E_{gs}$ |
| **WKB** | $V(x)$ varies slowly (semiclassical, large $n$) | bound-state energies & tunnelling rates from a single integral |

> **Units.** Natural units $\hbar=m=\omega=1$ throughout (documented in
> `approximations.py`); the oscillator test bed then has $E_n=n+\tfrac12$.

---

## 1. Perturbation theory (Griffiths §7.1, printed p.356)

Split the Hamiltonian into a solved part and a small correction,
$$H=H^0+\lambda H',\qquad H^0|\psi_n^0\rangle=E_n^0|\psi_n^0\rangle,$$
($\lambda$ is a bookkeeping knob, cranked to $1$ at the end). Expand the perturbed
eigenvalue and eigenstate as power series in $\lambda$ (Griffiths Eq. 7.5–7.6):
$$E_n=E_n^0+\lambda E_n^{(1)}+\lambda^2 E_n^{(2)}+\cdots,\qquad
|\psi_n\rangle=|\psi_n^0\rangle+\lambda|\psi_n^{(1)}\rangle+\cdots.$$
Insert into $H|\psi_n\rangle=E_n|\psi_n\rangle$ and collect powers of $\lambda$.

**First-order energy** (take $\langle\psi_n^0|\,\cdot\,$ of the $O(\lambda)$
equation; $H^0$ hermitian kills two terms). The result — *the most used equation
in QM* (Griffiths p.359):
$$\boxed{\,E_n^{(1)}=\langle\psi_n^0|H'|\psi_n^0\rangle\,}\qquad(\text{Eq. 7.9}).$$
The shift is just the expectation value of the perturbation in the unperturbed
state — no resolvent, no sum. (`first_order_energy`.)

**First-order state** (Griffiths Eq. 7.13, p.361). Expand $|\psi_n^{(1)}\rangle$
in the unperturbed basis; matching the $O(\lambda)$ equation gives
$$\boxed{\,|\psi_n^{(1)}\rangle=\sum_{m\neq n}
\frac{\langle\psi_m^0|H'|\psi_n^0\rangle}{E_n^0-E_m^0}\,|\psi_m^0\rangle\,}.$$
(`first_order_correction`.) The $m=n$ term is dropped by the normalization
choice. The denominator is the warning sign: if any $E_m^0=E_n^0$ it **blows
up** — that is the door to degenerate PT.

**Second-order energy** (take $\langle\psi_n^0|\,\cdot\,$ of the $O(\lambda^2)$
equation, Griffiths §7.1.3, p.363):
$$\boxed{\,E_n^{(2)}=\sum_{m\neq n}
\frac{|\langle\psi_m^0|H'|\psi_n^0\rangle|^2}{E_n^0-E_m^0}\,}\qquad(\text{Eq. 7.15}).$$
(`second_order_energy`.) For the **ground state** every denominator is negative,
so $E_0^{(2)}\le0$: second order always pushes the ground state *down* — adjacent
levels "repel". This is checked in `test_second_order_energy_pushes_ground_state_down`.

### The test bed and the error scaling
We take $H^0=$ the harmonic oscillator ($E_n^0=n+\tfrac12$) and physically
meaningful perturbations built from $x=\tfrac{1}{\sqrt2}(a+a^\dagger)$:

- $H'=x$ (a uniform field — Griffiths Problem 7.6). By parity $E_n^{(1)}=0$, and
  the sum gives $E_n^{(2)}=-\tfrac12$ for **every** $n$. Completing the square,
  $H=\tfrac{p^2}{2}+\tfrac12(x+\lambda)^2-\tfrac12\lambda^2$, so exactly
  $E_n=(n+\tfrac12)-\tfrac12\lambda^2$ — through-second-order PT is **exact** here
  (`test_stark_perturbation_exact_through_second_order`).
- $H'=x^2$ (an anharmonic stiffening). Then $E_n^{(1)}=\langle n|x^2|n\rangle=
  n+\tfrac12$ and $E_n^{(2)}=-\tfrac12(n+\tfrac12)$ — both reproduced by the code.

The central honesty check is the **truncation-error scaling** vs exact
diagonalization of $\operatorname{diag}(E^0)+\lambda H'$:
$$E_n-\big(E_n^0+\lambda E_n^{(1)}\big)=O(\lambda^2),\qquad
E_n-\big(E_n^0+\lambda E_n^{(1)}+\lambda^2 E_n^{(2)}\big)=O(\lambda^3).$$
Halving $\lambda$ divides the first-order error by $\approx4$ and the
through-second-order error by $\approx8$ — exactly what the tests assert. *(A PT
series is generically an **asymptotic** series, ~MA-21: the first few terms are
superb even when the full series diverges; Griffiths Problem 7.4 builds a
two-level case where it converges only if $H'$ is small enough.)*

## 1b. Degenerate perturbation theory (Griffiths §7.2, printed p.366)

If $d$ states share an energy $E^0$, the formulae above divide by zero. The cure
(Griffiths §7.2.1, p.367): you do not know *which* linear combinations of the
degenerate states the perturbation will select — the "good" states. Write the
$O(\lambda)$ equation in the degenerate subspace and project onto each degenerate
basis state; you get a matrix eigenvalue problem for the **W matrix**
$$W_{ij}=\langle\psi_i^0|H'|\psi_j^0\rangle,\qquad
\boxed{\,\det\!\big(W-E^{(1)}\mathbb 1\big)=0\,}\qquad(\text{Eq. 7.30, p.370}).$$
**The first-order corrections are the eigenvalues of $H'$ restricted to the
degenerate subspace**, and the eigenvectors are the good states (Griffiths: *"the
eigenvalues of the matrix $W$ give the first-order corrections to the energy"*).
(`degenerate_first_order_split`.) The module verifies this against the exact
splitting $(E^{\text{exact}}-E^0)/\lambda$ as $\lambda\to0$, and shows the
**naive** diagonal answer $\{W_{00},W_{11}\}$ is *wrong* whenever the off-diagonal
$W_{01}\neq0$ — eigenvalue interlacing puts the true splittings outside the
diagonal entries (`test_naive_nondegenerate_answer_is_wrong`).

---

## 2. The variational principle (Griffiths Ch.8, printed p.417)

For **any** normalized trial state $\psi$,
$$\boxed{\,\langle H\rangle_\psi=\langle\psi|H|\psi\rangle\ \ge\ E_{gs}\,}\qquad(\text{Eq. 8.1, p.418}).$$
*Proof:* expand $\psi=\sum_n c_n\psi_n$ in the (unknown) eigenbasis; then
$\langle H\rangle=\sum_n|c_n|^2E_n\ge E_{gs}\sum_n|c_n|^2=E_{gs}$ since $E_{gs}$ is
the smallest eigenvalue. Equality iff $\psi=\psi_{gs}$. So **any** trial energy
overestimates the ground state — pick a family $\psi_b$ and **minimize** over the
parameter $b$ to squeeze the bound down (`variational_energy`,
`gaussian_variational_min`). We use the positive-definite kinetic form
$\langle T\rangle=\tfrac{\hbar^2}{2m}\!\int|\psi'|^2dx$ (integration by parts).

**Gaussian on the oscillator (Griffiths Example 8.1, p.418).** With
$\psi_b=(2b/\pi)^{1/4}e^{-bx^2}$,
$$\langle H\rangle(b)=\frac{\hbar^2 b}{2m}+\frac{m\omega^2}{8b}
\ \xrightarrow{\ \partial_b=0\ }\ b=\frac{m\omega}{2\hbar},\quad
\langle H\rangle_{\min}=\tfrac12\hbar\omega=E_0.$$
The bound is hit **exactly** — because the Gaussian family happens to *contain*
the true ground state (`test_variational_gaussian_recovers_oscillator_exactly`).

**Gaussian on the quartic $V=\tfrac14x^4$.** Now the family does *not* contain the
true state, so the minimized bound sits a few percent **above** $E_{gs}$
(obtained by exact finite-difference diagonalization): $0.4293\ge0.4208$. The
inequality holds at *every* $b$, not just the optimum
(`test_variational_is_an_upper_bound`) — that is the whole content of Eq. 8.1.

---

## 3. The WKB approximation (Griffiths Ch.9, printed p.449)

When $V(x)$ is nearly constant over a wavelength (the **semiclassical** regime),
seek $\psi=A(x)e^{i\phi(x)/\hbar}$ with slowly varying amplitude. Dropping the
$A''$ term (Griffiths §9.1, p.450–451) gives the WKB wave function
$$\boxed{\,\psi(x)\approx\frac{C}{\sqrt{p(x)}}\,
\exp\!\Big(\pm\frac{i}{\hbar}\!\int p(x)\,dx\Big)\,},\qquad
p(x)=\sqrt{2m\big(E-V(x)\big)}\quad(\text{Eq. 9.10}).$$
The amplitude $|\psi|^2\propto1/p$ says the particle is found where it moves
slowly — the classical probability (`classical_momentum`).

### Bound states — Bohr–Sommerfeld quantization
Between two **smooth** turning points the connection formulas (Griffiths §9.3,
p.460–465, via Airy patching) force the phase to fit, giving
$$\boxed{\,\int_{x_1}^{x_2}p(x)\,dx=\Big(n+\tfrac12\Big)\pi\hbar\,},\qquad n=0,1,2,\dots
\quad(\text{Eq. 9.50, p.465}).$$
Equivalently the **loop** integral $\oint p\,dx=2\!\int_{x_1}^{x_2}p\,dx=
(n+\tfrac12)\,2\pi\hbar=(n+\tfrac12)h$. The half-integer is *boundary data*: the
number subtracted from $n$ is $0$, $\tfrac14$, or $\tfrac12$ for two vertical
walls, one wall, or two smooth turns respectively (Griffiths p.465). The code
selects it with `gamma` (default $\tfrac12$). (`bohr_sommerfeld_energy`.)

- **Oscillator — exact.** $\int_{-x_0}^{x_0}\sqrt{2m(E-\tfrac12m\omega^2x^2)}\,dx
  =\pi E/\omega$, so $\pi E/\omega=(n+\tfrac12)\pi\hbar\Rightarrow
  E_n=(n+\tfrac12)\hbar\omega$ — **WKB nails the oscillator spectrum**
  (`test_wkb_recovers_oscillator_exactly`). The half-harmonic well likewise gives
  the exact odd levels (Griffiths Example 9.3).
- **Quartic $\tfrac14x^4$ — asymptotically exact.** Error $18\%$ at $n=0$ but
  $<1\%$ by $n=2$ and shrinking: WKB is a *large-$n$* (semiclassical) method
  (`test_wkb_quartic_improves_with_quantum_number`).
- **Linear "gravity" well $V=Fx$, wall at $0$ — one vertical wall ($\gamma=\tfrac34$).**
  The exact levels are set by zeros $a_n$ of the Airy function,
  $E_n=-a_n(\hbar^2F^2/2m)^{1/3}$; WKB agrees to $<1\%$ already at the ground
  state and improves with $n$ (Griffiths Problem 9.7;
  `test_wkb_linear_well_matches_airy`).

### Tunnelling
In the classically **forbidden** region $E<V$, $p$ is imaginary and the wave
decays. For a barrier the transmission is dominated by the exponential decay
across it (Griffiths §9.2, p.455–456):
$$\boxed{\,T\approx e^{-2\gamma},\qquad
\gamma=\frac1\hbar\int_{x_1}^{x_2}\big|p(x)\big|\,dx
=\frac1\hbar\int_{x_1}^{x_2}\sqrt{2m\big(V(x)-E\big)}\,dx\,}\quad(\text{Eq. 9.22–9.23}).$$
(`tunneling_probability`, `barrier_action`.) For a **rectangular** barrier
$|p|=\sqrt{2m(V_0-E)}\equiv\hbar\kappa$ is constant, so $\gamma=\kappa a$ and
$T_{\text{WKB}}=e^{-2\kappa a}$ (`tunneling_rectangular`). Comparing to **~QM-08**'s
*exact* $T=\big[1+\tfrac{V_0^2\sinh^2\kappa a}{4E(V_0-E)}\big]^{-1}$: for a thick
barrier $\sinh\kappa a\to\tfrac12e^{\kappa a}$, so
$$\frac{T_{\text{exact}}}{T_{\text{WKB}}}\to\frac{16\,E(V_0-E)}{V_0^2}=\text{const}.$$
The ratio is **independent of $a$** — WKB captures the entire exponent and misses
only the $O(1)$ prefactor (`test_wkb_tunneling_shares_exact_exponent`, which
imports QM-08's exact result). This same exponent powers Gamow's theory of alpha
decay (Griffiths Example 9.2).

---
### Where this sits in the network
**Bridge B1** (key, not yet built): WKB *is* the $\hbar\to0$ limit of quantum
mechanics, and Bohr–Sommerfeld $\oint p\,dx=(n+\tfrac12)h$ is exactly the
**action** of ~CM-21 (Hamilton–Jacobi / action–angle variables) quantized — the
cleanest bridge from classical to quantum. ~MA-21 (asymptotics) underwrites the
"PT series = asymptotic series" caveat. The oscillator test bed is ~QM-09; the
tunnelling cross-check imports ~QM-08. Forward: ~QM-16 lifts perturbation theory
to *time-dependent* $H'(t)$ (Fermi's golden rule), and ~QM-18 applies it to
scattering (the Born approximation).
