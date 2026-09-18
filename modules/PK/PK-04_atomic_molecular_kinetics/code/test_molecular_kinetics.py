"""Tests for PK-04 atomic & molecular kinetics.

Run:  python3 test_molecular_kinetics.py     ->  "All N tests passed."
"""
import numpy as np

from molecular_kinetics import (
    K_B_EV, M_E,
    maxwell_energy_pdf, rate_coefficient_maxwellian,
    rate_coefficient_step_closed_form, arrhenius,
    saha_ratio, saha_ionization_fraction,
    default_krf_params, simulate_krf, photon_energy_eV,
)


# --- the EEDF ----------------------------------------------------------------

def test_maxwell_eedf_normalized_and_mean_energy():
    # int F dE = 1 and <E> = (3/2) kT for the Maxwellian EEDF
    T = 2.0e4
    kT = K_B_EV * T
    E = np.linspace(0.0, 40.0 * kT, 200000)
    F = maxwell_energy_pdf(E, T)
    norm = np.trapezoid(F, E)
    mean = np.trapezoid(E * F, E)
    assert abs(norm - 1.0) < 1e-3
    assert abs(mean - 1.5 * kT) < 1e-3 * (1.5 * kT)


# --- rate coefficient k = <sigma v> ------------------------------------------

def test_rate_coefficient_positive_and_increasing():
    sigma0, Eth = 1.0e-20, 9.9
    ks = [rate_coefficient_maxwellian(T, sigma0, Eth)
          for T in (1.0e4, 2.0e4, 3.0e4, 5.0e4)]
    assert all(k > 0 for k in ks)
    assert ks[0] < ks[1] < ks[2] < ks[3]      # rises with temperature


def test_rate_coefficient_matches_closed_form():
    # numeric energy integral == sigma0 <v> (1 + Eth/kT) exp(-Eth/kT)
    sigma0, Eth = 3.0e-20, 12.0
    for T in (1.5e4, 3.0e4, 6.0e4):
        k_num = rate_coefficient_maxwellian(T, sigma0, Eth)
        k_cf = rate_coefficient_step_closed_form(T, sigma0, Eth)
        assert abs(k_num - k_cf) < 1e-5 * k_cf


def test_rate_coefficient_apparent_activation_energy():
    # the exponential exp(-Eth/kT) dominates: the apparent Arrhenius activation
    # energy -d(ln k)/d(1/kT) is close to (just under) the threshold Eth.
    sigma0, Eth = 1.0e-20, 15.0
    T1, T2 = 1.2e4, 1.4e4
    k1 = rate_coefficient_maxwellian(T1, sigma0, Eth)
    k2 = rate_coefficient_maxwellian(T2, sigma0, Eth)
    Ea_app = -K_B_EV * (np.log(k2) - np.log(k1)) / (1.0 / T2 - 1.0 / T1)
    assert 0.85 * Eth < Ea_app < Eth          # ~ Eth - (1/2)kT, just below Eth


def test_arrhenius_formula_and_recovery():
    A, Ea = 1.0e-15, 3.0
    T1, T2 = 5.0e3, 1.0e4
    assert arrhenius(T2, A, Ea) > arrhenius(T1, A, Ea)            # increases with T
    # recover Ea exactly from two points (ln-linear in 1/T)
    Ea_fit = -K_B_EV * (np.log(arrhenius(T2, A, Ea)) - np.log(arrhenius(T1, A, Ea))) \
        / (1.0 / T2 - 1.0 / T1)
    assert abs(Ea_fit - Ea) < 1e-9
    assert abs(arrhenius(1.0e30, A, Ea) - A) < 1e-6 * A          # k -> A as T -> inf


# --- Saha ionization equilibrium ---------------------------------------------

def test_saha_ratio_formula_positive_increasing():
    T, E_ion = 1.5e4, 14.0
    S = saha_ratio(T, E_ion)
    assert S > 0
    # increases steeply with T
    assert saha_ratio(2.0e4, E_ion) > saha_ratio(1.0e4, E_ion)
    # explicit formula check (factor 2 = electron spin, quantum concentration)
    from molecular_kinetics import K_B_J, H_PLANCK
    qc = (2.0 * np.pi * M_E * K_B_J * T / H_PLANCK ** 2) ** 1.5
    S_ref = 2.0 * qc * np.exp(-E_ion / (K_B_EV * T))
    assert abs(S - S_ref) < 1e-12 * S_ref


def test_saha_fraction_bounded_and_monotonic():
    n_tot, E_ion = 1.0e24, 14.0
    xs = [saha_ionization_fraction(T, n_tot, E_ion)
          for T in (8.0e3, 1.2e4, 1.6e4, 2.5e4)]
    assert all(0.0 < x < 1.0 for x in xs)
    assert xs[0] < xs[1] < xs[2] < xs[3]               # rises with T
    assert saha_ionization_fraction(1.0e3, n_tot, E_ion) < 1e-3   # ~neutral when cold
    assert saha_ionization_fraction(1.0e5, n_tot, E_ion) > 0.99   # ~fully ionized when hot


# --- 0-D KrF* excimer kinetics -----------------------------------------------

def test_excimer_krfstar_peaks_then_decays():
    res = simulate_krf()
    KrFs = res["KrFs"]
    ipk = int(np.argmax(KrFs))
    assert KrFs[0] < 1e-9 * KrFs[ipk]          # starts essentially empty
    assert 0 < ipk < len(KrFs) - 1             # peak is interior (rise then fall)
    assert KrFs[-1] < 0.1 * KrFs[ipk]          # decays well below the peak
    assert res["peak_KrFs"] > 0


def test_excimer_atom_conservation():
    # closed reactions conserve Kr-atom and F-atom inventories
    res = simulate_krf()
    kr = res["kr_nuclei"]
    f = res["f_nuclei"]
    assert np.max(np.abs(kr / kr[0] - 1.0)) < 1e-6
    assert np.max(np.abs(f / f[0] - 1.0)) < 1e-6
    # the expected totals: Kr0 and 2*F2_0
    p = default_krf_params()
    assert abs(kr[0] - p["Kr0"]) < 1e-6 * p["Kr0"]
    assert abs(f[0] - 2.0 * p["F2_0"]) < 1e-6 * (2.0 * p["F2_0"])


def test_excimer_photons_and_reservoir():
    res = simulate_krf()
    ph = res["photons"]
    assert ph[0] == 0.0
    assert np.all(np.diff(ph) >= 0.0)          # cumulative emission only grows
    assert ph[-1] > 0.0                        # some 248 nm light was emitted
    assert res["F2"][-1] < res["F2"][0]        # F2 is consumed by harpooning
    assert res["F"][-1] > res["F"][0]          # atomic F builds up


def test_photon_energy_248nm():
    E = photon_energy_eV(248.0)
    assert abs(E - 5.0) < 0.02                 # KrF* B->X ~ 4.999 eV
    # energy scales as 1/lambda
    assert abs(photon_energy_eV(124.0) - 2.0 * E) < 1e-9 * E


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
