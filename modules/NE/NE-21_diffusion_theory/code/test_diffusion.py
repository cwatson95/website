"""NE-21 tests -- neutron diffusion theory against Shultis & Faw §10.10,
Eqs. (10.57)-(10.80) and Table 10.10.

Run:  python3 test_diffusion.py
"""

import math

from diffusion import (
    GEOMETRIES, J0_FIRST_ZERO, EXTRAPOLATION_COEFFICIENT,
    fick_current, diffusion_coefficient, transport_mfp,
    diffusion_length, diffusion_length_squared,
    plane_source_flux, point_source_flux, diffusion_valid,
    material_buckling, geometric_buckling, critical_dimension,
    critical_flux_profile, peak_to_average, extrapolation_distance,
    extrapolated_dimension, k_effective_from_buckling,
    bessel_j0, bessel_j1, SLAB_CRITICALITY_ERRATA,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _integrate(f, lo, hi, n=20000):
    h = (hi - lo) / n
    return sum(f(lo + (i + 0.5) * h) for i in range(n)) * h


# --- Fick's law ----------------------------------------------------------

def test_ficks_law_and_the_diffusion_length():
    """J = -D dphi/dx: neutrons flow DOWN the gradient, which is the whole
    physical content of the minus sign. D = lambda_tr/3, so it is a length, and
    L = sqrt(D/Sigma_a) is the scale on which a source's flux dies away."""
    assert _approx(fick_current(0.84, 1.0), -0.84)
    assert _approx(fick_current(0.84, -1.0), 0.84)
    assert fick_current(0.84, 0.0) == 0.0
    assert _rel(diffusion_coefficient(0.4), 1.0 / 1.2, 1e-12)
    assert _rel(transport_mfp(0.4), 2.5, 1e-12)
    # graphite: the module's own D and Sigma_a recover ~NE-19's Table 10.4
    d = diffusion_coefficient(0.4)
    assert _rel(diffusion_length(d, 2.74e-4), 55.4, 0.01)
    assert _rel(diffusion_length_squared(d, 2.74e-4), 3070.0, 0.02)
    # a stronger absorber gives a shorter L: 1/sqrt(Sigma_a)
    assert _rel(diffusion_length(d, 4 * 2.74e-4) / diffusion_length(d, 2.74e-4),
                0.5, 1e-12)
    for bad in ((0.0, 1.0), (1.0, 0.0), (-1.0, 1.0)):
        try:
            diffusion_length(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_reproduces_the_plane_source_solution():
    """S&F Eq. (10.72): phi(x) = (S0 L/2D) exp(-|x|/L).

    Two checks the book does not make. The solution satisfies its own
    differential equation d2phi/dx2 = phi/L^2, and it conserves neutrons: the
    total absorption Sigma_a * integral(phi) over all x must equal S0, since in a
    non-multiplying infinite medium every source neutron is eventually absorbed."""
    s0, d, l = 1.0, 0.84, 55.4
    phi0 = plane_source_flux(s0, 0.0, d, l)
    assert _rel(phi0, s0 * l / (2 * d), 1e-12)
    # symmetry
    for x in (1.0, 30.0, 200.0):
        assert _approx(plane_source_flux(s0, x, d, l),
                       plane_source_flux(s0, -x, d, l))
    # it decays by 1/e in exactly one diffusion length
    assert _rel(plane_source_flux(s0, l, d, l) / phi0, math.exp(-1.0), 1e-12)
    # it satisfies the ODE
    h = 1e-3
    for x in (10.0, 60.0):
        second = ((plane_source_flux(s0, x + h, d, l)
                   - 2 * plane_source_flux(s0, x, d, l)
                   + plane_source_flux(s0, x - h, d, l)) / h ** 2)
        assert _rel(second, plane_source_flux(s0, x, d, l) / l ** 2, 1e-4)
    # neutron conservation: Sigma_a * int phi dx over all x = S0
    sigma_a = d / l ** 2
    total = 2 * _integrate(lambda x: plane_source_flux(s0, x, d, l), 0.0, 40 * l)
    assert _rel(sigma_a * total, s0, 1e-6), "%.6f" % (sigma_a * total)
    # and the current at the surface is S0/2, the boundary condition it was built on
    j = fick_current(d, (plane_source_flux(s0, h, d, l) - phi0) / h)
    assert _rel(j, s0 / 2.0, 1e-3)


def test_the_point_source_is_not_the_uncollided_form():
    """phi = S exp(-r/L)/(4 pi D r), beyond S&F.

    The contrast with ~NE-11's uncollided S exp(-mu r)/(4 pi r^2) is the point:
    diffusion counts the SCATTERED population too, so the geometric falloff is
    1/r and not 1/r^2, and the exponent carries L rather than the total mean free
    path. Confusing the two is the classic shielding blunder."""
    s, d, l = 1.0, 0.84, 55.4
    for r in (1.0, 10.0, 100.0):
        assert _rel(point_source_flux(s, r, d, l),
                    s * math.exp(-r / l) / (4 * math.pi * d * r), 1e-12)
    # neutron conservation again: Sigma_a * int phi 4 pi r^2 dr = S
    sigma_a = d / l ** 2
    total = _integrate(lambda r: point_source_flux(s, r, d, l) * 4 * math.pi * r ** 2,
                       1e-9, 60 * l)
    assert _rel(sigma_a * total, s, 1e-5), "%.6f" % (sigma_a * total)
    # the diffusion solution falls off far more slowly than the uncollided one
    mu = 1.0 / 2.5
    ratio_near = point_source_flux(s, 10.0, d, l) / (s * math.exp(-mu * 10.0)
                                                     / (4 * math.pi * 100.0))
    assert ratio_near > 10.0
    try:
        point_source_flux(s, 0.0, d, l)
    except ValueError:
        pass
    else:
        raise AssertionError("the r = 0 singularity should be refused")


def test_diffusion_theory_knows_where_it_fails():
    """Fick's law needs a nearly isotropic angular flux and a nearly linear
    gradient over a mean free path, and gets neither within a few transport mean
    free paths of a source, a vacuum boundary, or a control rod.

    S&F say so in §10.10.3 and give no criterion. The module carries the usual
    one and applies it, because the plane-source solution's own boundary
    condition is imposed at exactly the place it is least valid."""
    sigma_tr = 0.4                       # lambda_tr = 2.5 cm
    assert not diffusion_valid(0.0, sigma_tr)
    assert not diffusion_valid(5.0, sigma_tr)
    assert diffusion_valid(7.5, sigma_tr)
    assert diffusion_valid(100.0, sigma_tr)
    # in water (lambda_tr ~ 0.43 cm) the invalid zone is a centimetre; in
    # graphite it is 7.5 cm, which is a real fraction of a small assembly
    assert _rel(3 * transport_mfp(1.0 / 0.43), 1.29, 1e-9)
    assert _rel(3 * transport_mfp(sigma_tr), 7.5, 1e-9)
    try:
        diffusion_valid(-1.0, sigma_tr)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative distance should be rejected")


# --- criticality ---------------------------------------------------------

def test_criticality_is_material_buckling_equals_geometric_buckling():
    """S&F Eq. (10.80). The left side has only materials in it and the right side
    only geometry, and criticality is where they are equal. That factorisation is
    the reason a reactor designer can choose fuel and shape almost separately."""
    k_inf, l2 = 1.6939, 570.1
    b2 = material_buckling(k_inf, l2)
    assert _rel(b2, 1.2172e-3, 1e-3), "%.5e" % b2
    for geom, dims in (("sphere", {"R": 90.0}), ("slab", {"a": 90.0}),
                       ("infinite cylinder", {"R": 90.0})):
        r = critical_dimension(geom, k_inf, l2)
        got = geometric_buckling(geom, **{list(dims)[0]: r})
        assert _rel(got, b2, 1e-9), "%s: %.5e vs %.5e" % (geom, got, b2)
    # a finite cylinder, with the aspect ratio returned
    rr, hh = critical_dimension("cylinder", k_inf, l2)
    assert _rel(geometric_buckling("cylinder", R=rr, H=hh), b2, 1e-9)
    # material buckling is positive only above k_inf = 1
    assert material_buckling(0.9, l2) < 0
    assert _approx(material_buckling(1.0, l2), 0.0)
    for k in (0.781, 1.0):
        try:
            critical_dimension("sphere", k, l2)
        except ValueError as exc:
            assert "critical" in str(exc)
        else:
            raise AssertionError("k_inf = %g should be refused" % k)
    try:
        geometric_buckling("torus", R=1.0)
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown geometry should be refused")
    try:
        geometric_buckling("cylinder", R=1.0)
    except KeyError:
        pass
    else:
        raise AssertionError("a missing dimension should be refused")


def test_the_sphere_is_the_smallest_critical_assembly():
    """Leakage is a surface effect, so for a given material the shape with the
    least surface per volume needs the least of it. The sphere wins, and the
    ordering sphere < cylinder < cube is a theorem, not a coincidence."""
    k_inf, l2 = 1.6939, 570.1
    r = critical_dimension("sphere", k_inf, l2)
    v_sphere = 4 / 3 * math.pi * r ** 3
    a = critical_dimension("parallelepiped", k_inf, l2)
    v_cube = a ** 3
    rr, hh = critical_dimension("cylinder", k_inf, l2)
    v_cyl = math.pi * rr ** 2 * hh
    assert v_sphere < v_cyl < v_cube
    assert _rel(v_cube / v_sphere, 1.24, 0.02)
    # the optimum cylinder aspect ratio is H/R = pi sqrt(2)/2.405 = 1.847
    assert _rel(hh / rr, 1.847, 1e-3), "%.4f" % (hh / rr)
    # ...and it really is a minimum: perturbing it costs volume
    for aspect in (1.2, 1.847, 3.0):
        r2, h2 = critical_dimension("cylinder", k_inf, l2, aspect=aspect)
        v = math.pi * r2 ** 2 * h2
        assert v >= v_cyl - 1e-6, "aspect %g gives less volume" % aspect
    # a bigger k_inf needs a smaller core, as 1/sqrt(k_inf - 1)
    assert (critical_dimension("sphere", 3.0, l2)
            < critical_dimension("sphere", 1.5, l2))


def test_only_the_lowest_eigenvalue_is_physical():
    """S&F §10.10.2 rejects n > 1 because those solutions go NEGATIVE inside the
    core, and a negative neutron density is meaningless. This test states that
    numerically rather than taking it on trust.

    (Eq. (10.79) then prints the criticality condition as B_mat = n pi/a, after
    having just discarded every n > 1. Table 10.10 gives (pi/a)^2 for the slab,
    and Eq. (10.78) has already fixed n = 1.)"""
    a = 100.0
    # the fundamental mode is positive everywhere strictly inside
    for frac in (0.0, 0.1, 0.3, 0.45, 0.499):
        assert critical_flux_profile("slab", frac * a, a=a) > 0
    # every higher harmonic changes sign inside the slab
    for n in (3, 5, 7):
        values = [math.cos(n * math.pi * (i / 500.0 - 0.5)) for i in range(501)]
        assert min(values) < -0.5, "n = %d does not go negative" % n
    # and the higher modes need a larger k_inf for the same size: B grows as n
    l2 = 570.1
    b1 = (math.pi / a) ** 2
    b3 = (3 * math.pi / a) ** 2
    assert _rel(b3 / b1, 9.0, 1e-12)
    assert (1.0 + l2 * b3) > (1.0 + l2 * b1)
    assert SLAB_CRITICALITY_ERRATA == "B_mat = n pi / a"
    # Table 10.10's slab entry is the n = 1 value
    assert _rel(geometric_buckling("slab", a=a), b1, 1e-12)


def test_the_flux_shape_contains_no_material_properties():
    """Table 10.10's profiles depend only on the geometry. Two consequences:
    the peak-to-average power is a pure number, and it is large."""
    for geom, dims, pos in (("slab", {"a": 100.0}, 0.0),
                            ("sphere", {"R": 100.0}, 0.0),
                            ("infinite cylinder", {"R": 100.0}, 0.0)):
        assert _rel(critical_flux_profile(geom, pos, **dims), 1.0, 1e-6)
    # the profiles vanish at the boundary
    for geom, dims, edge in (("slab", {"a": 100.0}, 50.0),
                             ("sphere", {"R": 100.0}, 100.0),
                             ("infinite cylinder", {"R": 100.0}, 100.0)):
        assert abs(critical_flux_profile(geom, edge, **dims)) < 1e-3
    # scale invariance: the shape at a fixed fraction of the size is the same
    for f in (0.25, 0.5, 0.75):
        assert _rel(critical_flux_profile("sphere", f * 50.0, R=50.0),
                    critical_flux_profile("sphere", f * 500.0, R=500.0), 1e-9)
    # peak-to-average, checked by direct integration rather than by formula
    slab = (_integrate(lambda x: math.cos(math.pi * x), -0.5, 0.5))
    assert _rel(1.0 / slab, peak_to_average("slab"), 1e-6)
    sph = 3.0 * _integrate(lambda r: r * math.sin(math.pi * r) / math.pi, 1e-12, 1.0)
    assert _rel(1.0 / sph, peak_to_average("sphere"), 1e-5)
    cyl = 2.0 * _integrate(lambda r: r * bessel_j0(J0_FIRST_ZERO * r), 0.0, 1.0)
    assert _rel(1.0 / cyl, peak_to_average("infinite cylinder"), 1e-4)
    # the numbers themselves
    assert _rel(peak_to_average("slab"), 1.5708, 1e-4)
    assert _rel(peak_to_average("sphere"), 3.2899, 1e-4)
    assert _rel(peak_to_average("infinite cylinder"), 2.3165, 1e-3)
    assert _rel(peak_to_average("cylinder"), 3.6387, 1e-3)
    assert _rel(peak_to_average("parallelepiped"), 3.8758, 1e-4)
    # a bare cylindrical core wastes a factor of 3.6 of its own capacity
    assert peak_to_average("cylinder") > 3.5
    try:
        peak_to_average("torus")
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown geometry should be refused")


def test_bessel_j0_and_j1():
    """The module's own Bessel routines, against known values and against the
    zero that Table 10.10's cylinder entry is built on."""
    assert _rel(bessel_j0(0.0), 1.0, 1e-7)     # A&S rational fit: |err| < 5e-8
    assert _approx(bessel_j1(0.0), 0.0)
    assert _rel(bessel_j0(1.0), 0.7651977, 1e-6)
    assert _rel(bessel_j0(5.0), -0.1775968, 1e-5)
    assert _rel(bessel_j1(1.0), 0.4400506, 1e-6)
    assert _rel(bessel_j1(2.405), 0.5191147, 1e-5)
    assert _rel(bessel_j1(10.0), 0.0434727, 1e-4)
    # 2.405 really is the first zero of J0
    assert abs(bessel_j0(J0_FIRST_ZERO)) < 1e-4
    assert bessel_j0(2.0) > 0 and bessel_j0(2.8) < 0
    # J0' = -J1
    h = 1e-6
    for x in (0.5, 2.0, 4.0):
        assert _rel((bessel_j0(x + h) - bessel_j0(x - h)) / (2 * h),
                    -bessel_j1(x), 1e-4)


def test_the_extrapolation_distance_the_book_sets_to_zero():
    """S&F drop it as "generally very small compared to the size of the reactor".
    True for a metre-scale power core and false for a small assembly: d = 0.7104
    lambda_tr, which in graphite is 1.8 cm, and a 20 cm slab is then 18% larger
    than it looks -- a 28% error in the buckling and hence in k_eff."""
    assert _rel(EXTRAPOLATION_COEFFICIENT, 0.7104, 1e-4)
    sigma_tr = 0.4
    d_ext = extrapolation_distance(sigma_tr=sigma_tr)
    assert _rel(d_ext, 1.776, 1e-3)
    # the two forms agree: d = 0.7104 lambda_tr = 2.1312 D
    assert _rel(extrapolation_distance(d=diffusion_coefficient(sigma_tr)), d_ext, 1e-9)
    errors = []
    for size in (20.0, 100.0, 400.0):
        ext = extrapolated_dimension(size, sigma_tr=sigma_tr)
        errors.append(1.0 - (size / ext) ** 2)
    assert _rel(errors[0], 0.279, 0.02)
    assert _rel(errors[-1], 0.0175, 0.05)
    assert errors == sorted(errors, reverse=True)
    try:
        extrapolation_distance()
    except ValueError:
        pass
    else:
        raise AssertionError("giving neither D nor Sigma_tr should be refused")


def test_this_is_where_NE_19s_non_leakage_probability_came_from():
    """~NE-19 asserted P_NL^th = 1/(1 + L^2 B^2) [Eq. (10.13)] with a citation and
    no derivation. It is exactly the one-speed diffusion result, and the numbers
    agree: Example 10.4's 0.7192 at R = 120 cm.

    The one-speed model is nonetheless INCOMPLETE, and its own answer says so: it
    has no fast leakage term, so it puts the critical sphere of ~NE-19's material
    at 90 cm where the two-group answer is 127 cm. Neglecting the slowing-down
    distance underestimates the critical size by 30%."""
    k_inf, l2 = 1.6939, 570.1
    b2 = geometric_buckling("sphere", R=120.0)
    assert _rel(1.0 / (1.0 + l2 * b2), 0.7192, 2e-3)
    assert _rel(k_effective_from_buckling(k_inf, l2, b2), k_inf * 0.7190, 1e-3)
    # the one-speed critical radius, against ~NE-19's two-group 126.7 cm
    r1 = critical_dimension("sphere", k_inf, l2)
    assert _rel(r1, 90.0, 0.01), "%.2f cm" % r1
    assert r1 < 126.7
    assert _rel(126.7 / r1, 1.41, 0.02)
    # adding the Fermi-age term recovers the larger answer
    tau = 368.0
    lo, hi = 1e-9, 1e-2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if k_inf * math.exp(-mid * tau) / (1 + l2 * mid) > 1.0:
            lo = mid
        else:
            hi = mid
    r2 = math.pi / math.sqrt(0.5 * (lo + hi))
    assert _rel(r2, 126.7, 2e-3), "%.2f cm" % r2
    # k_eff -> k_inf as the core grows, and -> 0 as it shrinks
    assert _rel(k_effective_from_buckling(k_inf, l2, geometric_buckling(
        "sphere", R=1e6)), k_inf, 1e-6)
    assert k_effective_from_buckling(k_inf, l2, geometric_buckling(
        "sphere", R=20.0)) < 0.15


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
