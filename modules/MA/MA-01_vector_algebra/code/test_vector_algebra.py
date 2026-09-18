"""Tests for MA-01 vector algebra -- numeric, functional and symbolic.

Run directly:   python3 test_vector_algebra.py        (-> "All N tests passed.")
Or with pytest: pytest test_vector_algebra.py
"""
import math
import random

from vector_algebra import (
    dot, cross, scalar_triple, vector_triple, norm, unit, angle,
    projection, rejection, are_perpendicular, are_coplanar, box_volume,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=TOL):
    return all(_approx(ui, vi, tol) for ui, vi in zip(u, v))


def _rand_vec(rng):
    return tuple(rng.uniform(-3.0, 3.0) for _ in range(3))


def test_dot_and_cross_basic():
    x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    assert dot(x, y) == 0
    assert dot(x, x) == 1
    assert tuple(cross(x, y)) == z
    assert tuple(cross(y, x)) == tuple(-w for w in z)        # anticommutative


def test_cross_orthogonality_and_lagrange():
    rng = random.Random(0)
    for _ in range(300):
        a, b = _rand_vec(rng), _rand_vec(rng)
        axb = cross(a, b)
        assert are_perpendicular(a, axb) and are_perpendicular(b, axb)
        # Lagrange identity:  |a x b|^2 = |a|^2 |b|^2 - (a.b)^2
        assert _approx(dot(axb, axb), dot(a, a) * dot(b, b) - dot(a, b) ** 2)


def test_bac_cab():
    rng = random.Random(1)
    for _ in range(300):
        a, b, c = _rand_vec(rng), _rand_vec(rng), _rand_vec(rng)
        lhs = vector_triple(a, b, c)
        rhs = tuple(b[i] * dot(a, c) - c[i] * dot(a, b) for i in range(3))
        assert _vapprox(lhs, rhs)


def test_jacobi():
    rng = random.Random(7)
    for _ in range(300):
        a, b, c = _rand_vec(rng), _rand_vec(rng), _rand_vec(rng)
        s = tuple(vector_triple(a, b, c)[i] + vector_triple(b, c, a)[i]
                  + vector_triple(c, a, b)[i] for i in range(3))
        assert _vapprox(s, (0.0, 0.0, 0.0))


def test_scalar_triple_cyclic_and_det():
    rng = random.Random(2)
    for _ in range(300):
        a, b, c = _rand_vec(rng), _rand_vec(rng), _rand_vec(rng)
        s = scalar_triple(a, b, c)
        assert _approx(s, scalar_triple(b, c, a))            # cyclic
        assert _approx(s, scalar_triple(c, a, b))
        assert _approx(s, -scalar_triple(a, c, b))           # odd swap -> sign flip
        det = (a[0] * (b[1] * c[2] - b[2] * c[1])
               - a[1] * (b[0] * c[2] - b[2] * c[0])
               + a[2] * (b[0] * c[1] - b[1] * c[0]))
        assert _approx(s, det)                               # == 3x3 determinant


def test_coplanar_and_volume():
    a, b = (1, 0, 0), (0, 1, 0)
    assert are_coplanar(a, b, (2, 3, 0))                     # all in the xy-plane
    assert not are_coplanar(a, b, (0, 0, 1))
    assert _approx(box_volume((1, 0, 0), (0, 1, 0), (0, 0, 1)), 1.0)


def test_function_inputs():
    """The headline feature: ops accept vector-valued functions and return one."""
    r = lambda t: (math.cos(t), math.sin(t), t)              # helix
    v = lambda t: (-math.sin(t), math.cos(t), 1.0)           # r'(t)
    L = cross(r, v)                                          # function t -> r x v
    speed = norm(v)                                          # function t -> |v|
    rv = dot(r, v)                                           # function t -> r . v
    for t in (0.0, 0.5, math.pi / 2, 1.234):
        assert _vapprox(L(t), cross(r(t), v(t)))
        assert _approx(speed(t), math.sqrt(2.0))             # |v| = sqrt(1+1)
        assert _approx(rv(t), dot(r(t), v(t)))
    # mixing a constant vector with a function: pick out the z-component
    zhat = (0, 0, 1)
    z_of = dot(zhat, r)
    for t in (0.3, 2.0):
        assert _approx(z_of(t), t)


def test_projection_rejection():
    rng = random.Random(3)
    for _ in range(200):
        a, b = _rand_vec(rng), _rand_vec(rng)
        p, q = projection(a, b), rejection(a, b)
        assert _vapprox(tuple(p[i] + q[i] for i in range(3)), a)   # p + q = a
        assert are_perpendicular(q, b)                             # rejection _|_ b
        assert _approx(dot(cross(p, b), cross(p, b)), 0.0)         # projection || b


def test_unit_and_angle():
    assert _approx(norm(unit((3.0, 0.0, 4.0))), 1.0)
    assert _approx(angle((1, 0, 0), (0, 1, 0)), math.pi / 2)
    assert _approx(angle((1, 1, 0), (1, 1, 0)), 0.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
