"""Tests for QO-03 emission & coherence.

Run:  python3 test_emission_coherence.py     ->  "All N tests passed."
"""
import numpy as np

from emission_coherence import (
    H_PLANCK, C_LIGHT, K_B,
    einstein_A_over_B, planck_spectral_energy_density,
    boltzmann_population_ratio, detailed_balance_energy_density,
    stimulated_to_spontaneous,
    laser_threshold, laser_steady_state, laser_rate_rhs,
    g2_thermal, g2_coherent, g2_fock, g2_from_distribution,
)


# --- Einstein A/B, Planck, detailed balance ----------------------------------

def test_einstein_A_over_B_formula_and_scaling():
    for nu in (1.0e9, 5.0e14, 1.21e15):
        assert np.isclose(einstein_A_over_B(nu),
                          8.0 * np.pi * H_PLANCK * nu ** 3 / C_LIGHT ** 3,
                          rtol=1e-12)
    # A/B scales as nu^3
    assert np.isclose(einstein_A_over_B(2.0e15) / einstein_A_over_B(1.0e15), 8.0)
    assert einstein_A_over_B(5.0e14) > 0.0


def test_planck_closed_form_and_rayleigh_jeans_limit():
    nu, T = 5.0e14, 4000.0
    x = H_PLANCK * nu / (K_B * T)
    assert np.isclose(planck_spectral_energy_density(nu, T),
                      einstein_A_over_B(nu) / (np.exp(x) - 1.0), rtol=1e-9)
    # Rayleigh-Jeans (h nu << kB T):  rho -> 8 pi nu^2 kB T / c^3
    nu_lo, T_hi = 1.0e9, 300.0
    rj = 8.0 * np.pi * nu_lo ** 2 * K_B * T_hi / C_LIGHT ** 3
    assert np.isclose(planck_spectral_energy_density(nu_lo, T_hi), rj, rtol=1e-3)
    assert planck_spectral_energy_density(nu, T) > 0.0


def test_detailed_balance_reproduces_planck():
    # Einstein's closure: the rate-balance rho equals Planck, independent of
    # A21 and the degeneracies g1, g2.
    nu, T = 6.0e13, 1200.0                      # h nu / kT ~ 2.4, no cancellation
    for g_lo, g_up, A21 in [(1.0, 1.0, 1.0), (1.0, 3.0, 7.5e6), (2.0, 5.0, 1.0e8)]:
        rho_db = detailed_balance_energy_density(nu, T, g_lo, g_up, A21)
        assert np.isclose(rho_db, planck_spectral_energy_density(nu, T), rtol=1e-9)


def test_boltzmann_population_ratio():
    nu, T = 5.0e14, 3000.0
    r = boltzmann_population_ratio(nu, T, g_lower=1.0, g_upper=1.0)
    assert np.isclose(r, np.exp(-H_PLANCK * nu / (K_B * T)))
    assert r < 1.0                               # no thermal inversion (T > 0)
    # degeneracy weight and the T -> infinity limit (-> g2/g1)
    assert np.isclose(boltzmann_population_ratio(nu, 1e12, 1.0, 3.0), 3.0, rtol=1e-3)


def test_stimulated_to_spontaneous():
    nu, T = 5.0e14, 2000.0
    assert np.isclose(stimulated_to_spontaneous(nu, T),
                      1.0 / (np.exp(H_PLANCK * nu / (K_B * T)) - 1.0), rtol=1e-9)
    # equals Planck / (A/B)
    assert np.isclose(stimulated_to_spontaneous(nu, T),
                      planck_spectral_energy_density(nu, T) / einstein_A_over_B(nu),
                      rtol=1e-9)
    # optical & room T: spontaneous overwhelmingly dominates
    assert stimulated_to_spontaneous(1.21e15, 300.0) < 1e-40
    # low frequency / warm: stimulated dominates (maser/Rayleigh-Jeans regime)
    assert stimulated_to_spontaneous(1.0e9, 300.0) > 100.0
    # crossover (equal rates) at h nu / kT = ln 2
    T2 = 1000.0
    nu_eq = np.log(2.0) * K_B * T2 / H_PLANCK
    assert np.isclose(stimulated_to_spontaneous(nu_eq, T2), 1.0, rtol=1e-9)


# --- laser threshold ---------------------------------------------------------

def test_laser_threshold_value():
    assert np.isclose(laser_threshold(gain=2.0, kappa=0.5, gamma=3.0), 3.0 * 0.5 / 2.0)
    assert np.isclose(laser_threshold(1.0, 1.0, 1.0), 1.0)


def test_laser_below_threshold_no_photons():
    g, k, gam = 1.0, 1.0, 1.0
    Rth = laser_threshold(g, k, gam)
    for R in (0.0, 0.3, 0.9):
        N, n = laser_steady_state(R, g, k, gam)
        assert n == 0.0                          # essentially dark below threshold
        assert np.isclose(N, R / gam)            # inversion rises linearly with pump
        assert N <= k / g + 1e-12                # has not yet reached N_th = kappa/gain
    assert Rth == 1.0


def test_laser_above_threshold_photons_rise_and_inversion_clamps():
    g, k, gam = 1.0, 1.0, 1.0
    Rth = laser_threshold(g, k, gam)
    Ns, ns = [], []
    for R in (1.5, 2.0, 3.0, 5.0):
        N, n = laser_steady_state(R, g, k, gam)
        assert n > 0.0
        assert np.isclose(n, (R - Rth) / k)      # linear photon turn-on
        assert np.isclose(N, k / g)              # gain clamping at N_th
        Ns.append(N); ns.append(n)
    assert all(np.isclose(N, Ns[0]) for N in Ns)             # inversion clamped
    assert ns[0] < ns[1] < ns[2] < ns[3]                     # photons rise with pump


def test_laser_steady_state_satisfies_rate_equations():
    g, k, gam = 1.3, 0.7, 0.4
    for R in (0.1, 0.5, 1.0, 2.0, 4.0):
        state = laser_steady_state(R, g, k, gam)
        Ndot, ndot = laser_rate_rhs(state, R, g, k, gam)
        assert abs(Ndot) < 1e-9 and abs(ndot) < 1e-9        # genuine fixed point


# --- second-order coherence g2(0) --------------------------------------------

def test_g2_canonical_values():
    assert g2_thermal() == 2.0
    assert g2_coherent() == 1.0
    assert g2_fock(1) == 0.0                     # single photon: perfect antibunching
    assert np.isclose(g2_fock(2), 0.5)
    assert np.isclose(g2_fock(1000), 1.0 - 1e-3)  # large Fock -> approaches 1


def test_g2_ordering_antibunched_coherent_bunched():
    # the physical ordering: single-photon < coherent < thermal
    assert g2_fock(1) < g2_coherent() < g2_thermal()


def test_g2_from_distribution_matches_closed_forms():
    nmax = 600
    n = np.arange(nmax)
    # thermal / Bose-Einstein:  p(n) = nbar^n / (1+nbar)^(n+1)  ->  g2 = 2
    nbar = 2.0
    p_th = nbar ** n / (1.0 + nbar) ** (n + 1)
    assert np.isclose(g2_from_distribution(p_th), g2_thermal(), rtol=1e-6)
    # coherent / Poisson:  p(n) = e^-nbar nbar^n / n!  ->  g2 = 1
    from math import lgamma
    lam = 3.0
    logp = -lam + n * np.log(lam) - np.array([lgamma(k + 1) for k in n])
    p_po = np.exp(logp)
    assert np.isclose(g2_from_distribution(p_po), g2_coherent(), rtol=1e-6)
    # Fock |5>:  delta_{n,5}  ->  g2 = 1 - 1/5
    p_fock = np.zeros(nmax); p_fock[5] = 1.0
    assert np.isclose(g2_from_distribution(p_fock), g2_fock(5))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
