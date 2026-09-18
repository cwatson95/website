# QF-04 — Renormalization & the Renormalization Group (notes)

Loop corrections in quantum field theory are infinite. **Renormalization** is the
discovery that this is not a disaster but a feature: the infinities hide inside
unmeasurable *bare* parameters, every physical prediction is finite, and the price —
a coupling that depends on the scale at which you probe it — is itself the deepest
idea, the **renormalization group**. The same RG that tames QED's divergences is the
one that explains why distant systems share critical exponents (`~SM-05`).

Citation key (full details in `refs.md`): **PS** = Peskin & Schroeder,
*An Introduction to QFT*; **Zee** = Zee, *QFT in a Nutshell*; **Riv** = Rivasseau,
*From Perturbative to Constructive Renormalization*. Cited at chapter/section level.

## 1. UV divergences and regularization
A one-loop correction is an integral over the loop momentum $k$ that runs to
infinity. The $\phi^4$ four-point function at one loop is logarithmically divergent
[PS Ch. 10]:
$$\Gamma^{(4)}=-\lambda+\frac{3\lambda^2}{2}\int\!\frac{d^4k}{(2\pi)^4}\,
\frac{1}{(k^2-m^2)^2}+\cdots
\;\sim\;-\lambda+\frac{3\lambda^2}{32\pi^2}\ln\frac{\Lambda^2}{\mu^2}.$$
To make sense of it we **regularize**: impose a momentum cutoff $\Lambda$ (used
above), or — preserving Lorentz and gauge symmetry — continue to $d=4-\epsilon$
dimensions (**dimensional regularization**), where the divergence appears as a pole
$1/\epsilon$.

## 2. Renormalization: bare vs. renormalized, counterterms
The cutoff dependence is absorbed by declaring the parameters in the Lagrangian
(the **bare** $\lambda_0,m_0,\phi_0$) to be cutoff-dependent, related to the
finite **renormalized** ones by $Z$-factors [PS Ch. 10]:
$$\phi_0=Z_\phi^{1/2}\,\phi,\qquad m_0^2=Z_m\,m^2,\qquad
\lambda_0=Z_\lambda\,\lambda .$$
Equivalently, split $\mathcal L=\mathcal L_\text{ren}+\mathcal L_\text{c.t.}$ into a
renormalized piece plus **counterterms** $\propto(Z-1)$, fixed by renormalization
conditions so that every measurable Green's function is finite as $\Lambda\to\infty$.
A theory needing only finitely many counterterms is **renormalizable**; that this
program is consistent to all orders is the content of constructive renormalization
[Riv].

## 3. The renormalization group and the beta function
The renormalized coupling is defined at an arbitrary sliding scale $\mu$. Physics
cannot depend on this choice, so $\mu$-independence of observables forces the
coupling to **run**. Its flow is the **beta function** [PS Ch. 12]:
$$\beta(g)\equiv\mu\,\frac{\partial g}{\partial\mu}\bigg|_{g_0,\,\Lambda},$$
the heart of the Callan–Symanzik equation. Integrating it gives the **running
coupling** $g(\mu)$. Code: `beta_qed`, `beta_phi4`, `beta_qcd`, `beta_toy`.

## 4. QED at one loop: the running fine-structure constant
Vacuum polarization (an electron–positron loop in the photon propagator) screens
charge, giving a positive beta function [PS Ch. 7]:
$$\beta(\alpha)=\mu\,\frac{d\alpha}{d\mu}=\frac{2\alpha^2}{3\pi}>0 ,$$
whose solution is the closed-form **running coupling**
$$\alpha(Q)=\frac{\alpha(\mu)}{\,1-\dfrac{\alpha(\mu)}{3\pi}\ln(Q^2/\mu^2)\,}.$$
So $\alpha$ **grows with energy**: from $\alpha(0)\simeq 1/137$ at the Thomson limit
to $\alpha(M_Z)\simeq 1/128$ at the $Z$ pole. The electron loop alone moves
$1/137\to 1/134.5$; summing over *all* charged Standard-Model fermions (each adding
$Q_f^2 N_c^f$ above its threshold) steepens the slope to the measured $1/128$. Code:
`qed_running_alpha` (electron-only closed form), `qed_alpha_sm` (full threshold sum).

## 5. The Landau pole
Because $\alpha$ increases without bound, the denominator in §4 reaches zero at a
finite energy — the **Landau pole**:
$$Q_\text{Landau}=\mu\,\exp\!\left(\frac{3\pi}{2\,\alpha(\mu)}\right).$$
For QED this is $\sim 10^{277}\,\text{GeV}$, vastly above the Planck scale
($\sim 10^{19}\,\text{GeV}$): the pole is not a real catastrophe but a signal that
perturbative QED cannot be the final theory at such energies. Code: `qed_landau_pole`.

## 6. $\phi^4$ theory and triviality
Scalar $\phi^4$ has the same-sign one-loop beta function [PS Ch. 12]:
$$\beta(\lambda)=\frac{3\lambda^2}{16\pi^2}>0
\quad\Longrightarrow\quad
\frac{1}{\lambda(\mu)}=\frac{1}{\lambda_0}-\frac{3}{16\pi^2}\ln\frac{\mu}{\mu_0}.$$
The coupling grows in the UV and again hits a Landau pole. Demanding a finite
continuum limit ($\Lambda\to\infty$ with the pole sent to infinity) forces
$\lambda\to 0$ — the celebrated **triviality** of $\phi^4$ in four dimensions. Code:
`phi4_running` (numerically integrates the ODE), `phi4_landau_pole`.

## 7. The other sign: asymptotic freedom
Non-abelian gauge theories reverse the sign. For $SU(N)$ with $n_f$ fermions
[PS Ch. 16–17]:
$$\beta(g)=-\frac{g^3}{16\pi^2}\!\left(\frac{11}{3}C_A-\frac{4}{3}T_F\,n_f\right)<0
\quad(\text{QCD: }C_A=3,\ n_f<\tfrac{33}{2}),$$
so the coupling **shrinks** at high energy: **asymptotic freedom**, why quarks are
nearly free inside hadrons and QCD is calculable at colliders. The running
$\alpha_s(M_Z)\simeq 0.118$ decreases toward higher $Q$. Code: `beta_qcd`,
`qcd_running_alpha`.

## 8. Fixed points and the bridge to critical phenomena
A zero of the beta function, $\beta(g_*)=0$, is a **fixed point**: there the theory
is scale-invariant. Its stability is set by the slope. For the toy
$\beta(g)=a\,g^2-b\,g^3$ the nontrivial zero and its slope are
$$g_*=\frac{a}{b},\qquad
\beta'(g_*)=-\frac{a^2}{b}<0\ \Rightarrow\ \text{UV-attractive (couplings flow into }g_*).$$
A negative slope draws nearby couplings *into* $g_*$ as $\mu\to\infty$; a positive
slope repels them. These linearized RG eigenvalues at the fixed point are exactly
what fix the **critical exponents** of statistical mechanics — the Wilson–Fisher
fixed point of $\phi^4$ in $d=4-\epsilon$ governs the Ising universality class of
`~SM-05` [PS Ch. 12–13]. Code: `beta_toy`, `fixed_point`.

## Where this goes
- `~SM-05` — the *same* RG: fixed points and the linearized eigenvalues are the critical exponents (universality).
- `~QF-02` — the loop diagrams (vacuum polarization, the $\phi^4$ bubble) whose divergences are renormalized here.
- `~QF-03` — the QED coupling that runs; gauge invariance constrains the counterterms (Ward identities).
- The running coupling is the working tool of every collider prediction; asymptotic freedom is what makes QCD usable.
