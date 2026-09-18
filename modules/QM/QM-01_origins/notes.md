# QM-01 — Origins of Quantum Theory (notes)

Classical physics by 1900 was two pillars: Newtonian mechanics and Maxwell's
electromagnetism. Four experiments could not be made to fit, and each forced one
quantum idea. The thread tying them together is a single new constant, **Planck's
constant** $h = 6.626\times10^{-34}\,\mathrm{J\,s}$: action comes in lumps.

## 1. Black-body radiation — energy is quantized

A black body in thermal equilibrium radiates a spectrum that depends only on its
temperature. Classically (equipartition over the cavity modes) one gets the
**Rayleigh–Jeans law**
$$u(\nu,T)=\frac{8\pi\nu^2}{c^3}\,k_BT,$$
which **diverges** as $\nu\to\infty$: the *ultraviolet catastrophe* (infinite
total energy). Planck (1900) fixed it by assuming each mode exchanges energy only
in quanta $E=h\nu$, giving
$$\boxed{\,u(\nu,T)=\frac{8\pi h\nu^3}{c^3}\,\frac{1}{e^{h\nu/k_BT}-1}\,}$$
- $h\nu\ll k_BT$: $e^x-1\to x$ recovers Rayleigh–Jeans (`rayleigh_jeans_u_nu`).
- $h\nu\gg k_BT$: $e^x-1\to e^x$ gives Wien's law (`wien_u_nu`).

Two classical laws are now *theorems*, recovered here numerically:
- **Stefan–Boltzmann:** $\int_0^\infty u\,d\nu = aT^4$ with
  $a=\frac{8\pi^5k_B^4}{15h^3c^3}=\frac{4\sigma}{c}$. Integrating $x^3/(e^x-1)$
  (value $\pi^4/15$) gives $\sigma=5.6704\times10^{-8}$ — see
  `stefan_boltzmann_sigma()`.
- **Wien displacement:** the peak of $B_\lambda$ obeys $\lambda_{\max}T=b$,
  $b=2.898\times10^{-3}\,\mathrm{m\,K}$, where $x=hc/\lambda k_BT$ solves
  $x=5(1-e^{-x})$, $x\approx4.965$ — see `wien_displacement_b()`. (The Sun,
  $T=5772$ K, peaks at $\sim$502 nm — green.)

## 2. Photoelectric effect — light is quantized (the photon)

Light on a metal ejects electrons, but only above a **threshold frequency**, and
the electron energy depends on *frequency*, not *intensity* — impossible for a
classical wave. Einstein (1905): light itself is quantized into photons $E=h\nu$,
so
$$\boxed{\,K_{\max}=h\nu-W\,}$$
$W$ = work function (binding energy at the surface). Below $f_0=W/h$ nothing is
emitted no matter how bright (`photoelectric_Kmax` clamps to 0). The stopping
voltage $V_s=K_{\max}/e$ vs $\nu$ is a straight line of **slope $h/e$** — this is
how Millikan measured $h$ (the test checks $dK_{\max}/d\nu=h$).

## 3. Bohr model — angular momentum is quantized

Rutherford's nuclear atom is classically unstable (the orbiting electron should
radiate and spiral in). Bohr (1913) postulated stationary orbits with quantized
angular momentum $L=n\hbar$, giving
$$E_n=-\frac{m_ee^4}{8\varepsilon_0^2h^2}\frac{Z^2}{n^2}=-13.606\,\frac{Z^2}{n^2}\ \mathrm{eV},
\qquad r_n=\frac{n^2}{Z}a_0,\quad a_0=\frac{4\pi\varepsilon_0\hbar^2}{m_ee^2}.$$
Transitions $n_2\to n_1$ emit photons $h\nu=E_{n_2}-E_{n_1}$, i.e. the **Rydberg
formula**
$$\frac1\lambda=RZ^2\!\left(\frac1{n_1^2}-\frac1{n_2^2}\right),\qquad
R=\frac{m_ee^4}{8\varepsilon_0^2h^3c}=1.097\times10^7\ \mathrm{m^{-1}}.$$
$n_1=1$ Lyman (UV), $n_1=2$ Balmer (visible: H$\alpha$ $3\to2$ = 656 nm),
$n_1=3$ Paschen (IR). The code rebuilds $a_0$, $E_1=-13.6$ eV and the line
wavelengths from constants. *(Bohr's quantization is provisional — `~QM-12`
replaces it with the Schrödinger hydrogen atom, which gives the same $E_n$ for
the right reason.)*

## 4. de Broglie waves — matter is wavelike

If light (a wave) carries momentum $p=E/c=h\nu/c=h/\lambda$, de Broglie (1924)
proposed the symmetric statement for matter:
$$\boxed{\,\lambda=\frac{h}{p}\,}$$
(Griffiths 3e §1.6.) For a non-relativistic particle of kinetic energy $E$,
$p=\sqrt{2mE}$ so $\lambda=h/\sqrt{2mE}$ — a 100 eV electron has $\lambda\approx
0.123$ nm, comparable to atomic spacings, which is why electrons diffract off
crystals (Davisson–Germer) and why electron microscopes resolve atoms. **This
wave is the object `~QM-02` promotes to the wavefunction $\Psi$, and `~QM-03`
governs with the Schrödinger equation.** Note quantum effects matter when $\lambda$
exceeds the system size (Griffiths Prob. 1.18).

## 5. Compton scattering — the photon's momentum, directly

X-rays scattering off electrons shift to *longer* wavelength by an amount that
depends only on the scattering angle:
$$\Delta\lambda=\frac{h}{m_ec}(1-\cos\theta)=\lambda_C(1-\cos\theta),\qquad
\lambda_C=2.426\ \mathrm{pm}.$$
This is exactly two-body relativistic kinematics if the photon carries energy
$h\nu$ *and* momentum $h/\lambda$ — clinching the photon's reality. Maximal shift
$2\lambda_C\approx4.85$ pm at back-scatter ($\theta=\pi$); zero forward.

---
### Why this is the trunk root
Black body + photoelectric + Compton say **radiation is quantized** ($E=h\nu$,
$p=h/\lambda$). de Broglie says **matter is wavelike** ($\lambda=h/p$). Bohr says
**bound systems are quantized**. The unresolved question each leaves — *what is
the wave, and what determines it?* — is answered in order by `~QM-02`
(Born: $|\Psi|^2$ is a probability density) and `~QM-03` (the Schrödinger
equation for $\Psi$).
