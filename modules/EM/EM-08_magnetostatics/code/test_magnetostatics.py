"""Tests for EM-08 magnetostatics. Reuses MA-01 (cross) and MA-02 (line_integral).

Run:  python3 test_magnetostatics.py     ->  "All N tests passed."
"""
import math

# own module first: chains MA-01/MA-02 onto sys.path
from magnetostatics import (
    MU0, lorentz_force, force_on_wire,
    biot_savart, circular_loop_field, loop_axis_field_closed,
    infinite_wire_field, ampere_circulation, div_B_residual,
)
from vector_algebra import dot, norm


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_lorentz_force_perpendicular():
    Q = 1.0
    v, B = (1e6, 0.0, 0.0), (0.0, 0.0, 0.5)
    F = lorentz_force(Q, v, B)
    assert _vapprox(F, (0.0, -Q * 1e6 * 0.5, 0.0), tol=1e-6)   # x_hat x z_hat = -y_hat
    # magnetic force does no work and is perpendicular to both v and B
    assert _approx(dot(F, v), 0.0, tol=1e-3)
    assert _approx(dot(F, B), 0.0, tol=1e-9)


def test_force_on_wire():
    I, dl, B = 3.0, (0.0, 2.0, 0.0), (0.0, 0.0, 1.0)
    F = force_on_wire(I, dl, B)                              # y_hat x z_hat = x_hat
    assert _vapprox(F, (I * 2.0, 0.0, 0.0), tol=1e-9)


def test_infinite_wire_magnitude_and_direction():
    I = 10.0
    B = infinite_wire_field(I)
    for s in (0.01, 0.05, 0.2):
        assert _approx(norm(B(s, 0, 0)), MU0 * I / (2 * math.pi * s), tol=1e-12)
    # azimuthal: at (s,0,0) the field points +y (right-hand rule about +z)
    bx, by, bz = B(0.05, 0.0, 0.0)
    assert bx == 0.0 and by > 0.0 and bz == 0.0
    # B is perpendicular to the cylindrical radial direction
    assert _approx(dot(B(0.03, 0.04, 0.1), (0.03, 0.04, 0.0)), 0.0, tol=1e-12)


def test_ampere_law_infinite_wire():
    I = 7.0
    B = infinite_wire_field(I)
    for s in (0.02, 0.1, 0.5):                              # independent of the radius
        assert _approx(ampere_circulation(B, s), MU0 * I, tol=1e-6)


def test_div_B_zero():
    B = infinite_wire_field(12.0)
    for p in ((0.04, 0.02, 0.0), (0.1, -0.05, 0.3)):
        assert abs(div_B_residual(B, p)) < 1e-4


def test_biot_savart_loop_on_axis():
    # Biot-Savart for a circular loop must match the closed-form on-axis field
    I, R = 5.0, 0.1
    B = circular_loop_field(I, R, n=3000)
    for z in (0.0, 0.05, 0.2, 0.5):
        assert _approx(B(0, 0, z)[2], loop_axis_field_closed(I, R, z), tol=1e-3)
        # on the axis the transverse components vanish by symmetry
        assert abs(B(0, 0, z)[0]) < 1e-9 and abs(B(0, 0, z)[1]) < 1e-9


def test_loop_center_field():
    # at the centre the closed form is mu0 I / (2 R)
    I, R = 4.0, 0.2
    assert _approx(loop_axis_field_closed(I, R, 0.0), MU0 * I / (2 * R), tol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
