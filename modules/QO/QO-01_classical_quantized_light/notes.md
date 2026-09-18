# QO-01 — Classical & Quantized Light — Modes, Fock & Coherent States (notes)

Light is a collection of **modes** of the electromagnetic field. Classically each
mode is a real oscillation with a complex amplitude $\alpha$ — the picture behind
the plane waves of `~EM-15`. The decisive step of quantum optics is that *a single
field mode is literally a quantum harmonic oscillator* (`~QM-09`, **KEY BRIDGE
B6**): its amplitude becomes the ladder operators $\hat a,\hat a^\dagger$, its
quanta are **photons**, and the eigenstates are the **Fock (number) states**
$|n\rangle$. The **coherent states** $|\alpha\rangle$ then sit between the two
worlds — eigenstates of $\hat a$ whose photon statistics are Poissonian and whose
noise is the bare vacuum level. They are the closest quantum analogue of a
classical field, and the natural input/pump state for the laser and SBS work this
trunk feeds.

Citation key (full details in `refs.md`): **SZ** = Scully & Zubairy, *Quantum
Optics*; **Bo** = Boyd, *Nonlinear Optics*. Citations are at section level.

## 1. A field mode is an oscillator (bridge B6)

Expand the field of a cavity/box in its normal modes (`~EM-15`); one mode of
frequency $\omega$ has a classical complex amplitude $\alpha$, and its energy is
that of a harmonic oscillator [SZ §1.1]. Promoting the amplitude to an operator
**quantizes** the mode:
$$\mathbf E(\mathbf r,t)=\mathcal E_0\big(\alpha\,e^{-i\omega t}+\alpha^*e^{+i\omega t}\big)\,\mathbf u(\mathbf r),\qquad \alpha\;\longrightarrow\;\hat a,\quad \alpha^*\;\longrightarrow\;\hat a^\dagger .$$
The mode Hamiltonian and the canonical commutator are then exactly those of the
quantum SHO of `~QM-09`:
$$\hat H=\hbar\omega\Big(\hat a^\dagger\hat a+\tfrac12\Big)=\hbar\omega\Big(\hat n+\tfrac12\Big),\qquad [\hat a,\hat a^\dagger]=1 .$$
Here $\hat n=\hat a^\dagger\hat a$ is the **number operator** (it counts photons)
and $\tfrac12\hbar\omega$ is the **zero-point energy** — the field fluctuates even
with no photons present. Code: `annihilation`, `creation`, `number`, `commutator`,
`energy`, `zero_point_energy` (matrices in a number basis truncated to $N$ levels,
so $[\hat a,\hat a^\dagger]=\mathrm{diag}(1,\dots,1,-(N{-}1))$ — identity on the
interior, exactly as in `~QM-09`).

## 2. Fock (number) states and the ladder

The eigenstates of $\hat n$ are the **Fock states** $|n\rangle$ ($n=0,1,2,\dots$
photons), and $\hat a,\hat a^\dagger$ move between them [SZ §1.2]:
$$\hat a\,|n\rangle=\sqrt{n}\,|n-1\rangle,\qquad \hat a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle,\qquad \hat a|0\rangle=0 .$$
Climbing from the vacuum $|0\rangle$ builds every state, the states are orthonormal,
and the energy is the oscillator spectrum with its zero-point offset:
$$|n\rangle=\frac{(\hat a^\dagger)^n}{\sqrt{n!}}\,|0\rangle,\qquad \langle m|n\rangle=\delta_{mn},\qquad E_n=\hbar\omega\Big(n+\tfrac12\Big).$$
A Fock state has a **sharp** photon number ($\Delta n=0$) but a completely
undefined phase — about as *un*classical as light gets. Code: `fock_state`,
`number`, and the photon-statistics functions `mean_n`/`var_n` (giving
$\langle\hat n\rangle=n$, $\Delta n=0$).

## 3. Quadratures and vacuum fluctuations

Split the field into its in-phase and out-of-phase parts — the dimensionless
**quadratures**, the "position" and "momentum" of the mode [SZ §2.3]:
$$\hat X=\frac{\hat a+\hat a^\dagger}{2},\qquad \hat P=\frac{\hat a-\hat a^\dagger}{2i},\qquad [\hat X,\hat P]=\frac{i}{2}\ \Rightarrow\ \Delta X\,\Delta P\ge\frac14 .$$
Because $\hat X,\hat P$ do not commute, the field cannot have both quadratures
sharp. The **vacuum** saturates the bound with equal noise in each quadrature:
$$\langle0|(\Delta\hat X)^2|0\rangle=\langle0|(\Delta\hat P)^2|0\rangle=\frac14,\qquad \Delta X\,\Delta P=\frac14 .$$
This irreducible $\tfrac14$ is the zero-point fluctuation made measurable;
redistributing it unequally between the quadratures is **squeezing** (`~QO-05`). A
Fock state $|n\rangle$ has the larger isotropic noise $(2n+1)/4$. Code:
`quadrature_x`, `quadrature_p`, `quadrature_variance`, `expectation`.

## 4. Coherent states — the eigenstates of $\hat a$

The **coherent state** $|\alpha\rangle$ (Glauber) is defined as the eigenstate of
the (non-Hermitian) annihilation operator; expanded in Fock states it is a
specific superposition [SZ §2.2]:
$$|\alpha\rangle=e^{-|\alpha|^2/2}\sum_{n=0}^{\infty}\frac{\alpha^n}{\sqrt{n!}}\,|n\rangle,\qquad \hat a\,|\alpha\rangle=\alpha\,|\alpha\rangle .$$
The complex eigenvalue $\alpha$ *is* the classical amplitude of §1: $|\alpha\rangle$
is a "displaced vacuum", a minimum-uncertainty wavepacket riding the classical
orbit in the $(X,P)$ plane. Code: `coherent_state` (built from this series by the
stable recurrence $c_n=c_{n-1}\,\alpha/\sqrt{n}$, then renormalized); the test
`test_coherent_is_eigenstate_of_annihilation` confirms $\hat a|\alpha\rangle=\alpha|\alpha\rangle$
to $\sim10^{-16}$ away from the truncation.

## 5. Poissonian statistics — the "most classical" light

Reading off $|\langle n|\alpha\rangle|^2$ gives a **Poisson** photon-number
distribution, with mean fixed by the intensity [SZ §2.3–2.4]:
$$P(n)=\big|\langle n|\alpha\rangle\big|^2=e^{-|\alpha|^2}\frac{|\alpha|^{2n}}{n!},\qquad \langle\hat n\rangle=|\alpha|^2 .$$
The Poisson hallmark is that the variance equals the mean, so the **Mandel $Q$
parameter** vanishes:
$$(\Delta n)^2=\langle\hat n\rangle=|\alpha|^2,\quad \Delta n=\sqrt{\langle\hat n\rangle}=|\alpha|,\qquad Q\equiv\frac{(\Delta n)^2-\langle\hat n\rangle}{\langle\hat n\rangle}=0 .$$
$Q=0$ marks the boundary between classical-like light and **nonclassical** light:
$Q<0$ (sub-Poissonian, e.g. a Fock state has $Q=-1$) has no classical-field
description, while $Q>0$ (super-Poissonian, e.g. thermal) does. With equal,
vacuum-level quadrature noise ($\Delta X=\Delta P=\tfrac12$, §3) *and* Poisson
counting, coherent states are the **closest quantum states to a classical wave** —
which is why an ideal laser far above threshold, and the pump/Stokes fields in the
SBS work, are modelled as coherent states. Code: `photon_distribution`, `mean_n`,
`var_n`, `mandel_q`.

## Where this goes
- `~EM-15` — the classical electromagnetic modes whose amplitudes $\alpha$ are
  promoted to $\hat a,\hat a^\dagger$ here; `~QM-09` — the quantum SHO this *is*
  (bridge **B6**: $\sim$CM-15 $\to$ QM-09 $\to$ **QO-01** $\to$ QF-01).
- `~QF-01` — quantizing **every** mode (a field = infinitely many oscillators)
  turns $\hat a_{\mathbf k}, \hat a^\dagger_{\mathbf k}$ into particle
  creation/annihilation operators; QO-01 is the single-mode seed of second
  quantization.
- `~QO-02` — coupling this mode to a two-level atom (Rabi / Jaynes–Cummings);
  `~QO-05` — squeezing and nonclassical light, where the equal-quadrature noise of
  §3 is deliberately broken; `~QO-06` — nonlinear/Brillouin (SBS) scattering, where
  coherent pump and Stokes modes drive the user's SBS research.
