"""Tests for RE-16 gravitational waves.

Run directly:   python3 test_gravitational_waves.py     (-> "All N tests passed.")
Or with pytest: pytest test_gravitational_waves.py

Property-based, real-physics checks (G = c = 1, mostly-plus eta):
  * the TT plane wave is transverse and traceless;
  * box h = 0 exactly when omega = |k|  (=> gravitational waves travel at c);
  * a ring of free particles: h_+ stretches x while squeezing y by equal
    fractions, h_x does the same along the 45-deg diagonals, and the area is
    preserved to linear order (traceless);
  * h_+ and h_x are independent, trace-orthogonal polarizations;
  * the chirp mass is symmetric and scales correctly;
  * f_GW = 2 f_orbital (Kepler), and a spherically symmetric source has zero
    quadrupole and therefore radiates zero power (no monopole/dipole waves).
"""
import math
import random

from gravitational_waves import (
    ETA, POL_PLUS, POL_CROSS, polarization_tensors,
    tt_wave, is_transverse_traceless,
    dispersion_omega, wave_equation_residual,
    unit_ring, ring_response, polygon_area, area_change,
    chirp_mass, orbital_frequency, gw_frequency,
    reduced_quadrupole, quadrupole_luminosity, chirp_rate, CHIRP_RATE_CONST,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- 1. the TT wave is transverse and traceless -------------------------------

def test_tt_wave_is_transverse_traceless():
    """For any amplitudes, frequency, and spacetime point, tt_wave is in the TT
    gauge: spatial-traceless, with the time and z (propagation) rows/cols zero."""
    rng = random.Random(0)
    for _ in range(400):
        hp = rng.uniform(-0.3, 0.3)
        hx = rng.uniform(-0.3, 0.3)
        w = rng.uniform(0.1, 5.0)
        t = rng.uniform(-10.0, 10.0)
        z = rng.uniform(-10.0, 10.0)
        h = tt_wave(hp, hx, w, t, z)
        assert is_transverse_traceless(h)
        # explicit structure: only the (x,y) block is populated, symmetric, traceless
        assert _approx(h[1][1], -h[2][2])            # h_xx = -h_yy
        assert _approx(h[1][2], h[2][1])             # symmetric
        assert all(_approx(h[0][mu], 0.0) and _approx(h[3][mu], 0.0)
                   for mu in range(4))               # transverse + TT
    # a tensor with a spatial trace or a longitudinal component is NOT TT
    bad_trace = [[0.0] * 4 for _ in range(4)]
    bad_trace[1][1] = 0.1                            # h_xx without h_yy = -h_xx
    assert not is_transverse_traceless(bad_trace)
    bad_long = tt_wave(0.1, 0.05, 1.0, 0.0, 0.0)
    bad_long[3][3] = 0.1                             # a z-z (longitudinal) piece
    assert not is_transverse_traceless(bad_long)


# --- 2. the wave equation: speed c <=> omega = |k| ----------------------------

def test_wave_equation_holds_iff_omega_equals_k():
    """box h = (omega^2 - k^2) h, so the plane wave solves box h = 0 exactly on
    the light cone omega = |k|, and fails off it.  This IS 'waves travel at c'."""
    rng = random.Random(1)
    for _ in range(300):
        k = rng.uniform(0.2, 4.0)
        hp = rng.uniform(-0.2, 0.2)
        hx = rng.uniform(-0.2, 0.2)
        # on-shell: omega = dispersion_omega(k) = |k|  -> residual is ~ 0
        w_on = dispersion_omega(k)
        assert _approx(w_on, k)
        for t in (0.0, 0.3, 1.7):
            for z in (0.0, -0.9, 2.1):
                assert wave_equation_residual(hp, hx, w_on, k, t, z) <= 1e-12
        # off-shell: omega != |k|  -> residual is nonzero (unless amplitude is 0)
        if abs(hp) > 1e-3 or abs(hx) > 1e-3:
            w_off = k * rng.uniform(1.2, 2.0)
            assert wave_equation_residual(hp, hx, w_off, k, 0.0, 0.0) > 1e-6


def test_dispersion_is_lightlike():
    """omega = |k| for a scalar or a 3-vector wavevector: phase speed = c = 1."""
    assert _approx(dispersion_omega(2.5), 2.5)
    assert _approx(dispersion_omega([0.0, 0.0, 3.0]), 3.0)
    assert _approx(dispersion_omega([1.0, 2.0, 2.0]), 3.0)          # sqrt(1+4+4)
    k = [0.6, -0.8, 0.0]
    assert _approx(dispersion_omega(k) / math.sqrt(sum(c * c for c in k)), 1.0)


# --- 3. effect on a ring of free particles ------------------------------------

def test_plus_stretches_x_squeezes_y_equally():
    """At phase 0, h_+ stretches x by +h_+/2 and squeezes y by -h_+/2 (equal and
    opposite fractions) -- and couples no shear into the off-diagonal directions."""
    hp = 0.1
    ex, ey = (1.0, 0.0), (0.0, 1.0)
    (xx, xy), (yx, yy) = ring_response(hp, 0.0, 0.0, [ex, ey])
    assert _approx(xx, 1.0 + hp / 2.0) and _approx(xy, 0.0)         # x -> (1+h/2, 0)
    assert _approx(yy, 1.0 - hp / 2.0) and _approx(yx, 0.0)         # y -> (0, 1-h/2)
    # equal and opposite fractional strains
    assert _approx((xx - 1.0), -(yy - 1.0))
    # the deformation reverses half a period later (phase = pi): stretch <-> squeeze
    (xx2, _), (_, yy2) = ring_response(hp, 0.0, math.pi, [ex, ey])
    assert _approx(xx2, 1.0 - hp / 2.0) and _approx(yy2, 1.0 + hp / 2.0)


def test_cross_acts_along_the_diagonals():
    """h_x is h_+ rotated 45 deg: at phase 0 its principal axes are the diagonals
    (1,1)/sqrt2 and (1,-1)/sqrt2, stretched/squeezed by +/- h_x/2."""
    hx = 0.1
    s = 1.0 / math.sqrt(2.0)
    diag_p, diag_m = (s, s), (s, -s)
    dp, dm = ring_response(0.0, hx, 0.0, [diag_p, diag_m])
    # the (1,1) diagonal lengthens by factor 1 + h_x/2, the (1,-1) diagonal shrinks
    assert _approx(math.hypot(*dp), 1.0 + hx / 2.0)
    assert _approx(math.hypot(*dm), 1.0 - hx / 2.0)
    # ... while along the coordinate axes a pure h_x is pure shear (x gains y)
    (ax, ay), = ring_response(0.0, hx, 0.0, [(1.0, 0.0)])
    assert _approx(ax, 1.0) and _approx(ay, hx / 2.0)


def test_area_is_preserved_to_linear_order():
    """The TT perturbation is traceless, so a ring's area is unchanged to first
    order; the exact change is -1/4 (h_+^2 + h_x^2) cos^2(phase) = O(h^2)."""
    rng = random.Random(2)
    for _ in range(200):
        hp = rng.uniform(-0.1, 0.1)
        hx = rng.uniform(-0.1, 0.1)
        phase = rng.uniform(0.0, 2.0 * math.pi)
        ac = area_change(hp, hx, phase)
        predicted = -0.25 * (hp * hp + hx * hx) * math.cos(phase) ** 2
        assert _approx(ac, predicted, 1e-9)                        # exact O(h^2)
        # second order: |area change| << the linear strain ~ |h|
        amp = max(abs(hp), abs(hx))
        if amp > 1e-3:
            assert abs(ac) <= amp * amp                            # truly O(h^2)
            assert abs(ac) < 0.5 * amp                             # << linear strain


def test_polarizations_independent_and_orthogonal():
    """h_+ and h_x are independent (responses superpose) and trace-orthogonal
    polarizations; a pure h_+ produces no off-diagonal (diagonal-axis) shear."""
    e_plus, e_cross = polarization_tensors()
    # trace-orthogonal, each of squared Frobenius norm 2
    ip = sum(e_plus[i][j] * e_cross[i][j] for i in range(3) for j in range(3))
    assert _approx(ip, 0.0)
    assert _approx(sum(e_plus[i][j] ** 2 for i in range(3) for j in range(3)), 2.0)
    assert _approx(sum(e_cross[i][j] ** 2 for i in range(3) for j in range(3)), 2.0)
    # pure h_+ leaves the diagonal directions as pure (un-sheared) eigen-axes:
    # a point on the x-axis acquires NO y-displacement (no cross coupling)
    (_, ay), = ring_response(0.3, 0.0, 0.0, [(1.0, 0.0)])
    assert _approx(ay, 0.0)
    # independence: response(h_+, h_x) = response(h_+,0) + response(0,h_x) - xi
    rng = random.Random(3)
    for _ in range(100):
        hp, hx = rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2)
        ph = rng.uniform(0.0, 6.28)
        pt = [(rng.uniform(-1, 1), rng.uniform(-1, 1))]
        (bx, by), = ring_response(hp, hx, ph, pt)
        (px, py), = ring_response(hp, 0.0, ph, pt)
        (cx, cy), = ring_response(0.0, hx, ph, pt)
        assert _approx(bx, px + cx - pt[0][0])
        assert _approx(by, py + cy - pt[0][1])


# --- 4. generation: chirp mass, frequency, quadrupole luminosity --------------

def test_chirp_mass_symmetry_and_scaling():
    """M_c = (m1 m2)^(3/5)/(m1+m2)^(1/5): symmetric, equal-mass -> m/2^(1/5),
    and homogeneous of degree 1 (scaling both masses by s scales M_c by s)."""
    rng = random.Random(4)
    for _ in range(300):
        m1 = rng.uniform(0.5, 50.0)
        m2 = rng.uniform(0.5, 50.0)
        assert _approx(chirp_mass(m1, m2), chirp_mass(m2, m1))       # symmetric
        s = rng.uniform(0.5, 3.0)
        assert _approx(chirp_mass(s * m1, s * m2), s * chirp_mass(m1, m2))
    # equal masses: M_c = m / 2^(1/5)
    for m in (1.0, 10.0, 30.0):
        assert _approx(chirp_mass(m, m), m / 2.0 ** 0.2)
    # the chirp mass lies between the (smaller) reduced mass scale and total mass
    m1, m2 = 36.0, 29.0
    assert chirp_mass(m1, m2) < m1 + m2


def test_gw_frequency_is_twice_orbital():
    """f_GW = 2 f_orbital, with f_orbital the Kepler frequency omega^2 = M/r^3."""
    rng = random.Random(5)
    for _ in range(300):
        m1 = rng.uniform(1.0, 40.0)
        m2 = rng.uniform(1.0, 40.0)
        r = rng.uniform(10.0, 200.0)
        f_orb = orbital_frequency(m1, m2, r)
        assert _approx(gw_frequency(m1, m2, r), 2.0 * f_orb)         # f_GW = 2 f_orb
        # Kepler's third law: omega_orb^2 r^3 = M
        omega_orb = 2.0 * math.pi * f_orb
        assert _approx(omega_orb ** 2 * r ** 3, m1 + m2)


def test_spherical_source_has_zero_quadrupole_and_zero_luminosity():
    """No monopole/dipole radiation: a spherically symmetric mass distribution
    has a vanishing trace-free quadrupole, hence radiates zero power."""
    # six equal masses at +-x, +-y, +-z (an octahedron) -- spherically symmetric
    R = 1.7
    shell = [(2.0, R, 0, 0), (2.0, -R, 0, 0),
             (2.0, 0, R, 0), (2.0, 0, -R, 0),
             (2.0, 0, 0, R), (2.0, 0, 0, -R)]
    Q = reduced_quadrupole(shell)
    assert all(abs(Q[i][j]) <= 1e-12 for i in range(3) for j in range(3))
    assert quadrupole_luminosity(Q) <= 1e-24           # silent (no GW)
    # a single point mass on a sphere is dipolar, not quadrupole-free; but a
    # genuinely aspherical source (a bar along x) DOES have a quadrupole
    bar = [(1.0, 2.0, 0, 0), (1.0, -2.0, 0, 0)]
    Qbar = reduced_quadrupole(bar)
    assert max(abs(Qbar[i][j]) for i in range(3) for j in range(3)) > 0.1
    # luminosity is the trace-free-quadrupole norm: positive for any nonzero Q3dot
    Q3 = [[1.0, 0.5, 0.0], [0.5, -1.0, 0.0], [0.0, 0.0, 0.0]]
    assert _approx(quadrupole_luminosity(Q3),
                   0.2 * (1.0 + 0.25 + 0.25 + 1.0))


def test_reduced_quadrupole_is_trace_free():
    """Qbar_ij is trace-free by construction (the trace is the radiation-silent
    monopole), for any mass distribution."""
    rng = random.Random(6)
    for _ in range(200):
        pts = [(rng.uniform(0.1, 5.0), rng.uniform(-2, 2),
                rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(5)]
        Q = reduced_quadrupole(pts)
        assert _approx(Q[0][0] + Q[1][1] + Q[2][2], 0.0)            # trace = 0
        assert all(_approx(Q[i][j], Q[j][i]) for i in range(3) for j in range(3))


def test_chirp_rate_powers_and_constant():
    """df/dt = (96/5) pi^(8/3) M_c^(5/3) f^(11/3): check the constant and the
    scaling exponents (11/3 in f, 5/3 in M_c) that define the inspiral chirp."""
    assert _approx(CHIRP_RATE_CONST, (96.0 / 5.0) * math.pi ** (8.0 / 3.0))
    f0, Mc0 = 0.01, 25.0
    base = chirp_rate(f0, Mc0)
    # f -> 2 f multiplies df/dt by 2^(11/3); M_c -> 2 M_c by 2^(5/3)
    assert _approx(chirp_rate(2.0 * f0, Mc0) / base, 2.0 ** (11.0 / 3.0))
    assert _approx(chirp_rate(f0, 2.0 * Mc0) / base, 2.0 ** (5.0 / 3.0))
    # frequency sweeps UP (df/dt > 0) for any physical binary
    assert base > 0.0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
