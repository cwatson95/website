"""NE-04 tests -- Q-values against Shultis & Faw §§4.4-4.8 and Appendix B.

Run:  python3 test_q_values.py
"""

from q_values import (
    M_N_U, M_H_U, M_E_U, U_MEV,
    load_atomic_masses, atomic_mass, has_nuclide,
    parse_nuclide, parse_reaction, format_nuclide, species_mass_u, species_ZA,
    q_value, q_value_reaction, is_exothermic, check_conservation,
    q_from_binding_energies, q_value_excited,
    threshold_energy_naive, coulomb_barrier_mev,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


TAB = load_atomic_masses()


# --- notation ----------------------------------------------------------------

def test_nuclide_parsing_and_formatting():
    assert parse_nuclide("235U") == (235, 92)
    assert parse_nuclide("4He") == (4, 2)
    assert parse_nuclide("U-238") == (238, 92)
    assert parse_nuclide("Fe56") == (56, 26)
    assert format_nuclide(4, 2) == "4He"
    assert format_nuclide(235, 92) == "235U"
    for bad in ("Xx12", "hello", "12"):
        try:
            parse_nuclide(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should not parse" % bad)


def test_particle_shorthands_map_to_neutral_atoms():
    """S&F's rule (printed p. 92): charged particles are replaced by their
    neutral-atom counterparts so the electrons cancel."""
    assert species_ZA("p") == (1, 1)          # proton -> 1H
    assert species_ZA("a") == (4, 2)          # alpha  -> 4He
    assert species_ZA("d") == (2, 1)
    assert species_ZA("t") == (3, 1)
    assert species_ZA("n") == (1, 0)
    assert species_ZA("g") is None            # gamma is massless
    assert _approx(species_mass_u("g"), 0.0)
    assert _approx(species_mass_u("p", TAB), M_H_U, tol=1e-9)
    assert _approx(species_mass_u("n", TAB), M_N_U)
    assert _approx(species_mass_u("a", TAB), atomic_mass(4, 2, TAB))


def test_reaction_parsing():
    assert parse_reaction("9Be(a,n)12C") == (["9Be", "a"], ["n", "12C"])
    assert parse_reaction("16O(n, p)16N") == (["16O", "n"], ["p", "16N"])
    for bad in ("9Be a n 12C", "9Be(a)12C"):
        try:
            parse_reaction(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should not parse" % bad)


# --- conservation  [§4.7] ----------------------------------------------------

def test_conservation_check():
    assert check_conservation(["9Be", "a"], ["n", "12C"]) == (0, 0)
    assert check_conservation(["16O", "n"], ["p", "16N"]) == (0, 0)
    # a gamma carries no A or Z
    assert check_conservation(["2H", "p"], ["3He", "g"]) == (0, 0)
    # nucleon number violated
    assert check_conservation(["9Be", "a"], ["n", "11C"]) != (0, 0)
    try:
        q_value(["9Be", "a"], ["n", "11C"], TAB)
    except ValueError:
        pass
    else:
        raise AssertionError("non-conserving reaction should be rejected")


# --- the book's worked examples ---------------------------------------------

def test_example_4_4_exothermic_and_endothermic():
    """S&F Example 4.4 (printed p. 92): 9Be(a,n)12C and 16O(n,a)13C."""
    q1 = q_value_reaction("9Be(a,n)12C", TAB)
    q2 = q_value_reaction("16O(n,a)13C", TAB)
    assert _approx(q1, 5.7011, tol=1e-3)
    assert _approx(q2, -2.2156, tol=1e-3)
    assert is_exothermic(["9Be", "a"], ["n", "12C"], TAB)
    assert not is_exothermic(["16O", "n"], ["a", "13C"], TAB)
    # cross-check against the book's own tabulated mass sums
    assert _approx(atomic_mass(9, 4, TAB) + atomic_mass(4, 2, TAB), 13.014785, tol=1e-6)
    assert _approx(atomic_mass(12, 6, TAB) + M_N_U, 13.008664, tol=1e-6)


def test_charge_conservation_trap():
    """Printed p. 92: for 16O(n,p)16N the number of bound electrons is not
    conserved unless the proton is written as a 1H atom.  Getting it wrong
    shifts Q by exactly one electron mass, 0.511 MeV."""
    right = q_value(["n", "16O"], ["16N", "p"], TAB)
    wrong = (M_N_U + atomic_mass(16, 8, TAB)
             - atomic_mass(16, 7, TAB) - (M_H_U - M_E_U)) * U_MEV
    assert _approx(right, -9.6381, tol=1e-3)
    assert _approx(wrong - right, M_E_U * U_MEV, tol=1e-6)
    assert _approx(M_E_U * U_MEV, 0.51100, tol=1e-4)


def test_fusion_reactions_of_problem_5():
    """S&F Ch. 4 Prob. 5: the two deuterium fusion channels."""
    assert _approx(q_value_reaction("2H(d,n)3He", TAB), 3.2689, tol=1e-3)
    assert _approx(q_value_reaction("3H(d,n)4He", TAB), 17.5893, tol=1e-3)
    # D-T is the reaction fusion reactors chase, and it is the most energetic
    assert q_value_reaction("3H(d,n)4He", TAB) > q_value_reaction("2H(d,n)3He", TAB)


# --- structure ---------------------------------------------------------------

def test_q_from_masses_equals_q_from_binding_energies():
    """Both routes must agree exactly when nucleons are conserved."""
    for rx in ("9Be(a,n)12C", "16O(n,a)13C", "2H(d,n)3He", "3H(d,n)4He",
               "14N(n,p)14C", "6Li(n,a)3H"):
        r, p = parse_reaction(rx)
        assert _approx(q_value(r, p, TAB), q_from_binding_energies(r, p, TAB), tol=1e-6), rx


def test_q_is_antisymmetric_under_reversal():
    """Running a reaction backwards flips the sign of Q."""
    for rx in ("9Be(a,n)12C", "16O(n,a)13C"):
        r, p = parse_reaction(rx)
        assert _approx(q_value(r, p, TAB), -q_value(p, r, TAB))


def test_q_values_are_additive_along_a_chain():
    """Q depends only on the endpoints, so a two-step route must sum to the
    one-step one.  Burning three deuterons,

        2H + 2H -> 3H + p        then    2H + 3H -> 4He + n
        ------------------------------------------------------
        3 x 2H  -> 4He + n + p

    is the backbone of D-D fusion (~NE-10, ~NE-24)."""
    step1 = q_value(["2H", "2H"], ["3H", "p"], TAB)
    step2 = q_value(["2H", "3H"], ["4He", "n"], TAB)
    net = q_value(["2H", "2H", "2H"], ["4He", "n", "p"], TAB)
    assert _approx(net, step1 + step2, tol=1e-6)
    assert step1 > 0 and step2 > 0 and net > 20.0


def test_neutron_capture_q_equals_separation_energy():
    """The Q of (n,gamma) capture is the neutron separation energy of the
    product -- the link to ~NE-03 and to compound-nucleus excitation (~NE-13)."""
    for A, Z in [(56, 26), (238, 92), (16, 8)]:
        q = q_value([format_nuclide(A - 1, Z), "n"], [format_nuclide(A, Z), "g"], TAB)
        sn = ((atomic_mass(A - 1, Z, TAB) + M_N_U - atomic_mass(A, Z, TAB)) * U_MEV)
        assert _approx(q, sn, tol=1e-6)
        assert q > 0                       # capture is always exothermic


# --- excited products  [§4.8] ------------------------------------------------

def test_excited_product_reduces_q_by_the_excitation():
    """Printed p. 93: an excited nucleus is heavier by its excitation energy."""
    r, p = parse_reaction("9Be(a,n)12C")
    base = q_value(r, p, TAB)
    for ex in (0.0, 4.44, 7.65):
        assert _approx(q_value_excited(r, p, ex, TAB), base - ex, tol=1e-9)
    # a large enough excitation turns an exothermic reaction endothermic
    assert q_value_excited(r, p, 7.65, TAB) < 0
    try:
        q_value_excited(r, p, -1.0, TAB)
    except ValueError:
        pass
    else:
        raise AssertionError("negative excitation should be rejected")


# --- thresholds and barriers -------------------------------------------------

def test_naive_threshold_is_zero_for_exothermic():
    assert threshold_energy_naive(["9Be", "a"], ["n", "12C"], TAB) == 0.0
    thr = threshold_energy_naive(["16O", "n"], ["a", "13C"], TAB)
    assert _approx(thr, 2.2156, tol=1e-3)
    # this is a lower bound only -- ~NE-08 adds the recoil correction
    assert thr == -q_value(["16O", "n"], ["a", "13C"], TAB)


def test_coulomb_barrier_scales_with_charge_and_size():
    v_dt = coulomb_barrier_mev(2, 1, 3, 1)
    v_au = coulomb_barrier_mev(4, 2, 238, 92)
    assert 0.2 < v_dt < 0.6
    assert 20 < v_au < 30
    assert v_au > v_dt
    # doubling both charges quadruples the barrier at fixed size
    assert _approx(coulomb_barrier_mev(4, 2, 4, 2) / coulomb_barrier_mev(4, 1, 4, 1), 4.0)
    # neutrons feel no barrier
    assert _approx(coulomb_barrier_mev(1, 0, 238, 92), 0.0)


def test_exothermic_does_not_mean_barrierless():
    """9Be(a,n)12C releases 5.7 MeV yet still needs ~2.2 MeV to get the alpha in."""
    assert q_value_reaction("9Be(a,n)12C", TAB) > 0
    assert coulomb_barrier_mev(4, 2, 9, 4) > 2.0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
