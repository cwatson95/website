# QO-06 — Nonlinear Optics — χ⁽²⁾/χ⁽³⁾, Parametric, SBS & Raman (notes)

Linear optics is what a medium does when the light is weak: the polarization
tracks the field, waves superpose, frequencies never mix. Turn up the intensity
and the bound electrons start to feel the **anharmonicity** of their potential —
the polarization acquires terms in E², E³, … — and the medium begins to
**generate new frequencies** and **couple beams** to one another. This module
follows that expansion from second-harmonic generation through to the stimulated
Brillouin scattering at the heart of the user's **SBS_Project**.

Citation key (full details in `refs.md`): **Boyd** = R. W. Boyd, *Nonlinear
Optics*, 4th ed.; **SZ** = Scully & Zubairy, *Quantum Optics*. Cited at
chapter/section level (the Boyd PDF has no machine-readable page layer). SI
units; intensity I = ½ n ε₀ c |E|² ∝ |E|² (`~EM-15`).

## 1. The nonlinear polarization
Expand the medium's polarization in powers of the driving field (Boyd Ch. 1):
$$P=\varepsilon_0\big(\chi^{(1)}E+\chi^{(2)}E^2+\chi^{(3)}E^3+\cdots\big).$$
The expansion parameter is the field measured against the **atomic field**
$E_{\rm at}=e/4\pi\varepsilon_0 a_0^2$, so successive susceptibilities scale as
$$\chi^{(2)}\sim\frac{\chi^{(1)}}{E_{\rm at}},\qquad
  \chi^{(3)}\sim\frac{\chi^{(1)}}{E_{\rm at}^{2}},\qquad
  E_{\rm at}\sim 10^{11}\,\text{V/m}.$$
With $\chi^{(1)}\sim1$ this gives $\chi^{(2)}\sim$ pm/V and
$\chi^{(3)}\sim10^{-22}\ \text{m}^2/\text{V}^2$ — the new terms only compete at
laser intensities. $\chi^{(2)}$ vanishes in centrosymmetric media (it would flip
sign under $E\to-E$), so three-wave mixing needs non-centrosymmetric crystals;
$\chi^{(3)}$ is universal. Code: `chi_polarization`.

## 2. χ⁽²⁾ second-harmonic generation and phase matching
Two photons of $\omega$ combine into one of $2\omega$. In the undepleted-pump,
slowly-varying-envelope approximation the harmonic amplitude integrates to
$A_2(L)\propto L\,\mathrm{sinc}(\Delta k L/2)$, so the **conversion efficiency**
is (Boyd Ch. 2)
$$\eta_{\rm SHG}\propto L^2\,\mathrm{sinc}^2\!\Big(\frac{\Delta k\,L}{2}\Big)
  =L^2\left(\frac{\sin(\Delta k L/2)}{\Delta k L/2}\right)^2,\qquad
  \Delta k=k(2\omega)-2k(\omega).$$
It is maximal at **perfect phase matching** $\Delta k=0$, where the harmonic
adds in phase all along the crystal, and falls to its **first null at**
$\Delta k L=2\pi$. Code: `shg_efficiency` (normalized to its peak $\eta_0$ at
$\Delta k=0$), `shg_phase_mismatch`.

## 3. Coherence length
Because $k=n\omega/c$, normal dispersion ($n(2\omega)>n(\omega)$, `~EM-15`)
forces $\Delta k>0$:
$$\Delta k=\frac{4\pi}{\lambda}\big(n(2\omega)-n(\omega)\big),\qquad
  L_c=\frac{\pi}{|\Delta k|}.$$
$L_c$ is the distance over which fundamental and harmonic slip by $\pi$ in
relative phase; beyond it power flows **back** to the fundamental, and the
sinc² curve of §2 first nulls at $L=2L_c$. A 0.03 index split at
$\lambda=1.064\,\mu$m gives $L_c\approx9\,\mu$m — which is why one engineers
$\Delta k\to0$ with birefringent or quasi-phase matching. Code:
`coherence_length`.

## 4. Manley–Rowe relations
Any lossless parametric process conserves **photon number**, not just energy. For
$\omega_3=\omega_1+\omega_2$ the intensities obey (Boyd Ch. 2)
$$\frac{d}{dz}\frac{I_1}{\omega_1}=\frac{d}{dz}\frac{I_2}{\omega_2}
  =-\frac{d}{dz}\frac{I_3}{\omega_3}.$$
Since $I_i/\hbar\omega_i$ is the photon flux, this says every pump ($\omega_3$)
photon destroyed creates exactly one signal ($\omega_1$) and one idler
($\omega_2$) photon — the classical shadow of the quantum down-conversion that
makes squeezed and entangled light (`~QO-05`, SZ). Energy conservation
$\Delta I_1+\Delta I_2+\Delta I_3=0$ follows automatically. Code:
`manley_rowe_check`.

## 5. χ⁽³⁾ optical Kerr effect and self-phase modulation
The third-order term, for a single strong beam, adds an **intensity-dependent
refractive index** (Boyd Ch. 4):
$$n=n_0+n_2 I,\qquad n_2=\frac{3\chi^{(3)}}{4n_0^2\varepsilon_0 c}.$$
A beam therefore phase-modulates *itself*: travelling a length $L$ at intensity
$I$ it picks up a nonlinear phase
$$\phi_{\rm NL}=\frac{2\pi}{\lambda}\,n_2 I L,$$
the **self-phase modulation** that broadens spectra in fibers and the
**B-integral** that limits high-power laser chains (`~PK-04`). Code: `kerr_index`,
`kerr_phase`.

## 6. Four-wave mixing
With three input waves $\chi^{(3)}$ generates a fourth obeying energy and
momentum conservation
$$\omega_4=\omega_1+\omega_2-\omega_3,\qquad
  \mathbf{k}_4=\mathbf{k}_1+\mathbf{k}_2-\mathbf{k}_3.$$
Degenerate FWM ($\omega_1=\omega_2=\omega_3$) is the engine of **optical phase
conjugation** — a wavefront-reversing "time-reversed" mirror — which also arises
from stimulated Brillouin scattering (§7) and is a workhorse of **SBS_Project**.

## 7. Stimulated Brillouin (SBS) and Raman scattering
A strong pump beats against a Stokes-shifted wave; the beat drives a material
excitation (an **acoustic phonon** for Brillouin, an **optical/vibrational
phonon** for Raman) which scatters the pump into the Stokes wave — a
**self-reinforcing gain**. Through $\chi^{(3)}$ the Stokes wave grows as
$e^{g(\Omega)\,I_{\rm pump}\,z}$ with a **Lorentzian gain spectrum** (Boyd Ch.
9–10)
$$g(\Omega)=g_0\,\frac{(\Gamma_B/2)^2}{(\Omega-\Omega_B)^2+(\Gamma_B/2)^2},$$
peaked at the shift $\Omega_B$ with peak $g_0$ and FWHM $\Gamma_B$ (the phonon
damping rate). For **backscattered Brillouin** the shift is set by the sound
speed $v_a$:
$$\nu_B=\frac{2 n v_a}{\lambda_p},\qquad \omega_S=\omega_p-\Omega_B.$$
Water at 532 nm gives $\nu_B\approx7.4$ GHz, $\Gamma_B\sim100$ MHz. SBS turns a
medium into a **phase-conjugate mirror** and a **pulse compressor** — exactly the
physics the user's **SBS_Project** models, where `brillouin_gain` is the
lineshape $g_B(\nu)$ fitted to data. Raman is the same Lorentzian at the far
larger vibrational shift (THz vs GHz). Code: `brillouin_shift`, `brillouin_gain`,
`raman_gain`.

## Where this goes
- **→ SBS_Project** — the Lorentzian `brillouin_gain` here is the kernel of the
  measured SBS gain spectra; phase conjugation (§6) and pulse compression are its
  applications.
- `~QO-05` — run χ⁽²⁾ as a *quantum* source and the Manley–Rowe pair becomes
  parametric down-conversion: squeezed vacuum and entangled photon pairs.
- `~QO-03` — the exponential gain $e^{gIz}$ of stimulated scattering is the same
  language as laser gain / stimulated emission.
- `~EM-15` — supplies the dispersion $n(\omega)$ and $k=n\omega/c$ that set both
  the SHG phase mismatch and the Brillouin shift; `~PK-04` — the high-fluence
  excimer regime where the Kerr B-integral and SBS thresholds matter.
