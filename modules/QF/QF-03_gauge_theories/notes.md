# QF-03 — Gauge Theories — QED & Gauge Invariance (notes)

Quantum electrodynamics is not *postulated* — it is *forced*. Demand that the free
Dirac field keep its phase symmetry **locally**, at every spacetime point
independently, and the photon, its coupling to charge, and the entire structure of
QED drop out as the unique price of consistency. This is the **gauge principle**, the
field-theory endpoint of **KEY BRIDGE B8** (`~MA-18` Lie groups → `~CM-18` Noether →
QF-03 gauge) and the quantum descendant of the classical gauge freedom
**A** → **A** + ∇λ of `~EM-09`.

Citation key (full details in `refs.md`): **Pe** = Peskin & Schroeder, *An
Introduction to Quantum Field Theory* (Ch. 4 QED & minimal coupling, Ch. 7 Ward
identity); **Zee** = Zee, *QFT in a Nutshell* (§III.4, the massless photon).
Citations are at **section/chapter** level (no page numbers verified).

## 1. Global U(1) symmetry and the Noether current
The free Dirac Lagrangian (`~QF-01`) is invariant under a **global** phase rotation —
the *same* angle $\alpha$ everywhere [Pe §4.1]:
$$\mathcal L_0=\bar\psi\,(i\gamma^\mu\partial_\mu-m)\,\psi,\qquad
  \psi\to e^{i\alpha}\psi,\quad \bar\psi\to e^{-i\alpha}\bar\psi\quad(\alpha=\text{const}).$$
Since $\partial_\mu\psi\to e^{i\alpha}\partial_\mu\psi$, every term is unchanged. This
is a U(1) symmetry (`~MA-18`); Noether's theorem (`~CM-18`) hands back a **conserved
current** — the electric charge of the electron:
$$j^\mu=\bar\psi\gamma^\mu\psi,\qquad \partial_\mu j^\mu=0.$$

## 2. Localizing the phase: the obstruction
Now let the angle vary from point to point, $\alpha\to\alpha(x)$ — a **local** U(1)
transformation. The mass term still survives, but the derivative does not: the
product rule produces a stray term that no global rotation can,
$$\partial_\mu\big(e^{i\alpha(x)}\psi\big)
  =e^{i\alpha(x)}\big(\partial_\mu\psi+i\,(\partial_\mu\alpha)\,\psi\big).$$
The extra $i(\partial_\mu\alpha)\psi$ spoils the invariance of $\bar\psi\gamma^\mu
\partial_\mu\psi$. Code: `covariant_derivative(psi, A, 0, dx)` is exactly this bare
$\partial_\mu\psi$, and its modulus is *not* invariant (the demo prints the O(1) change).

## 3. The covariant derivative and minimal coupling
To absorb the stray gradient, introduce a **connection field** $A_\mu$ and replace
$\partial_\mu$ by the **covariant derivative**. Demanding that $D_\mu\psi$ rotate
*like $\psi$ itself* fixes how $A_\mu$ must transform [Pe §4.1]:
$$D_\mu=\partial_\mu+ieA_\mu,\qquad
  A_\mu\to A_\mu-\frac1e\,\partial_\mu\alpha\ \ \Longrightarrow\ \
  D_\mu\psi\to e^{i\alpha(x)}\,D_\mu\psi.$$
The $-\tfrac1e\partial_\mu\alpha$ shift exactly cancels the $i(\partial_\mu\alpha)\psi$
of §2. This substitution $\partial_\mu\to D_\mu$ is **minimal coupling** — the same
$\mathbf p\to\mathbf p-q\mathbf A$ that made the gauge-invariant current of `~QM-04`.
Code: `covariant_derivative(psi, A, e, dx)`; `gauge_transform` with $\lambda=-\alpha/e$
realizes the paired shift of $A_\mu$, after which $|D_\mu\psi|$ is invariant.

## 4. Field strength: the gauge-invariant curvature
The field built from $A_\mu$ that *all* observers agree on is the antisymmetric
**field-strength tensor** — the curvature of the connection [Pe §4.1]:
$$\begin{aligned}
F_{\mu\nu}&=\partial_\mu A_\nu-\partial_\nu A_\mu=\frac{1}{ie}\,[D_\mu,D_\nu],\\
F_{\mu\nu}&\to F_{\mu\nu}-\frac1e\big(\partial_\mu\partial_\nu-\partial_\nu\partial_\mu\big)\alpha
  =F_{\mu\nu}.
\end{aligned}$$
The shift cancels because partial derivatives commute — and **so do their
finite-difference counterparts along distinct axes**, which is why the code reaches
machine precision. Code: `field_strength(A, dx)`; `gauge_transform` then
`field_strength` again gives `max|ΔF| ≈ 2×10⁻¹⁵`, and a **pure-gauge** potential
$A_\mu=\partial_\mu\lambda$ has $F_{\mu\nu}=0$ identically. ($F_{0i}=\mathbf E$,
$F_{ij}=-\varepsilon_{ijk}B_k$, so this *is* `~EM-18`'s field tensor.)

## 5. The QED Lagrangian
Add the unique gauge-invariant, Lorentz-invariant kinetic term $-\tfrac14 F_{\mu\nu}
F^{\mu\nu}$ for the photon, and the theory is complete [Pe §4.1]:
$$\boxed{\ \mathcal L_{\text{QED}}=\bar\psi\,(i\gamma^\mu D_\mu-m)\,\psi-\tfrac14 F_{\mu\nu}F^{\mu\nu}\ }$$
Expanding $D_\mu=\partial_\mu+ieA_\mu$ exposes the punchline of bridge **B8** —
*symmetry has generated the interaction*:
$$\mathcal L_{\text{QED}}=\underbrace{\bar\psi(i\gamma^\mu\partial_\mu-m)\psi}_{\text{free Dirac}}
  -\underbrace{e\,\bar\psi\gamma^\mu\psi\,A_\mu}_{e\,j^\mu A_\mu}
  -\tfrac14 F_{\mu\nu}F^{\mu\nu}.$$
The coupling $-e\,j^\mu A_\mu$ — photon to charge current — was *not* put in by hand;
local U(1) demanded it, and the strength is the single charge $e$.

## 6. The photon stays massless
A photon mass would enter as $\tfrac12 m_\gamma^2 A_\mu A^\mu$. But under the gauge
shift this term is **not invariant** [Zee §III.4]:
$$\tfrac12 m_\gamma^2 A_\mu A^\mu\ \to\
  \tfrac12 m_\gamma^2\Big(A_\mu-\tfrac1e\partial_\mu\alpha\Big)\Big(A^\mu-\tfrac1e\partial^\mu\alpha\Big)
  \neq\tfrac12 m_\gamma^2 A_\mu A^\mu .$$
Gauge symmetry therefore **forbids** a photon mass: $m_\gamma=0$ exactly. (Only
$F_{\mu\nu}F^{\mu\nu}$, built from gauge-invariant $F$, is allowed.) The masslessness
is not an accident to be fine-tuned — it is protected by the symmetry, and it is
*directly observable* as the infinite range of the Coulomb force (§8).

## 7. The Ward identity
Gauge invariance leaves a fingerprint on every amplitude. Writing a process with an
external photon as $\mathcal M=\epsilon_\mu(k)\,\mathcal M^\mu(k)$, a gauge change
shifts the polarization $\epsilon_\mu\to\epsilon_\mu+c\,k_\mu$; physics cannot
depend on it, so the longitudinal piece must decouple — the **Ward(–Takahashi)
identity** [Pe §5.5, §7.4]:
$$\boxed{\ k_\mu\,\mathcal M^\mu(k)=0\ }$$
It guarantees that only the **two transverse** polarizations of the massless photon
ever contribute, and underwrites the consistency (unitarity, renormalizability
`~QF-04`) of QED. It is the amplitude-level shadow of $\partial_\mu j^\mu=0$ from §1.

## 8. From the propagator to the Coulomb potential
Exchanging one boson of mass $m$ between two static charges gives, in the
non-relativistic limit, the spatial Fourier transform of the propagator
$1/(\mathbf q^2+m^2)$ — the Green's function of $(-\nabla^2+m^2)$ [Pe §4.7]:
$$V(r)=\int\!\frac{d^3q}{(2\pi)^3}\,\frac{e^{i\mathbf q\cdot\mathbf r}}{\mathbf q^2+m^2}
  =\frac{e^{-mr}}{4\pi r}\;\;\longrightarrow\;\;\frac{1}{4\pi r}\quad(m\to0).$$
A massive mediator gives the **short-range Yukawa** potential $e^{-mr}/4\pi r$; the
massless photon (§6) gives the **long-range Coulomb** potential $1/4\pi r$. The
$1/r$ law of `~EM-01` is thus a *measurement* of the photon's zero mass. Code:
`yukawa_to_coulomb(r, m)` returns $e^{-mr}/4\pi r$ and the demo tabulates the
ratio $V/V_{\text{Coulomb}}=e^{-mr}\to1$.

## Where this goes
- **KEY BRIDGE B8** completed: `~MA-18` (U(1) as a Lie group) → `~CM-18` (Noether:
  global symmetry → conserved $j^\mu$) → **QF-03** (local symmetry → the gauge field
  and its interaction). The classical seed is `~EM-09`'s **A** → **A** + ∇λ.
- `~QF-04` — the Ward identity and gauge symmetry are what make QED renormalizable;
  the running coupling $e(\mu)$ and the renormalization group live there.
- **Non-abelian** generalization: replace U(1) by SU(N), $\alpha(x)\to$ matrix
  $\alpha^a(x)T^a$, and $F_{\mu\nu}$ gains a $-ig[A_\mu,A_\nu]$ self-coupling — the
  Yang–Mills theories behind the weak and strong interactions [Zee Part IV].
- `~QM-04`/`~QM-22` — the gauge-covariant current and the minimal-coupling
  $\mathbf p\to\mathbf p-q\mathbf A$ first met in single-particle QM are the
  non-relativistic shadow of this construction.
