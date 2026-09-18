# QF-05 — QFT in Curved Spacetime — Hawking & Unruh Effects (notes)

The deepest lesson of quantum field theory in a gravitational field is that the
**vacuum is observer-dependent**. In flat space with inertial observers there is a
preferred set of positive-frequency modes and everyone agrees on what "no particles"
means. Remove that privilege — accelerate the observer, or curve the spacetime — and
the question *"how many particles are there?"* no longer has a single answer. The
machine that translates between two observers' notions of particle is the
**Bogoliubov transformation**, and its off-diagonal coefficients are, quite
literally, particles: an accelerated observer finds the inertial vacuum **hot**
(Unruh), and a black hole radiates its horizon away as a thermal body (Hawking).

Citation key (full details in `refs.md`): **BD** = Birrell & Davies, *Quantum
Fields in Curved Space* (Bogoliubov Ch. 2–3, Unruh Ch. 4, black holes Ch. 8);
**Ful** = Fulling, *Aspects of QFT in Curved Space-Time*. Conventions: SI units in
code, signature $(-,+,+,+)$, angular frequency $\omega$ so $\hbar\omega$ is an energy.

## 1. The vacuum is observer-dependent — Bogoliubov transformations
A free field is a sum of oscillators, but *which* oscillators depends on the chosen
complete set of solutions. Expand the **same** field $\phi$ in two complete sets of
positive-frequency modes, $\{u_k\}$ (operators $a_k$) and $\{u'_j\}$ (operators
$a'_j$) [BD §2.2–3.2]:
$$\phi=\sum_k\big(a_k\,u_k+a_k^\dagger u_k^*\big)=\sum_j\big(a'_j\,u'_j+a^{\prime\dagger}_j u^{\prime *}_j\big).$$
Because both sets are complete, one expands in the other,
$u'_j=\sum_k(\alpha_{jk}u_k+\beta_{jk}u_k^*)$, and the operators mix accordingly — the
**Bogoliubov transformation**:
$$\begin{aligned}
a'_j&=\sum_k\big(\alpha_{jk}^*\,a_k-\beta_{jk}^*\,a_k^\dagger\big),\\
\text{canonical}\ \ [a'_j,a^{\prime\dagger}_{j'}]=\delta_{jj'}\ &\Longleftrightarrow\
\sum_k\big(\alpha_{jk}\alpha_{j'k}^*-\beta_{jk}\beta_{j'k}^*\big)=\delta_{jj'} .
\end{aligned}$$
The single-mode shadow of that normalization, $|\alpha|^2-|\beta|^2=1$, is what keeps
the new operators canonical. Code: `bogoliubov_check` returns $\sum_k|\alpha_{jk}|^2-\sum_k|\beta_{jk}|^2$ (must be $1$).

## 2. Particle creation and the squeezed vacuum
The $\beta$ coefficients are the entire story. If $\beta_{jk}=0$ the two observers
share a vacuum; if any $\beta_{jk}\neq0$ the $a$-vacuum $|0\rangle$ is **full of
$a'$-particles**. The number the primed observer counts in the unprimed vacuum is
$$\langle 0|\,N'_j\,|0\rangle=\langle 0|\,a^{\prime\dagger}_j a'_j\,|0\rangle=\sum_k|\beta_{jk}|^2 .$$
Code: `particle_number(beta)` $=\sum_k|\beta_k|^2$. There is a beautiful optical
reading of this (the bridge to the user's squeezed-spacetimes work, `~QO-05`): a
single pair of mixed modes is a **two-mode squeezer**. Parametrize
$$\alpha=\cosh r,\qquad \beta=\sinh r\ \Rightarrow\ |\alpha|^2-|\beta|^2=1,\quad
\langle N\rangle=\sinh^2 r,$$
so the rotated vacuum is a *squeezed vacuum* whose photon number grows with the
squeeze parameter $r$. Code: `squeeze_to_bogoliubov(r)` returns $(\cosh r,\sinh r)$;
`bogoliubov_check` confirms the norm and `particle_number` gives $\sinh^2 r$.

## 3. The Unruh effect — acceleration is temperature
Take Minkowski space and a uniformly accelerated observer (proper acceleration $a$),
whose natural coordinates are Rindler's. Their positive-frequency modes are *not*
Minkowski's, so the Bogoliubov $\beta\neq0$ and the inertial vacuum looks populated.
The remarkable fact [BD §4.5; Ful] is that the population is exactly **thermal**, at
the **Unruh temperature**
$$\boxed{\,T_U=\frac{\hbar\,a}{2\pi c\,k_B}\,}\qquad(\texttt{unruh\_temperature}),$$
*linear* in the acceleration. The scale is brutal: $T_U$ reaches $1\,$K only near
$a\sim2.5\times10^{20}\,\mathrm{m/s^2}$ (the demo uses $a=10^{20}$, giving
$T_U\approx0.405\,$K); everyday $g$ gives $\sim10^{-20}\,$K. The vacuum is a heat
bath you can only feel if you shake it hard enough.

## 4. The thermal spectrum from Bogoliubov mixing
Why *thermal*? For a Rindler mode of frequency $\omega$ the Minkowski-vs-Rindler
Bogoliubov coefficients obey a detailed-balance relation,
$$\frac{|\beta_\omega|^2}{|\alpha_\omega|^2}=e^{-2\pi c\,\omega/a}\qquad(\texttt{unruh\_beta\_ratio}),$$
which is the only extra ingredient. Feed it through the normalization
$|\alpha_\omega|^2-|\beta_\omega|^2=1$ and the occupation collapses onto the
**Planck/Bose–Einstein** law:
$$\langle n_\omega\rangle=|\beta_\omega|^2=\frac{e^{-2\pi c\omega/a}}{1-e^{-2\pi c\omega/a}}
=\frac{1}{\,e^{\,\hbar\omega/k_BT_U}-1\,}\qquad(\texttt{unruh\_occupation}).$$
The exponent $2\pi c\omega/a$ is precisely $\hbar\omega/k_BT_U$ — the Bogoliubov
ratio *defines* the temperature. Code: `unruh_occupation(omega, a)` reproduces
`bose_occupation(omega, unruh_temperature(a))` to machine precision, and the generic
spectrum builder `thermal_beta_squared(omega, T, 'bose')` returns the same
$1/(e^{\hbar\omega/k_BT}-1)$ (use `'fermi'` for $+1$).

## 5. Hawking radiation — black holes are hot
The same mechanism, with a genuine horizon, is **Hawking radiation** [BD Ch. 8].
Field modes that fall toward a collapsing star are gravitationally redshifted as
they climb back out past the forming horizon; the ingoing/outgoing mode bases are
related by a Bogoliubov transformation whose $\beta$ is again thermal. The
temperature is set by the **surface gravity** $\kappa=c^4/(4GM)=c^2/(2r_s)$ of the
Schwarzschild horizon ($r_s=2GM/c^2$, `~RE-14`):
$$\boxed{\,T_H=\frac{\hbar\kappa}{2\pi c\,k_B}=\frac{\hbar c^3}{8\pi G M\,k_B}\,}\qquad(\texttt{hawking\_temperature}),$$
*inversely* proportional to mass. A solar-mass hole has $T_H\approx6.2\times10^{-8}\,$K
— far colder than the $2.7\,$K CMB, so astrophysical holes absorb more than they
emit — while a $1\,$kg hole would glow at $\sim10^{23}\,$K. The emitted spectrum is a
greybody-modulated Planck spectrum,
$$\langle n_\omega\rangle=\frac{\Gamma_\omega}{\,e^{\,\hbar\omega/k_BT_H}-1\,},$$
with $\Gamma_\omega$ the horizon transmission (greybody) factor; dropping $\Gamma_\omega$
recovers the exact blackbody `bose_occupation` at $T_H$. Code: `surface_gravity`,
`schwarzschild_radius`, `hawking_temperature`. The stress-energy that back-reacts on
the metric is the `~RE-13` source.

## 6. Evaporation and the information puzzle
A radiating hole loses energy, hence mass. Equating the Hawking luminosity (Stefan–
Boltzmann, $L=\sigma A T_H^4$ with $A=4\pi r_s^2\propto M^2$ and $T_H\propto1/M$) to
$-c^2\dot M$ gives a mass that runs *away* from equilibrium — the smaller it gets,
the hotter and faster it burns:
$$\frac{dM}{dt}=-\frac{\hbar c^4}{15360\,\pi G^2 M^2}\ \Longrightarrow\
\boxed{\,\tau=\frac{5120\,\pi G^2 M^3}{\hbar c^4}\propto M^3\,}\qquad(\texttt{evaporation\_lifetime}).$$
For $M_\odot$ this is $\tau\approx6.6\times10^{74}\,\mathrm{s}\approx2\times10^{67}\,$yr;
a primordial $10^{11}\,$kg hole would be expiring now. The endpoint — where $T_H$
diverges and a thermal, apparently information-free state is all that remains — is
the **black-hole information paradox**, the open problem this whole module leads to.

## Where this goes
- `~RE-14` — the Schwarzschild horizon, $r_s=2M$ and surface gravity $\kappa$, supplied here in SI; the redshift-to-the-horizon picture is the classical seed of Hawking's $\beta$.
- `~RE-13` — the Einstein equations and the stress-energy tensor $\langle T_{\mu\nu}\rangle$ that back-reacts as the hole evaporates.
- `~QF-01` — canonical quantization and the very definition of "the vacuum" that this module shows is not unique.
- `~QO-05` — squeezing and two-mode squeezed vacua: the horizon as a squeezer is the technology behind the user's **Quantum_Optics curved-spacetime / squeezed-spacetimes** drafts.
