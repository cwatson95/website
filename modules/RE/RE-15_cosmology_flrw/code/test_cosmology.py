"""Tests for RE-15 cosmology (the FLRW universe).

Run directly:   python3 test_cosmology.py        (-> "All N tests passed.")
Or with pytest: pytest test_cosmology.py

Two kinds of test.  (1) The HEADLINE -- FLRW => Friedmann -- feeds the FLRW metric
to RE-11's finite-difference Einstein tensor and recovers G_{00} = 3[(a'/a)^2 +
k/a^2]; because that goes through numerical curvature it uses a LOOSE relative
tolerance (TOL_FD).  (2) Everything else (the two Friedmann residuals, the fluid
equation, critical density / Omega, redshift) is closed-form and checked to
machine precision (TOL).  All physics is real: de Sitter, matter, radiation, the
Omega trichotomy, cosmological redshift.
"""
import math

from cosmology import (
    flrw_metric, hubble, redshift,
    friedmann_1_residual, friedmann_2_residual, fluid_equation_residual,
    critical_density, omega,
    G00_from_flrw,
    de_sitter_scale_factor, power_law_scale_factor, era_density,
)

TOL = 1e-12        # closed-form algebra
TOL_FD = 3e-2      # finite-difference curvature (G00_from_flrw): 3% relative

_EIGHT_PI = 8.0 * math.pi


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


# ----- the headline: FLRW metric => Friedmann equation, via RE-11 curvature ---

def test_flrw_implies_friedmann_de_sitter():
    """de Sitter a(t)=e^{Ht}, k=0:  G_00 = 3[(a'/a)^2 + k/a^2] = 3 H^2 (a CONSTANT,
    independent of t -- the steady exponential expansion of dark energy)."""
    for H in (0.5, 1.0, 1.5):
        a = de_sitter_scale_factor(H)
        for t in (0.0, 0.5, 1.2):                 # G_00 must be the same constant
            g00 = G00_from_flrw(a, 0, t)
            assert _approx(g00, 3.0 * H * H, TOL_FD)


def test_flrw_implies_friedmann_matter():
    """matter a(t)=t^{2/3}, k=0:  G_00 = 3 (a'/a)^2 with a' computed analytically.
    Confirms the coefficient is exactly +3 in G_00 = 3 (a'^2 + k)/a^2."""
    a = power_law_scale_factor(2.0 / 3.0)
    for t in (1.0, 1.5, 2.0):
        adot = (2.0 / 3.0) * t ** (-1.0 / 3.0)    # analytic a'
        aval = t ** (2.0 / 3.0)
        expected = 3.0 * (adot * adot + 0.0) / (aval * aval)   # 3(a'^2+k)/a^2, k=0
        assert _approx(expected, 3.0 * (2.0 / (3.0 * t)) ** 2, TOL)   # = 3(2/3t)^2
        assert _approx(G00_from_flrw(a, 0, t), expected, TOL_FD)


def test_flrw_implies_friedmann_curved():
    """Curved slices: G_00 = 3[(a'/a)^2 + k/a^2] picks up +k/a^2 (k=+1) and -1/a^2
    (k=-1) with the correct sign -- the spatial-curvature term of Friedmann I."""
    a = power_law_scale_factor(2.0 / 3.0)
    for k in (1, -1):
        for t in (2.0, 3.0):
            adot = (2.0 / 3.0) * t ** (-1.0 / 3.0)
            aval = t ** (2.0 / 3.0)
            expected = 3.0 * (adot * adot + k) / (aval * aval)
            assert _approx(G00_from_flrw(a, k, t), expected, TOL_FD)


def test_flat_static_metric_is_curvature_free():
    """a = const, k = 0 is just Minkowski in spherical spatial coordinates: no
    expansion (a'=0) and no spatial curvature, so G_00 = 3(0+0)/a^2 = 0."""
    a = lambda t: 1.0
    for t in (0.3, 1.0):
        # ~0 up to the finite-difference floor (~1e-2 at eps=1e-3); cf. the real
        # eras give G_00 ~ 0.75..3, so this is unambiguously "no curvature".
        assert abs(G00_from_flrw(a, 0, t)) <= 2e-2


# ----- the three eras satisfy BOTH Friedmann equations ------------------------

def _power_law_kinematics(power, t):
    return (t ** power,
            power * t ** (power - 1.0),
            power * (power - 1.0) * t ** (power - 2.0))


def test_three_eras_satisfy_both_friedmann():
    """Flat single-fluid eras a(t)=t^{2/(3(1+w))} with on-shell rho = 3H^2/8pi:
    matter (w=0, a~t^{2/3}), radiation (w=1/3, a~t^{1/2}) BOTH satisfy F1 and F2.
    F2 = 0 is the nontrivial check -- it pins the exponent to 2/(3(1+w))."""
    for w in (0.0, 1.0 / 3.0):
        power = 2.0 / (3.0 * (1.0 + w))
        for t in (0.7, 1.4, 2.5):
            aval, adot, addot = _power_law_kinematics(power, t)
            H = hubble(aval, adot)
            rho = critical_density(H)                  # flat on-shell density
            p = w * rho
            assert _approx(friedmann_1_residual(aval, adot, rho, 0), 0.0, 1e-9)
            assert _approx(friedmann_2_residual(aval, addot, rho, p), 0.0, 1e-9)


def test_de_sitter_satisfies_both_friedmann_two_ways():
    """de Sitter satisfies both Friedmann equations in EITHER description:
    (i) a dark-energy fluid rho = Lambda/8pi = const, p = -rho, Lambda-term off;
    (ii) pure cosmological constant rho = p = 0, Lambda = 3H^2.  Same a(t)."""
    H = 0.8
    aval, adot, addot = math.exp(H), H * math.exp(H), H * H * math.exp(H)
    # (i) fluid form: rho = Lambda/8pi = 3H^2/8pi, p = -rho
    rho = 3.0 * H * H / _EIGHT_PI
    assert _approx(friedmann_1_residual(aval, adot, rho, 0, Lambda=0.0), 0.0, 1e-12)
    assert _approx(friedmann_2_residual(aval, addot, rho, -rho, Lambda=0.0), 0.0, 1e-12)
    # (ii) geometric form: vacuum + explicit Lambda
    Lam = 3.0 * H * H
    assert _approx(friedmann_1_residual(aval, adot, 0.0, 0, Lambda=Lam), 0.0, 1e-12)
    assert _approx(friedmann_2_residual(aval, addot, 0.0, 0.0, Lambda=Lam), 0.0, 1e-12)


# ----- the fluid (continuity) equation ----------------------------------------

def test_fluid_equation_matter_and_radiation():
    """rho' = -3 H (rho + p) holds for matter (rho~a^-3) and radiation (rho~a^-4):
    rho(a) from era_density, rho' from the chain rule, residual must vanish."""
    for w in (0.0, 1.0 / 3.0):                         # matter, radiation
        for (aval, adot) in ((0.5, 0.3), (1.0, 1.0), (2.0, 0.4)):
            rho = era_density(aval, w)                 # a^{-3(1+w)}
            rhodot = -3.0 * (1.0 + w) * rho * (adot / aval)   # d/dt of the power law
            p = w * rho
            assert _approx(fluid_equation_residual(rho, rhodot, aval, adot, p), 0.0, 1e-12)


def test_era_density_scaling_matches_power_laws():
    """era_density encodes rho ~ a^{-3(1+w)}: matter a^-3, radiation a^-4, Lambda
    const.  Also: the on-shell flat density 3H^2/8pi scales the same way."""
    assert _approx(era_density(2.0, 0.0), 2.0 ** -3, TOL)        # matter ~ a^-3
    assert _approx(era_density(2.0, 1.0 / 3.0), 2.0 ** -4, TOL)  # radiation ~ a^-4
    assert _approx(era_density(2.0, -1.0), 1.0, TOL)             # Lambda const
    # critical density of a flat matter universe scales as a^-3 along the solution
    p = 2.0 / 3.0
    a1, ad1, _ = _power_law_kinematics(p, 1.0)
    a2, ad2, _ = _power_law_kinematics(p, 3.0)
    rho1, rho2 = critical_density(hubble(a1, ad1)), critical_density(hubble(a2, ad2))
    assert _approx(rho1 / rho2, (a2 / a1) ** 3, 1e-9)            # rho ~ a^-3


# ----- critical density and the Omega trichotomy ------------------------------

def test_critical_density_and_omega_unity():
    """rho_c = 3H^2/8pi and Omega = rho/rho_c, so Omega = 1 EXACTLY when rho = rho_c."""
    for H in (0.5, 1.0, 70.0):
        rc = critical_density(H)
        assert _approx(rc, 3.0 * H * H / _EIGHT_PI, TOL)
        assert _approx(omega(rc, H), 1.0, TOL)                  # rho_c <-> Omega=1
        assert _approx(omega(2.0 * rc, H), 2.0, TOL)            # linear in rho


def test_omega_trichotomy_matches_curvature_sign():
    """Flat <=> Omega=1; closed (k=+1) <=> Omega>1; open (k=-1) <=> Omega<1.
    Check on-shell: from Friedmann I, rho = 3H^2/8pi (1 + k/(a H)^2), so the sign of
    Omega-1 equals the sign of k."""
    H, a = 1.0, 1.0
    adot = H * a
    for k, want in ((0, 1.0), (1, "gt"), (-1, "lt")):
        rho = (3.0 * H * H / _EIGHT_PI) * (1.0 + k / (a * a * H * H))   # on-shell rho
        # this rho + this k must solve Friedmann I (Lambda=0):
        assert _approx(friedmann_1_residual(a, adot, rho, k), 0.0, TOL)
        Om = omega(rho, H)
        if want == 1.0:
            assert _approx(Om, 1.0, TOL)                        # flat
        elif want == "gt":
            assert Om > 1.0                                     # closed
        else:
            assert Om < 1.0                                     # open


# ----- kinematics: Hubble and redshift ----------------------------------------

def test_hubble_rate():
    assert _approx(hubble(2.0, 1.0), 0.5, TOL)
    assert _approx(hubble(math.e, math.e), 1.0, TOL)            # de Sitter H=a'/a


def test_redshift_value_and_monotonic():
    """a_emit=0.5 -> z=1; smaller a_emit (earlier emission) -> larger z; a_emit=a_obs
    -> z=0.  Also 1+z = a_obs/a_emit."""
    assert _approx(redshift(0.5), 1.0, TOL)                     # the canonical check
    assert _approx(redshift(1.0), 0.0, TOL)                     # here and now
    assert _approx(redshift(0.25), 3.0, TOL)
    assert _approx(redshift(0.5, a_obs=2.0), 3.0, TOL)          # a_obs/a_emit - 1
    zs = [redshift(ae) for ae in (0.8, 0.5, 0.2, 0.05)]         # decreasing a_emit
    assert all(zs[i] < zs[i + 1] for i in range(len(zs) - 1))   # monotonic increase


# ----- the FLRW metric itself -------------------------------------------------

def test_flrw_metric_structure():
    """Mostly-plus FLRW metric: g_tt=-1, diagonal, spatial block = a^2 times the
    constant-curvature 3-metric; reduces to Minkowski (spherical) when a=1,k=0."""
    a = de_sitter_scale_factor(0.5)
    g = flrw_metric(a, 1)
    t, r, th, ph = 0.7, 0.3, 1.1, 2.0
    G = g([t, r, th, ph])
    av = math.exp(0.5 * t)
    assert _approx(G[0][0], -1.0, TOL)                          # -dt^2
    assert _approx(G[1][1], av * av / (1.0 - 1 * r * r), TOL)   # a^2/(1-k r^2)
    assert _approx(G[2][2], av * av * r * r, TOL)               # a^2 r^2
    assert _approx(G[3][3], av * av * r * r * math.sin(th) ** 2, TOL)
    for i in range(4):                                          # diagonal
        for j in range(4):
            if i != j:
                assert G[i][j] == 0.0
    # a=1, k=0 -> Minkowski in spherical spatial coordinates
    flat = flrw_metric(lambda tt: 1.0, 0)([t, r, th, ph])
    assert _approx(flat[1][1], 1.0, TOL) and _approx(flat[2][2], r * r, TOL)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
