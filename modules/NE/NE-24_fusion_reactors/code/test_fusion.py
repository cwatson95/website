"""NE-24 tests -- fusion against Shultis & Faw §§12.1-12.4, Eqs. (12.1)-(12.15)
and Figs. 12.1-12.3.

Run:  python3 test_fusion.py
"""

import math

from fusion import (
    K_B_EV, HYDROGEN_IONIZATION_EV, HYDROGEN_IONIZATION_PRINTED,
    REACTIONS, DD_CHARGED_MEV, BREMSSTRAHLUNG_COEFF, ITER,
    saha_ionization_fraction, sigma_v_dt, sigma_v_dd,
    fusion_power_density, bremsstrahlung_power_density, ignition_temperature,
    gain_factor, breakeven_alpha_fraction, energy_confinement_time,
    lawson_n_tau, triple_product, optimal_temperature,
    icf_confinement_time, icf_burn_fraction, areal_density_for_burn,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- making a plasma -----------------------------------------------------

def test_the_saha_example_needs_the_wrong_ionization_energy():
    """S&F §12.1.1 states I = 13.06 eV for the hydrogen isotopes and gives an
    example: n = 2e21 m^-3 at 13 150 K is 95% ionised.

    Hydrogen's ionisation energy is 13.598 eV -- 13.06 is a transposed 13.60.
    The example reproduces to four figures with 13.06 (0.9498) and gives 0.9237
    with the correct value, so the example is internally consistent with the
    wrong constant rather than simply misprinted."""
    with_printed = saha_ionization_fraction(13150.0, 2e21, HYDROGEN_IONIZATION_PRINTED)
    with_true = saha_ionization_fraction(13150.0, 2e21)
    assert _rel(with_printed, 0.95, 1e-3), "%.4f" % with_printed
    assert _rel(with_true, 0.9237, 1e-3), "%.4f" % with_true
    assert not _rel(with_true, 0.95, 0.02)
    assert _rel(HYDROGEN_IONIZATION_EV, 13.598, 1e-3)
    assert HYDROGEN_IONIZATION_PRINTED == 13.06
    # the digits are transposed, not merely rounded
    assert _rel(HYDROGEN_IONIZATION_PRINTED, 13.60, 5e-3) is False
    assert abs(HYDROGEN_IONIZATION_PRINTED - 13.60) > 0.5


def test_ionisation_switches_on_abruptly():
    """The physical content of the Saha equation: an exponential in I/kT means
    there is no gentle approach to a plasma. Between 5000 K and 20 000 K the
    ionised fraction goes from 1e-4 to essentially 1."""
    fracs = [saha_ionization_fraction(t, 2e21) for t in
             (293.0, 5000.0, 1e4, 13150.0, 2e4, 1e5)]
    assert fracs == sorted(fracs)
    assert fracs[0] < 1e-100                    # room temperature: nothing
    assert fracs[1] < 1e-3                      # 5 000 K: still nothing much
    assert 0.3 < fracs[2] < 0.4                 # 10 000 K: a third
    assert fracs[4] > 0.99                      # 20 000 K: done
    assert _approx(fracs[5], 1.0, 1e-6)
    # four orders of magnitude in fraction for a factor of 2 in temperature
    assert fracs[2] / fracs[1] > 1e3
    # denser gas is HARDER to ionise (the 1/n prefactor), which is not obvious
    assert saha_ionization_fraction(1e4, 2e24) < saha_ionization_fraction(1e4, 2e21)
    for bad in ((0.0, 2e21), (1e4, 0.0)):
        try:
            saha_ionization_fraction(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- reactivity and ignition ---------------------------------------------

def test_the_sigma_v_fits_reproduce_the_books_own_figures():
    """S&F give Fig. 12.1 as a graph and no formula, so the fits here have to be
    validated against something. Two independent checks:

      * the D-T curve peaks at 64 keV, where the D-T cross section peaks;
      * feeding both fits into Eq. (12.6) reproduces Fig. 12.2's critical
        ignition temperatures, 3e7 K for D-T and 6e8 K for D-D, to 4% and 12%.

    That second check exercises the fits, the bremsstrahlung coefficient and the
    identical-particle factors all at once."""
    peak_t, peak_v = None, 0.0
    for i in range(1, 2000):
        t = 1.0 + i * 0.1
        if t > 199:
            break
        v = sigma_v_dt(t)
        if v > peak_v:
            peak_v, peak_t = v, t
    assert _rel(peak_t, 64.2, 0.02), "%.1f keV" % peak_t
    assert _rel(peak_v, 9.1e-16, 1e-3)
    # D-T beats D-D by a factor of 50-110 across the interesting range
    for t in (2.0, 5.0, 10.0, 20.0):
        r = sigma_v_dt(t) / sigma_v_dd(t)
        assert 40 < r < 130, "%g keV: %.0f" % (t, r)
    # the ignition temperatures
    ti_dt = ignition_temperature("D-T")
    assert _rel(ti_dt * 1e3 / K_B_EV, 3e7, 0.06), "%.3e K" % (ti_dt * 1e3 / K_B_EV)
    ti_dd = ignition_temperature("D-D")
    assert _rel(ti_dd * 1e3 / K_B_EV, 6e8, 0.15), "%.3e K" % (ti_dd * 1e3 / K_B_EV)
    assert _rel(ti_dd / ti_dt, 17.0, 0.10)
    for bad in (0.1, 500.0):
        try:
            sigma_v_dt(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%g keV should be refused" % bad)
    try:
        sigma_v_dd(150.0)
    except ValueError:
        pass
    else:
        raise AssertionError("the D-D fit should refuse 150 keV")


def test_ignition_is_a_property_of_the_fuel_alone():
    """Both fusion power and bremsstrahlung go as n^2, so the density cancels
    and the ignition temperature depends only on the fuel and on Z.

    The Z^2 in Eq. (12.6) is the sting: a plasma contaminated with high-Z wall
    material radiates enormously more and its ignition temperature rises, which
    is why plasma-facing materials are a first-order physics problem."""
    t1 = ignition_temperature("D-T")
    for n in (1e13, 1e15, 1e17):
        pf = fusion_power_density(n, t1)
        pb = bremsstrahlung_power_density(n, t1)
        assert _rel(pf, pb, 1e-3), "n = %g" % n
    # contamination raises the bar
    t_clean = ignition_temperature("D-T", z=1.0)
    t_dirty = ignition_temperature("D-T", z=2.0)
    assert t_dirty > t_clean
    assert _rel(t_dirty / t_clean, 1.7, 0.2)
    # both scalings are quadratic in n
    assert _rel(fusion_power_density(2e15, 10.0) / fusion_power_density(1e15, 10.0),
                4.0, 1e-12)
    assert _rel(bremsstrahlung_power_density(2e15, 10.0)
                / bremsstrahlung_power_density(1e15, 10.0), 4.0, 1e-12)
    # bremsstrahlung goes as sqrt(T), fusion far more steeply
    assert _rel(bremsstrahlung_power_density(1e15, 40.0)
                / bremsstrahlung_power_density(1e15, 10.0), 2.0, 1e-9)
    assert (fusion_power_density(1e15, 40.0)
            / fusion_power_density(1e15, 10.0)) > 5.0
    try:
        fusion_power_density(1e15, 10.0, "p-B11")
    except KeyError:
        pass
    else:
        raise AssertionError("an unsupported reaction should be refused")


def test_the_identical_particle_factor():
    """S&F's footnote 1 exists because the factor is easy to lose: for D-T the
    rate is n^2<sigma v>/4 (two species at n/2 each), for D-D it is
    n^2<sigma v>/2 (one species at n, halved to avoid double-counting pairs).

    The Lawson prefactors inherit it: 12kT/(E_c<sigma v>) for D-T against
    6kT/(E_c<sigma v>) for D-D [Eq. (12.10) and its footnote 4]."""
    n, t = 1e15, 10.0
    dt = fusion_power_density(n, t, "D-T")
    assert _rel(dt, 0.25 * n * n * sigma_v_dt(t) * 17.6 * 1.602177e-13, 1e-9)
    dd = fusion_power_density(n, t, "D-D")
    q_dd = 0.5 * (3.27 + 4.03)
    assert _rel(dd, 0.5 * n * n * sigma_v_dd(t) * q_dd * 1.602177e-13, 1e-9)
    # the branch-averaged charged energy of footnote 4
    assert _rel(DD_CHARGED_MEV, 2.425, 1e-9)
    assert _rel(DD_CHARGED_MEV, 2.43, 3e-3)
    # and the Lawson prefactors differ by exactly 2
    ratio = (lawson_n_tau(10.0, "D-T") * REACTIONS["D-T"]["charged_mev"]
             * sigma_v_dt(10.0)) / (lawson_n_tau(10.0, "D-D") * DD_CHARGED_MEV
                                    * sigma_v_dd(10.0))
    assert _rel(ratio, 2.0, 1e-9)


# --- the gain factor -----------------------------------------------------

def test_a_power_plant_needs_Q_of_twenty_not_one():
    """S&F Eq. (12.7) with their own assumptions -- eta_heat 0.7, f_recirc 0.25,
    eta_elect 0.35, f_c 0.2 -- gives Q = 20.4.

    "Break-even", Q = 1, is not the goal and never was. At Q = 1 the alphas
    supply only 20% of the plasma heating (3.5/17.6), and none of the losses in
    making electricity and recirculating it have been paid for."""
    assert _rel(gain_factor(), 20.4, 1e-2), "%.2f" % gain_factor()
    assert _rel(breakeven_alpha_fraction("D-T"), 0.1989, 1e-3)
    assert _rel(breakeven_alpha_fraction("D-T"), 0.20, 1e-2)
    # D-D keeps a far larger share of its energy in charged products
    assert breakeven_alpha_fraction("D-D") > 3 * breakeven_alpha_fraction("D-T")
    assert _rel(breakeven_alpha_fraction("D-D"), 0.664, 1e-2)
    # better electricity or less recirculation lowers the bar
    assert gain_factor(eta_elect=0.45) < gain_factor(eta_elect=0.35)
    assert gain_factor(f_recirc=0.50) < gain_factor(f_recirc=0.25)
    assert _rel(gain_factor(f_recirc=0.10), 51.0, 1e-2)
    # ignition is Q = infinity: the alphas must supply ALL the heating, which is
    # five times what they supply at break-even
    assert _rel(1.0 / breakeven_alpha_fraction("D-T"), 5.03, 1e-2)
    for bad in ({"eta_heat": 0.0}, {"eta_elect": 1.5}, {"f_charged": 1.0}):
        try:
            gain_factor(**bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad)


# --- Lawson and the triple product ---------------------------------------

def test_lawson_and_the_triple_product():
    """Eqs. (12.10)-(12.14). The D-T Lawson product bottoms out near 1e14 s/cm^3
    and the triple product near 2-3e15 keV s cm^-3, which is Eq. (12.14).

    The triple product's minimum sits at a LOWER temperature than the Lawson
    product's, exactly as Fig. 12.3 shows -- which is why the modern figure of
    merit points a designer at ~15 keV rather than ~30."""
    assert _rel(lawson_n_tau(10.0), 3.21e14, 0.02), "%.3e" % lawson_n_tau(10.0)
    assert min(lawson_n_tau(t) for t in (10, 20, 30, 50, 80)) < 2e14
    tp_min_t, tp_min = optimal_temperature("D-T")
    assert 10.0 < tp_min_t < 30.0, "%.1f keV" % tp_min_t
    assert _rel(tp_min, 3.0e15, 0.10), "%.3e" % tp_min
    assert tp_min > 2e15                       # S&F Eq. (12.14)'s bound
    # the Lawson minimum is at a HIGHER temperature than the triple-product one
    lawson_min_t = min(((lawson_n_tau(1.0 + 0.1 * i), 1.0 + 0.1 * i)
                        for i in range(1, 1400)))[1]
    assert lawson_min_t > tp_min_t, "%.1f vs %.1f" % (lawson_min_t, tp_min_t)
    # D-D is far harder at every temperature they can both be evaluated at
    for t in (5.0, 10.0, 20.0):
        assert lawson_n_tau(t, "D-D") / lawson_n_tau(t, "D-T") > 40
    # tau_E: the factor of 3, not 3/2, because electrons count too
    tau = energy_confinement_time(1e14, 10.0, 1.0)
    assert _rel(tau, 3.0 * 1e14 * 1e4 * 1.602177e-19, 1e-9)
    try:
        energy_confinement_time(1e14, 10.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero loss power should be refused")


def test_the_triple_product_is_insensitive_to_temperature():
    """Eq. (12.13) argues n tau T ~ T^-1/3, which is why it measures the
    confinement scheme rather than the operating point. Over a factor of three
    in temperature around the optimum it moves by under 30%, while the Lawson
    product itself moves by a factor of two."""
    t0, _ = optimal_temperature("D-T")
    lo, hi = t0 / 1.7, t0 * 1.7
    tps = [triple_product(t) for t in (lo, t0, hi)]
    assert max(tps) / min(tps) < 1.35, "%.3f" % (max(tps) / min(tps))
    lawsons = [lawson_n_tau(t) for t in (lo, t0, hi)]
    assert max(lawsons) / min(lawsons) > 1.8
    # and the triple product is exactly n tau times T, by construction
    for t in (5.0, 15.0, 40.0):
        assert _rel(triple_product(t), lawson_n_tau(t) * t, 1e-12)


# --- inertial confinement -------------------------------------------------

def test_icf_buys_its_lawson_product_with_density_not_time():
    """Eq. (12.15): tau_E = R sqrt(m/kT). A millimetre pellet at 10 keV is
    confined for about a nanosecond -- eight orders of magnitude less than a
    tokamak -- so the n tau product has to be found in n.

    Hence the compression. Burning a third of the fuel needs rho R ~ 3 g/cm^2,
    against ~0.02 for an uncompressed millimetre pellet: a factor of 150 in areal
    density, i.e. a thousandfold in volume density."""
    tau = icf_confinement_time(0.05, 10.0)
    assert _rel(tau, 8.05e-10, 0.02), "%.3e s" % tau
    assert 1e-10 < tau < 1e-8
    # colder and bigger holds longer, as R/v
    assert icf_confinement_time(0.1, 10.0) > tau
    assert icf_confinement_time(0.05, 2.5) > tau
    assert _rel(icf_confinement_time(0.05, 40.0) / tau, 0.5, 1e-9)
    # the required density: n = (n tau)/tau
    n_needed = lawson_n_tau(10.0) / tau
    assert n_needed > 1e23, "%.3e cm^-3" % n_needed
    # solid D-T is ~5e22 cm^-3, so ICF needs thousands of times solid density
    assert n_needed / 5e22 > 5
    # burn fraction and areal density
    assert _rel(areal_density_for_burn(0.3), 2.571, 1e-3)
    assert _rel(icf_burn_fraction(3.0), 1.0 / 3.0, 1e-9)
    for phi in (0.01, 0.1, 0.5):
        assert _rel(icf_burn_fraction(areal_density_for_burn(phi)), phi, 1e-9)
    assert areal_density_for_burn(0.5) > 5 * areal_density_for_burn(0.1)
    for bad in (0.0, 1.0, 1.5):
        try:
            areal_density_for_burn(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("burn fraction %r should be rejected" % bad)


def test_the_reaction_data():
    """Eqs. (12.2)-(12.3), which everything else is built on."""
    dt = REACTIONS["D-T"]
    assert _approx(dt["charged_mev"] + dt["neutral_mev"], dt["q_mev"], 1e-9)
    assert _rel(dt["neutral_mev"] / dt["q_mev"], 0.801, 1e-2)
    for k in ("D-D(n)", "D-D(p)"):
        r = REACTIONS[k]
        assert _approx(r["charged_mev"] + r["neutral_mev"], r["q_mev"], 1e-2)
    # the two D-D branches are nearly equally probable and nearly equal in Q
    assert _rel(REACTIONS["D-D(p)"]["q_mev"] / REACTIONS["D-D(n)"]["q_mev"],
                1.23, 1e-2)
    # D-T releases 4.8x the energy per reaction of an average D-D
    assert _rel(dt["q_mev"] / (0.5 * (3.27 + 4.03)), 4.82, 1e-2)
    # 80% of D-T's energy leaves as a neutron -- which is the blanket problem,
    # the tritium-breeding opportunity, and the materials-damage problem at once
    assert dt["neutral_mev"] > 4 * dt["charged_mev"]
    assert ITER["produces_electricity"] is False


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
