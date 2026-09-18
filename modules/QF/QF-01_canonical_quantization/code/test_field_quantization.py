"""Tests for QF-01 canonical field quantization.

Run:  python3 test_field_quantization.py     ->  "All N tests passed."
Self-contained: only numpy + field_quantization (no sibling-module imports).
"""
import numpy as np

from field_quantization import (
    kg_dispersion,
    annihilation, creation, number,
    commutator, anticommutator,
    single_mode_spectrum, mode_energy,
    field_modes, vacuum_energy,
    fermion_annihilation,
)


def _basis(n, D):
    e = np.zeros(D, dtype=complex)
    e[n] = 1.0
    return e


# --- 1. Klein-Gordon dispersion -----------------------------------------------

def test_dispersion_massless_is_abs_p():
    # massless field: omega_p = |p|  (the photon light cone)
    p = np.array([0.0, 0.5, 1.0, 3.0, 10.0])
    assert np.allclose(kg_dispersion(p, 0.0), p)
    # negative component magnitude still gives |p|
    assert np.isclose(kg_dispersion(-4.0, 0.0), 4.0)


def test_dispersion_massive_formula_and_bounds():
    p = np.array([0.0, 1.0, 2.0, 5.0])
    m = 1.5
    w = kg_dispersion(p, m)
    assert np.allclose(w, np.sqrt(p ** 2 + m ** 2))
    assert np.all(w >= m - 1e-12)          # omega >= m always
    assert np.all(w >= p - 1e-12)          # omega >= |p| always
    # at p = 0 the frequency is the rest energy m
    assert np.isclose(kg_dispersion(0.0, m), m)


def test_dispersion_ultrarelativistic_limit():
    # large p: omega_p -> |p| even for a massive field
    big = 1.0e6
    assert abs(kg_dispersion(big, 1.0) - big) / big < 1e-6
    # and is monotonically increasing in p
    p = np.linspace(0, 20, 50)
    w = kg_dispersion(p, 2.0)
    assert np.all(np.diff(w) > 0)


# --- 2. one mode = one oscillator (B6) ----------------------------------------

def test_number_operator_and_ladder_action():
    D = 6
    assert np.allclose(np.diag(number(D)).real, np.arange(D))
    assert np.allclose(number(D), np.diag(np.arange(D)))
    # a+|2> = sqrt(3)|3>
    got = creation(D) @ _basis(2, D)
    assert np.isclose(got[3], np.sqrt(3.0))
    assert np.allclose(np.delete(got, 3), 0.0)
    # a|0> = 0  (the vacuum is annihilated)
    assert np.allclose(annihilation(D) @ _basis(0, D), 0.0)
    # a|3> = sqrt(3)|2>
    got = annihilation(D) @ _basis(3, D)
    assert np.isclose(got[2], np.sqrt(3.0))


def test_ladder_commutator_interior_is_identity():
    # [a, a+] = 1 on the interior; truncation puts -(D-1) in the corner; trace 0
    D = 6
    c = commutator(annihilation(D), creation(D))
    diag = np.diag(c).real
    assert np.allclose(diag[:-1], 1.0)            # interior rungs: [a,a+] = 1
    assert np.isclose(diag[-1], -(D - 1))         # corner = -(D-1) (dropped rung)
    assert abs(np.trace(c)) < 1e-9                # tr[A,B] = 0 for finite matrices
    # off-diagonal entries vanish
    assert np.allclose(c - np.diag(diag), 0.0)


def test_single_mode_spectrum_is_n_plus_half():
    # the oscillator spectrum E_n = (n + 1/2) omega  (KEY BRIDGE B6)
    D = 10
    for omega in (1.0, 0.5, 3.7):
        ev = single_mode_spectrum(D, omega=omega)
        assert np.allclose(ev, omega * (np.arange(D) + 0.5))
    # ground-state (zero-point) energy is omega/2
    assert np.isclose(single_mode_spectrum(4, omega=2.0)[0], 1.0)


def test_mode_energy_quanta():
    # E = (n + 1/2) omega_p ; n=0 is the per-mode zero-point energy
    p, m = 3.0, 4.0
    w = kg_dispersion(p, m)            # = 5.0
    assert np.isclose(w, 5.0)
    assert np.isclose(mode_energy(p, m, 0), 0.5 * w)
    assert np.isclose(mode_energy(p, m, 1), 1.5 * w)
    # adding one quantum adds exactly omega_p
    assert np.isclose(mode_energy(p, m, 3) - mode_energy(p, m, 2), w)
    # vectorized over occupation number
    ns = np.array([0, 1, 2, 5])
    assert np.allclose(mode_energy(p, m, ns), (ns + 0.5) * w)


# --- 3. vacuum energy and the UV divergence -----------------------------------

def test_vacuum_energy_matches_explicit_mode_sum():
    # E_0 = (1/2) sum omega_p over box modes (recomputed independently here)
    for Lam, m in ((1.0, 0.0), (2.0, 0.0), (3.0, 1.5)):
        mags = field_modes(Lam)
        expected = 0.5 * np.sum(np.sqrt(mags ** 2 + m ** 2))
        assert np.isclose(vacuum_energy(float(m), Lam), expected)


def test_vacuum_energy_small_cutoff_modes():
    # cutoff = 0.5 keeps only the zero mode p=0
    assert np.isclose(vacuum_energy(0.0, 0.5), 0.0)          # massless: omega=0
    assert np.isclose(vacuum_energy(2.0, 0.5), 0.5 * 2.0)    # massive: (1/2) m
    # cutoff = 1.0 adds the 6 unit-axis modes (|p|=1): E_0 = (1/2)(6*1) = 3
    assert np.isclose(vacuum_energy(0.0, 1.0), 3.0)


def test_vacuum_energy_grows_with_cutoff_divergence():
    # finite for finite cutoff, but super-linear growth ~ cutoff^4 (UV divergence)
    e2 = vacuum_energy(0.0, 2.0)
    e4 = vacuum_energy(0.0, 4.0)
    e8 = vacuum_energy(0.0, 8.0)
    assert 0.0 < e2 < e4 < e8
    assert np.isfinite(e8)
    # doubling the cutoff multiplies E_0 by much more than 2 (it scales ~cutoff^4)
    assert e4 > 4.0 * e2
    assert e8 > 4.0 * e4


def test_vacuum_energy_mass_adds_energy_and_explicit_modes():
    # a heavier field has a larger zero-point energy at fixed cutoff
    assert vacuum_energy(3.0, 4.0) > vacuum_energy(0.0, 4.0)
    # the array branch: explicit mode magnitudes, summed with the `mass` keyword
    modes = np.array([0.0, 1.0, 2.0, 9.0])       # 9.0 is above the cutoff -> dropped
    e = vacuum_energy(modes, cutoff=5.0, mass=0.0)
    assert np.isclose(e, 0.5 * (0.0 + 1.0 + 2.0))


# --- 4. spin-statistics: fermions anticommute ---------------------------------

def test_fermion_anticommutator_and_pauli():
    b = fermion_annihilation()
    bd = b.conj().T
    # {b, b+} = 1 (the 2-d identity)
    assert np.allclose(anticommutator(b, bd), np.eye(2))
    # {b, b} = 0 and (b+)^2 = 0: no two identical fermions in one mode (Pauli)
    assert np.allclose(anticommutator(b, b), 0.0)
    assert np.allclose(bd @ bd, 0.0)
    # b empties the filled state and annihilates the empty one
    assert np.allclose(b @ _basis(1, 2), _basis(0, 2))
    assert np.allclose(b @ _basis(0, 2), 0.0)


def test_boson_vs_fermion_number_eigenvalues():
    # boson mode: occupation 0,1,2,...,D-1 unbounded; fermion mode: only 0 or 1
    D = 5
    assert np.allclose(np.diag(number(D)).real, np.arange(D))
    b = fermion_annihilation()
    n_f = (b.conj().T @ b).real          # fermion number operator b+ b
    assert np.allclose(np.diag(n_f), [0.0, 1.0])


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
