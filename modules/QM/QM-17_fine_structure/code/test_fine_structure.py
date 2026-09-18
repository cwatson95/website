"""Tests for QM-17 fine structure, Zeeman & hyperfine.

Every claim is checked against a closed form or a measured number:
  - alpha, mu_B, the 21 cm line are rederived from CODATA constants and checked
    to the reference values;
  - the central identity  E_rel + E_so + E_Darwin == E_fs(n,j)  (relativistic +
    spin-orbit + Darwin = the (n,j)-only fine-structure formula) is verified to
    machine precision for every state, which simultaneously proves the
    l-degeneracy-breaking / j-degeneracy-preserving structure;
  - the Lande g-factors are checked against their exact rational values.

Run directly:   python3 test_fine_structure.py     (-> "All N tests passed.")
Or with pytest: pytest test_fine_structure.py
"""
import math

from fine_structure import (
    h, c, e, m_e, m_p, a0, Ry_eV,
    alpha_ref, mu_B_ref, f_21cm_ref, lambda_21cm_ref,
    fine_structure_constant, electron_rest_energy_eV, rydberg_energy_eV,
    bohr_energy_eV,
    relativistic_correction_eV, LS_coupling, spin_orbit_correction_eV,
    darwin_correction_eV, fine_structure_correction_eV, hydrogen_energy_eV,
    lande_g_factor, bohr_magneton, bohr_magneton_eV_per_T,
    zeeman_weak_field_eV, zeeman_strong_field_eV,
    spin_spin_coupling, hyperfine_splitting_eV, hyperfine_frequency,
    hyperfine_wavelength,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# every hydrogen state up to n=4 as (n, l, j); l=0 has only j=1/2
def _states(nmax=4):
    out = []
    for n in range(1, nmax + 1):
        for l in range(n):
            for j in ([0.5] if l == 0 else [l - 0.5, l + 0.5]):
                out.append((n, l, j))
    return out


# --- 1. the scale: alpha -----------------------------------------------------

def test_fine_structure_constant():
    """alpha = e^2/(4 pi eps0 hbar c) ~= 1/137.036 (Griffiths Eq.7.44)."""
    alpha = fine_structure_constant()
    assert _approx(alpha, alpha_ref, rel=1e-8)
    assert _approx(1.0 / alpha, 137.035999, rel=1e-6)   # the famous "1/137"


def test_bohr_energy_from_alpha():
    """Ry = (1/2) alpha^2 m c^2: the Rydberg is alpha^2 below the rest energy. This
    is the lever that makes fine structure (another alpha^2) ~1e-4 eV.  Rederived
    from alpha + m c^2, it matches CODATA Ry_eV to ~1e-7 (QM-01 'derive, don't
    quote')."""
    alpha = fine_structure_constant()
    Ry_built = 0.5 * alpha ** 2 * electron_rest_energy_eV()
    assert _approx(Ry_built, Ry_eV, rel=1e-6)                 # derived ~= CODATA
    assert _approx(rydberg_energy_eV(), Ry_built, rel=1e-12)  # same derivation
    assert _approx(bohr_energy_eV(1), -Ry_eV, rel=1e-6)       # E_1 = -13.6 eV


# --- 2. fine structure -------------------------------------------------------

def test_relativistic_correction_sign_and_l_dependence():
    """H'_rel always lowers the level (E_rel < 0) and depends on l, not j
    (Griffiths Eq.7.58); for fixed n it grows as l decreases (penetrating orbits
    are faster)."""
    for n in (1, 2, 3, 4):
        for l in range(n):
            assert relativistic_correction_eV(n, l) < 0.0
        # more negative for smaller l at fixed n
        for l in range(n - 1):
            assert relativistic_correction_eV(n, l) < relativistic_correction_eV(n, l + 1)


def test_LS_coupling_values():
    """<L*S> = (hbar^2/2)[j(j+1)-l(l+1)-s(s+1)] (Griffiths Eq.7.65).
    For p (l=1): p_1/2 -> -hbar^2, p_3/2 -> +hbar^2/2; the (2j+1)-weighted average
    over the doublet vanishes (center-of-gravity rule)."""
    assert _approx(LS_coupling(0.5, 1), -1.0, abs_=1e-12)          # p_1/2 = -hbar^2
    assert _approx(LS_coupling(1.5, 1), 0.5, abs_=1e-12)           # p_3/2 = +hbar^2/2
    # center of gravity: sum_j (2j+1) <L*S> = 0
    cog = 2 * LS_coupling(0.5, 1) + 4 * LS_coupling(1.5, 1)
    assert _approx(cog, 0.0, abs_=1e-12)
    # d states (l=2): d_3/2 -> -3/2 hbar^2, d_5/2 -> +1 hbar^2
    assert _approx(LS_coupling(1.5, 2), -1.5, abs_=1e-12)
    assert _approx(LS_coupling(2.5, 2), 1.0, abs_=1e-12)


def test_spin_orbit_sign_and_s_state():
    """Spin-orbit vanishes for l=0 (no orbit) and raises j=l+1/2 / lowers j=l-1/2
    (Griffiths Eq.7.67), tracking the sign of <L*S>."""
    assert spin_orbit_correction_eV(2, 0, 0.5) == 0.0     # s-states: no coupling
    for (n, l) in [(2, 1), (3, 1), (3, 2), (4, 2), (4, 3)]:
        assert spin_orbit_correction_eV(n, l, l + 0.5) > 0.0   # j=l+1/2 raised
        assert spin_orbit_correction_eV(n, l, l - 0.5) < 0.0   # j=l-1/2 lowered


def test_fine_structure_decomposition():
    """THE central identity: relativistic + spin-orbit + Darwin = the (n,j)-only
    fine-structure formula, for EVERY state (Griffiths Eq.7.68 = 7.58 + 7.67,
    with the Darwin term covering l=0).  Exact to machine precision."""
    for (n, l, j) in _states(4):
        lhs = (relativistic_correction_eV(n, l)
               + spin_orbit_correction_eV(n, l, j)
               + darwin_correction_eV(n, l))
        rhs = fine_structure_correction_eV(n, j)
        assert _approx(lhs, rhs, rel=1e-12, abs_=1e-18), (n, l, j, lhs, rhs)


def test_fine_structure_decomposition_hydrogenic():
    """The same decomposition holds for a hydrogenic ion (He+, Z=2), where every
    fine-structure piece scales as Z^4."""
    for (n, l, j) in _states(3):
        lhs = (relativistic_correction_eV(n, l, Z=2)
               + spin_orbit_correction_eV(n, l, j, Z=2)
               + darwin_correction_eV(n, l, Z=2))
        rhs = fine_structure_correction_eV(n, j, Z=2)
        assert _approx(lhs, rhs, rel=1e-12, abs_=1e-18), (n, l, j)
    # Z^4 scaling of the overall fine structure (Z=2 vs Z=1, same n,j)
    ratio = fine_structure_correction_eV(2, 1.5, Z=2) / fine_structure_correction_eV(2, 1.5, Z=1)
    assert _approx(ratio, 16.0, rel=1e-9)


def test_fine_structure_depends_only_on_n_and_j():
    """Fine structure breaks the l-degeneracy but preserves the j-degeneracy
    (Griffiths Fig.7.8): states with the same (n,j) but different l shift
    identically -- e.g. 2S_1/2 and 2P_1/2 coincide."""
    # 2S_1/2 (l=0) and 2P_1/2 (l=1) -> identical shift
    assert _approx(fine_structure_correction_eV(2, 0.5),
                   fine_structure_correction_eV(2, 0.5), rel=0)  # by construction (n,j)
    # but they are built from DIFFERENT l-decompositions that still agree:
    s_path = (relativistic_correction_eV(2, 0) + spin_orbit_correction_eV(2, 0, 0.5)
              + darwin_correction_eV(2, 0))
    p_path = (relativistic_correction_eV(2, 1) + spin_orbit_correction_eV(2, 1, 0.5)
              + darwin_correction_eV(2, 1))
    assert _approx(s_path, p_path, rel=1e-12)
    # different j at same n DO split: 2P_1/2 != 2P_3/2
    assert fine_structure_correction_eV(2, 0.5) < fine_structure_correction_eV(2, 1.5)


def test_fine_structure_magnitude_is_alpha_squared():
    """Fine structure is ~1e-4..1e-5 of the Bohr energy (O(alpha^2)), exactly the
    top of the Griffiths Table 7.1 hierarchy."""
    for (n, j) in [(1, 0.5), (2, 0.5), (2, 1.5), (3, 1.5)]:
        ratio = abs(fine_structure_correction_eV(n, j) / bohr_energy_eV(n))
        assert 1e-6 < ratio < 1e-4                       # ~1e-4..1e-5 of Bohr
    # ground-state shift is a definite fraction of alpha^2 * |E_1|
    alpha = fine_structure_constant()
    assert abs(fine_structure_correction_eV(1, 0.5)) < alpha ** 2 * Ry_eV


def test_n2_fine_structure_splitting():
    """The measured n=2 fine-structure interval 2P_3/2 - 2P_1/2: ~4.5e-5 eV,
    i.e. ~10.9 GHz (Griffiths Problem 7.21)."""
    dE = fine_structure_correction_eV(2, 1.5) - fine_structure_correction_eV(2, 0.5)
    assert _approx(dE, 4.53e-5, rel=0.02)                # eV
    f = dE * e / h
    assert _approx(f / 1e9, 10.95, rel=0.02)             # GHz (lab value ~10.97)


def test_hydrogen_energy_with_fine_structure():
    """E_nj = Bohr + fine structure (Griffiths Eq.7.69); fine structure is a tiny
    downward nudge, and within a shell larger j sits higher."""
    for (n, j) in [(2, 0.5), (2, 1.5), (3, 0.5)]:
        assert _approx(hydrogen_energy_eV(n, j),
                       bohr_energy_eV(n) + fine_structure_correction_eV(n, j), rel=1e-12)
        assert hydrogen_energy_eV(n, j) < bohr_energy_eV(n)   # fs lowers the level
    assert hydrogen_energy_eV(2, 1.5) > hydrogen_energy_eV(2, 0.5)  # j=3/2 above j=1/2


# --- 3. the Zeeman effect ----------------------------------------------------

def test_lande_g_factor_known_terms():
    """Lande g_J for standard terms (Griffiths Eq.7.78): exact rationals."""
    assert _approx(lande_g_factor(0.5, 0), 2.0, rel=1e-12)        # 2S_1/2
    assert _approx(lande_g_factor(0.5, 1), 2.0 / 3.0, rel=1e-12)  # 2P_1/2
    assert _approx(lande_g_factor(1.5, 1), 4.0 / 3.0, rel=1e-12)  # 2P_3/2
    assert _approx(lande_g_factor(2.5, 2), 6.0 / 5.0, rel=1e-12)  # 2D_5/2


def test_lande_g_factor_limits():
    """g_J -> 1 for pure orbital motion (s=0, j=l) and -> 2 for pure spin (l=0)."""
    for l in (1, 2, 3):
        assert _approx(lande_g_factor(l, l, s=0.0), 1.0, rel=1e-12)   # spinless (j=l): g=1
    for s in (0.5, 1.0, 1.5):
        assert _approx(lande_g_factor(s, 0, s=s), 2.0, rel=1e-12)     # l=0, j=s: pure spin g=2


def test_bohr_magneton():
    """mu_B = e hbar/(2 m_e) ~= 9.274e-24 J/T = 5.788e-5 eV/T (CODATA)."""
    assert _approx(bohr_magneton(), mu_B_ref, rel=1e-7)
    assert _approx(bohr_magneton_eV_per_T(), bohr_magneton() / e, rel=1e-12)  # exact conversion
    assert _approx(bohr_magneton_eV_per_T(), 5.7883818e-5, rel=1e-6)


def test_zeeman_weak_field():
    """Weak-field shift E = mu_B g_J B m_j (Griffiths Eq.7.79): linear in B and
    m_j; the ground state 2S_1/2 (g=2) splits symmetrically into +/- mu_B B."""
    muB = bohr_magneton_eV_per_T()
    # ground state, B = 1 T: m_j = +/-1/2 with g=2 -> +/- mu_B B
    assert _approx(zeeman_weak_field_eV(0.5, 0, +0.5, 1.0), +muB, rel=1e-12)
    assert _approx(zeeman_weak_field_eV(0.5, 0, -0.5, 1.0), -muB, rel=1e-12)
    # linear in B
    assert _approx(zeeman_weak_field_eV(0.5, 0, +0.5, 2.0),
                   2.0 * zeeman_weak_field_eV(0.5, 0, +0.5, 1.0), rel=1e-12)
    # 2P_1/2 (g=2/3) splits 3x more weakly than 2S_1/2 at the same m_j
    assert _approx(zeeman_weak_field_eV(0.5, 1, +0.5, 1.0),
                   (1.0 / 3.0) * zeeman_weak_field_eV(0.5, 0, +0.5, 1.0), rel=1e-12)


def test_zeeman_strong_field_paschen_back():
    """Strong-field (Paschen-Back) shift E = mu_B B (m_l + 2 m_s) (Griffiths
    Eq.7.83): set by m_l + 2 m_s, so e.g. (m_l=+1, m_s=-1/2) and (m_l=-1,
    m_s=+1/2) are degenerate (both give 0)."""
    muB = bohr_magneton_eV_per_T()
    assert _approx(zeeman_strong_field_eV(0, +0.5, 1.0), 1.0 * muB, rel=1e-12)  # 2*(1/2)=1
    # degeneracy m_l + 2 m_s: (m_l=+1,m_s=-1/2) and (m_l=-1,m_s=+1/2) both give 0
    a = zeeman_strong_field_eV(+1, -0.5, 1.0)
    b = zeeman_strong_field_eV(-1, +0.5, 1.0)
    assert _approx(a, 0.0, abs_=1e-18) and _approx(b, 0.0, abs_=1e-18)
    # linear in B
    assert _approx(zeeman_strong_field_eV(1, 0.5, 3.0),
                   3.0 * zeeman_strong_field_eV(1, 0.5, 1.0), rel=1e-12)


def test_zeeman_scale_vs_fine_structure():
    """A ~1 T field gives a Zeeman shift (~tens of micro-eV) comparable to the n=2
    fine-structure interval -- which is why the weak/strong crossover sits near
    ~1 T in hydrogen (Griffiths Problem 7.23)."""
    zeeman_1T = bohr_magneton_eV_per_T() * 1.0
    fs_n2 = abs(fine_structure_correction_eV(2, 1.5) - fine_structure_correction_eV(2, 0.5))
    assert 0.1 < zeeman_1T / fs_n2 < 10.0    # same order of magnitude


# --- 4. hyperfine & the 21 cm line -------------------------------------------

def test_spin_spin_triplet_singlet():
    """<S_p*S_e> = (hbar^2/2)[F(F+1)-3/2] (Griffiths Eq.7.96): triplet F=1 ->
    +hbar^2/4, singlet F=0 -> -3hbar^2/4; the gap is hbar^2."""
    assert _approx(spin_spin_coupling(1), 0.25, abs_=1e-12)        # triplet
    assert _approx(spin_spin_coupling(0), -0.75, abs_=1e-12)       # singlet
    assert _approx(spin_spin_coupling(1) - spin_spin_coupling(0), 1.0, abs_=1e-12)
    # center-of-gravity: 3*(triplet) + 1*(singlet) = 0
    assert _approx(3 * spin_spin_coupling(1) + 1 * spin_spin_coupling(0), 0.0, abs_=1e-12)


def test_hyperfine_splitting_energy():
    """Ground-state hyperfine gap ~5.88 micro-eV (Griffiths Eq.7.97)."""
    dE = hyperfine_splitting_eV()
    assert _approx(dE * 1e6, 5.88, rel=0.02)             # micro-eV


def test_21cm_line():
    """The 21 cm / 1420 MHz line of hydrogen (Griffiths Eq.7.98-7.99): the
    closed-form lands within ~0.1% of the measured frequency/wavelength (the tiny
    residual is QED + proton structure)."""
    f = hyperfine_frequency()
    lam = hyperfine_wavelength()
    assert _approx(f, f_21cm_ref, rel=2e-3)              # ~1420.4 MHz
    assert _approx(lam, lambda_21cm_ref, rel=2e-3)       # ~0.2111 m
    assert _approx(lam * 100.0, 21.1, rel=0.01)          # the famous "21 cm"
    assert _approx(f * lam, c, rel=1e-12)                # f * lambda = c, of course


def test_hierarchy_bohr_fine_hyperfine():
    """Griffiths Table 7.1 hierarchy: |Bohr| >> |fine structure| >> |hyperfine|,
    each step ~alpha^2 then ~m_e/m_p smaller."""
    bohr = abs(bohr_energy_eV(1))                         # ~13.6 eV
    fine = abs(fine_structure_correction_eV(1, 0.5))     # ~1.8e-4 eV
    hyper = hyperfine_splitting_eV()                      # ~5.9e-6 eV
    assert bohr > 1e4 * fine                              # Bohr >> fine (~7.5e4x)
    assert fine > 10.0 * hyper                            # fine >> hyperfine (~30x)
    # fine/Bohr is of order alpha^2; hyper/fine is of order m_e/m_p
    alpha = fine_structure_constant()
    assert 0.1 < (fine / bohr) / alpha ** 2 < 1.0        # ~alpha^2
    assert 0.5 < (hyper / fine) / (m_e / m_p) < 100.0    # ~m_e/m_p (with g_p, factors)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
