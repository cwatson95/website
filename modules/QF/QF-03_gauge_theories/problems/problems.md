# QF-03 — Problems

Work by hand, then check with `code/gauge_theory.py`. Citations in `../refs.md`;
**Pe** = Peskin & Schroeder (Ch. 4, 5, 7), **Zee** = Zee, *QFT in a Nutshell* (§III.4).

### P1.  The global-to-local obstruction  *(Pe §4.1)*
Show that a **global** phase ψ → e^{iα}ψ (α constant) leaves
ℒ₀ = ψ̄(iγ^μ∂_μ − m)ψ invariant, but a **local** phase ψ → e^{iα(x)}ψ does not,
because ∂_μ(e^{iα(x)}ψ) = e^{iα}(∂_μψ + i(∂_μα)ψ) carries a stray gradient of the
phase. Then verify that replacing ∂_μ by D_μ = ∂_μ + ieA_μ and shifting
A_μ → A_μ − (1/e)∂_μα cancels that stray term, so D_μψ → e^{iα}D_μψ. *Check:* with
`A_g = gauge_transform(A, -alpha/e, dx)` and `psi_g = exp(i*alpha)*psi`,
`covariant_derivative(psi_g, A_g, e, dx)` has the **same modulus** as
`covariant_derivative(psi, A, e, dx)` to ≈ 5×10⁻³ (O(dx²)), while the bare gradient
`|∂_μψ|` changes by ≈ 1.0 — an O(1) violation.

*Answer:* The covariant derivative transforms like the field itself, $D_\mu\psi\to e^{i\alpha}D_\mu\psi$, so $|D_\mu\psi|$ is gauge invariant; the bare $\partial_\mu\psi$ is not.

**Solution.** For a *global* phase ($\alpha$ constant) $\partial_\mu(e^{i\alpha}\psi)=e^{i\alpha}\partial_\mu\psi$, so $\bar\psi\gamma^\mu\partial_\mu\psi$ is unchanged. Localizing $\alpha\to\alpha(x)$, the product rule produces a stray gradient,
$$\partial_\mu\big(e^{i\alpha(x)}\psi\big)=e^{i\alpha(x)}\big(\partial_\mu\psi+i(\partial_\mu\alpha)\psi\big),$$
and the extra $i(\partial_\mu\alpha)\psi$ spoils the invariance of $\bar\psi\gamma^\mu\partial_\mu\psi$. Introduce $D_\mu=\partial_\mu+ieA_\mu$ with the paired shift $A_\mu\to A_\mu-\tfrac1e\partial_\mu\alpha$; then under the combined transformation
$$D_\mu(e^{i\alpha}\psi)=e^{i\alpha}\Big[\partial_\mu\psi+i(\partial_\mu\alpha)\psi+ie\big(A_\mu-\tfrac1e\partial_\mu\alpha\big)\psi\Big]=e^{i\alpha}(\partial_\mu+ieA_\mu)\psi=e^{i\alpha}D_\mu\psi,$$
the $i(\partial_\mu\alpha)\psi$ cancelling exactly against the $-\tfrac1e\partial_\mu\alpha$ shift. Hence $|D_\mu\psi|$ is gauge invariant while $|\partial_\mu\psi|$ is not — matching the check: $|D_\mu\psi|$ changes by only $\approx5\times10^{-3}$ (the $O(dx^2)$ finite-difference error) while the bare $|\partial_\mu\psi|$ jumps by $\approx1.0$.

### P2.  Gauge invariance of the field strength  *(Pe §4.1)*
Prove that F_μν = ∂_μA_ν − ∂_νA_μ is unchanged by A_μ → A_μ + ∂_μλ for **any**
scalar λ (the shift contributes ∂_μ∂_νλ − ∂_ν∂_μλ = 0), and that a **pure-gauge**
potential A_μ = ∂_μλ therefore has F_μν = 0 everywhere. Why is F, not A, the
physical field? *Check:* `field_strength(gauge_transform(A, lam, dx), dx)` differs
from `field_strength(A, dx)` by `max|ΔF| ≈ 2×10⁻¹⁵`; and
`field_strength(gauge_transform(0*A, lam, dx), dx)` (a pure gauge) has
`max|F| ≈ 1.7×10⁻¹⁵` — both zero to machine precision.

*Answer:* $F_{\mu\nu}$ is gauge invariant because mixed partials commute; $A_\mu$ is gauge-dependent, so only $F_{\mu\nu}$ (i.e. $\mathbf E,\mathbf B$) is physical, and a pure gauge $A_\mu=\partial_\mu\lambda$ has $F_{\mu\nu}=0$.

**Solution.** Apply the shift $A_\mu\to A_\mu+\partial_\mu\lambda$ directly to the field strength:
$$F_{\mu\nu}\to\partial_\mu(A_\nu+\partial_\nu\lambda)-\partial_\nu(A_\mu+\partial_\mu\lambda)=F_{\mu\nu}+(\partial_\mu\partial_\nu-\partial_\nu\partial_\mu)\lambda.$$
Mixed partials commute, $\partial_\mu\partial_\nu\lambda=\partial_\nu\partial_\mu\lambda$, so the added term vanishes and $F_{\mu\nu}\to F_{\mu\nu}$ exactly. A *pure-gauge* potential is the special case $A_\mu=\partial_\mu\lambda$ (built from $A=0$), for which
$$F_{\mu\nu}=\partial_\mu\partial_\nu\lambda-\partial_\nu\partial_\mu\lambda=0$$
identically. So $A_\mu$ carries gauge-dependent (unphysical) information — the piece $\partial_\mu\lambda$ that any $\lambda$ can add — while $F_{\mu\nu}$, being invariant, is what every observer agrees on and what is measured ($F_{0i}=E_i$, $F_{ij}=-\varepsilon_{ijk}B_k$). Numerically the gauge shift moves $F$ by only $\max|\Delta F|\approx2\times10^{-15}$ and the pure gauge gives $\max|F|\approx1.7\times10^{-15}$ — both zero to machine precision, since the discrete cross-derivatives along distinct axes commute exactly.

### P3.  A uniform field and the field tensor  *(Pe §4.1; ~EM-18)*
For the 2-D potential A = (A₀, A₁) = (0, B x⁰), compute F_01 = ∂₀A₁ − ∂₁A₀ by hand
and show it is the constant B. Identify which entries of F_μν are the electric field
(F_{0i} = E_i) and which are the magnetic field (F_{ij} = −ε_{ijk}B_k), recovering
`~EM-18`'s field tensor. *Check:* `field_strength(np.stack([0*X0, B*X0]), dx)[0,1]`
equals B = 0.75 to ≈ 10⁻¹⁰ (np.gradient is exact on a linear field), and
F[1,0] = −F[0,1] = −B.

*Answer:* $F_{01}=\partial_0A_1-\partial_1A_0=B=0.75$ (uniform); the time–space entries are the electric field $F_{0i}=E_i$ and the space–space entries the magnetic field $F_{ij}=-\varepsilon_{ijk}B_k$.

**Solution.** With $A_0=0$ and $A_1=Bx^0$,
$$F_{01}=\partial_0A_1-\partial_1A_0=\partial_0(Bx^0)-\partial_1(0)=B,$$
a constant, and antisymmetry fixes $F_{10}=-F_{01}=-B$ with $F_{00}=F_{11}=0$. In the full tensor the time–space entries are the electric field, $F_{0i}=E_i$, and the space–space entries the magnetic field, $F_{ij}=-\varepsilon_{ijk}B_k$ — exactly `~EM-18`'s field tensor; here the single nonzero component is a uniform field of strength $B$ along the $x^1$ axis. Because `np.gradient` is exact on the linear field $Bx^0$, the code returns `field_strength(np.stack([0*X0, B*X0]), dx)[0,1]` $=B=0.75$ to $\approx10^{-10}$, with $F[1,0]=-F[0,1]=-0.75$ — confirming the value $B$ and the antisymmetry.

### P4.  The QED Lagrangian generates the interaction  *(Pe §4.1)*
Expand ℒ_QED = ψ̄(iγ^μD_μ − m)ψ − ¼F_μνF^μν with D_μ = ∂_μ + ieA_μ and show it splits
into the free Dirac term, the **interaction** −e ψ̄γ^μψ A_μ = −e j^μ A_μ, and the
photon kinetic term. Explain why the coupling could not have any strength other than
the single charge e, and how this realizes bridge **B8** (symmetry → interaction).
*Check:* the interaction lives in the ieA_μψ piece of `covariant_derivative`; setting
e = 0 collapses D_μψ back to the free ∂_μψ — `covariant_derivative(psi, A, 0.0, dx)`
equals `np.gradient(psi, dx, axis=mu)` to ≈ 10⁻¹⁴.

*Answer:* $\mathcal L_{\text{QED}}=\bar\psi(i\gamma^\mu\partial_\mu-m)\psi-e\,j^\mu A_\mu-\tfrac14F_{\mu\nu}F^{\mu\nu}$; the vertex strength is the single charge $e$ because the coupling enters only through $D_\mu$.

**Solution.** Insert $D_\mu=\partial_\mu+ieA_\mu$ into the Dirac term:
$$\bar\psi(i\gamma^\mu D_\mu-m)\psi=\underbrace{\bar\psi(i\gamma^\mu\partial_\mu-m)\psi}_{\text{free Dirac}}+\bar\psi\,i\gamma^\mu(ieA_\mu)\psi=\bar\psi(i\gamma^\mu\partial_\mu-m)\psi-e\,\bar\psi\gamma^\mu\psi\,A_\mu,$$
because $i\gamma^\mu\cdot ieA_\mu=-e\gamma^\mu A_\mu$. The cross term is exactly $-e\,j^\mu A_\mu$ with the Noether current $j^\mu=\bar\psi\gamma^\mu\psi$; adding the photon kinetic term gives
$$\mathcal L_{\text{QED}}=\bar\psi(i\gamma^\mu\partial_\mu-m)\psi-e\,j^\mu A_\mu-\tfrac14F_{\mu\nu}F^{\mu\nu}.$$
The interaction was never put in by hand — it rode in entirely on the single $e$ inside $D_\mu$ (the same $e$ fixing the gauge shift $A_\mu\to A_\mu-\tfrac1e\partial_\mu\alpha$), so the photon couples to the current with strength exactly $e$, no other value allowed. This is bridge **B8**: local U(1) symmetry has *generated* the interaction. The check isolates the mechanism — the coupling sits in the $ieA_\mu\psi$ piece, and setting $e=0$ collapses $D_\mu\psi$ to the free $\partial_\mu\psi$: `covariant_derivative(psi, A, 0.0, dx)` equals `np.gradient(psi, dx, axis=mu)` to $\approx10^{-14}$.

### P5.  Massless photon and the Coulomb tail  *(Pe §4.7; Zee §III.4)*
(a) Show that a photon mass term ½m²A_μA^μ is **not** gauge invariant under
A_μ → A_μ − (1/e)∂_μα, so gauge symmetry forces m_γ = 0. (b) The static potential
from one-boson exchange is the Fourier transform of 1/(**q**² + m²),
V(r) = e^{−mr}/(4πr); take m → 0 to get the Coulomb potential 1/(4πr) of `~EM-01`.
Why is the *infinite range* of electrostatics a direct measurement of the photon
mass? *Check:* `yukawa_to_coulomb(1.0, 1.0)/yukawa_to_coulomb(1.0, 0.0)` = e⁻¹ ≈
0.3679, rising monotonically to 1.0 as m → 0; and V = e^{−mr}/4πr solves
(−∇² + m²)V = 0 for r > 0 (see `test_yukawa_solves_screened_poisson`).

*Answer:* (a) $\tfrac12 m^2A_\mu A^\mu$ is not gauge invariant, so the symmetry forces $m_\gamma=0$. (b) $V(r)=e^{-mr}/4\pi r\to1/4\pi r$ as $m\to0$ — the Coulomb tail; its infinite range is a measurement of $m_\gamma=0$.

**Solution.** (a) Under $A_\mu\to A_\mu-\tfrac1e\partial_\mu\alpha$ a photon mass term transforms as
$$\tfrac12 m^2A_\mu A^\mu\to\tfrac12 m^2\Big(A_\mu-\tfrac1e\partial_\mu\alpha\Big)\Big(A^\mu-\tfrac1e\partial^\mu\alpha\Big)\neq\tfrac12 m^2A_\mu A^\mu,$$
since the cross and $(\partial\alpha)^2$ pieces do not cancel ($A_\mu$, unlike the gauge-invariant $F_{\mu\nu}F^{\mu\nu}$, is not invariant). So gauge symmetry forbids a photon mass: $m_\gamma=0$ exactly. (b) The static potential is the Fourier transform of the propagator $1/(\mathbf q^2+m^2)$, the Green's function of $(-\nabla^2+m^2)$:
$$V(r)=\int\!\frac{d^3q}{(2\pi)^3}\,\frac{e^{i\mathbf q\cdot\mathbf r}}{\mathbf q^2+m^2}=\frac{e^{-mr}}{4\pi r}\ \xrightarrow{\ m\to0\ }\ \frac{1}{4\pi r}.$$
A massive mediator screens the force over range $1/m$; the massless photon of (a) gives the infinite-range $1/r$ Coulomb law of `~EM-01`, so finding electrostatics to be exactly long-range *is* a bound on $m_\gamma$. The check confirms $V/V_{\text{Coulomb}}=e^{-mr}$: at $m=r=1$ it is $e^{-1}\approx0.3679$, rising monotonically to $1.0$ as $m\to0$, and $V=e^{-mr}/4\pi r$ solves $(-\nabla^2+m^2)V=0$ for $r>0$.

### P6.  The Ward identity and the inert gauge mode  *(Pe §5.5, §7.4)*
For an amplitude ℳ = ε_μ(k)ℳ^μ(k) with an external photon, argue that a gauge
transformation shifts the polarization ε_μ → ε_μ + c k_μ, so physical invariance
**requires** the **Ward identity** k_μℳ^μ = 0 — the longitudinal mode decouples,
leaving only the two transverse photon polarizations. Relate this to the current
conservation ∂_μ j^μ = 0 of the global symmetry. *Check:* the longitudinal/gauge
mode is physically inert already at the classical field level — a pure-gauge
potential A_μ = ∂_μλ (the "k_μ direction") carries no field strength:
`field_strength(gauge_transform(0*A, lam, dx), dx)` is ≈ 1.7×10⁻¹⁵, numerically zero.

*Answer:* Gauge invariance ($\epsilon_\mu\to\epsilon_\mu+ck_\mu$) requires the Ward identity $k_\mu\mathcal M^\mu=0$; the longitudinal mode decouples, leaving the two transverse photon polarizations — the amplitude-level image of $\partial_\mu j^\mu=0$.

**Solution.** An external photon enters an amplitude through its polarization, $\mathcal M=\epsilon_\mu(k)\mathcal M^\mu(k)$. A gauge transformation shifts the polarization along the photon momentum,
$$\epsilon_\mu(k)\to\epsilon_\mu(k)+c\,k_\mu,$$
the momentum-space image of $A_\mu\to A_\mu+\partial_\mu\lambda$. Physics cannot depend on the gauge parameter $c$, so the extra piece must not contribute: $\mathcal M\to\mathcal M+c\,k_\mu\mathcal M^\mu$ for all $c$ forces
$$k_\mu\mathcal M^\mu(k)=0,$$
the **Ward identity**. The longitudinal ($k_\mu$-direction) polarization decouples, so of the four components of $\epsilon_\mu$ only the **two transverse** ones are physical — the massless photon has two helicities. This is the amplitude-level shadow of current conservation $\partial_\mu j^\mu=0$ (in momentum space $k_\mu j^\mu=0$). The check shows the gauge mode is inert already classically: a pure-gauge $A_\mu=\partial_\mu\lambda$ — the "$k_\mu$ direction" — carries zero field strength, `field_strength(gauge_transform(0*A, lam, dx), dx)` $\approx1.7\times10^{-15}$, numerically zero.
