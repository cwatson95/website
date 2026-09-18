# QF-01 — Canonical Field Quantization (notes)

Quantum mechanics quantizes a particle: position and momentum become operators
with $[x,p]=i\hbar$ (`~QM-05`). **Quantum field theory** quantizes a *field* — a
dynamical variable $\phi(\mathbf x,t)$ at every point of space — by the same recipe:
promote the field and its canonical momentum to operators with an equal-time
commutator. The payoff is enormous. Fourier-expanded, a free field falls apart
into **infinitely many independent harmonic oscillators**, one per momentum mode
(**KEY BRIDGE B6**: `~CM-15` → `~CM-16` → `~QM-09` → here). The quanta of those
oscillators *are the particles*; creating and destroying them is **second
quantization**, and the leftover zero-point energy of all those oscillators is the
(divergent) energy of the vacuum.

Citation key (full details + granularity in `refs.md`): **PS** = Peskin &
Schroeder, *An Introduction to QFT* (Ch. 2 scalar, Ch. 3 Dirac); **Zee** = Zee,
*QFT in a Nutshell*; **Wbg** = Weinberg, *Quantum Theory of Fields, Vol. 1*. Cited
at **section/chapter level**. Natural units $\hbar=c=1$ unless shown.

## 1. From the Lagrangian to the canonical commutator

Start from a classical field with a Lagrangian *density*. The free real scalar
(Klein–Gordon) field is [PS §2.2]
$$\mathcal L=\tfrac12(\partial_\mu\phi)(\partial^\mu\phi)-\tfrac12 m^2\phi^2
=\tfrac12\dot\phi^2-\tfrac12(\nabla\phi)^2-\tfrac12 m^2\phi^2 .$$
The **canonical momentum** conjugate to $\phi$ is $\pi=\partial\mathcal L/
\partial(\partial_0\phi)=\dot\phi$, exactly as $p=\partial L/\partial\dot q$ in
`~CM-19`. The Euler–Lagrange equation gives the **Klein–Gordon equation**
$(\partial_\mu\partial^\mu+m^2)\phi=(\Box+m^2)\phi=0$ (`~QM-22`). Quantization
then promotes $\phi,\pi$ to operators and imposes the **equal-time canonical
commutator** [PS §2.2] — the field analogue of $[x,p]=i\hbar$ (bridge **B7**):
$$[\phi(\mathbf x,t),\pi(\mathbf y,t)]=i\hbar\,\delta^3(\mathbf x-\mathbf y),
\qquad [\phi,\phi]=[\pi,\pi]=0 .$$
The Dirac delta $\delta^3(\mathbf x-\mathbf y)$ is the continuum version of the
Kronecker $\delta_{ij}$ that couples a particle's coordinate only to *its own*
momentum: different points of space are independent degrees of freedom.

## 2. The Klein–Gordon field: dispersion and mode expansion

Fourier transform in space. Each mode amplitude $\phi_{\mathbf p}(t)$ obeys
$\ddot\phi_{\mathbf p}=-\omega_{\mathbf p}^2\,\phi_{\mathbf p}$ — a harmonic
oscillator — with frequency set by the **Klein–Gordon dispersion relation**
$$\omega_{\mathbf p}=\frac{\sqrt{\mathbf p^2c^2+m^2c^4}}{\hbar}
\;=\;\sqrt{\mathbf p^2+m^2}\ \ (\hbar=c=1),\qquad
m=0:\ \ \omega_{\mathbf p}=|\mathbf p| .$$
This is the relativistic energy–momentum relation $E^2=p^2c^2+m^2c^4$ read as a
frequency (`~RE-06`); massless fields give $\omega=|\mathbf p|$, the light cone.
Code: `kg_dispersion(p, m)`. Expanding the field operator in these modes [PS §2.3]:
$$\phi(\mathbf x)=\int\!\frac{d^3p}{(2\pi)^3}\,\frac{1}{\sqrt{2\omega_{\mathbf p}}}
\Big(a_{\mathbf p}\,e^{i\mathbf p\cdot\mathbf x}
+a_{\mathbf p}^\dagger\,e^{-i\mathbf p\cdot\mathbf x}\Big),$$
and the canonical commutator of §1 becomes the **ladder algebra** of the modes,
$$[a_{\mathbf p},a_{\mathbf q}^\dagger]=(2\pi)^3\,\delta^3(\mathbf p-\mathbf q),
\qquad [a_{\mathbf p},a_{\mathbf q}]=[a_{\mathbf p}^\dagger,a_{\mathbf q}^\dagger]=0 .$$
This is the single oscillator's $[a,a^\dagger]=1$ (`~QM-09`), now one copy per
momentum $\mathbf p$. Code: `annihilation`, `creation`, `commutator`.

## 3. A field is infinitely many oscillators — KEY BRIDGE B6

Substituting the expansion into $H=\int d^3x\,\big(\tfrac12\pi^2+\tfrac12(\nabla\phi)^2
+\tfrac12 m^2\phi^2\big)$ gives [PS §2.3]
$$H=\int\!\frac{d^3p}{(2\pi)^3}\,\omega_{\mathbf p}
\Big(a_{\mathbf p}^\dagger a_{\mathbf p}+\tfrac12[a_{\mathbf p},a_{\mathbf p}^\dagger]\Big).$$
The Hamiltonian is a **sum of independent oscillators**, one for each mode
$\mathbf p$, with $N_{\mathbf p}=a_{\mathbf p}^\dagger a_{\mathbf p}$ its number
operator. Every mode therefore carries the oscillator spectrum of `~QM-09`,
$$E_{n_{\mathbf p}}=\Big(n_{\mathbf p}+\tfrac12\Big)\hbar\omega_{\mathbf p},
\qquad n_{\mathbf p}=0,1,2,\dots$$
This is the whole bridge **B6** in one line: a classical normal mode (`~CM-16`)
is, quantum mechanically, a harmonic oscillator (`~QM-09`); a *field* is a
continuum of them. Code reproduces a single mode exactly: `number(D)` is
$\mathrm{diag}(0,1,\dots)$, `single_mode_spectrum(D,omega)` returns
$\omega(n+\tfrac12)$, and `mode_energy(p, m, n)` evaluates
$(n+\tfrac12)\omega_{\mathbf p}$.

## 4. Fock space and second quantization

Read the rungs as **particles**. The vacuum has no quanta; one $a^\dagger$ makes a
one-particle state; the integer $n_{\mathbf p}$ becomes the number of particles of
momentum $\mathbf p$ [PS §2.3]:
$$\begin{aligned}
a_{\mathbf p}\,|0\rangle&=0,\qquad
|\mathbf p\rangle=\sqrt{2\omega_{\mathbf p}}\;a_{\mathbf p}^\dagger|0\rangle,\\
H\,|\mathbf p\rangle&=\omega_{\mathbf p}\,|\mathbf p\rangle,\qquad
\mathbf P=\int\!\frac{d^3p}{(2\pi)^3}\,\mathbf p\,a_{\mathbf p}^\dagger a_{\mathbf p}.
\end{aligned}$$
Because the $a_{\mathbf p}^\dagger$ commute, multi-particle states are automatically
**symmetric** — the quanta of a scalar field are identical **bosons** (`~QM-14`),
with the right relativistic energy $\omega_{\mathbf p}$ and momentum $\mathbf p$.
This is **second quantization**: the classical field amplitude has become an
operator that *creates and destroys particles*, so particle number is no longer
fixed (pair creation, decays). The whole tower $\{|0\rangle,a^\dagger|0\rangle,
a^\dagger a^\dagger|0\rangle,\dots\}$ is **Fock space**. Code: `creation`,
`annihilation`, `number`.

## 5. The vacuum energy and its ultraviolet divergence

The $\tfrac12[a,a^\dagger]$ in $H$ does not vanish: every mode contributes a
**zero-point energy** $\tfrac12\hbar\omega_{\mathbf p}$ even when empty. Summed over
the infinitely many modes this is the **vacuum energy**
$$E_0=\langle 0|H|0\rangle=\tfrac12\sum_{\mathbf p}\hbar\omega_{\mathbf p}
=\frac{V}{2}\!\int\!\frac{d^3p}{(2\pi)^3}\,\omega_{\mathbf p}\;\longrightarrow\;\infty,$$
which **diverges in the ultraviolet** ($\omega_{\mathbf p}\sim|\mathbf p|$ for large
$p$, so the integrand $\sim p^3\,dp$). Put the field in a box and cut the sum off
at $|\mathbf p|\le\Lambda$: $E_0$ is then **finite for any finite cutoff but grows
like $\Lambda^4$**. Code `vacuum_energy(m, cutoff)` sums $\tfrac12\omega_{\mathbf p}$
over the discrete box modes (`field_modes`) and shows exactly this growth —
doubling $\Lambda$ multiplies $E_0$ by $\approx 2^4=16$. Two lessons: (i) only
energy *differences* are physical, so we **normal-order** $H$ (drop the $\tfrac12$),
setting $\langle 0|{:}H{:}|0\rangle=0$; (ii) the cutoff-independent *remainder* left
when boundaries are present is the measurable **Casimir energy**. Taming this
divergence systematically is **renormalization** (`~QF-04`).

## 6. Spin and statistics: the Dirac field anticommutes

Repeat the recipe for the spin-$\tfrac12$ Dirac field and a disaster appears:
quantizing with **commutators** gives a Hamiltonian unbounded below (negative-energy
modes you could fall down forever). The cure is to quantize with **anticommutators**
[PS §3.5]:
$$\{b^{\,s}_{\mathbf p},\,b^{\,r\dagger}_{\mathbf q}\}=(2\pi)^3\,\delta^3(\mathbf p-\mathbf q)\,\delta^{rs},
\qquad (b^{\,s\dagger}_{\mathbf p})^2=0 .$$
The last identity *is* the **Pauli exclusion principle** — you cannot put two
identical fermions in the same mode (`~QM-14`). This is the **spin–statistics
connection**: integer-spin fields are quantized with commutators (bosons,
symmetric states), half-integer-spin fields with anticommutators (fermions,
antisymmetric states). Code demonstrates one fermionic mode:
`fermion_annihilation()` gives a $2\times2$ $b$ with `anticommutator(b, b†)`$=\mathbb 1$
and $b^{\dagger2}=0$, its number operator having eigenvalues only $0$ or $1$.

## 7. The electromagnetic field: gauge constraints

The photon field $A_\mu$ adds one more wrinkle. Its time component has **no
conjugate momentum**, $\pi^0=\partial\mathcal L/\partial\dot A_0=0$ — a
*constraint*, the signature of **gauge redundancy** $A_\mu\to A_\mu+\partial_\mu\lambda$
(`~EM-09`). Naively imposing $[A_\mu,\pi^\nu]=i\delta^\nu_\mu\delta^3$ is
inconsistent; one must **fix a gauge** (Coulomb or Lorenz) first. After gauge
fixing only the **two transverse polarizations** survive, and each is quantized
just like the scalar field — a mode expansion in $a^\lambda_{\mathbf p}$,
$a^{\lambda\dagger}_{\mathbf p}$ with $\omega_{\mathbf p}=|\mathbf p|$ (massless),
$\lambda=1,2$. The result is the quantized radiation field of quantum optics
(`~QO-01`); the systematic treatment of gauge constraints is `~QF-03`.

## Where this goes

- `~QM-09` (the single quantum oscillator) and `~CM-16` (classical normal modes) —
  *what each field mode is*; this module is the top of **bridge B6**.
- `~QM-22` (Klein–Gordon & Dirac equations) — the classical field equations being
  quantized here; `~QM-19` (path integrals) — the alternative quantization route.
- `~QM-14` (identical particles, Pauli exclusion) — the spin–statistics payoff of §6.
- `~QF-02` (interactions & Feynman diagrams), `~QF-03` (gauge theories / QED,
  `~EM-09`), `~QF-04` (renormalization — taming the §5 vacuum divergence).
- `~QF-05` (QFT in curved spacetime — Hawking & Unruh) — where the very notion of
  "vacuum" and "particle" becomes observer-dependent; the user's Quantum_Optics
  curved-spacetime work builds on exactly the $a_{\mathbf p},a_{\mathbf p}^\dagger$
  machinery quantized here.
