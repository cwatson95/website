# QM-11 — Spin & Two-Level Systems (notes)

Spin is angular momentum that is **not** $\mathbf r\times\mathbf p$. In `~QM-10`
the algebra $[L_i,L_j]=i\hbar\varepsilon_{ijk}L_k$ allowed $l=0,\tfrac12,1,\dots$
— integer *or* half-integer — but the position-space realization $Y_l^m\propto
e^{im\phi}$ demanded single-valuedness and so killed the half-integer rungs. Spin
is exactly what is left of those rungs: an intrinsic angular momentum carried by a
structureless point particle, with **matrices but no wavefunction** (Griffiths 3e
§4.4, p.212). The smallest case, $s=\tfrac12$, is a genuine **two-level system**,
the workhorse of atomic physics, NMR, and quantum information.

Throughout, $\hbar$ is kept explicit in the formulae; the code uses natural units
$\hbar=1$ (documented in `spin.py`).

## 1. Spin: angular momentum without space

"The theory of spin is a carbon copy of the theory of orbital angular momentum"
(Griffiths 3e §4.4, p.212): copy `~QM-10` verbatim but **drop the differential
operators**. Keep only the algebra
$$\boxed{\,[S_x,S_y]=i\hbar S_z,\qquad[S_y,S_z]=i\hbar S_x,\qquad[S_z,S_x]=i\hbar S_y\,}$$
(Griffiths Eq. 4.134), the Casimir $S^2=S_x^2+S_y^2+S_z^2$ with
$$S^2|s\,m\rangle=\hbar^2 s(s+1)\,|s\,m\rangle,\qquad
S_z|s\,m\rangle=\hbar m\,|s\,m\rangle,$$
and the ladder $S_\pm=S_x\pm iS_y$, $S_\pm|s\,m\rangle=\hbar\sqrt{s(s+1)-m(m\pm1)}\,
|s,m\pm1\rangle$ (Griffiths Eq. 4.135–4.137). The number $s$ is fixed once and for
all for a given particle (the electron, proton, neutron all have $s=\tfrac12$); it
is not a dynamical variable. *(The code verifies the algebra and $S^2$ to machine
precision in `test_spin_algebra`, `test_S_squared_is_three_quarter`.)*

## 2. Spin-½: the Pauli matrices

For $s=\tfrac12$ there are exactly **two** states, $|\tfrac12,+\tfrac12\rangle\equiv
\;\uparrow$ and $|\tfrac12,-\tfrac12\rangle\equiv\;\downarrow$ (Griffiths 3e
§4.4.1, p.214). A general state is a two-component **spinor**
$$\chi=\binom{a}{b}=a\binom{1}{0}+b\binom{0}{1}=a\chi_++b\chi_-,\qquad|a|^2+|b|^2=1.$$
Working out the action of $S^2,S_z,S_\pm$ on $\chi_\pm$ turns the operators into
$2\times2$ matrices (Griffiths p.214–215). It is tidiest to factor out the common
$\hbar/2$:
$$\boxed{\,\mathbf S=\frac{\hbar}{2}\,\boldsymbol\sigma,\qquad
\sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\;
\sigma_y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\;
\sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}\,}$$
— the **Pauli matrices** (Griffiths Eq. 4.147–4.148, p.215). They are Hermitian,
traceless, and unitary, with $\det\sigma_i=-1$. Their entire algebra collapses to
one identity:
$$\boxed{\,\sigma_i\sigma_j=\delta_{ij}\,\mathbb 1+i\,\varepsilon_{ijk}\,\sigma_k\,}$$
Taking the symmetric and antisymmetric parts recovers the two relations one uses
constantly:
$$\{\sigma_i,\sigma_j\}=2\delta_{ij}\,\mathbb 1\quad(\text{so }\sigma_i^2=\mathbb 1),
\qquad[\sigma_i,\sigma_j]=2i\,\varepsilon_{ijk}\sigma_k.$$
The second, times $(\hbar/2)^2$, is the spin algebra of §1; the Pauli matrices are
the **su(2) generators** of `~MA-18`. And
$$S^2=\frac{\hbar^2}{4}(\sigma_x^2+\sigma_y^2+\sigma_z^2)=\frac{3}{4}\hbar^2\,\mathbb 1
=\hbar^2\,s(s+1)\,\mathbb 1\big|_{s=1/2},$$
the whole space being one $s=\tfrac12$ multiplet. *(All of §2:
`test_pauli_product_identity`, `test_pauli_anticommutator`,
`test_pauli_commutator`, `test_spin_operators_are_half_sigma_and_hermitian`.)*

## 3. Spin along an arbitrary axis $\hat{\mathbf n}$

The eigenstates of $S_z$ are $\chi_+=(1,0)^T$ and $\chi_-=(0,1)^T$ with
eigenvalues $\pm\hbar/2$. What about the component along a general unit vector
$\hat{\mathbf n}=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta)$? The operator is
$$\hat{\mathbf n}\cdot\mathbf S=\frac{\hbar}{2}\,\hat{\mathbf n}\cdot\boldsymbol\sigma
=\frac{\hbar}{2}\begin{pmatrix}\cos\theta&\sin\theta\,e^{-i\phi}\\
\sin\theta\,e^{i\phi}&-\cos\theta\end{pmatrix}.$$
Because $(\hat{\mathbf n}\cdot\boldsymbol\sigma)^2=\mathbb 1$ (from §2), its
eigenvalues are again $\pm\hbar/2$ for **every** direction. The normalized
$+\hbar/2$ eigenspinor is (Griffiths 3e Problem 4.33, p.218)
$$\boxed{\,\chi_+^{(\hat{\mathbf n})}=\binom{\cos(\theta/2)}{\sin(\theta/2)\,e^{i\phi}}\,}\qquad
\chi_-^{(\hat{\mathbf n})}=\binom{\sin(\theta/2)}{-\cos(\theta/2)\,e^{i\phi}}.$$
On this state $\langle\hat{\mathbf n}\cdot\mathbf S\rangle=+\hbar/2$ and, component
by component, $\langle\mathbf S\rangle=\tfrac{\hbar}{2}\hat{\mathbf n}$ — the
expectation points exactly along $\hat{\mathbf n}$, half a unit long (the **Bloch
sphere** picture). The half-angle $\theta/2$ is the fingerprint of spin-$\tfrac12$:
a *spatial* rotation by $\theta$ rotates the spinor by $\theta/2$. *(`test_n_dot_S_eigenstate`, `test_expectation_is_half_n`.)*

### Measurement and the $\cos^2(\theta/2)$ rule
Prepare $\chi_+^{(\hat{\mathbf n})}$, then measure $S_z$. By the Born rule the
probability of "up" is
$$\boxed{\,P(\uparrow_z)=|\langle\uparrow_z|\chi_+^{(\hat{\mathbf n})}\rangle|^2
=\cos^2(\theta/2),\qquad P(\downarrow_z)=\sin^2(\theta/2)\,}$$
(Griffiths 3e p.215; angle $\theta$ between the prepared axis and $z$). At
$\theta=0$ the result is certain ($P=1$); at $\theta=\pi/2$ it is fifty–fifty; at
$\theta=\pi$ it is certainly down. These are the only two outcomes — there is no
"in between" — which is precisely what the **Stern–Gerlach** experiment shows:
a beam of spin-$\tfrac12$ atoms in an inhomogeneous field splits into **$2s+1=2$**
discrete spots, not a classical smear (Griffiths 3e Example 4.4, p.221). A
Stern–Gerlach magnet *is* a measurement of $\hat{\mathbf n}\cdot\mathbf S$ (the
`~QM-06` postulates made concrete). *(`test_probability_cos_squared`,
`test_stern_gerlach_born_probabilities`.)*

## 4. A spin in a magnetic field — Larmor precession

A charged spinning particle is a magnetic dipole $\boldsymbol\mu=\gamma\mathbf S$,
with $\gamma$ the **gyromagnetic ratio** (Griffiths 3e Eq. 4.156, p.219). In a
field $\mathbf B$ its energy is $-\boldsymbol\mu\cdot\mathbf B$, so
$$\boxed{\,H=-\boldsymbol\mu\cdot\mathbf B=-\gamma\,\mathbf B\cdot\mathbf S\,}$$
(Griffiths Eq. 4.158). Take $\mathbf B=B_0\hat{\mathbf z}$: then
$H=-\gamma B_0 S_z=-\tfrac{\gamma B_0\hbar}{2}\sigma_z$, with eigenstates
$\chi_\pm$ and energies $E_\pm=\mp\tfrac{\gamma B_0\hbar}{2}$ (spin parallel to
$\mathbf B$ is lowest, just as classically). Start tilted at angle $\alpha$ to
$z$, $\chi(0)=\big(\cos\tfrac\alpha2,\ \sin\tfrac\alpha2\big)^T$, and evolve with
$|\chi(t)\rangle=e^{-iHt/\hbar}|\chi(0)\rangle$. The expectation values are
$$\boxed{\;\langle S_x\rangle=\frac{\hbar}{2}\sin\alpha\cos(\omega t),\quad
\langle S_y\rangle=-\frac{\hbar}{2}\sin\alpha\sin(\omega t),\quad
\langle S_z\rangle=\frac{\hbar}{2}\cos\alpha\;}$$
with the **Larmor frequency**
$$\boxed{\,\omega=\gamma B_0\,}$$
(Griffiths 3e Eq. 4.163–4.167, p.220, Fig. 4.14). So $\langle\mathbf S\rangle$
keeps a fixed angle $\alpha$ to the field and **precesses** about it at $\omega$,
tracing a cone — exactly the classical motion of a gyroscope, guaranteed here by
Ehrenfest's theorem. The transverse spin rotates ($\langle S_x\rangle^2+\langle
S_y\rangle^2$ is a constant circle) while $\langle S_z\rangle$ is frozen, and
everything repeats with period $2\pi/\omega$. The level splitting
$\Delta E=\hbar\omega=\gamma B_0\hbar$ is the resonance frequency NMR/ESR drive. *(`test_larmor_precession_closed_form`, `test_larmor_cone_and_period`,
`test_evolution_is_unitary_and_matches_ode` — the last checks the matrix
exponential against a `solve_ivp` integration of $i\hbar\,\dot\chi=H\chi$.)*

## 5. Driving the two-level system — Rabi oscillations

Add a resonant drive. In the rotating frame the two-level Hamiltonian is
$H=\tfrac{\hbar}{2}\big(\Delta\,\sigma_z+\Omega\,\sigma_x\big)=\Delta S_z+\Omega S_x$,
with **Rabi coupling** $\Omega$ (drive strength) and **detuning** $\Delta$ (drive
minus transition frequency). Starting in the lower level, the upper-level
probability is the **Rabi formula**
$$\boxed{\,P_{\uparrow}(t)=\frac{\Omega^2}{\Omega_R^2}\,\sin^2\!\Big(\frac{\Omega_R t}{2}\Big),
\qquad \Omega_R=\sqrt{\Omega^2+\Delta^2}\,}$$
($\Omega_R$ = generalized Rabi frequency). On resonance ($\Delta=0$) the amplitude
is $1$: a **complete population inversion** every $t=\pi/\Omega$ (a "$\pi$-pulse").
Off resonance the flop never finishes — it saturates at
$\Omega^2/(\Omega^2+\Delta^2)<1$ — and oscillates faster, at $\Omega_R$. This is
the engine of magnetic resonance and of single-qubit gates, and is the
rotating-field problem of Griffiths 3e Problem 4.36 (p.222). *(`test_rabi_resonant_full_inversion`, `test_rabi_detuned_amplitude`,
`test_rabi_matches_time_evolution` — closed form vs. genuine evolution of
$|\!\downarrow\rangle$ under $H$.)*

## 6. A spinor takes 720° to come home

Spatial rotations act on spinors through
$R_{\hat{\mathbf n}}(\theta)=e^{-i\theta(\hat{\mathbf n}\cdot\boldsymbol\sigma)/2}
=\cos\tfrac\theta2\,\mathbb 1-i\sin\tfrac\theta2\,(\hat{\mathbf n}\cdot\boldsymbol\sigma)$.
The half-angle has a famous consequence:
$$R_{\hat{\mathbf n}}(2\pi)=-\mathbb 1,\qquad R_{\hat{\mathbf n}}(4\pi)=+\mathbb 1.$$
A full $360^\circ$ rotation multiplies the spinor by $-1$; you must turn through
$720^\circ$ to get back to the start. This is the **two-to-one cover
$SU(2)\to SO(3)$** of `~MA-18`: spinors are representations of $SU(2)$, not of the
rotation group itself. *(`test_rotation_double_cover`.)*

---
### Why this matters in the trunk
Spin is the first physical system with **no classical wavefunction** — pure
algebra realized as $2\times2$ matrices — and it is the template for every qubit.
- It is the half-integer rung of `~QM-10` (verified in code: `~QM-10`'s $l=\tfrac12$
  matrices *are* $\mathbf S=\tfrac{\hbar}{2}\boldsymbol\sigma$), built on the
  su(2) of `~MA-18`.
- Stern–Gerlach makes the `~QM-06` measurement postulates tangible.
- It feeds `~QM-13` (adding the electron and proton spins gives the singlet and
  triplet; Clebsch–Gordan) and `~QM-17` (spin–orbit coupling $\propto\mathbf
  S\cdot\mathbf L$ and the Zeeman effect — fine structure).
- Classically the lineage is bridge **B3**: `~CM-09` (conserved $\mathbf L$) →
  `~QM-10/QM-11`. The lesson repeats: *fix the commutators, and the physics is
  forced* — here, into a single qubit.
