"""Tests for RE-14 Schwarzschild black holes.

Run directly:   python3 test_schwarzschild.py     (-> "All N tests passed.")
Or with pytest: pytest test_schwarzschild.py

These are real-physics checks: the metric is a vacuum solution with a finite
horizon (the RE-11 curvature invariants confirm it); the characteristic radii
2M / 3M / 6M emerge as extrema of the effective potentials; and the closed-form
classic tests reproduce the FAMOUS numbers -- Mercury's 43"/century perihelion
precession, the Sun's 1.75" light deflection, the diverging horizon redshift --
while a from-scratch RK4 integrator reproduces the precession with no weak-field
approximation.
"""
import math

from schwarzschild import (   # importing this puts RE-11's code dir on sys.path
    schwarzschild_metric, horizon_radius, photon_sphere, isco,
    kretschmann_formula, lapse,
    effective_potential, effective_potential_massless,
    circular_orbit_radius, photon_sphere_from_potential, isco_from_potential,
    perihelion_precession, light_deflection, shapiro_delay,
    gravitational_redshift, gravitational_redshift_factor,
    apsides_to_L_E, perihelion_advance,
    M_SUN, R_SUN, A_MERCURY, E_MERCURY, T_MERCURY_DAYS, ARCSEC_PER_RAD,
)
import curvature  # RE-11 (now importable: schwarzschild added its dir to sys.path)


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- the geometry is a vacuum solution with a finite-curvature horizon (RE-11) -

def test_schwarzschild_is_vacuum_solution():
    """R_uv = 0 for r > 2M -- Schwarzschild solves the vacuum Einstein equations
    (verified via RE-11's Ricci tensor)."""
    sch = schwarzschild_metric(1.0)
    for r in (3.0, 4.0, 6.0, 10.0, 20.0):
        Ric = curvature.ricci(sch, [0.0, r, 1.2, 0.7])
        assert all(abs(Ric[i][j]) <= 1e-4 for i in range(4) for j in range(4))


def test_kretschmann_matches_formula_and_horizon_is_finite():
    """RE-11's Kretschmann scalar reproduces 48 M^2/r^6; the closed form is FINITE
    at the horizon r=2M but DIVERGES at r=0 -- the coordinate/curvature
    distinction."""
    M = 1.0
    sch = schwarzschild_metric(M)
    for r in (3.0, 4.0, 6.0, 10.0):
        K = curvature.kretschmann(sch, [0.0, r, 1.0, 0.9])
        assert _approx(K, kretschmann_formula(r, M), 1e-2)
    # finite at the horizon ...
    assert math.isfinite(kretschmann_formula(2.0 * M, M))
    assert _approx(kretschmann_formula(2.0 * M, M), 48.0 / 64.0, 1e-12)   # = 0.75/M^4
    # ... but blows up at the singularity
    assert kretschmann_formula(1e-3, M) > kretschmann_formula(2.0 * M, M) * 1e6


def test_horizon_is_coordinate_singularity():
    """The lapse f = 1-2M/r vanishes at r=2M (g_rr -> infinity) yet curvature is
    finite there: the horizon is a coordinate, not a physical, singularity."""
    for M in (1.0, 3.0):
        assert _approx(lapse(horizon_radius(M), M), 0.0, 1e-12)
        assert lapse(horizon_radius(M) + 1e-6, M) > 0.0      # outside
        assert lapse(horizon_radius(M) - 1e-6, M) < 0.0      # inside (r,t swap roles)


# --- characteristic radii and the effective potentials -----------------------

def test_characteristic_radii():
    for M in (1.0, 2.0, 5.0):
        assert _approx(horizon_radius(M), 2.0 * M, 1e-12)
        assert _approx(photon_sphere(M), 3.0 * M, 1e-12)
        assert _approx(isco(M), 6.0 * M, 1e-12)
        # ordering: horizon < photon sphere < ISCO
        assert horizon_radius(M) < photon_sphere(M) < isco(M)


def test_photon_sphere_is_maximum_of_massless_potential():
    """3M emerges as the (unstable) maximum of V_massless = (1-2M/r)L^2/r^2."""
    for M in (1.0, 4.0):
        r_ph = photon_sphere_from_potential(M)
        assert _approx(r_ph, 3.0 * M, 2e-3)
        V = lambda r: effective_potential_massless(r, 1.0, M)
        assert V(3.0 * M) > V(2.6 * M) and V(3.0 * M) > V(3.6 * M)   # a maximum


def test_isco_is_marginal_circular_orbit():
    """6M emerges as the radius where the two circular-orbit roots of V'(r)=0
    merge (L = 2 sqrt(3) M); no stable circular orbit exists inside it."""
    M = 1.0
    assert _approx(isco_from_potential(M), 6.0 * M, 2e-3)
    L_isco = 2.0 * math.sqrt(3.0) * M
    # roots merge at 6M
    assert _approx(circular_orbit_radius(L_isco, M, stable=True), 6.0 * M, 1e-3)
    assert _approx(circular_orbit_radius(L_isco, M, stable=False), 6.0 * M, 1e-3)
    # below the critical L there is NO circular orbit
    assert circular_orbit_radius(0.99 * L_isco, M) is None
    # above it, the stable (outer) and unstable (inner) orbits split apart
    r_out = circular_orbit_radius(4.0, M, stable=True)
    r_in = circular_orbit_radius(4.0, M, stable=False)
    assert r_out > 6.0 * M > r_in > 3.0 * M


def test_circular_orbit_is_potential_extremum():
    """The radius from circular_orbit_radius is a true extremum of V (V'~0)."""
    M = 1.0
    for L in (4.0, 5.0, 8.0):
        r = circular_orbit_radius(L, M, stable=True)
        h = 1e-5
        dV = (effective_potential(r + h, L, M) - effective_potential(r - h, L, M)) / (2 * h)
        assert abs(dV) <= 1e-6


def test_effective_potential_has_the_relativistic_term():
    """V(r) - [Newtonian + centrifugal] = -2 M L^2/r^3, the GR term that is absent
    from the ~CM-11 Kepler problem and drives precession/ISCO/photon sphere."""
    M, L = 1.0, 5.0
    for r in (8.0, 12.0, 30.0):
        newtonian = 1.0 - 2.0 * M / r + L * L / (r * r)
        gr_term = effective_potential(r, L, M) - newtonian
        assert _approx(gr_term, -2.0 * M * L * L / r ** 3, 1e-12)


# --- classic test 1: Mercury's perihelion precession -> 43"/century ----------

def test_mercury_perihelion_precession():
    """Feed real Mercury orbital elements and the solar mass into the closed form
    and recover the historic ~43 arcseconds per century."""
    dphi_orbit = perihelion_precession(M_SUN, A_MERCURY, E_MERCURY)   # rad/orbit
    orbits_per_century = 100.0 * 365.25 / T_MERCURY_DAYS
    arcsec_century = dphi_orbit * orbits_per_century * ARCSEC_PER_RAD
    assert _approx(arcsec_century, 43.0, 0.03)        # within 3% of the famous number
    assert 42.0 < arcsec_century < 44.0


def test_newtonian_orbit_does_not_precess():
    """With the relativistic -2ML^2/r^3 term removed, the precession formula's
    origin vanishes: 6 pi M -> 0 as M -> 0 (flat space, closed Kepler ellipse)."""
    assert perihelion_precession(0.0, A_MERCURY, E_MERCURY) == 0.0


# --- classic test 2: solar light deflection -> 1.75" -------------------------

def test_solar_light_deflection():
    """A ray grazing the Sun bends by 4M/b = 1.75" (8.49e-6 rad)."""
    defl_rad = light_deflection(M_SUN, R_SUN)
    assert _approx(defl_rad, 8.49e-6, 2e-2)               # ~8.49e-6 rad
    assert _approx(defl_rad * ARCSEC_PER_RAD, 1.75, 2e-2)  # ~1.75 arcsec
    # it is exactly twice the equivalence-principle (time-only) value 2M/b
    assert _approx(light_deflection(M_SUN, R_SUN), 2.0 * (2.0 * M_SUN / R_SUN), 1e-12)


# --- classic test 3: Shapiro delay -------------------------------------------

def test_shapiro_delay_positive_scales_and_solar_magnitude():
    """Excess delay is positive, scales linearly with M, and is ~hundreds of
    microseconds for an Earth-Venus signal grazing the Sun."""
    r_earth, r_venus = 1.496e11, 1.082e11
    dt = shapiro_delay(r_earth, r_venus, R_SUN, M_SUN)
    assert dt > 0.0
    assert _approx(shapiro_delay(r_earth, r_venus, R_SUN, 2.0 * M_SUN), 2.0 * dt, 1e-12)
    roundtrip_us = 2.0 * dt / 2.99792458e8 * 1e6          # geometrized length -> seconds
    assert 150.0 < roundtrip_us < 300.0                  # famous result ~200 us


# --- classic test 4: gravitational redshift ----------------------------------

def test_redshift_weak_field_limit():
    """For r >> M, z -> M/r_emit - M/r_obs = Delta Phi/c^2 (RE-10's gh/c^2)."""
    M = 1.0
    r_emit, r_obs = 1.0e6, 1.0e9
    z = gravitational_redshift(r_emit, r_obs, M)
    weak = M / r_emit - M / r_obs
    assert _approx(z, weak, 1e-3)
    # the solar-surface redshift is ~ M_sun/R_sun
    z_sun = gravitational_redshift(R_SUN, 1.0e30, M_SUN)
    assert _approx(z_sun, M_SUN / R_SUN, 1e-3)


def test_redshift_diverges_at_horizon():
    """As the emitter approaches the horizon, z -> infinity (the static observer's
    clock there is infinitely dilated)."""
    M = 1.0
    z1 = gravitational_redshift(2.1, 1.0e9, M)
    z2 = gravitational_redshift(2.01, 1.0e9, M)
    z3 = gravitational_redshift(2.0001, 1.0e9, M)
    assert z1 < z2 < z3                       # grows without bound
    assert z3 > 100.0
    # the factor 1+z is the ratio of static-clock rates sqrt(f_obs)/sqrt(f_emit)
    r_e, r_o = 4.0, 100.0
    factor = math.sqrt(lapse(r_o, M)) / math.sqrt(lapse(r_e, M))
    assert _approx(gravitational_redshift_factor(r_e, r_o, M), factor, 1e-12)


# --- the precessing orbit, integrated from scratch (RK4) ---------------------

def test_apsides_round_trip():
    """apsides_to_L_E gives (L,E) whose turning points (V=E^2) are exactly the
    requested perihelion and aphelion."""
    M, r_p, r_a = 1.0, 50.0, 90.0
    L, E = apsides_to_L_E(M, r_p, r_a)
    assert _approx(effective_potential(r_p, L, M), E * E, 1e-12)
    assert _approx(effective_potential(r_a, L, M), E * E, 1e-12)


def test_integrated_orbit_precesses_like_the_formula():
    """A from-scratch RK4 geodesic integration reproduces the perihelion advance:
    to <2% in the weak field, and prograde with the right magnitude in a stronger
    field -- a direct, approximation-free check of perihelion_precession."""
    M = 1.0
    # weak field: RK4 should match the leading-order closed form closely
    r_p, r_a = 500.0, 900.0
    a, e = 0.5 * (r_p + r_a), (r_a - r_p) / (r_a + r_p)
    num = perihelion_advance(M, r_p, r_a, dtau=1.0, n_steps=5_000_000)
    assert _approx(num, perihelion_precession(M, a, e), 2e-2)
    assert num > 0.0                                          # prograde (advance)
    # stronger field: still prograde, same order of magnitude (formula is leading-order)
    r_p, r_a = 50.0, 90.0
    a, e = 0.5 * (r_p + r_a), (r_a - r_p) / (r_a + r_p)
    num2 = perihelion_advance(M, r_p, r_a)
    formula2 = perihelion_precession(M, a, e)
    assert num2 > 0.0
    assert 0.8 < num2 / formula2 < 1.3                        # right order of magnitude


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
