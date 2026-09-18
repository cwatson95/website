# QM-09 — The Quantum Harmonic Oscillator (notes)

The harmonic oscillator is the single most important exactly solvable system in
physics. Any smooth potential near a minimum is parabolic (expand $V$, drop the
constant, $V'(x_0)=0$, keep the quadratic term), so $V\approx\frac12 m\omega^2
x^2$ describes vibrating molecules, phonons in solids, the modes of the
electromagnetic field, and — promoted to a field — every free particle in QFT.
Griffiths 3e treats it in **§2.3 (printed p.57)**; the time-independent
Schrödinger equation (TISE) to solve is
$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2}+\frac12 m\omega^2 x^2\,\psi=E\,\psi.$$
There are **two standard routes**, and this module builds both and proves they
agree.

> **Units.** The code uses natural oscillator units $\hbar=m=\omega=1$: energies
> in units of $\hbar\omega$, lengths in $\sqrt{\hbar/m\omega}$. Then $\xi=x$ and
> $E_n=n+\tfrac12$. The formulas below keep the constants explicit.

## 1. Algebraic method — ladder operators (Griffiths §2.3.1, p.59)

Write $H=\frac{1}{2m}\big(p^2+(m\omega x)^2\big)$. With numbers this would factor
as a product; with operators $x,p$ it almost does. Define the dimensionless
**ladder operators**
$$\boxed{\,a=\sqrt{\tfrac{m\omega}{2\hbar}}\Big(x+\tfrac{i}{m\omega}p\Big),\qquad
a^\dagger=\sqrt{\tfrac{m\omega}{2\hbar}}\Big(x-\tfrac{i}{m\omega}p\Big)\,}$$
($a$ = lowering/annihilation, $a^\dagger$ = raising/creation). Everything hangs
off the **canonical commutation relation** $[x,p]=i\hbar$ (Griffiths Eq. 2.51,
p.60 — "this lovely and ubiquitous formula"). A short computation gives
$$\boxed{\,[a,a^\dagger]=1\,},\qquad
H=\hbar\omega\Big(a^\dagger a+\tfrac12\Big)=\hbar\omega\Big(N+\tfrac12\Big),$$
where $N\equiv a^\dagger a$ is the **number operator**. Because
$[N,a^\dagger]=a^\dagger$ and $[N,a]=-a$, if $N|n\rangle=n|n\rangle$ then
$a^\dagger|n\rangle$ has eigenvalue $n+1$ and $a|n\rangle$ has eigenvalue $n-1$
(Griffiths p.61: the operators raise/lower the energy by $\hbar\omega$). The
ladder must terminate below (energies can't go negative), so there is a **lowest
rung** with
$$a|0\rangle=0\quad\Rightarrow\quad E_0=\tfrac12\hbar\omega\ \text{(Griffiths p.62)}.$$
Applying $a^\dagger$ repeatedly and tracking the norms (the adjoint trick on
p.63–64) gives the normalized ladder relations
$$\boxed{\,a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle,\qquad
a|n\rangle=\sqrt{n}\,|n-1\rangle\,}\quad(\text{Griffiths Eq. 2.66},\ \text{p.64}),$$
and hence the spectrum with its **zero-point energy** $\tfrac12\hbar\omega$:
$$\boxed{\,E_n=\hbar\omega\Big(n+\tfrac12\Big),\qquad n=0,1,2,\dots\,}\quad(\text{Griffiths Eq. 2.62, p.62}).$$
The zero-point energy is forced by $[x,p]\neq0$: the oscillator cannot sit at the
bottom of the well with $x=p=0$ (that would violate uncertainty). This is the
$\sim$QM-05 commutator machinery in its cleanest application.

### Realising the algebra as matrices, and the truncation artifact
In the number basis $\{|0\rangle,|1\rangle,\dots\}$ the lowering operator has
matrix elements $\langle m|a|n\rangle=\sqrt{n}\,\delta_{m,n-1}$ — one
superdiagonal $\sqrt1,\sqrt2,\dots$. The code (`annihilation`, `creation`) builds
these in a basis **truncated** to $D$ levels. Two honest consequences:

- $N=a^\dagger a=\operatorname{diag}(0,1,\dots,D-1)$ is **exact** — lowering never
  needs the rung above the top.
- $[a,a^\dagger]=1$ **cannot** hold for finite matrices: $\operatorname{tr}[A,B]=
  \operatorname{tr}(AB)-\operatorname{tr}(BA)=0$ for any $A,B$, whereas
  $\operatorname{tr}\mathbb 1=D\neq0$. Truncation dumps the entire defect into one
  corner: $[a,a^\dagger]=\operatorname{diag}(1,1,\dots,1,-(D-1))$. The interior is
  the identity; the bottom-right entry is $-(D-1)$ (because $a^\dagger|D-1\rangle$
  falls off the top of the kept space). The tests assert *exactly this* rather
  than hiding it — see `test_truncation_artifact_is_honest`.

## 2. Analytic method — Hermite–Gaussians (Griffiths §2.3.2, p.67)

Solve the TISE directly. Introduce the dimensionless coordinate
$\xi=\sqrt{m\omega/\hbar}\,x$ and $K=2E/\hbar\omega$; the equation becomes
$\frac{d^2\psi}{d\xi^2}=(\xi^2-K)\psi$ (Griffiths Eq. 2.73, p.67). The
large-$\xi$ behavior is $e^{-\xi^2/2}$, so **peel it off**: $\psi=h(\xi)\,
e^{-\xi^2/2}$. Then $h$ obeys $h''-2\xi h'+(K-1)h=0$, solved by a power series
whose coefficients satisfy the recursion
$$a_{j+2}=\frac{2j+1-K}{(j+1)(j+2)}\,a_j\quad(\text{Griffiths Eq. 2.82, p.68}).$$
For a **normalizable** state the series must **terminate** (otherwise $h\sim
e^{\xi^2}$ and $\psi$ blows up): some $a_{n+2}=0$ with $2n+1-K=0$, i.e.
$$K=2n+1\ \Longrightarrow\ E_n=\hbar\omega\Big(n+\tfrac12\Big)\quad(\text{Griffiths p.69}).$$
**Quantization re-emerges**, by a completely different mechanism, identical to the
algebraic result. The terminating polynomials are (up to normalization) the
physicists' **Hermite polynomials** $H_n(\xi)$ (Table 2.1, p.71;
$H_0=1,\ H_1=2\xi,\ H_2=4\xi^2-2,\dots$, satisfying $H_{n+1}=2\xi H_n-2nH_{n-1}$).
The normalized eigenfunctions are
$$\boxed{\,\psi_n(x)=\Big(\frac{m\omega}{\pi\hbar}\Big)^{1/4}
\frac{1}{\sqrt{2^n\,n!}}\;H_n(\xi)\,e^{-\xi^2/2},\qquad \xi=\sqrt{\tfrac{m\omega}{\hbar}}\,x\,}$$
(Griffiths Eq. 2.85, p.71). Griffiths notes these are "identical, of course, to
the ones we obtained algebraically." Their key properties, all checked in code:

- **Orthonormality** $\int\psi_m\psi_n\,dx=\delta_{mn}$ (Griffiths Eq. 2.67,
  p.64) — verified to machine precision by `overlap`/Simpson.
- **Parity** $(-1)^n$: even $n$ symmetric, odd $n$ antisymmetric (so $\psi_n(0)=0$
  for odd $n$).
- Each $\psi_n$ solves the **discretized** TISE: sampling $\psi_n$ on a grid and
  applying the finite-difference Hamiltonian returns $E_n\psi_n$ (relative
  residual $\sim10^{-4}$, shrinking with the step) — `fd_residual`.

The module **imports $H_n$ from $\sim$MA-12** (`special_functions.hermite`),
demonstrating the curriculum edge; `numpy.polynomial.hermite` is an equivalent
drop-in.

## 3. The two methods give the same spectrum

`algebraic_spectrum(D)` diagonalises the matrix $H=\hbar\omega(N+\tfrac12)$ and
returns $E_n=\hbar\omega(n+\tfrac12)$ **exactly**. `fd_spectrum` diagonalises the
finite-difference Hamiltonian — built with no reference to ladder operators — and
returns the same numbers (to $\sim10^{-3}$, converging as the grid refines).
`test_two_methods_same_spectrum` asserts both equal $\hbar\omega(n+\tfrac12)$ and
each other. One physical spectrum, two independent derivations.

---
### Where this sits in the network (bridge B6)
$\sim$CM-15 (classical SHM, $\ddot x=-\omega^2 x$) $\to$ **QM-09 (quantum SHO)**
$\to$ $\sim$QF-01 (a free field is infinitely many decoupled oscillators, one per
mode; the $a,a^\dagger$ here become the field's particle creation/annihilation
operators). The Poisson-bracket$\to$commutator edge ($\sim$CM-20$\to\sim$QM-05,
$\{x,p\}=1\to[x,p]=i\hbar$) is exactly what powers the algebraic method. CM-15
and QF-01 are forward references — the bridge connects when they land; nothing
here imports them.
