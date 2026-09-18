"""NE-19 tests -- the neutron life cycle against Shultis & Faw §§10.1-10.6,
Examples 10.1-10.10 and Tables 10.1-10.8.

Three printed results are contradicted by the book's own numbers and are pinned
here with the evidence that forces each correction; see refs.md.

Run:  python3 test_neutron_cycle.py
"""

import math

from neutron_cycle import (
    K_BOLTZMANN_EV, ROOM_T_K, THERMAL_ENERGY_EV, AVOGADRO,
    FUEL_THERMAL_AVERAGED, FUEL_PROPERTIES, MODERATOR_SLOWING,
    MODERATOR_THERMAL, OPTIMUM_RATIOS, RESONANCE_ROD_CONSTANTS, XI_SIGMA_S,
    LATTICE_TABLE, EPSILON_FIT,
    most_probable_energy, mean_thermal_energy, maxwellian_flux,
    westcott_averaged_cross_section, fast_fission_factor,
    resonance_integral_homogeneous, resonance_escape_homogeneous,
    resonance_integral_rod, resonance_escape_lattice,
    thermal_utilization_homogeneous, thermal_fission_factor, eta_of_uranium,
    bessel_i0, bessel_i1, bessel_k0, bessel_k1, lattice_F, lattice_E,
    thermal_utilization_lattice, cell_radius,
    diffusion_length_squared, thermal_nonleakage, fast_nonleakage,
    geometric_buckling, k_infinity, k_effective,
    four_factor_formula_as_printed, critical_buckling, critical_radius_sphere,
    reactivity, SIGMA_S_D2O_ERRATA, L2_GRAPHITE_ERRATA,
)

NATURAL_U = {"234U": 0.000055, "235U": 0.007204, "238U": 0.992745}


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- thermal neutrons ----------------------------------------------------

def test_the_thermal_energy_and_the_two_kT_trap():
    """kT = 0.0253 eV at S&F's 293.61 K, the energy of a 2200 m/s neutron and the
    reference for every thermal cross section.

    The mean of the Maxwellian FLUX is 2kT, not the (3/2)kT of kinetic theory:
    the flux is the density spectrum weighted by speed, which shifts the mean up.
    Using 3/2 is a 33% error in a reaction rate."""
    assert _rel(most_probable_energy(ROOM_T_K), THERMAL_ENERGY_EV, 1e-3)
    assert _rel(mean_thermal_energy(), 2 * THERMAL_ENERGY_EV, 1e-3)
    assert not _rel(mean_thermal_energy(), 1.5 * THERMAL_ENERGY_EV, 0.2)
    # 0.0253 eV really is a 2200 m/s neutron: E = mv^2/2
    m_n = 1.674927e-27
    e_j = 0.5 * m_n * 2200.0 ** 2
    assert _rel(e_j / 1.602177e-19, THERMAL_ENERGY_EV, 3e-3)
    # the FLUX spectrum is linear in E, peaks at kT and averages 2kT; the
    # DENSITY spectrum goes as sqrt(E), peaks at kT/2 and averages 1.5 kT.
    # The extra factor of sqrt(E) is the neutron speed.
    kt = most_probable_energy()
    for delta in (0.3, 0.5, 0.8, 1.2, 2.0, 4.0):
        assert maxwellian_flux(kt, ROOM_T_K) > maxwellian_flux(kt * delta, ROOM_T_K)
    # numerically integrate to confirm both moments
    n_grid = 20000
    hi = 40.0 * kt
    de = hi / n_grid
    es = [(i + 0.5) * de for i in range(n_grid)]
    w = [maxwellian_flux(e, ROOM_T_K) for e in es]
    norm = sum(w) * de
    mean = sum(e * v for e, v in zip(es, w)) * de / norm
    assert _rel(mean, 2.0 * kt, 1e-3), "%.5f vs %.5f" % (mean, 2 * kt)
    for bad in ((-1.0, 300.0), (1.0, 0.0)):
        try:
            maxwellian_flux(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_two_cross_section_tables_differ_by_the_westcott_factor():
    """Table 10.1 is thermal-AVERAGED; Table 10.2 is at 0.0253 eV.  They differ
    by sqrt(pi)/2 = 0.886 times the Westcott non-1/v factor g(T), which is 1 for
    light nuclei and not for heavy ones.

    For 238U, a good 1/v absorber, the ratio is within 1% of 0.886.  For 235U it
    is 0.867, i.e. g = 0.978 -- the deviation the Westcott factor exists to
    describe.  Mixing the two tables silently is a systematic few-percent error."""
    assert _rel(0.5 * math.sqrt(math.pi), 0.8862, 1e-3)
    ratio_u8 = (FUEL_THERMAL_AVERAGED["238U"]["sigma_a"]
                / FUEL_PROPERTIES["238U"][0])
    assert _rel(ratio_u8, 0.8862, 0.02), "%.4f" % ratio_u8
    ratio_u5 = (FUEL_THERMAL_AVERAGED["235U"]["sigma_a"]
                / FUEL_PROPERTIES["235U"][0])
    assert _rel(ratio_u5, 0.8668, 1e-3), "%.4f" % ratio_u5
    g_u5 = ratio_u5 / (0.5 * math.sqrt(math.pi))
    assert 0.96 < g_u5 < 0.99, "%.4f" % g_u5
    # and the function reproduces the factor
    assert _rel(westcott_averaged_cross_section(1.0), 0.8862, 1e-3)
    # 1/sqrt(T): a hotter core sees a smaller thermal cross section
    assert _rel(westcott_averaged_cross_section(1.0, 4 * ROOM_T_K),
                0.5 * westcott_averaged_cross_section(1.0), 1e-12)
    for bad in ((-1.0,), (1.0, 0.0)):
        try:
            westcott_averaged_cross_section(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- the individual factors ----------------------------------------------

def test_reproduces_example_10_1():
    """S&F Ex. 10.1: f for graphite and natural uranium at N_C/N_U = 450.

    Note the printed working displays the fraction as 6.206 N^U/(6.206 N^U +
    0.003421 N^C) immediately after computing 6.639, and immediately before
    substituting 6.639 again.  The 6.206 is a stray: it reproduces neither the
    line above it nor the answer below it (0.8012 against the printed 0.8118)."""
    sig_u = sum(a * FUEL_THERMAL_AVERAGED[k]["sigma_a"]
                for k, a in NATURAL_U.items())
    assert _rel(sig_u, 6.639, 1e-3), "%.4f" % sig_u
    sig_c = westcott_averaged_cross_section(0.00386)
    assert _rel(sig_c, 0.003421, 1e-3)
    f = thermal_utilization_homogeneous(sig_u, sig_c, 450.0)
    assert _rel(f, 0.8118, 1e-3), "%.4f" % f
    # what the stray 6.206 would give
    stray = thermal_utilization_homogeneous(6.206, 0.003421, 450.0)
    assert _rel(stray, 0.8012, 1e-3)
    assert not _rel(stray, 0.8118, 5e-3)
    # 235U supplies 64% of natural uranium's absorption despite being 0.72% of it
    share = NATURAL_U["235U"] * FUEL_THERMAL_AVERAGED["235U"]["sigma_a"] / sig_u
    assert _rel(share, 0.643, 1e-2)


def test_reproduces_example_10_2_and_eta_of_natural_uranium():
    """S&F Ex. 10.2: eta = 1.738 for 2 atom-% enriched uranium.

    Natural uranium gives 1.338 -- the value Tables 10.5 and 10.8 use, and the
    number the whole subject turns on: above 1, so a chain reaction is possible;
    far below 2, so thermal breeding is not."""
    assert _rel(eta_of_uranium(0.02), 1.738, 1e-3), "%.4f" % eta_of_uranium(0.02)
    nat = eta_of_uranium(0.007204)
    assert _rel(nat, 1.338, 2e-3), "%.4f" % nat
    # eta rises monotonically with enrichment and saturates at pure 235U
    prev = 0.0
    for e in (0.007204, 0.02, 0.05, 0.20, 0.90, 1.0):
        v = eta_of_uranium(e)
        assert v > prev
        prev = v
    pure = thermal_fission_factor(FUEL_THERMAL_AVERAGED["235U"]["nu"],
                                  FUEL_THERMAL_AVERAGED["235U"]["sigma_f"],
                                  FUEL_THERMAL_AVERAGED["235U"]["sigma_a"])
    assert _rel(eta_of_uranium(1.0), pure, 1e-12)
    assert _rel(pure, 2.080, 1e-3)
    # 233U is the only thermal breeder candidate: eta > 2 with margin
    assert FUEL_PROPERTIES["233U"][5] > 2.29
    assert FUEL_PROPERTIES["239Pu"][5] < FUEL_PROPERTIES["233U"][5]
    for bad in (0.0, 1.5, -0.1):
        try:
            eta_of_uranium(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("enrichment %r should be rejected" % bad)


def test_reproduces_examples_10_7_and_10_8():
    """S&F Ex. 10.7-10.8: natural uranium in water at N_W/N_U = 1.70 gives
    eps = 1.0513 and p = 0.7270."""
    n238_over_nw = 0.992745 / 1.70
    assert _rel(n238_over_nw, 0.5840, 1e-3)
    eps = fast_fission_factor(n238_over_nw)
    assert _rel(eps, 1.0513, 1e-3), "%.4f" % eps
    p = resonance_escape_homogeneous(n238_over_nw, "water")
    assert _rel(p, 0.7270, 1e-3), "%.4f" % p
    # a lumped rod has a larger eps at the same composition -- but only just.
    # S&F's text says the heterogeneous eps is "5-10% higher"; Eq. (10.6)'s own
    # fitted constants give at most 1.2%, over the whole range of the fit. The
    # discrepancy is recorded rather than resolved (see refs.md).
    assert fast_fission_factor(n238_over_nw, "rod") > eps
    gaps = [fast_fission_factor(x, "rod") / fast_fission_factor(x) - 1.0
            for x in (0.3, 0.584, 1.0, 2.0, 5.0, 10.0)]
    assert max(gaps) < 0.013, "%.4f" % max(gaps)
    assert not any(g > 0.05 for g in gaps)

    # eps -> (a - c) as the fuel is diluted away, which the fit puts marginally
    # BELOW 1 (0.99934). eps counts fissions ADDED and cannot be below 1, so
    # that is a 0.07% artefact of an empirical fit used outside its range.
    limit = fast_fission_factor(1e-12)
    assert _rel(limit, EPSILON_FIT["homogeneous"][0] - EPSILON_FIT["homogeneous"][2], 1e-6)
    assert 0.999 < limit < 1.0
    for r in (0.05, 0.1, 1.0, 5.0):
        assert fast_fission_factor(r) > 1.0
    # p falls as the fuel concentration rises -- the tension that sets the optimum
    ps = [resonance_escape_homogeneous(x, "water") for x in (0.05, 0.2, 0.6, 2.0)]
    assert ps == sorted(ps, reverse=True)
    for bad in ((-1.0,), (1.0, "spherical")):
        try:
            fast_fission_factor(*bad)
        except (ValueError, KeyError):
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_resonance_integral_rises_as_the_absorber_is_diluted():
    """Eq. (10.8): I ~ (Sigma_sM/N_A)^c with c = 0.486 for 238U.

    A counter-intuitive but real effect: dilute the absorber and each of its
    atoms becomes MORE effective, because more scattering per absorber atom
    carries a neutron across each resonance faster and out of danger.  It is the
    same self-shielding that Eq. (10.19)'s 1/sqrt(r rho) expresses for a rod."""
    dense = resonance_integral_homogeneous(44.8, 0.02)
    dilute = resonance_integral_homogeneous(44.8, 0.002)
    assert dilute > dense
    assert _rel(dilute / dense, 10.0 ** 0.486, 1e-9)
    # thorium's integral is SMALLER than uranium's and far less
    # dilution-sensitive (c = 0.253 against 0.486), so a thorium lattice loses
    # much less to resonance capture and gains much less from being lumped
    th = resonance_integral_homogeneous(44.8, 0.02, "232Th")
    assert th < dense
    th_dilute = resonance_integral_homogeneous(44.8, 0.002, "232Th")
    assert (th_dilute / th) < (dilute / dense)
    assert _rel(th_dilute / th, 10.0 ** 0.253, 1e-9)
    for bad in ((0.0, 0.02), (44.8, 0.0)):
        try:
            resonance_integral_homogeneous(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    try:
        resonance_integral_homogeneous(44.8, 0.02, "240Pu")
    except KeyError:
        pass
    else:
        raise AssertionError("an absorber with no fit should be refused")


# --- the four-factor formula, and what is missing from it ----------------

def test_the_four_factor_formula_is_missing_epsilon():
    """S&F Eq. (10.17) prints k_inf = eta p f and calls it "the four-factor
    formula".  That is three factors, and the sixth defined factor, eps, is
    absent from both Eq. (10.16) and Eq. (10.17) and from Fig. 10.3.

    The book's OWN Table 10.5 settles it.  Its water row is eps = 1.051,
    eta = 1.338, f = 0.869, p = 0.727 and k_inf = 0.888.  The product eta p f is
    0.845; eps eta p f is 0.888.  Water is the only row with eps != 1, and it is
    exactly the row that discriminates.  Table 10.8 confirms it independently."""
    ratio, eps, eta, f, p, k = OPTIMUM_RATIOS["H2O"]
    assert _rel(k_infinity(eta, p, f, eps), k, 1e-3), "%.4f" % k_infinity(eta, p, f, eps)
    assert _rel(four_factor_formula_as_printed(eta, p, f), 0.845, 1e-3)
    assert not _rel(four_factor_formula_as_printed(eta, p, f), k, 0.02)
    # every row of Table 10.5 reproduces with eps, and the three rows with
    # eps = 1 cannot distinguish the two forms
    for mod, (ratio, eps, eta, f, p, k) in OPTIMUM_RATIOS.items():
        assert _rel(k_infinity(eta, p, f, eps), k, 2e-3), mod
        if eps == 1.0:
            assert _rel(four_factor_formula_as_printed(eta, p, f), k, 2e-3)
    # Table 10.8's whole column needs eps = 1.027
    for pitch, (eps, eta, f, p, k) in LATTICE_TABLE.items():
        assert _rel(k_infinity(eta, p, f, eps), k, 2e-3), "pitch %d" % pitch
        assert not _rel(four_factor_formula_as_printed(eta, p, f), k, 1e-2)
    # eps below 1 is meaningless -- it counts fissions ADDED
    try:
        k_infinity(1.3, 0.9, 0.9, 0.95)
    except ValueError:
        pass
    else:
        raise AssertionError("eps < 1 should be refused")
    for bad in ((1.3, 1.2, 0.9), (1.3, 0.9, 1.4)):
        try:
            k_infinity(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_only_heavy_water_moderates_natural_uranium_to_criticality():
    """Table 10.5, and the single most consequential fact in the chapter: at the
    OPTIMUM moderator-to-fuel ratio, k_inf for natural uranium is

        H2O 0.888,  D2O 1.173,  Be 0.779,  C 0.781

    -- below 1 for everything but heavy water.  A homogeneous natural-uranium
    reactor is therefore impossible except with D2O, which is why enrichment
    plants exist and why the only natural-uranium power reactors are CANDUs and
    the graphite designs that LUMP their fuel (see Table 10.8)."""
    kinf = dict((m, v[5]) for m, v in OPTIMUM_RATIOS.items())
    assert kinf["D2O"] > 1.0
    for m in ("H2O", "Be", "C"):
        assert kinf[m] < 1.0, m
    assert max(kinf, key=kinf.get) == "D2O"
    # the optimum ratios span a factor of 245: water needs 1.7 molecules per
    # uranium atom, graphite 417 atoms
    ratios = dict((m, v[0]) for m, v in OPTIMUM_RATIOS.items())
    assert _rel(ratios["C"] / ratios["H2O"], 245.0, 0.02)
    # and D2O wins on p, not on f -- it is the only moderator that barely
    # absorbs, so it can be piled on until p is high without killing f
    assert OPTIMUM_RATIOS["D2O"][4] > 0.9
    assert OPTIMUM_RATIOS["D2O"][3] > OPTIMUM_RATIOS["C"][3]
    assert (MODERATOR_THERMAL["D2O"]["Sigma_a"]
            < MODERATOR_THERMAL["H2O"]["Sigma_a"] / 500)


def test_the_factors_pull_against_each_other():
    """Why an optimum exists at all: adding moderator raises p and lowers f.
    Neither is monotone in k_inf, and the product has an interior maximum."""
    sig_u = sum(a * FUEL_THERMAL_AVERAGED[k]["sigma_a"]
                for k, a in NATURAL_U.items())
    sig_c = westcott_averaged_cross_section(0.00386)
    best, best_ratio = 0.0, None
    for ratio in [50 * i for i in range(1, 40)]:
        f = thermal_utilization_homogeneous(sig_u, sig_c, ratio)
        p = resonance_escape_homogeneous(0.992745 / ratio, "graphite")
        k = k_infinity(1.338, p, f)
        if k > best:
            best, best_ratio = k, ratio
    assert 250 <= best_ratio <= 700, "optimum at N_C/N_U = %s" % best_ratio
    assert 0.7 < best < 0.85, "%.4f" % best      # still below 1, as Table 10.5 says
    # and the two factors genuinely move in opposite directions across it
    lo, hi = best_ratio // 2, best_ratio * 2
    assert (thermal_utilization_homogeneous(sig_u, sig_c, lo)
            > thermal_utilization_homogeneous(sig_u, sig_c, hi))
    assert (resonance_escape_homogeneous(0.992745 / lo, "graphite")
            < resonance_escape_homogeneous(0.992745 / hi, "graphite"))


# --- leakage and criticality ---------------------------------------------

def test_reproduces_examples_10_3_to_10_6():
    """S&F Ex. 10.3-10.6: a bare sphere of 235U in graphite, 1:35 000.

    Ex. 10.4 writes L^2 = L_C^2(1-f) = 3500(1 - 0.8143) = 570.1.  Table 10.4
    gives L_T^2 = 3070 cm2 for graphite, and 3070 x 0.1857 = 570.1 exactly, while
    3500 x 0.1857 = 650.  The printed 3500 is contradicted by the printed answer."""
    u5 = FUEL_THERMAL_AVERAGED["235U"]
    eta = thermal_fission_factor(FUEL_PROPERTIES["235U"][4], u5["sigma_f"],
                                 u5["sigma_a"])
    assert _rel(eta, 2.080, 1e-3)
    f = thermal_utilization_homogeneous(u5["sigma_a"], 0.00386, 35000.0)
    assert _rel(f, 0.8143, 1e-3)
    kinf = k_infinity(eta, 1.0, f)
    assert _rel(kinf, 1.6939, 1e-3), "%.4f" % kinf

    # the erratum: 3070 reproduces 570.1, 3500 does not
    l2 = diffusion_length_squared(MODERATOR_THERMAL["C"]["L2"], f)
    assert _rel(l2, 570.1, 2e-3), "%.2f" % l2
    assert MODERATOR_THERMAL["C"]["L2"] == 3070.0
    assert _rel(diffusion_length_squared(L2_GRAPHITE_ERRATA, f), 650.0, 2e-3)

    b2 = geometric_buckling("sphere", R=120.0)
    assert _rel(b2, 6.85e-4, 1e-3)
    tau = MODERATOR_THERMAL["C"]["tau"]
    assert _rel(fast_nonleakage(b2, tau), 0.7772, 1e-3)
    assert _rel(thermal_nonleakage(l2, b2), 0.7192, 1e-3)
    # at 120 cm the core is subcritical: k_eff < 1
    keff = k_effective(eta, 1.0, f, fast_nonleakage(b2, tau),
                       thermal_nonleakage(l2, b2))
    assert keff < 1.0 and _rel(keff, 0.947, 1e-2), "%.4f" % keff

    # Ex. 10.5: the critical radius
    r = critical_radius_sphere(kinf, l2, tau)
    assert _rel(r, 126.7, 2e-3), "%.2f cm" % r
    assert _rel(critical_buckling(kinf, l2, tau), 6.152e-4, 3e-3)
    assert _rel(k_effective(eta, 1.0, f,
                            fast_nonleakage(critical_buckling(kinf, l2, tau), tau),
                            thermal_nonleakage(l2, critical_buckling(kinf, l2, tau))),
                1.0, 1e-4)
    # Ex. 10.6: the fissile mass
    mass = (4 / 3) * math.pi * r ** 3 * 1.60 * (1 / 35000.0) * (235.0 / 12.0)
    assert _rel(mass / 1000.0, 7.62, 2e-2), "%.3f kg" % (mass / 1000.0)


def test_criticality_refuses_a_subcritical_material():
    """If k_inf <= 1 no finite core is critical, however large -- leakage only
    removes neutrons.  Returning a buckling would be meaningless, so it raises.

    This is exactly the natural-uranium-in-graphite case of Table 10.5
    (k_inf = 0.781), which is why the world's first reactor was a LATTICE."""
    for kinf in (0.781, 0.888, 1.0):
        try:
            critical_buckling(kinf, 570.0, 368.0)
        except ValueError as exc:
            assert "critical" in str(exc)
        else:
            raise AssertionError("k_inf = %g should be refused" % kinf)
    # just above 1 it answers, with a huge core
    r = critical_radius_sphere(1.01, 570.0, 368.0)
    assert r > 500.0, "%.1f cm" % r
    # and the critical size falls as k_inf rises
    radii = [critical_radius_sphere(k, 570.0, 368.0) for k in (1.05, 1.3, 1.7)]
    assert radii == sorted(radii, reverse=True)


def test_buckling_geometry_and_the_leakage_trade():
    """Table 10.10's bucklings, and the fact that leakage is a surface-to-volume
    effect: for a fixed volume the sphere has the smallest buckling, hence the
    least leakage and the smallest critical mass."""
    v = 1e6                                     # cm3
    r_sph = (3 * v / (4 * math.pi)) ** (1 / 3.0)
    a_cube = v ** (1 / 3.0)
    r_cyl = (v / (math.pi * 1.0)) ** 0.5        # H = 1 cm slab-like, extreme
    assert (geometric_buckling("sphere", R=r_sph)
            < geometric_buckling("cube", a=a_cube))
    assert geometric_buckling("cylinder", R=r_cyl, H=1.0) > geometric_buckling(
        "sphere", R=r_sph)
    assert _rel(geometric_buckling("sphere", R=120.0), (math.pi / 120) ** 2, 1e-12)
    assert _rel(geometric_buckling("cube", a=100.0), 3 * (math.pi / 100) ** 2, 1e-12)
    # both non-leakage probabilities go to 1 as the core grows
    for fn, arg in ((lambda b: thermal_nonleakage(570.0, b), None),
                    (lambda b: fast_nonleakage(b, 368.0), None)):
        assert _rel(fn(geometric_buckling("sphere", R=1e6)), 1.0, 1e-6)
        assert fn(geometric_buckling("sphere", R=50.0)) < 0.6
    assert _approx(reactivity(1.0), 0.0)
    assert _rel(reactivity(1.01), 0.00990099, 1e-6)
    try:
        geometric_buckling("torus", R=1.0)
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown geometry should be refused")


# --- the heterogeneous lattice -------------------------------------------

def test_the_lattice_series_matches_the_bessel_form():
    """Eqs. (10.24)-(10.25) are series for the exact Bessel forms of Eq. (10.22),
    and both must agree for S&F's Ex. 10.9 arguments.

    The E series' grouping matters and the printed two-dimensional layout is easy
    to misread: z^2/(z^2-y^2) multiplies ONLY the logarithm, with z^2/2 outside
    the whole bracket.  Reading the two leading fractions as a single
    z^2/(2(z^2-y^2)) prefactor gives 1.736 instead of 1.031 -- a 68% error that
    would change Ex. 10.9's f from 0.905 to 0.553."""
    y, z = 1.25 / 55.4, cell_radius(20.0) / 55.4
    x = 1.25 / 1.55
    assert _rel(lattice_F(x), 1.0792, 1e-3)
    assert _rel(lattice_F(x, series=True), lattice_F(x), 1e-5)
    e_exact, e_series = lattice_E(y, z), lattice_E(y, z, series=True)
    assert _rel(e_exact, 1.0307, 1e-3), "%.5f" % e_exact
    assert _rel(e_series, e_exact, 1e-4), "%.5f vs %.5f" % (e_series, e_exact)
    # the misreading, stated explicitly so it stays refuted
    misread = 1.0 + (z ** 2 / (2 * (z ** 2 - y ** 2))) * (
        math.log(z / y) - 0.75 + y ** 2 / (4 * z ** 2))
    assert _rel(misread, 1.7357, 1e-3)
    assert not _rel(misread, e_exact, 0.5)
    # the Bessel routines themselves, against known values
    assert _rel(bessel_i0(1.0), 1.2660658, 1e-6)
    assert _rel(bessel_i1(1.0), 0.5651591, 1e-6)
    assert _rel(bessel_k0(1.0), 0.4210244, 1e-6)
    assert _rel(bessel_k1(1.0), 0.6019072, 1e-6)
    assert _rel(bessel_i0(5.0), 27.239872, 1e-5)
    assert _rel(bessel_k1(5.0), 0.00404461, 1e-4)
    for fn in (bessel_k0, bessel_k1):
        try:
            fn(0.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject 0" % fn.__name__)
    try:
        lattice_E(0.5, 0.2)
    except ValueError:
        pass
    else:
        raise AssertionError("z <= y should be refused")


def test_reproduces_examples_10_9_and_10_10():
    """S&F Ex. 10.9-10.10: the graphite lattice with 1.25 cm natural-uranium rods
    at 20 cm pitch gives f = 0.9051 and p = 0.90028, matching Table 10.8's row.

    Ex. 10.9 prints z = b/L_M = 11.8284/55.4 = 0.20368 two lines after computing
    b = 11.284 cm.  11.284/55.4 = 0.20368; 11.8284/55.4 = 0.21351.  The stray 8
    is contradicted by the value it is claimed to produce."""
    b = cell_radius(20.0)
    assert _rel(b, 11.284, 1e-3), "%.4f" % b
    assert _rel(b / 55.4, 0.20368, 1e-3)
    assert not _rel(11.8284 / 55.4, 0.20368, 1e-2)
    vm_vf = (20.0 ** 2 - math.pi * 1.25 ** 2) / (math.pi * 1.25 ** 2)
    assert _rel(vm_vf, 80.487, 1e-4)
    f = thermal_utilization_lattice(0.000274, 0.3208, vm_vf, 1.25, b, 1.55, 55.4)
    assert _rel(f, 0.9051, 1e-3), "%.4f" % f
    assert _rel(f, LATTICE_TABLE[20][2], 2e-3)

    n_f = 19.1 * AVOGADRO / 238.0289
    assert _rel(n_f, 0.04832, 1e-3), "%.5f" % n_f
    i = resonance_integral_rod(1.25, 19.1)
    assert _rel(i, 10.6384, 1e-4), "%.4f" % i
    p = resonance_escape_lattice(n_f, 1.0 / vm_vf, i)
    assert _rel(p, 0.90028, 1e-3), "%.5f" % p
    assert _rel(p, LATTICE_TABLE[20][3], 2e-3)
    # and the whole row of Table 10.8
    k = k_infinity(LATTICE_TABLE[20][1], p, f, LATTICE_TABLE[20][0])
    assert _rel(k, 1.118, 2e-3), "%.4f" % k


def test_lumping_the_fuel_is_what_makes_natural_uranium_work():
    """The point of §10.5.  At the same fuel-to-moderator ratio, lumping raises p
    from about 0.45 to 0.90 -- because neutrons slow down in moderator containing
    no 238U at all, and only those reaching a resonance energy near a lump are in
    danger.  f falls slightly (flux depression inside the rod), and the net is
    k_inf above 1 where the homogeneous mixture is at 0.78."""
    vm_vf = (20.0 ** 2 - math.pi * 1.25 ** 2) / (math.pi * 1.25 ** 2)
    p_het = resonance_escape_lattice(19.1 * AVOGADRO / 238.0289, 1.0 / vm_vf,
                                     resonance_integral_rod(1.25, 19.1))
    p_hom = resonance_escape_homogeneous(0.992745 / vm_vf, "graphite")
    assert p_het > p_hom
    assert _rel(p_het / p_hom, 2.01, 0.05), "%.3f" % (p_het / p_hom)
    # Table 10.8's best k_inf beats Table 10.5's best homogeneous graphite value
    assert max(v[4] for v in LATTICE_TABLE.values()) > 1.0
    assert OPTIMUM_RATIOS["C"][5] < 1.0
    # and the lattice has its own optimum pitch, at 20 cm
    best = max(LATTICE_TABLE.items(), key=lambda kv: kv[1][4])
    assert best[0] == 20
    # p rises and f falls with pitch, exactly as in the homogeneous case
    pitches = sorted(LATTICE_TABLE)
    assert [LATTICE_TABLE[a][3] for a in pitches] == sorted(
        LATTICE_TABLE[a][3] for a in pitches)
    assert [LATTICE_TABLE[a][2] for a in pitches] == sorted(
        (LATTICE_TABLE[a][2] for a in pitches), reverse=True)
    # the rod resonance integral falls with radius: lumping harder helps more
    assert (resonance_integral_rod(2.5, 19.1) < resonance_integral_rod(1.25, 19.1)
            < resonance_integral_rod(0.5, 19.1))
    assert resonance_integral_rod(1.25, 19.1) > RESONANCE_ROD_CONSTANTS["238U metal"][0]


def test_table_10_3_heavy_water_scattering_cross_section():
    """Table 10.3 prints sigma_sM = 0.509 b for heavy water -- exactly its own xi
    from the adjacent column, and 20x smaller than any plausible value.

    Table 10.7 gives xi_M Sigma_sM = 0.178 cm-1 for the same material, and with
    D2O's atom density that requires sigma_sM = 10.6 b, which is also the
    accepted value.  The cross-check is trustworthy because it reproduces
    graphite to four figures and beryllium to 0.7%."""
    for mod, key, rho, mass in (("graphite", "C", 1.60, 12.011),
                                ("beryllium", "Be", 1.85, 9.0122),
                                ("heavy water", "D2O", 1.10, 20.028)):
        n = rho * AVOGADRO / mass
        implied = XI_SIGMA_S[mod] / (MODERATOR_SLOWING[mod]["xi"] * n)
        assert _rel(implied, MODERATOR_SLOWING[mod]["sigma_s"], 0.03), \
            "%s: implied %.2f b vs table %.2f b" % (mod, implied,
                                                    MODERATOR_SLOWING[mod]["sigma_s"])
    # graphite is exact to four figures, which validates the method
    n_c = 1.60 * AVOGADRO / 12.011
    assert _rel(MODERATOR_SLOWING["graphite"]["xi"] * n_c
                * MODERATOR_SLOWING["graphite"]["sigma_s"],
                XI_SIGMA_S["graphite"], 1e-3)
    # the printed heavy-water value is out by a factor of 21
    n_d = 1.10 * AVOGADRO / 20.028
    printed = MODERATOR_SLOWING["heavy water"]["xi"] * n_d * SIGMA_S_D2O_ERRATA
    assert _rel(XI_SIGMA_S["heavy water"] / printed, 20.8, 0.05)
    assert SIGMA_S_D2O_ERRATA == MODERATOR_SLOWING["heavy water"]["xi"]


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
