"""Tests for CM-16 normal modes. Reuses MA-04 (imported transitively).

Run:  python3 test_normal_modes.py     ->  "All N tests passed."
"""
import math

from normal_modes import normal_modes, mode_inner_product


def _approx(x, y, tol=1e-7):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_two_equal_masses():
    k, m = 1.0, 1.0
    K = [[2 * k, -k], [-k, 2 * k]]
    freqs, modes = normal_modes(K, [m, m])
    assert _approx(freqs[0], math.sqrt(k / m)) and _approx(freqs[1], math.sqrt(3 * k / m))
    # low mode is in-phase (1,1), high mode out-of-phase (1,-1)
    assert _approx(abs(modes[0][0]), abs(modes[0][1]))          # equal-magnitude components
    assert _approx(modes[1][0], -modes[1][1])                   # opposite sign


def test_generalized_eigenproblem_holds():
    # K v = omega^2 M v  for unequal masses
    K = [[3.0, -1.0], [-1.0, 2.0]]
    M = [2.0, 1.0]
    freqs, modes = normal_modes(K, M)
    for w, v in zip(freqs, modes):
        Kv = [K[0][0] * v[0] + K[0][1] * v[1], K[1][0] * v[0] + K[1][1] * v[1]]
        Mv = [M[0] * v[0], M[1] * v[1]]
        for i in range(2):
            assert _approx(Kv[i], w ** 2 * Mv[i], tol=1e-7)


def test_modes_mass_orthonormal():
    K = [[3.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 3.0]]
    M = [1.0, 2.0, 1.0]
    freqs, modes = normal_modes(K, M)
    for a in range(3):
        for b in range(3):
            ip = mode_inner_product(M, modes[a], modes[b])
            assert _approx(ip, 1.0 if a == b else 0.0, tol=1e-7)   # va^T M vb = delta_ab


def test_three_mass_chain_frequencies():
    # fixed-fixed chain of 3 equal masses & springs: omega^2 = 2k/m (1 - cos(j pi/4)), j=1,2,3
    k, m = 1.0, 1.0
    K = [[2 * k, -k, 0.0], [-k, 2 * k, -k], [0.0, -k, 2 * k]]
    freqs, _ = normal_modes(K, [m, m, m])
    expected = sorted(math.sqrt(2 * k / m * (1 - math.cos(j * math.pi / 4))) for j in (1, 2, 3))
    assert all(_approx(a, b, tol=1e-7) for a, b in zip(freqs, expected))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
