"""NE-26 tests -- industrial and research applications against Shultis & Faw
Chapter 13 and Tables 13.1-13.3.

Run:  python3 test_applications.py
"""

import math

from applications import (
    PRODUCTION_ROUTES, APPLICATION_CATEGORIES, RADIOGRAPHY_SOURCES,
    NAA_SENSITIVITY, PROCESS_DOSES, GENERATORS,
    activation_activity, saturation_fraction, irradiation_time_for,
    generator_daughter_activity, optimal_milking_time,
    tracer_dilution_volume, flow_rate_from_tracer, transit_flow_rate,
    transmission, thickness_from_transmission, gauge_precision,
    optimal_gauge_thickness, geometric_unsharpness, naa_detectable_mass,
    radiodate,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- production -----------------------------------------------------------

def test_the_production_route_determines_the_decay_mode():
    """§13.1's organising insight. Reactor irradiation and fission both give
    NEUTRON-RICH products, which decay beta-minus; accelerators give
    PROTON-RICH products, which decay beta-plus.

    That is why every PET isotope comes from a cyclotron and no PET isotope
    comes from a reactor (~NE-27)."""
    assert len(PRODUCTION_ROUTES) == 3
    assert PRODUCTION_ROUTES["accelerator"]["decay"] == "beta-plus"
    for k in ("reactor irradiation", "fission-product recovery"):
        assert PRODUCTION_ROUTES[k]["decay"] == "beta-minus"
    # the accelerator reactions all remove neutrons or add protons
    for rxn in PRODUCTION_ROUTES["accelerator"]["examples"]:
        assert rxn.startswith(tuple("0123456789"))
        assert "(p," in rxn
    # and the reactor reactions are all neutron-induced
    for rxn in PRODUCTION_ROUTES["reactor irradiation"]["examples"]:
        assert "(n," in rxn


def test_activation_saturates_and_never_arrives():
    """A(t) = R(1 - e^{-lambda t}). Three half-lives gets 87.5% of saturation and
    ten gets 99.9%, so nobody irradiates for ten -- the extra seven half-lives
    buy 12 percentage points."""
    assert _approx(saturation_fraction(1.0, 1.0), 0.5)
    assert _approx(saturation_fraction(3.0, 1.0), 0.875)
    assert _rel(saturation_fraction(10.0, 1.0), 0.999023, 1e-5)
    # the last 12% costs seven half-lives
    assert _rel(irradiation_time_for(0.875, 1.0), 3.0, 1e-9)
    assert _rel(irradiation_time_for(0.999, 1.0), 9.97, 1e-2)
    assert _rel(activation_activity(100.0, 1.0, 1.0), 50.0, 1e-9)
    assert _rel(activation_activity(100.0, 1.0, 1e6), 100.0, 1e-9)
    # round trip
    for f in (0.1, 0.5, 0.9, 0.99):
        assert _rel(saturation_fraction(irradiation_time_for(f, 5.0), 5.0), f, 1e-9)
    # saturation is asymptotic
    for bad in (1.0, 1.5, 0.0):
        try:
            irradiation_time_for(bad, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("fraction %r should be refused" % bad)


def test_the_99mo_cow_says_when_to_milk_it():
    """§13.1 calls 99mTc "the most widely used radioisotope in medical
    diagnoses" and describes the generator without the transient equilibrium
    that operates it.

    99mTc ingrowth peaks 48.5 hours -- two days -- after elution, which is
    exactly why hospital generators are delivered weekly and eluted daily."""
    t = optimal_milking_time("99Mo")
    assert _rel(t, 48.5, 1e-2), "%.2f h" % t
    assert 40 < t < 55
    # the activity really does peak there
    peak = generator_daughter_activity(t)
    for other in (t / 2, t * 0.9, t * 1.1, t * 2):
        assert generator_daughter_activity(other) <= peak + 1e-12
    # after a day it is already at 80% of the peak, which is why daily elution works
    assert generator_daughter_activity(24.0) / peak > 0.75
    assert _approx(generator_daughter_activity(0.0), 0.0)
    # the parent must outlive the daughter for a generator to work at all
    for parent, (tp, _, td) in GENERATORS.items():
        assert tp > 10 * td, parent
    # 137Cs/137mBa is the extreme case: a 30-year parent, a 2.5-minute daughter
    assert _rel(GENERATORS["137Cs"][0] / GENERATORS["137Cs"][2], 6.2e6, 0.05)
    try:
        optimal_milking_time("235U")
    except KeyError:
        pass
    else:
        raise AssertionError("an unlisted generator should be refused")


# --- tracers --------------------------------------------------------------

def test_tracer_dilution_needs_no_absolute_calibration():
    """§13.3.6: V = V0(C0/C). The point S&F make and it is worth pinning: only
    the RATIO enters, so detector efficiency, geometry and absolute calibration
    all cancel.

    That is why one technique serves a river estuary, a blast furnace and a human
    bloodstream."""
    v = tracer_dilution_volume(10.0, 1e6, 2.5)
    assert _rel(v, 4.0e6, 1e-9)
    # scaling both concentrations by any factor changes nothing
    for k in (0.01, 3.0, 1e4):
        assert _rel(tracer_dilution_volume(10.0, 1e6 * k, 2.5 * k), v, 1e-9)
    # and a dilution cannot concentrate
    try:
        tracer_dilution_volume(10.0, 1.0, 2.0)
    except ValueError as exc:
        assert "concentrate" in str(exc)
    else:
        raise AssertionError("C > C0 should be refused")
    for bad in ((0.0, 1e6, 1.0), (10.0, 0.0, 1.0), (10.0, 1e6, 0.0)):
        try:
            tracer_dilution_volume(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_rate_balance_needs_no_cross_section():
    """§13.3.4: inject at a constant Q0 and the tracer must reappear downstream
    at the same rate, so q = Q0/C -- with no knowledge of the channel's geometry
    at all. That is why it is the method used on rivers, and the peak-to-peak
    method is the one used on pipelines."""
    q = flow_rate_from_tracer(1e7, 50.0)
    assert _rel(q, 2e5, 1e-9)
    assert _rel(flow_rate_from_tracer(2e7, 50.0), 2 * q, 1e-9)
    # the transit method needs an area and the rate balance does not
    qp = transit_flow_rate(1000.0, 500.0, 0.5)
    assert _rel(qp, 1.0, 1e-9)
    assert _rel(transit_flow_rate(1000.0, 250.0, 0.5), 2 * qp, 1e-9)
    for bad in ((0.0, 50.0), (1e7, 0.0)):
        try:
            flow_rate_from_tracer(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    # radiodating: one half-life halves the activity
    assert _rel(radiodate(0.5, 5730.0), 5730.0, 1e-9)
    assert _rel(radiodate(0.25, 5730.0), 11460.0, 1e-9)
    assert _approx(radiodate(1.0, 5730.0), 0.0)
    try:
        radiodate(1.5, 5730.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a ratio above 1 should be refused")


# --- gauges ---------------------------------------------------------------

def test_the_transmission_gauge_optimum_is_exactly_two_mean_free_paths():
    """The design rule Chapter 13 does not contain. Minimising

        sigma_t/t = e^{mu t/2}/(mu t sqrt(N0))

    over mu at fixed t gives mu*t = 2 exactly -- two mean free paths.

    Two effects fight: more attenuation gives more signal per unit thickness and
    fewer counts. The optimum is where they balance, and it is forgiving:
    1.9x worse at 0.5 mfp and 2.5x worse at 6."""
    assert _approx(optimal_gauge_thickness(), 2.0)
    assert _rel(optimal_gauge_thickness(0.4), 5.0, 1e-9)
    # verified numerically
    best = min(((gauge_precision(m / 100.0, 1.0, 1e6), m / 100.0)
                for m in range(1, 1500)))
    assert _rel(best[1], 2.0, 5e-3), "%.4f" % best[1]
    # the penalty on either side
    p2 = gauge_precision(2.0, 1.0, 1e6)
    assert _rel(gauge_precision(0.5, 1.0, 1e6) / p2, 1.89, 1e-2)
    assert _rel(gauge_precision(6.0, 1.0, 1e6) / p2, 2.46, 1e-2)
    assert _rel(gauge_precision(1.0, 1.0, 1e6) / p2, 1.21, 1e-2)
    # precision improves as 1/sqrt(counts), as counting statistics demand
    assert _rel(gauge_precision(2.0, 1.0, 4e6) / p2, 0.5, 1e-9)
    # the gauge reads back correctly
    for mu, t in ((0.5, 4.0), (2.0, 1.0)):
        assert _rel(thickness_from_transmission(transmission(mu, t), mu), t, 1e-9)
    for bad in ((0.0, 1.0, 1e6), (2.0, 0.0, 1e6), (2.0, 1.0, 0.0)):
        try:
            gauge_precision(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_radiography_is_not_run_at_the_gauge_optimum():
    """Table 13.2's source/thickness pairs run 2 to 9 mean free paths, not 2.

    That is not an inconsistency: a thickness gauge minimises the variance of a
    thickness estimate, while radiography maximises contrast through a workpiece
    of fixed thickness. Same attenuation law, different objective function -- and
    conflating them is the obvious way to misuse the mu*t = 2 rule."""
    mus = {0.084: 1.5, 0.34: 0.75, 0.662: 0.57, 1.25: 0.42}
    products = []
    for k, (t12, e, thick) in RADIOGRAPHY_SOURCES.items():
        products.append(mus[e] * thick)
    assert min(products) > 1.5
    assert max(products) > 8.0
    assert not all(abs(p - 2.0) < 1.0 for p in products)
    # harder gammas penetrate more steel, monotonically
    by_energy = sorted(RADIOGRAPHY_SOURCES.values(), key=lambda v: v[1])
    thicknesses = [v[2] for v in by_energy]
    assert thicknesses == sorted(thicknesses)
    assert _rel(thicknesses[-1] / thicknesses[0], 18.3, 1e-2)
    # geometric unsharpness: smaller source, farther away, closer to the film
    u = geometric_unsharpness(3.0, 5.0, 100.0)
    assert _rel(u, 0.15, 1e-9)
    assert geometric_unsharpness(1.0, 5.0, 100.0) < u
    assert geometric_unsharpness(3.0, 5.0, 300.0) < u
    assert geometric_unsharpness(3.0, 1.0, 100.0) < u
    try:
        geometric_unsharpness(0.0, 5.0, 100.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a zero source size should be refused")


def test_naa_sensitivity_spans_seven_decades():
    """Table 13.3. Europium is detectable at 0.9 picograms and iron only at
    10 micrograms -- seven orders of magnitude, set by the activation cross
    section and by whether the product emits a distinguishable gamma.

    NAA is therefore not a general-purpose assay: it is exquisite for a few dozen
    elements and blind to the rest, which is exactly why §13.4.7 lists what it is
    used for (forensics, geology, pesticide residues) rather than claiming it is
    universal."""
    best = min(NAA_SENSITIVITY.values())
    worst = max(NAA_SENSITIVITY.values())
    assert _rel(worst / best, 1.11e7, 0.02)
    assert min(NAA_SENSITIVITY, key=lambda k: NAA_SENSITIVITY[k]) == "Eu"
    assert max(NAA_SENSITIVITY, key=lambda k: NAA_SENSITIVITY[k]) == "Fe"
    # a picogram of europium is about 4e9 atoms -- a real physical limit
    atoms = 0.9e-12 / 152.0 * 6.022e23
    assert 1e9 < atoms < 1e10
    # scaling with flux and time
    assert _rel(naa_detectable_mass("Eu", 1.0, 1e14),
                NAA_SENSITIVITY["Eu"] / 10.0, 1e-9)
    assert _rel(naa_detectable_mass("Eu", 10.0), NAA_SENSITIVITY["Eu"] / 10.0, 1e-9)
    for bad in (("Eu", 0.0), ("Eu", 1.0, 0.0)):
        try:
            naa_detectable_mass(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    try:
        naa_detectable_mass("Pb")
    except KeyError:
        pass
    else:
        raise AssertionError("an element not in Table 13.3 should be refused")


def test_process_doses_span_a_factor_of_400():
    """§13.5. "Irradiation" covers 60 Gy to stop a potato sprouting and 25 000 Gy
    to sterilise a syringe -- a factor of 400, and the same word.

    Note where the doses sit relative to ~NE-18: 60 Gy is twenty times an
    unambiguously lethal human dose, and the lowest process dose here is already
    far outside anything in Table 9.7."""
    lows = [v[0] for v in PROCESS_DOSES.values()]
    assert _rel(max(lows) / min(lows), 417.0, 0.02)
    assert PROCESS_DOSES["sprout inhibition (potatoes, onions)"][0] == 60.0
    assert PROCESS_DOSES["medical sterilisation"][0] == 2.5e4
    # ordered by dose, the applications go: sprouting, insects, bacteria, spores
    order = sorted(PROCESS_DOSES, key=lambda k: PROCESS_DOSES[k][0])
    assert order[0].startswith("sprout")
    assert "sterilisation" in order[-1] or "sterilisation" in order[-2]
    # every one of them is far above a lethal human dose (~NE-18: LD50/60 ~ 3.5 Gy)
    assert min(lows) / 3.5 > 15
    # and the categories add up to the chapter
    total = sum(len(v) for v in APPLICATION_CATEGORIES.values())
    assert total == 29
    assert len(APPLICATION_CATEGORIES) == 3


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
