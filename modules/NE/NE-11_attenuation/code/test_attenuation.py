"""NE-11 tests -- attenuation, cross sections and reaction rates against
Shultis & Faw §§7.1-7.2, its Examples 7.1-7.3, and the extracted Appendix C.

Run:  python3 test_attenuation.py
"""

import math

from attenuation import (
    AVOGADRO, BARN_CM2, MATERIALS, DENSITY_ERRATA,
    load_photon_coefficients, load_thermal_cross_sections,
    absorption_cross_section, ABSORPTION_CHANNELS,
    mass_coefficient, linear_coefficient,
    uncollided_intensity, interaction_probability, survival_probability,
    path_length_pdf, mean_free_path, half_thickness, tenth_thickness,
    thickness_for_attenuation, mean_free_paths_traversed,
    atom_density, molecular_density, macroscopic_cross_section,
    mixture_mass_coefficient, mixture_density, compound_macroscopic,
    flux_density, reaction_rate_density, fluence,
    point_source_flux, point_source_flux_shielded, point_source_flux_layered,
    buildup_intensity,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the exponential law, and its identity with radioactive decay ----------

def test_attenuation_is_exponential_in_optical_thickness():
    """I(x) = I(0) exp(-mu x) [Eq. (7.4)].  The only variable that matters is
    the product mu*x -- the optical thickness in mean free paths, which is why
    shielding is designed in mfp rather than in centimetres."""
    for mu, x in [(0.07066, 14.15), (0.7721, 1.295), (2.0, 0.5)]:
        assert _approx(uncollided_intensity(1.0, mu, x), math.exp(-mu * x))
    # equal optical thickness, equal transmission, whatever the material
    a = uncollided_intensity(1.0, 0.07066, 1.0 / 0.07066)
    b = uncollided_intensity(1.0, 0.7721, 1.0 / 0.7721)
    assert _approx(a, b) and _approx(a, math.exp(-1.0))
    assert _approx(mean_free_paths_traversed(0.7721, 1.295), 1.0, tol=1e-3)
    assert uncollided_intensity(1.0, 0.5, 0.0) == 1.0


def test_probabilities_are_complementary_and_memoryless():
    """P(x) + Pbar(x) = 1 [Eqs. (7.5)-(7.6)], and the chance of surviving the
    next mfp does not depend on how far the particle has already come -- the same
    memorylessness as radioactive decay in ~NE-06."""
    mu = 0.07066
    for x in (0.5, 14.15, 100.0):
        assert _approx(interaction_probability(mu, x) + survival_probability(mu, x), 1.0)
    for already in (0.0, 10.0, 200.0):
        step = survival_probability(mu, already + 5.0) / survival_probability(mu, already)
        assert _approx(step, survival_probability(mu, 5.0))
    # small-x limit P -> mu dx, the definition of mu [Eq. (7.1)]
    assert _approx(interaction_probability(mu, 1e-7), mu * 1e-7, tol=1e-6)


def test_path_length_distribution_normalises_to_the_mean_free_path():
    """p(x) = mu exp(-mu x) [Eq. (7.7)] integrates to 1 with mean 1/mu
    [Eq. (7.8)].  Integrated numerically."""
    mu = 0.25
    n, xmax = 200000, 60.0 / mu
    h = xmax / n
    total = mean = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        p = path_length_pdf(mu, x)
        total += p * h
        mean += x * p * h
    assert _approx(total, 1.0, tol=1e-4)
    assert _approx(mean, mean_free_path(mu), tol=1e-4)
    assert path_length_pdf(mu, -1.0) == 0.0


def test_thicknesses_mirror_half_lives():
    """x_1/2 = ln2/mu [Eq. (7.9)], x_1/10 = ln10/mu.  Structurally identical to
    the half-life and to `~NE-06`'s time_to_fraction."""
    mu = 0.7721
    assert _approx(half_thickness(mu), math.log(2.0) / mu)
    assert _approx(tenth_thickness(mu), math.log(10.0) / mu)
    assert _approx(thickness_for_attenuation(mu, 2.0), half_thickness(mu))
    assert _approx(thickness_for_attenuation(mu, 10.0), tenth_thickness(mu))
    # each half-thickness halves the beam, exactly as each half-life halves N
    for k in range(1, 6):
        assert _approx(uncollided_intensity(1.0, mu, k * half_thickness(mu)),
                       0.5 ** k)
    # tenth-thickness is ln10/ln2 = 3.32 half-thicknesses
    assert _approx(tenth_thickness(mu) / half_thickness(mu), 3.3219, tol=1e-4)


# --- the book's worked examples --------------------------------------------

def test_reproduces_example_7_1():
    """S&F Example 7.1 (printed p. 182): the thickness of water and of lead that
    reduces a 1 MeV photon beam to a tenth.  Uses mu(water) = 0.07066 /cm and
    mu(lead) = 0.7721 /cm from Appendix C, giving 32.59 cm and 2.98 cm."""
    mu_w = linear_coefficient("water", 1.0)
    mu_pb = linear_coefficient("lead", 1.0)
    assert _approx(mu_w, 0.07066, tol=1e-4), "%.5f" % mu_w
    assert _approx(mu_pb, 0.7721, tol=1e-3), "%.5f" % mu_pb
    assert _approx(tenth_thickness(mu_w), 32.59, tol=1e-3)
    assert _approx(tenth_thickness(mu_pb), 2.98, tol=2e-3)
    # the book quotes 12.8 in and 1.17 in
    assert _approx(tenth_thickness(mu_w) / 2.54, 12.83, tol=2e-3)
    assert _approx(tenth_thickness(mu_pb) / 2.54, 1.175, tol=3e-3)
    # lead is ~11x better per centimetre but only ~1x per gram: the whole
    # difference is density, not any special photon-stopping virtue
    assert _approx(mu_pb / mu_w, 10.93, tol=1e-3)
    assert _approx(mass_coefficient("lead", 1.0) / mass_coefficient("water", 1.0),
                   0.963, tol=1e-3)


def test_reproduces_example_7_2():
    """S&F Example 7.2 (printed p. 184): a 50/50-by-weight iron-lead mixture at
    1 MeV.  (mu/rho)_mix = 0.06377 cm2/g, rho_mix = 9.298 g/cm3, mu = 0.5929 /cm."""
    mix = {"iron": 0.5, "lead": 0.5}
    assert _approx(mass_coefficient("iron", 1.0), 0.05951, tol=1e-4)
    assert _approx(mass_coefficient("lead", 1.0), 0.06803, tol=1e-4)

    mr = mixture_mass_coefficient(mix, 1.0)
    assert _approx(mr, 0.06377, tol=1e-3), "%.5f" % mr

    rho = mixture_density(mix)
    assert _approx(rho, 9.298, tol=1e-3), "%.4f" % rho
    assert _approx(rho * mr, 0.5929, tol=2e-3), "%.4f" % (rho * mr)

    # weight fractions must sum to 1 -- a silent renormalisation would hide a
    # composition error
    for bad in ({"iron": 0.5, "lead": 0.4}, {}):
        for fn in (mixture_mass_coefficient, mixture_density):
            try:
                fn(bad, 1.0) if fn is mixture_mass_coefficient else fn(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("%r should be rejected" % (bad,))


def test_the_iron_density_typo():
    """Example 7.2 prints rho(Fe) = 7.784 g/cm3 and then does arithmetic that
    requires 7.874.  The book's own next line gives 0.2151 cm3 for 2 g of the
    mixture and rho_mix = 9.298; with 7.784 those become 0.2166 and 9.235.

    7.874 g/cm3 is also the accepted density of iron, so the printed value is the
    typo and the arithmetic is correct."""
    printed, used = DENSITY_ERRATA["iron"]
    assert _approx(printed, 7.784) and _approx(used, 7.874)
    assert _approx(MATERIALS["iron"]["density"], used)

    vol_used = 1.0 / used + 1.0 / MATERIALS["lead"]["density"]
    vol_printed = 1.0 / printed + 1.0 / MATERIALS["lead"]["density"]
    assert _approx(vol_used, 0.2151, tol=1e-3), "%.5f" % vol_used
    assert not _approx(vol_printed, 0.2151, tol=1e-3)
    assert _approx(2.0 / vol_used, 9.298, tol=1e-3)
    assert _approx(2.0 / vol_printed, 9.235, tol=1e-3)


def test_reproduces_example_7_3():
    """S&F Example 7.3 (printed p. 184): the macroscopic thermal-neutron
    absorption cross section of water, summed over all five stable isotopes of
    hydrogen and oxygen.  Sigma_a = 0.0223 /cm.

    The point of the example is what it shows about NEGLECT: 1H alone gives the
    same 0.0223, because the other four isotopes are either rare or transparent.
    Cross sections and abundances multiply, so a term needs both to matter."""
    xs = load_thermal_cross_sections()
    n = molecular_density(1.0, 18.0153)
    assert _approx(n / 1e24, 0.03343, tol=1e-3), "%.6f" % (n / 1e24)

    contributions = [(2, 0.99985, absorption_cross_section("1H", xs)),
                     (2, 0.00015, absorption_cross_section("2H", xs)),
                     (1, 0.99756, absorption_cross_section("16O", xs)),
                     (1, 0.00039, absorption_cross_section("17O", xs)),
                     (1, 0.00205, absorption_cross_section("18O", xs))]
    sigma = compound_macroscopic(n, contributions)
    assert _approx(sigma, 0.0223, tol=5e-3), "%.5f" % sigma

    # the cross sections are the ones the book lists
    assert _approx(xs["1H"]["sigma"]["gamma"], 0.333)
    assert _approx(xs["16O"]["sigma"]["gamma"], 0.000190)
    # 17O's 0.239 b is the SUM of (n,alpha) 0.235 and (n,gamma) 0.0038 -- reading
    # the capture column alone would understate its absorption sixtyfold
    assert _approx(absorption_cross_section("17O", xs), 0.239, tol=5e-3)
    assert _approx(xs["17O"]["sigma"]["alpha"], 0.235)
    assert xs["17O"]["sigma"]["alpha"] > 50 * xs["17O"]["sigma"]["gamma"]

    # hydrogen alone reproduces the whole answer to three figures
    h_only = compound_macroscopic(n, contributions[:1])
    assert _approx(h_only, sigma, tol=2e-3)
    # 17O absorbs 1250x more strongly than 16O but is only 0.04% abundant, so it
    # still contributes almost nothing -- BOTH factors have to be large
    assert (absorption_cross_section("17O", xs)
            > 1000 * absorption_cross_section("16O", xs))
    o17 = compound_macroscopic(n, [contributions[3]])
    assert o17 / sigma < 1e-3


# --- microscopic to macroscopic  [§7.1.6] ---------------------------------

def test_number_densities_and_macroscopic_cross_sections():
    """N = rho N_a/A and Sigma = sigma N [Eq. (7.10)], with sigma in barns."""
    assert _approx(atom_density(1.0, 18.0153) / 1e24, 0.03343, tol=1e-3)
    # natural uranium metal: 19.05 g/cm3, A = 238.03
    n_u = atom_density(19.05, 238.03)
    assert _approx(n_u / 1e24, 0.0482, tol=1e-2)
    # 1 barn at 1e24 /cm3 is exactly 1 /cm -- the reason barns and 1e24 cm^-3
    # are the conventional pair
    assert _approx(macroscopic_cross_section(1.0, 1e24), 1.0)
    assert _approx(macroscopic_cross_section(0.0, 1e24), 0.0)
    assert _approx(BARN_CM2, 1e-24)
    for fn, args in [(atom_density, (1.0, 0.0)), (atom_density, (-1.0, 12.0)),
                     (macroscopic_cross_section, (-1.0, 1e24))]:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def test_mass_coefficients_are_density_independent():
    """mu/rho is an intrinsic property [Eq. (7.11)]; mu is not.  Water vapour and
    liquid water have the same mu/rho and wildly different mu -- which is exactly
    why Appendix C tabulates the ratio."""
    mr = mass_coefficient("water", 1.0)
    assert _approx(linear_coefficient("water", 1.0, density=1.0), mr)
    assert _approx(linear_coefficient("water", 1.0, density=0.001), mr * 0.001)
    assert _approx(linear_coefficient("water", 1.0, density=1.0)
                   / linear_coefficient("water", 1.0, density=0.001), 1000.0)


def test_photon_tables_load_and_interpolate_sensibly():
    """Appendix C.3 for the five tabulated materials, plus the interpolation."""
    for m in ("air", "water", "concrete", "iron", "lead"):
        rows = load_photon_coefficients(m)
        assert len(rows) > 20, m
        energies = [e for e, _ in rows]
        assert energies == sorted(energies), m
        # total >= each component, and the energy-absorption coefficient is
        # never larger than the total (it cannot absorb more than it interacts)
        for e, d in rows:
            assert d["total"] >= d["en"] - 1e-12, (m, e)
            assert d["total"] >= d["c"] - 1e-12, (m, e)

    # interpolation returns tabulated values exactly at grid points
    assert _approx(mass_coefficient("water", 1.0), 0.07066)
    assert _approx(mass_coefficient("lead", 1.0), 0.06803)
    # and lies between neighbours off-grid
    lo, hi = mass_coefficient("water", 1.25), mass_coefficient("water", 0.8)
    mid = mass_coefficient("water", 0.9)
    assert lo < mid < hi
    # out of range is an error rather than a silent extrapolation
    for e in (1e-6, 1e6):
        try:
            mass_coefficient("water", e)
        except ValueError:
            pass
        else:
            raise AssertionError("%g MeV should be out of range" % e)
    try:
        load_photon_coefficients("unobtainium")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown material should raise")


def test_pair_production_switches_on_at_1_022_mev():
    """Pair production needs 2 m_e c^2 = 1.022 MeV (~NE-05, ~NE-12), and the
    Appendix C.3 tables show exactly that: mu_pp is identically zero below the
    threshold and non-zero above it."""
    for m in ("water", "lead"):
        rows = load_photon_coefficients(m)
        below = [d["pp"] for e, d in rows if e < 1.022]
        above = [d["pp"] for e, d in rows if e > 1.5]
        assert all(v == 0.0 for v in below), m
        assert all(v > 0.0 for v in above), m


# --- flux, reaction rates and fluence  [§7.2] -----------------------------

def test_flux_density_and_reaction_rate():
    """phi = v n [Eq. (7.14)]; R = mu phi [Eq. (7.15)].  A 2200 m/s thermal
    neutron population of 1e8 /cm3 gives phi = 2.2e13 /cm2/s."""
    phi = flux_density(1e8, 2.2e5)
    assert _approx(phi, 2.2e13)
    assert _approx(reaction_rate_density(0.0223, phi), 0.0223 * phi)
    # rate is linear in both factors, and zero if either vanishes
    assert reaction_rate_density(0.0, phi) == 0.0
    assert reaction_rate_density(0.0223, 0.0) == 0.0
    assert _approx(reaction_rate_density(0.0223, 2 * phi),
                   2 * reaction_rate_density(0.0223, phi))
    for fn, args in [(flux_density, (-1.0, 1.0)), (reaction_rate_density, (1.0, -1.0)),
                     (fluence, (1.0, -1.0))]:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def test_fluence_is_the_time_integral_of_flux():
    """Phi = phi t for a steady field [Eq. (7.21)].  Flux measures the RATE of
    interactions; fluence measures the cumulative number, and dose limits are
    written against fluence (~NE-17)."""
    assert _approx(fluence(1e6, 3600.0), 3.6e9)
    assert _approx(fluence(1e6, 0.0), 0.0)
    # halving the flux and doubling the time gives the same fluence
    assert _approx(fluence(5e5, 7200.0), fluence(1e6, 3600.0))


# --- point sources  [§7.2.5] -----------------------------------------------

def test_point_source_falls_off_as_inverse_square():
    """phi = S/(4 pi r^2) [Eq. (7.23)] -- geometric attenuation, a power law."""
    s = 3.7e10                                # 1 Ci
    assert _approx(point_source_flux(s, 100.0), s / (4 * math.pi * 1e4))
    assert _approx(point_source_flux(s, 100.0) / point_source_flux(s, 1000.0), 100.0)
    for bad in (0.0, -1.0):
        try:
            point_source_flux(s, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("r = %r should be rejected" % bad)


def test_geometric_and_material_attenuation_are_different_animals():
    """[Eqs. (7.25)-(7.26)] Distance buys a POWER LAW; shielding buys an
    EXPONENTIAL.  Ten centimetres of lead beats moving ten times further away by
    a factor of 20 -- and another ten centimetres beats it by 45 000."""
    s, r, mu = 3.7e10, 100.0, linear_coefficient("lead", 1.0)
    bare = point_source_flux(s, r)
    assert _approx(point_source_flux_shielded(s, r, mu, 0.0), bare)
    shielded_10 = point_source_flux_shielded(s, r, mu, 10.0)
    further = point_source_flux(s, 10 * r)          # ten times the distance
    assert shielded_10 < further
    assert _approx(further / shielded_10, 22.6, tol=1e-2), "%.2f" % (further / shielded_10)
    # doubling the shield squares the attenuation; doubling the distance quarters it
    shielded_20 = point_source_flux_shielded(s, r, mu, 20.0)
    assert _approx(shielded_20 / bare, (shielded_10 / bare) ** 2)
    assert _approx(point_source_flux(s, 2 * r) / bare, 0.25)


def test_layered_shields_add_in_mean_free_paths():
    """[Eq. (7.27)] The exponent is sum(mu_i t_i): shields compose by optical
    thickness, and the ORDER does not matter for uncollided flux."""
    s, r = 3.7e10, 100.0
    mu_pb = linear_coefficient("lead", 1.0)
    mu_fe = linear_coefficient("iron", 1.0)
    a = point_source_flux_layered(s, r, [(mu_pb, 2.0), (mu_fe, 5.0)])
    b = point_source_flux_layered(s, r, [(mu_fe, 5.0), (mu_pb, 2.0)])
    assert _approx(a, b)
    # equivalent to applying the two shields in sequence
    step = point_source_flux_shielded(s, r, mu_pb, 2.0) / point_source_flux(s, r)
    assert _approx(a, point_source_flux_shielded(s, r, mu_fe, 5.0) * step)
    assert _approx(point_source_flux_layered(s, r, []), point_source_flux(s, r))


def test_buildup_never_reduces_the_field():
    """I = B I^o [§7.1.5] with B >= 1.  Uncollided attenuation is a LOWER BOUND
    on the true field, and for thick shields it is not a small correction -- so a
    shield designed on exponential attenuation alone is under-designed."""
    i_unc = uncollided_intensity(1.0, 0.7721, 5.0)
    assert _approx(buildup_intensity(1.0, 0.7721, 5.0, 1.0), i_unc)
    assert buildup_intensity(1.0, 0.7721, 5.0, 4.5) > i_unc
    assert _approx(buildup_intensity(1.0, 0.7721, 5.0, 4.5), 4.5 * i_unc)
    try:
        buildup_intensity(1.0, 0.7721, 5.0, 0.5)
    except ValueError:
        pass
    else:
        raise AssertionError("B < 1 should be rejected")


def test_thermal_cross_section_table_is_sane():
    """Appendix C.1 spot checks against numbers every reactor engineer knows."""
    xs = load_thermal_cross_sections()
    assert len(xs) == 27, len(xs)
    # 10B and 6Li are the standard thermal-neutron absorbers
    assert xs["10B"]["sigma"]["alpha"] > 3000
    assert xs["6Li"]["sigma"]["alpha"] > 900
    # 235U fissions; 238U does not have a thermal fission entry worth the name
    assert xs["235U"]["sigma"]["f"] > 500
    # 233Th has the largest capture cross section in this table
    biggest = max(xs, key=lambda k: xs[k]["sigma"].get("gamma", 0.0))
    assert biggest == "233Th", biggest
    # scattering is NOT absorption: 1H scatters 30.5 b and absorbs 0.333 b, which
    # is exactly why it moderates well and poisons only mildly (~NE-08, ~NE-19)
    assert xs["1H"]["sigma"]["s"] > 90 * absorption_cross_section("1H", xs)
    assert "s" not in ABSORPTION_CHANNELS
    for nuc in xs:
        assert absorption_cross_section(nuc, xs) >= 0.0
    try:
        absorption_cross_section("999Zz", xs)
    except KeyError:
        pass
    else:
        raise AssertionError("unknown nuclide should raise")


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
