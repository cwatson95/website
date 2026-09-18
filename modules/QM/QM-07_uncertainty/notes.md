# QM-07 — Uncertainty principle & Ehrenfest's theorem (notes)

Two theorems sit at the heart of how quantum mechanics differs from, and yet
recovers, classical mechanics. The **uncertainty principle** says non-commuting
observables cannot both be sharp; **Ehrenfest's theorem** says that despite this
fuzziness the *averages* obey the classical equations of motion. They are linked
by the commutator: the same $[\hat A,\hat B]$ that bounds the spread also drives
the time evolution.

Natural units throughout the code: $\hbar=m=1$. Formulae below keep $\hbar$ and
$m$ explicit; set them to 1 to compare with `code/uncertainty.py`.

## 1. The position–momentum uncertainty principle

A wave that is sharply localized in space must be built from a broad band of
wavelengths, and vice versa — there is "an inescapable trade-off … the more
precise a wave's position is, the less precise is its wavelength" (Griffiths 3e
§1.6, p.35). Through de Broglie $p=h/\lambda=\hbar k$, a spread in wavelength *is*
a spread in momentum, so
$$\boxed{\;\sigma_x\,\sigma_p\ \ge\ \frac{\hbar}{2}\;}$$
This is not a statement about clumsy measurement; it is a property of the
*state*. $x$ and $p$ are **conjugate Fourier variables** ($\tilde\psi(p)$ is the
Fourier transform of $\psi(x)$ — see `~MA-09`), and the inequality is the
quantum reading of the general Fourier bandwidth theorem (`code`: `sigma_x`,
`sigma_p` compute $\sigma_x,\sigma_p$ on a grid, $\hat p=-i\hbar\,d/dx$ applied
spectrally via the FFT).

## 2. The generalized (Robertson) uncertainty principle

The $\hbar/2$ above is one instance of a theorem for *any* two Hermitian
observables (Griffiths 3e §3.5.1, p.138, "Proof of the Generalized Uncertainty
Principle"):
$$\boxed{\;\sigma_A\,\sigma_B\ \ge\ \left|\frac{1}{2i}\langle[\hat A,\hat B]\rangle\right|
=\tfrac12\bigl|\langle[\hat A,\hat B]\rangle\bigr|\;}$$

The argument is "beautiful but rather abstract" (Griffiths p.137). It rests on
one lemma — the **Schwarz inequality** — so we derive that first, every step,
and then walk the uncertainty proof itself in full.

### 2.1 Every step of the Schwarz inequality

The lemma (Griffiths 3e Eq. 3.7, p.120; restated for abstract vectors as
Eq. A.27, p.594):
$$\langle f|f\rangle\,\langle g|g\rangle\ \ge\ |\langle f|g\rangle|^2 .$$
Griffiths relegates the proof to Problem A.5 (p.594), whose hint contains the
whole idea: *subtract from $|g\rangle$ its projection along $|f\rangle$ and use
$\langle h|h\rangle\ge0$*. Here is that proof, step by step.

**Step 1 — the axioms used.** Only three properties of the inner product enter
(Griffiths §3.1, p.120): (i) $\langle h|h\rangle\ge0$ for every vector, with
$\langle h|h\rangle=0$ only for $h=0$; (ii) conjugate symmetry
$\langle g|f\rangle=\langle f|g\rangle^*$ (Eq. 3.8); (iii) linearity in the
*second* slot — hence antilinearity in the first,
$\langle cf|g\rangle=c^*\langle f|g\rangle$.

**Step 2 — dispose of the trivial case.** If $\langle f|f\rangle=0$ then $f=0$
by (i), so $\langle f|g\rangle=0$ and both sides vanish: the inequality holds
as $0\ge0$. Assume from now on $\langle f|f\rangle>0$.

**Step 3 — subtract the projection.** Define
$$|h\rangle=|g\rangle-\frac{\langle f|g\rangle}{\langle f|f\rangle}\,|f\rangle$$
— $g$ minus its component along $f$ (the same move that drives Gram–Schmidt,
Griffiths Problem A.4). It is orthogonal to $f$ by construction:
$$\langle f|h\rangle=\langle f|g\rangle-\frac{\langle f|g\rangle}{\langle f|f\rangle}\langle f|f\rangle=0 .$$

**Step 4 — expand $\langle h|h\rangle\ge0$.** Write $c=\langle f|g\rangle/\langle f|f\rangle$,
so $|h\rangle=|g\rangle-c|f\rangle$. Using antilinearity in the first slot and
linearity in the second,
$$\langle h|h\rangle=\langle g|g\rangle-c\,\langle g|f\rangle-c^*\langle f|g\rangle+|c|^2\langle f|f\rangle .$$
Each of the last three terms is the *same* number, $|\langle f|g\rangle|^2/\langle f|f\rangle$:
by conjugate symmetry $c\,\langle g|f\rangle=\frac{\langle f|g\rangle\langle f|g\rangle^*}{\langle f|f\rangle}
=\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle}$; likewise
$c^*\langle f|g\rangle=\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle}$; and
$|c|^2\langle f|f\rangle=\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle^2}\langle f|f\rangle
=\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle}$. So two of the three cancel and
$$0\ \le\ \langle h|h\rangle=\langle g|g\rangle-\frac{|\langle f|g\rangle|^2}{\langle f|f\rangle}.$$

**Step 5 — rearrange.** Multiply by $\langle f|f\rangle>0$:
$$\langle f|f\rangle\langle g|g\rangle-|\langle f|g\rangle|^2=\langle f|f\rangle\langle h|h\rangle\ \ge\ 0 . \qquad\blacksquare$$
**Equality** holds exactly when $\langle h|h\rangle=0$, i.e. $h=0$, i.e.
$$g=c\,f\quad\text{for some complex }c$$
— one state a multiple of the other (Griffiths p.141). That criterion is reused
verbatim in §3 for the minimum-uncertainty packet. The Step-5 identity — the
gap $\langle f|f\rangle\langle g|g\rangle-|\langle f|g\rangle|^2$ *equals*
$\langle f|f\rangle\langle h|h\rangle$ — is checked numerically on random states
(`code`: `schwarz_gap`, `schwarz_residual_identity`;
`test_schwarz_projection_identity`, `test_schwarz_saturation`).

### 2.2 The uncertainty proof, step by step

(Griffiths 3e §3.5.1, p.138, Eqs. 3.59–3.62.) Fix a normalized state $\Psi$ and
define the **deviation states**
$$f=(\hat A-\langle A\rangle)\Psi,\qquad g=(\hat B-\langle B\rangle)\Psi .$$

**Step 1 — variances are norms (Eq. 3.59).** Since $\hat A$ is Hermitian and
$\langle A\rangle$ real, $\hat A-\langle A\rangle$ is Hermitian too, and one
factor can be moved across the inner product:
$$\sigma_A^2=\bigl\langle\Psi\big|(\hat A-\langle A\rangle)^2\Psi\bigr\rangle
=\bigl\langle(\hat A-\langle A\rangle)\Psi\big|(\hat A-\langle A\rangle)\Psi\bigr\rangle=\langle f|f\rangle,$$
and likewise $\sigma_B^2=\langle g|g\rangle$.

**Step 2 — apply Schwarz (§2.1).**
$$\sigma_A^2\,\sigma_B^2=\langle f|f\rangle\langle g|g\rangle\ \ge\ |\langle f|g\rangle|^2 .$$

**Step 3 — keep only the imaginary part (Eq. 3.60).** For any complex
$z=\operatorname{Re}z+i\operatorname{Im}z$,
$$|z|^2=(\operatorname{Re}z)^2+(\operatorname{Im}z)^2\ \ge\ (\operatorname{Im}z)^2
=\Bigl(\frac{z-z^*}{2i}\Bigr)^2 .$$
Take $z=\langle f|g\rangle$ (Eq. 3.61), so the discarded piece is
$\operatorname{Re}\langle f|g\rangle$ — dropping it is the proof's *second*
inequality (§3 forces it to zero for equality).

**Step 4 — compute $\langle f|g\rangle$.** Move the Hermitian factor
$(\hat A-\langle A\rangle)$ back to the right and expand, remembering that
$\langle A\rangle,\langle B\rangle$ are numbers:
$$\langle f|g\rangle=\bigl\langle\Psi\big|(\hat A-\langle A\rangle)(\hat B-\langle B\rangle)\Psi\bigr\rangle
=\langle\hat A\hat B\rangle-\langle B\rangle\langle A\rangle-\langle A\rangle\langle B\rangle+\langle A\rangle\langle B\rangle
=\langle\hat A\hat B\rangle-\langle A\rangle\langle B\rangle .$$
Swapping the roles of $A$ and $B$:
$\ \langle g|f\rangle=\langle\hat B\hat A\rangle-\langle A\rangle\langle B\rangle .$

**Step 5 — the commutator appears.** Subtract the two; the
$\langle A\rangle\langle B\rangle$ pieces cancel:
$$z-z^*=\langle f|g\rangle-\langle g|f\rangle=\langle\hat A\hat B\rangle-\langle\hat B\hat A\rangle=\bigl\langle[\hat A,\hat B]\bigr\rangle .$$

**Step 6 — chain and take the square root.** Assembling Steps 2, 3, 5:
$$\sigma_A^2\sigma_B^2\ \ge\ \Bigl(\frac{1}{2i}\bigl\langle[\hat A,\hat B]\bigr\rangle\Bigr)^2 .$$
The right side is **real and non-negative**: $[\hat A,\hat B]^\dagger=
(\hat A\hat B-\hat B\hat A)^\dagger=\hat B\hat A-\hat A\hat B=-[\hat A,\hat B]$
is *anti*-Hermitian, so its expectation value is pure imaginary and the $1/i$
turns it real (Griffiths p.139). Taking square roots gives the boxed result.
Every link of this chain — Step 1's norms, Step 2's Schwarz, Step 3's dropped
real part, Step 5's commutator — is verified separately on random spin states
in `code` (`test_uncertainty_chain_stepwise`).

- **Position–momentum:** $[\hat x,\hat p]=i\hbar$ (built in `~QM-05`), so
  $\tfrac1{2i}\langle i\hbar\rangle=\hbar/2$ and we recover $\sigma_x\sigma_p\ge\hbar/2$ (Griffiths p.139).
- **Spin-$\tfrac12$:** $[\hat S_x,\hat S_y]=i\hbar\hat S_z$, so
  $\sigma_{S_x}\sigma_{S_y}\ge\tfrac\hbar2|\langle\hat S_z\rangle|$ (`code`:
  `generalized_bound`, `spin_ops`; verified for random states and exactly
  saturated by $|{\uparrow_z}\rangle$).
- **Compatible observables** commute, the bound is $0$, and they admit
  simultaneous eigenstates — they can be sharp together (Griffiths p.139).

## 3. The minimum-uncertainty wave packet

When does equality hold? The proof used two inequalities (Schwarz, and dropping
$\operatorname{Re}z$); equality in both requires $g=c\,f$ with $c$ pure
imaginary, $c=ia$ (Griffiths 3e §3.5.2, p.141). For $A=\hat x,\ B=\hat p$ this is
the first-order ODE
$$\Bigl(-i\hbar\frac{d}{dx}-\langle p\rangle\Bigr)\psi=ia\,(x-\langle x\rangle)\psi,$$
whose solution is a **Gaussian**:
$$\psi(x)=\Bigl(\tfrac1{2\pi\sigma^2}\Bigr)^{1/4}
e^{-(x-x_0)^2/4\sigma^2}\,e^{ip_0x/\hbar},\qquad
\sigma_x=\sigma,\ \ \sigma_p=\frac{\hbar}{2\sigma},\ \ \sigma_x\sigma_p=\frac\hbar2.$$
"Evidently the minimum-uncertainty wave packet is a gaussian" (Griffiths p.141).
The two standard examples — the free-particle Gaussian packet and the **harmonic
oscillator ground state** — are exactly this object (`code`: `gaussian_packet`;
the ground state is `ho_eigenstate(x, 0)`, and `~QM-09` builds it from scratch).
Excited oscillator states have $\sigma_x\sigma_p=(n+\tfrac12)\hbar>\hbar/2$ — they
*exceed* the bound (verified for $n=0,1,2,3$).

## 4. Ehrenfest's theorem — the classical limit

How does this fuzzy theory reproduce Newton? Take the time derivative of an
expectation value. For a (time-independent) observable $\hat Q$,
$$\frac{d}{dt}\langle\hat Q\rangle=\frac{i}{\hbar}\bigl\langle[\hat H,\hat Q]\bigr\rangle,\qquad
\hat H=\frac{\hat p^2}{2m}+V(\hat x).$$
Feed in $\hat x$ and $\hat p$, using $[\hat p^2,\hat x]=-2i\hbar\hat p$ and
$[V,\hat p]=i\hbar\,V'(\hat x)$:
$$\boxed{\;\frac{d\langle x\rangle}{dt}=\frac{\langle p\rangle}{m},\qquad
\frac{d\langle p\rangle}{dt}=-\langle V'(\hat x)\rangle\;}$$
These are **Ehrenfest's theorem** — "expectation values obey the classical laws"
(Griffiths 3e §1.5; the name appears at Problem 1.7, p.34; the first relation is
Eq. 1.33, p.33). Eliminating $\langle p\rangle$ gives
$m\,d^2\langle x\rangle/dt^2=-\langle V'(\hat x)\rangle$ — Newton's second law for
the averages.

They are exactly **Hamilton's equations** $\dot x=\partial H/\partial p$,
$\dot p=-\partial H/\partial x$ with $(x,p)\to(\langle x\rangle,\langle p\rangle)$
— the bridge forward to `~CM-19`. Note the subtlety: the force is
$\langle V'(\hat x)\rangle$, **not** $V'(\langle x\rangle)$. They coincide when
$V'$ is linear — i.e. for free, constant, and **harmonic** potentials — so for
the SHO the packet centre rides the classical trajectory
$$\langle x\rangle(t)=x_0\cos\omega t+\frac{p_0}{m\omega}\sin\omega t$$
*exactly* (`code`: `split_step_evolve` + `classical_sho`; matched to $\sim10^{-5}$
over a full period). For a general (anharmonic) potential, $\langle V'\rangle\approx
V'(\langle x\rangle)$ only when the packet is narrow on the scale over which $V'$
curves — that controlled approximation **is** the classical limit.

---
### Why this is the hinge of the trunk
The commutator $[\hat A,\hat B]$ does double duty: through `~QM-05` it sets the
*right-hand side of the uncertainty bound* (§2), and through $\hat H$ it
*generates the dynamics* (§4). Where it vanishes, observables are simultaneously
sharp and conserved. The minimum-uncertainty Gaussian (§3) is the boundary case
that `~QM-09` promotes to the oscillator ground state, and Ehrenfest's reduction
to Hamilton's equations (`~CM-19`) is how the whole apparatus hands back classical
mechanics in the appropriate limit.
