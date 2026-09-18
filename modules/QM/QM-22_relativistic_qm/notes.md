# QM-22 — Relativistic Quantum Mechanics: Klein–Gordon & Dirac (notes)

Ordinary quantum mechanics is built on the Schrödinger equation, which is the
quantization of the **non-relativistic** energy $E=p^2/2m+V$. It treats time and
space asymmetrically (first order in $\partial_t$, second in $\nabla$) and so
cannot be Lorentz invariant. To marry quantum mechanics to special relativity we
must instead quantize the **relativistic** energy–momentum relation. This note
builds the two equations that result — Klein–Gordon (spin-0) and Dirac
(spin-$\tfrac12$) — and shows that spin, the $g=2$ magnetic moment, and the
antiparticle all fall out of the second.

Throughout, **natural units $\hbar=c=1$** (the code documents how to restore SI),
and the **metric is $g_{\mu\nu}=\mathrm{diag}(+1,-1,-1,-1)$** (mostly-minus). A
4-vector is $a^\mu=(a^0,\vec a)$ with $a_\mu=g_{\mu\nu}a^\nu=(a^0,-\vec a)$ and
invariant product $a\cdot b=a_\mu b^\mu=a^0b^0-\vec a\cdot\vec b$.

## 0. The relativistic energy–momentum relation

The single fact we quantize (its home module is `~RE-06`, relativistic dynamics,
which was **skipped** in the RE trunk pending `~CM-06` — so it is stated here):
$$\boxed{\,E^2=p^2c^2+m^2c^4\quad\xrightarrow{\ \hbar=c=1\ }\quad E^2=\vec p^{\,2}+m^2\,}$$
Equivalently, with the 4-momentum $p^\mu=(E,\vec p)$, the on-shell condition is
the Lorentz scalar $p\cdot p=E^2-\vec p^{\,2}=m^2$. The factor that makes this
*hard* to quantize is the square root $E=\pm\sqrt{\vec p^{\,2}+m^2}$: it is
non-local in $\vec p$, and it admits **negative-energy roots**. Both equations
below are different ways to cope with that square root.

## 1. The Klein–Gordon equation (spin 0)

Quantize by the usual replacement $E\to i\partial_t$, $\vec p\to-i\nabla$, i.e.
$p_\mu\to i\partial_\mu$. The scalar $p\cdot p=m^2$ becomes (note
$p\cdot p\to-\partial_\mu\partial^\mu=-\Box$ with $\Box\equiv\partial_t^2-\nabla^2$):
$$\boxed{\,(\Box+m^2)\,\phi=0,\qquad \Box=\partial_\mu\partial^\mu=\partial_t^2-\nabla^2\,}$$
This is **second order in time** and manifestly Lorentz invariant ($\Box$ and
$m^2$ are scalars). For a plane wave $\phi=e^{-ip\cdot x}$, each $\partial_\mu$
brings down $-ip_\mu$, so $\Box\phi=-(p\cdot p)\phi$ and
$$(\Box+m^2)\,e^{-ip\cdot x}=-(p\cdot p-m^2)\,e^{-ip\cdot x}=0
\iff p\cdot p=m^2\iff \boxed{E^2=\vec p^{\,2}+m^2.}$$
*(The code does this honestly: `box_fd` applies $\Box$ by finite differences and
`kg_operator_fd` confirms the residual vanishes on shell — for **both** energy
signs — and equals the closed-form $-(p\cdot p-m^2)\phi$ off shell.)*

**Its two problems**, which is why Dirac looked further:

1. **Negative-energy solutions.** $E=\pm\sqrt{\vec p^{\,2}+m^2}$ both solve it.
   There is no lowest energy; the spectrum is unbounded below. (`test_kg_negative_energy_exists`.)
2. **Indefinite probability density.** The conserved current of a second-order
   equation is $\rho=\tfrac{i}{2m}(\phi^*\partial_t\phi-\phi\,\partial_t\phi^*)$,
   which for a negative-energy mode is **negative** — it cannot be a probability.
   (Compare `~QM-04`'s positive-definite Schrödinger current $|\Psi|^2$.)

Both pathologies are eventually *features*, not bugs: in quantum field theory
(`~QF-01`) $\phi$ is a field, not a wavefunction, $\rho$ becomes a charge density
(allowed to be negative), and the negative-energy modes are repackaged as
**antiparticles**. Klein–Gordon is the correct equation for spin-0 bosons (pions,
the Higgs) — read as a field. *(Griffiths is non-relativistic and never mentions
Klein–Gordon; this is standard material — Sakurai, Ch. 8; Bjorken & Drell, Ch. 1.)*

## 2. The Dirac equation (spin $\tfrac12$)

Dirac wanted an equation **first order in $\partial_t$** (so the density is
positive, as in Schrödinger) yet still relativistic. The only way is to take the
*square root* of the operator $\Box+m^2$ — which requires the coefficients to be
**matrices**. Posit
$$\boxed{\,(i\gamma^\mu\partial_\mu-m)\,\psi=0\,}\qquad\text{(in SI: }i\hbar\gamma^\mu\partial_\mu\psi=mc\,\psi)$$
with four constant matrices $\gamma^\mu$ and $\psi$ a multi-component spinor.
Apply the conjugate operator $(i\gamma^\nu\partial_\nu+m)$:
$$(i\gamma^\nu\partial_\nu+m)(i\gamma^\mu\partial_\mu-m)\psi
=-\big(\gamma^\nu\gamma^\mu\partial_\nu\partial_\mu+m^2\big)\psi.$$
For this to collapse back to the Klein–Gordon operator $-(\Box+m^2)$ — so that
every Dirac solution is automatically a relativistic one — we need
$\gamma^\nu\gamma^\mu\partial_\nu\partial_\mu=\tfrac12\{\gamma^\mu,\gamma^\nu\}\partial_\mu\partial_\nu
=\Box=g^{\mu\nu}\partial_\mu\partial_\nu$, i.e. the **Clifford algebra**
$$\boxed{\,\{\gamma^\mu,\gamma^\nu\}=\gamma^\mu\gamma^\nu+\gamma^\nu\gamma^\mu=2g^{\mu\nu}\,\mathbb 1\,}$$
This is the whole content of "Dirac square-roots Klein–Gordon": **$\text{Dirac}^2=\text{Klein–Gordon}$.**

### The gamma matrices (Dirac representation)

$\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$ forces $(\gamma^0)^2=+\mathbb1$,
$(\gamma^i)^2=-\mathbb1$, and $\gamma^\mu\gamma^\nu=-\gamma^\nu\gamma^\mu$ for
$\mu\ne\nu$ — impossible for numbers, possible for $4\times4$ matrices. The
**Dirac (standard) representation** builds them from $2\times2$ Pauli blocks:
$$\gamma^0=\begin{pmatrix}\mathbb1&0\\0&-\mathbb1\end{pmatrix},\qquad
\gamma^i=\begin{pmatrix}0&\sigma_i\\-\sigma_i&0\end{pmatrix},\qquad
\gamma^5\equiv i\gamma^0\gamma^1\gamma^2\gamma^3=\begin{pmatrix}0&\mathbb1\\\mathbb1&0\end{pmatrix}.$$
Their key properties (all verified to machine precision in the tests, and the
$\sigma_i$ cross-checked against `~MA-18`):
- $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}\mathbb1_4$ for **all 16** pairs;
- $(\gamma^0)^\dagger=\gamma^0$ (Hermitian), $(\gamma^i)^\dagger=-\gamma^i$
  (anti-Hermitian); uniformly $\gamma^{\mu\dagger}=\gamma^0\gamma^\mu\gamma^0$;
- $(\gamma^5)^2=\mathbb1$, $\gamma^{5\dagger}=\gamma^5$, and
  $\{\gamma^5,\gamma^\mu\}=0$ (the root of chirality; `~QF-01`).

The Clifford structure is the subject of `~MA-18` (gamma/Clifford algebra). This
is also where **spin lives**: $\psi$ must have (at least) four components, and the
generators $S^{\mu\nu}=\tfrac{i}{4}[\gamma^\mu,\gamma^\nu]$ rotate them — the spin
representation of the Lorentz group.

### Plane waves and the spectrum

For $\psi=u(p)\,e^{-ip\cdot x}$, $\partial_\mu\to-ip_\mu$ and the equation becomes
the purely algebraic $(\,\not{\!p}-m)u=0$ with the **Feynman slash**
$\not{\!p}\equiv\gamma^\mu p_\mu=\gamma^0E-\vec\gamma\cdot\vec p$. The Clifford
algebra gives at once
$$\not{\!p}^{\,2}=p_\mu p_\nu\gamma^\mu\gamma^\nu=\tfrac12 p_\mu p_\nu\{\gamma^\mu,\gamma^\nu\}=(p\cdot p)\,\mathbb1_4,$$
so $(\not{\!p}-m)(\not{\!p}+m)=(p\cdot p-m^2)\mathbb1_4$ (`dirac_squared`), and a
nontrivial $u$ exists only when the operator is singular:
$$\det(\not{\!p}-m)=(p\cdot p-m^2)^2=0\iff p\cdot p=m^2\iff E^2=\vec p^{\,2}+m^2.$$
So **the Dirac equation still enforces $E^2=\vec p^{\,2}+m^2$** — and the
square-root still has both signs. In the Dirac representation
$$\not{\!p}=\begin{pmatrix}E\,\mathbb1&-\vec\sigma\cdot\vec p\\\vec\sigma\cdot\vec p&-E\,\mathbb1\end{pmatrix},$$
and the **four** independent plane-wave spinors (with $E=+\sqrt{\vec p^{\,2}+m^2}$,
$N=\sqrt{E+m}$, $\xi^s\in\{(1,0),(0,1)\}$) are
$$u^{s}(p)=N\begin{pmatrix}\xi^s\\\dfrac{\vec\sigma\cdot\vec p}{E+m}\,\xi^s\end{pmatrix}
\ \ \big[(\not{\!p}-m)u=0\big],\qquad
v^{s}(p)=N\begin{pmatrix}\dfrac{\vec\sigma\cdot\vec p}{E+m}\,\xi^s\\\xi^s\end{pmatrix}
\ \ \big[(\not{\!p}+m)v=0\big].$$
The two $u^s$ are **positive-energy** (the electron's two spin states); the two
$v^s$, carried by $e^{+ip\cdot x}$, are the **negative-energy / antiparticle**
(positron) solutions. They obey $\bar u^r u^s=+2m\,\delta^{rs}$,
$\bar v^r v^s=-2m\,\delta^{rs}$ ($\bar w=w^\dagger\gamma^0$),
$u^\dagger u=v^\dagger v=2E$, $\bar u^r v^s=0$ — verified in `test_dirac_spinor_normalization`.
The negative norm $\bar v v=-2m$ is the Dirac echo of the Klein–Gordon density
problem; again `~QF-01` resolves it (Dirac's original "hole theory" was the first
patch). *(Sakurai, Ch. 8; Bjorken & Drell, Ch. 3.)*

## 3. The non-relativistic limit — spin and $g=2$ for free

Couple to electromagnetism by minimal substitution $\partial_\mu\to\partial_\mu+iqA_\mu$,
i.e. $\vec p\to\vec\pi=\vec p-q\vec A$, and write $\psi=\binom{\varphi}{\chi}$
(upper/lower 2-spinors) with energy $E=m+\varepsilon$, $\varepsilon,|q\phi|\ll m$.
The lower equation gives $\chi\approx\dfrac{\vec\sigma\cdot\vec\pi}{2m}\varphi$
(small), and substituting into the upper equation yields the **Pauli equation**
$$\boxed{\,\Big[\frac{(\vec\sigma\cdot\vec\pi)^2}{2m}+q\phi\Big]\varphi=\varepsilon\,\varphi\,}$$
Now use the operator identity (the algebraic heart, `test_pauli_vector_identity`)
$$(\vec\sigma\cdot\vec a)(\vec\sigma\cdot\vec b)=(\vec a\cdot\vec b)\,\mathbb1+i\,\vec\sigma\cdot(\vec a\times\vec b)$$
with $\vec a=\vec b=\vec\pi$. The components of $\vec\pi$ no longer commute:
$[\pi_x,\pi_y]=iqB_z$ (gauge invariant), so
$\vec\pi\times\vec\pi=iq\vec B$ and
$$(\vec\sigma\cdot\vec\pi)^2=\vec\pi^{\,2}\,\mathbb1+i\,\vec\sigma\cdot(\vec\pi\times\vec\pi)
=\vec\pi^{\,2}\,\mathbb1-q\,\vec\sigma\cdot\vec B.$$
Hence the Pauli Hamiltonian carries a **spin magnetic-moment (Zeeman) term**
$$H_{\text{spin}}=-\frac{q}{2m}\,\vec\sigma\cdot\vec B
=-\frac{q}{2m}\,g\,\vec S\cdot\vec B,\qquad \vec S=\tfrac12\vec\sigma
\ \Rightarrow\ \boxed{\,g=2\,}$$
Spin-$\tfrac12$ was **never put in by hand** — it is forced by the four-component
spinor — and its gyromagnetic ratio is $g=2$, twice the classical $g=1$ of orbital
motion. Experiment gives $g=2.00232\ldots$; the small excess is the QED anomaly
(`~QF-01`), but the leading $2$ is pure Dirac. *(The code proves $g=2$ rigorously:
it represents $\vec\pi$ on a truncated basis with the exact magnetic commutator
$[\pi_x,\pi_y]=iqB$, forms $(\vec\sigma\cdot\vec\pi)^2$, and reads off the spin
term's coefficient — `dirac_g_factor` returns $g=2.000000$, residual $\sim10^{-15}$.)*

The expansion also reorganizes the kinetic energy. From the square root,
$$E=\sqrt{\vec p^{\,2}+m^2}=m+\frac{p^2}{2m}-\frac{p^4}{8m^3}+\cdots$$
The leading $p^2/2m$ is the Schrödinger kinetic energy (`test_nonrelativistic_energy_limit`);
the next term $-p^4/8m^3$ is the **leading relativistic correction** to hydrogen,
which — together with the spin–orbit coupling that also drops out of the Dirac
reduction — produces the **fine structure** of `~QM-17`. Griffiths gets that fine
structure perturbatively and notes (p.388, p.415) that the *exact* result comes
"from the (relativistic) Dirac equation" — this module is the equation behind that
remark.

---
### Why this is the gateway out of single-particle QM
The Dirac equation does three things at once: it makes QM Lorentz invariant, it
*derives* spin-$\tfrac12$ and $g=2$ (`~QM-11`, `~QM-17`), and — through its
unavoidable negative-energy solutions — it forces the move to **fields and
antiparticles**. The single-particle interpretation breaks down (a localized
electron has enough energy to pair-create); the consistent theory is quantum field
theory, `~QF-01`, where $\phi$ and $\psi$ are operator-valued fields, the
negative-energy modes become antiparticle creation operators, and the indefinite
densities become well-defined charges. Relativistic QM is thus both the capstone
of the QM trunk and the on-ramp to QFT.
