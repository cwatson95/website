"""Tests for CM-13 rigid-body dynamics. Reuses MA-01/MA-04 (imported transitively).

Run:  python3 test_rigid_body.py     ->  "All N tests passed."
"""
import math

from rigid_body import (
    inertia_tensor, principal_axes, moment_about_axis,
    angular_momentum, rotational_kinetic_energy,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


# four equal masses on the x and y axes -> I = diag(2, 2, 4) m a^2
PTS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
I4 = inertia_tensor([1.0] * 4, PTS)


def test_inertia_tensor_values():
    assert _approx(I4[0][0], 2.0) and _approx(I4[1][1], 2.0) and _approx(I4[2][2], 4.0)
    for i in range(3):
        for j in range(3):
            if i != j:
                assert _approx(I4[i][j], 0.0)                    # off-diagonals vanish (symmetric config)


def test_principal_moments():
    moments, axes = principal_axes(I4)
    assert _vapprox(moments, [2.0, 2.0, 4.0])                    # eigenvalues = principal moments
    # eigenvectors orthonormal
    for i in range(3):
        for j in range(3):
            d = sum(axes[i][k] * axes[j][k] for k in range(3))
            assert _approx(d, 1.0 if i == j else 0.0, tol=1e-8)


def test_moment_about_axis():
    assert _approx(moment_about_axis(I4, (0, 0, 1)), 4.0)        # = I_zz
    assert _approx(moment_about_axis(I4, (1, 0, 0)), 2.0)        # = I_xx
    assert _approx(moment_about_axis(I4, (2, 0, 0)), 2.0)        # axis need not be unit


def test_L_parallel_only_along_principal_axis():
    # omega along z (a principal axis) -> L parallel to omega
    L = angular_momentum(I4, (0.0, 0.0, 3.0))
    assert _vapprox(L, (0.0, 0.0, 12.0))                         # = I_zz omega
    # a principal eigenvector gives L = lambda * omega
    moments, axes = principal_axes(I4)
    for lam, v in zip(moments, axes):
        assert _vapprox(angular_momentum(I4, v), [lam * c for c in v], tol=1e-8)


def test_rotational_kinetic_energy():
    omega = (0.0, 0.0, 3.0)
    assert _approx(rotational_kinetic_energy(I4, omega), 0.5 * 4.0 * 9.0)   # 1/2 I_zz omega^2 = 18


def test_principal_moments_are_rotation_invariant():
    # rotate the whole body about z; the eigenvalues (principal moments) must not change
    def rot_z(p, phi):
        c, s = math.cos(phi), math.sin(phi)
        return (c * p[0] - s * p[1], s * p[0] + c * p[1], p[2])
    rotated = [rot_z(p, 0.7) for p in [(1, 0, 0.5), (-1, 0.3, 0), (0, 1, -0.2)]]
    base = [(1, 0, 0.5), (-1, 0.3, 0), (0, 1, -0.2)]
    m0, _ = principal_axes(inertia_tensor([1.0, 2.0, 1.5], base))
    m1, _ = principal_axes(inertia_tensor([1.0, 2.0, 1.5], rotated))
    assert _vapprox(sorted(m0), sorted(m1), tol=1e-7)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
