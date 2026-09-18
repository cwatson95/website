"""Tests for CM-04 work & energy. Reuses MA-01/MA-02 (imported transitively).

Run:  python3 test_work_energy.py     ->  "All N tests passed."
"""
from work_energy import kinetic_energy, work, power


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_kinetic_energy():
    assert _approx(kinetic_energy(2.0, (3.0, 0.0, 4.0)), 25.0)         # 1/2*2*25
    assert _approx(kinetic_energy(1.0, (1.0, 1.0, 1.0)), 1.5)


def test_work_of_constant_force():
    # W = F . displacement, independent of path detail for a constant field
    F = (2.0, -1.0, 0.5)
    straight = lambda s: (5.0 * s, 5.0 * s, 5.0 * s)                   # (0,0,0)->(5,5,5)
    W = work(lambda x, y, z: F, straight, 0.0, 1.0)
    assert _approx(W, F[0] * 5 + F[1] * 5 + F[2] * 5, tol=1e-6)        # = 7.5


def test_work_energy_theorem():
    # particle from rest under constant force: W along the actual path = Delta T
    F0, m, T = 3.0, 2.0, 2.0
    a = F0 / m
    path = lambda s: (0.5 * a * s * s, 0.0, 0.0)                       # x(s), s in [0,T]
    W = work(lambda x, y, z: (F0, 0.0, 0.0), path, 0.0, T)
    vT = a * T
    assert _approx(W, kinetic_energy(m, (vT, 0, 0)) - kinetic_energy(m, (0, 0, 0)), tol=1e-4)


def test_work_of_gravity():
    # lowering m by height h releases W = m g h
    m, g, h = 3.0, 9.81, 4.0
    drop = lambda s: (0.0, 0.0, h * (1 - s))                          # z: h -> 0
    W = work(lambda x, y, z: (0.0, 0.0, -m * g), drop, 0.0, 1.0)
    assert _approx(W, m * g * h, tol=1e-5)


def test_power():
    assert _approx(power((2.0, 0.0, 0.0), (3.0, 4.0, 0.0)), 6.0)       # F . v


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
