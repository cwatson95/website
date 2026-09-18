"""QO-06  Nonlinear optics -- chi^(2)/chi^(3), parametric, SBS & Raman.

Physics topic network, module QO-06 (modules/topic_network.txt).  Trunk: QO
(Quantum & Nonlinear Optics).  This module directly underpins the user's
**SBS_Project** (stimulated Brillouin scattering: gain spectra, phase
conjugation, pulse compression).

Source -- R. W. Boyd, *Nonlinear Optics*, 4th ed. (cited at chapter level; no
page numbers, see ../refs.md):
  * nonlinear-polarization expansion, chi^(n) orders of magnitude      Ch. 1
  * second-harmonic generation, phase matching, coherence length       Ch. 2
  * Manley-Rowe relations (photon-number conservation)                 Ch. 2
  * optical Kerr effect n = n0 + n2 I, self-phase modulation, FWM      Ch. 4 / 7
  * stimulated Brillouin scattering (SBS) -- Lorentzian gain           Ch. 9
  * stimulated Raman scattering -- Lorentzian gain                     Ch. 10

A medium's dielectric polarization, expanded in the driving field,

    P = eps0 ( chi1 E + chi2 E^2 + chi3 E^3 + ... ),

has higher orders set by the atomic field E_at ~ 1e11 V/m: chi2 ~ chi1/E_at,
chi3 ~ chi1/E_at^2, so nonlinear optics needs laser intensities.  The chi^(2)
(three-wave) term drives SHG / sum- & difference-frequency / optical parametric
amplification, all governed by the phase mismatch Delta k = k(2w) - 2k(w)
through eta_SHG ~ sinc^2(Delta k L / 2); the chi^(3) (four-wave) term gives the
Kerr effect n = n0 + n2 I, self-phase modulation, four-wave mixing, and the
stimulated Brillouin / Raman gain -- a Lorentzian peaked at the acoustic /
vibrational shift, which is the heart of SBS_Project.

Self-contained: numpy only, constants defined locally, SI units throughout.
"""

import numpy as np

__all__ = [
    "C", "EPS0", "HBAR",
    "chi_polarization",
    "shg_phase_mismatch", "shg_efficiency", "coherence_length",
    "manley_rowe_check",
    "kerr_index", "kerr_phase",
    "brillouin_shift", "brillouin_gain", "raman_gain",
]

# --- local physical constants (SI) -------------------------------------------
C = 299792458.0           # speed of light in vacuum   [m/s]
EPS0 = 8.8541878128e-12   # vacuum permittivity         [F/m]
HBAR = 1.054571817e-34    # reduced Planck constant     [J s]


def _sinc(x):
    """Unnormalized sinc, sin(x)/x, with sinc(0) = 1.

    numpy's np.sinc(y) = sin(pi y)/(pi y), so np.sinc(x/pi) = sin(x)/x."""
    return np.sinc(np.asarray(x, dtype=float) / np.pi)


# --- 1. the nonlinear polarization (Boyd Ch. 1) ------------------------------

def chi_polarization(E, chi1, chi2=0.0, chi3=0.0, eps0=EPS0):
    """Dielectric polarization series  P = eps0 (chi1 E + chi2 E^2 + chi3 E^3).

    chi1 is dimensionless, chi2 has units m/V, chi3 has units (m/V)^2.  Each
    successive term is smaller by ~ E/E_at with the atomic field
    E_at ~ 1e11 V/m, so the nonlinear terms matter only at laser intensities
    (Boyd Ch. 1)."""
    E = np.asarray(E, dtype=float)
    return eps0 * (chi1 * E + chi2 * E ** 2 + chi3 * E ** 3)


# --- 2. chi^(2): second-harmonic generation & phase matching (Boyd Ch. 2) ----

def shg_phase_mismatch(n_fund, n_sh, wavelength_fund):
    """Wavevector mismatch for second-harmonic generation,
        Delta k = k(2w) - 2 k(w) = (4 pi / lambda_fund) (n(2w) - n(w)).
    Normal dispersion (n(2w) > n(w)) gives Delta k > 0, so birefringent or
    quasi-phase matching is needed to reach Delta k = 0 (Boyd Ch. 2; ~EM-15
    dispersion)."""
    return 4.0 * np.pi * (n_sh - n_fund) / wavelength_fund


def shg_efficiency(delta_k, L, eta0=1.0):
    """SHG phase-matching factor,
        eta(Delta k) = eta0 * sinc^2(Delta k L / 2),   sinc(x) = sin(x)/x,
    normalized to its peak eta0 at perfect phase matching Delta k = 0.  (The
    absolute conversion also carries an L^2 prefactor: eta ~ L^2 at Delta k = 0.)
    First zeros at Delta k L = 2 pi (Boyd Ch. 2)."""
    return eta0 * _sinc(0.5 * np.asarray(delta_k, dtype=float) * L) ** 2


def coherence_length(delta_k):
    """SHG coherence length  L_c = pi / |Delta k|  -- the distance over which the
    fundamental and second harmonic slip by pi in relative phase, after which
    power flows back to the fundamental (Boyd Ch. 2).  The sinc^2 conversion
    curve first nulls at L = 2 L_c."""
    dk = abs(float(delta_k))
    return float("inf") if dk == 0.0 else np.pi / dk


# --- 3. Manley-Rowe relations -- photon-number conservation (Boyd Ch. 2) -----

def manley_rowe_check(omega_pump, omega_signal, I_pump, I_signal, I_idler,
                      d_photons, hbar=HBAR):
    """One parametric (three-wave) step: a pump photon at omega_pump splits into
    a signal photon at omega_signal and an idler at
        omega_idler = omega_pump - omega_signal   (energy conservation),
    transferring photon flux `d_photons` [1/m^2/s] from the pump to signal+idler.

    Manley-Rowe: d(I1/omega1) = d(I2/omega2) = -d(I3/omega3), i.e. signal and
    idler each gain one photon per pump photon destroyed.  Returns a dict with
    the updated intensities, the per-wave photon-flux change dPhi, and the
    (machine-zero) energy residual sum(dI) (Boyd Ch. 2; ~QO-05)."""
    w_p = float(omega_pump)
    w_s = float(omega_signal)
    w_i = w_p - w_s                       # idler fixed by energy conservation
    dN = float(d_photons)
    dI_pump = -hbar * w_p * dN
    dI_signal = hbar * w_s * dN
    dI_idler = hbar * w_i * dN
    return {
        "omega_idler": w_i,
        "I_pump": I_pump + dI_pump,
        "I_signal": I_signal + dI_signal,
        "I_idler": I_idler + dI_idler,
        "dI_pump": dI_pump,
        "dI_signal": dI_signal,
        "dI_idler": dI_idler,
        "dPhi_pump": dI_pump / (hbar * w_p),
        "dPhi_signal": dI_signal / (hbar * w_s),
        "dPhi_idler": dI_idler / (hbar * w_i),
        "energy_residual": dI_pump + dI_signal + dI_idler,
    }


# --- 4. chi^(3): optical Kerr effect & self-phase modulation (Boyd Ch. 4/7) --

def kerr_index(n0, n2, I):
    """Intensity-dependent refractive index  n = n0 + n2 I  (optical Kerr
    effect).  n2 [m^2/W] relates to chi^(3) by n2 = 3 chi3 / (4 n0^2 eps0 c)
    (Boyd Ch. 4)."""
    return n0 + n2 * np.asarray(I, dtype=float)


def kerr_phase(n2, I, L, wavelength):
    """Nonlinear self-phase-modulation phase over length L,
        phi_NL = (2 pi / lambda) n2 I L,
    the 'B-integral' of high-power laser physics (Boyd Ch. 4/7)."""
    return (2.0 * np.pi / wavelength) * n2 * np.asarray(I, dtype=float) * L


# --- 5. stimulated Brillouin & Raman scattering -- Lorentzian gain -----------

def brillouin_shift(n, v_sound, wavelength_pump):
    """Brillouin (Stokes) frequency shift for backscattering,
        nu_B = 2 n v_sound / lambda_pump   [Hz],
    the acoustic-phonon frequency at which the SBS gain peaks (Boyd Ch. 9).
    This is the line center computed by SBS_Project's gain spectra."""
    return 2.0 * n * v_sound / wavelength_pump


def brillouin_gain(Omega, Omega_B, gamma_B, g0=1.0):
    """Stimulated-Brillouin gain spectrum -- a Lorentzian in the Stokes detuning,
        g(Omega) = g0 (gamma_B/2)^2 / [(Omega - Omega_B)^2 + (gamma_B/2)^2],
    peaked at the Brillouin shift Omega_B with peak value g0 and FWHM gamma_B
    (the phonon damping rate / Brillouin linewidth).  This is exactly the
    lineshape modelled in SBS_Project (Boyd Ch. 9)."""
    half = 0.5 * gamma_B
    return g0 * half ** 2 / ((np.asarray(Omega, dtype=float) - Omega_B) ** 2 + half ** 2)


def raman_gain(Omega, Omega_R, gamma_R, g0=1.0):
    """Stimulated-Raman gain spectrum -- the same Lorentzian form as SBS but
    peaked at the (far larger) vibrational / optical-phonon Raman shift Omega_R
    with FWHM gamma_R (Boyd Ch. 10)."""
    half = 0.5 * gamma_R
    return g0 * half ** 2 / ((np.asarray(Omega, dtype=float) - Omega_R) ** 2 + half ** 2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QO-06  Nonlinear optics -- chi^(2)/chi^(3), parametric, SBS & Raman")
    print("=" * 68)

    # 1) orders of magnitude of the chi^(n) series
    E_at = 5.14e11          # characteristic atomic field [V/m]
    print("\n1) P = eps0 (chi1 E + chi2 E^2 + chi3 E^3):")
    print("   successive terms shrink by ~ E/E_at with E_at ~ %.2e V/m" % E_at)
    print("   -> chi2 ~ chi1/E_at ~ pm/V; nonlinearity needs laser fields")

    # 2) SHG phase matching: peak at Delta k = 0, first null at Delta k L = 2 pi
    lam, L = 1.064e-6, 1.0e-3
    print("\n2) SHG  eta = sinc^2(Delta k L/2)   (lambda = %.3f um, L = %.1f mm):"
          % (lam * 1e6, L * 1e3))
    print("   Delta k = 0       -> eta = %.4f   (perfect phase matching, peak)"
          % float(shg_efficiency(0.0, L)))
    dk_null = 2.0 * np.pi / L
    print("   Delta k L = 2 pi  -> eta = %.2e   (first null)"
          % float(shg_efficiency(dk_null, L)))
    dk = shg_phase_mismatch(n_fund=1.500, n_sh=1.530, wavelength_fund=lam)
    print("   normal dispersion dn = 0.030 -> Delta k = %.3e /m,  L_c = pi/|Delta k| = %.2f um"
          % (dk, coherence_length(dk) * 1e6))

    # 3) Manley-Rowe: one pump photon -> signal + idler, energy conserved
    om = lambda nm: 2.0 * np.pi * C / (nm * 1e-9)
    mr = manley_rowe_check(om(532.0), om(800.0), I_pump=1e12, I_signal=1e6,
                           I_idler=0.0, d_photons=1e24)
    print("\n3) Manley-Rowe parametric step (pump 532 nm -> signal 800 nm + idler):")
    print("   idler lambda = %.0f nm  (set by energy conservation)"
          % (2.0 * np.pi * C / mr["omega_idler"] * 1e9))
    print("   dPhi: signal %+.3e = idler %+.3e = -pump %+.3e  (photons conserved)"
          % (mr["dPhi_signal"], mr["dPhi_idler"], -mr["dPhi_pump"]))
    print("   energy residual sum(dI) = %.2e  (= 0: energy conserved)"
          % mr["energy_residual"])

    # 4) Kerr effect / self-phase modulation (the B-integral)
    n2, I, Lk = 2.6e-20, 1.0e15, 1.0e-2     # fused silica, 0.1 TW/cm^2, 1 cm
    print("\n4) optical Kerr effect  n = n0 + n2 I,  self-phase modulation:")
    print("   n2 = %.1e m^2/W, I = %.0e W/m^2, L = %.0f cm, lambda = %.3f um"
          % (n2, I, Lk * 1e2, lam * 1e6))
    print("   phi_NL = (2 pi/lambda) n2 I L = %.3f rad   (the B-integral)"
          % float(kerr_phase(n2, I, Lk, lam)))

    # 5) SBS / Raman gain -- Lorentzian peaked at the shift
    n, v_a, lam_p = 1.33, 1480.0, 532e-9     # water at 532 nm
    nu_B, gam = brillouin_shift(n, v_a, lam_p), 100e6
    print("\n5) stimulated Brillouin scattering (water, 532 nm):")
    print("   Brillouin shift nu_B = 2 n v_a/lambda = %.2f GHz" % (nu_B * 1e-9))
    print("   gain at line center nu_B           : g = %.4f g0  (peak)"
          % float(brillouin_gain(nu_B, nu_B, gam)))
    print("   gain at nu_B +/- gamma_B/2          : g = %.4f g0  (half max, FWHM = %.0f MHz)"
          % (float(brillouin_gain(nu_B + 0.5 * gam, nu_B, gam)), gam * 1e-6))
    print("   -> this Lorentzian is SBS_Project's g_B(nu) (Boyd Ch. 9)")


if __name__ == "__main__":
    _demo()
