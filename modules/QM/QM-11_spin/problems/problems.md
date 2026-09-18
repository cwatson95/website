# QM-11 — Problems

Work them by hand, then check with `code/spin.py`. Sources in `../refs.md`.
Natural units $\hbar=1$ (as in the code).

### P1.  The Pauli algebra in one line  *(Griffiths 3e §4.4.1, p.215)*
Show that the single identity $\sigma_i\sigma_j=\delta_{ij}\mathbb 1+i\varepsilon_{ijk}\sigma_k$
implies both $\{\sigma_i,\sigma_j\}=2\delta_{ij}\mathbb 1$ (so $\sigma_i^2=\mathbb 1$)
and $[\sigma_i,\sigma_j]=2i\varepsilon_{ijk}\sigma_k$.
*Answer:* add and subtract the identity with $i\leftrightarrow j$; the symmetric
part (using $\varepsilon_{jik}=-\varepsilon_{ijk}$) is the anticommutator, the
antisymmetric part the commutator.
*Check:* `test_pauli_product_identity`, `test_pauli_anticommutator`,
`test_pauli_commutator`; e.g. `sigma_x@sigma_y` $=i\,$`sigma_z`.

**Solution.** Write the identity once and again with $i\leftrightarrow j$, using
$\delta_{ji}=\delta_{ij}$ and $\varepsilon_{jik}=-\varepsilon_{ijk}$:
$$\sigma_i\sigma_j=\delta_{ij}\mathbb 1+i\varepsilon_{ijk}\sigma_k,\qquad
\sigma_j\sigma_i=\delta_{ij}\mathbb 1-i\varepsilon_{ijk}\sigma_k.$$
Adding cancels the antisymmetric term: $\{\sigma_i,\sigma_j\}=\sigma_i\sigma_j+\sigma_j\sigma_i=2\delta_{ij}\mathbb 1$, so $\sigma_i^2=\mathbb 1$.
Subtracting cancels the $\delta$ term: $[\sigma_i,\sigma_j]=\sigma_i\sigma_j-\sigma_j\sigma_i=2i\varepsilon_{ijk}\sigma_k$.
For $i=x,j=y$ this gives $\sigma_x\sigma_y=\delta_{xy}\mathbb 1+i\varepsilon_{xyz}\sigma_z=i\sigma_z$, exactly the
`sigma_x@sigma_y` $=i\,$`sigma_z` checked in `test_pauli_product_identity`.

### P2.  Spin is the same algebra as orbital $L$  *(Griffiths 3e §4.4, p.212; Bethe p.14)*
From $\mathbf S=\tfrac\hbar2\boldsymbol\sigma$, verify $[S_x,S_y]=i\hbar S_z$ (and
cyclic) and $S^2=\tfrac34\hbar^2\mathbb 1$. Identify $\tfrac34$ as $s(s+1)$.
*Answer:* $[S_x,S_y]=\tfrac{\hbar^2}{4}[\sigma_x,\sigma_y]=\tfrac{\hbar^2}{4}(2i\sigma_z)
=i\hbar S_z$; $S^2=\tfrac{\hbar^2}{4}\cdot3\,\mathbb 1$, and $s(s+1)=\tfrac12\cdot\tfrac32=\tfrac34$.
This is `~QM-10`'s algebra at the $s=\tfrac12$ rung — verified by importing it.
*Check:* `test_spin_algebra`, `test_S_squared_is_three_quarter`,
`test_cross_check_QM10_angular_momentum_and_MA18`.

**Solution.** With $\mathbf S=\tfrac\hbar2\boldsymbol\sigma$ the spin commutator inherits the Pauli
commutator of P1:
$$[S_x,S_y]=\Big(\tfrac\hbar2\Big)^2[\sigma_x,\sigma_y]=\frac{\hbar^2}{4}\,(2i\sigma_z)
=i\hbar\Big(\tfrac\hbar2\sigma_z\Big)=i\hbar S_z,$$
and cyclically — the orbital algebra $[L_i,L_j]=i\hbar\varepsilon_{ijk}L_k$ verbatim. Using $\sigma_i^2=\mathbb 1$,
$$S^2=\tfrac{\hbar^2}{4}(\sigma_x^2+\sigma_y^2+\sigma_z^2)=\tfrac{\hbar^2}{4}\cdot3\,\mathbb 1=\tfrac34\hbar^2\mathbb 1.$$
Comparing with $S^2=\hbar^2 s(s+1)\mathbb 1$ gives $s(s+1)=\tfrac34$, i.e. $s=\tfrac12$ (since $\tfrac12\cdot\tfrac32=\tfrac34$).
This is `~QM-10`'s ladder at its half-integer rung, confirmed by `test_spin_algebra` and `test_S_squared_is_three_quarter`.

### P3.  Spin along an arbitrary axis  *(Griffiths 3e Problem 4.33, p.218)*
Construct $\hat{\mathbf n}\cdot\mathbf S$ for $\hat{\mathbf n}=(\sin\theta\cos\phi,
\sin\theta\sin\phi,\cos\theta)$ and find its $+\hbar/2$ eigenspinor.
*Answer:* $\hat{\mathbf n}\cdot\mathbf S=\tfrac\hbar2\!\begin{pmatrix}\cos\theta&\sin\theta e^{-i\phi}\\
\sin\theta e^{i\phi}&-\cos\theta\end{pmatrix}$, eigenvalues $\pm\hbar/2$ for every
direction (since $(\hat{\mathbf n}\cdot\boldsymbol\sigma)^2=\mathbb 1$);
$\chi_+=(\cos\tfrac\theta2,\,\sin\tfrac\theta2 e^{i\phi})$.
*Check:* `spin_operator_along(θ,φ) @ spin_eigenstate(θ,φ)` $=0.5\,$`spin_eigenstate(θ,φ)`.
(`test_n_dot_S_eigenstate`.)

**Solution.** Build $\hat{\mathbf n}\cdot\boldsymbol\sigma=n_x\sigma_x+n_y\sigma_y+n_z\sigma_z$; the
off-diagonal entries combine as $n_x\mp in_y=\sin\theta\,e^{\mp i\phi}$, so
$$\hat{\mathbf n}\cdot\mathbf S=\tfrac\hbar2\begin{pmatrix}\cos\theta&\sin\theta\,e^{-i\phi}\\
\sin\theta\,e^{i\phi}&-\cos\theta\end{pmatrix}.$$
Since $(\hat{\mathbf n}\cdot\boldsymbol\sigma)^2=n_in_j\sigma_i\sigma_j=|\hat{\mathbf n}|^2\mathbb 1=\mathbb 1$
(using P1), the eigenvalues are $\pm1$, i.e. $\pm\hbar/2$ for every direction. The top row of
$(\hat{\mathbf n}\cdot\mathbf S-\tfrac\hbar2)\chi=0$ reads $(\cos\theta-1)a+\sin\theta\,e^{-i\phi}b=0$, giving
$b/a=\tfrac{1-\cos\theta}{\sin\theta}e^{i\phi}=\tan\tfrac\theta2\,e^{i\phi}$, hence
$\chi_+=(\cos\tfrac\theta2,\ \sin\tfrac\theta2\,e^{i\phi})^T$. This is the spinor for which
`spin_operator_along(θ,φ) @ spin_eigenstate(θ,φ)` $=0.5\,$`spin_eigenstate(θ,φ)`.

### P4.  $\langle\mathbf S\rangle$ points along $\hat{\mathbf n}$ (the Bloch sphere)  *(Griffiths 3e p.216, 218)*
On $\chi_+^{(\hat{\mathbf n})}$, show $\langle\mathbf S\rangle=\tfrac\hbar2\hat{\mathbf n}$,
so the expectation has length $\hbar/2$ and points exactly along the prepared axis.
*Answer:* $\langle S_z\rangle=\tfrac\hbar2(\cos^2\tfrac\theta2-\sin^2\tfrac\theta2)=\tfrac\hbar2\cos\theta$,
$\langle S_x\rangle=\tfrac\hbar2\sin\theta\cos\phi$,
$\langle S_y\rangle=\tfrac\hbar2\sin\theta\sin\phi$ — the components of $\tfrac\hbar2\hat{\mathbf n}$.
*Check:* `test_expectation_is_half_n`; e.g.
`[expectation(o, spin_eigenstate(1.0,2.0)) for o in S]` $=0.5\,$`n_hat(1.0,2.0)`.

**Solution.** Write $\chi_+=(a,b)$ with $a=\cos\tfrac\theta2$, $b=\sin\tfrac\theta2\,e^{i\phi}$. For the
diagonal $\sigma_z$, $\langle\sigma_z\rangle=|a|^2-|b|^2=\cos^2\tfrac\theta2-\sin^2\tfrac\theta2=\cos\theta$, so
$\langle S_z\rangle=\tfrac\hbar2\cos\theta$. For the off-diagonal pair, $\chi^\dagger\sigma_x\chi=2\,\mathrm{Re}(a^*b)$ and
$\chi^\dagger\sigma_y\chi=2\,\mathrm{Im}(a^*b)$ with $a^*b=\cos\tfrac\theta2\sin\tfrac\theta2\,e^{i\phi}$:
$$\langle S_x\rangle=\tfrac\hbar2\sin\theta\cos\phi,\qquad
\langle S_y\rangle=\tfrac\hbar2\sin\theta\sin\phi,$$
using $2\cos\tfrac\theta2\sin\tfrac\theta2=\sin\theta$. Thus $\langle\mathbf S\rangle=\tfrac\hbar2\hat{\mathbf n}$ —
length $\hbar/2$, pointing along $\hat{\mathbf n}$ (the Bloch sphere). At $\theta=1,\phi=2$ the code returns
$\langle\mathbf S\rangle=(-0.1751,\,0.3826,\,0.2702)=0.5\,$`n_hat(1.0,2.0)`, matching `test_expectation_is_half_n`.

### P5.  The $\cos^2(\theta/2)$ measurement rule & Stern–Gerlach  *(Griffiths 3e p.215; Example 4.4, p.221)*
A particle is prepared spin-up along $\hat{\mathbf n}(\theta,\phi)$ and sent into a
$z$-oriented Stern–Gerlach magnet. What are the probabilities of the two beams?
*Answer:* $P(\uparrow_z)=|\langle\uparrow_z|\chi_+\rangle|^2=\cos^2(\theta/2)$ and
$P(\downarrow_z)=\sin^2(\theta/2)$ — independent of $\phi$, summing to 1. The beam
splits into exactly **two** ($2s+1$) spots: angular momentum is quantized.
*Check:* `prob_up_z(spin_eigenstate(θ,φ))` $=\cos^2(θ/2)$;
`born_probabilities(Sz, spin_eigenstate(θ,φ))`. (`test_probability_cos_squared`,
`test_stern_gerlach_born_probabilities`.)

**Solution.** The prepared state is $\chi_+=(\cos\tfrac\theta2,\ \sin\tfrac\theta2\,e^{i\phi})$ from P3, and the
$S_z$ "up" eigenstate is $\uparrow_z=(1,0)$. The Born rule gives the amplitude as the inner product
$$\langle\uparrow_z|\chi_+\rangle=\cos\tfrac\theta2\ \Rightarrow\ P(\uparrow_z)=\big|\cos\tfrac\theta2\big|^2=\cos^2\tfrac\theta2,$$
and likewise $P(\downarrow_z)=|\sin\tfrac\theta2\,e^{i\phi}|^2=\sin^2\tfrac\theta2$. The phase $e^{i\phi}$ drops out of
the modulus, so the result is $\phi$-independent, and $\cos^2\tfrac\theta2+\sin^2\tfrac\theta2=1$. Only **two** outcomes
occur — the $2s+1=2$ Stern–Gerlach spots. For $\theta=1$, $\cos^2(0.5)=0.7702$, which is what
`prob_up_z(spin_eigenstate(1.0,2.0))` and `born_probabilities(Sz, …)` return ($\{+\hbar/2:0.7702,\,-\hbar/2:0.2298\}$).

### P6.  Larmor precession  *(Griffiths 3e Example 4.3, p.219–220)*
A spin tilted at angle $\alpha$ to a field $\mathbf B=B_0\hat{\mathbf z}$ evolves
under $H=-\gamma\,\mathbf B\cdot\mathbf S$. Find $\langle\mathbf S\rangle(t)$ and
the precession frequency.
*Answer:* $\langle S_x\rangle=\tfrac\hbar2\sin\alpha\cos\omega t$,
$\langle S_y\rangle=-\tfrac\hbar2\sin\alpha\sin\omega t$,
$\langle S_z\rangle=\tfrac\hbar2\cos\alpha$ (constant), with the **Larmor
frequency** $\omega=\gamma B_0$ — a cone precessing about $\mathbf B$.
*Check:* `spin_expectations(hamiltonian_field(γ,[0,0,B0]), spin_eigenstate(α,0), t)`
vs the closed forms; `larmor_frequency(γ,B0)`. (`test_larmor_precession_closed_form`,
`test_larmor_cone_and_period`.)

**Solution.** With $\mathbf B=B_0\hat{\mathbf z}$, $H=-\gamma B_0 S_z=-\tfrac{\gamma B_0\hbar}{2}\sigma_z$, so the
propagator is diagonal: $U(t)=e^{-iHt/\hbar}=\mathrm{diag}(e^{i\omega t/2},e^{-i\omega t/2})$ with $\omega\equiv\gamma B_0$.
Acting on the tilted initial spinor $\chi(0)=(\cos\tfrac\alpha2,\ \sin\tfrac\alpha2)$,
$$\chi(t)=\big(\cos\tfrac\alpha2\,e^{i\omega t/2},\ \sin\tfrac\alpha2\,e^{-i\omega t/2}\big).$$
This is the P3/P5 spinor with $\theta=\alpha$ and azimuth $\phi=-\omega t$. Substituting into $\langle\mathbf S\rangle=\tfrac\hbar2\hat{\mathbf n}$:
$$\langle S_x\rangle=\tfrac\hbar2\sin\alpha\cos\omega t,\quad
\langle S_y\rangle=-\tfrac\hbar2\sin\alpha\sin\omega t,\quad
\langle S_z\rangle=\tfrac\hbar2\cos\alpha.$$
So $\langle\mathbf S\rangle$ precesses on a cone of half-angle $\alpha$ at $\omega=\gamma B_0$; for $\gamma=2,B_0=3$,
`larmor_frequency(2,3)` $=6$, matching `test_larmor_precession_closed_form`.

### P7.  Driven two-level: Rabi oscillations  *(Griffiths 3e Problem 4.36, p.222)*
A two-level system starts in the lower level and is driven with Rabi coupling
$\Omega$ at detuning $\Delta$. Find the probability of finding it in the upper
level, and the largest transfer achievable off resonance.
*Answer:* $P_\uparrow(t)=\dfrac{\Omega^2}{\Omega_R^2}\sin^2\!\dfrac{\Omega_R t}{2}$,
$\Omega_R=\sqrt{\Omega^2+\Delta^2}$. On resonance ($\Delta=0$) it reaches 1 (a
$\pi$-pulse at $t=\pi/\Omega$); off resonance it saturates at
$\Omega^2/(\Omega^2+\Delta^2)<1$.
*Check:* `rabi_probability(np.pi,1,0)` $=1$; max of `rabi_probability(·,1,1.5)`
$=\Omega^2/\Omega_R^2$; and `evolve(rabi_hamiltonian(Ω,Δ), down_z, t)` projected on
`up_z` matches the formula. (`test_rabi_resonant_full_inversion`,
`test_rabi_detuned_amplitude`, `test_rabi_matches_time_evolution`.)

**Solution.** In the rotating frame $H=\tfrac\hbar2(\Delta\sigma_z+\Omega\sigma_x)$ has eigenvalues
$\pm\tfrac\hbar2\Omega_R$ with $\Omega_R=\sqrt{\Omega^2+\Delta^2}$. Evolving $|\!\downarrow\rangle$ and projecting on
$|\!\uparrow\rangle$ gives the Rabi formula
$$P_\uparrow(t)=\frac{\Omega^2}{\Omega_R^2}\sin^2\!\Big(\frac{\Omega_R t}{2}\Big).$$
On resonance $\Delta=0\Rightarrow\Omega_R=\Omega$, so $P_\uparrow=\sin^2(\Omega t/2)$ reaches $1$ at $t=\pi/\Omega$ (a
$\pi$-pulse): `rabi_probability(np.pi,1,0)` $=1.0$. Off resonance the prefactor caps the flop at
$\Omega^2/\Omega_R^2<1$; for $\Omega=1,\Delta=1.5$ the maximum is $1/(1+1.5^2)=1/3.25=0.3077$, matching
`test_rabi_detuned_amplitude`.

### P8.  A spinor needs $720^\circ$  *(Griffiths 3e §4.4; Sakurai Ch. 3; ~MA-18)*
Using $R_{\hat{\mathbf n}}(\theta)=e^{-i\theta\,\hat{\mathbf n}\cdot\boldsymbol\sigma/2}$,
evaluate $R(2\pi)$ and $R(4\pi)$. Why isn't $R(2\pi)=\mathbb 1$?
*Answer:* $R(\theta)=\cos\tfrac\theta2\,\mathbb 1-i\sin\tfrac\theta2\,(\hat{\mathbf n}\cdot\boldsymbol\sigma)$,
so $R(2\pi)=-\mathbb 1$ and $R(4\pi)=+\mathbb 1$: a $360^\circ$ rotation flips the
spinor's sign. Spinors carry a rep of $SU(2)$, the double cover of the rotation
group $SO(3)$ (`~MA-18`); the sign is unobservable in isolation but visible in
interference.
*Check:* `np.allclose(rotation(2*np.pi), -I2)`, `np.allclose(rotation(4*np.pi), I2)`.
(`test_rotation_double_cover`.)

**Solution.** Because $(\hat{\mathbf n}\cdot\boldsymbol\sigma)^2=\mathbb 1$, the exponential splits into even and
odd powers exactly like $e^{-i\theta/2}$ for a number:
$$R_{\hat{\mathbf n}}(\theta)=e^{-i\theta(\hat{\mathbf n}\cdot\boldsymbol\sigma)/2}
=\cos\tfrac\theta2\,\mathbb 1-i\sin\tfrac\theta2\,(\hat{\mathbf n}\cdot\boldsymbol\sigma).$$
The half-angle is the whole story. At $\theta=2\pi$: $\cos\pi=-1,\ \sin\pi=0$, so $R(2\pi)=-\mathbb 1$;
at $\theta=4\pi$: $\cos2\pi=1,\ \sin2\pi=0$, so $R(4\pi)=+\mathbb 1$. A $360^\circ$ rotation flips the spinor's
sign — it takes $720^\circ$ to return — because spinors carry a representation of $SU(2)$, the double cover of
$SO(3)$ (`~MA-18`). This is exactly `np.allclose(rotation(2*np.pi), -I2)` and `np.allclose(rotation(4*np.pi), I2)`.
