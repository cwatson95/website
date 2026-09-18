"""Tests for QO-06 nonlinear optics.

Run:  python3 test_nonlinear_optics.py     ->  "All N tests passed."
"""
import numpy as np

from nonlinear_optics import (
    C, EPS0, HBAR, chi_polarization, shg_phase_mismatch, shg_efficiency,
    coherence_length, manley_rowe_check, kerr_index, kerr_phase,
    brillouin_shift, brillouin_gain, raman_gain,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- chi^(n) polarization series ---------------------------------------------

def test_polarization_series_orders():
    E, chi1, chi2, chi3 = 1.0e8, 1.0, 1.0e-12, 1.0e-23
    # reduces to the linear response when chi2 = chi3 = 0
    assert _approx(float(chi_polarization(E, chi1)), EPS0 * chi1 * E)
    # the chi^(2) contribution scales as E^2 (doubling E -> x4)
    p1 = float(chi_polarization(E, 0.0, chi2))
    p2 = float(chi_polarization(2.0 * E, 0.0, chi2))
    assert _approx(p2 / p1, 4.0)
    # the full series is the sum of the three terms
    assert _approx(float(chi_polarization(E, chi1, chi2, chi3)),
                   EPS0 * (chi1 * E + chi2 * E ** 2 + chi3 * E ** 3))


# --- chi^(2): SHG, phase matching, coherence length --------------------------

def test_shg_peaks_at_phase_matching():
    L = 1.0e-3
    assert _approx(float(shg_efficiency(0.0, L)), 1.0)         # peak = eta0 = 1
    assert float(shg_efficiency(5.0e2, L)) < 1.0               # any mismatch lowers it
    # even function of Delta k
    assert _approx(float(shg_efficiency(-5.0e2, L)),
                   float(shg_efficiency(5.0e2, L)))


def test_shg_first_null_at_2pi():
    L = 1.0e-3
    dk_null = 2.0 * np.pi / L
    assert abs(float(shg_efficiency(dk_null, L))) < 1e-12      # sinc^2 zero
    assert float(shg_efficiency(0.5 * dk_null, L)) > 0.0       # positive before it


def test_coherence_length():
    dk = 3.5e5
    Lc = coherence_length(dk)
    assert _approx(Lc, np.pi / dk)
    assert _approx(dk * Lc, np.pi)                             # Delta k L_c = pi
    assert coherence_length(0.5 * dk) > Lc                     # smaller mismatch -> longer
    # the sinc^2 conversion curve first nulls at L = 2 L_c
    assert abs(float(shg_efficiency(dk, 2.0 * Lc))) < 1e-12
    assert coherence_length(0.0) == float("inf")              # phase matched -> infinite


def test_shg_phase_mismatch_from_dispersion():
    lam = 1.064e-6
    dk = shg_phase_mismatch(1.50, 1.53, lam)
    assert _approx(dk, 4.0 * np.pi * 0.03 / lam)
    assert dk > 0.0                                            # normal dispersion
    assert _approx(shg_phase_mismatch(1.5, 1.5, lam), 0.0)     # matched when n(2w)=n(w)
    # ~8.9 um coherence length for this 0.03 index split at 1.064 um
    assert 8.0e-6 < coherence_length(dk) < 10.0e-6


# --- Manley-Rowe (photon-number conservation) --------------------------------

def test_manley_rowe_photon_and_energy_conservation():
    om = lambda nm: 2.0 * np.pi * C / (nm * 1e-9)
    mr = manley_rowe_check(om(532.0), om(800.0), I_pump=1e12, I_signal=1e6,
                           I_idler=0.0, d_photons=1e24)
    # idler frequency fixed by energy conservation
    assert _approx(mr["omega_idler"], om(532.0) - om(800.0))
    # equal photon-flux gain for signal & idler, opposite for the pump
    assert _approx(mr["dPhi_signal"], mr["dPhi_idler"])
    assert _approx(mr["dPhi_signal"], -mr["dPhi_pump"])
    assert _approx(mr["dPhi_signal"], 1e24)
    # energy conserved: the intensity changes sum to ~0
    assert abs(mr["energy_residual"]) < 1e-9 * abs(mr["dI_pump"])
    # pump depletes; signal and idler grow
    assert mr["I_pump"] < 1e12
    assert mr["I_signal"] > 1e6 and mr["I_idler"] > 0.0


# --- chi^(3): Kerr effect & self-phase modulation ----------------------------

def test_kerr_index_and_phase():
    n0, n2, I = 1.45, 2.6e-20, 1.0e15
    assert _approx(float(kerr_index(n0, n2, I)), n0 + n2 * I)
    lam, L = 1.064e-6, 1.0e-2
    phi = float(kerr_phase(n2, I, L, lam))
    assert _approx(phi, (2.0 * np.pi / lam) * n2 * I * L)
    assert _approx(phi, 1.535, tol=1e-2)                       # ~1.54 rad B-integral
    # linear in intensity and in length
    assert _approx(float(kerr_phase(n2, 2.0 * I, L, lam)), 2.0 * phi)
    assert _approx(float(kerr_phase(n2, I, 2.0 * L, lam)), 2.0 * phi)


# --- stimulated Brillouin & Raman scattering ---------------------------------

def test_brillouin_shift_value():
    nu_B = brillouin_shift(1.33, 1480.0, 532e-9)
    assert _approx(nu_B, 2.0 * 1.33 * 1480.0 / 532e-9)
    assert 5.0e9 < nu_B < 1.0e10                               # ~7.4 GHz for water


def test_brillouin_gain_lorentzian():
    nu_B, gam, g0 = 7.4e9, 100e6, 2.5
    # peak at the Brillouin shift equals g0
    assert _approx(float(brillouin_gain(nu_B, nu_B, gam, g0)), g0)
    # half-maximum at +/- gamma_B/2  (FWHM = gamma_B)
    assert _approx(float(brillouin_gain(nu_B + 0.5 * gam, nu_B, gam, g0)), 0.5 * g0)
    assert _approx(float(brillouin_gain(nu_B - 0.5 * gam, nu_B, gam, g0)), 0.5 * g0)
    # falls off far from line center
    assert float(brillouin_gain(nu_B + 20.0 * gam, nu_B, gam, g0)) < 0.01 * g0
    # the maximum of a scan sits at the shift, with value g0
    Om = np.linspace(nu_B - 10.0 * gam, nu_B + 10.0 * gam, 4001)
    g = brillouin_gain(Om, nu_B, gam, g0)
    assert _approx(Om[int(np.argmax(g))], nu_B, tol=1e-3)
    assert _approx(float(g.max()), g0)


def test_raman_gain_lorentzian_and_shift_scale():
    Om_R, gam, g0 = 1.0e14, 5.0e12, 1.0      # optical-phonon scale
    assert _approx(float(raman_gain(Om_R, Om_R, gam, g0)), g0)          # peak = g0
    assert _approx(float(raman_gain(Om_R + 0.5 * gam, Om_R, gam, g0)), 0.5 * g0)
    # Raman shift (vibrational, ~THz) vastly exceeds the Brillouin shift (~GHz)
    assert Om_R > brillouin_shift(1.33, 1480.0, 532e-9)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
