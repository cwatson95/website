"""
gibbs_phase_rule.py  —  Module 4.5 (Gibbs phase rule)

For a NONREACTING system at equilibrium with N components in P phases, the number of
independent intensive properties you may freely specify (the degrees of freedom, or
variance) is
    F = 2 + N - P          (Moran 8e Eq. 14.68, Sec. 14.6.2, p.913)
Moran writes N for the number of components; the classic statement is F = C - P + 2.
It follows from requiring each component's chemical potential to be equal across all
phases (Eq. 14.67).  For a single component (N=1):  F = 3 - P  (Eq. 14.69).

This is the rigorous reason a pure substance inside the vapor dome (P=2) has F=1 --
T and p are NOT independent there, so quality x is needed as the second property
(module 4.4).  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


def gibbs_phase_rule(N, P):
    """Degrees of freedom  F = 2 + N - P  (N components, P phases).
    [Moran Eq. 14.68, Sec. 14.6.2, p.913]"""
    return 2 + N - P


def single_component_dof(P):
    """Single component (N=1):  F = 3 - P. [Moran Eq. 14.69, Sec. 14.6.2, p.913]"""
    return 3 - P


def max_phases(N):
    """Maximum number of phases that can coexist (F = 0):  P_max = N + 2.
    For a pure substance (N=1) this is 3 -- the triple point. [Moran Sec. 14.6.2, p.914]"""
    return N + 2


def _demo():
    print("Module 4.5 -- Gibbs phase rule  F = 2 + N - P\n")
    cases = [
        ("water vapor",                       1, 1),
        ("liquid water",                      1, 1),
        ("water vapor + ice (two phases)",    1, 2),
        ("triple point (vapor+liq+solid)",    1, 3),
        ("liquid water + ammonia (solution)", 2, 1),
        ("ammonia-water liquid + vapor",      2, 2),
    ]
    for name, N, P in cases:
        print("  N=%d, P=%d : F = %d   (%s)" % (N, P, gibbs_phase_rule(N, P), name))
    print("\n  Single component: F = 3 - P -> one phase F=2, two phases F=1, triple point F=0.")
    print("  Max coexisting phases of a pure substance: P_max = N+2 = %d (the triple point)."
          % max_phases(1))
    print("  Why quality exists: in the vapor dome of a pure substance P=2 -> F=1, so T and p")
    print("  are dependent; a second property (x) is required (module 4.4).")


if __name__ == "__main__":
    _demo()
