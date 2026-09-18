# QM-02 — The Wavefunction & Born's Rule (notes)

`~QM-01` ended with de Broglie's claim that matter is wavelike, $\lambda=h/p$, but
left the obvious question unanswered: *what is the wave?* It is not a wave of
anything material — not a displacement, not a pressure. The answer, due to **Max
Born (1926)**, is the conceptual core of quantum mechanics: the wave is a
*probability amplitude*. This module makes that statement quantitative and turns
it into operations you can evaluate on a grid (`code/wavefunction.py`).

Everywhere below, the state of a particle on a line is a complex function
$\Psi(x,t)$, the **wavefunction**, obtained (eventually, in `~QM-03`) by solving
the Schrödinger equation (Griffiths 3e §1.1, printed p.16).

## 1. The wavefunction $\Psi(x,t)$

Classical mechanics tracks a trajectory $x(t)$; quantum mechanics tracks instead a
complex field $\Psi(x,t)$ spread over all $x$ (Griffiths §1.1, p.16). A point
particle "is" this delocalized object — the tension that §1.2 resolves. $\Psi$ is
complex, so it carries both a magnitude and a phase; the magnitude will encode
*where* the particle is likely to be, and the phase (we'll see in §5) encodes *how
fast it is moving*.

## 2. Born's statistical interpretation — $|\Psi|^2$ is a probability density

Born's rule (Griffiths §1.2, printed p.17): $|\Psi(x,t)|^2$ is the **probability
density** for finding the particle at $x$ at time $t$. The probability of finding
it in a finite interval $[a,b]$ is the area under $|\Psi|^2$,
$$\boxed{\,P(a\le x\le b)=\int_a^b |\Psi(x,t)|^2\,dx\,}$$
(Griffiths §1.3.2 *Continuous Variables*, Eq.1.16, printed p.26; `prob_between`).
The quantity $\rho=|\Psi|^2$ is a density — it has units of 1/length and only
becomes a probability after integrating over an interval (`prob_density`). This is
the same probability machinery as `~MA-19`: a normalized non-negative density on
the line.

Born's rule injects genuine **indeterminacy**: even with complete knowledge of
$\Psi$, only the *statistics* of a position measurement are predictable, not the
outcome (Griffiths p.17). That is not ignorance of a hidden variable — Bell's
theorem (Griffiths' "Afterword," foreshadowed on p.18) later shows there is no
such variable.

## 3. Normalization, square-integrability, and preservation in time

A probability density must integrate to 1 — the particle is *somewhere*:
$$\boxed{\,\int_{-\infty}^{\infty}|\Psi(x,t)|^2\,dx=1\,}$$
(Griffiths §1.4 *Normalization*, Eq.1.20, printed p.29; `total_probability`,
`normalize`). Because the Schrödinger equation is linear, if $\Psi$ is a solution
so is $A\Psi$; we fix $A$ by demanding this integral equal 1 — *normalizing*
$\Psi$ (`normalize` divides by $\sqrt{\int|\Psi|^2dx}$).

For the integral to be finite, $\Psi$ must be **square-integrable**, which forces
$\Psi\to0$ as $x\to\pm\infty$. States with infinite (or zero) norm cannot be
normalized and "cannot represent particles, and must be rejected … physically
realizable states correspond to the square-integrable solutions" (Griffiths p.29).
(The plane wave $e^{ikx}$ of `~QM-01` is *not* square-integrable — a genuine
particle is a normalizable *packet*, §6.)

**Preservation in time.** Normalizing at $t=0$ would be pointless if the norm
drifted. It does not: the Schrödinger equation guarantees
$$\frac{d}{dt}\int_{-\infty}^{\infty}|\Psi|^2\,dx=0,$$
because the boundary term in the derivation vanishes for square-integrable $\Psi$
(Griffiths §1.4, Eq.1.27, printed p.30 — "if $\Psi$ is normalized at $t=0$, it
stays normalized for all future time. QED"). The *mechanism* — a probability
current obeying a continuity equation — is the subject of `~QM-04`. We *exhibit*
the fact here with `free_propagate`: a free Gaussian packet spreads, yet
$\int|\Psi|^2dx$ stays exactly 1 (test `test_free_evolution_preserves_normalization`).

## 4. Expectation values and the spread

The **expectation value** of position is the mean of the Born density,
$$\langle x\rangle=\int_{-\infty}^{\infty} x\,|\Psi(x,t)|^2\,dx
\tag{Griffiths Eq.1.28, §1.5, p.32}$$
(`expectation_x`). Crucially this is *not* the average of repeated measurements on
one particle (the first measurement collapses $\Psi$ to a spike, and `~QM-06`
explains why repeats then agree). It is the average over an **ensemble** of
identically-prepared systems — "a row of bottles on a shelf, each containing a
particle in the state $\Psi$" (Griffiths p.32).

The **spread** about the mean uses the variance theorem of probability
(Griffiths §1.3.1, Eq.1.12, printed p.24):
$$\sigma_x^2=\langle x^2\rangle-\langle x\rangle^2,\qquad
\sigma_x=\sqrt{\langle x^2\rangle-\langle x\rangle^2}$$
with $\langle x^2\rangle=\int x^2|\Psi|^2dx$ (`expectation_x2`, `sigma_x`). The
standard deviation $\sigma_x$ is the customary measure of how localized the
particle is.

## 5. Momentum and the operator $\hat p=-i\hbar\,\partial_x$

We can't write $\langle p\rangle=\int p\,|\Psi|^2dx$ — $\Psi$ is a function of $x$,
not $p$. Griffiths gets $\langle p\rangle$ by differentiating $\langle x\rangle$ in
time and using the Schrödinger equation (§1.5, Eqs.1.29–1.32, pp.32–33); the result
is that momentum is **represented by an operator**:
$$\boxed{\,\langle p\rangle=\int_{-\infty}^{\infty}\Psi^{*}\!\left(-i\hbar\frac{\partial}{\partial x}\right)\!\Psi\,dx\,}
\qquad \hat p=-i\hbar\frac{\partial}{\partial x}$$
(Griffiths Eqs.1.33–1.35, printed p.33; `expectation_p` via a central finite
difference). This is the first instance of the central rule: to get the
expectation of any observable $Q(x,p)$, "sandwich" the operator
$\hat Q(x,-i\hbar\partial_x)$ between $\Psi^*$ and $\Psi$ and integrate
(Griffiths Eq.1.36, p.33) — the seed of the operator formalism `~QM-05` and the
measurement postulates `~QM-06`.

Two consequences we check numerically:
- $\langle p^2\rangle=\int\Psi^*(-\hbar^2\partial_x^2)\Psi\,dx=\hbar^2\!\int|\partial_x\Psi|^2dx$
  (integration by parts; `expectation_p2`), hence $\sigma_p=\sqrt{\langle p^2\rangle-\langle p\rangle^2}$ (`sigma_p`).
- **Ehrenfest's theorem:** $\langle p\rangle=m\,d\langle x\rangle/dt$ and
  $d\langle p\rangle/dt=\langle -\partial V/\partial x\rangle$ — expectation values
  obey the classical laws (Griffiths Problem 1.7, printed p.34). For the free
  packet of §6 this is just $\langle x\rangle(t)=x_0+(\langle p\rangle/m)t$, which
  `free_propagate` reproduces (`test_free_evolution_group_velocity`).

## 6. The move to momentum space (Fourier transform)

A phase $e^{ik_0x}$ carries momentum: $\hat p\,e^{ik_0x}=\hbar k_0 e^{ik_0x}$. So
the same state can be described by its **momentum-space wavefunction**
$$\Phi(p,t)=\frac{1}{\sqrt{2\pi\hbar}}\int_{-\infty}^{\infty}\Psi(x,t)\,e^{-ipx/\hbar}\,dx,$$
the Fourier transform of $\Psi$ (Griffiths §3.4, "the momentum space wave
function," printed p.134; the transform machinery is `~MA-09`). $|\Phi(p)|^2$ is
the probability density over *momentum*, with $\int|\Phi|^2dp=1$ by Plancherel's
theorem — probability is conserved by the change of representation
(`momentum_space`, `test_momentum_space_is_normalized`). Computing $\langle p\rangle$
either way (finite difference in $x$, or $\int p|\Phi|^2dp$ in $p$) gives the same
number (`expectation_p_fft`).

### The Gaussian wavepacket — everything in closed form

The one state for which all of the above is elementary, and the validation target
for the whole module, is the **Gaussian wavepacket**
$$\Psi(x)=\big(2\pi\sigma^2\big)^{-1/4}\exp\!\Big(-\frac{(x-x_0)^2}{4\sigma^2}\Big)\,e^{ik_0x}
\quad\Rightarrow\quad |\Psi|^2=\frac{1}{\sqrt{2\pi\sigma^2}}\,e^{-(x-x_0)^2/2\sigma^2},$$
a normalized normal distribution of mean $x_0$ and standard deviation $\sigma$
(`gaussian_packet`). Then, in closed form (all checked in `test_wavefunction.py`):

| quantity | value | code / test |
|---|---|---|
| $\int|\Psi|^2dx$ | $1$ | `total_probability` |
| $\langle x\rangle$ | $x_0$ | `expectation_x` |
| $\langle x^2\rangle$ | $x_0^2+\sigma^2$ | `expectation_x2` |
| $\sigma_x$ | $\sigma$ | `sigma_x` |
| $\langle p\rangle$ | $\hbar k_0$ | `expectation_p` / `_fft` |
| $\langle p^2\rangle$ | $\hbar^2\!\left(k_0^2+\tfrac1{4\sigma^2}\right)$ | `expectation_p2` |
| $\sigma_p$ | $\hbar/2\sigma$ | `sigma_p` |
| $P(|x-x_0|<L\sigma)$ | $\operatorname{erf}(L/\sqrt2)$ | `prob_between` |

The last column of physics is the punchline:
$$\sigma_x\,\sigma_p=\sigma\cdot\frac{\hbar}{2\sigma}=\frac{\hbar}{2}.$$
The Gaussian **saturates** the Heisenberg bound $\sigma_x\sigma_p\ge\hbar/2$ — it is
the *minimum-uncertainty* state. Squeezing it in $x$ (small $\sigma$) necessarily
broadens it in $p$ (large $\hbar/2\sigma$), because $|\Psi|^2$ and $|\Phi|^2$ are a
Fourier pair. That trade-off is the whole story of `~QM-07`; here it falls out of
the closed forms (`test_minimum_uncertainty_product`).

---
### Where this sits in the trunk
`~QM-01` (the de Broglie wave) → **QM-02 (what the wave *means*: $|\Psi|^2$ is
probability)** → `~QM-03` (the Schrödinger equation that *evolves* $\Psi$) →
`~QM-04` (the probability current that *conserves* $\int|\Psi|^2$) → `~QM-05`/`~QM-06`
(observables as operators, and what a measurement does). The Fourier bridge to
momentum space is `~MA-09`; the probability spine is `~MA-19`.
