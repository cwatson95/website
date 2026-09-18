"""
CM-07  Centre of mass -- the CM of a system of particles, its velocity, and the
reduced mass of a two-body problem.

Part of the physics topic network (modules/topic_network.txt, module CM-07).
Pure vector arithmetic; feeds ~CM-08 (collisions in the CM frame) and ~CM-11
(two-body -> one-body via the reduced mass). Pure stdlib.
"""

__all__ = [
    "centre_of_mass", "cm_velocity", "reduced_mass",
    "relative_coordinate", "two_body_decompose",
]


def _weighted(masses, vectors):
    M = sum(masses)
    out = [0.0, 0.0, 0.0]
    for m, x in zip(masses, vectors):
        for i in range(3):
            out[i] += m * x[i]
    return [c / M for c in out]


def centre_of_mass(masses, positions):
    """R = (sum_i m_i r_i) / (sum_i m_i)."""
    return _weighted(masses, positions)


def cm_velocity(masses, velocities):
    """V = (sum_i m_i v_i) / (sum_i m_i)  (the velocity of the CM)."""
    return _weighted(masses, velocities)


def reduced_mass(m1, m2):
    """mu = m1 m2 / (m1 + m2)  -- the effective mass of the two-body relative motion."""
    return m1 * m2 / (m1 + m2)


def relative_coordinate(r1, r2):
    """The relative position  r = r1 - r2."""
    return [r1[i] - r2[i] for i in range(3)]


def two_body_decompose(m1, m2, r1, r2):
    """Split a two-body configuration into the CM position R and relative vector r
    (the coordinates in which the problem separates -- see ~CM-11)."""
    return centre_of_mass([m1, m2], [r1, r2]), relative_coordinate(r1, r2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-07 centre of mass -- demo")
    print("=" * 32)
    print("CM of equal masses at (0,0,0),(2,0,0):", centre_of_mass([1, 1], [[0, 0, 0], [2, 0, 0]]))
    print("CM of m=[3,1] at (0,0,0),(4,0,0):", centre_of_mass([3, 1], [[0, 0, 0], [4, 0, 0]]), "(pulled toward heavy one)")
    print("reduced mass mu(2,2):", reduced_mass(2.0, 2.0), " (= m/2)")
    print("reduced mass mu(1,1e9):", round(reduced_mass(1.0, 1e9), 6), " (-> lighter mass)")
    R, r = two_body_decompose(3.0, 1.0, [0, 0, 0], [4, 0, 0])
    print("two-body decompose: R =", R, " r_rel =", r)


if __name__ == "__main__":
    _demo()
