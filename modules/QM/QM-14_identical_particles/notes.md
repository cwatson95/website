# QM-14 — Identical Particles (notes)

Classical particles are always distinguishable in principle — paint one red, the
other blue. Quantum particles of the same kind are **not**: there is no
experiment, not even God's, that tells you *which* electron is *which*
(Griffiths 3e §5.1.1, p.256). This single fact — indistinguishability —
forces a restriction on the allowed states (the **symmetrization postulate**)
from which the Pauli exclusion principle, the periodic table, and the strange
"exchange force" all follow. Everything below is verified numerically in
`code/identical.py`.

## 1. Two-particle systems and the product state

The state of two particles is a function of *both* sets of coordinates,
$\Psi(\mathbf r_1,\mathbf r_2,t)$, evolving under the two-body Schrödinger
equation with $H=-\tfrac{\hbar^2}{2m_1}\nabla_1^2-\tfrac{\hbar^2}{2m_2}\nabla_2^2+V$
(Griffiths §5.1, p.252). For **noninteracting** particles, with particle 1 in
one-particle state $\psi_a$ and particle 2 in $\psi_b$, separation of variables
gives the **product state**

$$\Psi(\mathbf r_1,\mathbf r_2)=\psi_a(\mathbf r_1)\,\psi_b(\mathbf r_2).$$

In the module's discrete language a one-particle state is a vector
$|a\rangle\in\mathbb C^d$ and the product is the **tensor product**
$|a\rangle\otimes|b\rangle$ (`tensor`), an element of $\mathbb C^d\otimes\mathbb
C^d$. A general two-particle state need not factor — those that don't are
**entangled** (Schrödinger's term, Griffiths p.253). The whole chapter is about
*which* of these states Nature actually allows for *identical* particles.

## 2. The symmetrization postulate: bosons and fermions

If the particles are identical the labels "1" and "2" are physically
meaningless, so the wave function must be *noncommittal* about which particle is
in which state. Define the **exchange operator** $P_{12}$ that swaps the two
particles (Griffiths §5.1.4, Eq. 5.30, p.264):

$$P_{12}\,f(\mathbf r_1,\mathbf r_2)=f(\mathbf r_2,\mathbf r_1),\qquad P_{12}^2=\mathbb 1.$$

Because $P_{12}^2=\mathbb 1$, its only eigenvalues are $\pm1$ (`swap_operator`,
`test_swap_operator_involution_and_eigenvalues`). Since identical particles must
be treated identically, $[H,P_{12}]=0$: exchange parity is conserved. The
**symmetrization postulate** is the axiom that identical-particle states are not
merely *allowed* but *required* to be eigenstates of $P_{12}$:

$$\boxed{\,P_{12}\,\Psi=\pm\,\Psi\,}\qquad
\begin{cases}+\ \text{(symmetric)} &\textbf{bosons}\\[2pt]
-\ \text{(antisymmetric)} &\textbf{fermions.}\end{cases}$$

The two ways to build such a state from $\psi_a,\psi_b$ are (Griffiths Eq. 5.17,
p.256)

$$\Psi_\pm(\mathbf r_1,\mathbf r_2)=A\big[\psi_a(\mathbf r_1)\psi_b(\mathbf r_2)\pm\psi_b(\mathbf r_1)\psi_a(\mathbf r_2)\big],$$

i.e. `symmetrize` ($+$) and `antisymmetrize` ($-$). For orthonormal orbitals
$A=1/\sqrt2$; for non-orthogonal but normalized orbitals with overlap
$s=\langle a|b\rangle$ the norm of the unnormalized sum is
$\sqrt{2(1\pm|s|^2)}$ (`test_general_normalization_nonorthogonal`). Whether a
species is a boson or a fermion is fixed by its spin — the **spin–statistics
connection**: integer spin $\Rightarrow$ boson, half-integer spin
$\Rightarrow$ fermion. This is a theorem of *relativistic* QFT (`~QF-01`); in
nonrelativistic QM it is taken as an axiom (Griffiths p.256).

## 3. The Pauli exclusion principle

Put two identical **fermions** in the *same* one-particle state, $\psi_a=\psi_b$.
The antisymmetric combination collapses:

$$\Psi_-=A\big[\psi_a(\mathbf r_1)\psi_a(\mathbf r_2)-\psi_a(\mathbf r_1)\psi_a(\mathbf r_2)\big]=0.$$

"We are left with no wave function at all" (Griffiths p.256). This is the
**Pauli exclusion principle**: *no two identical fermions can occupy the same
state* (`antisymmetrize(a,a)` returns the zero vector,
`test_pauli_exclusion_two_identical_orbitals`). It is **not** an ad-hoc rule for
electrons — it is a corollary of antisymmetry, applying to *all* identical
fermions. Bosons have no such restriction: $\Psi_+=A\cdot2\,\psi_a\psi_a\neq0$,
so any number of bosons may pile into one state
(`test_bosons_may_share_a_state`) — the seed of Bose–Einstein condensation
(`~SM-04`).

## 4. The Slater determinant — $N$ fermions

For $N$ fermions in orthonormal orbitals $\phi_1,\dots,\phi_N$ the totally
antisymmetric state is the **Slater determinant** (Griffiths Problem 5.8, p.262;
"this device works for any number of particles"):

$$\Psi(\mathbf r_1,\dots,\mathbf r_N)=\frac{1}{\sqrt{N!}}
\begin{vmatrix}
\phi_1(\mathbf r_1) & \phi_1(\mathbf r_2) & \cdots & \phi_1(\mathbf r_N)\\
\phi_2(\mathbf r_1) & \phi_2(\mathbf r_2) & \cdots & \phi_2(\mathbf r_N)\\
\vdots & \vdots & \ddots & \vdots\\
\phi_N(\mathbf r_1) & \phi_N(\mathbf r_2) & \cdots & \phi_N(\mathbf r_N)
\end{vmatrix}
=\frac{1}{\sqrt{N!}}\sum_{\sigma\in S_N}\mathrm{sgn}(\sigma)\,
|\phi_{\sigma(1)}\rangle\otimes\cdots\otimes|\phi_{\sigma(N)}\rangle.$$

The determinant makes the three key facts automatic, each tested in
`code/identical.py` (`slater_determinant`):

- **Antisymmetry.** Swapping two *particles* swaps two *columns* of the
  determinant, flipping its sign: $P_{pq}\Psi=-\Psi$ for any pair — checked for
  $N=3,4$ and non-adjacent pairs in `test_slater_antisymmetric_under_any_pair_swap`.
- **Pauli for $N$ fermions.** Two equal *orbitals* are two equal *rows*, so the
  determinant vanishes (`test_slater_vanishes_if_two_orbitals_coincide`).
- **Normalization.** For orthonormal orbitals the raw antisymmetric sum has norm
  exactly $\sqrt{N!}$, so the $1/\sqrt{N!}$ prefactor makes $\Psi$ a unit vector
  (`test_slater_normalization_is_sqrt_N_factorial`).

## 5. Exchange forces — why fermions avoid and bosons bunch

Symmetrization has a measurable consequence even with **no interaction at all**.
Take two particles in orthonormal 1-D orbitals $\psi_a,\psi_b$ and compute the
mean-square separation $\langle(x_1-x_2)^2\rangle=\langle x_1^2\rangle+\langle
x_2^2\rangle-2\langle x_1x_2\rangle$ (Griffiths §5.1.2, p.259). For
**distinguishable** particles (Eq. 5.23),

$$\langle(x_1-x_2)^2\rangle_{\text{dist}}=\langle x^2\rangle_a+\langle x^2\rangle_b-2\langle x\rangle_a\langle x\rangle_b.$$

For **identical** particles the symmetric/antisymmetric cross-terms add one
extra piece (Eq. 5.25), built from the **off-diagonal matrix element** (Eq. 5.24)

$$\langle x\rangle_{ab}=\int x\,\psi_a(x)^{*}\psi_b(x)\,dx,$$

namely

$$\boxed{\,\langle(x_1-x_2)^2\rangle_\pm=\langle(x_1-x_2)^2\rangle_{\text{dist}}\mp 2\,|\langle x\rangle_{ab}|^2\,}$$

with the **upper sign for bosons** and the **lower sign for fermions** (Eq. 5.26;
`exchange_dx2`). Reading it off:

- **Bosons** ($-$): closer together than distinguishable particles — they
  *bunch*.
- **Fermions** ($+$): farther apart — they effectively *repel*.

So $\langle(x_1-x_2)^2\rangle_{\text{boson}}<\langle(x_1-x_2)^2\rangle_{\text{dist}}<\langle(x_1-x_2)^2\rangle_{\text{fermion}}$
(`test_exchange_force_ordering_infinite_well`). It is **not a real force** — no
agency pushes on the particles; it is a purely geometric consequence of
symmetrization, with no classical analogue (Griffiths p.261). Two independent
closed forms confirm the code:

- **Infinite well, $n=1,2$, width $L=1$** (Griffiths Problem 5.6):
  $\langle x\rangle_{12}=-\tfrac{16}{9\pi^2}$, distinguishable
  $\langle(\Delta x)^2\rangle=\tfrac16-\tfrac{5}{8\pi^2}\approx0.1033$, exchange
  term $2|\langle x\rangle_{12}|^2=\tfrac{512}{81\pi^4}\approx0.0649$
  (`test_exchange_force_infinite_well_closed_form`).
- **Harmonic oscillator, ground + first excited** (Griffiths Problem 5.7, natural
  units): distinguishable $=2$, boson $=1$, fermion $=3$ (in units $\hbar/m\omega$);
  $|\langle x\rangle_{01}|=1/\sqrt2$
  (`test_exchange_force_harmonic_oscillator_closed_form`).

Crucially $\langle x\rangle_{ab}$ — and hence the whole effect — **vanishes
unless the orbitals overlap.** An electron in Chicago and an electron in Seattle
can be treated as distinguishable: it makes no difference whether you
antisymmetrize (Griffiths p.260, `test_no_exchange_force_without_overlap`). This
is the only thing that lets chemists discuss one atom at a time.

## 6. Spin, the helium atom, and the periodic table

The exchange parity applies to the **whole** state, *position $\times$ spin*
(Griffiths §5.1.3, p.263). For two electrons (fermions) the total must be
antisymmetric, so

$$\underbrace{(\text{spatial})}_{\text{sym}}\times\underbrace{(\text{spin})}_{\text{antisym=singlet}}\quad\text{or}\quad\underbrace{(\text{spatial})}_{\text{antisym}}\times\underbrace{(\text{spin})}_{\text{sym=triplet}}.$$

The two-spin **singlet** $\tfrac{1}{\sqrt2}(|\!\uparrow\downarrow\rangle-|\!\downarrow\uparrow\rangle)$
is antisymmetric ($P_{12}=-1$); the three **triplet** states are symmetric
($P_{12}=+1$) — verified in `test_spin_singlet_antisymmetric_triplet_symmetric`.
**Helium's ground state** ($1s^2$) puts both electrons in the *same* spatial $1s$
orbital, a symmetric spatial state, so the spins are *forced* into the
antisymmetric singlet — "both spin up" is forbidden, exactly the zero vector of
the Pauli principle (`test_helium_ground_state_requires_singlet`). The product of
the spatial ($+1$) and spin ($-1$) exchange eigenvalues is $-1$: the full state
is antisymmetric, as required.

Generalize this with the Slater determinant and you get the **Aufbau** filling of
hydrogenic orbitals $(n,\ell,m_\ell,m_s)$: at most two electrons per spatial
orbital (one spin up, one down), shells filling in order — the structure of the
**periodic table** (Griffiths §5.2, p.267; the carbon ground state and Hund's
rules, p.272). The detailed multi-electron atom is `~QM-12`.

---
### Where this sits in the trunk
The exchange operator $P_{12}$ is just a Hermitian/unitary operator from the
`~QM-05` formalism, and the $\pm1$ outcome is a `~QM-06` measurement of exchange
parity. The bosonic/fermionic *counting* this enables — how many particles can
share a level, hence the occupation statistics — becomes **Bose–Einstein** and
**Fermi–Dirac** statistics in `~SM-04` (quantum statistics; *not yet built —
the bridge connects when it lands*). The application to real atoms is `~QM-12`.
